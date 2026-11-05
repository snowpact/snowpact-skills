# Publishing with Metricool (optional)

Metricool schedules one post to several networks (YouTube, TikTok, Instagram, Facebook, Threads,
LinkedIn…). Through its MCP server an agent can create posts. These are the traps we met.

## Rules

- **Create as a draft (or "for review"), never as a live scheduled post**, then let the decider
  validate in Metricool. Publication is an outward write: explicit approval each time.
- **The media must be a public URL.** A Google Drive "anyone with the link can view" URL works:
  Metricool downloads and re-hosts it. After creation, download the re-hosted copy and compare it
  byte for byte with the validated render.
- **Free plan quota**: one multi-network post counts as 1. Group networks in one post.

## Per-network limits

| Network | Trap |
|---|---|
| Threads | 500 characters max: write a shorter variant |
| TikTok | A title is mandatory |
| YouTube | No separate description field: the main text is used everywhere, so write it to work as a YouTube description too (no `<` `>`) |
| LinkedIn | Rewrite the caption for a professional audience instead of reusing the consumer one |

## API traps

- `updateScheduledPost` needs the **full post object**, not a patch, and **returns a new id**:
  re-read the post after any update and keep the new id.
- "Best time to post" suggestions are generic until the account has history; don't present them
  as measured.

## Rhythm

Regularity beats volume: 4 posts a week held over time is better than a burst. Plan a batch of
episodes in advance (validated, rendered, drafted) rather than producing the day before.
