"use client";

import { useMemo, useState } from "react";
import { updateWatchlistStatus } from "@/lib/api";
import type { WatchlistRecord, WatchlistStatus } from "@/lib/types";

const statuses: Array<WatchlistStatus | "all"> = [
  "all",
  "analyzed",
  "watching",
  "discarded",
  "bought"
];

function eur(value: number | null) {
  if (value === null) return "n/a";
  return new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency: "EUR",
    maximumFractionDigits: 0
  }).format(value);
}

function statusLabel(status: WatchlistStatus | "all") {
  return status === "all" ? "All" : status.charAt(0).toUpperCase() + status.slice(1);
}

export default function WatchlistDesk({ initialRecords }: { initialRecords: WatchlistRecord[] }) {
  const [records, setRecords] = useState(initialRecords);
  const [filter, setFilter] = useState<WatchlistStatus | "all">("watching");
  const [pendingId, setPendingId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const filteredRecords = useMemo(() => {
    if (filter === "all") return records;
    return records.filter((record) => record.status === filter);
  }, [filter, records]);

  const counts = useMemo(() => {
    return records.reduce<Record<WatchlistStatus, number>>(
      (acc, record) => {
        acc[record.status] += 1;
        return acc;
      },
      { analyzed: 0, watching: 0, discarded: 0, bought: 0 }
    );
  }, [records]);

  async function moveRecord(recordId: number, status: WatchlistStatus) {
    setError(null);
    setPendingId(recordId);

    try {
      const updated = await updateWatchlistStatus(recordId, status);
      setRecords((current) =>
        current.map((record) => (record.id === updated.id ? updated : record))
      );
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Could not update this record.");
    } finally {
      setPendingId(null);
    }
  }

  return (
    <div className="page-stack">
      <section className="watchlist-toolbar panel">
        <div>
          <p className="eyebrow">Workflow</p>
          <strong>{filteredRecords.length} visible opportunities</strong>
        </div>
        <div className="status-tabs" aria-label="Watchlist status filter">
          {statuses.map((status) => (
            <button
              className={filter === status ? "active" : undefined}
              key={status}
              onClick={() => setFilter(status)}
              type="button"
            >
              {statusLabel(status)}
              {status !== "all" ? <span>{counts[status]}</span> : <span>{records.length}</span>}
            </button>
          ))}
        </div>
      </section>

      {error ? <p className="error-text">{error}</p> : null}

      <section className="panel">
        <div className="panel-heading">
          <span>Saved listings</span>
          <strong>SQLite watchlist</strong>
        </div>
        {filteredRecords.length === 0 ? (
          <div className="empty-state">
            <strong>No records in this state</strong>
            <span>Analyze and save a listing, or switch filters to inspect older records.</span>
          </div>
        ) : (
          <div className="watchlist-table">
            {filteredRecords.map((record) => (
              <article className="watchlist-row" key={record.id}>
                <div className="watchlist-main">
                  <span className={`score-badge status-${record.status}`}>
                    {statusLabel(record.status)}
                  </span>
                  <div>
                    <strong>{record.set_id ?? "Unknown set"}</strong>
                    <span>
                      #{record.id} · {record.marketplace ?? "marketplace"} ·{" "}
                      {record.condition?.replace("_", " ") ?? "condition unknown"}
                    </span>
                  </div>
                </div>

                <div className="watchlist-metric">
                  <span>Ask</span>
                  <strong>{eur(record.asking_price_eur)}</strong>
                </div>
                <div className="watchlist-metric">
                  <span>Net margin</span>
                  <strong className={(record.net_margin_eur ?? 0) >= 0 ? "positive" : "negative"}>
                    {eur(record.net_margin_eur)}
                  </strong>
                </div>
                <div className="watchlist-metric">
                  <span>Score</span>
                  <strong>{record.opportunity_score ?? "n/a"}</strong>
                </div>

                <div className="row-actions">
                  <button
                    disabled={pendingId === record.id || record.status === "watching"}
                    onClick={() => moveRecord(record.id, "watching")}
                    type="button"
                  >
                    Watch
                  </button>
                  <button
                    disabled={pendingId === record.id || record.status === "discarded"}
                    onClick={() => moveRecord(record.id, "discarded")}
                    type="button"
                  >
                    Discard
                  </button>
                  <button
                    disabled={pendingId === record.id || record.status === "bought"}
                    onClick={() => moveRecord(record.id, "bought")}
                    type="button"
                  >
                    Bought
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
