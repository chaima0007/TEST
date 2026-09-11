"use client";

import { useState } from "react";

// ─── Agent BOUSSOLE — qualification / triage de leads (Caelum) ───────────────
// BOUSSOLE situe le prospect dans l'entonnoir (déterministe, transparent) et
// RECOMMANDE la prochaine action. La décision reste humaine (§10).

type Timing = "now" | "soon" | "later" | "unknown";
type WebsiteState = "none" | "outdated" | "recent" | "unknown";

interface Qualification {
  fit: "ÉLEVÉE" | "MODÉRÉE" | "FAIBLE";
  priority: "haute" | "moyenne" | "basse";
  score: number;
  maxScore: number;
  reasons: string[];
  questions: string[];
  recommendation: string;
}

interface LeadForm {
  firstName: string;
  company: string;
  sector: string;
  reply: string;
  needClear: boolean;
  budgetSignal: boolean;
  timing: Timing;
  decisionMaker: boolean;
  hasWebsite: WebsiteState;
}

const EMPTY: LeadForm = {
  firstName: "",
  company: "",
  sector: "",
  reply: "",
  needClear: false,
  budgetSignal: false,
  timing: "unknown",
  decisionMaker: false,
  hasWebsite: "unknown",
};

const fitStyle: Record<string, string> = {
  ÉLEVÉE: "bg-green-50 text-[#107C10] border-green-200",
  MODÉRÉE: "bg-amber-50 text-amber-700 border-amber-200",
  FAIBLE: "bg-slate-100 text-slate-500 border-slate-200",
};

export default function QualificationPage() {
  const [form, setForm] = useState<LeadForm>(EMPTY);
  const [result, setResult] = useState<Qualification | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canSubmit = form.firstName.trim() !== "" && form.company.trim() !== "";

  const text = (k: "firstName" | "company" | "sector" | "reply") =>
    (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) =>
      setForm((f) => ({ ...f, [k]: e.target.value }));
  const bool = (k: "needClear" | "budgetSignal" | "decisionMaker") =>
    (e: React.ChangeEvent<HTMLInputElement>) => setForm((f) => ({ ...f, [k]: e.target.checked }));

  const qualify = async () => {
    if (!canSubmit) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/boussole/qualify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lead: form }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        setError(data.error ?? "Erreur lors de la qualification");
        setResult(null);
      } else {
        setResult(await res.json());
      }
    } catch {
      setError("Réseau indisponible");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const inputCls =
    "mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500";

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-slate-900">Qualification de lead</h1>
        <p className="text-sm text-slate-600 mt-1">
          Agent <span className="font-semibold">BOUSSOLE</span> — situe le prospect dans
          l&apos;entonnoir (score déterministe, transparent) et recommande la prochaine action,
          entre HERMES (prospection) et PACTE (devis).
        </p>
      </header>

      <div className="flex gap-3 rounded-lg border border-slate-200 bg-slate-50 px-4 py-3">
        <span className="text-slate-500 text-lg leading-none">🧭</span>
        <p className="text-sm text-slate-700">
          Score de <strong>règles explicites</strong> (chaque point est justifié), sans boîte
          noire ni pourcentage inventé. BOUSSOLE <strong>recommande</strong> ; la décision reste
          la tienne.
        </p>
      </div>

      {/* Formulaire lead */}
      <div className="bg-white rounded-lg border border-slate-200 p-5 space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <label className="block">
            <span className="text-sm font-medium text-slate-700">
              Prénom <span className="text-red-500">*</span>
            </span>
            <input value={form.firstName} onChange={text("firstName")} placeholder="Sophie" className={inputCls} />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-slate-700">
              Entreprise <span className="text-red-500">*</span>
            </span>
            <input value={form.company} onChange={text("company")} placeholder="Cabinet Durand" className={inputCls} />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-slate-700">Secteur</span>
            <input value={form.sector} onChange={text("sector")} placeholder="cabinet d'avocats" className={inputCls} />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-slate-700">Échéance</span>
            <select
              value={form.timing}
              onChange={(e) => setForm((f) => ({ ...f, timing: e.target.value as Timing }))}
              className={inputCls}
            >
              <option value="unknown">Inconnue</option>
              <option value="now">Immédiate</option>
              <option value="soon">Proche</option>
              <option value="later">Plus tard</option>
            </select>
          </label>
          <label className="block">
            <span className="text-sm font-medium text-slate-700">Site actuel</span>
            <select
              value={form.hasWebsite}
              onChange={(e) => setForm((f) => ({ ...f, hasWebsite: e.target.value as WebsiteState }))}
              className={inputCls}
            >
              <option value="unknown">Inconnu</option>
              <option value="none">Aucun</option>
              <option value="outdated">Daté</option>
              <option value="recent">Récent</option>
            </select>
          </label>
          <label className="block md:col-span-2">
            <span className="text-sm font-medium text-slate-700">
              Message du prospect (facultatif — sert d&apos;indice)
            </span>
            <textarea
              value={form.reply}
              onChange={text("reply")}
              rows={2}
              placeholder="Bonjour, j'aimerais refaire mon site, quel est votre tarif ?"
              className={inputCls}
            />
          </label>
        </div>

        <div className="flex flex-wrap gap-4 pt-1">
          <label className="flex items-center gap-2 text-sm text-slate-700">
            <input type="checkbox" checked={form.needClear} onChange={bool("needClear")} /> Besoin clair
          </label>
          <label className="flex items-center gap-2 text-sm text-slate-700">
            <input type="checkbox" checked={form.budgetSignal} onChange={bool("budgetSignal")} /> Signal de budget
          </label>
          <label className="flex items-center gap-2 text-sm text-slate-700">
            <input type="checkbox" checked={form.decisionMaker} onChange={bool("decisionMaker")} /> Décideur
          </label>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={qualify}
            disabled={!canSubmit || loading}
            className="px-4 py-2 rounded-md bg-blue-600 text-white text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? "Analyse…" : "Qualifier"}
          </button>
          {!canSubmit && <span className="text-xs text-slate-500">Prénom et entreprise requis.</span>}
          {error && <span className="text-xs text-red-600">{error}</span>}
        </div>
      </div>

      {/* Résultat */}
      {result && (
        <div className="space-y-4">
          <div className={`rounded-lg border p-4 flex items-center justify-between ${fitStyle[result.fit]}`}>
            <div>
              <p className="text-xs uppercase tracking-wide opacity-70">Fit</p>
              <p className="text-xl font-bold">{result.fit}</p>
            </div>
            <div className="text-right">
              <p className="text-xs uppercase tracking-wide opacity-70">Score</p>
              <p className="text-xl font-bold">{result.score} / {result.maxScore}</p>
            </div>
          </div>

          <div className="border border-slate-200 rounded-lg bg-white p-5 space-y-4 text-sm text-slate-700">
            <div>
              <p className="font-semibold text-slate-800">Pourquoi ce score</p>
              <ul className="list-disc pl-5 mt-1 space-y-0.5">
                {result.reasons.map((r, i) => <li key={i}>{r}</li>)}
              </ul>
            </div>
            <div>
              <p className="font-semibold text-slate-800">Questions à poser</p>
              <ul className="list-disc pl-5 mt-1 space-y-0.5">
                {result.questions.map((q, i) => <li key={i}>{q}</li>)}
              </ul>
            </div>
            <div className="rounded-md bg-blue-50 border border-blue-100 px-4 py-3">
              <p className="font-semibold text-slate-800">Recommandation</p>
              <p className="mt-0.5">{result.recommendation}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
