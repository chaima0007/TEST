"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Page « Chômage : pouvez-vous travailler ? » (Belgique).
// Faits vérifiés : ONEM (chômage complet, activité pendant le chômage, carte de contrôle eC3.2).
// Réforme entrée en vigueur le 1er mars 2026.

const pointsCles = [
  {
    t: "Oui, vous pouvez travailler — mais il faut le DÉCLARER avant",
    d: "Travailler pendant le chômage n'est pas interdit. Ce qui est interdit, c'est de ne pas le déclarer. Toute activité (pour vous-même ou pour un tiers) doit être mentionnée sur votre carte de contrôle AVANT de commencer le travail. Ne jamais déclarer une activité = travail au noir = sanctions et récupération des allocations.",
  },
  {
    t: "La carte de contrôle est désormais électronique (eC3.2)",
    d: "La carte de contrôle se complète par voie électronique (portail de la sécurité sociale ou application eC3.2 sur smartphone). Le jour où vous travaillez, vous l'indiquez AVANT de commencer. Les jours réellement chômés, vous n'indiquez rien.",
  },
  {
    t: "Un jour travaillé = pas d'allocation ce jour-là",
    d: "Pour un jour où vous exercez une activité, vous n'avez en principe pas droit à l'allocation de chômage — même si c'est un samedi, un dimanche ou un jour férié. L'idée n'est pas un « minimum d'heures » à prester, mais : activité déclarée → ce jour n'est pas indemnisé.",
  },
  {
    t: "Activité accessoire : un plafond de revenu",
    d: "Une petite activité accessoire peut, sous conditions, être cumulée avec les allocations. Mais la partie du revenu journalier qui dépasse un montant plafond (18,08 € par jour à l'index en vigueur au 1er mars 2026) vient réduire votre allocation journalière. Les règles sont précises : vérifiez votre cas sur ONEM.",
  },
  {
    t: "Lancer une activité d'indépendant : « Tremplin-indépendants »",
    d: "La mesure « Tremplin-indépendants » permet, sous conditions, de combiner pendant 12 mois maximum le développement d'une activité indépendante complémentaire avec le maintien (réduit) de vos allocations. C'est un dispositif encadré : renseignez-vous avant de vous lancer.",
  },
  {
    t: "Rester disponible — et une durée désormais limitée",
    d: "Pendant le chômage, vous devez rester disponible pour le marché de l'emploi et chercher activement du travail. Depuis le 1er mars 2026, une nouvelle réglementation du chômage est en vigueur (la durée des allocations a notamment été revue). Vérifiez votre situation personnelle auprès de l'ONEM et de votre organisme de paiement.",
  },
];

const aRetenir = [
  "Déclarez TOUTE activité avant de la commencer (carte eC3.2)",
  "Un jour travaillé n'est pas indemnisé — même le week-end",
  "Ne « rendez pas service » contre paiement sans le déclarer",
  "En cas de doute, demandez à votre organisme de paiement AVANT d'agir",
];

const documentsOfficiels = [
  {
    label: "ONEM — Chômage complet (page principale)",
    url: "https://www.onem.be/citoyens/chomage-complet",
  },
  {
    label: "ONEM — Exercer une activité pendant votre chômage (feuille T41)",
    url: "https://www.onem.be/citoyens/chomage-complet/pouvez-vous-travailler-pendant-le-chomage-/pouvez-vous-exercer-une-activite-pendant-votre-chomage-complet",
  },
  {
    label: "ONEM — Nouvelle réglementation chômage (depuis le 1er mars 2026)",
    url: "https://www.onem.be/actualites/2026/03/02/nouvelle-reglementation-chomage-en-vigueur-depuis-le-1er-mars-2026",
  },
  {
    label: "ONEM — Avez-vous droit aux allocations après une occupation ?",
    url: "https://www.onem.be/citoyens/chomage-complet/avez-vous-droit-a-une-allocation-de-chomage-/avez-vous-droit-aux-allocations-apres-une-occupation",
  },
];

