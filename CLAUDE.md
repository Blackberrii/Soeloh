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

- **HorizonsRP** — a Garry's Mod DarkRP server. This is the one concrete active
  project. Real features: economy tuning, custom jobs, E2/Wiremod scripting,
  custom HUD, casino/coinflip systems, a "Credits" premium currency.
  - Discord invite: https://discord.gg/ywQaMYv8qJ
  - Server connect: `193.243.190.4:27087` (steam://connect/ link used for the button)
- **GeneratedByAccident** — AI-generated music project on Suno, wide genre range
  (brostep, hardstyle, sea shanties, conscious rap, comedy tracks, etc).
  - Suno profile: https://suno.com/@generatedbyaccident
  - Track list on the site is currently placeholder/example titles pulled from
    memory — verify against actual catalog before treating as final copy.

## What's NOT real — don't reintroduce

Earlier drafts of this site listed several things as live/shipped that turned out
not to be current or real:
- "Soeloh Hosting" as an actual hosting service
- Prompt Singularity (Godot idle game) as a shipped product
- Hermes/BAI Discord bot as a live deployment
- Home security AI camera pipeline as a public-facing project
- A general "Minecraft server network"
- A Downloads section (there's nothing to download — this was removed entirely)

If asked to add project cards, don't invent status/specifics for things — ask first
or leave placeholders, same pattern as the "Future Ideas" section below.

## "Future Ideas" section

Intentionally blank placeholder cards (`Untitled 01/02/03`), styled dashed/dimmed
to visually read as "not real yet." Meant to be filled in by hand later, not
auto-generated with guessed content.

## Design tokens

- Palette: near-black bg (`#0b0e12`), panel (`#12161d`), primary accent purple
  (`#b98cff`), secondary accent deep gold (`#d4af37`). Deliberately avoided the
  generic near-black + single neon-green "hacker" look.
- Type: Space Grotesk (display), IBM Plex Sans (body), JetBrains Mono (labels/terminal).
- Signature element: CRT scanline overlay + a terminal boot-sequence in the hero.
  Keep the boot lines terse and deadpan — an earlier version had a joke line
  ("sleep_schedule.dll not found") that read as try-hard/cheesy and was cut.
  Favor plain status lines over jokes.
- Vibe target: dark and techy, retro/arcade-adjacent, explicitly "not geeky or nerdy."

## Deploy

- Static single-file site (`index.html`), meant for GitHub Pages.
- Domain: soeloh.com — needs a `CNAME` file in repo root containing just `soeloh.com`,
  plus DNS pointed at GitHub Pages.
- Repo is private, GitHub Pro plan — Pages can still publish publicly from a
  private repo on Pro (this is expected/intentional, not a bug to "fix").
