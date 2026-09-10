# Artisan Backend API — SIH 2026

FastAPI backend for AI-powered artisan product cataloguing, pricing, and marketplace export.

## Quick Start

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env         # fill in your keys
uvicorn main:app --reload
```

API docs: http://localhost:8000/docs

## Environment Variables

| Key | Description |
|-----|-------------|
| `HUGGINGFACE_API_KEY` | HF Inference API token |
| `REPLICATE_API_TOKEN` | Replicate API token (fallback) |
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_SERVICE_KEY` | Supabase service role key |

## Deploy to Railway

1. Push to GitHub (never commit `.env`)
2. New Project → Deploy from GitHub
3. Add env vars in Railway dashboard
4. Done — public HTTPS URL auto-assigned

## Deploy to Render

1. New Web Service → connect repo
2. Build command: `pip install -r requirements.txt`
3. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add env vars → Deploy

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| POST | `/image/enhance` | AI bg removal + white composite |
| POST | `/voice/to-catalog` | Voice → multilingual catalog |
| POST | `/voice/tts` | Text → speech (14 Indian languages) |
| POST | `/voice/tts/catalog` | Read catalog back to artisan |
| POST | `/price/calculate` | AI pricing with image analysis |
| POST | `/products` | Create product |
| GET | `/products` | List products |
| POST | `/products/bulk` | Bulk create (up to 500) |
| POST | `/products/export/gem/csv` | GeM marketplace export |
| POST | `/products/export/ondc/json` | ONDC Beckn 2.0 export |
