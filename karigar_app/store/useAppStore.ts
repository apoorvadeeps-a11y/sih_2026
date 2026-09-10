import { create } from 'zustand';

export type Language = {
  code: string;
  label: string;
  native: string;
};

export const LANGUAGES: Language[] = [
  { code: 'en', label: 'English',   native: 'English' },
  { code: 'hi', label: 'Hindi',     native: 'हिंदी'   },
  { code: 'mr', label: 'Marathi',   native: 'मराठी'   },
  { code: 'bn', label: 'Bengali',   native: 'বাংলা'   },
  { code: 'ta', label: 'Tamil',     native: 'தமிழ்'   },
  { code: 'te', label: 'Telugu',    native: 'తెలుగు'  },
  { code: 'gu', label: 'Gujarati',  native: 'ગુજરાતી' },
  { code: 'kn', label: 'Kannada',   native: 'ಕನ್ನಡ'   },
  { code: 'pa', label: 'Punjabi',   native: 'ਪੰਜਾਬੀ'  },
  { code: 'ml', label: 'Malayalam', native: 'മലയാളം'  },
];

export type CatalogResult = {
  title: string;
  title_hi?: string;
  title_localized?: string;
  description: string;
  description_hi?: string;
  description_localized?: string;
  category: string;
  craft_technique: string;
  source_language?: string;
};

export type Product = CatalogResult & {
  id: string;
  sku: string;
  material_cost: number;
  labor_hours: number;
  base_cost: number;
  suggested_price: number;
  confidence_band: string;
  image_url?: string;
  audio_url?: string;
  created_at: string;
};

type AppState = {
  selectedLanguage: Language;
  setLanguage: (lang: Language) => void;

  currentCatalog: CatalogResult | null;
  setCurrentCatalog: (c: CatalogResult | null) => void;

  currentImageUri: string | null;
  setCurrentImageUri: (uri: string | null) => void;

  enhancedImageUrl: string | null;
  setEnhancedImageUrl: (url: string | null) => void;

  products: Product[];
  setProducts: (p: Product[]) => void;
  addProduct: (p: Product) => void;
};

export const useAppStore = create<AppState>((set) => ({
  selectedLanguage: LANGUAGES[1], // Hindi default

  setLanguage: (lang) => set({ selectedLanguage: lang }),

  currentCatalog: null,
  setCurrentCatalog: (c) => set({ currentCatalog: c }),

  currentImageUri: null,
  setCurrentImageUri: (uri) => set({ currentImageUri: uri }),

  enhancedImageUrl: null,
  setEnhancedImageUrl: (url) => set({ enhancedImageUrl: url }),

  products: [],
  setProducts: (p) => set({ products: p }),
  addProduct: (p) => set((s) => ({ products: [p, ...s.products] })),
}));
