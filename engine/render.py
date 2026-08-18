# -*- coding: utf-8 -*-
"""
Render pipeline. Reads build_all(), renders every slide to PNG, stitches
vertical MP4 slideshows, writes per-post caption files, and emits the
master schedule + per-platform CSVs. Output tree: content_backlog/.
"""
import os, csv, subprocess, shutil, json, glob, sys
import imageio_ffmpeg
import engine.styles as S
from engine.build import build_all, PLATFORMS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "content_backlog")
FF = imageio_ffmpeg.get_ffmpeg_exe()
PLAT_ORDER = {p[0]: n for n, p in enumerate(PLATFORMS)}

# asset filename hints per style role
ROLES = {"ig_": "cover", "beat_": "beat", "close_": "close", "v_": "frame",
         "pin_": "pin", "li_": "card", "x_": "card", "fb_": "card"}


def slide_name(k, style):
    role = next((v for p, v in ROLES.items() if style.startswith(p)), "slide")
    if style in ("beat_ledger", "beat_rows"):
        role = "recap"
    elif style == "v_end":
        role = "end"
    return f"{k:02d}_{role}.png"

def render_slides(post, folder):
    names = []
    for k, (style, spec) in enumerate(post["slides"], 1):
        img = S.STYLES[style](post["fmt"], spec)
        nm = slide_name(k, style)
        img.save(os.path.join(folder, nm), quality=95)
        names.append(nm)
    return names

# ---------------------------------------------------------------- VIDEO
# TikTok gets *motion* — the platform distributes on watch-time and sound, and a
# feed of held stills reads as a slideshow the algorithm barely pushes. So every
# TikTok frame is a slow Ken-Burns move (a centred zoom on a 2x-upscaled still,
# so the design's centred type never drifts out of frame) and the cuts between
# them are short cross-dissolves — the file plays as a video, not a deck of
# screenshots. The other outlets (Reels, Shorts, video pins) keep the held-frame
# build, which is already native to how they are usually posted.
FPS = 30
XFADE = 0.35                                   # seconds per cut
# Push / wipe transitions, not dissolves: a crossfade ghosts two sets of type
# over each other on text cards, but a slide or wipe reads as an intentional cut.
TRANSITIONS = ["slideleft", "smoothup", "wiperight", "slideup", "slideright", "smoothdown"]


def _render_frames(post, frames_dir):
    fnames = []
    for k, (style, spec) in enumerate(post["slides"], 1):
        img = S.STYLES[style]("vert", spec)
        fn = f"f{k:02d}.png"
        img.save(os.path.join(frames_dir, fn))
        fnames.append(fn)
    durs = post.get("durations") or [3.0] * len(fnames)
    durs = [durs[k] if k < len(durs) else 3.0 for k in range(len(fnames))]
    return fnames, durs


