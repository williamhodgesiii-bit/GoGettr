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


def ig_is_reel(i):
    """Instagram leads with Reels, not carousels.

    Reels are the only Instagram surface that reaches *non-followers* — carousels
    are shown almost entirely to people who already follow you, which a brand-new
    account does not have yet. So for a cold-start the day is a Reel by default,
    with a carousel every third day to keep the depth/saves play and the full
    cover-template rotation (which the grid audit relies on) alive.
    """
    return i % 3 != 0


# ---------------------------------------------------------------- TEXTURE
PLATE_TREATMENTS = ["chevron", "hatch", "grid", "rings", "dots", "sweep", "bars"]
PLATE_MOODS = ["ink", "graphite", "steel", "violet"]


def _tex(i, k=0):
    return PLATE_TREATMENTS[(i + k) % len(PLATE_TREATMENTS)]


def _mood(i, k=0):
    return PLATE_MOODS[(i + k * 3) % len(PLATE_MOODS)]


# ---------------------------------------------------------------- ROTATIONS
# board 08 — the nine-post grid rotation. Spread across all six covers (no one
# template dominates the grid) and grounded so the rotation reads as texture:
# the audit's allowed() still skips any slot that would break the grid rules.
IG_ROTATION = ["ig_spectrum", "ig_list", "ig_photo", "ig_stat", "ig_quote",
               "ig_photo", "ig_rule", "ig_spectrum", "ig_list"]

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
VIDEO_OFFSET = {"tiktok": 0, "youtube": 3, "instagram": 0, "pinterest": 6}

# ---------------------------------------------------------------- MEDIA MIX
# The board's own rule — "you do not have to post everything the same way" —
# applied to format. TikTok and Pinterest no longer ship one media type every
# day: the outlet rotates video / carousel / single, and (like every other
# rotation here) never serves the same media two days running.
#
#   TikTok  — video leads (native reach), but photo carousels (Photo Mode) and
#             single stills mix in. 2025/26: Photo Mode carousels over-index on
#             saves and shares, and a strong single still cuts through a video feed.
#   Pinterest — static pins lead (Pinterest is a still-first, search surface),
#             with multi-card carousels for step-by-step depth and the odd 2:3
#             video pin. Carousels and video both out-save a plain pin when the
#             topic is a process.
TT_MEDIA = ["video", "carousel", "video", "image", "video",
            "carousel", "video", "image", "carousel"]
PIN_MEDIA = ["image", "carousel", "image", "video", "image",
             "carousel", "image", "video"]

MEDIA_LABEL = {
    ("tiktok", "video"):    "Vertical MP4 · motion (1080x1920)",
    ("tiktok", "carousel"): "Photo carousel · {n} stills (1080x1920)",
    ("tiktok", "image"):    "Single image (1080x1920)",
    ("pinterest", "image"):    "Pin 1000x1500",
    ("pinterest", "carousel"): "Carousel Pin · {n} cards (1000x1500)",
    ("pinterest", "video"):    "Video Pin · vertical MP4 (1080x1920)",
}

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


_PLANS = {}


def rotation_plan(name, rotation, resolve=None):
    """Walk a rotation across every theme, skipping any slot that would serve
    the same layout two days running.

    Without this, a fallback silently collapses the rotation: a stat template
    on a day with no number falls back to its neighbour in the cycle, and the
    outlet quietly posts the same card twice in a row.
    """
    if name in _PLANS:
        return _PLANS[name]
    plan, prev, rot = {}, None, 0
    for t in C.THEMES:
        cand = None
        for _ in range(len(rotation)):
            cand = rotation[rot % len(rotation)]
            rot += 1
            if resolve:
                cand = resolve(t, cand)
            if cand != prev:
                break
        plan[idxof(t)] = cand
        prev = cand
    _PLANS[name] = plan
    return plan


