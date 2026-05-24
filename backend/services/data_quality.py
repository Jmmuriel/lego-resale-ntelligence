import csv
import json
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel

from scripts.v2_validate_seed_data import CATALOG_CANDIDATES_PATH, validate_seed_data


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CATALOG_RESEARCH_PATH = PROJECT_ROOT / "data" / "catalog_candidate_research.json"
CATALOG_ACTIVE_RESEARCH_PATH = PROJECT_ROOT / "data" / "catalog_active_research.json"
IssueSeverity = Literal["error", "warning"]
REQUIRED_RESEARCH_CHECKS = {
    "year_released": "release year",
    "year_retired": "retirement year",
    "retail_price_eur": "retail price",
    "pieces": "piece count",
    "popularity_score": "popularity score",
    "metadata_sources": "2 metadata sources",
    "price_sources": "2 price sources",
    "price_snapshots": "3 price snapshots",
}


class DataQualityIssue(BaseModel):
    """One data quality issue from the V2 seed validation gate."""

    severity: IssueSeverity
    code: str
    message: str


class DataQualityMetrics(BaseModel):
    """Coverage metrics for active and candidate V2 market data."""

    catalog_sets: int
    catalog_candidate_sets: int
    catalog_plus_candidates: int
    target_catalog_sets: int
    price_snapshots: int
    priced_sets: int
    candidate_ready_for_promotion: int
    portfolio_items: int
    portfolio_sets: int
    sets_with_3_plus_snapshots: int
    sets_with_5_plus_snapshots: int
    unpriced_catalog_sets: list[str]
    active_catalog_coverage_pct: float
    candidate_catalog_coverage_pct: float
    pricing_coverage_pct: float
    active_catalog_verified_sets: int
    active_catalog_verified_pct: float
    active_catalog_evidence_started_sets: int
    active_catalog_blocked_sets: int
    market_data_source_status: Literal["seed_demo", "partially_verified", "verified"]


class DataQualityReport(BaseModel):
    """API-ready report for V2 data maturity."""

    ok: bool
    status: Literal["ready", "needs_research", "blocked"]
    summary: str
    metrics: DataQualityMetrics
    warnings: list[DataQualityIssue]
    errors: list[DataQualityIssue]


class CandidateReadiness(BaseModel):
    """Research checklist status before a candidate can become active data."""

    completed_checks: int
    required_checks: int
    ready_for_promotion: bool
    missing_requirements: list[str]
    metadata_source_count: int
    price_source_count: int
    price_snapshot_count: int


class CatalogCandidate(BaseModel):
    """One set queued for manual research before activation."""

    set_id: str
    name: str
    theme: str
    reason: str
    validation_status: str
    readiness: CandidateReadiness


class ActiveCatalogEvidence(BaseModel):
    """External evidence status for an active catalog set."""

    set_id: str
    name: str
    theme: str | None = None
    verification_status: str
    audited_at: str | None = None
    audit_summary: str
    recommended_action: str | None = None
    catalog_mismatches: list[dict[str, Any]]
    metadata_source_count: int
    price_source_count: int
    price_snapshot_count: int
    ready_for_verified: bool
    missing_requirements: list[str]


