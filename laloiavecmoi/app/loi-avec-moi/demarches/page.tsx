"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Page « Démarches administratives » (Belgique).
// Faits vérifiés : loi du 29 juillet 1991 (motivation formelle des actes
// administratifs), Conseil d'État (délai 60 jours), Médiateur fédéral
// (réclamation gratuite, suspension du délai), publicité de l'administration.

const pointsCles = [
  {
    t: "Une décision de l'administration doit être motivée",
    d: "Depuis la loi du 29 juillet 1991, tout acte administratif individuel doit être « formellement motivé » : la décision doit indiquer les raisons de fait et de droit qui la justifient. Même l'urgence ne dispense pas l'administration de motiver. Si une décision qui vous concerne n'explique rien, c'est déjà un argument en votre faveur.",
  },
  {
    t: "La lettre doit vous indiquer comment et dans quel délai réagir",
    d: "Quand l'administration vous notifie une décision susceptible de recours, elle doit mentionner la possibilité de recours, le délai et la forme à respecter. Lisez toujours le bas du courrier : c'est souvent là que figurent vos voies de recours. Si ces mentions manquent, le délai peut ne pas vous être opposable.",
  },
  {
    t: "Les délais sont courts : repérez la date de notification",
    d: "En administratif, les délais se comptent généralement à partir du lendemain de la notification (le jour où vous recevez la décision). Pour un recours en annulation au Conseil d'État, le délai est de 60 jours. Notez immédiatement la date de réception et n'attendez pas : un délai dépassé ferme souvent la porte définitivement.",
  },
  {
    t: "Le recours administratif (gratuit) avant le juge",
    d: "Avant d'aller devant un tribunal, beaucoup de décisions peuvent être contestées par un recours administratif : on redemande à l'administration (ou à une instance supérieure) de revoir sa décision. C'est gratuit, par écrit, et cela permet souvent de régler le problème sans procès. Respectez la forme et le délai indiqués sur la décision.",
  },
  {
    t: "Le Médiateur fédéral : gratuit, et il « gèle » votre délai",
    d: "Si vous êtes en litige avec une administration fédérale, vous pouvez saisir gratuitement le Médiateur fédéral. Avantage majeur : sa saisine suspend le délai de recours au Conseil d'État pour 4 mois maximum. Si la médiation échoue, il vous reste donc du temps pour aller au Conseil d'État. (Régions et communes ont aussi leurs médiateurs.)",
  },
];

const reflexes = [
  {
    n: "1",
    t: "Lisez la décision en entier — surtout le bas de page",
    d: "Repérez : la date de notification, ce qui vous est demandé/refusé, les motifs, et les voies de recours (qui, comment, sous quel délai). Surlignez la date limite. Gardez l'enveloppe si elle prouve la date.",
  },
  {
    n: "2",
    t: "Demandez votre dossier si besoin (publicité de l'administration)",
    d: "Vous avez le droit d'accéder aux documents administratifs qui vous concernent. Si la décision est floue, demandez par écrit copie de votre dossier : cela vous aide à comprendre et à bien motiver votre contestation.",
  },
  {
    n: "3",
    t: "Contestez par écrit, dans les délais",
    d: "Introduisez d'abord le recours administratif indiqué (gratuit), ou saisissez le Médiateur compétent. Datez et conservez une copie (e-mail ou recommandé). En dernier recours, le Conseil d'État (60 jours) ou le tribunal compétent tranche.",
  },
];

const documentsOfficiels = [
  {
    label: "Belgium.be — Services & administrations",
    url: "https://www.belgium.be/fr",
  },
  {
    label: "Médiateur fédéral — déposer une réclamation (gratuit)",
    url: "https://www.mediateurfederal.be/fr",
  },
  {
    label: "Conseil d'État — Procédure (recours en annulation)",
    url: "https://www.raadvst-consetat.be/?page=proc_adm&lang=fr",
  },
  {
    label: "BOSA — Loi du 29 juillet 1991 (motivation des actes administratifs)",
    url: "https://bosa.belgium.be/fr/regulations/loi-du-29-juillet-1991",
  },
];

