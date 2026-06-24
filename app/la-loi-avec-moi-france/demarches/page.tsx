"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Page « Démarches administratives » — Édition FRANCE.
// Faits vérifiés : service-public.fr (litige administration F13158, recours),
// Code de justice administrative (art. R421-1, délai 2 mois), Défenseur des
// droits (saisine gratuite, ne suspend pas les délais). Distinct de l'édition belge.

const pointsCles = [
  {
    t: "Le délai clé : 2 mois pour contester",
    d: "Une décision administrative se conteste, en principe, dans un délai de 2 mois à compter de sa notification (article R. 421-1 du Code de justice administrative). C'est le délai le plus important à connaître : passé ce délai, la décision devient définitive. Le délai ne court que si la décision mentionne les voies et délais de recours.",
  },
  {
    t: "Le recours gracieux et hiérarchique (gratuits)",
    d: "Avant le tribunal, vous pouvez écrire à l'administration : le recours gracieux s'adresse à l'auteur de la décision, le recours hiérarchique à son supérieur. Tous deux sont gratuits. Avantage majeur : un recours administratif formé dans les 2 mois interrompt le délai de recours contentieux — un nouveau délai de 2 mois repart à la réponse.",
  },
  {
    t: "Le silence de l'administration vaut souvent refus",
    d: "Si l'administration ne répond pas dans les 2 mois à votre demande, son silence vaut en général décision implicite de rejet (avec des exceptions où il vaut acceptation). À partir de ce refus implicite, le délai pour saisir le juge administratif court. Ne restez jamais dans le flou : un silence est une décision que vous pouvez attaquer.",
  },
  {
    t: "Le tribunal administratif en dernier recours",
    d: "Si le désaccord persiste, vous pouvez saisir le tribunal administratif, dans le délai de 2 mois. La requête peut souvent se faire en ligne (Télérecours citoyens) et sans avocat pour de nombreux litiges. Selon vos revenus, l'aide juridictionnelle peut financer un avocat.",
  },
  {
    t: "Le Défenseur des droits : gratuit, mais attention aux délais",
    d: "En cas de litige avec un service public (préfecture, CAF, France Travail, impôts…), le Défenseur des droits peut intervenir gratuitement, après une première tentative amiable. Important : contrairement à certaines idées reçues, sa saisine ne suspend PAS les délais de recours. Continuez donc à surveiller le délai de 2 mois en parallèle.",
  },
];

const reflexes = [
  {
    n: "1",
    t: "Lisez la décision et notez la date",
    d: "Repérez les « voies et délais de recours » en bas du courrier : ils indiquent à qui écrire et sous quel délai (souvent 2 mois). Notez la date de réception : c'est elle qui fait courir le délai. Gardez l'enveloppe et le courrier.",
  },
  {
    n: "2",
    t: "Tentez le recours gracieux ou hiérarchique",
    d: "Écrivez en recommandé avec accusé de réception, en exposant calmement vos arguments et en joignant vos preuves. Fait dans les 2 mois, ce recours préserve vos droits : il interrompt le délai pour aller devant le juge.",
  },
  {
    n: "3",
    t: "Saisissez le juge ou le Défenseur des droits",
    d: "En cas d'échec, saisissez le tribunal administratif (Télérecours citoyens) dans le délai, ou le Défenseur des droits pour les litiges avec un service public — en gardant à l'esprit que lui ne suspend pas les délais.",
  },
];

const documentsOfficiels = [
  {
    label: "Service-Public.fr — Litige avec l'administration (recours)",
    url: "https://www.service-public.gouv.fr/particuliers/vosdroits/N20312",
  },
  {
    label: "Service-Public.fr — Saisir le Défenseur des droits",
    url: "https://www.service-public.gouv.fr/particuliers/vosdroits/F13158",
  },
  {
    label: "Légifrance — Délais de recours (art. R421-1 et s., CJA)",
    url: "https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006136478",
  },
  {
    label: "Défenseur des droits — site officiel (saisine gratuite)",
    url: "https://www.defenseurdesdroits.fr/",
  },
];

const readText = `Démarches administratives en France : vos droits. Cette page s'appuie sur service-public.fr, le Code de justice administrative et le Défenseur des droits, et ne remplace pas un conseil personnalisé. ${pointsCles
  .map((p) => p.t + ". " + p.d)
  .join(" ")} Le réflexe essentiel : repérer la date de notification et le délai de deux mois, tenter un recours gracieux ou hiérarchique gratuit dans ce délai, puis saisir le tribunal administratif ou le Défenseur des droits, sachant que celui-ci ne suspend pas les délais.`;

export default function DemarchesFrancePage() {
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
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(56,189,248,0.20),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            🇫🇷 Démarches administratives
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Contester une décision de l&apos;administration</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Comprendre un courrier, vos délais, vos recours, où vous adresser : l&apos;essentiel, adossé aux
            <strong className="text-white"> sources officielles (service-public.fr, Défenseur des droits)</strong>.
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
            name="Maître Hugo"
            role="Référent · droit administratif (France)"
            accent="sky"
            message="Face à l'administration, le temps est votre meilleur allié ou votre pire ennemi. La règle d'or : repérez le délai de 2 mois, et lancez un recours gracieux gratuit avant qu'il ne soit trop tard. Un courrier bien fait suffit souvent."
          />
        </div>
      </section>

      {/* Encadré le bon réflexe */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-sky-300 bg-sky-50 p-5">
          <p className="text-sky-900 text-sm leading-relaxed">
            🔑 <strong>À retenir :</strong> vous avez en général <strong>2 mois</strong> pour contester. Un
            <strong> recours gracieux</strong> gratuit, envoyé dans ce délai, <strong>relance le compteur</strong>.
            Et le silence de l&apos;administration pendant 2 mois vaut le plus souvent <strong>refus</strong>.
          </p>
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Information générale fondée sur des sources officielles françaises, <strong>pas un conseil juridique
            personnalisé</strong>. Les délais et exceptions varient selon le type de décision : vérifiez toujours les
            « voies et délais de recours » indiqués sur votre courrier, ou sur service-public.fr.
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

      {/* Les bons réflexes */}
      <section className="py-12 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">Les bons réflexes, dans l&apos;ordre</h2>
          <div className="mt-6 space-y-4">
            {reflexes.map((e) => (
              <div key={e.n} className="rounded-2xl border border-slate-200 bg-white p-5 flex gap-4">
                <span className="flex-shrink-0 w-9 h-9 rounded-full bg-sky-100 text-sky-800 font-bold flex items-center justify-center">{e.n}</span>
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
          Service-public.fr, Légifrance et le Défenseur des droits sont les références françaises. Ces pages font foi
          et sont tenues à jour.
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
            Le Défenseur des droits aide gratuitement en cas de litige avec un service public. Pour saisir le tribunal
            administratif, Télérecours citoyens est gratuit et souvent sans avocat. L&apos;aide juridictionnelle peut
            financer un avocat selon vos revenus.
          </p>
          <div className="mt-4 flex flex-col gap-2.5">
            <a href="https://www.defenseurdesdroits.fr/saisir-le-defenseur-des-droits" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-blue-700 bg-white border border-blue-200 hover:bg-blue-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 Défenseur des droits — saisine gratuite
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
        <Link href="/loi-avec-moi/demarches" className="text-slate-500 hover:text-slate-900">🇧🇪 Version Belgique</Link>
      </footer>
    </main>
  );
}
