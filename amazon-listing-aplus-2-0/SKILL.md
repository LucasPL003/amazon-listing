---
name: amazon-listing-aplus-2-0
description: Use when creating, redesigning, planning, reviewing, or preparing upload-ready Amazon Premium A+ / 高级 A+ image content, including seven-module mobile 1200×900 and separately composed desktop 1464×600 assets, previews, image copy, alt text, or delivery checklists.
---

# Amazon Listing A+

Create Amazon Premium A+ packages as seven coherent modules, not generic long-scroll slices. Use supported product facts only; preserve product geometry, colour, material, markings, accessories, and visible functions.

## Mandatory Image Model

Generate every A+ raster artwork—including mobile modules, desktop modules, samples, regenerations, and repairs—only with **Image 2 (`gpt-image-2`)**.

When a generation route exposes model selection, explicitly select `gpt-image-2`. The built-in `image_gen` route is permitted only when it is configured to use Image 2. Never use `gpt-image-1.5` or any lower-capability image model, and never automatically fall back to one. If Image 2 is unavailable or its use cannot be verified, stop and ask the user how to proceed; do not generate a substitute asset.

## Scene-First Content Direction

Use **photorealistic, scene-led artwork as the default A+ content strategy** whenever verified facts support a credible environment or use context. Place the product naturally in a real setting or interaction with believable scale, materials, motivated lighting, contact shadows, depth, surfaces, and environmental detail. The image should read as an intentional photographed moment, not a product cutout placed over a solid color or abstract gradient.

Classify every module as `scene-led` or `proof-led` and record a brief `scene_justification` in the blueprint. Use scene-led composition for every buyer question that can be answered through a fact-supported use, placement, storage, gifting, travel, or ownership context. QA modules are always scene-led; when their answers depend on dimensions, compatibility, care, components, or other inspection evidence, place that evidence inside the truthful scene as a restrained inset or information layer. Reserve proof-led composition for the overview/core modules when their task requires unobstructed inspection, such as dimensions, included components, macro construction, mechanism, or material evidence. Even proof-led modules should use a believable material surface or restrained contextual cue when clarity allows.

When four or more modules have fact-supported scene opportunities, at least four of the seven mobile modules—and their independently recomposed desktop partners—must be scene-led. When fewer than four qualify, use scene-led artwork for every qualifying module. Do not repeat generic “product + solid-color background” posters merely to maintain consistency. A solid, gradient-only, or empty studio background is acceptable only when a specific proof-led task requires it, and each such module must have a distinct evidence-based justification.

Scenes, people, and props must not obscure the product or imply unsupported performance, audience, safety, included accessories, or results.

## Output Contract

- Deliver exactly seven mobile images at `1200×900` and seven matching desktop images at `1464×600`.
- Create mobile artwork first. Desktop artwork is a new composition for the same module, never a resize, stretch, or mechanical crop of the mobile image.
- Deliver `移动端整页预览_1200x6300.jpg`, `PC端整页预览_1464x4200.jpg`, `A+内容.md`, `上传清单.md`, and `验证报告.md` with the 14 image files.
- Use RGB PNG or JPG files. Keep modules `1` through `7` permanently paired between mobile and desktop. Name each mobile image `N-<target-language theme>_1200x900.png` and its desktop partner `PCN-<target-language theme>_1464x600.png`, where `N` is the module number. The filename theme must use the same target language and script as that module's on-image copy; do not mix languages in a filename.
- Do not upload to Seller Central. Ask the operator to confirm the currently available modules before uploading.

## Approval Gates

Stop at all gates. Never treat silence or a generic “continue” as approval.

1. **Blueprint approval:** confirm the complete seven-module plan before generating artwork.
2. **Mobile sample approval:** generate only modules `01` and `02`, concatenate a `1200×1800` preview, inspect it, and present both files, the preview, the optional continuity master, and an audit before generating modules `03`–`07`.
3. **Mobile package confirmation:** after generating all seven mobile images and the `1200×6300` preview, obtain confirmation before creating desktop artwork.

## Workflow

### 1. Analyze inputs

Identify the target Amazon marketplace, product facts, source images, approved brand assets, target buyer, reference style, prohibited claims, and any upstream `产品卖点分析` / `A+ 整体策划`. Separate observed facts from creative inference. Request missing critical facts once; otherwise use cautious category-level inference and mark it for human review.

Before building modules, list every distinct A/B-evidenced selling point and select 1–2 core selling points. Merge semantic duplicates. Select core points by differentiation, purchase-decision impact, evidence strength, marketplace relevance, and visual proof potential; choose only one when a second point would be weak or artificial. When an upstream plan already provides this analysis, preserve it unless it conflicts with product truth.

Do not invent dimensions, performance metrics, certifications, awards, medical effects, discounts, prices, guarantees, competitor comparisons, reviews, QR codes, URLs, contact details, or brand partnerships.

### 2. Build the seven-module blueprint

Before image generation, create exactly seven ordered modules. Each row must contain:

