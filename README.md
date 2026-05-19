# LEGO Resale Intelligence

A personal e-commerce intelligence tool that turns retired LEGO marketplace listings into structured buying signals: fair price, net margin, risk flags and an opportunity score — built end-to-end in Python with a premium Streamlit UI.

> **Portfolio project** — built to demonstrate product engineering, LLM integration and UI polish without over-engineering the architecture.

---

## V2 status

V1 is the stable Streamlit product. V2 is an incremental expansion in the same repo, not a rewrite.

V2 adds:

- FastAPI backend in `backend/`
- Next.js frontend in `frontend/`
- dynamic pricing seed data
- set-level intelligence with price history charts
- portfolio P&L views
- local market briefings
- shared SQLite watchlist workflow
- premium Linear/Stripe-inspired UI with restrained LEGO cues and a Three.js scene

Current V2 progress:

- Demo local: **97/100**
- Full guide: **84/100**

Start V2 locally:

```bash
# Terminal 1
bash scripts/v2_start_api.sh

# Terminal 2
bash scripts/v2_start_frontend.sh
```

Open:

- V2 web: `http://127.0.0.1:3000`
- V2 API docs: `http://127.0.0.1:8000/docs`

Check V2:

```bash
bash scripts/v2_doctor.sh
```

V2 documentation:

- [`docs/v2/README.md`](docs/v2/README.md)
- [`docs/v2/demo_runbook.md`](docs/v2/demo_runbook.md)
- [`docs/v2/release_checklist.md`](docs/v2/release_checklist.md)
- [`docs/v2/portfolio_story.md`](docs/v2/portfolio_story.md)
- [`docs/v2/deploy_plan.md`](docs/v2/deploy_plan.md)
- [`docs/v2/guide_gap_analysis.md`](docs/v2/guide_gap_analysis.md)
- [`docs/v2/postgres_alembic_notes.md`](docs/v2/postgres_alembic_notes.md)
- [`docs/v2/db_read_fallback_notes.md`](docs/v2/db_read_fallback_notes.md)
- [`docs/v2/data_quality_notes.md`](docs/v2/data_quality_notes.md)

---

## Live demo

