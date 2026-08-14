"""
Style compositions — each returns a finished PIL image for a given format.
These are the visual 'skins' rotated across the grid so no two posts read alike.
Spec keys used (all optional): eyebrow, hook, sub, items[], numeral, numeral_label,
quote, cta, handle, index, url, ground, plate, accent, drop.
"""
import engine.brand as b
from engine.templates import Canvas, FORMATS

HANDLE = "@gogettrdaily"

def _accent(spec):
    return spec.get("accent", "volt")

def cover_hook(fmt, spec):
    c = Canvas(fmt, ground=spec.get("ground", "graphite"),
               plate_mood=spec.get("plate"), accent=_accent(spec))
    y = c.eyebrow(spec.get("eyebrow", "GOGETTR SYSTEM"))
    y += c.px(30)
    y = c.hook(spec["hook"], y, max_size=spec.get("hook_size", 124), max_lines=4)
    y = c.volt_bar(y + c.px(18))
    if spec.get("sub"):
        y = c.sub(spec["sub"], y + c.px(14))
    c.footer(spec.get("handle", HANDLE), spec.get("cta", "SAVE THIS →"))
    return c.img

def cover_list(fmt, spec):
    c = Canvas(fmt, ground=spec.get("ground", "graphite"), accent=_accent(spec))
    y = c.eyebrow(spec.get("eyebrow", "SYSTEM"))
    y += c.px(24)
    y = c.hook(spec["hook"], y, max_size=104, max_lines=3)
    y += c.px(30)
    c.rows(spec["items"][:6], y, size=spec.get("row_size", 50))
    c.footer(spec.get("handle", HANDLE), spec.get("cta", "SWIPE →"))
    return c.img

def body_beat(fmt, spec):
    """Carousel middle slide: index + one punchy beat line, big."""
    c = Canvas(fmt, ground=spec.get("ground", "graphite"),
               plate_mood=spec.get("plate"), accent=_accent(spec))
    c.eyebrow(spec.get("eyebrow", "GOGETTR"))
    if spec.get("index"):
        c.index_chip(spec["index"])
    y = int(c.h * 0.30)
    if spec.get("kicker"):
        fk = b.font("mono", c.px(30), 700)
        b.draw_tracked(c.d, (c.mx, y), spec["kicker"].upper(), fk, c.accent_rgb,
                       tracking=c.px(30) * 0.18)
        y += c.px(60)
    y = c.hook(spec["hook"], y, max_size=112, max_lines=5)
    if spec.get("sub"):
        c.sub(spec["sub"], y + c.px(20))
    c.footer(spec.get("handle", HANDLE), spec.get("cta", ""))
    return c.img

def stat(fmt, spec):
    c = Canvas(fmt, ground=spec.get("ground", "graphite"), accent=_accent(spec))
    y = c.eyebrow(spec.get("eyebrow", "THE NUMBER"))
    y = int(c.h * 0.20)
    y = c.numeral(spec["numeral"], y, size=spec.get("num_size", 300))
    c.volt_bar(y + c.px(6))
    y = c.hook(spec.get("numeral_label", spec.get("hook", "")), y + c.px(48),
               max_size=92, max_lines=3)
    if spec.get("sub"):
        c.sub(spec["sub"], y + c.px(16))
    c.footer(spec.get("handle", HANDLE), spec.get("cta", "SAVE THIS →"))
    return c.img

def quote(fmt, spec):
    grd = spec.get("ground", "violet")
    c = Canvas(fmt, ground=grd, accent="volt")
    c.fg = b.INK if grd == "chrome" else b.WHITE
    eb = b.INK if grd == "chrome" else b.CHROME
    c.eyebrow(spec.get("eyebrow", "GOGETTR"), color=eb)
    y = int(c.h * 0.24)
    y = c.quote(spec["quote"], y, size=spec.get("q_size", 104), max_lines=6)
    if spec.get("sub"):
        c.sub(spec["sub"], y + c.px(24), color=(c.fg))
    c.footer(spec.get("handle", HANDLE), spec.get("cta", ""), )
    return c.img

