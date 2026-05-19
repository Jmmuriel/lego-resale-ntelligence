import csv
import json
import sys
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.db.crud import replace_portfolio_items, replace_price_history, upsert_set_catalog
from backend.db.database import V2_DATABASE_URL, get_session_factory, init_v2_db
from backend.db.models import PortfolioItem, PriceHistory, SetCatalog


CATALOG_PATH = PROJECT_ROOT / "data" / "catalog.csv"
PRICE_HISTORY_PATH = PROJECT_ROOT / "data" / "price_history_seed.json"
PORTFOLIO_PATH = PROJECT_ROOT / "data" / "portfolio_seed.json"


def load_catalog_sets() -> list[SetCatalog]:
    with CATALOG_PATH.open(newline="", encoding="utf-8") as file:
        rows = csv.DictReader(file)
        return [
            SetCatalog(
                set_id=row["set_id"],
                name=row["name"],
                theme=row["theme"],
                year_released=_optional_int(row["year_released"]),
                year_retired=_optional_int(row["year_retired"]),
                retail_price_eur=_optional_float(row["retail_price_eur"]),
                pieces=_optional_int(row["pieces"]),
                popularity_score=_optional_int(row["popularity_score"]),
                metadata_json={"source": "data/catalog.csv"},
            )
            for row in rows
        ]


def load_price_history() -> list[PriceHistory]:
    raw_snapshots = json.loads(PRICE_HISTORY_PATH.read_text(encoding="utf-8"))
    return [
        PriceHistory(
            set_id=snapshot["set_id"],
            condition=snapshot["condition"],
            source=snapshot["source"],
            price_min_eur=snapshot["price_min_eur"],
            price_avg_eur=snapshot["price_avg_eur"],
            price_max_eur=snapshot["price_max_eur"],
            sample_count=snapshot["sample_count"],
            recorded_at=date.fromisoformat(snapshot["recorded_at"]),
        )
        for snapshot in raw_snapshots
    ]


def load_portfolio_items() -> list[PortfolioItem]:
    raw_items = json.loads(PORTFOLIO_PATH.read_text(encoding="utf-8"))
    return [
        PortfolioItem(
            set_id=item["set_id"],
            set_name=item["set_name"],
            condition=item["condition"],
            quantity=item["quantity"],
            cost_basis_eur=item["cost_basis_eur"],
            purchased_at=date.fromisoformat(item["purchased_at"]),
            status=item["status"],
            sell_target_eur=item.get("sell_target_eur"),
            notes=item.get("notes"),
        )
        for item in raw_items
    ]


def seed_database(database_url: str = V2_DATABASE_URL) -> dict[str, int]:
    init_v2_db(database_url)
    session_factory = get_session_factory(database_url)

    catalog_sets = load_catalog_sets()
    price_history = load_price_history()
    portfolio_items = load_portfolio_items()

    with session_factory() as session:
        for set_item in catalog_sets:
            upsert_set_catalog(session, set_item)
        price_history_count = replace_price_history(session, price_history)
        portfolio_count = replace_portfolio_items(session, portfolio_items)
        session.commit()

    return {
        "catalog_sets": len(catalog_sets),
        "price_history": price_history_count,
        "portfolio_items": portfolio_count,
    }


def _optional_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def _optional_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


if __name__ == "__main__":
    counts = seed_database()
    print("Seeded V2 database")
    for key, value in counts.items():
        print(f"{key}: {value}")
