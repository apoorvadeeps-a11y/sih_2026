from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import Response
from schemas import CatalogOutput, VoiceTranscriptRequest
from services.voice_engine import voice_to_catalog, transcribe_audio
from services.tts_engine import synthesize_speech
import httpx

router = APIRouter(prefix="/voice", tags=["Voice Engine"])

ALLOWED_AUDIO_TYPES = {
    "audio/webm", "audio/mp3", "audio/mpeg", "audio/wav",
    "audio/ogg", "audio/mp4", "audio/m4a", "audio/x-m4a",
    "audio/flac", "audio/x-wav", "application/octet-stream"
}

@router.post("/to-catalog", response_model=CatalogOutput)
async def voice_file_to_catalog(file: UploadFile = File(...)):
    if not file.content_type or (
        file.content_type not in ALLOWED_AUDIO_TYPES and not file.content_type.startswith("audio/")
    ):
        raise HTTPException(status_code=400, detail=f"File must be audio. Got: {file.content_type}")

    audio_bytes = await file.read()
    if len(audio_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty audio file")

    try:
        result = await voice_to_catalog(audio_bytes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/url/to-catalog", response_model=CatalogOutput)
async def voice_url_to_catalog(payload: VoiceTranscriptRequest):
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            r = await client.get(payload.audio_url)
            if r.status_code != 200:
                raise HTTPException(status_code=400, detail=f"Failed to download audio from URL (status {r.status_code})")
            audio_bytes = r.content
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Could not fetch audio: {e}")

    if len(audio_bytes) == 0:
        raise HTTPException(status_code=400, detail="Downloaded audio file is empty")

    try:
        result = await voice_to_catalog(audio_bytes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/url/transcribe")
async def voice_url_transcribe(payload: VoiceTranscriptRequest):
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            r = await client.get(payload.audio_url)
            if r.status_code != 200:
                raise HTTPException(status_code=400, detail=f"Failed to download audio from URL (status {r.status_code})")
            audio_bytes = r.content
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Could not fetch audio: {e}")

    if len(audio_bytes) == 0:
        raise HTTPException(status_code=400, detail="Downloaded audio file is empty")

    try:
        transcript = await transcribe_audio(audio_bytes)
        return {"transcript": transcript}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/raw/text")
async def transcribe_only(file: UploadFile = File(...)):
    if not file.content_type or (
        file.content_type not in ALLOWED_AUDIO_TYPES and not file.content_type.startswith("audio/")
    ):
        raise HTTPException(status_code=400, detail=f"File must be audio. Got: {file.content_type}")

    audio_bytes = await file.read()
    if len(audio_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty audio file")

    try:
        transcript = await transcribe_audio(audio_bytes)
        return {"transcript": transcript}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# TTS: read catalog text back to the artisan in their language
# ---------------------------------------------------------------------------

@router.post("/tts", summary="Text-to-speech readback")
async def text_to_speech(
    text: str = Query(..., description="Text to synthesize"),
    lang: str = Query("en", description="ISO-639-1 language code, e.g. hi, ta, bn")
):
    """
    Convert any text to speech using the MMS multilingual TTS model.
    Returns a WAV audio file — ideal for reading a generated catalog back
    to low-literacy artisans in their regional language.
    """
    try:
        wav_bytes = await synthesize_speech(text, lang_code=lang)
        return Response(content=wav_bytes, media_type="audio/wav",
                        headers={"Content-Disposition": "inline; filename=readback.wav"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tts/catalog", summary="Read full catalog entry back to artisan")
async def catalog_to_speech(
    catalog: CatalogOutput,
    lang: str = Query("hi", description="Language for readback: hi, ta, bn, etc.")
):
    """
    Given a CatalogOutput (e.g. from /voice/to-catalog), synthesizes the
    title + description in the requested language and returns WAV audio.
    Picks the right language slot automatically:
      - lang='hi'  → uses title_hi + description_hi
      - lang='en'  → uses title + description
      - anything else → uses title_localized + description_localized, falls back to English
    """
    lang = lang.lower()
    if lang == "hi":
        title = catalog.title_hi or catalog.title
        desc  = catalog.description_hi or catalog.description
    elif lang == "en":
        title = catalog.title
        desc  = catalog.description
    else:
        title = catalog.title_localized or catalog.title
        desc  = catalog.description_localized or catalog.description

    text = f"{title}. {desc}"
    try:
        wav_bytes = await synthesize_speech(text, lang_code=lang)
        return Response(content=wav_bytes, media_type="audio/wav",
                        headers={"Content-Disposition": "inline; filename=catalog_readback.wav"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
