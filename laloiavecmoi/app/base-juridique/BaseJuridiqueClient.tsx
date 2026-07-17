"use client";

import { useState } from "react";
import Link from "next/link";

// Index léger + recherche. Par défaut : grille des domaines (léger).
// Quand on tape une recherche : liste des questions correspondantes → lien vers /loi/[domaine]#id.

type FaitLeger = { id: string; question: string };
type ModuleLeger = { module: string; titre: string; theme: string; faits: FaitLeger[] };

function normaliser(s: string) {
  return s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "");
}

export default function BaseJuridiqueClient({ index }: { index: ModuleLeger[] }) {
  const [query, setQuery] = useState("");
  const [theme, setTheme] = useState<string>("");
  const q = normaliser(query.trim());

  // Liste des thèmes présents, avec leur nombre de domaines (ordre stable par fréquence).
  const themes = (() => {
    const compte = new Map<string, number>();
    for (const m of index) compte.set(m.theme, (compte.get(m.theme) || 0) + 1);
    return [...compte.entries()].sort((a, b) => b[1] - a[1]);
  })();

  // Filtrage par thème (appliqué aux deux vues).
  const indexFiltre = theme ? index.filter((m) => m.theme === theme) : index;

  // Résultats de recherche (questions correspondantes) — plafonnés pour rester légers.
  const resultats: { module: string; titre: string; id: string; question: string }[] = [];
  if (q) {
    for (const m of indexFiltre) {
      for (const f of m.faits) {
        if (normaliser(f.question).includes(q)) {
          resultats.push({ module: m.module, titre: m.titre, id: f.id, question: f.question });
        }
      }
    }
  }
  const MAX = 60;
  const affichage = resultats.slice(0, MAX);

  return (
    <div className="max-w-5xl mx-auto px-6 py-10">
      <div className="sticky top-0 z-10 bg-white/95 backdrop-blur py-4 -mx-6 px-6 border-b border-slate-100">
        <label htmlFor="recherche" className="sr-only">
          Rechercher une question
        </label>
        <input
          id="recherche"
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Rechercher : « bail », « licenciement », « amende », « garde »…"
          className="w-full rounded-xl border border-slate-300 px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />

        {/* Filtre par thème (chips) */}
        <div className="mt-3 flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => setTheme("")}
            className={
              "px-3 py-1.5 rounded-full text-sm font-medium border transition-colors " +
              (theme === "" ? "bg-indigo-600 border-indigo-600 text-white" : "bg-white border-slate-300 text-slate-600 hover:border-indigo-400")
            }
          >
            Tous les thèmes
          </button>
          {themes.map(([nom, n]) => (
            <button
              key={nom}
              type="button"
              onClick={() => setTheme(nom === theme ? "" : nom)}
              className={
                "px-3 py-1.5 rounded-full text-sm font-medium border transition-colors " +
                (theme === nom ? "bg-indigo-600 border-indigo-600 text-white" : "bg-white border-slate-300 text-slate-600 hover:border-indigo-400")
              }
            >
              {nom} <span className={theme === nom ? "text-indigo-100" : "text-slate-400"}>({n})</span>
            </button>
          ))}
        </div>

        {q ? (
          <p className="mt-2 text-sm text-slate-500" aria-live="polite">
            {resultats.length} question{resultats.length > 1 ? "s" : ""} pour « {query} »
            {theme ? ` dans « ${theme} »` : ""}
            {resultats.length > MAX ? ` (les ${MAX} premières affichées)` : ""}.
          </p>
        ) : theme ? (
          <p className="mt-2 text-sm text-slate-500" aria-live="polite">
            {indexFiltre.length} domaine{indexFiltre.length > 1 ? "s" : ""} dans « {theme} ».
          </p>
        ) : null}
      </div>

      {/* Résultats de recherche */}
      {q ? (
        affichage.length > 0 ? (
          <ul className="mt-6 grid gap-3">
            {affichage.map((r) => (
              <li key={`${r.module}-${r.id}`}>
                <Link
                  href={`/loi/${r.module}#${r.id}`}
                  className="block rounded-xl border border-slate-200 p-4 hover:border-indigo-400 hover:shadow-sm transition-all"
                >
                  <span className="font-medium text-slate-900">{r.question}</span>
                  <span className="block text-xs text-slate-500 mt-1">{r.titre} →</span>
                </Link>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-slate-600 py-10 text-center">
            Aucune question ne correspond. Essayez un autre mot (ex. « loyer », « congé », « dette »).
          </p>
        )
      ) : (
        /* Vue par défaut : grille des domaines (légère), filtrée par thème si choisi */
        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {indexFiltre.map((m) => (
            <Link
              key={m.module}
              href={`/loi/${m.module}`}
              className="rounded-2xl border border-slate-200 p-5 hover:border-indigo-400 hover:shadow-sm transition-all"
            >
              <span className="text-xs font-medium text-indigo-600">{m.theme}</span>
              <h2 className="font-semibold text-slate-900 mt-1">{m.titre}</h2>
              <p className="text-sm text-slate-500 mt-1">
                {m.faits.length} réponse{m.faits.length > 1 ? "s" : ""} →
              </p>
            </Link>
          ))}
        </div>
      )}

      <p className="text-xs text-slate-400 mt-10 border-t border-slate-100 pt-4">
        Information juridique générale, à jour à la date indiquée. Ne remplace pas un conseil juridique
        individualisé. Chaque réponse cite ses sources officielles. © La Loi Avec Moi.
      </p>
    </div>
  );
}
