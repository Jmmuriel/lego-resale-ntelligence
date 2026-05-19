import SetLookup from "@/components/SetLookup";

export default function SetIntelligencePage() {
  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <h1>Set Intelligence</h1>
          <p>Fair price, confidence, and recent price trend for a single retired set.</p>
        </div>
      </header>
      <SetLookup />
    </div>
  );
}
