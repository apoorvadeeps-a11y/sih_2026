import io
import os
import uuid
import csv
import json
import uuid
import time
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from core.supabase_client import supabase
from services.price_engine import calculate_price

PRODUCTS_TABLE = "products"
BUCKET_EXPORT = "exports"

CATEGORY_HSN = {
    "Pottery": "6913",
    "Textiles": "5811",
    "Jewelry": "7113",
    "Woodwork": "4420",
    "Metalwork": "8306",
    "Leather": "4205",
    "Basketry": "4602",
    "Stonework": "6803",
    "Glasswork": "7013",
    "Paintings": "9701",
    "Sculpture": "9703",
    "Embroidery": "5810",
    "Handmade Paper": "4802",
    "Candles & Soaps": "3401",
    "Toys & Dolls": "9503",
    "Musical Instruments": "9201",
    "Other": "9999"
}

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def _gen_sku(category: str) -> str:
    cat_prefix = "".join(c for c in category if c.isalnum())[:3].upper() or "ART"
    random_hex = uuid.uuid4().hex[:6].upper()
    return f"{cat_prefix}-{int(time.time()) % 100000:05d}-{random_hex}"

async def create_product(data: Dict[str, Any], image_url: Optional[str] = None,
                         audio_url: Optional[str] = None) -> Dict[str, Any]:
    title = data["title"].strip()
    description = data["description"].strip()
    category = data["category"].strip()
    craft_technique = (data.get("craft_technique") or "Other").strip()
    material_cost = float(data["material_cost"])
    labor_hours = float(data["labor_hours"])

    title_hi = data.get("title_hi") or None
    description_hi = data.get("description_hi") or None
    title_localized = data.get("title_localized") or None
    description_localized = data.get("description_localized") or None
    source_language = data.get("source_language") or None

    price_result = await calculate_price(material_cost, labor_hours, category,
                                         title=title, description=description,
                                         craft_technique=craft_technique,
                                         image_url=image_url)
    product_id = str(uuid.uuid4())
    sku = _gen_sku(category)
    created_at = _now_iso()

    record = {
        "id": product_id,
        "sku": sku,
        "title": title,
        "description": description,
        "title_hi": title_hi,
        "description_hi": description_hi,
        "title_localized": title_localized,
        "description_localized": description_localized,
        "source_language": source_language,
        "category": category,
        "craft_technique": craft_technique,
        "material_cost": material_cost,
        "labor_hours": labor_hours,
        "base_cost": price_result["base_cost"],
        "suggested_price": price_result["suggested_price"],
        "confidence_band": price_result["confidence_band"],
        "image_url": image_url,
        "audio_url": audio_url,
        "created_at": created_at,
        "status": "draft"
    }

    if not hasattr(create_product, "_memory_store"):
        create_product._memory_store = {}
    create_product._memory_store[product_id] = record

    if supabase is not None:
        try:
            supabase.table(PRODUCTS_TABLE).insert(record).execute()
        except Exception as db_err:
            print(f"Supabase insert failed (table/columns may not exist), data retained in-memory: {type(db_err).__name__}")

    return {
        "id": product_id,
        "sku": sku,
        "title": title,
        "description": description,
        "title_hi": title_hi,
        "description_hi": description_hi,
        "title_localized": title_localized,
        "description_localized": description_localized,
        "source_language": source_language,
        "category": category,
        "craft_technique": craft_technique,
        "material_cost": material_cost,
        "labor_hours": labor_hours,
        "base_cost": price_result["base_cost"],
        "suggested_price": price_result["suggested_price"],
        "confidence_band": price_result["confidence_band"],
        "image_url": image_url,
        "audio_url": audio_url,
        "created_at": created_at
    }

def _fetch_from_memory_store(product_id: Optional[str] = None) -> List[Dict[str, Any]]:
    store = getattr(create_product, "_memory_store", {})
    if product_id:
        return [store[product_id]] if product_id in store else []
    return list(store.values())

