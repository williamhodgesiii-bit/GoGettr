# GoGettr — Social Content Strategy & Backlog

**Brand:** GoGettr · `@gogettrdaily` · *Build the machine. Skip the mood.*
**Backlog:** 56 daily themes × 7 outlets = **392 finished posts**, starting **Mon Aug 17, 2026**.
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
| **Instagram** (main) | Carousel 1080×1350 (most days) + Reel every 3rd day | Carousels win engagement & saves (~0.55% vs 0.45% static); Reels win reach (~2.25×). We use carousels for depth, Reels for discovery. |
| **Facebook** (linked) | Single light "chrome" card 1080×1350 + conversational caption | Distinct lighter look for FB's audience; question-led captions drive comments. |
| **TikTok** | **Rotates** — vertical MP4 slideshow · Photo Mode carousel · single still (all 1080×1920) | No outlet ships one format every day. Video leads (native reach), but Photo Mode carousels over-index on saves/shares and a single still cuts through a video feed. Cold-open hook in <1.5s, text-on-screen (68% watch muted); the caption is cut to the format (video → *add sound*, carousel → *swipe*). |
| **X / Twitter** | Text thread + 1600×900 card | Text leads engagement on X (~3.56%); the card carries the hook, the thread carries the system. |
| **LinkedIn** | Single image 1080×1080 + a value-packed caption | Kept deliberately simple — the steps live in the caption (where LinkedIn readers actually engage). Calmer register, no slang. |
| **Pinterest** | **Rotates** — 2:3 Pin 1000×1500 · multi-card Carousel Pin · vertical Video Pin, sorted into 7 keyword-named boards | Still pins lead (Pinterest is still-first search), with carousels (2–5 full pins per theme) and video pins for step-by-step topics that out-save a plain pin. Keyword search, not hashtags — titles/descriptions are keyword-led and each pin is filed to a themed board. |
| **YouTube Shorts** | Vertical MP4 1080×1920 | Hook first, **logo/CTA at the END** (moving branding off the first 3s lifts retention 15–30%). |

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
Every caption front-loads the hook (it is all that shows above the fold — ~125
chars on IG, the first two lines on TikTok, ~40 on a Pinterest title) and then
the ask is cut to the **media type**, on 2025–26 research:

- **Instagram** — a carousel is a depth play (hook, sub, the full step list, a
  *swipe + save + send*); a Reel is a reach play, kept lean (*sound on, watch to
  the end*).
- **TikTok** — a video asks for a *trending sound*; a Photo Mode carousel asks
  for a *swipe* and a reply; a single still just asks for the *save*.
- **Pinterest** — no hashtags (keyword search); a keyword title + a keyword-rich
  description under the 500-char cap, and the lead line names the format so a
  carousel ("swipe through all N cards") or a video ("the quick breakdown")
  reads as one.

## Hashtags — broad reach, within each platform's limit
Tags are chosen for **broad, high-traffic reach** (e.g. `#selfimprovement`,
`#money`, `#productivity`, `#discipline`) and led by the post's own topic, and
they never exceed what a platform rewards in 2025–26 (the cap is per platform,
not per media type — a carousel and a Reel share Instagram's limit of five):

- **Instagram — 5** (a hard cap since Dec 2025; more get demoted from Explore/Reels)
- **TikTok — 5** (incl. `#fyp`) · **YouTube Shorts — 5** (incl. `#shorts`)
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

`python -m engine.audit` proves it. It re-renders all **1,090 slides** and fails on:

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
