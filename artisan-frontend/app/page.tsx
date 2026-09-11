'use client';

import { ChangeEvent, useEffect, useRef, useState, type ReactNode } from 'react';
import { ArrowRight, BadgeCheck, Globe2, Languages, Mic, Package, Sparkles, Users } from 'lucide-react';

type View = 'studio' | 'products' | 'market';
type Catalog = { title: string; title_hi?: string; description: string; description_hi?: string; category: string; craft_technique: string; transcript_language?: string };
type Product = { name: string; category: string; price: number; status: string; image: string };

type PriceResult = { base_cost: number; suggested_price: number; confidence_band: string };
type LanguageCode = 'hi' | 'en' | 'mr' | 'bn' | 'ta' | 'te';

const languages: { code: LanguageCode; native: string; english: string }[] = [
  { code: 'hi', native: 'हिंदी', english: 'Hindi' },
  { code: 'en', native: 'English', english: 'English' },
  { code: 'mr', native: 'मराठी', english: 'Marathi' },
  { code: 'bn', native: 'বাংলা', english: 'Bengali' },
  { code: 'ta', native: 'தமிழ்', english: 'Tamil' },
  { code: 'te', native: 'తెలుగు', english: 'Telugu' },
];

const copy: Record<LanguageCode, { studio: string; products: string; buyers: string; welcome: string; choose: string; continue: string }> = {
  hi: { studio: 'AI स्टूडियो', products: 'मेरे उत्पाद', buyers: 'ग्राहक खोजें', welcome: 'आपका हुनर, आपका बाज़ार', choose: 'अपनी भाषा चुनें', continue: 'आगे बढ़ें' },
  en: { studio: 'AI Studio', products: 'My products', buyers: 'Find buyers', welcome: 'Your craft, your market', choose: 'Choose your language', continue: 'Continue' },
  mr: { studio: 'AI स्टुडिओ', products: 'माझी उत्पादने', buyers: 'खरेदीदार शोधा', welcome: 'तुमची कला, तुमची बाजारपेठ', choose: 'तुमची भाषा निवडा', continue: 'पुढे जा' },
  bn: { studio: 'AI স্টুডিও', products: 'আমার পণ্য', buyers: 'ক্রেতা খুঁজুন', welcome: 'আপনার কারুশিল্প, আপনার বাজার', choose: 'ভাষা বেছে নিন', continue: 'এগিয়ে যান' },
  ta: { studio: 'AI ஸ்டுடியோ', products: 'என் தயாரிப்புகள்', buyers: 'வாங்குபவர்களைக் கண்டறியவும்', welcome: 'உங்கள் கைவினை, உங்கள் சந்தை', choose: 'மொழியைத் தேர்ந்தெடுக்கவும்', continue: 'தொடரவும்' },
  te: { studio: 'AI స్టూడియో', products: 'నా ఉత్పత్తులు', buyers: 'కొనుగోలుదారులను కనుగొనండి', welcome: 'మీ కళ, మీ మార్కెట్', choose: 'భాషను ఎంచుకోండి', continue: 'కొనసాగించండి' },
};

const starterProducts: Product[] = [
  { name: 'Terracotta Water Pot', category: 'Home & Living', price: 850, status: 'Live listing', image: 'https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&w=700&q=85' },
  { name: 'Handmade Clay Bowl', category: 'Home Decor', price: 950, status: 'Ready to sync', image: 'https://images.unsplash.com/photo-1517705008128-361805f42e86?auto=format&fit=crop&w=700&q=85' },
];

