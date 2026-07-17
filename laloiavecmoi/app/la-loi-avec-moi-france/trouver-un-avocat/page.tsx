"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Page « Trouver le bon avocat » — Édition FRANCE.
// Faits vérifiés : service-public.fr (aide juridictionnelle F18074, consultation
// gratuite F20706), CNB (annuaire officiel cnb.avocat.fr, 164 barreaux),
// justice.gouv.fr (Point-justice). Barème aide juridictionnelle 2026.
// Distinct de l'édition belge.

const pointsCles = [
  {
    t: "D'abord : avez-vous vraiment besoin d'un avocat ?",
    d: "Beaucoup de litiges se règlent sans avocat : conciliateur de justice (gratuit), médiateur, recours administratif, ou même un simple courrier recommandé. Pour certaines procédures (divorce, affaires pénales graves, appel…), l'avocat est en revanche obligatoire. Avant de payer, vérifiez si une étape gratuite peut suffire.",
  },
  {
    t: "L'aide juridictionnelle peut payer votre avocat",
    d: "Si vos revenus sont modestes, l'État prend en charge tout ou partie des frais d'avocat, d'huissier et d'expertise. En 2026, l'aide est totale (100 %) jusqu'à environ 12 957 € de revenu fiscal de référence pour une personne seule, partielle (55 % puis 25 %) jusqu'à environ 15 316 € et 19 433 €. La demande se fait au bureau d'aide juridictionnelle (BAJ) du tribunal, ou en ligne.",
  },
  {
    t: "L'annuaire officiel : le CNB",
    d: "Pour trouver un avocat fiable, utilisez l'annuaire officiel du Conseil national des barreaux (cnb.avocat.fr), qui référence tous les avocats inscrits aux 164 barreaux français. Vous pouvez filtrer par ville et par domaine. C'est la source qui fait foi : un « avocat » qui n'y figure pas n'en est pas un.",
  },
  {
    t: "Des consultations gratuites existent partout",
    d: "Avant d'engager des frais, profitez des consultations gratuites : les Point-justice (lieux d'accueil gratuits et confidentiels, partout en France) et les permanences organisées par chaque barreau, où un avocat répond gratuitement et anonymement à vos premières questions.",
  },
  {
    t: "Vérifiez votre assurance « protection juridique »",
    d: "Beaucoup de contrats (habitation, carte bancaire, mutuelle…) incluent une garantie de protection juridique qui peut financer un avocat et vous conseiller, souvent sans que vous le sachiez. Vérifiez vos contrats avant de payer : cette garantie peut couvrir tout ou partie des honoraires.",
  },
];

const etapes = [
  {
    n: "1",
    t: "Cadrez votre besoin et votre budget",
    d: "Notez précisément votre problème, les dates et les pièces. Vérifiez si vous avez droit à l'aide juridictionnelle ou à une protection juridique. Identifiez s'il existe une voie gratuite (conciliateur, recours) avant l'avocat.",
  },
  {
    n: "2",
    t: "Trouvez le bon avocat (annuaire + spécialité)",
    d: "Cherchez sur l'annuaire officiel du CNB un avocat de votre région et de votre domaine (famille, travail, immobilier…). Un avocat peut mentionner des « spécialisations » officielles. N'hésitez pas à en contacter plusieurs.",
  },
  {
    n: "3",
    t: "Demandez une convention d'honoraires écrite",
    d: "Depuis la loi, la convention d'honoraires écrite est obligatoire : elle fixe le tarif (au temps passé, au forfait…) avant toute mission. Exigez-la, comparez, et ne signez rien sans avoir compris ce que vous payez.",
  },
];

const documentsOfficiels = [
  {
    label: "Annuaire officiel des avocats de France — CNB",
    url: "https://cnb.avocat.fr/annuaire-des-avocats-de-france",
  },
  {
    label: "Service-Public.fr — Aide juridictionnelle (frais de justice)",
    url: "https://www.service-public.gouv.fr/particuliers/vosdroits/F18074",
  },
  {
    label: "Service-Public.fr — Consulter gratuitement un avocat",
    url: "https://www.service-public.gouv.fr/particuliers/vosdroits/F20706",
  },
  {
    label: "Justice.gouv.fr — Trouver un Point-justice près de chez vous",
    url: "https://www.justice.gouv.fr/annuaire/lieux-daccueil-dinformation/point-justice",
  },
];

