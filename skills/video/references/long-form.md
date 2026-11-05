# Long form: YouTube explainers (16:9)

1920 × 1080, ≈ 4 minutes, chapters.

## Why viewers leave, and the fix

The first long pilot stacked figures with no thread: viewers dropped off. What fixed it:

- **A recurring fictional character** with a concrete problem ("Léa blew a tyre in a pothole in
  front of her house"). Introduced as an example on screen. People follow a person, not a budget.
- **The viewer's question as the very first sentence** ("With all the taxes we pay, why does
  nobody fill this hole?"). The first draft took 20 s to get to the point.
- **A permanent visual landmark**: a metro line of 5 stations across the top of the screen, a dot
  that moves to the next station at each chapter. The viewer always knows where they are and how
  much is left.
- **One strong figure per station**, not five.
- **Each chapter ends on the question that opens the next** ("So where does this money go?").
- **A recap** that replays the whole line in four sentences before the CTA.

Other mechanics that hold attention on comparable channels (read from their intros, not from
retention data, which is not public): a question title with a counter-intuitive answer, following
something step by step where each step is an obstacle, a numeric paradox, a promise repeated at the
end. A topic that makes people grumble (their money, their taxes) beats a merely useful one.

## Production

- **Voice per chapter** (`voice/ch0.txt` … `ch6.txt`): when a chapter changes, regenerate only it.
  Concatenate with a fixed gap (≈ 0.8 s) and keep the start time of each chapter in the timings.
- **Cues are phrases searched in order** (a shot searches after the previous shot), not
  `word#N`: see [motion](motion-hyperframes.md#word-cues).
- **Illustrations** carry the character; real photos carry the proof. See
  [illustrations](illustrations-codex.md).
- **Thumbnail as a separate HTML page** rendered to 1280 × 720 PNG: the character, one figure,
  three words max.

## YouTube metadata

- **Title**: the character + the question, with the exact search term ("pothole").
- **Chapters**: `0:00 Title` lines in the description. **Re-measure them after every voice change**
  from the new chapter start times; never reuse old timestamps.
- **No `<` or `>` in a YouTube description** (rejected): write "less than", "more than".
- Sources with URLs at the end of the description.
- Tags: the exact terms people search, not the internal jargon.

## Recycling

Each station is a short: one figure, one question, the same character. A long video of 5 stations
gives 5 shorts that point back to it.
