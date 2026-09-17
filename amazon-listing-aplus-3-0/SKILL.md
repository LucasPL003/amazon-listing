---
name: amazon-listing-aplus-3-0
description: Use when creating, redesigning, planning, reviewing, or preparing upload-ready Amazon Premium A+ / 高级 A+ image content, including seven-module mobile 1200×900 and separately composed desktop 1464×600 assets, previews, image copy, alt text, or delivery checklists.
---

# Amazon Listing A+

Create Amazon Premium A+ packages as seven coherent modules, not generic long-scroll slices. Use supported product facts only; preserve product geometry, colour, material, markings, accessories, and visible functions.

## Image Generation Route

Use the currently available default image-generation route for A+ module artwork, samples, regenerations, and repairs. Do not hard-code or require a particular image model in this skill. When the user explicitly requests a specific model, use that model when the available generation route supports it; otherwise state that the requested model is unavailable rather than silently claiming it was used.

## Mandatory Product-Image Study and Fidelity Gate

Complete this gate before building the seven-module blueprint or generating any artwork. The user's original product photographs are the identity truth. Filenames, thumbnails, written summaries, style references, mobile artwork, and other AI-generated images are not substitutes for studying those originals.

1. Open and visually inspect **every user-supplied original product image** with `view_image`; use original detail when small construction features, texture, markings, ports, seams, edges, or fasteners require close inspection. Cross-check all available angles. If an original image cannot be accessed or inspected, stop and ask the user to reattach it before planning or generating.
2. Create an internal `product_identity_geometry_lock` from the original images. Record the evidenced silhouette and overall proportions; relative length, width, height, thickness, and part scale; component count, position, orientation, attachment points, curves, corners, openings, seams, joints, handles, ports, buttons, fasteners, and construction details; material, texture, finish, exact visible colour, logos, labels, patterns, and markings; included accessories, pack count, permitted product states, and the original image(s) supporting each observation.
3. Mark every hidden, blurred, cropped, conflicting, or occluded feature as `unknown`; never invent a plausible completion. When original images conflict, ask the user which is authoritative rather than averaging their shapes. If the lock cannot support a planned view, choose an evidenced camera angle that conceals the unknown area or request a clearer product photo.
4. Treat the product as an immutable photographed object. Do not beautify, stylize, simplify, symmetrize, smooth, bend, straighten, lengthen, shorten, widen, narrow, thicken, thin, recolour, relabel, or add, remove, merge, duplicate, or relocate any part. Only the scene, camera, lighting, props, composition, and typography may change.
5. In **every** mobile, desktop, sample, regeneration, and repair call, include one or more original user product photographs sufficient to establish that module's view and visible details as identity references. Repeat the relevant `product_identity_geometry_lock` fields in the prompt. Prior mobile/desktop artwork and any continuity or style master may guide layout, palette, typography, and mood only; no AI-generated asset may be the sole product-identity source.
6. After every generation, inspect the result with `view_image` and compare its product directly against the supporting original photographs and the lock. Check silhouette, proportions, part count, part scale and placement, attachment geometry, openings and controls, material response, colour, markings, accessories, and product state. Any unexplained difference is product deformation and fails the module. Regenerate only the failed asset with stronger original references or a better-evidenced angle; never approve, deliver, or explain away a deformed product.

## Photographic Cleanliness and AI-Artifact Gate

Every continuity master, mobile module, desktop module, sample, regeneration, and final JPEG must look like clean professional photography at original viewing resolution. Correct product identity, approved copy, and attractive composition never compensate for visible AI artifacts.

### Generation contract

Include a compact `photographic_cleanliness` block in every module specification and image prompt. Require natural non-repeating material microtexture, smooth continuous tonal transitions, coherent perspective, crisp physically plausible edges, consistent light direction, grounded contact shadows, and reflections that follow actual surface geometry. Low-detail regions such as walls, skies, tabletops, product surfaces, and soft backgrounds must remain visually calm rather than acquiring synthetic texture.

Explicitly exclude AI ripple/wave patterns, moiré, contour rings, swirls, repeated or tiled texture, melted or smeared detail, warped straight lines, plastic-looking material, haloing, ringing, banding, blotchy gradients, doubled edges, broken depth of field, and reflections, highlights, or shadows that undulate or contradict the scene lighting.

