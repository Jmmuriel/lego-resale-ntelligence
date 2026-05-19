import csv
import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal

from pydantic import ValidationError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.portfolio_engine import PortfolioItem
from backend.services.price_engine import PriceSnapshot


CATALOG_PATH = PROJECT_ROOT / "data" / "catalog.csv"
CATALOG_CANDIDATES_PATH = PROJECT_ROOT / "data" / "catalog_expansion_candidates.csv"
PRICE_HISTORY_PATH = PROJECT_ROOT / "data" / "price_history_seed.json"
PORTFOLIO_PATH = PROJECT_ROOT / "data" / "portfolio_seed.json"

CATALOG_REQUIRED_FIELDS = [
    "set_id",
    "name",
    "theme",
    "year_released",
    "year_retired",
    "retail_price_eur",
    "pieces",
    "popularity_score",
]
CANDIDATE_REQUIRED_FIELDS = [
    "set_id",
    "name",
    "theme",
    "reason",
    "validation_status",
]

Severity = Literal["error", "warning"]


@dataclass(frozen=True)
class SeedDataIssue:
    severity: Severity
    code: str
    message: str


def validate_seed_data(
    catalog_path: Path = CATALOG_PATH,
    price_history_path: Path = PRICE_HISTORY_PATH,
    portfolio_path: Path = PORTFOLIO_PATH,
    candidates_path: Path | None = CATALOG_CANDIDATES_PATH,
    target_catalog_size: int = 50,
) -> dict[str, Any]:
    """Validate V2 seed files before loading them into the database."""
    issues: list[SeedDataIssue] = []
    catalog_rows = _load_catalog_rows(catalog_path, issues)
    catalog_ids = _validate_catalog_rows(catalog_rows, issues, target_catalog_size)
    candidate_rows = _load_candidate_rows(candidates_path, issues)
    candidate_ids = _validate_candidate_rows(candidate_rows, catalog_ids, issues)
    snapshots = _load_price_snapshots(price_history_path, issues)
    portfolio_items = _load_portfolio_items(portfolio_path, issues)

    _validate_price_history(snapshots, catalog_ids, issues)
    _validate_portfolio_items(portfolio_items, catalog_ids, issues)

    priced_set_ids = {snapshot.set_id for snapshot in snapshots}
    portfolio_set_ids = {item.set_id for item in portfolio_items}
    snapshot_counts = Counter(snapshot.set_id for snapshot in snapshots)
    errors = [issue for issue in issues if issue.severity == "error"]
    warnings = [issue for issue in issues if issue.severity == "warning"]

    return {
        "ok": not errors,
        "errors": [asdict(issue) for issue in errors],
        "warnings": [asdict(issue) for issue in warnings],
        "metrics": {
            "catalog_sets": len(catalog_ids),
            "catalog_candidate_sets": len(candidate_ids),
            "catalog_plus_candidates": len(catalog_ids | candidate_ids),
            "target_catalog_sets": target_catalog_size,
            "price_snapshots": len(snapshots),
            "priced_sets": len(priced_set_ids),
            "portfolio_items": len(portfolio_items),
            "portfolio_sets": len(portfolio_set_ids),
            "sets_with_3_plus_snapshots": sum(
                1 for count in snapshot_counts.values() if count >= 3
            ),
            "sets_with_5_plus_snapshots": sum(
                1 for count in snapshot_counts.values() if count >= 5
            ),
            "unpriced_catalog_sets": sorted(catalog_ids - priced_set_ids),
        },
    }


