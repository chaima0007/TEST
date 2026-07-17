"use client";

import Link from "next/link";
import { useState } from "react";
import AgentAvocat from "@/components/AgentAvocat";

// Quiz « Connais-tu tes droits ? » — Édition FRANCE.
// Chaque question est adossée à une fiche de l'édition France, sourcée sur des
// références officielles françaises (service-public.fr, CNIL, code.travail.gouv.fr…).
// But : éducatif, honnête, et qui renvoie vers la bonne page pour approfondir.

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
      "Pour un achat à distance, vous disposez en principe de 14 jours pour vous rétracter sans avoir à vous justifier. Certains achats (sur mesure, contenus numériques téléchargés…) en sont exclus.",
    fiche: { href: "/la-loi-avec-moi-france/consommation", label: "Fiche Consommation (France)" },
  },
  {
    q: "Un appareil neuf acheté en magasin tombe en panne après 8 mois. Êtes-vous couvert·e ?",
    options: [
      "Non, la garantie du magasin est payante",
      "Oui : la garantie légale de conformité de 2 ans s'applique",
      "Seulement si vous avez gardé la boîte",
    ],
    correct: 1,
    explication:
      "La garantie légale de conformité de 2 ans s'applique aux biens neufs vendus par un professionnel à un consommateur. C'est un droit gratuit, distinct de toute garantie commerciale payante.",
    fiche: { href: "/la-loi-avec-moi-france/consommation", label: "Fiche Consommation (France)" },
  },
  {
    q: "Vous louez un logement vide en zone tendue (Paris, Lyon…). Quel est votre préavis de départ ?",
    options: ["3 mois, sans exception", "1 mois", "6 mois"],
    correct: 1,
    explication:
      "Le préavis du locataire est en principe de 3 mois pour un logement vide, mais il tombe à 1 mois en zone tendue (et dans d'autres cas : perte d'emploi, mutation, RSA, AAH, santé…). En meublé, c'est 1 mois partout.",
    fiche: { href: "/la-loi-avec-moi-france/logement", label: "Fiche Logement & bail (France)" },
  },
  {
    q: "Vous signez une rupture conventionnelle avec votre employeur. Pouvez-vous revenir en arrière ?",
    options: [
      "Non, une fois signé c'est définitif",
      "Oui : un délai de rétractation de 15 jours s'applique",
      "Oui, mais seulement dans les 24 heures",
    ],
    correct: 1,
    explication:
      "Après la signature de la convention de rupture, chaque partie dispose d'un délai de rétractation de 15 jours calendaires. Ensuite seulement, la convention est envoyée à l'administration pour homologation.",
    fiche: { href: "/la-loi-avec-moi-france/travail", label: "Fiche Travail & emploi (France)" },
  },
  {
    q: "Vous êtes pacsé·e (PACS). Si votre partenaire décède sans testament, héritez-vous automatiquement ?",
    options: [
      "Oui, comme un couple marié",
      "Non : sans testament, le partenaire de PACS n'hérite de rien",
      "Oui, mais seulement la moitié",
    ],
    correct: 1,
    explication:
      "Contrairement au mariage, le PACS ne donne aucun droit successoral automatique. Sans testament, le partenaire survivant est traité comme un tiers. Un testament le protège (et il est alors exonéré de droits de succession).",
    fiche: { href: "/la-loi-avec-moi-france/famille", label: "Fiche Famille & vie privée (France)" },
  },
  {
    q: "Vous recevez une décision défavorable de l'administration. Quel est, en principe, le délai pour la contester ?",
    options: ["2 mois", "1 an", "Aucun délai"],
    correct: 0,
    explication:
      "Le délai de recours est en principe de 2 mois à compter de la notification (art. R. 421-1 du Code de justice administrative). Un recours gracieux gratuit, fait dans ce délai, interrompt le compteur. Repérez toujours la date !",
    fiche: { href: "/la-loi-avec-moi-france/demarches", label: "Fiche Démarches administratives (France)" },
  },
  {
    q: "Vous estimez avoir été licencié·e à tort. Combien de temps avez-vous, en principe, pour saisir les prud'hommes ?",
    options: ["1 mois", "12 mois", "5 ans"],
    correct: 1,
    explication:
      "Pour contester la rupture de votre contrat de travail, vous disposez en principe de 12 mois à compter de la notification du licenciement pour saisir le conseil de prud'hommes. Passé ce délai, l'action n'est plus recevable.",
    fiche: { href: "/la-loi-avec-moi-france/travail", label: "Fiche Travail & emploi (France)" },
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
      "Le RGPD vous donne le droit d'accéder à vos données, de les corriger et souvent de les faire effacer. L'organisme doit répondre sous 1 mois. En cas de blocage, vous pouvez saisir gratuitement la CNIL.",
    fiche: { href: "/la-loi-avec-moi-france/famille", label: "Fiche Famille & vie privée (RGPD)" },
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
    accent: "blue" as const,
  };
}