def list_products(page: int = 1, per_page: int = 20, category: Optional[str] = None) -> tuple[List[Dict[str, Any]], int]:
    all_products: List[Dict[str, Any]] = []
    seen_ids: set = set()

    try:
        if supabase is not None:
            query = supabase.table(PRODUCTS_TABLE).select("*")
            if category:
                query = query.eq("category", category)
            res = query.order("created_at", desc=True).execute()
            for row in (res.data or []):
                pid = row.get("id")
                if pid and pid not in seen_ids:
                    all_products.append(row)
                    seen_ids.add(pid)
    except Exception as db_err:
        print(f"Supabase list failed, merging with memory: {type(db_err).__name__}")

    for row in _fetch_from_memory_store():
        pid = row.get("id")
        if pid and pid not in seen_ids:
            all_products.append(row)
            seen_ids.add(pid)

    if category:
        all_products = [p for p in all_products if p.get("category") == category]
    all_products.sort(key=lambda p: p.get("created_at", ""), reverse=True)

    total = len(all_products)
    start = (page - 1) * per_page
    end = start + per_page
    return all_products[start:end], total

def get_product(product_id: str) -> Optional[Dict[str, Any]]:
    db_result = None
    try:
        if supabase is not None:
            res = supabase.table(PRODUCTS_TABLE).select("*").eq("id", product_id).execute()
            if res.data and len(res.data) > 0:
                db_result = res.data[0]
    except Exception as db_err:
        print(f"Supabase get failed, falling back to memory: {type(db_err).__name__}")
    if db_result is not None:
        return db_result
    memory = _fetch_from_memory_store(product_id)
    return memory[0] if memory else None

def delete_product(product_id: str) -> bool:
    deleted = False
    try:
        if supabase is not None:
            res = supabase.table(PRODUCTS_TABLE).delete().eq("id", product_id).execute()
            deleted = True
    except Exception as db_err:
        print(f"Supabase delete failed, cleaning memory only: {type(db_err).__name__}")
    store = getattr(create_product, "_memory_store", None)
    if store and product_id in store:
        del store[product_id]
        deleted = True
    return deleted

def _row_to_response(p: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": p.get("id"),
        "sku": p.get("sku"),
        "title": p.get("title"),
        "description": p.get("description"),
        "title_hi": p.get("title_hi"),
        "description_hi": p.get("description_hi"),
        "title_localized": p.get("title_localized"),
        "description_localized": p.get("description_localized"),
        "source_language": p.get("source_language"),
        "category": p.get("category"),
        "craft_technique": p.get("craft_technique") or "Other",
        "material_cost": float(p.get("material_cost", 0)),
        "labor_hours": float(p.get("labor_hours", 0)),
        "base_cost": float(p.get("base_cost", 0)),
        "suggested_price": float(p.get("suggested_price", 0)),
        "image_url": p.get("image_url"),
        "audio_url": p.get("audio_url"),
        "created_at": p.get("created_at")
    }


def _get_hsn(category: str, hsn_override: Optional[str]) -> str:
    if hsn_override:
        return hsn_override
    cat = category.strip()
    if cat in CATEGORY_HSN:
        return CATEGORY_HSN[cat]
    for k, v in CATEGORY_HSN.items():
        if k.lower() == cat.lower():
            return v
    return CATEGORY_HSN["Other"]

def generate_gem_csv(products: List[Dict[str, Any]], opts: Dict[str, Any]) -> str:
    buf = io.StringIO(newline="")
    header = [
        "S.No", "Product Code (SKU)", "Product Name", "Product Name (Hindi)", "Model", "Brand",
        "Category", "Product Description", "Product Description (Hindi)", "Craft Technique",
        "Source Language", "Material Cost (INR)",
        "Labor Hours", "Base Cost (INR)", "MRP (INR)", "Offer / Selling Price (INR)",
        "Discount %", "Unit of Measure", "Minimum Order Qty", "HSN Code",
        "Country of Origin", "Local Content %", "GSTIN of Seller",
        "Primary Image URL", "Audio / Demo URL", "Data Confidence", "Status"
    ]
    writer = csv.writer(buf, quoting=csv.QUOTE_MINIMAL, lineterminator="\r\n")
    writer.writerow(header)

    seller_gstin = opts.get("seller_gstin", "27AABCU9603R1ZZ")
    brand_name = opts.get("brand_name", "ArtisanDirect")
    country_of_origin = opts.get("country_of_origin", "India")
    local_content_pct = opts.get("local_content_pct", 100)
    hsn_override = opts.get("hsn_code")
    min_order_qty = opts.get("min_order_qty", 1)
    uom = opts.get("unit_of_measure", "Piece")

    for idx, p in enumerate(products, start=1):
        suggested = float(p.get("suggested_price", 0))
        mrp = round(suggested * 1.25, 2)
        discount_pct = round(((mrp - suggested) / mrp) * 100, 1) if mrp > 0 else 0
        writer.writerow([
            idx,
            p.get("sku", ""),
            p.get("title", ""),
            p.get("title_hi") or "",
            p.get("sku", ""),
            brand_name,
            p.get("category", ""),
            (p.get("description", "") or "").replace("\n", " "),
            ((p.get("description_hi") or "") or "").replace("\n", " "),
            p.get("craft_technique", "") or "Other",
            p.get("source_language") or "",
            p.get("material_cost", ""),
            p.get("labor_hours", ""),
            p.get("base_cost", ""),
            mrp,
            suggested,
            discount_pct,
            uom,
            min_order_qty,
            _get_hsn(p.get("category", "") or "", hsn_override),
            country_of_origin,
            local_content_pct,
            seller_gstin,
            p.get("image_url", "") or "",
            p.get("audio_url", "") or "",
            p.get("confidence_band", "") or "Medium",
            "ACTIVE"
        ])

    return buf.getvalue()

