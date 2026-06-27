"use client";

import Link from "next/link";
import { useState } from "react";
import ReadAloud from "@/components/ReadAloud";

type Regle = {
  emoji: string;
  t: string;
  statut: "oui" | "non" | "depend";
  d: string;
};

const regles: Regle[] = [
  {
    emoji: "🚶",
    t: "Me promener en forêt",
    statut: "depend",
    d: "Oui, mais en Wallonie vous devez rester sur les routes, chemins, sentiers et aires balisés et ouverts au public. Hors de ces voies, l'accès à pied est interdit (sauf motif légitime). Une barrière, un panneau ou une perche = voie fermée.",
  },
  {
    emoji: "⛺",
    t: "Bivouaquer (une nuit, tente légère)",
    statut: "depend",
    d: "Le bivouac est autorisé surtout dans les aires de bivouac prévues à cet effet (réseau officiel wallon). La règle d'or : monter la tente le soir (souvent après 17h–18h), la démonter tôt le matin (avant 9h–10h), une seule nuit, et ne laisser AUCUNE trace.",
  },
  {
    emoji: "🏕️",
    t: "Faire du camping sauvage (plusieurs jours)",
    statut: "non",
    d: "Interdit partout : s'installer plusieurs jours au même endroit avec un gros équipement n'est pas du bivouac. C'est une infraction au Code forestier.",
  },
  {
    emoji: "🔥",
    t: "Faire un feu",
    statut: "non",
    d: "Interdit en dehors des zones expressément prévues. En période de sécheresse ou de canicule, le feu est totalement interdit, sous toutes ses formes. Pas de barbecue, pas de réchaud à flamme nue en zone à risque.",
  },
  {
    emoji: "🦌",
    t: "Respecter le calme et la faune",
    statut: "oui",
    d: "On ne dérange pas les animaux sauvages, on ne coupe pas de branches, on tient son chien sous contrôle. La forêt est un milieu vivant et fragile : la quiétude est protégée par la loi.",
  },
  {
    emoji: "🗑️",
    t: "Remporter tous ses déchets",
    statut: "oui",
    d: "On ne laisse rien : pas de déchets, pas de feu, pas de trace. « Ne laisser aucune trace » est la règle de base du bivouac et du respect de la forêt.",
  },
];

const statutStyle: Record<Regle["statut"], { label: string; cls: string; dot: string }> = {
  oui: { label: "Autorisé / recommandé", cls: "text-emerald-700 bg-emerald-50 border-emerald-200", dot: "bg-emerald-500" },
  non: { label: "Interdit", cls: "text-rose-700 bg-rose-50 border-rose-200", dot: "bg-rose-500" },
  depend: { label: "Sous conditions", cls: "text-amber-700 bg-amber-50 border-amber-200", dot: "bg-amber-500" },
};

const readText = `La loi en forêt, en Belgique. Ce que vous pouvez faire et ne pas faire. ${regles
  .map((r) => r.t + " : " + statutStyle[r.statut].label + ". " + r.d)
  .join(" ")} Le bivouac d'une nuit est toléré surtout dans les aires prévues à cet effet. Le camping sauvage de plusieurs jours est interdit partout. En cas d'infraction, l'administration peut proposer une transaction allant de cinquante à cent cinquante euros. Attention : les règles varient entre la Wallonie et la Flandre.`;

export default function LoiEnForetPage() {
  const [open, setOpen] = useState<string | null>(null);

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La Loi Avec Moi</span>
          </Link>
          <Link href="/loi-avec-moi" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Tous les sujets →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(16,185,129,0.26),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            La loi en forêt
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">En forêt : où dormir, ce que je risque</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Bivouac, camping sauvage, feu, promenade : la forêt belge a ses règles pour protéger la nature.
            Voici ce qui est <strong className="text-white">permis, toléré ou interdit</strong> — et les risques.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Règles cliquables */}
      <section className="py-14 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight text-center">Bivouac, feu, camping : les règles</h2>
        <p className="text-slate-500 mt-3 text-center">Touchez une règle pour les détails.</p>

        <div className="mt-8 space-y-3">
          {regles.map((r) => {
            const st = statutStyle[r.statut];
            const isOpen = open === r.t;
            return (
              <div key={r.t} className={`rounded-2xl border transition-all ${isOpen ? "border-emerald-300 shadow-md" : "border-slate-200"}`}>
                <button
                  type="button"
                  onClick={() => setOpen(isOpen ? null : r.t)}
                  aria-expanded={isOpen}
                  className="w-full text-left p-5 flex items-center gap-4"
                >
                  <span className="text-3xl flex-shrink-0" aria-hidden>{r.emoji}</span>
                  <span className="flex-1 font-bold tracking-tight">{r.t}</span>
                  <span className={`flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full border ${st.cls}`}>
                    <span className={`w-2 h-2 rounded-full ${st.dot}`} />
                    {st.label}
                  </span>
                </button>
                {isOpen && (
                  <p className="px-5 pb-5 -mt-1 text-sm text-slate-700 leading-relaxed pl-[4.25rem]">{r.d}</p>
                )}
              </div>
            );
          })}
        </div>
      </section>

      {/* Aires de bivouac officielles */}
      <section className="py-12 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">Où bivouaquer légalement ?</h2>
          <p className="text-slate-600 mt-2 text-sm leading-relaxed">
            La Wallonie a aménagé un <strong>réseau officiel d&apos;aires de bivouac</strong> (souvent gratuites, mais
            beaucoup demandent une réservation). C&apos;est la façon sûre et légale de dormir en pleine nature, sans
            risquer d&apos;amende et sans abîmer la forêt.
          </p>
          <div className="mt-5 flex flex-col gap-2.5">
            <a href="https://www.bivouacchezmoi.be/" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 Réseau des aires de bivouac en Wallonie
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
            <a href="https://environnement.wallonie.be/home/loisirs/circulation-en-foret.html" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 Wallonie — circuler en forêt & Code forestier (officiel)
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
          </div>
        </div>
      </section>

      {/* Ce que je risque */}
      <section className="py-12 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border-2 border-rose-200 bg-rose-50 p-6">
          <h2 className="text-xl font-bold tracking-tight text-rose-900">⚖️ Ce que je risque</h2>
          <p className="text-rose-800 text-sm mt-2 leading-relaxed">
            Camper hors des zones autorisées, faire un feu interdit ou laisser des déchets sont des infractions au
            Code forestier. L&apos;administration (SPW) peut dresser un constat et proposer une <strong>transaction
            de l&apos;ordre de 50 à 150 €</strong>. En cas de feu pendant une sécheresse, les conséquences (incendie,
            poursuites) peuvent être bien plus lourdes.
          </p>
        </div>
      </section>

      {/* Disclaimer */}
      <section className="pb-12 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ La forêt est <strong>régionalisée</strong> : les règles diffèrent entre la Wallonie et la Flandre, et
            certaines forêts (réserves naturelles, propriétés privées) ont des règles plus strictes. Ces informations
            générales sont tirées de sources officielles wallonnes ; vérifiez toujours la signalisation sur place et
            le règlement de la forêt concernée.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à « La Loi Avec Moi »</Link>
      </footer>
    </main>
  );
}
