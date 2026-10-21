# PROTOTYPE: Etch capture spike (throwaway)

Spike for [#15](https://github.com/happy-dwarf-team/.github/issues/15) "Does Playwright's Electron
driver capture Etch's preview sharply?" (map [#4](https://github.com/happy-dwarf-team/.github/issues/4)).
Not production code: no tests, no error handling. The verdict lives in the resolution comment on #15.
No screenshots or videos are committed here, because they show EU4 art.

## What it does

`capture.mjs` launches VS Code 1.142.0 (downloaded by `@vscode/test-electron`) with Etch loaded through
`--extensionDevelopmentPath`, a fresh user data dir and seeded settings, drives it with Playwright's
`_electron` (1.64.1, from Etch's own `@playwright/test`), sets the window to 1920×1080 with
`BrowserWindow.setBounds`, opens **Etch: Open Preview** on a copy of a vanilla `.gui` in a scratch mod
folder, finds the webview frame that holds `canvas#screen`, takes `page.screenshot()` PNGs and records
`recordVideo` while it types edits (Find, Escape, type over the selection). Options:

- `DPR=2` adds `--force-device-scale-factor=2`.
- `GFX=1` also records the same window by HWND with FFmpeg `gfxcapture` into a lossless master.
- `OCCLUDE=1` covers the window with another always-on-top window, then minimises it, editing each time.
- `LOOP=1` uses a six-edit sequence that ends where it started (a seamless loop).

`encode.sh` cuts ~15.3 s masters and encodes them with ticket #8's VP9 (two-pass, `-tune-content
screen`, `-deadline good -cpu-used 1`) and H.264 (`-preset veryslow`, `+faststart`) settings at
several CRFs, then reports size and SSIM against the master.

## Run (Windows 11, EU4 installed, full FFmpeg >= 8.1)

```sh
git clone https://github.com/happy-dwarf-team/etch && cd etch && pnpm install --frozen-lockfile
node packages/extension/build.mts
ETCH_ROOT=<etch> SHORT=<short folder, e.g. %TEMP%\e15> OUT=<out> FFMPEG=<ffmpeg.exe> \
  EU4_GUI="<EU4>/interface/ages_view.gui" DPR=1 GFX=1 LOOP=1 node capture.mjs
bash encode.sh <ffmpeg bin folder> <out root>
```

`SHORT` matters: with VS Code unpacked under a long scratch path the workbench fails to load
(`workbench.html net::ERR_FILE_NOT_FOUND`, MAX_PATH), so VS Code and its user data go to a short folder.

## Verdict (2026-10-21)

The capture works; see the resolution comment on #15 for the measurements. Picked by the user:
Playwright drives VS Code and takes the PNG stills; loops come from either `recordVideo` or a
`gfxcapture` lossless master, chosen by a flag in the script; capture at device scale 2 and publish
1920 px wide web files; start at VP9 CRF 34 and H.264 CRF 23 and re-check on the real scenes.
