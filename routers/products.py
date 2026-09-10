from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Form, UploadFile, File
from fastapi.responses import Response, StreamingResponse
from schemas import (
    ProductCreate, ProductResponse, ProductListResponse,
    GeMExportOptions, ONDCExportOptions,
    ExportStatusResponse, BulkProductCreateResponse, CatalogOutput
)
from services import catalog_engine
from services.price_engine import calculate_price
from services.voice_engine import voice_to_catalog
from services.image_engine import process_and_store_image
import csv
import io
import json
import uuid
import httpx
import asyncio

router = APIRouter(prefix="/products", tags=["Products & Exports"])

ALLOWED_AUDIO_TYPES = {
    "audio/webm", "audio/mp3", "audio/mpeg", "audio/wav",
    "audio/ogg", "audio/mp4", "audio/m4a", "audio/x-m4a",
    "audio/flac", "audio/x-wav", "application/octet-stream"
}

ALLOWED_IMG_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp", "application/octet-stream"}


@router.post("", response_model=ProductResponse, status_code=201)
async def create_product(payload: ProductCreate):
    try:
        record = await catalog_engine.create_product(payload.model_dump())
        return catalog_engine._row_to_response(record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/full-assembly", response_model=ProductResponse, status_code=201)
async def create_product_with_everything(
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    craft_technique: Optional[str] = Form(None),
    material_cost: Optional[float] = Form(None),
    labor_hours: Optional[float] = Form(None),
    audio_file: Optional[UploadFile] = File(None),
    image_file: Optional[UploadFile] = File(None),
):
    catalog_data: CatalogOutput | None = None

    if audio_file is not None:
        if audio_file.content_type and (
            audio_file.content_type not in ALLOWED_AUDIO_TYPES and not audio_file.content_type.startswith("audio/")
        ):
            raise HTTPException(status_code=400, detail=f"audio_file must be audio, got: {audio_file.content_type}")
        audio_bytes = await audio_file.read()
        if len(audio_bytes) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file uploaded")
        catalog_data = await voice_to_catalog(audio_bytes)

    image_url = None
    if image_file is not None:
        if image_file.content_type and (
            image_file.content_type not in ALLOWED_IMG_TYPES and not image_file.content_type.startswith("image/")
        ):
            raise HTTPException(status_code=400, detail=f"image_file must be image, got: {image_file.content_type}")
        image_bytes = await image_file.read()
        if len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="Empty image file uploaded")
        try:
            image_url = await process_and_store_image(image_bytes)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image processing failed: {e}")

    final_title = title or (catalog_data["title"] if catalog_data else None)
    final_description = description or (catalog_data["description"] if catalog_data else None)
    final_category = category or (catalog_data["category"] if catalog_data else None)
    final_craft = craft_technique or (catalog_data["craft_technique"] if catalog_data else None)

    missing = []
    if not final_title:
        missing.append("title (or audio_file)")
    if not final_description:
        missing.append("description (or audio_file)")
    if not final_category:
        missing.append("category (or audio_file)")
    if material_cost is None:
        missing.append("material_cost")
    if labor_hours is None:
        missing.append("labor_hours")
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing)}")

    try:
        record = await catalog_engine.create_product(
            {
                "title": final_title,
                "description": final_description,
                "category": final_category,
                "craft_technique": final_craft,
                "material_cost": float(material_cost),
                "labor_hours": float(labor_hours)
            },
            image_url=image_url
        )
        return catalog_engine._row_to_response(record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=ProductListResponse)
def list_products(
    page: int = Query(1, ge=1, description="Page number, 1-indexed"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page (1-100)"),
    category: Optional[str] = Query(None, description="Filter by category")
):
    items, total = catalog_engine.list_products(page=page, per_page=per_page, category=category)
    return {
        "products": [catalog_engine._row_to_response(p) for p in items],
        "total": total,
        "page": page,
        "per_page": per_page
    }


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str):
    p = catalog_engine.get_product(product_id)
    if not p:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return catalog_engine._row_to_response(p)


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: str):
    ok = catalog_engine.delete_product(product_id)
    if not ok:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return Response(status_code=204)


@router.post("/bulk", response_model=BulkProductCreateResponse, status_code=201)
async def create_products_bulk(items: List[ProductCreate]):
    if len(items) == 0:
        raise HTTPException(status_code=400, detail="At least one product is required")
    if len(items) > 500:
        raise HTTPException(status_code=400, detail="Maximum 500 products per bulk call")

    created = 0
    failed = 0
    errors: List[str] = []
    product_ids: List[str] = []

    for idx, item in enumerate(items):
        try:
            record = await catalog_engine.create_product(item.model_dump())
            product_ids.append(record["id"])
            created += 1
        except Exception as e:
            failed += 1
            errors.append(f"Row {idx+1} ({getattr(item, 'title', '?')[:30]}): {e}")

    return {
        "created": created,
        "failed": failed,
        "errors": errors,
        "product_ids": product_ids
    }


