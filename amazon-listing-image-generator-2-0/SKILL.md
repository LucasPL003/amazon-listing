---
name: amazon-listing-image-generator-2-0
description: Use when generating Amazon main images and secondary listing images from an Amazon Listing image plan, especially when the set must share one product-appropriate style, adapt to a target marketplace, and preserve verified product facts.
---

# Amazon Listing Image Generator

## Overview

Generate a complete Amazon listing image set from the upstream `amazon-listing-agent-2-0` output: one approved Text Master, one approved Visual Master, one compliant main image, and every planned secondary image. Product truth comes first; a consistent visual system then makes the set feel intentional and desirable to the target-market buyer.

## Mandatory Image Model

Generate every raster asset—including Visual Masters, main images, secondary images, regenerations, and repairs—only with **Image 2 (`gpt-image-2`)**. Use one generation call per distinct asset.

When a generation route exposes model selection, explicitly select `gpt-image-2`. The built-in `image_gen` route is permitted only when it is configured to use Image 2. Never use `gpt-image-1.5` or any lower-capability image model, and never automatically fall back to one. If Image 2 is unavailable or its use cannot be verified, stop and ask the user how to proceed; do not generate a substitute asset.

Do not switch to CLI/API generation unless the user explicitly requests it.

## Scene-First Visual Direction

Except for the Amazon main image, use **photorealistic, scene-led content as the default visual strategy** whenever the fact lock supports a credible environment or use context. Show the product naturally situated, handled, worn, placed, stored, gifted, travelled with, or used as appropriate to the verified product facts. Build scenes with believable scale, material response, natural or motivated lighting, contact shadows, depth, surfaces, and environmental detail; the result should read as a real photographed moment rather than a product cutout floating over a color field.

Classify every secondary image in the Text Master as either `scene-led` or `proof-led`, with one brief evidence-based reason. Use `scene-led` for every planned task whose buyer question can be answered through a fact-supported environment or interaction. Reserve `proof-led` for tasks that genuinely need unobstructed inspection, such as dimensions, quantity/included components, macro construction, mechanism, material, or care evidence. Even a proof-led image should use a believable surface or restrained contextual cue when that does not weaken the proof.

The Amazon main image remains the required pure-white catalogue exception. For secondary images, a plain solid-color, gradient-only, or empty studio background is not a reusable default layout. Do not replace scene-worthy planned tasks with repeated “product + solid background” posters for speed or set consistency. A set fails scene review when most fact-supported usage tasks are rendered as isolated product layouts, or when repeated isolated layouts lack a distinct proof-led justification.

Scenes, people, and props must remain compatible with the fact lock. They may clarify use but must not obscure the product, imply a non-included accessory, unsupported audience, unsafe use, or unverified result.

## Canvas and File Requirements

Every delivered asset—the Visual Master, main image, and every secondary image—must be a square **1500 × 1500 px** file. Compose every generation for a 1:1 canvas; never stretch a landscape or portrait image to fit.

If the built-in image tool returns another square pixel size, retain the approved image content and create a non-destructive 1500 × 1500 delivery copy in the project output folder. If it returns a non-square image, regenerate the asset rather than crop, pad, or distort its composition. Before delivery, inspect the saved file dimensions and require exactly 1500 pixels for both width and height.

## Required Inputs

Before generating anything, obtain all of the following:

1. The upstream Listing output containing `图片解析摘要`, `产品卖点分析`, and `附图策划`.
2. The target marketplace and its customer-facing language.
3. Product reference image(s) showing the actual sellable item. Treat them as identity references, not loose inspiration.
4. Product facts, pack count, variation information, and any user-approved brand assets when they exist.

`图片解析摘要` and the user-provided product facts are the only sources for visible product identity and product claims. `产品卖点分析` supplies the verified selling-point inventory and the 1–2 selected core selling points. `附图策划` supplies each image's sequence, single sales task, mapped selling point or buyer concern, evidence source, algorithm task, and compliance risk. This skill develops the scene, target-language image copy, props, layout direction, and generation prompt during the Text Master and Visual Master stages.

