import asyncio
import json
from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

import backend.services.portfolio_engine as portfolio_engine
from backend.main import app, create_app
from backend.services.portfolio_engine import PortfolioItem
from src.limits import LLMBudgetExceeded, reserve_llm_call
from src.models import ListingAnalysis
from src.pipeline import PipelineError, analyze_listing_url


READ_ONLY = {"detail": "This public demo is read-only."}
VALID_POSITION = {
    "set_id": "75192",
    "set_name": "Millennium Falcon (UCS)",
    "condition": "USED_COMPLETE",
    "quantity": 1,
    "cost_basis_eur": 585.0,
    "purchased_at": "2026-02-10",
}
VALID_ANALYSIS = {
    "url": "https://www.ebay.es/itm/lego-75192",
    "marketplace": "ebay",
    "set_id": "75192",
    "condition": "USED_COMPLETE",
    "asking_price_eur": 560.0,
    "fair_price_eur": 720.0,
    "opportunity_score": 72,
    "category": "GREEN",
    "risk_flags": [],
}


def _fail(*args, **kwargs):
    raise AssertionError("a write must not reach the data layer while the demo is read-only")


@pytest.fixture
def blocked_writes(monkeypatch):
    for name in ("add_portfolio_item", "delete_portfolio_item"):
        monkeypatch.setattr(f"backend.routers.portfolio.{name}", _fail)
    for name in ("save_listing_analysis", "update_listing_status"):
        monkeypatch.setattr(f"backend.routers.watchlist.{name}", _fail)
    monkeypatch.setattr("backend.routers.briefings.generate_briefing", _fail)
    monkeypatch.setattr("backend.routers.briefings.generate_briefing_with_llm", _fail)


@pytest.fixture
def fake_add_position(monkeypatch):
    def fake(**fields):
        return PortfolioItem(id=99, status="HOLDING", **{k: v for k, v in fields.items() if k != "status"})

    monkeypatch.setattr("backend.routers.portfolio.add_portfolio_item", fake)


@pytest.fixture
def fake_pipeline(monkeypatch):
    def fake(url: str) -> ListingAnalysis:
        return ListingAnalysis(url=url, marketplace="ebay", set_id="75192", condition="USED_COMPLETE")

    monkeypatch.setattr("backend.routers.analyze.analyze_listing_url", fake)


@pytest.mark.parametrize(
    ("method", "path", "body"),
    [
        ("POST", "/api/portfolio", VALID_POSITION),
        ("DELETE", "/api/portfolio/1", None),
        ("POST", "/api/watchlist?listing_status=watching", VALID_ANALYSIS),
        ("PATCH", "/api/watchlist/1/status", {"status": "bought"}),
        ("POST", "/api/briefings/generate?use_llm=true", None),
    ],
)
def test_write_routes_are_read_only_by_default(blocked_writes, method, path, body):
    client = TestClient(app)

    response = client.request(method, path, json=body)

    assert response.status_code == 403
    assert response.json() == READ_ONLY


def test_read_only_check_runs_before_body_validation(blocked_writes):
    client = TestClient(app)

    response = client.post("/api/portfolio", json={"set_name": "x" * 10_000})

    assert response.status_code == 403
    assert response.json() == READ_ONLY


def test_oversized_body_is_refused_before_read_only_check(blocked_writes):
    client = TestClient(app)

    response = client.post(
        "/api/portfolio",
        content=b"{" + b" " * 70_000 + b"}",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 413
    assert response.json() == {"detail": "Request body too large."}


def test_body_size_limit_is_configurable(monkeypatch, allow_demo_writes, fake_add_position):
    client = TestClient(app)

    assert client.post("/api/portfolio", json=VALID_POSITION).status_code == 201

    monkeypatch.setenv("LRI_MAX_BODY_BYTES", "100")
    assert client.post("/api/portfolio", json=VALID_POSITION).status_code == 413


def test_chunked_body_is_cut_off_at_the_limit(monkeypatch):
    """A body without Content-Length is counted as it arrives and never fully read."""
    monkeypatch.setenv("LRI_MAX_BODY_BYTES", "1000")
    monkeypatch.setattr("backend.routers.analyze.analyze_listing_url", _fail)
    chunks_read = 0
    sent = []

    async def endless_body():
        nonlocal chunks_read
        chunks_read += 1
        return {"type": "http.request", "body": b" " * 400, "more_body": True}

    async def collect(message):
        sent.append(message)

    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": "/api/analyze",
        "raw_path": b"/api/analyze",
        "root_path": "",
        "query_string": b"",
        "headers": [(b"content-type", b"application/json"), (b"transfer-encoding", b"chunked")],
        "client": ("203.0.113.7", 50000),
        "server": ("testserver", 80),
    }

    asyncio.run(app(scope, endless_body, collect))

    start = next(message for message in sent if message["type"] == "http.response.start")
    body = b"".join(message.get("body", b"") for message in sent if message["type"] == "http.response.body")
    assert start["status"] == 413
    assert json.loads(body) == {"detail": "Request body too large."}
    assert chunks_read == 3


