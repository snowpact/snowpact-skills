# Motion design with HyperFrames

HyperFrames renders HTML + GSAP compositions to MP4. Its own skills hold the engine contract: load
`hyperframes:hyperframes` (router), `hyperframes:hyperframes-core`, `hyperframes:hyperframes-animation`,
and `hyperframes:hyperframes-cli` for commands. This page only adds what we learned on top.

## Engine hygiene

- Pin the HyperFrames version in the project (`package.json` + lockfile); call the local CLI
  (`npx hyperframes …` from the project), never `@latest`.
- Disable telemetry for every command:
  `HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 npx hyperframes render …`
  (also `HYPERFRAMES_NO_UPDATE_CHECK=1`).
- Don't run commands that send data out (`feedback`, `publish`, `cloud`, `auth`…) unless the user
  asks for that exact command.

## Project layout (one template, one data file per video)

```
<series>-kit/
  template/compositions/film.html   the composition: reads window.EPISODE + window.ONSETS
  template/timeline.js              episode + word timings → dated shots, overlays, sound events
  scripts/                          voice, cut, build (mix + render + contact sheet)
<series>-01-<slug>/
  SCRIPT.txt   episode.json   assets/img/   voice/   onsets.json   renders/   snapshots/
```

- **No time is typed by hand.** `episode.json` says *what* happens and *on which words*;
  `timeline.js` computes *when* from the voice timings.
- **The same `timeline.js` runs in the browser (animation) and in Node (audio mix)**, so a sound
  effect can never drift from its animation. Wrap it as UMD (`module.exports` or `window.Timeline`).
- A shot lasts until the next one starts; the last one is stretched to fit the end card.
- **The end card guarantees its own length**: `duration = max(voiceDuration, endCardStart + 3.4)`.
  If the voice finishes early, the logo still holds ≥ 2.5 s.
- **Only one root composition** in the project folder (two give "multiple root compositions" and a
  doubled audio track): archive old versions outside the root.

## Word cues

Every event is anchored to a word of the voice, never to an absolute time: after a new voice cut,
absolute times show the wrong screen on the sentence.

- **Avoid `word#N` (n-th occurrence).** It looks precise but any text change shifts the count: a
  short got its end sequence started too early because one extra "a" earlier in the script moved
  "a#5". If you must use it, generate it from a phrase (see `scripts/words.py --cues`).
- **Prefer phrase cues searched in order**: a shot searches its phrase after the previous shot,
  an overlay after the start of its shot (`"at": "flat tyre"`). Ambiguity disappears and the data
  stays readable.
- **A missing cue must stop the build** with the faulty phrase — never fall back silently.
- **After any change of text, re-check every cue** (`scripts/words.py … --cues cues.txt` lists
  missing and ambiguous ones), then look at the contact sheet around each moved cue.
- Lead times: overlays appear ≈ 0.08 s before their word, shots change ≈ 0.15 s before.

## Layout traps

- **Two overlays at the same y**: a label that wraps to two lines covers the one below. Give each
  overlay a `lines` count or measure the box, and check the contact sheet at the moment both are
  visible.
- **Photos never scaled beyond native resolution** — they blur. Use a rounded card at native size,
  or crop, but don't upscale. Check `width × scale ≤ naturalWidth`.
- **Subtitles never over a figure, a face, or a dark photo**: switch them off on shots carrying a
  giant word, or move them.
- Safe zones (9:16): nothing important above y = 220 or below y ≈ 1540, 60 px on the sides.
- Text is added in HTML, never baked into generated images.

## GSAP and engine pitfalls

| Pitfall | Effect | Fix |
|---|---|---|
| `fromTo` shows its start state from t = 0 | Ghost dots/frames on the whole video | `immediateRender: false` in the **second** (to) object |
| The engine rewrites `visibility` on `.clip` elements when seeking | A hidden element comes back | Hide with `display:none` or opacity |
| Overriding `document.getElementById` in one shot | Every later shot crashes ("Maximum call stack size exceeded") | Never monkey-patch globals |
| Timing data inlined in the page from an older voice cut | Page crashes, contact sheet comes out blank | Regenerate the inlined data after every new voice cut; run headless and read the errors |
| Engine re-captures a doubtful frame during render | A short glitch at that moment | Look at that passage in the render, not only in the preview |
| `letterSpacing` animations | Jittery text | Animate split letters instead |

## Audio mix (ffmpeg)

- Voice: cut pauses **in the middle of measured silences** (`silencedetect=n=-35dB:d=0.08`),
  never on a word attack, 5 ms fades at each join. A pause placed from the alignment alone bit the
  start of the next word.
- Speeding up a take ≈ 1.05× with `atempo` keeps the pitch; divide word timings by the same factor.
- Music: a CC0 track, ≈ −22 dB under the voice, 1 s fade in, 2.5 s fade out.
- Sound effects on gestures only (pop, whoosh, click, cash register), ≈ −12 to −24 dB, 10–20 per
  minute at most.
- Final: `loudnorm=I=-16:TP=-1.5:LRA=11`, then measure with `ebur128` (−16 LUFS, peak < −1.5 dBTP).

## Build script shape

```
1. read episode.json + onsets.json → timeline.build() (throws on a missing cue)
2. write sfx-events.json, mix voice + music + effects (amix normalize=0, then loudnorm)
3. write index.html with the final duration
4. render (telemetry off) → renders/<name>.mp4
5. extract one frame per shot → snapshots/sheet.png
```

Keep a `--no-render` flag that checks cues and re-mixes only: it is the fast loop after a text change.
