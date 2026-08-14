# -*- coding: utf-8 -*-
"""
Measure-then-place layout.

A slide is a *stack of blocks* dropped into a content region that is bounded
by the artboard margins above and by the reserved footer band below. Every
block reports its real inked height before anything is drawn; if the stack is
taller than the region, type steps down (and optional blocks drop out) until
it fits.

Consequences that matter for the finished art:
  · a volt bar or hairline can never land on a descender — bars are blocks,
    placed after the text block they follow has been measured;
  · nothing can run under the footer or off the artboard;
  · text is set at the largest size that still fits, so posts look sized on
    purpose rather than squeezed.
"""
import engine.brand as b

MIN_SHRINK = 0.52          # never shrink type past this fraction of spec
SHRINK_STEP = 0.02


class Box:
    __slots__ = ("x0", "y0", "x1", "y1", "name")

    def __init__(self, x0, y0, x1, y1, name=""):
        self.x0, self.y0, self.x1, self.y1, self.name = x0, y0, x1, y1, name

    @property
    def w(self):
        return self.x1 - self.x0

    @property
    def h(self):
        return self.y1 - self.y0

    def empty(self):
        return self.w <= 0 or self.h <= 0

    def intersects(self, o, pad=0.0):
        return not (self.x1 - pad <= o.x0 or o.x1 - pad <= self.x0 or
                    self.y1 - pad <= o.y0 or o.y1 - pad <= self.y0)

    def union(self, o):
        if o is None or o.empty():
            return self
        if self.empty():
            return o
        return Box(min(self.x0, o.x0), min(self.y0, o.y0),
                   max(self.x1, o.x1), max(self.y1, o.y1), self.name)

    def __repr__(self):
        return f"Box({self.x0:.0f},{self.y0:.0f},{self.x1:.0f},{self.y1:.0f},{self.name!r})"


# ---------------------------------------------------------------- BLOCKS
class Block:
    """Base block. `gap` is space above the block, in 1080-artboard px."""
    optional = False

    def __init__(self, gap=0, optional=False):
        self.gap = gap
        self.optional = optional

    def gap_px(self, c, k):
        return c.px(self.gap) * (0.72 + 0.28 * k)

    def measure(self, c, width, k):
        return 0.0

    def draw(self, c, x, y, width, k):
        return Box(x, y, x, y)