export default function Home() {
  const [view, setView] = useState<View>('studio');
  const [language, setLanguage] = useState<LanguageCode | null>(null);
  const [languageReady, setLanguageReady] = useState(false);
  const [products, setProducts] = useState(starterProducts);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState('');
  const [enhancedImage, setEnhancedImage] = useState('');
  const [catalog, setCatalog] = useState<Catalog | null>(null);
  const [price, setPrice] = useState<PriceResult | null>(null);
  const [materialCost, setMaterialCost] = useState('180');
  const [laborHours, setLaborHours] = useState('3');
  const [category, setCategory] = useState('Pottery');
  const [busy, setBusy] = useState('');
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [recording, setRecording] = useState(false);
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const recorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  useEffect(() => () => { if (imagePreview) URL.revokeObjectURL(imagePreview); }, [imagePreview]);
  useEffect(() => { const saved = window.localStorage.getItem('karigar-language') as LanguageCode | null; setLanguage(saved); setLanguageReady(true); }, []);

  const selectLanguage = (code: LanguageCode) => { setLanguage(code); window.localStorage.setItem('karigar-language', code); };

  if (!languageReady) return null;
  if (!language) return <LanguageChooser onSelect={selectLanguage} />;
  const labels = copy[language];

  const selectImage = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    setImageFile(file);
    setEnhancedImage('');
    setImagePreview(URL.createObjectURL(file));
    setError('');
  };

  const enhanceImage = async () => {
    if (!imageFile) return setError('Choose a product photo first.');
    setBusy('image'); setError('');
    try {
      const body = new FormData(); body.append('file', imageFile);
      const response = await fetch('/api/image/enhance', { method: 'POST', body });
      if (!response.ok) throw new Error(await response.text());
      const data = await response.json(); setEnhancedImage(data.image_url); setNotice('AI cleaned the image and prepared a marketplace-ready white background.');
    } catch (failure) { setError(await apiError(failure, 'Image enhancement failed. Check that the backend is live and its AI keys are configured.')); } finally { setBusy(''); }
  };

  const startRecording = async () => {
    if (!navigator.mediaDevices?.getUserMedia) return setError('Audio recording is not supported in this browser.');
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      audioChunksRef.current = [];
      recorder.ondataavailable = (event) => { if (event.data.size > 0) audioChunksRef.current.push(event.data); };
      recorder.onstop = () => { setAudioFile(new File([new Blob(audioChunksRef.current, { type: recorder.mimeType })], 'artisan-voice.webm', { type: recorder.mimeType })); stream.getTracks().forEach((track) => track.stop()); };
      recorderRef.current = recorder; recorder.start(); setRecording(true); setError('');
    } catch { setError('Microphone permission was denied. You can upload an audio file instead.'); }
  };

  const stopRecording = () => { recorderRef.current?.stop(); setRecording(false); };

  const catalogFromVoice = async () => {
    if (!audioFile) return setError('Record a voice note or upload an audio file first.');
    setBusy('voice'); setError('');
    try {
      const body = new FormData(); body.append('file', audioFile);
      const response = await fetch('/api/voice/to-catalog', { method: 'POST', body });
      if (!response.ok) throw new Error(await response.text());
      const data = await response.json() as Catalog; setCatalog(data); setCategory(data.category || 'Pottery'); setNotice('Voice converted into an English and Hindi catalogue draft.');
    } catch (failure) { setError(await apiError(failure, 'Catalog generation failed. Confirm the backend AI credentials and try again.')); } finally { setBusy(''); }
  };

  const calculatePrice = async () => {
    if (!catalog) return setError('Generate a catalogue before calculating price.');
    setBusy('price'); setError('');
    try {
      const response = await fetch('/api/price/calculate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ material_cost: Number(materialCost), labor_hours: Number(laborHours), category, title: catalog.title, description: catalog.description, craft_technique: catalog.craft_technique }) });
      if (!response.ok) throw new Error(await response.text());
      setPrice(await response.json()); setNotice('Pricing assistant calculated a competitive suggestion from your costs and catalogue details.');
    } catch (failure) { setError(await apiError(failure, 'Pricing failed. Enter valid material and labor costs and confirm the backend is live.')); } finally { setBusy(''); }
  };

  const saveDraft = () => {
    if (!catalog || !price) return setError('Complete the catalogue and pricing steps first.');
    setProducts((items) => [{ name: catalog.title, category: catalog.category, price: price.suggested_price, status: 'AI draft ready', image: enhancedImage || imagePreview || starterProducts[0].image }, ...items]);
    setNotice('AI-generated listing saved to My products.'); setView('products');
  };

  return <main className="app-shell">
    <header className="topbar"><button className="brand-mark" onClick={() => setView('studio')}><span className="brand-dot" /> KARIGAR</button><div className="top-actions"><span className="offline"><span /> AI services connected</span><button className="language-shortcut" onClick={() => { setLanguage(null); window.localStorage.removeItem('karigar-language'); }} title="Change language"><Languages size={16} /> {language}</button><button className="avatar" aria-label="Open profile">M</button></div></header>
    <div className="layout">
      <aside className="sidebar"><div className="profile"><div className="profile-avatar">M</div><div><strong>Namaste, Mitra</strong><span>Verified artisan partner</span></div></div><nav className="side-nav"><NavButton active={view === 'studio'} label={labels.studio} icon={<Sparkles size={18} />} onClick={() => setView('studio')} /><NavButton active={view === 'products'} label={labels.products} icon={<Package size={18} />} onClick={() => setView('products')} /><NavButton active={view === 'market'} label={labels.buyers} icon={<Users size={18} />} onClick={() => setView('market')} /></nav><div className="sidebar-note"><BadgeCheck size={19} /><div><strong>Verified artisan</strong><small>Your craft is protected</small></div></div></aside>
      <section className="workspace">{notice && <button className="notice" onClick={() => setNotice('')}>{notice} <span>×</span></button>}{error && <button className="error-notice" onClick={() => setError('')}>{error} <span>×</span></button>}
        {view === 'studio' && <Studio labels={labels} imagePreview={imagePreview} enhancedImage={enhancedImage} selectImage={selectImage} enhanceImage={enhanceImage} audioFile={audioFile} setAudioFile={setAudioFile} recording={recording} startRecording={startRecording} stopRecording={stopRecording} catalog={catalog} catalogFromVoice={catalogFromVoice} materialCost={materialCost} setMaterialCost={setMaterialCost} laborHours={laborHours} setLaborHours={setLaborHours} category={category} setCategory={setCategory} price={price} calculatePrice={calculatePrice} saveDraft={saveDraft} busy={busy} />}
        {view === 'products' && <Products products={products} onStudio={() => setView('studio')} />}
        {view === 'market' && <Market />}
      </section>
    </div>
  </main>;
}

