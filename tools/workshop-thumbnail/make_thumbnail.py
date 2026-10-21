"""Steam Workshop preview image for an Anvil plugin, in the Anvil website's "dark forge" style.

    python make_thumbnail.py --icon bellows.svg --name Bellows --subtitle "Faster Game Start" --out thumbnail.png

The icon is the plugin's icon from anvil-website (src/assets/plugins/<id>.svg); its currentColor
becomes the accent. Needs ImageMagick 7 (`magick`) with librsvg. See README.md.
"""
import argparse, os, shutil, subprocess, tempfile
from pathlib import Path

BG, SURFACE, ACCENT, ACCENT_SOFT = "#16171a", "#1f2024", "#f5922a", "#3d2611"
TEXT, MUTED = "#f7f5f2", "#a8a29e"
SIZE = 1024


def raster(svg_text, size, out):
    """Rasterises SVG text to a transparent PNG of size x size."""
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False, encoding="utf-8") as f:
        f.write(svg_text)
    subprocess.run(["magick", "-background", "none", "-density", "600", f"rsvg:{f.name}",
                    "-resize", f"{size}x{size}", out], check=True)
    os.unlink(f.name)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--icon", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--subtitle", required=True)
    p.add_argument("--assets", default=str(Path(__file__).parent / "assets"))
    p.add_argument("--out", required=True)
    a = p.parse_args()
    assets = Path(a.assets)
    bold, regular = assets / "JetBrainsMono-Bold.ttf", assets / "JetBrainsMono-Regular.ttf"
    tmp = Path(tempfile.mkdtemp())

    icon = Path(a.icon).read_text(encoding="utf-8").replace("currentColor", ACCENT)
    raster(icon, 460, tmp / "icon.png")
    raster((assets / "happy-dwarf.svg").read_text(encoding="utf-8"), 132, tmp / "logo.png")
    anvil = (assets / "anvil-mark.svg").read_text(encoding="utf-8").replace("currentColor", ACCENT)
    raster(anvil, 56, tmp / "anvil.png")

    name = a.name.upper()
    name_pt = 150 if len(name) <= 8 else max(80, int(150 * 8 / len(name)))
    subprocess.run([
        "magick", "-size", f"{SIZE}x{SIZE}", f"xc:{BG}",
        # A soft forge glow behind the icon.
        "(", "-size", f"{SIZE}x{SIZE}", f"radial-gradient:{ACCENT_SOFT}-{BG}", "-crop", f"{SIZE}x{SIZE}+0+0", ")",
        "-geometry", "+0-150", "-compose", "over", "-composite",
        str(tmp / "icon.png"), "-gravity", "north", "-geometry", "+0+120", "-composite",
        "-gravity", "north", "-font", bold.as_posix(), "-pointsize", str(name_pt), "-fill", TEXT,
        "-kerning", "4", "-annotate", "+0+600", name,
        "-font", regular.as_posix(), "-pointsize", "54", "-fill", MUTED, "-kerning", "0",
        "-annotate", "+0+790", a.subtitle,
        # Footer: "Anvil plugin" on the left, the team logo on the right, the accent bar below.
        "-gravity", "southwest", str(tmp / "anvil.png"), "-geometry", "+64+66", "-composite",
        "-font", regular.as_posix(), "-pointsize", "34", "-fill", ACCENT, "-annotate", "+136+76", "Anvil plugin",
        "-gravity", "southeast", str(tmp / "logo.png"), "-geometry", "+52+40", "-composite",
        "-gravity", "south", "-fill", ACCENT, "-draw", f"rectangle 0,{SIZE - 14} {SIZE},{SIZE}",
        "-depth", "8", "-strip", "-define", "png:compression-level=9", a.out,
    ], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print(a.out, os.path.getsize(a.out), "bytes")


if __name__ == "__main__":
    main()
