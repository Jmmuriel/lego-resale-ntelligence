import WatchlistDesk from "@/components/WatchlistDesk";
import { getWatchlist } from "@/lib/api";
import { DEMO_ALLOW_WRITES } from "@/lib/demo";

export const dynamic = "force-dynamic";

export default async function WatchlistPage() {
  const records = await getWatchlist(50);

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <h1>Watchlist</h1>
          <p>
            {DEMO_ALLOW_WRITES
              ? "Saved opportunities — move them through the resale workflow."
              : "Saved opportunities and their resale status."}
          </p>
        </div>
        <div className="page-header-actions">
          <span style={{ color: "var(--muted)", fontSize: "13px" }}>
            {records.length} saved
          </span>
        </div>
      </header>
      <WatchlistDesk initialRecords={records} />
    </div>
  );
}