If the summary, plan, reference images, marketplace, or required product facts are missing or conflict, ask the user for the missing source before generating. Do not infer material composition, measurements, performance, included accessories, certification, pack quantity, compatibility, or use conditions.

### Reference Role Contract

Before planning or prompting, classify every supplied reference internally as one or more of these roles:

- **Identity reference:** the authoritative source for the sellable product's appearance, construction, included items, and evidenced variation.
- **Component reference:** the authoritative source for a specific included item, accessory, count, finish, or visible detail when it is not fully shown by the identity reference.
- **Style reference:** guidance only for composition, lighting, color, typography character, or scene mood.

When references conflict, identity and component references override style references. A style reference must never alter the product's silhouette, printed/physical artwork, structure, included contents, colorway, scale relationship, or supported claims. Record the source used for every product-critical visual decision in the fact lock.

## 文本母版与视觉母版

Use two set-level masters as the only production handoff. Do not create an individual execution record for each secondary image:

`上游附图策划 → 文本母版 + 视觉母版 → 一次用户审批 → 全套主附图`

### 文本母版

Create one Text Master before any production listing image. It is a compact, set-level execution table derived from the upstream plan, not a second upstream creative-brief deliverable. Preserve each image's sequence, type, single sales task, mapped selling point or buyer concern, supported fact source, algorithm task, and compliance risk without changing them. Then develop exactly one `buyer_question`, exactly one `evidence_type`, `scene-led` or `proof-led` classification with its evidence-based reason, a product-appropriate scene and permitted props, exact target-language copy and emphasis, and prohibited content for each secondary image. Keep the main-image copy fields empty and its scene a compliant pure-white catalogue presentation. The Text Master also locks the set-wide text hierarchy, typography character, and no-extra-text rule.

Use the upstream core-selling-point labels to prioritize the strongest supported benefit communication, but do not invent an extra core claim or silently promote an ordinary selling point. If the upstream plan assigns a QA concern, answer it through the Text Master scene and copy only when its cited A/B evidence supports the answer.

### 视觉母版

Generate one square 1:1 Visual Master before any production listing image. It is an approval asset and a set-level style reference, not a production listing image. It must show the actual product or a faithful product reference, material and lighting cues, text-safe layout examples, and a scenario board with multiple product-appropriate secondary-image use cases drawn from the upstream plan. Prioritize plausible usage scenes such as creating, resting, gifting, or travel when the facts and plan support them; do not force a lifestyle scene onto a product-detail, count, dimension, or care-proof task that needs a clearer evidentiary composition.

People may appear in Visual Master scenario examples and secondary-image scenes when the plan and facts support the use. They are never permitted in the Amazon main image. People must not obscure the product, imply an unsupported audience, use condition, safety claim, or performance result, or appear as a non-included product component.

The Visual Master must establish palette, background treatment, contrast, warmth, lighting direction/softness/shadow treatment, camera distance/angle/depth of field/product scale, material realism, scene/prop/human/whitespace rules, and secondary-image text placement/scale/contrast/typography, hierarchy, and text-safe zones. It must also visibly choose one text-presentation treatment that suits the product and plan: for example, open whitespace, an integrated surface, a restrained label, or a card/callout. Do not default to boxed copy; use cards, borders, bubbles, or callouts only when that treatment is deliberately chosen in the approved Visual Master.

Define typography as reusable roles rather than an image-by-image guess: headline, supporting copy, and emphasis must each have an approved character, weight, color, relative scale, alignment, and spacing. Extract compact reusable `visual-system tokens` from this system.