class Text(Block):
    """A fitted run of type. Shrinks until it wraps inside `max_lines`."""

    def __init__(self, text, family="display", size=116, min_size=44, weight=None,
                 color=None, tracking=None, leading=None, max_lines=4, align="left",
                 gap=0, optional=False, accent=None, accent_mode=None,
                 accent_color=None, upper=False, wrap=True, balance=None):
        super().__init__(gap, optional)
        self.text = b.normalise(text or "")
        if upper:
            self.text = self.text.upper()
        self.family, self.size, self.min_size = family, size, min_size
        self.weight, self.color = weight, color
        if tracking is None:
            tracking = {"display": b.HOOK_TRACK, "mono": b.LABEL_TRACK}.get(family, 0.0)
        self.tracking = tracking
        if leading is None:
            leading = {"display": b.HOOK_LEAD, "mono": 1.42}.get(family, 1.32)
        self.leading = leading
        self.max_lines, self.align, self.upper, self.wrap = max_lines, align, upper, wrap
        self.balance = (align == "center") if balance is None else balance
        self.accent = accent                    # (start, end) into normalised text
        self.accent_mode = accent_mode          # "colour" | "highlight" | None
        self.accent_color = accent_color
        self._cache = {}

    # -- fitting ----------------------------------------------------
    def _fit(self, c, width, k):
        key = (round(width), round(k, 3))
        if key in self._cache:
            return self._cache[key]
        top = max(c.px(self.size) * k, c.px(self.min_size) * MIN_SHRINK)
        floor = c.px(self.min_size) * max(MIN_SHRINK, min(1.0, k + 0.18))
        size = top
        f = lines = None
        while size >= floor - 0.5:
            f = b.font(self.family, size, self.weight)
            tr = size * self.tracking
            lines = b.wrap_indexed(self.text, f, width, tr) if self.wrap else [(self.text, 0)]
            if len(lines) <= self.max_lines and all(
                    b.tracked_width(f, ln, tr) <= width + 1 for ln, _ in lines):
                break
            size -= max(1.0, top * 0.02)
        size = max(size, 1.0)
        f = b.font(self.family, size, self.weight)
        tr = size * self.tracking
        lines = b.wrap_indexed(self.text, f, width, tr) if self.wrap else [(self.text, 0)]
        if self.balance and self.wrap and len(lines) > 1:
            lines = self._balance(f, tr, width, len(lines))
        ink_top, ink_bot = b.ink_extent(f, [ln for ln, _ in lines], tr)
        lead = size * self.leading
        h = (len(lines) - 1) * lead + (ink_bot - ink_top)
        res = (f, size, tr, lines, lead, ink_top, ink_bot, h)
        self._cache[key] = res
        return res

    def _balance(self, f, tr, width, n_lines):
        """Even out the rag: the narrowest measure that still holds n lines."""
        lo, hi, best = width * 0.45, width, None
        for _ in range(14):
            mid = (lo + hi) / 2
            trial = b.wrap_indexed(self.text, f, mid, tr)
            if len(trial) <= n_lines:
                best, hi = trial, mid
            else:
                lo = mid
        return best or b.wrap_indexed(self.text, f, width, tr)

    def measure(self, c, width, k):
        if not self.text:
            return 0.0
        return self._fit(c, width, k)[7]

    # -- drawing ----------------------------------------------------
    def draw(self, c, x, y, width, k):
        if not self.text:
            return Box(x, y, x, y)
        f, size, tr, lines, lead, ink_top, ink_bot, h = self._fit(c, width, k)
        c.type_sizes.append((size, self.family, c.px(self.size)))
        col = self.color if self.color is not None else c.fg
        acol = self.accent_color if self.accent_color is not None else c.accent_rgb
        box = None
        for n, (ln, start) in enumerate(lines):
            ly = y - ink_top + n * lead
            lw = b.tracked_width(f, ln, tr)
            lx = x + (width - lw) / 2 if self.align == "center" else x
            runs = None
            if self.accent:
                a0 = max(self.accent[0] - start, 0)
                a1 = min(self.accent[1] - start, len(ln))
                if a1 > a0:
                    if self.accent_mode == "highlight":
                        sx0, sx1 = b.span_x(f, ln, a0, a1, tr)
                        pad = size * 0.10
                        c.d.rectangle([lx + sx0 - pad, ly + ink_top - size * 0.10,
                                       lx + sx1 + pad, ly + ink_bot + size * 0.14],
                                      fill=acol)
                        box = Box(lx + sx0 - pad, ly + ink_top - size * 0.10,
                                  lx + sx1 + pad, ly + ink_bot + size * 0.14).union(box)
                    elif self.accent_mode == "colour":
                        runs = [(a0, a1, acol)]
            bb = b.draw_tracked(c.d, (lx, ly), ln, f, col, tracking=tr, runs=runs)
            box = Box(*bb).union(box)
        out = box or Box(x, y, x, y)
        out.name = "text"
        c.record(out)
        return out


class Rule(Block):
    """The volt bar. A block, so it is always placed *below* measured text."""

    def __init__(self, width_ratio=0.26, thickness=14, color=None, gap=26,
                 align="left", max_width=None):
        super().__init__(gap)
        self.wr, self.th, self.color, self.align = width_ratio, thickness, color, align
        self.max_width = max_width

    def measure(self, c, width, k):
        return c.px(self.th) * max(0.75, k)

    def draw(self, c, x, y, width, k):
        h = self.measure(c, width, k)
        w = width * self.wr
        if self.max_width:
            w = min(w, c.px(self.max_width))
        x0 = x + (width - w) / 2 if self.align == "center" else x
        c.d.rectangle([x0, y, x0 + w, y + h], fill=self.color or c.accent_rgb)
        box = Box(x0, y, x0 + w, y + h, "rule")
        c.record(box)
        return box


