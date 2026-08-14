# -*- coding: utf-8 -*-
"""
The template library.

Every named template on the design board is here — the five Instagram covers,
the four TikTok/Reels frames, the four Pinterest pins and the LinkedIn set —
plus the carousel interiors and X cards the board implies. Templates differ by
*structure* (where the content region sits, how it is split, which components
carry it), not by colour swap, so a grid of them reads as texture.

Every template is a Stack rendered into a measured region, so type is set at
the largest size that still fits and nothing can land on anything else.

No URL is stamped anywhere: the board calls for one, but this brand has no
live domain, so the real handle carries the mark instead.
"""
import engine.brand as b
from engine.layout import (Stack, Text, Rows, Rule, Numeral, Chip,
                           Spectrum, Plate, SideRule, Group, Box)
from engine.surface import Canvas

HANDLE = "@gogettrdaily"
MARK = "GOGETTR"


# ---------------------------------------------------------------- helpers
def _acc(spec):
    return spec.get("accent", "volt")


def _span(text, spec, mode="colour"):
    """The phrase the board would set in volt. A highlighter box is tighter
    than coloured type, so it takes the shorter phrase."""
    if spec.get("no_accent"):
        return None
    phrase = spec.get("accent_phrase")
    if phrase:
        t, p = b.normalise(text), b.normalise(phrase)
        i = t.find(p)
        return (i, i + len(p)) if i >= 0 else None
    if mode == "highlight":
        return b.accent_span(text, max_words=2, max_share=0.32)
    return b.accent_span(text, max_words=3, max_share=0.34)


def _hook(c, spec, text=None, size=116, max_lines=4, min_size=46, color=None,
          align="left", gap=0, accent=True, mode=None):
    t = text if text is not None else spec.get("hook", "")
    m = mode or c.accent_text_mode
    return Text(t, size=size, max_lines=max_lines, min_size=min_size, color=color,
                align=align, gap=gap,
                accent=_span(t, spec, m) if accent else None,
                accent_mode=m,
                accent_color=c.accent_text if m == "colour" else c.accent_rgb)


def _sub(c, spec, size=38, gap=30, color=None, align="left", max_lines=3, key="sub"):
    t = spec.get(key)
    if not t:
        return None
    return Text(t, family="body", size=size, min_size=26, max_lines=max_lines,
                color=color if color is not None else c.sub_col, gap=gap,
                align=align, optional=True)


def _head(c, spec, eyebrow=None, index=None, eb_color=None, ix_color=None,
          pad=58):
    """Draw the top labels and return the y the content region may start at."""
    e = c.eyebrow(spec.get("eyebrow", eyebrow), color=eb_color)
    i = c.index_chip(spec.get("index", index), color=ix_color)
    ys = [x.y1 for x in (e, i) if x]
    return (max(ys) + c.px(pad)) if ys else c.top_safe


def _foot(c, spec, left=HANDLE, right=None, badge=False):
    return c.footer(left=spec.get("footer_left", left),
                    right=spec.get("footer_right", right), badge=badge)


# ================================================================ INSTAGRAM
def ig_spectrum(fmt, spec):
    """01 SPECTRUM HOOK — violet/volt/chrome ticks over a bottom-set hook."""
    c = Canvas(fmt, ground=spec.get("ground", "graphite"),
               plate_treatment=spec.get("plate"), plate_mood=spec.get("mood", "ink"),
               accent=_acc(spec))
    region = c.region(top=_head(c, spec, eyebrow=None))
    Stack(Spectrum(),
          _hook(c, spec, size=118, max_lines=4, gap=44),
          _sub(c, spec, gap=34),
          align="bottom").render(c, region)
    _foot(c, spec, right="SAVE THIS →")
    return c.img


def ig_list(fmt, spec):
    """02 LIST COVER — light ground, volt highlighter, numbered rows."""
    c = Canvas(fmt, ground=spec.get("ground", "chrome"), accent="volt")
    top = _head(c, spec, eb_color=b.VIOLET, pad=48)
    region = c.region(top=top)
    Stack(_hook(c, spec, size=100, max_lines=3, mode="highlight"),
          Rows(spec.get("items", [])[:4], mode="numbered", family="mono",
               size=34, gap=54, row_gap=30, index_color=b.VIOLET,
               text_color=b.INK_SOFT, max_lines=1),
          align="top").render(c, region)
    _foot(c, spec, left=spec.get("footer_left", "1 / 7"), right="SWIPE →")
    return c.img


