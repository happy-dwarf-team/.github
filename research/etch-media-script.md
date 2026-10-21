# Can Etch screenshots and recordings come from a repeatable script?

Research for [happy-dwarf-team/.github#6](https://github.com/happy-dwarf-team/.github/issues/6)
(map: [#4](https://github.com/happy-dwarf-team/.github/issues/4)). Researched 2026-10-21 against
`etch` at `8a82e70` (release 0.1.0), Playwright v1.64.1, VS Code `main`, FFmpeg docs on `master`.

## Answer

**Yes.** The recommended shape is a Node script in the `etch` repo that downloads a pinned VS Code
with `@vscode/test-electron` (already a dev dependency), launches it through Playwright's
`_electron.launch()` with Etch loaded via `--extensionDevelopmentPath`, a fresh user data dir and
seeded settings, drives a demo mod through the keyboard, and takes PNG screenshots with
`page.screenshot()` and WebM recordings with `recordVideo`. This is the same mechanism VS Code's
own smoke tests use to drive and record a built VS Code. If Playwright's video turns out too soft
for editor text, the recording half swaps to FFmpeg's `gfxcapture` (Windows.Graphics.Capture,
FFmpeg 8.1+) started by the same script.

The script must run on the maintainer's Windows 11 machine, not in CI, as long as the media show
real EU4 art: Etch ships no game files and draws from an installed game, and Etch's own rules keep
game assets out of Git and the corpus off shared runners. Nothing below was tried end to end; see
[Unverified](#unverified).

## What Etch already has

Verified by reading the repo at `8a82e70`:

- **Extension tests in a real VS Code.** `packages/extension/test/run.mts` calls `runTests` from
  `@vscode/test-electron` with `version: process.env.ETCH_VSCODE_VERSION ?? 'stable'` and
  `launchArgs: ['--disable-extensions', '--disable-workspace-trust', '--skip-welcome']`. CI runs it
  on `windows-2022` (`.github/workflows/build.yml`); the last three `main` runs succeeded.
- **An end-to-end preview scenario that is almost a shot list.** `packages/extension/test/preview.ts`
  builds a fixture game in a temp folder (fake `eu4.exe`, one `.gfx`, one `.gui`, TGA texture,
  BMFont, English localisation, own profile), opens the preview through `etch.openPreview`, edits the
  unsaved buffer, moves the cursor between windows, pins, changes resolution, edits localisation,
  overwrites a texture and a font on disk, and checks the Problems panel. Its art is solid-colour
  4×4 TGAs, so it is not presentable as is, but the steps are the scenes a demo needs.
- **A paint signal, but only inside the extension host.** `activate()` returns an `EtchApi`; its
  `preview` has `onDidPaint`, `idle()` and `probe(points)`, which returns the RGBA of chosen pixels
  read with `gl.readPixels` in the webview (`webview/main.ts`, `src/preview/protocol.ts`). There is
  no full-frame export and no DOM marker a process outside VS Code could wait on.
- **Renderer tests in headless Chromium.** `packages/renderer` uses `@playwright/test` ^1.64.1;
  `draw.spec.ts` paints a draw list into a WebGL2 canvas and reads every pixel back with
  `EtchRenderer.readPixels`. CI enables SwiftShader (`--enable-unsafe-swiftshader`) because runners
  have no GPU. The context is created with `preserveDrawingBuffer: false`
  (`packages/renderer/src/index.ts`), so `canvas.toDataURL()` after compositing is not a reliable
  way to get a frame; `readPixels` right after a paint is.
- **No PNG or media output anywhere.** The only PNG in the repo is `media/icon.png`. Policy points
  the other way: `CONTRIBUTING.md` says "Screenshots and other game assets never enter Git"; ADR 0002
  keeps corpus screenshots in a local folder; ADR 0004 / CONTRIBUTING put corpus and budget runs on
  the maintainer's machine because "the corpus needs a licensed game". The extension README: "Etch
  draws with the game's own textures, fonts and localisation, and ships none of them."

## Options

| Option | Shows VS Code + preview | Waits on real paint | Output | Runs where | Verdict |
|---|---|---|---|---|---|
| A. Playwright `_electron` driving a downloaded VS Code | yes | via DOM in webview frame (needs a hook) or settle delay | PNG screenshots, VP9 WebM | interactive Windows desktop; CI possible with fixture art | **recommended** |
| B. `@vscode/test-electron` suite + external capture | yes | yes (`onDidPaint`) | whatever the capture tool gives | same | fallback driver |
| C. FFmpeg screen capture (`gfxcapture` / `ddagrab` / `gdigrab`) | yes (whatever is on screen) | no, timing only | any codec, lossless possible | interactive desktop only | capture backend for A or B |
| D. Browser VS Code (code-server, `code serve-web`, `vscode-test-web`) | browser variant | via Playwright | same as A | — | rejected |
| E. Frames from Etch's renderer (Playwright Chromium) | no, game window only | yes | exact PNG | headless, CI | complement for stills / OG images |

### A. Playwright `_electron` driving VS Code (recommended)

- Playwright: "Playwright has **experimental** support for Electron automation", Electron v21+.
  `electron.launch()` takes `executablePath`, `args`, `env`, `cwd`, `colorScheme` and
  `recordVideo: { dir, size }` ("Enables video recording for all pages"; size defaults to the
  viewport scaled to fit 800×800) ([Electron API](https://playwright.dev/docs/api/class-electron),
  [Videos](https://playwright.dev/docs/videos)). Videos are written when the context closes.
- VS Code does exactly this for its smoke tests: `test/automation/src/playwrightElectron.ts` calls
  `playwright._electron.launch({ executablePath, args, recordVideo: { dir, size: 1920×1080 }, env })`
  and then resizes the window with `BrowserWindow.setBounds` from `electron.evaluate`, with the
  comment that this "also renders reliably when it is larger than the screen". The args it passes
  (`test/automation/src/electron.ts`) are a good template: `--skip-release-notes --skip-welcome
  --disable-telemetry --disable-experiments --disable-updates --disable-workspace-trust
  --user-data-dir=… --extensions-dir=… --extensionDevelopmentPath=…`. The smoke README runs it
  against shipped builds: `npm run smoketest -- --build <path to latest version>`.
- Getting the executable: `downloadAndUnzipVSCode(version)` from `@vscode/test-electron` returns
  the path of a downloaded VS Code
  ([Testing Extensions](https://code.visualstudio.com/api/working-with-extensions/testing-extension)).
  Etch already pins through `ETCH_VSCODE_VERSION`; the media script should pin a specific version
  so a re-run per release changes only what Etch changed.
- Video encoding, from Playwright v1.64.1 `server/videoRecorder.ts` and `server/screencast.ts`:
  CDP screencast frames as JPEG at quality 90, encoded with `libvpx-vp9 -crf 8 -deadline realtime
  -cpu-used 8`, bitrate scaled from 1 Mbit/s at 800×450/25 fps by pixel rate, default 25 fps,
  output must be `.webm`. Playwright downloads its own FFmpeg for this (`playwright install ffmpeg`).
  The JPEG step plus realtime VP9 is a double lossy path: fine for a silent loop, possibly soft on
  small editor text. The final web format is ticket #8's question; this is an intermediate.
- Screenshots: `page.screenshot()` captures the workbench page, which hosts the preview; VS Code's
  docs: "Think of a webview as an `iframe` within VS Code that your extension controls"
  ([Webview API](https://code.visualstudio.com/api/extension-guides/webview)). PNG, lossless.
- Driving: keyboard and mouse through Playwright (`Ctrl+P`, typing into the editor), so the
  recording shows a real cursor and typing. Look and size come from a seeded
  `<user-data-dir>/User/settings.json` (theme, font size, zoom, minimap off) and the `setBounds`
  call; `--user-data-dir` "lets you run isolated instances with separate environments, settings,
  and extensions" ([CLI](https://code.visualstudio.com/docs/configure/command-line)).
- Waiting for the preview: the script runs outside the extension host, so it cannot use
  `onDidPaint`. Either wait a settle time after each edit (warm reload median is 6–7 ms per
  `docs/spec/v1.md`, so a few hundred ms is generous but not proof), or add a tiny hook in
  `webview/main.ts` (e.g. a paint counter as a `data-` attribute on the canvas) that Playwright
  reads through the webview's frames. The hook is the cleaner choice and is an Etch change.

### B. `@vscode/test-electron` suite plus external capture

Tests "run inside a special instance of VS Code named the Extension Development Host, and have full
access to the VS Code API" (Testing Extensions). A `media` suite next to `suite.ts` could replay the
scenario with exact waits on `preview.onDidPaint`, typing through the `type` command. But nothing
in the extension API captures the workbench, and `probe` only returns chosen canvas pixels, so the
pixels must come from an OS capture (option C) synchronised by timing or a file/console signal.
Two processes and timing coupling make it weaker than A; keep it as the fallback if Playwright's
Electron support breaks with a VS Code release.

### C. FFmpeg screen capture on Windows

From the FFmpeg docs (`doc/filters.texi`, [devices](https://ffmpeg.org/ffmpeg-devices.html)):

- `gfxcapture` (FFmpeg 8.1, released 2026-03-16, Changelog: "Windows.Graphics.Capture based
  window/monitor capture"): picks a window by regex on title, class or executable name, or by HWND;
  options for cropping, canvas size, cursor on/off, `max_framerate` (default 60). It "does NOT hold
  a stable FPS", so add an `fps` filter. Outputs D3D11 frames; needs `hwdownload,format=bgra` for
  software encoders. Best fit: captures just the VS Code window by its process.
- `ddagrab` (FFmpeg 6.0): Desktop Duplication of a whole output, region via
  `video_size`/`offset_x`/`offset_y`, 30 fps default with frame duplication, D3D11 frames. Captures
  whatever is on top in that rectangle (toasts, other windows).
- `gdigrab`: GDI capture of the desktop, a region, or a window by `title=`/`hwnd=`. The docs list no
  caveat, but GDI capture of GPU-composited windows is a known source of black frames (not verified
  here).

All three need an interactive, unlocked desktop session; none works on a locked screen or a
service session. Gains over Playwright video: true screen pixels, any codec, lossless intermediate.
Cost: one more pinned binary (FFmpeg ≥ 8.1 for `gfxcapture`), window placement must be fixed, and
no knowledge of when the preview painted.

### D. Browser-hosted VS Code (rejected)

- `vscode-test-web` "helps testing VS Code web extensions locally"
  ([repo](https://github.com/microsoft/vscode-test-web)). Etch is a Node extension (`main` only, no
  `browser` entry, Windows x64 VSIX per ADR 0004), so it cannot load there.
- code-server: "We currently do not publish Windows releases"
  ([install docs](https://coder.com/docs/code-server/install)).
- `code serve-web` (VS Code CLI, `cli/src/commands/args.rs`: `--host`, `--port`,
  `--connection-token`, `--server-data-dir`, `--default-folder`, …) runs a Node extension host on
  Windows, but has no `--extensionDevelopmentPath`, downloads its server on first run, and shows the
  browser variant of the workbench rather than the desktop app users install. No gain over A.

### E. Frames from Etch's own renderer

The renderer tests already show the pipeline: a draw list from `@etch/core`, painted by
`@etch/renderer` in headless Chromium, read back with `readPixels` as straight RGBA. A small script
could write those pixels to PNG for chosen vanilla windows at chosen resolutions: exact,
deterministic, CI-capable, and transparent background. It does not show VS Code, typing or the
outline, so it cannot carry the "Etch at work" loop, but it suits a gallery of what the preview
draws and Open Graph images. With real art it still needs the installed game (core's playset reads
the game folder), so the same "maintainer machine" constraint applies.

## Recommendation and trade-offs

1. **Driver:** Playwright `_electron.launch()` on a pinned VS Code from `downloadAndUnzipVSCode`,
   args copied from VS Code's smoke tests, fresh user data and extensions dirs, seeded settings,
   window set to a fixed size with `setBounds`. Lives in `etch` (e.g. `pnpm media`), reusing the
   Playwright version the renderer package already pins.
2. **Stills:** `page.screenshot()` to PNG, optionally clipped to editor + preview.
3. **Loops:** start with `recordVideo` at the target size; if text is visibly soft, switch to
   `gfxcapture` on the VS Code window (FFmpeg ≥ 8.1) with a lossless or high-quality intermediate.
   Transcode to the web format chosen in ticket #8 as a last step of the same script.
4. **Scenes:** a demo mod (its own small folder, not the vanilla files) replayed from a scene list;
   `test/preview.ts` is the template for what to show. A paint marker in the webview makes waits
   exact.
5. **Where:** maintainer's Windows 11 machine with EU4 1.37.5 installed, outputs outside Git, upload
   per ticket #8. If ticket #7 rules out EU4 art, the same script with fixture art could run on a
   `windows-2022` runner (Etch's extension tests already open and paint the preview there, on a
   runner without a GPU).

Trade-offs: Playwright Electron is officially experimental, so a VS Code or Playwright upgrade can
break the script (mitigated by pinning both, and by VS Code depending on it for its own smoke
tests). Playwright video is convenient but lossy twice. OS capture is sharper but timing-coupled and
needs a quiet desktop. Running locally means media refresh is a manual step per release, not an
automatic workflow.

## Unverified

Not run in this research (no VS Code, Playwright or FFmpeg was installed or launched):

- That `page.screenshot()` and `recordVideo` on a stable VS Code build include the preview's WebGL2
  canvas inside the webview iframe (expected, since CDP captures the composited page, but VS Code
  webviews are cross-origin iframes and this was not tried).
- That Playwright can reach the webview's inner frame to read a paint marker.
- Behaviour under Windows display scaling (screenshot pixel size vs. the 1920×1080 target), and
  whether `--force-device-scale-factor` passes through `Code.exe`.
- Whether Chromium's native window occlusion on Windows pauses painting (and so screenshots and the
  screencast) when the VS Code window is covered or minimised during a run.
- The `gdigrab` black-frame risk, and whether `gfxcapture` keeps capturing a partly covered window.
- Visual quality of Playwright's VP9 output on small editor text at 1920×1080.
- Behaviour on a GitHub `windows-2022` runner (screen size, video) for the fixture-art variant.

A one-hour spike (launch, screenshot, 10 s recording of an edit) would settle the first four.

## Sources

- Etch at `8a82e70`: `packages/extension/test/run.mts`, `test/suite.ts`, `test/preview.ts`,
  `src/preview/protocol.ts`, `webview/main.ts`, `packages/renderer/playwright.config.ts`,
  `test/draw.spec.ts`, `src/index.ts`, `.github/workflows/build.yml`, `CONTRIBUTING.md`,
  `packages/extension/README.md`, `docs/adr/0002-*.md`, `docs/spec/v1.md` —
  <https://github.com/happy-dwarf-team/etch>
- Playwright Electron API — <https://playwright.dev/docs/api/class-electron>
- Playwright videos — <https://playwright.dev/docs/videos>
- Playwright v1.64.1 source: `packages/playwright-core/src/server/videoRecorder.ts`,
  `screencast.ts`, `electron/electron.ts` — <https://github.com/microsoft/playwright/tree/v1.64.1>
- VS Code smoke tests: `test/automation/src/playwrightElectron.ts`, `electron.ts`,
  `test/smoke/README.md` — <https://github.com/microsoft/vscode/tree/main/test>
- VS Code CLI `serve-web` args: `cli/src/commands/args.rs` — <https://github.com/microsoft/vscode>
- Testing Extensions — <https://code.visualstudio.com/api/working-with-extensions/testing-extension>
- Webview API — <https://code.visualstudio.com/api/extension-guides/webview>
- Command line interface — <https://code.visualstudio.com/docs/configure/command-line>
- vscode-test-web — <https://github.com/microsoft/vscode-test-web>
- code-server install — <https://coder.com/docs/code-server/install>
- FFmpeg `ddagrab` and `gfxcapture`: `doc/filters.texi`; Changelog — <https://github.com/FFmpeg/FFmpeg>
- FFmpeg devices (`gdigrab`) — <https://ffmpeg.org/ffmpeg-devices.html>
- FFmpeg releases — <https://ffmpeg.org/index.html>