const readText = `Trouver le bon avocat en France. Cette page s'appuie sur service-public.fr, le Conseil national des barreaux et le ministère de la Justice, et ne remplace pas un conseil personnalisé. ${pointsCles
  .map((p) => p.t + ". " + p.d)
  .join(" ")} Le réflexe gagnant : vérifier l'aide juridictionnelle et votre protection juridique, utiliser l'annuaire officiel du CNB, profiter des consultations gratuites des Point-justice, et exiger une convention d'honoraires écrite avant toute mission.`;

export default function TrouverAvocatFrancePage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/la-loi-avec-moi-france" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La Loi Avec Moi <span className="text-blue-700">· France</span></span>
          </Link>
          <Link href="/la-loi-avec-moi-france" className="text-sm font-semibold text-blue-700 hover:text-blue-900">Tous les sujets →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-blue-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(245,158,11,0.18),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            🇫🇷 Trouver le bon avocat
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Le bon avocat, au bon prix</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Aide juridictionnelle, annuaire officiel, consultations gratuites, honoraires : comment s&apos;y prendre,
            adossé aux <strong className="text-white">sources officielles (service-public.fr, CNB)</strong>.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Agent rassurant */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-8 rounded-2xl border border-amber-100 bg-amber-50/60 p-5">
          <AgentAvocat
            name="Sofia"
            role="Assistante · accès au droit (France)"
            accent="amber"
            message="Un bon avocat, ce n'est pas forcément le plus cher. Le réflexe malin : vérifier d'abord l'aide juridictionnelle et votre assurance protection juridique, profiter d'une consultation gratuite, puis exiger une convention d'honoraires écrite. Vous gardez la main."
          />
        </div>
      </section>

      {/* Encadré le bon réflexe */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-300 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            🔑 <strong>À retenir :</strong> avec des revenus modestes, l&apos;<strong>aide juridictionnelle</strong>
            peut payer 100 % de votre avocat. Et avant de signer, la <strong>convention d&apos;honoraires écrite</strong>
            est obligatoire — exigez-la.
          </p>
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Information générale fondée sur des sources officielles françaises, <strong>pas un conseil juridique
            personnalisé</strong>. Les barèmes de l&apos;aide juridictionnelle sont revalorisés chaque année :
            vérifiez les montants exacts sur service-public.fr avant toute démarche.
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

      {/* Les étapes */}
      <section className="py-12 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">Comment s&apos;y prendre, étape par étape</h2>
          <div className="mt-6 space-y-4">
            {etapes.map((e) => (
              <div key={e.n} className="rounded-2xl border border-slate-200 bg-white p-5 flex gap-4">
                <span className="flex-shrink-0 w-9 h-9 rounded-full bg-amber-100 text-amber-800 font-bold flex items-center justify-center">{e.n}</span>
                <div>
                  <h3 className="font-bold tracking-tight">{e.t}</h3>
                  <p className="text-slate-700 text-sm mt-2 leading-relaxed">{e.d}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Documents officiels de référence */}
      <section className="py-12 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">📚 Les sources officielles</h2>
        <p className="text-slate-600 mt-2 text-sm leading-relaxed">
          Le Conseil national des barreaux (CNB), service-public.fr et le ministère de la Justice sont les références.
          Ces pages font foi et sont tenues à jour.
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
            Les Point-justice offrent une première consultation gratuite et confidentielle partout en France. Pour
            choisir un avocat, l&apos;annuaire officiel du CNB est la référence. Et n&apos;oubliez pas l&apos;aide
            juridictionnelle si vos revenus sont modestes.
          </p>
          <div className="mt-4 flex flex-col gap-2.5">
            <a href="https://cnb.avocat.fr/annuaire-des-avocats-de-france" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-blue-700 bg-white border border-blue-200 hover:bg-blue-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 Annuaire officiel des avocats (CNB)
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
        <Link href="/loi-avec-moi/trouver-un-avocat" className="text-slate-500 hover:text-slate-900">🇧🇪 Version Belgique</Link>
      </footer>
    </main>
  );
}
