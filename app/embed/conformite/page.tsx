"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

// Widget marque blanche embarquable (pépite com n°4 — canal fiduciaires scalable).
// À intégrer en iframe sur le site d'un cabinet : <iframe src=".../embed/conformite?cabinet=NomCabinet">.
// Compact, sans header/footer. Le diagnostic complet reste hébergé par Caelum (le moteur).

export default function EmbedConformite() {
  const [cabinet, setCabinet] = useState("");

  useEffect(() => {
    try {
      const c = new URLSearchParams(window.location.search).get("cabinet");
      if (c) setCabinet(c.slice(0, 60));
    } catch {}
  }, []);

  return (
    <main className="min-h-screen bg-white text-slate-900 flex items-center justify-center p-5">
      <div className="w-full max-w-md rounded-2xl border border-slate-200 shadow-sm p-6">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold uppercase tracking-wide text-indigo-600">Conformité 2026</span>
          {cabinet && <span className="text-[11px] text-slate-400">par {cabinet}</span>}
        </div>
        <h1 className="mt-2 text-xl font-bold leading-snug">Votre entreprise est-elle en règle pour 2026 ?</h1>
        <p className="mt-2 text-sm text-slate-600">
          E-facturation, RGPD, NIS2, CSRD… Découvrez en 1 minute les obligations qui vous concernent,
          votre score, et les aides publiques qui financent la mise en conformité.
        </p>
        <ul className="mt-4 space-y-1.5 text-sm text-slate-700">
          {["Diagnostic gratuit en 1 minute", "Sources légales officielles", "Aides régionales identifiées"].map((p) => (
            <li key={p} className="flex items-center gap-2">
              <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-emerald-500 flex-shrink-0">
                <path fillRule="evenodd" d="M16.7 5.3a1 1 0 010 1.4l-7.5 7.5a1 1 0 01-1.4 0L3.3 9.7a1 1 0 011.4-1.4L8.5 12l6.8-6.8a1 1 0 011.4 0z" clipRule="evenodd" />
              </svg>
              {p}
            </li>
          ))}
        </ul>
        <Link
          href="/conformite-2026"
          target="_top"
          className="mt-5 block text-center bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-5 py-3 rounded-xl transition-colors"
        >
          Faire le diagnostic gratuit
        </Link>
        <p className="mt-3 text-[11px] text-slate-400 text-center">
          Diagnostic indicatif (auto-évaluation). Propulsé par Caelum.
        </p>
      </div>
    </main>
  );
}