### Two-stage inspection

1. **Generated-source inspection:** before resize, conversion, preview assembly, or other delivery processing, open every generated source with `view_image` at original detail. Inspect the product surface and outline, small construction details, hands/skin/hair when present, fabric, walls, floors, tabletops, sky, gradients, bokeh, highlights, contact shadows, cast shadows, and reflections. Any unexplained ripple, repeated pattern, melted edge, halo, banding, synthetic plastic texture, or optical inconsistency fails the module even when identity, copy, and dimensions are correct.
2. **Final-JPEG inspection:** after the approved source is resized or exported, open the exact final module `.jpg` at original detail and repeat the cleanliness inspection. Inspect concatenated previews after assembly for export damage, seams, ringing, or banding. Passing the generated-source inspection does not waive the final-file check.
3. If the generated source contains the defect, classify it as a generation artifact and regenerate only that mobile or desktop module with the cleanliness block strengthened or the problematic scene detail simplified without changing the approved module job. If the source is clean but the final JPEG is dirty, classify it as a resize/export artifact and re-export from the clean source with high-quality non-destructive processing; do not regenerate clean artwork unnecessarily.

Never use blur, sharpening, denoise, aggressive JPEG compression, downscaling, upscaling, texture overlays, or local smearing to conceal a failed artifact. Required size conversion may use high-quality non-destructive resampling, but the exact final file must independently pass inspection. A defect that is merely less visible after processing is still a failed module.

## Scene-First Content Direction

Use **photorealistic, scene-led artwork as the default A+ content strategy** whenever verified facts support a credible environment or use context. Place the product naturally in a real setting or interaction with believable scale, materials, motivated lighting, contact shadows, depth, surfaces, and environmental detail. The image should read as an intentional photographed moment, not a product cutout placed over a solid color or abstract gradient.

Classify every module as `scene-led` or `proof-led` and record a brief `scene_justification` in the blueprint. Use scene-led composition for every buyer question that can be answered through a fact-supported use, placement, storage, gifting, travel, or ownership context. QA modules are always scene-led; when their answers depend on dimensions, compatibility, care, components, or other inspection evidence, place that evidence inside the truthful scene as a restrained inset or information layer. Reserve proof-led composition for the overview/core modules when their task requires unobstructed inspection, such as dimensions, included components, macro construction, mechanism, or material evidence. Even proof-led modules should use a believable material surface or restrained contextual cue when clarity allows.

When four or more modules have fact-supported scene opportunities, at least four of the seven mobile modules—and their independently recomposed desktop partners—must be scene-led. When fewer than four qualify, use scene-led artwork for every qualifying module. Do not repeat generic “product + solid-color background” posters merely to maintain consistency. A solid, gradient-only, or empty studio background is acceptable only when a specific proof-led task requires it, and each such module must have a distinct evidence-based justification.

Scenes, people, and props must not obscure the product or imply unsupported performance, audience, safety, included accessories, or results.

## Output Contract

- Deliver exactly seven mobile images at `1200×900` and seven matching desktop images at `1464×600`.
- Create mobile artwork first. Desktop artwork is a new composition for the same module, never a resize, stretch, or mechanical crop of the mobile image.
- Deliver `移动端整页预览_1200x6300.jpg`, `PC端整页预览_1464x4200.jpg`, `A+内容.md`, `上传清单.md`, and `验证报告.md` with the 14 image files.
- Deliver every module image and concatenated preview as a high-quality RGB JPEG with the `.jpg` extension. If the generation tool returns PNG, WebP, or another format, preserve the approved content and export the final delivery copy as RGB JPEG; do not deliver the source-format image as final artwork.
- Keep modules `1` through `7` permanently paired between mobile and desktop. Name each mobile image exactly `N-<target-language theme>.jpg` and its desktop partner exactly `PCN-<target-language theme>.jpg`, where `N` is the module number. The PC marker is the uppercase prefix `PC` immediately before the sequence number. The filename theme must use the same target language and script as that module's on-image copy. Do not append dimensions, device labels, English descriptors, or other suffixes.
- Save the completed A+ package in one workspace folder under `output/amazon-aplus/` without overwriting existing files. Keep final module images, final concatenated previews, and the required handoff documents together in that package folder; keep exploratory or superseded files outside the final package.
- Do not upload to Seller Central. Ask the operator to confirm the currently available modules before uploading.