def ig_photo(fmt, spec):
    """03 INSET PHOTO — inset plate up top, hook underneath."""
    c = Canvas(fmt, ground=spec.get("ground", "ink"), accent=_acc(spec))
    region = c.region(top=_head(c, spec))
    Stack(Plate(spec.get("plate_h", 560), spec.get("treatment", "chevron"),
                mood=spec.get("mood", "graphite"), label=spec.get("kicker")),
          _hook(c, spec, size=98, max_lines=4, gap=64),
          align="top").render(c, region)
    _foot(c, spec, right="READ MORE →")
    return c.img


def ig_stat(fmt, spec):
    """04 STAT — a violet numeral, centred, with the line it answers."""
    c = Canvas(fmt, ground=spec.get("ground", "chrome"), accent="volt")
    region = c.region(top=_head(c, spec, eb_color=b.VIOLET))
    Stack(Numeral(spec.get("numeral", "1"), size=300, align="center"),
          Text(spec.get("numeral_label", spec.get("hook", "")), size=62,
               min_size=34, max_lines=3, align="center", gap=46,
               color=b.INK),
          _sub(c, spec, gap=30, align="center", color=b.INK_FAINT),
          align="center").render(c, region)
    _foot(c, spec, right="SAVE THIS →")
    return c.img


def ig_quote(fmt, spec):
    """05 VIOLET QUOTE — the most saveable line, one to a card."""
    c = Canvas(fmt, ground=spec.get("ground", "violet"), accent="volt")
    region = c.region(top=_head(c, spec, eb_color=c.muted))
    Stack(_hook(c, spec, text=spec.get("quote", spec.get("hook", "")),
                size=112, max_lines=5, color=b.WHITE, accent=False),
          Rule(0.20, gap=42),
          _sub(c, spec, gap=36),
          align="center").render(c, region)
    _foot(c, spec, right="SAVE THIS →")
    return c.img


def ig_rule(fmt, spec):
    """A light cover that leads with the bar and sets the line beneath it —
    the light slot in the rotation when a day has no number to show."""
    c = Canvas(fmt, ground=spec.get("ground", "chrome"), accent="volt")
    region = c.region(top=_head(c, spec, eb_color=b.VIOLET, pad=46))
    Stack(Rule(0.30, thickness=16),
          _hook(c, spec, size=104, max_lines=4, gap=46, mode="highlight",
                color=b.INK),
          _sub(c, spec, gap=34, color=b.INK_SOFT),
          align="bottom").render(c, region)
    _foot(c, spec, right="SAVE THIS →")
    return c.img


# ================================================================ INTERIORS
def beat_stat(fmt, spec):
    """Interior: the number, on the dark ground, mid-carousel."""
    c = Canvas(fmt, ground=spec.get("ground", "ink"), accent="volt")
    region = c.region(top=_head(c, spec))
    Stack(Numeral(spec.get("numeral", "1"), size=260),
          Rule(0.22, gap=38),
          Text(spec.get("numeral_label", spec.get("hook", "")), size=68,
               min_size=34, max_lines=3, gap=38, color=c.fg),
          align="center").render(c, region)
    _foot(c, spec)
    return c.img


def beat_number(fmt, spec):
    """Interior: an oversized violet step numeral over the beat."""
    c = Canvas(fmt, ground=spec.get("ground", "graphite"), accent=_acc(spec))
    region = c.region(top=_head(c, spec))
    Stack(Numeral(spec.get("step", "01"), size=170, color=b.VIOLET),
          _hook(c, spec, size=96, max_lines=4, gap=54),
          _sub(c, spec, gap=30),
          align="center").render(c, region)
    _foot(c, spec)
    return c.img


def beat_split(fmt, spec):
    """Interior: full-bleed plate band over the beat."""
    c = Canvas(fmt, ground=spec.get("ground", "graphite"), accent=_acc(spec))
    ph = int(c.h * spec.get("plate_ratio", 0.38))
    c.paste_plate(0, 0, c.w, ph, spec.get("treatment", "hatch"),
                  spec.get("mood", "ink"))
    c.record(Box(0, 0, c.w, ph, "plate"))
    if spec.get("kicker"):
        c.label(spec["kicker"], c.mx, c.my, size=28, color=b.VOLT)
    if spec.get("index"):
        c.label(spec["index"], c.w - c.mx, c.my, size=26, anchor="ra",
                color=b.VOLT)
    region = c.region(top=ph + c.px(96))
    Stack(_hook(c, spec, size=98, max_lines=5),
          _sub(c, spec, gap=30),
          align="top").render(c, region)
    _foot(c, spec)
    return c.img


