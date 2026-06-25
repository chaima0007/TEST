"use client";

import Link from "next/link";
import { useState } from "react";
import ReadAloud from "@/components/ReadAloud";

type Sujet = {
  id: string;
  emoji: string;
  t: string;
  points: string[];
  amende?: string;
};

const sujets: Sujet[] = [
  {
    id: "bruit-nuit",
    emoji: "🌙",
    t: "Musique ou bruit la nuit (tapage nocturne)",
    points: [
      "En Belgique, le tapage nocturne vise les bruits qui troublent le voisinage la nuit — généralement entre 22h et 6h du matin.",
      "Peu importe que ce soit de la musique, une fête, des cris ou du bricolage : si ça dérange les voisins la nuit, c'est une infraction.",
      "Bon réflexe : baissez le son après 22h, prévenez vos voisins avant une fête, et privilégiez le dialogue.",
    ],
    amende: "Sanction pénale (contravention) ou amende communale (GAS) souvent de 50 à 250 € selon la commune.",
  },
  {
    id: "bruit-jour",
    emoji: "🔊",
    t: "Bruit excessif en journée (tapage diurne)",
    points: [
      "Le bruit excessif est aussi interdit le jour s'il dépasse les inconvénients normaux du voisinage (musique très forte, aboiements continus, travaux répétés).",
      "On parle de « trouble anormal de voisinage » : ce n'est pas le bruit normal de la vie, mais l'excès répété.",
      "Tondre, percer, bricoler : beaucoup de communes fixent des plages horaires (souvent pas tôt le matin, ni le dimanche après-midi). Vérifiez votre règlement communal.",
    ],
    amende: "Amende communale possible (GAS) ; surtout, médiation et obligation de faire cesser le trouble.",
  },
  {
    id: "poubelles",
    emoji: "🗑️",
    t: "Sortir ses poubelles au mauvais moment",
    points: [
      "Chaque commune (via son intercommunale) fixe les jours et les heures de collecte, et le moment où sortir vos sacs.",
      "Sortir ses déchets trop tôt (la veille en journée, par exemple) ou le mauvais jour est sanctionnable : les sacs traînent, s'éventrent, attirent les nuisibles.",
      "Utilisez les bons sacs/conteneurs de votre commune et respectez le tri : un sac non conforme peut être refusé et verbalisé.",
    ],
    amende: "Amende communale (GAS) pour dépôt anticipé ou non conforme ; les dépôts clandestins coûtent beaucoup plus cher.",
  },
  {
    id: "voie-publique",
    emoji: "🚷",
    t: "Uriner ou cracher sur la voie publique",
    points: [
      "Uriner, déféquer ou cracher en rue, devant tout le monde, est une incivilité interdite partout en Belgique.",
      "C'est sanctionné par le règlement de police de la commune (sanctions administratives communales — GAS), au même titre que jeter un déchet.",
      "En cas de besoin, cherchez des toilettes publiques, un café ou un commerce : beaucoup de communes ont une carte des toilettes accessibles.",
    ],
    amende: "Amende communale (GAS) souvent de l'ordre de plusieurs dizaines à quelques centaines d'euros selon la commune.",
  },
  {
    id: "parties-communes",
    emoji: "🏢",
    t: "Respecter les parties communes (immeuble)",
    points: [
      "Cage d'escalier, hall, local poubelles, jardin : ce sont des espaces partagés. On n'y laisse pas ses affaires ni ses déchets.",
      "Le règlement de copropriété ou d'ordre intérieur précise les règles (horaires de calme, animaux, vélos…).",
      "En cas de conflit, le syndic, la médiation de quartier ou la commune peuvent aider avant d'en arriver à la police.",
    ],
  },
];

const readText = `Vivre en communauté, en Belgique : le respect des voisins. ${sujets
  .map((s) => s.t + ". " + s.points.join(" "))
  .join(" ")} La règle d'or : le dialogue d'abord. La plupart des conflits de voisinage se règlent en parlant, avant la police ou les amendes.`;

