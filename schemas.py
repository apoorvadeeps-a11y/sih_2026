from pydantic import BaseModel
from typing import Optional, List, Any, Dict


MAJOR_INDIAN_LANGUAGES = [
    "as",   # Assamese
    "bn",   # Bengali
    "gu",   # Gujarati
    "hi",   # Hindi
    "kn",   # Kannada
    "ml",   # Malayalam
    "mr",   # Marathi
    "ne",   # Nepali
    "or",   # Odia
    "pa",   # Punjabi
    "ta",   # Tamil
    "te",   # Telugu
    "ur",   # Urdu
    "sa",   # Sanskrit
    "en",   # English (link language)
]


class LocalizedText(BaseModel):
    en: str = ""
    hi: str = ""
    language_code: Optional[str] = None
    localized: Optional[str] = None


class ProductCreate(BaseModel):
    title: str
    description: str
    category: str
    craft_technique: Optional[str] = None
    material_cost: float
    labor_hours: float
    title_hi: Optional[str] = None
    description_hi: Optional[str] = None
    title_localized: Optional[str] = None
    description_localized: Optional[str] = None
    source_language: Optional[str] = None


class ProductResponse(ProductCreate):
    id: str
    suggested_price: float
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    base_cost: Optional[float] = None
    created_at: Optional[str] = None
    sku: Optional[str] = None


class ProductListResponse(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int
    per_page: int


class VoiceTranscriptRequest(BaseModel):
    audio_url: str


class CatalogOutput(BaseModel):
    title: str
    description: str
    category: str
    craft_technique: str
    title_hi: Optional[str] = None
    description_hi: Optional[str] = None
    title_localized: Optional[str] = None
    description_localized: Optional[str] = None
    source_language: Optional[str] = None
    transcript_language: Optional[str] = None
    transcript_raw: Optional[str] = None


class PriceRequest(BaseModel):
    material_cost: float
    labor_hours: float
    category: str
    title: Optional[str] = None
    description: Optional[str] = None
    craft_technique: Optional[str] = None


class PriceResponse(BaseModel):
    base_cost: float
    suggested_price: float
    confidence_band: str


class ImageUploadResponse(BaseModel):
    image_url: str


class ExportStatusResponse(BaseModel):
    format: str
    record_count: int
    download_url: Optional[str] = None
    generated_at: str
    file_size_bytes: Optional[int] = None
    preview: Optional[List[str]] = None
    payload: Optional[Any] = None


class GeMExportOptions(BaseModel):
    seller_gstin: Optional[str] = "27AABCU9603R1ZZ"
    brand_name: Optional[str] = "ArtisanDirect"
    country_of_origin: Optional[str] = "India"
    local_content_pct: Optional[int] = 100
    hsn_code: Optional[str] = None
    min_order_qty: Optional[int] = 1
    unit_of_measure: Optional[str] = "Piece"


class ONDCExportOptions(BaseModel):
    seller_name: Optional[str] = "Artisan Direct"
    seller_gstin: Optional[str] = "27AABCU9603R1ZZ"
    fulfillment_pincode: Optional[str] = "110001"
    delivery_days: Optional[int] = 7
    currency: Optional[str] = "INR"
    gst_pct: Optional[float] = 12.0
    country_of_origin: Optional[str] = "IND"


class BulkProductCreateResponse(BaseModel):
    created: int
    failed: int
    errors: List[str] = []
    product_ids: List[str] = []
