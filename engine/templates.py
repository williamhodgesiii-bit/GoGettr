"""
GoGettr render engine — procedural backgrounds, the Forward mark,
and a Canvas of on-brand template styles used across every platform.

One symbol, three cuts. Volt is a highlighter (one element per post).
Violet is reserved for numerals. Never volt type on white.
"""
from PIL import Image, ImageDraw, ImageChops, ImageFilter
import random, math
import engine.brand as b

# ---------------------------------------------------------------- FORMATS
FORMATS = {
    "ig":     (1080, 1350),   # Instagram / Facebook portrait carousel
    "vert":   (1080, 1920),   # TikTok / Reels / YouTube Shorts
    "square": (1080, 1080),   # LinkedIn feed carousel
    "pin":    (1000, 1500),   # Pinterest 2:3
    "wide":   (1600, 900),    # X / Twitter card
    "link":   (1200, 628),    # LinkedIn / FB link card
}

# ---------------------------------------------------------------- BACKGROUNDS
def linear_gradient(size, c1, c2, vertical=True):
    w, h = size
    base = Image.new("RGB", size, c1)
    d = ImageDraw.Draw(base)
    n = h if vertical else w
    for i in range(n):
        t = i / max(1, n - 1)
        col = tuple(int(c1[j] + (c2[j] - c1[j]) * t) for j in range(3))
        if vertical:
            d.line([(0, i), (w, i)], fill=col)
        else:
            d.line([(i, 0), (i, h)], fill=col)
    return base

def add_grain(img, amount=0.045, sigma=48):
    g = Image.effect_noise(img.size, sigma).convert("RGB")
    return Image.blend(img, ImageChops.overlay(img, g), amount)