def beat_center(fmt, spec):
    """Interior: one line, centred, nothing else on the card."""
    c = Canvas(fmt, ground=spec.get("ground", "ink"), accent=_acc(spec))
    region = c.region(top=_head(c, spec, eyebrow=None, index=None))
    Stack(_hook(c, spec, size=110, max_lines=4, align="center"),
          Rule(0.16, gap=46, align="center"),
          align="center").render(c, region)
    _foot(c, spec)
    return c.img


def beat_highlight(fmt, spec):
    """Interior: light card, the operative phrase boxed in volt."""
    c = Canvas(fmt, ground=spec.get("ground", "chrome"), accent="volt")
    region = c.region(top=_head(c, spec, eb_color=b.VIOLET, ix_color=b.VIOLET))
    Stack(_hook(c, spec, size=100, max_lines=4, mode="highlight", color=b.INK),
          _sub(c, spec, gap=34, color=b.INK_SOFT),
          align="center").render(c, region)
    _foot(c, spec)
    return c.img


def beat_rail(fmt, spec):
    """Interior: a step rail down the gutter, beat beside it."""
    c = Canvas(fmt, ground=spec.get("ground", "graphite"), accent=_acc(spec))
    top = _head(c, spec)
    rail_w = c.px(30)
    region = c.region(top=top, inset=rail_w + c.px(46))
    box = Stack(_hook(c, spec, size=96, max_lines=5),
                _sub(c, spec, gap=30),
                align="center").render(c, region)
    n = max(1, int(spec.get("of", 5)))
    k = max(1, min(n, int(spec.get("k", 1))))
    x = c.mx + rail_w / 2
    y0, y1 = box.y0, max(box.y1, box.y0 + c.px(120))
    c.d.line([(x, y0), (x, y1)], fill=c.hairline, width=max(1, int(c.px(3))))
    step = (y1 - y0) / max(1, n - 1) if n > 1 else 0
    for i in range(n):
        cy = y0 + step * i
        r = c.px(11) if i == k - 1 else c.px(6)
        col = c.accent_rgb if i == k - 1 else c.muted
        c.d.ellipse([x - r, cy - r, x + r, cy + r], fill=col)
    c.record(Box(x - c.px(11), y0 - c.px(11), x + c.px(11), y1 + c.px(11), "rail"))
    _foot(c, spec)
    return c.img


def beat_rows(fmt, spec):
    """Interior: the whole system as a checklist, one card."""
    c = Canvas(fmt, ground=spec.get("ground", "chrome"), accent="volt")
    region = c.region(top=_head(c, spec, eb_color=b.VIOLET))
    Stack(_hook(c, spec, size=76, max_lines=2, color=b.INK, accent=False),
          Rows(spec.get("items", [])[:5], mode="check", size=40, gap=52,
               row_gap=30, text_color=b.INK, max_lines=2),
          align="top").render(c, region)
    _foot(c, spec)
    return c.img


def beat_ledger(fmt, spec):
    """Interior: hairline rows — a ledger of the beats."""
    c = Canvas(fmt, ground=spec.get("ground", "graphite"), accent=_acc(spec))
    region = c.region(top=_head(c, spec))
    Stack(_hook(c, spec, size=74, max_lines=2, accent=False),
          Rows(spec.get("items", [])[:5], mode="hairline", size=40, gap=56,
               row_gap=48, text_color=c.fg, max_lines=2),
          align="top").render(c, region)
    _foot(c, spec)
    return c.img


def beat_quote(fmt, spec):
    """Interior: the quotable turn, set as a plate card."""
    c = Canvas(fmt, ground=spec.get("ground", "ink"),
               plate_treatment=spec.get("plate"), plate_mood=spec.get("mood", "violet"),
               accent=_acc(spec))
    region = c.region(top=_head(c, spec))
    Stack(Text("“", size=132, min_size=84, max_lines=1, color=c.accent_rgb),
          _hook(c, spec, text=spec.get("quote", spec.get("hook", "")),
                size=100, max_lines=4, gap=26, accent=False),
          Rule(0.18, gap=40),
          align="center").render(c, region)
    _foot(c, spec)
    return c.img


def close_follow(fmt, spec):
    """Close: the mark, the ask, the bar."""
    c = Canvas(fmt, ground=spec.get("ground", "ink"), accent=_acc(spec))
    region = c.region(top=c.top_safe)
    box = Stack(_hook(c, spec, text=spec.get("cta_hook", spec.get("hook", "")),
                      size=100, max_lines=4),
                Rule(0.24, gap=40),
                _sub(c, spec, gap=34),
                align="center").render(c, region)
    c.mark(c.mx, box.y0 - c.px(150), c.px(96))
    _foot(c, spec, right="FOLLOW →")
    return c.img


