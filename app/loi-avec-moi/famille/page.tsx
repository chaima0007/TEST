"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Page « Famille & vie privée » (Belgique).
// Faits vérifiés : Belgium.be (couple, divorce, autorité parentale),
// justice.belgium.be, notaire.be (cohabitation, succession), SPF Finances,
// Autorité de protection des données (APD) pour le volet RGPD.

const pointsCles = [
  {
    t: "Mariage, cohabitation légale, cohabitation de fait : trois statuts très différents",
    d: "La cohabitation de fait ne crée aucun lien juridique : si l'un décède, l'autre n'hérite de rien automatiquement et vous êtes imposés séparément. La cohabitation légale (déclaration à la commune) crée des droits : protection du logement familial et usufruit de ce logement à la succession — mais le partenaire peut vous déshériter par testament ou rompre du jour au lendemain. Le mariage offre la protection la plus large : solidarité, part réservataire garantie (on ne peut pas vous déshériter totalement) et usufruit sur toute la succession.",
  },
  {
    t: "Un contrat chez le notaire sécurise votre couple",
    d: "Sans contrat de mariage, vous tombez automatiquement sous le régime légal de communauté (ce qui s'accumule pendant le mariage devient commun). Un contrat de mariage, ou un contrat de cohabitation légale par acte notarié, permet d'organiser revenus, frais du ménage, logement et protection en cas de séparation. C'est le meilleur moment pour décider — pas après le conflit.",
  },
  {
    t: "Divorce : deux voies, selon que vous êtes d'accord ou non",
    d: "Le divorce par consentement mutuel suppose un accord complet (biens, logement, enfants, pension) déposé au tribunal de la famille — c'est le plus rapide (souvent 3 à 4 mois). À défaut d'accord, le divorce pour désunion irrémédiable s'impose : demande conjointe après 6 mois de séparation, ou unilatérale après 1 an. Les frais de greffe au tribunal sont de l'ordre de 191 € en 2026 (le coût total dépend de l'avocat).",
  },
  {
    t: "Séparation et enfants : l'autorité parentale reste conjointe",
    d: "Que vous viviez ensemble ou non, le principe légal est que les deux parents exercent ensemble l'autorité parentale (décisions importantes : santé, école, religion). Pour l'hébergement, en cas de désaccord et à la demande d'un parent, le tribunal de la famille examine en priorité l'hébergement égalitaire (semaine/semaine) — mais il peut décider autrement si c'est dans l'intérêt de l'enfant. La médiation familiale est encouragée avant le procès.",
  },
  {
    t: "Succession : vos proches ne peuvent pas être totalement déshérités",
    d: "La loi belge protège certains héritiers par une « part réservataire » : les enfants (et, dans le mariage, le conjoint survivant) ne peuvent pas être totalement écartés de l'héritage, même par testament. Vous disposez librement d'une autre partie (la « quotité disponible »). Un notaire est l'interlocuteur clé pour un testament, une donation ou une planification successorale valable.",
  },
];

const separation = [
  {
    n: "1",
    t: "Privilégiez l'accord (et écrivez-le)",
    d: "Un accord sur les enfants, le logement et l'argent — même provisoire — vous fait gagner du temps, de l'argent et beaucoup de tension. Mettez-le par écrit. C'est la base d'un divorce par consentement mutuel.",
  },
  {
    n: "2",
    t: "La médiation familiale avant le tribunal",
    d: "Un médiateur familial agréé aide les deux parties à trouver une solution équilibrée, notamment pour les enfants. C'est plus rapide et moins coûteux qu'un procès, et le tribunal de la famille y oriente souvent en premier.",
  },
  {
    n: "3",
    t: "Le tribunal de la famille tranche si besoin",
    d: "À défaut d'accord, le tribunal de la famille décide (divorce, hébergement, contribution alimentaire). Selon vos revenus, le Bureau d'Aide Juridique peut vous fournir un avocat gratuitement ou à coût réduit. Une assurance « protection juridique » peut aussi prendre en charge les frais.",
  },
];

const documentsOfficiels = [
  {
    label: "Belgium.be — Divorce & séparation",
    url: "https://www.belgium.be/fr/famille/couple/divorce_et_separation",
  },
  {
    label: "Belgium.be — Séparation et enfants (autorité parentale)",
    url: "https://www.belgium.be/fr/famille/couple/divorce_et_separation/autorite_parentale",
  },
  {
    label: "SPF Justice — Le divorce",
    url: "https://justice.belgium.be/fr/themes_et_dossiers/personnes_et_familles/divorce",
  },
  {
    label: "Notaire.be — Relations et vivre ensemble (cohabitation, mariage, succession)",
    url: "https://www.notaire.be/relations-et-vivre-ensemble",
  },
  {
    label: "Autorité de protection des données (APD) — vos droits RGPD",
    url: "https://www.autoriteprotectiondonnees.be/citoyen",
  },
];

const readText = `Famille et vie privée en Belgique : vos droits. Cette page s'appuie sur des sources officielles (Belgium.be, SPF Justice, notaires, Autorité de protection des données) et ne remplace pas un conseil personnalisé. ${pointsCles
  .map((p) => p.t + ". " + p.d)
  .join(" ")} En cas de séparation : privilégiez l'accord écrit, puis la médiation familiale, et le tribunal de la famille en dernier recours. Pour vos données personnelles, le RGPD vous donne le droit d'accéder à vos données, de les corriger et de les faire effacer, et de porter plainte auprès de l'Autorité de protection des données.`;

