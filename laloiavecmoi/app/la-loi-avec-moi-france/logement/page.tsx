"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Page « Logement & bail » — Édition FRANCE.
// Faits vérifiés : loi n° 89-462 du 6 juillet 1989, service-public.fr
// (préavis F1168, dépôt de garantie F31269), ANIL. Distinct de l'édition belge.

const pointsCles = [
  {
    t: "La loi de référence : le 6 juillet 1989",
    d: "La location de votre résidence principale est encadrée par la loi du 6 juillet 1989. Elle fixe des règles d'ordre public que le bail ne peut pas contourner à votre désavantage : durée, dépôt, préavis, restitution. Un bail vide « classique » dure 3 ans (propriétaire particulier), un meublé 1 an (9 mois pour un étudiant).",
  },
  {
    t: "Dépôt de garantie : 1 mois (vide) ou 2 mois (meublé)",
    d: "Le dépôt de garantie est plafonné à 1 mois de loyer hors charges pour un logement vide, et 2 mois pour un meublé. Il doit être restitué dans un délai d'1 mois si l'état des lieux de sortie est conforme à celui d'entrée, ou 2 mois en cas de différences. Tout retard entraîne une majoration de 10 % du loyer mensuel par mois commencé.",
  },
  {
    t: "Votre préavis : 3 mois, souvent réductible à 1 mois",
    d: "Pour un logement vide, votre préavis est de 3 mois. Il tombe à 1 mois en zone tendue (Paris, Lyon, Bordeaux et de nombreuses villes), ou dans des cas précis : perte involontaire d'emploi, mutation, premier emploi, bénéficiaire du RSA ou de l'AAH, raison de santé. En meublé, le préavis du locataire est d'1 mois dans tous les cas.",
  },
  {
    t: "Le congé du propriétaire est très encadré",
    d: "Le propriétaire ne peut pas vous mettre dehors quand il veut. Pour un logement vide, il doit donner congé 6 mois avant la fin du bail (3 mois en meublé), et seulement pour un motif légitime : vendre, reprendre le logement pour y habiter (lui ou un proche), ou un motif légitime et sérieux (ex. impayés).",
  },
  {
    t: "L'état des lieux protège les deux parties",
    d: "Faites toujours un état des lieux d'entrée et de sortie, détaillé et contradictoire (photos à l'appui). C'est lui qui détermine ce qui peut être retenu sur votre dépôt. Sans état des lieux d'entrée, le logement est présumé avoir été remis en bon état — ce qui vous protège à la sortie.",
  },
];

const litige = [
  {
    n: "1",
    t: "Réclamez par écrit (recommandé)",
    d: "Dépôt non rendu, réparation non faite, charges contestées : écrivez au propriétaire en recommandé avec accusé de réception, en rappelant la loi de 1989 et en fixant un délai. Gardez une copie. C'est la base de tout recours.",
  },
  {
    n: "2",
    t: "La commission départementale de conciliation (gratuite)",
    d: "Pour beaucoup de litiges locatifs (dépôt, charges, réparations, loyer), vous pouvez saisir gratuitement la commission départementale de conciliation (CDC) avant d'aller au tribunal. L'ANIL/ADIL vous renseigne gratuitement.",
  },
  {
    n: "3",
    t: "Le tribunal judiciaire en dernier recours",
    d: "Si le désaccord persiste, le juge des contentieux de la protection (au tribunal judiciaire) tranche les litiges locatifs. Selon vos revenus, l'aide juridictionnelle peut prendre en charge tout ou partie des frais d'avocat.",
  },
];

const documentsOfficiels = [
  {
    label: "Service-Public.fr — Préavis du locataire (congé)",
    url: "https://www.service-public.gouv.fr/particuliers/vosdroits/F1168",
  },
  {
    label: "Service-Public.fr — Dépôt de garantie d'un bail d'habitation",
    url: "https://www.service-public.gouv.fr/particuliers/vosdroits/F31269",
  },
  {
    label: "Légifrance — Loi n° 89-462 du 6 juillet 1989",
    url: "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000509310/",
  },
  {
    label: "ANIL — information gratuite sur le logement (ADIL)",
    url: "https://www.anil.org/",
  },
];

const readText = `Logement et bail en France : vos droits. Cette page s'appuie sur la loi du 6 juillet 1989 et des sources officielles (service-public.fr, ANIL) et ne remplace pas un conseil personnalisé. ${pointsCles
  .map((p) => p.t + ". " + p.d)
  .join(" ")} En cas de litige : réclamez par écrit en recommandé, puis saisissez gratuitement la commission départementale de conciliation, et en dernier recours le tribunal judiciaire. Faites toujours un état des lieux détaillé à l'entrée et à la sortie.`;

