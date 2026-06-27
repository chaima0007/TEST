"use client";

import Link from "next/link";
import AgentAvocat from "@/components/AgentAvocat";

// Page transparence — « Qui sont nos assistants ? » (espace Belgique).
// Objectif : honnêteté totale, sans exception. Les personnages sont des assistants
// virtuels (IA + supervision humaine), pas de vrais avocats. Le titre « Maître » /
// « avocat » est protégé : on ne l'utilise jamais pour nos personnages.

const assistants = [
  { name: "Léa", role: "Assistante · droits du citoyen", accent: "indigo" as const },
  { name: "Sami", role: "Assistant · contrôle & police", accent: "sky" as const },
  { name: "Inès", role: "Assistante · famille & vie privée", accent: "rose" as const },
  { name: "Hugo", role: "Assistant · démarches administratives", accent: "blue" as const },
  { name: "Karim", role: "Assistant · travail & chômage", accent: "emerald" as const },
  { name: "Sofia", role: "Assistante · consommation", accent: "amber" as const },
];

const principes = [
  {
    titre: "Ce sont des personnages virtuels",
    texte:
      "Chaque assistant (Léa, Hugo, Inès…) est une illustration animée, pas une personne réelle. Les prénoms et les visages servent à rendre le juridique plus humain et moins intimidant — rien de plus.",
  },
  {
    titre: "Ce ne sont PAS des avocats",
    texte:
      "« Avocat » et « Maître » sont des titres protégés par la loi, réservés aux professionnels inscrits à un barreau. Nos assistants ne portent jamais ces titres et ne donnent jamais de conseil juridique personnalisé.",
  },
  {
    titre: "IA + supervision humaine",
    texte:
      "Les contenus sont préparés par des agents d'intelligence artificielle spécialisés, puis relus et validés par des humains. Chaque information renvoie vers sa source officielle pour que vous puissiez vérifier.",
  },
  {
    titre: "Information, pas conseil",
    texte:
      "Nous expliquons vos droits en termes clairs et nous vous orientons. Pour une décision importante ou un litige, nous vous dirigeons vers le bon professionnel agréé (avocat, notaire, médiateur).",
  },
];

export default function NosAssistantsPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-indigo-950 to-slate-900 text-white">
        <div
          className="absolute inset-0 opacity-40"
          style={{
            background:
              "radial-gradient(60% 60% at 50% 0%, rgba(99,102,241,0.25) 0%, rgba(15,23,42,0) 70%)",
          }}
        />
        <div className="relative max-w-3xl mx-auto px-6 py-20 text-center">
          <Link
            href="/loi-avec-moi"
            className="inline-block text-indigo-200 hover:text-white text-sm font-medium mb-6"
          >
            ← La Loi Avec Moi
          </Link>
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight">
            Qui sont nos assistants&nbsp;?
          </h1>
          <p className="mt-5 text-lg text-indigo-100 leading-relaxed">
            En toute honnêteté&nbsp;: nos guides sont des <strong>assistants virtuels</strong>, pas
            de vrais avocats. Voici exactement qui ils sont, et ce qu&apos;ils font (et ne font pas).
          </p>
        </div>
      </section>

      {/* Mise en avant honnêteté */}
      <section className="px-6 py-14 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-6">
          <h2 className="font-semibold text-amber-900 text-lg">⚖️ La règle, sans exception</h2>
          <p className="text-amber-800 mt-2 leading-relaxed">
            Sur chaque page, l&apos;avatar de l&apos;assistant affiche automatiquement la mention
            «&nbsp;<strong>Assistant virtuel · pas un avocat réel</strong>&nbsp;». C&apos;est volontaire&nbsp;:
            nous préférons être clairs trop souvent que pas assez. Vous savez toujours à qui vous parlez.
          </p>
        </div>
      </section>

      {/* Les principes */}
      <section className="px-6 pb-6 max-w-3xl mx-auto">
        <div className="grid sm:grid-cols-2 gap-5">
          {principes.map((p) => (
            <div
              key={p.titre}
              className="rounded-2xl border border-slate-200 bg-white p-6"
            >
              <h3 className="font-semibold text-slate-900">{p.titre}</h3>
              <p className="text-slate-600 text-sm mt-2 leading-relaxed">{p.texte}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Galerie des assistants */}
      <section className="px-6 py-14 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight text-center">
          Faites connaissance avec l&apos;équipe
        </h2>
        <p className="text-slate-500 text-center mt-3">
          Des prénoms chaleureux pour vous mettre à l&apos;aise — chacun spécialisé sur un domaine.
        </p>
        <div className="mt-8 grid sm:grid-cols-2 gap-6">
          {assistants.map((a) => (
            <div
              key={a.name}
              className="rounded-2xl border border-slate-200 bg-slate-50 p-5"
            >
              <AgentAvocat name={a.name} role={a.role} accent={a.accent} size={72} />
            </div>
          ))}
        </div>
      </section>

      {/* Pourquoi ce choix */}
      <section className="px-6 pb-14 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-indigo-200 bg-indigo-50 p-6">
          <h2 className="font-semibold text-indigo-900 text-lg">
            Pourquoi des assistants virtuels&nbsp;?
          </h2>
          <p className="text-indigo-800/90 mt-2 leading-relaxed text-sm">
            Le droit fait peur et coûte cher. Beaucoup de gens renoncent à faire valoir leurs droits
            simplement parce qu&apos;ils ne savent pas par où commencer. Nos assistants rendent
            l&apos;information juridique <strong>claire, gratuite et accessible 24h/24</strong>, sans
            jugement. Quand votre situation dépasse l&apos;information générale, nous vous orientons vers
            un <strong>vrai professionnel agréé</strong> — c&apos;est là que commence le conseil juridique.
          </p>
        </div>
      </section>

      {/* CTA */}
      <section className="px-6 pb-24 text-center">
        <h2 className="text-2xl font-bold tracking-tight">Une question vous bloque&nbsp;?</h2>
        <p className="text-slate-500 mt-3">
          Posez-la simplement — un assistant vous répond clairement, gratuitement.
        </p>
        <Link
          href="/contact"
          className="inline-block mt-7 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-8 py-3.5 rounded-xl transition-colors shadow-lg shadow-indigo-600/20"
        >
          Poser ma question
        </Link>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">
          ← Retour à « La Loi Avec Moi »
        </Link>
      </footer>
    </main>
  );
}