def video_plan(platform):
    """Same idea for video: no two days running may open on the same frame."""
    key = f"video:{platform}"
    if key in _PLANS:
        return _PLANS[key]
    plan, prev, rot = {}, None, VIDEO_OFFSET.get(platform, 0)
    for t in C.THEMES:
        idx = rot % len(VIDEO_RECIPES)
        for _ in range(len(VIDEO_RECIPES)):
            idx = rot % len(VIDEO_RECIPES)
            rot += 1
            if VIDEO_RECIPES[idx][0] != prev:
                break
        plan[idxof(t)] = idx
        prev = VIDEO_RECIPES[idx][0]
    _PLANS[key] = plan
    return plan


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

    prev_style = None

    def allowed(g, style):
        if style == prev_style:              # never the same tile twice running
            return False
        if g == "light" and prev == "light":
            return False
        if g == "violet" and (prev == "violet" or prev2 == "violet"):
            return False
        return True

    for t in C.THEMES:
        i = idxof(t)
        if ig_is_reel(i):                    # a Reel: its opening frame is the tile
            for _ in range(len(IG_REEL_RECIPES)):
                idx = rrot % len(IG_REEL_RECIPES)
                rrot += 1
                style = IG_REEL_RECIPES[idx][0]
                ground = TEMPLATE_GROUND.get(style, "dark")
                if allowed(ground, style):
                    break
            reels[i] = idx
        else:
            for _ in range(len(IG_ROTATION)):
                style = _cover_style(t, IG_ROTATION[rot % len(IG_ROTATION)])
                rot += 1
                ground = TEMPLATE_GROUND.get(style, "dark")
                if allowed(ground, style):
                    break
            covers[i] = style
        prev2, prev = prev, ground
        prev_style = style
    _IG_PLAN = (covers, reels)
    return _IG_PLAN


def ig_cover(t, i):
    """The day's slot in the nine-post rotation."""
    name = ig_plan()[0].get(i) or _cover_style(t, IG_ROTATION[(i - 1) % len(IG_ROTATION)])
    spec = _base(t, treatment=_tex(i), mood=_mood(i))
    if name == "ig_photo":
        spec["plate_h"] = 520 + (i % 3) * 40
    if name == "ig_spectrum":
        # the flat-dark cover alternates graphite/ink so a run of dark tiles in
        # the grid never reads as the same tone twice
        spec["ground"] = "ink" if i % 2 else "graphite"
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
        recipe = VIDEO_RECIPES[video_plan(platform)[i]]
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


# ---------------------------------------------------------------- SINGLE STILL
# The frames that can carry a post on their own — a hook, a plate, a line, a
# number — used on a TikTok single-image day. They rotate so image days do not
# all look alike.
SINGLE_VERT = ["v_coldopen", "v_broll", "v_quote", "v_stat"]


def single_vert(t, i):
    """A TikTok single-image day: one self-contained vertical still."""
    pool = [s for s in SINGLE_VERT if s != "v_stat" or t.get("numeral")]
    style = pool[(i - 1) % len(pool)]
    spec = _base(t, treatment=_tex(i), mood=_mood(i), kicker=t["series"])
    if style == "v_quote":
        spec["quote"] = t["quote"]
    if style == "v_stat":
        spec["numeral_label"] = t.get("numeral_label", t["hook"])
    return [(style, spec)]


# --------------------------------------------------------------- PIN CAROUSEL
# A Pinterest carousel is a short sequence of full 2:3 pins on one theme —
# a photo-top hook, the checklist, the one-line rule — every card a different
# layout and every card standalone-strong (Pinterest caps a carousel at five
# cards). The pin templates are built for 2:3, so no card floats in empty space
# the way a 4:5 interior would when stretched to a taller frame.
PIN_CAROUSEL_RECIPES = [
    ["pin_photo", "pin_printable", "pin_rule"],
    ["pin_rule", "pin_list", "pin_photo"],
    ["pin_printable", "pin_photo", "pin_rule"],
    ["pin_photo", "pin_rule", "pin_list"],
]


