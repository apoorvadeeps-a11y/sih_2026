from fastapi import FastAPI
from routers import image as image_router
from routers import voice as voice_router
from routers import price as price_router
from routers import products as products_router

app = FastAPI(title="Artisan Backend API")

app.include_router(image_router.router)
app.include_router(voice_router.router)
app.include_router(price_router.router)
app.include_router(products_router.router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Backend unblocked"}
