import io
import os
import uuid
import base64
import asyncio
import httpx
from PIL import Image
from dotenv import load_dotenv
from core.supabase_client import supabase

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")
REPLICATE_TOKEN = os.getenv("REPLICATE_API_TOKEN")

HF_API_URL = "https://api-inference.huggingface.co/models/briaai/RMBG-2.0"
HF_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

def compress_image(image_bytes: bytes) -> bytes:
    from PIL import ImageOps, ImageEnhance
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    try:
        img = ImageOps.autocontrast(img, cutoff=1)
    except Exception:
        pass

    try:
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.08)
    except Exception:
        pass

    try:
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.05)
    except Exception:
        pass

    try:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.02)
    except Exception:
        pass

    img.thumbnail((1920, 1920))

    buf = io.BytesIO()
    quality = 85
    while True:
        buf.seek(0)
        buf.truncate()
        img.save(buf, format="JPEG", quality=quality)
        if buf.tell() <= 1_000_000 or quality < 20:
            break
        quality -= 5
    return buf.getvalue()

async def remove_background_hf(image_bytes: bytes) -> bytes | None:
    if not HF_TOKEN:
        print("HF Token missing from environment")
        return None
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            r = await client.post(HF_API_URL, headers=HF_HEADERS, content=image_bytes)
            if r.status_code == 200:
                return r.content
            print(f"HF returned status code: {r.status_code}")
        except Exception as e:
            print(f"HF Exception: {e}")
        return None

async def remove_background_replicate(image_bytes: bytes) -> bytes | None:
    if not REPLICATE_TOKEN:
        print("Replicate Token missing from environment")
        return None
    b64 = base64.b64encode(image_bytes).decode()
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            r = await client.post(
                "https://api.replicate.com/v1/predictions",
                headers={
                    "Authorization": f"Bearer {REPLICATE_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "version": "fb8af171cfa1616ddcf1242c093f9c46bcaded94bcfe2b14923456c2c2441fdb",
                    "input": {"image": f"data:image/jpeg;base64,{b64}"}
                }
            )
            if r.status_code not in (200, 201):
                print(f"Replicate request failed with status {r.status_code}: {r.text[:300]}")
                return None
            pred = r.json()
            if "urls" not in pred or "get" not in pred["urls"]:
                print(f"Replicate error response (no urls.get): {pred}")
                return None
            poll_url = pred["urls"]["get"]

            output_url = None
            for _ in range(25):
                await asyncio.sleep(3)
                res = await client.get(
                    poll_url,
                    headers={"Authorization": f"Bearer {REPLICATE_TOKEN}"}
                )
                data = res.json()
                status = data.get("status")
                if status == "succeeded":
                    out = data.get("output")
                    if isinstance(out, str):
                        output_url = out
                    elif isinstance(out, list) and len(out) > 0:
                        output_url = out[0] if isinstance(out[0], str) else None
                    elif isinstance(out, dict):
                        output_url = out.get("uri") or out.get("url") or out.get("output")
                    if output_url:
                        break
                    print(f"Replicate succeeded but could not extract output URL from: {type(out)} {str(out)[:200]}")
                    return None
                if status == "failed":
                    err = data.get("error") or data
                    print(f"Replicate prediction failed: {err}")
                    return None
            if not output_url:
                print("Replicate prediction timed out (no success after 25 polls)")
                return None
            img_r = await client.get(output_url, timeout=30)
            if img_r.status_code == 200:
                return img_r.content
            print(f"Replicate output download failed: {img_r.status_code}")
        except Exception as e:
            print(f"Replicate Exception: {e}")
        return None

def composite_on_white(png_bytes: bytes, size: int = 1000) -> bytes:
    """Place the bg-removed PNG on a clean white square canvas — marketplace ready."""
    img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    canvas = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    img.thumbnail((size, size), Image.LANCZOS)
    x = (size - img.width) // 2
    y = (size - img.height) // 2
    canvas.paste(img, (x, y), img)
    out = canvas.convert("RGB")
    buf = io.BytesIO()
    out.save(buf, format="JPEG", quality=88)
    return buf.getvalue()


async def process_and_store_image(raw_image_bytes: bytes) -> str:
    compressed = compress_image(raw_image_bytes)

    result = await remove_background_hf(compressed)
    if result is None:
        print("HF failed — falling back to Replicate")
        result = await remove_background_replicate(compressed)

    if result is None:
        raise RuntimeError("Both background removal services failed")

    # Composite onto white background for e-commerce standards
    result = composite_on_white(result)

    filename = f"products/{uuid.uuid4()}.jpg"
    bucket_name = "product-images"

    if supabase is not None:
        try:
            supabase.storage.from_(bucket_name).upload(
                path=filename,
                file=result,
                file_options={"content-type": "image/jpeg"}
            )
            return supabase.storage.from_(bucket_name).get_public_url(filename)
        except Exception as e:
            print(f"Supabase storage upload failed, using data URL fallback: {e}")

    b64 = base64.b64encode(result).decode()
    return f"data:image/jpeg;base64,{b64}"