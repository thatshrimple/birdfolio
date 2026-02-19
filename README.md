# 🦅 Birdfolio

**An AI-powered bird life list skill for OpenClaw agents.**

Send a bird photo to your agent. Get an instant species ID, a rarity classification, a shareable trading card, and a personal life list — all automatically. No apps, no accounts, no setup beyond a single command.

---

## What It Does

1. **Snap & Identify** — Send any bird photo via Telegram. The agent uses Vision AI to identify the species, scientific name, and notable features.
2. **Rarity Classification** — Searches real-time eBird data to classify the bird as Common 🟢, Rare 🟡, Super Rare 🔴, or Bonus ✨ for your region.
3. **Trading Card** — Generates a styled card with your actual photo, fun fact, and rarity badge. Screenshots it to a PNG and sends it back.
4. **Life List** — Every lifer is logged to your personal field journal stored in a Railway PostgreSQL database.
5. **PWA** — Your life list lives at `yourdomain.com/app/{telegram_id}` — installable to your homescreen, no app store needed.
6. **Regional Checklist** — Tracks progress against a 16-species checklist (10 common, 5 rare, 1 super rare) built from eBird data for your home region.

---

## Demo

> **Live PWA:** [birdfolio.tonbistudio.com](https://birdfolio.tonbistudio.com)

![Birdfolio PWA screenshot showing life list with Anna's Hummingbird card](assets/preview.png)

---

## Stack

| Layer | Tech |
|---|---|
| Agent | [OpenClaw](https://openclaw.ai) + Claude Vision |
| Backend API | FastAPI + SQLAlchemy async + PostgreSQL |
| Hosting | Railway |
| Card images | Cloudflare R2 |
| PWA | Vanilla JS, installable |
| Card rendering | Playwright (headless Chrome screenshot) |
| Search | You.com API (real-time eBird data) |

---

## Install

```bash
clawhub install birdfolio
```

Or clone this repo into your OpenClaw `skills/` folder:

```bash
git clone https://github.com/tonbistudio/birdfolio skills/birdfolio
```

---

## Setup

### 1. Deploy the API

The skill requires a backend API. Deploy [birdfolio-api](https://github.com/tonbistudio/birdfolio-api) to Railway (or any platform that supports FastAPI + PostgreSQL).

### 2. Set up Cloudflare R2

Create an R2 bucket and save credentials to `secrets/r2-birdfolio.json` in your OpenClaw workspace:

```json
{
  "account_id": "your_account_id",
  "access_key_id": "your_key_id",
  "secret_access_key": "your_secret",
  "bucket": "birdfolio-cards",
  "endpoint": "https://your_account_id.r2.cloudflarestorage.com",
  "public_url": "https://pub-xxxx.r2.dev"
}
```

Enable **Public Access** on the bucket in the Cloudflare dashboard to get your `pub-xxxx.r2.dev` URL.

### 3. Initialize your Birdfolio

Tell your agent: *"Set up my Birdfolio"* — it will ask for your region, create your checklist, and register you in the API.

Or run directly:

```bash
python scripts/init_birdfolio.py \
  --telegram-id YOUR_TELEGRAM_ID \
  --region "Northern California" \
  --api-url "https://your-api.up.railway.app" \
  --workspace /path/to/birdfolio
```

---

## Scripts

| Script | What it does |
|---|---|
| `init_birdfolio.py` | First-time setup — registers user, creates workspace |
| `log_sighting.py` | Logs a sighting to the API |
| `update_checklist.py` | Marks a species as found on your checklist |
| `get_stats.py` | Fetches stats + checklist progress from API |
| `generate_card.py` | Generates the HTML trading card with embedded photo |
| `screenshot_card.js` | Screenshots the card HTML to PNG (uses playwright-core) |
| `upload_card.py` | Uploads card PNG to Cloudflare R2, returns public URL |
| `sync_checklist.py` | Pushes local checklist.json to the API (run after editing) |
| `generate_checklist_card.py` | Generates a visual checklist progress card |

---

## Project Structure

```
birdfolio/
├── SKILL.md                  # Agent instructions (OpenClaw skill)
├── scripts/                  # All executable scripts
├── assets/
│   └── card-template.html    # Base card HTML template
└── references/
    ├── data-schema.md        # API + data structure docs
    └── you-search-queries.md # You.com query templates for rarity lookup
```

---

## Related Repos

- **[birdfolio-api](https://github.com/tonbistudio/birdfolio-api)** — FastAPI backend + PWA frontend

---

## Built By

**Scampi & Tonbi** — a human-AI duo building onchain projects in public.

- 🐦 Scampi: [@itsthatshrimple](https://x.com/itsthatshrimple)
- 🐦 Tonbi: [@tonbistudio](https://x.com/tonbistudio)
- 📺 YouTube: [Onchain Vibe Code](https://youtube.com/@OnchainVibeCode)
- 🌐 Portfolio: [scampi.tonbistudio.com](https://scampi.tonbistudio.com)

---

*Built with 🦐 and too many bird facts.*
