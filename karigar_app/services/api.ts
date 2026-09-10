import axios from 'axios';
import { API_BASE, ENDPOINTS } from '../constants/api';
import { CatalogResult, Product } from '../store/useAppStore';

const client = axios.create({
  baseURL: API_BASE,
  timeout: 120000,
});

// ── Voice → Catalog ──────────────────────────────────────────
export async function voiceToCatalog(audioUri: string): Promise<CatalogResult> {
  const form = new FormData();
  form.append('file', {
    uri: audioUri,
    name: 'voice.m4a',
    type: 'audio/m4a',
  } as any);
  const res = await client.post(ENDPOINTS.voiceToCatalog, form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
}

// ── Image Enhance ─────────────────────────────────────────────
export async function enhanceImage(imageUri: string): Promise<string> {
  const form = new FormData();
  form.append('file', {
    uri: imageUri,
    name: 'product.jpg',
    type: 'image/jpeg',
  } as any);
  const res = await client.post(ENDPOINTS.imageEnhance, form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data.image_url;
}

// ── Price Calculate ───────────────────────────────────────────
export async function calculatePrice(
  material_cost: number,
  labor_hours: number,
  category: string,
  title?: string,
  image_url?: string,
) {
  const res = await client.post(ENDPOINTS.priceCalculate, {
    material_cost,
    labor_hours,
    category,
    title,
    image_url,
  });
  return res.data as { base_cost: number; suggested_price: number; confidence_band: string };
}

// ── Create Product ────────────────────────────────────────────
export async function createProduct(data: any): Promise<Product> {
  const res = await client.post(ENDPOINTS.products, data);
  return res.data;
}

// ── List Products ─────────────────────────────────────────────
export async function listProducts(page = 1): Promise<{ products: Product[]; total: number }> {
  const res = await client.get(`${ENDPOINTS.products}?page=${page}&per_page=20`);
  return res.data;
}

// ── TTS text ─────────────────────────────────────────────────
export async function ttsText(text: string, lang: string): Promise<string> {
  const res = await client.post(
    `${ENDPOINTS.ttsText}?text=${encodeURIComponent(text)}&lang=${lang}`,
    {},
    { responseType: 'blob' },
  );
  return URL.createObjectURL(res.data);
}

// ── TTS catalog readback ──────────────────────────────────────
export async function ttsCatalog(catalog: CatalogResult, lang: string): Promise<ArrayBuffer> {
  const res = await client.post(
    `${ENDPOINTS.ttsCatalog}?lang=${lang}`,
    catalog,
    { responseType: 'arraybuffer' },
  );
  return res.data;
}
