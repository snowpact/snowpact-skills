#!/usr/bin/env python3
"""Contact sheet of a rendered video, plus its measured format.

    python3 contact_sheet.py renders/film.mp4                    # 12 evenly spaced frames
    python3 contact_sheet.py renders/film.mp4 --at 0,mid,end     # first / middle / last frame
    python3 contact_sheet.py renders/film.mp4 --at 1.2,8.5,30 --loudness

Writes <video>-sheet.png next to the video (or -o). Frames are read from the render, not the preview.
Prints duration, resolution and fps (ffprobe), and with --loudness the integrated loudness (ebur128).
"""
import argparse, json, pathlib, subprocess, sys, tempfile


def probe(video):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate:format=duration", "-of", "json", str(video)],
                         capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    s = j["streams"][0]
    return float(j["format"]["duration"]), s["width"], s["height"], s["r_frame_rate"]


def times(spec, count, duration):
    if not spec:
        return [round(duration * (i + 0.5) / count, 2) for i in range(count)]
    last = max(0.0, duration - 0.05)
    named = {"mid": duration / 2, "end": last}
    return [round(min(last, named[x] if x in named else float(x)), 2) for x in spec.split(",")]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("video", type=pathlib.Path)
    p.add_argument("--at", help="comma-separated seconds, or 0 / mid / end")
    p.add_argument("--count", type=int, default=12, help="evenly spaced frames when --at is not given")
    p.add_argument("--cols", type=int, default=6)
    p.add_argument("--width", type=int, default=270, help="width of each thumbnail")
    p.add_argument("--loudness", action="store_true")
    p.add_argument("-o", "--out", type=pathlib.Path)
    a = p.parse_args()
    duration, w, h, fps = probe(a.video)
    print(f"{a.video.name}: {duration:.2f} s, {w}x{h}, {fps} fps")
    ts = times(a.at, a.count, duration)
    out = a.out or a.video.with_name(a.video.stem + "-sheet.png")
    th = round(a.width * h / w / 2) * 2
    with tempfile.TemporaryDirectory() as tmp:
        frames = []
        for i, t in enumerate(ts):
            f = pathlib.Path(tmp) / f"{i:03}.png"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(a.video), "-frames:v", "1",
                            "-vf", f"scale={a.width}:{th}", str(f)], check=True)
            frames.append(f)
        cols = min(a.cols, len(frames))
        layout = "|".join(f"{(i % cols) * a.width}_{(i // cols) * th}" for i in range(len(frames)))
        inputs = sum([["-i", str(f)] for f in frames], [])
        graph = f"xstack=inputs={len(frames)}:layout={layout}:fill=white" if len(frames) > 1 else "null"
        subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", graph, str(out)], check=True)
    print(f"{out}: frames at {ts} s (left to right, top to bottom)")
    if a.loudness:
        err = subprocess.run(["ffmpeg", "-v", "info", "-i", str(a.video), "-af", "ebur128=peak=true", "-f", "null", "-"],
                             capture_output=True, text=True).stderr
        summary = err.split("Summary:")[-1]
        lufs = summary.split("I:")[1].split("LUFS")[0].strip() if "I:" in summary else "?"
        peak = summary.split("Peak:")[1].split("dBFS")[0].strip() if "Peak:" in summary else "?"
        print(f"loudness: {lufs} LUFS integrated, true peak {peak} dBTP")


if __name__ == "__main__":
    sys.exit(main())