class Spectrum(Block):
    """01 SPECTRUM HOOK — three short segments: violet, volt, chrome."""

    def __init__(self, gap=0, seg=54, thickness=12, colors=None):
        super().__init__(gap)
        self.seg, self.th = seg, thickness
        self.colors = colors

    def measure(self, c, width, k):
        return c.px(self.th) * max(0.8, k)

    def draw(self, c, x, y, width, k):
        h = self.measure(c, width, k)
        seg = c.px(self.seg) * max(0.8, k)
        gap = seg * 0.30
        cols = self.colors or (b.VIOLET, b.VOLT, c.fg)
        cx = x
        for col in cols:
            c.d.rectangle([cx, y, cx + seg, y + h], fill=col)
            cx += seg + gap
        box = Box(x, y, cx - gap, y + h, "spectrum")
        c.record(box)
        return box


class Chip(Block):
    """Volt label chip (board: the 'STACK' tag on B-roll frames)."""

    def __init__(self, text, gap=0, size=28, fill=None, color=None):
        super().__init__(gap)
        self.text, self.size = b.normalise(text).upper(), size
        self.fill, self.color = fill, color

    def _f(self, c, k):
        return b.font("mono", c.px(self.size) * max(0.8, k), 700)

    def measure(self, c, width, k):
        f = self._f(c, k)
        return (f.size * 1.05) + c.px(20) * k

    def draw(self, c, x, y, width, k):
        f = self._f(c, k)
        tr = f.size * b.LABEL_TRACK
        tw = b.tracked_width(f, self.text, tr)
        padx, pady = f.size * 0.55, f.size * 0.42
        h = self.measure(c, width, k)
        c.d.rectangle([x, y, x + tw + padx * 2, y + h], fill=self.fill or c.accent_rgb)
        b.draw_tracked(c.d, (x + padx, y + pady * 0.62), self.text, f,
                       self.color or b.INK, tracking=tr)
        box = Box(x, y, x + tw + padx * 2, y + h, "chip")
        c.record(box)
        return box


class Numeral(Block):
    """Violet numerals — the board reserves violet for stats."""

    def __init__(self, text, size=250, color=None, align="left", gap=0):
        super().__init__(gap)
        self.text, self.size, self.color, self.align = str(text), size, color, align

    def _fit(self, c, width, k):
        size = c.px(self.size) * k
        f = b.font("display", size, 700)
        tr = size * -0.02
        while b.tracked_width(f, self.text, tr) > width and size > c.px(60):
            size *= 0.96
            f = b.font("display", size, 700)
            tr = size * -0.02
        return f, size, tr

    def measure(self, c, width, k):
        f, size, tr = self._fit(c, width, k)
        t, bot = b.ink_extent(f, [self.text], tr)
        return bot - t

    def draw(self, c, x, y, width, k):
        f, size, tr = self._fit(c, width, k)
        t, _ = b.ink_extent(f, [self.text], tr)
        w = b.tracked_width(f, self.text, tr)
        x0 = x + (width - w) / 2 if self.align == "center" else x
        bb = b.draw_tracked(c.d, (x0, y - t), self.text, f,
                            self.color or b.VIOLET, tracking=tr)
        box = Box(*bb)
        box.name = "numeral"
        c.record(box)
        return box


