"""
Clean workflow diagram — no overlapping, fixed geometry, no emoji dependency.
All sizing is calculated explicitly before drawing anything.
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ── Constants ─────────────────────────────────────────────────────────────────
W          = 1600
MARGIN     = 60
CARD_W     = W - 2 * MARGIN
BULLET_H   = 30        # px per bullet line
CHIP_H     = 36        # chip pill height
CHIP_PAD_X = 18        # chip horizontal padding
CHIP_GAP   = 12        # gap between chips
CARD_PAD_T = 24        # card top padding
CARD_PAD_B = 24        # card bottom padding
TITLE_H    = 44        # title row height
BADGE_R    = 22        # step badge radius
SECTION_H  = 40        # section label height
ARROW_H    = 54        # space reserved for arrow between cards
STEP_GAP   = 20        # extra gap below arrow

# ── Palette ───────────────────────────────────────────────────────────────────
P = {
    "bg":     (240, 243, 248),
    "card":   (255, 255, 255),
    "shadow": (210, 215, 225),
    "dark":   ( 28,  32,  46),
    "body":   ( 55,  60,  80),
    "dim":    (130, 135, 155),
    "white":  (255, 255, 255),
    # accents
    "orange": (242, 120,  40),
    "purple": (130,  70, 220),
    "blue":   ( 52, 120, 240),
    "teal":   ( 22, 170, 160),
    "yellow": (210, 160,  20),
    "green":  ( 38, 170, 100),
    "red":    (220,  55,  55),
    "gray":   (130, 135, 155),
}

# chip tint = very light version of accent
def tint(color, strength=0.15):
    r, g, b = color
    return (
        int(r + (255-r)*(1-strength)),
        int(g + (255-g)*(1-strength)),
        int(b + (255-b)*(1-strength)),
    )

# ── Font loader ───────────────────────────────────────────────────────────────
def load_font(size, bold=False):
    names = (
        ["arialbd.ttf","calibrib.ttf","verdanab.ttf"] if bold
        else ["arial.ttf","calibri.ttf","verdana.ttf","DejaVuSans.ttf"]
    )
    dirs = ["C:/Windows/Fonts/",
            "/usr/share/fonts/truetype/msttcorefonts/",
            "/usr/share/fonts/truetype/dejavu/"]
    for d in dirs:
        for n in names:
            p = d + n
            if os.path.exists(p):
                try: return ImageFont.truetype(p, size)
                except: pass
    return ImageFont.load_default()

F = {
    "title":  load_font(30, bold=True),
    "badge":  load_font(24, bold=True),
    "body":   load_font(22, bold=False),
    "chip":   load_font(19, bold=False),
    "header": load_font(44, bold=True),
    "sub":    load_font(20, bold=False),
    "section":load_font(20, bold=True),
    "footer": load_font(19, bold=False),
    "outcome":load_font(22, bold=True),
}

# ── Measure text ──────────────────────────────────────────────────────────────
_dummy = ImageDraw.Draw(Image.new("RGB", (1,1)))
def measure(text, fnt):
    bb = _dummy.textbbox((0,0), text, font=fnt)
    return bb[2]-bb[0], bb[3]-bb[1]

# ── Pre-calculate card height ─────────────────────────────────────────────────
def card_height(bullets, chips):
    """Returns the exact pixel height a card will need."""
    h = CARD_PAD_T
    h += TITLE_H          # step badge + title
    h += 10               # gap after title
    h += len(bullets) * BULLET_H
    h += 16               # gap before chips
    h += CHIP_H
    h += CARD_PAD_B
    return h

# ── Step data ─────────────────────────────────────────────────────────────────
STEPS = [
    {
        "num": 1,
        "title": "Artisan Provides Input",
        "accent": P["orange"],
        "bullets": [
            "Records a voice note in their own regional language",
            "Takes or uploads a product photo (any background)",
            "Optionally types material cost and labour hours",
        ],
        "chips": [
            ("Voice Note",    P["orange"]),
            ("Product Photo", P["orange"]),
            ("Cost & Hours",  P["orange"]),
        ],
    },
    {
        "num": 2,
        "title": "Voice  ->  Text   (Speech Recognition)",
        "accent": P["purple"],
        "bullets": [
            "Whisper large-v3 AI listens to the voice note",
            "Automatically detects the spoken language",
            "Converts speech to text in any Indian language",
        ],
        "chips": [
            ("Whisper large-v3  (HuggingFace)", P["purple"]),
            ("Replicate fallback",              P["teal"]),
        ],
    },
    {
        "num": 3,
        "title": "AI Writes the Product Catalog",
        "accent": P["blue"],
        "bullets": [
            "Mistral-7B reads the transcript and writes a professional listing",
            "Produces title + description in English, Hindi, and original language",
            "Picks the right product category and craft technique automatically",
            "NLLB-200 fills any missing translation slots",
        ],
        "chips": [
            ("Mistral-7B-Instruct",    P["blue"]),
            ("NLLB-200 Translation",   P["blue"]),
            ("Replicate fallback",     P["teal"]),
        ],
    },
    {
        "num": 4,
        "title": "AI Cleans the Product Photo",
        "accent": P["teal"],
        "bullets": [
            "RMBG-2.0 removes the cluttered background",
            "Product placed on a clean white 1000x1000 canvas",
            "Brightness, sharpness and colour auto-enhanced",
            "Saved to cloud storage — public URL returned",
        ],
        "chips": [
            ("RMBG-2.0 bg removal",  P["teal"]),
            ("White canvas 1000px",  P["teal"]),
            ("Replicate fallback",   P["green"]),
        ],
    },
    {
        "num": 5,
        "title": "AI Suggests the Right Selling Price",
        "accent": P["yellow"],
        "bullets": [
            "Rule engine calculates base cost from materials + labour + category rates",
            "BLIP AI captions the product photo for visual quality signals",
            "Mistral-7B adjusts price using description and photo caption",
            "Returns a confidence band:  High / Medium-High / Medium",
        ],
        "chips": [
            ("Rule-based engine",      P["yellow"]),
            ("BLIP image captioning",  P["yellow"]),
            ("Mistral-7B pricing",     P["yellow"]),
        ],
    },
    {
        "num": 6,
        "title": "Product Saved to Database",
        "accent": P["green"],
        "bullets": [
            "Full product record stored in Supabase (PostgreSQL)",
            "Stores English + Hindi + regional language fields, image URL, price",
            "Falls back to in-memory store if database is unreachable",
        ],
        "chips": [
            ("Supabase PostgreSQL", P["green"]),
            ("Supabase Storage",    P["green"]),
            ("In-memory fallback",  P["gray"]),
        ],
    },
    {
        "num": 7,
        "title": "Catalog Read Back to Artisan",
        "accent": P["orange"],
        "bullets": [
            "MMS-TTS AI converts the catalog text to spoken audio",
            "Artisan hears their listing — no reading required",
            "Supports Hindi, Tamil, Telugu, Bengali, Gujarati, Kannada and more",
        ],
        "chips": [
            ("Meta MMS-TTS  (HuggingFace)", P["orange"]),
            ("14 Indian languages",         P["red"]),
        ],
    },
    {
        "num": 8,
        "title": "Listed on Government Marketplaces",
        "accent": P["red"],
        "bullets": [
            "One click exports all products as a GeM CSV (27 columns, Excel-ready)",
            "One click exports ONDC Beckn 2.0 JSON for all ONDC buyer apps",
            "Exports include Hindi titles, HSN codes, GSTIN, MRP and craft technique",
        ],
        "chips": [
            ("GeM CSV  27 cols",    P["red"]),
            ("ONDC Beckn 2.0 JSON", P["red"]),
            ("HSN + GSTIN + MRP",   P["red"]),
        ],
    },
]

# ── Calculate total canvas height ─────────────────────────────────────────────
HEADER_H   = 120
OUTCOME_H  = 80
FOOTER_H   = 70
PADDING_TOP = 20

total_h = HEADER_H + PADDING_TOP
for i, s in enumerate(STEPS):
    total_h += card_height(s["bullets"], s["chips"])
    if i < len(STEPS) - 1:
        total_h += ARROW_H + STEP_GAP

total_h += 40              # gap before outcome
total_h += OUTCOME_H
total_h += 30              # gap before footer
total_h += FOOTER_H
total_h += 30              # bottom padding

# ── Create canvas ─────────────────────────────────────────────────────────────
img  = Image.new("RGB", (W, total_h), P["bg"])
draw = ImageDraw.Draw(img)

# ── Draw helpers ──────────────────────────────────────────────────────────────
def rbox(x1, y1, x2, y2, fill, outline=None, r=16, width=2):
    draw.rounded_rectangle([x1,y1,x2,y2], radius=r,
                            fill=fill, outline=outline or fill, width=width)

def put_text(text, x, y, fnt, color):
    draw.text((x, y), text, font=fnt, fill=color)

def put_text_c(text, cx, cy, fnt, color):
    w_, h_ = measure(text, fnt)
    draw.text((cx - w_//2, cy - h_//2), text, font=fnt, fill=color)

def draw_arrow_down(cx, y_top, y_bot, color):
    shaft_bot = y_bot - 12
    draw.line([(cx, y_top),(cx, shaft_bot)], fill=color, width=4)
    # triangle head
    draw.polygon([(cx-11, shaft_bot),(cx+11, shaft_bot),(cx, y_bot)], fill=color)

def draw_chip(draw_, x, y, text, accent):
    tw_, _ = measure(text, F["chip"])
    cw = tw_ + CHIP_PAD_X * 2
    # background tint fill
    rbox(x, y, x+cw, y+CHIP_H, fill=tint(accent, 0.18),
         outline=accent, r=CHIP_H//2, width=2)
    put_text(text, x + CHIP_PAD_X, y + (CHIP_H - measure(text, F["chip"])[1])//2,
             F["chip"], accent)
    return cw  # return width consumed

# ── DRAW HEADER ───────────────────────────────────────────────────────────────
rbox(0, 0, W, HEADER_H, fill=P["dark"])
put_text_c("Artisan AI Platform  —  How It Works",
           W//2, 46, F["header"], P["white"])
put_text_c("Voice / Photo  ->  AI Processing  ->  Live on GeM & ONDC",
           W//2, 94, F["sub"], (170, 185, 215))

# ── DRAW CARDS ────────────────────────────────────────────────────────────────
cy = HEADER_H + PADDING_TOP

for idx, step in enumerate(STEPS):
    accent  = step["accent"]
    bullets = step["bullets"]
    chips   = step["chips"]
    ch      = card_height(bullets, chips)

    x1, y1 = MARGIN,         cy
    x2, y2 = MARGIN + CARD_W, cy + ch

    # -- shadow
    rbox(x1+5, y1+5, x2+5, y2+5, fill=P["shadow"], r=20)

    # -- card body
    rbox(x1, y1, x2, y2, fill=P["card"], outline=accent, r=20, width=2)

    # -- left accent bar
    draw.rounded_rectangle([x1, y1, x1+8, y2], radius=20, fill=accent)

    # -- step badge (circle)
    bx = x1 + 28
    by = y1 + CARD_PAD_T
    brad = BADGE_R
    draw.ellipse([bx, by, bx + brad*2, by + brad*2], fill=accent)
    put_text_c(str(step["num"]), bx+brad, by+brad, F["badge"], P["white"])

    # -- title
    tx = bx + brad*2 + 16
    ty = by + (brad*2 - measure(step["title"], F["title"])[1])//2
    put_text(step["title"], tx, ty, F["title"], P["dark"])

    # -- bullets
    bullet_x = x1 + 36
    by_start = y1 + CARD_PAD_T + TITLE_H + 10
    for i, b in enumerate(bullets):
        dot_x = bullet_x + 4
        dot_y = by_start + i*BULLET_H + 10
        draw.ellipse([dot_x, dot_y, dot_x+8, dot_y+8], fill=accent)
        put_text(b, bullet_x + 20, by_start + i*BULLET_H + 2,
                 F["body"], P["body"])

    # -- chips row  (always fits — positioned from bottom of card)
    chip_y = y2 - CARD_PAD_B - CHIP_H
    chip_x = x1 + 36

    for chip_text, chip_color in chips:
        cw = draw_chip(draw, chip_x, chip_y, chip_text, chip_color)
        chip_x += cw + CHIP_GAP

    cy += ch

    # -- arrow between cards
    if idx < len(STEPS) - 1:
        arrow_cx  = W // 2
        arrow_top = cy + 8
        arrow_bot = cy + ARROW_H - 8
        draw_arrow_down(arrow_cx, arrow_top, arrow_bot, accent)
        cy += ARROW_H + STEP_GAP

# ── OUTCOME BOX ───────────────────────────────────────────────────────────────
cy += 40
ox1, oy1 = MARGIN,         cy
ox2, oy2 = MARGIN + CARD_W, cy + OUTCOME_H

rbox(ox1+4, oy1+4, ox2+4, oy2+4, fill=P["shadow"], r=20)
rbox(ox1, oy1, ox2, oy2, fill=P["dark"], outline=P["green"], r=20, width=3)

outcome_text = "Artisan's product is now live on GeM & ONDC — reachable by crores of buyers across India"
put_text_c(outcome_text, W//2, cy + OUTCOME_H//2, F["outcome"], P["white"])

cy += OUTCOME_H

# ── FOOTER TECH STRIP ─────────────────────────────────────────────────────────
fy = cy + 30
draw.rectangle([0, fy, W, fy + FOOTER_H], fill=(228, 232, 242))
draw.line([(0, fy),(W, fy)], fill=(200,206,218), width=2)

techs = [
    ("FastAPI",      P["blue"]),
    ("HuggingFace",  P["purple"]),
    ("Replicate",    P["teal"]),
    ("Supabase",     P["green"]),
    ("Pillow",       P["teal"]),
    ("Python 3.11",  (60, 130, 70)),
]

label_text = "Tech Stack:"
lw, lh = measure(label_text, F["section"])
put_text(label_text,
         MARGIN, fy + (FOOTER_H - lh)//2,
         F["section"], P["dim"])

tx = MARGIN + lw + 24
for tech, color in techs:
    tw_, th_ = measure(tech, F["footer"])
    pad = 14
    bw  = tw_ + pad*2
    bh  = th_ + 12
    bx1 = tx
    by1 = fy + (FOOTER_H - bh)//2
    bx2, by2 = bx1+bw, by1+bh
    rbox(bx1, by1, bx2, by2,
         fill=tint(color, 0.18), outline=color, r=bh//2, width=2)
    put_text(tech, bx1+pad, by1+6, F["footer"], color)
    tx += bw + 10

# ── SAVE ──────────────────────────────────────────────────────────────────────
final_h = fy + FOOTER_H + 20
img_out = img.crop((0, 0, W, final_h))
out_path = "workflow_clean.png"
img_out.save(out_path, "PNG", optimize=True)
print(f"Saved: {out_path}  ({W} x {final_h} px)  {os.path.getsize(out_path)//1024} KB")
