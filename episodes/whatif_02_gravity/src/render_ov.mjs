// usage: node render.mjs stills t1,t2,...   |  node render.mjs video start end out.mp4
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import { spawn } from 'child_process';
const [mode, a, b, out] = process.argv.slice(2);
const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
page.on('console', m => console.log('[page]', m.text()));
page.on('pageerror', e => console.log('[pageerror]', e.message));
await page.goto('http://127.0.0.1:8766/overlay.html');
await page.waitForFunction(() => window.ready === true, null, { timeout: 60000 });
await page.evaluate(() => document.fonts.ready);
const FPS = 30;
if (mode === 'stills') {
  for (const t of a.split(',').map(Number)) {
    await page.evaluate(t => window.renderAt(t), t);
    await page.screenshot({ path: `ov_stills/s_${t.toFixed(2)}.png`, omitBackground: true });
    console.log('still', t);
  }
} else {
  const f0 = Math.round(Number(a) * FPS), f1 = Math.round(Number(b) * FPS);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
    '-c:v', 'qtrle', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let f = f0; f < f1; f++) {
    await page.evaluate(t => window.renderAt(t), f / FPS);
    const buf = await page.screenshot({ type: 'png', omitBackground: true });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 30 === 0) console.log(out, 'frame', f, ((Date.now() - t0) / (f - f0 + 1)).toFixed(0), 'ms/frame');
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
}
await browser.close();
