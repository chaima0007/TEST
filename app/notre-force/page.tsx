"use client";

import Link from "next/link";

const pillars = [
  {
    title: "Vérification à plusieurs niveaux",
    desc: "Chaque livrable passe par une série de contrôles automatisés et humains avant de vous être remis. Rien n'est livré sans avoir été validé.",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <path d="M9 12l2 2 4-4" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M12 3l7 4v5c0 5-3.5 7.5-7 9-3.5-1.5-7-4-7-9V7l7-4z" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    title: "Zéro erreur, par conception",
    desc: "Notre méthode est pensée pour détecter et corriger les problèmes avant qu'ils n'arrivent jusqu'à vous. La fiabilité n'est pas un hasard, c'est notre standard.",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <circle cx="12" cy="12" r="9" />
        <path d="M8 12l3 3 5-6" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    title: "Rapidité sans compromis",
    desc: "Nos processus nous permettent de livrer vite tout en gardant un niveau d'exigence élevé. Vous gagnez du temps sans perdre en qualité.",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    title: "Couverture complète",
    desc: "Du premier échange à la livraison finale et au suivi, chaque étape est prise en charge. Vous n'avez aucune zone d'ombre à gérer vous-même.",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <circle cx="12" cy="12" r="9" />
        <path d="M3 12h18M12 3a15 15 0 010 18M12 3a15 15 0 000 18" strokeLinecap="round" />
      </svg>
    ),
  },
];

const promises = [
  "Un devis clair et transparent avant tout démarrage",
  "Un interlocuteur unique, disponible et réactif",
  "Des livrables testés et vérifiés, jamais « au hasard »",
  "Un accompagnement qui ne s'arrête pas à la livraison",
];

export default function NotreForcePage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      {/* Header */}
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <span className="font-bold text-lg tracking-tight">Caelum</span>
          </Link>
          <Link href="/contact" className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold px-5 py-2.5 rounded-lg transition-colors">
            Demander un devis
          </Link>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-24 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(37,99,235,0.25),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Notre force
          </span>
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight leading-tight">
            La qualité n&apos;est pas une option,
            <span className="block bg-gradient-to-r from-indigo-300 to-sky-300 bg-clip-text text-transparent">
              c&apos;est notre méthode
            </span>
          </h1>
          <p className="text-lg text-slate-300 mt-6 leading-relaxed">
            Ce qui nous distingue : une organisation rigoureuse où chaque projet est
            vérifié à plusieurs niveaux. Le résultat ? Une fiabilité que peu peuvent garantir.
          </p>
        </div>
      </section>

      {/* Pillars */}
      <section className="py-24 px-6 max-w-6xl mx-auto">
        <div className="grid md:grid-cols-2 gap-6">
          {pillars.map((p) => (
            <div key={p.title} className="rounded-2xl border border-slate-200 p-7 hover:shadow-lg transition-all">
              <div className="w-14 h-14 rounded-xl bg-slate-900 text-indigo-300 flex items-center justify-center mb-5">
                {p.icon}
              </div>
              <h3 className="text-xl font-bold">{p.title}</h3>
              <p className="text-slate-600 mt-3 leading-relaxed">{p.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Promesses */}
      <section className="py-20 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-center">Nos engagements</h2>
          <p className="text-slate-500 text-center mt-3">Ce que vous obtenez à chaque projet, sans exception.</p>
          <ul className="mt-10 space-y-4">
            {promises.map((p) => (
              <li key={p} className="flex items-start gap-3 bg-white rounded-xl border border-slate-200 p-5">
                <svg viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5">
                  <path fillRule="evenodd" d="M16.7 5.3a1 1 0 010 1.4l-7.5 7.5a1 1 0 01-1.4 0L3.3 9.7a1 1 0 011.4-1.4L8.5 12l6.8-6.8a1 1 0 011.4 0z" clipRule="evenodd" />
                </svg>
                <span className="text-slate-700">{p}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 px-6 text-center">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-3xl font-bold">Envie de travailler avec une équipe qui ne laisse rien au hasard ?</h2>
          <Link href="/contact" className="inline-block mt-8 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-8 py-3.5 rounded-xl transition-colors shadow-lg shadow-indigo-600/20">
            Parlons de votre projet
          </Link>
        </div>
      </section>
    </main>
  );
}