export default function VivreEnCommunautePage() {
  const [open, setOpen] = useState<string | null>(sujets[0].id);

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La loi avec moi</span>
          </Link>
          <Link href="/loi-avec-moi" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Tous les sujets →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-indigo-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(99,102,241,0.26),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Vivre en communauté
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Bien vivre avec ses voisins</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Musique trop forte, poubelles sorties au mauvais moment, parties communes… Voici les règles simples
            du « vivre ensemble » en Belgique — et comment <strong className="text-white">éviter les conflits</strong>.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Sujets cliquables */}
      <section className="py-14 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight text-center">Les situations du quotidien</h2>
        <p className="text-slate-500 mt-3 text-center">Touchez un sujet pour les détails.</p>

        <div className="mt-8 space-y-3">
          {sujets.map((s) => {
            const isOpen = open === s.id;
            return (
              <div key={s.id} className={`rounded-2xl border transition-all ${isOpen ? "border-indigo-300 shadow-md" : "border-slate-200"}`}>
                <button
                  type="button"
                  onClick={() => setOpen(isOpen ? null : s.id)}
                  aria-expanded={isOpen}
                  className="w-full text-left p-5 flex items-center gap-4"
                >
                  <span className="text-3xl flex-shrink-0" aria-hidden>{s.emoji}</span>
                  <span className="flex-1 font-bold tracking-tight">{s.t}</span>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className={`w-5 h-5 text-slate-400 flex-shrink-0 transition-transform ${isOpen ? "rotate-180" : ""}`}><path d="M6 9l6 6 6-6" strokeLinecap="round" strokeLinejoin="round" /></svg>
                </button>
                {isOpen && (
                  <div className="px-5 pb-5 -mt-1 pl-[4.25rem]">
                    <ul className="space-y-2.5">
                      {s.points.map((p, i) => (
                        <li key={i} className="flex items-start gap-2.5 text-sm text-slate-700 leading-relaxed">
                          <span className="flex-shrink-0 w-5 h-5 rounded-full bg-indigo-100 text-indigo-700 text-xs font-bold flex items-center justify-center mt-0.5">{i + 1}</span>
                          {p}
                        </li>
                      ))}
                    </ul>
                    {s.amende && (
                      <p className="mt-4 text-xs font-medium text-rose-700 bg-rose-50 border border-rose-200 rounded-lg px-3 py-2">
                        ⚖️ {s.amende}
                      </p>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </section>

      {/* La règle d'or : dialogue */}
      <section className="pb-8 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border-2 border-emerald-200 bg-emerald-50 p-6">
          <h2 className="text-xl font-bold tracking-tight text-emerald-900">🤝 La règle d&apos;or : parler d&apos;abord</h2>
          <p className="text-emerald-900/80 text-sm mt-2 leading-relaxed">
            La plupart des conflits de voisinage se règlent <strong>en discutant calmement</strong>, sans police ni
            amende. Si le dialogue échoue, beaucoup de communes proposent une <strong>médiation de quartier</strong>
            gratuite. La police et la plainte ne viennent qu&apos;en dernier recours.
          </p>
        </div>
      </section>

      {/* Sources + disclaimer */}
      <section className="pb-12 px-6 max-w-3xl mx-auto">
        <div className="flex flex-col gap-2.5">
          <a href="https://www.police.be/5269/questions/declaration/je-veux-signaler-un-tapage-nocturnediurne" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
            🔗 Police.be — signaler un tapage (officiel)
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
          </a>
          <a href="https://environnement.brussels/citoyen/reglementation/obligations-et-autorisations/bruit-de-voisinage-quelle-legislation" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
            🔗 Bruxelles Environnement — bruit de voisinage (officiel)
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
          </a>
        </div>
        <div className="mt-6 rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ Le bruit et la propreté sont largement réglés au niveau <strong>communal</strong> (sanctions
            administratives, horaires de collecte, règlement de police). Les montants et horaires exacts figurent dans
            le règlement de votre commune. Informations générales vérifiées auprès de sources officielles belges.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à « La loi avec moi »</Link>
      </footer>
    </main>
  );
}
