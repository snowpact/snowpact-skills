# Editorial: facts, wording, ethics

The quality of a video that explains something is the quality of its facts. Viewers forgive a
plain animation; they do not forgive a wrong number, and one wrong number discredits the rest.

## The brief (step 0)

`BRIEF.md`, half a page:

- **Audience** — one video per audience (residents, customers, prospects, the team).
- **Goal and call to action** — "download the app", "book a demo", "subscribe".
- **Format and length** — see the table in [SKILL.md](../SKILL.md#format-at-a-glance).
- **Tone** — informal or formal address, serious or playful.
- **Channels** — YouTube, Shorts, Reels, TikTok, LinkedIn, website, app store.
- **Ethics rules** of the project (examples below), written once, checked on every script.

### Ethics parameters (examples to adapt)

- Never name a third party (a town, a company, a person) in a negative light; say "a town".
- No figures that shame the people you work with (e.g. non-response rates of your own clients).
- No political party, no candidate.
- Fictional characters are introduced as examples ("Léa is an example", small text on screen).
- Sensitive topics are shown by a symbol, never by a victim.
- Real photos only with the right to reuse them (check the terms of the source).

## The facts file (step 1)

Before writing a single line, list every figure the script might use in `FACTS.md`:

| Claim | Value | Tag | Source (URL, body, document, date) | What it counts exactly |
|---|---|---|---|---|

- **PUBLISHED** — read in the cited document, by you, today.
- **CALCULATION** — your own arithmetic on published figures; write the operation.
- **ASSUMED** — a hypothesis with no source. It may shape the story ("the size of a plate") but is
  never stated as a fact, and never carries a precise number.

Rules learned the hard way:

- **Ask "what does this number count exactly?"** A "97 out of 99" was a processing rate, not an
  accuracy rate. A price per m² was what a town bills utility companies for a full reconstruction,
  not the cost of filling a pothole.
- **Open the primary source.** A press article or a search summary is a lead, not a source. When
  the PDF returns 403, say so in the facts file and do not use the figure.
- **When two sources disagree, write both** with their scope and year, and decide with the
  decider which one to use. Never average them.
- **What cannot be sourced is not said.** No growth speed for a pothole exists anywhere: the
  script says "later", "after a few weeks of rain and frost", never "on day 10".
- **Compare comparable things, and say what each side covers.** "€20 of material on day one" vs
  "€774 for the full repair" is honest only if the text says "of material".
- **Keep national averages national.** Don't turn an average into a claim about one place.
- **After a correction, search every file for the old figure** (script, captions, episode data,
  thumbnail, description): `grep -rn "79 €\|236\|786" .`.

## Writing the script (step 2)

- **One idea per sentence, one image per sentence.**
- **Hook on a lived scene or a question, never on a slogan.** For long form, the viewer's own
  question is the very first sentence.
- **Exact terms at the key moments**: use the precise word (e.g. "pothole", in French
  "nid-de-poule") where it matters and in the title, tags and description, because that is what
  people search. The familiar word ("a hole in the road") is fine in the hook.
- **A topic that annoys people beats a topic that is merely useful.** Money people pay and see
  wasted holds attention; a neutral explanation plateaus.
- **Real labels**: names of screens and buttons copied from the real product.
- **Numbers written in words** for the voice ("one thousand six hundred and eighty-five"), digits
  on screen. Keep a digits version for captions.
- **Estimate the length before showing it**: ≈ 18.5 characters per second, ≈ 3 words per second
  (measured with a French synthetic voice, pauses included). 30 s ≈ 65–90 words.
- **Show the full text to the decider before generating any voice.** Present it as a multiple
  choice (keep / adjust / alternative) with the measured word count and estimated duration.

## Sources on screen

- One small source line under each figure while it is on screen ("Body, document, year").
- Calculations say so: "calculation from <body> 2024".
- Fictional character disclaimer during the intro.
- The description repeats the sources with their URLs.
