"""
GoGettr — Volt Brand Kit, codified.
Design tokens + typography helpers for the content-backlog render engine.

Source of truth: "GoGettr Volt Brand Kit" design board.
Colour, type scale, mark rules and voice all mirror the kit.
"""
from PIL import ImageFont
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "assets", "fonts")

# ---------------------------------------------------------------- COLOUR
# 01 — COLOUR (exact hex from the brand board)
GRAPHITE = (35, 38, 43)     # #23262B  primary ground
INK      = (14, 16, 19)     # #0E1013  photo & video ground
CHROME   = (230, 231, 233)  # #E6E7E9  light ground
VOLT     = (214, 255, 46)   # #D6FF2E  accent — one element per post, never text on white
VIOLET   = (123, 77, 255)   # #7B4DFF  second accent — numerals
STEEL    = (108, 114, 124)  # #6C727C  captions, meta, rules
WHITE    = (245, 246, 247)
BLACK    = (0, 0, 0)

# tints used for procedural "photo/video" plates
GRAPHITE_HI = (48, 52, 59)
INK_HI      = (26, 30, 36)
VIOLET_DK   = (58, 40, 120)
VOLT_DK     = (120, 150, 20)

# ---------------------------------------------------------------- TYPE
# 02 — TYPE. Variable TTFs; we pin weights via named/axis variation.
_CACHE = {}

def font(family, size, weight=None):
    """family in {display, mono, body}. size in px. weight overrides default."""
    key = (family, size, weight)
    if key in _CACHE:
        return _CACHE[key]
    if family == "display":     # Space Grotesk
        path, w = os.path.join(FONTS, "SpaceGrotesk-Bold.ttf"), weight or 700
    elif family == "mono":      # JetBrains Mono
        path, w = os.path.join(FONTS, "JetBrainsMono.ttf"), weight or 500
    else:                        # Archivo (body / ui)
        path, w = os.path.join(FONTS, "Archivo.ttf"), weight or 500
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_axes([w] if family != "body" else [100, w])
    except Exception:
        pass
    _CACHE[key] = f
    return f

# type scale on a 1080 artboard (from the board), used as ratios elsewhere
SCALE = {
    "hook_xl": 130, "hook_l": 116, "hook_m": 96, "numeral": 250,
    "sub": 74, "eyebrow": 30, "footer": 28, "body": 40,
}
MARGIN = 96          # side margin on a 1080 board
TOP    = 120         # top/bottom margin on a 1080 board

# ---------------------------------------------------------------- TEXT HELPERS
def _adv(font, ch):
    try:
        return font.getlength(ch)
    except Exception:
        return font.getbbox(ch)[2]

def tracked_width(font, s, tracking=0.0):
    if not s:
        return 0
    return sum(_adv(font, c) for c in s) + tracking * (len(s) - 1)

def draw_tracked(draw, xy, s, font, fill, tracking=0.0, anchor="la"):
    """Draw text with per-character tracking (letter-spacing in px).
    anchor: horizontal l/m/r + vertical a(scent-top)/m/s(baseline-ish). Mimics a subset of PIL anchors."""
    x, y = xy
    w = tracked_width(font, s, tracking)
    ah, av = anchor[0], anchor[1]
    if ah == "m":
        x -= w / 2
    elif ah == "r":
        x -= w
    for c in s:
        draw.text((x, y), c, font=font, fill=fill, anchor="l" + av)
        x += _adv(font, c) + tracking

def wrap_tracked(text, font, max_width, tracking=0.0):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if tracked_width(font, trial, tracking) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines

def draw_paragraph(draw, xy, text, font, fill, max_width, leading, tracking=0.0,
                   anchor_h="l", center_x=None):
    lines = wrap_tracked(text, font, max_width, tracking) if isinstance(text, str) else text
    x, y = xy
    for ln in lines:
        if anchor_h == "m":
            draw_tracked(draw, (center_x, y), ln, font, fill, tracking, anchor="ma")
        else:
            draw_tracked(draw, (x, y), ln, font, fill, tracking, anchor="la")
        y += leading
    return y

def fit_hook(draw, text, box_w, max_size, min_size, family="display",
             tracking_ratio=-0.045, max_lines=4):
    """Pick the largest display size where `text` wraps into <= max_lines within box_w."""
    for size in range(max_size, min_size - 1, -2):
        f = font(family, size, 700)
        tr = size * tracking_ratio
        lines = wrap_tracked(text, f, box_w, tr)
        if len(lines) <= max_lines:
            return f, size, tr, lines
    f = font(family, min_size, 700)
    tr = min_size * tracking_ratio
    return f, min_size, tr, wrap_tracked(text, f, box_w, tr)
