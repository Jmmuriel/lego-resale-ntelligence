import { getDataQualityReport, getLatestBriefing, getMarketTrends, getPortfolio } from "@/lib/api";

function eur(value: number) {
  return new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency: "EUR",
    maximumFractionDigits: 0
  }).format(value);
}

function pct(value: number) {
  const sign = value >= 0 ? "+" : "";
  return `${sign}${(value * 100).toFixed(1)}%`;
}

export default async function MarketOverviewPage() {
  const [portfolio, trends, briefings, dataQuality] = await Promise.all([
    getPortfolio(),
    getMarketTrends(),
    getLatestBriefing(),
    getDataQualityReport()
  ]);
  const briefing = briefings[0];

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <h1>Market Overview</h1>
          <p>Collector-grade signals for retired LEGO sets — prices, P&amp;L, and briefing context.</p>
        </div>
        <div className="page-header-actions">
          <span
            className={`trend-badge ${briefing.market_trend === "BULLISH" ? "trend-up" : briefing.market_trend === "BEARISH" ? "trend-down" : "trend-flat"}`}
          >
            Market {briefing.market_trend}
          </span>
        </div>
      </header>

      <div className="stat-strip" aria-label="Portfolio KPIs">
        <div className="stat-cell">
          <span className="stat-label">Portfolio value</span>
          <span className="stat-value">{eur(portfolio.total_current_fair_value_eur)}</span>
          <span className="stat-sub">{portfolio.open_positions} open positions</span>
        </div>
        <div className="stat-cell">
          <span className="stat-label">Net if sold</span>
          <span className="stat-value">{eur(portfolio.total_net_if_sold_eur)}</span>
        </div>
        <div className="stat-cell">
          <span className="stat-label">Unrealized P&amp;L</span>
          <span
            className={`stat-value ${portfolio.total_unrealized_pnl_eur >= 0 ? "positive" : "negative"}`}
          >
            {eur(portfolio.total_unrealized_pnl_eur)}
          </span>
        </div>
        <div className="stat-cell">
          <span className="stat-label">Dominant signal</span>
          <span className="stat-value" style={{ fontSize: "18px" }}>{portfolio.dominant_signal}</span>
        </div>
        <div className="stat-cell">
          <span className="stat-label">Catalog coverage</span>
          <span className="stat-value">{dataQuality.metrics.catalog_plus_candidates}/{dataQuality.metrics.target_catalog_sets}</span>
          <span className="stat-sub">{dataQuality.metrics.candidate_catalog_coverage_pct.toFixed(0)}% of target</span>
        </div>
      </div>

      <section className="content-grid">
        <article className="panel">
          <div className="panel-heading">
            <strong>Top movers</strong>
            <span>Recent price changes</span>
          </div>
          <div>
            {trends.length === 0 ? (
              <p className="microcopy">No trend data yet.</p>
            ) : trends.slice(0, 5).map((trend) => (
              <div className="data-row" key={`${trend.set_id}-${trend.condition}`}>
                <div>
                  <strong style={{ fontSize: "14px" }}>{trend.set_id}</strong>
                  <span style={{ color: "var(--muted)", fontSize: "12px" }}>
                    {trend.condition.replace(/_/g, " ")}
                  </span>
                </div>
                <em className={trend.change_pct >= 0 ? "positive" : "negative"} style={{ fontWeight: 700 }}>
                  {pct(trend.change_pct)}
                </em>
              </div>
            ))}
          </div>
        </article>

        <div style={{ display: "grid", gap: "14px" }}>
          <article className="panel">
            <div className="panel-heading">
              <strong>Latest briefing</strong>
              <span className={`trend-badge ${briefing.market_trend === "BULLISH" ? "trend-up" : briefing.market_trend === "BEARISH" ? "trend-down" : "trend-flat"}`}>
                {briefing.market_trend}
              </span>
            </div>
            <p className="briefing-text" style={{ fontSize: "13px", lineHeight: "1.65" }}>
              {briefing.briefing_text.replaceAll("#", "").slice(0, 320)}…
            </p>
          </article>

          <article className="panel">
            <div className="panel-heading">
              <strong>Data maturity</strong>
              <span>{dataQuality.status.replace(/_/g, " ")}</span>
            </div>
            <div>
              <div className="data-row">
                <div>
                  <strong style={{ fontSize: "14px" }}>{dataQuality.metrics.catalog_sets} active sets</strong>
                  <span style={{ color: "var(--muted)", fontSize: "12px" }}>
                    {dataQuality.metrics.catalog_candidate_sets} in research queue
                  </span>
                </div>
                <em style={{ fontWeight: 700 }}>
                  {dataQuality.metrics.catalog_plus_candidates}/{dataQuality.metrics.target_catalog_sets}
                </em>
              </div>
              <div className="data-row">
                <div>
                  <strong style={{ fontSize: "14px" }}>{dataQuality.metrics.priced_sets} priced sets</strong>
                  <span style={{ color: "var(--muted)", fontSize: "12px" }}>
                    {dataQuality.metrics.price_snapshots} snapshots
                  </span>
                </div>
                <em style={{ fontWeight: 700 }}>
                  {dataQuality.metrics.pricing_coverage_pct.toFixed(0)}%
                </em>
              </div>
            </div>
          </article>
        </div>
      </section>
    </div>
  );
}