def close_volt(fmt, spec):
    """Close: full-bleed volt, ink type — the loudest card in the set."""
    c = Canvas(fmt, ground="volt", accent="volt")
    region = c.region(top=_head(c, spec, eb_color=c.muted))
    Stack(_hook(c, spec, text=spec.get("cta_hook", spec.get("hook", "")),
                size=110, max_lines=4, color=b.INK, accent=False),
          Rule(0.22, gap=44, color=b.INK),
          align="center").render(c, region)
    c.footer(left=HANDLE, right="FOLLOW →", left_color=c.muted, right_color=b.INK)
    return c.img


def close_violet(fmt, spec):
    """Close: violet card, white ask, volt bar."""
    c = Canvas(fmt, ground="violet", accent="volt")
    region = c.region(top=_head(c, spec, eb_color=c.muted))
    Stack(_hook(c, spec, text=spec.get("cta_hook", spec.get("hook", "")),
                size=104, max_lines=4, color=b.WHITE, accent=False),
          Rule(0.22, gap=42),
          align="center").render(c, region)
    _foot(c, spec, right="FOLLOW →")
    return c.img


# ================================================================ VERTICAL
def v_coldopen(fmt, spec):
    """01 COLD-OPEN HOOK — hatched UI bands, text inside the middle 60%."""
    c = Canvas("vert", ground=spec.get("ground", "graphite"), accent=_acc(spec))
    c.ui_bands(alpha=spec.get("band_alpha", 26))
    region = c.region(top=c.top_safe + c.px(40), reserve_footer=False,
                      bottom=c.bot_safe - c.px(120))
    Stack(Spectrum(),
          _hook(c, spec, size=124, max_lines=4, gap=48),
          _sub(c, spec, gap=34),
          align="center").render(c, region)
    c.vert_handle()
    return c.img


def v_day(fmt, spec):
    """02 DAY COUNTER — full-bleed volt, ink type."""
    c = Canvas("vert", ground="volt", accent="volt")
    region = c.region(top=c.top_safe + c.px(60), reserve_footer=False,
                      bottom=c.bot_safe - c.px(120))
    Stack(Text(spec.get("day") or spec.get("eyebrow", MARK), family="mono",
               size=38, weight=700, max_lines=1, color=c.muted, upper=True),
          _hook(c, spec, size=118, max_lines=4, color=b.INK, accent=False, gap=42),
          _sub(c, spec, gap=32),
          align="center").render(c, region)
    c.vert_handle(color=c.muted)
    return c.img


def v_broll(fmt, spec):
    """03 B-ROLL + PLATE — a plate ground with a volt chip label."""
    c = Canvas("vert", ground="ink", plate_treatment=spec.get("treatment", "sweep"),
               plate_mood=spec.get("mood", "graphite"), accent=_acc(spec))
    region = c.region(top=c.top_safe + c.px(40), reserve_footer=False,
                      bottom=c.bot_safe - c.px(120))
    Stack(Chip(spec.get("kicker", "STACK")),
          _hook(c, spec, size=124, max_lines=5, gap=46),
          align="center").render(c, region)
    c.vert_handle()
    return c.img


def v_listtease(fmt, spec):
    """04 LIST TEASE — the last row redacted so the swipe is owed."""
    c = Canvas("vert", ground=spec.get("ground", "ink"), accent=_acc(spec))
    region = c.region(top=c.top_safe + c.px(40), reserve_footer=False,
                      bottom=c.bot_safe - c.px(120))
    items = list(spec.get("items", []))[:3] + [""]
    Stack(_hook(c, spec, size=104, max_lines=3),
          Rows([i for i in items if i] + ["—"], mode="tease", family="mono",
               size=34, gap=56, row_gap=30, text_color=c.muted, max_lines=1),
          align="center").render(c, region)
    c.vert_handle()
    return c.img


def v_stat(fmt, spec):
    """Vertical stat frame — violet numeral, one line under it."""
    c = Canvas("vert", ground=spec.get("ground", "graphite"), accent="volt")
    region = c.region(top=c.top_safe + c.px(40), reserve_footer=False,
                      bottom=c.bot_safe - c.px(120))
    Stack(Numeral(spec.get("numeral", "1"), size=280),
          Text(spec.get("numeral_label", spec.get("hook", "")), size=74,
               min_size=40, max_lines=4, gap=40, color=c.fg),
          align="center").render(c, region)
    c.vert_handle()
    return c.img


