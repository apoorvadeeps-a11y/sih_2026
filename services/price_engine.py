import os
import json
import httpx
import asyncio
import base64
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")
REPLICATE_TOKEN = os.getenv("REPLICATE_API_TOKEN")

HF_LLM_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HF_CAPTION_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
HF_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

CATEGORY_DATA = {
    "Pottery": {
        "hourly_rate": 180.0,
        "markup_low": 2.3,
        "markup_high": 3.2,
        "overhead_pct": 0.18,
        "gem_premium": 1.10,
        "data_quality": "High",
        "market_demand": "High"
    },
    "Textiles": {
        "hourly_rate": 220.0,
        "markup_low": 2.8,
        "markup_high": 3.8,
        "overhead_pct": 0.22,
        "gem_premium": 1.15,
        "data_quality": "High",
        "market_demand": "Very High"
    },
    "Jewelry": {
        "hourly_rate": 450.0,
        "markup_low": 3.8,
        "markup_high": 5.5,
        "overhead_pct": 0.25,
        "gem_premium": 1.25,
        "data_quality": "High",
        "market_demand": "Very High"
    },
    "Woodwork": {
        "hourly_rate": 260.0,
        "markup_low": 2.7,
        "markup_high": 3.9,
        "overhead_pct": 0.20,
        "gem_premium": 1.12,
        "data_quality": "Medium-High",
        "market_demand": "High"
    },
    "Metalwork": {
        "hourly_rate": 320.0,
        "markup_low": 3.2,
        "markup_high": 4.8,
        "overhead_pct": 0.23,
        "gem_premium": 1.18,
        "data_quality": "Medium-High",
        "market_demand": "Medium-High"
    },
    "Leather": {
        "hourly_rate": 240.0,
        "markup_low": 2.4,
        "markup_high": 3.4,
        "overhead_pct": 0.18,
        "gem_premium": 1.10,
        "data_quality": "Medium-High",
        "market_demand": "High"
    },
    "Basketry": {
        "hourly_rate": 140.0,
        "markup_low": 2.0,
        "markup_high": 2.9,
        "overhead_pct": 0.15,
        "gem_premium": 1.08,
        "data_quality": "Medium",
        "market_demand": "Medium"
    },
    "Stonework": {
        "hourly_rate": 300.0,
        "markup_low": 2.9,
        "markup_high": 4.4,
        "overhead_pct": 0.22,
        "gem_premium": 1.15,
        "data_quality": "Medium",
        "market_demand": "Medium-High"
    },
    "Glasswork": {
        "hourly_rate": 420.0,
        "markup_low": 3.6,
        "markup_high": 5.8,
        "overhead_pct": 0.26,
        "gem_premium": 1.20,
        "data_quality": "Medium",
        "market_demand": "Medium"
    },
    "Paintings": {
        "hourly_rate": 500.0,
        "markup_low": 4.5,
        "markup_high": 7.5,
        "overhead_pct": 0.20,
        "gem_premium": 1.30,
        "data_quality": "Medium-High",
        "market_demand": "Medium-High"
    },
    "Sculpture": {
        "hourly_rate": 400.0,
        "markup_low": 3.5,
        "markup_high": 5.5,
        "overhead_pct": 0.24,
        "gem_premium": 1.22,
        "data_quality": "Medium",
        "market_demand": "Medium"
    },
    "Embroidery": {
        "hourly_rate": 280.0,
        "markup_low": 3.0,
        "markup_high": 4.8,
        "overhead_pct": 0.20,
        "gem_premium": 1.15,
        "data_quality": "High",
        "market_demand": "Very High"
    },
    "Handmade Paper": {
        "hourly_rate": 160.0,
        "markup_low": 2.2,
        "markup_high": 3.2,
        "overhead_pct": 0.17,
        "gem_premium": 1.10,
        "data_quality": "Medium",
        "market_demand": "Medium"
    },
    "Candles & Soaps": {
        "hourly_rate": 150.0,
        "markup_low": 2.5,
        "markup_high": 3.8,
        "overhead_pct": 0.16,
        "gem_premium": 1.10,
        "data_quality": "Medium-High",
        "market_demand": "High"
    },
    "Toys & Dolls": {
        "hourly_rate": 200.0,
        "markup_low": 2.4,
        "markup_high": 3.6,
        "overhead_pct": 0.18,
        "gem_premium": 1.12,
        "data_quality": "Medium",
        "market_demand": "Medium-High"
    },
    "Musical Instruments": {
        "hourly_rate": 380.0,
        "markup_low": 3.4,
        "markup_high": 5.2,
        "overhead_pct": 0.25,
        "gem_premium": 1.20,
        "data_quality": "Medium",
        "market_demand": "Medium"
    },
    "Other": {
        "hourly_rate": 220.0,
        "markup_low": 2.2,
        "markup_high": 3.5,
        "overhead_pct": 0.20,
        "gem_premium": 1.10,
        "data_quality": "Low",
        "market_demand": "Variable"
    }
}

