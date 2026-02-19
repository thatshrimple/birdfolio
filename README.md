# 🦅 Birdfolio

**An AI-powered bird life list skill for OpenClaw agents.**

Send a bird photo to your agent. Get an instant species ID, a rarity classification, a shareable trading card, and a personal life list — automatically. No apps, no accounts, no setup beyond a single command.

Compatible with any multimodal model (Claude, GPT-4o, Gemini, etc.).

---

## What It Does

1. **Snap & Identify** — Send a bird photo via Telegram. The agent uses Vision AI to identify the species, scientific name, and notable features.
2. **Rarity Classification** — Searches real-time eBird data to classify the bird as Common 🟢, Rare 🟡, Super Rare 🔴, or Bonus ✨ for your region.
3. **Trading Card** — Generates a styled card with your actual photo, a fun fact, and a rarity badge. Screenshots it to PNG and sends it back.
4. **Life List** — Every lifer is logged to a Railway PostgreSQL database, scoped to your Telegram ID.
5. **PWA** — Your life list lives at `yourdomain.com/app/{telegram_id}` — installable to homescreen, no app store needed.
6. **Regional Checklist** — Tracks progress against a 16-species checklist (10 common, 5 rare, 1 super rare) built from eBird data for your region.

---

## Demo

> **Live PWA:** [birdfolio.tonbistudio.com](https://birdfolio.tonbistudio.com)

---

## Stack

| Layer | Tech |
|---|---|
| Agent runtime | [OpenClaw](https://openclaw.ai) |
| Vision AI | Any multimodal model (Claude, GPT-4o, Gemini, etc.) |
| Backend API | FastAPI + SQLAlchemy async + PostgreSQL |
| Hosting | Railway |
| Card images | Cloudflare R2 |
| PWA | Vanilla JS, installable |
| Card rendering | Playwright (headless Chrome screenshot) |
| Bird data | You.com API (real-time eBird results) |

---

## Requirements

- **OpenClaw** agent with a multimodal model configured (Claude, GPT-4o, Gemini, etc.)
- **You.com API key** for real-time eBird rarity lookups
- Python 3.10+, Node.js (for the card screenshot script)

That's it. The API, database, and card image hosting are all provided.

---

## Install

```bash
clawhub install birdfolio
```

Or clone into your OpenClaw `skills/` folder:

```bash
git clone https://github.com/thatshrimple/birdfolio skills/birdfolio
```

---

## Setup

Just tell your agent: **"Set up my Birdfolio"**

It will ask for your home region, build a 16-species checklist from eBird data, register you in the shared API, and send you a link to your personal PWA. No accounts, no deployments, no credentials to manage.

> **Your PWA:** `https://birdfolio.tonbistudio.com/app/{your_telegram_id}`

### Self-Hosting (Advanced)

If you'd prefer to run your own backend, deploy [birdfolio-api](https://github.com/thatshrimple/birdfolio-api) to Railway and pass `--api-url` to the init script. See the API repo for full setup instructions.

---

## Scripts

| Script | What it does |
|---|---|
| `init_birdfolio.py` | First-time setup — registers user, creates workspace |
| `log_sighting.py` | Logs a sighting to the API |
| `update_checklist.py` | Marks a species as found on your checklist |
| `sync_checklist.py` | Pushes local `checklist.json` to the API |
| `get_stats.py` | Fetches stats + checklist progress from the API |
| `generate_card.py` | Generates the HTML trading card with embedded photo |
| `screenshot_card.js` | Screenshots the card HTML to PNG (uses playwright-core) |
| `upload_card.py` | Uploads card PNG to Cloudflare R2, returns public URL |
| `generate_checklist_card.py` | Generates a visual checklist progress card |

All scripts output JSON to stdout and accept `--workspace` + `--api-url` args.

---

## Project Structure

```
birdfolio/
├── SKILL.md                  # Agent instructions (OpenClaw skill format)
├── scripts/                  # All executable scripts
├── assets/
│   └── card-template.html    # Base card HTML template
└── references/
    ├── data-schema.md        # API + data structure reference
    └── you-search-queries.md # You.com query templates for rarity lookup
```

---

## Multi-User

The API and database are fully multi-user — each user is keyed by Telegram ID. The PWA is accessible at `/app/{telegram_id}` for any registered user. The agent automatically sends new users their personal link after their first lifer sighting.

---

## Related

- **[birdfolio-api](https://github.com/thatshrimple/birdfolio-api)** — FastAPI backend + PWA frontend

---

## Built By

**Scampi & Tonbi** — a human-AI duo building onchain and AI projects in public.

- 🐦 Scampi: [@itsthatshrimple](https://x.com/itsthatshrimple)
- 🐦 Tonbi: [@tonbistudio](https://x.com/tonbistudio)
- 📺 YouTube: [Onchain Vibe Code](https://youtube.com/@OnchainVibeCode)
- 🌐 Portfolio: [scampi.tonbistudio.com](https://scampi.tonbistudio.com)

---

*Built with 🦐 and too many bird facts.*
