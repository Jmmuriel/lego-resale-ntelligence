import { getCatalogCandidates, getDataQualityReport } from "@/lib/api";
import ResearchQueue from "@/components/ResearchQueue";

export default async function ResearchPage() {
  const [candidates, dataQuality] = await Promise.all([
    getCatalogCandidates(),
    getDataQualityReport()
  ]);
  const byTheme = new Map<string, number>();
  for (const candidate of candidates) {
    byTheme.set(candidate.theme, (byTheme.get(candidate.theme) ?? 0) + 1);
  }

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <h1>Research Queue</h1>
          <p>
            {candidates.length} candidates waiting for validation — not active pricing data yet.
          </p>
        </div>
        <div className="page-header-actions">
          <span className={`trend-badge ${dataQuality.metrics.candidate_ready_for_promotion > 0 ? "trend-up" : "trend-flat"}`}>
            {dataQuality.metrics.candidate_ready_for_promotion} ready
          </span>
        </div>
      </header>

      <div className="stat-strip" aria-label="Research KPIs">
        <div className="stat-cell">
          <span className="stat-label">Active catalog</span>
          <span className="stat-value">{dataQuality.metrics.catalog_sets}</span>
        </div>
        <div className="stat-cell">
          <span className="stat-label">Candidates</span>
          <span className="stat-value">{dataQuality.metrics.catalog_candidate_sets}</span>
        </div>
        <div className="stat-cell">
          <span className="stat-label">Total / target</span>
          <span className="stat-value">{dataQuality.metrics.catalog_plus_candidates}/{dataQuality.metrics.target_catalog_sets}</span>
        </div>
        <div className="stat-cell">
          <span className="stat-label">Ready to promote</span>
          <span className="stat-value">{dataQuality.metrics.candidate_ready_for_promotion}</span>
        </div>
        <div className="stat-cell">
          <span className="stat-label">Status</span>
          <span className="stat-value" style={{ fontSize: "14px" }}>{dataQuality.status.replace(/_/g, " ")}</span>
        </div>
      </div>

      <section className="content-grid">
        <article className="panel">
          <div className="panel-heading">
            <strong>By theme</strong>
            <span>{byTheme.size} themes</span>
          </div>
          <div>
            {Array.from(byTheme.entries()).map(([theme, count]) => (
              <div className="data-row" key={theme}>
                <strong style={{ fontSize: "14px" }}>{theme}</strong>
                <em style={{ fontWeight: 700 }}>{count}</em>
              </div>
            ))}
          </div>
        </article>

        <article className="panel">
          <div className="panel-heading">
            <strong>Promotion rule</strong>
          </div>
          <p className="briefing-text" style={{ fontSize: "13px" }}>
            A candidate needs all 8 evidence checks before promotion to the active catalog:
            release year, retirement, retail price, piece count, source links, and at least
            3 market price snapshots. No invented prices — ever.
          </p>
        </article>
      </section>

      <ResearchQueue candidates={candidates} />
    </div>
  );
}
