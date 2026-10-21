// PROTOTYPE (happy-dwarf-team/.github#15): throwaway spike, not production code.
// Launches a pinned VS Code with Etch loaded (--extensionDevelopmentPath), drives it with
// Playwright's _electron, takes screenshots and a recordVideo of an edit to a .gui file, and
// optionally records the same window with FFmpeg gfxcapture and tests occlusion.
//
// Env:
//   ETCH_ROOT   clone of happy-dwarf-team/etch, built (`node packages/extension/build.mts`)
//   EU4_GUI     a .gui file to copy into a scratch mod (read only; the original is never written)
//   FFMPEG      full FFmpeg >= 8.1 (for GFX=1)
//   OUT         output folder (screenshots, videos, log.json)
//   DPR=1|2     --force-device-scale-factor
//   GFX=1       also record the window with gfxcapture (lossless master)
//   OCCLUDE=1   cover / minimise the window mid-run and see what capture gets
import { spawn } from 'node:child_process';
import { cp, mkdir, rm, writeFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import * as path from 'node:path';

const etch = process.env.ETCH_ROOT;
const out = path.resolve(process.env.OUT);
const dpr = Number(process.env.DPR ?? '1');
const VSCODE_VERSION = '1.142.0';
const SIZE = { width: 1920, height: 1080 };

const { downloadAndUnzipVSCode } = createRequire(path.join(etch, 'packages/extension/package.json'))(
  '@vscode/test-electron',
);
const { _electron } = createRequire(path.join(etch, 'packages/renderer/package.json'))('@playwright/test');

const log = { vscode: VSCODE_VERSION, dpr, size: SIZE, events: [] };
const t0 = Date.now();
const note = (event, data = {}) => {
  const entry = { t: (Date.now() - t0) / 1000, event, ...data };
  log.events.push(entry);
  console.log(JSON.stringify(entry));
};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

await rm(out, { recursive: true, force: true });
await mkdir(out, { recursive: true });
// VS Code fails to load workbench.html (ERR_FILE_NOT_FOUND) when its install path passes MAX_PATH,
// so VS Code and its user data live under a short folder (SHORT), outputs under OUT.
const short = path.resolve(process.env.SHORT);
const scratch = path.join(short, 'run');
await rm(scratch, { recursive: true, force: true });
const mod = path.join(scratch, 'demo-mod');
await mkdir(path.join(mod, 'interface'), { recursive: true });
await writeFile(path.join(mod, 'descriptor.mod'), 'name="Etch capture spike"\nsupported_version="1.37.*"\n');
const gui = path.join(mod, 'interface', path.basename(process.env.EU4_GUI));
await cp(process.env.EU4_GUI, gui);

const userData = path.join(scratch, 'user-data');
await mkdir(path.join(userData, 'User'), { recursive: true });
await writeFile(
  path.join(userData, 'User', 'settings.json'),
  JSON.stringify(
    {
      'workbench.colorTheme': 'Default Dark Modern',
      'workbench.startupEditor': 'none',
      'workbench.tips.enabled': false,
      'workbench.secondarySideBar.defaultVisibility': 'hidden',
      'workbench.layoutControl.enabled': false,
      'chat.disableAIFeatures': true,
      'window.zoomLevel': 0,
      'window.restoreWindows': 'none',
      'window.commandCenter': false,
      'editor.fontSize': 16,
      'editor.minimap.enabled': false,
      'editor.cursorBlinking': 'solid',
      'editor.accessibilitySupport': 'off',
      'telemetry.telemetryLevel': 'off',
      'update.mode': 'none',
      'extensions.autoCheckUpdates': false,
      'security.workspace.trust.enabled': false,
      'etch.previewResolution': '1920x1080',
    },
    null,
    2,
  ),
);

const executablePath = await downloadAndUnzipVSCode({
  version: VSCODE_VERSION,
  cachePath: path.join(short, 'vscode'),
});
note('vscode', { executablePath });

const args = [
  mod,
  gui,
  `--extensionDevelopmentPath=${path.join(etch, 'packages/extension')}`,
  `--user-data-dir=${userData}`,
  `--extensions-dir=${path.join(scratch, 'extensions')}`,
  '--skip-release-notes',
  '--skip-welcome',
  '--disable-telemetry',
  '--disable-experiments',
  '--disable-updates',
  '--disable-workspace-trust',
  '--no-cached-data',
];
if (dpr !== 1) args.push(`--force-device-scale-factor=${dpr}`);

const app = await _electron.launch({
  executablePath,
  args,
  recordVideo: { dir: path.join(out, 'pw-video'), size: { width: SIZE.width * dpr, height: SIZE.height * dpr } },
});
const pid = app.process().pid;
note('launched', { pid });
// The workbench window, defined in Electron's main process (it may also have helper windows).
await app.evaluate(() => {
  globalThis.mainWindow = (B) => B.getAllWindows().find((w) => w.webContents.getURL().includes('workbench'));
});

let page;
for (let i = 0; i < 300 && page === undefined; i++) {
  page = app.windows().find((w) => w.url().includes('workbench'));
  if (page === undefined) await sleep(100);
}
note('windows', { urls: app.windows().map((w) => w.url().slice(0, 100)) });
const hwnd = await app.evaluate(({ BrowserWindow }, size) => {
  const win = mainWindow(BrowserWindow);
  win.setBounds({ x: 40, y: 40, ...size });
  return win.getNativeWindowHandle().readBigUInt64LE().toString();
}, SIZE);
await page.waitForSelector('.monaco-workbench');
await page.waitForSelector('.monaco-editor .view-lines');
note('workbench', {
  hwnd,
  devicePixelRatio: await page.evaluate(() => window.devicePixelRatio),
  inner: await page.evaluate(() => [window.innerWidth, window.innerHeight]),
  bounds: await app.evaluate(({ BrowserWindow }) => mainWindow(BrowserWindow).getBounds()),
});

// Etch: Open Preview through the command palette.
await page.keyboard.press('Control+Shift+P');
await page.keyboard.type('Etch: Open Preview');
await sleep(400);
await page.keyboard.press('Enter');

// Find the frame that holds Etch's canvas (VS Code nests the webview two iframes deep).
let frame;
for (let i = 0; i < 150 && frame === undefined; i++) {
  for (const f of page.frames()) {
    const visible = await f
      .evaluate(() => {
        const c = document.querySelector('canvas#screen');
        return c !== null && !c.hidden && c.width > 0;
      })
      .catch(() => false);
    if (visible) frame = f;
  }
  if (frame === undefined) await sleep(200);
}
note('frames', {
  frames: page.frames().map((f) => f.url().slice(0, 120)),
  canvasFrame: frame?.url().slice(0, 120),
  depth: frame === undefined ? null : (() => { let d = 0; for (let f = frame; f.parentFrame(); f = f.parentFrame()) d++; return d; })(),
});
if (frame === undefined) throw new Error('canvas#screen not found in any frame');
const canvasInfo = () =>
  frame.evaluate(() => {
    const c = document.querySelector('canvas#screen');
    const r = c.getBoundingClientRect();
    return { width: c.width, height: c.height, css: [r.width, r.height], visibility: document.visibilityState, dataset: { ...c.dataset } };
  });
await sleep(2000);
note('canvas', { ...(await canvasInfo()), box: await frame.locator('canvas#screen').boundingBox() });
// Click into the editor so the keyboard goes there, not to the webview.
await page.locator('.monaco-editor .view-lines').first().click({ position: { x: 300, y: 200 } });
await page.screenshot({ path: path.join(out, 'shot-initial.png') });
await frame.locator('canvas#screen').screenshot({ path: path.join(out, 'shot-canvas-element.png') });
note('screenshot');

let ffmpeg;
if (process.env.GFX === '1') {
  ffmpeg = spawn(
    process.env.FFMPEG,
    [
      '-hide_banner', '-loglevel', 'warning', '-y',
      '-filter_complex', `gfxcapture=hwnd=${hwnd}:capture_cursor=0:max_framerate=60,hwdownload,format=bgra,fps=30,format=bgr0`,
      '-c:v', 'libx264rgb', '-preset', 'ultrafast', '-crf', '0',
      path.join(out, 'gfx-master.mkv'),
    ],
    { stdio: ['pipe', 'inherit', 'inherit'] },
  );
  note('gfxcapture-start', { pid: ffmpeg.pid });
  await sleep(1500);
}

// Select a unique piece of text with Find (the editor keeps the match selected after Escape) and
// type over it, so the recording shows real typing.
const replace = async (find, text) => {
  await page.keyboard.press('Control+F');
  await page.keyboard.type(find);
  await sleep(200);
  await page.keyboard.press('Escape');
  await sleep(300);
  await page.keyboard.type(text, { delay: 180 });
};

note('edit-start');
// LOOP=1: a longer edit that ends where it started, so the clip loops without a jump.
const edits = process.env.LOOP === '1'
  ? [['-290', '-100'], ['-280', '-150'], ['-100', '-350'], ['-150', '-200'], ['-350', '-290'], ['-200', '-280']]
  : [['-290', '-100'], ['-280', '-150']];
for (const [find, text] of edits) {
  await replace(find, text);
  await sleep(1200);
}
note('canvas-after-edit-1', await canvasInfo());
await page.screenshot({ path: path.join(out, 'shot-after.png') });

if (process.env.OCCLUDE === '1') {
  // A second, always-on-top window over VS Code, then an edit that is only visible if painting
  // goes on under cover.
  await app.evaluate(({ BrowserWindow }) => {
    const main = mainWindow(BrowserWindow);
    const cover = new BrowserWindow({ ...main.getBounds(), alwaysOnTop: true, frame: false, backgroundColor: '#ff00ff', show: false });
    cover.showInactive();
    globalThis.__cover = cover;
  });
  await sleep(1000);
  note('covered', await canvasInfo());
  await replace('-100', '-400');
  await sleep(1500);
  note('covered-after-edit', await canvasInfo());
  await page.screenshot({ path: path.join(out, 'shot-covered.png') });
  await app.evaluate(() => globalThis.__cover.close());
  await sleep(1000);
  await app.evaluate(({ BrowserWindow }) => mainWindow(BrowserWindow).minimize());
  await sleep(1000);
  await replace('-400', '-200');
  await sleep(1500);
  note('minimised-after-edit', await canvasInfo());
  await page.screenshot({ path: path.join(out, 'shot-minimised.png'), timeout: 10_000 }).catch((e) => note('minimised-screenshot-failed', { error: String(e).slice(0, 200) }));
  await app.evaluate(({ BrowserWindow }) => { const w = mainWindow(BrowserWindow); w.restore(); w.setBounds({ x: 40, y: 40, width: 1920, height: 1080 }); });
  await sleep(1500);
  note('restored', await canvasInfo());
  await page.screenshot({ path: path.join(out, 'shot-restored.png') });
}
note('edit-end');

if (ffmpeg !== undefined) {
  ffmpeg.stdin.write('q');
  await new Promise((r) => ffmpeg.on('exit', r));
  note('gfxcapture-end');
}
const video = page.video();
await app.close();
note('closed', { videoPath: await video?.path() });
await writeFile(path.join(out, 'log.json'), JSON.stringify(log, null, 2));
