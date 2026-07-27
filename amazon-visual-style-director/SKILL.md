---
name: amazon-visual-style-director
description: Use when turning Amazon Listing image briefs, product images, 图片解析摘要, 附图策划, or exact image copy into three complete visual-and-typography direction samples, approved Style ID systems, text-free Image Gen visual plates, deterministic final listing images, visual QA, or targeted image rework.
---

# Amazon Visual Style Director

Turn a verified Listing image brief into a product-specific visual system and a cohesive Amazon image set. Design the visual plate and typography as one composition, but produce them separately: Image Gen creates only text-free plates, and the deterministic renderer applies approved exact copy.

Do not read unrelated project context. Use only the current `图片解析摘要`, `附图策划`, `图片创意简报`, original product images, user-provided product facts, approved fonts or brand assets, and revision notes.

## Required references and scripts

Read all four references completely before beginning direction work:

1. `references/input-contract.md` for input normalization, required fields, main-image rules, sample selection, and manifest shape.
2. `references/direction-card-and-sample.md` for the three complete samples and locked Style ID contract.
3. `references/visual-typography-rubric.md` for the four quality gates and the boundary between design judgment and script execution.
4. `references/rework-routing.md` for deterministic failure routing and the two-attempt stop rule.

Use all three bundled scripts whenever their checks apply. These are importable Python modules, not command-line interfaces:

- Before visual direction, call `scripts/validate_brief.py` functions `validate_briefs` for the normalized ordered collection and `select_sample_candidate` for the representative secondary task.
- After a plate passes visual QA, call `scripts/render_composition.py` function `render_composition` with the approved 1500×1500 plate, composition manifest, and output directory.
- After rendering, call `scripts/validate_output.py` functions `validate_output`, `route_failure`, and `should_stop_retry` for package validation, rework routing, and retry control.

Scripts check declared inputs, manifest and package structure, dimensions, expected files, font-rights metadata, and routing. They do not compare rendered glyphs with approved copy or establish copy fidelity, product truth, or aesthetic quality. Make those judgments against the references; never treat script success as aesthetic approval.

**REQUIRED SUB-SKILL:** Use `imagegen` for every visual-plate generation or edit. Never use it to render final copy.

## Required inputs

Require all of the following before direction selection:

- `## 图片解析摘要` from `$amazon-listing-agent`.
- `## 附图策划` from `$amazon-listing-agent`.
- `## 图片创意简报` with one entry for every image plan.
- Original product images.

Accept user-approved brand assets and style preferences as optional constraints. If a required section, original product image, or factual lock is missing, request it or rerun `$amazon-listing-agent`; do not invent it.

## Workflow

Follow this order without skipping, merging, or generating ahead.

### 1. Validate and normalize the brief

Map each human-readable `图片创意简报` entry to `references/input-contract.md`:

- `图 N` → `image_id`.
- `图片类型` → `image_type` (`主图` = `main`, `副图` = `secondary`).
- `单一销售任务` → `sales_task`.
- `产品真实性锁定` → `product_truth_lock`.
- `目标用户与使用场景` → `target_user_and_scene`; retain it as a required internal direction field.
- `精确图片文案` → `exact_copy`, preserving every word, digit, unit, punctuation mark, case, emphasis word, and language.
- `Prompt Skeleton` → `prompt_skeleton`.
- `禁止内容与合规风险` → `prohibited_content`.
- `样张候选` → `sample_candidate`; normalize `是`/`true` to `True` and `否`/`false` to `False` before selection.

Apply one observable sentinel conversion before calling `validate_briefs`: 主图的 `主标题`、`副标题`、`数字与单位` 和 `强调词` 值恰为 `无` 时，将对应 `exact_copy` 值规范化为空字符串 `""`。保留原始 `语言` 值。Do not convert `无` inside any factual field, secondary-image copy, or longer user-supplied text. 其他用户提供的事实与文案逐字保持不变。Record the normalized `exact_copy` and `target_user_and_scene` in the internal brief so the pre-validation result is inspectable.

Resolve `font_rights` here: use only a user-provided or open-license, loadable font file. The Listing Agent does not choose typography or fonts. Record the approved rights status and path before calling `validate_briefs`.

Run `validate_briefs` on the complete ordered collection, then inspect every entry's returned violations. Stop and report exact violations when any entry fails; do not silently complete missing facts, copy, language, rights, or product locks. Confirm that the number and order of brief entries match `附图策划` one-to-one. Main-image headline, subtitle, number/unit, and emphasis values must be empty after the exact `无` normalization above; secondary-image copy must contain at least a headline and language.

### 2. Select one representative secondary task

Call `select_sample_candidate` across the validated briefs. Use the first secondary entry marked `样张候选：是`; otherwise use the first secondary entry. Never use a main image for the three-direction comparison. Keep the same product, sales task, product lock, and exact copy across all three samples.

