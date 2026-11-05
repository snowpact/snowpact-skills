# QA checklist

Run it yourself before every gate. Show the decider what you checked and what you could not.

## Before showing the script

- [ ] Every figure is in `FACTS.md` with a source and a PUBLISHED / CALCULATION / ASSUMED tag.
- [ ] No ASSUMED value stated as a fact; nothing invented "for illustration".
- [ ] Comparisons say what each side covers.
- [ ] The project's ethics rules hold (third parties, client figures, politics, fictional character disclaimer).
- [ ] Exact search term present at the key moments; word count and estimated duration given.

## After the voice

- [ ] `voice_check.py` clean on the chosen take (or every difference explained).
- [ ] The decider is told that a human must listen, and to which passages (all regenerated ones).
- [ ] Every cue resolves (`words.py … --cues`), none ambiguous, after **every** text change.
- [ ] Duration measured with ffprobe, not estimated.

## Contact sheet (before rendering)

- [ ] One or two key frames per shot, with subtitles, from the assembled composition.
- [ ] No overlay covering another (two-line labels at the same y).
- [ ] No subtitle over a figure, a face or a dark photo; everything inside the safe zones.
- [ ] No photo upscaled beyond its native resolution.
- [ ] Text not cut by the frame; no ghost element from t = 0.

## The render

- [ ] Frames at **0 s, middle and last frame** extracted from the MP4 (the render can differ from
      the preview): `scripts/contact_sheet.py renders/x.mp4 --at 0,mid,end`.
- [ ] First frame = the hook (no logo); last frame = the logo, held ≥ 2.5 s (short form).
- [ ] The end sequence starts on the right word (cue drift is the classic bug).
- [ ] `ffprobe`: resolution, fps, duration, codec as expected for the destination.
- [ ] `ebur128`: ≈ −16 LUFS integrated, peak below −1.5 dBTP. Listened to once, fully.
- [ ] Jump scan where shots should flow: `select='gt(scene,0.3)'` — a clean join measured ≤ 0.04,
      a real jump ≈ 0.22.
- [ ] Look at any passage the engine reported re-capturing.

## After a correction

- [ ] Search every file for the old figure or wording (script, episode data, captions,
      description, thumbnail): `grep -rn "<old>" .`.
- [ ] Chapters re-measured if the voice changed (long form).
- [ ] The previous validated version backed up (`.before-<change>`), not overwritten.

## Before publishing

- [ ] The media hosted for the scheduler is byte-identical to the validated render
      (`cmp` or `shasum -a 256` on the downloaded copy).
- [ ] Captions per network within their limits; no `<` `>` in the YouTube description.
- [ ] Everything created as a draft; nothing goes live without explicit approval.

## The message to the decider

- What changed, what was measured, what is assumed.
- What is staged (fictional data, fictional character, simulated screens).
- Images in the message itself, then one clear question: validate, adjust, or choose.
