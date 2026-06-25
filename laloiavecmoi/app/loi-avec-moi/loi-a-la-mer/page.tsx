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
    emoji: "🏊",
    t: "Se baigner",
    statut: "depend",
    d: "Uniquement dans les zones surveillées, entre les bouées jaunes, et seulement quand le drapeau le permet. La baignade est interdite dans toutes les zones non surveillées, même par beau temps.",
  },
  {
    emoji: "🐕",
    t: "Venir avec son chien",
    statut: "depend",
    d: "Ça dépend de la commune et de la saison. En haute saison (souvent d'avril/Pâques à fin septembre), les chiens sont interdits sur la plage une grande partie de la journée. Vérifiez le règlement de la commune où vous allez.",
  },
  {
    emoji: "🔥",
    t: "Faire un barbecue ou un feu",
    statut: "non",
    d: "Interdit sur la plage et dans les dunes. Risque d'incendie et de pollution. Quelques zones spéciales peuvent exister : renseignez-vous auprès de la commune.",
  },
  {
    emoji: "⛺",
    t: "Camper ou dormir sur la plage",
    statut: "non",
    d: "Interdit dans la quasi-totalité des communes côtières : on ne campe pas et on ne passe pas la nuit sur la plage ou dans les dunes.",
  },
  {
    emoji: "⛱️",
    t: "Planter une tente / un parasol en journée",
    statut: "depend",
    d: "Une petite tente de plage ou un parasol pour s'abriter du soleil est généralement toléré en journée sur les plages flamandes. Mais on remballe le soir : pas de campement.",
  },
  {
    emoji: "👙",
    t: "Bronzer seins nus (topless)",
    statut: "depend",
    d: "Toléré de façon « statique » (allongée sur sa serviette). Se promener ou se baigner seins nus n'est en revanche pas autorisé. Le naturisme complet n'est permis qu'à la plage de Bredene.",
  },
  {
    emoji: "🏖️",
    t: "Respecter la plage (déchets, dunes)",
    statut: "oui",
    d: "On remporte ses déchets, on ne piétine pas les dunes protégées (elles protègent la côte et abritent une nature fragile). Les petites infractions peuvent donner lieu à une amende communale (GAS).",
  },
];

const statutStyle: Record<Regle["statut"], { label: string; cls: string; dot: string }> = {
  oui: { label: "Autorisé / recommandé", cls: "text-emerald-700 bg-emerald-50 border-emerald-200", dot: "bg-emerald-500" },
  non: { label: "Interdit", cls: "text-rose-700 bg-rose-50 border-rose-200", dot: "bg-rose-500" },
  depend: { label: "Ça dépend", cls: "text-amber-700 bg-amber-50 border-amber-200", dot: "bg-amber-500" },
};

const drapeaux = [
  { c: "bg-emerald-500", t: "Drapeau vert", d: "Baignade et nage autorisées dans la zone surveillée." },
  { c: "bg-amber-400", t: "Drapeau jaune", d: "Baignade dangereuse. Objets gonflables (matelas, bouées) interdits." },
  { c: "bg-rose-600", t: "Drapeau rouge", d: "Baignade et nage interdites : danger." },
];

const readText = `La loi à la mer, sur la côte belge. Ce que vous pouvez faire et ne pas faire. ${regles
  .map((r) => r.t + " : " + statutStyle[r.statut].label + ". " + r.d)
  .join(" ")} Les drapeaux de baignade : vert, la baignade est autorisée. Jaune, la baignade est dangereuse et les objets gonflables sont interdits. Rouge, la baignade est interdite. Les sauveteurs surveillent les plages en été, en général de 10h30 à 18h30. Baignez-vous toujours entre les bouées jaunes, dans une zone surveillée.`;