def pin_carousel(t, i):
    """A themed sequence of full pins — hook, checklist, rule — each a different
    layout, each strong enough to stand on its own."""
    recipe = PIN_CAROUSEL_RECIPES[(i - 1) % len(PIN_CAROUSEL_RECIPES)]
    slides = []
    for k, style in enumerate(recipe):
        spec = _base(t, treatment=_tex(i, k), mood=_mood(i, k),
                     kicker="CHECKLIST", plate_ratio=0.40 + (k % 3) * 0.03)
        slides.append((style, spec))
    return slides


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


def cap_instagram(t, media="carousel"):
    """De-duplicated from the rest of the drop. The cover/first frame already
    carries the hook, so the caption opens on the *why* (the sub) rather than
    repeating the exact headline the other five platforms run that day — an
    identical first line across accounts is precisely what Instagram's
    unoriginal-content demotion keys on, and a new account has no trust to spend.
    The ask is then cut to the format: a Reel is a lean reach play, a carousel a
    depth play that earns the swipe and the save."""
    sub, cta = t["sub"], t["cta"]
    if media == "video":                 # Reel — lean (research: 75-150 words)
        body = (f"{sub}\n\n{cta}\n\n"
                f"Watch to the end, save it, then follow {HANDLE} for a new "
                f"system every day.")
    else:                                 # Carousel — depth (150-300 words)
        body = (f"{sub}\n\n"
                f"{_arrow_list(t['beats'])}\n\n"
                f"Swipe through, save it for later, and send it to someone who "
                f"needs it. Follow {HANDLE} for a new system every day.")
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


def cap_pinterest(t, media="image", cards=0):
    """Pinterest ranks on keywords, not hashtags: a keyword title (the first
    ~40 chars carry it) and a keyword-rich description kept under the 500-char
    cap. The lead line names the format so a carousel or video reads as one."""
    title = t["keyword"].title()
    body = f"{t['hook']} {t['sub']}"
    if media == "carousel":
        lead = f"{title}: swipe through all {cards} cards."
        tail = "Save this pin and follow for systems that actually stick."
    elif media == "video":
        lead = f"{title} — the quick breakdown."
        tail = "Save this pin for the next time you need it."
    else:
        lead = f"{title}."
        tail = f"Save this pin for later, and follow {HANDLE} for more."
    return title, f"{lead} {body} {tail}"[:498].rstrip()


def cap_youtube(t):
    """De-duplicated from the rest of the drop. The video already shows the hook,
    so the title and description lead with the *searchable keyword* and the
    theme's own line instead of the same headline every other outlet runs.
    Shorts are increasingly a search surface: a keyword title earns impressions a
    repeated hook does not, and a numbered breakdown reads differently from the
    arrow lists the other captions use — so YouTube isn't a carbon copy the
    algorithm can flag as reposted."""
    kw = t["keyword"].title()
    title = f"{kw} #shorts"
    if len(title) > 98:
        title = kw[:88].rstrip() + " #shorts"
    desc = (f"{kw}\n\n{t['quote']}\n\n"
            + "\n".join(f"{k}. {b}" for k, b in enumerate(t['beats'], 1))
            + f"\n\nFollow {HANDLE} for more.\n\n"
            + " ".join(tags_for(t, 4) + ["#shorts"]))   # Shorts: keep to ~5
    return title, desc


