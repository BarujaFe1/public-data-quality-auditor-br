import { test, expect } from "@playwright/test";

const MOJIBAKE = /\u251c.|\u00c3\u00a9|\u00c2 /;

test.describe("critical lab path", () => {
  test("home to audit demo score and issues", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTestId("cta-run-demo")).toBeVisible();
    await page.getByTestId("cta-run-demo").click();
    await expect(page).toHaveURL(/\/audit$/);

    await expect(page.getByTestId("demo-municipios")).toBeVisible();
    await expect(page.getByTestId("demo-ibge_municipios")).toBeVisible();

    await page.getByTestId("demo-municipios").click();
    await expect(page).toHaveURL(/\/audit\/.+/, { timeout: 15_000 });
    await expect(page.getByTestId("quality-score-card")).toBeVisible({ timeout: 15_000 });
    await expect(page.getByTestId("overall-score")).toContainText("87.4");

    await page.getByTestId("tab-issues").click();
    await expect(page.getByText(/duplicate_id|empty_rows|invalid_/i).first()).toBeVisible({
      timeout: 10_000,
    });
  });

  test("UI copy must not contain UTF-8 mojibake", async ({ page }) => {
    await page.goto("/");
    expect(await page.locator("body").innerText()).not.toMatch(MOJIBAKE);

    await page.goto("/audit");
    await page.getByTestId("demo-municipios").click();
    await expect(page.getByTestId("quality-score-card")).toBeVisible({ timeout: 15_000 });
    const auditText = await page.locator("body").innerText();
    expect(auditText).not.toMatch(MOJIBAKE);
    expect(auditText).toMatch(/utiliz\u00e1vel|S\u00e3o Paulo/);
  });
});
