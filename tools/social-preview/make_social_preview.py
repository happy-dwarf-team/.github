"""GitHub social preview image (1280x640) of a team repository, in the Anvil website's "dark forge" style.

    python make_social_preview.py --icon bellows.svg --name Bellows \
        --subtitle "Faster start-up for" --subtitle "Europa Universalis IV" \
        --kicker "Anvil plugin" --anvil-mark --out bellows.png

The icon's currentColor becomes the accent; a background square that fills the icon's whole
viewBox (as in Etch's extension icon) is dropped. Needs ImageMagick 7 (`magick`) with librsvg.
Fonts, the team logo and the anvil mark come from ../workshop-thumbnail/assets. See README.md.
"""
import argparse, os, re, shutil, subprocess, tempfile
from pathlib import Path

BG, ACCENT, ACCENT_SOFT = "#16171a", "#f5922a", "#3d2611"
TEXT, MUTED = "#f7f5f2", "#a8a29e"
W, H = 1280, 640


def raster(svg_text, size, out):
    """Rasterises SVG text to a transparent PNG that fits size x size."""
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False, encoding="utf-8") as f:
        f.write(svg_text)
    subprocess.run(["magick", "-background", "none", "-density", "1200", f"rsvg:{f.name}",
                    "-resize", f"{size}x{size}", out], check=True)
    os.unlink(f.name)


def icon_svg(path):
    svg = Path(path).read_text(encoding="utf-8").replace("currentColor", ACCENT)
    box = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg)
    if box:
        w, h = box.groups()
        svg = re.sub(rf'<rect width="{w}" height="{h}"[^>]*/>', "", svg, count=1)
    return svg


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--icon", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--subtitle", action="append", required=True, help="one line; give it twice for two lines")
    p.add_argument("--kicker", required=True, help="the accent line at the bottom left")
    p.add_argument("--anvil-mark", action="store_true", help="put the small anvil before the kicker (Anvil family)")
    p.add_argument("--assets", default=str(Path(__file__).parent.parent / "workshop-thumbnail" / "assets"))
    p.add_argument("--out", required=True)
    a = p.parse_args()
    assets = Path(a.assets)
    bold = (assets / "JetBrainsMono-Bold.ttf").as_posix()
    regular = (assets / "JetBrainsMono-Regular.ttf").as_posix()
    tmp = Path(tempfile.mkdtemp())

    raster(icon_svg(a.icon), 300, tmp / "icon.png")
    raster((assets / "happy-dwarf.svg").read_text(encoding="utf-8"), 96, tmp / "logo.png")
    raster((assets / "anvil-mark.svg").read_text(encoding="utf-8").replace("currentColor", ACCENT), 40, tmp / "anvil.png")

    name = a.name.upper()
    # JetBrains Mono advances 0.6 em per character; the text column is 660 px wide.
    name_pt = min(124, int(660 / (len(name) * 0.6 + (len(name) - 1) * 0.03)))
    subtitle = []
    for i, line in enumerate(a.subtitle[:2]):
        subtitle += ["-annotate", f"+524+{170 + name_pt + 40 + 56 * i}", line]
    if a.anvil_mark:
        kicker = [str(tmp / "anvil.png"), "-geometry", "+120+530", "-composite",
                  "-font", regular, "-pointsize", "30", "-fill", ACCENT, "-annotate", "+176+532", a.kicker]
    else:
        kicker = ["-font", regular, "-pointsize", "30", "-fill", ACCENT, "-annotate", "+120+532", a.kicker]

    subprocess.run([
        "magick", "-size", f"{W}x{H}", f"xc:{BG}",
        # A soft forge glow behind the icon.
        "(", "-size", "760x760", f"radial-gradient:{ACCENT_SOFT}-{BG}", ")",
        "-geometry", "-110-60", "-compose", "over", "-composite",
        str(tmp / "icon.png"), "-gravity", "northwest", "-geometry", "+120+150", "-composite",
        "-font", bold, "-pointsize", str(name_pt), "-fill", TEXT, "-kerning", "4", "-annotate", "+520+150", name,
        "-font", regular, "-pointsize", "36", "-fill", MUTED, "-kerning", "0", *subtitle,
        *kicker,
        # The team logo on the right, the accent bar below.
        str(tmp / "logo.png"), "-gravity", "southeast", "-geometry", "+60+44", "-composite",
        "-gravity", "northwest", "-fill", ACCENT, "-draw", f"rectangle 0,{H - 10} {W},{H}",
        "-depth", "8", "-strip", "-define", "png:compression-level=9", a.out,
    ], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print(a.out, os.path.getsize(a.out), "bytes")


if __name__ == "__main__":
    main()
