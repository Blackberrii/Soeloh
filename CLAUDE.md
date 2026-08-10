# soeloh.com — context notes

Background info from building this site that isn't obvious from the code alone.

## Identity

- "Soeloh" is a personal brand name, not a company or product. There is no Soeloh
  Hosting business, no hosting product, nothing sold under that name.
- Real name does not appear anywhere on the site. Keep it that way — no full name
  in copy, meta tags, alt text, comments, or filenames. Discord handle (Blackberrii)
  and Suno alias (GeneratedByAccident) are fine to use; those are public handles,
  not identifying info.

## What's actually real (safe to feature/expand)

- **Blackthorn** (renamed from "BlackberryAI", 2026-08-10 — see note below on the
  name's earlier, unrelated use) — a self-hosted LLM gateway (LiteLLM proxy + Open
  WebUI + SearXNG) for friends/family, with per-friend budgeted keys routed through
  an auto-router called "Nightshade". This is the current flagship section on
  `index.html` (`#blackthorn`, replacing the old `#project`/HorizonsRP slot).
  - **Deliberately kept as a homepage section, not its own page.** A previous pass
    split it out to its own page (mirroring the music.html/horizonsrp.html
    pattern) — the user explicitly reverted that and asked for the full content
    back on `index.html` itself. Don't re-split it out without asking first.
  - The section now covers the model lineup (Nightshade as the default
    auto-router; "Belladonna" as the vision-capable tier) and the tool
    ecosystem (42 custom tools, proactive tool-calling, private search,
    real code execution, plain-language usage%). These are in-house display
    names for the underlying models, matching the existing "Nightshade"
    naming convention — real backing models/vendors are not named on the
    site, same as before.
  - "Belladonna" used to be two different things at two different points:
    briefly a separate roleplay/creative-writing model (decommissioned,
    removed from the lineup card entirely - don't reintroduce a creative-
    writing card without a real instance backing it), then later reused as
    the display name for the renamed vision tier (previously shown here as
    "Nemotron Vision"). The site now only reflects the current meaning -
    vision. Local transcription (previously a "Voice" tool card, backed by
    a self-hosted Whisper instance) was also decommissioned and removed from
    the tool cards and the top pill-row - don't reintroduce either without a
    real live instance backing it.
  - **Naming note on "Blackthorn":** the name was briefly used before, for something
    unrelated — a Hermes Agent-backed agentic/tool-use model card that existed as a
    fourth lineup entry (2026-08-07/08) then was fully decommissioned (2026-08-08).
    The maintenance cost (its own container, key management, config-drift bugs)
    outweighed the demonstrated value once DeepSeek/Nightshade's own proactive
    tool-calling turned out to cover the same ground for how friends actually use
    it. That guidance still applies on its own terms — don't reintroduce a
    Hermes/bolt-on-style agentic model *card* without a real, current instance
    backing it. Separately, as of 2026-08-10 "Blackthorn" was reused as the name of
    the *entire project* (formerly "BlackberryAI") — a different and much bigger
    thing than the old model card, not a revival of it.
  - **Invite-only, not public signup** — per explicit decision, the site describes
    what it is (stack, features) but does NOT publish the actual chat URL/domain.
    Only a Discord contact ("message me for access") is given. Don't add a direct
    link to the deployed instance without asking first — this was a deliberate
    privacy choice, not an oversight.
  - No live status badge for this (unlike HorizonsRP) — there's no public
    equivalent of `status.json` for it, and shouldn't be exposed for an
    invite-only service anyway. The hero's "blackthorn · live" badge is static,
    not fetched.
  - Source project lives in a separate local directory, not this repo.