Treat the upstream `图片解析摘要`, `产品卖点分析`, and `附图策划` as authoritative for product truth, selling-point priority, sequence, and sales tasks. Do not require the upstream plan to contain a composition, scene, headline, subtitle, or prompt. Stop and ask for an upstream-plan revision or clarification only when a task conflicts with the fact lock, cannot support its claim, has no safe proof approach, or duplicates another sales task.

## Internal Fact Lock

Create an internal fact lock before the first image call. Do not show this internal record in the final response.

### Set-level lock

- Marketplace and target language.
- Exact product identity: silhouette, color, material only when evidenced, visible structure, included parts, pack count, and variation.
- Product-state boundaries: the evidenced product configuration and use state permitted for the main image, detail/proof images, and lifestyle/usage images. Do not drift to a different configuration, degree of assembly, degree of use, or implied inclusion merely to make a scene more attractive.
- Allowed claims: only A/B-level facts supplied by the user or directly visible in the product references/`图片解析摘要`.
- Disallowed claims and objects: every prohibition from the upstream plan plus unsupported material, performance, medical, environmental, certification, comparison, warranty, price, promotion, ranking, brand, and competitor content.

### Per-image lock

For the main image and every `附图策划` item, record internally:

- target-language theme and final filename. Name every delivered asset as `<sequence>-<target-language theme>.png`: use `0-<target-language equivalent of Visual Master>` for the Visual Master, `1-<target-language equivalent of Main Image>` for the main image, then the upstream `附图策划` image number for every secondary image. The theme in the filename must use the same target language and script as that image's visible copy; do not mix languages in a filename.
- image type and sales task;
- exact product truth that must be visible;
- approved product state and its evidence source;
- target user/scene and capability shown;
- target-language headline, subtitle, numbers, and emphasis exactly as approved in the Text Master;
- scene props that are permitted but not included in the product;
- prohibited content and the approved Text Master and `visual-system tokens` that its prompt must use.

If a theme is not provided, create one concise theme in the target language that expresses that image's intended message. Use the target-language equivalent of “Visual Master” or “Main Image” where applicable, then apply the required sequence prefix.

## Single Approval Gate

1. Create the internal fact lock and Text Master.
2. Generate and inspect the Visual Master, including its scenario board.
3. Present the Text Master and Visual Master together, then wait for exactly one user approval. The user must be able to assess the proposed scenes, people, product identity, visual system, and text direction before production begins.
4. Do not generate any production main image or secondary image before approval.
5. After approval, generate the main image and every planned secondary image in the approved sequence. Do not create a sample package, seek a second approval, or pause for user review between assets.

Internal compliance, identity, dimension, and direct-text checks remain mandatory during production but are not user approval gates. Ask for direction only when a fact, upstream-plan, or compliance conflict makes safe production impossible. After delivery, make revisions only to the image(s) and change(s) the user specifically requests.

## Marketplace Adaptation

Use restrained, product-specific local ecommerce conventions. Do not stereotype a nationality, invent survey findings, or claim to have researched current consumer trends. When the brief provides no market-specific evidence, use a conservative, clean marketplace baseline. For example, prioritize direct benefit and credible use context where appropriate for US shopping images; prioritize ordered composition, detail, and whitespace where appropriate for Japanese shopping images.

The marketplace controls the visible copy language, theme-file language, scene cues, typography character, and visual emphasis. It never overrides the product fact lock or Amazon main-image contract.

## Main Image Contract

Generate the main image only after the Text Master and Visual Master have received the single required user approval, then continue through the approved full production sequence.

- Use a pure white, seamless background.
- Compose for a 1:1 canvas and deliver at exactly 1500 × 1500 px.
- Show only the accurate sellable product and its evidenced included components/quantity.
- Center the product clearly; use a practical Amazon catalogue crop with the product prominent and fully recognizable.
- Use no text, lettering, numbers, badges, logos, borders, props, hands, people, packaging, gifts, scenery, watermarks, or decorative graphics.
- Do not show a non-included object, even as an implied free gift or bundle.
- Preserve the actual product’s visible silhouette, color, scale relationship, structure, and construction from the reference images.