class Rows(Block):
    """List rows in four cuts, straight off the board:
       numbered  · 01/02 mono index, accent-coloured (IG list cover)
       check     · outlined checkbox, one filled volt (Pinterest printable)
       hairline  · plain text on a hairline rule (Pinterest list pin)
       tease     · numbered, final row redacted to a bar (TikTok list tease)
    """

    def __init__(self, items, mode="numbered", size=48, gap=0, row_gap=34,
                 index_color=None, text_color=None, max_lines=2, index_size=None,
                 family=None):
        super().__init__(gap)
        self.items = [b.normalise(i) for i in items if b.normalise(i)]
        self.mode, self.size, self.row_gap = mode, size, row_gap
        self.index_color, self.text_color = index_color, text_color
        self.max_lines = max_lines
        self.index_size = index_size
        self.family = family or ("display" if mode in ("numbered", "tease") else "body")

    def _fonts(self, c, k):
        size = c.px(self.size) * k
        ft = b.font(self.family, size, 500)
        fi = b.font("mono", c.px(self.index_size or self.size * 0.62) * k, 700)
        return ft, fi, size

    def _layout(self, c, width, k):
        ft, fi, size = self._fonts(c, k)
        if self.mode == "check":
            indent = size * 1.42
        elif self.mode == "hairline":
            indent = 0.0
        else:   # index column, measured off the real index glyphs
            indent = b.tracked_width(fi, "00", fi.size * 0.06) + size * 0.62
        tw = width - indent
        tr = size * {"display": -0.02, "mono": 0.02}.get(self.family, 0.0)
        rows, total = [], 0.0
        n = len(self.items)
        for i, it in enumerate(self.items, 1):
            redacted = (self.mode == "tease" and i == n)
            lines = [] if redacted else [ln for ln, _ in b.wrap_indexed(it, ft, tw, tr)][:self.max_lines]
            if redacted:
                h = size * 0.9
            else:
                top, bot = b.ink_extent(ft, lines, tr)
                h = (len(lines) - 1) * size * 1.16 + (bot - top)
            rows.append((lines, h, redacted))
            total += h
            if i < n:
                total += c.px(self.row_gap) * k
        return ft, fi, size, indent, tr, rows, total

    def measure(self, c, width, k):
        if not self.items:
            return 0.0
        return self._layout(c, width, k)[6]

    def draw(self, c, x, y, width, k):
        if not self.items:
            return Box(x, y, x, y)
        ft, fi, size, indent, tr, rows, total = self._layout(c, width, k)
        icol = self.index_color if self.index_color is not None else c.accent_rgb
        tcol = self.text_color if self.text_color is not None else c.fg
        box = None
        yy = y
        for i, (lines, h, redacted) in enumerate(rows, 1):
            if self.mode in ("numbered", "tease"):
                itop, _ = b.ink_extent(fi, [f"{i:02d}"], fi.size * 0.06)
                bb = b.draw_tracked(c.d, (x, yy + size * 0.10 - itop), f"{i:02d}", fi,
                                    icol if not redacted else c.muted,
                                    tracking=fi.size * 0.06)
                box = Box(*bb).union(box)
            elif self.mode == "check":
                s = size * 0.72
                filled = (i == len(rows))
                c.d.rectangle([x, yy + size * 0.06, x + s, yy + size * 0.06 + s],
                              outline=None if filled else c.muted,
                              fill=c.accent_rgb if filled else None,
                              width=max(2, int(c.px(3) * k)))
                box = Box(x, yy + size * 0.06, x + s, yy + size * 0.06 + s).union(box)
            if redacted:
                bw = width * 0.30
                c.d.rectangle([x + indent, yy + size * 0.34,
                               x + indent + bw, yy + size * 0.34 + c.px(6)],
                              fill=c.muted)
                box = Box(x + indent, yy + size * 0.34,
                          x + indent + bw, yy + size * 0.34 + c.px(6)).union(box)
            else:
                top, _ = b.ink_extent(ft, lines, tr)
                ly = yy - top
                for ln in lines:
                    bb = b.draw_tracked(c.d, (x + indent, ly), ln, ft, tcol, tracking=tr)
                    box = Box(*bb).union(box)
                    ly += size * 1.16
            if self.mode == "hairline" and i < len(rows):
                ry = yy + h + c.px(self.row_gap) * k * 0.5
                c.d.line([(x, ry), (x + width, ry)], fill=c.hairline,
                         width=max(1, int(c.px(2) * k)))
                box = Box(x, ry, x + width, ry + 1).union(box)
            yy += h + c.px(self.row_gap) * k
        out = box or Box(x, y, x, y)
        out.name = "rows"
        c.record(out)
        return out


