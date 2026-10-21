## Happy Dwarf Team

Open-source tools and mods for **Europa Universalis IV**. Our main project is
**[Anvil](https://anvil.happydwarf.dev)**, a plugin loader that lets native plugins
improve the game without changing `eu4.exe`, so Steam updates and file verification
keep working.

### Anvil and its plugins

| Project | What it is |
| --- | --- |
| [**Anvil**](https://github.com/happy-dwarf-team/anvil) | The plugin loader: a proxy `version.dll`, the plugin API (C, C++, Rust) and the `anvil` CLI for plugin authors |
| [**Bellows**](https://github.com/happy-dwarf-team/bellows) | Makes the game start faster, without changing game files or behaviour |
| [**Tongs**](https://github.com/happy-dwarf-team/tongs) | Lets scripts and agents control a running game: state, screenshots, keyboard and mouse |
| [**Plugin template**](https://github.com/happy-dwarf-team/anvil-plugin-template) | Start your own Anvil plugin: build, CI checks and releases ready to go |
| [**Website**](https://github.com/happy-dwarf-team/anvil-website) | Source of [anvil.happydwarf.dev](https://anvil.happydwarf.dev): install guide, plugin catalog and author docs |

### Tools for mod authors

| Project | What it is |
| --- | --- |
| [**Etch**](https://github.com/happy-dwarf-team/etch) | A Visual Studio Code extension that previews EU4 interface mods: edit a `.gui` or `.gfx` file and see the window as the game draws it (early preview) |
| [**paradox-workshop-publish**](https://github.com/happy-dwarf-team/paradox-workshop-publish) | `pdx-ws` and a GitHub Action that publish Paradox game mods to the Steam Workshop, driven by the mod descriptor |

### Anbennar mods

- [Proper 2K UI](https://github.com/happy-dwarf-team/eu4-anbennar-proper-2k-ui) (archived) – a proper 2K interface for the Anbennar mod
- [Widescreen loading screens](https://github.com/happy-dwarf-team/eu4-anbennar-widescreen-loading-screens) – Anbennar loading screens that fit widescreen monitors
- [Dwarven Knowledge patch](https://github.com/happy-dwarf-team/eu4-anbennar-proper-2k-ui-dwarven-knowledge-patch) (archived) – compatibility between Proper 2K UI and the Dwarven Knowledge submod

### Get involved

Install guide and plugin catalog: **[anvil.happydwarf.dev](https://anvil.happydwarf.dev)**.
Bug reports and ideas go to the issues of the project they concern; each repository's
`CONTRIBUTING.md` explains how to send a change, and `SECURITY.md` how to report a
vulnerability privately.

<sub>Unofficial community projects, not affiliated with Paradox Interactive. MIT licensed.</sub>
