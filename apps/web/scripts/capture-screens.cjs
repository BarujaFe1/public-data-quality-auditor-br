#!/usr/bin/env node
/**
 * Portfolio screen capture - Playwright
 *
 * Usage:
 *   node scripts/capture-screens.mjs
 *   BASE_URL=https://example.vercel.app node scripts/capture-screens.mjs
 *   npx playwright install chromium   # once
 *
 * Config: screenshots.config.json (same folder or project root)
 * Output: artifacts/screenshots/<timestamp>/ + latest/
 */

const fs = require("fs");
const path = require("path");
const { chromium, devices } = require("playwright");

function findConfig() {
  const candidates = [
    path.join(process.cwd(), "screenshots.config.json"),
    path.join(process.cwd(), "scripts", "screenshots.config.json"),
    path.join(__dirname, "screenshots.config.json"),
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) return c;
  }
  throw new Error("screenshots.config.json not found. Create one next to package.json.");
}

function loadConfig() {
  const file = findConfig();
  const cfg = JSON.parse(fs.readFileSync(file, "utf8"));
  if (!cfg.routes || !Array.isArray(cfg.routes) || cfg.routes.length === 0) {
    throw new Error("screenshots.config.json must include a non-empty routes[]");
  }
  return { cfg, file };
}

async function settle(page, ms = 800) {
  await page.waitForLoadState("networkidle", { timeout: 20000 }).catch(() => {});
  await page.waitForTimeout(ms);
}

async function runActions(page, actions = []) {
  for (const action of actions) {
    if (action.click) {
      await page.locator(action.click).first().click({ timeout: 10000 });
      await settle(page, action.waitMs ?? 600);
    } else if (action.fill) {
      await page.locator(action.fill.selector).fill(action.fill.value);
    } else if (action.press) {
      await page.keyboard.press(action.press);
    } else if (action.waitMs) {
      await page.waitForTimeout(action.waitMs);
    }
  }
}

async function captureOne(context, baseUrl, route, outDir, mobile = false) {
  const page = await context.newPage();
  const url = new URL(route.path || "/", baseUrl).toString();
  const name = route.name || route.path.replace(/\W+/g, "_") || "page";
  const suffix = mobile ? ".mobile" : "";
  const file = path.join(outDir, `${name}${suffix}.png`);

  const result = {
    name: `${name}${suffix}`,
    url,
    ok: false,
    status: null,
    file: path.relative(process.cwd(), file),
    title: null,
    errors: [],
    mojibake: false,
  };

  page.on("pageerror", (err) => result.errors.push(`pageerror: ${err.message}`));
  page.on("console", (msg) => {
    if (msg.type() === "error") result.errors.push(`console: ${msg.text()}`);
  });

  try {
    const response = await page.goto(url, { waitUntil: "domcontentloaded", timeout: 45000 });
    result.status = response ? response.status() : null;
    await settle(page, route.waitMs ?? 1000);
    if (route.actions) await runActions(page, route.actions);

    result.title = await page.title();
    const bodyText = await page.locator("body").innerText().catch(() => "");
    // Practical form of /├.|Ã.|Â./ — catch CP850/Latin1 mojibake without false+ on PT "ÃO"
    result.mojibake = /├.|Ã©|Ã¡|Ã­|Ã³|Ãº|Ã§|Ãµ|Ã¢|Ã£|Â /.test(bodyText);
    if (result.mojibake) {
      result.errors.push("mojibake detected in page body");
    }

    await page.screenshot({ path: file, fullPage: Boolean(route.fullPage ?? true) });
    result.ok = result.status !== null && result.status < 400;
  } catch (err) {
    result.errors.push(String(err && err.message ? err.message : err));
  } finally {
    await page.close();
  }
  return result;
}

async function main() {
  const { cfg } = loadConfig();
  const baseUrl = (process.env.BASE_URL || cfg.baseUrl || "").replace(/\/$/, "");
  if (!baseUrl) throw new Error("Set baseUrl in screenshots.config.json or BASE_URL env");

  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const rootOut = path.join(process.cwd(), "artifacts", "screenshots");
  const outDir = path.join(rootOut, stamp);
  const latestDir = path.join(rootOut, "latest");
  fs.mkdirSync(outDir, { recursive: true });
  fs.mkdirSync(latestDir, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const desktop = await browser.newContext({
    viewport: cfg.viewport || { width: 1440, height: 900 },
    locale: cfg.locale || "pt-BR",
    colorScheme: cfg.colorScheme || "light",
  });

  const report = {
    project: cfg.name || path.basename(process.cwd()),
    baseUrl,
    capturedAt: new Date().toISOString(),
    results: [],
  };

  console.log(`\n📸 ${report.project} → ${baseUrl}`);
  for (const route of cfg.routes) {
    const r = await captureOne(desktop, baseUrl, route, outDir, false);
    report.results.push(r);
    const flag = r.ok ? (r.mojibake ? "⚠️ " : "✅") : "❌";
    console.log(`${flag} ${r.name}  HTTP ${r.status}  ${r.mojibake ? "MOJIBAKE" : ""}`);
  }

  if (cfg.mobile !== false) {
    const mobileCtx = await browser.newContext({
      ...devices["iPhone 14"],
      locale: cfg.locale || "pt-BR",
    });
    for (const route of cfg.routes.filter((r) => r.mobile !== false).slice(0, cfg.mobileLimit || 4)) {
      const r = await captureOne(mobileCtx, baseUrl, route, outDir, true);
      report.results.push(r);
      console.log(`${r.ok ? "📱" : "❌"} ${r.name}  HTTP ${r.status}`);
    }
    await mobileCtx.close();
  }

  await desktop.close();
  await browser.close();

  const reportPath = path.join(outDir, "report.json");
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2), "utf8");

  // refresh latest/
  for (const f of fs.readdirSync(latestDir)) {
    fs.rmSync(path.join(latestDir, f), { force: true, recursive: true });
  }
  for (const f of fs.readdirSync(outDir)) {
    fs.copyFileSync(path.join(outDir, f), path.join(latestDir, f));
  }

  const bad = report.results.filter((r) => !r.ok || r.mojibake || r.errors.length);
  console.log(`\nOutput: ${outDir}`);
  console.log(`Latest: ${latestDir}`);
  console.log(`Issues: ${bad.length}/${report.results.length}`);
  if (bad.length) {
    console.log(JSON.stringify(bad, null, 2));
    process.exitCode = 1;
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
