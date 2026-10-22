import io
import time

import pytest
import requests

from src.capture import (
    ListingFetchError,
    UnsupportedListingURLError,
    fetch_html,
    validate_listing_url,
)
from src.pipeline import PipelineError, analyze_listing_url


PUBLIC_IP = "93.184.215.14"


@pytest.fixture
def public_dns(monkeypatch):
    monkeypatch.setattr("src.capture._resolve_host", lambda hostname: [PUBLIC_IP])


@pytest.fixture
def no_network(monkeypatch):
    def fail_get(*args, **kwargs):
        raise AssertionError("requests.get must not be called for a rejected URL")

    monkeypatch.setattr("src.capture.requests.get", fail_get)


def _response(status_code: int, body: bytes = b"", headers: dict | None = None) -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    response.raw = io.BytesIO(body)
    response.encoding = "utf-8"
    response.headers.update(headers or {})
    return response


@pytest.mark.parametrize(
    "url",
    [
        "https://www.ebay.es/itm/123",
        "https://ebay.es/itm/123",
        "https://es.wallapop.com/item/lego-75192",
        "https://www.vinted.es/items/123",
        "https://www.ebay.co.uk:443/itm/123",
    ],
)
def test_validate_listing_url_accepts_supported_marketplaces(url):
    assert validate_listing_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "http://www.ebay.es/itm/123",
        "ftp://www.ebay.es/itm/123",
        "file:///etc/passwd",
        "https://example.com/item/123",
        "https://ebay.es.evil.com/itm/123",
        "https://notebay.es/itm/123",
        "https://ebay.es@evil.com/",
        "https://user:pass@www.ebay.es/itm/123",
        "https://www.ebay.es\\@evil.com/",
        "https://www.ebay.es:8443/itm/123",
        "https://127.0.0.1/internal",
        "https://169.254.169.254/latest/meta-data/",
        "https://[::1]/internal",
        "https://www.ebay.es/itm/1 23",
        "https://www.ebay.es/itm/1\x00",
        "https://evil.com%40www.ebay.es/itm/123",
        "https://www.ebay.es%2F.evil.com/",
        "https://www.ebay\u3002es/itm/123",
        "https://www.ebay.es/" + "a" * 3000,
    ],
)
def test_fetch_html_rejects_unsupported_urls_without_network(url, no_network):
    with pytest.raises(UnsupportedListingURLError):
        fetch_html(url)


@pytest.mark.parametrize(
    "resolved",
    [
        ["127.0.0.1"],
        ["10.0.0.5"],
        ["192.168.1.10"],
        ["169.254.169.254"],
        ["100.64.0.1"],
        ["::1"],
        ["fd12::1"],
        ["::ffff:127.0.0.1"],
        [PUBLIC_IP, "10.0.0.5"],
    ],
)
def test_fetch_html_rejects_hosts_resolving_to_private_addresses(monkeypatch, no_network, resolved):
    monkeypatch.setattr("src.capture._resolve_host", lambda hostname: resolved)

    with pytest.raises(UnsupportedListingURLError):
        fetch_html("https://www.ebay.es/itm/123")


def test_fetch_html_downloads_allowed_listing(monkeypatch, public_dns):
    calls = []

    def fake_get(url, **kwargs):
        calls.append((url, kwargs))
        return _response(200, b"<html><h1>LEGO 75192</h1></html>")

    monkeypatch.setattr("src.capture.requests.get", fake_get)

    html = fetch_html("https://www.ebay.es/itm/123")

    assert "LEGO 75192" in html
    assert calls[0][1]["allow_redirects"] is False
    assert calls[0][1]["stream"] is True


def test_fetch_html_follows_redirects_within_allowlist(monkeypatch, public_dns):
    responses = {
        "https://ebay.es/itm/123": _response(301, headers={"Location": "https://www.ebay.es/itm/123"}),
        "https://www.ebay.es/itm/123": _response(200, b"<html><h1>LEGO 10221</h1></html>"),
    }
    monkeypatch.setattr("src.capture.requests.get", lambda url, **kwargs: responses[url])

    assert "LEGO 10221" in fetch_html("https://ebay.es/itm/123")


def test_fetch_html_rejects_cross_host_redirect(monkeypatch, public_dns):
    requested = []

    def fake_get(url, **kwargs):
        requested.append(url)
        return _response(302, headers={"Location": "https://evil.example/internal"})

    monkeypatch.setattr("src.capture.requests.get", fake_get)

    with pytest.raises(UnsupportedListingURLError):
        fetch_html("https://www.ebay.es/itm/123")

    assert requested == ["https://www.ebay.es/itm/123"]


def test_fetch_html_rejects_redirect_to_private_address(monkeypatch, no_network):
    monkeypatch.setattr(
        "src.capture._resolve_host",
        lambda hostname: ["10.0.0.7"] if hostname == "internal.ebay.es" else [PUBLIC_IP],
    )
    requested = []

    def fake_get(url, **kwargs):
        requested.append(url)
        return _response(302, headers={"Location": "https://internal.ebay.es/admin"})

    monkeypatch.setattr("src.capture.requests.get", fake_get)

    with pytest.raises(UnsupportedListingURLError):
        fetch_html("https://www.ebay.es/itm/123")

    assert requested == ["https://www.ebay.es/itm/123"]


def test_fetch_html_stops_after_too_many_redirects(monkeypatch, public_dns):
    monkeypatch.setattr(
        "src.capture.requests.get",
        lambda url, **kwargs: _response(302, headers={"Location": "https://www.ebay.es/loop"}),
    )

    with pytest.raises(ListingFetchError):
        fetch_html("https://www.ebay.es/itm/123")


def test_fetch_html_caps_response_size(monkeypatch, public_dns):
    monkeypatch.setenv("LRI_FETCH_MAX_BYTES", "1000")
    monkeypatch.setattr(
        "src.capture.requests.get",
        lambda url, **kwargs: _response(200, b"x" * 5000),
    )

    with pytest.raises(ListingFetchError):
        fetch_html("https://www.ebay.es/itm/123")


def test_fetch_html_enforces_total_deadline(monkeypatch, public_dns):
    monkeypatch.setenv("LRI_FETCH_TIMEOUT_SECONDS", "1")

    def slow_get(url, **kwargs):
        time.sleep(1.5)
        return _response(200, b"<html><h1>too late</h1></html>")

    monkeypatch.setattr("src.capture.requests.get", slow_get)

    started = time.monotonic()
    with pytest.raises(ListingFetchError):
        fetch_html("https://www.ebay.es/itm/123")

    assert time.monotonic() - started < 1.4


def test_fetch_errors_do_not_leak_network_details(monkeypatch, public_dns):
    def refused(url, **kwargs):
        raise requests.ConnectionError("HTTPSConnectionPool(host='10.1.2.3', port=443): refused")

    monkeypatch.setattr("src.capture.requests.get", refused)

    with pytest.raises(PipelineError) as raised:
        analyze_listing_url("https://www.ebay.es/itm/123")

    assert str(raised.value) == "No se pudo descargar el HTML del listing."
    assert "10.1.2.3" not in str(raised.value)


def test_pipeline_lets_unsupported_url_errors_through(no_network):
    with pytest.raises(UnsupportedListingURLError):
        analyze_listing_url("http://127.0.0.1:8000/internal")
