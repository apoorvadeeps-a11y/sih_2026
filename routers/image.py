from fastapi import APIRouter, UploadFile, File, HTTPException
from schemas import ImageUploadResponse
from services.image_engine import process_and_store_image

router = APIRouter(prefix="/image", tags=["Image Engine"])

@router.post("/enhance", response_model=ImageUploadResponse)
async def enhance_image(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
        
    raw_bytes = await file.read()
    try:
        processed_url = await process_and_store_image(raw_bytes)
        return {"image_url": processed_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))