The Amazon main-image contract overrides visual-system tokens, especially background treatment. The main image remains pure white and may use only compatible product-identity and lighting constraints from the visual system; shared visual-system tokens apply to secondary images.

Prompt the main image as a product catalogue image and explicitly repeat every no-text/no-prop constraint. A beautiful lifestyle scene is not a substitute for a compliant main image.

## Secondary Image Contract

Generate one secondary image for each `附图策划` item whose `图片类型` is `副图`, in its planned sequence. The upstream `主图` item maps only to the separate main-image workflow and must not be generated again as a secondary image. Each secondary image must prove a distinct buyer-relevant point rather than restating the main image.

For each prompt:

1. Start with the approved Text Master entry for that image: its sales task, `buyer_question`, `evidence_type`, copy, planned scene/props, prohibited content, and product fact lock.
2. Compose for a 1:1 canvas and deliver at exactly 1500 × 1500 px.
3. Use the scene, target user, product capability, permitted props, and exclusions approved in the Text Master, while preserving the upstream plan item's sales task and evidence boundary. Demonstrate one distinct buyer-relevant point, and answer its `buyer_question` through the stated `evidence_type`.
4. Apply the same approved `visual-system tokens`, text-presentation treatment, and typography roles from the Visual Master. Do not introduce cards, borders, bubbles, callouts, or a new font character that the approved master does not use. Use a product-appropriate usage scene with people when it best proves the approved task; otherwise use the factual proof composition required by that task.
5. Quote the supplied headline, subtitle, number/unit, and emphasis verbatim in the target language. For non-Latin text, supply the exact text once in quotation marks and once character-by-character when that improves rendering fidelity.
6. Specify a clean text-safe region, high readable contrast, no extra text, no logo, no watermark, and no invented badge or data visualization.
7. State clearly that scene props are not included when the plan requires such clarification. Do not add this clarification if it is not in the approved copy.
8. Retain inherited copy exactly, use the shared `visual-system tokens`, and do not introduce unsupported or duplicate claims.

Do not use a secondary image to make an unsupported claim merely because it is visually persuasive. A lifestyle scene can show plausible use only when the plan and fact lock support that use. Props and people may clarify fact-supported use, but must not obscure the product or imply extra inclusion, a restricted audience, safety, compatibility, or performance that is not evidenced.

## Direct-Model Text Validation

The user has chosen direct in-image text generation. Do not replace it with programmatic text overlay unless the user changes that instruction.

After each secondary image is generated, inspect it with `view_image` and check:

- every required headline, subtitle, number/unit, and emphasis is present exactly and in the target script;
- there are no misspellings, missing characters, Latin-script substitutions, unreadable glyphs, accidental text, or watermarks;
- text is sufficiently large, legible, contrasted, and not cut off;
- typography, text placement, and text-presentation treatment match the approved Visual Master roles;
- the saved delivery copy is exactly 1500 × 1500 px;
- the image still follows its approved Text Master entry, `buyer_question`, `evidence_type`, fact lock, prohibited-content list, and shared visual-system tokens;
- it demonstrates one distinct buyer-relevant point and answers its buyer question through the stated evidence type;
- inherited copy is retained exactly and there are no unsupported or duplicate claims.

Any failed text check fails that asset. Do not call it final, silently substitute an explanation, or deliver it with an error label.

## Repair Loop

Use this order:

1. Create and inspect the Text Master and Visual Master, then obtain the one required user approval.
2. Generate and internally inspect the main image and each secondary image in the approved sequence, without another user review gate.
3. Run the set-level internal review for product identity, marketplace language, visual-system consistency, scenario appropriateness, scene-led coverage, proof-led justification, repeated isolated-product layouts, duplicate selling points, Amazon main-image compliance, and plan coverage.

When an asset fails, route the correction to the `最小责任层` (minimum responsible layer) and keep all passing assets unchanged:

