# Etch media: formats, loading and hosting

Research for [happy-dwarf-team/.github#8](https://github.com/happy-dwarf-team/.github/issues/8)
(map: [#4](https://github.com/happy-dwarf-team/.github/issues/4)). Researched 2026-10-21.

**Question.** The Etch site (`etch.happydwarf.dev`, static Astro on GitHub Pages) needs a few
short silent demo loops (5 to 20 s screen recordings of VS Code: sharp text, flat colours) and
screenshots. Which formats and encoder settings, how should the loops load, what does
accessibility require, and should the files live in the site repository or in Cloudflare R2 on
`media.happydwarf.dev`?

**Answer in one line.** Ship each loop as VP9 WebM with an H.264 MP4 fallback and a same-origin
poster, started from script only when motion is allowed and the loop is on screen, with a visible
pause button and a text description; **confirm R2** (custom domain `media.happydwarf.dev`,
immutable versioned keys) for the video files, and keep posters and screenshots in the site
repository so Astro optimises them.

Labels used below: **[doc]** is stated by a primary source, **[observed]** was checked live
during this research, **[inference]** is reasoning from those, **[to verify]** needs a test with
real recordings.

## 1. Formats and codecs

### Browser support

| Codec / container | Chrome, Edge | Firefox | Safari macOS | Safari iOS | Source |
|---|---|---|---|---|---|
| H.264 in MP4 | yes | yes (35+) | yes | yes | [caniuse mpeg4](https://caniuse.com/mpeg4) |
| VP9 in WebM | yes | yes | full from 16.0 (14.1 to 15.6 on macOS 11.3+) | full from 17.4; before that WebRTC only | [caniuse webm data](https://github.com/Fyrd/caniuse/blob/main/features-json/webm.json) |
| AV1 | Chrome 70+, Edge 121+ | 67+ | partial from 17.0 | partial from 17.0 | [caniuse av1 data](https://github.com/Fyrd/caniuse/blob/main/features-json/av1.json) |

- **[doc]** Safari's AV1 support is "Supported only on devices with hardware decoder, e.g.
  iPhone 15 Pro, M3 MacBook Pro" (caniuse note 4, every Safari and iOS version).
- **[doc]** Global usage per caniuse: H.264/MP4 97.49 %, WebM 97.25 %, AV1 95.97 % (79.04 % full).
- **[doc]** The browser plays the first `<source>` it can play and moves on if one fails
  ([MDN `<video>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/video)).
  The `type` attribute may carry a `codecs` parameter, which lets the browser skip a source
  without downloading it.

### Recommendation

1. **VP9 WebM first, H.264 MP4 second.** This is the pair web.dev uses for GIF replacement
   ([web.dev: replace GIFs with video](https://web.dev/articles/replace-gifs-with-videos)); in its
   example a 3.7 MB GIF became a 551 KB MP4 and a 341 KB WebM **[doc]**. The MP4 covers iOS before
   17.4 and anything without VP9 **[inference]**.
2. **No AV1 at launch.** It would be a third file per loop, and on Apple devices it only plays
   with a hardware decoder, so the H.264/VP9 pair is still needed **[inference]**. Revisit only if
   the VP9 files miss the size targets below.
3. **No animated GIF / APNG / animated WebP** for the loops: video is several times smaller per
   web.dev, and `<video>` gives pause control and posters **[doc + inference]**.
4. **Silent:** encode with `-an` (no audio track). **[doc]** Autoplay blocking "is _not_ applied
   to `<video>` elements when the source media does not have an audio track, or if the audio track
   is muted" ([MDN Autoplay guide](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Autoplay)).

### Encoding screen recordings

Screen content (thin text, flat fills, few changing pixels per frame) behaves differently from
camera footage. The settings below come from encoder documentation; the CRF values are starting
points **[to verify]** on the first real Etch recording.

**Capture and master** **[inference]**

- Record a lossless or near-lossless master (for example a PNG sequence or lossless H.264/FFV1)
  and derive every web file from it, so the per-release script can re-encode without re-recording.
- Record at 2x the CSS display size (for a 960 CSS px wide hero, a 1920 px wide master), crop to
  the panels that matter instead of the full window, and keep both dimensions even (libx264 needs
  even sizes; web.dev shows a `crop=trunc(iw/2)*2:trunc(ih/2)*2` filter for this).
- Use a larger editor font or zoom than usual. Web video uses 4:2:0 chroma (`yuv420p`), which
  halves colour resolution, so thin coloured text (syntax colours, diagnostics squiggles) smears
  first. 4:4:4 H.264/VP9 is not reliably decodable in browsers, so make the text big rather than
  change the pixel format.
- 30 fps is enough for UI; 24 fps is acceptable if typing still looks smooth. Make the last frame
  match the first so the loop does not jump.

**VP9 WebM** (options per [FFmpeg codecs: libvpx](https://ffmpeg.org/ffmpeg-codecs.html#libvpx)):
`-tune-content screen` sets the content type to screen **[doc]**; `-deadline good` with
`-cpu-used` is the documented speed/quality trade-off, and `best` "should be avoided" **[doc]**;
alternate reference frames are "2-pass only" **[doc]**, so use two passes.

```sh
ffmpeg -y -i master.mkv -an -c:v libvpx-vp9 -b:v 0 -crf 34 -pix_fmt yuv420p \
  -tune-content screen -deadline good -cpu-used 1 -row-mt 1 -g 240 \
  -pass 1 -f null /dev/null
ffmpeg -y -i master.mkv -an -c:v libvpx-vp9 -b:v 0 -crf 34 -pix_fmt yuv420p \
  -tune-content screen -deadline good -cpu-used 1 -row-mt 1 -g 240 \
  -pass 2 loop.webm
```

(`-b:v 0 -crf N` is constant-quality mode, as in web.dev's command, which used `-crf 41`.)

**H.264 MP4** (web.dev's baseline is `-crf 25 -vcodec libx264 -pix_fmt yuv420p`):

```sh
ffmpeg -y -i master.mkv -an -c:v libx264 -preset veryslow -crf 22 \
  -pix_fmt yuv420p -profile:v high -g 240 -movflags +faststart loop.mp4
```

`+faststart` moves the MP4 index to the front so playback can start before the whole file has
arrived. `yuv420p` is needed for broad decoder support (web.dev uses it for the same reason).

**Optional AV1** (if ever needed): SVT-AV1 has a screen content mode `--scm` (range 0 to 3,
default 2, "Set screen content detection level"), `--crf` 1 to 70 (default 35) and `--preset`
up to 13 ([SVT-AV1 Parameters.md](https://gitlab.com/AOMediaCodec/SVT-AV1/-/blob/master/Docs/Parameters.md));
libaom has `enable-intrabc` ("useful for screen content") and `enable-palette`
([FFmpeg codecs: libaom](https://ffmpeg.org/ffmpeg-codecs.html#libaom_002dav1)). Example:
`-c:v libsvtav1 -preset 4 -crf 35 -svtav1-params scm=1`.

**Size targets** **[inference, to verify]**: hero loop at most ~1.5 MB (WebM) / ~2.5 MB (MP4)
for 10 to 15 s at 1920 px wide; gallery loops at most ~1 MB WebM at 1280 px; posters and
screenshots 50 to 200 KB after Astro's AVIF/WebP conversion. If a file misses the target, first
crop tighter, shorten, or lower fps, and only then raise CRF; check text sharpness at 100 % and on
a 2x display before accepting.

## 2. Loading behaviour

**[doc]** facts that shape the markup:

- `autoplay` overrides `preload`; `preload` is only a hint; the spec advises `metadata` as the
  default ([MDN `<video>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/video)).
- `poster` is shown while the video downloads; without it nothing is shown until the first frame
  (same source).
- `playsinline` is "required for autoplay in Safari" ([MDN Autoplay](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Autoplay)).
- `play()` returns a promise; a `NotAllowedError` rejection means autoplay was refused, and the
  page should then offer a play button (same source).
- `loading="lazy"` on `<video>` is experimental: Chrome/Edge 150 only, not in Firefox or Safari
  ([MDN browser-compat-data `html.elements.video.loading`](https://github.com/mdn/browser-compat-data/blob/main/html/elements/video.json)).
  web.dev's fallback is `preload="none"` + `poster` + an IntersectionObserver that starts playback
  in view ([web.dev: lazy-loading video](https://web.dev/articles/lazy-loading-video)).
- For `<video>`, LCP uses "the poster image load time or first frame presentation time ...
  whichever is earlier" ([web.dev: LCP](https://web.dev/articles/lcp)). web.dev advises that an
  LCP video gets a poster preloaded with `fetchpriority="high"` and no `loading="lazy"`.

**Recommended pattern** **[inference]**:

```html
<figure>
  <video class="demo" muted loop playsinline preload="none" controls
         width="960" height="600" poster="/_astro/edit-gui.poster.avif"
         aria-describedby="demo-edit-desc" disablepictureinpicture disableremoteplayback>
    <source src="https://media.happydwarf.dev/etch/v0.4.0/edit-gui.webm"
            type='video/webm; codecs="vp09.00.40.08"'>
    <source src="https://media.happydwarf.dev/etch/v0.4.0/edit-gui.mp4"
            type='video/mp4; codecs="avc1.640028"'>
  </video>
  <figcaption id="demo-edit-desc">Editing a .gui file: the preview window updates as the
    size of the button changes, then a diagnostic marks a missing sprite.</figcaption>
</figure>
```

- No `autoplay` attribute: HTML cannot make autoplay conditional on `prefers-reduced-motion`, so
  a small script decides (below). Without JavaScript the user gets the poster and native
  `controls`, which is a working fallback.
- The script: if `matchMedia('(prefers-reduced-motion: no-preference)')` matches, remove
  `controls`, show the site's own pause/play button, and call `play()` when the loop enters the
  viewport (IntersectionObserver) and `pause()` when it leaves. Catch `NotAllowedError` and show
  the play button. Listen to the media query's `change` event.
- Hero: `preload="none"` is fine because the script calls `play()` as soon as it is visible; add
  `<link rel="preload" as="image" href="(poster)" fetchpriority="high">` for the hero poster only.
  Gallery loops: `preload="none"`, start on visibility.
- Always set `width`/`height` (or CSS `aspect-ratio`) so the box does not shift when the poster
  arrives.
- The exact `codecs` strings depend on the encoded profile/level; the build script should read
  them from the files (for example with `ffprobe` or MP4Box) rather than hard-code them
  **[to verify]**.
- The posters are the first (or a representative) frame, exported by the same media script.

## 3. Accessibility

- **Pause control is mandatory [doc].** WCAG 2.2 SC 2.2.2 Pause, Stop, Hide (Level A): moving
  content that starts automatically, lasts more than five seconds and sits beside other content
  needs a mechanism to pause, stop or hide it; G4 ("allowing the content to be paused and
  restarted from where it was paused") is a sufficient technique
  ([Understanding 2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)). A
  looping demo always exceeds five seconds, so every autoplaying loop needs a visible, keyboard-
  reachable pause/play button; honouring reduced motion does not replace it **[inference]**.
- **Reduced motion [doc].** `prefers-reduced-motion: reduce` reports the OS setting to minimise
  non-essential motion (Windows 11: Accessibility > Visual effects > Animation effects; macOS and
  iOS: Reduce motion; Android: Remove animations)
  ([MDN prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion)).
  With `reduce`, show the poster and a play button and never start the loop by itself
  **[inference]**; this matches the map's "prefers-reduced-motion respected" rule.
- **Text alternative instead of captions [doc].** A silent screen recording is "video-only"
  content. WCAG SC 1.2.1 (Level A) requires "an alternative for time-based media or an audio track"
  unless the video is a media alternative for text and clearly labelled as such
  ([Understanding 1.2.1](https://www.w3.org/WAI/WCAG22/Understanding/audio-only-and-video-only-prerecorded.html);
  techniques G159, G166). Captions are not needed (there is no audio). Practical form
  **[inference]**: a `<figcaption>` (linked with `aria-describedby`) that says step by step what
  the loop shows, or, when the surrounding text already describes the feature, mark the video as
  illustrating that text.
- **No flashing**: cuts between scenes must not flash more than three times a second (SC 2.3.1,
  referenced from the 2.2.2 page) **[doc]**.
- `<video>` has no `alt` attribute; the description above plays that role **[doc]** (MDN lists no
  implicit ARIA role and no alt guidance for `<video>`).

## 4. Hosting: site repository vs Cloudflare R2

### GitHub Pages (files in the site repository)

- **[doc]** Published site at most 1 GB; source repository recommended at most 1 GB; deployments
  time out after 10 minutes; soft bandwidth limit 100 GB per month; rate limiting returns HTTP 429
  ([GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)).
- **[doc]** Git warns on files over 50 MiB and GitHub blocks files over 100 MiB; repositories
  should ideally stay under 1 GB and "less than 5 GB is strongly recommended"
  ([About large files on GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)).
  These docs do not say whether Pages serves Git LFS files.
- **[observed]** `anvil.happydwarf.dev` (same stack) answers with `Cache-Control: max-age=600`
  even for content-hashed `/_astro/` files, `Accept-Ranges: bytes`, and a `206 Partial Content`
  for `Range: bytes=0-99`. Pages behind Fastly therefore supports the byte ranges that Safari
  needs ("HTTP servers hosting media files for iOS must support byte-range requests",
  [Apple Safari Web Content Guide](https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariWebContent/CreatingVideoforSafarioniPhone/CreatingVideoforSafarioniPhone.html)),
  but the 10-minute cache lifetime cannot be changed. Revalidation uses `ETag`, so it is cheap.
- **[inference]** The real cost of the repository route is history, not bandwidth: the map wants
  media refreshed per release by script, and every refresh of 5 to 15 MB of video stays in Git
  history forever. That is fine for a few releases and a slow drift towards the 1 GB
  recommendation over years; it also makes every clone of the site repo heavier.

### Cloudflare R2 on `media.happydwarf.dev`

- **Cost [doc]** ([R2 pricing](https://developers.cloudflare.com/r2/pricing/)): Standard storage
  $0.015 per GB-month, Class A (writes, lists) $4.50 per million, Class B (`GetObject`,
  `HeadObject`) $0.36 per million; free each month: 10 GB-month, 1 million Class A, 10 million
  Class B; egress is free. **[doc]** "Every cache hit avoids origin fetch costs, ... and R2
  operations" ([How charges accrue](https://developers.cloudflare.com/billing/understand/how-charges-accrue/)).
  **[inference]** At Etch's scale (tens of MB stored, a handful of uploads per release, reads
  mostly served from cache) the bill is $0; even with no cache at all it would take 10 million
  reads a month to leave the free tier.
- **Custom domain [doc]** ([R2 public buckets](https://developers.cloudflare.com/r2/buckets/public-buckets/)):
  the domain "must have been added as a zone in the same account as the R2 bucket" (true for
  `happydwarf.dev`); connecting it adds the DNS record for you. The `r2.dev` URL "is intended for
  non-production traffic", is rate-limited and has no caching, WAF or bot management, so disable
  it once the custom domain works.
- **The record is proxied, not DNS-only [doc].** R2 custom domains appear as "read-only proxied
  records" in the DNS table ([Enforce DNS-only](https://developers.cloudflare.com/dns/proxy-status/enforce-dns-only/)).
  The organisation's "DNS only" rule is for GitHub Pages records; it must not be applied to
  `media` **[inference]**.
- **Caching [doc]**: custom-domain requests go through Cloudflare's cache
  ([Enable cache in an R2 bucket](https://developers.cloudflare.com/cache/interaction-cloudflare-products/r2/));
  MP4, WEBM, AVIF, WEBP, PNG and JPG are in the default cached extensions, so no "Cache Everything"
  rule is needed; the Free plan caches files up to 512 MB; Cloudflare honours the origin's
  `Cache-Control` and otherwise keeps 200/206 responses for 120 minutes
  ([Default cache behavior](https://developers.cloudflare.com/cache/concepts/default-cache-behavior/)).
  Smart Tiered Cache is recommended for R2 because it "reduces the number of requests that reach
  R2" (R2 cache page). Object metadata such as `Cache-Control` and `Content-Type` is set at upload,
  for example `wrangler r2 object put --cache-control ... --content-type ...`
  ([Wrangler R2 commands](https://developers.cloudflare.com/workers/wrangler/commands/r2/)).
- **Range requests [doc]**: Cloudflare "can serve HTTP range requests from complete or partial
  cached files", aligns origin range fetches to 1 MiB, and omits `Range` on a cold miss
  ([Range request behavior](https://developers.cloudflare.com/cache/reference/range-requests/)).
  So Safari's byte-range playback works from cache **[inference; to verify with
  `curl --range 0-99` once the bucket exists, as Apple's guide suggests]**.
- **CORS [doc]**: R2 CORS applies to browser interaction with a bucket; requests without an
  `Origin` header get no CORS headers; the docs name scripts that read headers, "such as when using
  a video player", as the case that needs a policy ([R2 CORS](https://developers.cloudflare.com/r2/buckets/cors/)).
  **[inference]** A plain `<video><source src>` or `<img>` without `crossorigin` does not need
  CORS. Add a `GET` policy for `https://etch.happydwarf.dev` (and `http://localhost:4321` for
  development) anyway, so a later `<track>` file, `crossorigin` attribute or `fetch` does not
  break; after changing CORS, purge the cache for the hostname (same page).
- **Terms [doc]**: Cloudflare's service-specific terms say non-Enterprise customers must use
  specific paid services "(e.g., the Developer Platform, Images, and Stream)" to serve video and
  large files via the CDN ([Service-specific terms](https://www.cloudflare.com/service-specific-terms-application-services/)).
  **[inference]** R2 is a Developer Platform product, so short loops from an R2 bucket fit this
  rule; the terms do not name R2 explicitly. (GitHub Pages records are DNS-only, so files served by
  Pages do not pass through Cloudflare's CDN at all.)

### Comparison

| | Site repo on GitHub Pages | R2 on `media.happydwarf.dev` |
|---|---|---|
| Cost at Etch scale | $0 | $0 (free tier) |
| Limits that matter | 1 GB site, 100 GB/month soft, 100 MiB per file | 512 MB cacheable file on Free; none relevant |
| Cache lifetime | fixed `max-age=600` [observed] | set per object, e.g. one year `immutable` |
| Byte ranges (Safari) | yes [observed] | yes, from cache [doc] |
| Git history growth per media refresh | yes, permanent | none |
| Same origin (LCP, no extra connection) | yes | no: one extra DNS + TLS handshake |
| Moving parts | none | bucket, custom domain, upload credentials, CORS |
| Build-time processing | Astro optimises images in `src/` | none: Astro "has no native video support" and only optimises authorised remote images ([Astro images](https://docs.astro.build/en/guides/images/)) |

## 5. Decision: confirm R2 for video, keep stills in the repository

**R2 is confirmed as the direction for the demo loops**, because:

1. The loops are regenerated every release by a script. In R2 they become immutable, versioned
   objects that never enter Git history; in the repo each refresh is a permanent multi-megabyte
   commit.
2. It costs nothing at this scale, egress is free, and cache hits do not count as R2 operations.
3. It allows long-lived `immutable` caching, which Pages cannot (fixed 10-minute `max-age`).
4. It keeps the site's GitHub Pages bandwidth and size budgets for the site itself, and it is the
   Cloudflare-sanctioned way to serve video on a non-Enterprise plan.
5. The sibling sites (organisation site, Anvil) can reuse the same bucket and hostname under
   their own prefixes.

What R2 does **not** win: it adds a cross-origin connection and a credentialed upload step. Both
are small, and the repository route would also work for the first release; R2 is chosen for the
per-release refresh, not because Pages cannot serve video.

**Conditions of the decision**

- Video only on R2. **Posters and screenshots stay in the site repository** (`src/`), where Astro
  converts them to AVIF/WebP with hashed names; the hero poster is the LCP candidate and should be
  same-origin. They are small enough that per-release refreshes do not matter. (Alternative if
  that ever changes: put stills on R2 too and authorise `media.happydwarf.dev` in Astro's
  `image.remotePatterns`, at the cost of a build-time network dependency.)
- Keys are versioned and never overwritten: `etch/<version>/<scene>.webm|.mp4`, uploaded with
  `Content-Type` set and `Cache-Control: public, max-age=31536000, immutable`. The site points at
  the version it was built for; old versions stay until deliberately removed.
- One bucket for the organisation's public media, custom domain `media.happydwarf.dev` (proxied,
  managed by R2), `r2.dev` access disabled, Smart Tiered Cache on if the plan has it, CORS `GET`
  for the site origins.
- Credentials follow the user's rule: tokens only from environment variables or CI secrets, never
  in files or chat.
- Before launch, verify with real files: `curl --range 0-99` gets `206`, a second request shows a
  cache hit, Safari iOS plays the MP4 (or WebM on 17.4+) inline, and the encoded sizes meet the
  targets in section 1.

## Open questions surfaced

1. **Who uploads and from where?** The media script in the `etch` repo (local run with an env
   token) or a CI job (release workflow with an R2 token secret scoped to one bucket)? Ties in with
   the map's "keeping Etch's site current with releases".
2. **Bucket naming and layout** for the whole organisation (`etch/`, `anvil/`, `org/` prefixes in
   one bucket vs a bucket per site), and a retention rule for old versions.
3. **DNS for `media`** belongs in the "DNS and Pages details for the apex" item: it is the one
   proxied record in an otherwise DNS-only zone setup, and should be documented as an intentional
   exception.
4. **Recording pipeline feasibility**: can the master be captured headlessly (VS Code in a virtual
   display, fixed window size and zoom) so the script really is repeatable? This decides the
   capture settings above.
5. **Size targets and CRF values** need a measurement on the first real recording (WebM vs MP4
   sizes, text sharpness at 1x and 2x).
