"use client";

import { FormEvent, useState } from "react";
import { analyzeDemoOpportunity, analyzeUrl, saveAnalysisToWatchlist } from "@/lib/api";
import type { AnalysisResult, WatchlistRecord } from "@/lib/types";

function eur(value: number | null | undefined) {
  if (value === null || value === undefined) return "n/a";
  return new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency: "EUR",
    maximumFractionDigits: 0
  }).format(value);
}

export default function AnalyzeWorkbench() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [savedRecord, setSavedRecord] = useState<WatchlistRecord | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setSaveError(null);
    setResult(null);
    setSavedRecord(null);
    setIsLoading(true);

    try {
      const analysis = await analyzeUrl(url);
      setResult(analysis);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Could not analyze this listing.");
    } finally {
      setIsLoading(false);
    }
  }

  async function onLoadDemo() {
    setError(null);
    setSaveError(null);
    setResult(null);
    setSavedRecord(null);
    setIsLoading(true);

    try {
      const analysis = await analyzeDemoOpportunity();
      setUrl(analysis.url);
      setResult(analysis);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Could not load the demo opportunity.");
    } finally {
      setIsLoading(false);
    }
  }

  async function onSaveToWatchlist() {
    if (!result) return;

    setSaveError(null);
    setIsSaving(true);

    try {
      setSavedRecord(await saveAnalysisToWatchlist(result));
    } catch (caught) {
      setSaveError(caught instanceof Error ? caught.message : "Could not save this listing.");
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <div className="workbench-grid">
      <section className="panel panel-large">
        <div className="panel-heading">
          <span>Live analyzer</span>
          <strong>Listing URL</strong>
        </div>
        <form className="analyze-form" onSubmit={onSubmit}>
          <input
            aria-label="Listing URL"
            onChange={(event) => setUrl(event.target.value)}
            placeholder="Paste an eBay, Wallapop or marketplace listing URL"
            required
            type="url"
            value={url}
          />
          <button disabled={isLoading} type="submit">
            {isLoading ? "Analyzing" : "Analyze"}
          </button>
        </form>
        <button className="text-action" disabled={isLoading} onClick={onLoadDemo} type="button">
          Load no-cost demo opportunity
        </button>
        <p className="microcopy">
          Real URLs use the V1 extraction pipeline. The demo opportunity is local and does not
          spend Anthropic tokens.
        </p>
      </section>

      <section className="panel">
        <div className="panel-heading">
          <span>Status</span>
          <strong>{isLoading ? "Running" : result ? "Ready" : "Idle"}</strong>
        </div>
        {error ? <p className="error-text">{error}</p> : null}
        {!error && !result ? (
          <div className="empty-state">
            <strong>Waiting for a listing</strong>
            <span>Paste a URL to create the first V2 enriched analysis.</span>
          </div>
        ) : null}
        {result ? (
          <div className="result-stack">
            <div className={`score-badge score-${result.category?.toLowerCase() ?? "unknown"}`}>
              {result.category ?? "UNKNOWN"}
            </div>
            <dl className="metric-list">
              <div>
                <dt>Set</dt>
                <dd>{result.set_id ?? "Unknown"}</dd>
              </div>
              <div>
                <dt>Asking price</dt>
                <dd>{eur(result.asking_price_eur)}</dd>
              </div>
              <div>
                <dt>Fair price</dt>
                <dd>{eur(result.market_context.fair_price_eur ?? result.fair_price_eur)}</dd>
              </div>
              <div>
                <dt>Net margin</dt>
                <dd>{eur(result.net_margin_eur)}</dd>
              </div>
              <div>
                <dt>Confidence</dt>
                <dd>{result.market_context.price_confidence}</dd>
              </div>
              <div>
                <dt>Anomaly</dt>
                <dd>
                  {result.market_context.anomaly_score === null
                    ? "n/a"
                    : result.market_context.anomaly_score.toFixed(2)}
                </dd>
              </div>
            </dl>
            <button className="secondary-action" disabled={isSaving || Boolean(savedRecord)} onClick={onSaveToWatchlist}>
              {savedRecord ? `Saved #${savedRecord.id}` : isSaving ? "Saving" : "Save to watchlist"}
            </button>
            {saveError ? <p className="error-text">{saveError}</p> : null}
            {savedRecord ? (
              <p className="success-text">
                Saved as {savedRecord.status}. It is now visible in the shared SQLite watchlist.
              </p>
            ) : null}
          </div>
        ) : null}
      </section>
    </div>
  );
}
