import io
import os
import json
import httpx
import base64
import asyncio
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")
REPLICATE_TOKEN = os.getenv("REPLICATE_API_TOKEN")

HF_TRANSCRIBE_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
HF_TRANSLATE_URL = "https://api-inference.huggingface.co/models/facebook/nllb-200-distilled-600M"
HF_LLM_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HF_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

CATEGORIES = [
    "Pottery", "Textiles", "Jewelry", "Woodwork", "Metalwork",
    "Leather", "Basketry", "Stonework", "Glasswork", "Paintings",
    "Sculpture", "Embroidery", "Handmade Paper", "Candles & Soaps",
    "Toys & Dolls", "Musical Instruments", "Other"
]

CRAFT_TECHNIQUES = [
    "Hand Weaving", "Wheel Throwing", "Hand Coiling", "Slab Building",
    "Wood Carving", "Hand Forging", "Silversmithing", "Soldering",
    "Hand Stitching", "Block Printing", "Batik", "Tie-Dye",
    "Crochet", "Knitting", "Loom Weaving", "Beadwork",
    "Inlay Work", "Terracotta Firing", "Stone Carving", "Engraving",
    "Blown Glass", "Fused Glass", "Paper Mache", "Origami",
    "Natural Dyeing", "Hand Tooled Leather", "Wax Casting", "Other"
]

LANG_NAME_MAP = {
    "as": "Assamese", "bn": "Bengali", "gu": "Gujarati", "hi": "Hindi",
    "kn": "Kannada", "ml": "Malayalam", "mr": "Marathi", "ne": "Nepali",
    "or": "Odia", "pa": "Punjabi", "ta": "Tamil", "te": "Telugu",
    "ur": "Urdu", "sa": "Sanskrit", "en": "English",
    "sd": "Sindhi", "mni": "Manipuri",
    "kok": "Konkani", "doi": "Dogri", "ks": "Kashmiri",
    "brx": "Bodo", "sat": "Santali"
}

INDIAN_NLLB_LANG_CODES = {
    "as": "asm_Beng", "bn": "ben_Beng", "gu": "guj_Gujr", "hi": "hin_Deva",
    "kn": "kan_Knda", "ml": "mal_Mlym", "mr": "mar_Deva", "ne": "npi_Deva",
    "or": "ory_Orya", "pa": "pan_Guru", "ta": "tam_Taml", "te": "tel_Telu",
    "ur": "urd_Arab", "sa": "san_Deva", "en": "eng_Latn",
    "sd": "snd_Arab", "kok": "gom_Deva"
}


SYSTEM_PROMPT = f"""You are an expert Indian artisan product cataloguer supporting all major Indian regional languages. You are part of a system that empowers low-literacy micro-entrepreneurs.

Given a voice transcript (may be in English, Hindi, or ANY Indian regional language like Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, Assamese, etc.), generate a structured multilingual catalog entry.

Respond ONLY with valid JSON using this exact format:
{{
    "title": "English title: Short catchy product title (max 8 words), SEO-friendly for e-commerce",
    "title_hi": "Hindi title: Same meaning translated to professional Devanagari Hindi (max 8 words). NEVER use romanized Hindi — always pure Devanagari script.",
    "title_localized": "Original language version: If the transcript was NOT in English or Hindi, preserve the artisan's original language meaning here. If transcript IS in English or Hindi, this can be null or match the corresponding title.",
    "description": "English description: Professional 2-3 sentence product description suitable for e-commerce (GeM/ONDC). Mention materials, craftsmanship, uniqueness. Use SEO keywords.",
    "description_hi": "Hindi description: Translate the English description into pure Devanagari Hindi. Professional tone suitable for government marketplaces. NEVER use romanized Hindi.",
    "description_localized": "Original language description: If transcript was in a regional language, write description in that same regional script. Otherwise null.",
    "category": "One category chosen exactly from: {', '.join(CATEGORIES)}",
    "craft_technique": "One technique chosen exactly from: {', '.join(CRAFT_TECHNIQUES)}"
}}

RULES:
1. Translate accurately between all languages. Hindi output MUST be in Devanagari script only (no Hinglish).
2. Category and craft_technique MUST be chosen exactly from the lists provided (in English).
3. If transcript is already in English, title_localized can be null and title_hi must be a proper Devanagari translation.
4. If transcript is already in Hindi, title_localized can be the Hindi version and title must be a proper English translation.
5. If transcript is in a third regional language (e.g. Tamil, Bengali), provide ALL THREE versions: English title, Hindi title, and original language in title_localized.
6. Do NOT include any text outside the JSON object.
7. If translation meaning is unclear, make the most reasonable marketplace-appropriate choice.
"""