async function apiError(failure: unknown, fallback: string) {
  if (failure instanceof Error && failure.message) {
    try {
      const parsed = JSON.parse(failure.message);
      return parsed.detail ? `${fallback} ${parsed.detail}` : fallback;
    } catch {
      return fallback;
    }
  }
  return fallback;
}

function Studio(props: { labels: typeof copy.en; imagePreview: string; enhancedImage: string; selectImage: (event: ChangeEvent<HTMLInputElement>) => void; enhanceImage: () => void; audioFile: File | null; setAudioFile: (value: File) => void; recording: boolean; startRecording: () => void; stopRecording: () => void; catalog: Catalog | null; catalogFromVoice: () => void; materialCost: string; setMaterialCost: (value: string) => void; laborHours: string; setLaborHours: (value: string) => void; category: string; setCategory: (value: string) => void; price: PriceResult | null; calculatePrice: () => void; saveDraft: () => void; busy: string }) {
  return <><div className="page-heading"><div><p className="eyebrow">AI-POWERED WORKSPACE • AI सहायता</p><h1>{props.labels.welcome}.</h1><p className="subheading">Prepare a professional listing in three guided steps. Your photo, words, and price work together.</p></div><span className="live-chip">● LIVE AI STUDIO</span></div><div className="studio-grid">
    <section className="studio-card"><Step number="01" title="AI Image Enhancer & Studio" detail="Clean the background, correct the presentation, and prepare a marketplace-ready product image." /><div className="dropzone">{props.enhancedImage || props.imagePreview ? <img src={props.enhancedImage || props.imagePreview} alt="Product preview" /> : <div className="upload-placeholder"><span>＋</span><strong>Drop a product photo here</strong><small>JPG, PNG or WEBP · up to 10 MB</small></div>}<label className="secondary-button">Choose photo<input type="file" accept="image/*" onChange={props.selectImage} /></label></div><button className="primary-button full" onClick={props.enhanceImage} disabled={props.busy === 'image'}>{props.busy === 'image' ? 'Enhancing image…' : '✦ Enhance product photo'}</button>{props.enhancedImage && <span className="success-line">✓ Background cleaned and formatted for commerce</span>}</section>
    <section className="studio-card"><Step number="02" title="Multilingual Auto-Cataloger" detail="Describe your craft in a regional language. AI creates professional English and Hindi copy." /><div className="voice-recorder"><div className={`record-dot ${props.recording ? 'recording' : ''}`} /><div><strong>{props.recording ? 'Listening… speak naturally' : props.audioFile ? 'Voice note ready' : 'Record your product story'}</strong><small>Hindi, Tamil, Bengali, Marathi and more</small></div><button className="record-button" onClick={props.recording ? props.stopRecording : props.startRecording}>{props.recording ? 'Stop' : 'Record'}</button></div><div className="or-line"><span>or upload audio</span></div><label className="audio-upload">Choose audio file<input type="file" accept="audio/*" onChange={(event) => { const file = event.target.files?.[0]; if (file) props.setAudioFile(file); }} /></label><button className="primary-button full" onClick={props.catalogFromVoice} disabled={props.busy === 'voice'}>{props.busy === 'voice' ? 'Generating catalogue…' : '✦ Generate English + Hindi copy'}</button>{props.catalog && <div className="catalog-result"><span className="result-label">AI CATALOGUE DRAFT</span><h3>{props.catalog.title}</h3><h4>{props.catalog.title_hi}</h4><p>{props.catalog.description}</p><p className="hindi-copy">{props.catalog.description_hi}</p><small>{props.catalog.category} · {props.catalog.craft_technique}</small></div>}</section>
    <section className="studio-card pricing-card"><Step number="03" title="Dynamic Pricing Assistant" detail="Combine raw material cost, labor, category, description, and AI market logic into a fair selling price." /><div className="form-row"><label>Material cost (₹)<input type="number" min="0" value={props.materialCost} onChange={(event) => props.setMaterialCost(event.target.value)} /></label><label>Labor hours<input type="number" min="0" step=".5" value={props.laborHours} onChange={(event) => props.setLaborHours(event.target.value)} /></label><label>Category<select value={props.category} onChange={(event) => props.setCategory(event.target.value)}><option>Pottery</option><option>Textiles</option><option>Jewelry</option><option>Woodwork</option><option>Metalwork</option><option>Other</option></select></label></div><button className="primary-button full" onClick={props.calculatePrice} disabled={props.busy === 'price'}>{props.busy === 'price' ? 'Calculating price…' : '₹ Calculate competitive price'}</button>{props.price && <div className="price-result"><div><span>RECOMMENDED SELLING PRICE</span><strong>₹{props.price.suggested_price.toLocaleString('en-IN')}</strong><small>Base cost ₹{props.price.base_cost.toLocaleString('en-IN')} · Confidence {props.price.confidence_band}</small></div><span className="price-badge">AI FAIR<br />PRICE</span></div>}<button className="save-listing" onClick={props.saveDraft} disabled={!props.catalog || !props.price}>Save complete listing →</button></section>
  </div></>;
}

