/**
 * Locale-integrity gate — copy-paste template (Playwright).
 * ----------------------------------------------------------------------------
 * WHY: bundle-parity tests (compare en.json ↔ xx.json keys) are blind to
 * user-facing strings that come from the API / backend / data — those leak
 * into the UI untranslated, or as raw identifiers, and ship unnoticed. This
 * gate scans the *rendered* DOM in a target locale and fails on:
 *   1. raw camelCase/snake_case identifiers shown as labels (e.g. `furnishingCost`)
 *   2. user-facing lines with no target-script characters (untranslated source text)
 *
 * HOW TO ADAPT (4 edits, marked TODO):
 *   1. TARGET_LOCALE_PATH — the route that renders your non-default locale.
 *   2. TARGET_SCRIPT      — the Unicode range of that locale's script.
 *   3. LATIN_ALLOWLIST    — brand names / units that are legitimately Latin.
 *   4. gotoContentRichScreen() — navigate to the DEEP, data-dense screen
 *      (results / settings / details) where backend strings actually render —
 *      NOT just the hero. Most leaks hide there.
 *
 * Cypress/other: same logic — get the rendered text of a region, run the two
 * regex checks. Run this in CI on every UI change.
 */
import { expect, test, type Page } from "@playwright/test";

// 1. Route that renders the target (non-default) locale.
const TARGET_LOCALE_PATH = "/ar"; // TODO

// 2. Unicode range for the target locale's script. Common ranges:
//    Arabic [؀-ۿ] · Hebrew [֐-׿] · Cyrillic [Ѐ-ӿ]
//    CJK [一-鿿] · Hiragana/Katakana [぀-ヿ] · Thai [฀-๿]
const TARGET_SCRIPT = /[؀-ۿ]/; // TODO (Arabic shown)

// 3. Brand / proper nouns / units that are legitimately Latin in this locale.
const LATIN_ALLOWLIST = new Set<string>(["YourBrand", "SAR", "USD"]); // TODO

// camelCase / PascalCase-with-internal-cap identifiers leaking as labels.
const IDENTIFIER = /\b[a-z]+[A-Z][a-zA-Z0-9]*\b/g;
// Region of the page to scan (narrow to your app's main content if needed).
const SCAN_SELECTOR = "main";

// 4. Reach the deep, data-dense screen (where API/backend strings render).
async function gotoContentRichScreen(page: Page) {
  await page.goto(TARGET_LOCALE_PATH);
  // TODO: drive the app to the data-rich view — e.g. fill a form + submit,
  //       open the details/results/settings panel, expand disclosures, etc.
  //       Mock network responses so the data-sourced strings are present.
  // await page.getByRole("button", { name: /…/ }).click();
  // await expect(page.getByTestId("results")).toBeVisible();
}

test.describe("i18n integrity (rendered output)", () => {
  test("no raw identifiers leak into the localized UI", async ({ page }) => {
    await gotoContentRichScreen(page);
    const text = await page.locator(SCAN_SELECTOR).innerText();
    const leaked = [
      ...new Set([...text.matchAll(IDENTIFIER)].map((m) => m[0]).filter((w) => !LATIN_ALLOWLIST.has(w)))
    ];
    expect(leaked, `raw identifiers leaked into the localized UI: ${leaked.join(", ")}`).toEqual([]);
  });

  test("no user-facing line is untranslated source text", async ({ page }) => {
    await gotoContentRichScreen(page);
    // Scan list items / paragraphs / labels — adjust selectors to your app.
    const lines = await page.locator(`${SCAN_SELECTOR} li, ${SCAN_SELECTOR} p, ${SCAN_SELECTOR} dd`).allInnerTexts();
    const untranslated = lines
      .map((l) => l.trim())
      .filter((l) => l.length > 2)
      // a line with NO target-script char and that contains ≥2 ASCII words = likely source text
      .filter((l) => !TARGET_SCRIPT.test(l) && (l.match(/[A-Za-z]{2,}/g)?.length ?? 0) >= 2)
      .filter((l) => ![...LATIN_ALLOWLIST].some((w) => l === w));
    expect(untranslated, `untranslated source text in the localized UI: ${untranslated.join(" | ")}`).toEqual([]);
  });
});