def get_data_quality_report() -> DataQualityReport:
    """Return an API-ready V2 seed data quality report."""
    report = validate_seed_data()
    raw_metrics = report["metrics"]
    readiness_index = get_candidate_readiness_index()
    active_evidence_index = get_active_catalog_evidence_index()
    catalog_sets = raw_metrics["catalog_sets"]
    candidate_total = raw_metrics["catalog_plus_candidates"]
    target = raw_metrics["target_catalog_sets"]
    priced_sets = raw_metrics["priced_sets"]
    active_verified_sets = sum(
        readiness.ready_for_promotion for readiness in active_evidence_index.values()
    )
    source_status = _build_market_data_source_status(active_verified_sets, catalog_sets)

    errors = [DataQualityIssue.model_validate(issue) for issue in report["errors"]]
    warnings = [DataQualityIssue.model_validate(issue) for issue in report["warnings"]]
    if catalog_sets and active_verified_sets < catalog_sets:
        warnings.append(
            DataQualityIssue(
                severity="warning",
                code="ACTIVE_CATALOG_UNVERIFIED",
                message=(
                    f"External evidence covers {active_verified_sets}/{catalog_sets} active sets; "
                    "treat current market data as seed/demo until verified."
                ),
            )
        )
    status: Literal["ready", "needs_research", "blocked"]
    if errors:
        status = "blocked"
    elif candidate_total >= target and catalog_sets < target:
        status = "needs_research"
    else:
        status = "ready"

    metrics = DataQualityMetrics(
        **raw_metrics,
        candidate_ready_for_promotion=sum(
            readiness.ready_for_promotion for readiness in readiness_index.values()
        ),
        active_catalog_coverage_pct=_pct(catalog_sets, target),
        candidate_catalog_coverage_pct=_pct(candidate_total, target),
        pricing_coverage_pct=_pct(priced_sets, catalog_sets),
        active_catalog_verified_sets=active_verified_sets,
        active_catalog_verified_pct=_pct(active_verified_sets, catalog_sets),
        active_catalog_evidence_started_sets=len(active_evidence_index),
        active_catalog_blocked_sets=max(
            len(active_evidence_index) - active_verified_sets,
            0,
        ),
        market_data_source_status=source_status,
    )

    return DataQualityReport(
        ok=report["ok"],
        status=status,
        summary=_build_summary(status, metrics),
        metrics=metrics,
        warnings=warnings,
        errors=errors,
    )


def list_catalog_candidates(
    research_path: Path = CATALOG_RESEARCH_PATH,
) -> list[CatalogCandidate]:
    """Return catalog expansion candidates that still need manual validation."""
    readiness_index = get_candidate_readiness_index(research_path)

    with CATALOG_CANDIDATES_PATH.open(newline="", encoding="utf-8") as file:
        rows = csv.DictReader(file)
        return [
            CatalogCandidate(
                set_id=row["set_id"],
                name=row["name"],
                theme=row["theme"],
                reason=row["reason"],
                validation_status=row["validation_status"],
                readiness=readiness_index.get(
                    row["set_id"], _build_candidate_readiness({})
                ),
            )
            for row in rows
        ]


def list_active_catalog_evidence(
    research_path: Path = CATALOG_ACTIVE_RESEARCH_PATH,
) -> list[ActiveCatalogEvidence]:
    """Return audit evidence already collected for active catalog sets."""
    research_entries = _load_research_entries(research_path, collection_key="active_sets")
    evidence_log: list[ActiveCatalogEvidence] = []

    for set_id, entry in sorted(research_entries.items()):
        readiness = _build_candidate_readiness(entry, require_verified_status=True)
        evidence_log.append(
            ActiveCatalogEvidence(
                set_id=set_id,
                name=str(entry.get("name", "")),
                theme=_optional_text(entry.get("theme")),
                verification_status=str(entry.get("verification_status", "not_started")),
                audited_at=_optional_text(entry.get("audited_at")),
                audit_summary=str(entry.get("audit_summary", "")),
                recommended_action=_optional_text(entry.get("recommended_action")),
                catalog_mismatches=_list_of_dicts(entry.get("catalog_mismatches")),
                metadata_source_count=readiness.metadata_source_count,
                price_source_count=readiness.price_source_count,
                price_snapshot_count=readiness.price_snapshot_count,
                ready_for_verified=readiness.ready_for_promotion,
                missing_requirements=readiness.missing_requirements,
            )
        )

    return evidence_log


def get_candidate_readiness_index(
    research_path: Path = CATALOG_RESEARCH_PATH,
) -> dict[str, CandidateReadiness]:
    """Return promotion readiness by candidate set id."""
    research_entries = _load_research_entries(research_path, collection_key="candidates")
    return {
        set_id: _build_candidate_readiness(entry)
        for set_id, entry in research_entries.items()
    }


