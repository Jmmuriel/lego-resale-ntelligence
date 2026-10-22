import ipaddress
import json
import logging
import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeoutError
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup

from src.limits import env_int
from src.models import ListingInput


log = logging.getLogger(__name__)

REQUEST_TIMEOUT_SECONDS = 10
CONNECT_TIMEOUT_SECONDS = 5
DEFAULT_FETCH_DEADLINE_SECONDS = 15
DEFAULT_FETCH_MAX_BYTES = 2_000_000
MAX_REDIRECTS = 3
MAX_URL_LENGTH = 2048
READ_CHUNK_BYTES = 64 * 1024
HOSTNAME_PATTERN = re.compile(r"^[a-z0-9-]+(\.[a-z0-9-]+)+$")

# Only the marketplaces the analyzer supports. A host matches when it equals one
# of these domains or ends with "." + domain (www.ebay.es, es.wallapop.com...).
ALLOWED_LISTING_DOMAINS = (
    "ebay.es",
    "ebay.com",
    "ebay.co.uk",
    "ebay.de",
    "ebay.fr",
    "ebay.it",
    "ebay.nl",
    "ebay.be",
    "ebay.at",
    "ebay.ie",
    "ebay.ch",
    "ebay.pl",
    "wallapop.com",
    "vinted.es",
    "vinted.com",
    "vinted.fr",
    "vinted.it",
    "vinted.de",
    "vinted.co.uk",
    "vinted.pt",
    "vinted.nl",
    "vinted.be",
    "vinted.at",
    "vinted.pl",
)

UNSUPPORTED_URL_MESSAGE = "Solo se pueden analizar URLs https de listings de eBay, Wallapop o Vinted."
FETCH_ERROR_MESSAGE = "No se pudo descargar el HTML del listing."

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}

# Bounded pool so a slow marketplace cannot pile up threads; the caller stops
# waiting at the deadline even if a worker is still blocked on a socket read.
_FETCH_EXECUTOR = ThreadPoolExecutor(max_workers=4, thread_name_prefix="listing-fetch")


class UnsupportedListingURLError(ValueError):
    """The URL is not an https listing on a supported marketplace, or points to a non-public address."""

    def __init__(self) -> None:
        super().__init__(UNSUPPORTED_URL_MESSAGE)


class ListingFetchError(RuntimeError):
    """The listing could not be downloaded. The message is safe to show to users."""

    def __init__(self) -> None:
        super().__init__(FETCH_ERROR_MESSAGE)


def fetch_html(url: str) -> str:
    """Descarga el HTML de una única URL de listing de un marketplace soportado.

    Solo acepta https en el puerto 443 hacia hosts de ALLOWED_LISTING_DOMAINS que
    resuelvan a IPs públicas. Valida cada redirección, corta la descarga al pasar
    de LRI_FETCH_MAX_BYTES y deja de esperar a los LRI_FETCH_TIMEOUT_SECONDS.
    """
    if not url:
        raise ValueError("La URL no puede estar vacía.")

    validate_listing_url(url)
    timeout_seconds = env_int("LRI_FETCH_TIMEOUT_SECONDS", DEFAULT_FETCH_DEADLINE_SECONDS, minimum=1)
    deadline = time.monotonic() + timeout_seconds
    future = _FETCH_EXECUTOR.submit(_download_listing, url, deadline)
    try:
        return future.result(timeout=timeout_seconds)
    except FutureTimeoutError as exc:
        future.cancel()
        log.warning("Listing fetch exceeded the %ss deadline", timeout_seconds)
        raise ListingFetchError() from exc


def validate_listing_url(url: str) -> str:
    """Comprueba la URL sin tocar la red y devuelve el hostname normalizado."""
    if (
        len(url) > MAX_URL_LENGTH
        or "\\" in url
        or any(char.isspace() or not char.isprintable() for char in url)
    ):
        raise UnsupportedListingURLError()

    try:
        parts = urlsplit(url)
        port = parts.port
    except ValueError as exc:
        raise UnsupportedListingURLError() from exc

    if parts.scheme != "https" or "@" in parts.netloc or port not in (None, 443):
        raise UnsupportedListingURLError()

    hostname = (parts.hostname or "").rstrip(".")
    if not HOSTNAME_PATTERN.match(hostname) or _is_ip_literal(hostname):
        raise UnsupportedListingURLError()

    if not any(hostname == domain or hostname.endswith(f".{domain}") for domain in ALLOWED_LISTING_DOMAINS):
        raise UnsupportedListingURLError()

    return hostname


def _download_listing(url: str, deadline: float) -> str:
    current_url = url
    for _ in range(MAX_REDIRECTS + 1):
        hostname = validate_listing_url(current_url)
        _ensure_public_host(hostname)

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise ListingFetchError()

        try:
            response = requests.get(
                current_url,
                headers=BROWSER_HEADERS,
                timeout=(
                    min(CONNECT_TIMEOUT_SECONDS, remaining),
                    min(REQUEST_TIMEOUT_SECONDS, remaining),
                ),
                allow_redirects=False,
                stream=True,
            )
        except requests.RequestException as exc:
            log.warning("Listing fetch failed for host %s: %s", hostname, exc)
            raise ListingFetchError() from exc

        with response:
            if response.is_redirect:
                current_url = urljoin(current_url, response.headers["location"])
                continue

            try:
                response.raise_for_status()
                return _read_capped_text(response, deadline)
            except requests.RequestException as exc:
                log.warning("Listing fetch failed for host %s: %s", hostname, exc)
                raise ListingFetchError() from exc

    log.warning("Listing fetch stopped after %s redirects", MAX_REDIRECTS)
    raise ListingFetchError()


def _read_capped_text(response: requests.Response, deadline: float) -> str:
    max_bytes = env_int("LRI_FETCH_MAX_BYTES", DEFAULT_FETCH_MAX_BYTES, minimum=1)
    body = bytearray()
    # iter_content yields decompressed bytes, so the cap also stops gzip bombs.
    for chunk in response.iter_content(chunk_size=READ_CHUNK_BYTES):
        body.extend(chunk)
        if len(body) > max_bytes:
            log.warning("Listing response exceeded %s bytes", max_bytes)
            raise ListingFetchError()
        if time.monotonic() > deadline:
            raise ListingFetchError()

    encoding = response.encoding or "utf-8"
    try:
        return body.decode(encoding, errors="replace")
    except LookupError:
        return body.decode("utf-8", errors="replace")


def _ensure_public_host(hostname: str) -> None:
    """Rechaza hosts que resuelven a IPs privadas, loopback, link-local o reservadas."""
    try:
        addresses = _resolve_host(hostname)
    except (OSError, UnicodeError) as exc:
        log.warning("Could not resolve listing host %s: %s", hostname, exc)
        raise ListingFetchError() from exc

    if not addresses:
        raise ListingFetchError()

    for address in addresses:
        ip = ipaddress.ip_address(address.split("%", 1)[0])
        if ip.version == 6 and ip.ipv4_mapped is not None:
            ip = ip.ipv4_mapped
        if not ip.is_global or ip.is_multicast:
            log.warning("Blocked listing host %s resolving to non-public address %s", hostname, ip)
            raise UnsupportedListingURLError()


def _resolve_host(hostname: str) -> list[str]:
    infos = socket.getaddrinfo(hostname, 443, type=socket.SOCK_STREAM)
    return [str(info[4][0]) for info in infos]


def _is_ip_literal(hostname: str) -> bool:
    try:
        ipaddress.ip_address(hostname)
    except ValueError:
        return False
    return True


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
