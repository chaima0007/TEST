"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Fiche « avocat-référent » — Droit des étrangers / séjour (Belgique).
// Faits vérifiés : Office des étrangers (dofi.ibz.be), CGRA/CGVS (cgra.be),
// Conseil du Contentieux des Étrangers (rvv-cce.be). Loi du 15/12/1980.

const pointsCles = [
  {
    t: "Deux administrations différentes",
    d: "L'Office des étrangers (séjour, visa, regroupement familial, éloignement) et le Commissariat général aux réfugiés et apatrides — CGRA (demandes d'asile / protection internationale) sont deux instances distinctes. Vérifiez toujours QUI a pris la décision : cela détermine la voie de recours.",
  },
  {
    t: "La date de notification fait courir le délai",
    d: "Le délai de recours est indiqué DANS la lettre de notification qui accompagne la décision. Ce délai est souvent court (parfois 30 jours, parfois beaucoup moins selon le type de décision). Conservez l'enveloppe : la date de réception compte. Ne laissez jamais passer le délai.",
  },
  {
    t: "Le recours se porte devant le CCE",
    d: "Les décisions de l'Office des étrangers et du CGRA peuvent être contestées devant le Conseil du Contentieux des Étrangers (CCE), une juridiction administrative indépendante. Un avocat dépose et motive le recours.",
  },
  {
    t: "Effet suspensif : à vérifier au cas par cas",
    d: "Certains recours sont en principe suspensifs (on ne peut pas vous éloigner pendant l'examen, et vous gardez l'accueil) — mais pas tous, et les règles évoluent. Faites vérifier sans tarder par un avocat si votre recours suspend ou non la décision.",
  },
  {
    t: "Regroupement familial & titre de séjour : des conditions précises",
    d: "Regroupement familial, séjour étudiant, travail, séjour de longue durée : chaque statut a ses conditions (revenus, logement, assurance, documents légalisés/traduits). Un dossier complet et bien monté évite beaucoup de refus.",
  },
];

const documentsOfficiels = [
  {
    label: "Office des étrangers (IBZ) — séjour, visa, regroupement familial",
    url: "https://dofi.ibz.be/fr",
  },
  {
    label: "CGRA — Demande de protection internationale (asile)",
    url: "https://www.cgra.be/fr",
  },
  {
    label: "Conseil du Contentieux des Étrangers (CCE) — les recours",
    url: "https://www.rvv-cce.be/fr",
  },
  {
    label: "Belgium.be — Venir & séjourner en Belgique",
    url: "https://www.belgium.be/fr/famille/international",
  },
];

const docsAApporter = [
  "Votre passeport et tout titre de séjour / annexe / carte reçus",
  "La décision contestée ET son enveloppe (la date de notification est cruciale)",
  "Tous les documents du dossier (revenus, logement, état civil, légalisations, traductions)",
  "Les preuves de vos démarches et tout courrier de l'administration",
];

const readText = `Avocat-référent : le droit des étrangers et du séjour en Belgique. Cette fiche s'appuie sur des sources officielles et ne remplace pas un avocat. ${pointsCles
  .map((p) => p.t + ". " + p.d)
  .join(" ")} Les sources officielles de référence sont l'Office des étrangers, le CGRA et le Conseil du Contentieux des Étrangers. Point essentiel : le délai de recours est indiqué dans la lettre de notification et il est souvent court — agissez vite et consultez un avocat dès réception d'une décision. Le Bureau d'Aide Juridique peut désigner un avocat gratuitement ou à coût réduit selon vos revenus.`;

export default function AvocatEtrangersPage() {
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
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(56,189,248,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            🌍 Avocat-référent · Droit des étrangers
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Séjour & étrangers — l&apos;essentiel, sourcé</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Titre de séjour, regroupement familial, asile, recours : les points clés, adossés à des
            <strong className="text-white"> sources officielles</strong>. Une décision a un délai —
            consultez un avocat <strong className="text-white">dès réception</strong>.
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
            name="Yasmine"
            role="Assistante · droit des étrangers"
            accent="sky"
            message="Une décision de l'administration, c'est stressant — surtout avec un délai. Le bon réflexe : noter la date de réception et consulter un avocat tout de suite."
          />
        </div>
      </section>

      {/* Encadré délai — crucial */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-sky-300 bg-sky-50 p-5">
          <p className="text-sky-900 text-sm leading-relaxed">
            ⏱️ <strong>Le délai compte avant tout.</strong> La date de recours figure dans la lettre de notification
            et elle est souvent <strong>courte</strong>. Gardez l&apos;enveloppe, notez la date de réception, et
            contactez un avocat <strong>sans attendre</strong> : un délai dépassé peut fermer la voie de recours.
          </p>
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Information générale fondée sur des sources officielles, <strong>pas un conseil juridique
            personnalisé</strong>. Le droit des étrangers est technique et évolue souvent :
            <strong> consultez un avocat spécialisé</strong> pour votre situation.
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
        <p className="text-slate-600 mt-2 text-sm leading-relaxed">Apportez ces documents à votre avocat — vous gagnerez un temps précieux, et le délai joue contre vous.</p>
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
          <h2 className="text-xl font-bold tracking-tight text-indigo-900">Trouver un avocat en droit des étrangers</h2>
          <p className="text-indigo-900/80 text-sm mt-2 leading-relaxed">
            Via l&apos;annuaire officiel, ou gratuitement / à coût réduit selon vos revenus grâce au Bureau d&apos;Aide
            Juridique (« pro deo »). Beaucoup d&apos;avocats sont spécialisés en droit des étrangers.
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
