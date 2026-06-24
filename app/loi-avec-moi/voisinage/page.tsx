"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Page « Conflits de voisinage : du dialogue à l'arbitrage » (Belgique).
// Faits vérifiés : Belgium.be (problèmes de voisinage), SPF Justice (juge de paix, médiation),
// Droits Quotidiens (conciliation, solutions négociées).

const etapes = [
  {
    n: "1",
    t: "Le dialogue direct (et l'écrit)",
    d: "Commencez par parler à votre voisin·e, calmement. Si ça ne suffit pas, écrivez un courrier daté (recommandé si possible) décrivant précisément le trouble et ce que vous demandez. Cet écrit prouvera plus tard que vous avez tenté une solution amiable.",
  },
  {
    n: "2",
    t: "La médiation volontaire",
    d: "Vous et votre voisin·e faites appel à un médiateur (de préférence agréé) qui facilite le dialogue et vous aide à trouver vous-mêmes un accord. C'est confidentiel et plus rapide qu'un procès. Un accord de médiation peut être homologué par le juge pour avoir force exécutoire.",
  },
  {
    n: "3",
    t: "La conciliation devant le juge de paix",
    d: "Avant tout procès, vous pouvez demander une conciliation au juge de paix : c'est une procédure GRATUITE et rapide. Le juge tente de rapprocher les points de vue mais ne tranche pas. Si vous trouvez un accord, il rédige un procès-verbal de conciliation qui a la valeur d'un jugement.",
  },
  {
    n: "4",
    t: "Le procès devant le juge de paix",
    d: "Si rien n'aboutit, le juge de paix est le juge compétent pour la plupart des conflits de voisinage (bruit, plantations, vues, mitoyenneté, troubles anormaux). Là, il tranche par un jugement obligatoire. Un avocat n'est pas obligatoire devant le juge de paix, mais il peut aider.",
  },
  {
    n: "5",
    t: "L'arbitrage (voie privée, par accord)",
    d: "L'arbitrage est une justice privée : par une convention (clause ou compromis d'arbitrage), vous et votre voisin·e confiez le litige à un ou plusieurs arbitres dont la décision (la « sentence ») s'impose comme un jugement. C'est rare entre voisins et payant — il faut l'accord des deux parties — mais c'est une option si vous voulez une décision privée et définitive hors tribunal.",
  },
];

const conciliationVsArbitrage = [
  {
    t: "Conciliation / médiation",
    points: [
      "Objectif : trouver un accord ensemble",
      "Le tiers ne tranche pas (il rapproche)",
      "Conciliation au juge de paix : gratuite",
      "Vous gardez la main sur la solution",
    ],
  },
  {
    t: "Arbitrage",
    points: [
      "Objectif : obtenir une décision (sentence)",
      "L'arbitre tranche, comme un juge privé",
      "Payant, nécessite l'accord des deux parties",
      "La sentence s'impose et est difficile à contester",
    ],
  },
];

const documentsOfficiels = [
  {
    label: "Belgium.be — Problèmes de voisinage",
    url: "https://www.belgium.be/fr/logement/problemes_de_logement/problemes_de_voisinage",
  },
  {
    label: "Droits Quotidiens — Comment régler mon conflit de voisinage ?",
    url: "https://www.droitsquotidiens.be/fr/question/comment-regler-mon-conflit-de-voisinage",
  },
  {
    label: "SPF Justice — La médiation, une alternative au tribunal",
    url: "https://justice.belgium.be/fr/themes_et_dossiers/mediation",
  },
  {
    label: "SPF Justice — Le juge de paix, le juge proche du citoyen (brochure)",
    url: "https://justice.belgium.be/sites/default/files/downloads/DEF-BROCHURE_VREDERECHTER_FR.pdf",
  },
];

const readText = `Conflits de voisinage en Belgique : du dialogue à l'arbitrage. Cette page s'appuie sur des sources officielles et ne remplace pas un avocat. ${etapes
  .map((e) => "Étape " + e.n + " : " + e.t + ". " + e.d)
  .join(" ")} À retenir : la conciliation devant le juge de paix est gratuite, le juge de paix est le juge compétent pour la plupart des conflits de voisinage, et l'arbitrage est une voie privée qui suppose l'accord des deux parties. Pour beaucoup de litiges, mieux vaut tenter la médiation ou la conciliation avant le procès.`;