🔗 [https://lego-resale-ntelligence-gybrigvpvh9aa9epszcdul.streamlit.app](https://lego-resale-ntelligence-gybrigvpvh9aa9epszcdul.streamlit.app)

### Deploy to Streamlit Community Cloud

1. Push this repo to GitHub (make sure `.env` and `db/lri.db` are in `.gitignore` — they already are)
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Set the main file path to: `app/main.py`
4. Under **Advanced settings → Secrets**, paste:
   ```toml
   ANTHROPIC_API_KEY = "your_key_here"
   ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"
   ```
5. Deploy — the app will be live at `https://your-app-name.streamlit.app`

> **Note on persistence:** The SQLite archive is ephemeral on Streamlit Cloud — analyses won't survive redeploys. This is expected for a portfolio demo; for a persistent version, swap `DATABASE_URL` for a hosted Postgres instance.

---

## What it does

Paste a listing URL from Wallapop or eBay. The system:

1. Downloads the listing HTML
2. Extracts structured data (title, set ID, condition, risks) via Anthropic
3. Matches the set against a local catalog
4. Looks up a manual fair price reference
5. Calculates gross margin, net margin and selling fees
6. Produces an opportunity score (0–100) with a GREEN / AMBER / RED category
7. Persists the result to a local SQLite archive
8. Displays everything in a clean, premium Streamlit interface

---

## Screenshots

| Overview | Analyze | About |
|---|---|---|
| ![Overview](docs/screenshots/phase3b_desktop_overview.png) | ![Analyze](docs/screenshots/phase3b_desktop_analyze.png) | ![About](docs/screenshots/phase3b_desktop_about.png) |

**Archived score detail**

![Archived score](docs/screenshots/phase3b_closeup_archived_score.png)

**Mobile**

| Overview | Analyze | Archive |
|---|---|---|
| ![Mobile overview](docs/screenshots/phase3b_mobile_overview.png) | ![Mobile analyze](docs/screenshots/phase3b_mobile_analyze.png) | ![Mobile archive](docs/screenshots/phase3b_closeup_mobile_archive.png) |

---

## Architecture

Eight focused modules, each with a single responsibility. No FastAPI, no React, no Docker — intentionally small so every part is explainable and testable.

```
URL
 └─▶ capture.py              Download listing HTML (requests + BeautifulSoup)
      └─▶ extract.py         Structure the text via Anthropic (title, set ID, condition, risks)
           └─▶ identify.py   Match against data/catalog.csv
                └─▶ pricing_reference.py   Look up manual fair price by set + condition
                     └─▶ scoring.py        Calculate margins, fees and opportunity score
                          └─▶ db.py        Persist result to SQLite via SQLAlchemy
                               └─▶ app/main.py   Streamlit UI (Overview · Analyze · About)
```

**Scoring is explicit, not a black box.**
Net margin drives the score. Risk flags reduce confidence. GREEN requires a strong score AND a positive absolute margin.

```
gross_margin  = fair_price − asking_price
net_margin    = gross_margin − selling_fees − outbound_shipping
```

---

## Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| UI | Streamlit + custom CSS/HTML |
| LLM | Anthropic (`claude-haiku-4-5`) |
| Data modeling | Pydantic v2 |
| Persistence | SQLite + SQLAlchemy |
| HTML capture | requests + BeautifulSoup |
| Testing | pytest |
| Config | python-dotenv |

---

## Test coverage

```
114 passed
```

Tests cover: data models, capture, extraction mocks, catalog matching, pricing lookups, scoring logic, margin calculations, database operations, FastAPI routes, dynamic pricing, DB-backed seed loading, seed data validation, data quality API, catalog research queue, portfolio logic (including CRUD), Claude Sonnet briefings with local fallback, expanded price history for all 10 active sets, and watchlist workflows.

---

## Local setup

```bash
# 1. Clone and create virtual environment
git clone https://github.com/YOUR_USERNAME/lego-resale-intelligence.git
cd lego-resale-intelligence
python -m venv .venv && source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

# 4. Run
streamlit run app/main.py
```

Open `http://localhost:8501`

### Environment variables

```env
ANTHROPIC_API_KEY=your_key_here
ANTHROPIC_MODEL=claude-haiku-4-5-20251001   # optional, this is the default
DATABASE_URL=                                # leave empty to use db/lri.db
```

### Run tests

```bash
pytest
```

---

## Catalog coverage

10 retired sets currently supported:

| Set | Name | Theme |
|---|---|---|
| 75192 | Millennium Falcon (UCS) | Star Wars |
| 75252 | Imperial Star Destroyer (UCS) | Star Wars |
| 75313 | AT-AT (UCS) | Star Wars |
| 75059 | Sandcrawler (UCS) | Star Wars |
| 75095 | TIE Fighter (UCS) | Star Wars |
| 10179 | Millennium Falcon (original UCS) | Star Wars |
| 10030 | Imperial Star Destroyer (original) | Star Wars |
| 21003 | Seattle Space Needle | Architecture |
| 10214 | Tower Bridge | Creator Expert |
| 10243 | Parisian Restaurant | Creator Expert |

Fair price references are stored in `src/pricing_reference.py` and updated manually.

---

## Known limits

These are documented constraints, not hidden failures.

- **Catalog is small by design** — fair prices require manual research; expanding coverage takes time.
- **HTML parsing is basic** — marketplaces can change page structure; this is a known fragility.
- **eBay may block requests** — 403 errors are an external constraint, not a bug.
- **Score is explainable, not financial advice** — every signal is visible and traceable.
- **No real-time pricing** — fair prices are manually set references, not live market data.

---

## Validation

Tested against 20+ real Wallapop and eBay URLs. 13 completed the full pipeline end-to-end; 7 failed due to external marketplace constraints (404s, 403 blocks, removed listings) — all documented.

Full validation notes: [`docs/phase_2_validation.md`](docs/phase_2_validation.md)

---

## Project context

Built as a personal portfolio project to demonstrate:

- **End-to-end product thinking** — from raw marketplace HTML to a scored, archived buying signal
- **LLM integration** — structured extraction with Anthropic, explicit fallback handling
- **Explainable scoring** — every number is traceable; no magic
- **UI polish** — premium Streamlit experience without a frontend framework
- **Honest scope** — v1 that works, with documented limits and a clear path forward

---

_Personal educational project. Not affiliated with or endorsed by the LEGO Group._
