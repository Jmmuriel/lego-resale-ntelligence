from fastapi.testclient import TestClient

from src.models import ListingAnalysis
from backend.main import app


def test_health_endpoint_reports_api_alive():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "lego-resale-intelligence-api",
    }


def test_initial_v2_routers_are_registered():
    client = TestClient(app)

    for route in [
        "/api/analyze/ping",
        "/api/market/ping",
        "/api/portfolio/ping",
        "/api/briefings/ping",
        "/api/watchlist/ping",
    ]:
        response = client.get(route)

        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_market_price_endpoint_returns_dynamic_fair_price():
    client = TestClient(app)

    response = client.get("/api/market/price/75192?condition=USED_COMPLETE")

    assert response.status_code == 200
    payload = response.json()
    assert payload["set_id"] == "75192"
    assert payload["condition"] == "USED_COMPLETE"
    assert payload["confidence"] == "HIGH"
    assert payload["avg_eur"] is not None


def test_market_trends_endpoint_returns_price_changes():
    client = TestClient(app)

    response = client.get("/api/market/trends?days=120")

    assert response.status_code == 200
    payload = response.json()
    assert payload
    assert "change_pct" in payload[0]


def test_market_data_quality_endpoint_returns_coverage_metrics():
    client = TestClient(app)

    response = client.get("/api/market/data-quality")

    assert response.status_code == 200
    payload = response.json()
    assert payload["ok"] is True
    assert payload["status"] == "ready"
    assert payload["metrics"]["catalog_sets"] == 50
    assert payload["metrics"]["catalog_candidate_sets"] == 0
    assert payload["metrics"]["catalog_plus_candidates"] == 50
    assert payload["metrics"]["candidate_catalog_coverage_pct"] == 100.0
    assert payload["metrics"]["active_catalog_verified_sets"] == 0
    assert payload["metrics"]["active_catalog_evidence_started_sets"] >= 0
    assert payload["metrics"]["active_catalog_blocked_sets"] >= 0
    assert payload["metrics"]["market_data_source_status"] == "seed_demo"
    assert any(
        warning["code"] == "ACTIVE_CATALOG_UNVERIFIED"
        for warning in payload["warnings"]
    )


def test_market_catalog_candidates_endpoint_returns_research_queue():
    client = TestClient(app)

    response = client.get("/api/market/catalog-candidates")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 0


def test_market_active_evidence_endpoint_returns_audit_log():
    client = TestClient(app)

    response = client.get("/api/market/active-evidence")

    assert response.status_code == 200
    payload = response.json()
    assert payload
    assert payload[0]["set_id"] == "75192"
    assert payload[0]["verification_status"] == "blocked_catalog_mismatch"
    assert payload[0]["ready_for_verified"] is False


def test_market_set_intelligence_endpoint_returns_set_summary():
    client = TestClient(app)

    response = client.get("/api/market/set/75192?days=120")

    assert response.status_code == 200
    payload = response.json()
    assert payload["set_id"] == "75192"
    assert payload["market_signal"] in {"UP", "DOWN", "STABLE", "UNKNOWN"}
    assert payload["fair_prices"]
    assert "summary" in payload


def test_market_history_endpoint_returns_price_snapshots():
    client = TestClient(app)

    response = client.get("/api/market/history/75192?condition=USED_COMPLETE&days=120")

    assert response.status_code == 200
    payload = response.json()
    assert payload
    assert payload[0]["set_id"] == "75192"
    assert payload[0]["condition"] == "USED_COMPLETE"
    assert "price_avg_eur" in payload[0]


def test_portfolio_summary_endpoint_returns_pnl_rollup():
    client = TestClient(app)

    response = client.get("/api/portfolio")

    assert response.status_code == 200
    payload = response.json()
    assert payload["open_positions"] >= 1
    assert payload["total_cost_basis_eur"] > 0
    assert "positions" in payload
    assert "unrealized_pnl_eur" in payload["positions"][0]["pnl"]


def test_portfolio_positions_endpoint_returns_positions():
    client = TestClient(app)

    response = client.get("/api/portfolio/positions")

    assert response.status_code == 200
    payload = response.json()
    assert payload
    assert "item" in payload[0]
    assert "pnl" in payload[0]


def test_briefings_endpoint_returns_latest_briefing():
    client = TestClient(app)

    response = client.get("/api/briefings")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["used_llm"] is False
    assert "briefing_text" in payload[0]


def test_generate_briefing_endpoint_returns_market_briefing():
    client = TestClient(app)

    response = client.post("/api/briefings/generate?period_days=7&use_llm=false")

    assert response.status_code == 200
    payload = response.json()
    assert payload["market_trend"] in {"BULLISH", "NEUTRAL", "BEARISH"}
    assert payload["token_count"] == 0


def test_watchlist_endpoint_saves_and_lists_analysis(tmp_path, monkeypatch):
    database_url = f"sqlite:///{tmp_path / 'watchlist.db'}"

    monkeypatch.setattr("backend.routers.watchlist.save_listing_analysis", lambda analysis, status: __import__(
        "src.db", fromlist=["save_listing_analysis"]
    ).save_listing_analysis(analysis, database_url=database_url, status=status))
    monkeypatch.setattr("backend.routers.watchlist.list_recent_listings", lambda limit: __import__(
        "src.db", fromlist=["list_recent_listings"]
    ).list_recent_listings(limit=limit, database_url=database_url))

    client = TestClient(app)
    payload = {
        "url": "https://www.ebay.es/itm/lego-75192",
        "marketplace": "ebay",
        "set_id": "75192",
        "condition": "USED_COMPLETE",
        "asking_price_eur": 560.0,
        "shipping_eur": 25.0,
        "fair_price_eur": 720.0,
        "gross_margin_eur": 135.0,
        "net_margin_eur": 55.0,
        "opportunity_score": 72,
        "category": "GREEN",
        "risk_flags": ["Confirmar piezas completas"],
        "notes": "Análisis mock desde API V2.",
    }

    create_response = client.post("/api/watchlist?listing_status=watching", json=payload)
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["status"] == "watching"
    assert created["set_id"] == "75192"

    list_response = client.get("/api/watchlist")
    assert list_response.status_code == 200
    records = list_response.json()
    assert len(records) == 1
    assert records[0]["id"] == created["id"]