def test_read_routes_and_demo_analysis_stay_public():
    client = TestClient(app)

    assert client.get("/api/portfolio").status_code == 200
    assert client.get("/api/briefings").status_code == 200
    assert client.get("/api/market/trends?days=120").status_code == 200
    assert client.post("/api/analyze/demo").status_code == 200


def test_allow_writes_flag_enables_write_routes(allow_demo_writes, fake_add_position):
    client = TestClient(app)

    response = client.post("/api/portfolio", json=VALID_POSITION)

    assert response.status_code == 201
    assert response.json()["set_id"] == "75192"


@pytest.mark.parametrize(
    "override",
    [
        {"set_id": "<img src=x onerror=alert(1)>"},
        {"set_name": "x" * 121},
        {"set_name": ""},
        {"condition": "<script>"},
        {"quantity": 999_999_999},
        {"quantity": 0},
        {"cost_basis_eur": 1e308},
        {"cost_basis_eur": float("inf")},
        {"notes": "x" * 501},
        {"sell_target_eur": 1_000_000},
        {"purchased_at": "0001-01-01"},
        {"purchased_at": "2999-01-01"},
    ],
)
def test_add_position_rejects_out_of_bounds_input(allow_demo_writes, fake_add_position, override):
    client = TestClient(app)

    response = client.post(
        "/api/portfolio",
        content=json.dumps({**VALID_POSITION, **override}),
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "override",
    [
        {"url": "https://www.ebay.es/" + "a" * 3000},
        {"notes": "x" * 1001},
        {"risk_flags": ["flag"] * 21},
        {"risk_flags": ["x" * 121]},
        {"fair_price_eur": 999_999},
        {"opportunity_score": 101},
    ],
)
def test_watchlist_rejects_out_of_bounds_input(allow_demo_writes, monkeypatch, override):
    monkeypatch.setattr("backend.routers.watchlist.save_listing_analysis", _fail)
    client = TestClient(app)

    response = client.post("/api/watchlist", json={**VALID_ANALYSIS, **override})

    assert response.status_code == 422


def test_watchlist_rejects_unknown_status(allow_demo_writes, monkeypatch):
    monkeypatch.setattr("backend.routers.watchlist.update_listing_status", _fail)
    client = TestClient(app)

    response = client.patch("/api/watchlist/1/status", json={"status": "hacked"})

    assert response.status_code == 422


def test_portfolio_json_fallback_never_writes_while_read_only(monkeypatch, tmp_path):
    seed_path = tmp_path / "portfolio_seed.json"
    seed_path.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(portfolio_engine, "DEFAULT_PORTFOLIO_PATH", seed_path)

    def broken_session_factory(*args, **kwargs):
        raise OperationalError("SELECT 1", {}, Exception("no such table"))

    monkeypatch.setattr(portfolio_engine, "get_session_factory", broken_session_factory)

    with pytest.raises(OperationalError):
        portfolio_engine.add_portfolio_item(
            set_id="75192",
            set_name="Millennium Falcon",
            condition="USED_COMPLETE",
            quantity=1,
            cost_basis_eur=500.0,
            purchased_at=date(2026, 1, 1),
        )
    with pytest.raises(OperationalError):
        portfolio_engine.delete_portfolio_item(1)

    assert seed_path.read_text(encoding="utf-8") == "[]"

    monkeypatch.setenv("LRI_DEMO_ALLOW_WRITES", "1")
    item = portfolio_engine.add_portfolio_item(
        set_id="75192",
        set_name="Millennium Falcon",
        condition="USED_COMPLETE",
        quantity=1,
        cost_basis_eur=500.0,
        purchased_at=date(2026, 1, 1),
    )

    assert item.id == 1
    assert json.loads(seed_path.read_text(encoding="utf-8"))[0]["set_id"] == "75192"