# TikTok hashtags — tighter than the broad cross-platform set, and NO #fyp.
# A small account wins by ranking in a *smaller* pool, so we lead with niche,
# native ("-tok") and long-tail tags over #motivation/#success, which only put
# the post up against the biggest accounts on the platform. Kept to 4-5 (the
# range TikTok rewards) and rotated by day so two posts on one topic don't carry
# the identical set.
TT_NICHE = {
    "core":      ["#selfimprovementjourney", "#disciplineovermotivation",
                  "#personalgrowthtips", "#betteryourself"],
    "systems":   ["#atomichabits", "#habitbuilding", "#productivitysystem",
                  "#systemsthinking"],
    "money":     ["#moneytok", "#personalfinancetips", "#budgetingtips",
                  "#financialliteracy"],
    "career":    ["#careertok", "#careeradvice", "#worktok", "#careergrowth"],
    "training":  ["#gymtok", "#fitnessroutine", "#workoutmotivation", "#trainingsplit"],
    "recovery":  ["#wellnesstok", "#selfcareroutine", "#burnoutrecovery", "#restday"],
    "mindset":   ["#mindsetshift", "#mentalstrength", "#growthmindset", "#stoicmindset"],
    "time":      ["#timeblocking", "#productivitytok", "#timemanagementtips", "#deepwork"],
    "social":    ["#confidencetips", "#socialskills", "#communicationskills", "#charismatips"],
    "declutter": ["#declutter", "#minimalisttok", "#organizationtips", "#slowliving"],
    "challenge": ["#30daychallenge", "#disciplinechallenge", "#habitchallenge", "#dailyhabits"],
}


def tt_tags(t):
    """4-5 niche/native tags led by the theme's own topic — no #fyp, no wash of
    mega-broad tags. Rotated by day so a topic's posts don't all match."""
    i = idxof(t)

    def rot(lst, k):
        k %= len(lst)
        return lst[k:] + lst[:k]

    keys = t["tags"] or ["core"]
    picked = []
    for h in rot(TT_NICHE.get(keys[0], TT_NICHE["core"]), i)[:3]:
        if h not in picked:
            picked.append(h)
    if len(keys) > 1:
        for h in rot(TT_NICHE.get(keys[1], []), i + 1)[:2]:
            if len(picked) < 5 and h not in picked:
                picked.append(h)
    for h in rot(TT_NICHE["core"], i)[:2]:       # one broad-ish reach tag to round out
        if len(picked) >= 5:
            break
        if h not in picked:
            picked.append(h)
    return picked[:5]


# Per-post sound direction (creator-facing, written to the caption header — NOT
# the pasted caption). TikTok distributes on sound: the winning move is to attach
# a *trending* sound in the app, which links the post to that sound's traffic.
TT_SOUND_MOOD = {
    "energetic": "a high-energy beat (gym / phonk / hype), ~120-140 BPM",
    "clean":     "a clean lo-fi or corporate-motivational beat, ~90-110 BPM",
    "calm":      "a calm cinematic or soft-piano track, ~70-90 BPM",
    "warm":      "a warm, feel-good pop track",
}
TT_SOUND_TAG = {
    "training": "energetic", "challenge": "energetic",
    "money": "clean", "career": "clean", "time": "clean",
    "systems": "clean", "declutter": "clean", "core": "clean",
    "recovery": "calm", "mindset": "calm", "social": "warm",
}


def _audio_mood(t):
    """The kind of track that fits the theme's energy, shared by every platform
    whose file ships silent (TikTok, YouTube Shorts, IG Reels)."""
    key = next((k for k in t["tags"] if k in TT_SOUND_TAG), "systems")
    return TT_SOUND_MOOD[TT_SOUND_TAG[key]]


def tt_sound(t, media):
    mood = _audio_mood(t)
    return (f"Add {mood} in the TikTok editor (Add sound -> Trending) and duck it "
            f"under your on-screen text. The file ships without audio on purpose — "
            f"attaching a trending sound in-app is what earns its reach.")


# YouTube Shorts and Instagram Reels both distribute on watch-time, and a *silent*
# vertical video is suppressed almost automatically — the single most common
# reason a Short or Reel gets ~0 views. These MP4s render without an audio track
# (the type is on-screen), so the fix is a creator-facing AUDIO note in the header
# telling you exactly what to add before you publish.
def yt_audio(t):
    mood = _audio_mood(t)
    return (f"The MP4 ships silent, and a silent Short gets suppressed. Add sound "
            f"before you post: record a quick voiceover of the hook and steps, or "
            f"in the YouTube Shorts editor tap Add sound and pick {mood} (or a "
            f"track from the free YouTube Audio Library). Keep it under the "
            f"on-screen text.")


