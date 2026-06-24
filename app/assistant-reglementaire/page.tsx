"use client";

import Link from "next/link";

const steps = [
  { n: "1", t: "Vous posez votre question", d: "« Quelles obligations RGPD pour mon site ? », « Dois-je une mention légale ? »… en langage simple." },
  { n: "2", t: "L'IA vous éclaire", d: "Vous recevez une explication claire, sans jargon, avec les points clés à connaître et à vérifier." },
  { n: "3", t: "Validation par un expert", d: "Pour toute décision importante, on vous oriente vers notre réseau de partenaires (avocats, comptables)." },
];

const covers = [
  "Obligations d'un site web (mentions, RGPD, cookies)",
  "Bases de la protection des données",
  "Comprendre un contrat ou des CGV",
  "Repérer les points à faire vérifier par un pro",
  "Préparer vos questions avant de voir un expert",
];

export default function AssistantReglementairePage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-violet-600 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <span className="font-bold text-lg tracking-tight">Caelum</span>
          </Link>
          <Link href="/contact" className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold px-5 py-2.5 rounded-lg transition-colors">Demander un devis</Link>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-24 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(37,99,235,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Assistant réglementaire IA
          </span>
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight leading-tight">
            Comprenez vos obligations,
            <span className="block bg-gradient-to-r from-blue-400 to-violet-400 bg-clip-text text-transparent">sans jargon, en quelques minutes</span>
          </h1>
          <p className="text-lg text-slate-300 mt-6 leading-relaxed">
            On utilise l'IA pour vous aider à <strong className="text-white">comprendre et naviguer</strong> vos
            obligations légales et administratives — et on vous oriente vers le bon expert pour vos décisions.
          </p>
        </div>
      </section>

      {/* Steps */}
      <section className="py-24 px-6 max-w-5xl mx-auto">
        <div className="grid md:grid-cols-3 gap-8">
          {steps.map((s) => (
            <div key={s.n} className="bg-white rounded-2xl border border-slate-200 p-7">
              <div className="w-11 h-11 rounded-full bg-blue-600 text-white font-bold flex items-center justify-center text-lg mb-4">{s.n}</div>
              <h3 className="text-lg font-bold">{s.t}</h3>
              <p className="text-slate-600 mt-2 text-sm leading-relaxed">{s.d}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Covers */}
      <section className="py-16 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold text-center">Ce qu'on peut éclaircir pour vous</h2>
          <ul className="mt-8 space-y-3">
            {covers.map((c) => (
              <li key={c} className="flex items-start gap-3 bg-white rounded-xl border border-slate-200 p-4">
                <svg viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5">
                  <path fillRule="evenodd" d="M16.7 5.3a1 1 0 010 1.4l-7.5 7.5a1 1 0 01-1.4 0L3.3 9.7a1 1 0 011.4-1.4L8.5 12l6.8-6.8a1 1 0 011.4 0z" clipRule="evenodd" />
                </svg>
                <span className="text-slate-700 text-sm">{c}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* Disclaimer honnête */}
      <section className="py-14 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-6">
          <h3 className="font-semibold text-amber-900">⚖️ En toute transparence</h3>
          <p className="text-amber-800 text-sm mt-2 leading-relaxed">
            Cet assistant fournit de l'<strong>information et de l'orientation</strong>, pas un conseil
            juridique ou fiscal personnalisé (une activité réservée aux professionnels agréés).
            Pour toute décision engageante, nous vous mettons en relation avec notre <strong>réseau de
            partenaires experts</strong> (avocats, experts-comptables). Vous gagnez en clarté et en
            temps — en toute sécurité.
          </p>
        </div>
      </section>

      {/* CTA */}
      <section className="px-6 pb-24 text-center">
        <h2 className="text-3xl font-bold">Une question qui vous bloque ?</h2>
        <p className="text-slate-500 mt-3">Posez-la — on vous éclaire, gratuitement, et on vous oriente si besoin.</p>
        <Link href="/contact" className="inline-block mt-7 bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-3.5 rounded-xl transition-colors shadow-lg shadow-blue-600/20">
          Poser ma question
        </Link>
      </section>
    </main>
  );
}