def _load_catalog_rows(path: Path, issues: list[SeedDataIssue]) -> list[dict[str, str]]:
    try:
        with path.open(newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
    except OSError as exc:
        issues.append(
            SeedDataIssue("error", "CATALOG_READ_FAILED", f"Cannot read catalog: {exc}")
        )
        return []

    if not rows:
        issues.append(SeedDataIssue("error", "CATALOG_EMPTY", "Catalog CSV is empty."))
        return []

    missing_fields = [field for field in CATALOG_REQUIRED_FIELDS if field not in rows[0]]
    if missing_fields:
        issues.append(
            SeedDataIssue(
                "error",
                "CATALOG_COLUMNS_MISSING",
                f"Catalog is missing columns: {', '.join(missing_fields)}",
            )
        )

    return rows


def _validate_catalog_rows(
    rows: list[dict[str, str]],
    issues: list[SeedDataIssue],
    target_catalog_size: int,
) -> set[str]:
    catalog_ids: set[str] = set()
    seen_ids: set[str] = set()

    if len(rows) < target_catalog_size:
        issues.append(
            SeedDataIssue(
                "warning",
                "CATALOG_BELOW_TARGET",
                f"Catalog has {len(rows)} sets; guide target is {target_catalog_size}.",
            )
        )

    for row_number, row in enumerate(rows, start=2):
        set_id = row.get("set_id", "").strip()
        if not set_id:
            issues.append(
                SeedDataIssue(
                    "error",
                    "CATALOG_SET_ID_MISSING",
                    f"Catalog row {row_number} has no set_id.",
                )
            )
            continue

        if set_id in seen_ids:
            issues.append(
                SeedDataIssue(
                    "error",
                    "CATALOG_DUPLICATE_SET",
                    f"Catalog set {set_id} appears more than once.",
                )
            )
        seen_ids.add(set_id)
        catalog_ids.add(set_id)

        _require_text(row, row_number, set_id, "name", issues)
        _require_text(row, row_number, set_id, "theme", issues)
        _require_int(row, row_number, set_id, "year_released", issues, minimum=1949)
        _require_int(row, row_number, set_id, "year_retired", issues, minimum=1949)
        _require_float(row, row_number, set_id, "retail_price_eur", issues, minimum=0)
        _require_int(row, row_number, set_id, "pieces", issues, minimum=1)
        _require_int(row, row_number, set_id, "popularity_score", issues, minimum=0)

    return catalog_ids


def _load_candidate_rows(
    path: Path | None,
    issues: list[SeedDataIssue],
) -> list[dict[str, str]]:
    if path is None or not path.exists():
        return []

    try:
        with path.open(newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
    except OSError as exc:
        issues.append(
            SeedDataIssue(
                "error",
                "CATALOG_CANDIDATES_READ_FAILED",
                f"Cannot read catalog candidates: {exc}",
            )
        )
        return []

    if not rows:
        return []

    missing_fields = [field for field in CANDIDATE_REQUIRED_FIELDS if field not in rows[0]]
    if missing_fields:
        issues.append(
            SeedDataIssue(
                "error",
                "CATALOG_CANDIDATE_COLUMNS_MISSING",
                f"Catalog candidates missing columns: {', '.join(missing_fields)}",
            )
        )

    return rows


def _validate_candidate_rows(
    rows: list[dict[str, str]],
    catalog_ids: set[str],
    issues: list[SeedDataIssue],
) -> set[str]:
    candidate_ids: set[str] = set()

    for row_number, row in enumerate(rows, start=2):
        set_id = row.get("set_id", "").strip()
        if not set_id:
            issues.append(
                SeedDataIssue(
                    "error",
                    "CATALOG_CANDIDATE_SET_ID_MISSING",
                    f"Candidate row {row_number} has no set_id.",
                )
            )
            continue

        if set_id in candidate_ids:
            issues.append(
                SeedDataIssue(
                    "error",
                    "CATALOG_CANDIDATE_DUPLICATE_SET",
                    f"Candidate set {set_id} appears more than once.",
                )
            )

        if set_id in catalog_ids:
            issues.append(
                SeedDataIssue(
                    "error",
                    "CATALOG_CANDIDATE_ALREADY_ACTIVE",
                    f"Candidate set {set_id} already exists in active catalog.",
                )
            )

        candidate_ids.add(set_id)
        _require_text(row, row_number, set_id, "name", issues)
        _require_text(row, row_number, set_id, "theme", issues)
        _require_text(row, row_number, set_id, "reason", issues)
        _require_text(row, row_number, set_id, "validation_status", issues)

    return candidate_ids


def _load_price_snapshots(
    path: Path,
    issues: list[SeedDataIssue],
) -> list[PriceSnapshot]:
    raw_snapshots = _load_json_list(path, issues, "PRICE_HISTORY")
    snapshots: list[PriceSnapshot] = []

    for index, raw_snapshot in enumerate(raw_snapshots):
        try:
            snapshots.append(PriceSnapshot.model_validate(raw_snapshot))
        except ValidationError as exc:
            issues.append(
                SeedDataIssue(
                    "error",
                    "PRICE_HISTORY_INVALID_ROW",
                    f"Price history item {index} is invalid: {exc.errors()[0]['msg']}",
                )
            )

    return snapshots


def _load_portfolio_items(
    path: Path,
    issues: list[SeedDataIssue],
) -> list[PortfolioItem]:
    raw_items = _load_json_list(path, issues, "PORTFOLIO")
    items: list[PortfolioItem] = []

    for index, raw_item in enumerate(raw_items):
        try:
            items.append(PortfolioItem.model_validate(raw_item))
        except ValidationError as exc:
            issues.append(
                SeedDataIssue(
                    "error",
                    "PORTFOLIO_INVALID_ROW",
                    f"Portfolio item {index} is invalid: {exc.errors()[0]['msg']}",
                )
            )

    return items


def _validate_price_history(
    snapshots: list[PriceSnapshot],
    catalog_ids: set[str],
    issues: list[SeedDataIssue],
) -> None:
    seen_keys: set[tuple[str, str, str]] = set()
    for snapshot in snapshots:
        if snapshot.set_id not in catalog_ids:
            issues.append(
                SeedDataIssue(
                    "error",
                    "PRICE_UNKNOWN_SET",
                    f"Price history references unknown set {snapshot.set_id}.",
                )
            )

        if not snapshot.price_min_eur <= snapshot.price_avg_eur <= snapshot.price_max_eur:
            issues.append(
                SeedDataIssue(
                    "error",
                    "PRICE_BAND_INVALID",
                    f"Price band is invalid for {snapshot.set_id} {snapshot.condition}.",
                )
            )

        if snapshot.sample_count == 0:
            issues.append(
                SeedDataIssue(
                    "warning",
                    "PRICE_SAMPLE_COUNT_ZERO",
                    f"Price snapshot for {snapshot.set_id} has sample_count 0.",
                )
            )

        key = (snapshot.set_id, snapshot.condition, snapshot.recorded_at.isoformat())
        if key in seen_keys:
            issues.append(
                SeedDataIssue(
                    "error",
                    "PRICE_DUPLICATE_SNAPSHOT",
                    f"Duplicate price snapshot for {snapshot.set_id} on {snapshot.recorded_at}.",
                )
            )
        seen_keys.add(key)


def _validate_portfolio_items(
    items: list[PortfolioItem],
    catalog_ids: set[str],
    issues: list[SeedDataIssue],
) -> None:
    seen_ids: set[int] = set()
    for item in items:
        if item.id in seen_ids:
            issues.append(
                SeedDataIssue(
                    "error",
                    "PORTFOLIO_DUPLICATE_ID",
                    f"Portfolio item id {item.id} appears more than once.",
                )
            )
        seen_ids.add(item.id)

        if item.set_id not in catalog_ids:
            issues.append(
                SeedDataIssue(
                    "error",
                    "PORTFOLIO_UNKNOWN_SET",
                    f"Portfolio references unknown set {item.set_id}.",
                )
            )


def _load_json_list(path: Path, issues: list[SeedDataIssue], label: str) -> list[dict[str, Any]]:
    try:
        raw_data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(SeedDataIssue("error", f"{label}_READ_FAILED", str(exc)))
        return []

    if not isinstance(raw_data, list):
        issues.append(
            SeedDataIssue("error", f"{label}_NOT_LIST", f"{path.name} must contain a list.")
        )
        return []

    return raw_data


def _require_text(
    row: dict[str, str],
    row_number: int,
    set_id: str,
    field: str,
    issues: list[SeedDataIssue],
) -> None:
    if not row.get(field, "").strip():
        issues.append(
            SeedDataIssue(
                "error",
                "CATALOG_TEXT_MISSING",
                f"Catalog row {row_number} set {set_id} has empty {field}.",
            )
        )


def _require_int(
    row: dict[str, str],
    row_number: int,
    set_id: str,
    field: str,
    issues: list[SeedDataIssue],
    minimum: int,
) -> None:
    try:
        value = int(row.get(field, ""))
    except ValueError:
        issues.append(
            SeedDataIssue(
                "error",
                "CATALOG_INT_INVALID",
                f"Catalog row {row_number} set {set_id} has invalid {field}.",
            )
        )
        return

    if value < minimum:
        issues.append(
            SeedDataIssue(
                "error",
                "CATALOG_INT_TOO_SMALL",
                f"Catalog row {row_number} set {set_id} has {field} below {minimum}.",
            )
        )


def _require_float(
    row: dict[str, str],
    row_number: int,
    set_id: str,
    field: str,
    issues: list[SeedDataIssue],
    minimum: float,
) -> None:
    try:
        value = float(row.get(field, ""))
    except ValueError:
        issues.append(
            SeedDataIssue(
                "error",
                "CATALOG_FLOAT_INVALID",
                f"Catalog row {row_number} set {set_id} has invalid {field}.",
            )
        )
        return

    if value < minimum:
        issues.append(
            SeedDataIssue(
                "error",
                "CATALOG_FLOAT_TOO_SMALL",
                f"Catalog row {row_number} set {set_id} has {field} below {minimum}.",
            )
        )


def print_validation_report(report: dict[str, Any]) -> None:
    status = "OK" if report["ok"] else "FAILED"
    print(f"V2 seed data validation: {status}")
    for key, value in report["metrics"].items():
        print(f"{key}: {value}")

    for issue in report["warnings"]:
        print(f"WARNING {issue['code']}: {issue['message']}")

    for issue in report["errors"]:
        print(f"ERROR {issue['code']}: {issue['message']}")


if __name__ == "__main__":
    validation_report = validate_seed_data()
    print_validation_report(validation_report)
    raise SystemExit(0 if validation_report["ok"] else 1)
