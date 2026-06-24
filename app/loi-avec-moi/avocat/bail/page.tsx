"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Fiche « avocat-référent » — Bail & immobilier (Belgique).
// ATTENTION : le bail d'habitation est une compétence RÉGIONALE (Wallonie / Bruxelles / Flandre).
// Faits vérifiés : logement.wallonie.be, logement.brussels, vlaanderen.be, Belgium.be.

const pointsCles = [
  {
    t: "Durée : 9 ans en principe",
    d: "Le bail de résidence principale dure en principe 9 ans. Il existe aussi le bail de courte durée (3 ans maximum) et le bail de longue durée (plus de 9 ans). Les conditions de fin diffèrent selon le type.",
  },
  {
    t: "Garantie locative sur un compte bloqué",
    d: "La garantie doit être placée sur un compte bloqué au nom du locataire (le propriétaire ne peut pas la garder sur son compte). Selon le mode et la région, elle est plafonnée (souvent 2 mois de loyer en espèces/virement, jusqu'à 3 mois pour une garantie bancaire).",
  },
  {
    t: "Préavis du locataire : 3 mois",
    d: "Le locataire peut en principe mettre fin au bail à tout moment moyennant un préavis de 3 mois (une indemnité peut être due s'il part dans les premières années — vérifiez selon votre région et votre type de bail).",
  },
  {
    t: "Indexation du loyer : une fois par an",
    d: "Le loyer peut être indexé au maximum une fois par an, à la date anniversaire du bail, selon une formule légale. Le propriétaire qui a oublié peut rattraper l'indexation, mais de façon limitée dans le temps (rétroactivité plafonnée).",
  },
  {
    t: "État des lieux : faites-le, en détail",
    d: "Un état des lieux d'entrée détaillé et contradictoire (signé par les deux parties) est essentiel : sans lui, il est très difficile de prouver l'état du logement à la sortie. Prenez des photos datées.",
  },
];

const documentsOfficiels = [
  {
    label: "Wallonie — Logement : le bail de résidence principale",
    url: "https://logement.wallonie.be/fr/bail/type-bail-residence-principale",
  },
  {
    label: "Bruxelles Logement — Le bail d'habitation",
    url: "https://logement.brussels/louer/le-bail/",
  },
  {
    label: "Vlaanderen — Huren (location en Flandre)",
    url: "https://www.vlaanderen.be/huren-en-verhuren",
  },
  {
    label: "Belgium.be — Logement & location",
    url: "https://www.belgium.be/fr/logement",
  },
];

const docsAApporter = [
  "Le bail signé et l'état des lieux d'entrée (et de sortie, le cas échéant)",
  "Les preuves de paiement du loyer et de la garantie locative",
  "Les photos datées et constats des problèmes (humidité, dégâts, vices)",
  "Tous les courriers échangés avec le propriétaire / le locataire",
];

const readText = `Avocat-référent : le bail et l'immobilier en Belgique. Attention, c'est une matière régionale : les règles diffèrent entre la Wallonie, Bruxelles et la Flandre. Cette fiche s'appuie sur des sources officielles et ne remplace pas un avocat. ${pointsCles
  .map((p) => p.t + ". " + p.d)
  .join(" ")} Vérifiez toujours la source officielle de VOTRE région. Avant de consulter, préparez : ${docsAApporter.join(", ")}. Si vos revenus sont modestes, le Bureau d'Aide Juridique peut désigner un avocat gratuitement ou à coût réduit. Pour beaucoup de litiges locatifs, le juge de paix est compétent.`;

