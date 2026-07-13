import { test, expect } from "@playwright/test";

test.describe("critical lab path", () => {
  test("home → audit demo → score and issues", async ({ page }) => {
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
});