export default function VoisinagePage() {
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
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(20,184,166,0.20),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            🏘️ Voisinage · du dialogue à l&apos;arbitrage
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Conflit de voisinage — vos solutions, sourcées</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Bruit, plantations, vues, mitoyenneté : avant le procès, il existe des voies
            <strong className="text-white"> amiables, rapides et souvent gratuites</strong>. On vous explique la médiation,
            la conciliation, le juge de paix et l&apos;arbitrage — du plus simple au plus formel.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Agent rassurant */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-8 rounded-2xl border border-teal-100 bg-teal-50/60 p-5">
          <AgentAvocat
            name="Maître Léna"
            role="Référente · voisinage & modes amiables"
            accent="teal"
            message="Un conflit de voisinage empoisonne le quotidien — mais le tribunal n'est pas la première étape. Souvent, une conciliation gratuite au juge de paix suffit à tout débloquer."
          />
        </div>
      </section>

      {/* Encadré : commencez par l'amiable */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-teal-300 bg-teal-50 p-5">
          <p className="text-teal-900 text-sm leading-relaxed">
            💡 <strong>Le bon réflexe :</strong> gardez une trace écrite de vos démarches (courriers datés, photos,
            constats). Puis tentez la <strong>conciliation gratuite</strong> devant le juge de paix avant tout procès :
            c&apos;est rapide, et un accord y a la <strong>valeur d&apos;un jugement</strong>.
          </p>
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Information générale fondée sur des sources officielles, <strong>pas un conseil juridique
            personnalisé</strong>. Chaque conflit est différent : pour un cas précis, <strong>consultez un avocat</strong>
            ou renseignez-vous auprès du juge de paix de votre canton.
          </p>
        </div>
      </section>

      {/* Les étapes */}
      <section className="py-14 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">Les étapes, du plus simple au plus formel</h2>
        <div className="mt-6 space-y-4">
          {etapes.map((e) => (
            <div key={e.n} className="rounded-2xl border border-slate-200 p-5 flex gap-4">
              <span className="flex-shrink-0 w-9 h-9 rounded-full bg-teal-100 text-teal-800 font-bold flex items-center justify-center">{e.n}</span>
              <div>
                <h3 className="font-bold tracking-tight">{e.t}</h3>
                <p className="text-slate-700 text-sm mt-2 leading-relaxed">{e.d}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Conciliation vs arbitrage */}
      <section className="py-12 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">Conciliation/médiation ou arbitrage ?</h2>
          <p className="text-slate-600 mt-2 text-sm leading-relaxed">
            Deux logiques différentes : trouver un accord ensemble, ou confier la décision à un tiers. Voici la différence.
          </p>
          <div className="mt-5 grid sm:grid-cols-2 gap-4">
            {conciliationVsArbitrage.map((c) => (
              <div key={c.t} className="rounded-2xl border border-slate-200 bg-white p-5">
                <h3 className="font-bold tracking-tight">{c.t}</h3>
                <ul className="mt-3 space-y-2">
                  {c.points.map((p, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-slate-700 leading-relaxed">
                      <span className="flex-shrink-0 text-teal-600 mt-0.5">•</span>
                      {p}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Documents officiels de référence */}
      <section className="py-12 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">📚 Les sources officielles</h2>
        <p className="text-slate-600 mt-2 text-sm leading-relaxed">
          Ces pages officielles font foi et sont tenues à jour. Vérifiez toujours la procédure exacte de votre canton.
        </p>
        <div className="mt-5 flex flex-col gap-2.5">
          {documentsOfficiels.map((d) => (
            <a key={d.url} href={d.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-50 rounded-lg px-4 py-2.5 transition-colors">
              🔗 {d.label}
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
          ))}
        </div>
      </section>

      {/* Accès avocat / aide juridique */}
      <section className="pb-14 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border-2 border-indigo-200 bg-indigo-50 p-6">
          <h2 className="text-xl font-bold tracking-tight text-indigo-900">Besoin d&apos;un coup de main ?</h2>
          <p className="text-indigo-900/80 text-sm mt-2 leading-relaxed">
            Un avocat (via l&apos;annuaire officiel, gratuitement / à coût réduit selon vos revenus grâce au Bureau
            d&apos;Aide Juridique) peut vous accompagner. Pour un bail ou un problème de logement lié, voyez aussi la
            fiche dédiée.
          </p>
          <div className="mt-4 flex flex-col gap-2.5">
            <a href="https://avocats.be/fr" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 AVOCATS.BE — annuaire officiel
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
            <Link href="/loi-avec-moi/avocat/bail" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              🏠 Fiche « Bail & immobilier » →
            </Link>
            <Link href="/loi-avec-moi/trouver-un-avocat" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              ⚖️ Trouver le bon avocat & aide juridique →
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