export default function QuizFrancePage() {
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
          <Link href="/la-loi-avec-moi-france" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La Loi Avec Moi <span className="text-blue-700">· France</span></span>
          </Link>
          <Link href="/la-loi-avec-moi-france" className="text-sm font-semibold text-blue-700 hover:text-blue-900">Tous les sujets →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-blue-950 to-slate-900 text-white py-16 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(37,99,235,0.24),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            🧠 Quiz · Connais-tu tes droits ?
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Testez vos droits en 8 questions</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Des situations de tous les jours en France. Chaque réponse est expliquée et renvoie vers une fiche
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
                className="h-full bg-blue-600 transition-all"
                style={{ width: `${((current + (answered ? 1 : 0)) / total) * 100}%` }}
              />
            </div>

            {/* Question */}
            <h2 className="mt-8 text-xl font-bold tracking-tight leading-snug">{question.q}</h2>
            <div className="mt-6 space-y-3">
              {question.options.map((opt, i) => {
                const isCorrect = i === question.correct;
                const isChosen = i === selected;
                let cls = "border-slate-200 hover:border-blue-300 hover:bg-blue-50/40";
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
              <div className="mt-6 rounded-2xl border-2 border-blue-200 bg-blue-50 p-5">
                <p className="text-blue-900 text-sm leading-relaxed">
                  {selected === question.correct ? "✅ Bonne réponse ! " : "💡 La bonne réponse : "}
                  {question.explication}
                </p>
                <Link
                  href={question.fiche.href}
                  className="mt-3 inline-flex items-center gap-1.5 text-sm font-semibold text-blue-700 hover:text-blue-900"
                >
                  📄 {question.fiche.label} →
                </Link>
              </div>
            )}

            {answered && (
              <button
                onClick={next}
                className="mt-6 w-full rounded-2xl bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3.5 transition-colors"
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
              <p className="mt-1 text-5xl font-black tracking-tight text-blue-700">
                {score}<span className="text-2xl text-slate-400"> / {total}</span>
              </p>
            </div>

            <div className="mt-8 rounded-2xl border border-blue-100 bg-blue-50/60 p-5">
              <AgentAvocat
                name="Léa"
                role="Votre assistante juridique (France)"
                accent={v!.accent}
                message={v!.texte}
              />
            </div>

            <h2 className="mt-8 text-2xl font-bold tracking-tight text-center">{v!.titre}</h2>

            <div className="mt-8 flex flex-col gap-3">
              <button
                onClick={restart}
                className="w-full rounded-2xl bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3.5 transition-colors"
              >
                🔄 Recommencer le quiz
              </button>
              <Link
                href="/la-loi-avec-moi-france"
                className="w-full text-center rounded-2xl border-2 border-blue-200 hover:bg-blue-50 text-blue-700 font-semibold py-3.5 transition-colors"
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
        <Link href="/la-loi-avec-moi-france" className="hover:text-slate-900">← Retour à tous les sujets</Link>
        <span className="mx-2 text-slate-300">·</span>
        <Link href="/loi-avec-moi/quiz" className="text-slate-500 hover:text-slate-900">🇧🇪 Version Belgique</Link>
      </footer>
    </main>
  );
}
