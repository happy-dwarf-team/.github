# PROTOTYPE: organization home page (throwaway)

Answers [#12](https://github.com/happy-dwarf-team/.github/issues/12) "What does the organization home page look like?"
for `happydwarf.dev`. Not production code; this branch is never merged.

`index.html` is the body of a single page (published as a private claude.ai Artifact, which adds the
document skeleton). Three structurally different variants of the home page plus the 404 page, switched
from the floating bar at the bottom (or the ← / → keys); "No motion" simulates `prefers-reduced-motion`, and the plugin button adds made-up example plugins (all, or capped at five on the hub with a link to the Anvil catalog) to test how the Anvil group grows.

- **A · Stacked groups**: centred hero, each project group a heading and a card grid, Anvil full width on top.
- **B · Ledger** (picked): left-aligned hero with a large logo, each group a sticky rail beside dense project rows.
- **C · Ecosystem map**: compact hero, Anvil as the trunk with its plugins branching off, the other two groups side by side.

Content comes from #9, tokens from #11 (family orange, Etch's verdigris on its icon only). Icons for the
Plugin template, paradox-workshop-publish, the two Anbennar mods and the favicon glyph are first drafts.

## Verdict

The user picked **B · Ledger**, with the Anvil group capped at five plugins plus the Plugin template and a
link to the Anvil plugin catalog once there are more than five plugins. A and C were rejected. The decisions
are in the resolution comment on #12.

Screenshots of the pick (rendered in headless Edge): [desktop](screenshots/ledger-desktop.png),
[desktop with 11 plugins, capped](screenshots/ledger-desktop-11-plugins-capped.png),
[phone, 375 px](screenshots/ledger-phone-375.png).
