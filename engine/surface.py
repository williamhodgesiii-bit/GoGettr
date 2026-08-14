# -*- coding: utf-8 -*-
"""
The drawing surface: artboards, grounds, procedural plates, the Forward mark,
platform UI-safe bands and the footer rows — the pieces every template is
assembled from.

Ground rules taken from the board:
  · Volt is a highlighter, one element per post, and never type on white —
    on light grounds an accent phrase becomes a volt *box* behind ink type.
  · Violet is reserved for numerals and rules.
  · Nothing crosses the margin except full-bleed plates.
  · Footers are mono, tracked, and sit in a band the content region never
    reaches into.
"""
from PIL import Image, ImageDraw, ImageChops, ImageFilter
import math
import engine.brand as b
from engine.layout import Box

# ---------------------------------------------------------------- FORMATS
# size, artboard scale, side margin, top/bottom margin
FORMATS = {
    "ig":     dict(size=(1080, 1350), s=1.00, mx=96,  my=120),   # IG / FB portrait
    "vert":   dict(size=(1080, 1920), s=1.00, mx=96,  my=150,    # TikTok / Reels / Shorts
                   top_safe=0.135, bot_safe=0.775),
    "square": dict(size=(1080, 1080), s=1.00, mx=96,  my=104),   # LinkedIn feed
    "pin":    dict(size=(1000, 1500), s=0.93, mx=88,  my=112),   # Pinterest 2:3
    "wide":   dict(size=(1600, 900),  s=0.92, mx=112, my=88),    # X / Twitter card
    "link":   dict(size=(1200, 628),  s=0.74, mx=88,  my=70),    # link card
}

GROUNDS = {"graphite": b.GRAPHITE, "ink": b.INK, "chrome": b.CHROME,
           "violet": b.VIOLET, "volt": b.VOLT}
LIGHT_GROUNDS = {"chrome", "volt"}


