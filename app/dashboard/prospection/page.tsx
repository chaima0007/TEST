"use client";

import { useState } from "react";

// ─── Agent HERMES — prospection LinkedIn (Caelum) ─────────────────────────────
// HERMES PRÉPARE des brouillons ; l'envoi reste MANUEL par Chaima après
// relecture (PROTOCOLE §10). Aucun scraping, aucune automatisation d'envoi.

interface OutreachDraft {
  connectionNote: string;
  altConnectionNote: string;
  firstMessage: string;
  followUp: string;
  generatedBy: "heuristic" | "llm";
}

interface ProspectForm {
  firstName: string;
  company: string;
  sector: string;
  signal: string;
  city: string;
}

const EMPTY: ProspectForm = { firstName: "", company: "", sector: "", signal: "", city: "" };

// Petit bloc copiable : un brouillon + un bouton « Copier ».
function DraftBlock({
  label,
  hint,
  value,
}: {
  label: string;
  hint?: string;
  value: string;
}) {
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
        <div className="min-w-0">
          <p className="text-sm font-semibold text-slate-800 truncate">{label}</p>
          {hint && <p className="text-xs text-slate-500 truncate">{hint}</p>}
        </div>
        <button
          onClick={copy}
          className="ml-3 flex-shrink-0 text-xs font-medium px-3 py-1.5 rounded-md bg-blue-600 text-white hover:bg-blue-700 transition-colors"
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

export default function ProspectionPage() {
  const [form, setForm] = useState<ProspectForm>(EMPTY);
  const [draft, setDraft] = useState<OutreachDraft | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canSubmit = form.firstName.trim() !== "" && form.company.trim() !== "";

  const set = (k: keyof ProspectForm) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((f) => ({ ...f, [k]: e.target.value }));

  const generate = async () => {
    if (!canSubmit) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/hermes/draft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prospect: form }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        setError(data.error ?? "Erreur lors de la génération");
        setDraft(null);
      } else {
        setDraft(await res.json());
      }
    } catch {
      setError("Réseau indisponible");
      setDraft(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-slate-900">Prospection LinkedIn</h1>
        <p className="text-sm text-slate-600 mt-1">
          Agent <span className="font-semibold">HERMES</span> — brouillons personnalisés pour
          l&apos;offre « site web premium » à 500&nbsp;€. Vérité avant tout : aucune promesse
          invérifiable.
        </p>
      </header>

      {/* Garde-fou humain — visible, non décoratif (PROTOCOLE §10). */}
      <div className="flex gap-3 rounded-lg border border-amber-200 bg-amber-50 px-4 py-3">
        <span className="text-amber-600 text-lg leading-none">⚠</span>
        <p className="text-sm text-amber-800">
          HERMES <strong>prépare</strong> les messages ; il n&apos;envoie rien. Relis, ajuste,
          puis copie-colle manuellement dans LinkedIn. Aucune automatisation ni scraping.
        </p>
      </div>

      {/* Formulaire prospect */}
      <div className="bg-white rounded-lg border border-slate-200 p-5 space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <label className="block">
            <span className="text-sm font-medium text-slate-700">
              Prénom <span className="text-red-500">*</span>
            </span>
            <input
              value={form.firstName}
              onChange={set("firstName")}
              placeholder="Sophie"
              className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-slate-700">
              Entreprise <span className="text-red-500">*</span>
            </span>
            <input
              value={form.company}
              onChange={set("company")}
              placeholder="Cabinet Durand"
              className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-slate-700">Secteur</span>
            <input
              value={form.sector}
              onChange={set("sector")}
              placeholder="cabinet d'avocats"
              className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-slate-700">Ville</span>
            <input
              value={form.city}
              onChange={set("city")}
              placeholder="Bruxelles"
              className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </label>
          <label className="block md:col-span-2">
            <span className="text-sm font-medium text-slate-700">Signal observé</span>
            <input
              value={form.signal}
              onChange={set("signal")}
              placeholder="site daté et lent sur mobile"
              className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </label>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={generate}
            disabled={!canSubmit || loading}
            className="px-4 py-2 rounded-md bg-blue-600 text-white text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? "Génération…" : "Générer les brouillons"}
          </button>
          {!canSubmit && (
            <span className="text-xs text-slate-500">Prénom et entreprise requis.</span>
          )}
          {error && <span className="text-xs text-red-600">{error}</span>}
        </div>
      </div>

      {/* Résultat */}
      {draft && (
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-slate-900">Brouillons</h2>
            <span className="text-xs text-slate-500">
              Rédigé par&nbsp;
              {draft.generatedBy === "llm" ? "Claude" : "règles déterministes (heuristique)"}
            </span>
          </div>
          <DraftBlock
            label="Note de connexion"
            hint="À joindre à la demande de connexion (courte)."
            value={draft.connectionNote}
          />
          <DraftBlock
            label="Note de connexion — variante A/B"
            hint="Alternative à tester."
            value={draft.altConnectionNote}
          />
          <DraftBlock
            label="1er message"
            hint="Après acceptation de la connexion."
            value={draft.firstMessage}
          />
          <DraftBlock
            label="Relance"
            hint="Si pas de réponse — polie, sans insistance."
            value={draft.followUp}
          />
        </div>
      )}
    </div>
  );
}