`module_id`, `module_type`, `source_item`, `buyer_question`, `verified_answer`, `module_job`, `evidence_type`, `scene_mode`, `scene_justification`, `content_density`, `mobile_composition`, `desktop_composition`, `text_exact`, `visual_style_notes`, `fact_support`, and `risk_unknowns`.

Use this fixed sequence:

1. **Module 01 — all-selling-points overview:** present every verified selling point in one concise overview. `module_type` is `all-selling-points-overview`; do not add a claim that is absent from the selling-point inventory.
2. **Core modules from 02:** assign one image to each selected core selling point. With one core point, only module 02 is a core module; with two, modules 02 and 03 are core modules. `module_type` is `core-selling-point`, and `source_item` names exactly one selected core point.
3. **All remaining modules — QA scene answers:** each answers one verified buyer question that has not already been answered by a core module. `module_type` is `qa-scene-answer`. State the question, direct verified answer, A/B fact support, a truthful usage scene that demonstrates the answer, and exact target-language copy.

Ordinary selling points appear in module 01 only and never receive standalone modules from module 02 onward. Semantically exclude every QA already answered by a core-selling-point module, even when the wording differs. For example, if waterproof performance is a selected core point and its module answers whether the product can handle water exposure, do not create a separate waterproof QA module.

Deduplicate equivalent non-core questions. When more verified QA remains than available slots, prioritize decision-critical questions with the strongest evidence and clearest scene proof; never invent traffic or frequency. When fewer remain, add fact-derived question-and-answer modules about suitability, usage, compatibility, package contents, care, or real limitations. Identify those as fact-derived, keep the question-and-direct-answer structure, and do not disguise an ordinary selling point as QA.

Module 01 may use an overview composition; core modules may be scene-led or proof-led according to the evidence. Every QA module must be scene-led and use its scene plus copy to answer the question. Use natural buyer-facing copy; never display planning labels.

### 3. Lock the visual system

Before generating final assets, lock palette, typography, lighting, background world, product scale, camera language, spacing, icon treatment, visual motifs, text hierarchy, and the scene-led/proof-led rhythm across all seven modules. Define believable locations, surfaces, lighting logic, depth, and recurring environmental cues for scene-led modules without making every scene composition identical. An optional `1:3` continuous master may guide shared art direction and transitions, but it is internal only: never deliver it as a final A+ image or crop it into the seven modules.

### 4. Generate the mobile package

Write one complete `1200×900` mobile specification for each approved module. Preserve the locked visual system while changing composition and information density between modules. Generate modules `01` and `02` first, inspect them, and create the mobile sample preview for the second approval gate.

After approval, generate modules `03`–`07`, concatenate the seven images vertically into `移动端整页预览_1200x6300.jpg`, and inspect the full page for factual accuracy, product consistency, legible copy, coherent rhythm, and repeated poster layouts. Obtain mobile package confirmation before desktop work.

### 5. Recompose the desktop package

For each confirmed mobile module, create a new `1464×600` desktop specification. Preserve the module's facts, claim, copy intent, and visual identity, but deliberately recompose subject position, crop, whitespace, text hierarchy, and reading direction for the horizontal canvas.

Never resize, stretch, directly crop, or mechanically transform a mobile image into its desktop partner. Generate and inspect all seven desktop images, then concatenate them into `PC端整页预览_1464x4200.jpg`.

### 6. Audit and deliver

Audit all files before handoff:

- Seven mobile and seven desktop images exist and have exact dimensions.
- Every image is RGB PNG/JPG and every module has one mobile/desktop pair.
- Image copy is legible, target-marketplace appropriate, and free of unsupported claims.
- Product identity, palette, typography, and visual world are consistent; module 01 covers all selling points, core modules each cover one selected core point, QA modules answer only non-core questions, and adjacent modules do not repeat the same composition.
- Every fact-supported scene opportunity is used according to the scene-led minimum; every isolated solid/gradient studio layout has a distinct proof-led justification.
- Previews use the required dimensions and include all seven modules in order.

Route revisions to the smallest responsible layer: revise copy for wording failures, one module for a local composition or product-drift failure, an adjacent pair for continuity failures, and the visual system only for page-wide style failures.

Use the following names (replace `N` with the module number `1`–`7`, and use the same target-language theme for the paired mobile and PC assets):

```text
N-<target-language theme>_1200x900.png
PCN-<target-language theme>_1464x600.png
移动端整页预览_1200x6300.jpg
PC端整页预览_1464x4200.jpg
A+内容.md
上传清单.md
验证报告.md
```

For example, Japanese module `1` with the theme `商品紹介` is named `1-商品紹介_1200x900.png` for mobile and `PC1-商品紹介_1464x600.png` for desktop. Never use the former `主题+01` naming pattern or a theme in a different language from its image copy.

`A+内容.md` records each module's on-image copy, complementary native A+ copy, and accurate alt text. `上传清单.md` lists the paired files in A+ order without overwriting existing human edits. `验证报告.md` records the final audit.

## Reference

Read `references/detail-page-patterns.md` when selecting module patterns, reviewing continuity, or preparing the final handoff.
