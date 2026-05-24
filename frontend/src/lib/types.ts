export type Signal = "GREEN" | "YELLOW" | "RED";
export type Condition = "SEALED" | "USED_COMPLETE" | "USED_INCOMPLETE" | "UNKNOWN";
export type Confidence = "HIGH" | "MEDIUM" | "LOW" | "NONE";
export type HoldSellSignal = "HOLD" | "NEUTRAL" | "SELL";
export type MarketTrend = "BULLISH" | "NEUTRAL" | "BEARISH";
export type WatchlistStatus = "analyzed" | "watching" | "discarded" | "bought";

export interface MarketContext {
  fair_price_eur: number | null;
  fair_price_source: "dynamic_history" | "manual_reference" | "unavailable";
  price_confidence: Confidence;
  anomaly_score: number | null;
  snapshot_count: number;
  days_since_update: number | null;
}

export interface AnalysisResult {
  url: string;
  marketplace: string | null;
  set_id: string | null;
  condition: Condition | null;
  asking_price_eur: number | null;
  shipping_eur: number | null;
  fair_price_eur: number | null;
  gross_margin_eur: number | null;
  net_margin_eur: number | null;
  opportunity_score: number | null;
  category: Signal | null;
  risk_flags: string[];
  notes: string | null;
  market_context: MarketContext;
}

export interface WatchlistRecord {
  id: number;
  created_at: string;
  status: WatchlistStatus;
  url: string;
  marketplace: string | null;
  set_id: string | null;
  condition: Condition | null;
  asking_price_eur: number | null;
  shipping_eur: number | null;
  fair_price_eur: number | null;
  gross_margin_eur: number | null;
  net_margin_eur: number | null;
  opportunity_score: number | null;
  category: Signal | null;
  risk_flags: string[];
  notes: string | null;
}

export interface PriceChange {
  set_id: string;
  condition: Condition;
  start_avg_eur: number;
  end_avg_eur: number;
  change_eur: number;
  change_pct: number;
}

export interface FairPrice {
  set_id: string;
  condition: Condition | string;
  avg_eur: number | null;
  min_eur: number | null;
  max_eur: number | null;
  confidence: Confidence;
  sample_count: number;
  snapshot_count: number;
  days_since_update: number | null;
}

export interface PriceSnapshot {
  set_id: string;
  condition: Condition | string;
  source: string;
  price_min_eur: number;
  price_avg_eur: number;
  price_max_eur: number;
  sample_count: number;
  recorded_at: string;
}

export interface SetIntelligence {
  set_id: string;
  available_conditions: string[];
  fair_prices: FairPrice[];
  strongest_change: PriceChange | null;
  market_signal: "UP" | "DOWN" | "STABLE" | "UNKNOWN";
  summary: string;
}

export interface DataQualityIssue {
  severity: "error" | "warning";
  code: string;
  message: string;
}

export interface DataQualityMetrics {
  catalog_sets: number;
  catalog_candidate_sets: number;
  catalog_plus_candidates: number;
  target_catalog_sets: number;
  price_snapshots: number;
  priced_sets: number;
  candidate_ready_for_promotion: number;
  portfolio_items: number;
  portfolio_sets: number;
  sets_with_3_plus_snapshots: number;
  sets_with_5_plus_snapshots: number;
  unpriced_catalog_sets: string[];
  active_catalog_coverage_pct: number;
  candidate_catalog_coverage_pct: number;
  pricing_coverage_pct: number;
  active_catalog_verified_sets: number;
  active_catalog_verified_pct: number;
  active_catalog_evidence_started_sets: number;
  active_catalog_blocked_sets: number;
  market_data_source_status: "seed_demo" | "partially_verified" | "verified";
}

export interface DataQualityReport {
  ok: boolean;
  status: "ready" | "needs_research" | "blocked";
  summary: string;
  metrics: DataQualityMetrics;
  warnings: DataQualityIssue[];
  errors: DataQualityIssue[];
}

export interface CatalogCandidate {
  set_id: string;
  name: string;
  theme: string;
  reason: string;
  validation_status: string;
  readiness: CandidateReadiness;
}

export interface CandidateReadiness {
  completed_checks: number;
  required_checks: number;
  ready_for_promotion: boolean;
  missing_requirements: string[];
  metadata_source_count: number;
  price_source_count: number;
  price_snapshot_count: number;
}

export interface ActiveCatalogEvidence {
  set_id: string;
  name: string;
  theme: string | null;
  verification_status: string;
  audited_at: string | null;
  audit_summary: string;
  recommended_action: string | null;
  catalog_mismatches: Array<Record<string, unknown>>;
  metadata_source_count: number;
  price_source_count: number;
  price_snapshot_count: number;
  ready_for_verified: boolean;
  missing_requirements: string[];
}

export interface PortfolioItem {
  id: number;
  set_id: string;
  set_name: string;
  condition: Condition;
  quantity: number;
  cost_basis_eur: number;
  purchased_at: string;
  status: "HOLDING" | "LISTED" | "SOLD";
  notes: string | null;
  sell_target_eur: number | null;
}

export interface PositionPnL {
  cost_basis_eur: number;
  current_fair_value_eur: number;
  net_if_sold_eur: number;
  unrealized_pnl_eur: number;
  unrealized_pnl_pct: number;
  annualized_return_pct: number;
  days_held: number;
  price_confidence: Confidence;
  hold_sell_signal: HoldSellSignal;
  hold_sell_reason: string;
}

export interface PortfolioPosition {
  item: PortfolioItem;
  pnl: PositionPnL;
}

export interface PortfolioSummary {
  total_cost_basis_eur: number;
  total_current_fair_value_eur: number;
  total_net_if_sold_eur: number;
  total_unrealized_pnl_eur: number;
  total_unrealized_pnl_pct: number;
  open_positions: number;
  dominant_signal: HoldSellSignal;
  top_position_id: number | null;
  worst_position_id: number | null;
  positions: PortfolioPosition[];
}

export interface AddPositionRequest {
  set_id: string;
  set_name: string;
  condition: Condition;
  quantity: number;
  cost_basis_eur: number;
  purchased_at: string;
  status?: "HOLDING" | "LISTED" | "SOLD";
  notes?: string;
  sell_target_eur?: number | null;
}

export interface MarketBriefing {
  period_start: string;
  period_end: string;
  briefing_text: string;
  key_opportunities: string[];
  market_trend: MarketTrend;
  generated_at: string;
  model_version: string;
  token_count: number;
  used_llm: boolean;
}
