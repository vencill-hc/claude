---
name: visual-verify
description: Take screenshots of the Metroline frontend UI using Playwright for visual verification. Use when the user says "check the UI", "screenshot", "verify visually", "how does it look", "take a screenshot", "show me the page", or after any visual/CSS/layout change to verify the result without manual browser inspection. Eliminates the manual screenshot-paste loop.
---

# Visual Verify

Automate frontend visual verification using Playwright. After any UI change (CSS, layout, component, styling), take a headless browser screenshot and return it for analysis -- eliminating the need for the user to manually open a browser, take a screenshot, and paste it back.

## Prerequisites

- Playwright is installed via npx (`npx playwright` available, v1.58.0+)
- Chromium browser installed at: `~/Library/Caches/ms-playwright/`
- If Chromium is missing, run: `npx playwright install chromium`
- Vite dev server runs on port 3000 (`web/` directory)
- API backend runs on port 8420

## CRITICAL: NODE_PATH Required

Playwright is installed in the npx cache, NOT as a local project dependency. Every `node -e` command MUST include the `NODE_PATH` environment variable:

```bash
NODE_PATH=/Users/huntclub-vencill/.npm/_npx/e41f203b7505f1fb/node_modules node -e "..."
```

Without this, `require('playwright')` will fail with `MODULE_NOT_FOUND`. If the npx cache path changes (after an npx update), find the current path with:

```bash
find ~/.npm/_npx -name "playwright" -type d 2>/dev/null | head -1
```

## Quick Reference: Page Routes

| Route | Page | Description |
|-------|------|-------------|
| `/` | MetroMap | Main metro map with station markers, handler badges, dispatch panel |
| `/agents` | AgentDashboard | Agent list, spawn agent form |
| `/queue` | WorkQueue | Train dispatch form, work queue |
| `/history` | HistoryTimeline | Historical timeline of train runs |

## Workflow

### Step 1: Ensure the Dev Server is Running

Check if the Vite dev server is already running on port 3000:

```bash
lsof -i :3000 -sTCP:LISTEN 2>/dev/null | head -5
```

If NOT running, start it in the background:

```bash
cd /Users/huntclub-vencill/Documents/git/metroline/web && npm run dev -- --port 3000 &
sleep 3  # Wait for server startup
```

Record whether you started the server (for cleanup later).

Optionally, also check the API backend on port 8420 if the page needs live data:

```bash
lsof -i :8420 -sTCP:LISTEN 2>/dev/null | head -5
```

If the API is not running and the page needs it, start it:

```bash
cd /Users/huntclub-vencill/Documents/git/metroline && .venv/bin/python -m uvicorn metroline.api.app:app --port 8420 &
sleep 2
```

### Step 2: Take the Screenshot

Use Playwright's built-in screenshot capability via a Node.js one-liner. This is the core command pattern:

#### Full-page screenshot of a specific route

```bash
NODE_PATH=/Users/huntclub-vencill/.npm/_npx/e41f203b7505f1fb/node_modules node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.goto('http://localhost:3000/');
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: '/tmp/metroline-screenshot.png', fullPage: true });
  await browser.close();
  console.log('/tmp/metroline-screenshot.png');
})();
" 2>/dev/null
```

#### Screenshot of a specific CSS selector (component-level)

```bash
NODE_PATH=/Users/huntclub-vencill/.npm/_npx/e41f203b7505f1fb/node_modules node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.goto('http://localhost:3000/');
  await page.waitForLoadState('networkidle');
  const el = await page.waitForSelector('CSS_SELECTOR_HERE', { timeout: 5000 });
  await el.screenshot({ path: '/tmp/metroline-component.png' });
  await browser.close();
  console.log('/tmp/metroline-component.png');
})();
" 2>/dev/null
```

#### Screenshot with custom viewport (mobile, tablet, etc.)

```bash
NODE_PATH=/Users/huntclub-vencill/.npm/_npx/e41f203b7505f1fb/node_modules node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  await page.goto('http://localhost:3000/');
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: '/tmp/metroline-mobile.png', fullPage: true });
  await browser.close();
  console.log('/tmp/metroline-mobile.png');
})();
" 2>/dev/null
```

### Step 3: Read and Analyze the Screenshot

After taking the screenshot, use the Read tool to view the image:

```
Read file: /tmp/metroline-screenshot.png
```

