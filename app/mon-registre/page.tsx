"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

// Registre de conformité — LOCAL au navigateur (localStorage), aucun envoi serveur.
// Switching-cost honnête + RGPD-clean : l'historique des diagnostics/attestations s'accumule
// chez l'utilisateur. Exportable (JSON) pour le conserver / le transmettre à son comptable.

type Entree = {
  date: string; type?: string; ref?: string; raison_sociale?: string | null;
  pct_global?: number; normes?: string[];
};

export default function MonRegistre() {
  const [entrees, setEntrees] = useState<Entree[]>([]);
  const [pret, setPret] = useState(false);

  useEffect(() => {
    try {
      setEntrees(JSON.parse(localStorage.getItem("caelum_registre") || "[]"));
    } catch {}
    setPret(true);
  }, []);

  function exporter() {
    const blob = new Blob([JSON.stringify(entrees, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = "registre-conformite-caelum.json"; a.click();
    URL.revokeObjectURL(url);
  }
  function vider() {
    if (!confirm("Effacer tout votre registre local ? (action irréversible)")) return;
    localStorage.removeItem("caelum_registre"); setEntrees([]);
  }

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-3xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <span className="font-bold text-lg">Caelum</span>
          </Link>
          <Link href="/conformite-2026" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Nouveau diagnostic</Link>
        </div>
      </header>

      <section className="bg-gradient-to-b from-slate-950 to-slate-900 text-white py-14 px-6">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-bold">Mon registre de conformité</h1>
          <p className="mt-3 text-slate-300 max-w-2xl">
            L'historique de vos diagnostics et attestations — conservé <strong>dans votre navigateur</strong>,
            jamais envoyé à un serveur. Exportez-le pour le garder ou le transmettre à votre comptable.
          </p>
        </div>
      </section>

      <div className="max-w-3xl mx-auto px-6 py-10">
        {!pret ? null : entrees.length === 0 ? (
          <div className="rounded-2xl border border-slate-200 p-8 text-center">
            <p className="text-slate-600">Votre registre est vide.</p>
            <Link href="/conformite-2026" className="inline-block mt-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-6 py-3 rounded-xl transition-colors">
              Faire mon premier diagnostic
            </Link>
          </div>
        ) : (
          <>
            <div className="flex items-center justify-between mb-4">
              <p className="text-sm text-slate-500">{entrees.length} entrée{entrees.length > 1 ? "s" : ""}</p>
              <div className="flex gap-2">
                <button onClick={exporter} className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Exporter (JSON)</button>
                <button onClick={vider} className="text-sm font-semibold text-rose-600 hover:text-rose-800">Vider</button>
              </div>
            </div>
            <div className="grid gap-3">
              {[...entrees].reverse().map((e, i) => (
                <article key={i} className="rounded-2xl border border-slate-200 p-5">
                  <div className="flex items-center justify-between gap-3">
                    <span className="font-semibold text-slate-900">
                      {e.type === "attestation" ? "📄 Attestation" : "🧭 Diagnostic"}
                      {e.raison_sociale ? ` — ${e.raison_sociale}` : ""}
                    </span>
                    <span className="text-xs text-slate-400">{e.date?.slice(0, 16).replace("T", " ")}</span>
                  </div>
                  {typeof e.pct_global === "number" && (
                    <p className="text-sm text-slate-600 mt-1">Score d'auto-évaluation : <strong>{e.pct_global}%</strong></p>
                  )}
                  {e.ref && <p className="text-xs text-slate-500 mt-1">Réf. {e.ref}</p>}
                  {e.normes && e.normes.length > 0 && (
                    <p className="text-xs text-slate-500 mt-1">{e.normes.length} norme(s) : {e.normes.slice(0, 6).join(", ")}{e.normes.length > 6 ? "…" : ""}</p>
                  )}
                </article>
              ))}
            </div>
          </>
        )}

        <p className="mt-8 text-xs text-slate-400 border-t border-slate-100 pt-4">
          🔒 Confidentialité : ce registre vit uniquement dans votre navigateur (localStorage). Rien n'est transmis à Caelum.
          Videz le cache du navigateur = perte du registre → pensez à <strong>exporter</strong>. Auto-évaluation, pas une certification officielle.
        </p>
      </div>
    </main>
  );
}
