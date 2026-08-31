# Listing TXT Output Template

Write all final deliverables as UTF-8 TXT files under the current task's `output/` directory. Do not emit the complete deliverable as a single chat Markdown response. Do not prefix every line with `*`.

## `output/listing.txt`

Use only these sections:

```text
## 图片解析摘要

## Title
标题文本

## Item Highlight
亮点短语, 亮点短语, 规格/适用范围, 场景/兼容/材质信息

## Bullet Points
1. 【核心卖点】：功能 + 益处描述
2. 【核心卖点】：功能 + 益处描述
3. 【核心卖点】：功能 + 益处描述
4. 【核心卖点】：功能 + 益处描述
5. 【核心卖点】：功能 + 益处描述

## Description

## Search Terms

## 生成检查
```

## `output/main-secondary-images.txt`

Keep the verified selling-point analysis and image plan in one file:

```text
## 产品卖点分析

### 产品全部卖点

### 核心卖点

## 附图策划
```

Include 1 main image and at least 7 secondary images. List every A/B-evidenced selling point, merge semantic duplicates, and identify 1–2 core selling points with selection reasons. Do not include a creative brief, composition suggestions, on-image-copy direction, exact image copy, or generation prompts; the downstream listing-image skill owns those decisions.

## `output/aplus-plan.txt`

```text
## A+ 整体策划

### 产品全部卖点

### 核心卖点

### A+ 1

...

### A+ 7
```

Include exactly 7 plans numbered A+ 1 through A+ 7.

Do not output separate sections named `关键词整理与排序摘要` or `合规与优化检查`.

`图片解析摘要` must be generated only from the first image analysis and reused by downstream image-design skills. Include appearance, color, material, structure, accessories, visible functions, usage mode, suitable scenes, and visual details that must stay consistent during image design.

附图策划 must contain at least 8 image-plan items. Build them from the specific product's features, scenarios, parameters, material, size, functions, user pain points, target users, usage steps, compatibility, and packaging facts. Each item states its image number/type, single sales task, core purpose, mapped selling point/parameter/pain point or verified QA, supporting A/B fact and source, compliance risk, and algorithm task. It does not prescribe composition or on-image copy.

Secondary image plans may name a fact-supported target user, use moment, or buyer concern as scene intent. They must not prescribe the actual scene image, camera, composition, props, visual style, or text placement; the downstream listing-image skill owns those execution decisions.

`A+ 整体策划` must contain exactly 7 A+ image-plan items, numbered A+ 1 through A+ 7. Before the modules, list 产品全部卖点 and identify 1–2 核心卖点. Use this fixed sequence:

1. `A+ 1`: overview of all verified selling points.
2. From `A+ 2`: one image for each core selling point, using one or two images according to the number selected.
3. Every remaining image: a scene-and-copy answer to one verified, non-duplicate QA concern not already answered by a core-selling-point image.

General selling points may appear in `A+ 1` but do not receive standalone images from `A+ 2` onward. 核心卖点对应的问答 must be excluded from QA modules even when phrased differently. If verified QA exceeds the remaining slots, prioritize decision-critical questions with the strongest evidence and clearest scene proof. If it is insufficient, add fact-derived question-and-answer decision modules about suitability, use, compatibility, package contents, care, or limitations; identify them as fact-derived rather than externally collected QA, and do not disguise a general selling point as a QA module.

For each A+ image, provide its module type, role, core objective, visual composition or scene, target-marketplace exact headline and explanatory copy, relationship to the main/secondary images, new information added, required facts or source materials, and compliance risks. Core modules map exactly one selected core selling point. QA modules include the customer question, direct verified answer, evidence source, and a truthful scene that demonstrates the answer. Never adopt unsupported competitor answers.
Alexa for Shopping/Rufus Q&A handling:

- Treat Alexa for Shopping and Rufus as the same Amazon AI shopping assistant system. US marketplace materials may say Alexa for Shopping; Japan marketplace materials may say Rufus.
- Use Q&A files mainly to identify customer concerns, purchase objections, common scenarios, comparison dimensions, answer structure, and GEO/Rufus semantic coverage opportunities.
- Do not treat competitor answers as product facts. Any function, material, specification, size, compatibility, effect, certification, warranty, pack count, audience, or use case from competitor answers must be verified against the user's product facts and first image-analysis summary before it appears in final Listing copy.
- If a Q&A answer conflicts with the user's product facts or is not supported by user-provided materials, do not write it as a selling point. Use it only as a customer concern, missing-information note, or image-planning angle when appropriate.
## Internal Quality Contract

Before drafting, create an internal algorithm task sheet for every core selling point and image topic: verified product fact and evidence level, keyword and field role, COSMO chain (target user -> use scenario -> pain point -> product capability -> tangible benefit), verified Alexa for Shopping/Rufus question and answer, Listing placement, image/A+ placement, limitation, and compliance risk. Do not expose the full sheet in the three final TXT files.