export default function LoiALaMerPage() {
  const [open, setOpen] = useState<string | null>(null);

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

      <section className="relative overflow-hidden bg-gradient-to-b from-sky-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(14,165,233,0.28),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            La loi à la mer
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">À la plage : ce que je peux faire (et pas)</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            La côte belge a ses règles, pour la sécurité de tous et pour protéger la nature. Voici l&apos;essentiel,
            simplement — pour profiter de la mer <strong className="text-white">sans mauvaise surprise</strong>.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Règles cliquables */}
      <section className="py-14 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight text-center">Les règles, en un coup d&apos;œil</h2>
        <p className="text-slate-500 mt-3 text-center">Touchez une règle pour les détails.</p>

        <div className="mt-8 space-y-3">
          {regles.map((r) => {
            const st = statutStyle[r.statut];
            const isOpen = open === r.t;
            return (
              <div key={r.t} className={`rounded-2xl border transition-all ${isOpen ? "border-sky-300 shadow-md" : "border-slate-200"}`}>
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

      {/* Drapeaux de baignade */}
      <section className="py-12 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">Les drapeaux de baignade</h2>
          <p className="text-slate-600 mt-2 text-sm leading-relaxed">
            Avant de vous baigner, regardez toujours le drapeau hissé par les sauveteurs. C&apos;est lui qui décide,
            pas la météo qui a l&apos;air belle.
          </p>
          <div className="mt-6 grid sm:grid-cols-3 gap-4">
            {drapeaux.map((d) => (
              <div key={d.t} className="bg-white rounded-2xl border border-slate-200 p-5">
                <div className={`w-12 h-8 rounded ${d.c} mb-3`} aria-hidden />
                <h3 className="font-bold tracking-tight">{d.t}</h3>
                <p className="text-slate-600 text-sm mt-1.5 leading-relaxed">{d.d}</p>
              </div>
            ))}
          </div>
          <div className="mt-6 rounded-2xl border border-sky-200 bg-sky-50 p-5">
            <p className="text-sky-900 text-sm leading-relaxed">
              🛟 Baignez-vous <strong>uniquement entre les bouées jaunes</strong>, dans une zone surveillée. Les
              sauveteurs sont en général présents l&apos;été de <strong>10h30 à 18h30</strong>. En dehors des zones
              surveillées, la baignade est interdite — même quand la mer paraît calme (courants, eau froide).
            </p>
          </div>
        </div>
      </section>

      {/* Sources officielles */}
      <section className="py-12 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">Vérifier la source officielle</h2>
        <p className="text-slate-600 mt-2 text-sm leading-relaxed">
          Chaque commune côtière (Knokke, Ostende, La Panne, Bredene…) fixe son propre règlement de police pour la
          plage : chiens, horaires, zones. En cas de doute, la source la plus fiable reste le site de la commune et
          celui des sauveteurs.
        </p>
        <div className="mt-5 flex flex-col gap-2.5">
          <a href="https://fr.ikwv.be/signalisatie" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
            🔗 IKWV — signalisation et drapeaux des plages (officiel)
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
          </a>
          <a href="https://www.dewestkust.be/fr" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
            🔗 La côte belge — infos tourisme & communes (officiel)
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
          </a>
        </div>
      </section>

      {/* Disclaimer + lien danger */}
      <section className="pb-12 px-6 max-w-3xl mx-auto space-y-5">
        <div className="rounded-2xl border border-rose-200 bg-rose-50 p-5">
          <h3 className="font-semibold text-rose-900">🆘 Un danger en mer ?</h3>
          <p className="text-rose-800 text-sm mt-2 leading-relaxed">
            Quelqu&apos;un se noie ou est en difficulté ? Prévenez immédiatement un sauveteur, ou appelez le
            <strong> 112</strong>. N&apos;allez pas seul·e dans des courants forts.
          </p>
          <a href="tel:112" className="inline-flex items-center gap-2 mt-3 bg-rose-600 hover:bg-rose-700 text-white text-sm font-semibold rounded-lg px-4 py-2 transition-colors">
            📞 Urgence — 112
          </a>
        </div>
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ Les règles précises (surtout pour les chiens et les horaires) <strong>varient d&apos;une commune à
            l&apos;autre</strong> et peuvent changer chaque saison. Ces informations générales sont vérifiées auprès
            de sources belges ; pour votre plage, confirmez toujours sur le site de la commune avant de partir.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à « La loi avec moi »</Link>
      </footer>
    </main>
  );
}
