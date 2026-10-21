# Workshop thumbnail

Generates the Steam Workshop preview image of an Anvil plugin in the "dark forge" style of [anvil.happydwarf.dev](https://anvil.happydwarf.dev/).

The image is 1024×1024 and about 125 KB, well under Steam's 1 MB limit. It shows:
- the plugin's icon in the accent colour, over a soft forge glow;
- the name in JetBrains Mono, upper case, with the subtitle below;
- an "Anvil plugin" mark on the left and the Happy Dwarf Team logo on the right;
- the accent bar along the bottom.

![Bellows example](https://raw.githubusercontent.com/happy-dwarf-team/bellows/main/workshop/thumbnail.png)

## Use

Needs Python 3 and ImageMagick 7 (`magick`, with its librsvg SVG renderer).

```sh
python tools/workshop-thumbnail/make_thumbnail.py   --icon ../anvil-website/src/assets/plugins/bellows.svg   --name Bellows --subtitle "Faster Game Start"   --out ../bellows/workshop/thumbnail.png
```

- **`--icon`:** the plugin's icon from anvil-website, `src/assets/plugins/<plugin id>.svg`. A plugin without one gets an icon there first, so the site and the Workshop show the same mark. The icon's `currentColor` becomes the accent `#f5922a`.
- **`--name`, `--subtitle`:** the two parts of the Workshop title `<Name> - <subtitle>` (see [docs/workshop-pages.md](../../docs/workshop-pages.md)). Names longer than 8 characters get a smaller font.

Commit the result as the mod's `thumbnail.png` (`workshop/thumbnail.png` in plugin repositories).

## Assets

- **`happy-dwarf.svg`, `anvil-mark.svg`:** copies of anvil-website's `src/assets/`. Update them here when the site's logo changes.
- **`JetBrainsMono-*.ttf`:** [JetBrains Mono](https://github.com/JetBrains/JetBrainsMono), the website's heading font, under the SIL Open Font License ([`JetBrainsMono-OFL.txt`](assets/JetBrainsMono-OFL.txt)).
