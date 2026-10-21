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
2. **Overview:** what the mod does, in a player's words, with one human-scale number if there is one.
3. **Before you subscribe:** what must already be there.
   - Required mods, as links.
   - The supported game version.
   - **Anvil plugins: Anvil comes first, linked to [anvil.happydwarf.dev](https://anvil.happydwarf.dev/)**, whose Download button is the easiest way in. Say plainly that the Workshop cannot install Anvil.
4. **Getting it running** (Anvil plugins): three numbered steps.
   1. Subscribe and enable the mod in the playset.
   2. Start the game and approve the plugin in Anvil's panel (Ctrl+Shift+F12 → **Mods**) or in Anvil Manager.
   3. Restart.

   Then one line: Anvil asks again after every update, and the previously approved version keeps working until then.
5. **What it doesn't touch:** checksum and ironman achievements, gameplay and multiplayer, and that unsubscribing leaves nothing behind. Only claim what the mod really does; for a mod of only `descriptor.mod` and `anvil/**` the checksum stays unchanged.
6. **Current state** (optional): what works, what is still rough.
7. **Required / Recommended / Compatible / Integrated mods** (optional): link lists.
8. **Alternative download:** the GitHub repository.
9. **FAQ:**
   - 4–6 questions players really ask (load order, compatibility, "why do I have to approve it", "it didn't get faster");
   - short answers, the joke after the answer;
   - always end with the dwarf-head question (below).
10. **Credits:**
    - the people and projects the mod builds on;
    - one personal, joking line at the end ("All dwarves for staying short and strong").

### The standing FAQ entry

```markdown
### What is that little dwarf head on the thumbnail?
If you check the mod's GitHub page, you will notice the repository belongs to Happy Dwarf Team.

I like dwarves.
I like being happy.
I am, in fact, a happy dwarf myself.
```

## Examples

- [Anbennar - Widescreen Loading Screens](https://steamcommunity.com/sharedfiles/filedetails/?id=3686212690): a content mod.
- [Bellows](https://github.com/happy-dwarf-team/bellows/blob/main/workshop/description.md): an Anvil plugin.
- New Anvil plugins start from the skeleton in [anvil-plugin-template](https://github.com/happy-dwarf-team/anvil-plugin-template/blob/main/workshop/description.md).
