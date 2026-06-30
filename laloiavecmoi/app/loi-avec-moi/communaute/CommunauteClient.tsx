"use client";

import { useState } from "react";
import Link from "next/link";

type QPub = {
  id: string;
  question: string;
  domaine: string;
  module: string;
  reponse_resume: string;
  lien_module: string;
  fait_id: string;
};

function normaliser(s: string) {
  return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
}

export default function CommunauteClient({ questions }: { questions: QPub[] }) {
  const [query, setQuery] = useState("");
  const [domaine, setDomaine] = useState("");
  const q = normaliser(query.trim());

  // Domaines présents, triés par fréquence (les plus fournis d'abord).
  const domaines = (() => {
    const compte = new Map<string, number>();
    for (const item of questions) compte.set(item.domaine, (compte.get(item.domaine) || 0) + 1);
    return [...compte.entries()].sort((a, b) => b[1] - a[1]);
  })();

  const base = domaine ? questions.filter((x) => x.domaine === domaine) : questions;
  const resultats = q
    ? base.filter((x) => normaliser(x.question).includes(q) || normaliser(x.reponse_resume).includes(q))
    : base;

  const MAX = 80;
  const affichage = resultats.slice(0, MAX);

  return (
    <div className="max-w-5xl mx-auto px-6 py-8">
      <div className="sticky top-0 z-10 bg-white/95 backdrop-blur py-4 -mx-6 px-6 border-b border-slate-100">
        <label htmlFor="rech-comm" className="sr-only">
          Rechercher une question
        </label>
        <input
          id="rech-comm"
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Rechercher : « bail », « licenciement », « garantie », « succession »…"
          className="w-full rounded-xl border border-slate-300 px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <div className="mt-3 flex flex-wrap gap-2">
          <button
            onClick={() => setDomaine("")}
            className={`px-3 py-1.5 rounded-full text-sm border ${
              domaine === "" ? "bg-indigo-600 text-white border-indigo-600" : "border-slate-300 text-slate-600 hover:bg-slate-100"
            }`}
          >
            Tous
          </button>
          {domaines.slice(0, 10).map(([nom, n]) => (
            <button
              key={nom}
              onClick={() => setDomaine(nom)}
              className={`px-3 py-1.5 rounded-full text-sm border ${
                domaine === nom ? "bg-indigo-600 text-white border-indigo-600" : "border-slate-300 text-slate-600 hover:bg-slate-100"
              }`}
            >
              {nom} <span className="opacity-60">({n})</span>
            </button>
          ))}
        </div>
      </div>

      <p className="mt-5 text-sm text-slate-500">
        {resultats.length} question{resultats.length > 1 ? "s" : ""}
        {affichage.length < resultats.length ? ` (les ${MAX} premières affichées — affinez votre recherche)` : ""}
      </p>

      <ul className="mt-4 space-y-3">
        {affichage.map((r) => (
          <li key={r.id}>
            <Link
              href={`/loi/${r.lien_module}#${r.fait_id}`}
              className="block rounded-2xl border border-slate-200 p-4 hover:border-indigo-300 hover:bg-indigo-50/40 transition"
            >
              <div className="flex items-center gap-2">
                <span className="text-[11px] font-medium text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full">
                  {r.domaine}
                </span>
              </div>
              <p className="mt-2 font-semibold text-slate-900">{r.question}</p>
              {r.reponse_resume && <p className="mt-1 text-sm text-slate-600">{r.reponse_resume}</p>}
              <span className="mt-2 inline-block text-sm text-indigo-700 font-medium">Lire la réponse complète →</span>
            </Link>
          </li>
        ))}
      </ul>

      {affichage.length === 0 && (
        <p className="mt-10 text-center text-slate-500">
          Aucune question ne correspond. Essayez un autre mot-clé, ou consultez la{" "}
          <Link href="/base-juridique" className="text-indigo-700 font-medium">
            base juridique complète
          </Link>
          .
        </p>
      )}
    </div>
  );
}
