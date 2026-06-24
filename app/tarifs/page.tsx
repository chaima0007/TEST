"use client";

import Link from "next/link";

const offers = [
  {
    name: "Site web",
    price: "dès 500 €",
    tagline: "Une vitrine moderne qui inspire confiance.",
    features: [
      "Site vitrine 1 à 5 pages",
      "Design moderne & responsive",
      "Optimisé mobile et rapidité",
      "Formulaire de contact intégré",
      "Livré en quelques jours",
    ],
    highlight: false,
  },
  {
    name: "Tableau de bord",
    price: "dès 800 €",
    tagline: "Vos données enfin claires et exploitables.",
    features: [
      "Dashboard sur-mesure",
      "Données en temps réel",
      "Indicateurs adaptés à votre activité",
      "Simple à utiliser au quotidien",
      "Formation à la prise en main",
    ],
    highlight: true,
  },
  {
    name: "Automatisation",
    price: "dès 300 €",
    tagline: "Gagnez du temps, supprimez les tâches répétitives.",
    features: [
      "Automatisation sur-mesure",
      "Connexion à vos outils existants",
      "Moins d'erreurs manuelles",
      "Supervisée et fiable",
      "Gain de temps mesurable",
    ],
    highlight: false,
  },
  {
    name: "Business plan",
    price: "dès 400 €",
    tagline: "Un plan d'affaires clair pour convaincre.",
    features: [
      "Plan d'affaires structuré",
      "Analyse marché & concurrence",
      "Chiffrage et projections",
      "Stratégie de croissance",
      "Présentation prête à pitcher",
    ],
    highlight: false,
  },
];

const faq = [
  { q: "Combien de temps pour livrer ?", a: "La plupart des sites vitrines sont livrés en quelques jours. Les projets plus complexes (dashboards, automatisations) prennent 1 à 2 semaines. On vous donne un délai clair dès le devis." },
  { q: "Comment se passe le paiement ?", a: "Un acompte au démarrage, le solde à la livraison. Tout est annoncé à l'avance dans le devis — aucune surprise." },
  { q: "Et après la livraison ?", a: "On reste disponible. Une formule de maintenance mensuelle (dès 50 €/mois) est possible si vous souhaitez un suivi continu." },
  { q: "Les prix sont-ils fixes ?", a: "Les prix affichés sont des points de départ. Le devis final dépend de votre besoin précis — toujours transparent, validé par vous avant qu'on commence." },
];

export default function TarifsPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      {/* Header */}
      <header className="border-b border-slate-100">
        <div className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-violet-600 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <span className="font-bold text-lg tracking-tight">Caelum</span>
          </Link>
          <Link href="/contact" className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold px-5 py-2.5 rounded-lg transition-colors">
            Demander un devis
          </Link>
        </div>
      </header>

      {/* Hero */}
      <section className="text-center px-6 pt-20 pb-12 max-w-3xl mx-auto">
        <span className="text-blue-600 font-semibold text-sm uppercase tracking-wide">Services &amp; Tarifs</span>
        <h1 className="text-4xl sm:text-5xl font-bold tracking-tight mt-3">Des prix clairs, sans surprise</h1>
        <p className="text-slate-500 mt-4 text-lg">
          Vous savez exactement ce que vous payez, avant de commencer. Devis gratuit et sans engagement.
        </p>
      </section>

      {/* Offres */}
      <section className="px-6 max-w-6xl mx-auto pb-8">
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {offers.map((o) => (
            <div key={o.name}
              className={`rounded-2xl border p-7 flex flex-col ${o.highlight ? "border-blue-500 ring-2 ring-blue-200 shadow-lg" : "border-slate-200"}`}>
              {o.highlight && (
                <span className="self-start text-xs font-semibold bg-blue-600 text-white px-3 py-1 rounded-full mb-3">Le plus demandé</span>
              )}
              <h3 className="text-xl font-bold">{o.name}</h3>
              <p className="text-slate-500 text-sm mt-1">{o.tagline}</p>
              <div className="text-3xl font-bold mt-5">{o.price}</div>
              <ul className="mt-6 space-y-2.5 flex-1">
                {o.features.map((f) => (
                  <li key={f} className="flex items-start gap-2 text-sm text-slate-700">
                    <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-emerald-500 flex-shrink-0 mt-0.5">
                      <path fillRule="evenodd" d="M16.7 5.3a1 1 0 010 1.4l-7.5 7.5a1 1 0 01-1.4 0L3.3 9.7a1 1 0 011.4-1.4L8.5 12l6.8-6.8a1 1 0 011.4 0z" clipRule="evenodd" />
                    </svg>
                    {f}
                  </li>
                ))}
              </ul>
              <Link href="/contact"
                className={`mt-7 text-center font-semibold px-5 py-3 rounded-xl transition-colors ${o.highlight ? "bg-blue-600 hover:bg-blue-700 text-white" : "bg-slate-900 hover:bg-slate-700 text-white"}`}>
                Demander un devis
              </Link>
            </div>
          ))}
        </div>
        <p className="text-center text-sm text-slate-400 mt-6">
          Maintenance mensuelle optionnelle dès 50 €/mois · Tarifs de départ, devis personnalisé gratuit
        </p>
      </section>

      {/* Garantie */}
      <section className="px-6 py-16 bg-slate-50">
        <div className="max-w-4xl mx-auto grid sm:grid-cols-3 gap-6 text-center">
          {[
            { t: "Devis gratuit", d: "Aucun engagement, aucune avance pour discuter." },
            { t: "Prix transparents", d: "Le montant annoncé est le montant facturé." },
            { t: "Satisfaction suivie", d: "On ajuste jusqu'à ce que le résultat vous convienne." },
          ].map((g) => (
            <div key={g.t}>
              <div className="w-12 h-12 mx-auto rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mb-3">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8} className="w-6 h-6">
                  <path d="M9 12l2 2 4-4" strokeLinecap="round" strokeLinejoin="round" />
                  <circle cx="12" cy="12" r="9" />
                </svg>
              </div>
              <h3 className="font-semibold">{g.t}</h3>
              <p className="text-slate-500 text-sm mt-1">{g.d}</p>
            </div>
          ))}
        </div>
      </section>

      {/* FAQ */}
      <section className="px-6 py-20 max-w-3xl mx-auto">
        <h2 className="text-3xl font-bold text-center">Questions fréquentes</h2>
        <div className="mt-10 space-y-4">
          {faq.map((f) => (
            <div key={f.q} className="rounded-xl border border-slate-200 p-5">
              <h3 className="font-semibold">{f.q}</h3>
              <p className="text-slate-600 text-sm mt-2 leading-relaxed">{f.a}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="px-6 pb-24">
        <div className="max-w-4xl mx-auto rounded-3xl bg-gradient-to-br from-slate-900 to-slate-950 px-8 py-14 text-center relative overflow-hidden">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(37,99,235,0.25),transparent_60%)]" />
          <div className="relative z-10">
            <h2 className="text-3xl font-bold text-white">Un projet en tête ?</h2>
            <p className="text-slate-300 mt-3">Recevez un devis clair et gratuit sous 24h.</p>
            <Link href="/contact"
              className="inline-block mt-7 bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-3.5 rounded-xl transition-colors shadow-lg shadow-blue-600/30">
              Demander mon devis gratuit
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}