export default function LogementFrancePage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/la-loi-avec-moi-france" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La loi avec moi <span className="text-blue-700">· France</span></span>
          </Link>
          <Link href="/la-loi-avec-moi-france" className="text-sm font-semibold text-blue-700 hover:text-blue-900">Tous les sujets →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-blue-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(20,184,166,0.20),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            🇫🇷 Logement &amp; bail
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Locataire ou propriétaire — vos droits</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Dépôt de garantie, préavis, congé, état des lieux : ce que la loi du 6 juillet 1989 garantit, adossé aux
            <strong className="text-white"> sources officielles (service-public.fr, ANIL)</strong>.
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
            name="Thomas"
            role="Assistant · droit du logement (France)"
            accent="teal"
            message="Le logement, c'est le litige n°1 du quotidien. Bonne nouvelle : la loi de 1989 encadre tout et protège fortement le locataire. Le réflexe clé : un état des lieux détaillé, et tout par écrit en recommandé."
          />
        </div>
      </section>

      {/* Encadré le bon réflexe */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-teal-300 bg-teal-50 p-5">
          <p className="text-teal-900 text-sm leading-relaxed">
            🔑 <strong>À retenir :</strong> le dépôt de garantie doit revenir sous <strong>1 mois</strong> (état des
            lieux conforme) ou <strong>2 mois</strong> au maximum, sinon il est majoré de 10 % du loyer par mois de
            retard. Et en zone tendue, votre préavis n&apos;est que d&apos;<strong>1 mois</strong>.
          </p>
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Information générale fondée sur des sources officielles françaises, <strong>pas un conseil juridique
            personnalisé</strong>. Les règles varient entre logement vide et meublé, et selon la zone : vérifiez
            votre cas sur service-public.fr ou auprès de l&apos;ADIL (gratuit).
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

      {/* En cas de litige */}
      <section className="py-12 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">En cas de litige : la marche à suivre</h2>
          <div className="mt-6 space-y-4">
            {litige.map((e) => (
              <div key={e.n} className="rounded-2xl border border-slate-200 bg-white p-5 flex gap-4">
                <span className="flex-shrink-0 w-9 h-9 rounded-full bg-teal-100 text-teal-800 font-bold flex items-center justify-center">{e.n}</span>
                <div>
                  <h3 className="font-bold tracking-tight">{e.t}</h3>
                  <p className="text-slate-700 text-sm mt-2 leading-relaxed">{e.d}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Documents officiels de référence */}
      <section className="py-12 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">📚 Les sources officielles</h2>
        <p className="text-slate-600 mt-2 text-sm leading-relaxed">
          Service-public.fr, Légifrance et l&apos;ANIL (réseau des ADIL) sont les références françaises du logement.
          Ces pages font foi et sont tenues à jour.
        </p>
        <div className="mt-5 flex flex-col gap-2.5">
          {documentsOfficiels.map((d) => (
            <a key={d.url} href={d.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-blue-700 bg-white border border-blue-200 hover:bg-blue-50 rounded-lg px-4 py-2.5 transition-colors">
              🔗 {d.label}
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
          ))}
        </div>
      </section>

      {/* Aide */}
      <section className="pb-14 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border-2 border-blue-200 bg-blue-50 p-6">
          <h2 className="text-xl font-bold tracking-tight text-blue-900">Besoin d&apos;aller plus loin ?</h2>
          <p className="text-blue-900/80 text-sm mt-2 leading-relaxed">
            L&apos;ADIL (Agence départementale d&apos;information sur le logement) répond gratuitement à vos questions.
            La commission départementale de conciliation est gratuite. Pour un litige lourd, l&apos;aide
            juridictionnelle peut financer un avocat selon vos revenus.
          </p>
          <div className="mt-4 flex flex-col gap-2.5">
            <a href="https://www.anil.org/" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-blue-700 bg-white border border-blue-200 hover:bg-blue-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 ANIL / ADIL — information gratuite logement
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
            <Link href="/la-loi-avec-moi-france" className="inline-flex items-center gap-1.5 text-sm font-medium text-blue-700 bg-white border border-blue-200 hover:bg-blue-100 rounded-lg px-4 py-2.5 transition-colors">
              ← Retour à tous les sujets (France)
            </Link>
          </div>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/la-loi-avec-moi-france" className="hover:text-slate-900">← Retour à tous les sujets</Link>
        <span className="mx-2 text-slate-300">·</span>
        <Link href="/loi-avec-moi/logement" className="text-slate-500 hover:text-slate-900">🇧🇪 Version Belgique</Link>
      </footer>
    </main>
  );
}
