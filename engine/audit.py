# -*- coding: utf-8 -*-
"""
Render audit — the guarantee behind "it renders correctly".

Every slide of every post is rendered and checked for:
  · exact artboard size (so every asset is in its platform's aspect ratio);
  · zero overlap between foreground elements — no bar, rule or footer sitting
    on type, which is what the layout engine exists to prevent;
  · everything inside the margins and, on vertical video, inside the UI-safe
    band where the caption and action rail live;
  · type above the legibility floor *and* set near the size its template asks
    for — copy that has to be squeezed to fit is a template mismatch, not a
    layout that "just fits";
  · volt read as one accent element, not a wash (unless the template fields
    volt by design, like the day counter);
  · the shape that earns a swipe — a forward cue on the cover, a CTA card at
    the close, and the mark at the END of every video;
  · template diversity — no post repeats a layout, no outlet repeats itself two
    days running, and the Instagram grid keeps the board's rotation (never two
    light grounds side by side, violet ≈ one per row of three).

Run:  python -m engine.audit            (full)
      python -m engine.audit --sample 40
"""
import sys
from collections import Counter, defaultdict

import engine.styles as S
import engine.brand as b
from engine.surface import FORMATS
from engine.build import build_all, IG_ROTATION

# elements that are meant to sit *behind* type
BACKGROUND = {"plate", "band", "panel", "region", "footer_band"}
TOL = 2.0                      # px of anti-aliasing slack
SIDE_TOL = 12.0                # optical overhang allowed on the side edges
MIN_TYPE = 24                  # px on a 1080 artboard
MIN_FILL = 0.05                # sanity floor: an all-but-empty card is a bug
MIN_SET = 0.72                 # type must land near the size the template asks for
MAX_VOLT = 0.10                # volt is an accent element, never a wash

# the cues that make a post worth swiping: a forward promise on the cover,
# an ask on the close, the mark at the END of a video (the retention rule)
FORWARD_CUES = ("SWIPE", "SAVE THIS", "READ MORE", "READ")
CLOSE_STYLES = {"close_follow", "close_volt", "close_violet"}


def _expected(fmt):
    return FORMATS[fmt]["size"]


def check_slide(fmt, style, spec):
    """Render one slide and return a list of problem strings."""
    img = S.STYLES[style](fmt, dict(spec))
    c = img.canvas                 # the element registry the canvas built up
    check_slide.last = c
    problems = []

    # 1 — aspect ratio / exact size
    want = _expected(fmt)
    if img.size != want:
        problems.append(f"size {img.size} != {want}")

    # 2 — safe area
    if fmt == "vert":
        top, bottom = c.top_safe, c.bot_safe
    else:
        top, bottom = min(c.my, c.top_safe), c.h - c.px(b.FOOTER_OFFSET)
    fg = [x for x in c.boxes if x.name not in BACKGROUND]
    for box in fg:
        if box.x0 < c.safe_x0 - SIDE_TOL or box.x1 > c.safe_x1 + SIDE_TOL:
            problems.append(f"{box.name} crosses the side margin ({box.x0:.0f}..{box.x1:.0f})")
        if box.y0 < top - TOL or box.y1 > bottom + TOL:
            problems.append(f"{box.name} outside the safe band ({box.y0:.0f}..{box.y1:.0f} "
                            f"vs {top:.0f}..{bottom:.0f})")

    # 3 — no foreground element may touch another
    for n, a in enumerate(fg):
        for other in fg[n + 1:]:
            if a.intersects(other, pad=TOL):
                problems.append(f"{a.name} overlaps {other.name} "
                                f"({a} / {other})")

    # 4 — legibility floor
    for size, family, asked in c.type_sizes:
        if size / c.s < MIN_TYPE:
            problems.append(f"{family} type set at {size / c.s:.0f}px (floor {MIN_TYPE})")
        elif asked and size < asked * MIN_SET:
            problems.append(f"{family} type squeezed to {size / asked:.0%} of spec "
                            f"({size / c.s:.0f}px of {asked / c.s:.0f}px) — copy is "
                            f"too long for this template")

    # 5 — the card has to be *set*, not floated in a sea of ground
    fill = _fill_ratio(c, fg)
    if fill is not None and fill < MIN_FILL:
        problems.append(f"content fills only {fill:.0%} of the card — near-empty")

    # 6 — volt is a highlighter, not a background: one element, not a wash
    share = volt_share(img)
    if c.volt_field:
        if share < 0.20:
            problems.append(f"{style} fields volt by design but volt covers "
                            f"only {share:.0%}")
    elif share > MAX_VOLT:
        problems.append(f"volt covers {share:.1%} of the card (cap {MAX_VOLT:.0%}) "
                        f"— it should read as one accent element")

    return problems


