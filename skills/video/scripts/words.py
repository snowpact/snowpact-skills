#!/usr/bin/env python3
"""Turn ElevenLabs alignments into timed words, and check phrase cues against them.

    python3 words.py voice/SCRIPT-take1-alignment.json --tail 3 -o onsets.json
    python3 words.py voice/ch0-alignment.json voice/ch1-alignment.json --gap 0.8 -o onsets.json
    python3 words.py onsets.json --cues cues.txt      # re-run after ANY change of text

Output: {"duration", "chapters": [start of each input], "words": [{"w", "s", "e"}]}; tone tags dropped.
Several alignments are laid end to end with --gap seconds between them (each input's length is
its sibling .mp3, measured with ffprobe, when present): mix the audio with the same offsets. Timings are for the raw takes; if you cut pauses or change
the tempo afterwards, recompute them on the cut voice.
--cues: one phrase per line, in order of appearance. Each is searched after the previous match;
a missing phrase is an error (exit 1), a phrase that also occurs elsewhere is flagged, and the
equivalent "word#N" is printed for templates that still use occurrence cues.
"""
import argparse, json, pathlib, re, subprocess, sys


def norm(w):
    return re.sub(r"[.,;:!?…«»\"()“”]", "", w.lower().replace("’", "'")).strip()


def from_alignment(a, offset):
    words, cur, in_tag = [], None, False
    for c, s, e in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
        if c == "[":
            in_tag = True
        if in_tag or c.isspace():
            if cur:
                words.append(cur)
            cur = None
            in_tag = in_tag and c != "]"
            continue
        if cur is None:
            cur = {"w": c, "s": s + offset, "e": e + offset}
        else:
            cur["w"] += c
            cur["e"] = e + offset
    if cur:
        words.append(cur)
    return [{"w": w["w"], "s": round(w["s"], 2), "e": round(w["e"], 2)} for w in words if norm(w["w"])]


def audio_length(alignment_path, a):
    # the next input starts after the audio itself, which runs a little past the last character
    mp3 = alignment_path.with_name(alignment_path.name.replace("-alignment.json", ".mp3"))
    if mp3.exists():
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)],
                             capture_output=True, text=True).stdout.strip()
        if out:
            return float(out)
    return a["character_end_times_seconds"][-1]


def build(alignments, gap, lead, tail, paths=None):
    words, chapters, t = [], [], lead
    for k, a in enumerate(alignments):
        chapters.append(round(t, 2))
        words += from_alignment(a, t)
        t += (audio_length(paths[k], a) if paths else a["character_end_times_seconds"][-1]) + gap
    return {"duration": round(t - gap + tail, 2), "chapters": chapters, "words": words}


def check_cues(words, phrases):
    tokens = [norm(w["w"]) for w in words]
    errors, pos = 0, 0
    for phrase in phrases:
        p = [norm(x) for x in phrase.split() if norm(x)]
        hits = [i for i in range(len(tokens) - len(p) + 1) if tokens[i:i + len(p)] == p]
        after = [i for i in hits if i >= pos]
        if not after:
            errors += 1
            print(f"MISSING  {phrase!r}" + (" (only before the previous cue)" if hits else ""))
            continue
        i = after[0]
        occurrence = tokens[:i + 1].count(p[0])
        note = f"  ({len(hits)} occurrences: keep searching in order)" if len(hits) > 1 else ""
        print(f"{words[i]['s']:7.2f}s  {phrase!r} = {p[0]}#{occurrence}{note}")
        pos = i + 1
    return errors


def self_test():
    chars = list("[excited] Un trou. Un [very calm] pneu")
    a = {"characters": chars, "character_start_times_seconds": [i * 0.1 for i in range(len(chars))],
         "character_end_times_seconds": [i * 0.1 + 0.1 for i in range(len(chars))]}
    w = from_alignment(a, 0)
    assert [x["w"] for x in w] == ["Un", "trou.", "Un", "pneu"], w
    out = build([a, a], gap=1.0, lead=0, tail=2)
    assert out["chapters"] == [0, 4.8] and len(out["words"]) == 8, out
    assert check_cues(out["words"], ["un pneu", "trou", "pneu"]) == 0  # in order: 2nd input's "trou" and "pneu"
    assert check_cues(out["words"], ["pneu", "trou", "absent"]) == 1
    print("self-test ok")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("inputs", nargs="*", type=pathlib.Path, help="alignment JSONs in order, or one onsets.json")
    p.add_argument("--gap", type=float, default=0.8, help="silence between inputs (s)")
    p.add_argument("--lead", type=float, default=0.0, help="silence before the first input (s)")
    p.add_argument("--tail", type=float, default=3.0, help="room for the end card (s)")
    p.add_argument("-o", "--out", type=pathlib.Path)
    p.add_argument("--cues", type=pathlib.Path, help="text file, one phrase per line, in order")
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        return self_test()
    if not a.inputs:
        p.error("give alignment files or an onsets.json")
    data = [json.loads(f.read_text()) for f in a.inputs]
    onsets = data[0] if "words" in data[0] else build(data, a.gap, a.lead, a.tail, a.inputs)
    if a.out:
        a.out.write_text(json.dumps(onsets, ensure_ascii=False))
        print(f"{a.out}: {len(onsets['words'])} words, {onsets['duration']} s, chapters at {onsets['chapters']}")
    if a.cues:
        phrases = [line.strip() for line in a.cues.read_text(encoding="utf-8").splitlines() if line.strip()]
        sys.exit(1 if check_cues(onsets["words"], phrases) else 0)


if __name__ == "__main__":
    main()