def v_quote(fmt, spec):
    """Vertical turn frame — violet card, the quotable line."""
    c = Canvas("vert", ground=spec.get("ground", "violet"), accent="volt")
    region = c.region(top=c.top_safe + c.px(40), reserve_footer=False,
                      bottom=c.bot_safe - c.px(120))
    Stack(_hook(c, spec, text=spec.get("quote", spec.get("hook", "")),
                size=120, max_lines=5, color=b.WHITE, accent=False),
          Rule(0.20, gap=44),
          align="center").render(c, region)
    c.vert_handle(color=c.muted)
    return c.img


def v_step(fmt, spec):
    """Vertical step frame — index chip and one beat."""
    c = Canvas("vert", ground=spec.get("ground", "graphite"),
               plate_treatment=spec.get("plate"), plate_mood=spec.get("mood", "ink"),
               accent=_acc(spec))
    region = c.region(top=c.top_safe + c.px(40), reserve_footer=False,
                      bottom=c.bot_safe - c.px(120))
    Stack(Chip(spec.get("index", "01"), fill=c.accent_rgb),
          _hook(c, spec, size=118, max_lines=5, gap=44),
          align="center").render(c, region)
    c.vert_handle()
    return c.img


def v_end(fmt, spec):
    """End card — the mark and the ask, at the END (retention rule)."""
    ground = spec.get("ground", "ink")
    c = Canvas("vert", ground=ground, accent=_acc(spec))
    region = c.region(top=c.top_safe + c.px(120), reserve_footer=False,
                      bottom=c.bot_safe - c.px(140))
    txt = spec.get("cta_hook", "Follow for more.")
    box = Stack(Text(txt, size=92, min_size=48, max_lines=3, align="center",
                     color=c.fg),
                Rule(0.22, gap=44, align="center", max_width=190,
                     color=b.INK if ground == "volt" else c.accent_rgb),
                align="center").render(c, region)
    h = c.px(120)
    c.mark(c.w / 2 - h * 0.58, box.y0 - h - c.px(70), h,
           color=b.INK if ground == "volt" else c.accent_rgb)
    c.label(HANDLE, c.w / 2, c.bot_safe - c.px(46), size=30, anchor="ma",
            color=c.muted if ground == "volt" else c.accent_rgb)
    return c.img


# ================================================================ PINTEREST
def pin_list(fmt, spec):
    """01 LIST PIN — keyword eyebrow, hairline rows, mark at the foot."""
    c = Canvas("pin", ground=spec.get("ground", "chrome"), accent="volt")
    top = _head(c, spec, eyebrow=spec.get("keyword"), eb_color=b.VIOLET, pad=44)
    region = c.region(top=top)
    Stack(_hook(c, spec, size=88, max_lines=3, color=b.INK, mode="highlight"),
          Rows(spec.get("items", [])[:5], mode="hairline", size=34, gap=50,
               row_gap=44, text_color=b.INK_SOFT, max_lines=2),
          align="top").render(c, region)
    c.footer(left=HANDLE, right=None, badge=True)
    return c.img


def pin_printable(fmt, spec):
    """02 PRINTABLE — dark title band over a checklist."""
    c = Canvas("pin", ground="chrome", accent="volt")
    bh = int(c.h * 0.30)
    c.d.rectangle([0, 0, c.w, bh], fill=b.GRAPHITE)
    c.record(Box(0, 0, c.w, bh, "band"))
    band = Box(c.mx, c.my * 0.72, c.w - c.mx, bh - c.px(46))
    Stack(Text(spec.get("kicker", "CHECKLIST"), family="mono", size=26, weight=700,
               max_lines=1, color=b.VOLT, upper=True),
          Text(spec.get("hook", ""), size=80, min_size=40, max_lines=3, gap=30,
               color=b.WHITE),
          align="center").render(c, band)
    region = c.region(top=bh + c.px(78))
    Stack(Rows(spec.get("items", [])[:5], mode="check", size=36, gap=0,
               row_gap=34, text_color=b.INK, max_lines=2),
          align="top").render(c, region)
    c.footer(left=HANDLE, right=None, badge=True)
    return c.img


