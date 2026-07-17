"use client";

import Link from "next/link";
import { useState } from "react";
import ReadAloud from "@/components/ReadAloud";

type Cas = {
  id: string;
  emoji: string;
  t: string;
  quoi: string[];
  liens: { label: string; url: string }[];
};

const cas: Cas[] = [
  {
    id: "chien-chat",
    emoji: "🐕",
    t: "J'ai trouvé un chien ou un chat errant",
    quoi: [
      "Mettez l'animal en sécurité, sans vous mettre en danger (un animal apeuré peut mordre).",
      "Un vétérinaire ou un refuge peut lire la puce électronique pour retrouver le propriétaire — c'est souvent gratuit.",
      "En Wallonie : vous devez confier l'animal à l'administration communale dans les 4 jours si le propriétaire reste introuvable.",
      "À Bruxelles : prévenez la police locale (101), elle se déplace pour récupérer l'animal.",
    ],
    liens: [
      { label: "Wallonie — animaux errants (officiel)", url: "https://bienetreanimal.wallonie.be/home/animaux/autres-animaux/animaux-errants.html" },
      { label: "Bruxelles Environnement — bien-être animal", url: "https://environnement.brussels/" },
    ],
  },
  {
    id: "sauvage",
    emoji: "🦔",
    t: "J'ai trouvé un animal sauvage blessé",
    quoi: [
      "Hérisson, oiseau, renard, chevreuil… : ne le gardez pas chez vous, c'est interdit et risqué pour lui.",
      "Contactez un centre de revalidation de la faune sauvage (CREAVES en Wallonie) ou le service Nature.",
      "Manipulez le moins possible ; suivez les consignes données par téléphone.",
    ],
    liens: [
      { label: "Wallonie — faune sauvage / CREAVES (officiel)", url: "https://biodiversite.wallonie.be/fr/creaves.html?IDC=5859" },
    ],
  },
  {
    id: "maltraitance",
    emoji: "💔",
    t: "Je vois un animal maltraité ou abandonné",
    quoi: [
      "La maltraitance et l'abandon sont des INFRACTIONS punies par la loi en Belgique.",
      "Signalez-le au service Bien-être animal de votre Région (Wallonie, Bruxelles ou Flandre).",
      "En cas d'urgence ou de danger immédiat, appelez la police (101).",
      "Notez date, lieu, photos si possible : ça aide l'enquête.",
    ],
    liens: [
      { label: "Wallonie — Bien-être animal (signalement)", url: "https://bienetreanimal.wallonie.be/" },
      { label: "Flandre — Dierenwelzijn (officiel)", url: "https://www.vlaanderen.be/dierenwelzijn" },
    ],
  },
  {
    id: "perdu",
    emoji: "🐾",
    t: "J'ai perdu mon animal",
    quoi: [
      "Signalez la perte rapidement : plus c'est tôt, plus les chances de le retrouver sont grandes.",
      "Contactez les refuges, vétérinaires et la commune autour de vous.",
      "Vérifiez que les données de sa puce électronique (DogID / CatID) sont à jour.",
    ],
    liens: [
      { label: "Wallonie — signaler / retrouver un animal perdu", url: "https://www.wallonie.be/fr/demarches/signaler-ou-retrouver-un-animal-perdu" },
    ],
  },
  {
    id: "vacances",
    emoji: "✈️",
    t: "Je pars en vacances : que faire de mon animal ?",
    quoi: [
      "On n'abandonne jamais un animal : c'est une infraction, et il en souffre. Anticipez avant de partir.",
      "Solutions : pension pour animaux, garde par un proche, ou « pet-sitter » de confiance.",
      "Si vous l'emmenez : passeport européen pour animal, puce et vaccins à jour (surtout la rage).",
    ],
    liens: [
      { label: "Belgium.be — voyager avec son animal", url: "https://www.belgium.be/fr/sante/en_voyage" },
    ],
  },
];