Claude can directly view PNG images via the Read tool. Analyze the screenshot for:
- Layout correctness (elements positioned as expected)
- Text readability (font size, contrast, overlap)
- Color accuracy (Solarized palette compliance)
- Component rendering (no broken elements, proper spacing)
- Responsive behavior (if testing multiple viewports)

### Step 4: Report Findings

After analyzing the screenshot, report:

1. **What looks correct** -- confirm elements that render properly
2. **What needs fixing** -- identify visual issues with specifics (element, problem, suggested fix)
3. **Comparison to intent** -- does the visual match what was intended by the code change?

If issues are found, fix them and re-run the screenshot to verify the fix. This replaces the manual loop of: change code -> user opens browser -> user takes screenshot -> user pastes screenshot -> Claude analyzes -> repeat.

### Step 5: Cleanup

If you started the dev server in Step 1, stop it when done:

```bash
# Only if YOU started the server
kill $(lsof -t -i :3000) 2>/dev/null
```

## Common Selectors for Metroline Components

| Component | Likely Selector | Page |
|-----------|----------------|------|
| Metro map SVG | `svg`, `.metro-map` | `/` |
| Station markers | `circle[data-station]`, `.station-marker` | `/` |
| Handler badges | `.handler-badge`, `text.handler-label` | `/` |
| Dispatch panel | `.dispatch-panel`, `[data-testid="dispatch"]` | `/` |
| Agent cards | `.agent-card` | `/agents` |
| Spawn form | `form`, `.spawn-form` | `/agents` |
| Train queue | `.train-queue`, `.work-queue` | `/queue` |
| Nav bar | `nav`, `.navbar` | all |

Note: These selectors are approximate. If a selector fails, use the browser's DOM to find the correct one:

```bash
NODE_PATH=/Users/huntclub-vencill/.npm/_npx/e41f203b7505f1fb/node_modules node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('http://localhost:3000/');
  await page.waitForLoadState('networkidle');
  const html = await page.content();
  console.log(html.substring(0, 5000));
  await browser.close();
})();
"
```

## Multiple Screenshots in One Pass

When verifying a broad change (e.g., design token update), capture all pages at once:

```bash
NODE_PATH=/Users/huntclub-vencill/.npm/_npx/e41f203b7505f1fb/node_modules node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const routes = ['/', '/agents', '/queue', '/history'];
  for (const route of routes) {
    await page.goto('http://localhost:3000' + route);
    await page.waitForLoadState('networkidle');
    const name = route === '/' ? 'map' : route.slice(1);
    await page.screenshot({ path: '/tmp/metroline-' + name + '.png', fullPage: true });
    console.log('/tmp/metroline-' + name + '.png');
  }
  await browser.close();
})();
" 2>/dev/null
```

Then read each screenshot file to analyze all pages.

## Dark Mode Testing

If dark mode is supported, toggle it before screenshotting:

```bash
NODE_PATH=/Users/huntclub-vencill/.npm/_npx/e41f203b7505f1fb/node_modules node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: 1280, height: 900 },
    colorScheme: 'dark'
  });
  await page.goto('http://localhost:3000/');
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: '/tmp/metroline-dark.png', fullPage: true });
  await browser.close();
  console.log('/tmp/metroline-dark.png');
})();
" 2>/dev/null
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `playwright` not found as module | Ensure `NODE_PATH` env var is set (see "CRITICAL: NODE_PATH Required" section above) |
| Chromium browser not installed | Run `npx playwright install chromium` |
| Port 3000 not responding | Start dev server: `cd web && npm run dev` |
| Page shows loading spinner | API backend on 8420 not running; start it or use `vite preview` for static content |
| Screenshot is blank/white | Increase `waitForLoadState` timeout or add explicit `page.waitForTimeout(2000)` |
| Element selector not found | Use the DOM dump command above to find correct selectors |
| `require is not defined` | The node script is running in ESM mode; should not happen with plain `node -e`. If it does, add `--input-type=commonjs` flag |
| npx cache path changed | Run `find ~/.npm/_npx -name "playwright" -type d 2>/dev/null` to find the new path |

## Anti-patterns

- Do NOT ask the user to take a screenshot manually. Use this skill instead.
- Do NOT skip visual verification after CSS/layout changes. Always screenshot.
- Do NOT leave the dev server running if you started it. Clean up.
- Do NOT take screenshots against `localhost:3000` if the dev server is not confirmed running.
- Do NOT ignore network errors in screenshots (missing images, failed API calls). Check the console output too if needed.