## Approval Gates

Stop at all gates. Never treat silence or a generic “continue” as approval.

1. **Blueprint approval:** confirm the complete seven-module plan before generating artwork.
2. **Mobile sample approval:** generate only modules `01` and `02`, concatenate `移动端样稿预览_1200x1800.jpg`, inspect it, and present both module files, the preview, the optional continuity master, and an audit before generating modules `03`–`07`.
3. **Mobile package confirmation:** after generating all seven mobile images and the `1200×6300` preview, present the images and obtain confirmation before creating desktop artwork.

## Workflow

### 1. Analyze inputs

Identify the target Amazon marketplace, product facts, source images, approved brand assets, target buyer, reference style, prohibited claims, and any upstream `产品卖点分析` / `A+ 整体策划`. Separate observed facts from creative inference. Request missing critical facts once; otherwise use cautious category-level inference and mark it for human review.

Complete the Mandatory Product-Image Study and Fidelity Gate at this stage. The blueprint must not begin until every supplied original product image has been inspected and the evidence-mapped `product_identity_geometry_lock`, including all unknown/occluded features, is complete.

Before building modules, list every distinct A/B-evidenced selling point and select 1–2 core selling points. Merge semantic duplicates. Select core points by differentiation, purchase-decision impact, evidence strength, marketplace relevance, and visual proof potential; choose only one when a second point would be weak or artificial. When an upstream plan already provides this analysis, preserve it unless it conflicts with product truth.

Do not invent dimensions, performance metrics, certifications, awards, medical effects, discounts, prices, guarantees, competitor comparisons, reviews, QR codes, URLs, contact details, or brand partnerships.

### 2. Build the seven-module blueprint

Before image generation, create exactly seven ordered modules. Each row must contain:

`module_id`, `module_type`, `source_item`, `buyer_question`, `verified_answer`, `module_job`, `evidence_type`, `scene_mode`, `scene_justification`, `content_density`, `mobile_composition`, `desktop_composition`, `text_exact`, `visual_style_notes`, `fact_support`, `identity_reference_ids`, `visible_geometry_constraints`, `risk_unknowns`, `photographic_cleanliness`, and `artifact_risk_areas`.

For each row, `identity_reference_ids` names the original user product images that support its planned mobile and desktop views; `visible_geometry_constraints` copies the relevant immutable fields from `product_identity_geometry_lock`; and `risk_unknowns` records any hidden, cropped, blurred, or conflicting product area the composition must avoid. `photographic_cleanliness` contains the required cleanliness block, and `artifact_risk_areas` names surfaces, gradients, fine texture, edges, reflections, or shadows that require extra original-detail inspection. A row without sufficient original-image evidence or these cleanliness fields is not generation-ready.

Use this fixed sequence:

1. **Module 01 — all-selling-points overview:** present every verified selling point in one concise overview. `module_type` is `all-selling-points-overview`; do not add a claim that is absent from the selling-point inventory.
2. **Core modules from 02:** assign one image to each selected core selling point. With one core point, only module 02 is a core module; with two, modules 02 and 03 are core modules. `module_type` is `core-selling-point`, and `source_item` names exactly one selected core point.
3. **All remaining modules — QA scene answers:** each answers one verified buyer question that has not already been answered by a core module. `module_type` is `qa-scene-answer`. State the question, direct verified answer, A/B fact support, a truthful usage scene that demonstrates the answer, and exact target-language copy.

Ordinary selling points appear in module 01 only and never receive standalone modules from module 02 onward. Semantically exclude every QA already answered by a core-selling-point module, even when the wording differs. For example, if waterproof performance is a selected core point and its module answers whether the product can handle water exposure, do not create a separate waterproof QA module.

