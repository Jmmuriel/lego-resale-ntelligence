import type {
  ActiveCatalogEvidence,
  AddPositionRequest,
  AnalysisResult,
  CatalogCandidate,
  DataQualityReport,
  MarketBriefing,
  PortfolioItem,
  PortfolioSummary,
  PriceChange,
  PriceSnapshot,
  SetIntelligence,
  WatchlistRecord,
  WatchlistStatus
} from "./types";

const LOCAL_API_URL = "http://127.0.0.1:8000";
const PUBLIC_API_URL = "https://lego-resale-ntelligence-production.up.railway.app";

function getApiUrl(): string {
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }

  if (process.env.VERCEL === "1") {
    return PUBLIC_API_URL;
  }

  if (typeof window !== "undefined") {
    const hostname = window.location.hostname;
    if (hostname === "localhost" || hostname === "127.0.0.1") {
      return LOCAL_API_URL;
    }
    return PUBLIC_API_URL;
  }

  return LOCAL_API_URL;
}

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;

  try {
    response = await fetch(`${getApiUrl()}${path}`, {
      ...init,
      headers: {
        "Content-Type": "application/json",
        ...init?.headers
      },
      cache: "no-store"
    });
  } catch (error) {
    throw new ApiError(
      0,
      "Could not reach the LEGO Resale Intelligence API. Please try the demo opportunity, or retry in a moment if the Railway backend is waking up."
    );
  }

  if (!response.ok) {
    const detail = await response.text();
    throw new ApiError(response.status, detail || response.statusText);
  }

  return response.json() as Promise<T>;
}

export function analyzeUrl(url: string): Promise<AnalysisResult> {
  return apiFetch<AnalysisResult>("/api/analyze", {
    method: "POST",
    body: JSON.stringify({ url })
  });
}

export function analyzeDemoOpportunity(): Promise<AnalysisResult> {
  return apiFetch<AnalysisResult>("/api/analyze/demo", {
    method: "POST"
  });
}

export function saveAnalysisToWatchlist(
  analysis: AnalysisResult,
  status: WatchlistStatus = "watching"
): Promise<WatchlistRecord> {
  return apiFetch<WatchlistRecord>(`/api/watchlist?listing_status=${encodeURIComponent(status)}`, {
    method: "POST",
    body: JSON.stringify(analysis)
  });
}

export function getWatchlist(limit = 30): Promise<WatchlistRecord[]> {
  return apiFetch<WatchlistRecord[]>(`/api/watchlist?limit=${limit}`);
}

export function updateWatchlistStatus(
  recordId: number,
  status: WatchlistStatus
): Promise<WatchlistRecord> {
  return apiFetch<WatchlistRecord>(`/api/watchlist/${recordId}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status })
  });
}

export function getMarketTrends(days = 120): Promise<PriceChange[]> {
  return apiFetch<PriceChange[]>(`/api/market/trends?days=${days}`);
}

export function getDataQualityReport(): Promise<DataQualityReport> {
  return apiFetch<DataQualityReport>("/api/market/data-quality");
}

export function getCatalogCandidates(): Promise<CatalogCandidate[]> {
  return apiFetch<CatalogCandidate[]>("/api/market/catalog-candidates");
}

export function getActiveCatalogEvidence(): Promise<ActiveCatalogEvidence[]> {
  return apiFetch<ActiveCatalogEvidence[]>("/api/market/active-evidence");
}

export function getSetIntelligence(setId: string, days = 180): Promise<SetIntelligence> {
  return apiFetch<SetIntelligence>(`/api/market/set/${encodeURIComponent(setId)}?days=${days}`);
}

export function getSetPriceHistory(
  setId: string,
  condition = "USED_COMPLETE",
  days = 180
): Promise<PriceSnapshot[]> {
  const params = new URLSearchParams({ condition, days: String(days) });
  return apiFetch<PriceSnapshot[]>(
    `/api/market/history/${encodeURIComponent(setId)}?${params.toString()}`
  );
}

export function getPortfolio(): Promise<PortfolioSummary> {
  return apiFetch<PortfolioSummary>("/api/portfolio");
}

export function addPortfolioPosition(data: AddPositionRequest): Promise<PortfolioItem> {
  return apiFetch<PortfolioItem>("/api/portfolio", {
    method: "POST",
    body: JSON.stringify(data)
  });
}

export function deletePortfolioPosition(id: number): Promise<{ ok: boolean }> {
  return apiFetch<{ ok: boolean }>(`/api/portfolio/${id}`, {
    method: "DELETE"
  });
}

export function getLatestBriefing(): Promise<MarketBriefing[]> {
  return apiFetch<MarketBriefing[]>("/api/briefings");
}
