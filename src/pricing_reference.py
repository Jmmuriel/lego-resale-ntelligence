PRICE_REFERENCES_EUR = {
    "75192": {
        "SEALED": 880.0,
        "USED_COMPLETE": 720.0,
        "USED_INCOMPLETE": 560.0,
        "UNKNOWN": 660.0,
    },
    "10221": {
        "SEALED": 650.0,
        "USED_COMPLETE": 430.0,
        "USED_INCOMPLETE": 310.0,
        "UNKNOWN": 390.0,
    },
    "21309": {
        "SEALED": 135.0,
        "USED_COMPLETE": 95.0,
        "USED_INCOMPLETE": 70.0,
        "UNKNOWN": 85.0,
    },
    "10179": {
        "SEALED": 2300.0,
        "USED_COMPLETE": 1100.0,
        "USED_INCOMPLETE": 850.0,
        "UNKNOWN": 1000.0,
    },
    "10214": {
        "SEALED": 280.0,
        "USED_COMPLETE": 180.0,
        "USED_INCOMPLETE": 130.0,
        "UNKNOWN": 160.0,
    },
    "75252": {
        "SEALED": 1200.0,
        "USED_COMPLETE": 740.0,
        "USED_INCOMPLETE": 560.0,
        "UNKNOWN": 700.0,
    },
    "75313": {
        "SEALED": 1200.0,
        "USED_COMPLETE": 760.0,
        "USED_INCOMPLETE": 600.0,
        "UNKNOWN": 720.0,
    },
    "75059": {
        "SEALED": 600.0,
        "USED_COMPLETE": 380.0,
        "USED_INCOMPLETE": 280.0,
        "UNKNOWN": 340.0,
    },
    "10030": {
        "SEALED": 1450.0,
        "USED_COMPLETE": 740.0,
        "USED_INCOMPLETE": 560.0,
        "UNKNOWN": 700.0,
    },
    "75095": {
        "SEALED": 340.0,
        "USED_COMPLETE": 260.0,
        "USED_INCOMPLETE": 190.0,
        "UNKNOWN": 240.0,
    },
}


def get_fair_price(set_id: str | None, condition: str | None = None) -> float | None:
    """Devuelve el precio justo manual para un set y una condición."""
    if not set_id:
        return None

    set_reference = PRICE_REFERENCES_EUR.get(set_id)
    if not set_reference:
        return None

    condition_key = condition or "UNKNOWN"
    fair_price = set_reference.get(condition_key)
    if fair_price is not None:
        return fair_price

    return set_reference.get("UNKNOWN")


def has_reference(set_id: str | None) -> bool:
    """Indica si existe una referencia manual para el set."""
    if not set_id:
        return False

    return set_id in PRICE_REFERENCES_EUR