def _fill_ratio(c, fg):
    """How much of the usable card the content actually occupies."""
    body = [x for x in fg if x.name not in ("label", "badge")]
    if not body:
        return None
    top = c.top_safe
    bottom = c._footer_top if c._footer_top else c.bot_safe
    available = bottom - top
    if available <= 0:
        return None
    used = max(x.y1 for x in body) - min(x.y0 for x in body)
    return used / available


def volt_share(img):
    """Fraction of the card within a short reach of volt."""
    small = img.resize((108, int(108 * img.height / img.width)))
    hits = 0
    px = small.load()
    w, h = small.size
    for y in range(h):
        for x in range(w):
            r, g, bl = px[x, y][:3]
            if abs(r - b.VOLT[0]) < 40 and abs(g - b.VOLT[1]) < 40 and abs(bl - b.VOLT[2]) < 50:
                hits += 1
    return hits / float(w * h)


def check_shape(post, styles, cues):
    """Is this post built for its format? A video (or a TikTok Photo Mode
    carousel — the same vertical frame set, shown as swipeable stills) opens on
    a hook and closes on the mark at the END (the retention rule). An Instagram
    carousel opens on a cover, closes on a CTA card and carries a forward cue.
    A Pinterest carousel opens on a keyword cover and stays within five cards."""
    out = []
    pid = post["post_id"]
    media = post.get("media")
    plat = post["platform"]
    vertical_frames = post["is_video"] or (media == "carousel" and post["fmt"] == "vert")
    if vertical_frames:
        if styles[-1] != "v_end":
            out.append(f"{pid}: {media} does not close on the end card ({styles[-1]})")
        if styles[0] == "v_end":
            out.append(f"{pid}: {media} opens on the end card")
        if len(styles) < 4:
            out.append(f"{pid}: {media} is only {len(styles)} frames")
    elif media == "carousel" and plat == "pinterest":
        if not styles[0].startswith("pin_"):
            out.append(f"{pid}: pin carousel opens on {styles[0]}, not a cover")
        if not 2 <= len(styles) <= 5:           # Pinterest caps a carousel at 5 cards
            out.append(f"{pid}: pin carousel is {len(styles)} cards (max 5)")
    elif media == "carousel":                   # Instagram carousel
        if not styles[0].startswith("ig_"):
            out.append(f"{pid}: carousel opens on {styles[0]}, not a cover")
        if styles[-1] not in CLOSE_STYLES:
            out.append(f"{pid}: carousel does not close on a CTA card ({styles[-1]})")
        if not 6 <= len(styles) <= 9:
            out.append(f"{pid}: carousel is {len(styles)} slides")
        if not any(any(cue.startswith(f) for f in FORWARD_CUES) for cue in cues):
            out.append(f"{pid}: cover carries no forward cue (got {cues})")
    return out


def check_cadence(posts):
    """Day to day, an outlet must not serve the same layout twice running."""
    out = []
    by_plat = defaultdict(list)
    for p in posts:
        by_plat[p["platform"]].append(p)
    for plat, plist in sorted(by_plat.items()):
        plist.sort(key=lambda p: p["date"])
        for n in range(len(plist) - 1):
            if plist[n].get("media") != plist[n + 1].get("media"):
                continue                        # a different media type is already variety
            a = [s for s, _ in plist[n]["slides"]]
            c = [s for s, _ in plist[n + 1]["slides"]]
            if a == c:
                out.append(f"{plat}: {plist[n]['date']} and {plist[n + 1]['date']} "
                           f"use the identical layout set {a}")
            elif a[0] == c[0]:
                out.append(f"{plat}: {plist[n]['date']} and {plist[n + 1]['date']} "
                           f"both open on {a[0]}")
    return out


