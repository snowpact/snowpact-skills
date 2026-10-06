---
name: design-prototype
description: Use when a product decision has to be shown before it is built — "make a design prototype", "show the impact on the back office", "a before/after walkthrough", "a mockup so we can decide together". Builds ONE self-contained HTML file that replays the real app screens (problem → before/after → choices) so people can decide without reading a spec.
---

# Design prototype

A **clickable** presentation, in a single HTML file, whose job is to **settle a product decision**
before any code is written. It replays the app's **real screens**, in the order of a story, with
every change clearly marked.

## Why copy the real app

That's the whole point of the format, and it changes three things:

1. **People see the actual impact, not an idea.** "Add a field" becomes "this column, in this
   table, next to Permissions". People react to what they recognise.
2. **It forces you to read the code before proposing anything.** Rebuilding the screen shows what
   already exists, what can be reused, and the traps (a dead button with no service behind it, a
   warning that would silently disappear, two parallel implementations of the same action).
3. **The decision comes out ready to be split into work.** What is marked NEW on screen is exactly
   what has to be built; everything else is already there.

Generic wireframes, on the other hand, get people debating the drawing instead of the product.

## When not to use it

- A logic or data-model question → a throwaway terminal prototype is faster.
- Exploring several visual directions for a brand-new screen → a storyboard (`flowboard` skill)
  or quick UI variations.
- A short scoping note with no screens → a `.md` file is enough.

## The fixed outline

Always these three parts, in this order:

1. **The problem** — 1 or 2 slides. A plain explanation (short sentences, no technical jargon) plus
   **one diagram**: the current journey, or the usage modes side by side. Nobody should need prior
   context to follow.
2. **The journeys** — most of the steps. The real screens, **BEFORE then AFTER**, in the order of a
   story lived by a named person ("the secretary opens a report"). One tab per scenario / usage mode.
3. **The choices** — the last slides. For each open decision: the options, what each brings and
   costs, and the recommendation. This is the part you open in a meeting when someone says
   "why not do it this way instead…".

## Method

### 1. Ground it in the code (mandatory, before any mockup)

- Read the screens involved: pages, components, forms, dashboards.
- Pull the **real labels** from the app's translation files — never invent copy the app already has.
- Check what exists on the backend: routes, use cases, email templates, enums. Anything that
  already exists must **not** be presented as new.
- List reusable components: they're what makes the plan credible ("we reuse form X and drop one").

### 2. Start from the existing styles

Never redraw the application. If the project already has a design prototype, extract its
stylesheet and assets (logos, photos, maps as data URIs) and reuse them. Otherwise, copy the
app's design tokens (colours, fonts, radii, spacing) into the prototype's `<style>`.

```bash
# Example: extract the <style> block and the inlined assets line from an earlier prototype
python3 - <<'EOF'
lines = open('docs/features/previous-prototype.html', encoding='utf-8').read().split('\n')
end = next(i for i, l in enumerate(lines) if l.strip() == '</style>')
open('/tmp/parts_css.txt', 'w').write('\n'.join(lines[lines.index('<style>') + 1:end]))
open('/tmp/parts_assets.txt', 'w').write(
    next(l for l in lines if l.startswith('<script>const ASSETS'))[8:].replace('</script>', ''))
EOF
```

### 3. Assemble with a script, never by hand

With inlined assets the file easily reaches several hundred KB, so build it from parts — base CSS,
`extra.css` (presentation-only additions), assets, and the rendering JS. Check the JS **before**
assembling:

```bash
node --check /tmp/body.js
```

### 4. Layout

- **Top bar**: title + a PROTOTYPE pill + one tab per scenario (with its status: shipped, batch N,
  exists).
- **Stage**: a browser window (URL bar, traffic lights) or phone frames, with the app screen
  inside — or a full-page slide for the problem and the choices.
- **Bottom bar**: Previous / Next, the step title, two sentences of narration, progress dots.
  ← → keyboard arrows.
- **A label on every screen**: `CURRENT` (grey) or `NEW` (bright pink), top right of the window.
  It stops the "what are we looking at here?" question on every slide.
- Mark new **details** inside the screen too: a small "batch 2" pill next to the added field or
  column, a dashed pink outline around the new block.

### 5. Check it in a browser

Open the file, go through **every** step of every tab, check that none is empty and the console is
clean, then take 3–4 representative screenshots.

```js
for (let sc = 0; sc < N; sc++) { /* click the tab, then each dot, check .window is filled */ }
```

## Content rules

- **One idea per step.** If the narration needs three sentences, it's two steps.
- **Named characters** and a consistent fictional place (e.g. Claire, admin in a small town).
  People project themselves onto a person, not onto "the user".
- **The real labels**, including the ones we don't like — that's exactly what triggers
  "by the way, that word is confusing".
- **No invented screen without saying so.** A screen that doesn't exist yet carries the NEW label,
  full stop.
- **The choice slides read on their own**: options, pros, cons, recommendation. They'll be used
  without you in the room.
- Write in the language of the app and of the people who'll decide.

## Deliverables

1. `docs/features/<topic>.html` — the presentation.
2. `docs/features/<topic>.md` — the scoping note: numbered decisions (`D1`, `D2`…), impacts
   (`I1`, `I2`…) with where they live in the code, a plan split into batches, open questions.
   The HTML shows, the `.md` decides and gets quoted in meetings.

The two mirror each other: every NEW step in the HTML maps to a batch in the `.md`.

## Pitfalls we hit

- **Never nest `<script>` tags**: an extracted assets line may already contain its own tag — strip
  it before inserting.
- **Computing replacement offsets before injecting CSS** breaks the slicing: replace from the last
  position to the first, or re-read the file between passes.
- **`[hidden]` loses against a class that sets `display`**: add `[hidden] { display: none !important; }`.
- **A tooltip inside a scrolling container gets clipped**: open it downwards, not upwards.
- **Mermaid from a CDN doesn't work offline**: for a simple diagram, use HTML/CSS (chips + arrows),
  which always renders and matches the app's look.
- **A disabled button with a tooltip** is a bad pattern: prefer an active button that opens an
  empty state explaining what to do.
