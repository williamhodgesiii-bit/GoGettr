# -*- coding: utf-8 -*-
"""
Adaptation engine: theme x platform -> finished Post spec.
Decides slide composition (varied per day), assembles platform-native
captions/hashtags, and schedules each post. Start: Mon 2026-08-17, ET.
Times are platform-optimal (2025/26 research), the calendar opens 8:00 AM.
"""
from datetime import date, timedelta
import engine.content as C

START = date(2026, 8, 17)   # Monday
HANDLE = "@gogettrdaily"
SITE = "gogettr.co"

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

def tags_for(t, n, extra=None):
    pool = []
    for k in (["core"] + t["tags"] + (extra or [])):
        for h in C.HASHTAGS.get(k, []):
            if h not in pool:
                pool.append(h)
    # keep #gogettr first, then spread
    out = []
    for h in pool:
        if h not in out:
            out.append(h)
        if len(out) >= n:
            break
    return out

# ------------------------------------------------------------------ SLIDES
def _cover(t, fmt, calmer=False):
    """Choose a varied cover style per theme for grid rhythm."""
    i = idxof(t)
    eb = t["series"] if not calmer else f"GOGETTR · {t['pillar'].title()}"
    base = dict(eyebrow=eb, hook=t["hook"], sub=t["sub"], accent=t["accent"],
                handle=HANDLE, cta="SWIPE →" if not calmer else "READ →")
    if t["kind"] == "stat" and t.get("numeral"):
        return ("stat", {**base, "numeral": t["numeral"],
                         "numeral_label": t.get("numeral_label", t["hook"]),
                         "ground": "graphite"})
    r = i % 5
    if r == 1:
        return ("cover_hook", {**base, "plate": "ink"})
    if r == 2 and not calmer:
        return ("cover_hook", {**base, "ground": "chrome", "cta": "SWIPE →"})
    if r == 3:
        return ("cover_hook", {**base, "plate": "graphite"})
    return ("cover_hook", {**base, "ground": "graphite"})

def _beats(t, fmt, calmer=False):
    slides = []
    n = len(t["beats"])
    for k, beat in enumerate(t["beats"], 1):
        plate = "graphite" if (k % 2 == 0) else None
        slides.append(("body_beat", dict(
            eyebrow=t["series"] if not calmer else "GOGETTR",
            index=f"{k} / {n}", kicker=f"MOVE {k:02d}",
            hook=beat, accent=t["accent"], handle=HANDLE, cta="",
            plate=plate, ground="graphite")))
    return slides

def _close(t, fmt, calmer=False):
    drop = f"NEW SYSTEM EVERY MORNING · {SITE.upper()}"
    return ("close_cta", dict(cta_hook=t["cta"], drop=drop, accent=t["accent"],
            handle=HANDLE, cta="FOLLOW →" if not calmer else "FOLLOW GOGETTR →",
            ground="ink"))

def carousel(t, fmt, calmer=False):
    return [_cover(t, fmt, calmer)] + _beats(t, fmt, calmer) + [_close(t, fmt, calmer)]

def video_frames(t, platform):
    """4-frame vertical slideshow -> MP4. Hook, system, turn, CTA."""
    eb = t["series"]
    f1 = ("vert_hook", dict(eyebrow=eb, hook=t["hook"], accent=t["accent"],
                            plate="ink"))
    # frame 2: three beats as a fast list
    f2 = ("cover_list", dict(eyebrow=eb, hook="The system", items=t["beats"][:4],
                             accent=t["accent"], ground="graphite", cta="", handle=HANDLE))
    # frame 3: the quotable turn, big
    f3 = ("rule", dict(hook=t["quote"], accent=t["accent"], ground="ink", cta=""))
    f4 = ("vert_end", dict(cta_hook="Follow for one system a day.", accent=t["accent"],
                           ground="ink"))
    # normalize all to vertical format at render time
    return [f1, f2, f3, f4]

# ------------------------------------------------------------------ CAPTIONS
def _arrow_list(beats):
    return "\n".join(f"→ {b}" for b in beats)

def cap_instagram(t):
    body = (f"{t['hook']}\n\n{t['sub']}\n\n"
            f"Swipe the carousel for the full system.\n\n"
            f"Save this and send it to someone who needs the reminder. "
            f"Follow {HANDLE} for one system a day.")
    return body + "\n\n" + " ".join(tags_for(t, 12))

def cap_facebook(t):
    return (f"{t['hook']}\n\n{t['sub']}\n\n"
            f"{_arrow_list(t['beats'])}\n\n"
            f"Which one would move your month the most? Tell me below. "
            f"(Save the post so it is there when you need it.)\n\n"
            + " ".join(tags_for(t, 3)))

def cap_x(t):
    thread = (f"{t['hook']}\n\n"
              + "\n".join(f"{k}. {b}" for k, b in enumerate(t['beats'], 1))
              + f"\n\n{t['cta']}")
    return thread + "\n\n" + " ".join(tags_for(t, 2))