def test_briefing_generation_defaults_to_local_briefing(allow_demo_writes, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr("backend.routers.briefings.generate_briefing_with_llm", _fail)
    client = TestClient(app)

    response = client.post("/api/briefings/generate")

    assert response.status_code == 200
    assert response.json()["used_llm"] is False


def test_analyze_is_rate_limited_per_client(monkeypatch, fake_pipeline):
    monkeypatch.setenv("LRI_RATE_LIMIT_PER_MINUTE", "2")
    client = TestClient(app)

    statuses = [
        client.post("/api/analyze", json={"url": "https://www.ebay.es/itm/lego-75192"}).status_code
        for _ in range(3)
    ]

    assert statuses == [200, 200, 429]
    limited = client.post("/api/analyze", json={"url": "https://www.ebay.es/itm/lego-75192"})
    assert "Too many analysis requests" in limited.json()["detail"]
    assert int(limited.headers["Retry-After"]) >= 1


def test_analyze_daily_limit_per_client(monkeypatch, fake_pipeline):
    monkeypatch.setenv("LRI_RATE_LIMIT_PER_DAY", "1")
    client = TestClient(app)

    first = client.post("/api/analyze", json={"url": "https://www.ebay.es/itm/lego-75192"})
    second = client.post("/api/analyze", json={"url": "https://www.ebay.es/itm/lego-75192"})

    assert first.status_code == 200
    assert second.status_code == 429


def test_analyze_never_fetches_the_demo_url(monkeypatch):
    monkeypatch.setattr("backend.routers.analyze.analyze_listing_url", _fail)
    client = TestClient(app)

    response = client.post("/api/analyze", json={"url": "https://www.ebay.es/itm/demo-lego-75192"})

    assert response.status_code == 200
    assert response.json() == client.post("/api/analyze/demo").json()


def test_demo_analysis_is_not_rate_limited(monkeypatch):
    monkeypatch.setenv("LRI_RATE_LIMIT_PER_MINUTE", "1")
    client = TestClient(app)

    assert all(client.post("/api/analyze/demo").status_code == 200 for _ in range(3))


def test_global_llm_cap_returns_429(monkeypatch):
    def over_budget(url: str) -> ListingAnalysis:
        raise LLMBudgetExceeded(retry_after=3600)

    monkeypatch.setattr("backend.routers.analyze.analyze_listing_url", over_budget)
    client = TestClient(app)

    response = client.post("/api/analyze", json={"url": "https://www.ebay.es/itm/lego-75192"})

    assert response.status_code == 429
    assert "daily limit" in response.json()["detail"]
    assert response.headers["Retry-After"] == "3600"


def test_reserve_llm_call_enforces_daily_cap(monkeypatch):
    monkeypatch.setenv("LRI_LLM_DAILY_CAP", "2")

    reserve_llm_call()
    reserve_llm_call()
    with pytest.raises(LLMBudgetExceeded):
        reserve_llm_call()


def test_pipeline_does_not_hide_llm_cap_as_extraction_error(monkeypatch):
    monkeypatch.setattr(
        "src.pipeline.fetch_html",
        lambda url: "<html><h1>LEGO 75192 Millennium Falcon</h1></html>",
    )

    def over_budget(raw_text):
        raise LLMBudgetExceeded(retry_after=60)

    monkeypatch.setattr("src.pipeline.extract_listing", over_budget)

    with pytest.raises(LLMBudgetExceeded):
        analyze_listing_url("https://www.ebay.es/itm/lego-75192")


@pytest.mark.parametrize(
    "url",
    [
        "http://127.0.0.1:8000/internal",
        "https://169.254.169.254/latest/meta-data/",
        "https://evil.example/listing",
        "https://www.ebay.es@evil.example/",
    ],
)
def test_analyze_rejects_unsupported_urls_with_400(monkeypatch, url):
    monkeypatch.setattr("src.capture.requests.get", _fail)
    client = TestClient(app)

    response = client.post("/api/analyze", json={"url": url})

    assert response.status_code == 400
    assert "eBay, Wallapop or Vinted" in response.json()["detail"]


def test_analyze_rejects_allowlisted_host_resolving_to_private_ip(monkeypatch):
    monkeypatch.setattr("src.capture._resolve_host", lambda hostname: ["127.0.0.1"])
    monkeypatch.setattr("src.capture.requests.get", _fail)
    client = TestClient(app)

    response = client.post("/api/analyze", json={"url": "https://www.ebay.es/itm/lego-75192"})

    assert response.status_code == 400


def test_analyze_does_not_leak_extraction_errors(monkeypatch):
    monkeypatch.setattr(
        "src.pipeline.fetch_html",
        lambda url: "<html><h1>LEGO 75192 Millennium Falcon</h1></html>",
    )

    def leaky_extraction(raw_text):
        raise RuntimeError("Anthropic devolvió un error de API: 401 invalid x-api-key sk-ant-secret")

    monkeypatch.setattr("src.pipeline.extract_listing", leaky_extraction)
    client = TestClient(app)

    response = client.post("/api/analyze", json={"url": "https://www.ebay.es/itm/lego-75192"})

    assert response.status_code == 422
    assert "Could not analyze this listing" in response.json()["detail"]
    assert "Anthropic" not in response.text


def test_unhandled_errors_return_generic_message(monkeypatch):
    def broken_summary():
        raise RuntimeError("password=hunter2 at postgres://internal-db:5432")

    monkeypatch.setattr("backend.routers.portfolio.get_portfolio_summary", broken_summary)
    client = TestClient(app, raise_server_exceptions=False)

    response = client.get("/api/portfolio")

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error."}
    assert "hunter2" not in response.text


def test_pipeline_error_messages_never_include_exception_text(monkeypatch):
    monkeypatch.setattr(
        "src.pipeline.fetch_html",
        lambda url: "<html><h1>LEGO 75192 Millennium Falcon</h1></html>",
    )

    def missing_key(raw_text):
        raise RuntimeError("Falta ANTHROPIC_API_KEY en el entorno.")

    monkeypatch.setattr("src.pipeline.extract_listing", missing_key)

    with pytest.raises(PipelineError) as raised:
        analyze_listing_url("https://www.ebay.es/itm/lego-75192")

    assert "ANTHROPIC" not in str(raised.value)


@pytest.mark.parametrize("path", ["/docs", "/redoc", "/openapi.json"])
def test_api_docs_are_disabled_by_default(path):
    client = TestClient(create_app())

    assert client.get(path).status_code == 404


def test_api_docs_can_be_enabled(monkeypatch):
    monkeypatch.setenv("LRI_ENABLE_DOCS", "1")
    client = TestClient(create_app())

    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.json").status_code == 200


def _preflight(client: TestClient, origin: str):
    return client.options(
        "/api/analyze",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )


def test_cors_defaults_to_public_frontend_without_credentials(monkeypatch):
    monkeypatch.delenv("BACKEND_CORS_ORIGINS", raising=False)
    client = TestClient(create_app())

    allowed = _preflight(client, "https://lego-resale-ntelligence.vercel.app")
    local = _preflight(client, "http://localhost:3000")
    foreign = _preflight(client, "https://evil.example")

    assert allowed.status_code == 200
    assert allowed.headers["access-control-allow-origin"] == "https://lego-resale-ntelligence.vercel.app"
    assert "access-control-allow-credentials" not in allowed.headers
    assert "PUT" not in allowed.headers["access-control-allow-methods"]
    assert local.status_code == 400
    assert foreign.status_code == 400


def test_cors_uses_configured_origins(monkeypatch):
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "http://localhost:3000")
    client = TestClient(create_app())

    assert _preflight(client, "http://localhost:3000").status_code == 200
    assert _preflight(client, "https://lego-resale-ntelligence.vercel.app").status_code == 400
