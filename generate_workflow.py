"""
Generates the full end-to-end workflow diagram for the Artisan Backend.
Uses only Pillow (already installed). Output: workflow_diagram.png
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ── Canvas ────────────────────────────────────────────────────────────────────
W, H = 2400, 3200
BG      = (15, 15, 25)        # near-black background
img     = Image.new("RGB", (W, H), BG)
draw    = ImageDraw.Draw(img)

# ── Colour palette ────────────────────────────────────────────────────────────
C = {
    "artisan":   (255, 165,  40),   # orange  — artisan / user
    "api":       ( 60, 160, 255),   # blue    — FastAPI layer
    "ai":        (140,  90, 255),   # purple  — AI models
    "db":        ( 40, 200, 120),   # green   — storage / DB
    "export":    (255,  80, 120),   # red     — marketplace export
    "tts":       (255, 200,  50),   # yellow  — TTS readback
    "arrow":     (180, 180, 200),
    "fallback":  ( 80, 180, 180),   # teal    — fallback path
    "white":     (255, 255, 255),
    "dim":       (140, 140, 160),
    "title_bg":  ( 30,  30,  50),
}

# ── Font helpers ─────────────────────────────────────────────────────────────
def font(size):
    for name in ["arialbd.ttf","arial.ttf","DejaVuSans-Bold.ttf","DejaVuSans.ttf"]:
        for base in [
            "C:/Windows/Fonts/",
            "/usr/share/fonts/truetype/dejavu/",
            "/usr/share/fonts/truetype/msttcorefonts/",
        ]:
            path = base + name
            if os.path.exists(path):
                try: return ImageFont.truetype(path, size)
                except: pass
    return ImageFont.load_default()

F = {
    "title":  font(52),
    "h1":     font(34),
    "h2":     font(26),
    "body":   font(22),
    "small":  font(18),
    "tiny":   font(15),
}

# ── Drawing helpers ───────────────────────────────────────────────────────────
def box(x, y, w, h, color, radius=18, alpha=220):
    """Rounded rect with subtle inner highlight."""
    r, g, b = color
    draw.rounded_rectangle([x, y, x+w, y+h], radius=radius, fill=color,
                            outline=(min(r+60,255), min(g+60,255), min(b+60,255)), width=2)

def text_c(txt, cx, cy, color=C["white"], f="body"):
    """Centre-aligned text."""
    fnt = F[f]
    bb  = draw.textbbox((0,0), txt, font=fnt)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    draw.text((cx - tw//2, cy - th//2), txt, font=fnt, fill=color)

def text_l(txt, x, y, color=C["white"], f="body"):
    draw.text((x, y), txt, font=F[f], fill=color)

def arrow(x1, y1, x2, y2, color=C["arrow"], width=3, label="", dashed=False):
    if dashed:
        # draw dashed line
        import math
        dx, dy = x2-x1, y2-y1
        length = math.hypot(dx, dy)
        ux, uy = dx/length, dy/length
        dash, gap = 14, 8
        d = 0
        while d < length:
            sx = x1 + ux*d;  sy = y1 + uy*d
            ex = x1 + ux*min(d+dash, length); ey = y1 + uy*min(d+dash, length)
            draw.line([(sx,sy),(ex,ey)], fill=color, width=width)
            d += dash + gap
    else:
        draw.line([(x1,y1),(x2,y2)], fill=color, width=width)
    # arrowhead
    import math
    angle = math.atan2(y2-y1, x2-x1)
    hs = 16
    for a in [0.45, -0.45]:
        ax = x2 - hs*math.cos(angle-a)
        ay = y2 - hs*math.sin(angle-a)
        draw.line([(x2,y2),(ax,ay)], fill=color, width=width+1)
    if label:
        mx, my = (x1+x2)//2, (y1+y2)//2
        text_c(label, mx+2, my-14, C["dim"], "tiny")

def badge(x, y, txt, color):
    bb = draw.textbbox((0,0), txt, font=F["tiny"])
    tw = bb[2]-bb[0]+16; th = bb[3]-bb[1]+8
    draw.rounded_rectangle([x, y, x+tw, y+th], radius=6, fill=color)
    draw.text((x+8, y+4), txt, font=F["tiny"], fill=C["white"])
    return tw

# ══════════════════════════════════════════════════════════════════════════════
#  TITLE BANNER
# ══════════════════════════════════════════════════════════════════════════════
draw.rectangle([0, 0, W, 100], fill=C["title_bg"])
draw.rectangle([0, 96, W, 100], fill=C["api"])
text_c("Artisan Backend — End-to-End AI Workflow", W//2, 50, C["white"], "title")

# ── Section label helper ──────────────────────────────────────────────────────
def section_label(x, y, txt, color):
    bb = draw.textbbox((0,0), txt, font=F["h2"])
    tw = bb[2]-bb[0]+24
    draw.rounded_rectangle([x, y, x+tw, y+36], radius=8, fill=color)
    draw.text((x+12, y+6), txt, font=F["h2"], fill=C["white"])

# ══════════════════════════════════════════════════════════════════════════════
#  LAYER 0 — ARTISAN (INPUT)
# ══════════════════════════════════════════════════════════════════════════════
Y0 = 130
section_label(40, Y0, "  STEP 1 — ARTISAN INPUT  ", C["artisan"])

# Three input boxes
inputs = [
    ("🎤  Voice Note", "Regional language\n(Hindi/Tamil/Bengali/\nGujarati/Telugu…)", 200),
    ("📷  Product Photo", "Raw cluttered\nbackground photo\n(JPEG/PNG/WEBM)", 800),
    ("✏️  Manual Entry", "Optional: title,\ncategory, cost,\nlabour hours", 1400),
]
IBW, IBH = 380, 140
IY = Y0 + 60
for label, sub, ix in inputs:
    box(ix, IY, IBW, IBH, C["artisan"], radius=20)
    text_c(label, ix+IBW//2, IY+38, C["white"], "h2")
    for i, line in enumerate(sub.split("\n")):
        text_c(line, ix+IBW//2, IY+72+i*22, (255,230,180), "small")

# ══════════════════════════════════════════════════════════════════════════════
#  LAYER 1 — FastAPI ROUTER
# ══════════════════════════════════════════════════════════════════════════════
Y1 = IY + IBH + 70
section_label(40, Y1-44, "  STEP 2 — FastAPI ROUTER (Python 3.11)  ", C["api"])

routes = [
    ("POST /voice/to-catalog", 200),
    ("POST /image/enhance", 800),
    ("POST /products  or\nPOST /products/full-assembly", 1300),
    ("POST /price/calculate", 1800),
]
RBW, RBH = 360, 72
for label, rx in routes:
    box(rx, Y1, RBW, RBH, C["api"], radius=14)
    for i, line in enumerate(label.split("\n")):
        text_c(line, rx+RBW//2, Y1+20+i*26, C["white"], "small")

# Arrows input → router
arrow(390,  IY+IBH,    390,  Y1,          C["artisan"], label="audio bytes")
arrow(990,  IY+IBH,    990,  Y1,          C["artisan"], label="image bytes")
arrow(1590, IY+IBH,    1590, Y1,          C["artisan"], label="JSON payload")

# ══════════════════════════════════════════════════════════════════════════════
#  LAYER 2 — AI SERVICES
# ══════════════════════════════════════════════════════════════════════════════
Y2 = Y1 + RBH + 80
section_label(40, Y2-44, "  STEP 3 — AI SERVICE LAYER  ", C["ai"])

services = [
    # (label, sublabel, x, color)
    ("voice_engine.py",    "transcribe_audio()\ngenerate_catalog()\ntranslate_pipeline()", 60,   C["ai"]),
    ("image_engine.py",    "compress_image()\nremove_background()\ncomposite_on_white()", 560,  (80, 60, 180)),
    ("price_engine.py",    "_rule_based_price()\n_caption_image()\n_llm_price_advice()",  1060, (120, 40, 160)),
    ("tts_engine.py",      "synthesize_speech()\nMMS multilingual\n14 Indian languages",  1560, (160, 100, 20)),
    ("catalog_engine.py",  "create_product()\nlist_products()\nexport_gem/ondc()",        2060, C["db"]),
]
SBW, SBH = 300, 120
for label, sub, sx, color in services:
    box(sx, Y2, SBW, SBH, color, radius=16)
    text_c(label, sx+SBW//2, Y2+22, C["white"], "h2")
    for i, line in enumerate(sub.split("\n")):
        text_c(line, sx+SBW//2, Y2+52+i*22, (220,210,255), "small")

# Arrows router → services
arrow(390,  Y1+RBH,  210,  Y2,    C["api"], label="audio")
arrow(980,  Y1+RBH,  710,  Y2,    C["api"], label="image")
arrow(1480, Y1+RBH,  1210, Y2,    C["api"], label="meta+img_url")
arrow(1480, Y1+RBH,  1710, Y2,    C["api"], label="text+lang")
arrow(1590, Y1+RBH,  2210, Y2,    C["api"], label="product data")

# ══════════════════════════════════════════════════════════════════════════════
#  LAYER 3 — EXTERNAL AI APIs (HF primary + Replicate fallback)
# ══════════════════════════════════════════════════════════════════════════════
Y3 = Y2 + SBH + 90
section_label(40, Y3-44, "  STEP 4 — EXTERNAL AI APIs  ", C["ai"])

# HF primary row
hf_models = [
    ("HuggingFace\nWhisper large-v3", "Speech-to-Text\n99 languages", 60),
    ("HuggingFace\nNLLB-200", "Translation\n200 languages", 380),
    ("HuggingFace\nMistral-7B-Instruct", "Catalog JSON\n+ Price advice", 700),
    ("HuggingFace\nRMBG-2.0", "Background\nRemoval", 1020),
    ("HuggingFace\nBLIP-large", "Image Caption\nfor Pricing", 1340),
    ("HuggingFace\nMMS-TTS", "Text-to-Speech\n14 Indian langs", 1660),
]
HBW, HBH = 270, 100
HF_COLOR = (40, 100, 200)
for label, sub, hx in hf_models:
    box(hx, Y3, HBW, HBH, HF_COLOR, radius=14)
    text_c("HuggingFace API", hx+HBW//2, Y3+18, (160,200,255), "tiny")
    for i, line in enumerate(label.split("\n")[1:] + sub.split("\n")):
        text_c(line, hx+HBW//2, Y3+34+i*20, C["white"], "small")

# Replicate fallback row
Y3b = Y3 + HBH + 44
rep_models = [
    ("Replicate\nWhisper large-v3", "STT Fallback", 60),
    ("Replicate\nMistral-7B", "Catalog Fallback", 380),
    ("Replicate\nMistral-7B", "Price Fallback", 700),
    ("Replicate\nbg-removal", "BG Remove Fallback", 1020),
]
RBH2 = 80
REP_COLOR = (40, 120, 100)
for label, sub, rx in rep_models:
    box(rx, Y3b, HBW, RBH2, REP_COLOR, radius=14)
    text_c("Replicate API", rx+HBW//2, Y3b+14, (160,230,200), "tiny")
    for i, line in enumerate(label.split("\n")[1:] + [sub]):
        text_c(line, rx+HBW//2, Y3b+30+i*20, C["white"], "small")

# Arrows service → HF models
centers_svc  = [210, 710, 1210, 1710, 2210]
centers_hf   = [195, 515, 835, 1155, 1475, 1795]

arrow(210,  Y2+SBH, 195,  Y3,  C["ai"])   # voice → whisper
arrow(210,  Y2+SBH, 515,  Y3,  C["ai"])   # voice → nllb
arrow(210,  Y2+SBH, 835,  Y3,  C["ai"])   # voice → mistral
arrow(710,  Y2+SBH, 1155, Y3,  C["ai"])   # image → rmbg
arrow(1210, Y2+SBH, 1475, Y3,  C["ai"])   # price → blip
arrow(1210, Y2+SBH, 835,  Y3,  C["ai"])   # price → mistral
arrow(1710, Y2+SBH, 1795, Y3,  C["ai"])   # tts → mms

# Fallback arrows (dashed)
arrow(195,  Y3+HBH, 195,  Y3b, C["fallback"], dashed=True, label="fallback")
arrow(835,  Y3+HBH, 515,  Y3b, C["fallback"], dashed=True, label="fallback")
arrow(835,  Y3+HBH, 835,  Y3b, C["fallback"], dashed=True)
arrow(1155, Y3+HBH, 1155, Y3b, C["fallback"], dashed=True)

# Fallback legend
fx = 1700
draw.rounded_rectangle([fx, Y3b+10, fx+220, Y3b+36], radius=6, fill=(30,30,50), outline=C["fallback"], width=2)
draw.line([(fx+10, Y3b+23),(fx+50, Y3b+23)], fill=C["fallback"], width=2)
# dashes
for d in range(0,40,10):
    draw.line([(fx+10+d, Y3b+23),(fx+10+d+6, Y3b+23)], fill=C["fallback"], width=3)
text_l("= Fallback path", fx+56, Y3b+12, C["fallback"], "small")

# ══════════════════════════════════════════════════════════════════════════════
#  LAYER 4 — PROCESSING RESULTS
# ══════════════════════════════════════════════════════════════════════════════
Y4 = Y3b + RBH2 + 80
section_label(40, Y4-44, "  STEP 5 — PROCESSING RESULTS  ", (60, 140, 60))

results_boxes = [
    ("📝 Multilingual Catalog",
     "title (EN) + title_hi (HI)\n+ title_localized (regional)\ndescription × 3 languages\ncategory + craft_technique",
     60, C["ai"]),
    ("🖼️ Enhanced Image",
     "Background removed\nWhite 1000×1000 canvas\nE-commerce JPEG\nUploaded to Supabase Storage",
     640, (80, 60, 180)),
    ("💰 Smart Price",
     "Rule-based base cost\n+ LLM market adjustment\n+ Image caption signal\nConfidence band",
     1220, (120, 40, 160)),
    ("🔊 Audio Readback",
     "WAV audio in artisan's\nown regional language\nLow-literacy accessible\nMMS-TTS output",
     1800, (160, 100, 20)),
]
RES_W, RES_H = 480, 130
for label, sub, rx, color in results_boxes:
    box(rx, Y4, RES_W, RES_H, color, radius=16)
    text_c(label, rx+RES_W//2, Y4+24, C["white"], "h2")
    for i, line in enumerate(sub.split("\n")):
        text_c(line, rx+RES_W//2, Y4+56+i*20, (220,220,255), "small")

# Arrows AI → results
arrow(515,  Y3b+RBH2, 300,  Y4,    C["ai"])
arrow(1155, Y3b+RBH2, 880,  Y4,    C["ai"])
arrow(835,  Y3b+RBH2, 1460, Y4,    C["ai"])
arrow(1795, Y3+HBH,   2040, Y4,    C["ai"])

# ══════════════════════════════════════════════════════════════════════════════
#  LAYER 5 — SUPABASE PERSISTENCE
# ══════════════════════════════════════════════════════════════════════════════
Y5 = Y4 + RES_H + 80
section_label(40, Y5-44, "  STEP 6 — PERSISTENCE (Supabase / PostgreSQL)  ", C["db"])

db_boxes = [
    ("🗄️ products table",
     "id, sku, title, title_hi\ntitle_localized, description\ndescription_hi, description_localized\nsource_language, category\ncraft_technique, material_cost\nlabor_hours, base_cost\nsuggested_price, confidence_band\nimage_url, audio_url, created_at",
     200, 540, C["db"]),
    ("📦 product-images bucket",
     "White-bg JPEG\n1000×1000px\nPublic URL returned\nFallback: base64 data URI",
     820, 200, (30,150,90)),
    ("📁 exports bucket",
     "GeM CSV files\nONDC JSON files\nTimestamped filenames\nPublic download URLs",
     1100, 200, (30,130,80)),
    ("💾 In-memory fallback",
     "Python dict store\nActive if Supabase down\nData survives restart\nAuto-merged on list",
     1380, 200, (80,80,120)),
]
for label, sub, dbx, dbw, color in db_boxes:
    dbh_calc = 40 + len(sub.split("\n")) * 22 + 20
    box(dbx, Y5, dbw, dbh_calc, color, radius=14)
    text_c(label, dbx+dbw//2, Y5+22, C["white"], "h2")
    for i, line in enumerate(sub.split("\n")):
        text_c(line, dbx+dbw//2, Y5+46+i*22, (200,240,200), "small")

# Arrow results → DB
DB_CX = 470  # center of products table
arrow(300,  Y4+RES_H, DB_CX,  Y5, C["db"])
arrow(880,  Y4+RES_H, 920,    Y5, C["db"])
arrow(1460, Y4+RES_H, DB_CX,  Y5, C["db"])

# ══════════════════════════════════════════════════════════════════════════════
#  LAYER 6 — MARKETPLACE EXPORT
# ══════════════════════════════════════════════════════════════════════════════
Y6 = Y5 + 320
section_label(40, Y6-44, "  STEP 7 — MARKETPLACE EXPORT  ", C["export"])

exp_boxes = [
    ("📊 GeM CSV Export",
     "POST /products/export/gem/csv\n27 columns incl. HSN, MRP,\nGSTIN, Hindi titles,\ncraft technique, audio URL\nUTF-8 BOM (Excel-ready)",
     200, C["export"]),
    ("🌐 ONDC JSON Export",
     "POST /products/export/ondc/json\nBeckn Protocol 2.0.0\nONDC:RET10 domain\nPrice breakup (MRP+GST)\nmake_in_india tags",
     900, (200, 40, 80)),
    ("🔁 Bulk Operations",
     "POST /products/bulk\nUp to 500 products\nPer-row error handling\nAll IDs returned",
     1600, (160, 40, 100)),
]
EBW, EBH = 520, 150
for label, sub, ex, color in exp_boxes:
    box(ex, Y6, EBW, EBH, color, radius=16)
    text_c(label, ex+EBW//2, Y6+24, C["white"], "h1")
    for i, line in enumerate(sub.split("\n")):
        text_c(line, ex+EBW//2, Y6+58+i*22, (255,200,200), "small")

arrow(DB_CX, Y5+280, 460, Y6,    C["db"])
arrow(DB_CX, Y5+280, 1160, Y6,   C["db"])
arrow(DB_CX, Y5+280, 1860, Y6,   C["db"])

# ══════════════════════════════════════════════════════════════════════════════
#  LAYER 7 — FINAL OUTPUT to artisan / marketplace
# ══════════════════════════════════════════════════════════════════════════════
Y7 = Y6 + EBH + 80
section_label(40, Y7-44, "  STEP 8 — FINAL OUTPUT  ", C["tts"])

final_boxes = [
    ("🏪 GeM Marketplace",   "Government e-Marketplace\nbulk upload ready",          200,  (220,80,40)),
    ("📲 ONDC Network",      "Open Network for\nDigital Commerce",                    680,  (180,40,80)),
    ("🔊 Artisan Hears",     "Product read back\nin their language\nvia /voice/tts",  1160, C["tts"]),
    ("📱 Frontend App",      "Any frontend can call\nthese REST endpoints\n(React/Flutter/etc)",  1640, (60,140,200)),
    ("📈 Analytics",         "All data in Supabase\nQueryable via\nPostgres/REST",    2120, C["db"]),
]
FBW, FBH = 340, 110
for label, sub, fx, color in final_boxes:
    box(fx, Y7, FBW, FBH, color, radius=20)
    text_c(label, fx+FBW//2, Y7+24, C["white"], "h2")
    for i, line in enumerate(sub.split("\n")):
        text_c(line, fx+FBW//2, Y7+54+i*22, (255,240,200), "small")

arrow(460,  Y6+EBH, 370,   Y7, C["export"])
arrow(1160, Y6+EBH, 850,   Y7, C["export"])
arrow(1460, Y4+RES_H, 1330, Y7, C["tts"])    # TTS direct to artisan
arrow(DB_CX, Y5+280, 1810,  Y7, C["db"])
arrow(DB_CX, Y5+280, 2290,  Y7, C["db"])

# ══════════════════════════════════════════════════════════════════════════════
#  LEGEND
# ══════════════════════════════════════════════════════════════════════════════
LY = Y7 + FBH + 40
draw.rectangle([40, LY, W-40, LY+90], fill=(25,25,40), outline=(60,60,80), width=1)
text_l("LEGEND:", 70, LY+10, C["dim"], "h2")
legend_items = [
    (C["artisan"],  "Artisan / Input"),
    (C["api"],      "FastAPI Router"),
    (C["ai"],       "AI Service / Model"),
    (C["db"],       "Storage / DB"),
    (C["export"],   "Marketplace Export"),
    (C["tts"],      "TTS Readback"),
    (C["fallback"], "Fallback path (dashed)"),
]
lx = 220
for color, label in legend_items:
    draw.rounded_rectangle([lx, LY+20, lx+28, LY+44], radius=5, fill=color)
    text_l(label, lx+36, LY+22, C["white"], "small")
    lx += len(label)*12 + 60

# ── Footer ────────────────────────────────────────────────────────────────────
draw.rectangle([0, H-44, W, H], fill=C["title_bg"])
text_c("SIH 2026  ·  Artisan Backend  ·  FastAPI + HuggingFace + Replicate + Supabase", 
       W//2, H-22, C["dim"], "small")

# ── Save ──────────────────────────────────────────────────────────────────────
out_path = "workflow_diagram.png"
img.save(out_path, format="PNG", optimize=True)
print(f"Saved: {out_path}  ({W}x{H}px)")
print(f"File size: {os.path.getsize(out_path) / 1024:.1f} KB")