def _encode_static(post, frames_dir, fnames, durs, out):
    """Held frames (Reels / Shorts / video pins) — hold each still for its beat."""
    lines = []
    for k, fn in enumerate(fnames):
        lines.append(f"file '{fn}'\nduration {durs[k]}")
    lines.append(f"file '{fnames[-1]}'")        # duplicate last so its duration applies
    with open(os.path.join(frames_dir, "list.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    cmd = [FF, "-y", "-f", "concat", "-safe", "0", "-i", "list.txt",
           "-vf", f"fps={FPS},format=yuv420p", "-c:v", "libx264", "-preset", "veryfast",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", os.path.abspath(out)]
    return cmd


def _encode_motion(post, frames_dir, fnames, durs, out):
    """TikTok — Ken-Burns each still and cross-dissolve the cuts, so the file
    plays as a video, not a deck of screenshots. The move is a slow *centred*
    zoom (a time-driven scale + centre-crop on a constant-rate looped still), so
    the design's centred type never drifts out of frame; the direction alternates
    in/out and the transition rotates, so no two cuts look the same."""
    n = len(fnames)
    secs = [max(0.6, float(d)) for d in durs]
    inputs = []
    for k, fn in enumerate(fnames):
        # a constant-rate looped still — xfade needs CFR, and this keeps it simple
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{secs[k]:.4f}", "-i", fn]
    parts = []
    for k in range(n):
        d = secs[k]
        if k % 2 == 0:                          # ease in:  1.015x -> 1.10x
            zexpr = f"1.015+0.085*t/{d:.4f}"
        else:                                    # ease out: 1.10x -> 1.015x
            zexpr = f"1.10-0.085*t/{d:.4f}"
        # NB: no setpts here — it strips the frame-rate metadata that xfade
        # requires (it then rejects the stream as "1/0, not constant").
        parts.append(
            f"[{k}:v]scale=w='ceil(1080*({zexpr})/2)*2':"
            f"h='ceil(1920*({zexpr})/2)*2':eval=frame:flags=bicubic,"
            f"crop=1080:1920,setsar=1,fps={FPS},format=yuv420p[v{k}]")
    if n == 1:
        chain = "v0"
    else:
        prev, run = "v0", secs[0]
        for k in range(1, n):
            label = "vout" if k == n - 1 else f"x{k}"
            trans = TRANSITIONS[(k - 1) % len(TRANSITIONS)]
            parts.append(f"[{prev}][v{k}]xfade=transition={trans}:"
                         f"duration={XFADE}:offset={run - XFADE:.4f}[{label}]")
            run += secs[k] - XFADE
            prev = label
        chain = "vout"
    cmd = [FF, "-y"] + inputs + [
        "-filter_complex", ";".join(parts), "-map", f"[{chain}]",
        "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", os.path.abspath(out)]
    return cmd


def make_video(post, folder):
    frames_dir = os.path.join(folder, "frames")
    os.makedirs(frames_dir, exist_ok=True)
    fnames, durs = _render_frames(post, frames_dir)
    out = os.path.join(folder, "video.mp4")
    build = _encode_motion if post.get("platform") == "tiktok" else _encode_static
    cmd = build(post, frames_dir, fnames, durs, out)
    r = subprocess.run(cmd, cwd=frames_dir, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("ffmpeg failed for %s: %s" % (post["post_id"], r.stderr[-500:]))
    shutil.rmtree(frames_dir, ignore_errors=True)   # keep only the finished mp4
    return "video.mp4", []

def write_caption(post, folder, assets, primary):
    lines = [
        f"POST ID   : {post['post_id']}",
        f"PLATFORM  : {post['platform_label']}",
        f"PUBLISH   : {post['datetime']}  ({post['weekday']})",
        f"FORMAT    : {post['format']}",
        f"PILLAR    : {post['pillar']}   (theme {post['theme_id']} · {post['theme_title']})",
        f"PRIMARY   : {primary}",
        f"ASSETS    : {', '.join(assets)}",
    ]
    if post.get("board"):
        lines.append(f"BOARD     : {post['board']}   <- pin to this Pinterest board")
    if post.get("title"):
        lines.append(f"TITLE     : {post['title']}")
    if post.get("sound"):
        lines.append(f"SOUND     : {post['sound']}")
    lines += ["", "-" * 60, "CAPTION (copy below):", "-" * 60, "", post["caption"], ""]
    with open(os.path.join(folder, "caption.txt"), "w") as f:
        f.write("\n".join(lines))

def main(render_assets=True):
    if render_assets and os.path.isdir(OUT):
        for name in os.listdir(OUT):        # wipe generated content, keep README.md
            if name == "README.md":
                continue
            p = os.path.join(OUT, name)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    elif not os.path.isdir(OUT):
        os.makedirs(OUT, exist_ok=True)
    posts = build_all()
    rows = []
    per_plat = {}
    total_assets = 0
    for n, post in enumerate(posts, 1):
        folder = os.path.join(OUT, post["platform"], post["post_id"])
        os.makedirs(folder, exist_ok=True)
        if not render_assets:
            # captions-only refresh: reuse the assets already on disk
            if post["is_video"]:
                assets, primary = ["video.mp4"], "video.mp4"
            else:
                pngs = sorted(os.path.basename(x) for x in glob.glob(os.path.join(folder, "*.png")))
                assets = pngs
                primary = pngs[0] if pngs else "image.png"
        elif post["is_video"]:
            primary, extra = make_video(post, folder)
            assets = [primary] + extra
        else:
            names = render_slides(post, folder)
            assets = names
            primary = names[0]
        total_assets += len([a for a in assets if not a.startswith("frames/")])
        write_caption(post, folder, assets, primary)
        rel = os.path.relpath(folder, ROOT)
        row = {
            "post_id": post["post_id"], "date": post["date"], "time": post["time"],
            "tz": post["tz"], "weekday": post["weekday"], "platform": post["platform_label"],
            "pillar": post["pillar"], "theme_id": post["theme_id"], "format": post["format"],
            "board": post.get("board", ""),
            "is_video": "yes" if post["is_video"] else "no", "hook": post["hook"],
            "title": post.get("title", ""), "asset_folder": rel, "primary_asset": primary,
            "caption": post["caption"],
        }
        rows.append(row)
        per_plat.setdefault(post["platform"], []).append(row)
        if n % 50 == 0:
            print(f"  ...{n}/{len(posts)} posts rendered")

    rows.sort(key=lambda r: (r["date"], PLAT_ORDER.get(_pk(r["platform"]), 9), r["time"]))
    cols = ["post_id", "date", "time", "tz", "weekday", "platform", "pillar",
            "board", "theme_id", "format", "is_video", "hook", "title",
            "primary_asset", "asset_folder", "caption"]
    with open(os.path.join(OUT, "00_MASTER_SCHEDULE.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    bp = os.path.join(OUT, "by_platform"); os.makedirs(bp, exist_ok=True)
    for plat, rws in per_plat.items():
        with open(os.path.join(bp, f"{plat}.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rws)
    # Pinterest broken down by board (one CSV per board) + a board index
    pins = per_plat.get("pinterest", [])
    if pins:
        bb = os.path.join(OUT, "pinterest", "by_board"); os.makedirs(bb, exist_ok=True)
        boards = {}
        for r in pins:
            boards.setdefault(r["board"], []).append(r)
        idx = []
        for board, rws in sorted(boards.items()):
            slug = board.lower().replace(" & ", "-and-").replace(" ", "-")
            with open(os.path.join(bb, f"{slug}.csv"), "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rws)
            idx.append(f"{board}  ->  {len(rws)} pins  ->  by_board/{slug}.csv")
        with open(os.path.join(bb, "_BOARDS.txt"), "w") as f:
            f.write("PINTEREST BOARDS — create these boards, then upload each pin to its board.\n\n"
                    + "\n".join(sorted(idx)) + "\n")
    manifest = dict(total_posts=len(posts), total_image_assets=total_assets,
                    videos=sum(1 for p in posts if p["is_video"]),
                    platforms=list(per_plat.keys()))
    json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=2)
    print("DONE:", manifest)

def _pk(label):
    for k, v in {"Instagram (+Facebook link)": "instagram", "Facebook": "facebook",
                 "X / Twitter": "x", "LinkedIn": "linkedin", "YouTube Shorts": "youtube",
                 "TikTok": "tiktok", "Pinterest": "pinterest"}.items():
        if label == k:
            return v
    return label

if __name__ == "__main__":
    main(render_assets="--captions-only" not in sys.argv)
