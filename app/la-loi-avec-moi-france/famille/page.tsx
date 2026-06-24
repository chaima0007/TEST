"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Page « Famille & vie privée » — Édition FRANCE.
// Faits vérifiés : service-public.fr (PACS/mariage F14485, succession partenaire
// F1621, divorce consentement mutuel F10567), CNIL (droits RGPD art. 15-21,
// délai de réponse 1 mois). Distinct de l'édition belge.

const pointsCles = [
  {
    t: "Mariage, PACS, concubinage : trois statuts très différents",
    d: "Le concubinage (union libre) ne crée presque aucun droit entre partenaires. Le PACS organise la vie commune (biens, solidarité de certaines dettes) mais reste léger. Le mariage est le plus protecteur, notamment pour la succession et la pension de réversion. Choisir son statut, c'est choisir son niveau de protection.",
  },
  {
    t: "Succession : le mariage protège, pas le PACS",
    d: "Point crucial : le partenaire de PACS n'hérite PAS automatiquement. En l'absence de testament, il est traité comme un tiers et ne reçoit rien de la loi. Le conjoint marié, lui, est héritier légal. Si vous êtes pacsé, un testament est indispensable pour protéger l'autre — il sera alors exonéré de droits de succession. Le concubin, sans testament, n'a aucun droit (et 60 % de taxation s'il est légué).",
  },
  {
    t: "Divorce par consentement mutuel : sans juge, mais avec deux avocats",
    d: "Depuis 2017, le divorce amiable se fait sans passer devant le juge : une convention rédigée par avocats, puis déposée chez un notaire. Mais chaque époux doit avoir son propre avocat (deux avocats au total). Comptez en moyenne 2 à 4 mois. Le juge n'intervient que si un enfant mineur demande à être entendu.",
  },
  {
    t: "Enfants : l'autorité parentale reste conjointe",
    d: "Après une séparation, les deux parents conservent en principe l'autorité parentale conjointe : les décisions importantes (santé, école, etc.) se prennent à deux. La résidence de l'enfant et la pension alimentaire sont fixées par accord ou par le juge aux affaires familiales, toujours dans l'intérêt de l'enfant.",
  },
  {
    t: "Vie privée : la loi protège vos données personnelles",
    d: "Le RGPD vous donne des droits forts sur vos données : savoir qui les détient, les corriger, les faire effacer, vous opposer à leur usage. Tout organisme doit vous répondre dans un délai d'1 mois (3 mois si la demande est complexe, avec justification). En cas de blocage, la CNIL est votre recours gratuit.",
  },
];

const rgpd = [
  { t: "Accéder & corriger", d: "Demandez à tout organisme quelles données il détient sur vous (droit d'accès, art. 15) et faites corriger ce qui est faux (droit de rectification, art. 16)." },
  { t: "Faire effacer", d: "Le « droit à l'oubli » (art. 17) permet de demander la suppression de vos données dans de nombreux cas (consentement retiré, données plus nécessaires)." },
  { t: "Vous opposer", d: "Vous pouvez vous opposer à l'usage de vos données (art. 21), notamment à la prospection commerciale, et retirer votre consentement à tout moment." },
  { t: "Saisir la CNIL", d: "Si l'organisme ne répond pas sous 1 mois ou refuse à tort, déposez plainte gratuitement auprès de la CNIL, autorité française de protection des données." },
];

const documentsOfficiels = [
  {
    label: "Service-Public.fr — Mariage, PACS ou concubinage : différences",
    url: "https://www.service-public.gouv.fr/particuliers/vosdroits/F14485",
  },
  {
    label: "Service-Public.fr — Décès du partenaire de PACS et succession",
    url: "https://www.service-public.gouv.fr/particuliers/vosdroits/F1621",
  },
  {
    label: "Service-Public.fr — Divorce par consentement mutuel",
    url: "https://www.service-public.gouv.fr/particuliers/vosdroits/F10567",
  },
  {
    label: "CNIL — Les droits sur vos données personnelles",
    url: "https://www.cnil.fr/fr/passer-laction/les-droits-des-personnes-sur-leurs-donnees",
  },
];

const readText = `Famille et vie privée en France : vos droits. Cette page s'appuie sur service-public.fr et la CNIL et ne remplace pas un conseil personnalisé. ${pointsCles
  .map((p) => p.t + ". " + p.d)
  .join(" ")} Pour vos données personnelles, vous pouvez accéder, corriger, faire effacer et vous opposer, et saisir gratuitement la CNIL si un organisme ne répond pas dans le délai d'un mois.`;

