import { getLatestBriefing } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function BriefingsPage() {
  const briefings = await getLatestBriefing();
  const briefing = briefings[0];

  const trendClass =
    briefing.market_trend === "BULLISH" ? "trend-up"
    : briefing.market_trend === "BEARISH" ? "trend-down"
    : "trend-flat";

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <h1>Market Briefing</h1>
          <p>AI-generated market context — prices, portfolio signals, and key opportunities.</p>
        </div>
        <div className="page-header-actions">
          <span className={`trend-badge ${trendClass}`}>
            Market {briefing.market_trend}
          </span>
          {briefing.used_llm && (
            <span className="trend-badge trend-up" style={{ marginLeft: 4 }}>Sonnet</span>
          )}
        </div>
      </header>

      <section className="content-grid">
        <article className="panel">
          <div className="panel-heading">
            <strong>Briefing</strong>
            <span>{new Date(briefing.generated_at).toLocaleDateString("en-GB")}</span>
          </div>
          <p className="briefing-text">{briefing.briefing_text.replaceAll("#", "")}</p>
          <div style={{ marginTop: "16px", borderTop: "1px solid var(--line)", paddingTop: "12px", display: "flex", gap: "16px" }}>
            <span className="microcopy">
              Source: {briefing.used_llm ? `Claude Sonnet · ${briefing.token_count} tokens` : "Local deterministic model"}
            </span>
          </div>
        </article>

        <article className="panel">
          <div className="panel-heading">
            <strong>Key signals</strong>
            <span>{briefing.key_opportunities.length} flagged</span>
          </div>
          <div>
            {briefing.key_opportunities.map((opportunity) => (
              <div className="data-row" key={opportunity}>
                <strong style={{ fontSize: "14px" }}>{opportunity}</strong>
              </div>
            ))}
            {briefing.key_opportunities.length === 0 && (
              <p className="microcopy">No opportunities flagged in this briefing.</p>
            )}
          </div>
        </article>
      </section>
    </div>
  );
}