const readText = `Chômage en Belgique : pouvez-vous travailler ? Cette page s'appuie sur des sources officielles de l'ONEM et ne remplace pas un conseil personnalisé. Précision importante : il n'existe pas de règle générale qui vous obligerait à travailler un certain nombre d'heures, par exemple trois heures, quand vous êtes au chômage. Ce qui compte, c'est ceci. ${pointsCles
  .map((p) => p.t + ". " + p.d)
  .join(" ")} En résumé : déclarez toute activité avant de la commencer, sachez qu'un jour travaillé n'est pas indemnisé, et vérifiez toujours votre situation auprès de l'ONEM et de votre organisme de paiement, syndicat ou CAPAC.`;

export default function ChomagePage() {
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
          <Link href="/loi-avec-moi" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Tous les sujets →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(79,70,229,0.25),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            💼 Chômage · pouvez-vous travailler ?
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Chômage & travail — ce qui est vraiment permis</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Peut-on travailler en touchant des allocations ? Oui, mais à des conditions précises.
            On vous explique la <strong className="text-white">déclaration obligatoire</strong>, l&apos;impact sur vos
            allocations et les pièges à éviter — adossé aux <strong className="text-white">sources officielles ONEM</strong>.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Agent rassurant */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-8 rounded-2xl border border-indigo-100 bg-indigo-50/50 p-5">
          <AgentAvocat
            name="Bruno"
            role="Assistant · chômage & sécurité sociale"
            accent="indigo"
            message="Bonne nouvelle : travailler un peu pendant le chômage est possible. La seule règle d'or, c'est de tout déclarer AVANT. C'est ce qui vous protège."
          />
        </div>
      </section>

      {/* Clarification honnête sur le "3 heures" */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-indigo-200 bg-indigo-50 p-5">
          <p className="text-indigo-900 text-sm leading-relaxed">
            ❓ <strong>« Au chômage, on doit travailler plus de 3 heures » — vrai ou faux ?</strong> Il n&apos;existe
            <strong> pas</strong> de règle générale qui vous oblige à prester un nombre d&apos;heures précis (3 h ou autre)
            pour avoir droit aux allocations. Le principe est différent : vous pouvez travailler, mais <strong>tout jour
            d&apos;activité doit être déclaré avant</strong> et <strong>n&apos;est pas indemnisé</strong>. Ce qui compte,
            c&apos;est la déclaration et le plafond de revenu — pas une durée minimale.
          </p>
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Information générale fondée sur des sources officielles, <strong>pas un conseil personnalisé</strong>.
            La réglementation du chômage est technique et a changé le 1er mars 2026 : <strong>vérifiez toujours votre
            situation</strong> auprès de l&apos;ONEM et de votre organisme de paiement (syndicat ou CAPAC).
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

      {/* À retenir */}
      <section className="py-12 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">✅ À retenir</h2>
          <ul className="mt-5 space-y-2.5">
            {aRetenir.map((d, i) => (
              <li key={i} className="flex items-start gap-2.5 text-sm text-slate-700 leading-relaxed">
                <span className="flex-shrink-0 text-indigo-600 mt-0.5 font-bold">✓</span>
                {d}
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* Documents officiels de référence */}
      <section className="py-12 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">📚 Les sources officielles (ONEM)</h2>
        <p className="text-slate-600 mt-2 text-sm leading-relaxed">
          L&apos;ONEM (Office National de l&apos;Emploi) est la source officielle. Ces pages font foi et sont tenues à jour.
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

      {/* Où poser sa question */}
      <section className="pb-14 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border-2 border-indigo-200 bg-indigo-50 p-6">
          <h2 className="text-xl font-bold tracking-tight text-indigo-900">Une question sur VOTRE dossier ?</h2>
          <p className="text-indigo-900/80 text-sm mt-2 leading-relaxed">
            Avant d&apos;agir, posez la question à votre <strong>organisme de paiement</strong> : votre syndicat
            (FGTB, CSC, CGSLB) ou la <strong>CAPAC</strong> (organisme public). C&apos;est gratuit et c&apos;est eux qui
            gèrent vos allocations. Pour un litige, un avocat en sécurité sociale peut aussi vous aider.
          </p>
          <div className="mt-4 flex flex-col gap-2.5">
            <a href="https://www.capac.fgov.be/fr" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 CAPAC — organisme public de paiement
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
            <Link href="/loi-avec-moi/avocat/travail" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              💼 Fiche « Travail & emploi » →
            </Link>
            <Link href="/loi-avec-moi/trouver-un-avocat" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              ⚖️ Trouver le bon avocat & aide juridique →
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
