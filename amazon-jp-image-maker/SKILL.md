---
name: amazon-jp-image-maker
description: Analyze Amazon.co.jp competitor product links and user product materials to create Japanese Amazon main/sub image sets. Use when the user asks to extract Amazon Japan listing titles, images, bullet copy, A+ content, specs, reviews, advantages, recommend three image styles, or generate new compliant Amazon Japan listing images from competitor references. Triggers include 亚马逊日本站主图, 副图, 竞品链接, Amazon.co.jp 商品图, 日本站图片生成, and extracting competitor listing information for image generation.
---

# Amazon JP Image Maker

Create a new Amazon.co.jp listing image set from competitor listing research and the user's own product materials. Use only the Codex in-app browser for page access; do not use Chrome or any other local browser.

## Required Tools

- For page access, use the `browser:control-in-app-browser` skill and its in-app browser only.
- For bitmap image generation or edits, use the `imagegen` skill/tool.
- Do not use the user's local Chrome session, saved Chrome cookies, or any other local browser.

## Workflow

1. Confirm inputs: competitor Amazon.co.jp link(s), user's product images/materials, product facts, preferred image count if provided, and any brand/style constraints.
2. Open each competitor link in the in-app browser. If login, region confirmation, captcha, or blocked content appears, ask the user to complete it inside the in-app browser and continue after they confirm.
3. Extract visible listing information. Prefer `scripts/extract_amazon_jp_listing.mjs` for repeatable extraction after the page is open in the in-app browser:
   - title, brand/store, price, rating, review count, variations, coupons/promotions if relevant
   - main image, sub images, video thumbnails, A+ images, and page screenshots when image URLs are unreliable
   - bullet points, product description, A+ visible copy, specs/detail table, Q&A/review snippets visible on page
4. Keep extraction notes in memory by default. Do not create output folders, reports, prompt files, or image-plan files unless the user explicitly asks for saved files.
5. Analyze the competitor listing:
   - product positioning, target audience, core promise, primary buying reasons
   - image-by-image role in the group, information hierarchy, visual hooks, scenario choices
   - advantages implied by title, bullets, specs, images, reviews, and A+ content
6. Recommend exactly three product-fit image styles before generating:
   - include style name, visual keywords, color/background direction, best-fit image roles, why it fits, and risks
   - mark one as the recommended default
   - if the user does not choose a style, continue with the recommended default
7. Output a concise in-chat image plan and stop for user confirmation before Image Gen:
   - one main image and normally 5-7 sub images unless the user asks otherwise
   - all Amazon main/sub images must default to a 1500 x 1500 px square canvas
   - keep each image line short: image number, role, key selling point, composition, and Japanese text if any
   - include only essential compliance or missing-input notes
   - do not output long prompts unless the user asks
8. After the user confirms the plan, directly call Image Gen for the confirmed images. Generate final images only from the user's product assets or clearly permissible generated scene elements. If user product assets are missing or insufficient, ask for the missing product image(s) before generating.
9. Deliver generated images in chat with short per-image labels. Save files only when the user explicitly requests a saved package or workspace output.

## Extraction Guidance

Use DOM inspection and screenshots together. Amazon pages vary; prefer visible truth over brittle selectors.

### Reusable extraction script

After opening a product page in the in-app browser and selecting the tab, use the bundled extractor first:

```js
const { extractFromBrowserTab } = await import("<skill path>/scripts/extract_amazon_jp_listing.mjs");
const listing = await extractFromBrowserTab(tab, { timeoutMs: 8000 });
nodeRepl.write(JSON.stringify(listing, null, 2));
```

Use the JSON result as working context. Save it only if the user explicitly requests files. The extractor returns partial data with `extractionWarnings` when Amazon blocks or slows part of the page; mention important warnings briefly instead of inventing missing facts.

For saved page HTML, run:

```bash
node scripts/extract_amazon_jp_listing.mjs --html page.html --url "<Amazon URL>" --out listing.json
```

If the script times out or returns incomplete data, continue with targeted DOM reads and screenshots. Ask the user to complete captcha, login, or region prompts inside the in-app browser when needed.

Helpful targets to inspect include `#productTitle`, `#bylineInfo`, `#landingImage`, `#altImages`, `#feature-bullets`, `#productDescription`, `#aplus`, `#productDetails_techSpec_section_1`, `#productDetails_detailBullets_sections1`, rating/review blocks, variation swatches, and thumbnail image attributes such as `src`, `data-old-hires`, and `data-a-dynamic-image`.

When images are lazy-loaded or URLs are low resolution, click thumbnails in the in-app browser and capture the displayed gallery image or screenshot. Preserve competitor images as references only; do not place them directly into generated outputs.

## In-Chat Output Shape

Default response before generation must be short and text-only, not a file package. Write in this order:

1. `竞品要点`: 1-3 bullets, only facts that were extracted or confirmed.
2. `推荐风格`: exactly three short style options; mark one as recommended.
3. `图片方案`: main image plus 5-7 sub images, one short line per image.
4. `待确认`: only blockers that affect generation; end by asking the user to confirm the plan.

After user confirmation, skip another long report and call Image Gen directly. Do not create Markdown, JSON, prompt, or report files unless the user asks for files.

Read `references/amazon-jp-image-workflow.md` before planning the image set. Read `references/image-similarity-boundaries.md` before writing prompts or generating images.

## Compliance Rules

- Do not copy competitor images, brand names, logos, packaging design, watermarks, identifiable people, protected illustrations, or exact layouts.
- Do not represent the competitor product as the user's product.
- Do not invent unsupported certifications, rankings, technical specs, materials, safety claims, or performance claims.
- Main image should keep the product as the clear subject and avoid decorative, misleading, or unsupported elements.
- Export Amazon main/sub images at 1500 x 1500 px unless the user explicitly requests another size.
- If the requested similarity would be too close, explain the boundary and provide a safer visual direction.
