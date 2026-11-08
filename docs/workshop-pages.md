# Steam Workshop pages

How Happy Dwarf Team mods and Anvil plugins present themselves on the Steam Workshop: the title, the tone and the sections of the description. The description lives in the mod's repository (e.g. `workshop/description.md`) and is published with [paradox-workshop-publish](https://github.com/happy-dwarf-team/paradox-workshop-publish), which turns Markdown into Steam BBCode.

## Title

`<Name> - <subtitle>`, for example `Anbennar - Proper 2K UI` or `Bellows - Faster Start, Faster Game`.

- **Subtitle:**
  - 2–4 words that say what the mod does, in a player's words;
  - no jargon;
  - no "Anvil": players don't need to know the loader's name to understand the mod.
- **Where it lives:** the title is the descriptor's `name`, so it is the same on Steam and in the launcher.

## Thumbnail

**Anvil plugins** use a generated preview image, never a hand-made placeholder:
- generate it with [`tools/workshop-thumbnail`](../tools/workshop-thumbnail) from the plugin's icon on the Anvil website (`src/assets/plugins/<id>.svg` in anvil-website), with the title's name and subtitle;
- commit it as `workshop/thumbnail.png`.

The result follows the website's look, shows the plugin icon and carries the Happy Dwarf Team logo. A plugin without an icon gets one on the website first.

Content mods keep their own artwork.

## Tone

- **A short, plain top.** The opening line, the short paragraph and "What you get" are what a player reads first, often on a phone in the Steam app: they say what the mod gives them in a few lines. The sections below carry what a player needs next (requirements, setup, limits), and the FAQ and Credits stay; they are part of the page and of its character.
- **Plain first, joke second.** Every section starts with something a player understands without knowing how EU4 works inside.
- **Dwarven, not overdone.** Light, dry dwarven humour ("A beats Z. Dwarf law."), at most one dwarven touch per section. The FAQ and Credits may be the most playful.
- **No internals.**
  - No module names, file names, settings keys or function names.
  - Numbers only in human terms ("about 15 seconds instead of 35").
  - Technical details belong in the repository's README; link it.
- **No promises the mod can't keep.**
  - Say "does not touch the files the game checks", not "achievements are guaranteed".
  - Say "should", "usually", "on our test machine" where it applies.

## Sections

Anvil plugins, in this order. A section that has nothing to say goes. Images come from [`tools/workshop-images`](../tools/workshop-images) and are served from `https://anvil.happydwarf.dev/workshop/`; everything a player must search, copy or click stays text.

1. **Hero image:** the plugin's name, a short tagline and two measured facts.
2. **A short paragraph:** what the plugin gives the player, in two or three sentences.
3. **Install:** the banner, the steps image (one action per step, a bold verb first in the source; a plugin that needs another step, like Tongs, adds it before the restart), then one paragraph with the minimum Anvil, the game versions, what to do if Windows warns about Anvil, and anything to remove first.
4. **Tiles:** a banner and four tiles: what the plugin leaves alone, or what the player should know. Limits that matter stay honest; a sentence of text under the tiles may carry what four tiles can't.
5. **Sections a plugin needs of its own**, as a banner and text, such as Mei's translation mods.
6. **Buttons:** `SETTINGS AND DOCS` to the plugin's page on the Anvil website, `VIEW ON GITHUB` to the repository. Settings, the benchmark and how the plugin works live there, not here. Below them, on its own line, the `ASK US ON DISCORD` button (`discord-en.png`, or the page's language) to <https://discord.happydwarf.dev/>. The FAQ keeps its text entry "Something's wrong. Where do I ask?" with the same link, for players who skip images.
7. **FAQ:** banner and text. The usual questions, at least: why approve it, GOG, the name if it has a story, and last the dwarf head on the thumbnail.
8. **Credits:** banner and text, one line each, a bold name first. People and projects the plugin stands on come first, with their licence.
9. **Collection button:** the image with the Happy Dwarf logo, linking to [our Workshop collection](https://steamcommunity.com/sharedfiles/filedetails/?id=3833899418). Content mods end with it too.

Steam takes at most 8000 bytes of BBCode; an image adds about 60. Images stay under 1 MB. A translated page gets its own images.

Content mods stay text: required mods, the game version, what the mod doesn't touch, link lists, FAQ, Credits, and the collection button at the end.

### The standing FAQ entry

```markdown
### What is that little dwarf head on the thumbnail?
If you check the mod's GitHub page, you will notice the repository belongs to Happy Dwarf Team.

I like dwarves.
I like being happy.
I am, in fact, a happy dwarf myself.
```

## Examples

- [Anbennar - Widescreen Loading Screens](https://github.com/happy-dwarf-team/eu4-anbennar-widescreen-loading-screens/blob/main/workshop/description.md): a content mod.
- [Bellows](https://github.com/happy-dwarf-team/bellows/blob/main/workshop/description.md): an Anvil plugin.
- New Anvil plugins start from the skeleton in [anvil-plugin-template](https://github.com/happy-dwarf-team/anvil-plugin-template/blob/main/workshop/description.md).
