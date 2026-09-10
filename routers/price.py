from fastapi import APIRouter, HTTPException
from schemas import PriceRequest, PriceResponse
from services.price_engine import calculate_price

router = APIRouter(prefix="/price", tags=["Price Engine"])

@router.post("/calculate", response_model=PriceResponse)
async def calculate_price_endpoint(payload: PriceRequest):
    if payload.material_cost < 0:
        raise HTTPException(status_code=400, detail="material_cost must be non-negative")
    if payload.labor_hours < 0:
        raise HTTPException(status_code=400, detail="labor_hours must be non-negative")
    if payload.material_cost == 0 and payload.labor_hours == 0:
        raise HTTPException(status_code=400, detail="material_cost and labor_hours cannot both be zero")

    try:
        result = await calculate_price(
            material_cost=payload.material_cost,
            labor_hours=payload.labor_hours,
            category=payload.category,
            title=payload.title,
            description=payload.description,
            craft_technique=payload.craft_technique
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def list_pricing_categories():
    from services.price_engine import CATEGORY_DATA
    return {
        "categories": [
            {
                "name": name,
                "hourly_rate_inr": data["hourly_rate"],
                "markup_range": f"{data['markup_low']}x - {data['markup_high']}x",
                "overhead_pct": int(data["overhead_pct"] * 100),
                "gem_premium": f"+{int((data['gem_premium'] - 1) * 100)}%",
                "market_demand": data["market_demand"],
                "data_quality": data["data_quality"]
            }
            for name, data in CATEGORY_DATA.items()
        ]
    }

@router.post("/breakdown")
async def calculate_price_with_breakdown(payload: PriceRequest):
    from services.price_engine import _rule_based_price
    if payload.material_cost < 0 or payload.labor_hours < 0:
        raise HTTPException(status_code=400, detail="costs must be non-negative")
    if payload.material_cost == 0 and payload.labor_hours == 0:
        raise HTTPException(status_code=400, detail="both zero")

    rule_result = _rule_based_price(payload.material_cost, payload.labor_hours, payload.category)
    final_result = await calculate_price(
        material_cost=payload.material_cost,
        labor_hours=payload.labor_hours,
        category=payload.category,
        title=payload.title,
        description=payload.description,
        craft_technique=payload.craft_technique
    )
    return {
        **final_result,
        "breakdown": rule_result["_debug"],
        "margin_pct": round(
            ((final_result["suggested_price"] - final_result["base_cost"]) / final_result["base_cost"]) * 100,
            1
        ) if final_result["base_cost"] > 0 else 0
    }
