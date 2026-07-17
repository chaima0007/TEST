"use client";

import Link from "next/link";
import { useState } from "react";

// Simulateur « Quelle aide pour mon projet ? » — Caelum (projet ENTREPRISES, séparé de La Loi Avec Moi).
// 4 questions → liste d'aides + marchés publics pertinents, sourcés. Logique alignée sur
// scripts/appels_projets_agent.py et data/caelum/appels_projets.json.

type Aide = { nom: string; why: string; url: string };

const REGIONS = [
  { id: "wallonie", label: "Wallonie" },
  { id: "bruxelles", label: "Bruxelles" },
  { id: "flandre", label: "Flandre" },
];
const TAILLES = [
  { id: "independant", label: "Indépendant / TPE" },
  { id: "pme", label: "PME (< 250)" },
  { id: "grande", label: "Grande entreprise" },
];
const BESOINS = [
  { id: "numerique", label: "Digitalisation" },
  { id: "cybersecurite", label: "Cybersécurité" },
  { id: "conformite", label: "Conformité (RGPD, normes)" },
  { id: "innovation", label: "Innovation / R&D" },
  { id: "marches_publics", label: "Gagner des marchés publics" },
];

function recommander(region: string, taille: string, besoin: string): Aide[] {
  const reco: Aide[] = [];

  if (region === "wallonie")
    reco.push({
      nom: "Chèques-entreprises (Wallonie)",
      why: "Maturité numérique, cybersécurité, conseil stratégique — prise en charge d'une part des honoraires de prestataires agréés.",
      url: "https://www.digitalwallonia.be/fr/publications/aides-transformation-numerique/",
    });
  else if (region === "bruxelles")
    reco.push({
      nom: "Innoviris (Bruxelles)",
      why: "Recherche & innovation. ⚠️ Budget limité en 2026 : on vérifie la disponibilité réelle avant de vous engager.",
      url: "https://innoviris.brussels",
    });
  else if (region === "flandre")
    reco.push({
      nom: "VLAIO (Flandre)",
      why: "Subsides innovation / numérique. Réforme 2026 : le volet conseil est recentré sur la cybersécurité.",
      url: "https://www.vlaio.be",
    });

  if (besoin === "innovation" && (taille === "pme" || taille === "grande"))
    reco.push({
      nom: "Horizon Europe / EIC Accelerator (UE)",
      why: "Innovation deep-tech. Montants élevés, très compétitif, souvent en consortium.",
      url: "https://eic.ec.europa.eu",
    });

  if (besoin === "numerique" || besoin === "cybersecurite")
    reco.push({
      nom: "Digital Europe / EDIH (UE)",
      why: "Pôles d'innovation numérique : accompagnement des PME sur la transfo numérique, l'IA et la cyber.",
      url: "https://digital-strategy.ec.europa.eu",
    });

  if (besoin === "marches_publics" || taille === "pme" || taille === "grande") {
    reco.push({
      nom: "e-Procurement (publicprocurement.be)",
      why: "Plateforme fédérale officielle des marchés publics belges. Gratuite. On vise les LOTS réservés aux PME.",
      url: "https://bosa.belgium.be/fr/applications/e-procurement",
    });
    reco.push({
      nom: "TED — Tenders Electronic Daily (UE)",
      why: "Marchés publics européens. Seuils revus à la baisse = davantage d'opportunités publiées.",
      url: "https://ted.europa.eu",
    });
  }

  if (besoin === "conformite" || besoin === "marches_publics")
    reco.push({
      nom: "🔑 Conformité = clé des marchés publics",
      why: "Le RGPD s'applique à TOUS les marchés publics et la cybersécurité est de plus en plus exigée. Être conforme grâce à Caelum vous rend éligible et mieux noté.",
      url: "https://marchespublics.wallonie.be",
    });

  return reco;
}

