# Steam Workshop pages

How Happy Dwarf Team mods and Anvil plugins present themselves on the Steam Workshop: the title, the tone and the sections of the description. The description lives in the mod's repository (e.g. `workshop/description.md`) and is published with [paradox-workshop-publish](https://github.com/happy-dwarf-team/paradox-workshop-publish), which turns Markdown into Steam BBCode.

## Title

`<Name> - <subtitle>`, for example `Anbennar - Proper 2K UI` or `Bellows - Faster Game Start`.

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

- **Short and plain.** A player reads the page on a phone in the Steam app, between two turns. Say what the mod gives them and what they need; the details live in the repository's README and the plugin page, linked from the page.
- **Plain first, joke second.** Every line starts with something a player understands without knowing how EU4 works inside.
- **Dwarven, not overdone.** Light, dry dwarven humour ("A beats Z. Dwarf law."), at most one dwarven touch per section.
- **No internals.**
  - No module names, file names, settings keys or function names.
  - Numbers only in human terms ("about 15 seconds instead of 35").
- **No promises the mod can't keep.**
  - Say "changes none of the files the game checks", not "achievements are guaranteed".
  - Say "should", "usually", "on our test machine" where it applies.

## Sections

In this order, and skip what has nothing to say. One divider image goes between the body and the footer:

```markdown
![](https://i.imgur.com/Uf8Z21n.png)
```

1. **Opening line** (bold, no heading): one sentence that sells the mod.
2. **A short paragraph:** what the mod gives the player, in two or three sentences, with one human-scale number if there is one.
3. **What you get:** 3–5 bullets, one line each, a bold lead-in first. One of them says what the mod does not touch: the checksum and ironman achievements, gameplay and multiplayer. Only claim what the mod really does; for a mod of only `descriptor.mod` and `anvil/**` the checksum stays unchanged. A plugin that reports to Anvil's start-up benchmark says in one bullet that the **Benchmark** tab in Anvil Manager compares starts with and without it.
4. **Not there yet** (optional): one bold-led line with the known limits.
5. **You need:** what must already be there, as bullets.
   - **Anvil plugins: Anvil comes first, linked to [anvil.happydwarf.dev](https://anvil.happydwarf.dev/)**, with its minimum version, and that the Workshop cannot install it.
   - The game version and store: Steam, and whether the GOG build works (from GitHub, since GOG has no Workshop).
   - Required mods, as links, and anything to remove first.
   - **Anvil plugins:** the last bullet says how to start it: start the game, approve the plugin in Anvil (Ctrl+Shift+F12, then Mods), restart, and that Anvil asks again after every update.
6. The divider, then the footer, each a single bold-led line:
   - **More:** links to the plugin page and the GitHub repository, saying in a few words what the reader finds there.
   - **More from Happy Dwarf Team:** (below).
   - **Credits** (or **Credits and licence**): the people and projects the mod builds on, with the licence notice where the original's licence asks for one, one personal, joking line, and the dwarf-head line (below). Where the name has a story, it gets one sentence here.

A page should stay around 2,000–3,000 characters in Markdown. Questions players ask go to the README or the plugin page, not to an FAQ on the Workshop.

### More from Happy Dwarf Team

```markdown
**More from Happy Dwarf Team:** [Anvil](https://anvil.happydwarf.dev/) · [<another plugin or mod>, <what it gives this reader>](<its Workshop item>) · [happydwarf.dev](https://happydwarf.dev/)
```

- **3–5 links,** the last always [happydwarf.dev](https://happydwarf.dev/).
- **Only what helps this page's reader.** A player of a big overhaul gets the faster start; a page for testers or modders gets the tools. Skip the page's own mod and anything its reader has no use for.
- **Links:** a Workshop mod links to its Workshop item, a tool to its website.
- **A few words per link,** in a player's words.

### The dwarf head

Every page ends its credits with:

```markdown
The little dwarf head on the thumbnail? The repository belongs to Happy Dwarf Team, and I am, in fact, a happy dwarf myself.
```

## Examples

- [Anbennar - Widescreen Loading Screens](https://github.com/happy-dwarf-team/eu4-anbennar-widescreen-loading-screens/blob/main/workshop/description.md): a content mod.
- [Bellows](https://github.com/happy-dwarf-team/bellows/blob/main/workshop/description.md): an Anvil plugin.
- New Anvil plugins start from the skeleton in [anvil-plugin-template](https://github.com/happy-dwarf-team/anvil-plugin-template/blob/main/workshop/description.md).
