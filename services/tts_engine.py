"""
Text-to-Speech engine for artisan catalog readback.
Primary: HuggingFace facebook/mms-tts-* (per-language MMS models)
Fallback: HuggingFace espnet/kan-bayashi_ljspeech_vits (English only)
The output is raw WAV bytes returned directly to the caller.
"""

import os
import io
import httpx
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")
HF_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

# HuggingFace MMS-TTS supports 1100+ languages including all major Indian ones.
# Model IDs follow the pattern: facebook/mms-tts-<iso-639-3-code>
# Map our ISO-639-1 codes to the correct MMS model names.
_MMS_MODEL_MAP = {
    "hi":  "facebook/mms-tts-hin",
    "bn":  "facebook/mms-tts-ben",
    "ta":  "facebook/mms-tts-tam",
    "te":  "facebook/mms-tts-tel",
    "mr":  "facebook/mms-tts-mar",
    "gu":  "facebook/mms-tts-guj",
    "kn":  "facebook/mms-tts-kan",
    "ml":  "facebook/mms-tts-mal",
    "pa":  "facebook/mms-tts-pan",
    "or":  "facebook/mms-tts-ory",
    "as":  "facebook/mms-tts-asm",
    "ur":  "facebook/mms-tts-urd",
    "ne":  "facebook/mms-tts-npi",
    "sa":  "facebook/mms-tts-san",
    "kok": "facebook/mms-tts-kok",
    "sd":  "facebook/mms-tts-snd",
    "en":  "facebook/mms-tts-eng",
}

_FALLBACK_MODEL = "facebook/mms-tts-eng"


def _get_model_url(lang_code: str) -> str:
    model = _MMS_MODEL_MAP.get((lang_code or "en").lower(), _FALLBACK_MODEL)
    return f"https://api-inference.huggingface.co/models/{model}"


async def synthesize_speech(text: str, lang_code: str = "en") -> bytes:
    """
    Convert text to speech. Returns WAV bytes.
    Tries the language-specific MMS model first; falls back to English MMS if it fails.
    Raises RuntimeError if all attempts fail.
    """
    if not text or not text.strip():
        raise ValueError("text must not be empty")

    primary_url = _get_model_url(lang_code)
    fallback_url = _get_model_url("en")

    payload = {"inputs": text.strip()}

    async with httpx.AsyncClient(timeout=60) as client:
        # Primary: language-specific model
        try:
            r = await client.post(primary_url, headers=HF_HEADERS, json=payload)
            if r.status_code == 200 and r.headers.get("content-type", "").startswith("audio/"):
                return r.content
            print(f"TTS primary [{lang_code}] returned {r.status_code}: {r.text[:150]}")
        except Exception as e:
            print(f"TTS primary exception [{lang_code}]: {e}")

        # Fallback: English model (always available)
        if primary_url != fallback_url:
            try:
                r = await client.post(fallback_url, headers=HF_HEADERS, json=payload)
                if r.status_code == 200 and r.headers.get("content-type", "").startswith("audio/"):
                    print(f"TTS fallback to English succeeded for lang [{lang_code}]")
                    return r.content
                print(f"TTS fallback [en] returned {r.status_code}: {r.text[:150]}")
            except Exception as e:
                print(f"TTS fallback exception [en]: {e}")

    raise RuntimeError(f"TTS synthesis failed for lang={lang_code}")
