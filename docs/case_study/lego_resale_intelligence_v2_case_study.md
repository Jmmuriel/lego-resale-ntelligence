# LEGO Resale Intelligence V2 Case Study

## One-line summary

LEGO Resale Intelligence evolved from a working Streamlit URL analyzer into a deployed collector intelligence product with FastAPI, Next.js, dynamic seed pricing, watchlists, portfolio P&L, analyst briefings and explicit data-quality governance.

## Role

Solo builder: product strategy, backend, frontend, data modeling, UX direction, testing, deployment preparation, public smoke validation and portfolio storytelling.

## Context

V1 proved the core workflow:

- capture a marketplace listing;
- extract structured listing data with an LLM;
- identify the LEGO set;
- calculate fair price, net margin, risk and opportunity score;
- save the result to a local archive.

V2 was intentionally incremental. The working V1 pipeline remains useful while the new product layer expands around it.

## Product problem

Collectors and resellers do not only need one-off listing analysis. They need a repeatable operating system:

- which sets are worth watching;
- how prices are moving;
- what a portfolio is worth;
- when an opportunity is attractive;
- which data is reliable enough to trust.

## V2 scope

V2 adds:

- FastAPI backend;
- Next.js frontend;
- market overview dashboard;
- set intelligence and price-history charts;
- watchlist workflow;
- portfolio P&L;
- analyst briefings with local fallback;
- Research page for data maturity;
- active evidence audit log;
- Railway backend deployment;
- Vercel frontend deployment;
- Postgres/Alembic foundation with local seed fallback.

## Design direction

The UI direction keeps restrained LEGO cues while moving toward a premium collector terminal:

- Linear/Stripe-inspired structure;
- red/yellow LEGO accents;
- dense dashboard layout;
- product-grade 2D interface;
- no final 3D direction;
- same case-study deck style as V1.

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

## Data governance

The most important V2 decision was not to overclaim the data.

Current status:

- 50 active catalog sets;
- 250 seed price snapshots;
- 50 active evidence audits started;
- 49 externally verified active sets under the current app rules;
- 1 set remains under review because sources materially disagree with the seed catalog.

This means the project should be presented as a seed-backed, partially verified prototype, not as a fully verified live market data platform.

Evidence tracking lives in:

```text
data/catalog_active_research.json
```

The app exposes this through:

```text
/api/market/active-evidence
```

The Research page displays the audit log directly in the UI.

## Example audit finding

Set `10220` Volkswagen T1 Camper Van remains intentionally under review.

Reason:

- external sources materially disagree on lifecycle, piece count and EUR/RRP assumptions;
- forcing a weak verification claim would make the portfolio story less credible;
- keeping it as seed/demo data shows better product judgment.

## Deployment status

The V2 public demo is live as a split deployment:

- Web: `https://lego-resale-ntelligence.vercel.app/`
- API: `https://lego-resale-ntelligence-production.up.railway.app/`

The repo includes:

- Railway backend setup via `Dockerfile`;
- Vercel frontend setup from `frontend/`;
- CORS configuration for the public frontend;
- optional Railway Postgres through `V2_DATABASE_URL`;
- production smoke testing through `scripts/v2_deploy_smoke.sh`.

## Quality bar

Verified:

```text
116 passed
npm run build OK
public smoke OK
```

Tests cover the core pipeline, API routes, dynamic pricing, seed validation, data quality APIs, research queue, watchlist workflows, portfolio logic and briefing fallback.

## Interview framing

I first built a working Streamlit V1 to prove the end-to-end pipeline. Then I evolved it into V2 without throwing away the stable core. The key product shift was moving from a single listing analyzer to a collector intelligence terminal: market trends, portfolio P&L, watchlist, briefings and data maturity.

The most important engineering decision was data honesty. Instead of claiming that 50 sets were verified live market data, I added provenance tracking and an audit log. That made the product more credible, because it can show what is seed data, what is under review and what is actually verified.

## Remaining work

- Resolve the remaining `10220` evidence conflict.
- Move from seed/demo price history to externally sourced market snapshots.
- Add more sets only through the candidate evidence gate.
- Decide whether active, retiring and retired sets need separate lifecycle models.
- Refresh screenshots if the UI changes again.

## Honest positioning

Use this phrase:

> Seed-backed LEGO resale intelligence prototype with production-style architecture, data-quality gates and portfolio workflows.

Avoid this phrase for now:

> Verified live LEGO market pricing platform.
