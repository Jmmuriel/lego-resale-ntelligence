"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { addPortfolioPosition, deletePortfolioPosition } from "@/lib/api";
import type { AddPositionRequest, PortfolioPosition } from "@/lib/types";

interface Props {
  positions: PortfolioPosition[];
}

const CONDITIONS = ["SEALED", "USED_COMPLETE", "USED_INCOMPLETE"] as const;

export default function AddPositionPanel({ positions }: Props) {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [form, setForm] = useState<AddPositionRequest>({
    set_id: "",
    set_name: "",
    condition: "USED_COMPLETE",
    quantity: 1,
    cost_basis_eur: 0,
    purchased_at: new Date().toISOString().slice(0, 10),
    notes: "",
    sell_target_eur: null
  });

  function update(field: keyof AddPositionRequest, value: string | number | null) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSaving(true);
    try {
      await addPortfolioPosition(form);
      setOpen(false);
      setForm({
        set_id: "",
        set_name: "",
        condition: "USED_COMPLETE",
        quantity: 1,
        cost_basis_eur: 0,
        purchased_at: new Date().toISOString().slice(0, 10),
        notes: "",
        sell_target_eur: null
      });
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save position");
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(id: number) {
    setDeleting(id);
    try {
      await deletePortfolioPosition(id);
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete position");
    } finally {
      setDeleting(null);
    }
  }

  return (
    <>
      {/* Delete buttons on existing positions */}
      {positions.map((pos) => (
        <div key={pos.item.id} style={{ display: "contents" }}>
          <button
            className="btn-danger"
            disabled={deleting === pos.item.id}
            onClick={() => handleDelete(pos.item.id)}
            aria-label={`Delete position ${pos.item.set_id}`}
          >
            {deleting === pos.item.id ? "…" : "×"}
          </button>
        </div>
      ))}

      {/* Add position toggle */}
      <div className="add-position-toggle">
        <button className="btn-ghost" onClick={() => { setOpen((o) => !o); setError(null); }}>
          {open ? "Cancel" : "+ Add position"}
        </button>
      </div>

      {open && (
        <form className="add-position-form" onSubmit={handleAdd}>
          <h3>Add position</h3>
          <div className="form-grid">
            <div className="form-field">
              <label className="form-label" htmlFor="set_id">Set ID</label>
              <input
                className="form-input"
                id="set_id"
                placeholder="75192"
                required
                value={form.set_id}
                onChange={(e) => update("set_id", e.target.value)}
              />
            </div>
            <div className="form-field">
              <label className="form-label" htmlFor="set_name">Set name</label>
              <input
                className="form-input"
                id="set_name"
                placeholder="Millennium Falcon"
                required
                value={form.set_name}
                onChange={(e) => update("set_name", e.target.value)}
              />
            </div>
            <div className="form-field">
              <label className="form-label" htmlFor="condition">Condition</label>
              <select
                className="form-input"
                id="condition"
                value={form.condition}
                onChange={(e) => update("condition", e.target.value)}
              >
                {CONDITIONS.map((c) => (
                  <option key={c} value={c}>{c.replace(/_/g, " ")}</option>
                ))}
              </select>
            </div>
            <div className="form-field">
              <label className="form-label" htmlFor="quantity">Quantity</label>
              <input
                className="form-input"
                id="quantity"
                min={1}
                required
                type="number"
                value={form.quantity}
                onChange={(e) => update("quantity", Number(e.target.value))}
              />
            </div>
            <div className="form-field">
              <label className="form-label" htmlFor="cost">Cost basis (€)</label>
              <input
                className="form-input"
                id="cost"
                min={0}
                required
                step="0.01"
                type="number"
                value={form.cost_basis_eur}
                onChange={(e) => update("cost_basis_eur", Number(e.target.value))}
              />
            </div>
            <div className="form-field">
              <label className="form-label" htmlFor="purchased_at">Purchase date</label>
              <input
                className="form-input"
                id="purchased_at"
                required
                type="date"
                value={form.purchased_at}
                onChange={(e) => update("purchased_at", e.target.value)}
              />
            </div>
            <div className="form-field">
              <label className="form-label" htmlFor="sell_target">Sell target (€, optional)</label>
              <input
                className="form-input"
                id="sell_target"
                min={0}
                step="0.01"
                type="number"
                value={form.sell_target_eur ?? ""}
                onChange={(e) => update("sell_target_eur", e.target.value ? Number(e.target.value) : null)}
              />
            </div>
            <div className="form-field">
              <label className="form-label" htmlFor="notes">Notes (optional)</label>
              <input
                className="form-input"
                id="notes"
                placeholder="e.g. bought sealed at Wallapop"
                value={form.notes ?? ""}
                onChange={(e) => update("notes", e.target.value)}
              />
            </div>
          </div>
          {error && <p className="error-text">{error}</p>}
          <div className="add-position-actions">
            <button className="btn-ghost" type="button" onClick={() => setOpen(false)}>
              Cancel
            </button>
            <button className="btn-primary" disabled={saving} type="submit">
              {saving ? "Saving…" : "Save position"}
            </button>
          </div>
        </form>
      )}
    </>
  );
}