def pin_photo(fmt, spec):
    """03 PHOTO-TOP — plate above, keyword and the line below."""
    c = Canvas("pin", ground="chrome", accent="volt")
    ph = int(c.h * spec.get("plate_ratio", 0.42))
    c.paste_plate(0, 0, c.w, ph, spec.get("treatment", "rings"),
                  spec.get("mood", "graphite"))
    c.record(Box(0, 0, c.w, ph, "plate"))
    top = ph + c.px(70)
    eb = c.eyebrow(spec.get("keyword"), color=b.VIOLET, y=top)
    region = c.region(top=(eb.y1 + c.px(44)) if eb else top)
    Stack(_hook(c, spec, size=84, max_lines=4, color=b.INK, mode="highlight"),
          _sub(c, spec, gap=34, color=b.INK_SOFT, max_lines=4),
          align="top").render(c, region)
    c.footer(left=HANDLE, right=None, badge=True)
    return c.img


def pin_rule(fmt, spec):
    """04 RULE PIN — violet ground, the one-line rule."""
    c = Canvas("pin", ground="violet", accent="volt")
    top = _head(c, spec, eyebrow=spec.get("keyword"), eb_color=c.muted, pad=44)
    region = c.region(top=top)
    Stack(_hook(c, spec, text=spec.get("quote", spec.get("hook", "")),
                size=100, max_lines=5, color=b.WHITE, accent=False),
          Rule(0.22, gap=40),
          _sub(c, spec, gap=34, max_lines=4),
          align="center").render(c, region)
    c.footer(left=HANDLE, right=None, badge=True)
    return c.img


# ================================================================ LINKEDIN
def li_carousel(fmt, spec):
    """03 CAROUSEL COVER — calm register, the value lives in the caption."""
    c = Canvas("square", ground=spec.get("ground", "ink"), accent="volt")
    top = _head(c, spec, eb_color=b.VOLT, pad=52)
    region = c.region(top=top)
    Stack(_hook(c, spec, size=92, max_lines=4, accent=False),
          _sub(c, spec, gap=34),
          align="center").render(c, region)
    c.footer(left=MARK, right=spec.get("footer_right", "READ →"))
    return c.img


def li_stat(fmt, spec):
    """04 STAT CARD — violet numeral, the sentence it settles."""
    c = Canvas("square", ground="chrome", accent="volt")
    top = _head(c, spec, eb_color=b.VIOLET, pad=48)
    region = c.region(top=top)
    Stack(Numeral(spec.get("numeral", "1"), size=250),
          Text(spec.get("numeral_label", spec.get("hook", "")), size=66,
               min_size=34, max_lines=3, gap=36, color=b.INK),
          align="center").render(c, region)
    c.footer(left=MARK, right=None)
    return c.img


def li_quote(fmt, spec):
    """02 QUOTE CARD — violet side rule, quiet type."""
    c = Canvas("square", ground="chrome", accent="volt")
    region = c.region(top=_head(c, spec, eb_color=b.VIOLET, pad=48))
    Stack(SideRule(Group(
              Text("“%s”" % b.normalise(spec.get("quote", spec.get("hook", ""))),
                   size=86, min_size=36, max_lines=5, color=b.INK),
              _sub(c, spec, gap=30, color=b.INK_SOFT, max_lines=3))),
          align="center").render(c, region)
    c.footer(left=MARK, right=None)
    return c.img


def li_note(fmt, spec):
    """A LinkedIn note card — the system in hairline rows."""
    c = Canvas("square", ground=spec.get("ground", "graphite"), accent="volt")
    region = c.region(top=_head(c, spec, eb_color=b.VOLT, pad=50))
    Stack(_hook(c, spec, size=70, max_lines=2, accent=False),
          Rows(spec.get("items", [])[:4], mode="hairline", size=38, gap=50,
               row_gap=42, text_color=c.fg, max_lines=2),
          align="top").render(c, region)
    c.footer(left=MARK, right=None)
    return c.img


# ================================================================ X / TWITTER
def x_headline(fmt, spec):
    """The hook, set wide, with the mark on the baseline."""
    c = Canvas("wide", ground=spec.get("ground", "graphite"),
               plate_treatment=spec.get("plate"), plate_mood=spec.get("mood", "ink"),
               accent=_acc(spec))
    region = c.region(top=_head(c, spec, eb_color=c.accent_rgb, pad=44))
    Stack(_hook(c, spec, size=112, max_lines=3),
          _sub(c, spec, gap=30),
          align="center").render(c, region)
    _foot(c, spec, badge=True, left=HANDLE)
    return c.img


