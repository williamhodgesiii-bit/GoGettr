# -*- coding: utf-8 -*-
"""
GoGettr — Volt Brand Kit, codified.
Design tokens, typography and text metrics for the content-backlog engine.

Source of truth: "GoGettr Instagram design board" (Volt Brand Kit v1, 2026).

Everything here measures before it draws. `ink_bbox` returns the real inked
box of a tracked string, which is what the layout engine stacks against — so
a rule, a bar or a footer can never land on a descender.
"""
from PIL import ImageFont
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "assets", "fonts")

# ---------------------------------------------------------------- COLOUR
# 01 — COLOUR (exact hex from the brand board)
GRAPHITE = (35, 38, 43)     # #23262B  primary ground · 45%
INK      = (14, 16, 19)     # #0E1013  photo & video ground · 15%
CHROME   = (230, 231, 233)  # #E6E7E9  light ground · 28%
VOLT     = (214, 255, 46)   # #D6FF2E  accent · 9% · never type on white
VIOLET   = (123, 77, 255)   # #7B4DFF  second accent · 3% · numerals
STEEL    = (108, 114, 124)  # #6C727C  captions, meta, rules
WHITE    = (245, 246, 247)
BLACK    = (0, 0, 0)

# tints used for procedural plates (the board's "photo" slots)
GRAPHITE_HI = (48, 52, 59)
INK_HI      = (26, 30, 36)
VIOLET_DK   = (58, 40, 120)
VIOLET_HI   = (142, 102, 255)
VOLT_DK     = (120, 150, 20)
CHROME_LO   = (214, 216, 219)

# ink-on-light greys (board captions sit at ~62% black, not steel-on-white)
INK_SOFT  = (74, 79, 88)
INK_FAINT = (128, 134, 143)

# ---------------------------------------------------------------- TYPE
# 02 — TYPE. Variable TTFs; weights pinned via axis variation.
_CACHE = {}

def font(family, size, weight=None):
    """family in {display, mono, body}. size in px. weight overrides default."""
    size = max(8, int(round(size)))
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

# 03 — SCALE on a 1080 artboard (from the board)
SCALE = {
    "hook_xl": 130, "hook_l": 116, "hook_m": 96, "numeral": 250,
    "sub": 74, "eyebrow": 30, "footer": 28, "body": 40,
}
HOOK_TRACK = -0.045     # board: tracking −4.5%
HOOK_LEAD  = 1.02       # board: leading 0.98–1.02
LABEL_TRACK = 0.18      # board: 0.16–0.22em on mono labels
MARGIN = 96             # 96px side on a 1080-wide artboard
TOP    = 120            # 120px top/bottom
FOOTER_OFFSET = 74      # "Footer row 74px off the bottom"

# ---------------------------------------------------------------- METRICS
def _adv(f, ch):
    try:
        return f.getlength(ch)
    except Exception:
        return f.getbbox(ch)[2]

def tracked_width(f, s, tracking=0.0):
    if not s:
        return 0.0
    return sum(_adv(f, c) for c in s) + tracking * (len(s) - 1)

def ink_bbox(f, s, tracking=0.0):
    """Real inked box of `s` drawn at (0,0) with anchor 'la'.
    Returns (x0, y0, x1, y1); y is measured down from the ascender line."""
    x, box = 0.0, None
    for ch in s:
        bb = f.getbbox(ch)
        if bb and bb[2] > bb[0] and bb[3] > bb[1]:
            cur = (x + bb[0], float(bb[1]), x + bb[2], float(bb[3]))
            box = cur if box is None else (min(box[0], cur[0]), min(box[1], cur[1]),
                                           max(box[2], cur[2]), max(box[3], cur[3]))
        x += _adv(f, ch) + tracking
    return box or (0.0, 0.0, 0.0, 0.0)

def ink_extent(f, lines, tracking=0.0):
    """(top, bottom) ink offsets for a set of lines drawn at the same y."""
    top, bot = None, None
    for ln in lines:
        bb = ink_bbox(f, ln, tracking)
        if bb[3] > bb[1]:
            top = bb[1] if top is None else min(top, bb[1])
            bot = bb[3] if bot is None else max(bot, bb[3])
    if top is None:                      # empty / whitespace only
        a, d = f.getmetrics()
        return 0.0, float(a)
    return top, bot

