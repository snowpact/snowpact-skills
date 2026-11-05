# Illustrations with an image generator (Codex `image_gen`)

Illustrations carry a fictional character and the ideas a photo cannot show. They complement real
photos; on shorts, credibility comes from the real photos.

Measured on a real series: **6 generations for 4 accepted scenes** (reference sheet included),
then **19 generations for 14 more scenes** (5 rejected and redone). Budget ≈ 1.3–1.5 calls per
accepted image.

## The procedure

1. **Write `STYLE.md` first** (template below): technique, exact palette, light, framing,
   forbidden things, character identity.
2. **Generate the character reference sheet first**: front, three-quarter, profile and three
   expressions, on a transparent background. Get it validated. Never regenerate it between scenes.
3. **Attach the reference sheet to EVERY generation**, even for a building or an object without
   the character: it carries the style too. Never replace it with the last image produced —
   drift accumulates.
4. **A fixed prompt template**: only the `SCENE:` part changes.
5. **Native transparent background** (`transparent_background: true`). Check the PNG is really
   RGBA with zero alpha around the subject — not an RGB image with a painted checkerboard.
6. **Clean the alpha lightly**: zero only alpha ≤ 8/255, add a transparent margin; no chroma key,
   no blur, no dilated outline. Keep the raw original next to it.
7. **Check on a light AND a dark background**, at final size and at 100 %: hair, fingers, light
   shoes, gaps between arms and body, windows. Refuse halos, background crumbs, flat areas turned
   transparent, cropped edges.
8. **A series contact sheet** (all scenes in a grid) to check consistency: face, haircut, outfit,
   palette, texture.
9. **Correct with a targeted prompt**: attach the master sheet first and the faulty image second,
   and say only what to fix ("the scarf knot on her left side").
10. **Log every call** (prompt file, decision, reason). Keep rejects.

If the generator gives no alpha: ask for a flat background colour absent from the subject and key
out only the background connected to the edges, with edge decontamination. Never remove every pixel
of a colour close to the subject's clothes.

## Limits to tell the decider

- Faces vary slightly between scenes; it is not a rigged character.
- Hex colours are targets, not locks: light, grain and texture produce nuances. Use exact hex in
  the HTML/SVG layers.
- **No text in the image** (not even a sign): text is added in HTML.
- Sensitive subjects through a symbol.
- Fine texture disappears at small sizes; check at the size the video uses.
- **Usage limits can hit in the middle of a series.** Plan the batch, spread it, and plan a resume
  (the log says which scenes are done).

## `STYLE.md` template

```markdown
# <Character> — style sheet

## Technique
<e.g. retouched cut-paper editorial illustration, gouache volumes, fine paper grain inside the
shapes, thin slightly irregular navy outline, crisp cutout edges, no white sticker border>

## Light and framing
- Soft light from the upper left; cool shadows inside the shapes, no drop shadow around the cutout.
- Whole scene isolated, three-quarter view, moderate perspective, 6 % transparent margin (check it:
  the model doesn't always respect it).
- Source size <e.g. 1536 × 1024>; delivered with <n> px transparent margin, never upscaled.

## Palette (targets)
| Use | Hex |
|---|---|
| Background of the composition | #… |
| Text, outlines | #… |
| Main colour | #… |
| Accent (tiny touches only) | #… |
| Skin / hair | #… / #… |
| Neutral | #… |
| Dark control background | #… |

## Character identity
Fictional adult, age …, proportions … heads. Face …, hair …, outfit … (never change the outfit
to tell scenes apart: use pose and expression). `ref/<character>-sheet.png` is the master.

## Forbidden
Photorealism, likeness of a real person, logos and brands, text, letters, numbers, watermark,
painted checkerboard, white halo, new dominant bright colours, <topic-specific: e.g. a spectacular
crater when the story says "the size of a plate">.

## Prompt template (only SCENE changes; attach the master sheet as image 1)
Use case: illustration-story. Image 1 is the MASTER reference for identity AND illustration
technique, not a layout to reproduce. Create one editorial illustration, landscape about 1600px
wide, genuine transparent alpha background. Match the reference's <technique>. <Light>. No external
shadow, no white outline, no backdrop or ground rectangle. Palette <hex list>. Natural adult
proportions. If <character> appears, exactly match the reference face, <hair>, <outfit>; fictional
adult, no photorealism. NO text, letters, numbers, signage, labels, logo, watermark. Whole scene
fits with 6% transparent margins. SCENE:
{{SCENE}}
```

Scene prompts: one readable action, the indispensable objects, their scale relative to the
character, the direction of the gaze. Be physical when the action is tricky ("phone almost
horizontal, screen facing up, rear camera facing down" for a photo of the ground).

## Landmarks and overlays

Recurring diagrams (a metro line, a progress bar, a ticket) are HTML/SVG, not generated images:
exact colours, exact text, animatable from the timeline. Drive their state from the timeline
(frame-exact), not from a real-time CSS animation.
