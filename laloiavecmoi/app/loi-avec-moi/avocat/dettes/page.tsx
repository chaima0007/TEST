"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Fiche « avocat-référent » — Dettes & surendettement (Belgique).
// Faits vérifiés : SPF Justice (règlement collectif de dettes), SPF Finances,
// Droits Quotidiens, Wikifin. Procédure RCD devant le tribunal du travail.

const pointsCles = [
  {
    t: "Le règlement collectif de dettes (RCD)",
    d: "Si vous êtes une personne non commerçante durablement incapable de payer vos dettes, vous pouvez demander un règlement collectif de dettes. C'est une procédure judiciaire qui vise à rembourser vos dettes tout en vous garantissant une vie conforme à la dignité humaine.",
  },
  {
    t: "La demande se fait au tribunal du travail",
    d: "La requête en RCD s'introduit auprès du tribunal du travail de l'arrondissement où vous habitez. Si la requête est complète, le juge statue rapidement (souvent l'ordonnance d'admissibilité tombe dans les semaines qui suivent le dépôt).",
  },
  {
    t: "Un médiateur de dettes est désigné",
    d: "Le juge désigne un médiateur de dettes (avocat ou service agréé) qui négocie avec vos créanciers un plan de remboursement et gère vos revenus. Vous recevez un « pécule de médiation » pour vivre dignement pendant la procédure.",
  },
  {
    t: "Un plan limité dans le temps",
    d: "Le plan de remboursement est encadré et limité dans le temps (en règle, jusqu'à 7 ans maximum). Pendant la procédure, vous êtes protégé·e : les poursuites individuelles et la course aux saisies sont suspendues.",
  },
  {
    t: "Avant le tribunal : la médiation de dettes",
    d: "Sans aller jusqu'au RCD, un service de médiation de dettes (souvent au CPAS ou dans un service agréé) peut vous aider à négocier avec vos créanciers, vérifier la légalité des frais réclamés, et établir un budget. C'est gratuit ou peu coûteux.",
  },
];

const documentsOfficiels = [
  {
    label: "SPF Justice — Règlement collectif de dettes",
    url: "https://justice.belgium.be/fr",
  },
  {
    label: "SPF Finances — Règlement collectif de dettes",
    url: "https://finances.belgium.be/fr/pai/r%C3%A8glement-collectif-de-dettes",
  },
  {
    label: "Droits Quotidiens — Demander un RCD (langage clair)",
    url: "https://www.droitsquotidiens.be/fr/question/comment-demander-un-reglement-collectif-de-dettes-rcd-et-qui-sadresser",
  },
  {
    label: "Wikifin — Que faire si vous n'arrivez plus à rembourser ?",
    url: "https://www.wikifin.be/fr/budget-payer-emprunter-et-assurer/pret-et-credit/comment-rembourser-un-emprunt-ou-un-credit/que",
  },
];

const docsAApporter = [
  "La liste de toutes vos dettes et les courriers des créanciers / huissiers",
  "Vos preuves de revenus et de charges (loyer, énergie, alimentation)",
  "Les contrats de crédit, factures et mises en demeure reçues",
  "Tout jugement, saisie ou plan de paiement déjà en cours",
];

const readText = `Avocat-référent : les dettes et le surendettement en Belgique. Cette fiche s'appuie sur des sources officielles et ne remplace pas un avocat. ${pointsCles
  .map((p) => p.t + ". " + p.d)
  .join(" ")} Les sources officielles de référence sont le SPF Justice, le SPF Finances, Droits Quotidiens et Wikifin. Bon à savoir : le règlement collectif de dettes se demande au tribunal du travail, et avant cela un service de médiation de dettes, souvent au CPAS, peut vous aider gratuitement. Le Bureau d'Aide Juridique peut désigner un avocat gratuitement ou à coût réduit selon vos revenus.`;

export default function AvocatDettesPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La loi avec moi</span>
          </Link>
          <Link href="/loi-avec-moi/trouver-un-avocat" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">← Toutes les spécialisations</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(16,185,129,0.20),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            💶 Avocat-référent · Dettes & surendettement
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Dettes — il existe des solutions, sourcées</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Surendettement, saisies, médiation, règlement collectif de dettes : les points clés, adossés à des
            <strong className="text-white"> sources officielles</strong>. Trop de dettes n&apos;est pas une fatalité —
            la loi prévoit une issue digne.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Agent rassurant */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-8 rounded-2xl border border-emerald-100 bg-emerald-50/60 p-5">
          <AgentAvocat
            name="Tom"
            role="Assistant · dettes & surendettement"
            accent="emerald"
            message="Les dettes, ça isole et ça fait honte — à tort. La loi prévoit une vraie sortie : on protège votre dignité pendant qu'on rembourse à votre rythme."
          />
        </div>
      </section>

      {/* Encadré espoir / action */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-emerald-300 bg-emerald-50 p-5">
          <p className="text-emerald-900 text-sm leading-relaxed">
            ✅ <strong>Premier réflexe gratuit :</strong> un service de médiation de dettes (souvent au
            <strong> CPAS</strong> de votre commune) peut vous recevoir, vérifier la légalité des frais réclamés et
            négocier avec vos créanciers — <strong>sans frais</strong> ou presque, avant même d&apos;aller au tribunal.
          </p>
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Information générale fondée sur des sources officielles, <strong>pas un conseil juridique
            personnalisé</strong>. Chaque situation de dettes est différente : <strong>consultez un avocat ou un
            service de médiation de dettes</strong> pour la vôtre.
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
          <h2 className="text-2xl font-bold tracking-tight">📚 Les documents officiels de référence</h2>
          <p className="text-slate-600 mt-2 text-sm leading-relaxed">
            Les sources officielles sur lesquelles un avocat s&apos;appuie pour ce domaine. Toujours à jour, elles font foi.
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
        <p className="text-slate-600 mt-2 text-sm leading-relaxed">Apportez ces documents — un dossier clair accélère la mise en place d&apos;une solution.</p>
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
          <h2 className="text-xl font-bold tracking-tight text-indigo-900">Trouver de l&apos;aide pour vos dettes</h2>
          <p className="text-indigo-900/80 text-sm mt-2 leading-relaxed">
            Un avocat via l&apos;annuaire officiel (gratuitement / à coût réduit selon vos revenus grâce au Bureau
            d&apos;Aide Juridique), ou un service de médiation de dettes agréé, souvent au CPAS de votre commune.
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
