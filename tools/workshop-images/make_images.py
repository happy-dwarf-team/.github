"""Renders the images of the Workshop pages: hero, install steps, tiles, banners and buttons.

    python tools/workshop-images/make_images.py --out ../anvil-website/public/workshop

Run it from a checkout next to anvil-website, which holds the plugin icons and serves the result at
https://anvil.happydwarf.dev/workshop/. It needs ImageMagick 7 (`magick`) and a Chromium with a working
--screenshot: set CHROME to its path, or install Playwright's chromium-headless-shell, which is found by
itself. Edge's headless mode writes no screenshot on Windows. A changed number means changing PAGES and
running this again; the image's URL stays, so the Workshop page needs no new publish.
"""
import argparse, glob, html, os, re, shutil, subprocess, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "tools/workshop-thumbnail/assets"
ICONS = ROOT.parent / "anvil-website/src/assets/plugins"
PATTERN = "~/AppData/Local/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe"


def icon(name):
    return re.sub(r' (width|height)="\d+"', "", (ICONS / f"{name}.svg").read_text(encoding="utf-8"))


DWARF = re.sub(r' (width|height)="[^"]+"', "", (ASSETS / "happy-dwarf.svg").read_text(encoding="utf-8"))

PAGES = {
    "bellows": dict(
        repo="bellows", icon="bellows", name="BELLOWS", tag="Faster EU4. Same game.",
        stats=[("START", "41 → 13s", "10 mods, our test machine"), ("YEARS", "27 → 20s", "year 1720, speed 5")],
        steps=[("Install Anvil", "Once. Run it, click Install Anvil."), ("Subscribe", "Enable Bellows in your playset."), ("Approve", "Ctrl+Shift+F12, Mods, approve."), ("Restart", "Done. Enjoy the shorter wait.")],
        tiles_title="WHAT IT DOESN'T TOUCH",
        tiles=[("Same game", "No game files or rules change."), ("Ironman stays", "Achievements stay available."), ("Multiplayer in sync", "233 days, no out-of-sync."), ("Check it yourself", "Benchmark tab in Anvil Manager.")],
    ),
    "hamweard": dict(
        repo="hamweard", icon="hamweard", name="HAMWEARD", tag="Home to the menu. No restart.",
        stats=[("BACK TO MENU", "4s", "usually, without a restart"), ("TESTED", "66 returns", "in one day, no crash")],
        steps=[("Install Anvil", "Once. Run it, click Install Anvil."), ("Subscribe", "Enable Hamweard in your playset."), ("Approve", "Ctrl+Shift+F12, Mods, approve."), ("Restart", "From then on, no more restarts.")],
        tiles_title="GOOD TO KNOW",
        tiles=[("Ironman", "Off unless you allow it in Anvil."), ("Multiplayer", "Exit to Menu restarts as usual."), ("Canals", "After a save with one, a restart."), ("Your saves", "Nothing is left in them.")],
    ),
    "tongs": dict(
        repo="tongs", icon="tongs", name="TONGS", tag="Scripts and AI agents, through the front door.",
        stats=[("SEE", "the game", "date, speed, windows, events"), ("PLAY", "if allowed", "keys, clicks, console: one switch each")],
        steps=[("Install Anvil", "Once. Run it, click Install Anvil."), ("Subscribe", "Enable Tongs in your playset."), ("Approve", "Ctrl+Shift+F12, Mods, approve."), ("Switch on", "Same panel. It starts off."), ("Restart", "Point your script at it.")],
        tiles_title="SAFE BY DEFAULT",
        tiles=[("Starts off", "It does nothing until you say so."), ("Your PC only", "No one on the internet gets in."), ("Reading changes nothing", "Input needs its own switch."), ("Ready clients", "PowerShell, Python, MCP.")],
    ),
    "mei": dict(
        repo="mei", icon="mei", name="MEI 銘", tag="Chinese, Japanese and Korean text in EU4.",
        stats=[("TEXT", "中 日 한", "menus, events, the map"), ("FONTS", "13,000", "characters, from Source Han Sans")],
        steps=[("Install Anvil", "Once. Run it, click Install Anvil."), ("Subscribe", "Mei and your translation mod."), ("Approve", "Ctrl+Shift+F12, Mods, approve."), ("Restart", "Nothing to configure.")],
        tiles_title="WHAT YOU GET",
        tiles=[("Text that shows", "Old patch packs work as they are."), ("Proper line breaks", "No crash on a long paragraph."), ("Fonts included", "Where the game's own have none."), ("Search and typing", "Characters, pinyin, initials.")],
        extra=["TRANSLATION MODS", "NOT THERE YET"],
        labels=dict(install="INSTALL", time="1 minute"),
    ),
    "mei-schinese": dict(
        repo="mei", icon="mei", name="MEI 銘", tag="让《欧陆风云4》显示中文、日文和韩文",
        stats=[("文字", "中 日 한", "菜单、事件和地图"), ("字体", "13,000", "个字，思源黑体")],
        steps=[("安装 Anvil", "只需一次。运行后点击 Install Anvil。"), ("订阅", "Mei 和你的汉化 Mod。"), ("批准", "Ctrl+Shift+F12，Mods，批准。"), ("重启", "无需任何设置。")],
        tiles_title="你将得到",
        tiles=[("文字正常显示", "旧补丁的汉化包无需修改。"), ("正确换行", "长段落不再闪退。"), ("自带字体", "游戏字体没有的文字由 Mei 补上。"), ("搜索和输入", "汉字、拼音和首字母。")],
        extra=["汉化 MOD", "尚未完成"],
        labels=dict(install="安装", time="1 分钟", docs="文档", github="GITHUB", credits="致谢与许可", coll="HAPPY DWARF 的其他作品", collsub="Workshop 合集：我们所有的 EU4 插件"),
    ),
    "mei-tchinese": dict(
        repo="mei", icon="mei", name="MEI 銘", tag="讓《歐陸風雲4》顯示中文、日文和韓文",
        stats=[("文字", "中 日 한", "選單、事件和地圖"), ("字型", "13,000", "個字，思源黑體")],
        steps=[("安裝 Anvil", "只需一次。執行後點擊 Install Anvil。"), ("訂閱", "Mei 和你的中文化 Mod。"), ("核准", "Ctrl+Shift+F12，Mods，核准。"), ("重新啟動", "無需任何設定。")],
        tiles_title="你將得到",
        tiles=[("文字正常顯示", "舊補丁的中文化包無需修改。"), ("正確換行", "長段落不再閃退。"), ("自帶字型", "遊戲字型沒有的文字由 Mei 補上。"), ("搜尋和輸入", "漢字、拼音和首字母。")],
        extra=["中文化 MOD", "尚未完成"],
        labels=dict(install="安裝", time="1 分鐘", docs="文件", github="GITHUB", credits="致謝與授權", coll="HAPPY DWARF 的其他作品", collsub="Workshop 合集：我們所有的 EU4 外掛"),
    ),
}

