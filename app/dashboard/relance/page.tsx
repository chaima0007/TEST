"use client";

import { useState } from "react";

// ─── Agent RELANCE — relance de devis (Caelum) ───────────────────────────────
// RELANCE PRÉPARE une séquence de relance après un devis sans réponse.
// L'envoi reste MANUEL par Chaima (§10). Relancer sans harceler.

interface FollowUp {
  label: string;
  body: string;
}
interface FollowUpSequence {
  messages: FollowUp[];
  generatedBy: "heuristic" | "llm";
}

type Objection = "none" | "price" | "timing" | "trust";

interface QuoteForm {
  firstName: string;
  company: string;
  service: string;
  objection: Objection;
}

const EMPTY: QuoteForm = { firstName: "", company: "", service: "", objection: "none" };

function CopyBlock({ label, value }: { label: string; value: string }) {
  const [copied, setCopied] = useState(false);
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(value);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      setCopied(false);
    }
  };
  return (
    <div className="border border-slate-200 rounded-lg bg-white overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2 bg-slate-50 border-b border-slate-200">
        <p className="text-sm font-semibold text-slate-800">{label}</p>
        <button
          onClick={copy}
          className="text-xs font-medium px-3 py-1.5 rounded-md bg-blue-600 text-white hover:bg-blue-700 transition-colors"
        >
          {copied ? "Copié ✓" : "Copier"}
        </button>
      </div>
      <pre className="px-4 py-3 text-sm text-slate-700 whitespace-pre-wrap font-sans leading-relaxed">
        {value}
      </pre>
    </div>
  );
}

export default function RelancePage() {
  const [form, setForm] = useState<QuoteForm>(EMPTY);
  const [seq, setSeq] = useState<FollowUpSequence | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canSubmit = form.firstName.trim() !== "" && form.company.trim() !== "";

  const generate = async () => {
    if (!canSubmit) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/relance/draft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ quote: form }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        setError(data.error ?? "Erreur lors de la génération");
        setSeq(null);
      } else {
        setSeq(await res.json());
      }
    } catch {
      setError("Réseau indisponible");
      setSeq(null);
    } finally {
      setLoading(false);
    }
  };

  const inputCls =
    "mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500";

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-slate-900">Relance de devis</h1>
        <p className="text-sm text-slate-600 mt-1">
          Agent <span className="font-semibold">RELANCE</span> — séquence de relance après un
          devis (PACTE) resté sans réponse. Relancer sans harceler.
        </p>
      </header>

      <div className="flex gap-3 rounded-lg border border-amber-200 bg-amber-50 px-4 py-3">
        <span className="text-amber-600 text-lg leading-none">⚠</span>
        <p className="text-sm text-amber-800">
          RELANCE <strong>prépare</strong> les messages ; tu les envoies à la main, à ton rythme.
          Aucune fausse urgence, aucune remise inventée — la clôture rend poliment la main au
          prospect.
        </p>
      </div>

      <div className="bg-white rounded-lg border border-slate-200 p-5 space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <label className="block">
            <span className="text-sm font-medium text-slate-700">
              Prénom <span className="text-red-500">*</span>
            </span>
            <input
              value={form.firstName}
              onChange={(e) => setForm((f) => ({ ...f, firstName: e.target.value }))}
              placeholder="Sophie"
              className={inputCls}
            />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-slate-700">
              Entreprise <span className="text-red-500">*</span>
            </span>
            <input
              value={form.company}
              onChange={(e) => setForm((f) => ({ ...f, company: e.target.value }))}
              placeholder="Cabinet Durand"
              className={inputCls}
            />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-slate-700">Service proposé</span>
            <input
              value={form.service}
              onChange={(e) => setForm((f) => ({ ...f, service: e.target.value }))}
              placeholder="site web premium (défaut)"
              className={inputCls}
            />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-slate-700">Objection évoquée</span>
            <select
              value={form.objection}
              onChange={(e) => setForm((f) => ({ ...f, objection: e.target.value as Objection }))}
              className={inputCls}
            >
              <option value="none">Aucune / pas de réponse</option>
              <option value="price">Prix / budget</option>
              <option value="timing">Timing</option>
              <option value="trust">Confiance / preuve</option>
            </select>
          </label>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={generate}
            disabled={!canSubmit || loading}
            className="px-4 py-2 rounded-md bg-blue-600 text-white text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? "Génération…" : "Générer la séquence"}
          </button>
          {!canSubmit && <span className="text-xs text-slate-500">Prénom et entreprise requis.</span>}
          {error && <span className="text-xs text-red-600">{error}</span>}
        </div>
      </div>

      {seq && (
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-slate-900">Séquence de relance</h2>
            <span className="text-xs text-slate-500">
              Rédigé par&nbsp;
              {seq.generatedBy === "llm" ? "Claude" : "règles déterministes (heuristique)"}
            </span>
          </div>
          {seq.messages.map((m, i) => (
            <CopyBlock key={i} label={m.label} value={m.body} />
          ))}
        </div>
      )}
    </div>
  );
}
