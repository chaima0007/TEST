"use client";

import { useState } from "react";
import Link from "next/link";

// Composant client : recherche plein texte + filtre par domaine sur les réponses sourcées.
// Reçoit les modules chargés côté serveur (data/belgium) et n'affiche que ce qui correspond.

type Source = { type?: string; url?: string; intitule?: string };
type Contact = { nom?: string; numero?: string; lien?: string; pour?: string; dispo?: string };
type Fait = {
  id: string;
  question: string;
  reponse: string;
  reference_legale?: string;
  alerte_delai?: string;
  contacts?: Contact[];
  sources?: Source[];
  date_verification?: string;
};
type Module = { module: string; titre: string; domaine?: string; faits: Fait[] };

function normaliser(s: string) {
  return s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, ""); // enlève les accents pour une recherche tolérante
}

export default function BaseJuridiqueClient({ modules }: { modules: Module[] }) {
  const [query, setQuery] = useState("");
  const [domaineActif, setDomaineActif] = useState<string>("");

  const q = normaliser(query.trim());

  const modulesFiltres = modules
    .filter((m) => !domaineActif || m.module === domaineActif)
    .map((m) => {
      if (!q) return m;
      const faits = m.faits.filter((f) => {
        const blob = normaliser(
          [f.question, f.reponse, f.reference_legale, ...(f.contacts || []).map((c) => c.nom || "")]
            .filter(Boolean)
            .join(" ")
        );
        return blob.includes(q);
      });
      return { ...m, faits };
    })
    .filter((m) => m.faits.length > 0);

  const totalAffiche = modulesFiltres.reduce((n, m) => n + m.faits.length, 0);

  return (
    <div className="max-w-5xl mx-auto px-6 py-10">
      {/* Barre de recherche */}
      <div className="sticky top-0 z-10 bg-white/95 backdrop-blur py-4 -mx-6 px-6 border-b border-slate-100">
        <label htmlFor="recherche" className="sr-only">
          Rechercher une réponse
        </label>
        <input
          id="recherche"
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Rechercher : « bail », « licenciement », « amende », « garde »…"
          className="w-full rounded-xl border border-slate-300 px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <p className="mt-2 text-sm text-slate-500" aria-live="polite">
          {totalAffiche} réponse{totalAffiche > 1 ? "s" : ""}
          {query ? ` pour « ${query} »` : ""}
          {domaineActif ? " dans ce domaine" : ""}.
        </p>
      </div>

      {/* Filtres par domaine */}
      <nav aria-label="Domaines" className="flex flex-wrap gap-2 my-6">
        <button
          type="button"
          onClick={() => setDomaineActif("")}
          className={
            "text-sm px-3 py-1.5 rounded-full border transition-colors " +
            (!domaineActif
              ? "bg-indigo-600 border-indigo-600 text-white"
              : "border-slate-200 hover:border-indigo-400 hover:text-indigo-700")
          }
        >
          Tous
        </button>
        {modules.map((m) => (
          <button
            key={m.module}
            type="button"
            onClick={() => setDomaineActif(m.module === domaineActif ? "" : m.module)}
            className={
              "text-sm px-3 py-1.5 rounded-full border transition-colors " +
              (domaineActif === m.module
                ? "bg-indigo-600 border-indigo-600 text-white"
                : "border-slate-200 hover:border-indigo-400 hover:text-indigo-700")
            }
          >
            {m.titre}
          </button>
        ))}
      </nav>

      {totalAffiche === 0 && (
        <p className="text-slate-600 py-10 text-center">
          Aucune réponse ne correspond. Essayez un autre mot (ex. « loyer », « congé », « dette »).
        </p>
      )}

      {modulesFiltres.map((m) => (
        <section key={m.module} id={m.module} className="mb-12 scroll-mt-24">
          <h2 className="text-2xl font-bold text-blue-900 border-b-2 border-slate-100 pb-2">
            <Link href={`/loi/${m.module}`} className="hover:underline">
              {m.titre}
            </Link>
          </h2>
          <div className="mt-6 grid gap-5">
            {m.faits.map((f) => (
              <article key={f.id} className="rounded-2xl border border-slate-200 p-5 bg-white">
                <h3 className="font-semibold text-lg text-slate-900">{f.question}</h3>
                <p className="mt-2 text-slate-700 leading-relaxed">{f.reponse}</p>

                {f.alerte_delai && (
                  <p className="mt-3 text-sm rounded-lg bg-red-50 border border-red-200 text-red-800 px-3 py-2">
                    ⏱ <strong>À ne pas tarder.</strong> {f.alerte_delai}
                  </p>
                )}

                {f.contacts && f.contacts.length > 0 && (
                  <div className="mt-3 text-sm rounded-lg bg-blue-50 border border-blue-200 px-3 py-2">
                    <strong>📞 Qui contacter :</strong>
                    <ul className="mt-1 list-disc list-inside text-slate-700">
                      {f.contacts.map((c, i) => (
                        <li key={i}>
                          {c.nom}
                          {c.numero ? ` — ${c.numero}` : ""}
                          {c.pour ? ` (${c.pour})` : ""}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {f.reference_legale && <p className="mt-3 text-sm text-slate-500">⚖️ {f.reference_legale}</p>}

                {f.sources && f.sources.length > 0 && (
                  <div className="mt-2 text-sm">
                    <span className="font-semibold text-slate-600">Sources : </span>
                    {f.sources.map((s, i) => (
                      <span key={i}>
                        {i > 0 ? " · " : ""}
                        <a
                          href={s.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-indigo-700 hover:underline"
                        >
                          {s.intitule}
                        </a>
                        {s.type === "officiel" ? (
                          <span className="text-emerald-700 font-medium"> [officiel]</span>
                        ) : (
                          <span className="text-slate-400"> [complément]</span>
                        )}
                      </span>
                    ))}
                  </div>
                )}

                {f.date_verification && (
                  <p className="mt-2 text-xs text-slate-400">Vérifié le {f.date_verification}</p>
                )}
              </article>
            ))}
          </div>
        </section>
      ))}

      <p className="text-xs text-slate-400 mt-10 border-t border-slate-100 pt-4">
        Information juridique générale, à jour à la date indiquée. Ne remplace pas un conseil juridique
        individualisé. Chaque réponse cite ses sources officielles. © La Loi Avec Moi.
      </p>
    </div>
  );
}