export default function FamillePage() {
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
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(139,92,246,0.20),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            👪 Famille &amp; vie privée
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Votre famille, vos données — vos droits</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Mariage ou cohabitation, séparation, enfants, succession, et vos droits sur vos données personnelles
            (RGPD) : l&apos;essentiel, clair et <strong className="text-white">adossé aux sources officielles</strong>,
            pour décider en confiance.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Agent rassurant */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-8 rounded-2xl border border-violet-100 bg-violet-50/60 p-5">
          <AgentAvocat
            name="Camille"
            role="Assistante · droit de la famille & vie privée"
            accent="violet"
            message="Les questions de famille touchent au plus intime. Le bon réflexe est presque toujours le même : posez les choses par écrit, et privilégiez l'accord. Un notaire ou un médiateur familial coûte bien moins cher qu'un long conflit."
          />
        </div>
      </section>

      {/* Encadré le bon réflexe */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-violet-300 bg-violet-50 p-5">
          <p className="text-violet-900 text-sm leading-relaxed">
            💡 <strong>À retenir :</strong> vivre ensemble sans rien signer (cohabitation de fait) ne protège
            quasiment <strong>pas</strong> le survivant ni le partenaire en cas de coup dur. Une déclaration de
            cohabitation légale à la commune, ou un contrat chez le notaire, change tout — et c&apos;est souvent
            gratuit ou peu coûteux.
          </p>
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Information générale fondée sur des sources officielles, <strong>pas un conseil juridique
            personnalisé</strong>. Chaque situation familiale est unique : pour un acte (contrat, testament,
            divorce), consultez un notaire ou un avocat.
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

      {/* Vie privée / RGPD */}
      <section className="py-12 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">Vos données personnelles (RGPD)</h2>
          <p className="text-slate-600 mt-2 text-sm leading-relaxed">
            En Belgique comme dans toute l&apos;UE, le RGPD vous donne des droits concrets sur vos données. C&apos;est
            l&apos;<strong>Autorité de protection des données (APD)</strong> qui veille à leur respect — et chez qui
            vous pouvez porter plainte gratuitement.
          </p>
          <div className="mt-6 grid sm:grid-cols-2 gap-4">
            <div className="rounded-2xl border border-slate-200 bg-white p-5">
              <h3 className="font-bold tracking-tight">Accéder &amp; corriger</h3>
              <p className="text-slate-700 text-sm mt-2 leading-relaxed">
                Vous pouvez demander à une entreprise ou un organisme quelles données il détient sur vous, et exiger
                la correction de ce qui est inexact.
              </p>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-white p-5">
              <h3 className="font-bold tracking-tight">Faire effacer (« droit à l&apos;oubli »)</h3>
              <p className="text-slate-700 text-sm mt-2 leading-relaxed">
                Dans bien des cas, vous pouvez demander l&apos;effacement de vos données, ou vous opposer à leur
                utilisation (par exemple à des fins de publicité).
              </p>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-white p-5">
              <h3 className="font-bold tracking-tight">Être informé·e &amp; consentir</h3>
              <p className="text-slate-700 text-sm mt-2 leading-relaxed">
                On doit vous dire clairement pourquoi vos données sont collectées. Pour beaucoup d&apos;usages, votre
                consentement libre est requis — et vous pouvez le retirer.
              </p>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-white p-5">
              <h3 className="font-bold tracking-tight">Porter plainte à l&apos;APD</h3>
              <p className="text-slate-700 text-sm mt-2 leading-relaxed">
                Si on ne répond pas à votre demande ou si vos données sont mal utilisées, vous pouvez saisir
                gratuitement l&apos;Autorité de protection des données.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Séparation : marche à suivre */}
      <section className="py-12 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">Séparation : la marche à suivre</h2>
        <div className="mt-6 space-y-4">
          {separation.map((e) => (
            <div key={e.n} className="rounded-2xl border border-slate-200 bg-white p-5 flex gap-4">
              <span className="flex-shrink-0 w-9 h-9 rounded-full bg-violet-100 text-violet-800 font-bold flex items-center justify-center">{e.n}</span>
              <div>
                <h3 className="font-bold tracking-tight">{e.t}</h3>
                <p className="text-slate-700 text-sm mt-2 leading-relaxed">{e.d}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Documents officiels de référence */}
      <section className="py-12 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">📚 Les sources officielles</h2>
          <p className="text-slate-600 mt-2 text-sm leading-relaxed">
            Belgium.be, le SPF Justice, les notaires de Belgique et l&apos;Autorité de protection des données font
            autorité et tiennent leurs pages à jour.
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

      {/* Aide */}
      <section className="py-14 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border-2 border-indigo-200 bg-indigo-50 p-6">
          <h2 className="text-xl font-bold tracking-tight text-indigo-900">Besoin d&apos;aller plus loin ?</h2>
          <p className="text-indigo-900/80 text-sm mt-2 leading-relaxed">
            Pour un contrat, un testament ou une succession, le notaire est l&apos;interlocuteur clé. Pour un divorce
            ou un conflit sur les enfants, un avocat (gratuitement / à coût réduit selon vos revenus grâce au Bureau
            d&apos;Aide Juridique) ou un médiateur familial vous accompagne.
          </p>
          <div className="mt-4 flex flex-col gap-2.5">
            <a href="https://www.notaire.be/relations-et-vivre-ensemble" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 Notaire.be — Relations &amp; vivre ensemble
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
            <Link href="/loi-avec-moi/avocat/famille" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              👪 Fiche « Avocat en droit de la famille » →
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
