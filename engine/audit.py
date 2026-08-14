# -*- coding: utf-8 -*-
"""
Render audit — the guarantee behind "it renders correctly".

Every slide of every post is rendered and checked for:
  · exact artboard size (so every asset is in its platform's aspect ratio);
  · zero overlap between foreground elements — no bar, rule or footer sitting
    on type, which is what the layout engine exists to prevent;
  · everything inside the margins and, on vertical video, inside the UI-safe
    band where the caption and action rail live;
  · type never set below the legibility floor;
  · template diversity — no post repeats a layout, and the Instagram grid
    keeps the board's rotation (no two light grounds side by side).

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


def _expected(fmt):
    return FORMATS[fmt]["size"]


def check_slide(fmt, style, spec):
    """Render one slide and return a list of problem strings."""
    img = S.STYLES[style](fmt, dict(spec))
    c = img.canvas                 # the element registry the canvas built up
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
    for size, family in c.type_sizes:
        if size / c.s < MIN_TYPE:
            problems.append(f"{family} type set at {size / c.s:.0f}px (floor {MIN_TYPE})")

    return problems


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

        for k, (style, spec) in enumerate(post["slides"], 1):
            for p in check_slide(fmt, style, spec):
                issues.append(f"{post['post_id']} slide {k} [{style}] {p}")
            slides_checked += 1
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

    # 6 — every outlet must be running a real spread of templates
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
