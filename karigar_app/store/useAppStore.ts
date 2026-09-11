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

const defaultCatalog: CatalogResult = {
  title: 'Clay Pottery Bowl',
  title_hi: 'मिट्टी का बर्तन',
  description: 'Handcrafted pottery bowl made from natural clay with a refined finish and artisanal charm.',
  description_hi: 'प्राकृतिक मिट्टी से बना हाथ से निर्मित कढ़ाई वाला बर्तन, सुंदर फिनिश और कारीगरी वाली सुंदरता के साथ।',
  category: 'Home Decor',
  craft_technique: 'Terracotta',
  source_language: 'hi',
};

export const useAppStore = create<AppState>((set) => ({
  selectedLanguage: LANGUAGES[1],

  setLanguage: (lang) => set({ selectedLanguage: lang }),

  currentCatalog: defaultCatalog,
  setCurrentCatalog: (c) => set({ currentCatalog: c }),

  currentImageUri: null,
  setCurrentImageUri: (uri) => set({ currentImageUri: uri }),

  enhancedImageUrl: null,
  setEnhancedImageUrl: (url) => set({ enhancedImageUrl: url }),

  products: [
    {
      id: 'demo-1',
      sku: 'KAR-001',
      title: 'Clay Pottery Bowl',
      title_hi: 'मिट्टी का बर्तन',
      description: 'Handcrafted pottery bowl made from natural clay with a refined finish and artisanal charm.',
      description_hi: 'प्राकृतिक मिट्टी से बना...',
      category: 'Home Decor',
      craft_technique: 'Terracotta',
      material_cost: 180,
      labor_hours: 3,
      base_cost: 540,
      suggested_price: 950,
      confidence_band: 'High',
      source_language: 'hi',
      created_at: new Date().toISOString(),
    },
  ],
  setProducts: (p) => set({ products: p }),
  addProduct: (p) => set((s) => ({ products: [p, ...s.products] })),
}));
