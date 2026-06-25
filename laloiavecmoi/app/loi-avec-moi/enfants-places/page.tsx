"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";

const rights = [
  "Tu as le droit d'être entendu·e. À partir de 12 ans, le juge doit t'inviter à parler dans beaucoup de situations qui te concernent.",
  "Tu as le droit à un avocat. Entre 12 et 14 ans, un avocat doit t'assister pour accepter une mesure d'aide. Cet avocat peut être gratuit.",
  "Tu as le droit de donner ton avis. À partir de 12 ans, ton accord est demandé pour certaines mesures d'aide (au SAJ).",
  "Tu as le droit de garder le contact avec ta famille, sauf si un juge décide que ce n'est pas dans ton intérêt.",
  "Tu as le droit d'être informé·e de ce qui se décide pour toi, dans des mots que tu comprends.",
  "Tu as le droit d'être respecté·e et protégé·e là où tu vis.",
];

const judgeSteps = [
  "Tu peux écrire au juge pour demander à être entendu·e (on te donne un modèle de lettre).",
  "Le jour de l'entretien, tu peux venir avec ton avocat. Tu n'es pas seul·e.",
  "Dis simplement ce que tu ressens et ce que tu voudrais. Il n'y a pas de « mauvaise » façon de parler.",
  "Tu as le droit de dire que tu ne comprends pas, et de demander qu'on t'explique autrement.",
];

const lawyerSteps = [
  "Tu peux demander un avocat « jeunesse », spécialisé pour les jeunes. Il est de ton côté.",
  "Tu peux tout lui dire : il est tenu au secret, il ne le répétera pas sans ton accord.",
  "Demande-lui d'expliquer simplement tes droits et ce qui va se passer.",
  "Si tu n'as pas les moyens, l'avocat peut être gratuit (aide juridique).",
];

const readText = `Tes droits quand tu es placé·e. ${rights.join(" ")} Pour parler à ton juge : ${judgeSteps.join(" ")} Pour ton avocat : ${lawyerSteps.join(" ")} Tu n'es pas seul·e, et tes droits comptent.`;

export default function EnfantsPlacesPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La loi avec moi</span>
          </Link>
          <Link href="/loi-avec-moi/modeles#juge-jeunesse" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Lettre au juge →</Link>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(79,70,229,0.25),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Tes droits quand tu es placé·e
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">
            Tu n&apos;es pas seul·e. Tu as des droits.
          </h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Quand on est placé·e, on a souvent l&apos;impression que les décisions se prennent sans nous.
            Pourtant, la loi belge te donne une voix. Voici comment l&apos;utiliser.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Tes droits */}
      <section className="py-16 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">Tes droits, simplement</h2>
        <ul className="mt-6 space-y-3">
          {rights.map((r, i) => (
            <li key={i} className="flex items-start gap-3 rounded-xl border border-slate-200 p-4">
              <svg viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5">
                <path fillRule="evenodd" d="M16.7 5.3a1 1 0 010 1.4l-7.5 7.5a1 1 0 01-1.4 0L3.3 9.7a1 1 0 011.4-1.4L8.5 12l6.8-6.8a1 1 0 011.4 0z" clipRule="evenodd" />
              </svg>
              <span className="text-slate-700 text-sm leading-relaxed">{r}</span>
            </li>
          ))}
        </ul>
      </section>

      {/* Parler à ton juge */}
      <section className="py-14 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">Comment parler à ton juge de la jeunesse</h2>
          <div className="mt-6 grid gap-4">
            {judgeSteps.map((s, i) => (
              <div key={i} className="flex items-start gap-3 bg-white rounded-xl border border-slate-200 p-4">
                <span className="flex-shrink-0 w-7 h-7 rounded-full bg-indigo-600 text-white text-sm font-bold flex items-center justify-center">{i + 1}</span>
                <span className="text-slate-700 text-sm leading-relaxed">{s}</span>
              </div>
            ))}
          </div>
          <Link href="/loi-avec-moi/modeles#juge-jeunesse" className="inline-block mt-6 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-6 py-3 rounded-xl transition-colors">
            Voir le modèle de lettre au juge
          </Link>
        </div>
      </section>

      {/* Ton avocat */}
      <section className="py-14 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">Comment demander un avocat</h2>
        <div className="mt-6 grid gap-4">
          {lawyerSteps.map((s, i) => (
            <div key={i} className="flex items-start gap-3 rounded-xl border border-slate-200 p-4">
              <span className="flex-shrink-0 w-7 h-7 rounded-full bg-indigo-600 text-white text-sm font-bold flex items-center justify-center">{i + 1}</span>
              <span className="text-slate-700 text-sm leading-relaxed">{s}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Réconfort + sources */}
      <section className="pb-12 px-6 max-w-3xl mx-auto space-y-5">
        <div className="rounded-2xl bg-indigo-50 border border-indigo-100 p-6 text-center">
          <p className="text-indigo-900 font-medium">💙 Demander de l&apos;aide ou poser des questions, c&apos;est ton droit. Tu mérites d&apos;être écouté·e.</p>
        </div>
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ Informations générales tirées de sources officielles belges (SPF Justice, aide à la jeunesse,
            Défense des Enfants International). Pour ta situation précise, ton avocat « jeunesse » est la
            meilleure personne pour t&apos;aider.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à « La loi avec moi »</Link>
      </footer>
    </main>
  );
}