function Step({ number, title, detail }: { number: string; title: string; detail: string }) { return <div className="step-heading"><span className="step-number">{number}</span><div><h2>{title}</h2><p>{detail}</p></div></div>; }
function LanguageChooser({ onSelect }: { onSelect: (code: LanguageCode) => void }) {
  const [selected, setSelected] = useState<LanguageCode>('hi');
  return <main className="language-screen"><div className="language-panel"><div className="language-brand"><span className="brand-dot" /> KARIGAR</div><div className="language-icon"><Globe2 size={30} /></div><p className="eyebrow">WELCOME • स्वागत है</p><h1>Choose your language</h1><h2>अपनी भाषा चुनें</h2><p className="language-intro">Use Karigar in the language that feels most natural to you.</p><div className="language-grid">{languages.map((item) => <button key={item.code} className={`language-card ${selected === item.code ? 'selected' : ''}`} onClick={() => setSelected(item.code)}><span>{item.native}</span><small>{item.english}</small>{selected === item.code && <span className="language-check"><BadgeCheck size={18} /></span>}</button>)}</div><button className="language-continue" onClick={() => onSelect(selected)}><Languages size={18} /> {copy[selected].continue} <ArrowRight size={18} /></button><p className="language-note"><Mic size={14} /> Voice help is available in regional languages</p></div></main>;
}

function NavButton({ active, label, icon, onClick }: { active: boolean; label: string; icon: ReactNode; onClick: () => void }) { return <button className={`nav-button ${active ? 'active' : ''}`} onClick={onClick}><span>{icon}</span>{label}</button>; }
function Products({ products, onStudio }: { products: Product[]; onStudio: () => void }) { return <><div className="page-heading"><div><p className="eyebrow">CATALOGUE</p><h1>My products</h1><p className="subheading">AI-prepared listings ready for buyers.</p></div><button className="primary-button" onClick={onStudio}>＋ Create with AI</button></div><div className="product-list">{products.map((product) => <article className="product-card large" key={`${product.name}-${product.status}`}><img src={product.image} alt="" /><div className="product-info"><div className="status-pill">● {product.status}</div><h3>{product.name}</h3><p>{product.category}</p><strong className="product-price">₹{product.price} <small>/ piece</small></strong></div></article>)}</div></>; }
function Market() { return <><div className="page-heading"><div><p className="eyebrow">MARKETPLACE</p><h1>Find buyers</h1><p className="subheading">Discover verified buyers looking for Indian craft.</p></div></div><div className="buyer-list"><article className="buyer-card"><div className="buyer-avatar">R</div><div className="buyer-info"><div className="buyer-title"><strong>Rajesh Organic Fab</strong><span>★ 4.8</span></div><small>New Delhi</small><p>Currently buying: Terracotta cookware, clay pots and traditional diyas.</p><button className="connect-button" onClick={() => alert('Connection request sent')}>☎ Connect buyer</button></div></article><article className="buyer-card"><div className="buyer-avatar">D</div><div className="buyer-info"><div className="buyer-title"><strong>Delhi Haat Crafts Company</strong><span>★ 4.9</span></div><small>Jaipur, Rajasthan</small><p>Currently buying: Local home decor and hand-finished terracotta pieces.</p><button className="connect-button" onClick={() => alert('Connection request sent')}>☎ Connect buyer</button></div></article></div></>; }