@router.post("/export/gem/csv")
async def export_gem_csv(
    opts: Optional[GeMExportOptions] = None,
    category: Optional[str] = Query(None, description="Filter products by category before export"),
    product_ids: Optional[List[str]] = Query(None, description="Specific product IDs to export")
):
    opts_dict = opts.model_dump() if opts else {}
    items: List[dict] = []

    if product_ids:
        for pid in product_ids:
            p = catalog_engine.get_product(pid)
            if p:
                items.append(p)
            else:
                raise HTTPException(status_code=404, detail=f"Product {pid} not found")
    else:
        items, _ = catalog_engine.list_products(page=1, per_page=10000, category=category)

    if len(items) == 0:
        raise HTTPException(status_code=400, detail="No products to export")

    csv_text = catalog_engine.generate_gem_csv(items, opts_dict)
    csv_bytes = csv_text.encode("utf-8-sig")
    filename = f"gem-product-export_{len(items)}-items.csv"
    return Response(
        content=csv_bytes,
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )


@router.post("/export/gem/status", response_model=ExportStatusResponse)
async def export_gem_status(
    opts: Optional[GeMExportOptions] = None,
    category: Optional[str] = Query(None),
    product_ids: Optional[List[str]] = Query(None)
):
    opts_dict = opts.model_dump() if opts else {}
    items: List[dict] = []
    if product_ids:
        for pid in product_ids:
            p = catalog_engine.get_product(pid)
            if p:
                items.append(p)
    else:
        items, _ = catalog_engine.list_products(page=1, per_page=10000, category=category)
    if len(items) == 0:
        raise HTTPException(status_code=400, detail="No products to export")
    result = await catalog_engine.export_products_gem(items, opts_dict)
    return result


@router.post("/export/ondc/json")
async def export_ondc_json(
    opts: Optional[ONDCExportOptions] = None,
    category: Optional[str] = Query(None),
    product_ids: Optional[List[str]] = Query(None)
):
    opts_dict = opts.model_dump() if opts else {}
    items: List[dict] = []
    if product_ids:
        for pid in product_ids:
            p = catalog_engine.get_product(pid)
            if p:
                items.append(p)
            else:
                raise HTTPException(status_code=404, detail=f"Product {pid} not found")
    else:
        items, _ = catalog_engine.list_products(page=1, per_page=10000, category=category)
    if len(items) == 0:
        raise HTTPException(status_code=400, detail="No products to export")

    payload = catalog_engine.generate_ondc_json(items, opts_dict)
    json_bytes = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    filename = f"ondc-catalog_{len(items)}-items.json"
    return Response(
        content=json_bytes,
        media_type="application/json",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )


@router.post("/export/ondc/status", response_model=ExportStatusResponse)
async def export_ondc_status(
    opts: Optional[ONDCExportOptions] = None,
    category: Optional[str] = Query(None),
    product_ids: Optional[List[str]] = Query(None)
):
    opts_dict = opts.model_dump() if opts else {}
    items: List[dict] = []
    if product_ids:
        for pid in product_ids:
            p = catalog_engine.get_product(pid)
            if p:
                items.append(p)
    else:
        items, _ = catalog_engine.list_products(page=1, per_page=10000, category=category)
    if len(items) == 0:
        raise HTTPException(status_code=400, detail="No products to export")
    result = await catalog_engine.export_products_ondc(items, opts_dict)
    return result


@router.get("/export/formats")
async def list_export_formats():
    return {
        "formats": [
            {
                "id": "gem_csv",
                "name": "GeM (Government e-Marketplace) Bulk Upload CSV",
                "description": "Comma-separated values format matching the GeM seller portal's bulk product upload template. Includes SKU, HSN, MRP, offer price, discount, seller GSTIN, country of origin, Make-in-India fields, category, craft technique, and URLs for images/audio.",
                "columns": 24,
                "encoding": "UTF-8 BOM (Excel-compatible)",
                "endpoints": [
                    "POST /products/export/gem/csv          -> CSV file download",
                    "POST /products/export/gem/status       -> JSON status + Supabase download URL"
                ]
            },
            {
                "id": "ondc_json",
                "name": "ONDC (Open Network for Digital Commerce) Catalog JSON",
                "description": "Beckn Protocol 2.0.0 compatible catalog payload. ONDC RET10 domain with context, BPP descriptor, provider with items array, price breakup (MRP + value + GST), item categories, HSN / asset_code / country_of_origin / make_in_india / craft_technique tags. Suitable for broadcast to ONDC buyer apps via a BPP or gateway.",
                "schemas": ["Item", "Provider", "Catalog", "BPPFulfillment", "Context"],
                "endpoints": [
                    "POST /products/export/ondc/json        -> JSON file download",
                    "POST /products/export/ondc/status      -> JSON status + Supabase download URL"
                ]
            }
        ]
    }
