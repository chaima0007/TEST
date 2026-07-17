"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

type Actu = { id: string; titre: string; domaine?: string; detail?: string; date?: string; type: string; lien_fiche?: string };

const KEY = "llam_dossiers_suivis";

export default function AlertesClient({ domaines, actus }: { domaines: string[]; actus: Actu[] }) {
  const [suivis, setSuivis] = useState<string[]>([]);
  const [pret, setPret] = useState(false);

  // Lecture du suivi local au montage (localStorage : reste sur l'appareil).
  useEffect(() => {
    try {
      const raw = localStorage.getItem(KEY);
      if (raw) setSuivis(JSON.parse(raw));
    } catch {
      /* ignore */
    }
    setPret(true);
  }, []);

  useEffect(() => {
    if (pret) {
      try {
        localStorage.setItem(KEY, JSON.stringify(suivis));
      } catch {
        /* ignore */
      }
    }
  }, [suivis, pret]);

  const toggle = (d: string) => setSuivis((s) => (s.includes(d) ? s.filter((x) => x !== d) : [...s, d]));

  const actusSuivies = suivis.length
    ? actus.filter((a) => a.domaine && suivis.includes(a.domaine))
    : [];
  const moduleDepuis = (lien?: string) => (lien || "").replace("/fiche/", "").replace("/loi/", "").split("#")[0];

  return (
    <div className="max-w-3xl mx-auto px-6 py-6">
      <fieldset className="rounded-2xl border border-slate-200 p-5">
        <legend className="px-2 text-sm font-semibold text-slate-700">Mes domaines suivis</legend>
        <div className="flex flex-wrap gap-2">
          {domaines.map((d) => {
            const on = suivis.includes(d);
            return (
              <button
                key={d}
                onClick={() => toggle(d)}
                aria-pressed={on}
                className={`px-3 py-1.5 rounded-full text-sm border transition ${
                  on
                    ? "bg-indigo-600 text-white border-indigo-600"
                    : "border-slate-300 text-slate-600 hover:bg-slate-100"
                }`}
              >
                {on ? "✓ " : "+ "}
                {d}
              </button>
            );
          })}
        </div>
        <p className="mt-3 text-xs text-slate-400">
          {suivis.length === 0
            ? "Sélectionnez un ou plusieurs domaines pour activer votre suivi."
            : `${suivis.length} domaine(s) suivi(s) · enregistré sur votre appareil.`}
        </p>
      </fieldset>

      <div className="mt-6">
        <h2 className="text-lg font-bold">Évolutions de mes dossiers</h2>
        {suivis.length === 0 ? (
          <p className="mt-2 text-slate-500 text-sm">
            Choisissez des domaines ci-dessus : leurs actualités apparaîtront ici.
          </p>
        ) : actusSuivies.length === 0 ? (
          <p className="mt-2 text-slate-500 text-sm">
            Aucune évolution récente sur vos domaines suivis. C&apos;est bon signe — rien d&apos;urgent.
          </p>
        ) : (
          <ul className="mt-3 space-y-3">
            {actusSuivies.map((a) => {
              const mod = moduleDepuis(a.lien_fiche);
              const inner = (
                <>
                  <div className="flex items-center gap-2">
                    <span className="text-[11px] font-medium text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full">
                      {a.domaine}
                    </span>
                    {a.date && <span className="text-[11px] text-slate-400 ml-auto">{a.date}</span>}
                  </div>
                  <p className="mt-2 font-semibold text-slate-900">{a.titre}</p>
                  {a.detail && <p className="mt-1 text-sm text-slate-600">{a.detail}</p>}
                </>
              );
              return (
                <li key={a.id}>
                  {mod ? (
                    <Link href={`/loi/${mod}`} className="block rounded-2xl border border-slate-200 p-4 hover:border-indigo-300 hover:bg-indigo-50/40 transition">
                      {inner}
                    </Link>
                  ) : (
                    <div className="rounded-2xl border border-slate-200 p-4">{inner}</div>
                  )}
                </li>
              );
            })}
          </ul>
        )}
      </div>

      <p className="mt-8 text-xs rounded-lg bg-slate-50 border border-slate-200 px-3 py-2 text-slate-500">
        Bientôt : recevoir ces alertes par e-mail ou notification. Cette option (qui nécessite un
        envoi externe) sera activée prochainement — pour l&apos;instant, le suivi reste 100 % privé,
        sur votre appareil.
      </p>
    </div>
  );
}