CSS = """
@font-face { font-family:JB; font-weight:400; src:url('FONT_R'); }
@font-face { font-family:JB; font-weight:700 800; src:url('FONT_B'); }
:root { --forge:#16171a; --surface:#1f2024; --accent:#f5922a; --cream:#f5f3ee; --muted:#a8a29e; }
* { box-sizing:border-box; } html, body { margin:0; background:#000; }
.shot { width:636px; font-family:JB, 'Microsoft YaHei', 'Microsoft JhengHei', sans-serif; color:var(--cream); overflow:hidden; }
.half { width:314px; }
.ic { display:inline-block; color:var(--accent); flex:none; } .ic svg { width:100%; height:100%; display:block; }
.banner { background:radial-gradient(120% 220% at 0% 50%, #3d2611 0%, var(--forge) 55%); border-bottom:2px solid var(--accent); padding:11px 16px; font-weight:800; font-size:17px; letter-spacing:.14em; display:flex; align-items:center; gap:12px; }
.banner small { margin-left:auto; color:var(--muted); font-weight:400; font-size:11px; letter-spacing:.04em; }
.hero { background:radial-gradient(70% 120% at 50% 0%, #3d2611 0%, var(--forge) 70%); padding:20px; border-bottom:3px solid var(--accent); }
.top { display:flex; align-items:center; gap:14px; margin-bottom:14px; }
.name { font-weight:800; font-size:34px; letter-spacing:.12em; line-height:1.1; } .sub { color:var(--muted); font-size:12.5px; }
.stats { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
.stat { background:var(--surface); border-radius:8px; padding:10px 12px; } .k { font-weight:700; font-size:12px; letter-spacing:.1em; } .v { color:var(--accent); font-weight:800; font-size:27px; line-height:1.25; white-space:nowrap; } .c { color:var(--muted); font-size:11px; }
.steps { display:grid; gap:8px; background:var(--forge); padding:12px; }
.step { background:var(--surface); border-top:3px solid var(--accent); border-radius:4px; padding:9px; } .n { color:var(--accent); font-weight:800; font-size:22px; line-height:1; } .t { font-weight:700; font-size:12px; margin:6px 0 3px; } .d { color:var(--muted); font-size:10.5px; line-height:1.35; }
.tiles { display:grid; grid-template-columns:1fr 1fr; gap:8px; background:var(--forge); padding:12px; }
.tile { background:var(--surface); border-left:3px solid var(--accent); padding:10px 12px; } .tile .t { font-size:13px; margin:0; } .tile .d { font-size:11px; margin-top:3px; }
.btn { display:flex; align-items:center; justify-content:space-between; background:var(--accent); color:var(--forge); font-weight:800; font-size:13px; letter-spacing:.08em; padding:15px 16px; }
.btn.ghost { background:var(--forge); color:var(--accent); box-shadow:inset 0 0 0 2px var(--accent); }
.arrow { font-size:18px; line-height:1; }
.coll { display:flex; align-items:center; gap:14px; background:radial-gradient(120% 220% at 100% 50%, #3d2611 0%, var(--forge) 60%); box-shadow:inset 0 0 0 2px var(--accent); padding:12px 16px; }
.ct { flex:1; } .cn { font-weight:800; letter-spacing:.1em; font-size:16px; } .cs { color:var(--muted); font-size:11.5px; margin-top:3px; } .coll .arrow { color:var(--accent); }
"""


