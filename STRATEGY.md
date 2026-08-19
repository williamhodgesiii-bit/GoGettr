# GoGettr — Social Content Strategy & Backlog

**Brand:** GoGettr · `@gogettrdaily` · *Build the machine. Skip the mood.*
**Backlog:** 112 daily themes × 7 outlets = **784 finished posts**, **Mon Aug 17 – Sun Dec 6, 2026** (Vol. 01 weeks 1–8, Vol. 02 weeks 9–16 on all-new topics).
**Voice:** short declaratives, second person, a number where a number will do. No hype, no emoji, no exclamation marks — the colour is already shouting.

This backlog was built to a design system (the *Volt Brand Kit*) and to platform
research on what actually performs in 2025–2026. Every post is finished art +
caption, named and scheduled, ready to upload. Nothing here needs an editor.

---

## The one idea, seven ways

Each day has **one theme** (a system, audit, or challenge drawn from the Content
Vault + originals). That theme is then re-cut per platform so the drop reads as
*one campaign* while each outlet gets a native-feeling post — different framing,
different asset, different caption, same spine.

| Outlet | Format(s) used | Why (2025–26 research) |
|---|---|---|
| **Instagram** (main) | **Reel 1080×1920 (most days)** + Carousel 1080×1350 every 3rd day | A new account has no follower base, and carousels are shown almost entirely to people who *already* follow you — so they can't find new viewers. Reels are the only surface that reaches non-followers (~2.25× the reach), so on a cold-start they lead for discovery, with a carousel every third day for the depth/saves play (and to keep the full cover-template rotation alive). |
| **Facebook** (linked) | Single light "chrome" card 1080×1350 + conversational caption | Distinct lighter look for FB's audience; question-led captions drive comments. |
| **TikTok** | **Rotates** — vertical MP4 (motion) · Photo Mode carousel · single still (all 1080×1920) | No outlet ships one format every day. Video leads (native reach), but Photo Mode carousels over-index on saves/shares and a single still cuts through a video feed. The video is **real motion** — a slow Ken-Burns push on every frame and a slide/wipe cut between them, so it plays as a video, not a deck of held stills (which TikTok barely distributes). Cold-open hook in <1.5s, text-on-screen (68% watch muted). Sound is added **in-app** at upload (see below), so the file ships without audio on purpose. |
| **X / Twitter** | Text thread + 1600×900 card | Text leads engagement on X (~3.56%); the card carries the hook, the thread carries the system. |
| **LinkedIn** | Single image 1080×1080 + a value-packed caption | Kept deliberately simple — the steps live in the caption (where LinkedIn readers actually engage). Calmer register, no slang. |
| **Pinterest** | **Rotates** — 2:3 Pin 1000×1500 · multi-card Carousel Pin · vertical Video Pin, sorted into 7 keyword-named boards | Still pins lead (Pinterest is still-first search), with carousels (2–5 full pins per theme) and video pins for step-by-step topics that out-save a plain pin. Keyword search, not hashtags — titles/descriptions are keyword-led and each pin is filed to a themed board. |
| **YouTube Shorts** | Vertical MP4 1080×1920 | Hook first, **logo/CTA at the END** (moving branding off the first 3s lifts retention 15–30%). The file ships **silent** — a silent Short is suppressed automatically, so each caption carries an **AUDIO** note (add a voiceover or a track before upload). The title/description lead with the **searchable keyword**, not the on-screen hook, because Shorts is now a search surface. |

Neither **TikTok** nor **Pinterest** serves the same media two days running — the outlet
rotates video / carousel / still (TikTok) and pin / carousel / video (Pinterest), so the
feed reads as varied on format, not just on theme.

## Posting times (ET) — the daily "drip"

The calendar opens **Monday 8/17 at 8:00 AM** and each platform fires at its
research-backed best time, so the brand shows up across the whole day:

```
08:00  LinkedIn      (morning, pre-work routine)
08:00  Instagram     (flagship drop)
09:00  Facebook      (morning, Meta)
09:00  X / Twitter   (morning peak)
15:00  YouTube Shorts(afternoon 2–6pm window)
19:00  TikTok        (evening peak)
20:00  Pinterest     (evening / weekend skew)
```

You do **not** have to post everything every day — this is a *backlog* to draw
from. If you post a platform 3×/week, the library simply lasts longer. Times are
in the schedule CSV and can be shifted in one place (`engine/build.py`).