Deduplicate equivalent non-core questions. When more verified QA remains than available slots, prioritize decision-critical questions with the strongest evidence and clearest scene proof; never invent traffic or frequency. When fewer remain, add fact-derived question-and-answer modules about suitability, usage, compatibility, package contents, care, or real limitations. Identify those as fact-derived, keep the question-and-direct-answer structure, and do not disguise an ordinary selling point as QA.

Module 01 may use an overview composition; core modules may be scene-led or proof-led according to the evidence. Every QA module must be scene-led and use its scene plus copy to answer the question. Use natural buyer-facing copy; never display planning labels.

### 3. Lock the visual system

Before generating final assets, lock palette, typography, lighting, background world, product scale, camera language, spacing, icon treatment, visual motifs, text hierarchy, and the scene-led/proof-led rhythm across all seven modules. Define believable locations, surfaces, lighting logic, depth, and recurring environmental cues for scene-led modules without making every scene composition identical. An optional `1:3` continuous master may guide shared art direction and transitions, but it is internal only: never deliver it as a final A+ image or crop it into the seven modules.

The visual-system lock controls art direction only and may not overwrite `product_identity_geometry_lock`. A continuity master or approved module is never authoritative for product shape or construction.

### 4. Generate the mobile package

Write one complete `1200×900` mobile specification for each approved module. Preserve the locked visual system while changing composition and information density between modules. Generate modules `01` and `02` first, inspect them, and create the mobile sample preview for the second approval gate.

Each mobile specification and generation call must include its original-photo `identity_reference_ids`, relevant `visible_geometry_constraints`, and `risk_unknowns`. After generation, compare the product directly with those original images; product fidelity is a pass/fail requirement independent of scene quality and copy quality.

Each mobile source and exact final JPEG must also pass the Photographic Cleanliness and AI-Artifact Gate. Inspect the row's `artifact_risk_areas` at original detail before presenting modules `01` and `02` or completing modules `03`–`07`.

After approval, generate modules `03`–`07`, concatenate the seven images vertically into `移动端整页预览_1200x6300.jpg`, and inspect the full page for factual accuracy, product consistency, legible copy, coherent rhythm, and repeated poster layouts. Obtain mobile package confirmation before desktop work.

### 5. Recompose the desktop package

For each confirmed mobile module, create a new `1464×600` desktop specification. Preserve the module's facts, claim, copy intent, and visual identity, but deliberately recompose subject position, crop, whitespace, text hierarchy, and reading direction for the horizontal canvas.

Never resize, stretch, directly crop, or mechanically transform a mobile image into its desktop partner. Generate and inspect all seven desktop images, then concatenate them into `PC端整页预览_1464x4200.jpg`.

For every desktop generation, return independently to the original user product photographs listed by `identity_reference_ids` and include the relevant `product_identity_geometry_lock`. The confirmed mobile module may guide message, layout relationship, and art direction, but it must never be the sole product reference. Inspect and compare each desktop product directly against the originals, not merely against its mobile partner.

Every desktop specification and prompt must independently carry the same `photographic_cleanliness` block and canvas-specific `artifact_risk_areas`. Inspect both the desktop generated source and exact final JPEG at original detail; a clean mobile partner does not prove that its desktop recomposition is clean.

### 6. Audit and deliver

Audit all files before handoff:

- Seven mobile and seven desktop images exist and have exact dimensions.
- Every image is an RGB JPEG with a `.jpg` extension and every module has one mobile/desktop pair.
- Image copy is legible, target-marketplace appropriate, and free of unsupported claims.
- Product identity, palette, typography, and visual world are consistent; module 01 covers all selling points, core modules each cover one selected core point, QA modules answer only non-core questions, and adjacent modules do not repeat the same composition.
- Every mobile and desktop product has been compared directly with its supporting original product photographs and passes the `product_identity_geometry_lock`; no image contains stretched, compressed, simplified, smoothed, invented, missing, duplicated, merged, or relocated product geometry.
- Every generated source and exact final module JPEG passes the Photographic Cleanliness and AI-Artifact Gate at original detail; no asset contains AI waves, ripples, moiré, repeated texture, melted edges, halos, ringing, banding, plastic-looking material, warped lines, broken depth of field, or incoherent reflections/highlights/shadows.
- Every fact-supported scene opportunity is used according to the scene-led minimum; every isolated solid/gradient studio layout has a distinct proof-led justification.
- Previews use the required dimensions and include all seven modules in order.