def shots():
    done = {}
    for key, p in PAGES.items():
        mark = lambda s: f'<span class="ic" style="width:{s}px;height:{s}px">{icon(p["icon"])}</span>'
        lab = p.get("labels", {})
        banner = lambda t, s="": f'<div class="banner">{mark(22)}{html.escape(t)}{f"<small>{html.escape(s)}</small>" if s else ""}</div>'
        done[f"{key}-hero"] = ("", f'<div class="hero"><div class="top">{mark(44)}<div><div class="name">{p["name"]}</div><div class="sub">{html.escape(p["tag"])}</div></div></div><div class="stats">' + "".join(f'<div class="stat"><div class="k">{k}</div><div class="v">{v}</div><div class="c">{c}</div></div>' for k, v, c in p["stats"]) + "</div></div>")
        done[f"{key}-install"] = ("", banner(lab.get("install", "INSTALL"), lab.get("time", "1 minute")))
        n = len(p["steps"])
        done[f"{key}-steps"] = ("", f'<div class="steps" style="grid-template-columns:repeat({n},1fr)">' + "".join(f'<div class="step"><div class="n">{i}</div><div class="t">{html.escape(t)}</div><div class="d">{html.escape(d)}</div></div>' for i, (t, d) in enumerate(p["steps"], 1)) + "</div>")
        done[f"{key}-tiles-title"] = ("", banner(p["tiles_title"]))
        done[f"{key}-tiles"] = ("", '<div class="tiles">' + "".join(f'<div class="tile"><div class="t">{html.escape(t)}</div><div class="d">{html.escape(d)}</div></div>' for t, d in p["tiles"]) + "</div>")
        done[f"{key}-faq"] = ("", banner("FAQ"))
        done[f"{key}-credits"] = ("", banner(lab.get("credits", "CREDITS")))
        done[f"{key}-docs"] = ("half", f'<div class="btn"><span>{lab.get("docs", "SETTINGS AND DOCS")}</span><span class="arrow">→</span></div>')
        done[f"{key}-github"] = ("half", f'<div class="btn ghost"><span>{lab.get("github", "VIEW ON GITHUB")}</span><span class="arrow">→</span></div>')
        for i, t in enumerate(p.get("extra", [])):
            done[f"{key}-extra{i}"] = ("", banner(t))
        coll = lab.get("coll", "MORE FROM HAPPY DWARF")
        sub = lab.get("collsub", "All our EU4 plugins in one Workshop collection")
        suffix = key.split("-")[1] if "-" in key else "en"
        done.setdefault(f"collection-{suffix}", ("", f'<div class="coll"><span class="ic" style="width:64px;height:64px">{DWARF}</span><div class="ct"><div class="cn">{coll}</div><div class="cs">{sub}</div></div><span class="arrow">→</span></div>'))
    return done


def chrome():
    found = os.environ.get("CHROME") or next(iter(sorted(glob.glob(os.path.expanduser(PATTERN)), reverse=True)), None)
    if not found:
        raise SystemExit("set CHROME to a Chromium with --screenshot")
    return found


def render(items, out):
    # Each image is one screenshot on magenta, trimmed to its edges.
    tmp = Path(tempfile.mkdtemp())
    css = CSS.replace("FONT_R", (ASSETS / "JetBrainsMono-Regular.ttf").as_uri()).replace("FONT_B", (ASSETS / "JetBrainsMono-Bold.ttf").as_uri())
    css += "html, body { background:#ff00ff !important; }"
    out.mkdir(parents=True, exist_ok=True)
    base = [chrome(), "--disable-gpu", "--no-sandbox", "--hide-scrollbars", f"--user-data-dir={tmp/'edge'}", "--allow-file-access-from-files", "--virtual-time-budget=2500", "--force-device-scale-factor=2", "--window-size=640,420"]
    for n, (cls, h) in items.items():
        sheet = tmp / f"{n}.html"
        sheet.write_text(f'<!doctype html><meta charset="utf-8"><style>{css}</style><div class="shot {cls}">{h}</div>', encoding="utf-8")
        png = tmp / f"{n}.png"
        subprocess.run(base + [f"--screenshot={png}", sheet.as_uri()], capture_output=True, timeout=60)
        subprocess.run(["magick", str(png), "-trim", "+repage", "-strip", str(out / f"{n}.png")], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print(len(items), "images")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True, type=Path)
    render(shots(), p.parse_args().out)
