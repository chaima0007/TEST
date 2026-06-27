"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Fiche « avocat-référent » — Droit pénal (Belgique).
// Faits vérifiés : Police.be (audition & droits), SPF Justice (déclaration des droits / Salduz),
// Justice-en-ligne. Cadre : loi Franchimont (1998) et loi Salduz (2011/2014/2016).

const pointsCles = [
  {
    t: "Vous avez le droit de garder le silence",
    d: "Lors d'une audition, vous pouvez vous taire, répondre aux questions, ou faire une déclaration. Personne ne peut être contraint de s'accuser soi-même. Vous recevez aussi une déclaration écrite de vos droits avant l'audition.",
  },
  {
    t: "Droit à un avocat (loi Salduz)",
    d: "Si vous êtes suspect·e, vous avez droit à une concertation confidentielle avec un avocat AVANT l'audition, et à son assistance PENDANT l'audition. Quand la loi Salduz l'exige, l'audition ne peut pas commencer sans cet accès à l'avocat.",
  },
  {
    t: "Vos droits dépendent de votre statut",
    d: "Les droits diffèrent selon que vous êtes victime/plaignant·e, témoin, ou suspect·e — et, pour un suspect, selon que vous êtes libre ou privé·e de liberté. Demandez toujours en quelle qualité vous êtes entendu·e.",
  },
  {
    t: "Privation de liberté : un délai encadré",
    d: "En cas d'arrestation judiciaire, la Constitution fixe un délai maximum (porté à 48 heures) avant de devoir être présenté·e à un juge d'instruction, qui décide de la suite. Vous avez droit à une assistance médicale et à prévenir une personne de confiance.",
  },
  {
    t: "Victime : vous pouvez vous constituer partie civile",
    d: "En tant que victime, vous pouvez porter plainte, vous déclarer personne lésée, ou vous constituer partie civile pour demander réparation. Un avocat vous aide à choisir la voie la plus efficace.",
  },
];

const documentsOfficiels = [
  {
    label: "Police.be — Audition par la police : quels sont mes droits ?",
    url: "https://www.police.be/5337/actualites/audition-par-la-police-quels-sont-mes-droits",
  },
  {
    label: "SPF Justice — Renforcement des droits des personnes auditionnées",
    url: "https://justice.belgium.be/fr/nouvelles/communiques_de_presse/nouvelle_declaration_des_droits_renforcement_de_la_protection_des",
  },
  {
    label: "Justice-en-ligne — L'audition par la police, le parquet ou le juge d'instruction",
    url: "https://www.justice-en-ligne.be/L-audition-par-la-police-le",
  },
  {
    label: "SPF Justice — Que faire comme victime (procédure)",
    url: "https://justice.belgium.be/fr/themes_et_dossiers/que_faire_comme/victime",
  },
];

const docsAApporter = [
  "La convocation, le procès-verbal ou la citation reçue (et l'enveloppe : la date compte)",
  "Votre carte d'identité",
  "Tout élément de preuve (photos, messages, certificats médicaux, factures)",
  "Les coordonnées des témoins éventuels",
];

const readText = `Avocat-référent : le droit pénal en Belgique. Cette fiche s'appuie sur des sources officielles et ne remplace pas un avocat. ${pointsCles
  .map((p) => p.t + ". " + p.d)
  .join(" ")} Les documents officiels de référence viennent de la police, du SPF Justice et de Justice-en-ligne. Avant de consulter, préparez : ${docsAApporter.join(", ")}. Si vous êtes convoqué·e par la police, contactez un avocat avant l'audition : c'est votre droit. Le Bureau d'Aide Juridique peut en désigner un gratuitement selon vos revenus, y compris en urgence (permanence Salduz).`;

export default function AvocatPenalPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La Loi Avec Moi</span>
          </Link>
          <Link href="/loi-avec-moi/trouver-un-avocat" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">← Toutes les spécialisations</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(244,63,94,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            ⚖️ Avocat-référent · Droit pénal
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Droit pénal — vos droits, sourcés</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Convoqué·e, interrogé·e, arrêté·e, ou victime : ce que la loi vous garantit (silence, avocat, délais),
            adossé à des <strong className="text-white">sources officielles</strong>. Avant toute audition,
            consultez un avocat — c&apos;est votre droit.
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
            name="Adil"
            role="Assistant · droit pénal"
            accent="rose"
            message="Être convoqué·e fait peur, c'est normal. Retenez l'essentiel : vous pouvez vous taire, et vous avez droit à un avocat avant de parler."
          />
        </div>
      </section>

      {/* Encadré urgence */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-rose-200 bg-rose-50 p-5">
          <p className="text-rose-900 text-sm leading-relaxed">
            🚨 <strong>Convoqué·e ou arrêté·e maintenant ?</strong> Vous avez le droit de parler à un avocat
            <strong> avant</strong> l&apos;audition et de <strong>garder le silence</strong>. Demandez l&apos;assistance d&apos;un
            avocat (permanence Salduz) — y compris la nuit et le week-end.
          </p>
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Information générale fondée sur des sources officielles, <strong>pas un conseil juridique
            personnalisé</strong>. En matière pénale, les enjeux sont lourds : <strong>consultez un avocat</strong> sans tarder.
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
        <p className="text-slate-600 mt-2 text-sm leading-relaxed">Apportez ces documents à votre avocat — vous gagnerez du temps, et c&apos;est crucial en pénal.</p>
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
          <h2 className="text-xl font-bold tracking-tight text-indigo-900">Trouver un avocat pénaliste</h2>
          <p className="text-indigo-900/80 text-sm mt-2 leading-relaxed">
            Via l&apos;annuaire officiel, ou gratuitement / à coût réduit selon vos revenus grâce au Bureau d&apos;Aide
            Juridique. En cas d&apos;arrestation, une permanence d&apos;avocats (Salduz) est joignable en urgence.
          </p>
          <div className="mt-4 flex flex-col gap-2.5">
            <a href="https://avocats.be/fr" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 AVOCATS.BE — annuaire officiel
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
            <Link href="/loi-avec-moi/porter-plainte" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              📖 Vous êtes victime ? Voir « Porter plainte & vos droits » →
            </Link>
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
