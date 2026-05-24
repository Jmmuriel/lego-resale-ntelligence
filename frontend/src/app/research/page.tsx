import { getActiveCatalogEvidence, getCatalogCandidates, getDataQualityReport } from "@/lib/api";
import ResearchQueue from "@/components/ResearchQueue";

export default async function ResearchPage() {
  const [candidates, dataQuality, activeEvidence] = await Promise.all([
    getCatalogCandidates(),
    getDataQualityReport(),
    getActiveCatalogEvidence()
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
          <span className="stat-label">Audit started</span>
          <span className="stat-value">{dataQuality.metrics.active_catalog_evidence_started_sets}</span>
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
            <strong>Evidence rule</strong>
          </div>
          <p className="briefing-text" style={{ fontSize: "13px" }}>
            A candidate needs all 8 evidence checks before promotion to the active catalog:
            release year, retirement, retail price, piece count, source links, and at least
            3 market price snapshots. Active sets need the same evidence before being called
            externally verified. No invented prices — ever.
          </p>
        </article>
      </section>

      <section className="panel">
        <div className="panel-heading">
          <span>Active audit log</span>
          <strong>{activeEvidence.length} reviewed</strong>
        </div>

        {activeEvidence.length === 0 ? (
          <div className="empty-state">
            <strong>No active-set audits yet</strong>
            <span>Verified market claims stay disabled until evidence is logged here.</span>
          </div>
        ) : (
          <div className="evidence-grid">
            {activeEvidence.map((entry) => (
              <article className="evidence-card" key={entry.set_id}>
                <div className="candidate-card-header">
                  <strong>{entry.set_id}</strong>
                  <span>{entry.theme ?? "Active catalog"}</span>
                </div>
                <h2>{entry.name}</h2>
                <p>{entry.audit_summary}</p>
                <div className="evidence-counts">
                  <span>{entry.metadata_source_count} metadata</span>
                  <span>{entry.price_source_count} price sources</span>
                  <span>{entry.price_snapshot_count} snapshots</span>
                </div>
                <div className="readiness-meta">
                  <strong>{entry.verification_status.replace(/_/g, " ")}</strong>
                  <span>{entry.ready_for_verified ? "verified" : `${entry.missing_requirements.length} blockers`}</span>
                </div>
                {entry.recommended_action ? <em>{entry.recommended_action}</em> : null}
              </article>
            ))}
          </div>
        )}
      </section>

      <ResearchQueue candidates={candidates} />
    </div>
  );
}