Route revisions to the smallest responsible layer: revise copy for wording failures, one module for a local composition or product-drift failure, an adjacent pair for continuity failures, and the visual system only for page-wide style failures.

Any product deformation is a failed asset, not a stylistic variation. Regenerate the affected mobile or desktop module from the original product photographs with a stronger lock or a better-evidenced angle. If the required view is unsupported, ask for a clearer source image rather than inventing the missing geometry.

Any listed AI artifact in a generated source is a failed module, not a stylistic variation. Regenerate only the affected source using a strengthened `photographic_cleanliness` block; never conceal it with blur, sharpening, denoise, compression, scaling, overlays, or smearing. When the source is clean and only the exported JPEG is defective, re-export the clean source and repeat the final-file inspection.

Use the following names (replace `N` with the module number `1`–`7`, and use the same target-language theme for the paired mobile and PC assets):

```text
N-<target-language theme>.jpg
PCN-<target-language theme>.jpg
移动端样稿预览_1200x1800.jpg
移动端整页预览_1200x6300.jpg
PC端整页预览_1464x4200.jpg
A+内容.md
上传清单.md
验证报告.md
```

For example, Japanese module `1` with the theme `商品紹介` is named `1-商品紹介.jpg` for mobile and `PC1-商品紹介.jpg` for desktop. Never use the former `主题+01` pattern, add dimension suffixes, or use a theme in a different language from its image copy.

`A+内容.md` records each module's on-image copy, complementary native A+ copy, and accurate alt text. `上传清单.md` lists the paired filenames and confirmation status in A+ order without overwriting existing human edits. `验证报告.md` records the final audit.

After the complete A+ package has been generated, validated, named, and saved, add exactly one clickable Markdown link to the final package folder at the end of the final handoff: `[打开A+图片文件夹](</absolute/path/output/amazon-aplus/>)`. The link target must be the actual absolute directory containing the final `.jpg` images and previews. Wrap the target in angle brackets so paths containing spaces remain clickable. Do not use `file://`, a relative path, a temporary generation location, or a folder containing only superseded files. Do not place the Markdown link inside backticks or a code block.

Do not output individual image paths or per-image file links at approval gates or final delivery. Provide only the single final output-folder link after the whole package is complete.

## Common Product-Fidelity Failures

| Mistake | Required correction |
| --- | --- |
| Starting the blueprint after viewing only thumbnails, filenames, summaries, or a subset of supplied product images | Inspect every original product image and complete the evidence-mapped `product_identity_geometry_lock` first. |
| Guessing a hidden side or averaging conflicting product shapes | Mark the feature `unknown`; use an evidenced angle or ask for a clearer/authoritative photo. |
| Using an approved mobile module, desktop partner, or continuity master as the sole product reference | Include sufficient original user product photographs in every generation and repair call; generated assets control art direction only. |
| Accepting an attractive module whose product proportions, structure, or parts drifted | Compare directly with the originals, fail it as deformation, and regenerate only that module. |
| Deriving PC product geometry from the mobile AI artwork | Return independently to the original-photo `identity_reference_ids` and rebuild the PC composition from those product truths. |
| Delivering a module with AI waves, ripples, moiré, repeated texture, melted edges, halos, banding, plastic material, or broken reflections/shadows because its product and text are correct | Fail it under the Photographic Cleanliness and AI-Artifact Gate and regenerate only that generated source. |
| Inspecting only a reduced preview, mobile partner, generated source, or final JPEG | Inspect each generated source and its exact final mobile/desktop JPEG at original detail; inspect assembled previews for export damage. |
| Hiding AI artifacts with blur, sharpening, denoise, aggressive compression, scaling, or texture overlays | Reject the concealment; regenerate a defective source or re-export a clean source, then repeat the final-file inspection. |

## Reference

Read `references/detail-page-patterns.md` when selecting module patterns, reviewing continuity, or preparing the final handoff.