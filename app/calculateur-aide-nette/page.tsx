"use client";

import Link from "next/link";
import { useState } from "react";

// « Calculateur d'aide nette » — Caelum (pépite com n°3).
// Différenciateur : montrer que la conformité (surtout cyber/numérique) peut être
// PARTIELLEMENT FINANCÉE. Honnêteté : les TAUX sont officiels et sourcés ; le COÛT est
// une estimation saisie par l'utilisateur (rien d'inventé). Aide = prestataire labellisé requis.

type Aide = { id: string; region: string; nom: string; taux: number; plafond: number; url: string; note: string };

const AIDES: Aide[] = [
  {
    id: "wal-cyber", region: "Wallonie", nom: "Chèque « cybersécurité »", taux: 0.75, plafond: 50000,
    url: "https://www.wallonie.be/fr/demarches/etre-accompagne-par-un-expert-pour-securiser-les-donnees-de-mon-entreprise-cheque-cybersecurite",
    note: "Conseil en cybersécurité par un prestataire labellisé.",
  },
  {
    id: "wal-matnum", region: "Wallonie", nom: "Chèque « maturité numérique »", taux: 0.50, plafond: 50000,
    url: "https://www.wallonie.be/fr/demarches/etre-accompagne-par-un-expert-pour-digitaliser-les-processus-internes-de-mon-entreprise-cheque-maturite-numerique",
    note: "Diagnostic et plan numérique par un prestataire labellisé.",
  },
  {
    id: "vla-kmo", region: "Flandre", nom: "kmo-portefeuille (cybersécurité)", taux: 0.45, plafond: 7500,
    url: "https://www.vlaio.be/nl/subsidies-financiering/kmo-portefeuille",
    note: "Petites entreprises (45 %). Conseil limité à la cybersécurité depuis le 01/02/2026.",
  },
];

const eur = (n: number) => n.toLocaleString("fr-BE", { maximumFractionDigits: 0 }) + " €";

export default function CalculateurAideNette() {
  const [cout, setCout] = useState(5000);
  const [aideId, setAideId] = useState("wal-cyber");
  const aide = AIDES.find((a) => a.id === aideId)!;

  const brut = Math.max(0, cout);
  const aideMontant = Math.min(brut * aide.taux, aide.plafond);
  const net = brut - aideMontant;
  const economiePct = brut > 0 ? Math.round((aideMontant / brut) * 100) : 0;

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-3xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <span className="font-bold text-lg">Caelum</span>
          </Link>
          <Link href="/conformite-2026" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Suis-je concerné ?</Link>
        </div>
      </header>

      <section className="bg-gradient-to-b from-slate-950 to-slate-900 text-white py-14 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-5">
            Conformité finançable
          </span>
          <h1 className="text-3xl sm:text-4xl font-bold">Combien votre mise en conformité coûte-t-elle <span className="text-emerald-300">vraiment</span> ?</h1>
          <p className="mt-3 text-slate-300">La plupart ne voient que le coût brut. Voici le coût <strong>net</strong>, après l'aide publique qui le finance.</p>
        </div>
      </section>

      <div className="max-w-3xl mx-auto px-6 py-12">
        <div className="rounded-2xl border border-slate-200 p-6">
          <label className="block text-sm font-semibold text-slate-800">Coût estimé de l'accompagnement (HTVA)</label>
          <p className="text-xs text-slate-500 mt-1">Votre estimation — c'est vous qui la saisissez (devis prestataire, budget…).</p>
          <div className="mt-3 flex items-center gap-3">
            <input
              type="range" min={500} max={50000} step={500} value={cout}
              onChange={(e) => setCout(Number(e.target.value))}
              className="flex-1 accent-indigo-600"
            />
            <input
              type="number" min={0} value={cout}
              onChange={(e) => setCout(Number(e.target.value))}
              className="w-28 rounded-lg border border-slate-300 px-3 py-2 text-sm"
            />
          </div>

          <label className="block text-sm font-semibold text-slate-800 mt-6">Aide publique applicable</label>
          <div className="mt-2 flex flex-wrap gap-2">
            {AIDES.map((a) => (
              <button
                key={a.id} type="button" onClick={() => setAideId(a.id)}
                className={"px-3 py-2 rounded-full border text-sm font-medium transition-colors " +
                  (aideId === a.id ? "bg-indigo-600 border-indigo-600 text-white" : "bg-white border-slate-300 text-slate-700 hover:border-indigo-400")}
              >
                {a.region} · {a.nom} ({Math.round(a.taux * 100)} %)
              </button>
            ))}
          </div>

          {/* Résultat */}
          <div className="mt-6 grid sm:grid-cols-3 gap-3 text-center">
            <div className="rounded-xl bg-slate-50 border border-slate-200 p-4">
              <p className="text-xs text-slate-500">Coût brut</p>
              <p className="text-xl font-bold text-slate-800">{eur(brut)}</p>
            </div>
            <div className="rounded-xl bg-emerald-50 border border-emerald-200 p-4">
              <p className="text-xs text-emerald-700">Aide publique (−{economiePct} %)</p>
              <p className="text-xl font-bold text-emerald-700">− {eur(aideMontant)}</p>
            </div>
            <div className="rounded-xl bg-indigo-600 p-4">
              <p className="text-xs text-indigo-100">Reste à votre charge</p>
              <p className="text-xl font-bold text-white">{eur(net)}</p>
            </div>
          </div>

          <p className="text-[11px] text-slate-500 mt-4 leading-snug">
            Taux et plafonds <strong>officiels</strong> ({aide.note} Plafond ~{eur(aide.plafond)}). ⚠️ Aide soumise à conditions :
            prestataire <strong>labellisé/enregistré</strong> requis, TVA et frais non éligibles à votre charge. Le coût saisi est votre estimation.
            {" "}<a href={aide.url} target="_blank" rel="noopener noreferrer" className="text-indigo-700 hover:underline">Source officielle ↗</a>
          </p>
        </div>

        <div className="mt-8 rounded-2xl bg-slate-900 text-white p-6 text-center">
          <h2 className="text-lg font-bold">Quelles obligations vous concernent — et lesquelles sont finançables ?</h2>
          <p className="text-slate-300 text-sm mt-2">Le simulateur vous donne votre liste exacte et les aides liées, en 1 minute.</p>
          <Link href="/conformite-2026" className="inline-block mt-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-6 py-3 rounded-xl transition-colors">
            Faire le test gratuit
          </Link>
        </div>
      </div>
    </main>
  );
}
