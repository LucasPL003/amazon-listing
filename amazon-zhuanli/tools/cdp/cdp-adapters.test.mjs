import test from "node:test";
import assert from "node:assert/strict";
import { chromium } from "playwright-core";

import {
  extractAfterLabel,
  extractAmazonProduct,
  parsePatentRows,
  parseTrademarkRows,
  tableRows,
} from "./cdp-cli.mjs";

const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

test("Amazon and USPTO adapters read only rendered fixture state", async () => {
  const browser = await chromium.launch({
    executablePath: CHROME,
    headless: true,
  });
  try {
    const page = await browser.newPage();
    await page.setContent(`
      <div id="wayfinding-breadcrumbs_feature_div"><a>Office Products</a><a>Mouse Pads</a></div>
      <h1 id="productTitle">Mock Cat Paw Mouse Pad</h1>
      <a id="bylineInfo">Visit the MOCKMARK Store</a>
      <input id="ASIN" value="B0TEST1234">
      <div id="feature-bullets"><li><span class="a-list-item">Ergonomic wrist support</span></li></div>
      <button aria-checked="true">Pink</button>
      <img id="landingImage" src="https://m.media-amazon.com/images/I/mock.jpg">
      <table id="productDetails_detailBullets_sections1"><tr><th>Manufacturer</th><td>Mock Inc</td></tr></table>
    `);
    const product = await extractAmazonProduct(page);
    assert.equal(product.title, "Mock Cat Paw Mouse Pad");
    assert.equal(product.pageAsin, "B0TEST1234");
    assert.equal(product.specifications.Manufacturer, "Mock Inc");
    assert.deepEqual(product.selectedVariants, ["Pink"]);

    await page.setContent(`
      <table><tr><td>MOCKMARK</td><td>Serial Number 78787878</td><td>Mock Inc</td><td>Live / Registered</td></tr></table>
    `);
    assert.equal(parseTrademarkRows(await tableRows(page))[0].serial_number, "78787878");

    await page.setContent(`
      <table><tr><td>US-D1234567-S</td><td>Cat paw mouse pad</td><td>Issued</td><td>Mock Inc</td></tr></table>
    `);
    assert.equal(parsePatentRows(await tableRows(page))[0].record_number, "US-D1234567-S");

    assert.equal(
      extractAfterLabel("Status\nLIVE\nOwner Name\nMock Inc", ["Status"]),
      "LIVE",
    );
  } finally {
    await browser.close();
  }
});

test("USPTO patent keyword recall uses Basic Search fields instead of quick lookup", async () => {
  const module = await import("./cdp-cli.mjs");
  assert.equal(
    typeof module.submitPatentBasicSearch,
    "function",
    "the patent keyword adapter must expose its Basic Search submission behavior",
  );
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });
  try {
    const page = await browser.newPage();
    await page.setContent(`
      <form id="quick"><input id="quickLookupTextInput"><button id="quickLookupSearchBtn">Search</button></form>
      <form id="basic">
        <select id="searchField1"><option>Everything</option></select>
        <input id="searchText1">
        <select id="searchOperator"><option>AND</option><option>OR</option></select>
        <select id="searchField2"><option>Everything</option></select>
        <input id="searchText2">
        <button id="basicSearchBtn">Search</button>
      </form>
    `);
    await page.locator("form").evaluateAll((forms) => {
      forms.forEach((form) => form.addEventListener("submit", (event) => event.preventDefault()));
    });

    const renderedTerms = await module.submitPatentBasicSearch(
      page,
      "black outline coffee dessert doodle pattern on white sherpa",
    );

    assert.deepEqual(renderedTerms, ["coffee", "sherpa"]);
    assert.equal(await page.locator("#quickLookupTextInput").inputValue(), "");
    assert.equal(await page.locator("#searchText1").inputValue(), "coffee");
    assert.equal(await page.locator("#searchText2").inputValue(), "sherpa");
    assert.equal(await page.locator("#searchOperator").inputValue(), "AND");
  } finally {
    await browser.close();
  }
});

test("TSDR verification expands required sections and rejects loading placeholders", async () => {
  const module = await import("./cdp-cli.mjs");
  assert.equal(typeof module.expandTsdrSections, "function");
  assert.equal(typeof module.parseTsdrRenderedText, "function");
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });
  try {
    const page = await browser.newPage();
    await page.setContent(`
      <div>Mark:\tCRAFTIKIT</div>
      <div>US Serial Number:\t99697586</div>
      <div>Status:\tLIVE/APPLICATION/Under Examination</div>
      <a class="sectionLink" data-kind="goods">Goods and Services</a>
      <a class="sectionLink" data-kind="owner">Current Owner(s) Information</a>
      <div id="details"></div>
      <script>
        document.querySelectorAll('a.sectionLink').forEach((link) => link.addEventListener('click', () => {
          if (link.dataset.kind === 'goods') {
            document.querySelector('#details').insertAdjacentHTML('beforeend', '<div>For:\tBlankets; fleece blankets; throws.</div>');
          } else {
            document.querySelector('#details').insertAdjacentHTML('beforeend', '<div>Owner Name:\tCraftikit</div>');
          }
        }));
      </script>
    `);

    await module.expandTsdrSections(page);
    const parsed = module.parseTsdrRenderedText(await page.locator("body").innerText(), "99697586");
    assert.equal(parsed.ready, true);
    assert.equal(parsed.mark_text, "CRAFTIKIT");
    assert.equal(parsed.case_status, "LIVE/APPLICATION/Under Examination");
    assert.deepEqual(parsed.owners, ["Craftikit"]);
    assert.deepEqual(parsed.goods_services, ["Blankets; fleece blankets; throws."]);
    assert.equal(
      module.parseTsdrRenderedText(`LOADING\n${await page.locator("body").innerText()}`, "99697586").ready,
      false,
    );
  } finally {
    await browser.close();
  }
});