def get_active_catalog_evidence_index(
    research_path: Path = CATALOG_ACTIVE_RESEARCH_PATH,
) -> dict[str, CandidateReadiness]:
    """Return external evidence readiness by active catalog set id."""
    research_entries = _load_research_entries(research_path, collection_key="active_sets")
    return {
        set_id: _build_candidate_readiness(entry, require_verified_status=True)
        for set_id, entry in research_entries.items()
    }


def _pct(value: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((value / total) * 100, 1)


def _build_summary(status: str, metrics: DataQualityMetrics) -> str:
    if status == "blocked":
        return "Seed data has blocking errors and should not be loaded into the V2 database."

    if metrics.market_data_source_status == "seed_demo":
        return (
            "Seed data is technically ready for the local demo, but active catalog "
            "market data is not externally verified yet."
        )

    if metrics.market_data_source_status == "partially_verified":
        return (
            f"Seed data is technically ready; external evidence covers "
            f"{metrics.active_catalog_verified_sets}/{metrics.catalog_sets} active sets."
        )

    if status == "needs_research":
        return (
            f"{metrics.catalog_sets} active sets and {metrics.catalog_candidate_sets} candidates "
            f"cover the 50-set research target; candidates still need manual validation."
        )

    return "Seed data is ready for the current target."


def _load_research_entries(path: Path, collection_key: str) -> dict[str, dict[str, object]]:
    if not path.exists():
        return {}

    try:
        raw_data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}

    if isinstance(raw_data, dict):
        raw_entries = raw_data.get(collection_key, [])
    elif isinstance(raw_data, list):
        raw_entries = raw_data
    else:
        return {}

    if not isinstance(raw_entries, list):
        return {}

    entries: dict[str, dict[str, object]] = {}
    for raw_entry in raw_entries:
        if not isinstance(raw_entry, dict):
            continue
        set_id = str(raw_entry.get("set_id", "")).strip()
        if set_id:
            entries[set_id] = raw_entry
    return entries


def _build_candidate_readiness(
    entry: dict[str, object],
    require_verified_status: bool = False,
) -> CandidateReadiness:
    missing_requirements: list[str] = []
    completed_checks = 0

    for field, label in REQUIRED_RESEARCH_CHECKS.items():
        if _research_field_is_complete(field, entry.get(field)):
            completed_checks += 1
        else:
            missing_requirements.append(label)

    if require_verified_status:
        if entry.get("verification_status") == "verified":
            completed_checks += 1
        else:
            missing_requirements.append("verified evidence status")

    metadata_source_count = _list_count(entry.get("metadata_sources"))
    price_source_count = _list_count(entry.get("price_sources"))
    price_snapshot_count = _list_count(entry.get("price_snapshots"))
    required_checks = len(REQUIRED_RESEARCH_CHECKS) + int(require_verified_status)

    return CandidateReadiness(
        completed_checks=completed_checks,
        required_checks=required_checks,
        ready_for_promotion=completed_checks == required_checks,
        missing_requirements=missing_requirements,
        metadata_source_count=metadata_source_count,
        price_source_count=price_source_count,
        price_snapshot_count=price_snapshot_count,
    )


def _research_field_is_complete(field: str, value: object) -> bool:
    if field in {"metadata_sources", "price_sources"}:
        return _list_count(value) >= 2
    if field == "price_snapshots":
        return _list_count(value) >= 3
    if isinstance(value, (int, float)):
        return value > 0
    if isinstance(value, str):
        return bool(value.strip())
    return False


def _list_count(value: object) -> int:
    if not isinstance(value, list):
        return 0
    return len([item for item in value if item])


def _optional_text(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    return stripped or None


def _list_of_dicts(value: object) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _build_market_data_source_status(
    active_verified_sets: int,
    catalog_sets: int,
) -> Literal["seed_demo", "partially_verified", "verified"]:
    if catalog_sets <= 0 or active_verified_sets <= 0:
        return "seed_demo"
    if active_verified_sets >= catalog_sets:
        return "verified"
    return "partially_verified"
