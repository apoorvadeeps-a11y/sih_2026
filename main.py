from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from routers import image as image_router
from routers import price as price_router
from routers import products as products_router
from routers import voice as voice_router

app = FastAPI(title="Artisan Backend API")

# Enable CORS so your frontend can call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(image_router.router)
app.include_router(voice_router.router)
app.include_router(price_router.router)
app.include_router(products_router.router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Backend unblocked"}

@app.get("/config/status")
def config_status():
    return {
        "status": "ok",
        "providers": {
            "huggingface": bool(os.getenv("HUGGINGFACE_API_KEY")),
            "replicate": bool(os.getenv("REPLICATE_API_TOKEN")),
            "supabase": bool(os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_KEY")),
        },
    }