import AnalyzeWorkbench from "@/components/AnalyzeWorkbench";

export default function AnalyzePage() {
  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <h1>Analyze Listing</h1>
          <p>Paste a URL — V2 adds dynamic fair price, confidence, and anomaly context.</p>
        </div>
      </header>
      <AnalyzeWorkbench />
    </div>
  );
}
