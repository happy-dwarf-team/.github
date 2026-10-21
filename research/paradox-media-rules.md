# What Paradox's rules allow for EU4 art in Etch media

Research for [happy-dwarf-team/.github#7](https://github.com/happy-dwarf-team/.github/issues/7) (map: #4).
Sources retrieved on **2026-10-21**. **This is not legal advice**; it is a reading of Paradox's public terms
for planning the Etch site (`etch.happydwarf.dev`).

## Short answer

Paradox has **no separate fan-content policy, mod policy page or public trademark/brand guidelines** for
Europa Universalis IV. The governing text is the **Paradox User Agreement** (last update 2026-01-21), which
EU4's own Steam EULA points to. Its section 6 lets anyone make *videos, live streams or artwork* containing
gameplay and screenshots, if the content is free to the public, adds the creator's own creative input, uses
only released games, and does not imply official endorsement. Section 5 lets the community make and publish
UGC (explicitly including "scripts and programs" and mods) for non-commercial purposes only.

For a free, non-commercial Etch website, screenshots and short silent recordings of Etch rendering EU4
interface art from local game files fit these terms, as long as Etch's own UI and the mod author's work are
the subject (not bare copies of game art), no game files are redistributed, and the site states plainly that
it is unofficial. Nothing grants a right to use the **EU4 or Paradox logos**; use the name "Europa Universalis
IV" only as plain text to say what Etch works with.

## What the sources say

### 1. The User Agreement governs EU4

- EU4's Steam EULA (app 236850) consists only of a pointer: buyers agree to the Paradox User Agreement and
  Privacy Policy.
  Source: <https://store.steampowered.com/eula/236850_eula_0>
- The User Agreement covers Paradox games "and thereto related content, mod tools ... websites, forums".
  Header: "Last update: January 21, 2026". Amendments take effect 30 days after posting (section 13).
  Source: <https://legal.paradoxplaza.com/eula>
- The old standalone mod policy URL, `https://www.paradoxplaza.com/mod-static-info-ca.html` (still linked from
  the World of Darkness Dark Pack agreement), now **redirects to the User Agreement**. `paradoxplaza.com/mod-policy`
  returns 404. Verified with `curl -L` on the retrieval date.

### 2. Screenshots, videos and artwork (User Agreement section 6, "Streaming Paradox Games")

Source: <https://legal.paradoxplaza.com/eula>, section 6.

- Permitted: videos, live streams or artwork containing gameplay, music, sound and screenshots
  ("Paradox Game Content"), shared on "media sharing websites such as Twitch, YouTube, Bilibili, Reddit, etc."
- Must be free to the public; no paywall.
- Monetization only via those sites' official affiliate, advertising or partner programs; any other
  monetization of Paradox Game Content is not permitted.
- Only from officially released games or officially released promotional material.
- Required: "your own creative input and commentary". The section forbids videos and images that are
  mere copies of Paradox Game Content without creative input.
- Third-party IP (e.g. music) is the creator's responsibility; soundtracks may never be distributed apart
  from footage; music from the EU4 Sabaton soundtrack may not be used at all.
- Not permitted: to "imply or state that your videos are officially affiliated with, sponsored, endorsed,
  or approved" by Paradox, unless directed to.

### 3. User-generated content, tools and mods (User Agreement section 5)

Source: <https://legal.paradoxplaza.com/eula>, section 5.

- Paradox grants the right to create and make UGC publicly available "for non-commercial purposes".
- "UGC" explicitly includes "scripts and programs", mods, gameplay and other works relating to the Services.
- UGC must not contain unlawful or infringing material.
- The creator's rights extend only to their own new, original content, not to the game or content Paradox
  makes available through it.
- UGC must be free and freely available; donations (e.g. Patreon) and sponsorships are allowed.
- Paradox does not own the IP of every game, so UGC is not allowed unconditionally for all games
  (contact support for which games). EU4 is Paradox-owned (see 5 below).
- By publishing UGC, the creator grants Paradox a broad, perpetual, royalty-free license to it.
- Paradox may restrict or remove UGC at its sole discretion.

### 4. Logos, the game name and trademark notices

- **No public trademark or brand-use guidelines** were found on `paradoxinteractive.com`, `paradoxplaza.com`
  or `legal.paradoxplaza.com`. Searched: legal pages, the Corporate Media page, the Image bank, and probes of
  `/legal`, `/brand`, `/press` (404).
- The Image bank (<https://www.paradoxinteractive.com/media/image-bank>) offers no usage terms and no EU4
  entry. The Licensing Request Form (<https://www.paradoxinteractive.com/contact/licensing-request-form>) is
  aimed at business partners (merchandise, board games, films, etc.), not fan projects.
- EU4's Steam store page carries Paradox's own notice: ©2013 and published by Paradox Interactive AB;
  EUROPA UNIVERSALIS and PARADOX INTERACTIVE are trademarks and/or registered trademarks of
  Paradox Interactive AB in Europe, the U.S. and other countries.
  Source: <https://store.steampowered.com/app/236850/>
- The User Agreement and the Rules of Conduct grant no trademark or logo license. The Rules of Conduct
  (last update 2022-05-02) list "Unauthorized copyrighted or trademarked material" as not allowed on
  Paradox platforms. Source: <https://legal.paradoxplaza.com/rules-of-conduct>
- An older Paradox *Terms of Use* (2019-04-05, still hosted as the Steam EULA of *Surviving the Aftermath*)
  says nothing in it grants any trademark license, and forbids meta tags or hidden text using Paradox's
  name or trademarks. Its mod section bars third-party logos "except for those assets provided by Paradox".
  It is not EU4's current agreement; cited only as evidence of Paradox's stance.
  Source: <https://store.steampowered.com/eula/684450_eula_2>
- **For comparison only** (does not cover EU4): Paradox's World of Darkness *Dark Pack* program allows
  non-commercial fan websites without asking, but requires a legal statement and the Dark Pack logo when
  promoting. No equivalent program exists for EU4.
  Source: <https://www.paradoxinteractive.com/games/world-of-darkness/community/dark-pack-agreement>

### 5. Ownership of the EU4 name

- USPTO registration 3831875 for EUROPA UNIVERSALIS (video game software), owner Paradox Interactive AB,
  renewed 2019 (via the Justia record of USPTO data):
  <https://trademarks.justia.com/owners/paradox-interactive-ab-998900>. Secondary mirror of a primary
  register; the EU4 Steam notice above confirms the claim first-hand.

## Interpretation for the Etch site

These are our readings, not statements from Paradox.

**Likely allowed**

- Screenshots and short silent loops of Etch at work (VS Code, a `.gui` file, the preview drawing an EU4
  window from the user's local install, outlines, diagnostics). The subject is Etch and the mod author's
  layout; that is the "creative input" section 6 asks for. Captions on the site add commentary.
- Hosting these on our own free site (and on R2). Section 6 lists media-sharing sites "such as" YouTube;
  it does not name project websites, so this is a reasonable reading rather than an explicit grant. The
  terms that matter are met: free, no paywall, no monetization.
- Writing "Europa Universalis IV" (or "EU4") in plain text to say what Etch is for, e.g. "a VS Code
  extension for Europa Universalis IV interface mods". That is descriptive use of the name, not branding.

**Required by the terms (as we read them)**

- Free access, no paywall, no ads or sales tied to the media. Donations/sponsorship are tolerated by
  section 5, but the site has none.
- Own creative input in every image or clip: never publish a frame that is only game art.
- No implied endorsement: a clear "unofficial, not affiliated" line.
- No game audio. The planned silent loops already satisfy this.

**Advisable, not required by any source**

- A footer disclaimer combining the `anvil-website` line with Paradox's own trademark notice, e.g.:

  > Etch is an unofficial community project, not affiliated with or endorsed by Paradox Interactive.
  > Europa Universalis and Paradox Interactive are trademarks or registered trademarks of Paradox
  > Interactive AB. Game interface art shown in screenshots is © Paradox Interactive AB and is rendered
  > from a local copy of the game; Etch does not include or distribute game files.

  No Paradox source mandates exact wording; this mirrors the Steam notice and section 6's endorsement rule.
- Keep the Etch name, icon and accent free of the EU4 or Paradox logos, the EU4 key art, and Paradox's
  trade dress.
- Do not put the game name in hidden text or meta keywords beyond normal descriptive titles.
- Keep the share of game art in each frame modest (crop to the window being edited, show the editor
  beside it) and prefer vanilla or our own test mods over third-party mods, whose authors hold their own rights.

**Not allowed / avoid**

- Using the Europa Universalis IV logo, the Paradox logo or official key art as site branding, hero
  images, favicon or Open Graph image. No license exists; the Image bank has no terms.
- Distributing extracted game files (`.dds`, `.gfx`, fonts, sounds), e.g. as downloadable assets, test
  fixtures in public repos or R2 objects. Section 5 gives no rights to Paradox content.
- Any paid tier, paywall or sale tied to the media.
- Wording such as "official", "approved by Paradox" or "for Paradox", or anything that implies a partnership.
- Media from unreleased content (betas, leaked builds).
- Game music, including the Sabaton soundtrack.

## Open points

- The User Agreement can change with 30 days' notice; re-check section 6 before each media refresh.
- If we ever want the EU4 logo, a sponsored listing or certainty about own-site hosting, the only route is
  asking Paradox in writing (no fan-program form exists for EU4).