def _get_category_data(category: str) -> dict:
    cat_key = category.strip() if category else "Other"
    if cat_key in CATEGORY_DATA:
        return CATEGORY_DATA[cat_key]
    for key in CATEGORY_DATA:
        if key.lower() == cat_key.lower():
            return CATEGORY_DATA[key]
    return CATEGORY_DATA["Other"]

async def _caption_image(image_url: str) -> str | None:
    """
    Fetch an image and run BLIP captioning on it.
    Returns a short English description to enrich price prompts.
    Best-effort — returns None on any failure.
    """
    if not HF_TOKEN or not image_url:
        return None
    # Skip data URIs — convert base64 back to bytes
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            if image_url.startswith("data:image"):
                header, b64data = image_url.split(",", 1)
                img_bytes = base64.b64decode(b64data)
            else:
                r = await client.get(image_url)
                if r.status_code != 200:
                    return None
                img_bytes = r.content

            r = await client.post(HF_CAPTION_URL, headers=HF_HEADERS, content=img_bytes)
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, list) and data:
                    return data[0].get("generated_text")
                if isinstance(data, dict):
                    return data.get("generated_text")
    except Exception as e:
        print(f"Image captioning exception: {e}")
    return None


def _rule_based_price(material_cost: float, labor_hours: float, category: str) -> dict:
    cat = _get_category_data(category)

    labor_cost = labor_hours * cat["hourly_rate"]
    direct_cost = material_cost + labor_cost
    overhead = direct_cost * cat["overhead_pct"]
    base_cost = round(direct_cost + overhead, 2)

    if labor_hours <= 1:
        complexity_factor = 0.92
    elif labor_hours <= 3:
        complexity_factor = 1.0
    elif labor_hours <= 8:
        complexity_factor = 1.05
    elif labor_hours <= 20:
        complexity_factor = 1.10
    else:
        complexity_factor = 1.15

    markup_mid = (cat["markup_low"] + cat["markup_high"]) / 2
    effective_markup = markup_mid * complexity_factor

    raw_suggestion = base_cost * effective_markup
    suggestion_with_premium = raw_suggestion * cat["gem_premium"]

    suggested_price = round(suggestion_with_premium, 0)
    if suggested_price < base_cost * 1.5:
        suggested_price = round(base_cost * 1.5, 0)

    return {
        "base_cost": round(base_cost, 2),
        "suggested_price": float(suggested_price),
        "confidence_band": cat["data_quality"],
        "_debug": {
            "labor_cost": round(labor_cost, 2),
            "direct_cost": round(direct_cost, 2),
            "overhead": round(overhead, 2),
            "hourly_rate": cat["hourly_rate"],
            "markup_used": round(effective_markup, 2),
            "gem_premium": cat["gem_premium"],
            "matched_category": category if category in CATEGORY_DATA else "Other (fallback)"
        }
    }

