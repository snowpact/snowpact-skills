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

### 2. Know the layout

The engine is [html-design-proto](https://github.com/snowpact/html-design-proto): it draws the
shell (tabs, narration, keyboard, browser and phone frames, CURRENT/NEW tags, batch colours) and
the slide blocks. You write the screens and the story, never the shell.

```
<prototypes root>/              e.g. docs/features/, docs/prototypes/
  _kit/                         shared by every prototype of the project
    app.css                     the app's look, reproduced once
    screens.js                  screens and data used by two prototypes or more
    assets.js                   const ASSETS = { logo: "data:image/png;base64,…" }
  <topic>/
    prototype.scenario.js       screens specific to this prototype + DesignProto.init({...})
    prototype.html              GENERATED — never edit it
    <topic>.md                  the scoping note
```

**Find the prototypes root first:**

```bash
find . -type d -name _kit -not -path '*/node_modules/*' -not -path '*/.git/*'
```

- **A `_kit/` exists**: its parent is the root. Don't ask, put the new prototype next to the others.
  Read `screens.js` to see what you can reuse, and only the parts of `app.css` you need. Don't
  open `assets.js` (it's all base64): grep its keys.
- **No `_kit/` yet**: ask the user where prototypes should live, in one question. Offer the folder
  where the project already keeps its specs or epics if there is one (`docs/features/`,
  `docs/specs/`, `specs/`…), and `docs/prototypes/` as the default. If they don't answer or you
  can't ask, use `docs/prototypes/`. Then create the kit there: `app.css` from the app's real
  tokens and components (colours, fonts, radii, spacing — never redraw the app from memory), and
  `assets.js` with the logos and photos you need. Leave `screens.js` empty: screens stay in the
  scenario until a **second** prototype needs one, then move it to `screens.js`.

The build finds `_kit/` by walking up from the scenario, so the kit must sit at the root, above
every `<topic>/` folder.

### 3. Write the scenario

```js
DesignProto.init({
  lang: "fr",                                   // or "en": built-in labels
  title: "Signaleo — la mairie informe",
  url: "app.example.com",
  links: [{ label: "Le cadrage", href: "<topic>.md" }],
  lots: [{ id: 1, label: "suivre" }, { id: 2, label: "notifications" }, { id: "later", label: "Plus tard" }],
  scenarios: [
    { tab: "Le problème", steps: [
      { kicker: "Le problème", title: "…", text: "Two sentences.", slide: () => DesignProto.board(title, lead,
          DesignProto.flow([{ title, text, kind: "ko" }]), DesignProto.cards([{ title, tag, items, win }])) },
    ] },
    { tab: "L'application", persona: { name: "Léa Fontaine", role: "habitante", color: "#d1345b" }, steps: [
      { kicker: "Aujourd'hui", title: "…", text: "…", tag: "now", phones: [homeScreen()] },
      { kicker: "Lot 1", lot: 1, title: "…", text: "…", tag: "new",
        phones: [{ html: homeScreen(), tag: "now", caption: "Avant" }, { html: homeScreen({ follow: true }), tag: "new", highlight: true, lot: 1 }],
        phonesOptions: { arrows: true } },
      { kicker: "Lot 1", lot: 1, title: "…", text: "…", tag: "new", url: "back-office.example.com/issues", screen: () => boIssue() },
    ] },
    { tab: "Les décisions", steps: [ { kicker: "Décisions", title: "…", text: "…", slide: () => DesignProto.board(…,
        DesignProto.cards([{ title, tag: DesignProto.yes("reco"), pros: [], cons: [], win: true }]), DesignProto.verdict("…")) } ] },
  ],
});
```

- A step shows **one** of: `screen` (browser window, HTML or function), `phones` (1 to 4 phones in
  the window), `slide` (full page). `tag: "now" | "new"` labels the window; `lot` colours the kicker.
- A phone is an HTML string or `{ html, tabBar, device: "ios" | "android", time, dark, bg, caption,
  tag, highlight, lot, scale }`.
- Slide blocks: `board`, `flow`, `cards` (pros/cons, `win` = recommended), `table`, `verdict`,
  `lots`, and the pills `state("ok" | "todo" | "warn", label)`, `yes`, `no`, `mark()`, `lotChip(id)`.
  Mix them with your own HTML when a slide needs something else.
- Inside your screens, mark new parts with the `dp-new` class (dashed outline in the batch colour)
  and `DesignProto.mark()` (NEW pill). Engine classes all start with `dp-`: never reuse that prefix
  in `app.css`.
- Screens are plain functions returning HTML strings: `const issueCard = (o = {}) => \`…\``.
  Wrap human text in backticks (apostrophes are everywhere in French).

### 4. Build

```bash
npx -y github:snowpact/html-design-proto build <prototypes root>/<topic>/prototype.scenario.js
```

It finds `_kit/`, inlines it with the scenario into one standalone `prototype.html`, loads the
engine from jsDelivr pinned to a version, and fails on any syntax error. Never edit the HTML:
edit the sources and build again.

### 5. Check it in a browser

Open the file, go through **every** step of every tab, check that none is empty and the console is
clean, then take 3–4 representative screenshots. `#2.3` in the URL opens scenario 3, step 4.

```js
// in the page: walk every step
for (let sc = 0; sc < N; sc++) for (let st = 0; st < steps[sc]; st++) { DesignProto.goTo(sc, st); /* check .dp-window */ }
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

1. `<prototypes root>/<topic>/prototype.scenario.js` and the generated `prototype.html` — the
   presentation (plus any screen moved into `_kit/screens.js`).
2. `<prototypes root>/<topic>/<topic>.md` — the scoping note: numbered decisions (`D1`, `D2`…), impacts
   (`I1`, `I2`…) with where they live in the code, a plan split into batches, open questions.
   The HTML shows, the `.md` decides and gets quoted in meetings.

The two mirror each other: every NEW step in the HTML maps to a batch in the `.md`.

## Pitfalls we hit

- **A tooltip inside a scrolling container gets clipped**: open it downwards, not upwards.
- **Mermaid from a CDN is fragile**: for a simple diagram, use `DesignProto.flow` or HTML/CSS,
  which always renders and matches the app's look.
- **A disabled button with a tooltip** is a bad pattern: prefer an active button that opens an
  empty state explaining what to do.
- **Screens built before `init()` are fine**, but don't read `DesignProto.position` there: it
  only exists once the page renders.
