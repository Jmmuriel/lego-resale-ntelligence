import { getPortfolio } from "@/lib/api";
import AddPositionPanel from "@/components/AddPositionPanel";

export const dynamic = "force-dynamic";

function eur(value: number) {
  return new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency: "EUR",
    maximumFractionDigits: 0
  }).format(value);
}

export default async function PortfolioPage() {
  const portfolio = await getPortfolio();
  const pnlPositive = portfolio.total_unrealized_pnl_eur >= 0;

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <h1>Portfolio</h1>
          <p>Cost basis, fair value, P&amp;L and hold/sell signals for your positions.</p>
        </div>
        <div className="page-header-actions">
          <span className={`trend-badge ${pnlPositive ? "trend-up" : "trend-down"}`}>
            {portfolio.dominant_signal}
          </span>
        </div>
      </header>

      <div className="stat-strip" aria-label="Portfolio KPIs">
        <div className="stat-cell">
          <span className="stat-label">Cost basis</span>
          <span className="stat-value">{eur(portfolio.total_cost_basis_eur)}</span>
        </div>
        <div className="stat-cell">
          <span className="stat-label">Fair value</span>
          <span className="stat-value">{eur(portfolio.total_current_fair_value_eur)}</span>
        </div>
        <div className="stat-cell">
          <span className="stat-label">Net if sold</span>
          <span className="stat-value">{eur(portfolio.total_net_if_sold_eur)}</span>
        </div>
        <div className="stat-cell">
          <span className="stat-label">Unrealized P&amp;L</span>
          <span className={`stat-value ${pnlPositive ? "positive" : "negative"}`}>
            {eur(portfolio.total_unrealized_pnl_eur)}
          </span>
          <span className="stat-sub">
            {pnlPositive ? "+" : ""}{portfolio.total_unrealized_pnl_pct.toFixed(1)}%
          </span>
        </div>
        <div className="stat-cell">
          <span className="stat-label">Open positions</span>
          <span className="stat-value">{portfolio.open_positions}</span>
        </div>
      </div>

      <section className="panel">
        <div className="panel-heading">
          <strong>Positions</strong>
          <span>{portfolio.open_positions} sets</span>
        </div>
        <div className="position-list">
          {portfolio.positions.length === 0 ? (
            <div className="empty-state" style={{ minHeight: "100px" }}>
              <span>No positions yet. Use the form below to add your first purchase.</span>
            </div>
          ) : portfolio.positions.map((position) => (
            <article
              className="position-row"
              key={position.item.id}
              style={{ gridTemplateColumns: "minmax(220px, 1.8fr) repeat(4, minmax(110px, 1fr)) auto" }}
            >
              <div>
                <strong>{position.item.set_name}</strong>
                <span>
                  {position.item.set_id} · {position.item.condition.replace(/_/g, " ")} · ×{position.item.quantity}
                </span>
              </div>
              <div>
                <span>Cost</span>
                <strong>{eur(position.pnl.cost_basis_eur)}</strong>
              </div>
              <div>
                <span>Net if sold</span>
                <strong>{eur(position.pnl.net_if_sold_eur)}</strong>
              </div>
              <div>
                <span>P&amp;L</span>
                <strong className={position.pnl.unrealized_pnl_eur >= 0 ? "positive" : "negative"}>
                  {eur(position.pnl.unrealized_pnl_eur)}
                </strong>
              </div>
              <div>
                <span>Signal</span>
                <strong>{position.pnl.hold_sell_signal}</strong>
              </div>
            </article>
          ))}
        </div>
      </section>

      <AddPositionPanel positions={portfolio.positions} />
    </div>
  );
}