def x_stat(fmt, spec):
    """Numeral column and label column, each measured against the other."""
    c = Canvas("wide", ground=spec.get("ground", "chrome"), accent="volt")
    light = c.light
    top = _head(c, spec, eb_color=b.VIOLET if light else c.accent_rgb, pad=40)
    region = c.region(top=top)
    num = Numeral(spec.get("numeral", "1"), size=280)
    nw = min(region.w * 0.42, c.px(560))
    nh = num.measure(c, nw, 1.0)
    ny = region.y0 + (region.h - nh) / 2
    nbox = num.draw(c, region.x0, ny, nw, 1.0)
    right = Box(nbox.x1 + c.px(70), region.y0, region.x1, region.y1)
    Stack(Rule(0.30, thickness=12, gap=0),
          Text(spec.get("numeral_label", spec.get("hook", "")), size=64,
               min_size=32, max_lines=4, gap=32,
               color=b.INK if light else c.fg),
          align="center").render(c, right)
    _foot(c, spec, badge=True, left=HANDLE)
    return c.img


def x_quote(fmt, spec):
    """Quote card — violet side rule, calm ground."""
    c = Canvas("wide", ground=spec.get("ground", "chrome"), accent="volt")
    region = c.region(top=_head(c, spec, eb_color=b.VIOLET, pad=40))
    Stack(SideRule(Text("“%s”" % b.normalise(spec.get("quote", spec.get("hook", ""))),
                        size=90, min_size=38, max_lines=4,
                        color=b.INK if c.light else c.fg)),
          align="center").render(c, region)
    _foot(c, spec, badge=True, left=HANDLE)
    return c.img


def x_split(fmt, spec):
    """A coloured panel carries the label; the hook takes the rest."""
    c = Canvas("wide", ground=spec.get("ground", "ink"), accent=_acc(spec))
    pw = int(c.w * 0.34)
    panel = spec.get("panel", "violet")
    fill = b.VIOLET if panel == "violet" else b.VOLT
    c.d.rectangle([0, 0, pw, c.h], fill=fill)
    c.record(Box(0, 0, pw, c.h, "panel"))
    ptext = b.WHITE if panel == "violet" else b.INK
    c.safe_x0 = c.px(64)                       # the panel is its own column
    pregion = Box(c.px(64), c.my, pw - c.px(56), c.h - c.my)
    Stack(Text(spec.get("eyebrow", "GOGETTR"), family="mono", size=26, weight=700,
               max_lines=2, color=ptext, upper=True),
          Text(spec.get("panel_line", spec.get("quote", "")), size=54, min_size=28,
               max_lines=5, gap=34, color=ptext, optional=True),
          align="center").render(c, pregion)
    band = c.footer_band()
    region = Box(pw + c.px(80), c.my, c.w - c.mx, band.y0 - c.px(40))
    Stack(_hook(c, spec, size=104, max_lines=4),
          _sub(c, spec, gap=28),
          align="center").render(c, region)
    c.label(HANDLE, c.w - c.mx, (band.y0 + band.y1) / 2, size=28, anchor="rm",
            color=c.muted)
    return c.img


def x_ledger(fmt, spec):
    """The system as hairline rows — reads at thumbnail size."""
    c = Canvas("wide", ground=spec.get("ground", "graphite"), accent=_acc(spec))
    region = c.region(top=_head(c, spec, eb_color=c.accent_rgb, pad=38))
    Stack(_hook(c, spec, size=68, max_lines=2, accent=False),
          Rows(spec.get("items", [])[:4], mode="hairline", size=40, gap=42,
               row_gap=36, text_color=c.fg, max_lines=1),
          align="center").render(c, region)
    _foot(c, spec, badge=True, left=HANDLE)
    return c.img


def x_spectrum(fmt, spec):
    """Spectrum ticks and a bottom-set hook — the X cut of the IG cover."""
    c = Canvas("wide", ground=spec.get("ground", "ink"), accent=_acc(spec))
    region = c.region(top=_head(c, spec, eyebrow=None))
    Stack(Spectrum(),
          _hook(c, spec, size=104, max_lines=3, gap=40),
          _sub(c, spec, gap=26),
          align="bottom").render(c, region)
    _foot(c, spec, badge=True, left=HANDLE)
    return c.img


# ================================================================ FACEBOOK
def fb_card(fmt, spec):
    """Facebook keeps the light chrome identity, question-led."""
    c = Canvas("ig", ground="chrome", accent="volt")
    region = c.region(top=_head(c, spec, eb_color=b.VIOLET, pad=48))
    Stack(_hook(c, spec, size=100, max_lines=4, mode="highlight", color=b.INK),
          _sub(c, spec, gap=36, color=b.INK_SOFT, max_lines=4),
          align="center").render(c, region)
    c.footer(left=HANDLE, right=None)
    return c.img


