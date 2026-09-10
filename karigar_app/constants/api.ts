export const API_BASE = 'https://sih-2026-jjd8.onrender.com';

export const ENDPOINTS = {
  health:          '/',
  voiceToCatalog:  '/voice/to-catalog',
  ttsText:         '/voice/tts',
  ttsCatalog:      '/voice/tts/catalog',
  imageEnhance:    '/image/enhance',
  priceCalculate:  '/price/calculate',
  products:        '/products',
  productById:     (id: string) => `/products/${id}`,
  exportGem:       '/products/export/gem/csv',
  exportOndc:      '/products/export/ondc/json',
};
