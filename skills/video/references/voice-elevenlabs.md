# Voice with ElevenLabs

## The key

- Stored in the OS keychain or a secrets manager, read at run time, **never printed, logged,
  written to a file or pasted in a prompt**.
- macOS: `security add-generic-password -s elevenlabs -a "$USER" -w` (prompts for the value), read
  with `security find-generic-password -s elevenlabs -w`. Elsewhere: an environment variable
  (`ELEVENLABS_API_KEY`) injected by the secrets manager. `scripts/voice.py` tries both.
- A paid plan is required for library voices and commercial use.

## Settings that worked (an example, not a rule)

| Setting | Value | Note |
|---|---|---|
| Endpoint | `POST /v1/text-to-speech/{voice_id}/with-timestamps` | Returns audio + per-character timings |
| Model | `eleven_v4` | Expressive, understands tone tags |
| `stability` | ≈ 0.38 | Lower = livelier, more variation between takes |
| `similarity_boost` | ≈ 0.85 | |
| `language_code` | the script's language | |
| Output | `mp3_44100_192` | |
| Voice | a male French voice from the library | Choose by listening to 2–4 candidates on the same sentence |

- `eleven_v4` **ignores the speed setting**: set the pace in the cut (pauses, `atempo` ≈ 1.05),
  not at generation.
- **Tone tags** in English between brackets: `[excited]`, `[annoyed]`, `[surprised]`,
  `[playfully]`, `[cheerfully]`, `[laughing]`. They are not read aloud (they take < 0.2 s in the
  alignment) — drop them from the word list.

## Pace and length

Measured on this setup: **≈ 18.5 characters per second ≈ 3 words per second**, cut pauses
included. Estimate the duration from the script before generating; a 140-word short lands
around 44 s, which is already too long for a short.

## Takes

- **2 takes** per script (or per chapter), same settings; pick by ear. Three takes for a hero
  video.
- **Generate per chapter** in long form: when one chapter changes, regenerate only it.
- **Adding a sentence afterwards**: generate the sentence alone with `previous_text` and
  `next_text` to keep the intonation, then keep the take whose words-per-minute and loudness are
  closest to the main take.

## The transcription check

A synthetic voice sometimes says a different word. One take said "bought" (*acheté*) instead of
"thrown" (*jeté*) — and nobody had listened yet.

```bash
python3 scripts/voice_check.py voice/take-1.mp3 SCRIPT.txt --lang fr
```

- Transcribes the take (whisper) and diffs it against the script, ignoring tone tags,
  punctuation and case. Numbers written in words vs digits and close homophones are flagged as
  "to check", real word changes as errors (exit code 1).
- **Whisper errs too.** On a full 45 s take it once skipped a whole clause and wrote "974" for
  "774"; transcribing that passage alone gave the exact text. Before regenerating, cut the
  passage (times from the alignment) and transcribe it alone:
  `ffmpeg -ss 25.9 -to 31.3 -i take.mp3 -ar 16000 -ac 1 seg.wav`. The check also catches a stale
  take generated before the last script edit.
- A clean check is **not** a listening. Say explicitly to the decider that the transcription
  matched but **a human must listen** to the takes — especially to every passage regenerated
  after a change.

## Cutting the voice

1. Word timings come from the alignment (characters grouped into words on spaces; tone tags removed).
2. Pauses go into the middle of measured silences before the chosen words.
3. Add a tail (≈ 2.5–3.5 s) for the end card.
4. Recompute every word timing on the cut voice (`onsets.json`) — everything else hangs on it.
5. Long form: concatenate chapters with a fixed gap and store each chapter's start
   (`scripts/words.py voice/ch*-alignment.json --gap 0.8`).
