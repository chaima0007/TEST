"use client";

import Link from "next/link";

// « Compte à rebours public des échéances » — Caelum (pépite com n°1).
// Aimant SEO/LinkedIn : transforme le calendrier réglementaire en objet partageable.
// Compte à rebours calculé en direct (navigateur). Dates cohérentes avec la base de normes ;
// chaque ligne renvoie à sa fiche norme sourcée et au simulateur. Honnête : « en vigueur »
// pour le passé, jamais de date inventée.

type Echeance = {
  nom: string;
  dateISO: string;
  slug: string; // page /conformite/[slug]
  sanction: string;
};

const ECHEANCES: Echeance[] = [
  { nom: "Facturation électronique B2B (Peppol)", dateISO: "2026-01-01", slug: "e-facturation", sanction: "Amendes + perte de la déduction TVA" },
  { nom: "DORA — résilience numérique (finance)", dateISO: "2025-01-17", slug: "dora-resilience-numerique", sanction: "Sanctions administratives (BNB/FSMA)" },
  { nom: "PPWR — emballages", dateISO: "2026-08-12", slug: "emballages-ppwr", sanction: "Retrait/rappel des emballages non conformes" },
  { nom: "CSRD — reporting durabilité", dateISO: "2027-01-01", slug: "csrd", sanction: "Sanctions + risque réputationnel" },
  { nom: "CBAM — ajustement carbone aux frontières", dateISO: "2027-05-31", slug: "cbam-carbone", sanction: "Sanctions + blocage à l'importation" },
  { nom: "Transparence salariale (égalité F/H)", dateISO: "2027-06-07", slug: "transparence-salariale", sanction: "Évaluation conjointe si écart injustifié > 5 %" },
  { nom: "CSDDD — devoir de vigilance", dateISO: "2029-07-26", slug: "csddd", sanction: "Responsabilité + sanctions" },
];

function jours(dateISO: string): number {
  const cible = new Date(dateISO + "T00:00:00");
  const now = new Date();
  return Math.ceil((cible.getTime() - now.getTime()) / 86_400_000);
}

export default function Echeances2026() {
  const items = ECHEANCES.map((e) => ({ ...e, j: jours(e.dateISO) })).sort((a, b) => a.j - b.j);

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-white/10">
        <div className="max-w-4xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <span className="font-bold text-lg">Caelum</span>
          </Link>
          <Link href="/conformite-2026" className="text-sm font-semibold text-indigo-300 hover:text-white">Suis-je concerné ?</Link>
        </div>
      </header>

      <section className="max-w-4xl mx-auto px-6 pt-14 pb-8 text-center">
        <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-5">
          Compte à rebours réglementaire
        </span>
        <h1 className="text-3xl sm:text-5xl font-bold">Le compte à rebours des échéances</h1>
        <p className="mt-4 text-slate-300 max-w-2xl mx-auto">
          Chaque obligation a une date — et une sanction. Voici le temps qu'il vous reste,
          en direct. Chaque ligne renvoie à sa fiche sourcée.
        </p>
      </section>

      <section className="max-w-4xl mx-auto px-6 pb-10 grid gap-3">
        {items.map((e) => {
          const passe = e.j <= 0;
          const urgent = e.j > 0 && e.j <= 90;
          return (
            <Link
              key={e.slug}
              href={`/conformite/${e.slug}`}
              className={`rounded-2xl border p-5 flex items-center justify-between gap-4 transition-all hover:-translate-y-0.5 ${
                passe ? "border-white/10 bg-white/5" : urgent ? "border-rose-400/40 bg-rose-500/10" : "border-amber-400/30 bg-amber-500/5"
              }`}
            >
              <div>
                <h2 className="font-semibold text-slate-100">{e.nom}</h2>
                <p className="text-xs text-slate-400 mt-1">⚠️ {e.sanction}</p>
              </div>
              <div className="text-right whitespace-nowrap">
                {passe ? (
                  <span className="text-emerald-400 font-bold text-sm">déjà en vigueur</span>
                ) : (
                  <>
                    <span className={`text-2xl font-black ${urgent ? "text-rose-300" : "text-amber-300"}`}>{e.j}</span>
                    <span className="block text-xs text-slate-400">jours restants</span>
                  </>
                )}
              </div>
            </Link>
          );
        })}
      </section>

      <section className="max-w-4xl mx-auto px-6 pb-16">
        <div className="rounded-2xl bg-indigo-600 p-7 text-center">
          <h2 className="text-xl font-bold">Lesquelles vous concernent vraiment ?</h2>
          <p className="text-indigo-100 mt-2 text-sm">Le simulateur vous donne votre liste exacte en 1 minute — et les aides qui financent la mise en conformité.</p>
          <Link href="/conformite-2026" className="inline-block mt-5 bg-white text-indigo-700 font-semibold px-6 py-3 rounded-xl hover:bg-indigo-50 transition-colors">
            Faire le test gratuit
          </Link>
        </div>
        <p className="text-center text-xs text-slate-500 mt-5">
          Dates indicatives issues de notre base de normes vérifiée ; vérifiez toujours la source officielle de chaque fiche. Caelum.
        </p>
      </section>
    </main>
  );
}