def cap_linkedin(t):
    opener = "The most capable people I know don't run on willpower. They design defaults."
    close = ("Systems beat motivation because they only ask you to decide once.\n\n"
             "Operating systems for ambitious people — new one every morning.")
    return (f"{opener}\n\n{t['hook']}\n\n"
            + "\n".join(f"• {b}" for b in t['beats'])
            + f"\n\n{close}\n\n" + " ".join(tags_for(t, 4)))

def cap_pinterest(t):
    title = t["keyword"].title()
    desc = (f"{title} — a simple GoGettr system. {t['hook']} "
            f"{t['sub']} Save this pin for the next time you need it. "
            f"More systems for money, training and recovery at {SITE}.")
    kws = " ".join(tags_for(t, 6))
    return title, desc + "\n\n" + kws

def cap_youtube(t):
    title = f"{t['hook']} #shorts"
    if len(title) > 98:
        title = t["hook"][:88].rstrip(". ") + " #shorts"
    desc = (f"{t['hook']}\n\n{t['sub']}\n\n"
            + _arrow_list(t['beats'])
            + f"\n\nNew system every morning. {SITE}\n\n"
            + " ".join(tags_for(t, 4, extra=None) + ["#shorts", "#gogettr"]))
    return title, desc

def cap_tiktok(t):
    return (f"{t['hook']} {t['cta']}\n\n"
            f"(add a trending sound) — save it for later.\n"
            + " ".join(tags_for(t, 6) + ["#fyp", "#foryou"]))

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
                # mostly carousels; every 3rd day a Reel (reach) cross-posted from vert
                if i % 3 == 0:
                    slides = video_frames(t, pkey)
                    common.update(fmt="vert", is_video=True, format="Reel · vertical MP4 (1080x1920)",
                                  slides=slides, caption=cap_instagram(t))
                else:
                    slides = carousel(t, "ig")
                    common.update(fmt="ig", is_video=False,
                                  format=f"Carousel · {len(slides)} slides (1080x1350)",
                                  slides=slides, caption=cap_instagram(t))
            elif pkey == "facebook":
                cov = _cover(t, "ig")
                # give FB its own identity: a light chrome card, violet accent (legal on light)
                spec = dict(cov[1])
                spec.pop("plate", None)
                spec["ground"] = "chrome"
                spec["accent"] = "violet"
                spec["cta"] = "GOGETTR.CO"
                common.update(fmt="ig", is_video=False, format="Single image (1080x1350)",
                              slides=[(cov[0], spec)], caption=cap_facebook(t))
            elif pkey == "x":
                style = "wide_stat" if (t["kind"] == "stat" and t.get("numeral")) else "wide_quote"
                spec = dict(eyebrow=t["series"], hook=t["hook"], accent=t["accent"],
                            numeral=t.get("numeral", ""), numeral_label=t.get("numeral_label", t["hook"]),
                            ground="graphite", handle=HANDLE, cta="GOGETTR.CO")
                common.update(fmt="wide", is_video=False, format="Text + image card (1600x900)",
                              slides=[(style, spec)], caption=cap_x(t))
            elif pkey == "linkedin":
                slides = carousel(t, "square", calmer=True)
                # append a link card asset
                link = ("wide_quote", dict(eyebrow="GOGETTR · THE SYSTEM AUDIT",
                        hook=t["hook"], accent=t["accent"], ground="graphite",
                        handle="GOGETTR.CO/AUDIT", cta=""))
                common.update(fmt="square", link_slide=link, is_video=False,
                              format=f"Document carousel · {len(slides)} slides (1080x1080) + link card",
                              slides=slides, caption=cap_linkedin(t))
            elif pkey == "youtube":
                slides = video_frames(t, pkey)
                title, desc = cap_youtube(t)
                common.update(fmt="vert", is_video=True, format="Shorts · vertical MP4 (1080x1920)",
                              slides=slides, title=title, caption=desc)
            elif pkey == "tiktok":
                slides = video_frames(t, pkey)
                common.update(fmt="vert", is_video=True,
                              format="Vertical MP4 slideshow (1080x1920)",
                              slides=slides, caption=cap_tiktok(t))
            elif pkey == "pinterest":
                style = "pin_rule" if i % 4 == 0 else "pin_list"
                spec = dict(keyword=t["keyword"], hook=t["hook"], items=t["beats"],
                            accent=t["accent"], url=f"{SITE.upper()}",
                            ground="violet" if style == "pin_rule" else "graphite",
                            plate="violet" if style == "pin_rule" else None)
                title, desc = cap_pinterest(t)
                common.update(fmt="pin", is_video=False, format="Pin 1000x1500",
                              slides=[(style, spec)], title=title, caption=desc)
            posts.append(common)
    return posts

if __name__ == "__main__":
    ps = build_all()
    print("total posts:", len(ps))
    vids = sum(1 for p in ps if p["is_video"])
    print("videos:", vids, "| images posts:", len(ps) - vids)
    from collections import Counter
    print(Counter(p["platform"] for p in ps))
