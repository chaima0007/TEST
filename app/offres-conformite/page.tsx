"use client";

import Link from "next/link";

// Page Offres « Conformité » — Caelum (ENTREPRISES, séparé de La Loi Avec Moi).
// Distincte de /tarifs (offre studio web/data). Modèle de revenu récurrent :
// produit d'appel e-facture → abonnement Veille+Conformité (cœur) → sur-mesure.
// Aucun montant inventé : « sur devis » tant que les prix ne sont pas fixés.

const offres = [
  {
    id: "essentiel",
    nom: "Essentiel — e-facturation",
    pitch: "Se mettre en règle vite avec l'obligation 2026.",
    prix: "Sur devis",
    cadence: "",
    points: [
      "Diagnostic « suis-je concerné ? »",
      "Mise en place de la facturation électronique (Peppol)",
      "Vérification du format conforme",
      "Accompagnement à la bascule",
    ],
    accent: false,
  },
  {
    id: "serenite",
    nom: "Sérénité — Veille + Conformité",
    pitch: "Dès qu'une norme change, on vous prévient et on vous met à jour.",
    prix: "Sur devis",
    cadence: "abonnement",
    points: [
      "Veille réglementaire personnalisée (alertes)",
      "Tableau de bord de conformité",
      "Documents tenus à jour (RGPD, registres…)",
      "Canal de signalement (lanceurs d'alerte)",
      "Support prioritaire",
    ],
    accent: true,
  },
  {
    id: "surmesure",
    nom: "Sur-mesure — Audit & accompagnement",
    pitch: "Pour les besoins approfondis et les dossiers à enjeux.",
    prix: "Sur devis",
    cadence: "",
    points: [
      "Audit RGPD complet",
      "Mise en conformité NIS2 (cybersécurité)",
      "Montage de dossiers de subvention",
      "Réponse aux appels d'offres / marchés publics",
      "Réseau d'experts (avocats, comptables)",
    ],
    accent: false,
  },
];

export default function OffresConformitePage() {
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

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(37,99,235,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Offres conformité
          </span>
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight leading-tight">
            Une mise en conformité
            <span className="block bg-gradient-to-r from-indigo-300 to-sky-300 bg-clip-text text-transparent">
              simple, suivie, sereine
            </span>
          </h1>
          <p className="text-lg text-slate-300 mt-6 leading-relaxed">
            On entre par l&apos;urgent (l&apos;e-facturation 2026), puis on vous garde en règle dans le temps.
            Et on cherche la subvention publique qui finance votre mise en conformité.
          </p>
          <Link
            href="/conformite-2026"
            className="inline-block mt-7 bg-white/10 border border-white/20 hover:bg-white/20 text-white font-semibold px-6 py-3 rounded-xl transition-colors"
          >
            D&apos;abord : suis-je concerné ?
          </Link>
        </div>
      </section>

      <section className="py-16 px-6 max-w-6xl mx-auto">
        <div className="grid md:grid-cols-3 gap-6">
          {offres.map((o) => (
            <div
              key={o.id}
              className={
                "rounded-2xl border p-7 flex flex-col " +
                (o.accent ? "border-indigo-300 ring-2 ring-indigo-200 bg-indigo-50/40" : "border-slate-200 bg-white")
              }
            >
              {o.accent && (
                <span className="self-start mb-3 text-xs font-semibold px-2.5 py-1 rounded-full bg-indigo-600 text-white">
                  Le plus populaire
                </span>
              )}
              <h2 className="text-xl font-bold">{o.nom}</h2>
              <p className="mt-2 text-sm text-slate-600">{o.pitch}</p>
              <div className="mt-4">
                <span className="text-2xl font-bold">{o.prix}</span>
                {o.cadence && <span className="text-slate-500 text-sm"> · {o.cadence}</span>}
              </div>
              <ul className="mt-5 space-y-2 flex-1">
                {o.points.map((p) => (
                  <li key={p} className="flex items-start gap-2 text-sm text-slate-700">
                    <svg viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5">
                      <path
                        fillRule="evenodd"
                        d="M16.7 5.3a1 1 0 010 1.4l-7.5 7.5a1 1 0 01-1.4 0L3.3 9.7a1 1 0 011.4-1.4L8.5 12l6.8-6.8a1 1 0 011.4 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                    <span>{p}</span>
                  </li>
                ))}
              </ul>
              <Link
                href="/contact"
                className={
                  "mt-6 text-center font-semibold px-5 py-3 rounded-xl transition-colors " +
                  (o.accent
                    ? "bg-indigo-600 hover:bg-indigo-700 text-white"
                    : "border border-slate-300 hover:border-indigo-400 text-slate-800")
                }
              >
                Demander un devis
              </Link>
            </div>
          ))}
        </div>

        <div className="mt-10 rounded-2xl bg-slate-900 text-white p-7 text-center">
          <h3 className="text-xl font-bold">Le combo gagnant</h3>
          <p className="text-slate-300 mt-2 text-sm max-w-2xl mx-auto leading-relaxed">
            On vous met aux normes <strong className="text-white">et</strong> on cherche la subvention publique qui
            finance la mise en conformité. Pour beaucoup d&apos;entreprises, le coût net s&apos;en trouve fortement réduit.
          </p>
        </div>

        <div className="mt-6 rounded-2xl border border-slate-200 p-7">
          <h3 className="font-bold text-lg">Vous êtes fiduciaire ou comptable ?</h3>
          <p className="text-slate-600 mt-2 text-sm leading-relaxed">
            Proposez Caelum à vos clients et offrez-leur une conformité suivie, sans charge supplémentaire pour votre
            cabinet. Programme partenaire dédié.
          </p>
          <Link href="/contact" className="inline-block mt-4 text-sm font-semibold text-indigo-700 hover:text-indigo-900">
            Devenir partenaire →
          </Link>
        </div>
      </section>

      <section className="py-12 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-6">
          <h3 className="font-semibold text-amber-900">⚖️ En toute transparence</h3>
          <p className="text-amber-800 text-sm mt-2 leading-relaxed">
            Chaque mission fait l&apos;objet d&apos;un devis clair et validé avant de commencer. On vérifie toujours ce
            qui vous concerne réellement — pas de prestation inutile, pas de promesse en l&apos;air.
          </p>
        </div>
      </section>
    </main>
  );
}