export default function FamilleFrancePage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/la-loi-avec-moi-france" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">L</span>
            </div>
            <span className="font-bold text-lg tracking-tight">La loi avec moi <span className="text-blue-700">· France</span></span>
          </Link>
          <Link href="/la-loi-avec-moi-france" className="text-sm font-semibold text-blue-700 hover:text-blue-900">Tous les sujets →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-blue-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(244,63,94,0.20),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            🇫🇷 Famille &amp; vie privée
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Couple, enfants, données : vos droits</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Mariage, PACS, séparation, succession et protection de vos données (RGPD) : l&apos;essentiel, adossé aux
            <strong className="text-white"> sources officielles (service-public.fr, CNIL)</strong>.
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
            name="Maître Inès"
            role="Référente · droit de la famille (France)"
            accent="rose"
            message="La famille, c'est l'émotion — mais le droit, lui, est précis. Le point que trop de gens ignorent : pacsés, vous n'héritez PAS l'un de l'autre sans testament. Un document simple peut tout changer pour protéger ceux qu'on aime."
          />
        </div>
      </section>

      {/* Encadré le bon réflexe */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-rose-300 bg-rose-50 p-5">
          <p className="text-rose-900 text-sm leading-relaxed">
            🔑 <strong>À retenir :</strong> seul le <strong>mariage</strong> donne au survivant un droit successoral
            automatique. En <strong>PACS</strong>, il faut un <strong>testament</strong>. En concubinage, sans
            testament, l&apos;autre n&apos;a aucun droit.
          </p>
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Information générale fondée sur des sources officielles françaises, <strong>pas un conseil juridique
            personnalisé</strong>. Le droit de la famille dépend beaucoup de votre situation : un notaire (succession,
            testament) ou un avocat (divorce) reste indispensable pour les décisions importantes.
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

      {/* Vos données personnelles (RGPD) */}
      <section className="py-12 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">Vos données personnelles (RGPD)</h2>
          <p className="text-slate-600 mt-2 text-sm leading-relaxed">
            La vie privée, c&apos;est aussi vos données. Voici vos quatre droits essentiels, garantis par le RGPD et
            défendus gratuitement par la CNIL.
          </p>
          <div className="mt-6 grid sm:grid-cols-2 gap-4">
            {rgpd.map((r, i) => (
              <div key={i} className="rounded-2xl border border-slate-200 bg-white p-5">
                <h3 className="font-bold tracking-tight text-rose-800">{r.t}</h3>
                <p className="text-slate-700 text-sm mt-2 leading-relaxed">{r.d}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Documents officiels de référence */}
      <section className="py-12 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">📚 Les sources officielles</h2>
        <p className="text-slate-600 mt-2 text-sm leading-relaxed">
          Service-public.fr et la CNIL (autorité française de protection des données) sont les références. Ces pages
          font foi et sont tenues à jour.
        </p>
        <div className="mt-5 flex flex-col gap-2.5">
          {documentsOfficiels.map((d) => (
            <a key={d.url} href={d.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-blue-700 bg-white border border-blue-200 hover:bg-blue-50 rounded-lg px-4 py-2.5 transition-colors">
              🔗 {d.label}
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
          ))}
        </div>
      </section>

      {/* Aide */}
      <section className="pb-14 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border-2 border-blue-200 bg-blue-50 p-6">
          <h2 className="text-xl font-bold tracking-tight text-blue-900">Besoin d&apos;aller plus loin ?</h2>
          <p className="text-blue-900/80 text-sm mt-2 leading-relaxed">
            Pour un testament ou une succession, consultez un notaire. Pour un divorce, un avocat est obligatoire (et
            l&apos;aide juridictionnelle peut le financer selon vos revenus). Pour vos données, la CNIL répond et agit
            gratuitement.
          </p>
          <div className="mt-4 flex flex-col gap-2.5">
            <a href="https://www.cnil.fr/fr/plaintes" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-blue-700 bg-white border border-blue-200 hover:bg-blue-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 CNIL — déposer une plainte (gratuit)
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
            <Link href="/la-loi-avec-moi-france" className="inline-flex items-center gap-1.5 text-sm font-medium text-blue-700 bg-white border border-blue-200 hover:bg-blue-100 rounded-lg px-4 py-2.5 transition-colors">
              ← Retour à tous les sujets (France)
            </Link>
          </div>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/la-loi-avec-moi-france" className="hover:text-slate-900">← Retour à tous les sujets</Link>
        <span className="mx-2 text-slate-300">·</span>
        <Link href="/loi-avec-moi/famille" className="text-slate-500 hover:text-slate-900">🇧🇪 Version Belgique</Link>
      </footer>
    </main>
  );
}