Use evidence levels: A = user-provided product facts, manuals, reports, or verifiable parameter documents; B = directly visible first-image-analysis facts; C = reasonable but unproven inference; D = keywords, QA, competitor answers, or competitor analysis; E = unsupported or conflicting. Only A/B facts may become product claims. C is internal clarification only; D identifies intent only; E is excluded.

Use a keyword role ledger after five gates: basic cleanup, fact-conflict removal, legal/compliance screening, relevance layering, and COSMO/QA seed selection. Assign each retained term a primary role in Title, Item Highlight, Bullet Points, Description, Search Terms, image planning, or A+; do not repeat terms without purpose.

Generate with a writer pass, then validate with a separate judge pass. The judge checks evidence, keyword roles, COSMO chains, verified QA, marketplace rules, length, deduplication, image/A+ task coverage, compliance, and unsupported claims. Repair only failed modules and revalidate for up to two cycles. If blocked by missing evidence or data, state the reason in the final generation check rather than inventing details.

For image plans, every secondary image must identify its algorithm task: target user or scenario, capability proved, keyword/COSMO intent served, relevant verified QA fact when applicable, and evidence source. Across the fixed A+ module order, the content should still help the buyer decide suitability, understand the core capability, verify conditions, and resolve purchase questions; this decision objective does not change or reorder the required module types.
Keyword relevance labels:

- `核心属性关键词-高相关`: keyword includes product name or alias plus clear selling point, scenario, function, parameter, material, size, or other narrowing attribute.
- `大词泛词-相关`: keyword mainly contains product name or alias without clear selling point, scenario, function, or parameter.
- `泛属性关键词-低优先级`: keyword contains product name or alias plus vague attributes that do not narrow search intent, such as fashion. Exclude by default from visible Listing and Search Terms.

Hard limits:

- US Title: at least 65 and no more than 75 characters, including spaces. JP Title: at least 50 and no more than 75 characters. Rewrite before final output if outside the target marketplace range.
- US Item Highlight: at least 100 and no more than 125 characters, including spaces. JP Item Highlight: at least 70 and no more than 125 characters. Rewrite before final output if outside the target marketplace range.
- Bullet Points: exactly five numbered bullets. US bullets must be 200-250 characters each. JP bullets must be 150-250 characters each. Rewrite before final output if any bullet is outside the target marketplace range.
- Description: at least 1000 characters including spaces for every marketplace. It must naturally embed precise long-tail keywords that match verified product facts. When a provided Alexa for Shopping/Rufus Q&A contains product-supported answers, embed the verified customer-question intent and answer in the Description; never copy or adopt unsupported competitor claims. Rewrite before final output if the Description is under 1000 characters or omits required long-tail keywords or verified Q&A content.
- Search Terms: lowercase, spaces only, no punctuation, no duplicate words, no Title or Item Highlight repetition, no more than 250 bytes and no more than 250 characters.
- A+ planning: exactly 7 numbered image plans. `A+ 1` covers all verified selling points, the next one or two modules each cover one core selling point, and all remaining modules answer non-core QA concerns with scene and copy. General selling points do not receive standalone modules after `A+ 1`.
- Character counts are for internal validation only. Do not append character counts after Title, Item Highlight, Bullet Points, Description, Search Terms, or image-plan content in the final output.
- Item Highlight is a supplement to Title, not a second title that repeats the same parameters. It must not reuse product attributes already present in Title, including exact repeats, inflections, synonyms, translated variants, or reordered attribute phrases. Product attributes include material, color, size, specification, capacity, weight, quantity, pack count, shape, style, compatible model, target object, usage scene, audience, installation method, core function, and functional parameters. Generic product type words may repeat only when needed for readability.

Final self-check:

- Complete internal length, deduplication, and compliance checks without showing per-field character counts in the final output.
- Internally confirm that Item Highlight contains no product attributes already used in Title; rewrite Item Highlight before final output if any overlap exists.
- Internally confirm that Description is at least 1000 characters, contains product-accurate precise long-tail keywords, and covers every relevant Q&A answer supported by the user's product facts. Do not show the character count in final output.
- Internally confirm that A+ planning contains exactly 7 distinct, sequential image plans; lists all selling points and 1–2 core selling points; uses `A+ 1` as the complete overview; gives each core selling point one image; excludes core-selling-point questions from QA modules; and maps the remaining verified Q&A without importing unsupported competitor claims.
- Internally confirm that every product claim comes from A/B evidence, every core selling point has a COSMO chain, every keyword has a purposeful field role, and all failed checks have completed the independent-validator repair loop or are explicitly blocked in the final generation check.
- Do not promise ranking, traffic, conversion, sales, or boom sales; Listing copy cannot control price, inventory, fulfillment, reviews, advertising, historical sales, or category competition.
- If Title or Item Highlight cannot reach the lower bound without inventing facts, explain the reason in `## 生成检查`.
