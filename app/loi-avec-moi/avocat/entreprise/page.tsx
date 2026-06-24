"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Fiche « avocat-référent » — Entreprise & commercial (Belgique).
// Faits vérifiés : SPF Justice (insolvabilité, réorganisation & faillite),
// SPF Economie, Droits Quotidiens. Livre XX du Code de droit économique.

const pointsCles = [
  {
    t: "Le tribunal de l'entreprise est compétent",
    d: "Les litiges entre entreprises, les faillites et les procédures de réorganisation relèvent du tribunal de l'entreprise. Toute entreprise est identifiée par son numéro BCE (Banque-Carrefour des Entreprises) — pensez à l'avoir sous la main.",
  },
  {
    t: "En difficulté ? La PRJ avant la faillite",
    d: "La procédure de réorganisation judiciaire (PRJ) permet à une entreprise en difficulté d'obtenir un sursis pour se réorganiser et éviter la faillite. La loi a simplifié l'accès (moins de documents, possibilité d'accords amiables discrets). Agir TÔT augmente fortement les chances de sauvetage.",
  },
  {
    t: "La faillite obéit à des règles précises",
    d: "Une entreprise est en faillite quand elle a cessé ses paiements de manière persistante et que son crédit est ébranlé. Un curateur est désigné. Il existe des protections (notamment l'« excusabilité » / effacement de dettes pour l'entrepreneur de bonne foi) : un avocat sécurise vos droits.",
  },
  {
    t: "Impayés B2B : des leviers existent",
    d: "Pour une facture impayée entre entreprises, vous disposez d'outils : mise en demeure, intérêts et indemnités de retard, procédure de recouvrement, voire injonction de payer. Un dossier clair (contrat, bon de commande, facture, rappels) accélère le recouvrement.",
  },
  {
    t: "Contrats & statuts : la prévention paie",
    d: "Conditions générales, clauses de réserve de propriété, statuts de société adaptés : beaucoup de litiges s'évitent en amont par des contrats bien rédigés. Un avocat d'affaires intervient autant en prévention qu'en contentieux.",
  },
];

const documentsOfficiels = [
  {
    label: "SPF Justice — Réorganisation judiciaire & faillite",
    url: "https://justice.belgium.be/fr/themes_et_dossiers/societes_associations_et_fondations/insolvabilite/reorganisation_judiciaire_et",
  },
  {
    label: "SPF Economie — Fin des activités d'une entreprise",
    url: "https://economie.fgov.be/fr/themes/entreprises/fin-des-activites-dune",
  },
  {
    label: "Droits Quotidiens — Indépendant en difficulté financière : que faire ?",
    url: "https://www.droitsquotidiens.be/fr/question/je-suis-independant-en-difficulte-financiere-que-puis-je-faire",
  },
  {
    label: "SPF Finances — Faillite et liquidation",
    url: "https://finances.belgium.be/fr/pai/faillite-et-liquidation",
  },
];

const docsAApporter = [
  "Les statuts et données d'entreprise (numéro BCE)",
  "Les contrats, bons de commande et conditions générales concernés",
  "Les factures impayées, rappels et mises en demeure",
  "La comptabilité récente et tout courrier lié au litige ou aux difficultés",
];

const readText = `Avocat-référent : le droit de l'entreprise et commercial en Belgique. Cette fiche s'appuie sur des sources officielles et ne remplace pas un avocat. ${pointsCles
  .map((p) => p.t + ". " + p.d)
  .join(" ")} Les sources officielles de référence sont le SPF Justice, le SPF Economie et le SPF Finances. Message clé pour un dirigeant en difficulté : agissez tôt, la procédure de réorganisation judiciaire permet souvent d'éviter la faillite. Pour les questions d'entreprise, un avocat d'affaires intervient autant en prévention qu'en contentieux.`;

export default function AvocatEntreprisePage() {
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
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(59,130,246,0.20),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            🏢 Avocat-référent · Entreprise & commercial
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Entreprise — l&apos;essentiel, sourcé</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Litiges B2B, contrats, impayés, réorganisation, faillite : les points clés, adossés à des
            <strong className="text-white"> sources officielles</strong>. En difficulté ?
            <strong className="text-white"> Agir tôt</strong> change tout.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Agent rassurant */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-8 rounded-2xl border border-blue-100 bg-blue-50/60 p-5">
          <AgentAvocat
            name="Maître Karim"
            role="Référent · entreprise & commercial"
            accent="blue"
            message="Diriger, c'est gérer des risques. Une difficulté n'est pas une faute : prise tôt, elle se traite. On sécurise vos contrats et, s'il le faut, on protège l'entreprise."
          />
        </div>
      </section>

      {/* Encadré agir tôt */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-blue-200 bg-blue-50 p-5">
          <p className="text-blue-900 text-sm leading-relaxed">
            ⏳ <strong>En difficulté de trésorerie ?</strong> N&apos;attendez pas la cessation de paiements. La
            <strong> procédure de réorganisation judiciaire (PRJ)</strong> offre un sursis pour se réorganiser et
            éviter la faillite — mais elle est bien plus efficace <strong>tôt</strong>. Parlez-en vite à un avocat.
          </p>
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Information générale fondée sur des sources officielles, <strong>pas un conseil juridique
            personnalisé</strong>. Le droit de l&apos;entreprise est technique : <strong>consultez un avocat
            d&apos;affaires</strong> pour votre situation.
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
        <p className="text-slate-600 mt-2 text-sm leading-relaxed">Apportez ces documents à votre avocat — un dossier structuré accélère l&apos;analyse et la stratégie.</p>
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
          <h2 className="text-xl font-bold tracking-tight text-indigo-900">Trouver un avocat d&apos;affaires</h2>
          <p className="text-indigo-900/80 text-sm mt-2 leading-relaxed">
            Via l&apos;annuaire officiel. Pour un indépendant en difficulté, des dispositifs spécifiques existent ;
            selon vos revenus, le Bureau d&apos;Aide Juridique peut aussi intervenir.
          </p>
          <div className="mt-4 flex flex-col gap-2.5">
            <a href="https://avocats.be/fr" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 AVOCATS.BE — annuaire officiel
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
            <Link href="/loi-avec-moi/trouver-un-avocat" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              ⚖️ Aide juridique & autres spécialisations →
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