def span_x(f, s, i0, i1, tracking=0.0):
    """Horizontal offsets of characters [i0, i1) inside a tracked string."""
    x, x0, x1 = 0.0, 0.0, 0.0
    for i, ch in enumerate(s):
        if i == i0:
            x0 = x
        if i == i1:
            x1 = x
            break
        x += _adv(f, ch) + tracking
    else:
        x1 = x - tracking if s else 0.0
    if i1 >= len(s):
        x1 = tracked_width(f, s, tracking)
    return x0, x1

# ---------------------------------------------------------------- DRAWING
def draw_tracked(draw, xy, s, f, fill, tracking=0.0, anchor="la", runs=None):
    """Draw `s` with per-character tracking. Returns the inked bbox.

    anchor: horizontal l/m/r + vertical a(scender)/m/s.
    runs:   optional [(start, end, colour)] spans that override `fill`.
    """
    x, y = float(xy[0]), float(xy[1])
    w = tracked_width(f, s, tracking)
    if anchor[0] == "m":
        x -= w / 2
    elif anchor[0] == "r":
        x -= w
    va = anchor[1]
    # PIL positions glyphs from the anchor; the ink box has to follow it or the
    # layout bookkeeping drifts (and bars start landing on type again).
    asc, desc = f.getmetrics()
    voff = {"a": 0.0, "t": 0.0, "m": -(asc + desc) / 2.0,
            "s": -float(asc), "b": -(asc + desc), "d": -(asc + desc)}.get(va, 0.0)
    box = None
    for i, ch in enumerate(s):
        col = fill
        if runs:
            for a, bnd, c in runs:
                if a <= i < bnd:
                    col = c
                    break
        draw.text((x, y), ch, font=f, fill=col, anchor="l" + va)
        bb = f.getbbox(ch)
        if bb and bb[2] > bb[0] and bb[3] > bb[1]:
            cur = (x + bb[0], y + voff + bb[1], x + bb[2], y + voff + bb[3])
            box = cur if box is None else (min(box[0], cur[0]), min(box[1], cur[1]),
                                           max(box[2], cur[2]), max(box[3], cur[3]))
        x += _adv(f, ch) + tracking
    return box or (x, y, x, y)

def normalise(text):
    return " ".join(str(text).split())

def wrap_indexed(text, f, max_width, tracking=0.0):
    """Wrap into [(line, start_index)] against the normalised string, so accent
    spans can be mapped back onto individual lines."""
    text = normalise(text)
    out, cur, cur_start, pos = [], "", 0, 0
    for word in text.split(" "):
        trial = (cur + " " + word) if cur else word
        if not cur or tracked_width(f, trial, tracking) <= max_width:
            if not cur:
                cur_start = pos
            cur = trial
        else:
            out.append((cur, cur_start))
            cur_start, cur = pos, word
        pos += len(word) + 1
    if cur:
        out.append((cur, cur_start))
    return out

def wrap_tracked(text, f, max_width, tracking=0.0):
    return [ln for ln, _ in wrap_indexed(text, f, max_width, tracking)]

# ---------------------------------------------------------------- ACCENT SPAN
_STOP = {"the", "a", "an", "of", "to", "and", "or", "is", "are", "in", "on",
         "for", "your", "you", "it", "that", "this", "not", "do", "be", "my"}

def sentences(text):
    """Split into (start, end) spans on sentence-ending punctuation."""
    t = normalise(text)
    out, start = [], 0
    for i, ch in enumerate(t):
        if ch in ".?!" and (i + 1 >= len(t) or t[i + 1] == " "):
            out.append((start, i + 1))
            start = i + 2
    if start < len(t):
        out.append((start, len(t)))
    return out or [(0, len(t))]


def accent_span(text, max_words=3, max_share=0.34):
    """Pick the phrase the board would set in volt.

    The board accents a *noun phrase*, never a whole sentence — "machine.",
    "performance metric", "5 apps". So: take the closing sentence, keep its
    last two or three words, and refuse anything that would tint more than
    a third of the hook. Returns (start, end) into the normalised text.
    """
    t = normalise(text)
    words = t.split(" ")
    if len(words) < 4:
        return None
    a, bnd = sentences(t)[-1]
    seg_words = t[a:bnd].split(" ")
    if len(seg_words) < 2:                    # closing fragment too short to carry it
        a, bnd = 0, len(t)
        seg_words = words
    for n in range(min(max_words, len(seg_words)), 1, -1):
        tail = seg_words[-n:]
        while len(tail) > 2 and tail[0].strip("“”\"'.,;:").lower() in _STOP:
            tail = tail[1:]
        seg = " ".join(tail)
        start = t.rfind(seg, a, bnd)
        if start <= 0 or len(seg) > len(t) * max_share:
            continue
        return start, start + len(seg)
    return None