def ig_reel_audio(t):
    mood = _audio_mood(t)
    return (f"The MP4 ships silent, and a silent Reel is barely pushed. In the "
            f"Reels editor tap Add audio -> Trending (the tracks marked with the "
            f"up-arrow) and pick {mood}; duck it under the on-screen text. On "
            f"Reels, using a trending audio is itself a reach signal.")


# Caption asks, rotated by day so no two posts read from the same template. The
# hook always leads (it is the whole job of the first line); {cta} is the theme's
# own call to action, so the ask stays specific to the post.
TT_VIDEO_ASKS = [
    "{cta} Comment where you're starting.",
    "Save this, then run it. {cta}",
    "{cta} Which one is you? Drop the number.",
    "{cta} Follow for the next system.",
    "{cta} Send it to someone who needs it.",
    "Save it now. {cta}",
    "{cta} Tell me the one you'll skip.",
    "Bookmark this. {cta}",
]
TT_CAROUSEL_ASKS = [
    "Swipe through. {cta}",
    "Swipe to the end, then save the one you need.",
    "Swipe. {cta} Comment the step you'll run first.",
    "Swipe through and save it. {cta}",
    "Swipe. Which one are you skipping? Be honest.",
    "Swipe through. {cta} Drop your number below.",
]
TT_IMAGE_ASKS = [
    "Save it for the next time you need it.",
    "Screenshot this one.",
    "Save this where you'll see it tonight.",
    "Keep this on hand.",
    "Save it, and follow for the next one.",
]


def _pick(pool, i):
    return pool[(i - 1) % len(pool)]


