# -*- coding: utf-8 -*-
"""
Adaptation engine: theme x platform -> finished Post spec.

Composition rules, from the board:
  · Instagram covers follow the nine-post rotation (hook, list, photo, stat,
    hook, quote, photo, list, hook) so the grid reads as texture — never two
    light grounds side by side, photo posts on the diagonal.
  · A carousel never repeats a layout inside itself: every interior slide is a
    different template, and the recipe rotates day to day.
  · Video frames rotate too, and each outlet gets a different recipe for the
    same theme, so a TikTok and its Short are not the same four cards.

Start: Mon 2026-08-17, ET. Times are platform-optimal (2025/26 research).
"""
from datetime import date, timedelta
import engine.content as C

START = date(2026, 8, 17)   # Monday
HANDLE = "@gogettrdaily"

# platform code, optimal daily post time (ET, 24h), primary format, is_video
PLATFORMS = [
    ("instagram", "IG",  (8, 0),  False),
    ("facebook",  "FB",  (9, 0),  False),
    ("x",         "X",   (9, 0),  False),
    ("linkedin",  "LI",  (8, 0),  False),
    ("youtube",   "YT",  (15, 0), True),
    ("tiktok",    "TT",  (19, 0), True),
    ("pinterest", "PIN", (20, 0), False),
]
PLAT_LABEL = {"instagram": "Instagram (+Facebook link)", "facebook": "Facebook",
              "x": "X / Twitter", "linkedin": "LinkedIn", "youtube": "YouTube Shorts",
              "tiktok": "TikTok", "pinterest": "Pinterest"}


def idxof(t):
    return int(t["id"][1:])


# ---------------------------------------------------------------- TEXTURE
PLATE_TREATMENTS = ["chevron", "hatch", "grid", "rings", "dots", "sweep", "bars"]
PLATE_MOODS = ["ink", "graphite", "steel", "violet"]


def _tex(i, k=0):
    return PLATE_TREATMENTS[(i + k) % len(PLATE_TREATMENTS)]


def _mood(i, k=0):
    return PLATE_MOODS[(i + k * 3) % len(PLATE_MOODS)]


# ---------------------------------------------------------------- ROTATIONS
# board 08 — the nine-post grid rotation
IG_ROTATION = ["ig_spectrum", "ig_list", "ig_photo", "ig_stat", "ig_spectrum",
               "ig_quote", "ig_photo", "ig_list", "ig_spectrum"]

INTERIOR_RECIPES = [
    ["beat_number", "beat_split", "beat_highlight", "beat_rail", "beat_quote"],
    ["beat_rail", "beat_center", "beat_number", "beat_split", "beat_quote"],
    ["beat_split", "beat_highlight", "beat_rail", "beat_number", "beat_center"],
    ["beat_highlight", "beat_number", "beat_split", "beat_center", "beat_quote"],
    ["beat_number", "beat_rail", "beat_center", "beat_highlight", "beat_quote"],
    ["beat_split", "beat_number", "beat_highlight", "beat_center", "beat_quote"],
    ["beat_rail", "beat_split", "beat_center", "beat_number", "beat_quote"],
]
RECAPS = ["beat_ledger", "beat_rows"]
CLOSERS = ["close_follow", "close_volt", "close_violet"]

VIDEO_RECIPES = [
    ["v_coldopen", "v_step", "v_listtease", "v_end"],
    ["v_broll", "v_step", "v_quote", "v_end"],
    ["v_day", "v_listtease", "v_step", "v_end"],
    ["v_coldopen", "v_listtease", "v_quote", "v_end"],
    ["v_broll", "v_step", "v_listtease", "v_quote", "v_end"],
    ["v_day", "v_step", "v_quote", "v_end"],
    ["v_coldopen", "v_broll", "v_step", "v_end"],
    ["v_broll", "v_listtease", "v_step", "v_quote", "v_end"],
    ["v_coldopen", "v_step", "v_quote", "v_end"],
]
VIDEO_OFFSET = {"tiktok": 0, "youtube": 3, "instagram": 0}

