from src.identify import find_set_by_id, find_set_by_title, identify_set, load_catalog
from src.models import CatalogSet


def test_load_catalog_returns_catalog_sets():
    catalog = load_catalog()

    assert catalog
    assert isinstance(catalog[0], CatalogSet)


def test_find_set_by_id_returns_exact_match():
    catalog = load_catalog()

    result = find_set_by_id("75192", catalog)

    assert result is not None
    assert result.name == "Millennium Falcon"


def test_load_catalog_includes_expanded_phase_2_sets():
    catalog = load_catalog()
    set_ids = {catalog_set.set_id for catalog_set in catalog}

    assert {"75252", "75313", "75059", "10030", "75095"}.issubset(set_ids)


def test_find_set_by_id_returns_none_for_unknown_set():
    catalog = load_catalog()

    result = find_set_by_id("00000", catalog)

    assert result is None


def test_find_set_by_title_returns_conservative_match():
    catalog = load_catalog()

    result = find_set_by_title("LEGO Star Wars Super Star Destroyer usado", catalog)

    assert result is not None
    assert result.set_id == "10221"


def test_find_set_by_title_returns_none_when_confidence_is_low():
    catalog = load_catalog()

    result = find_set_by_title("lote piezas sueltas varias", catalog)

    assert result is None


def test_identify_set_prefers_set_id_over_title():
    result = identify_set(
        set_id="21309",
        title="LEGO Star Wars Millennium Falcon",
    )

    assert result is not None
    assert result.set_id == "21309"


def test_identify_set_does_not_fallback_when_unknown_set_id_is_present():
    result = identify_set(
        set_id="00000",
        title="LEGO Star Wars Millennium Falcon",
    )

    assert result is None
