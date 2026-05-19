import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.data_quality import list_catalog_candidates


def check_candidate_readiness(set_id: str | None = None) -> int:
    """Print the manual research gate status for candidate promotion."""
    candidates = list_catalog_candidates()
    selected = [
        candidate
        for candidate in candidates
        if set_id is None or candidate.set_id == set_id
    ]

    if set_id is not None and not selected:
        print(f"Candidate {set_id} was not found in the research queue.")
        return 1

    ready = [candidate for candidate in selected if candidate.readiness.ready_for_promotion]
    blocked = [candidate for candidate in selected if not candidate.readiness.ready_for_promotion]

    print("V2 candidate promotion readiness")
    print(f"checked_candidates: {len(selected)}")
    print(f"ready_for_promotion: {len(ready)}")
    print(f"blocked: {len(blocked)}")

    for candidate in blocked[:10]:
        missing = ", ".join(candidate.readiness.missing_requirements)
        print(f"BLOCKED {candidate.set_id} {candidate.name}: missing {missing}")

    if len(blocked) > 10:
        print(f"...and {len(blocked) - 10} more blocked candidates")

    return 0 if not blocked else 2


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether V2 catalog candidates have enough evidence to promote."
    )
    parser.add_argument("set_id", nargs="?", help="Optional LEGO set number to check.")
    args = parser.parse_args()
    return check_candidate_readiness(args.set_id)


if __name__ == "__main__":
    raise SystemExit(main())
