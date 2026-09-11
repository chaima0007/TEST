"use client";

import { useState } from "react";

// ─── Agent PACTE — devis / proposition commerciale (Caelum) ──────────────────
// PACTE PRÉPARE le devis ; l'envoi et la signature restent HUMAINS (§10/§11).
// Modalités de facturation « À CONFIRMER » : Caelum n'a pas encore d'inscription
// légale ni de paiement en ligne — Chaima complète avant tout engagement.

interface Proposal {
  subject: string;
  greeting: string;
  understanding: string;
  scope: string[];
  outOfScope: string[];
  timeline: string;
  priceLine: string;
  terms: string[];
  nextStep: string;
  generatedBy: "heuristic" | "llm";
}

interface LeadForm {
  firstName: string;
  company: string;
  sector: string;
  need: string;
  city: string;
}

const EMPTY: LeadForm = { firstName: "", company: "", sector: "", need: "", city: "" };

// Assemble le devis en texte brut copiable (à coller dans un mail ou un PDF).
function toPlainText(p: Proposal): string {
  const bullets = (items: string[]) => items.map((s) => `  • ${s}`).join("\n");
  return [
    `Objet : ${p.subject}`,
    ``,
    p.greeting,
    ``,
    p.understanding,
    ``,
    `Ce qui est inclus :`,
    bullets(p.scope),
    ``,
    `Hors périmètre :`,
    bullets(p.outOfScope),
    ``,
    p.timeline,
    ``,
    `Prix : ${p.priceLine}`,
    ``,
    `Modalités :`,
    bullets(p.terms),
    ``,
    p.nextStep,
  ].join("\n");
}

export default function DevisPage() {
  const [form, setForm] = useState<LeadForm>(EMPTY);
  const [proposal, setProposal] = useState<Proposal | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const canSubmit = form.firstName.trim() !== "" && form.company.trim() !== "";

  const set = (k: keyof LeadForm) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((f) => ({ ...f, [k]: e.target.value }));

  const generate = async () => {
    if (!canSubmit) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/pacte/draft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lead: form }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        setError(data.error ?? "Erreur lors de la génération");
        setProposal(null);
      } else {
        setProposal(await res.json());
      }
    } catch {
      setError("Réseau indisponible");
      setProposal(null);
    } finally {
      setLoading(false);
    }
  };

  const copyAll = async () => {
    if (!proposal) return;
    try {
      await navigator.clipboard.writeText(toPlainText(proposal));
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      setCopied(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-slate-900">Devis / proposition</h1>
        <p className="text-sm text-slate-600 mt-1">
          Agent <span className="font-semibold">PACTE</span> — transforme un lead qualifié en
          proposition commerciale structurée pour l&apos;offre Caelum. Sobre et factuel : aucune
          promesse invérifiable.
        </p>
      </header>

      {/* Garde-fou humain — non décoratif (§10/§11). */}
      <div className="flex gap-3 rounded-lg border border-amber-200 bg-amber-50 px-4 py-3">
        <span className="text-amber-600 text-lg leading-none">⚠</span>
        <p className="text-sm text-amber-800">
          PACTE <strong>rédige</strong> le devis ; l&apos;envoi et la signature restent à toi.
          Les <strong>modalités de facturation sont « À CONFIRMER »</strong> — à compléter selon
          ton statut (inscription en cours, pas de paiement en ligne pour l&apos;instant).
        </p>
      </div>

      {/* Formulaire lead */}
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
            <span className="text-sm font-medium text-slate-700">Besoin exprimé</span>
            <input
              value={form.need}
              onChange={set("need")}
              placeholder="avoir un site vitrine clair avec un formulaire de contact"
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
            {loading ? "Génération…" : "Générer le devis"}
          </button>
          {!canSubmit && (
            <span className="text-xs text-slate-500">Prénom et entreprise requis.</span>
          )}
          {error && <span className="text-xs text-red-600">{error}</span>}
        </div>
      </div>

      {/* Résultat */}
      {proposal && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-slate-900">Proposition</h2>
            <div className="flex items-center gap-3">
              <span className="text-xs text-slate-500">
                Rédigé par&nbsp;
                {proposal.generatedBy === "llm" ? "Claude" : "règles déterministes (heuristique)"}
              </span>
              <button
                onClick={copyAll}
                className="text-xs font-medium px-3 py-1.5 rounded-md bg-blue-600 text-white hover:bg-blue-700 transition-colors"
              >
                {copied ? "Copié ✓" : "Copier le devis complet"}
              </button>
            </div>
          </div>

          <article className="border border-slate-200 rounded-lg bg-white p-5 space-y-4 text-sm text-slate-700 leading-relaxed">
            <p className="font-semibold text-slate-900">{proposal.subject}</p>
            <p>{proposal.greeting}</p>
            <p>{proposal.understanding}</p>

            <div>
              <p className="font-semibold text-slate-800">Ce qui est inclus</p>
              <ul className="list-disc pl-5 mt-1 space-y-0.5">
                {proposal.scope.map((s, i) => <li key={i}>{s}</li>)}
              </ul>
            </div>

            <div>
              <p className="font-semibold text-slate-800">Hors périmètre</p>
              <ul className="list-disc pl-5 mt-1 space-y-0.5 text-slate-600">
                {proposal.outOfScope.map((s, i) => <li key={i}>{s}</li>)}
              </ul>
            </div>

            <p>{proposal.timeline}</p>
            <p className="font-semibold text-slate-900">{proposal.priceLine}</p>

            <div>
              <p className="font-semibold text-slate-800">Modalités</p>
              <ul className="list-disc pl-5 mt-1 space-y-0.5">
                {proposal.terms.map((s, i) => <li key={i}>{s}</li>)}
              </ul>
            </div>

            <p className="text-slate-900">{proposal.nextStep}</p>
          </article>
        </div>
      )}
    </div>
  );
}
