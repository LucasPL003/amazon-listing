#!/usr/bin/env node
import { readFile, writeFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';

function cleanText(value) {
  return decodeHtml(String(value ?? ''))
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function decodeHtml(value) {
  const named = {
    amp: '&',
    apos: "'",
    gt: '>',
    lt: '<',
    nbsp: ' ',
    quot: '"',
  };
  return String(value ?? '').replace(/&(#x?[0-9a-f]+|[a-z]+);/gi, (match, entity) => {
    const key = entity.toLowerCase();
    if (key[0] === '#') {
      const code = key[1] === 'x' ? Number.parseInt(key.slice(2), 16) : Number.parseInt(key.slice(1), 10);
      return Number.isFinite(code) ? String.fromCodePoint(code) : match;
    }
    return Object.prototype.hasOwnProperty.call(named, key) ? named[key] : match;
  });
}

function attrMap(tag) {
  const attrs = {};
  const pattern = /([:\w-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))/g;
  for (const match of tag.matchAll(pattern)) {
    attrs[match[1].toLowerCase()] = decodeHtml(match[2] ?? match[3] ?? match[4] ?? '');
  }
  return attrs;
}

function firstMatch(html, pattern) {
  return pattern.exec(html)?.[1] ?? null;
}

function textById(html, id) {
  const pattern = new RegExp(`<[^>]+id=["']${escapeRegExp(id)}["'][^>]*>([\\s\\S]*?)(?:<\\/[^>]+>)`, 'i');
  return cleanText(firstMatch(html, pattern));
}

function sectionById(html, id) {
  const start = html.search(new RegExp(`<[^>]+id=["']${escapeRegExp(id)}["']`, 'i'));
  if (start < 0) return '';
  return html.slice(start, start + 20000);
}

function firstClassText(html, className) {
  const pattern = new RegExp(`<[^>]+class=["'][^"']*\\b${escapeRegExp(className)}\\b[^"']*["'][^>]*>([\\s\\S]*?)<\\/[^>]+>`, 'i');
  return cleanText(firstMatch(html, pattern));
}

function escapeRegExp(value) {
  return String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function parseDetails(html) {
  const details = [];
  const sections = [
    sectionById(html, 'productDetails_techSpec_section_1'),
    sectionById(html, 'productDetails_detailBullets_sections1'),
  ].join('\n');
  const rowPattern = /<tr[\s\S]*?<\/tr>/gi;
  for (const rowMatch of sections.matchAll(rowPattern)) {
    const row = rowMatch[0];
    const name = cleanText(firstMatch(row, /<th[^>]*>([\s\S]*?)<\/th>/i));
    const value = cleanText(firstMatch(row, /<td[^>]*>([\s\S]*?)<\/td>/i));
    if (name || value) details.push({ name, value });
  }
  const bulletDetails = sectionById(html, 'detailBullets_feature_div');
  for (const li of bulletDetails.matchAll(/<li[\s\S]*?<\/li>/gi)) {
    const text = cleanText(li[0]);
    if (text) details.push({ name: null, value: text });
  }
  return uniqueObjects(details, (item) => `${item.name ?? ''}:${item.value ?? ''}`).slice(0, 80);
}

function parseBullets(html) {
  const section = sectionById(html, 'feature-bullets');
  const bullets = [];
  for (const match of section.matchAll(/<li[\s\S]*?<\/li>/gi)) {
    const text = cleanText(match[0]);
    if (text) bullets.push(text);
  }
  return [...new Set(bullets)].slice(0, 30);
}

function parseImages(html) {
  const images = [];
  for (const match of html.matchAll(/<img\b[^>]*>/gi)) {
    const attrs = attrMap(match[0]);
    const candidates = [];
    if (attrs['data-a-dynamic-image']) {
      try {
        const dynamic = JSON.parse(attrs['data-a-dynamic-image']);
        for (const [url, size] of Object.entries(dynamic)) {
          candidates.push({
            alt: attrs.alt || null,
            height: Array.isArray(size) ? size[1] ?? null : null,
            source: 'data-a-dynamic-image',
            url,
            width: Array.isArray(size) ? size[0] ?? null : null,
          });
        }
      } catch {
        // Ignore malformed Amazon dynamic image payloads and keep other candidates.
      }
    }
    for (const [name, source] of [
      ['data-old-hires', 'data-old-hires'],
      ['src', 'src'],
    ]) {
      if (attrs[name]) {
        candidates.push({
          alt: attrs.alt || null,
          height: null,
          source,
          url: attrs[name],
          width: null,
        });
      }
    }
    images.push(...candidates);
  }
  return uniqueObjects(images, (item) => item.url)
    .filter((item) => /^https?:\/\//i.test(item.url))
    .slice(0, 80);
}

function uniqueObjects(items, keyFn) {
  const seen = new Set();
  const result = [];
  for (const item of items) {
    const key = keyFn(item);
    if (!key || seen.has(key)) continue;
    seen.add(key);
    result.push(item);
  }
  return result;
}

export function extractFromHtml(html, { url = null } = {}) {
  const title = textById(html, 'productTitle') || cleanText(firstMatch(html, /<title[^>]*>([\s\S]*?)<\/title>/i));
  const priceSection = sectionById(html, 'corePrice_feature_div') || html;
  const ratingSection = sectionById(html, 'acrPopover') || html;
  return {
    url,
    title,
    brand: textById(html, 'bylineInfo') || textById(html, 'brand'),
    price: firstClassText(priceSection, 'a-offscreen') || firstClassText(html, 'a-offscreen'),
    rating: firstClassText(ratingSection, 'a-icon-alt') || firstClassText(html, 'a-icon-alt'),
    reviewCount: textById(html, 'acrCustomerReviewText'),
    availability: textById(html, 'availability'),
    coupon: textById(html, 'couponText') || firstClassText(html, 'couponLabelText'),
    variations: [],
    bullets: parseBullets(html),
    details: parseDetails(html),
    images: parseImages(html),
    extractionWarnings: [],
  };
}

function pageExtractor() {
  const clean = (value) => String(value ?? '').replace(/\s+/g, ' ').trim();
  const text = (selector) => clean(document.querySelector(selector)?.textContent);
  const attr = (selector, name) => document.querySelector(selector)?.getAttribute(name) || null;
  const rows = (selector) => Array.from(document.querySelectorAll(selector));
  const images = [];
  for (const img of rows('#altImages img, #imageBlock img, #landingImage, img')) {
    const dynamicRaw = img.getAttribute('data-a-dynamic-image');
    if (dynamicRaw) {
      try {
        const dynamic = JSON.parse(dynamicRaw);
        for (const [url, size] of Object.entries(dynamic)) {
          images.push({
            alt: img.getAttribute('alt') || null,
            height: Array.isArray(size) ? size[1] ?? null : null,
            source: 'data-a-dynamic-image',
            url,
            width: Array.isArray(size) ? size[0] ?? null : null,
          });
        }
      } catch {}
    }
    for (const [name, source] of [['data-old-hires', 'data-old-hires'], ['src', 'src']]) {
      const url = img.getAttribute(name);
      if (url) {
        images.push({
          alt: img.getAttribute('alt') || null,
          height: img.naturalHeight || null,
          source,
          url,
          width: img.naturalWidth || null,
        });
      }
    }
  }
  const seen = new Set();
  const uniqueImages = images.filter((item) => {
    if (!item.url || seen.has(item.url)) return false;
    seen.add(item.url);
    return true;
  });
  return {
    url: location.href,
    title: text('#productTitle') || document.title,
    brand: text('#bylineInfo') || text('#brand'),
    price: text('#corePrice_feature_div .a-price .a-offscreen') || text('.a-price .a-offscreen'),
    rating: text('#acrPopover .a-icon-alt') || text('.reviewCountTextLinkedHistogram .a-icon-alt'),
    reviewCount: text('#acrCustomerReviewText'),
    availability: text('#availability'),
    coupon: text('#couponText') || text('.couponLabelText'),
    variations: rows('#variation_color_name li, #variation_size_name li, .twisterSwatchWrapper, .swatchAvailable')
      .map((el) => clean(el.textContent))
      .filter(Boolean)
      .slice(0, 40),
    bullets: rows('#feature-bullets li, #feature-bullets .a-list-item')
      .map((el) => clean(el.textContent))
      .filter(Boolean)
      .slice(0, 40),
    details: rows('#productDetails_techSpec_section_1 tr, #productDetails_detailBullets_sections1 tr')
      .map((tr) => ({
        name: clean(tr.querySelector('th')?.textContent),
        value: clean(tr.querySelector('td')?.textContent),
      }))
      .filter((row) => row.name || row.value)
      .slice(0, 80),
    images: uniqueImages.slice(0, 80),
    extractionWarnings: [],
  };
}

export const browserExtractorSource = `(${pageExtractor.toString()})()`;

async function withTimeout(label, promise, timeoutMs, warnings) {
  let timeoutId;
  const timedOut = Symbol('timed-out');
  const timeout = new Promise((resolve) => {
    timeoutId = setTimeout(() => resolve(timedOut), timeoutMs);
  });
  try {
    const value = await Promise.race([promise, timeout]);
    if (value === timedOut) {
      warnings.push(`${label} timed out after ${timeoutMs} ms`);
      return null;
    }
    return value;
  } catch (error) {
    warnings.push(`${label} failed: ${error.message}`);
    return null;
  } finally {
    clearTimeout(timeoutId);
  }
}

export async function extractFromBrowserTab(tab, { timeoutMs = 8000 } = {}) {
  const result = {
    url: null,
    title: null,
    brand: null,
    price: null,
    rating: null,
    reviewCount: null,
    availability: null,
    coupon: null,
    variations: [],
    bullets: [],
    details: [],
    images: [],
    extractionWarnings: [],
  };
  const fieldTimeoutMs = Math.min(timeoutMs, 3000);
  result.title = await withTimeout('title read', tab.title(), fieldTimeoutMs, result.extractionWarnings);
  result.url = await withTimeout('url read', tab.url(), fieldTimeoutMs, result.extractionWarnings);

  const pageData = await withTimeout(
    'page extraction',
    tab.playwright.evaluate(browserExtractorSource, undefined, { timeoutMs }),
    timeoutMs + 1000,
    result.extractionWarnings,
  );
  if (pageData) {
    return {
      ...result,
      ...pageData,
      title: pageData.title || result.title,
      url: pageData.url || result.url,
      extractionWarnings: [...result.extractionWarnings, ...(pageData.extractionWarnings ?? [])],
    };
  }
  return result;
}

function parseArgs(argv) {
  const args = { html: null, out: null, url: null };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--html') args.html = argv[++i];
    else if (arg === '--out') args.out = argv[++i];
    else if (arg === '--url') args.url = argv[++i];
    else if (arg === '--help' || arg === '-h') args.help = true;
    else throw new Error(`Unknown argument: ${arg}`);
  }
  return args;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.html) {
    console.log('Usage: extract_amazon_jp_listing.mjs --html page.html [--url URL] [--out listing.json]');
    return args.help ? 0 : 2;
  }
  const html = await readFile(args.html, 'utf8');
  const listing = extractFromHtml(html, { url: args.url });
  const json = `${JSON.stringify(listing, null, 2)}\n`;
  if (args.out) await writeFile(args.out, json, 'utf8');
  else process.stdout.write(json);
  return 0;
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? '').href) {
  main().then((code) => {
    process.exitCode = code;
  }).catch((error) => {
    console.error(error.stack || error.message);
    process.exitCode = 1;
  });
}