def vignette(img, strength=0.35):
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([-w * 0.35, -h * 0.35, w * 1.35, h * 1.35], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(min(w, h) // 6))
    dark = Image.new("RGB", (w, h), (0, 0, 0))
    return Image.composite(img, Image.blend(img, dark, strength), mask)

def draw_chevron(d, x, y, h, color, weight=None, double=True):
    """The Forward mark: bold right-pointing chevron(s)."""
    w = weight or int(h * 0.30)
    wing = h * 0.60
    def one(px):
        d.line([(px, y), (px + wing, y + h / 2), (px, y + h)],
               fill=color, width=w, joint="curve")
    one(x)
    if double:
        one(x + wing * 0.92)

def chevron_field(size, base_color, mark_color, big=True, alpha=None):
    """Ghosted oversized chevron watermark — reads as brand texture, not noise."""
    w, h = size
    img = Image.new("RGB", size, base_color)
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    a = alpha if alpha is not None else 26
    col = mark_color + (a,)
    ch = int(h * (0.9 if big else 0.34))
    draw_chevron(ld, int(w * 0.42), int(h * 0.5 - ch / 2), ch, col,
                 weight=int(ch * 0.24))
    img.paste(Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB"), (0, 0))
    return img

def plate(size, mood="graphite", accent="volt"):
    """A designed 'photo / B-roll' cover plate (no stock photography)."""
    w, h = size
    pairs = {
        "graphite": (b.GRAPHITE_HI, b.INK),
        "ink":      ((30, 34, 41), b.INK),
        "violet":   (b.VIOLET_DK, b.INK),
        "steel":    ((70, 76, 86), (24, 27, 32)),
    }
    c1, c2 = pairs.get(mood, pairs["graphite"])
    img = linear_gradient(size, c1, c2, vertical=True)
    # diagonal brand slash (echoes the profile banner)
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    acol = (b.VOLT if accent == "volt" else b.VIOLET) + (22,)
    sx = int(w * 0.64)
    ld.polygon([(sx, 0), (sx + int(w * 0.07), 0),
                (sx - int(w * 0.20), h), (sx - int(w * 0.27), h)], fill=acol)
    ghost = Image.new("RGBA", size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(ghost)
    ch = int(h * 0.7)
    draw_chevron(gd, int(w * 0.5), int(h * 0.5 - ch / 2), ch,
                 (255, 255, 255, 16), weight=int(ch * 0.22))
    img = Image.alpha_composite(img.convert("RGBA"), layer)
    img = Image.alpha_composite(img, ghost).convert("RGB")
    img = add_grain(img, 0.06)
    img = vignette(img, 0.4)
    return img

GROUNDS = {"graphite": b.GRAPHITE, "ink": b.INK, "chrome": b.CHROME, "violet": b.VIOLET}

# ---------------------------------------------------------------- CANVAS
class Canvas:
    def __init__(self, fmt, ground="graphite", plate_mood=None, accent="volt"):
        self.fmt = fmt
        self.w, self.h = FORMATS[fmt]
        self.accent = accent
        self.accent_rgb = b.VOLT if accent == "volt" else b.VIOLET
        self.s = self.w / 1080.0            # artboard scale factor
        self.dark = ground != "chrome"
        if plate_mood:
            self.img = plate((self.w, self.h), plate_mood, accent)
            self.dark = True
        else:
            self.img = Image.new("RGB", (self.w, self.h), GROUNDS[ground])
        self.d = ImageDraw.Draw(self.img)
        # margins
        self.mx = int(b.MARGIN * self.s)
        self.my = int(b.TOP * self.s)
        # vertical UI safe band (TikTok/Shorts): keep content off UI rails
        if fmt == "vert":
            self.top_safe = int(self.h * 0.14)
            self.bot_safe = int(self.h * 0.80)
        else:
            self.top_safe = self.my
            self.bot_safe = self.h - self.my
        # text colours by ground
        self.fg = b.INK if not self.dark else b.WHITE
        self.muted = b.STEEL if self.dark else (90, 96, 104)

    def px(self, v):
        return int(v * self.s)

    # -- primitives --------------------------------------------------
    def eyebrow(self, text, y=None, color=None):
        y = self.top_safe if y is None else y
        f = b.font("mono", self.px(30), 600)
        b.draw_tracked(self.d, (self.mx, y), text.upper(), f,
                       color or self.muted, tracking=self.px(30) * 0.20)
        return y + self.px(46)

    def volt_bar(self, y, w_ratio=0.28, color=None):
        x2 = self.mx + int((self.w - 2 * self.mx) * w_ratio)
        self.d.rectangle([self.mx, y, x2, y + self.px(14)],
                         fill=color or self.accent_rgb)
        return y + self.px(40)

    def hook(self, text, y, max_size=130, min_size=54, max_lines=4, color=None,
             box_ratio=1.0):
        box = int((self.w - 2 * self.mx) * box_ratio)
        f, sz, tr, lines = b.fit_hook(self.d, text, box, self.px(max_size),
                                      self.px(min_size), max_lines=max_lines)
        lh = sz * 1.03
        for ln in lines:
            b.draw_tracked(self.d, (self.mx, y), ln, f, color or self.fg, tracking=tr)
            y += lh
        return int(y)

    def sub(self, text, y, size=40, color=None, weight=500, gap=1.28):
        f = b.font("body", self.px(size), weight)
        return int(b.draw_paragraph(self.d, (self.mx, y), text, f,
                    color or (self.muted if self.dark else (70, 76, 84)),
                    self.w - 2 * self.mx, self.px(size) * gap))

    def numeral(self, text, y, size=250, color=None, center=False):
        f = b.font("display", self.px(size), 700)
        x = self.w / 2 if center else self.mx
        anchor = "ma" if center else "la"
        b.draw_tracked(self.d, (x, y), text, f, color or b.VIOLET,
                       tracking=self.px(size) * -0.02, anchor=anchor)
        return int(y + size * self.s * 0.98)

    def rows(self, items, y, size=52, gap=1.7, numbered=True, index_color=None):
        f = b.font("display", self.px(size), 500)
        fi = b.font("mono", self.px(int(size * 0.62)), 700)
        for i, it in enumerate(items, 1):
            if numbered:
                idx = f"{i:02d}"
                b.draw_tracked(self.d, (self.mx, y + self.px(6)), idx, fi,
                               index_color or self.accent_rgb, tracking=1)
                tx = self.mx + self.px(size * 1.55)
            else:
                self.d.rectangle([self.mx, y + self.px(size*0.4),
                                  self.mx + self.px(size*0.5), y + self.px(size*0.4)+self.px(8)],
                                 fill=index_color or self.accent_rgb)
                tx = self.mx + self.px(size * 0.9)
            lines = b.wrap_tracked(it, f, self.w - tx - self.mx, tr := self.px(size)*-0.02)
            for ln in lines:
                b.draw_tracked(self.d, (tx, y), ln, f, self.fg, tracking=tr)
                y += self.px(size) * 1.04
            y += self.px(size) * (gap - 1.04)
        return int(y)

    def quote(self, text, y, size=96, color=None, max_lines=6):
        box = self.w - 2 * self.mx
        f, sz, tr, lines = b.fit_hook(self.d, text, box, self.px(size),
                                      self.px(48), max_lines=max_lines)
        # opening tick
        self.d.text((self.mx - self.px(6), y - self.px(sz*0.5)), "“",
                    font=b.font("display", self.px(int(size*1.2)), 700), fill=self.accent_rgb)
        for ln in lines:
            b.draw_tracked(self.d, (self.mx, y), ln, f, color or self.fg, tracking=tr)
            y += sz * 1.05
        return int(y)

    def chevron(self, x, y, h, color=None, double=True):
        draw_chevron(self.d, x, y, self.px(h), color or self.accent_rgb,
                     weight=self.px(int(h * 0.26)), double=double)

    def wordmark(self, x, y, size=30, color=None):
        h = self.px(size)
        draw_chevron(self.d, x, y, h, color or self.accent_rgb, weight=self.px(int(size*0.28)))
        f = b.font("display", int(h * 1.02), 700)
        b.draw_tracked(self.d, (x + h * 1.35, y - h*0.06), "GOGETTR", f,
                       color or (self.fg), tracking=h * 0.06)

    def footer(self, left="@GOGETTRDAILY", right="SAVE THIS →", y=None,
               show_mark=True):
        y = (self.bot_safe - self.px(6)) if y is None else y
        f = b.font("mono", self.px(28), 600)
        # thin rule
        self.d.line([(self.mx, y - self.px(30)), (self.w - self.mx, y - self.px(30))],
                    fill=self.muted, width=max(1, self.px(2)))
        if show_mark:
            self.chevron(self.mx, y, 30, color=self.accent_rgb)
            b.draw_tracked(self.d, (self.mx + self.px(58), y + self.px(2)),
                           left.upper(), f, self.fg if self.dark else b.INK,
                           tracking=self.px(28) * 0.16)
        else:
            b.draw_tracked(self.d, (self.mx, y + self.px(2)), left.upper(), f,
                           self.fg, tracking=self.px(28) * 0.16)
        if right:
            b.draw_tracked(self.d, (self.w - self.mx, y + self.px(2)), right.upper(),
                           f, self.accent_rgb if self.dark else b.VIOLET,
                           tracking=self.px(28) * 0.16, anchor="ra")

    def url_stamp(self, text="GOGETTR", y=None):  # (unused; kept for optional URL pill)
        y = (self.h - self.my) if y is None else y
        f = b.font("mono", self.px(30), 700)
        pill_w = b.tracked_width(f, text.upper(), self.px(30)*0.16) + self.px(56)
        self.d.rounded_rectangle([self.mx, y - self.px(20),
                                  self.mx + pill_w, y + self.px(40)],
                                 radius=self.px(10), fill=self.accent_rgb)
        b.draw_tracked(self.d, (self.mx + self.px(28), y), text.upper(), f,
                       b.INK, tracking=self.px(30) * 0.16)

    def index_chip(self, text, right=True):
        f = b.font("mono", self.px(26), 700)
        y = self.top_safe
        x = self.w - self.mx if right else self.mx
        anchor = "ra" if right else "la"
        b.draw_tracked(self.d, (x, y), text.upper(), f, self.accent_rgb,
                       tracking=self.px(26)*0.18, anchor=anchor)

    def save(self, path):
        self.img.save(path, quality=95)
        return path
