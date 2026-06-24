"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

interface Lead {
  id: string;
  name: string;
  email: string;
  company?: string;
  message?: string;
  tier?: string;
  status: "nouveau" | "en_cours" | "termine";
  ts: string;
}

interface Counts { total: number; nouveau: number; en_cours: number; termine: number; }

const STATUS_META: Record<string, { label: string; cls: string }> = {
  nouveau:  { label: "Nouveau",  cls: "bg-blue-100 text-blue-700 border-blue-200" },
  en_cours: { label: "En cours", cls: "bg-amber-100 text-amber-700 border-amber-200" },
  termine:  { label: "Terminé",  cls: "bg-emerald-100 text-emerald-700 border-emerald-200" },
};

export default function EspaceGestionPage() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [counts, setCounts] = useState<Counts>({ total: 0, nouveau: 0, en_cours: 0, termine: 0 });
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<"all" | "nouveau" | "en_cours" | "termine">("all");

  async function load() {
    setLoading(true);
    try {
      const res = await fetch("/api/waitlist");
      const d = await res.json();
      setLeads(d.leads ?? []);
      setCounts(d.counts ?? { total: 0, nouveau: 0, en_cours: 0, termine: 0 });
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  const shown = filter === "all" ? leads : leads.filter((l) => l.status === filter);

  function fmtDate(ts: string) {
    try { return new Date(ts).toLocaleString("fr-BE", { day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit" }); }
    catch { return ts; }
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-violet-600 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <div>
              <h1 className="font-bold leading-tight">Espace de gestion</h1>
              <p className="text-xs text-slate-400">Ton centre de contrôle</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button onClick={load} className="text-sm font-medium text-slate-600 hover:text-slate-900 px-3 py-2 rounded-lg hover:bg-slate-100">
              ↻ Rafraîchir
            </button>
            <Link href="/" className="text-sm text-slate-500 hover:text-slate-900">← Site</Link>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        {/* Résumé */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
          {[
            { key: "all", label: "Total", value: counts.total, color: "text-slate-900" },
            { key: "nouveau", label: "Nouveaux", value: counts.nouveau, color: "text-blue-600" },
            { key: "en_cours", label: "En cours", value: counts.en_cours, color: "text-amber-600" },
            { key: "termine", label: "Terminés", value: counts.termine, color: "text-emerald-600" },
          ].map((c) => (
            <button key={c.key} onClick={() => setFilter(c.key as typeof filter)}
              className={`text-left bg-white rounded-xl border p-4 transition-all hover:shadow-sm ${filter === c.key ? "border-blue-400 ring-1 ring-blue-200" : "border-slate-200"}`}>
              <div className={`text-2xl font-bold ${c.color}`}>{c.value}</div>
              <div className="text-sm text-slate-500 mt-0.5">{c.label}</div>
            </button>
          ))}
        </div>

        {/* Liste des demandes */}
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
            <h2 className="font-semibold">Demandes des clients</h2>
            <span className="text-xs text-slate-400">{shown.length} affichée(s)</span>
          </div>

          {loading ? (
            <div className="p-12 text-center text-slate-400">Chargement…</div>
          ) : shown.length === 0 ? (
            <div className="p-12 text-center">
              <div className="text-4xl mb-3">📭</div>
              <p className="text-slate-600 font-medium">Aucune demande pour l&apos;instant</p>
              <p className="text-slate-400 text-sm mt-1">
                Dès qu&apos;un client remplit le formulaire de contact, sa demande apparaîtra ici automatiquement.
              </p>
              <Link href="/contact" className="inline-block mt-4 text-sm text-blue-600 hover:underline">
                Voir le formulaire de contact →
              </Link>
            </div>
          ) : (
            <ul className="divide-y divide-slate-100">
              {shown.map((l) => {
                const s = STATUS_META[l.status] ?? STATUS_META.nouveau;
                return (
                  <li key={l.id} className="px-5 py-4 hover:bg-slate-50 transition-colors">
                    <div className="flex items-start justify-between gap-4">
                      <div className="min-w-0">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="font-semibold">{l.name}</span>
                          <span className={`text-xs px-2 py-0.5 rounded-full border ${s.cls}`}>{s.label}</span>
                          {l.tier && <span className="text-xs text-slate-400">· {l.tier}</span>}
                        </div>
                        <p className="text-sm text-slate-500 mt-0.5">{l.email}{l.company ? ` · ${l.company}` : ""}</p>
                        {l.message && <p className="text-sm text-slate-600 mt-2 line-clamp-2">{l.message}</p>}
                      </div>
                      <span className="text-xs text-slate-400 whitespace-nowrap flex-shrink-0">{fmtDate(l.ts)}</span>
                    </div>
                  </li>
                );
              })}
            </ul>
          )}
        </div>

        <p className="text-xs text-slate-400 text-center mt-6">
          Espace privé de gestion · Les demandes arrivent depuis ton formulaire de contact.
        </p>
      </main>
    </div>
  );
}
