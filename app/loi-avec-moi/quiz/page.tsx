"use client";

import Link from "next/link";
import { useState } from "react";
import AgentAvocat from "@/components/AgentAvocat";

// Quiz « Connais-tu tes droits ? » (Belgique).
// Chaque question est adossée à une fiche du site, elle-même sourcée
// sur des références officielles. But : éducatif, honnête, et qui
// renvoie vers la bonne page pour approfondir.

type Question = {
  q: string;
  options: string[];
  correct: number;
  explication: string;
  fiche: { href: string; label: string };
};

const questions: Question[] = [
  {
    q: "Vous achetez un objet en ligne. Combien de temps avez-vous, en principe, pour vous rétracter sans justification ?",
    options: ["48 heures", "14 jours", "Aucun délai, c'est définitif"],
    correct: 1,
    explication:
      "Pour un achat à distance, vous disposez en principe de 14 jours pour vous rétracter sans devoir vous justifier. Attention : certains achats (sur mesure, contenus numériques téléchargés…) en sont exclus.",
    fiche: { href: "/loi-avec-moi/consommation", label: "Fiche Consommation & achats" },
  },
  {
    q: "Un appareil neuf acheté en magasin tombe en panne après 8 mois. Êtes-vous couvert·e ?",
    options: [
      "Non, la garantie du magasin est payante",
      "Oui : une garantie légale de 2 ans s'applique",
      "Seulement si vous avez gardé la boîte",
    ],
    correct: 1,
    explication:
      "Une garantie légale de 2 ans s'applique sur un produit neuf acheté par un consommateur auprès d'une entreprise dans l'UE. C'est un droit gratuit, qui s'ajoute à toute garantie commerciale payante.",
    fiche: { href: "/loi-avec-moi/consommation", label: "Fiche Consommation & achats" },
  },
  {
    q: "Conflit avec un voisin. Quelle démarche est GRATUITE et peut donner un accord ayant la valeur d'un jugement ?",
    options: [
      "La conciliation devant le juge de paix",
      "Engager directement un huissier",
      "Porter plainte à la police",
    ],
    correct: 0,
    explication:
      "La conciliation devant le juge de paix est gratuite et facultative. Si un accord est trouvé, le procès-verbal a la valeur d'un jugement. C'est souvent la meilleure première étape pour un conflit de voisinage.",
    fiche: { href: "/loi-avec-moi/voisinage", label: "Fiche Conflits de voisinage" },
  },
  {
    q: "Vous êtes au chômage et on vous propose un petit boulot ponctuel. Que devez-vous faire ?",
    options: [
      "Travailler au moins 3 heures, c'est obligatoire",
      "Déclarer l'activité AVANT de commencer",
      "Rien, tant que c'est moins d'une journée",
    ],
    correct: 1,
    explication:
      "Il n'existe pas de règle de « 3 heures minimum ». Le principe est la déclaration : vous devez déclarer une activité ou un travail AVANT de le commencer (carte de contrôle). Un jour travaillé n'est en général pas indemnisé.",
    fiche: { href: "/loi-avec-moi/chomage", label: "Fiche Chômage & travail" },
  },
  {
    q: "Vous vivez en couple sans être mariés ni en cohabitation légale (cohabitation de fait). Si votre partenaire décède, héritez-vous automatiquement ?",
    options: [
      "Oui, comme un couple marié",
      "Non, vous n'avez droit à rien automatiquement",
      "Oui, mais seulement la moitié",
    ],
    correct: 1,
    explication:
      "En cohabitation de fait, aucun lien juridique n'est créé : le survivant n'hérite de rien automatiquement. La cohabitation légale (déclaration à la commune) ou le mariage offrent une protection bien plus forte.",
    fiche: { href: "/loi-avec-moi/famille", label: "Fiche Famille & vie privée" },
  },
  {
    q: "Vous recevez une décision administrative défavorable. Quel est le réflexe n°1 ?",
    options: [
      "Attendre de voir si ça se confirme",
      "Repérer tout de suite la date de notification et le délai de recours",
      "La jeter si vous n'êtes pas d'accord",
    ],
    correct: 1,
    explication:
      "Le piège n°1 en administratif, c'est le délai. Notez la date de réception et cherchez le délai de recours (souvent au bas du courrier). Le recours administratif et le Médiateur fédéral sont gratuits.",
    fiche: { href: "/loi-avec-moi/demarches", label: "Fiche Démarches administratives" },
  },
  {
    q: "Vous voulez lancer votre activité d'indépendant. Quand devez-vous être inscrit·e à la BCE ?",
    options: [
      "Dans l'année qui suit le démarrage",
      "Au plus tard le jour du début de l'activité",
      "Seulement si vous dépassez un certain chiffre d'affaires",
    ],
    correct: 1,
    explication:
      "Toute activité doit être enregistrée à la Banque-Carrefour des Entreprises (BCE) au plus tard le jour du début de l'activité, via un guichet d'entreprises agréé. Votre numéro d'entreprise devient votre numéro de TVA.",
    fiche: { href: "/loi-avec-moi/creer-entreprise", label: "Fiche Créer son entreprise" },
  },
  {
    q: "Une entreprise détient des données personnelles sur vous. Pouvez-vous demander à y accéder et à les faire corriger ?",
    options: [
      "Non, c'est sa propriété",
      "Oui, le RGPD vous en donne le droit",
      "Seulement via un avocat",
    ],
    correct: 1,
    explication:
      "Le RGPD vous donne le droit d'accéder à vos données, de les corriger, et souvent de les faire effacer. En cas de blocage, vous pouvez porter plainte gratuitement auprès de l'Autorité de protection des données (APD).",
    fiche: { href: "/loi-avec-moi/famille", label: "Fiche Famille & vie privée (RGPD)" },
  },
];