def close_cta(fmt, spec):
    c = Canvas(fmt, ground=spec.get("ground", "ink"), accent=_accent(spec))
    y = int(c.h * 0.26)
    c.chevron(c.mx, y, 120)
    y += c.px(190)
    y = c.hook(spec.get("cta_hook", "Save this. Run it this week."), y,
               max_size=104, max_lines=4)
    c.volt_bar(y + c.px(18))
    c.footer(spec.get("handle", HANDLE), spec.get("cta", "FOLLOW →"))
    return c.img

def day_counter(fmt, spec):
    c = Canvas(fmt, ground=spec.get("ground", "graphite"),
               plate_mood=spec.get("plate"), accent=_accent(spec))
    y = c.eyebrow(spec.get("eyebrow", "THE 30-DAY SYSTEM AUDIT"), y=c.top_safe)
    y = int(c.h * 0.30)
    fbig = b.font("mono", c.px(40), 700)
    b.draw_tracked(c.d, (c.mx, y), spec.get("day", "DAY 01 / 30"), fbig,
                   c.accent_rgb, tracking=c.px(40) * 0.14)
    y += c.px(80)
    y = c.hook(spec["hook"], y, max_size=118, max_lines=4)
    if spec.get("sub"):
        c.sub(spec["sub"], y + c.px(18))
    c.footer(spec.get("handle", HANDLE), spec.get("cta", "SAVE THE SERIES →"))
    return c.img

def rule(fmt, spec):
    c = Canvas(fmt, ground=spec.get("ground", "ink"), accent=_accent(spec))
    y = int(c.h * 0.34)
    y = c.hook(spec["hook"], y, max_size=132, max_lines=4)
    c.volt_bar(y + c.px(20))
    c.footer(spec.get("handle", HANDLE), spec.get("cta", ""))
    return c.img

def pin_list(fmt, spec):
    c = Canvas(fmt, ground=spec.get("ground", "graphite"), accent=_accent(spec))
    y = c.eyebrow(spec.get("keyword", spec.get("eyebrow", "SYSTEMS")))
    y += c.px(18)
    y = c.hook(spec["hook"], y, max_size=88, max_lines=3)
    y += c.px(24)
    c.rows(spec.get("items", [])[:6], y, size=44, gap=1.55)
    c.footer(spec.get("handle", HANDLE), "SAVE →")
    return c.img

def pin_rule(fmt, spec):
    c = Canvas(fmt, ground=spec.get("ground", "violet"),
               plate_mood=spec.get("plate"), accent="volt")
    y = c.eyebrow(spec.get("keyword", "GOGETTR"), color=b.WHITE)
    y = int(c.h * 0.30)
    y = c.hook(spec["hook"], y, max_size=104, max_lines=5, color=b.WHITE)
    c.footer(spec.get("handle", HANDLE), "SAVE →")
    return c.img

def vert_hook(fmt, spec):
    """Cold-open vertical hook, held in the middle 60% (TikTok / Shorts / Reels)."""
    c = Canvas(fmt, ground=spec.get("ground", "ink"),
               plate_mood=spec.get("plate"), accent=_accent(spec))
    # index / system chip near top-safe
    if spec.get("eyebrow"):
        fe = b.font("mono", c.px(30), 600)
        b.draw_tracked(c.d, (c.mx, c.top_safe), spec["eyebrow"].upper(), fe,
                       c.accent_rgb, tracking=c.px(30) * 0.18)
    # hook centred in safe band
    box = c.w - 2 * c.mx
    f, sz, tr, lines = b.fit_hook(c.d, spec["hook"], box, c.px(128), c.px(56),
                                  max_lines=5)
    total = len(lines) * sz * 1.05
    y = (c.top_safe + c.bot_safe) / 2 - total / 2
    for ln in lines:
        b.draw_tracked(c.d, (c.mx, y), ln, f, c.fg, tracking=tr)
        y += sz * 1.05
    c.volt_bar(int(y + c.px(20)))
    if spec.get("sub"):
        c.sub(spec["sub"], int(y + c.px(46)), size=38)
    # handle lifted above the action rail
    fh = b.font("mono", c.px(30), 600)
    b.draw_tracked(c.d, (c.mx, c.bot_safe - c.px(6)), HANDLE.upper(), fh,
                   c.muted, tracking=c.px(30) * 0.16)
    return c.img

