from src.pricing_reference import get_fair_price, has_reference


def test_get_fair_price_with_known_set_and_known_condition():
    fair_price = get_fair_price("75192", "USED_COMPLETE")

    assert fair_price == 720.0


def test_get_fair_price_with_none_condition_uses_unknown():
    fair_price = get_fair_price("10221")

    assert fair_price == 390.0


def test_get_fair_price_with_unknown_set_returns_none():
    fair_price = get_fair_price("00000", "SEALED")

    assert fair_price is None


def test_has_reference_with_known_set():
    assert has_reference("21309") is True


def test_has_reference_for_expanded_phase_2_sets():
    assert has_reference("75252") is True
    assert has_reference("75313") is True
    assert has_reference("75095") is True


def test_get_fair_price_for_expanded_phase_2_set():
    fair_price = get_fair_price("75313", "USED_COMPLETE")

    assert fair_price == 760.0


def test_has_reference_with_unknown_set():
    assert has_reference("00000") is False
