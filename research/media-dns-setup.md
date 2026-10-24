# Setting up and verifying `media.happydwarf.dev` and the apex on GitHub Pages

Research for [happy-dwarf-team/.github#25](https://github.com/happy-dwarf-team/.github/issues/25)
(map: [#4](https://github.com/happy-dwarf-team/.github/issues/4); builds on
[#8](https://github.com/happy-dwarf-team/.github/issues/8) and
[#17](https://github.com/happy-dwarf-team/.github/issues/17)). Researched 2026-10-24.
Nothing was created or changed on Cloudflare or GitHub for this research. The zone was read only
through public DNS (1.1.1.1), and GitHub only through read-only `gh api` calls.

**Question.** How is `media.happydwarf.dev` (R2 bucket `happydwarf-media`) set up on the Happy
Dwarf Cloudflare account, how is it verified before the Etch site launches, and how do the apex
`happydwarf.dev` and `www` go onto GitHub Pages without colliding with what the zone already has?

**Answer in one line.** Enable R2 in the dashboard (the only dashboard-only step), then do
everything else with Wrangler or the Cloudflare API (MCP): create `happydwarf-media`, connect
`media.happydwarf.dev` with `--min-tls 1.2`, confirm `r2.dev` stays disabled (it is off by
default), set a `GET`/`HEAD` CORS policy for the three origins, turn on Smart Tiered Cache
(available on every plan, Free included), and add no cache or WAF rule; put the apex on GitHub
Pages with the four A and four AAAA records (DNS only) plus `www` as a DNS-only CNAME to
`happy-dwarf-team.github.io`, and let GitHub Pages redirect `www` to the apex. The org domain is
already verified and nothing in the zone collides.

Labels: **[doc]** stated by a primary source, **[observed]** checked live on 2026-10-24,
**[inference]** reasoning from those, **[to verify]** to check during the build.

## 1. What the zone has today

Public DNS answers from 1.1.1.1 on 2026-10-24 **[observed]**:

| Name | Records | Note |
|---|---|---|
| `happydwarf.dev` | NS `nena`/`norman.ns.cloudflare.com`; MX `route1..3.mx.cloudflare.net`; TXT `v=spf1 include:_spf.mx.cloudflare.net ~all` | Cloudflare Email Routing. **No A, AAAA, CNAME, CAA or HTTPS record.** |
| `_dmarc` | TXT `v=DMARC1; p=reject; ...` | email |
| `cf2024-1._domainkey` | TXT DKIM key | Email Routing |
| `anvil` | CNAME `happy-dwarf-team.github.io` | DNS only: resolves to GitHub's 185.199.108-111.153, not Cloudflare IPs |
| `_github-pages-challenge-happy-dwarf-team` | TXT (challenge value) | GitHub Pages org domain verification |
| `www`, `etch`, `media` | none (NXDOMAIN) | free to create |
| a random name | NXDOMAIN | no wildcard record |

- **[observed]** `gh api repos/happy-dwarf-team/anvil-website/pages` reports
  `"protected_domain_state": "verified"`, certificate `approved` (expires 2027-01-13),
  `https_enforced: true`, `build_type: workflow`. So **the organization's domain verification for
  `happydwarf.dev` is already done** and working.
- **[inference]** Nothing collides: the apex has only MX/TXT, which coexist with A/AAAA records;
  `www`, `etch` and `media` do not exist. Public DNS cannot list a zone, so a record at a name not
  queried above could exist; the build step should glance at the dashboard's DNS table once.
- **[observed]** in #17: R2 is not enabled on the account yet, so no bucket exists.

## 2. R2 and `media.happydwarf.dev`: setup checklist

Columns: **Dashboard** = Cloudflare dashboard; **Wrangler** = `wrangler` CLI (authenticated with
`wrangler login` or `CLOUDFLARE_API_TOKEN` from the environment, never a file); **API / MCP** = the
Cloudflare REST API, which the Cloudflare API MCP's `execute` tool can call. Whether the MCP's
OAuth grant carries R2 and zone-settings scopes is **[to verify]** on first use.

| # | Step | Dashboard | Wrangler | API / MCP |
|---|---|---|---|---|
| 1 | Enable R2 on the account | **only here** | no | no |
| 2 | Create bucket `happydwarf-media` | yes | yes | yes |
| 3 | Connect custom domain `media.happydwarf.dev` | yes | yes | yes |
| 4 | Minimum TLS 1.2 on that domain | not documented | yes (`--min-tls`) | yes (`minTLS`) |
| 5 | `r2.dev` access: confirm disabled | yes | yes | yes |
| 6 | CORS policy | yes | yes | yes |
| 7 | Smart Tiered Cache on the zone | yes | no | yes |
| 8 | Cache or WAF rule | none needed | | |

### Step 1. Enable R2 (dashboard only)

- **[doc]** "a Cloudflare account with an R2 subscription" is a prerequisite; without one, go to
  **Storage & databases > R2 > Overview** and complete the checkout flow
  ([R2 get started](https://developers.cloudflare.com/r2/get-started/)). R2 "is free to get started
  with included free monthly usage."
- **[observed]** in #17: the API refuses R2 calls with "Please enable R2 through the Cloudflare
  Dashboard". So this step cannot go through Wrangler or the MCP.
- **[to verify]** whether the checkout asks for a payment method on a $0 plan (the docs do not say).

### Step 2. Create the bucket

Settings fixed by #17: name `happydwarf-media`, Standard storage, default jurisdiction, automatic
location hint (no hint).

- Wrangler **[doc]** ([Wrangler R2 commands](https://developers.cloudflare.com/workers/wrangler/commands/r2/)):
  ```sh
  npx wrangler r2 bucket create happydwarf-media --storage-class Standard
  npx wrangler r2 bucket info happydwarf-media
  npx wrangler r2 bucket lifecycle list happydwarf-media
  ```
  No `--location` (automatic) and no `--jurisdiction` (default).
- API **[doc]** ([create bucket](https://developers.cloudflare.com/api/resources/r2/subresources/buckets/methods/create/)):
  `POST /accounts/{account_id}/r2/buckets` with `{"name": "happydwarf-media", "storageClass": "Standard"}`;
  `locationHint` and the `cf-r2-jurisdiction` header are optional and left out.
- Check that the only lifecycle rule is the default abort of incomplete multipart uploads (#17).

### Step 3. Connect `media.happydwarf.dev`, with step 4 (minimum TLS)

- **[doc]** The domain "must have been added as a zone in the same account as the R2 bucket" (true
  for `happydwarf.dev`). Dashboard: bucket > Settings > Custom Domains > Add > enter the domain >
  Continue > review the DNS record > Connect Domain; status goes from Initializing to Active within
  a few minutes ([R2 public buckets](https://developers.cloudflare.com/r2/buckets/public-buckets/)).
- **[doc]** The record R2 adds is a **read-only proxied record** in the DNS table
  ([Enforce DNS-only](https://developers.cloudflare.com/dns/proxy-status/enforce-dns-only/));
  removing the domain removes the CNAME (public buckets page). So `media` is proxied by
  construction and cannot be switched to DNS only: it is the documented exception (section 4).
- **Minimum TLS [doc]:** the custom-domain API's `minTLS` takes `"1.0"`, `"1.1"`, `"1.2"` or
  `"1.3"` and, if not set, "defaults to 1.0"
  ([create custom domain](https://developers.cloudflare.com/api/resources/r2/subresources/buckets/subresources/domains/subresources/custom/methods/create/)).
  The zone's Minimum TLS setting "does not apply to R2 custom domains"
  ([Minimum TLS](https://developers.cloudflare.com/ssl/edge-certificates/additional-options/minimum-tls/)).
  The R2 docs describe changing it only by API ("issue an API call to edit R2 custom domain
  settings ... add the optional `minTLS` and `ciphers` parameters"); Wrangler has `--min-tls` on
  `domain add` and `domain update`. No dashboard control is documented.
- **Choice: TLS 1.2 [inference].** 1.0/1.1 are obsolete and every browser that can play VP9 or
  H.264 `<video>` speaks TLS 1.2; 1.3-only would gain nothing for public, cookie-less media and
  could shut out old clients. Leave `ciphers` at the default.
- Wrangler (zone ID from the dashboard's zone overview or `GET /zones?name=happydwarf.dev`):
  ```sh
  npx wrangler r2 bucket domain add happydwarf-media \
    --domain media.happydwarf.dev --zone-id <ZONE_ID> --min-tls 1.2
  npx wrangler r2 bucket domain get happydwarf-media --domain media.happydwarf.dev
  ```
- API: `POST /accounts/{account_id}/r2/buckets/happydwarf-media/domains/custom` with
  `{"domain": "media.happydwarf.dev", "zoneId": "<ZONE_ID>", "enabled": true, "minTLS": "1.2"}`.
- If connected from the dashboard instead, set TLS afterwards with
  `wrangler r2 bucket domain update happydwarf-media --domain media.happydwarf.dev --min-tls 1.2`.

### Step 5. `r2.dev` stays disabled

- **[doc]** "By default, buckets are never publicly accessible and will always require explicit
  user permission to enable", and custom domains and `r2.dev` "can be used independently. Enabling
  custom domains does not require enabling `r2.dev` access" (public buckets page). So on a new
  bucket this step is a **check**, not a change.
- **[doc]** Why it matters: `r2.dev` is rate-limited, "intended for non-production traffic", has
  no cache, WAF or bot management, and if it is on, the bucket stays public through it whatever
  the custom domain does (same page).
- Check: `npx wrangler r2 bucket dev-url get happydwarf-media` (expect disabled). If it ever shows
  enabled: `npx wrangler r2 bucket dev-url disable happydwarf-media`, or API
  `PUT /accounts/{account_id}/r2/buckets/happydwarf-media/domains/managed` with
  `{"enabled": false}` ([managed domain](https://developers.cloudflare.com/api/resources/r2/subresources/buckets/subresources/domains/subresources/managed/methods/update/)),
  or dashboard: Settings > Public Development URL > Disable.

### Step 6. CORS policy

The policy (dashboard JSON tab, field names per [R2 CORS](https://developers.cloudflare.com/r2/buckets/cors/)):

```json
[
  {
    "AllowedOrigins": [
      "https://etch.happydwarf.dev",
      "https://happydwarf.dev",
      "http://localhost:4321"
    ],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedHeaders": ["Range"],
    "ExposeHeaders": ["Content-Range", "Accept-Ranges", "ETag"],
    "MaxAgeSeconds": 86400
  }
]
```

The same policy for Wrangler (`--file cors.json`) and the API
(`PUT /accounts/{account_id}/r2/buckets/happydwarf-media/cors`, which **replaces** all rules), in
the API's schema
([update CORS](https://developers.cloudflare.com/api/resources/r2/subresources/buckets/subresources/cors/methods/update/)):

```json
{
  "rules": [
    {
      "id": "site-origins-read",
      "allowed": {
        "origins": ["https://etch.happydwarf.dev", "https://happydwarf.dev", "http://localhost:4321"],
        "methods": ["GET", "HEAD"],
        "headers": ["Range"]
      },
      "exposeHeaders": ["Content-Range", "Accept-Ranges", "ETag"],
      "maxAgeSeconds": 86400
    }
  ]
}
```

```sh
npx wrangler r2 bucket cors set happydwarf-media --file cors.json
npx wrangler r2 bucket cors list happydwarf-media
```

Why each field:

- **Origins.** The two production origins and Astro's dev server. Origins carry no path and no
  trailing slash; ports cannot be wildcarded **[doc]** (R2 CORS). `https://www.happydwarf.dev`
  is left out on purpose: `www` only redirects to the apex (section 3), so no page is ever served
  from it **[inference]**.
- **Methods `GET`, `HEAD`.** Read only; the allowed set is `GET`, `PUT`, `POST`, `DELETE`,
  `HEAD` **[doc]** (update CORS). Uploads go through the S3 API or Wrangler, not a browser, so no
  `PUT` **[inference]**.
- **Allowed header `Range`.** **[doc]** Fetch makes `Range` CORS-safelisted only for a single range
  with a start (`bytes=N-` or `bytes=N-M`); suffix ranges (`bytes=-N`) are not
  ([Fetch standard](https://fetch.spec.whatwg.org/)). Listing it avoids a failed preflight if a
  script ever fetches a suffix range **[inference]**.
- **Exposed headers.** `Content-Length` is already a CORS-safelisted response header,
  `Content-Range` is not **[doc]** (Fetch), so a script that reads ranges needs it exposed;
  `Accept-Ranges` and `ETag` are useful to a player or a check script **[inference]**.
- **Max age 86400.** The documented maximum; "Browsers may limit this to 2 hours or less"
  **[doc]**. The origins rarely change, so the longest cache is fine **[inference]**.
- **Reminder from #8:** a plain `<video><source>` without `crossorigin` needs no CORS at all; the
  policy is there so a later `crossorigin`, `<track>` or `fetch` does not break.
- **[doc]** "Requests without an `Origin` header do not return CORS response headers." Rule
  changes can take up to 30 seconds; after any CORS change, **purge the cache for
  `media.happydwarf.dev`**, because cached objects keep the old headers (R2 CORS). Purge by
  hostname is available on every plan, Free included (5 requests per minute)
  ([Purge cache](https://developers.cloudflare.com/cache/how-to/purge-cache/)); dashboard or API.

### Step 7. Smart Tiered Cache

- **[doc]** Smart Tiered Cache is available on **Free, Pro, Business and Enterprise**; only
  Generic Global, Regional and Custom topologies are Enterprise-only
  ([Tiered Cache](https://developers.cloudflare.com/cache/how-to/tiered-cache/)). So the zone's
  plan does not matter; the account's plan was not read (no account access in this research).
- **[doc]** For R2 it "automatically selects the upper-tier data center with the lowest latency
  to your R2 bucket", so edge misses check one upper tier before R2
  ([R2 and cache](https://developers.cloudflare.com/cache/interaction-cloudflare-products/r2/)).
- Dashboard: Caching > Tiered Cache, enable, choose Smart topology (the docs note this is now also
  offered under Smart Shield, so the menu may have moved). API:
  `PATCH /zones/{zone_id}/cache/tiered_cache_smart_topology_enable` with `{"value": "on"}`
  (token needs Zone Settings Write). No Wrangler command.
- **[inference]** It is a zone setting, but it only affects proxied traffic; the GitHub Pages
  records are DNS only, so today it touches `media` alone.

### Step 8. Cache and WAF rules: none

- **[doc]** WEBM and MP4 (and AVIF, WEBP, PNG, JPG) are in the default cached extensions; HTML and
  JSON are not. Cloudflare honours the origin's `Cache-Control` (`public` with `max-age > 0` is
  cached) and Origin Cache Control is on by default on Free, Pro and Business; files up to 512 MB
  are cacheable on those plans
  ([Default cache behavior](https://developers.cloudflare.com/cache/concepts/default-cache-behavior/)).
- **[inference]** The bucket holds only `.webm` and `.mp4` (the media manifest and posters live in
  the site repositories, #17 and #8), so **no Cache Everything or cache rule is needed**. If a
  JSON or HTML file is ever put in the bucket, that is when a cache rule becomes necessary.
- **[inference]** No WAF rule: the content is public, cookie-less and immutable; abuse costs at
  most cache-served egress, which is free. Revisit only if R2 Class B operations ever approach the
  10 million free reads per month (#8).
- **[doc]** Range requests are served "from complete or partial cached files", and a cold miss
  fetches from R2 without `Range`
  ([Range requests](https://developers.cloudflare.com/cache/reference/range-requests/)).

## 3. Apex `happydwarf.dev` and `www` on GitHub Pages

### Records (all DNS only, grey cloud)

| Name | Type | Value |
|---|---|---|
| `@` | A | `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` |
| `@` | AAAA | `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153` |
| `www` | CNAME | `happy-dwarf-team.github.io` |
| `etch` | CNAME | `happy-dwarf-team.github.io` (Etch site, same pattern as `anvil`) |

- **[doc]** These are the A and AAAA addresses GitHub lists for an apex, with ALIAS/ANAME to
  `ORGANIZATION.github.io` as the alternative; GitHub recommends keeping A records alongside AAAA
  ([Managing a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)).
  `www` is a CNAME to `<organization>.github.io` without the repository name (same page).
- **A/AAAA rather than a flattened CNAME [inference].** Cloudflare flattens an apex CNAME by
  default on all plans, Free included **[doc]**
  ([Set up CNAME flattening](https://developers.cloudflare.com/dns/cname-flattening/set-up-cname-flattening/)),
  so a CNAME `@ → happy-dwarf-team.github.io` would also work. A/AAAA is preferred because it is
  exactly GitHub's list, `dig`/`Resolve-DnsName` checks compare against it directly, and the
  Cloudflare docs do not address an apex CNAME beside the existing MX/TXT records. The cost: if
  GitHub ever changes its IPs, the eight records must be edited by hand.
- **DNS only is required, not just preferred.** The team's rule says GitHub Pages records must be
  DNS only or the certificate is not issued. **[doc]** GitHub: certificate failures "can be caused
  by extra DNS records, or records not pointing to the IP addresses for GitHub Pages"
  ([Securing with HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https));
  a proxied record would point at Cloudflare's IPs **[inference]**.
- **CAA [doc]:** "If you're using ... CAA records, at least one CAA record must exist with the
  value `letsencrypt.org`"
  ([Troubleshooting custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/troubleshooting-custom-domains-and-github-pages)).
  The zone has no CAA today **[observed]**, so nothing to do; whoever adds one later must include
  `letsencrypt.org`.
- **No wildcard record** ever: GitHub "strongly recommend[s]" against `*.example.com` (managing a
  custom domain page). There is none today **[observed]**.

### How `www` reaches the apex: GitHub Pages, not a Cloudflare rule

- **[doc]** With both records in place, GitHub Pages "will automatically create redirects between
  the domains", towards whichever one is configured in the repository's Pages settings: with
  `example.com` configured, `www.example.com` redirects to it (managing a custom domain page; same
  in [About custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages)).
- **[doc]** A Cloudflare redirect needs "a proxied DNS A or CNAME record" so Cloudflare can "apply
  rules, redirects, and Workers to incoming traffic"
  ([Redirect a domain](https://developers.cloudflare.com/fundamentals/manage-domains/redirect-domain/)).
  **[inference]** With DNS-only records, Cloudflare never sees the request, so a Cloudflare
  redirect rule cannot work without breaking the DNS-only rule. **Use GitHub's built-in redirect;
  configure the apex, not `www`, as the custom domain.**
- **[doc]** GitHub recommends a `www` record even when the apex is the custom domain (about
  custom domains page), which is what makes the redirect and its certificate possible.

### Order (GitHub side and DNS)

1. **Org domain verification: already done [observed]** (section 1). **[doc]** It means "only
   repositories owned by that organization may be used to publish a GitHub Pages site to the
   verified custom domain or the domain's immediate subdomains"; deeper names (`a.b.happydwarf.dev`)
   are not covered; "keep the TXT record" or verification lapses
   ([Verifying your custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages)).
   So **never delete `_github-pages-challenge-happy-dwarf-team`.** Verification lives in the org's
   Settings > Pages; the Pages REST docs list no endpoint for it (dashboard only, already done).
2. Create `happydwarf-website`, deploy once with the Pages workflow (`build_type: workflow`, as
   `anvil-website`).
3. **Set the custom domain `happydwarf.dev` in the repository before adding DNS [doc]:** "Make
   sure you add your custom domain to your GitHub Pages site before configuring your DNS
   provider" (managing a custom domain page). With a custom Actions workflow no `CNAME` file is
   created and "any existing CNAME file is ignored" (same page). Repo Settings > Pages > Custom
   domain, or `PUT /repos/happy-dwarf-team/happydwarf-website/pages` with `{"cname": "happydwarf.dev"}`
   ([Pages REST API](https://docs.github.com/en/rest/pages/pages)).
4. Add the A, AAAA and `www` records above in Cloudflare, **DNS only** (dashboard, or API
   `POST /zones/{zone_id}/dns_records` with `"proxied": false`). Leave the MX, SPF, DMARC and DKIM
   records alone.
5. Wait for the certificate, then **Enforce HTTPS** (Settings, or the same `PUT` with
   `{"https_enforced": true}`). GitHub says provisioning may take several minutes and Enforce HTTPS
   "can take up to 24 hours" to become available **[doc]**.
6. The hub launches after the Etch site (#12), so steps 2 to 5 for the apex happen at hub launch;
   the `etch` CNAME follows the same order for `etch-website`.

**[well known, not re-checked]** `.dev` is on the browsers' HSTS preload list as a whole TLD
([get.dev](https://get.dev/)), so browsers never try plain HTTP on `happydwarf.dev`, `www` or
`etch`: until GitHub's certificate is issued, the site (and the `www` redirect) simply does not
load in a browser. Plan the DNS change for a moment when a short gap does not matter.

## 4. Where the `media` exception is written down

The hub spec (organization site, `happydwarf-website`) gets a **DNS** section with the whole
zone's web records, so the one proxied record sits beside the DNS-only ones it is an exception to.
Proposed text:

> | Name | Type | Target | Proxy | Owner |
> |---|---|---|---|---|
> | `@` | A ×4, AAAA ×4 | GitHub Pages IPs | DNS only | `happydwarf-website` |
> | `www` | CNAME | `happy-dwarf-team.github.io` | DNS only | redirects to the apex (GitHub Pages) |
> | `anvil` | CNAME | `happy-dwarf-team.github.io` | DNS only | `anvil-website` |
> | `etch` | CNAME | `happy-dwarf-team.github.io` | DNS only | `etch-website` |
> | `media` | CNAME (read-only) | R2 custom domain of `happydwarf-media` | **Proxied** | R2 |
> | `_github-pages-challenge-happy-dwarf-team` | TXT | org verification | n/a | never delete |
>
> GitHub Pages records are DNS only, or GitHub cannot issue their certificates. `media` is the one
> intentional exception: R2 creates it as a read-only proxied record and serves the bucket through
> Cloudflare's cache; it cannot be made DNS only. Email Routing records (MX, SPF, DMARC, DKIM) are
> not part of the sites.

The Etch spec links to that section instead of repeating it. The team's existing rule ("Records for
GitHub Pages ... must be DNS only") is already scoped to Pages records, so it needs no change
**[inference]**.

## 5. Verification

Run after the first real upload (e.g. `etch/v<version>/hero.<hash8>.mp4` and `.webm`, uploaded
with `Content-Type` and `Cache-Control: public, max-age=31536000, immutable`, #17). Shell is
Git Bash; `U` is the object URL.

**Setup state**

```sh
npx wrangler r2 bucket domain get happydwarf-media --domain media.happydwarf.dev   # enabled, minTLS 1.2
npx wrangler r2 bucket dev-url get happydwarf-media                                # disabled
npx wrangler r2 bucket cors list happydwarf-media                                  # the policy above
```

Smart Tiered Cache: `GET /zones/{zone_id}/cache/tiered_cache_smart_topology_enable` returns
`"value": "on"` (or the dashboard toggle).

**DNS:** `Resolve-DnsName media.happydwarf.dev -Server 1.1.1.1` returns Cloudflare addresses (it
is proxied), whereas the apex and `www` return GitHub's (section 6).

**1. Byte range, expect `206`** (Apple: media servers for iOS must support byte ranges, #8):

```sh
curl -s -o /dev/null -D - --range 0-99 "$U"
# expect: HTTP/2 206, content-range: bytes 0-99/<size>, content-length: 100
```

On a cold miss Cloudflare fetches from R2 without `Range` **[doc]**; whether that first answer
is already `206` is **[to verify]**. Repeat if it is a `200`.

**2. Cache hit on the second request**

```sh
curl -s -o /dev/null -D - "$U" | grep -i cf-cache-status   # MISS (or EXPIRED) the first time
curl -s -o /dev/null -D - "$U" | grep -i cf-cache-status   # HIT
```

Requests from different places may land on different edges; run both from the same machine.

**3. Metadata as uploaded**

```sh
curl -s -o /dev/null -D - "$U" | grep -iE '^(content-type|cache-control):'
# content-type: video/mp4 (video/webm for .webm)
# cache-control: public, max-age=31536000, immutable
```

**4. CORS only with an `Origin` header**

```sh
curl -s -o /dev/null -D - "$U" | grep -i access-control                                      # nothing
curl -s -o /dev/null -D - -H 'Origin: https://etch.happydwarf.dev' "$U" | grep -i access-control
# access-control-allow-origin: https://etch.happydwarf.dev (+ access-control-expose-headers)
curl -s -o /dev/null -D - -H 'Origin: https://example.org' "$U" | grep -i access-control     # nothing
curl -s -o /dev/null -D - -X OPTIONS -H 'Origin: https://happydwarf.dev' \
  -H 'Access-Control-Request-Method: GET' -H 'Access-Control-Request-Headers: range' "$U"
# 2xx with access-control-allow-methods / -headers / -max-age
```

Run the `Origin` checks **after** step 2, on a cache `HIT` that was first filled by a request
without `Origin`: the docs say cached objects keep old CORS headers until purged, so whether a hit
filled without `Origin` still returns `access-control-allow-origin` is **[to verify]**. If it does
not, the fix is a cache-key or rule question for the build, not a reason to drop the policy.

**5. TLS floor**

```sh
curl -sS -o /dev/null --tls-max 1.1 "$U"   # expect a handshake failure
curl -sS -o /dev/null --tlsv1.2 "$U"       # expect success
```

(On Windows, Git's curl may use Schannel, which may refuse TLS 1.1 on its own; confirm the
failure comes from the server, e.g. with `openssl s_client -connect media.happydwarf.dev:443 -tls1_1`.)

**6. Safari on iOS plays inline (manual)**

On an iPhone, open the deployed Etch page (or a one-file test page on any HTTPS origin listed in
CORS) with the `<video muted loop playsinline>` markup from #8: the loop starts in place (no
fullscreen), loops, the pause button works, and Web Inspector shows `206` responses from
`media.happydwarf.dev`. Check the MP4 on iOS below 17.4 if a device is at hand, the WebM on 17.4+.

## 6. Verification of the apex and `www`

```powershell
Resolve-DnsName happydwarf.dev -Type A -Server 1.1.1.1        # the four 185.199.10x.153
Resolve-DnsName happydwarf.dev -Type AAAA -Server 1.1.1.1     # the four 2606:50c0:800x::153
Resolve-DnsName www.happydwarf.dev -Server 1.1.1.1            # CNAME happy-dwarf-team.github.io
```

(GitHub's docs give `dig` and name `Resolve-DnsName` for Windows **[doc]**.) Cloudflare
addresses here instead of GitHub's mean a record is proxied.

```sh
gh api repos/happy-dwarf-team/happydwarf-website/pages \
  --jq '{cname, protected_domain_state, https_enforced, cert: .https_certificate}'
# cname happydwarf.dev, protected_domain_state verified, https_enforced true, cert state approved
gh api repos/happy-dwarf-team/happydwarf-website/pages/health   # 202 first, then the DNS check result
curl -sI https://www.happydwarf.dev/ | grep -iE '^(HTTP|location)'
# 301 to https://happydwarf.dev/
```

Whether GitHub's certificate lists `www.happydwarf.dev` beside the apex (needed for the HTTPS
redirect to work without a warning) is **[to verify]** in `https_certificate.domains`; the docs do
not say.

## Open questions surfaced

1. **Does a cache `HIT` filled without `Origin` still carry CORS headers?** If not, the build
   needs a decision (always send `crossorigin`, a cache-key rule, or accept no CORS on hits).
   Only testable once the bucket exists; small enough to stay a verification step unless it fails.
2. **Does GitHub's apex certificate cover `www`?** Decides whether the `www` redirect works over
   HTTPS on a `.dev` (HSTS-preloaded) domain; checkable only once the hub repository has its
   domain.
3. **Does the Cloudflare API MCP's OAuth grant carry R2 and zone-settings scopes?** If not, steps
   2 to 7 go through Wrangler (`wrangler login`) instead; it does not change the checklist.
4. **Does R2 checkout require a payment method on the free tier?** A dashboard step for the account owner
   either way.
