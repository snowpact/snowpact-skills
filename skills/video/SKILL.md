---
name: video
description: Use when the user wants a video produced — a motion design short (vertical 9:16 for Shorts, Reels, TikTok), a long YouTube explainer (16:9), a product film, a series of episodes, a voice-over, or the illustrations for one. Triggers include "make a video", "motion design", "short", "reel", "tiktok", "youtube video", "explainer", "voice-over", "ElevenLabs", "subtitles", "thumbnail", "illustrations for the video", "a series of shorts". Drives the whole pipeline (framing → script → voice → contact sheet → render → publishing) with one validation gate per step, and builds on the HyperFrames skills for the rendering.
---

# Video

Produce a video an agent can stand behind: every claim sourced, every step approved by the person
who decides, every render checked frame by frame before anyone else sees it. It covers vertical
shorts (20–30 s) and long YouTube explainers (≈ 4 min), animated in HTML + GSAP and rendered with
[HyperFrames](https://hyperframes.heygen.com), voiced with ElevenLabs.

Everything here was learned on a real series (about thirty shorts and a long-form pilot for
Signaleo, a civic reporting app). The mistakes listed were made for real; the fixes are measured.

## When not to use it

- Editing existing footage or a talking head → the `hyperframes:talking-head-recut` skill.
- A video made from a pull request, a music track or a Remotion project → the matching
  `hyperframes:*` workflow skill.
- A one-off animation with no voice, no claim and no audience → `hyperframes:motion-graphics`.

## Prerequisites

- The HyperFrames skills (`npx skills add heygen-com/hyperframes`, or the `hyperframes` Claude Code
  plugin; skill names below drop the `hyperframes:` prefix when installed with `npx skills`).
  This skill decides *what* to make and *when it is good enough*; they know *how* the engine works. Load `hyperframes:hyperframes` (router), `hyperframes:hyperframes-core`
  (composition contract) and `hyperframes:hyperframes-animation` before writing a composition.
- Node 22+, ffmpeg/ffprobe, Python 3. Optional: whisper (whisper.cpp or `openai-whisper`) for the
  voice check, an image generator (Codex `image_gen`) for illustrations.
- An ElevenLabs account. The API key lives in the OS keychain or a secrets manager, never in a file,
  a prompt or the terminal output (see [voice](references/voice-elevenlabs.md)).

## The pipeline and its gates

One step at a time. **Never start a step on an assumption about the previous one**: going back
after a render costs ten times more than asking.

| # | Step | Deliverable | Gate (the decider approves) |
|---|---|---|---|
| 0 | Framing | `BRIEF.md`: audience, goal, call to action, format, length, tone, channels, ethics rules | Brief |
| 1 | Facts | `FACTS.md`: every figure with source URL, body, date, and a PUBLISHED / CALCULATION / ASSUMED tag | Facts, before any writing |
| 2 | Script | `SCRIPT.txt` (+ per-chapter files for long form), word count, estimated duration | **The text, shown in full, before any voice is generated** |
| 3 | Voice | 2 takes per script or chapter, transcription check, chosen take, cut voice + word timings | The take (a human listens) |
| 4 | Style | 3+ visual directions as short mock-ups (not one) | One direction |
| 5 | Contact sheet | One or two key frames per shot, with subtitles, from the real composition | The sheet |
| 6 | Render | MP4 + contact sheet of the render (0 s / middle / end) + measured duration and loudness | The video |
| 7 | Publishing | Title, description, tags, chapters, thumbnail, captions per network; drafts only | Every outward write |

Steps 4 and 5 can be skipped when the series already has a validated style and template: a new
episode then goes script → voice → render, with the contact sheet still checked by you.

## How to ask for a decision

- **Multiple choice**, 2–4 options, the recommended one first with its reason. The question must
  make sense on its own: put the context *inside* the question.
- **Images go in the message itself** (Markdown image with an absolute path, or a link), not only
  in a preview field of the question widget: deciders often never see those previews.
- Say what was **measured** and what is **assumed**, every time. Never present the second as the first.
- Before showing anything, **review it yourself** (frames, text cut off, overlaps, sound). A defect
  you catch costs nothing; one the decider catches costs their trust.

## Non-negotiable rules

1. **Every figure is sourced** — URL, organisation, date — and tagged PUBLISHED, CALCULATION or
   ASSUMED. ASSUMED never reaches the script as a fact.
2. **No invented "illustrative" example.** What you cannot source, you do not say: write "later"
   instead of "on day 10". (A made-up "3 m² pothole growing to 10 m² in 10 days" was spotted by a
   viewer; a real pothole is about 0.1 m² and no source gives a growth speed.)
3. **Read the primary source.** A "€79/m²" figure was in fact a rate billed to utility companies
   for full road reconstruction; the right figure was in the same document.
4. **Compare like with like, and say what each side covers** ("€20 of material" vs "€774 for the
   full repair, crew included").
5. **Ethics rules are written in the brief and checked on every script** — for example: never name
   a third party negatively, no figures that shame a client, fictional characters introduced as
   examples, no political party. They are parameters of the project, not of this skill.
6. **Show the script before generating the voice.** Re-check the word cues after *any* change of
   text (see [motion](references/motion-hyperframes.md#word-cues)).
7. **No secrets, no real personal data on screen**, no production capture with real users.
8. **Nothing leaves the machine without explicit approval**: no upload, no publication, no
   scheduled post outside drafts, no commit or push.
9. **Back up before overwriting** a validated file (`film.before-<change>.mp4`, `SCRIPT.before-<change>.txt`).

## Format at a glance

| | Short (9:16) | Long (16:9) |
|---|---|---|
| Length | 20–30 s (35–46 s retained less) | ≈ 4 min, chapters |
| Hook | First second, image AND voice, no logo before | The viewer's own question as the very first sentence |
| Spine | One idea | A recurring fictional character + a permanent visual landmark (e.g. a 5-station metro line) |
| End | Short spoken CTA naming the platforms + official store badges + logo held ≥ 2.5 s as the last frame | Recap, CTA, subscribe; each chapter ends on the question that opens the next |
| Details | [short-form](references/short-form.md) | [long-form](references/long-form.md) |

## Delegation

- Hand long renders, captures and illustration batches to background agents: **one task = one
  checkable deliverable** (a file and a contact sheet), with the brief, the paths and the checks
  to run written in the task.
- Each agent backs up before overwriting, and stops only the processes it started (note the PIDs;
  never `pkill -f` on a shared pattern).
- Re-check what an agent returns (frames, durations) before relaying it.

## References

- [references/editorial.md](references/editorial.md) — sourcing, the facts file, wording, exact terms, ethics parameters.
- [references/short-form.md](references/short-form.md) — hook, length, CTA, end card, subtitles, store badges, style choice.
- [references/long-form.md](references/long-form.md) — character, landmark, chapters, YouTube metadata, recycling into shorts.
- [references/motion-hyperframes.md](references/motion-hyperframes.md) — project layout, word-driven timeline, cue pitfalls, layout traps.
- [references/voice-elevenlabs.md](references/voice-elevenlabs.md) — key handling, settings, tone tags, pace, takes, transcription check.
- [references/illustrations-codex.md](references/illustrations-codex.md) — style sheet, character reference, prompt template, transparency checks.
- [references/qa-checklist.md](references/qa-checklist.md) — what to check before each gate and before sending.
- [references/publishing-metricool.md](references/publishing-metricool.md) — optional: scheduling with Metricool and its traps.

## Scripts

Small, dependency-free helpers (Python 3 + ffmpeg). Run with `--help`.

- `scripts/voice.py` — ElevenLabs takes with per-character timestamps; key from env or macOS keychain.
- `scripts/voice_check.py` — transcribes a take and diffs it against the script; exit 1 on a wrong word.
- `scripts/words.py` — turns one or more alignments into timed words, and checks a list of phrase cues.
- `scripts/contact_sheet.py` — grid of frames from a render (evenly spaced, or at given times) + duration.
