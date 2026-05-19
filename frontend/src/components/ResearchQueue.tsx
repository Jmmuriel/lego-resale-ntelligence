"use client";

import { useMemo, useState } from "react";
import type { CatalogCandidate } from "@/lib/types";

interface ResearchQueueProps {
  candidates: CatalogCandidate[];
}

export default function ResearchQueue({ candidates }: ResearchQueueProps) {
  const themes = useMemo(
    () => ["All", ...Array.from(new Set(candidates.map((candidate) => candidate.theme))).sort()],
    [candidates]
  );
  const [query, setQuery] = useState("");
  const [theme, setTheme] = useState("All");

  const filteredCandidates = candidates.filter((candidate) => {
    const normalizedQuery = query.trim().toLowerCase();
    const matchesTheme = theme === "All" || candidate.theme === theme;
    const matchesQuery =
      normalizedQuery.length === 0 ||
      candidate.set_id.toLowerCase().includes(normalizedQuery) ||
      candidate.name.toLowerCase().includes(normalizedQuery) ||
      candidate.reason.toLowerCase().includes(normalizedQuery);

    return matchesTheme && matchesQuery;
  });

  return (
    <section className="panel">
      <div className="panel-heading">
        <span>Candidate list</span>
        <strong>{filteredCandidates.length}/{candidates.length} sets</strong>
      </div>

      <div className="research-toolbar">
        <label>
          <span>Search</span>
          <input
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Set number, name or reason"
            type="search"
            value={query}
          />
        </label>
        <div className="theme-filter" aria-label="Filter candidates by theme">
          {themes.map((nextTheme) => (
            <button
              className={nextTheme === theme ? "active" : undefined}
              key={nextTheme}
              onClick={() => setTheme(nextTheme)}
              type="button"
            >
              {nextTheme}
            </button>
          ))}
        </div>
      </div>

      {filteredCandidates.length === 0 ? (
        <div className="empty-state">
          <strong>No candidates found</strong>
          <span>Adjust the search or theme filter.</span>
        </div>
      ) : (
        <div className="candidate-grid">
          {filteredCandidates.map((candidate) => {
            const readiness = candidate.readiness ?? {
              completed_checks: 0,
              required_checks: 8,
              ready_for_promotion: false,
              missing_requirements: [],
              metadata_source_count: 0,
              price_source_count: 0,
              price_snapshot_count: 0
            };
            const progress = Math.round(
              (readiness.completed_checks / readiness.required_checks) * 100
            );

            return (
              <article className="candidate-card" key={candidate.set_id}>
                <div className="candidate-card-header">
                  <strong>{candidate.set_id}</strong>
                  <span>{candidate.theme}</span>
                </div>
                <h2>{candidate.name}</h2>
                <p>{candidate.reason}</p>
                <div className="readiness-meter">
                  <span style={{ width: `${progress}%` }} />
                </div>
                <div className="readiness-meta">
                  <strong>
                    {readiness.completed_checks}/{readiness.required_checks} checks
                  </strong>
                  <span>
                    {readiness.ready_for_promotion
                      ? "ready"
                      : `${readiness.missing_requirements.length} missing`}
                  </span>
                </div>
                <em>{candidate.validation_status.replace("_", " ")}</em>
              </article>
            );
          })}
        </div>
      )}
    </section>
  );
}