async def _llm_price_advice_hf(material_cost: float, labor_hours: float, category: str, rule_result: dict,
                                title: str | None = None, description: str | None = None,
                                craft_technique: str | None = None,
                                image_caption: str | None = None) -> float | None:
    if not HF_TOKEN:
        return None

    product_narrative = ""
    if title or description or craft_technique or image_caption:
        image_note = f"\n- Visual Analysis (AI image caption): {image_caption}" if image_caption else ""
        product_narrative = f"""
Product Marketing Details (use these to differentiate pricing quality tier):
- Product Title: {title or '(not provided)'}
- Craft Technique: {craft_technique or '(not provided)'}
- Product Description: {description or '(not provided)'}{image_note}

IMPORTANT PRICING SIGNALS TO ANALYZE:
- Look for premium indicators in description: hand-painted, zari work, natural dyes, miniature, 
  Madhubani, Kanjivaram, Banarasi, bidri, tanjore, pattachitra, silver filigree, stone studded,
  embroidered, carved, inlay, jadau, nakshi, temple jewelry, etc. → ADD 10-25% premium.
- Look for mass-market signals: generic, simple design, basic materials → no premium or 5% discount.
- Look for luxury materials mention: silver, gold plating, semi-precious stones, silk, teak wood → premium.
- Products with elaborate technique names (Zardozi, Ikat, Patola, Kalamkari) → premium tier.
- Use the visual analysis caption to gauge complexity, finish quality, and material richness."""

    prompt = f"""<s>[INST] You are an expert pricing analyst for the Indian Government e-Marketplace (GeM) and ONDC platform, specializing in handcrafted artisan products.

Given the following pricing context, return ONLY a SINGLE NUMBER (the adjusted suggested price in INR). No currency symbol, no explanation, no extra text.

Product Context:
- Category: {category}
- Material Cost: ₹{material_cost}
- Labor Hours: {labor_hours} hrs
- Calculated Base Cost: ₹{rule_result['base_cost']}
- Rule-based Suggested Price: ₹{rule_result['suggested_price']}
- Labor Cost: ₹{rule_result['_debug']['labor_cost']}
- Hourly Rate Used: ₹{rule_result['_debug']['hourly_rate']}/hr
- Markup Used: {rule_result['_debug']['markup_used']}x
- GeM Premium: {rule_result['_debug']['gem_premium']}x
{product_narrative}

Indian Artisan Market Guidance for {category}:
- Typical market demand: {_get_category_data(category)['market_demand']}
- Adjust up if this is a premium/labor-intensive item (>{labor_hours}h)
- Adjust down if material cost dominates and labor content is low
- GeM bulk government procurement typically expects 5-15% premium over retail fair price
- ONDC marketplace pricing is competitive but fair to artisans

Respond with ONLY the final adjusted price as a single integer number. [/INST]"""
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 20,
            "temperature": 0.2,
            "top_p": 0.8,
            "return_full_text": False
        }
    }
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            r = await client.post(HF_LLM_URL, headers=HF_HEADERS, json=payload)
            if r.status_code == 200:
                data = r.json()
                raw = None
                if isinstance(data, list) and len(data) > 0:
                    raw = data[0].get("generated_text", "")
                elif isinstance(data, dict):
                    raw = data.get("generated_text", "")
                if raw:
                    cleaned = ''.join(c for c in raw if c.isdigit() or c == '.')
                    if cleaned:
                        adjusted = float(cleaned)
                        rule_price = rule_result["suggested_price"]
                        lower_bound = rule_price * 0.75
                        upper_bound = rule_price * 1.40
                        if lower_bound <= adjusted <= upper_bound:
                            return adjusted
        except Exception as e:
            print(f"HF Price LLM Exception: {e}")
        return None