def vert_end(fmt, spec):
    """Shorts/TikTok end-card: logo + CTA at the END (per retention research)."""
    c = Canvas(fmt, ground=spec.get("ground", "ink"), accent=_accent(spec))
    y = (c.top_safe + c.bot_safe) / 2 - c.px(230)
    c.chevron(int(c.w / 2 - c.px(84)), int(y), 150)
    y += c.px(250)
    txt = spec.get("cta_hook", "Follow for more.")
    f, sz, tr, lines = b.fit_hook(c.d, txt, c.w - 2 * c.mx, c.px(92), c.px(48), max_lines=3)
    for ln in lines:
        b.draw_tracked(c.d, (c.w / 2, y), ln, f, c.fg, tracking=tr, anchor="ma")
        y += sz * 1.06
    c.d.rectangle([c.w / 2 - c.px(90), y + c.px(18), c.w / 2 + c.px(90), y + c.px(30)],
                  fill=c.accent_rgb)
    fh = b.font("mono", c.px(30), 600)
    b.draw_tracked(c.d, (c.w / 2, c.bot_safe - c.px(6)), HANDLE.upper(), fh,
                   c.accent_rgb, tracking=c.px(30) * 0.16, anchor="ma")
    return c.img

# X / Twitter wide cards --------------------------------------------------
def wide_quote(fmt, spec):
    c = Canvas(fmt, ground=spec.get("ground", "graphite"), accent=_accent(spec))
    y = c.eyebrow(spec.get("eyebrow", "GOGETTR"))
    y = int(c.h * 0.24)
    y = c.hook(spec.get("hook", spec.get("quote", "")), y, max_size=104, max_lines=3)
    c.volt_bar(y + c.px(16))
    c.footer(spec.get("handle", HANDLE), spec.get("cta", ""))
    return c.img

def wide_stat(fmt, spec):
    c = Canvas(fmt, ground=spec.get("ground", "graphite"), accent=_accent(spec))
    c.eyebrow(spec.get("eyebrow", "THE NUMBER"))
    num = spec.get("numeral", "1")
    fnum = b.font("display", c.px(300), 700)
    bbox = c.d.textbbox((0, 0), num, font=fnum)
    nh, nw = bbox[3] - bbox[1], bbox[2] - bbox[0]
    ny = (c.h - nh) // 2 - bbox[1] + c.px(20)
    c.d.text((c.mx, ny), num, font=fnum, fill=b.VIOLET)
    lx = c.mx + nw + c.px(64)
    f, sz, tr, lines = b.fit_hook(c.d, spec.get("numeral_label", spec.get("hook", "")),
                                  c.w - lx - c.mx, c.px(66), c.px(34), max_lines=4)
    th = len(lines) * sz * 1.06
    yy = (c.h - th) // 2 + c.px(20)
    c.d.rectangle([lx, yy - c.px(26), lx + c.px(90), yy - c.px(14)], fill=c.accent_rgb)
    for ln in lines:
        b.draw_tracked(c.d, (lx, yy), ln, f, c.fg, tracking=tr); yy += sz * 1.06
    fh = b.font("mono", c.px(28), 600)
    b.draw_tracked(c.d, (c.w - c.mx, c.h - c.my), HANDLE.upper(),
                   fh, c.muted, tracking=c.px(28) * 0.16, anchor="ra")
    c.chevron(c.mx, c.h - c.my - c.px(4), 28)
    return c.img

# registry
STYLES = {
    "cover_hook": cover_hook, "cover_list": cover_list, "body_beat": body_beat,
    "stat": stat, "quote": quote, "close_cta": close_cta, "day_counter": day_counter,
    "rule": rule, "pin_list": pin_list, "pin_rule": pin_rule, "vert_hook": vert_hook,
    "vert_end": vert_end, "wide_quote": wide_quote, "wide_stat": wide_stat,
}