class Plate(Block):
    """An inset designed plate — the board's 'photo' slot, filled with brand
    texture instead of stock photography so the asset ships finished."""

    def __init__(self, height, treatment="chevron", gap=0, bleed=False, label=None,
                 mood="ink"):
        super().__init__(gap)
        self.height, self.treatment, self.bleed = height, treatment, bleed
        self.label, self.mood = label, mood

    def measure(self, c, width, k):
        return c.px(self.height) * (0.80 + 0.20 * k)

    def draw(self, c, x, y, width, k):
        h = self.measure(c, width, k)
        x0, w = (0, c.w) if self.bleed else (x, width)
        c.paste_plate(int(x0), int(y), int(w), int(h), self.treatment, self.mood)
        if self.label:
            f = b.font("mono", c.px(26) * max(0.85, k), 600)
            b.draw_tracked(c.d, (x0 + c.px(30), y + c.px(26)), self.label.upper(), f,
                           c.accent_rgb, tracking=f.size * b.LABEL_TRACK)
        box = Box(x0, y, x0 + w, y + h, "plate")
        c.record(box)
        return box


class Group(Block):
    """Several blocks measured and drawn as one — lets a composite sit inside
    another block (a side rule, a panel) without breaking the fit pass."""

    def __init__(self, *blocks, gap=0, optional=False):
        super().__init__(gap, optional)
        self.blocks = [x for x in blocks if x is not None]

    def measure(self, c, width, k):
        total, first = 0.0, True
        for blk in self.blocks:
            if not first:
                total += blk.gap_px(c, k)
            total += blk.measure(c, width, k)
            first = False
        return total

    def draw(self, c, x, y, width, k):
        out, first, yy = None, True, y
        for blk in self.blocks:
            if not first:
                yy += blk.gap_px(c, k)
            h = blk.measure(c, width, k)
            box = blk.draw(c, x, yy, width, k)
            out = box.union(out) if out else box
            yy += h
            first = False
        return out or Box(x, y, x, y)


class SideRule(Block):
    """A vertical violet rule with text beside it (LinkedIn quote card)."""

    def __init__(self, child, gap=0, thickness=10, color=None, pad=34):
        super().__init__(gap)
        self.child, self.th, self.color, self.pad = child, thickness, color, pad

    def _inset(self, c, k):
        return c.px(self.th) * max(0.8, k) + c.px(self.pad) * k

    def measure(self, c, width, k):
        return self.child.measure(c, width - self._inset(c, k), k)

    def draw(self, c, x, y, width, k):
        ins = self._inset(c, k)
        h = self.child.measure(c, width - ins, k)
        tw = c.px(self.th) * max(0.8, k)
        c.d.rectangle([x, y, x + tw, y + h], fill=self.color or b.VIOLET)
        c.record(Box(x, y, x + tw, y + h, "siderule"))
        return self.child.draw(c, x + ins, y, width - ins, k).union(
            Box(x, y, x + tw, y + h, "siderule"))


# ---------------------------------------------------------------- STACK
class Stack:
    """Blocks placed in order inside a region, at the largest type that fits."""

    def __init__(self, *blocks, align="top"):
        self.blocks = [x for x in blocks if x is not None]
        self.align = align

    def _measure(self, c, blocks, width, k):
        total, first = 0.0, True
        for blk in blocks:
            if not first:
                total += blk.gap_px(c, k)
            total += blk.measure(c, width, k)
            first = False
        return total

    def fit(self, c, region, width=None):
        width = width if width is not None else region.w
        blocks = list(self.blocks)
        while True:
            k = 1.0
            while k >= MIN_SHRINK - 1e-6:
                if self._measure(c, blocks, width, k) <= region.h:
                    return blocks, k
                k -= SHRINK_STEP
            drop = next((i for i in range(len(blocks) - 1, -1, -1) if blocks[i].optional), None)
            if drop is None:
                return blocks, MIN_SHRINK
            blocks.pop(drop)

    def render(self, c, region, width=None):
        width = width if width is not None else region.w
        blocks, k = self.fit(c, region, width)
        total = self._measure(c, blocks, width, k)
        if self.align == "center":
            y = region.y0 + (region.h - total) / 2
        elif self.align == "bottom":
            y = region.y1 - total
        else:
            y = region.y0
        out, first = None, True
        for blk in blocks:
            if not first:
                y += blk.gap_px(c, k)
            h = blk.measure(c, width, k)
            box = blk.draw(c, region.x0, y, width, k)
            out = box.union(out) if out else box
            y += h
            first = False
        return out or Box(region.x0, region.y0, region.x0, region.y0)
