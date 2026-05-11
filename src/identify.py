import csv
import re
from pathlib import Path

from src.models import CatalogSet


DEFAULT_CATALOG_PATH = Path(__file__).resolve().parents[1] / "data" / "catalog.csv"
MIN_TITLE_MATCH_SCORE = 0.6
IGNORED_TITLE_TOKENS = {
    "lego",
    "set",
    "nuevo",
    "usado",
    "used",
    "complete",
    "completo",
    "completa",
    "sealed",
}


def load_catalog(catalog_path: str | Path = DEFAULT_CATALOG_PATH) -> list[CatalogSet]:
    """Carga el catálogo local de sets retirados desde CSV."""
    path = Path(catalog_path)
    if not path.exists():
        raise FileNotFoundError(f"No existe el catálogo local: {path}")

    with path.open(newline="", encoding="utf-8") as file:
        rows = csv.DictReader(file)
        return [_catalog_set_from_row(row) for row in rows]


def find_set_by_id(set_id: str | None, catalog: list[CatalogSet]) -> CatalogSet | None:
    """Busca un set por ID exacto dentro del catálogo."""
    if not set_id:
        return None

    clean_set_id = set_id.strip()
    for catalog_set in catalog:
        if catalog_set.set_id == clean_set_id:
            return catalog_set

    return None


def find_set_by_title(title: str | None, catalog: list[CatalogSet]) -> CatalogSet | None:
    """Busca un set por coincidencia conservadora de tokens del título."""
    title_tokens = _meaningful_tokens(title)
    if not title_tokens:
        return None

    best_match = None
    best_score = 0.0

    for catalog_set in catalog:
        name_tokens = _meaningful_tokens(catalog_set.name)
        if not name_tokens:
            continue

        score = len(title_tokens & name_tokens) / len(name_tokens)
        if score > best_score:
            best_score = score
            best_match = catalog_set

    if best_score >= MIN_TITLE_MATCH_SCORE:
        return best_match

    return None


def identify_set(
    set_id: str | None = None,
    title: str | None = None,
    catalog_path: str | Path = DEFAULT_CATALOG_PATH,
) -> CatalogSet | None:
    """Identifica un set usando primero set_id y luego fallback por título."""
    catalog = load_catalog(catalog_path)

    clean_set_id = set_id.strip() if set_id else None
    if clean_set_id:
        return find_set_by_id(clean_set_id, catalog)

    return find_set_by_title(title, catalog)


def _catalog_set_from_row(row: dict[str, str]) -> CatalogSet:
    """Convierte una fila cruda del CSV en un CatalogSet validado."""
    return CatalogSet(
        set_id=row["set_id"],
        name=row["name"],
        theme=row["theme"],
        year_released=int(row["year_released"]),
        year_retired=int(row["year_retired"]),
        retail_price_eur=float(row["retail_price_eur"]),
        pieces=int(row["pieces"]),
        popularity_score=int(row["popularity_score"]),
    )


def _meaningful_tokens(text: str | None) -> set[str]:
    """Obtiene tokens simples para matching conservador por nombre."""
    if not text:
        return set()

    tokens = {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if len(token) >= 3
    }

    return tokens - IGNORED_TITLE_TOKENS