def _blend(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


# ---------------------------------------------------------------- TEXTURE
def linear_gradient(size, c1, c2, vertical=True):
    w, h = size
    base = Image.new("RGB", size, c1)
    d = ImageDraw.Draw(base)
    n = h if vertical else w
    for i in range(n):
        t = i / max(1, n - 1)
        col = _blend(c1, c2, t)
        d.line([(0, i), (w, i)] if vertical else [(i, 0), (i, h)], fill=col)
    return base


def add_grain(img, amount=0.05, sigma=48):
    g = Image.effect_noise(img.size, sigma).convert("RGB")
    return Image.blend(img, ImageChops.overlay(img, g), amount)


def vignette(img, strength=0.32):
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse([-w * 0.35, -h * 0.35, w * 1.35, h * 1.35], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(max(4, min(w, h) // 6)))
    dark = Image.new("RGB", (w, h), (0, 0, 0))
    return Image.composite(img, Image.blend(img, dark, strength), mask)


def draw_chevron(d, x, y, h, color, weight=None, double=True):
    """The Forward mark — the chevron never changes shape, only its ground."""
    w = max(2, int(weight or h * 0.30))
    wing = h * 0.60

    def one(px):
        d.line([(px, y), (px + wing, y + h / 2), (px, y + h)],
               fill=color, width=w, joint="curve")
    one(x)
    if double:
        one(x + wing * 0.92)


PLATE_MOODS = {
    "ink":      (b.INK_HI, b.INK),
    "graphite": (b.GRAPHITE_HI, b.GRAPHITE),
    "violet":   (b.VIOLET_DK, b.INK),
    "steel":    ((70, 76, 86), (24, 27, 32)),
}


def plate(size, treatment="chevron", mood="ink", accent=b.VOLT):
    """A designed plate for the board's 'photo' slots. Brand texture, not stock
    photography, so every asset ships finished."""
    w, h = size
    if w < 2 or h < 2:
        return Image.new("RGB", (max(1, w), max(1, h)), b.INK)
    c1, c2 = PLATE_MOODS.get(mood, PLATE_MOODS["ink"])
    img = linear_gradient((w, h), c1, c2, vertical=True)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    unit = min(w, h)

    if treatment == "chevron":
        ch = int(h * 0.78)
        draw_chevron(ld, int(w * 0.46), int(h * 0.5 - ch / 2), ch,
                     (255, 255, 255, 15), weight=int(ch * 0.22))
        ld.polygon([(int(w * 0.70), 0), (int(w * 0.77), 0),
                    (int(w * 0.50), h), (int(w * 0.43), h)], fill=accent + (16,))
    elif treatment == "hatch":
        step = max(12, int(unit * 0.062))
        for i in range(-h, w + h, step):
            ld.line([(i, 0), (i + h, h)], fill=(255, 255, 255, 13),
                    width=max(2, int(step * 0.30)))
    elif treatment == "grid":
        step = max(16, int(unit * 0.085))
        for x in range(step, w, step):
            ld.line([(x, 0), (x, h)], fill=(255, 255, 255, 11), width=1)
        for y in range(step, h, step):
            ld.line([(0, y), (w, y)], fill=(255, 255, 255, 11), width=1)
        ld.rectangle([int(w * 0.62), int(h * 0.14), int(w * 0.62) + step * 2,
                      int(h * 0.14) + step * 2], fill=accent + (30,))
    elif treatment == "rings":
        cx, cy = int(w * 0.72), int(h * 0.42)
        for i in range(7):
            r = unit * (0.14 + i * 0.13)
            ld.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255, 14),
                       width=max(2, int(unit * 0.008)))
        r = unit * 0.14
        ld.ellipse([cx - r, cy - r, cx + r, cy + r], outline=accent + (46,),
                   width=max(2, int(unit * 0.010)))
    elif treatment == "dots":
        step = max(18, int(unit * 0.075))
        r = max(2, int(step * 0.13))
        for y in range(step, h, step):
            for x in range(step, w, step):
                a = 22 if ((x // step + y // step) % 7) else 60
                col = accent + (a,) if a > 30 else (255, 255, 255, a)
                ld.ellipse([x - r, y - r, x + r, y + r], fill=col)
    elif treatment == "sweep":
        for i in range(0, 5):
            x0 = int(w * (0.12 + i * 0.20))
            ld.polygon([(x0, 0), (x0 + int(w * 0.09), 0),
                        (x0 - int(w * 0.18), h), (x0 - int(w * 0.27), h)],
                       fill=(255, 255, 255, 10 if i % 2 else 14))
        ld.polygon([(int(w * 0.52), 0), (int(w * 0.58), 0),
                    (int(w * 0.34), h), (int(w * 0.28), h)], fill=accent + (20,))
    elif treatment == "bars":
        n = 9
        for i in range(n):
            bw = w / n
            hh = h * (0.20 + 0.62 * abs(math.sin(i * 1.7)))
            ld.rectangle([i * bw + bw * 0.22, h - hh, (i + 1) * bw - bw * 0.22, h],
                         fill=(255, 255, 255, 12) if i % 3 else accent + (26,))

    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    img = add_grain(img, 0.055)
    return vignette(img, 0.34)


def hatch_band(size, base, accent=b.VOLT, alpha=30):
    """Hatched band marking a platform UI zone (board: TikTok/Reels rules)."""
    w, h = size
    img = Image.new("RGB", (max(1, w), max(1, h)), base)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    step = max(20, int(h * 0.16))
    for i in range(-h, w + h, step):
        ld.line([(i, 0), (i + h, h)], fill=accent + (alpha,), width=max(3, int(step * 0.34)))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


# ---------------------------------------------------------------- CANVAS
class Canvas:
    def __init__(self, fmt, ground="graphite", plate_treatment=None,
                 plate_mood="ink", accent="volt"):
        spec = FORMATS[fmt]
        self.fmt = fmt
        self.w, self.h = spec["size"]
        self.s = spec["s"]
        self.ground = ground
        self.boxes = []
        self.mx = self.px(spec["mx"])
        self.my = self.px(spec["my"])

        if plate_treatment:
            self.img = plate((self.w, self.h), plate_treatment, plate_mood,
                             b.VOLT if accent == "volt" else b.VIOLET)
            self.light = False
        else:
            self.img = Image.new("RGB", (self.w, self.h), GROUNDS[ground])
            self.light = ground in LIGHT_GROUNDS
        self.d = ImageDraw.Draw(self.img)

        # accent policy — volt is a highlighter, never type on white
        if ground == "volt":
            self.accent_rgb = b.INK
            self.accent_text = b.VIOLET
            self.accent_text_mode = "colour"
        else:
            self.accent_rgb = b.VOLT if accent == "volt" else b.VIOLET
            self.accent_text = self.accent_rgb
            self.accent_text_mode = "highlight" if self.light else "colour"

        # ink colours by ground. `muted` carries meta (labels, footers),
        # `sub_col` carries the second line — it has to stay readable.
        if ground == "chrome" and not plate_treatment:
            self.fg, self.muted, self.hairline = b.INK, b.INK_FAINT, (203, 206, 210)
            self.sub_col = b.INK_SOFT
        elif ground == "volt" and not plate_treatment:
            self.fg = b.INK
            self.muted = _blend(b.INK, b.VOLT, 0.34)
            self.hairline = _blend(b.INK, b.VOLT, 0.62)
            self.sub_col = _blend(b.INK, b.VOLT, 0.28)
        elif ground == "violet" and not plate_treatment:
            self.fg, self.muted = b.WHITE, _blend(b.WHITE, b.VIOLET, 0.46)
            self.hairline = _blend(b.WHITE, b.VIOLET, 0.62)
            self.sub_col = _blend(b.WHITE, b.VIOLET, 0.15)
        else:
            self.fg, self.muted, self.hairline = b.WHITE, b.STEEL, (58, 63, 71)
            self.sub_col = (154, 160, 170)

        # platform UI-safe rails (vertical video)
        if fmt == "vert":
            self.top_safe = int(self.h * spec["top_safe"])
            self.bot_safe = int(self.h * spec["bot_safe"])
        else:
            self.top_safe, self.bot_safe = self.my, self.h - self.my

        self._footer_top = None
        self.type_sizes = []
        self.cues = []                       # forward promises drawn in the footer
        self.volt_field = (ground == "volt")  # volt as ground/panel, by design
        # the safe edges the audit holds elements to; a template that lays out
        # in its own column (a colour panel) may widen them
        self.safe_x0, self.safe_x1 = self.mx, self.w - self.mx
        # the audit reads the element registry back off the finished image
        self.img.canvas = self

    # -- geometry ----------------------------------------------------
    def px(self, v):
        return v * self.s

    def record(self, box):
        if box is not None and not box.empty():
            self.boxes.append(box)
        return box

    @property
    def content_w(self):
        return self.w - 2 * self.mx

    def footer_band(self, height=None):
        """Reserve the footer row. Content never enters this band."""
        fh = height if height is not None else self.px(b.SCALE["footer"] * 1.5)
        if self.fmt == "vert":
            bottom = self.bot_safe
        else:
            bottom = self.h - self.px(b.FOOTER_OFFSET)
        self._footer_top = bottom - fh
        return Box(self.mx, self._footer_top, self.w - self.mx, bottom, "footer_band")

    def region(self, top=None, bottom=None, reserve_footer=True, footer_h=None,
               inset=0.0):
        """The content region: inside the margins, above the footer band."""
        t = self.top_safe if top is None else top
        if bottom is not None:
            bt = bottom
        elif reserve_footer:
            bt = self.footer_band(footer_h).y0 - self.px(44)
        else:
            bt = self.bot_safe
        x0 = self.mx + inset
        return Box(x0, t, self.w - self.mx, bt, "region")

    # -- components --------------------------------------------------
    def paste_plate(self, x, y, w, h, treatment="chevron", mood="ink"):
        if w <= 0 or h <= 0:
            return
        self.img.paste(plate((int(w), int(h)), treatment, mood, self.accent_rgb),
                       (int(x), int(y)))
        self.d = ImageDraw.Draw(self.img)
        self.img.canvas = self

    def ui_bands(self, alpha=26):
        """Hatched top/bottom bands marking the platform UI zones."""
        base = GROUNDS.get(self.ground, b.INK)
        if self.top_safe > 0:
            self.img.paste(hatch_band((self.w, self.top_safe), base, b.VOLT, alpha), (0, 0))
        bh = self.h - self.bot_safe
        if bh > 0:
            self.img.paste(hatch_band((self.w, bh), base, b.VOLT, alpha), (0, self.bot_safe))
        self.d = ImageDraw.Draw(self.img)
        self.img.canvas = self

    def label(self, text, x, y, size=30, color=None, anchor="la", weight=600,
              track=None):
        f = b.font("mono", self.px(size), weight)
        tr = f.size * (b.LABEL_TRACK if track is None else track)
        bb = b.draw_tracked(self.d, (x, y), b.normalise(text).upper(), f,
                            color if color is not None else self.muted,
                            tracking=tr, anchor=anchor)
        return self.record(Box(*bb, name="label"))

    def eyebrow(self, text, color=None, y=None, size=30):
        """Top-left label. Sits on the top-safe line, above the content region."""
        if not text:
            return None
        yy = self.top_safe if y is None else y
        return self.label(text, self.mx, yy, size=size,
                          color=color if color is not None else self.muted)

    def index_chip(self, text, color=None, y=None, size=26):
        if not text:
            return None
        yy = self.top_safe if y is None else y
        return self.label(text, self.w - self.mx, yy, size=size, anchor="ra",
                          color=color if color is not None else self.accent_text
                          if not self.light else b.VIOLET)

    def chevron_badge(self, x, y, d=None, ring=True):
        """Small mark used where the full lockup would be too big (board 04)."""
        d = d or self.px(40)
        if ring:
            self.d.ellipse([x, y, x + d, y + d],
                           fill=b.INK if self.light else b.VOLT)
            col = b.VOLT if self.light else b.INK
        else:
            col = self.accent_rgb
        draw_chevron(self.d, x + d * 0.30, y + d * 0.30, d * 0.40, col,
                     weight=max(2, int(d * 0.11)))
        return self.record(Box(x, y, x + d, y + d, "badge"))

    def mark(self, x, y, h=None, color=None, double=True):
        h = h or self.px(34)
        draw_chevron(self.d, x, y, h, color or self.accent_rgb,
                     weight=max(2, int(h * 0.28)), double=double)
        wing = h * 0.60
        return self.record(Box(x, y, x + wing * 1.92 + h * 0.15, y + h, "mark"))

    # -- footers -----------------------------------------------------
    def footer(self, left="@GOGETTR", right=None, badge=False, size=28,
               left_color=None, right_color=None):
        """Board footer row: mono, tracked, no rule. Lives in the reserved band."""
        band = self.footer_band()
        y = (band.y0 + band.y1) / 2          # centred in the band, never below it
        boxes = []
        x = self.mx
        if badge:
            d = self.px(38)
            boxes.append(self.chevron_badge(x, y - d / 2, d))
            x += d * 1.45
        if left:
            boxes.append(self.label(left, x, y, size=size, anchor="lm",
                                    color=left_color if left_color is not None
                                    else (self.muted if not self.light else b.INK_FAINT)))
        if right:
            self.cues.append(b.normalise(right).upper())
            boxes.append(self.label(right, self.w - self.mx, y, size=size, anchor="rm",
                                    color=right_color if right_color is not None
                                    else (b.VOLT if not self.light else b.VIOLET)))
        return boxes

    def vert_handle(self, text="@GOGETTRDAILY", color=None):
        """Vertical video: the handle rides just above the action rail."""
        return self.label(text, self.mx, self.bot_safe - self.px(46), size=30,
                          color=color if color is not None else self.muted)

    def save(self, path):
        self.img.save(path, quality=95, subsampling=0)
        return path