def generate_ondc_json(products: List[Dict[str, Any]], opts: Dict[str, Any]) -> Dict[str, Any]:
    seller_name = opts.get("seller_name", "Artisan Direct")
    seller_gstin = opts.get("seller_gstin", "27AABCU9603R1ZZ")
    pincode = opts.get("fulfillment_pincode", "110001")
    delivery_days = opts.get("delivery_days", 7)
    currency = opts.get("currency", "INR")
    gst_pct = float(opts.get("gst_pct", 12.0))
    country_of_origin = opts.get("country_of_origin", "IND")

    items = []
    for p in products:
        suggested = float(p.get("suggested_price", 0))
        mrp = round(suggested * 1.25, 2)
        category = (p.get("category") or "Other").strip()
        hsn = _get_hsn(category, None)
        keywords = list(filter(None, [
            category,
            (p.get("craft_technique") or "").strip(),
            "handcrafted",
            "artisan",
            "indian",
            "make in india"
        ]))
        item_id = p.get("id") or f"item_{uuid.uuid4().hex[:10]}"
        price_excl = round(suggested / (1 + gst_pct / 100), 2)
        gst_amount = round(suggested - price_excl, 2)

        title_en = (p.get("title") or "").strip()
        title_hi = (p.get("title_hi") or "").strip()
        desc_en = (p.get("description") or "").strip()
        desc_hi = (p.get("description_hi") or "").strip()
        source_lang = p.get("source_language")

        descriptor_name = title_en
        if title_hi:
            descriptor_name = f"{title_en} | {title_hi}"

        short_desc = desc_en[:140]
        if desc_hi:
            combined_short = f"{desc_en[:120]} | {desc_hi[:120]}"
            short_desc = combined_short[:280]

        items.append({
            "id": item_id,
            "parent_item_id": None,
            "descriptor": {
                "name": descriptor_name,
                "code": p.get("sku") or "",
                "short_desc": short_desc,
                "long_desc": desc_en + (f" | {desc_hi}" if desc_hi else ""),
                "images": [p.get("image_url")] if p.get("image_url") else [],
                "audio": [p.get("audio_url")] if p.get("audio_url") else [],
                "additional_descriptors": [
                    {"name": "title_en", "code": "title_en", "value": title_en},
                    {"name": "description_en", "code": "description_en", "value": desc_en},
                    {"name": "title_hi", "code": "title_hi", "value": title_hi or ""},
                    {"name": "description_hi", "code": "description_hi", "value": desc_hi or ""},
                    {"name": "source_language", "code": "source_language", "value": source_lang or ""}
                ]
            },
            "price": {
                "currency": currency,
                "value": str(suggested),
                "maximum": str(mrp),
                "breakup": [
                    {"title": "Item Value", "price": {"currency": currency, "value": str(price_excl)}},
                    {"title": f"GST @ {gst_pct}%", "price": {"currency": currency, "value": str(gst_amount)}}
                ]
            },
            "category_id": category.lower().replace(" ", "_").replace("&", "and"),
            "fulfillment_id": "STD-DELIVERY",
            "rating": None,
            "tags": [
                {"code": "country_of_origin", "list": [{"code": country_of_origin}]},
                {"code": "key_words", "list": [{"code": k} for k in keywords]},
                {"code": "asset_code", "list": [{"code": hsn}]},
                {"code": "gst_pct", "list": [{"code": str(gst_pct)}]},
                {"code": "craft_technique", "list": [{"code": (p.get("craft_technique") or "Other")}]},
                {"code": "hsn_code", "list": [{"code": hsn}]},
                {"code": "make_in_india", "list": [{"code": "YES"}]}
            ],
            "matched": True,
            "related": False,
            "recommended": False,
            "ttl": "P7D"
        })

    catalog = {
        "context": {
            "domain": "ONDC:RET10",
            "country": "IND",
            "city": "*",
            "action": "on_search",
            "core_version": "2.0.0",
            "bap_id": "buyer-app.ondc.org",
            "bap_uri": "https://buyer-app.ondc.org/",
            "bpp_id": "seller.artisandirect.in",
            "bpp_uri": "https://seller.artisandirect.in/api/ondc",
            "transaction_id": f"txn_{uuid.uuid4().hex}",
            "message_id": f"msg_{uuid.uuid4().hex}",
            "timestamp": _now_iso()
        },
        "message": {
            "catalog": {
                "bpp_descriptor": {
                    "name": seller_name,
                    "short_desc": "Authentic handcrafted artisan products from Indian craftsmen",
                    "images": [],
                },
                "bpp_fulfillments": [
                    {
                        "id": "STD-DELIVERY",
                        "type": "Delivery",
                        "end": {"location": {"address": {"area_code": pincode}}},
                        "rateable": False,
                        "tracking": False,
                        "time": {"label": "Standard", "duration": f"P{delivery_days}D"}
                    }
                ],
                "bpp_providers": [
                    {
                        "id": f"PROV-{seller_gstin[:8]}",
                        "descriptor": {
                            "name": seller_name,
                            "short_desc": "Direct-from-artisan marketplace"
                        },
                        "ttl": "P7D",
                        "categories": [
                            {"id": (p.get("category") or "Other").strip().lower().replace(" ", "_").replace("&", "and"),
                             "descriptor": {"name": (p.get("category") or "Other").strip()}}
                            for p in {x.get("category") or "Other": x for x in products}.values()
                        ],
                        "items": items,
                        "tags": [
                            {"code": "seller_gstin", "list": [{"code": seller_gstin}]},
                            {"code": "msme", "list": [{"code": "REGISTERED"}]},
                            {"code": "artisan_products", "list": [{"code": "YES"}]}
                        ]
                    }
                ]
            }
        }
    }
    return catalog