async def transcribe_hf(audio_bytes: bytes) -> dict | None:
    """Returns dict with keys 'text' and optionally 'language'."""
    if not HF_TOKEN:
        print("HF Token missing for transcription")
        return None
    async with httpx.AsyncClient(timeout=180) as client:
        try:
            r = await client.post(HF_TRANSCRIBE_URL, headers=HF_HEADERS, content=audio_bytes,
                                  params={"generate_timestamps": False})
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, dict):
                    text = data.get("text")
                    lang = data.get("detected_language") or data.get("language")
                    if text:
                        return {"text": text, "language": lang}
            print(f"HF Transcribe returned status: {r.status_code}, body: {r.text[:200]}")
        except Exception as e:
            print(f"HF Transcribe Exception: {e}")
        return None


async def transcribe_replicate(audio_bytes: bytes) -> dict | None:
    """Returns dict with keys 'text' and optionally 'language'."""
    if not REPLICATE_TOKEN:
        print("Replicate Token missing for transcription")
        return None
    b64 = base64.b64encode(audio_bytes).decode()
    async with httpx.AsyncClient(timeout=300) as client:
        try:
            r = await client.post(
                "https://api.replicate.com/v1/predictions",
                headers={
                    "Authorization": f"Bearer {REPLICATE_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "version": "33b410e394c93c9b64ef75d1817b699f2e9f7990605c941f6ab8f0c1f4ed5c8e",
                    "input": {
                        "audio": f"data:audio/webm;base64,{b64}",
                        "model": "large-v3",
                        "language": "auto",
                        "translate": False,
                        "temperature": 0.0
                    }
                }
            )
            if r.status_code not in (200, 201):
                print(f"Replicate transcribe request failed: {r.status_code}")
                return None
            pred = r.json()
            if "urls" not in pred or "get" not in pred["urls"]:
                print(f"Replicate transcribe error response: {pred}")
                return None
            poll_url = pred["urls"]["get"]

            for _ in range(40):
                await asyncio.sleep(3)
                res = await client.get(poll_url, headers={"Authorization": f"Bearer {REPLICATE_TOKEN}"})
                data = res.json()
                status = data.get("status")
                if status == "succeeded":
                    out = data.get("output")
                    text = None
                    lang = None
                    if isinstance(out, dict):
                        text = out.get("text") or out.get("transcription")
                        segments = out.get("segments") or []
                        if len(segments) > 0 and isinstance(segments[0], dict):
                            lang = segments[0].get("language")
                        if not lang:
                            lang = out.get("language") or out.get("detected_language")
                    elif isinstance(out, str):
                        text = out
                    if text:
                        return {"text": text, "language": lang}
                if status == "failed":
                    print(f"Replicate transcribe prediction failed: {data}")
                    return None
        except Exception as e:
            print(f"Replicate Transcribe Exception: {e}")
        return None


async def transcribe_audio(audio_bytes: bytes) -> dict:
    """Returns {"text": str, "language": str or None}"""
    result = await transcribe_hf(audio_bytes)
    if not result or not result.get("text", "").strip():
        print("HF transcription failed — falling back to Replicate")
        result = await transcribe_replicate(audio_bytes)
    if not result or not result.get("text", "").strip():
        raise RuntimeError("Both transcription services failed")
    if not result.get("language"):
        result["language"] = None
    return result


async def translate_text_hf(text: str, src_lang_code: str, tgt_lang_code: str) -> str | None:
    """Translate using NLLB 200 HF model."""
    if not HF_TOKEN:
        return None
    src_nllb = INDIAN_NLLB_LANG_CODES.get(src_lang_code)
    tgt_nllb = INDIAN_NLLB_LANG_CODES.get(tgt_lang_code)
    if not src_nllb or not tgt_nllb:
        return None
    payload = {
        "inputs": text,
        "parameters": {
            "src_lang": src_nllb,
            "tgt_lang": tgt_nllb,
            "max_length": 250
        }
    }
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            r = await client.post(HF_TRANSLATE_URL, headers=HF_HEADERS, json=payload)
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get("translation_text") or None
                if isinstance(data, dict):
                    return data.get("translation_text") or None
        except Exception as e:
            print(f"HF Translation Exception: {e}")
    return None