export default function AvocatBailPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">L</span>
            </div>
            <span className="font-bold text-lg tracking-tight">La loi avec moi</span>
          </Link>
          <Link href="/loi-avec-moi/trouver-un-avocat" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">← Toutes les spécialisations</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(20,184,166,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            🏠 Avocat-référent · Bail & immobilier
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Bail & logement — l&apos;essentiel, sourcé</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Garantie locative, durée, préavis, indexation, état des lieux : les points clés, adossés à des
            <strong className="text-white"> sources officielles régionales</strong>. Pour un litige, consultez un avocat —
            vous arriverez préparé·e.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Agent rassurant */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-8 rounded-2xl border border-teal-100 bg-teal-50/60 p-5">
          <AgentAvocat
            name="Maître Hugo"
            role="Référent · bail & immobilier"
            accent="teal"
            message="Un souci de bail, ça angoisse vite quand c'est votre toit. On clarifie vos droits — et on regarde d'abord la règle de VOTRE région."
          />
        </div>
      </section>

      {/* Avertissement régional — crucial */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-teal-300 bg-teal-50 p-5">
          <p className="text-teal-900 text-sm leading-relaxed">
            📍 <strong>Important :</strong> en Belgique, le bail d&apos;habitation dépend de la <strong>Région</strong> où se
            trouve le logement (Wallonie, Bruxelles, Flandre). Les règles (garantie, préavis, indexation) peuvent
            <strong> varier</strong>. Référez-vous toujours à la source officielle de votre région (liens ci-dessous).
          </p>
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Information générale fondée sur des sources officielles, <strong>pas un conseil juridique
            personnalisé</strong>. Pour un litige (caution non rendue, expulsion, vices), <strong>consultez un avocat</strong> ;
            le juge de paix est souvent compétent.
          </p>
        </div>
      </section>

      {/* Points clés */}
      <section className="py-14 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">Les points clés</h2>
        <div className="mt-6 space-y-4">
          {pointsCles.map((p, i) => (
            <div key={i} className="rounded-2xl border border-slate-200 p-5">
              <h3 className="font-bold tracking-tight">{p.t}</h3>
              <p className="text-slate-700 text-sm mt-2 leading-relaxed">{p.d}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Documents officiels de référence */}
      <section className="py-12 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">📚 Les sources officielles par région</h2>
          <p className="text-slate-600 mt-2 text-sm leading-relaxed">
            Choisissez la région où se trouve le logement. Ces pages officielles font foi et sont tenues à jour.
          </p>
          <div className="mt-5 flex flex-col gap-2.5">
            {documentsOfficiels.map((d) => (
              <a key={d.url} href={d.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-50 rounded-lg px-4 py-2.5 transition-colors">
                🔗 {d.label}
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* Documents à apporter */}
      <section className="py-12 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">📎 Préparez votre dossier</h2>
        <p className="text-slate-600 mt-2 text-sm leading-relaxed">Apportez ces documents à votre avocat — vous gagnerez du temps et de l&apos;argent.</p>
        <ul className="mt-5 space-y-2.5">
          {docsAApporter.map((d, i) => (
            <li key={i} className="flex items-start gap-2.5 text-sm text-slate-700 leading-relaxed">
              <span className="flex-shrink-0 w-5 h-5 rounded-md border-2 border-indigo-300 mt-0.5" aria-hidden />
              {d}
            </li>
          ))}
        </ul>
      </section>

      {/* Accès avocat / aide juridique */}
      <section className="pb-14 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border-2 border-indigo-200 bg-indigo-50 p-6">
          <h2 className="text-xl font-bold tracking-tight text-indigo-900">Trouver un avocat en droit du bail</h2>
          <p className="text-indigo-900/80 text-sm mt-2 leading-relaxed">
            Via l&apos;annuaire officiel, ou gratuitement / à coût réduit selon vos revenus grâce au Bureau d&apos;Aide
            Juridique (« pro deo »). Beaucoup de litiges locatifs se règlent devant le juge de paix.
          </p>
          <div className="mt-4 flex flex-col gap-2.5">
            <a href="https://avocats.be/fr" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 AVOCATS.BE — annuaire officiel
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
            <Link href="/loi-avec-moi/trouver-un-avocat" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              ⚖️ Aide juridique gratuite (pro deo) & autres spécialisations →
            </Link>
          </div>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi/trouver-un-avocat" className="hover:text-slate-900">← Retour aux spécialisations</Link>
      </footer>
    </main>
  );
}
