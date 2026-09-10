"""
Simple, clean workflow diagram — fixed text overlap.
Two-pass: calculate total height first, then draw everything.
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ── fonts ─────────────────────────────────────────────────────────────────────
def font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

FB = {s: font(s, bold=True)  for s in [48, 38, 28, 22, 18]}
FR = {s: font(s, bold=False) for s in [48, 38, 28, 22, 18]}

# ── layout constants ──────────────────────────────────────────────────────────
W          = 1800
CW         = 1600          # card width
LX         = (W - CW) // 2
CX         = W // 2
GAP        = 40            # vertical gap between cards
HEADER_H   = 115
TITLE_H    = 74            # step badge row height
BULLET_H   = 38            # height per bullet
CHIP_H     = 48            # chip row height
PAD_AFTER_TITLE  = 10
PAD_BEFORE_CHIPS = 18
PAD_BOTTOM       = 28
OUTCOME_H  = 110
FOOTER_H   = 90
ARROW_H    = GAP + 20

CLR = {
    "orange": (255, 138,  60),
    "blue":   ( 66, 135, 245),
    "purple": (142,  68, 228),
    "green":  ( 46, 184, 120),
    "red":    (235,  75,  75),
    "yellow": (242, 180,  30),
    "teal":   ( 32, 178, 170),
    "gray":   (160, 165, 180),
    "white":  (255, 255, 255),
    "dark":   ( 30,  35,  50),
    "card":   (255, 255, 255),
    "bg":     (245, 247, 250),
}

# ── steps definition ──────────────────────────────────────────────────────────
STEPS = [
    dict(
        num=1, icon="👨‍🎨", title="Artisan Provides Input",
        accent=CLR["orange"],
        bullets=[
            "Records a voice note in their own language  (Hindi, Tamil, Bengali, Gujarati…)",
            "Takes or uploads a product photo  (any cluttered background is fine)",
            "Optionally enters material cost and labour hours",
        ],
        chips=[
            ("🎤", "Voice Note",    CLR["orange"]),
            ("📷", "Product Photo", CLR["orange"]),
            ("✏️",  "Cost & Hours", CLR["orange"]),
        ],
    ),
    dict(
        num=2, icon="🎙️", title="Voice  →  Text   (Speech Recognition)",
        accent=CLR["purple"],
        bullets=[
            "Whisper large-v3 AI listens to the voice note",
            "Automatically detects the language — artisan does not need to select anything",
            "Converts spoken words to accurate text for any Indian language",
        ],
        chips=[
            ("🤖", "Whisper large-v3  (HuggingFace)", CLR["purple"]),
            ("🔄", "Replicate fallback",               CLR["teal"]),
        ],
    ),
    dict(
        num=3, icon="📝", title="AI Generates a Professional Product Catalog",
        accent=CLR["blue"],
        bullets=[
            "Mistral-7B AI reads the transcript and writes a professional e-commerce listing",
            "Creates title + description in English, Hindi (Devanagari), and the original language",
            "Automatically selects the correct product category and craft technique",
            "NLLB-200 translation model fills any missing language slots",
        ],
        chips=[
            ("🧠", "Mistral-7B-Instruct",    CLR["blue"]),
            ("🌐", "NLLB-200  (translation)", CLR["blue"]),
            ("🔄", "Replicate fallback",      CLR["teal"]),
        ],
    ),
    dict(
        num=4, icon="🖼️", title="AI Cleans the Product Photo",
        accent=CLR["teal"],
        bullets=[
            "RMBG-2.0 AI removes the cluttered background automatically",
            "Product is placed on a clean white 1000 × 1000 canvas  (e-commerce standard)",
            "Brightness, sharpness, and colour are auto-enhanced by Pillow",
            "Final JPEG is uploaded to Supabase Storage — a public URL is returned",
        ],
        chips=[
            ("✂️", "RMBG-2.0  (HuggingFace)", CLR["teal"]),
            ("⬜",  "White canvas composite",  CLR["teal"]),
            ("🔄", "Replicate fallback",       CLR["green"]),
        ],
    ),
    dict(
        num=5, icon="💰", title="AI Suggests the Right Selling Price",
        accent=CLR["yellow"],
        bullets=[
            "Rule engine calculates base cost:  material cost + labour hours × category rate",
            "BLIP AI reads the product photo and writes a visual description of it",
            "Mistral-7B uses the text description + visual caption to suggest a market price",
            "Returns a confidence band:  High / Medium-High / Medium",
        ],
        chips=[
            ("📊", "Rule-based cost engine",  CLR["yellow"]),
            ("👁️",  "BLIP image captioning",  CLR["yellow"]),
            ("🧠", "Mistral-7B pricing",      CLR["yellow"]),
        ],
    ),
    dict(
        num=6, icon="💾", title="Product Record Saved to Database",
        accent=CLR["green"],
        bullets=[
            "Complete product record stored in Supabase  (PostgreSQL)",
            "Stores English + Hindi + regional language fields, image URL, audio URL, price",
            "Falls back to an in-memory store automatically if the database is unreachable",
        ],
        chips=[
            ("🗄️", "Supabase  (PostgreSQL)", CLR["green"]),
            ("📦", "Supabase Storage",        CLR["green"]),
            ("🔒", "In-memory fallback",      CLR["gray"]),
        ],
    ),
    dict(
        num=7, icon="🔊", title="Catalog Read Back to Artisan  (Text-to-Speech)",
        accent=CLR["orange"],
        bullets=[
            "MMS-TTS AI converts the generated catalog text to spoken audio",
            "Artisan hears their own product listing — no reading required",
            "Supports 14 Indian languages  (Hindi, Tamil, Telugu, Bengali, Kannada, Gujarati…)",
        ],
        chips=[
            ("🔊", "Meta MMS-TTS  (HuggingFace)", CLR["orange"]),
            ("🌍", "14 Indian languages",          CLR["purple"]),
        ],
    ),
    dict(
        num=8, icon="🚀", title="Product Goes Live on Government Marketplaces",
        accent=CLR["red"],
        bullets=[
            "One-click export as GeM CSV  (27 columns, UTF-8 BOM, ready for bulk upload)",
            "One-click export as ONDC JSON  (Beckn Protocol 2.0 — reaches all ONDC buyer apps)",
            "Both exports include Hindi titles, HSN codes, GSTIN, MRP, and craft technique tags",
        ],
        chips=[
            ("📊", "GeM CSV  (27 columns)", CLR["red"]),
            ("🌐", "ONDC Beckn 2.0 JSON",  CLR["red"]),
            ("🏷️",  "HSN + GSTIN + MRP",   CLR["red"]),
        ],
    ),
]

# ── card height calculator ─────────────────────────────────────────────────────
def card_h(step):
    h = TITLE_H + PAD_AFTER_TITLE
    h += len(step["bullets"]) * BULLET_H
    h += PAD_BEFORE_CHIPS
    if step.get("chips"):
        h += CHIP_H
    h += PAD_BOTTOM
    return h

# ── PASS 1: compute total canvas height ───────────────────────────────────────
total_h = HEADER_H + GAP
for i, step in enumerate(STEPS):
    total_h += card_h(step)
    total_h += ARROW_H   # arrow after each card (incl. last — outcome box follows)
total_h += OUTCOME_H + GAP + FOOTER_H + 20

# ── create canvas ─────────────────────────────────────────────────────────────
img  = Image.new("RGB", (W, total_h), CLR["bg"])
draw = ImageDraw.Draw(img)

# ── helpers ───────────────────────────────────────────────────────────────────
def tc(text, cx, cy, color, fnt):
    bb = draw.textbbox((0, 0), text, font=fnt)
    draw.text((cx - (bb[2]-bb[0])//2, cy - (bb[3]-bb[1])//2), text, font=fnt, fill=color)

def tl(text, x, y, color, fnt):
    draw.text((x, y), text, font=fnt, fill=color)

def down_arrow(cx, y_top, y_bot, color):
    mid = y_bot - 16
    draw.line([(cx, y_top), (cx, mid)], fill=color, width=5)
    draw.polygon([(cx-13, mid), (cx+13, mid), (cx, y_bot)], fill=color)

def draw_card(step, y):
    x, w = LX, CW
    h = card_h(step)
    accent = step["accent"]

    # shadow
    draw.rounded_rectangle([x+5, y+5, x+w+5, y+h+5], radius=22, fill=(205, 210, 220))
    # body
    draw.rounded_rectangle([x, y, x+w, y+h], radius=22,
                            fill=CLR["card"], outline=accent, width=3)
    # left accent stripe
    draw.rounded_rectangle([x, y, x+12, y+h], radius=8, fill=accent)

    # step number badge
    draw.ellipse([x+26, y+18, x+74, y+66], fill=accent)
    tc(str(step["num"]), x+50, y+42, CLR["white"], FB[28])

    # title row
    tl(step["icon"] + "  " + step["title"], x+90, y+22, CLR["dark"], FB[28])

    # bullets
    by = y + TITLE_H + PAD_AFTER_TITLE
    for bullet in step["bullets"]:
        draw.ellipse([x+98, by+12, x+110, by+24], fill=accent)
        tl(bullet, x+118, by+6, (55, 60, 75), FR[22])
        by += BULLET_H

    # chips
    if step.get("chips"):
        chip_y = by + PAD_BEFORE_CHIPS
        chip_x = x + 90
        for c_icon, c_text, c_color in step["chips"]:
            r, g, b = c_color
            cw = len(c_text) * 13 + 58
            # light tint fill
            draw.rounded_rectangle(
                [chip_x, chip_y, chip_x+cw, chip_y+CHIP_H-6],
                radius=10,
                fill=(min(r+158, 255), min(g+158, 255), min(b+158, 255)),
                outline=c_color, width=2
            )
            tl(c_icon + "  " + c_text, chip_x+10, chip_y+11, (25, 28, 45), FR[18])
            chip_x += cw + 16

    return y + h  # bottom y of card

# ══════════════════════════════════════════════════════════════════════════════
#  PASS 2: DRAW EVERYTHING
# ══════════════════════════════════════════════════════════════════════════════

# Header
draw.rectangle([0, 0, W, HEADER_H], fill=CLR["dark"])
draw.rectangle([0, HEADER_H-4, W, HEADER_H], fill=CLR["blue"])
tc("Artisan AI Platform — How It Works", W//2, 52, CLR["white"], FB[48])
tc("From artisan's voice / photo  →  live on GeM & ONDC marketplace",
   W//2, 92, (155, 178, 225), FR[22])

cy = HEADER_H + GAP

for i, step in enumerate(STEPS):
    bottom = draw_card(step, cy)

    # arrow to next card / outcome
    arrow_color = step["accent"]
    down_arrow(CX, bottom, bottom + ARROW_H - 6, arrow_color)

    cy = bottom + ARROW_H

# Outcome box
ox, oy = LX, cy
draw.rounded_rectangle([ox+5, oy+5, ox+CW+5, oy+OUTCOME_H+5], radius=20, fill=(175, 185, 198))
draw.rounded_rectangle([ox, oy, ox+CW, oy+OUTCOME_H], radius=20,
                        fill=CLR["dark"], outline=CLR["green"], width=4)
tc("✅   Artisan's product is now live on GeM & ONDC", CX, oy+36, CLR["white"], FB[28])
tc("Reachable by crores of buyers across India — year-round, no physical fair needed",
   CX, oy+76, (160, 230, 180), FR[22])

# Footer tech strip
fy = oy + OUTCOME_H + 30
draw.rectangle([0, fy, W, fy + FOOTER_H], fill=(232, 235, 242))
draw.line([(0, fy), (W, fy)], fill=(195, 200, 212), width=2)

tl("Tech Stack:", LX + 20, fy + 24, (100, 105, 120), FB[22])
techs = [
    ("⚡", "FastAPI",       CLR["blue"]),
    ("🤖", "HuggingFace",  CLR["purple"]),
    ("🔄", "Replicate",    CLR["teal"]),
    ("🗄️",  "Supabase",    CLR["green"]),
    ("🖼️",  "Pillow",      CLR["teal"]),
    ("🐍", "Python 3.11",  (55, 120, 70)),
]
tx = LX + 160
for t_icon, t_label, t_color in techs:
    r, g, b = t_color
    cw = len(t_label) * 13 + 56
    draw.rounded_rectangle([tx, fy+14, tx+cw, fy+FOOTER_H-14],
                            radius=10,
                            fill=(min(r+155,255), min(g+155,255), min(b+155,255)),
                            outline=t_color, width=2)
    tl(t_icon + "  " + t_label, tx+10, fy+22, (25, 28, 45), FR[18])
    tx += cw + 16

# ── save ──────────────────────────────────────────────────────────────────────
import pathlib
out = str(pathlib.Path(__file__).parent / "workflow_simple.png")
img.save(out, format="PNG", optimize=True)
print(f"Saved: {out}  ({W} x {total_h} px)  {os.path.getsize(out)//1024} KB")
