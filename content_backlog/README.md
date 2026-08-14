# GoGettr Content Backlog — Upload Guide

**392 finished posts** · 56 daily themes × 7 outlets · starts **Mon Aug 17, 2026**.
Everything here is final art + caption. No editing required.

> Read `../STRATEGY.md` for the why (formats, timing, hooks, research).

---

## Where everything is

```
content_backlog/
├── 00_MASTER_SCHEDULE.csv     ← every post: ID, date, time, platform, format, hook, caption, asset path
├── manifest.json              ← counts
├── by_platform/               ← the same schedule split per outlet (import one at a time)
│   ├── instagram.csv  facebook.csv  x.csv  linkedin.csv
│   ├── youtube.csv    tiktok.csv    pinterest.csv
├── instagram/  facebook/  x/  linkedin/  youtube/  tiktok/  pinterest/
│   └── pinterest/by_board/    ← pins split by board + _BOARDS.txt (create these boards)
│   └── <POST_ID>/
│        ├── 01_cover.png, 02_beat.png … 07_close.png   (Instagram carousels)
│        ├── video.mp4                                    (TikTok / Shorts / IG Reels)
│        ├── 01_card.png / 01_pin.png / 01_cover.png      (X / Pinterest / FB / LinkedIn single image)
│        └── caption.txt   ← ID, publish time, format, and the caption to paste
```

## Post ID format
`GG-YYMMDD-PLATFORM` → e.g. **`GG-260817-IG`** = the Instagram post for Aug 17, 2026.
Platform codes: `IG` Instagram · `FB` Facebook · `X` X/Twitter · `LI` LinkedIn ·
`YT` YouTube Shorts · `TT` TikTok · `PIN` Pinterest.

## Two ways to publish

**A. Manual (fastest to start).** Open a post folder → upload the PNGs in numeric
order (or `video.mp4`) → open `caption.txt`, copy the caption, paste. Done.

**B. Bulk scheduler.** Import `00_MASTER_SCHEDULE.csv` (or a `by_platform/*.csv`)
into Metricool / Later / Buffer / Publer. Columns map cleanly: `date`, `time`
(ET), `caption`, `primary_asset`, `asset_folder`. Point the tool at the matching
folder for the media.

## Per-platform notes
- **Instagram** — carousels: upload `01…07` in order. Reels (every 3rd day):
  upload `video.mp4`, add a trending audio in-app. IG is the main page; mirror to
  Facebook or use the FB-specific card in `facebook/`.
- **Facebook** — one image + a comment-friendly caption. Lighter look on purpose.
- **TikTok** — upload `video.mp4`, then **add a trending sound in-app** (native
  audio > embedded music for reach). Text is already burned in.
- **X / Twitter** — attach `01_card.png`; the caption is written as a short thread
  (post line 1, then the numbered steps as replies).
- **LinkedIn** — one square image + the caption. The steps live in the caption
  (bulleted), which is where LinkedIn readers engage. Simple on purpose.
- **Pinterest** — **organised by board.** Create the 7 boards listed in
  `pinterest/by_board/_BOARDS.txt`, then upload each pin to the board named in its
  `caption.txt` (`BOARD:` line) — or work board-by-board from the
  `pinterest/by_board/*.csv` files. Paste the title (first caption line) +
  description. Pinterest ranks on keywords, so the titles/descriptions are
  keyword-led and carry **no hashtags** (Pinterest no longer recommends them).
- **YouTube Shorts** — upload `video.mp4`, paste the title line + description.

## Hashtags (already capped to each platform's 2025/26 limit)
Broad, high-traffic tags only — and never more than a platform rewards:
**Instagram 5** (hard cap since Dec 2025), **TikTok 5** (incl. #fyp),
**YouTube Shorts 5** (incl. #shorts), **LinkedIn 3**, **X 2**, **Facebook 2**,
**Pinterest 0** (keywords + boards instead). They're baked into each caption.

## About the videos
Per the Vault's *Easy MP4* rule, videos are clean vertical slideshows (hook →
system → the turn → CTA, ~11s) with no audio baked in — **add a trending native
sound when you post**. That's the highest-reach move on TikTok/Reels/Shorts and
keeps you clear of music licensing.

## Want changes?
The whole backlog regenerates from `engine/` (`python -m engine.render`). Edit a
theme's words in `engine/content.py`, tweak times/formats in `engine/build.py`, or
adjust the look in `engine/templates.py` / `styles.py`, then re-run.
