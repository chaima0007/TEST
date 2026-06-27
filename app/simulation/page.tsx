"use client";

import Link from "next/link";

const capabilities = [
  {
    title: "Anticipation des risques",
    desc: "Nous modélisons ce qui pourrait mal tourner avant que ça n'arrive : baisse de ventes, pics de charge, ruptures. Vous voyez venir, vous décidez sereinement.",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <path d="M12 9v4M12 17h.01" strokeLinecap="round" />
        <path d="M10.3 3.9L1.8 18a2 2 0 001.7 3h17a2 2 0 001.7-3L13.7 3.9a2 2 0 00-3.4 0z" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    title: "Des milliers de scénarios testés",
    desc: "Chaque décision importante est éprouvée sur des milliers de cas simulés. On ne devine pas : on mesure la robustesse de vos choix face à l'incertitude.",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <path d="M3 3v18h18" strokeLinecap="round" />
        <path d="M7 15l3-3 3 2 4-6" strokeLinecap="round" strokeLinejoin="round" />
        <circle cx="7" cy="15" r="1" fill="currentColor" /><circle cx="10" cy="12" r="1" fill="currentColor" /><circle cx="13" cy="14" r="1" fill="currentColor" />
      </svg>
    ),
  },
  {
    title: "Plusieurs angles de vue",
    desc: "Optimiste, prudent, pessimiste : nous évaluons chaque situation sous plusieurs perspectives pour une vision complète, jamais biaisée par un seul scénario.",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <circle cx="12" cy="12" r="3" />
        <path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    title: "Validé par notre protocole unique",
    desc: "Chaque résultat passe par notre protocole de vérification multi-couches. Une analyse n'est livrée que si elle a franchi tous nos contrôles de fiabilité.",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <path d="M12 3l7 4v5c0 5-3.5 7.5-7 9-3.5-1.5-7-4-7-9V7l7-4z" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M9 12l2 2 4-4" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
];

const useCases = [
  { t: "Prévoir vos ventes", d: "Estimer plusieurs trajectoires de chiffre d'affaires selon différents scénarios de marché." },
  { t: "Anticiper les risques", d: "Identifier les points de fragilité avant qu'ils ne deviennent des problèmes coûteux." },
  { t: "Tester une décision", d: "Mesurer la solidité d'un choix stratégique avant de l'engager pour de vrai." },
];

export default function SimulationPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      {/* Header */}
      <header className="border-b border-slate-100">
        <div className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
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
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(124,58,237,0.25),transparent_60%)]" />
        <div className="absolute inset-0 opacity-[0.04]"
          style={{ backgroundImage: "linear-gradient(rgba(255,255,255,.6) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.6) 1px,transparent 1px)", backgroundSize: "70px 70px" }} />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Simulation &amp; anticipation
          </span>
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight leading-tight">
            Voyez vos problèmes
            <span className="block bg-gradient-to-r from-indigo-300 to-sky-300 bg-clip-text text-transparent">
              avant qu&apos;ils n&apos;arrivent
            </span>
          </h1>
          <p className="text-lg text-slate-300 mt-6 leading-relaxed">
            Notre force unique : nous simulons des milliers de scénarios pour anticiper
            l&apos;avenir de votre activité et fiabiliser vos décisions.
          </p>
        </div>
      </section>

      {/* Capabilities */}
      <section className="py-24 px-6 max-w-6xl mx-auto">
        <div className="grid md:grid-cols-2 gap-6">
          {capabilities.map((c) => (
            <div key={c.title} className="rounded-2xl border border-slate-200 p-7 hover:shadow-lg transition-all">
              <div className="w-14 h-14 rounded-xl bg-slate-900 text-violet-400 flex items-center justify-center mb-5">{c.icon}</div>
              <h3 className="text-xl font-bold">{c.title}</h3>
              <p className="text-slate-600 mt-3 leading-relaxed">{c.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Use cases */}
      <section className="py-20 px-6 bg-slate-50">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold text-center">Concrètement, ça sert à quoi ?</h2>
          <div className="grid sm:grid-cols-3 gap-6 mt-10">
            {useCases.map((u) => (
              <div key={u.t} className="bg-white rounded-xl border border-slate-200 p-6">
                <h3 className="font-semibold text-lg">{u.t}</h3>
                <p className="text-slate-500 text-sm mt-2 leading-relaxed">{u.d}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Honnêteté */}
      <section className="py-16 px-6 max-w-3xl mx-auto text-center">
        <p className="text-slate-500 text-sm leading-relaxed">
          <strong className="text-slate-700">En toute transparence :</strong> nos simulations sont des
          modélisations statistiques avancées, pas des prédictions infaillibles. Aucune méthode ne
          garantit l&apos;avenir à 100 %. Mais en testant des milliers de scénarios, nous réduisons
          fortement l&apos;incertitude — et ça, ça change tout pour décider sereinement.
        </p>
      </section>

      {/* CTA */}
      <section className="px-6 pb-24">
        <div className="max-w-4xl mx-auto rounded-3xl bg-gradient-to-br from-slate-900 to-slate-950 px-8 py-14 text-center relative overflow-hidden">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(124,58,237,0.25),transparent_60%)]" />
          <div className="relative z-10">
            <h2 className="text-3xl font-bold text-white">Anticipez l&apos;avenir de votre activité</h2>
            <p className="text-slate-300 mt-3">Discutons de ce qu&apos;on peut simuler pour vous — gratuitement.</p>
            <Link href="/contact" className="inline-block mt-7 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-8 py-3.5 rounded-xl transition-colors shadow-lg shadow-indigo-600/30">
              Parlons-en
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}