async def _llm_price_advice_replicate(material_cost: float, labor_hours: float, category: str, rule_result: dict,
                                       title: str | None = None, description: str | None = None,
                                       craft_technique: str | None = None,
                                       image_caption: str | None = None) -> float | None:
    if not REPLICATE_TOKEN:
        return None

    product_narrative = ""
    if title or description or craft_technique or image_caption:
        image_note = f"\n- Visual Analysis (AI image caption): {image_caption}" if image_caption else ""
        product_narrative = f"""
Product Marketing Details (use these to differentiate pricing quality tier):
- Product Title: {title or '(not provided)'}
- Craft Technique: {craft_technique or '(not provided)'}
- Product Description: {description or '(not provided)'}{image_note}

Premium pricing signals (add 10-25% if mentioned): hand-painted, zari work, natural dyes,
Madhubani, Kanjivaram, Banarasi, bidri, tanjore, pattachitra, silver filigree, stone studded,
embroidered, carved, inlay, jadau, nakshi, temple jewelry, zardozi, ikat, patola, kalamkari,
silver, gold plating, semi-precious stones, silk, teak wood.
Mass-market signals (reduce 5% or no change): generic, simple, basic, standard.
Also consider the visual caption for material richness and finish quality."""

    prompt = f"""You are an expert pricing analyst for the Indian Government e-Marketplace (GeM) and ONDC platform, specializing in handcrafted artisan products.

Given the following pricing context, return ONLY a SINGLE NUMBER (the adjusted suggested price in INR). No currency symbol, no explanation, no extra text.

Product Context:
- Category: {category}
- Material Cost: ₹{material_cost}
- Labor Hours: {labor_hours} hrs
- Calculated Base Cost: ₹{rule_result['base_cost']}
- Rule-based Suggested Price: ₹{rule_result['suggested_price']}
{product_narrative}

Guidance:
- Typical market demand for {category}: {_get_category_data(category)['market_demand']}
- Adjust up if this is a premium/labor-intensive item
- Adjust down if material cost dominates and labor content is low
- Stay within ±25% of the rule-based suggested price.

Respond with ONLY the final adjusted price as a single integer."""
    async with httpx.AsyncClient(timeout=180) as client:
        try:
            r = await client.post(
                "https://api.replicate.com/v1/predictions",
                headers={
                    "Authorization": f"Bearer {REPLICATE_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "version": "5f2cc6d936a5027244f722ffcd2ddc86e4a07fda805a9dfc1ac24c227f1f5d6d",
                    "input": {
                        "prompt": prompt,
                        "max_tokens": 30,
                        "temperature": 0.2,
                        "top_p": 0.8
                    }
                }
            )
            pred = r.json()
            if "urls" not in pred or "get" not in pred["urls"]:
                return None
            poll_url = pred["urls"]["get"]

            for _ in range(20):
                await asyncio.sleep(3)
                res = await client.get(
                    poll_url,
                    headers={"Authorization": f"Bearer {REPLICATE_TOKEN}"}
                )
                data = res.json()
                if data.get("status") == "succeeded":
                    output = data.get("output")
                    raw = "".join(output) if isinstance(output, list) else str(output)
                    cleaned = ''.join(c for c in raw if c.isdigit() or c == '.')
                    if cleaned:
                        adjusted = float(cleaned)
                        rule_price = rule_result["suggested_price"]
                        if rule_price * 0.75 <= adjusted <= rule_price * 1.40:
                            return adjusted
                if data.get("status") == "failed":
                    return None
        except Exception as e:
            print(f"Replicate Price LLM Exception: {e}")
        return None

async def calculate_price(material_cost: float, labor_hours: float, category: str,
                          title: str | None = None, description: str | None = None,
                          craft_technique: str | None = None,
                          image_url: str | None = None) -> dict:
    if material_cost < 0 or labor_hours < 0:
        raise ValueError("material_cost and labor_hours must be non-negative")
    if material_cost == 0 and labor_hours == 0:
        raise ValueError("material_cost and labor_hours cannot both be zero")

    # Run rule-based calc and image captioning concurrently
    rule_result, image_caption = await asyncio.gather(
        asyncio.to_thread(_rule_based_price, material_cost, labor_hours, category),
        _caption_image(image_url) if image_url else asyncio.sleep(0, result=None)
    )

    if image_caption:
        print(f"Image caption for pricing: {image_caption}")

    llm_adjusted = await _llm_price_advice_hf(material_cost, labor_hours, category, rule_result,
                                              title=title, description=description,
                                              craft_technique=craft_technique,
                                              image_caption=image_caption)
    if llm_adjusted is None:
        llm_adjusted = await _llm_price_advice_replicate(material_cost, labor_hours, category, rule_result,
                                                         title=title, description=description,
                                                         craft_technique=craft_technique,
                                                         image_caption=image_caption)

    if llm_adjusted is not None:
        final_price = round(llm_adjusted, 0)
        confidence = rule_result["confidence_band"]
        if confidence == "Low":
            confidence = "Medium"
        elif confidence == "Medium":
            confidence = "Medium-High"
    else:
        final_price = rule_result["suggested_price"]
        confidence = rule_result["confidence_band"]

    return {
        "base_cost": rule_result["base_cost"],
        "suggested_price": float(final_price),
        "confidence_band": confidence
    }