### 3. Generate three complete direction samples

Create three meaningfully different, product-specific direction cards and complete sample specifications for the selected secondary task. Follow every required field in `references/direction-card-and-sample.md`. Differences must include visual narrative, lighting, color relationship, typography character, and icon/shape language while serving the same sales task and preserving identical copy.

For each direction, co-design the text-free plate and typography before generation: define product placement, focal path, negative-space shape, copy anchors, hierarchy, palette roles, icons, line work, and contrast behavior. A direction sample is a reviewable final image, not a mood board, direction card, or text-free plate.

Present the three direction cards and planned samples first. Before any sample Image Gen call, obtain an explicit user confirmation such as `确认生成三套样张`. Then generate three text-free plates, render their exact copy deterministically, run all four QA gates, and show the three complete samples together.

### 4. Wait for the user's direction choice

After showing all three complete samples, stop and ask the user to either select one direction or specify an explicit cross-direction combination. Do not choose on the user's behalf. Do not infer unspecified combinations or begin the full image set.

### 5. Lock the Style ID

Convert the selected or explicitly combined direction into one internally coherent Style ID. Populate every field in `references/direction-card-and-sample.md`, including the creative thesis, visual narrative, anti-template rule, palette roles, lighting and camera logic, product scale, negative space, typography master, headline/subtitle/number hierarchy, icon and shape system, allowed variations, and locked consistency rules.

Record a Product Truth Lock for shape, proportions, color, material, structure, interfaces, accessories, quantity, supported functions, usage, and unknown facts. Lock the Style ID before planning final plates. Any proposed change to a locked field returns to user direction approval.

### 6. Co-design every final plate and typography composition

Map every brief one-to-one to its `附图策划` item. Preserve its single sales task, normalized `target_user_and_scene` mapped from `目标用户与使用场景`, exact copy, product truth, prompt skeleton, and prohibited content.

For every image, write two linked specifications before generation:

1. A text-free visual-plate specification containing the Style ID, product locks, scene, action, camera, lighting, product scale, focal path, palette roles, props, negative space, copy-safe region, and negative constraints.
2. A composition manifest containing the approved font rights, exact copy, hierarchy, line breaks, coordinates, bounding boxes, sizes, colors, icon/shape layers, and Style ID.

Use the actual plate design to refine text color, placement, support shapes, shadow, or line work only within the locked Style ID. Do not rewrite, translate, shorten, or generate approved copy. Keep the main image text-free.

Present a concise full-set review and wait for explicit confirmation such as `确认生成整套图片`. Treat revisions as specification changes and ask for confirmation again.

### 7. Generate text-free plates and render exact copy

Only after explicit confirmation, call Image Gen for text-free 1500×1500 plates. Every prompt must prohibit words, letters, labels, captions, digits, units, logos, watermarks, text-like symbols, and gibberish. Regenerate any plate that contains text or violates product truth, composition, or the locked Style ID.

After a plate passes visual review, call `render_composition`. Deliver one package per image containing:

```text
visual-plate.png
typography-overlay.png
final-image.png
composition.json
```

The overlay is transparent RGBA; the final image is the deterministic composite. Never use Image Gen, image-to-image editing, or generative fill to add, correct, translate, or restyle final copy.

### 8. Run the four QA gates and route failures

Run these gates in order for each final image and then for the complete set:

1. Product Truth.
2. Single-Image Visual Quality.
3. Typography-to-Image Harmony.
4. Set Consistency.

Use the full checks in `references/visual-typography-rubric.md`. Call `validate_output` for every rendered package. For any failure, classify it and call `route_failure`:

- `product-truth` or `visual-composition` → regenerate the visual plate.
- `text-accuracy` → rerender the typography overlay.
- `typography-harmony` → redesign the composition.
- `style-id` → restart direction selection and obtain user approval again.

After each automatic rework, rerun all applicable gates and package validation. Call `should_stop_retry`; after two completed automatic attempts, stop. Deliver the current best result, name the failed gate and prescribed next action, and request user direction before continuing.

## Handoff contract

Hand off the approved replacement Style ID, Product Truth Lock, palette roles, typography master and font-rights record, icon/shape system, visual rhythm, locked consistency rules, allowed variations, exact-copy records, package validation result, and approved images when present. This is the upstream visual contract for `$amazon-premium-aplus-designer`.

## Non-negotiable rules

- Preserve original product truth and unknowns; never reshape the product, invent accessories or capabilities, or turn inference into a claim.
- Keep one sales task per image and one approved Style ID per set.
- Use exactly the approved marketplace-language copy; Image Gen never writes it.
- Make all style choices product-specific; reject generic ecommerce templates and unexplained decoration.
- Do not call Image Gen without explicit confirmation.
- Do not exceed two automatic rework attempts.