def _save_export_bytes(filename: str, content: bytes, content_type: str) -> Optional[str]:
    try:
        if not supabase:
            return None
        supabase.storage.from_(BUCKET_EXPORT).upload(
            path=filename,
            file=content,
            file_options={"content-type": content_type, "cache-control": "max-age=604800"}
        )
        return supabase.storage.from_(BUCKET_EXPORT).get_public_url(filename)
    except Exception as e:
        print(f"Export upload to Supabase failed (bucket may not exist): {e}")
        return None

async def export_products_gem(products: List[Dict[str, Any]], opts: Dict[str, Any]) -> Dict[str, Any]:
    csv_content = generate_gem_csv(products, opts)
    csv_bytes = csv_content.encode("utf-8-sig")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"gem-product-catalog_{ts}.csv"
    url = _save_export_bytes(filename, csv_bytes, "text/csv; charset=utf-8")
    return {
        "format": "gem_csv",
        "record_count": len(products),
        "download_url": url,
        "generated_at": _now_iso(),
        "file_size_bytes": len(csv_bytes),
        "preview": csv_content.splitlines()[:5]
    }

async def export_products_ondc(products: List[Dict[str, Any]], opts: Dict[str, Any]) -> Dict[str, Any]:
    payload = generate_ondc_json(products, opts)
    json_content = json.dumps(payload, ensure_ascii=False, indent=2)
    json_bytes = json_content.encode("utf-8")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ondc-catalog_{ts}.json"
    url = _save_export_bytes(filename, json_bytes, "application/json")
    return {
        "format": "ondc_json",
        "record_count": len(products),
        "download_url": url,
        "generated_at": _now_iso(),
        "file_size_bytes": len(json_bytes),
        "payload": payload
    }