const readText = `Les animaux ont des droits. En Belgique, l'abandon et la maltraitance sont interdits et punis par la loi. ${cas
  .map((c) => c.t + ". " + c.quoi.join(" "))
  .join(" ")} Le bien-être animal dépend de votre Région : la Wallonie, Bruxelles et la Flandre ont chacune leur service.`;

export default function AnimauxPage() {
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

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(16,185,129,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Les animaux aussi ont des droits
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Protéger les animaux</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            En Belgique, l&apos;abandon et la maltraitance sont <strong className="text-white">interdits par la loi</strong>.
            Choisissez votre situation : on vous dit quoi faire et qui contacter.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Pictogrammes cliquables */}
      <section className="py-14 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight text-center">Quelle est votre situation ?</h2>
        <p className="text-slate-500 mt-3 text-center">Touchez la situation qui vous concerne.</p>

        <div className="grid sm:grid-cols-2 gap-4 mt-8">
          {cas.map((c) => (
            <button
              key={c.id}
              type="button"
              onClick={() => setOpen(open === c.id ? null : c.id)}
              aria-expanded={open === c.id}
              className={`text-left rounded-2xl border-2 p-5 transition-all ${
                open === c.id ? "border-emerald-400 bg-emerald-50" : "border-slate-200 hover:border-emerald-300 hover:shadow-md"
              }`}
            >
              <div className="flex items-center gap-3">
                <span className="text-3xl flex-shrink-0" aria-hidden>{c.emoji}</span>
                <span className="font-bold tracking-tight">{c.t}</span>
              </div>
            </button>
          ))}
        </div>

        {/* Détail de la situation ouverte */}
        {cas
          .filter((c) => c.id === open)
          .map((c) => (
            <div key={c.id} className="mt-6 rounded-2xl border border-emerald-200 bg-white p-6 shadow-sm">
              <div className="flex items-center gap-3">
                <span className="text-3xl" aria-hidden>{c.emoji}</span>
                <h3 className="text-xl font-bold tracking-tight">{c.t}</h3>
              </div>
              <ul className="mt-4 space-y-2.5">
                {c.quoi.map((q, i) => (
                  <li key={i} className="flex items-start gap-2.5 text-sm text-slate-700 leading-relaxed">
                    <span className="flex-shrink-0 w-5 h-5 rounded-full bg-emerald-100 text-emerald-700 text-xs font-bold flex items-center justify-center mt-0.5">{i + 1}</span>
                    {q}
                  </li>
                ))}
              </ul>
              <div className="mt-5 flex flex-col gap-2">
                <a href="tel:101" className="inline-flex items-center gap-2 self-start bg-rose-600 hover:bg-rose-700 text-white text-sm font-semibold rounded-lg px-4 py-2 transition-colors">
                  📞 Urgence / danger : appeler la police 101
                </a>
                {c.liens.map((l) => (
                  <a key={l.url} href={l.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 self-start text-xs font-medium text-indigo-700 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded-lg px-3 py-2 transition-colors">
                    🔗 {l.label}
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
                  </a>
                ))}
              </div>
            </div>
          ))}
      </section>

      {/* Horaires honnête + disclaimer */}
      <section className="pb-12 px-6 max-w-3xl mx-auto space-y-5">
        <div className="rounded-2xl bg-indigo-50 border border-indigo-100 p-5">
          <h3 className="font-semibold text-indigo-900">🕐 À propos des horaires</h3>
          <p className="text-indigo-900/80 text-sm mt-2 leading-relaxed">
            La police (101) et l&apos;urgence (112) répondent 24h/24. Les refuges, communes et services
            Bien-être animal ont des horaires variables : ils sont indiqués sur les pages officielles
            ci-dessus, toujours à jour.
          </p>
        </div>
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ Le bien-être animal est <strong>régionalisé</strong> en Belgique : Wallonie, Bruxelles et Flandre
            ont chacune leur réglementation et leur service. Informations générales tirées des sources officielles.
            Pour un cas précis, suivez les consignes du service compétent de votre Région.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à « La Loi Avec Moi »</Link>
      </footer>
    </main>
  );
}
