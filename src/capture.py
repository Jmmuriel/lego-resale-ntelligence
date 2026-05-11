import json
import re

import requests
from bs4 import BeautifulSoup

from src.models import ListingInput


REQUEST_TIMEOUT_SECONDS = 10
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}


def fetch_html(url: str) -> str:
    """Descarga el HTML de una única URL de listing."""
    if not url:
        raise ValueError("La URL no puede estar vacía.")

    try:
        response = requests.get(url, headers=BROWSER_HEADERS, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"No se pudo descargar el HTML del listing: {exc}") from exc

    return response.text


def detect_marketplace_from_url(url: str | None) -> str | None:
    """Detecta el marketplace a partir de la URL del listing."""
    if not url:
        return None

    url_lower = url.lower()

    if "ebay" in url_lower:
        return "ebay"
    if "wallapop" in url_lower:
        return "wallapop"
    if "vinted" in url_lower:
        return "vinted"

    return "unknown"


def parse_listing_html(html: str, url: str | None = None) -> ListingInput:
    """Convierte HTML básico de un listing en un ListingInput."""
    soup = BeautifulSoup(html or "", "html.parser")

    return ListingInput(
        url=url,
        marketplace=detect_marketplace_from_url(url),
        raw_title=_extract_title(soup),
        raw_description=_extract_description(soup),
        asking_price_eur=_extract_asking_price(soup),
        shipping_eur=_extract_shipping_price(soup),
    )


def _extract_title(soup: BeautifulSoup) -> str | None:
    structured_name = _json_ld_value(soup, "name")
    if structured_name and not _is_generic_title(structured_name):
        return structured_name

    meta_title = _meta_content(soup, "property", "og:title")
    if meta_title and not _is_generic_title(meta_title):
        return meta_title

    title_selectors = [
        "h1",
        "[data-testid*='title']",
        "[class*='title']",
        "[id*='title']",
    ]

    text = _first_text_from_selectors(soup, title_selectors)
    if text and not _is_generic_title(text):
        return text

    if soup.title and soup.title.string:
        page_title = _clean_text(soup.title.string)
        if page_title and not _is_generic_title(page_title):
            return page_title

    return None


def _extract_description(soup: BeautifulSoup) -> str | None:
    structured_description = _json_ld_value(soup, "description")
    if structured_description:
        return structured_description

    description_selectors = [
        "[itemprop='description']",
        "[data-testid*='description']",
        "[class*='description']",
        "[id*='description']",
    ]

    text = _first_text_from_selectors(soup, description_selectors)
    if text:
        return text

    return _meta_content(soup, "name", "description")


def _extract_asking_price(soup: BeautifulSoup) -> float | None:
    structured_price = _parse_price(_json_ld_value(soup, "price"))
    if structured_price is not None:
        return structured_price

    price_selectors = [
        "[itemprop='price']",
        "[data-testid*='price']",
        "[class*='price']",
        "[id*='price']",
    ]

    for selector in price_selectors:
        for element in soup.select(selector):
            content = element.get("content")
            price = _parse_price(content or element.get_text(" ", strip=True))
            if price is not None:
                return price

    for attr_name, attr_value in [
        ("property", "product:price:amount"),
        ("property", "og:price:amount"),
    ]:
        price = _parse_price(_meta_content(soup, attr_name, attr_value))
        if price is not None:
            return price

    return None


def _extract_shipping_price(soup: BeautifulSoup) -> float | None:
    page_text = soup.get_text(" ", strip=True)
    shipping_patterns = [
        r"(env[ií]o|shipping)[^€$]{0,40}(gratis|free)",
        r"(?:env[ií]o|shipping)\s*(?:a domicilio|standard|est[aá]ndar)?\s*:?\s*([€$]?\s*\d+(?:[.,]\d{1,2})?\s*(?:€|eur)?)",
    ]

    for pattern in shipping_patterns:
        match = re.search(pattern, page_text, flags=re.IGNORECASE)
        if not match:
            continue

        captured_value = match.group(1)
        if captured_value.lower() in {"envío", "envio", "shipping"}:
            captured_value = match.group(2)

        if captured_value.lower() in {"gratis", "free"}:
            return 0.0

        return _parse_price(captured_value)

    return None


def _first_text_from_selectors(soup: BeautifulSoup, selectors: list[str]) -> str | None:
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            text = _clean_text(element.get_text(" ", strip=True))
            if text:
                return text

    return None


def _meta_content(soup: BeautifulSoup, attr_name: str, attr_value: str) -> str | None:
    element = soup.find("meta", attrs={attr_name: attr_value})
    if not element:
        return None

    return _clean_text(element.get("content"))


def _json_ld_value(soup: BeautifulSoup, key: str) -> str | None:
    """Lee valores simples desde JSON-LD cuando el marketplace los expone."""
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        if not script.string:
            continue

        try:
            data = json.loads(script.string)
        except json.JSONDecodeError:
            continue

        value = _find_key_in_json(data, key)
        if value is not None:
            return _clean_text(str(value))

    return None


def _find_key_in_json(data: object, key: str) -> object | None:
    """Busca una clave en una estructura JSON sencilla sin asumir un formato único."""
    if isinstance(data, dict):
        if key in data:
            return data[key]

        offers = data.get("offers")
        if key == "price" and isinstance(offers, dict) and "price" in offers:
            return offers["price"]

        for value in data.values():
            found = _find_key_in_json(value, key)
            if found is not None:
                return found

    if isinstance(data, list):
        for item in data:
            found = _find_key_in_json(item, key)
            if found is not None:
                return found

    return None


def _is_generic_title(value: str) -> bool:
    """Evita títulos de navegación que algunos marketplaces ponen en el HTML."""
    normalized = value.strip().lower()
    generic_titles = {
        "todas las categorías",
        "todas las categorias",
        "wallapop",
        "ebay",
        "vinted",
    }
    return normalized in generic_titles


def _clean_text(value: str | None) -> str | None:
    if value is None:
        return None

    text = " ".join(value.split())
    return text or None


def _parse_price(value: str | None) -> float | None:
    if not value:
        return None

    match = re.search(
        r"(?:€|eur)?\s*(\d{1,6}(?:[.,]\d{1,2})?)\s*(?:€|eur)?",
        value,
        flags=re.IGNORECASE,
    )
    if not match:
        return None

    normalized = match.group(1).replace(",", ".")
    return round(float(normalized), 2)