async def translate_text_replicate(text: str, src_lang: str, tgt_lang: str) -> str | None:
    """Fallback translation via Replicate LLM."""
    if not REPLICATE_TOKEN:
        return None
    src_name = LANG_NAME_MAP.get(src_lang, src_lang or "Auto-detect")
    tgt_name = LANG_NAME_MAP.get(tgt_lang, tgt_lang)
    prompt = f"""You are a professional translator. Translate the following text from {src_name} to {tgt_name}.
Return ONLY the translated text — no commentary, no quotes, no explanation. Preserve all meaning and nuance.
If the text is already in {tgt_name}, return it unchanged.

Text: {text}

Translated text only:"""
    async with httpx.AsyncClient(timeout=180) as client:
        try:
            r = await client.post(
                "https://api.replicate.com/v1/predictions",
                headers={"Authorization": f"Bearer {REPLICATE_TOKEN}", "Content-Type": "application/json"},
                json={
                    "version": "5f2cc6d936a5027244f722ffcd2ddc86e4a07fda805a9dfc1ac24c227f1f5d6d",
                    "input": {"prompt": prompt, "max_tokens": 250, "temperature": 0.2, "top_p": 0.9}
                }
            )
            if r.status_code not in (200, 201):
                return None
            pred = r.json()
            if "urls" not in pred or "get" not in pred["urls"]:
                return None
            poll_url = pred["urls"]["get"]
            for _ in range(20):
                await asyncio.sleep(3)
                res = await client.get(poll_url, headers={"Authorization": f"Bearer {REPLICATE_TOKEN}"})
                data = res.json()
                if data.get("status") == "succeeded":
                    out = data.get("output")
                    raw = "".join(out) if isinstance(out, list) else str(out)
                    return raw.strip() or None
                if data.get("status") == "failed":
                    return None
        except Exception as e:
            print(f"Replicate Translation Exception: {e}")
    return None


async def translate_pipeline(text: str, src_lang: str, tgt_lang: str) -> str | None:
    """Two-tier translation: HF NLLB -> Replicate LLM"""
    if not text or not text.strip():
        return text
    result = await translate_text_hf(text, src_lang, tgt_lang)
    if result and result.strip():
        return result.strip()
    result = await translate_text_replicate(text, src_lang, tgt_lang)
    if result and result.strip():
        return result.strip()
    return None


async def generate_catalog_hf(transcript: str, transcript_language: str | None = None) -> dict | None:
    if not HF_TOKEN:
        return None
    language_note = ""
    if transcript_language:
        lang_name = LANG_NAME_MAP.get(transcript_language, transcript_language)
        language_note = f"\n\nIMPORTANT: Transcript language detected as: {lang_name}. Provide accurate translations."
    prompt = f"<s>[INST] {SYSTEM_PROMPT}{language_note}\n\nVoice transcript:\n{transcript} [/INST]"
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 800,
            "temperature": 0.3,
            "top_p": 0.9,
            "return_full_text": False
        }
    }
    async with httpx.AsyncClient(timeout=180) as client:
        try:
            r = await client.post(HF_LLM_URL, headers=HF_HEADERS, json=payload)
            if r.status_code == 200:
                data = r.json()
                raw = None
                if isinstance(data, list) and len(data) > 0:
                    raw = data[0].get("generated_text")
                elif isinstance(data, dict):
                    raw = data.get("generated_text")
                if raw:
                    parsed = _parse_json_output(raw)
                    if parsed:
                        return parsed
            print(f"HF LLM returned status: {r.status_code}, body: {r.text[:300]}")
        except Exception as e:
            print(f"HF LLM Exception: {e}")
    return None


async def generate_catalog_replicate(transcript: str, transcript_language: str | None = None) -> dict | None:
    if not REPLICATE_TOKEN:
        return None
    language_note = ""
    if transcript_language:
        lang_name = LANG_NAME_MAP.get(transcript_language, transcript_language)
        language_note = f"\n\nDetected transcript language: {lang_name}. Provide accurate translations."
    prompt = f"{SYSTEM_PROMPT}{language_note}\n\nVoice transcript:\n{transcript}"
    async with httpx.AsyncClient(timeout=300) as client:
        try:
            r = await client.post(
                "https://api.replicate.com/v1/predictions",
                headers={"Authorization": f"Bearer {REPLICATE_TOKEN}", "Content-Type": "application/json"},
                json={
                    "version": "5f2cc6d936a5027244f722ffcd2ddc86e4a07fda805a9dfc1ac24c227f1f5d6d",
                    "input": {"prompt": prompt, "max_tokens": 1000, "temperature": 0.3, "top_p": 0.9}
                }
            )
            if r.status_code not in (200, 201):
                return None
            pred = r.json()
            if "urls" not in pred or "get" not in pred["urls"]:
                return None
            poll_url = pred["urls"]["get"]
            for _ in range(35):
                await asyncio.sleep(3)
                res = await client.get(poll_url, headers={"Authorization": f"Bearer {REPLICATE_TOKEN}"})
                data = res.json()
                if data.get("status") == "succeeded":
                    out = data.get("output")
                    raw = "".join(out) if isinstance(out, list) else str(out)
                    parsed = _parse_json_output(raw)
                    if parsed:
                        return parsed
                if data.get("status") == "failed":
                    return None
        except Exception as e:
            print(f"Replicate LLM Exception: {e}")
    return None


