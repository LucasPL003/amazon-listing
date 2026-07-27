# Listing Output Template

Use this Markdown template for final Amazon Listing output. Do not prefix every line with `*`.

Use only these sections:

```markdown
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

## 附图策划

## A+ 整体策划

## 生成检查
```

Do not output separate sections named `关键词整理与排序摘要` or `合规与优化检查`.

`图片解析摘要` must be generated only from the first image analysis and reused by downstream image-design skills. Include appearance, color, material, structure, accessories, visible functions, usage mode, suitable scenes, and visual details that must stay consistent during image design.

附图策划 must contain at least 8 image-plan items. Build them from the specific product's features, scenarios, parameters, material, size, functions, user pain points, target users, usage steps, compatibility, and packaging facts.

Secondary image plans may use lifestyle or usage-scene images. Choose product-specific scenes that increase purchase desire and match the product category, target buyer, real function, and supported use cases.

`A+ 整体策划` must contain exactly 7 A+ image-plan items, numbered A+ 1 through A+ 7. Build the A+ sequence on the first image-analysis summary and the main/secondary image plan, then deepen the presentation with product positioning, customer pain points, selling-point explanation, scenarios, structure/material/parameters, usage or compatibility details, verified Alexa for Shopping/Rufus Q&A, and purchase-decision information. Do not merely repeat the main or secondary image copy.

For each A+ image, provide its module role, core objective, deepened selling point, visual composition or scene, target-marketplace headline/body-copy direction, relationship to the main/secondary images, new information added, relevant verified Q&A angle when applicable, required product facts or source materials, and compliance risks. If provided Q&A contains product-supported customer concerns, map those concerns and verified answers to the most suitable A+ images. Never adopt unsupported competitor answers.
Alexa for Shopping/Rufus Q&A handling:

- Treat Alexa for Shopping and Rufus as the same Amazon AI shopping assistant system. US marketplace materials may say Alexa for Shopping; Japan marketplace materials may say Rufus.
- Use Q&A files mainly to identify customer concerns, purchase objections, common scenarios, comparison dimensions, answer structure, and GEO/Rufus semantic coverage opportunities.
- Do not treat competitor answers as product facts. Any function, material, specification, size, compatibility, effect, certification, warranty, pack count, audience, or use case from competitor answers must be verified against the user's product facts and first image-analysis summary before it appears in final Listing copy.
- If a Q&A answer conflicts with the user's product facts or is not supported by user-provided materials, do not write it as a selling point. Use it only as a customer concern, missing-information note, or image-planning angle when appropriate.
## Internal Quality Contract

Before drafting, create an internal algorithm task sheet for every core selling point and image topic: verified product fact and evidence level, keyword and field role, COSMO chain (target user -> use scenario -> pain point -> product capability -> tangible benefit), verified Alexa for Shopping/Rufus question and answer, Listing placement, image/A+ placement, limitation, and compliance risk. Do not expose the full sheet in final Markdown.

Use evidence levels: A = user-provided product facts, manuals, reports, or verifiable parameter documents; B = directly visible first-image-analysis facts; C = reasonable but unproven inference; D = keywords, QA, competitor answers, or competitor analysis; E = unsupported or conflicting. Only A/B facts may become product claims. C is internal clarification only; D identifies intent only; E is excluded.

Use a keyword role ledger after five gates: basic cleanup, fact-conflict removal, legal/compliance screening, relevance layering, and COSMO/QA seed selection. Assign each retained term a primary role in Title, Item Highlight, Bullet Points, Description, Search Terms, image planning, or A+; do not repeat terms without purpose.

Generate with a writer pass, then validate with a separate judge pass. The judge checks evidence, keyword roles, COSMO chains, verified QA, marketplace rules, length, deduplication, image/A+ task coverage, compliance, and unsupported claims. Repair only failed modules and revalidate for up to two cycles. If blocked by missing evidence or data, state the reason in the final generation check rather than inventing details.

For image plans, every secondary image must identify its algorithm task: target user or scenario, capability proved, keyword/COSMO intent served, relevant verified QA fact when applicable, and evidence source. A+ must form a coherent decision path: suitability -> reason/product capability -> details and conditions -> purchase decision.
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
- A+ planning: exactly 7 numbered image plans. The sequence must deepen rather than duplicate the main/secondary images and must cover relevant Alexa for Shopping/Rufus concerns that are supported by the user's product facts.
- Character counts are for internal validation only. Do not append character counts after Title, Item Highlight, Bullet Points, Description, Search Terms, or image-plan content in the final output.
- Item Highlight is a supplement to Title, not a second title that repeats the same parameters. It must not reuse product attributes already present in Title, including exact repeats, inflections, synonyms, translated variants, or reordered attribute phrases. Product attributes include material, color, size, specification, capacity, weight, quantity, pack count, shape, style, compatible model, target object, usage scene, audience, installation method, core function, and functional parameters. Generic product type words may repeat only when needed for readability.

Final self-check:

- Complete internal length, deduplication, and compliance checks without showing per-field character counts in the final output.
- Internally confirm that Item Highlight contains no product attributes already used in Title; rewrite Item Highlight before final output if any overlap exists.
- Internally confirm that Description is at least 1000 characters, contains product-accurate precise long-tail keywords, and covers every relevant Q&A answer supported by the user's product facts. Do not show the character count in final output.
- Internally confirm that A+ planning contains exactly 7 distinct, sequential image plans, explains how each plan builds on the main/secondary images, and maps verified Q&A concerns without importing unsupported competitor claims.
- Internally confirm that every product claim comes from A/B evidence, every core selling point has a COSMO chain, every keyword has a purposeful field role, and all failed checks have completed the independent-validator repair loop or are explicitly blocked in the final generation check.
- Do not promise ranking, traffic, conversion, sales, or boom sales; Listing copy cannot control price, inventory, fulfillment, reviews, advertising, historical sales, or category competition.
- If Title or Item Highlight cannot reach the lower bound without inventing facts, explain the reason in `## 生成检查`.