function verdict(score: number, total: number) {
  const pct = (score / total) * 100;
  if (pct >= 80)
    return {
      titre: "Vous connaissez bien vos droits 👏",
      texte:
        "Beau score ! Vous avez les bons réflexes. Gardez ce site sous la main pour les détails et les sources officielles.",
      accent: "emerald" as const,
    };
  if (pct >= 50)
    return {
      titre: "Bonne base, à consolider 💪",
      texte:
        "Vous connaissez l'essentiel, mais quelques pièges classiques subsistent. Relisez les fiches liées aux questions ratées.",
      accent: "sky" as const,
    };
  return {
    titre: "Pas de panique — on est là pour ça 🤝",
    texte:
      "Personne ne naît en connaissant ses droits. Le bon réflexe, c'est justement de venir vérifier. Explorez les fiches : tout est sourcé et expliqué simplement.",
    accent: "indigo" as const,
  };
}

export default function QuizPage() {
  const [current, setCurrent] = useState(0);
  const [selected, setSelected] = useState<number | null>(null);
  const [score, setScore] = useState(0);
  const [answered, setAnswered] = useState(false);
  const [finished, setFinished] = useState(false);

  const total = questions.length;
  const question = questions[current];

  function choose(i: number) {
    if (answered) return;
    setSelected(i);
    setAnswered(true);
    if (i === question.correct) setScore((s) => s + 1);
  }

  function next() {
    if (current + 1 >= total) {
      setFinished(true);
      return;
    }
    setCurrent((c) => c + 1);
    setSelected(null);
    setAnswered(false);
  }

  function restart() {
    setCurrent(0);
    setSelected(null);
    setScore(0);
    setAnswered(false);
    setFinished(false);
  }

  const v = finished ? verdict(score, total) : null;

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

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-16 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(99,102,241,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            🧠 Quiz · Connais-tu tes droits ?
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Testez vos droits en 8 questions</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Des situations de tous les jours en Belgique. Chaque réponse est expliquée et renvoie vers une fiche
            <strong className="text-white"> sourcée officiellement</strong>. Aucun piège méchant — juste de quoi
            apprendre.
          </p>
        </div>
      </section>

      <section className="py-12 px-6 max-w-2xl mx-auto">
        {!finished ? (
          <>
            {/* Progression */}
            <div className="flex items-center justify-between text-sm font-medium text-slate-500">
              <span>Question {current + 1} / {total}</span>
              <span>Score : {score}</span>
            </div>
            <div className="mt-2 h-2 rounded-full bg-slate-100 overflow-hidden">
              <div
                className="h-full bg-indigo-500 transition-all"
                style={{ width: `${((current + (answered ? 1 : 0)) / total) * 100}%` }}
              />
            </div>

            {/* Question */}
            <h2 className="mt-8 text-xl font-bold tracking-tight leading-snug">{question.q}</h2>
            <div className="mt-6 space-y-3">
              {question.options.map((opt, i) => {
                const isCorrect = i === question.correct;
                const isChosen = i === selected;
                let cls = "border-slate-200 hover:border-indigo-300 hover:bg-indigo-50/40";
                if (answered && isCorrect) cls = "border-emerald-400 bg-emerald-50";
                else if (answered && isChosen && !isCorrect) cls = "border-rose-400 bg-rose-50";
                else if (answered) cls = "border-slate-200 opacity-60";
                return (
                  <button
                    key={i}
                    onClick={() => choose(i)}
                    disabled={answered}
                    className={`w-full text-left rounded-2xl border-2 p-4 text-sm font-medium transition-colors ${cls}`}
                  >
                    <span className="inline-flex items-center gap-3">
                      <span className="flex-shrink-0 w-6 h-6 rounded-full border border-current flex items-center justify-center text-xs">
                        {String.fromCharCode(65 + i)}
                      </span>
                      {opt}
                      {answered && isCorrect && <span className="ml-1">✓</span>}
                      {answered && isChosen && !isCorrect && <span className="ml-1">✗</span>}
                    </span>
                  </button>
                );
              })}
            </div>

            {/* Explication */}
            {answered && (
              <div className="mt-6 rounded-2xl border-2 border-indigo-200 bg-indigo-50 p-5">
                <p className="text-indigo-900 text-sm leading-relaxed">
                  {selected === question.correct ? "✅ Bonne réponse ! " : "💡 La bonne réponse : "}
                  {question.explication}
                </p>
                <Link
                  href={question.fiche.href}
                  className="mt-3 inline-flex items-center gap-1.5 text-sm font-semibold text-indigo-700 hover:text-indigo-900"
                >
                  📄 {question.fiche.label} →
                </Link>
              </div>
            )}

            {answered && (
              <button
                onClick={next}
                className="mt-6 w-full rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3.5 transition-colors"
              >
                {current + 1 >= total ? "Voir mon résultat" : "Question suivante →"}
              </button>
            )}
          </>
        ) : (
          <>
            {/* Résultat */}
            <div className="text-center">
              <p className="text-sm font-medium text-slate-500">Votre score</p>
              <p className="mt-1 text-5xl font-black tracking-tight text-indigo-700">
                {score}<span className="text-2xl text-slate-400"> / {total}</span>
              </p>
            </div>

            <div className="mt-8 rounded-2xl border border-indigo-100 bg-indigo-50/60 p-5">
              <AgentAvocat
                name="Maître Léa"
                role="Votre guide juridique"
                accent={v!.accent}
                message={v!.texte}
              />
            </div>

            <h2 className="mt-8 text-2xl font-bold tracking-tight text-center">{v!.titre}</h2>

            <div className="mt-8 flex flex-col gap-3">
              <button
                onClick={restart}
                className="w-full rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3.5 transition-colors"
              >
                🔄 Recommencer le quiz
              </button>
              <Link
                href="/loi-avec-moi"
                className="w-full text-center rounded-2xl border-2 border-indigo-200 hover:bg-indigo-50 text-indigo-700 font-semibold py-3.5 transition-colors"
              >
                Explorer tous les sujets →
              </Link>
            </div>

            <p className="mt-6 text-center text-xs text-slate-400 leading-relaxed">
              Ce quiz est éducatif et simplifié. Pour votre situation précise, consultez les fiches (sourcées
              officiellement) ou un professionnel.
            </p>
          </>
        )}
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à tous les sujets</Link>
      </footer>
    </main>
  );
}
