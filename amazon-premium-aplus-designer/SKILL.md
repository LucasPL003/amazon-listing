---
name: amazon-premium-aplus-designer
description: Use when creating Amazon Premium A+ / 高级 A+ full-screen image pages after Amazon Listing and listing-image design output, including mobile 1200x900 and separately composed PC 1464x600 A+ assets, native copy, alt text, previews, or upload handoff files.
---

# Amazon Premium A+ Designer

Create a complete, continuous Premium A+ page from the upstream Listing and image-design contracts. Use only seven full-screen image modules: mobile first, then independently composed PC artwork after final mobile approval.

## Required Inputs

Require the seven-item `A+ 整体策划` and `图片解析摘要` from `$amazon-listing-agent`. Reuse `$amazon-listing-image-designer` output when available: approved images or concepts, typography and font-rights status, text colors, palette, icon system, visual rhythm, and Product Truth and Geometry Lock.

Also use user-provided product facts, source product images, approved brand assets, and revision notes. Do not read unrelated project context.

If the Listing A+ plan is missing or does not contain exactly seven items, request that the user supply it or rerun `$amazon-listing-agent`. Do not invent a different count.

If main/secondary images or an approved image-design visual system are unavailable, create one coherent page style from the product category, buyer, use scenario, price positioning, and purchase motivation. Lock it before planning images.

## Page Contract

Map `A+ 1` through `A+ 7` one-to-one. Every image has one primary sales task, a distinct role in the reading sequence, a clear carryover from the previous section, and new supported information. A+ deepens the main/secondary image story; it does not repeat their image or copy.

Create a private page style bible before the user review. Lock typography, verified font permission, text colors, palette, icon treatment, background world, lighting, color temperature, product scale, camera language, cards, corner treatment, spacing, and recurring motifs. If Image Designer supplied odd/even text colors, preserve that system.

Preserve product geometry, colors, materials, structure, interfaces, accessories, scale, and visible functions. Unknown facts remain unresolved; never turn a useful composition into a claim.

## Mobile-First Workflow

1. Build complete internal mobile specifications for all seven `1200×900` images. Include source-plan mapping, product-truth lock, task, scene, composition, exact on-image copy, native title/body copy, Alt text, typography, colors, icons, fact support, and negative constraints.
2. Present the concise seven-row table in `references/aplus-review-output-template.md`. Do not expose full generation prompts by default.
3. Do not call Image Gen until the user explicitly replies “确认生成移动端”.
4. Generate seven mobile images, then apply `references/aplus-quality-checklist.md` and create the `1200×6300` preview.
5. Accept local revisions as `A+N：修改内容`. Propagate global style, product, typography, color, or visual-world changes to every affected image and specification.
6. Wait for final confirmation of the complete mobile page before any PC design.

## PC Recomposition

After final mobile confirmation, create seven new `1464×600` PC specifications. Preserve each image's information, factual content, and visual identity, but recompose subject placement, crop, whitespace, text hierarchy, and reading direction for the horizontal canvas.

Never resize, stretch, directly crop, or mechanically transform mobile pixels into PC images. Generate the seven PC images only from the new PC specifications, run the quality checklist again, and create the `1464×4200` preview.

## Copy, Naming, and Handoff

For every image, deliver target-marketplace-language on-image headline/supporting copy, native Amazon title/body copy that complements the image, and accurate Alt text that describes the real image without keyword stuffing.

Use this image naming pattern:

```text
[图片核心表达]+01_移动端_1200x900.png
[图片核心表达]+01_PC端_1464x600.png
```

The image core expression is concise, unique within a device set, factually accurate, and in the image-copy language. `+01` through `+07` permanently map to `A+ 1` through `A+ 7`. Device labels and all handoff filenames use Chinese:

```text
移动端整页预览_1200x6300.jpg
PC端整页预览_1464x4200.jpg
A+内容.md
上传清单.md
验证报告.md
```

Populate `A+内容.md` with all seven on-image-copy, native-copy, and Alt-text records. Keep `上传清单.md` in A+ order with filenames and confirmation status; never overwrite existing human edits.

## Mandatory Final Package

Treat the final delivery as one fixed package, not a menu of optional files. A completed request always contains all of the following, in this order:

1. Seven mobile `1200×900` image files.
2. Seven independently composed PC `1464×600` image files.
3. `移动端整页预览_1200x6300.jpg` and `PC端整页预览_1464x4200.jpg`.
4. `A+内容.md` with seven on-image-copy, native-copy, and Alt-text records.
5. `上传清单.md` and `验证报告.md`.

If a user requests images only or asks to skip any listed artifact, keep the package contract unchanged and explain that the requested A+ delivery is incomplete without these files. If required upstream inputs are missing, request them before generation; do not change the final package shape.

## Validation

After mobile generation, run:

```powershell
python scripts/validate_aplus_package.py "<输出目录>" --phase mobile --prepare
```

After final delivery, run:

```powershell
python scripts/validate_aplus_package.py "<输出目录>" --phase final --prepare
```

The validator checks image count, dimensions, RGB mode, JPG/PNG format, target-language core expression uniqueness, Chinese device labels, naming, mobile/PC pairing, preview generation, checklist preservation, and required handoff files. It never deletes or overwrites source artwork.

## Non-Negotiable Quality Rules

Follow `references/aplus-quality-checklist.md` before generation, after mobile generation, before PC generation, and before final handoff.

Do not include unsupported claims, price, promotion, discount, purchase call-to-action, customer review, warranty/guarantee, competitor comparison, QR code, URL, contact details, unsupported certification, or absolute superiority claim. Do not upload directly to Seller Central; remind the operator to validate against the current module requirements before upload.