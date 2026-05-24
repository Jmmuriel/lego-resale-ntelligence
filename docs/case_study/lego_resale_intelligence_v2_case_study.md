# LEGO Resale Intelligence V2 Case Study

## One-line Summary

LEGO Resale Intelligence evolved from a Streamlit URL analyzer into a product-style market intelligence dashboard with FastAPI, Next.js, portfolio P&L, seeded price history, research governance and deploy-ready architecture.

## Role

Solo builder: product strategy, backend, frontend, data modeling, UX direction, testing, documentation and deployment preparation.

## Context

V1 proved the core workflow:

- capture a marketplace listing;
- extract structured data with an LLM;
- identify the LEGO set;
- calculate fair price, margin, risk and opportunity score;
- save the result to a local archive.

V2 was designed as an incremental evolution, not a rewrite. The goal was to preserve the working V1 pipeline while adding a more professional product surface around it.

## Product Problem

Collectors and resellers do not just need one-off listing analysis. They need a repeatable operating system:

- which sets are worth watching;
- how prices are moving;
- what a portfolio is worth;
- when an opportunity is attractive;
- which data is reliable enough to trust.

## V2 Scope

V2 adds:

- FastAPI backend;
- Next.js frontend;
- market overview dashboard;
- set intelligence and price history charts;
- watchlist workflow;
- portfolio P&L;
- local analyst briefings;
- Research page for data maturity;
- active evidence audit log;
- Railway/Vercel deploy preparation;
- Postgres/Alembic foundation.

## Design Direction

The UI direction moved away from toy-like LEGO styling and toward a premium collector terminal:

- Linear/Stripe-inspired structure;
- restrained LEGO cues;
- dense dashboard layout;
- professional 2D interface;
- no 3D in the final direction.

## Architecture

```text
V1 core pipeline
  capture -> extract -> identify -> price -> score -> archive

V2 backend
  FastAPI routers
    /api/analyze
    /api/market
    /api/watchlist
    /api/portfolio
    /api/briefings

V2 frontend
  Next.js routes
    Market
    Analyze
    Watchlist
    Sets
    Research
    Portfolio
    Briefings
```

The system keeps JSON/CSV seed data as a local fallback while introducing SQLAlchemy models, Alembic migrations and a seed-to-database path for SQLite or Postgres.

## Data Governance

The most important V2 decision was not to overclaim the data.

Current status:

- 50 active seed/demo catalog sets;
- 250 seed price snapshots;
- 0 externally verified active sets;
- 1 active evidence audit started;
- set `75192` blocked by a retirement-date mismatch.

This means the project can be presented as a seed-backed prototype, but not as a verified live market data platform yet.

Evidence tracking now lives in:

```text
data/catalog_active_research.json
```

The app exposes this through:

```text
/api/market/active-evidence
```

The Research page displays the audit log directly in the UI.

## Example Audit Finding

Set `75192` had enough metadata and pricing source candidates to start an evidence review, but it was not promoted to verified status.

Reason:

- the seed catalog marks `year_retired = 2024`;
- external sources indicate active status or estimated retirement in 2026;
- therefore the app keeps it as seed/demo data until the catalog assumption is resolved.

This is a useful portfolio point: the system does not just collect data; it prevents unsafe claims.

## Deployment Readiness

The repo is prepared for:

- Railway backend deployment using `Dockerfile`;
- Vercel frontend deployment from `frontend/`;
- optional Railway Postgres through `V2_DATABASE_URL`;
- CORS configuration via `BACKEND_CORS_ORIGINS`;
- optional first-run migrations and seed through:
  - `V2_RUN_MIGRATIONS=1`;
  - `V2_SEED_DATABASE=1`;
- production smoke testing through `scripts/v2_deploy_smoke.sh`.

## Quality Bar

Verified locally:

- backend/core tests passing;
- frontend production build passing;
- V2 doctor passing;
- browser check passing for Market and Research data status.

Latest local verification:

```text
116 passed
npm run build OK
bash scripts/v2_doctor.sh OK
```

## What I Would Say In An Interview

I first built a working Streamlit V1 to prove the end-to-end pipeline. Then I evolved it into V2 without throwing away the stable core. The key product shift was moving from a single listing analyzer to a collector intelligence terminal: market trends, portfolio P&L, watchlist, briefings and data maturity.

The most important engineering decision was data honesty. Instead of claiming that 50 sets were verified market data, I added explicit provenance tracking and an audit log. That made the product more credible, because it can show what is seed data, what is under review and what is actually verified.

## Remaining Work

- Publish backend on Railway.
- Publish frontend on Vercel.
- Decide whether active/retiring sets belong in the same catalog as retired sets.
- Resolve the `75192` retirement-date mismatch.
- Add verified evidence for more sets.
- Move from seed/demo price history to externally sourced market snapshots.
- Turn the Markdown case study into a final visual PDF/web case study.

## Honest Positioning

Use this phrase:

> Seed-backed LEGO resale intelligence prototype with production-style architecture, data-quality gates and portfolio workflows.

Avoid this phrase for now:

> Verified live LEGO market pricing platform.