# A Reel also takes a tile in the profile grid, so Instagram gets its own pool:
# openers vary across dark and violet, and never the full-volt frame (which
# would put two light tiles side by side and spend volt far too freely).
IG_REEL_RECIPES = [
    ["v_coldopen", "v_step", "v_listtease", "v_end"],
    ["v_quote", "v_step", "v_listtease", "v_end"],
    ["v_broll", "v_step", "v_listtease", "v_quote", "v_end"],
    ["v_coldopen", "v_listtease", "v_quote", "v_end"],
    ["v_broll", "v_step", "v_quote", "v_end"],
    ["v_quote", "v_broll", "v_step", "v_end"],
    ["v_coldopen", "v_broll", "v_step", "v_end"],
]

PIN_ROTATION = ["pin_list", "pin_photo", "pin_printable", "pin_rule"]
LI_ROTATION = ["li_carousel", "li_quote", "li_note", "li_stat"]
X_ROTATION = ["x_headline", "x_ledger", "x_quote", "x_split", "x_spectrum", "x_stat"]
FB_ROTATION = ["fb_card", "fb_rows", "fb_photo", "fb_quote"]


def _base(t, **kw):
    spec = dict(eyebrow=t["series"], hook=t["hook"], sub=t["sub"],
                items=list(t["beats"]), quote=t["quote"], keyword=t["keyword"],
                cta_hook=t["cta"], accent=t["accent"], handle=HANDLE)
    if t.get("numeral"):
        spec["numeral"] = t["numeral"]
        spec["numeral_label"] = t.get("numeral_label", t["hook"])
    spec.update(kw)
    return spec


# ------------------------------------------------------------------ SLIDES
def _cover_style(t, name):
    if name == "ig_stat" and not t.get("numeral"):
        return "ig_rule"                     # keeps the light ground the grid wants
    return name


_IG_PLAN = None


def ig_plan():
    """Lay out the whole Instagram *profile grid* up front.

    Carousels and Reels both take a tile, so both are planned together: walk
    the board's nine-post rotation and skip any slot that would break the grid
    rules — never two light grounds side by side, and violet kept to roughly
    one tile per row of three.
    """
    global _IG_PLAN
    if _IG_PLAN is not None:
        return _IG_PLAN
    from engine.styles import TEMPLATE_GROUND
    covers, reels = {}, {}
    prev = prev2 = None
    rot = rrot = 0

    def allowed(g):
        if g == "light" and prev == "light":
            return False
        if g == "violet" and (prev == "violet" or prev2 == "violet"):
            return False
        return True

    for t in C.THEMES:
        i = idxof(t)
        if i % 3 == 0:                       # a Reel: its opening frame is the tile
            for _ in range(len(IG_REEL_RECIPES)):
                idx = rrot % len(IG_REEL_RECIPES)
                rrot += 1
                ground = TEMPLATE_GROUND.get(IG_REEL_RECIPES[idx][0], "dark")
                if allowed(ground):
                    break
            reels[i] = idx
        else:
            for _ in range(len(IG_ROTATION)):
                name = _cover_style(t, IG_ROTATION[rot % len(IG_ROTATION)])
                rot += 1
                ground = TEMPLATE_GROUND.get(name, "dark")
                if allowed(ground):
                    break
            covers[i] = name
        prev2, prev = prev, ground
    _IG_PLAN = (covers, reels)
    return _IG_PLAN


def ig_cover(t, i):
    """The day's slot in the nine-post rotation."""
    name = ig_plan()[0].get(i) or _cover_style(t, IG_ROTATION[(i - 1) % len(IG_ROTATION)])
    spec = _base(t, treatment=_tex(i), mood=_mood(i))
    if name == "ig_photo":
        spec["plate_h"] = 520 + (i % 3) * 40
    return name, spec


