import { test, expect } from "@playwright/test";

const MOJIBAKE = /\u251c.|\u00c3\u00a9|\u00c2 /;

test.describe("encoding and lab path", () => {
  test("UI copy must not contain UTF-8 mojibake", async ({ page }) => {
    await page.goto("/");
    const homeText = await page.locator("body").innerText();
    expect(homeText).not.toMatch(MOJIBAKE);

    await page.goto("/audit");
    await expect(page.getByRole("heading", { name: /Auditar dataset/i })).toBeVisible();
    await page.getByRole("button", { name: /Munic\u00edpios/i }).first().click();
    await expect(page).toHaveURL(/\/audit\/.+/, { timeout: 15_000 });
    await expect(page.getByText("87.4")).toBeVisible({ timeout: 15_000 });

    const auditText = await page.locator("body").innerText();
    expect(auditText).not.toMatch(MOJIBAKE);
    expect(auditText).toMatch(/utiliz\u00e1vel|S\u00e3o Paulo/);
  });
});