- Text/copy or typography failures: revise the exact text constraints and role-specific type treatment, then regenerate only that image. When an already-approved in-set asset is used as a typography reference, use it only to match the shared typography system, not to copy its product composition or sales task.
- Product identity failures: strengthen product references/fact lock and regenerate only that image.
- Composition/hierarchy failures: revise the affected prompt from its approved Text Master entry without changing the approved sales task or copy.
- Visual-system consistency failure in an individual secondary image: revise the visual specification and visual-system tokens as necessary, then regenerate only the affected secondary asset.
- Set-wide style failures: revise the visual specification and regenerate only affected images.
- Sales-task duplication, missing proof, or unsupported plan claims: return to upstream `附图策划` for clarification or revision.

Allow at most two repair cycles per failed asset where technically applicable. If a failed Visual Master changes the set-level visual system, regenerate all affected listing images; otherwise retain valid assets. If an image still cannot meet the fact, compliance, or readable-copy requirement after two repairs, stop and ask the user how to proceed. Never present it as a final asset.

## Final Output Contract

When all assets pass, save 1500 × 1500 px project-bound images in the workspace under an `output/amazon-listing-images/` folder without overwriting existing files. Every final filename must use the fixed format `<sequence>-<target-language theme>.png`: `0-` for the Visual Master, `1-` for the main image, and each upstream secondary-image number thereafter. The filename theme must be in the same language and script as the image's customer-facing copy; for example, Japanese copy uses a Japanese theme name. Do not use a different-language theme or omit the sequence prefix.

Maintain an internal final-asset manifest mapping every approved sequence to exactly one final filename. The delivery folder must contain one selected final asset per sequence only. Store exploratory, failed, and superseded generations separately under `output/amazon-listing-images/revisions/` with versioned filenames; never present multiple versions of the same planned image as final deliverables.

The final user-facing response must contain only these image assets, in this order:

1. The Visual Master.
2. The main image.
3. Every secondary image in the upstream-plan order.

Do not add explanatory prose, a numbered list, prompt set, filenames, or any other metadata to that final response.

## Common Mistakes

| Mistake | Required correction |
| --- | --- |
| Generating each secondary image in a different aesthetic | Generate and obtain approval of one Visual Master, then repeat its visual-system tokens in every prompt. |
| Generating production images before scenario direction is approved | Present the Text Master and Visual Master together; wait for the single approval before production. |
| Treating product references as loose inspiration | Re-read the fact lock and preserve visible product identity exactly. |
| Letting a style reference change the sellable product | Apply the Reference Role Contract: style controls art direction only; identity and component references control product truth. |
| Changing the product's displayed state from one image to another without evidence | Re-read the product-state boundaries and regenerate the affected image in its approved configuration/use state. |
| Adding boxes, badges, or unrelated font treatments to copy | Follow the approved Visual Master's text-presentation treatment and typography roles; regenerate only the inconsistent image. |
| Putting a lifestyle prop in the main image | Regenerate the main image on pure white with only the sellable product. |
| Repeating “product + solid-color background” across scene-worthy secondary tasks | Reclassify each image as `scene-led` or `proof-led`; regenerate every scene-worthy task as a photorealistic environment or use moment and retain isolated layouts only where the proof task requires them. |
| Shipping garbled Japanese or other localized copy | Fail and regenerate only that image; do not explain it away. |
| Adding a claim to make an image more persuasive | Remove it unless it has A/B evidence in the upstream Listing material. |
| Producing a written handoff together with images | Deliver only the Visual Master, main image, and planned secondary images. |
| Naming files only by theme, or using a different-language filename theme | Name each final file `<sequence>-<target-language theme>.png`; use `0-` for Visual Master, `1-` for main image, and the upstream secondary-image number thereafter. |
| Leaving multiple candidate versions in the final delivery folder | Use the final-asset manifest; retain one final file per sequence and move other versions to `revisions/`. |
