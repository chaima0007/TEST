"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Fiche « avocat-référent » — Droit de la famille (Belgique).
// Faits vérifiés : Belgium.be (famille), notaire.be, SPF Justice (Tribunal de la famille),
// SECAL (Service des Créances Alimentaires). Loi du 18/07/2006 (hébergement égalitaire).

const pointsCles = [
  {
    t: "Autorité parentale : on décide à deux",
    d: "Après une séparation, les parents continuent en principe d'exercer ensemble l'autorité parentale : les décisions importantes (santé, éducation, religion, loisirs) se prennent à deux, même si l'enfant vit principalement chez l'un.",
  },
  {
    t: "Hébergement : l'égalitaire est privilégié",
    d: "Depuis la loi du 18 juillet 2006, en cas de désaccord et de saisine du juge, le Tribunal de la famille examine en priorité un hébergement égalitaire (50/50). Il peut toutefois décider d'un autre rythme si l'intérêt de l'enfant le justifie.",
  },
  {
    t: "Contribution alimentaire",
    d: "Chaque parent doit contribuer aux frais de l'enfant (nourriture, logement, santé, éducation), en proportion de ses revenus et des besoins de l'enfant. C'est une obligation qui existe dès la naissance et se poursuit après la séparation.",
  },
  {
    t: "Le Tribunal de la famille tranche — ou homologue",
    d: "Un accord amiable (éventuellement via une médiation familiale) peut être homologué par le juge : il a alors la même valeur qu'un jugement. À défaut d'accord, le Tribunal de la famille tranche les points litigieux dans l'intérêt de l'enfant.",
  },
  {
    t: "Si la contribution n'est pas payée : le SECAL",
    d: "Si l'autre parent ne paie pas la contribution alimentaire fixée, le Service des Créances Alimentaires (SECAL, au SPF Finances) peut, sous conditions, la récupérer et même verser des avances.",
  },
];

const documentsOfficiels = [
  {
    label: "Belgium.be — Divorce, séparation & autorité parentale",
    url: "https://www.belgium.be/fr/famille/couple/divorce_et_separation/autorite_parentale",
  },
  {
    label: "Notaire.be — L'hébergement des enfants",
    url: "https://www.notaire.be/relations-et-vivre-ensemble/separation-et-divorce/les-decisions-relatives-aux-enfants/lhebergement-des-enfants",
  },
  {
    label: "SPF Finances — SECAL (Service des Créances Alimentaires)",
    url: "https://finances.belgium.be/fr/particuliers/famille/pensions_alimentaires/secal",
  },
  {
    label: "Belgium.be — Le Tribunal de la famille",
    url: "https://www.belgium.be/fr/justice/organisation/cours_et_tribunaux/tribunal_de_premiere_instance/tribunal_de_la_famille",
  },
];

const docsAApporter = [
  "Votre carte d'identité et celles des enfants concernés",
  "Acte de mariage / contrat de cohabitation, et tout jugement déjà rendu",
  "Les preuves de revenus des deux parents (fiches de paie, avertissement-extrait de rôle)",
  "Les frais liés aux enfants (école, santé, garde) et tout accord écrit ou échange utile",
];

const readText = `Avocat-référent : le droit de la famille en Belgique. Cette fiche s'appuie sur des sources officielles et ne remplace pas un avocat. ${pointsCles
  .map((p) => p.t + ". " + p.d)
  .join(" ")} Les documents officiels de référence viennent de Belgium.be, du notariat, du SPF Justice et du SECAL. Avant de consulter, préparez : ${docsAApporter.join(", ")}. Si vos revenus sont modestes, le Bureau d'Aide Juridique peut désigner un avocat gratuitement ou à coût réduit.`;

export default function AvocatFamillePage() {
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
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(79,70,229,0.25),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            👨‍👩‍👧 Avocat-référent · Droit de la famille
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Famille — l&apos;essentiel, sourcé</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Séparation, garde des enfants, contribution alimentaire : les points clés, adossés à des
            <strong className="text-white"> sources officielles</strong>. Pour défendre vos droits et ceux de vos enfants,
            consultez un avocat — vous arriverez préparé·e.
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
            name="Maître Clara"
            role="Référente · droit de la famille"
            accent="violet"
            message="Une séparation touche au plus intime. Ici, on garde le cap sur l'essentiel : vos droits, et surtout l'intérêt de l'enfant."
          />
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Cette fiche est une <strong>information générale fondée sur des sources officielles</strong>, pas un
            conseil juridique personnalisé. Chaque famille est unique : <strong>consultez un avocat</strong> (ou un
            médiateur familial) pour votre situation.
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
          <h2 className="text-xl font-bold tracking-tight text-indigo-900">Trouver un avocat en droit de la famille</h2>
          <p className="text-indigo-900/80 text-sm mt-2 leading-relaxed">
            Via l&apos;annuaire officiel, ou gratuitement / à coût réduit selon vos revenus grâce au Bureau d&apos;Aide
            Juridique (« pro deo »). Une médiation familiale peut aussi éviter le tribunal.
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