def cap_tiktok(t, media="video"):
    """The hook leads (it is the whole job of the first line, the only thing that
    shows above the fold). The ask rotates so no two posts read the same, and is
    cut to the format. Trending-sound direction lives in the caption header, not
    here — you tell the algorithm about sound by adding it in-app, not by asking
    a viewer to."""
    hook, cta, i = t["hook"], t["cta"], idxof(t)
    if media == "carousel":               # Photo Mode — swipe-led
        body = f"{hook}\n\n{_pick(TT_CAROUSEL_ASKS, i).format(cta=cta)}"
    elif media == "image":                # single still
        body = f"{hook} {cta}\n\n{_pick(TT_IMAGE_ASKS, i).format(cta=cta)}"
    else:                                  # video
        body = f"{hook}\n\n{_pick(TT_VIDEO_ASKS, i).format(cta=cta)}"
    return body + "\n\n" + " ".join(tt_tags(t))   # TikTok: 4-5 niche tags, no #fyp


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
                # video-first for cold-start reach: a Reel by default, a carousel
                # every third day for depth/saves and the cover rotation
                if ig_is_reel(i):
                    slides = video_frames(t, i, "instagram")
                    common.update(fmt="vert", is_video=True, media="video",
                                  format="Reel · vertical MP4 (1080x1920)",
                                  slides=slides, durations=video_durations(len(slides)),
                                  caption=cap_instagram(t, "video"),
                                  audio=ig_reel_audio(t))
                else:
                    slides = carousel(t, i)
                    common.update(fmt="ig", is_video=False, media="carousel",
                                  format=f"Carousel · {len(slides)} slides (1080x1350)",
                                  slides=slides, caption=cap_instagram(t, "carousel"))
            elif pkey == "facebook":
                style = rotation_plan("fb", FB_ROTATION)[i]
                spec = _base(t, treatment=_tex(i, 2), mood=_mood(i, 2))
                common.update(fmt="ig", is_video=False, media="image",
                              format="Single image (1080x1350)",
                              slides=[(style, spec)], caption=cap_facebook(t))
            elif pkey == "x":
                style = rotation_plan(
                    "x", X_ROTATION,
                    lambda th, c: "x_headline" if c == "x_stat"
                    and not th.get("numeral") else c)[i]
                spec = _base(t, treatment=_tex(i, 4), mood=_mood(i, 4),
                             panel="violet" if i % 2 else "volt",
                             panel_line=t["quote"])
                common.update(fmt="wide", is_video=False, media="image",
                              format="Text + image card (1600x900)",
                              slides=[(style, spec)], caption=cap_x(t))
            elif pkey == "linkedin":
                style = rotation_plan(
                    "li", LI_ROTATION,
                    lambda th, c: "li_note" if c == "li_stat"
                    and not th.get("numeral") else c)[i]
                spec = _base(t, eyebrow=f"GOGETTR · {t['pillar'].title()}",
                             footer_right="READ →" if style == "li_carousel" else None)
                common.update(fmt="square", is_video=False, media="image",
                              format="Single image (1080x1080)",
                              slides=[(style, spec)], caption=cap_linkedin(t))
            elif pkey == "youtube":
                slides = video_frames(t, i, "youtube")
                title, desc = cap_youtube(t)
                common.update(fmt="vert", is_video=True, media="video",
                              format="Shorts · vertical MP4 (1080x1920)",
                              slides=slides, durations=video_durations(len(slides)),
                              title=title, caption=desc, audio=yt_audio(t))
            elif pkey == "tiktok":
                media = rotation_plan("tt_media", TT_MEDIA)[i]
                if media == "image":
                    slides = single_vert(t, i)
                    common.update(fmt="vert", is_video=False, media="image",
                                  format=MEDIA_LABEL[("tiktok", "image")],
                                  slides=slides, caption=cap_tiktok(t, "image"))
                elif media == "carousel":
                    slides = video_frames(t, i, "tiktok")     # Photo Mode stills
                    common.update(fmt="vert", is_video=False, media="carousel",
                                  format=MEDIA_LABEL[("tiktok", "carousel")].format(n=len(slides)),
                                  slides=slides, caption=cap_tiktok(t, "carousel"))
                else:
                    slides = video_frames(t, i, "tiktok")
                    common.update(fmt="vert", is_video=True, media="video",
                                  format=MEDIA_LABEL[("tiktok", "video")],
                                  slides=slides, durations=video_durations(len(slides)),
                                  caption=cap_tiktok(t, "video"))
                common["sound"] = tt_sound(t, media)
            elif pkey == "pinterest":
                media = rotation_plan("pin_media", PIN_MEDIA)[i]
                board = board_for(t)
                if media == "carousel":
                    slides = pin_carousel(t, i)
                    title, desc = cap_pinterest(t, "carousel", cards=len(slides))
                    common.update(fmt="pin", is_video=False, media="carousel",
                                  format=MEDIA_LABEL[("pinterest", "carousel")].format(n=len(slides)),
                                  board=board, slides=slides, title=title, caption=desc)
                elif media == "video":
                    slides = video_frames(t, i, "pinterest")
                    title, desc = cap_pinterest(t, "video")
                    common.update(fmt="vert", is_video=True, media="video",
                                  format=MEDIA_LABEL[("pinterest", "video")],
                                  slides=slides, durations=video_durations(len(slides)),
                                  board=board, title=title, caption=desc)
                else:
                    style = rotation_plan("pin", PIN_ROTATION)[i]
                    spec = _base(t, board=board, treatment=_tex(i, 5), mood=_mood(i, 5),
                                 kicker="CHECKLIST", plate_ratio=0.40 + (i % 3) * 0.03)
                    title, desc = cap_pinterest(t, "image")
                    common.update(fmt="pin", is_video=False, media="image",
                                  format=MEDIA_LABEL[("pinterest", "image")],
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