def main(argv):
    sample = None
    if "--sample" in argv:
        sample = int(argv[argv.index("--sample") + 1])

    posts = build_all()
    if sample:
        step = max(1, len(posts) // sample)
        posts = posts[::step][:sample]

    issues = []
    per_platform_templates = defaultdict(set)
    slides_checked = 0

    for n, post in enumerate(posts, 1):
        fmt = post["fmt"]
        styles = [s for s, _ in post["slides"]]
        per_platform_templates[post["platform"]].update(styles)

        # a post must never repeat a layout inside itself
        dupes = [s for s, cnt in Counter(styles).items() if cnt > 1]
        if dupes:
            issues.append(f"{post['post_id']}: repeats template(s) {dupes}")

        cues = []
        for k, (style, spec) in enumerate(post["slides"], 1):
            for p in check_slide(fmt, style, spec):
                issues.append(f"{post['post_id']} slide {k} [{style}] {p}")
            if k == 1:
                cues = list(check_slide.last.cues)
            slides_checked += 1

        # a post has to earn the next tap: a forward promise on the opener,
        # an ask at the close, the mark at the END of a video
        issues += check_shape(post, styles, cues)
        if n % 40 == 0:
            print(f"  ...{n}/{len(posts)} posts, {slides_checked} slides")

    # 5 — Instagram grid rotation: never two light grounds side by side.
    #     Reels take a tile in the profile grid, so they count as tiles too.
    if not sample:
        tiles = sorted((p["date"], p["slides"][0][0]) for p in posts
                       if p["platform"] == "instagram")
        grounds = [S.TEMPLATE_GROUND.get(s, "dark") for _, s in tiles]
        for n in range(len(grounds) - 1):
            if grounds[n] == "light" and grounds[n + 1] == "light":
                issues.append(f"grid: two light tiles side by side at {tiles[n][0]} "
                              f"({tiles[n][1]} then {tiles[n + 1][1]})")
            if grounds[n] == "violet" and grounds[n + 1] == "violet":
                issues.append(f"grid: two violet tiles side by side at {tiles[n][0]} "
                              f"({tiles[n][1]} then {tiles[n + 1][1]})")
        for n in range(len(grounds) - 2):    # one violet per row of three
            if grounds[n:n + 3].count("violet") > 1:
                issues.append(f"grid: more than one violet in the row at {tiles[n][0]}")
        covers = {s for _, s in tiles}
        missing = set(IG_ROTATION) - covers - {"ig_stat"}
        if missing:
            issues.append(f"grid: rotation slots never used: {sorted(missing)}")

    # 6 — day to day, no outlet may repeat itself
    if not sample:
        issues += check_cadence(posts)

    # 7 — every outlet must be running a real spread of templates
    if not sample:
        for plat, tset in sorted(per_platform_templates.items()):
            if len(tset) < 4:
                issues.append(f"{plat}: only {len(tset)} template(s) "
                              f"in rotation {sorted(tset)}")

    print(f"\nslides checked : {slides_checked}")
    print(f"posts checked  : {len(posts)}")
    print("templates per outlet:")
    for plat, tset in sorted(per_platform_templates.items()):
        print(f"  {plat:<10} {len(tset):>2}  {', '.join(sorted(tset))}")
    if issues:
        print(f"\nISSUES: {len(issues)}")
        for msg in issues[:60]:
            print("  -", msg)
        if len(issues) > 60:
            print(f"  ... and {len(issues) - 60} more")
        return 1
    print("\nNo issues: every slide is in format, inside its margins, "
          "and nothing overlaps.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
