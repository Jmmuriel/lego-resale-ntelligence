"use client";

import { FormEvent, useState } from "react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import { getSetIntelligence, getSetPriceHistory } from "@/lib/api";
import type { PriceSnapshot, SetIntelligence } from "@/lib/types";

function eur(value: number | null) {
  if (value === null) return "n/a";
  return new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency: "EUR",
    maximumFractionDigits: 0
  }).format(value);
}

function pct(value: number | null | undefined) {
  if (value === null || value === undefined) return "n/a";
  return `${(value * 100).toFixed(1)}%`;
}

export default function SetLookup() {
  const [setId, setSetId] = useState("75192");
  const [result, setResult] = useState<SetIntelligence | null>(null);
  const [history, setHistory] = useState<PriceSnapshot[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      const normalizedSetId = setId.trim();
      const [nextResult, nextHistory] = await Promise.all([
        getSetIntelligence(normalizedSetId),
        getSetPriceHistory(normalizedSetId)
      ]);
      setResult(nextResult);
      setHistory(nextHistory);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Could not load set intelligence.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="workbench-grid">
      <section className="panel panel-large">
        <div className="panel-heading">
          <span>Set intelligence</span>
          <strong>Lookup</strong>
        </div>
        <form className="analyze-form" onSubmit={onSubmit}>
          <input
            aria-label="LEGO set number"
            inputMode="numeric"
            onChange={(event) => setSetId(event.target.value)}
            placeholder="75192"
            required
            value={setId}
          />
          <button disabled={isLoading} type="submit">
            {isLoading ? "Loading" : "Load"}
          </button>
        </form>
        <p className="microcopy">
          Try seeded sets like 75192, 75313, 75095 or 10214 while the database is still small.
        </p>

        {result ? (
          <div className="set-summary-block">
            <div className={`score-badge signal-${result.market_signal.toLowerCase()}`}>
              {result.market_signal}
            </div>
            <p>{result.summary}</p>
          </div>
        ) : null}
        {error ? <p className="error-text">{error}</p> : null}
      </section>

      <section className="panel">
        <div className="panel-heading">
          <span>Market data</span>
          <strong>{result?.set_id ?? "No set"}</strong>
        </div>
        {!result ? (
          <div className="empty-state">
            <strong>No set loaded</strong>
            <span>Load a set to inspect fair price, confidence and recent movement.</span>
          </div>
        ) : null}
        {result ? (
          <div className="result-stack">
            <div className="chart-card">
              <ResponsiveContainer height={184} width="100%">
                <AreaChart data={history} margin={{ bottom: 0, left: 0, right: 8, top: 12 }}>
                  <defs>
                    <linearGradient id="priceArea" x1="0" x2="0" y1="0" y2="1">
                      <stop offset="5%" stopColor="#f7c600" stopOpacity={0.42} />
                      <stop offset="95%" stopColor="#f7c600" stopOpacity={0.02} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke="rgba(8, 10, 15, 0.08)" vertical={false} />
                  <XAxis
                    dataKey="recorded_at"
                    minTickGap={18}
                    tick={{ fill: "#7a756c", fontSize: 11 }}
                    tickLine={false}
                  />
                  <YAxis
                    domain={["dataMin - 20", "dataMax + 20"]}
                    tick={{ fill: "#7a756c", fontSize: 11 }}
                    tickFormatter={(value) => `€${value}`}
                    tickLine={false}
                    width={46}
                  />
                  <Tooltip
                    contentStyle={{
                      background: "#fffdf7",
                      border: "1px solid rgba(8, 10, 15, 0.12)",
                      borderRadius: 8,
                      boxShadow: "0 18px 48px rgba(8, 10, 15, 0.12)"
                    }}
                    formatter={(value) => eur(Number(value))}
                    labelFormatter={(value) => `Snapshot ${value}`}
                  />
                  <Area
                    dataKey="price_avg_eur"
                    fill="url(#priceArea)"
                    stroke="#080a0f"
                    strokeWidth={2.4}
                    type="monotone"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            <dl className="metric-list">
              <div>
                <dt>Conditions</dt>
                <dd>{result.available_conditions.length}</dd>
              </div>
              <div>
                <dt>Strongest move</dt>
                <dd>{pct(result.strongest_change?.change_pct)}</dd>
              </div>
              <div>
                <dt>Direction</dt>
                <dd>{result.market_signal}</dd>
              </div>
            </dl>

            <div className="table-stack">
              {result.fair_prices.map((price) => (
                <div className="data-row" key={price.condition}>
                  <div>
                    <strong>{price.condition.replace("_", " ")}</strong>
                    <span>{price.confidence} confidence · {price.snapshot_count} snapshots</span>
                  </div>
                  <em>{eur(price.avg_eur)}</em>
                </div>
              ))}
            </div>
          </div>
        ) : null}
      </section>
    </div>
  );
}
