"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Fiche « avocat-référent » — Accidents & responsabilité (Belgique).
// Faits vérifiés : SPF Justice (victimes), Droits Quotidiens (assurance, usagers faibles),
// Fonds des accidents médicaux. Indemnisation automatique des usagers faibles (art. 29bis).

const pointsCles = [
  {
    t: "Usagers faibles : indemnisation automatique",
    d: "Piéton, cycliste, passager : si un véhicule automoteur est impliqué, l'assureur de ce véhicule doit indemniser automatiquement votre dommage corporel — sans débat sur votre éventuelle faute. Attention : l'assureur ne bouge pas tout seul, c'est à vous (ou votre avocat) de faire la demande.",
  },
  {
    t: "L'assureur a des délais à respecter",
    d: "Quand vous demandez par écrit à être indemnisé·e, l'assureur doit en principe répondre dans les 3 mois. Si vous acceptez sa proposition, il doit payer dans les 30 jours. Gardez une copie datée de toutes vos demandes écrites.",
  },
  {
    t: "Ne signez pas une offre trop vite",
    d: "Une première offre d'assurance peut sous-évaluer un dommage corporel (séquelles, incapacité, douleurs futures). Avant de signer une transaction, faites évaluer votre préjudice — un avocat et un médecin-conseil indépendant protègent vos intérêts.",
  },
  {
    t: "L'expertise médicale est centrale",
    d: "L'ampleur de l'indemnisation dépend de l'expertise médicale (taux d'incapacité, durée, séquelles). Vous pouvez être assisté·e d'un médecin-conseil de victime face au médecin de l'assurance : c'est souvent décisif sur le montant.",
  },
  {
    t: "Faute médicale : le Fonds des accidents médicaux",
    d: "En cas de dommage lié à des soins de santé, le Fonds des accidents médicaux (FAM) peut, sous conditions, examiner gratuitement votre dossier et indemniser certains accidents médicaux, y compris sans faute. Un avocat vous aide à choisir entre cette voie et l'action en responsabilité.",
  },
];

const documentsOfficiels = [
  {
    label: "SPF Justice — Victimes : information & droits",
    url: "https://justice.belgium.be/fr/themes_et_dossiers/que_faire_comme/victime",
  },
  {
    label: "Droits Quotidiens — Assurance : 3 mois pour répondre, 30 jours pour payer",
    url: "https://www.droitsquotidiens.be/fr/actualites/assurance-3-mois-pour-repondre-et-30-jours-pour-payer",
  },
  {
    label: "Droits Quotidiens — Quels dommages sont indemnisés automatiquement ?",
    url: "https://www.droitsquotidiens.be/fr/question/quels-dommages-sont-indemnises-automatiquement",
  },
  {
    label: "Droits Quotidiens — Le Fonds des accidents médicaux (faute médicale)",
    url: "https://www.droitsquotidiens.be/fr/question/mon-medecin-commis-une-faute-medicale-puis-je-demander-laide-du-fonds-des-accidents",
  },
];

const docsAApporter = [
  "Le constat amiable et/ou le PV de police de l'accident",
  "Tous les certificats, rapports et factures médicales",
  "Les échanges avec l'assurance et toute offre d'indemnisation reçue",
  "Les justificatifs de frais, de pertes de revenus et de l'incapacité",
];

const readText = `Avocat-référent : les accidents et la responsabilité en Belgique. Cette fiche s'appuie sur des sources officielles et ne remplace pas un avocat. ${pointsCles
  .map((p) => p.t + ". " + p.d)
  .join(" ")} Les sources officielles de référence sont le SPF Justice, Droits Quotidiens et le Fonds des accidents médicaux. Conseil essentiel : ne signez jamais une transaction d'assurance sans avoir fait évaluer votre préjudice, surtout en cas de dommage corporel. Le Bureau d'Aide Juridique peut désigner un avocat gratuitement ou à coût réduit selon vos revenus.`;

export default function AvocatAccidentsPage() {
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
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(244,63,94,0.20),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            🚑 Avocat-référent · Accidents & responsabilité
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Accident — vos droits, sourcés</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Accident de la route, dommage corporel, litige d&apos;assurance, faute médicale : les points clés, adossés à des
            <strong className="text-white"> sources officielles</strong>. Avant de signer une offre,
            <strong className="text-white"> faites évaluer votre préjudice</strong>.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Agent rassurant */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-8 rounded-2xl border border-rose-100 bg-rose-50/60 p-5">
          <AgentAvocat
            name="Maître Sofia"
            role="Référente · accidents & dommage corporel"
            accent="rose"
            message="Après un accident, on a juste envie que ça se termine — et c'est là qu'on signe trop vite. Prenez le temps : votre santé future a une valeur, on la chiffre correctement."
          />
        </div>
      </section>

      {/* Encadré ne pas signer trop vite */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-rose-200 bg-rose-50 p-5">
          <p className="text-rose-900 text-sm leading-relaxed">
            ✋ <strong>Avant de signer une offre d&apos;assurance :</strong> une transaction signée est difficile à
            revenir dessus. En cas de dommage corporel, <strong>faites évaluer vos séquelles</strong> par un
            médecin-conseil de victime et un avocat — l&apos;écart de montant est souvent important.
          </p>
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Information générale fondée sur des sources officielles, <strong>pas un conseil juridique
            personnalisé</strong>. L&apos;indemnisation dépend de chaque dossier : <strong>consultez un avocat</strong>
            spécialisé en dommage corporel.
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
        <p className="text-slate-600 mt-2 text-sm leading-relaxed">Apportez ces documents à votre avocat — ils sont la base du calcul de votre indemnisation.</p>
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
          <h2 className="text-xl font-bold tracking-tight text-indigo-900">Trouver un avocat en dommage corporel</h2>
          <p className="text-indigo-900/80 text-sm mt-2 leading-relaxed">
            Via l&apos;annuaire officiel, ou gratuitement / à coût réduit selon vos revenus grâce au Bureau d&apos;Aide
            Juridique (« pro deo »). Vérifiez aussi votre assurance « protection juridique » : elle couvre souvent ces frais.
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