- **HorizonsRP** — a Garry's Mod DarkRP server. Now has its own page,
  `horizonsrp.html`, rather than being a section of `index.html` (moved out once
  Blackthorn became the flagship project — same pattern as `music.html` getting
  split out earlier). Still linked from nav on every page, the hero, and the
  Links section. Real features: economy tuning, custom jobs, custom HUD,
  casino/coinflip systems, a "Credits" premium currency. (E2/Wiremod scripting was
  listed here before but isn't a current feature — don't reintroduce it.)
  - Discord invite: https://discord.gg/ywQaMYv8qJ
  - Server connect: `193.243.190.4:27087` (steam://connect/ link used for the button)
  - Live status: `scripts/query_status.py` queries the server via A2S and writes
    `status.json` at the repo root; `.github/workflows/server-status.yml` runs it
    on a cron. `horizonsrp.html` fetches `status.json` client-side to show
    online/offline + player count next to the heading; `index.html`'s hero badge
    also reads the same file for a lightweight online/offline indicator.
  - Branding assets (logo, banner) live in `assets/` — `horizonsrpicon.png` is the
    real server logo, used as the small icon next to the HorizonsRP heading.
- **GeneratedByAccident** — AI-generated music project on Suno, wide genre range
  (brostep, hardstyle, sea shanties, conscious rap, comedy tracks, etc).
  - Suno profile: https://suno.com/@generatedbyaccident
  - Has its own page: `music.html` (linked from nav / hero / about — not a section
    of `index.html` anymore, moved out once the catalog got real).
  - The track list is live, not hand-written. `scripts/query_suno_tracks.py`
    pulls the real catalog (title, genre tags, direct CDN audio URL, play count)
    by parsing the JSON that Suno's profile page embeds in its Next.js payload —
    there's no official Suno API for this. Writes `tracks.json` at the repo root;
    `.github/workflows/suno-tracks.yml` runs it every 3h, with retries on the
    fetch itself. `music.html` fetches `tracks.json` client-side, shows up to 20
    tracks with genre pills, play counts, and an inline `<audio>` player wired to
    the real CDN mp3 URL per track.
  - This is inherently fragile — it depends on Suno's frontend structure, not a
    stable protocol. The script fails closed: on any parse error or zero results
    it leaves `tracks.json` untouched rather than wiping the site's copy, so a
    broken scrape just means stale data, not an empty page. If it ever needs
    fixing, the parsing approach (decode `self.__next_f.push(...)` chunks, then
    brace-match `"content_type":"clip","content_item":{...}` objects out of the
    resulting text) is documented in the script's docstring.

## What's NOT real — don't reintroduce

Earlier drafts of this site listed several things as live/shipped that turned out
not to be current or real:
- "Soeloh Hosting" as an actual hosting service
- Prompt Singularity (Godot idle game) as a shipped product
- Hermes/BAI Discord bot as a live deployment
- Home security AI camera pipeline as a public-facing project
- A general "Minecraft server network"
- A Downloads section (there's nothing to download — this was removed entirely)

If asked to add project cards for something speculative/unshipped, don't invent
status or specifics — ask first or leave an honest placeholder. This doesn't
apply to the "Active Projects" section below, which is real live data, not
hand-curated copy.

## "Active Projects" section (`#projects`, on `index.html`)

This used to be "Future Ideas" — three intentionally-blank dashed placeholder
cards. It's now a live feed instead, and — like HorizonsRP/Suno — goes through
the cron+JSON pattern rather than calling the GitHub API client-side (an earlier
version did call the API directly from the browser on every page load; moved off
that for reliability and to allow richer per-repo data without an API-call-per-repo
cost on every visit).

`scripts/query_github.py` writes `github.json` at the repo root, containing:
- `projects`: public repos (forks/archived/the Soeloh repo itself excluded),
  sorted by `pushed_at`, top 6. Each includes a `languages` breakdown (name +
  percent, from the GitHub per-repo languages endpoint — that's why project
  cards show pills like "Python 91.7%" instead of a single language tag) and
  `topics` if the repo has any set.
- `activity`: last 5 public events from `/users/Blackberrii/events/public`, with
  real commit messages resolved server-side for push events via the per-commit
  endpoint. No sorting/filtering beyond "most recent 5" — kept simple on purpose.

`.github/workflows/github-data.yml` runs it hourly. Fails closed like the other
scripts — leaves `github.json` untouched on error rather than wiping the site's
copy. `index.html` fetches `github.json` client-side (same-origin) and renders
both the project grid and the activity list from it; if that fetch fails, it
shows an honest fallback card rather than inventing content.

There are no more hand-edited placeholder cards anywhere on the site — if a new
"not real yet" section is wanted in the future, ask before reintroducing that
pattern rather than assuming it should look like the old Future Ideas cards.

The `.pill`/`.pill-row` classes (small rounded label chips) are used for both
GitHub language/topic tags and Suno genre tags — it's a shared visual language
across the live-data sections now, not something specific to music.

## Design tokens

- Palette: near-black bg (`#0b0e12`), panel (`#12161d`), primary accent purple
  (`#b98cff`), secondary accent deep gold (`#d4af37`). Deliberately avoided the
  generic near-black + single neon-green "hacker" look.
- Type: Space Grotesk (display), IBM Plex Sans (body), JetBrains Mono (labels/terminal).
- Signature element: CRT scanline overlay sitewide, plus a row of GitHub-shields-
  style status badges (label|value pills) at the top of the hero. There used to be
  a fake terminal window there (traffic-light dots, `root@soeloh` title bar, typing
  animation) — it got cut because it read as costume-y "hacker LARP," which cuts
  against the vibe target below. The badges keep the same real-status info
  (HorizonsRP online/offline, live from `status.json`) without the terminal
  cosplay. Don't reintroduce the fake-terminal treatment.
- Vibe target: dark and techy, retro/arcade-adjacent, explicitly "not geeky or nerdy."

## Deploy

- Static site, meant for GitHub Pages: `index.html` (hub — hero, about,
  Blackthorn, Active Projects, music teaser, links), `horizonsrp.html`
  (full HorizonsRP server page), `music.html` (full Suno catalog), and
  `404.html`. Multi-page now, but still hand-written files, not a build
  pipeline — no shared stylesheet, so base CSS (design tokens, nav, scanlines,
  `.card`/`.btn`/`.pill`, etc.) is duplicated across `index.html`,
  `horizonsrp.html`, and `music.html`. If a design-token or nav change is made
  in one, it needs to be mirrored in the other two — nav in particular, since
  each page lists all the others.
- Live data files at the repo root (`status.json`, `tracks.json`, `github.json`)
  are all generated by scripts in `scripts/` on schedules defined in
  `.github/workflows/`. Don't hand-edit these — they get overwritten by the next
  cron run. Same fail-closed pattern across all three: a bad run leaves the
  existing file untouched rather than blanking it.
- Domain: soeloh.com — `CNAME` file in repo root contains `soeloh.com`. DNS is on
  Porkbun: 4 A records (GitHub Pages IPs) + 4 AAAA records for the apex, plus a
  `www` CNAME to `blackberrii.github.io`. Existing Porkbun email-forwarding
  (MX/SPF) and `_acme-challenge` TXT records were left alone — don't touch those.
- Repo is private, GitHub Pro plan — Pages can still publish publicly from a
  private repo on Pro (this is expected/intentional, not a bug to "fix").
