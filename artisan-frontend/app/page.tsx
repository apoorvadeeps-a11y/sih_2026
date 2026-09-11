'use client';

import { useState } from 'react';

type Product = { name: string; category: string; price: number; status: string; image: string };

const starterProducts: Product[] = [
  { name: 'Terracotta Water Pot', category: 'Home & Living', price: 850, status: 'Live listing', image: 'https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&w=700&q=85' },
  { name: 'Handmade Clay Bowl', category: 'Home Decor', price: 950, status: 'Ready to sync', image: 'https://images.unsplash.com/photo-1517705008128-361805f42e86?auto=format&fit=crop&w=700&q=85' },
];

const buyers = [
  { name: 'Rajesh Organic Fab', location: 'New Delhi', rating: '4.8', need: 'Terracotta cookware, clay pots and traditional diyas' },
  { name: 'Delhi Haat Crafts Company', location: 'Jaipur, Rajasthan', rating: '4.9', need: 'Local home decor and hand-finished terracotta pieces' },
];

export default function Home() {
  const [activeView, setActiveView] = useState<'home' | 'products' | 'market'>('home');
  const [products, setProducts] = useState(starterProducts);
  const [notice, setNotice] = useState('');

  const addListing = () => {
    setProducts((items) => [{ ...starterProducts[0], name: 'New artisan listing', status: 'Draft saved' }, ...items]);
    setNotice('Your new listing is saved locally and ready for review.');
    setActiveView('products');
  };

  return (
    <main className="app-shell">
      <header className="topbar"><div className="brand-mark"><span className="brand-dot" /> KARIGAR</div><div className="top-actions"><span className="offline"><span /> Offline mode active</span><button className="avatar" aria-label="Open profile">M</button></div></header>
      <div className="layout">
        <aside className="sidebar"><div className="profile"><div className="profile-avatar">M</div><div><strong>Namaste, Mitra</strong><span>Verified artisan partner</span></div></div><nav className="side-nav" aria-label="Main navigation"><NavButton active={activeView === 'home'} label="Overview" icon="⌂" onClick={() => setActiveView('home')} /><NavButton active={activeView === 'products'} label="My products" icon="▣" onClick={() => setActiveView('products')} /><NavButton active={activeView === 'market'} label="Find buyers" icon="♧" onClick={() => setActiveView('market')} /></nav><div className="sidebar-note"><span>✓</span><div><strong>Verified artisan</strong><small>Your craft is protected</small></div></div></aside>
        <section className="workspace">{notice && <button className="notice" onClick={() => setNotice('')}>{notice} <span>×</span></button>}{activeView === 'home' && <Overview onAdd={addListing} onProducts={() => setActiveView('products')} onMarket={() => setActiveView('market')} products={products} />}{activeView === 'products' && <Products products={products} onAdd={addListing} />}{activeView === 'market' && <Market />}</section>
      </div>
    </main>
  );
}

function NavButton({ active, label, icon, onClick }: { active: boolean; label: string; icon: string; onClick: () => void }) { return <button className={`nav-button ${active ? 'active' : ''}`} onClick={onClick}><span>{icon}</span>{label}</button>; }
function Overview({ onAdd, onProducts, onMarket, products }: { onAdd: () => void; onProducts: () => void; onMarket: () => void; products: Product[] }) { return <><div className="page-heading"><div><p className="eyebrow">WELCOME • स्वागतम्</p><h1>Your craft, your market.</h1><p className="subheading">Turn your handmade work into listings buyers can discover.</p></div><button className="primary-button" onClick={onAdd}>＋ New listing</button></div><div className="voice-banner"><div className="voice-icon">◉</div><div><span>VOICE HELP • बोलें</span><strong>Speak to sell or get help</strong></div><button onClick={onAdd}>Start</button></div><div className="stat-grid"><Stat label="Live listings" value={products.length.toString()} detail="+1 this week" /><Stat label="Interested buyers" value="3" detail="Near Jaipur" /><Stat label="This month" value="₹12,450" detail="Estimated earnings" /></div><div className="section-heading"><div><p className="eyebrow">YOUR WORK</p><h2>Recent listings</h2></div><button className="text-button" onClick={onProducts}>View all →</button></div><div className="product-grid">{products.slice(0, 2).map((product) => <ProductCard key={product.name} product={product} />)}</div><div className="section-heading buyer-heading"><div><p className="eyebrow">MARKETPLACE</p><h2>Find the right buyers</h2></div><button className="text-button" onClick={onMarket}>Explore →</button></div><div className="buyer-preview"><span className="buyer-count">3</span><div><strong>Active buyers near your workshop</strong><p>Connect with people looking for handmade products.</p></div><button className="round-arrow" onClick={onMarket}>→</button></div></>; }
function Products({ products, onAdd }: { products: Product[]; onAdd: () => void }) { return <><div className="page-heading"><div><p className="eyebrow">CATALOGUE</p><h1>My products</h1><p className="subheading">Manage listings and keep your catalogue ready for buyers.</p></div><button className="primary-button" onClick={onAdd}>＋ New listing</button></div><div className="product-list">{products.map((product) => <ProductCard key={product.name} product={product} large />)}</div></>; }
function Market() { return <><div className="page-heading"><div><p className="eyebrow">MARKETPLACE</p><h1>Find buyers</h1><p className="subheading">Discover verified buyers looking for Indian craft.</p></div><button className="filter-button">⌕ Search buyers</button></div><div className="category-row"><button className="category active">Clay & pottery</button><button className="category">Textiles</button><button className="category">Brass craft</button></div><div className="buyer-list">{buyers.map((buyer) => <article className="buyer-card" key={buyer.name}><div className="buyer-avatar">{buyer.name[0]}</div><div className="buyer-info"><div className="buyer-title"><strong>{buyer.name}</strong><span>★ {buyer.rating}</span></div><small>{buyer.location}</small><p>Currently buying: {buyer.need}</p><button className="connect-button" onClick={() => alert(`Connection request sent to ${buyer.name}`)}>☎ Connect buyer</button></div></article>)}</div></>; }
function Stat({ label, value, detail }: { label: string; value: string; detail: string }) { return <div className="stat"><span>{label}</span><strong>{value}</strong><small>{detail}</small></div>; }
function ProductCard({ product, large = false }: { product: Product; large?: boolean }) { return <article className={`product-card ${large ? 'large' : ''}`}><img src={product.image} alt="" /><div className="product-info"><div className="status-pill">● {product.status}</div><h3>{product.name}</h3><p>{product.category}</p><strong className="product-price">₹{product.price} <small>/ piece</small></strong><button className="edit-button">Edit listing →</button></div></article>; }