def fb_rows(fmt, spec):
    """Facebook: the system listed out, light ground."""
    c = Canvas("ig", ground="chrome", accent="volt")
    region = c.region(top=_head(c, spec, eb_color=b.VIOLET, pad=46))
    Stack(_hook(c, spec, size=74, max_lines=2, color=b.INK, accent=False),
          Rows(spec.get("items", [])[:5], mode="hairline", size=38, gap=52,
               row_gap=46, text_color=b.INK_SOFT, max_lines=2),
          align="top").render(c, region)
    c.footer(left=HANDLE, right=None)
    return c.img


def fb_photo(fmt, spec):
    """Facebook: plate over the line."""
    c = Canvas("ig", ground="chrome", accent="volt")
    ph = int(c.h * 0.40)
    c.paste_plate(0, 0, c.w, ph, spec.get("treatment", "dots"),
                  spec.get("mood", "graphite"))
    c.record(Box(0, 0, c.w, ph, "plate"))
    top = ph + c.px(72)
    eb = c.eyebrow(spec.get("eyebrow"), color=b.VIOLET, y=top)
    region = c.region(top=(eb.y1 + c.px(46)) if eb else top)
    Stack(_hook(c, spec, size=88, max_lines=4, color=b.INK, mode="highlight"),
          _sub(c, spec, gap=32, color=b.INK_SOFT, max_lines=3),
          align="top").render(c, region)
    c.footer(left=HANDLE, right=None)
    return c.img


def fb_quote(fmt, spec):
    """Facebook: violet quote card, the one line worth re-sharing."""
    c = Canvas("ig", ground="violet", accent="volt")
    region = c.region(top=_head(c, spec, eb_color=c.muted, pad=46))
    Stack(_hook(c, spec, text=spec.get("quote", spec.get("hook", "")),
                size=104, max_lines=5, color=b.WHITE, accent=False),
          Rule(0.20, gap=42),
          align="center").render(c, region)
    c.footer(left=HANDLE, right=None)
    return c.img


# ---------------------------------------------------------------- registry
STYLES = {
    # Instagram covers (board 04)
    "ig_spectrum": ig_spectrum, "ig_list": ig_list, "ig_photo": ig_photo,
    "ig_stat": ig_stat, "ig_quote": ig_quote, "ig_rule": ig_rule,
    # carousel interiors
    "beat_number": beat_number, "beat_split": beat_split, "beat_center": beat_center,
    "beat_highlight": beat_highlight, "beat_rail": beat_rail, "beat_rows": beat_rows,
    "beat_ledger": beat_ledger, "beat_quote": beat_quote, "beat_stat": beat_stat,
    "close_follow": close_follow, "close_volt": close_volt, "close_violet": close_violet,
    # vertical video (board 05)
    "v_coldopen": v_coldopen, "v_day": v_day, "v_broll": v_broll,
    "v_listtease": v_listtease, "v_stat": v_stat, "v_quote": v_quote,
    "v_step": v_step, "v_end": v_end,
    # Pinterest (board 06)
    "pin_list": pin_list, "pin_printable": pin_printable, "pin_photo": pin_photo,
    "pin_rule": pin_rule,
    # LinkedIn (board 07)
    "li_carousel": li_carousel, "li_stat": li_stat, "li_quote": li_quote,
    "li_note": li_note,
    # X / Twitter
    "x_headline": x_headline, "x_stat": x_stat, "x_quote": x_quote,
    "x_split": x_split, "x_ledger": x_ledger, "x_spectrum": x_spectrum,
    # Facebook
    "fb_card": fb_card, "fb_rows": fb_rows, "fb_photo": fb_photo, "fb_quote": fb_quote,
}

# The ground each template lands on. The audit uses this to check the board's
# grid rule: never two light grounds side by side, photo posts on the diagonal.
TEMPLATE_GROUND = {
    "ig_spectrum": "dark", "ig_list": "light", "ig_photo": "dark",
    "ig_stat": "light", "ig_quote": "violet", "ig_rule": "light",
    "fb_card": "light", "fb_rows": "light", "fb_photo": "light", "fb_quote": "violet",
    # Reels take a tile in the profile grid too, so their opening frame counts
    "v_coldopen": "dark", "v_broll": "dark", "v_day": "light",
    "v_step": "dark", "v_stat": "dark", "v_listtease": "dark", "v_quote": "violet",
}

# Templates whose composition is a plate ("photo") post — the board wants these
# on the diagonal of the nine-post grid.
PHOTO_TEMPLATES = {"ig_photo", "fb_photo", "pin_photo", "beat_split", "v_broll"}
