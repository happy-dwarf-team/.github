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

In this order. Skip a section that has nothing to say. Separate sections with the divider image:

```markdown
![](https://i.imgur.com/Uf8Z21n.png)
```

1. **Opening line** (bold, no heading): one sentence that sells the mod.
2. **Overview**, without a heading:
   - a short paragraph: what the mod gives the player, in two or three sentences, with one human-scale number if there is one;
   - **What you get:** 3–5 bullets, one line each, a bold lead-in first. A plugin that reports to Anvil's start-up benchmark says in one bullet that the **Benchmark** tab in Anvil Manager compares starts with and without it.

   Details that do not fit there (how it works, the settings) get a section of their own further down, not a longer overview.
3. **Before you subscribe:** what must already be there.
   - Required mods, as links, and anything to remove first.
   - The supported game version and store: Steam, and whether the GOG build works (from GitHub, since GOG has no Workshop).
   - **Anvil plugins: Anvil comes first, linked to [anvil.happydwarf.dev](https://anvil.happydwarf.dev/)**, with its minimum version, whose Download button is the easiest way in. Say plainly that the Workshop cannot install Anvil.
4. **Getting it running** (Anvil plugins): numbered steps, one action each.
   1. Subscribe and enable the mod in the playset.
   2. Start the game; Anvil says a new plugin is waiting.
   3. Approve the plugin in Anvil's panel (Ctrl+Shift+F12 → **Mods**) or in Anvil Manager.
   4. Restart.

   Then one line: Anvil asks again after every update, and the previously approved version keeps working until then.
5. **In the settings** (optional): the settings a player may want to change, by the name shown in Anvil, each with what it gives and whether it is on by default.
6. **What it doesn't touch:** checksum and ironman achievements, gameplay and multiplayer, and that unsubscribing leaves nothing behind. Only claim what the mod really does; for a mod of only `descriptor.mod` and `anvil/**` the checksum stays unchanged.
7. **Current state** or **Not there yet** (optional): what works, what is still rough.
8. **Required / Recommended / Compatible / Integrated mods** (optional): link lists. They are for the mod's own dependencies and what it works with; the rest of the team's work goes in the next section.
9. **More from Happy Dwarf Team:** every team page has it, in the format below.
10. **Alternative download:** the GitHub repository (and, for an Anvil plugin, its page on anvil.happydwarf.dev).
11. **FAQ:**
    - 4–6 questions players really ask (load order, compatibility, "why do I have to approve it", "it didn't get faster", "I play on GOG");
    - short answers, the joke after the answer;
    - always end with the dwarf-head question (below).
12. **Credits:**
    - the people and projects the mod builds on, with the licence notice where the original's licence asks for one;
    - one personal, joking line at the end ("All dwarves for staying short and strong").

A mod with a story behind its name tells it in a short "Why …?" section after the overview.

### More from Happy Dwarf Team

```markdown
## More from Happy Dwarf Team
- **[Anvil](https://anvil.happydwarf.dev/)**: <one plain sentence>
- **[<another plugin or mod>](<its Workshop item>)**: <what it gives this page's player or tester>
- **[Etch](https://etch.happydwarf.dev/)**: for interface modders, see your `.gui` window as the game draws it, right in VS Code.
- Everything we make: [happydwarf.dev](https://happydwarf.dev/)
```

- **3–5 entries,** the last always the [happydwarf.dev](https://happydwarf.dev/) line.
- **Only what helps this page's reader.** A player of a big overhaul gets the faster start; a page for testers or modders gets the tools. Skip the page's own mod and anything its reader has no use for.
- **Links:** a Workshop mod links to its Workshop item, a tool to its website.
- **One sentence per entry,** in a player's words, as the Tone section says: no internals, numbers only in human terms.

### Measure it yourself

A plugin that reports to Anvil's start-up benchmark (Anvil 1.5 or newer, the **Benchmark** tab in Anvil Manager) says so on its page: a short "Measure it yourself" section, or an FAQ entry of that name. In two or three sentences: open Anvil Manager, pick the plugin on the Benchmark tab, and it compares starts with and without it on the player's own computer. Link the privacy page ([benchmark-privacy.md](https://github.com/happy-dwarf-team/anvil/blob/main/docs/benchmark-privacy.md)) for what the report contains.

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
