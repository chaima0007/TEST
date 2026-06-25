"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Fiche « avocat-référent » — Droit du travail (Belgique).
// Adossée aux documents officiels du SPF Emploi et au Code du travail.
// Ne remplace pas une consultation : oriente et prépare.

const pointsCles = [
  {
    t: "Fin d'un contrat à durée indéterminée",
    d: "L'employeur ou le travailleur peut rompre le contrat soit moyennant un préavis (le contrat continue pendant cette période), soit immédiatement en payant une indemnité de rupture.",
  },
  {
    t: "Délais de préavis (depuis le 01/01/2014)",
    d: "Les délais sont fixés par des barèmes selon l'ancienneté, et sont désormais identiques pour ouvriers et employés. Le préavis se notifie par lettre recommandée ou par exploit d'huissier (l'employeur), ou par un écrit remis en double (le travailleur).",
  },
  {
    t: "Motif grave",
    d: "Un licenciement (ou une démission) pour motif grave permet une rupture immédiate sans préavis ni indemnité, mais il est strictement encadré : délais courts et motivation obligatoire. À ne jamais improviser.",
  },
  {
    t: "Documents sociaux & C4",
    d: "À la fin du contrat, l'employeur doit remettre vos documents sociaux, dont le certificat de chômage (C4) qui vous permet de demander des allocations. Vérifiez que les dates et le motif y sont corrects.",
  },
];

const documentsOfficiels = [
  {
    label: "SPF Emploi — Fin du contrat (licenciement & démission)",
    url: "https://emploi.belgique.be/fr/themes/contrats-de-travail/fin-du-contrat-de-travail/fin-du-contrat-duree-indeterminee-licenciement",
  },
  {
    label: "SPF Emploi — Délais de préavis (contrats depuis 2014)",
    url: "https://emploi.belgique.be/fr/themes/contrats-de-travail/fin-du-contrat-de-travail/fin-du-contrat-duree-indeterminee-11",
  },
  {
    label: "SPF Emploi — Motif grave & acte équipollent à rupture",
    url: "https://emploi.belgique.be/fr/themes/contrats-de-travail/fin-du-contrat-de-travail/modes-de-rupture-communs-tous-les-contrats-le",
  },
  {
    label: "Belgium.be — Préavis et licenciement",
    url: "https://www.belgium.be/fr/emploi/contrats_de_travail/preavis_et_licenciement",
  },
];

const docsAApporter = [
  "Votre contrat de travail et le règlement de travail",
  "Vos fiches de paie et votre compte individuel",
  "La lettre de licenciement et le C4 (le cas échéant)",
  "Tout email, avertissement, certificat médical ou témoignage utile",
];

const readText = `Avocat-référent : le droit du travail en Belgique. Cette fiche s'appuie sur les documents officiels du SPF Emploi et ne remplace pas un avocat. ${pointsCles
  .map((p) => p.t + ". " + p.d)
  .join(" ")} Les documents officiels de référence sont ceux du SPF Emploi et de Belgium.be. Avant de consulter, préparez : ${docsAApporter.join(", ")}. Si vos revenus sont modestes, le Bureau d'Aide Juridique peut vous désigner un avocat gratuitement ou à coût réduit.`;

export default function AvocatTravailPage() {
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
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(79,70,229,0.25),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            💼 Avocat-référent · Droit du travail
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Droit du travail — l&apos;essentiel, sourcé</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Licenciement, préavis, motif grave, documents de fin de contrat : les points clés, adossés aux
            <strong className="text-white"> documents officiels du SPF Emploi</strong>. Pour défendre vos droits,
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
            name="Yann"
            role="Assistant · droit du travail"
            accent="indigo"
            message="Perdre ou quitter un emploi, c'est stressant. On va à l'essentiel, vous saurez quoi vérifier et quoi préparer."
          />
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Cette fiche est une <strong>information générale fondée sur des sources officielles</strong>, pas un
            conseil juridique personnalisé. Chaque situation est particulière (secteur, ancienneté, conventions
            collectives) : <strong>consultez un avocat</strong> pour votre cas.
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
            Voici les sources officielles sur lesquelles un avocat s&apos;appuie pour ce domaine. Toujours à jour,
            elles font foi.
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
          <h2 className="text-xl font-bold tracking-tight text-indigo-900">Trouver un avocat en droit du travail</h2>
          <p className="text-indigo-900/80 text-sm mt-2 leading-relaxed">
            Via l&apos;annuaire officiel, ou gratuitement / à coût réduit selon vos revenus grâce au Bureau d&apos;Aide
            Juridique (« pro deo »).
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