export default function AppelsProjetsPage() {
  const [region, setRegion] = useState("");
  const [taille, setTaille] = useState("");
  const [besoin, setBesoin] = useState("");
  const [resultats, setResultats] = useState<Aide[] | null>(null);

  const pret = region && taille && besoin;

  function lancer() {
    if (!pret) return;
    setResultats(recommander(region, taille, besoin));
  }

  function Choix({
    titre,
    options,
    valeur,
    set,
  }: {
    titre: string;
    options: { id: string; label: string }[];
    valeur: string;
    set: (v: string) => void;
  }) {
    return (
      <div>
        <h3 className="font-semibold text-slate-800 mb-3">{titre}</h3>
        <div className="flex flex-wrap gap-2">
          {options.map((o) => (
            <button
              key={o.id}
              type="button"
              onClick={() => {
                set(o.id);
                setResultats(null);
              }}
              className={
                "px-4 py-2 rounded-full border text-sm font-medium transition-colors " +
                (valeur === o.id
                  ? "bg-indigo-600 border-indigo-600 text-white"
                  : "bg-white border-slate-300 text-slate-700 hover:border-indigo-400")
              }
            >
              {o.label}
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <span className="font-bold text-lg tracking-tight">Caelum</span>
          </Link>
          <Link
            href="/contact"
            className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold px-5 py-2.5 rounded-lg transition-colors"
          >
            Demander un devis
          </Link>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(37,99,235,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Appels à projets & financements
          </span>
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight leading-tight">
            Quelle aide pour
            <span className="block bg-gradient-to-r from-indigo-300 to-sky-300 bg-clip-text text-transparent">
              votre projet ?
            </span>
          </h1>
          <p className="text-lg text-slate-300 mt-6 leading-relaxed">
            Subventions, chèques-entreprises, marchés publics… On repère ce à quoi vous êtes éligible,
            et on s'occupe du dossier — automatiquement quand c'est possible, avec un expert quand il le faut.
          </p>
        </div>
      </section>

      {/* Simulateur */}
      <section className="py-16 px-6 max-w-3xl mx-auto">
        <div className="bg-white rounded-2xl border border-slate-200 p-7 space-y-7 shadow-sm">
          <Choix titre="1. Votre région" options={REGIONS} valeur={region} set={setRegion} />
          <Choix titre="2. Votre taille" options={TAILLES} valeur={taille} set={setTaille} />
          <Choix titre="3. Votre besoin principal" options={BESOINS} valeur={besoin} set={setBesoin} />

          <button
            type="button"
            onClick={lancer}
            disabled={!pret}
            className={
              "w-full py-3.5 rounded-xl font-semibold transition-colors " +
              (pret
                ? "bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-600/20"
                : "bg-slate-200 text-slate-400 cursor-not-allowed")
            }
          >
            Voir mes aides possibles
          </button>
        </div>

        {/* Résultats */}
        {resultats && (
          <div className="mt-10">
            <h2 className="text-2xl font-bold">
              {resultats.length} piste{resultats.length > 1 ? "s" : ""} pour vous
            </h2>
            <div className="mt-6 grid gap-4">
              {resultats.map((a) => (
                <article key={a.nom} className="rounded-2xl border border-slate-200 p-5 bg-white">
                  <h3 className="font-semibold text-lg text-slate-900">{a.nom}</h3>
                  <p className="mt-2 text-slate-600 text-sm leading-relaxed">{a.why}</p>
                  <a
                    href={a.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-block mt-3 text-sm font-semibold text-indigo-700 hover:text-indigo-900"
                  >
                    Source officielle →
                  </a>
                </article>
              ))}
            </div>

            <div className="mt-8 rounded-2xl bg-indigo-600 text-white p-7 text-center">
              <h3 className="text-xl font-bold">On monte le dossier pour vous</h3>
              <p className="text-indigo-100 mt-2 text-sm leading-relaxed">
                Veille, éligibilité (Go/No-Go), rédaction et dépôt : on s'occupe de tout.
                Et le combo gagnant — on vous met aux normes ET on cherche la subvention qui le finance.
              </p>
              <Link
                href="/contact"
                className="inline-block mt-5 bg-white text-indigo-700 font-semibold px-7 py-3 rounded-xl hover:bg-indigo-50 transition-colors"
              >
                Parler de mon projet
              </Link>
            </div>
          </div>
        )}
      </section>

      {/* Disclaimer honnête */}
      <section className="py-12 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-6">
          <h3 className="font-semibold text-amber-900">⚖️ En toute transparence</h3>
          <p className="text-amber-800 text-sm mt-2 leading-relaxed">
            Les budgets, taux et échéances des aides changent souvent — certains dispositifs ferment
            en cours d'année. On vérifie toujours l'appel exact sur le portail officiel avant de vous
            engager. Pas de promesse en l'air : c'est ce qui fait notre crédibilité.
          </p>
        </div>
      </section>
    </main>
  );
}