def carousel(t, i):
    """Cover + one card per beat + (every other day) a recap + a close card.
    Every interior in a carousel is a different template."""
    beats = t["beats"]
    recipe = list(INTERIOR_RECIPES[(i - 1) % len(INTERIOR_RECIPES)])
    if t.get("numeral"):                     # let the number have a card of its own
        recipe[2] = "beat_stat"
    slides = [ig_cover(t, i)]
    for k, (style, beat) in enumerate(zip(recipe, beats), 1):
        spec = _base(t, hook=beat, sub=None, step=f"{k:02d}", k=k, of=len(beats),
                     treatment=_tex(i, k), mood=_mood(i, k),
                     plate_ratio=0.34 + (k % 3) * 0.04)
        if style == "beat_quote":
            spec["quote"] = beat
        if style == "beat_stat":
            spec["numeral_label"] = t.get("numeral_label", beat)
        slides.append((style, spec))
    if i % 2 == 0:
        slides.append((RECAPS[(i // 2) % len(RECAPS)],
                       _base(t, hook="The system, in five moves.", sub=None)))
    slides.append((CLOSERS[(i - 1) % len(CLOSERS)], _base(t, sub=None)))

    total = len(slides)
    for pos, (style, spec) in enumerate(slides, 1):
        if pos > 1:
            spec["index"] = f"{pos} / {total}"
        if style == "ig_list":
            spec["footer_left"] = f"1 / {total}"
    return slides


def video_frames(t, i, platform):
    """A vertical recipe that differs by outlet, hook first and the mark last."""
    if platform == "instagram":
        idx = ig_plan()[1].get(i)
        recipe = IG_REEL_RECIPES[idx if idx is not None else (i - 1) % len(IG_REEL_RECIPES)]
    else:
        recipe = VIDEO_RECIPES[(i - 1 + VIDEO_OFFSET.get(platform, 0)) % len(VIDEO_RECIPES)]
    if t.get("numeral") and "v_step" in recipe:
        recipe = [("v_stat" if s == "v_step" else s) for s in recipe]
    beats = list(t["beats"])
    bi = 0
    slides = []
    for k, style in enumerate(recipe):
        spec = _base(t, treatment=_tex(i, k), mood=_mood(i, k))
        if k == 0:                                    # cold open: the hook
            spec["hook"] = t["hook"]
            spec["kicker"] = t["series"]
            if style == "v_quote":                    # open on the line itself
                spec["quote"] = t["hook"]
            if style == "v_day" and t["kind"] == "challenge":
                spec["day"] = f"DAY {i:02d} / {len(C.THEMES)}"
        elif style in ("v_step", "v_broll", "v_day"):
            spec["hook"] = beats[bi % len(beats)]
            spec["sub"] = None
            spec["index"] = f"{bi + 1:02d}"
            spec["kicker"] = t["series"]
            bi += 1
        elif style == "v_stat":
            spec["numeral_label"] = t.get("numeral_label", t["hook"])
        elif style == "v_listtease":
            spec["hook"] = t["series"].title() if len(t["series"]) < 22 else "The system"
            spec["sub"] = None
        elif style == "v_quote":
            spec["hook"] = t["quote"]
        if style == "v_end":
            spec["cta_hook"] = t["cta"]
            spec["ground"] = "volt" if (i % 4 == 0) else "ink"
        slides.append((style, spec))
    return slides


def video_durations(n):
    """Hold each frame long enough to read, short enough to keep the loop."""
    if n <= 4:
        return [2.7, 3.1, 3.1, 2.5]
    return [2.5, 2.7, 2.7, 2.7, 2.3][:n]


# ------------------------------------------------------------------ CAPTIONS
def tags_for(t, n, extra=None):
    """Broad, high-traffic tags: lead with the theme's own topic, guarantee at
    least one universal-reach tag, cap at n (the platform's limit)."""
    topic = []
    for k in (t["tags"] + (extra or [])):
        for h in C.HASHTAGS.get(k, []):
            if h not in topic:
                topic.append(h)
    picked = topic[:max(1, n - 1)] if n > 1 else topic[:1]
    for h in C.HASHTAGS["core"]:            # ensure a universal broad tag
        if len(picked) >= n:
            break
        if h not in picked:
            picked.append(h)
    for h in topic:                          # backfill if topic was short
        if len(picked) >= n:
            break
        if h not in picked:
            picked.append(h)
    return picked[:n]


# Pinterest boards — keyword-rich names (Pinterest is search, not hashtags).
BOARDS = {
    "money": "Money & Personal Finance", "career": "Career Growth & Success",
    "training": "Fitness & Healthy Habits", "recovery": "Fitness & Healthy Habits",
    "time": "Productivity & Time Management", "declutter": "Home & Life Organization",
    "social": "Confidence & Social Skills",
}
BOARD_DEFAULT = "Self Improvement & Discipline"


def board_for(t):
    for k in ["money", "career", "training", "recovery", "time", "declutter", "social"]:
        if k in t["tags"]:
            return BOARDS[k]
    return BOARD_DEFAULT


def _arrow_list(beats):
    return "\n".join(f"→ {b}" for b in beats)


def cap_instagram(t):
    body = (f"{t['hook']}\n\n{t['sub']}\n\n"
            f"Save this one and send it to someone who needs it. "
            f"Follow {HANDLE} for more.")
    return body + "\n\n" + " ".join(tags_for(t, 5))   # IG hard-caps at 5 (Dec 2025)


def cap_facebook(t):
    return (f"{t['hook']}\n\n{t['sub']}\n\n"
            f"{_arrow_list(t['beats'])}\n\n"
            f"Which one would move your month the most? Tell me below. "
            f"(Save the post so it is there when you need it.)\n\n"
            + " ".join(tags_for(t, 2)))   # FB: hashtags barely help, keep it to 2


def cap_x(t):
    thread = (f"{t['hook']}\n\n"
              + "\n".join(f"{k}. {b}" for k, b in enumerate(t['beats'], 1))
              + f"\n\n{t['cta']}")
    return thread + "\n\n" + " ".join(tags_for(t, 2))


def cap_linkedin(t):
    opener = "The most capable people I know don't run on willpower. They design defaults."
    return (f"{opener}\n\n{t['hook']}\n\n"
            + "\n".join(f"• {b}" for b in t['beats'])
            + "\n\nSystems beat motivation because they only ask you to decide once.\n\n"
            + " ".join(tags_for(t, 3)))   # LinkedIn: 1-3 is the sweet spot


def cap_pinterest(t):
    # Pinterest is keyword search, not hashtags — keyword-rich title + description.
    title = t["keyword"].title()
    desc = (f"{title}. {t['hook']} {t['sub']} "
            f"Save this pin for the next time you need it. Follow {HANDLE} for more.")
    return title, desc


def cap_youtube(t):
    title = f"{t['hook']} #shorts"
    if len(title) > 98:
        title = t["hook"][:88].rstrip(". ") + " #shorts"
    desc = (f"{t['hook']}\n\n{t['sub']}\n\n"
            + _arrow_list(t['beats'])
            + f"\n\nFollow {HANDLE} for more.\n\n"
            + " ".join(tags_for(t, 4) + ["#shorts"]))   # Shorts: keep to ~5
    return title, desc


def cap_tiktok(t):
    return (f"{t['hook']} {t['cta']}\n\n"
            f"(add a trending sound) — save it for later.\n"
            + " ".join(tags_for(t, 4) + ["#fyp"]))   # TikTok: 3-5 relevant


# ------------------------------------------------------------------ BUILD
def post_id(d, code):
    return f"GG-{d:%y%m%d}-{code}"


def build_all():
    posts = []
    for t in C.THEMES:
        i = idxof(t)
        d = START + timedelta(days=i - 1)
        for pkey, code, (hh, mm), is_vid in PLATFORMS:
            pid = post_id(d, code)
            common = dict(post_id=pid, theme_id=t["id"], theme_title=t["series"].title(),
                          pillar=t["pillar"], platform=pkey, platform_label=PLAT_LABEL[pkey],
                          date=d.isoformat(), weekday=d.strftime("%a"),
                          time=f"{hh:02d}:{mm:02d}", tz="ET",
                          datetime=f"{d.isoformat()} {hh:02d}:{mm:02d} ET",
                          hook=t["hook"])
            if pkey == "instagram":
                # mostly carousels; every 3rd day a Reel (reach)
                if i % 3 == 0:
                    slides = video_frames(t, i, "instagram")
                    common.update(fmt="vert", is_video=True,
                                  format="Reel · vertical MP4 (1080x1920)",
                                  slides=slides, durations=video_durations(len(slides)),
                                  caption=cap_instagram(t))
                else:
                    slides = carousel(t, i)
                    common.update(fmt="ig", is_video=False,
                                  format=f"Carousel · {len(slides)} slides (1080x1350)",
                                  slides=slides, caption=cap_instagram(t))
            elif pkey == "facebook":
                style = FB_ROTATION[(i - 1) % len(FB_ROTATION)]
                spec = _base(t, treatment=_tex(i, 2), mood=_mood(i, 2))
                common.update(fmt="ig", is_video=False, format="Single image (1080x1350)",
                              slides=[(style, spec)], caption=cap_facebook(t))
            elif pkey == "x":
                style = X_ROTATION[(i - 1) % len(X_ROTATION)]
                if style == "x_stat" and not t.get("numeral"):
                    style = "x_headline"
                spec = _base(t, treatment=_tex(i, 4), mood=_mood(i, 4),
                             panel="violet" if i % 2 else "volt",
                             panel_line=t["quote"])
                common.update(fmt="wide", is_video=False,
                              format="Text + image card (1600x900)",
                              slides=[(style, spec)], caption=cap_x(t))
            elif pkey == "linkedin":
                style = LI_ROTATION[(i - 1) % len(LI_ROTATION)]
                if style == "li_stat" and not t.get("numeral"):
                    style = "li_note"
                spec = _base(t, eyebrow=f"GOGETTR · {t['pillar'].title()}",
                             footer_right="READ →" if style == "li_carousel" else None)
                common.update(fmt="square", is_video=False,
                              format="Single image (1080x1080)",
                              slides=[(style, spec)], caption=cap_linkedin(t))
            elif pkey == "youtube":
                slides = video_frames(t, i, "youtube")
                title, desc = cap_youtube(t)
                common.update(fmt="vert", is_video=True,
                              format="Shorts · vertical MP4 (1080x1920)",
                              slides=slides, durations=video_durations(len(slides)),
                              title=title, caption=desc)
            elif pkey == "tiktok":
                slides = video_frames(t, i, "tiktok")
                common.update(fmt="vert", is_video=True,
                              format="Vertical MP4 slideshow (1080x1920)",
                              slides=slides, durations=video_durations(len(slides)),
                              caption=cap_tiktok(t))
            elif pkey == "pinterest":
                style = PIN_ROTATION[(i - 1) % len(PIN_ROTATION)]
                board = board_for(t)
                spec = _base(t, board=board, treatment=_tex(i, 5), mood=_mood(i, 5),
                             kicker="CHECKLIST", plate_ratio=0.40 + (i % 3) * 0.03)
                title, desc = cap_pinterest(t)
                common.update(fmt="pin", is_video=False, format="Pin 1000x1500",
                              board=board, slides=[(style, spec)], title=title,
                              caption=desc)
            posts.append(common)
    return posts


if __name__ == "__main__":
    from collections import Counter
    ps = build_all()
    print("total posts:", len(ps))
    vids = sum(1 for p in ps if p["is_video"])
    print("videos:", vids, "| image posts:", len(ps) - vids)
    print(Counter(p["platform"] for p in ps))
    print("templates in play:",
          len({s for p in ps for s, _ in p["slides"]}))