const readText = `Démarches administratives en Belgique : vos droits. Cette page s'appuie sur des sources officielles et ne remplace pas un conseil personnalisé. ${pointsCles
  .map((p) => p.t + ". " + p.d)
  .join(" ")} Les bons réflexes : lisez la décision en entier, surtout le bas de page où figurent les voies de recours, repérez la date de notification, demandez votre dossier si besoin, et contestez par écrit dans les délais. Le Médiateur fédéral est gratuit et suspend votre délai de recours.`;

export default function DemarchesPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La loi avec moi</span>
          </Link>
          <Link href="/loi-avec-moi" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Tous les sujets →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(56,189,248,0.20),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            📄 Démarches administratives
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Une lettre de l&apos;administration ? On débroussaille</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Comprendre une décision, repérer vos délais, savoir où et comment réagir : l&apos;essentiel pour ne pas
            rester bloqué·e face à l&apos;administration, <strong className="text-white">adossé aux sources
            officielles</strong>.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Agent rassurant */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-8 rounded-2xl border border-sky-100 bg-sky-50/60 p-5">
          <AgentAvocat
            name="Adrien"
            role="Assistant · droit administratif"
            accent="sky"
            message="Une lettre administrative, ça impressionne — mais ça suit des règles précises qui vous protègent. La décision doit être motivée et vous indiquer comment réagir. Le réflexe n°1 : repérer la date de réception et le délai, tout de suite."
          />
        </div>
      </section>

      {/* Encadré le bon réflexe */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-sky-300 bg-sky-50 p-5">
          <p className="text-sky-900 text-sm leading-relaxed">
            ⏱️ <strong>Le piège n°1, c&apos;est le délai.</strong> Dès que vous recevez une décision qui vous
            déplaît, notez la date de réception et cherchez le délai de recours (souvent au bas du courrier).
            Le recours administratif et le Médiateur fédéral sont <strong>gratuits</strong> — et le Médiateur
            « gèle » même votre délai au Conseil d&apos;État jusqu&apos;à 4 mois.
          </p>
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Information générale fondée sur des sources officielles, <strong>pas un conseil juridique
            personnalisé</strong>. Les délais et voies de recours varient selon le type de décision et le niveau
            de pouvoir (fédéral, régional, communal) : vérifiez toujours les mentions de votre courrier.
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

      {/* Réflexes : marche à suivre */}
      <section className="py-12 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">Face à une décision : la marche à suivre</h2>
          <div className="mt-6 space-y-4">
            {reflexes.map((e) => (
              <div key={e.n} className="rounded-2xl border border-slate-200 bg-white p-5 flex gap-4">
                <span className="flex-shrink-0 w-9 h-9 rounded-full bg-sky-100 text-sky-800 font-bold flex items-center justify-center">{e.n}</span>
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
          Le portail Belgium.be, le Médiateur fédéral et le Conseil d&apos;État font autorité et tiennent leurs
          pages à jour.
        </p>
        <div className="mt-5 flex flex-col gap-2.5">
          {documentsOfficiels.map((d) => (
            <a key={d.url} href={d.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-50 rounded-lg px-4 py-2.5 transition-colors">
              🔗 {d.label}
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
          ))}
        </div>
      </section>

      {/* Aide */}
      <section className="pb-14 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border-2 border-indigo-200 bg-indigo-50 p-6">
          <h2 className="text-xl font-bold tracking-tight text-indigo-900">Besoin d&apos;aller plus loin ?</h2>
          <p className="text-indigo-900/80 text-sm mt-2 leading-relaxed">
            Le Médiateur fédéral intervient gratuitement pour les litiges avec une administration fédérale. Pour un
            recours au Conseil d&apos;État ou un dossier complexe, un avocat (gratuitement / à coût réduit selon vos
            revenus grâce au Bureau d&apos;Aide Juridique) peut vous accompagner.
          </p>
          <div className="mt-4 flex flex-col gap-2.5">
            <a href="https://www.mediateurfederal.be/fr" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 Médiateur fédéral — déposer une réclamation
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
            <Link href="/loi-avec-moi/en-cas-injustice" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              ⚖️ En cas d&apos;injustice : vos recours →
            </Link>
            <Link href="/loi-avec-moi/trouver-un-avocat" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              ⚖️ Trouver le bon avocat &amp; aide juridique →
            </Link>
          </div>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à tous les sujets</Link>
      </footer>
    </main>
  );
}