def test_watchlist_status_endpoint_updates_record(tmp_path, monkeypatch):
    from src.db import save_listing_analysis as db_save_listing_analysis
    from src.db import update_listing_status as db_update_listing_status

    database_url = f"sqlite:///{tmp_path / 'watchlist.db'}"
    record = db_save_listing_analysis(_sample_listing_analysis(), database_url=database_url)

    monkeypatch.setattr("backend.routers.watchlist.update_listing_status", lambda listing_id, status: db_update_listing_status(
        listing_id=listing_id,
        status=status,
        database_url=database_url,
    ))

    client = TestClient(app)
    response = client.patch(f"/api/watchlist/{record.id}/status", json={"status": "discarded"})

    assert response.status_code == 200
    assert response.json()["status"] == "discarded"


def test_analyze_endpoint_returns_v1_pipeline_result(monkeypatch):
    def fake_analyze_listing_url(url: str) -> ListingAnalysis:
        return ListingAnalysis(
            url=url,
            marketplace="ebay",
            set_id="75192",
            condition="USED_COMPLETE",
            asking_price_eur=560.0,
            shipping_eur=25.0,
            fair_price_eur=720.0,
            gross_margin_eur=135.0,
            net_margin_eur=55.0,
            opportunity_score=72,
            category="GREEN",
            risk_flags=["Confirmar piezas completas"],
            notes="Análisis mock desde API V2.",
        )

    monkeypatch.setattr("backend.routers.analyze.analyze_listing_url", fake_analyze_listing_url)
    client = TestClient(app)

    response = client.post(
        "/api/analyze",
        json={"url": "https://www.ebay.es/itm/lego-75192"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["url"] == "https://www.ebay.es/itm/lego-75192"
    assert payload["set_id"] == "75192"
    assert payload["category"] == "GREEN"
    assert payload["opportunity_score"] == 72
    assert payload["market_context"]["fair_price_source"] == "dynamic_history"
    assert payload["market_context"]["price_confidence"] == "HIGH"
    assert payload["market_context"]["anomaly_score"] < 0


def test_analyze_demo_endpoint_returns_no_cost_demo_result():
    client = TestClient(app)

    response = client.post("/api/analyze/demo")

    assert response.status_code == 200
    payload = response.json()
    assert payload["url"] == "https://www.ebay.es/itm/demo-lego-75192"
    assert payload["set_id"] == "75192"
    assert payload["market_context"]["fair_price_source"] == "dynamic_history"
    assert payload["market_context"]["price_confidence"] == "HIGH"


def test_analyze_endpoint_falls_back_to_manual_price_without_dynamic_history(monkeypatch):
    def fake_analyze_listing_url(url: str) -> ListingAnalysis:
        return ListingAnalysis(
            url=url,
            marketplace="ebay",
            set_id="10221",
            condition="USED_COMPLETE",
            asking_price_eur=500.0,
            shipping_eur=20.0,
            fair_price_eur=430.0,
            gross_margin_eur=-90.0,
            net_margin_eur=-141.0,
            opportunity_score=0,
            category="RED",
            risk_flags=[],
            notes="Sin histórico dinámico todavía.",
        )

    monkeypatch.setattr("backend.routers.analyze.analyze_listing_url", fake_analyze_listing_url)
    client = TestClient(app)

    response = client.post(
        "/api/analyze",
        json={"url": "https://www.ebay.es/itm/lego-10221"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["set_id"] == "10221"
    assert payload["market_context"]["fair_price_source"] == "manual_reference"
    assert payload["market_context"]["fair_price_eur"] == 430.0
    assert payload["market_context"]["price_confidence"] == "NONE"
    assert payload["market_context"]["anomaly_score"] > 0


def test_analyze_endpoint_returns_controlled_pipeline_error(monkeypatch):
    from src.pipeline import PipelineError

    def fail_analyze_listing_url(url: str) -> ListingAnalysis:
        raise PipelineError("No se pudo identificar el set contra el catálogo local.")

    monkeypatch.setattr("backend.routers.analyze.analyze_listing_url", fail_analyze_listing_url)
    client = TestClient(app)

    response = client.post(
        "/api/analyze",
        json={"url": "https://example.com/unknown"},
    )

    assert response.status_code == 422
    assert "No se pudo identificar" in response.json()["detail"]


def _sample_listing_analysis() -> ListingAnalysis:
    return ListingAnalysis(
        url="https://www.ebay.es/itm/lego-75192",
        marketplace="ebay",
        set_id="75192",
        condition="USED_COMPLETE",
        asking_price_eur=560.0,
        shipping_eur=25.0,
        fair_price_eur=720.0,
        gross_margin_eur=135.0,
        net_margin_eur=55.0,
        opportunity_score=72,
        category="GREEN",
        risk_flags=["Confirmar piezas completas"],
        notes="Análisis mock desde API V2.",
    )