def _parse_json_output(raw: str) -> dict | None:
    raw = raw.strip()
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1:
        return None
    json_str = raw[start:end + 1]
    try:
        parsed = json.loads(json_str)
        required_base = {"title", "description", "category", "craft_technique"}
        if not required_base.issubset(parsed.keys()):
            return None
        result = {
            "title": str(parsed["title"]).strip(),
            "description": str(parsed["description"]).strip(),
            "category": str(parsed["category"]).strip(),
            "craft_technique": str(parsed["craft_technique"]).strip(),
        }
        for opt_key in ("title_hi", "description_hi", "title_localized", "description_localized"):
            v = parsed.get(opt_key)
            if isinstance(v, str) and v.strip():
                result[opt_key] = v.strip()
        return result
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}, raw: {raw[:300]}")
    return None


def _fallback_catalog(transcript: str, transcript_language: str | None = None) -> dict:
    words = transcript.split()
    snippet = " ".join(words[:12]) if len(words) >= 5 else transcript
    short_title = (snippet[:50] + "...") if len(snippet) > 50 else snippet
    base_title = short_title.capitalize() or "Handcrafted Artisan Product"

    result = {
        "title": base_title,
        "description": f"Handmade product described as: {transcript[:180]}. Crafted with traditional artisan techniques and premium materials for lasting quality and authentic design.",
        "category": "Other",
        "craft_technique": "Other",
    }
    source_lang = (transcript_language or "").lower()
    if source_lang == "en":
        pass
    elif source_lang == "hi":
        result["title_hi"] = base_title
        result["description_hi"] = f"हस्तनिर्मित उत्पाद: {transcript[:150]}. पारंपरिक शिल्प तकनीकों और उत्तम सामग्री से बनाया गया।"
        result["title_localized"] = base_title
        result["description_localized"] = result["description_hi"]
    else:
        result["title_localized"] = base_title
        result["description_localized"] = transcript[:180]
        result["title_hi"] = "हस्तनिर्मित शिल्प उत्पाद"
        result["description_hi"] = "हमारे कुशल कारीगरों द्वारा पारंपरिक तकनीकों से बनाया गया उत्कृष्ट हस्तशिल्प उत्पाद।"
    return result


async def _fill_missing_translations(result: dict, transcript: str, transcript_language: str | None) -> dict:
    """Use translation pipeline to fill in missing Hindi or localized fields."""
    en_title = result.get("title", "")
    en_desc = result.get("description", "")
    src_lang = (transcript_language or "en").lower() if transcript_language else "en"

    if not result.get("title_hi") and en_title:
        translated = await translate_pipeline(en_title, "en", "hi")
        if translated:
            result["title_hi"] = translated
    if not result.get("description_hi") and en_desc:
        translated = await translate_pipeline(en_desc, "en", "hi")
        if translated:
            result["description_hi"] = translated

    if transcript_language and transcript_language.lower() != "en" and transcript_language.lower() != "hi":
        src_lang_key = transcript_language.lower()
        if not result.get("title_localized") and en_title:
            translated = await translate_pipeline(en_title, "en", src_lang_key)
            if translated:
                result["title_localized"] = translated
            else:
                result["title_localized"] = transcript[:50]
        if not result.get("description_localized") and en_desc:
            translated = await translate_pipeline(en_desc, "en", src_lang_key)
            if translated:
                result["description_localized"] = translated
            else:
                result["description_localized"] = transcript[:180]

    return result


async def voice_to_catalog(audio_bytes: bytes) -> dict:
    tx_result = await transcribe_audio(audio_bytes)
    transcript = tx_result["text"]
    transcript_language = tx_result.get("language")
    if len(transcript) < 250:
        print(f"Transcript [{transcript_language}]: {transcript}")
    else:
        print(f"Transcript [{transcript_language}]: {transcript[:250]}...")

    result = await generate_catalog_hf(transcript, transcript_language)
    if result is None:
        print("HF catalog generation failed — falling back to Replicate")
        result = await generate_catalog_replicate(transcript, transcript_language)

    if result is None:
        print("Both LLM services failed — using rule-based fallback")
        result = _fallback_catalog(transcript, transcript_language)
    else:
        result = await _fill_missing_translations(result, transcript, transcript_language)

    result["source_language"] = transcript_language or "en"
    result["transcript_language"] = transcript_language or "en"
    result["transcript_raw"] = transcript
    return result