## How the posts stay "hooky" and swipe-worthy

- **S1 is a contract.** Every cover leaves something unfinished and points at the
  next slide — a question, a gap, a first step. If the cover could stand alone, it
  was rewritten. (Straight from the Vault's own rule.)
- **Escalation.** Carousels and videos go hook → tension → evidence/steps → close
  with a save/comment/follow. Videos are 4–5 frames that build to the CTA so
  people watch to the end, and no two frames use the same layout.
- **One idea per frame.** Big type, one thought, high contrast.
- **Recognisable shell.** Fixed eyebrow + `2 / 7` slide index so a
  carousel and its Reel read as the same drop and a series is recognised before
  it's read.
- **No slide repeats another.** A carousel is a cover, one card per beat, an
  optional recap and a close — and **every one of them is a different layout**:
  a step numeral, a plate band, a centred line, a highlighted phrase, a step
  rail, a quote card. Carousels run 7 or 8 slides and the recipe rotates daily.
  No outlet serves the same layout two days running — the audit fails the
  build if it does.
- **Grid rhythm.** Cover templates follow the board's nine-post rotation and
  Reels are planned as grid tiles too, so the profile reads as texture: never
  two light grounds side by side, and violet held to about one tile per row of
  three.

## Captions — cut to the platform *and* the format
Most captions front-load the hook (it is all that shows above the fold — ~125
chars on IG, the first two lines on TikTok, ~40 on a Pinterest title) and then
the ask is cut to the **media type**, on 2025–26 research. **Instagram and
YouTube are the deliberate exception:** their caption/title text does *not* open
on the shared hook (see *Originality* below).

- **Instagram** — the cover/first frame already carries the hook, so the caption
  opens on the **sub** (the "why"), not the exact headline the other five outlets
  run that day. A carousel is then a depth play (the full step list, a *swipe +
  save + send*); a Reel is a reach play, kept lean (*watch to the end + save*).
- **YouTube** — the title and description lead with the **searchable keyword**
  (e.g. "Systems That Beat Willpower"), and the steps are a **numbered** list, so
  YouTube reads natively for search and isn't a text copy of the IG/FB caption.
- **TikTok** — the hook leads and the ask **rotates** post to post (no two read
  from the same template) and is cut to the format: a video points at the *save
  / comment*, a Photo Mode carousel at the *swipe*, a single still at the *save*.
  The old "add a trending sound" line is gone from the caption — you don't ask a
  *viewer* to add sound. Instead each TikTok caption file carries a **SOUND** note
  (creator-facing): the kind of trending sound to add *in the TikTok editor*,
  where the app links the post to that sound's reach. A silent slideshow is the
  single biggest reason a TikTok gets 0 views; motion + an in-app trending sound
  is the fix.
- **Pinterest** — no hashtags (keyword search); a keyword title + a keyword-rich
  description under the 500-char cap, and the lead line names the format so a
  carousel ("swipe through all N cards") or a video ("the quick breakdown")
  reads as one.

## Silent video is suppressed — the AUDIO note
A vertical video with **no audio track gets almost no reach** on any of the three
video surfaces — it's the most common reason a Short or Reel sits at 0 views. The
rendered MP4s ship silent on purpose (the type is on-screen and the sound is
chosen at upload), so every video caption carries a creator-facing note naming
exactly what to add before you post:

- **TikTok** → a **SOUND** note (add a *trending* sound in-app, which links the
  post to that sound's traffic).
- **YouTube Shorts / Instagram Reels** → an **AUDIO** note (add a voiceover, a
  trending Reels audio, or a YouTube Audio Library track). Do not upload the
  silent file as-is.

## Originality — why IG and YouTube are not carbon copies
Instagram (2024–25) and YouTube both **demote content they detect as
unoriginal / reposted**, and a brand-new account has no trust to spend. Running
the *identical* headline and caption across seven accounts on the same day is
exactly that pattern. So the two flagship discovery platforms are deliberately
de-duplicated: **Instagram** opens its caption on the sub, **YouTube** leads its
title and description with the searchable keyword and lists the steps numbered.
The hook still appears — burned into the cover/first frame, where it's the brand's
recognisable line — but the *indexed text* each platform submits is its own.

## Hashtags — broad reach, within each platform's limit
Tags are chosen for **broad, high-traffic reach** (e.g. `#selfimprovement`,
`#money`, `#productivity`, `#discipline`) and led by the post's own topic, and
they never exceed what a platform rewards in 2025–26 (the cap is per platform,
not per media type — a carousel and a Reel share Instagram's limit of five):

- **Instagram — 5** (a hard cap since Dec 2025; more get demoted from Explore/Reels)
- **TikTok — 4–5, niche not broad, and *no* `#fyp`.** `#fyp` does nothing for reach
  in 2026 and reads as low-effort; the mega-broad tags (`#motivation`, `#success`)
  only put a small account up against the biggest ones. So TikTok leads with
  niche, native ("-tok") and long-tail tags (`#atomichabits`, `#timeblocking`,
  `#moneytok`), rotated by day so a topic's posts don't all carry the same set —
  the way to win is to rank in a *smaller* pool. · **YouTube Shorts — 5** (incl. `#shorts`)
- **LinkedIn — 3** · **X — 2** (3+ hashtags measurably drops reach) · **Facebook — 2**
- **Pinterest — 0.** Pinterest is keyword search, so pins rely on keyword titles,
  descriptions and board names instead of hashtags.

## Design system (from the Volt Brand Kit)

- **Colour:** Graphite `#23262B` · Ink `#0E1013` · Chrome `#E6E7E9` · Volt
  `#D6FF2E` (one accent element per post, never type on white) · Violet `#7B4DFF`
  (numerals) · Steel `#6C727C` (meta).
- **Type:** Space Grotesk (display/hook), JetBrains Mono (eyebrows/indices/footers),
  Archivo (body). Exact scale & tracking from the board.
- **Mark:** the Forward chevron `»` in three cuts (graphite / volt / violet).
- **Templates:** every named layout on the board is built — Instagram's five
  covers (spectrum hook, list cover, inset photo, stat, violet quote), the four
  TikTok/Reels frames (cold-open, day counter, B-roll plate, list tease), the
  four Pinterest pins (list, printable, photo-top, rule) and the LinkedIn set —
  plus carousel interiors and X cards in the same language. **43 distinct
  templates** are in rotation, and they differ by *structure* — where the content
  region sits, how the artboard is split, which components carry it — not by
  colour swap.
- **Plates instead of stock:** where the board marks a "photo" slot, the asset
  ships with a designed plate (seven procedural treatments — chevron, hatch,
  grid, rings, dots, sweep, bars) so nothing is a placeholder.
- **No URL:** the board stamps `gogettr.co` on pins and link cards. There is no
  live domain, so the handle carries the mark instead.

## Why nothing overlaps

Layout is measured before it is drawn. Each slide is a stack of blocks that
report their real inked height (from font metrics, not estimates) into a content
region bounded by the margins above and a reserved footer band below. If the
stack is too tall, type steps down and optional lines drop out until it fits —
so a volt bar, a hairline or a footer can never land on a descender, and text
can never run off the artboard.

`python -m engine.audit` proves it. It re-renders all **2,048 slides** and fails on:

- a slide out of format, crossing a margin, or entering the video UI-safe band;
- any two foreground elements overlapping;
- type below the legibility floor, **or squeezed well under the size its
  template asks for** — copy that has to be shrunk to fit is a template
  mismatch, not a layout that "just fits";
- volt reading as a wash rather than one accent element (measured off the
  rendered pixels), unless the template fields volt by design;
- a post that isn't built for its format — no forward cue on an IG cover, no CTA
  card at a carousel's close, a video (or a TikTok Photo Mode carousel) that
  doesn't end on the mark, or a Pinterest carousel that doesn't open on a cover;
- a layout repeated inside one post, **an outlet serving the same layout — or the
  same media type — two days running**, or a break in the grid rotation.

The backlog ships at zero issues on every one of those.

## Sources (research)
- Socialinsider / Buffer — 2025–26 format benchmarks (carousels vs Reels; 45M-post format study).
- Hootsuite / Sprout / Buffer — best time to post 2025–26.
- AuthoredUp / Socialinsider — LinkedIn document-post performance.
- Buffer / Pinterest — 2:3 pin save-rate; Pinterest video engagement.
- CapCut / Meta data — short-form 3-second hook & retention.
