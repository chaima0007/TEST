"use client";

import { useState, useEffect } from "react";

interface Report {
  id: string;
  title: string;
  description: string;
  pages: number;
  status: string;
  createdAt: string;
}

function formatDate(dateStr: string) {
  const date = new Date(dateStr);
  return date.toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" });
}

function ReportSkeleton() {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 animate-pulse">
      <div className="flex items-start justify-between mb-4">
        <div className="w-11 h-11 bg-slate-100 rounded-xl" />
        <div className="h-5 w-14 bg-slate-100 rounded-full" />
      </div>
      <div className="h-4 w-52 bg-slate-200 rounded mb-2" />
      <div className="h-3 w-full bg-slate-100 rounded mb-1.5" />
      <div className="h-3 w-3/4 bg-slate-100 rounded mb-5" />
      <div className="flex items-center justify-between mb-4">
        <div className="h-3 w-24 bg-slate-100 rounded" />
        <div className="h-3 w-16 bg-slate-100 rounded" />
      </div>
      <div className="flex gap-2">
        <div className="flex-1 h-8 bg-slate-100 rounded-lg" />
        <div className="flex-1 h-8 bg-slate-100 rounded-lg" />
      </div>
    </div>
  );
}

const REPORT_PALETTE = [
  "from-indigo-500 to-indigo-600",
  "from-violet-500 to-violet-600",
  "from-blue-500 to-blue-600",
];

const TEMPLATES = [
  { title: "Analyse concurrentielle complète", desc: "Vue d'ensemble de tous vos concurrents", icon: "🏆", color: "group-hover:text-amber-600", hover: "hover:border-amber-200 hover:bg-amber-50" },
  { title: "Comparaison des prix", desc: "Focus sur les stratégies tarifaires", icon: "💰", color: "group-hover:text-emerald-600", hover: "hover:border-emerald-200 hover:bg-emerald-50" },
  { title: "Rapport de fonctionnalités", desc: "Matrice de comparaison des fonctionnalités", icon: "⚡", color: "group-hover:text-indigo-600", hover: "hover:border-indigo-200 hover:bg-indigo-50" },
  { title: "Rapport de menaces", desc: "Identification des risques concurrentiels", icon: "⚠️", color: "group-hover:text-red-600", hover: "hover:border-red-200 hover:bg-red-50" },
  { title: "Tendances du marché", desc: "Évolutions et opportunités du secteur", icon: "📈", color: "group-hover:text-blue-600", hover: "hover:border-blue-200 hover:bg-blue-50" },
  { title: "Rapport exécutif", desc: "Synthèse pour la direction", icon: "📋", color: "group-hover:text-violet-600", hover: "hover:border-violet-200 hover:bg-violet-50" },
];

export default function ReportsPage() {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    fetch("/api/reports")
      .then((r) => r.json())
      .then((data: Report[]) => {
        setReports(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const generateReport = async () => {
    setGenerating(true);
    try {
      const res = await fetch("/api/reports", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });
      if (res.ok) {
        const newReport = await res.json() as Report;
        setReports((prev) => [newReport, ...prev]);
      }
    } catch {
      // silent
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Rapports</h2>
          <p className="text-slate-500 text-sm mt-1">
            {loading
              ? "Chargement…"
              : `${reports.length} rapport${reports.length > 1 ? "s" : ""} disponible${reports.length > 1 ? "s" : ""}`}
          </p>
        </div>
        <button
          onClick={generateReport}
          disabled={generating || loading}
          className="bg-indigo-600 text-white px-4 py-2.5 rounded-lg text-sm font-medium hover:bg-indigo-700 active:bg-indigo-800 transition-colors disabled:opacity-60 disabled:cursor-not-allowed flex items-center gap-2 shadow-sm"
        >
          {generating ? (
            <>
              <span className="w-3.5 h-3.5 rounded-full border-2 border-white/30 border-t-white animate-spin" />
              Génération…
            </>
          ) : (
            <>
              <span className="text-indigo-200">✦</span>
              Générer un rapport
            </>
          )}
        </button>
      </div>

      {/* Report grid */}
      <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-5">
        {loading
          ? [...Array(3)].map((_, i) => <ReportSkeleton key={i} />)
          : reports.map((r, idx) => (
              <div
                key={r.id}
                className="bg-white rounded-xl border border-slate-200 p-5 hover:shadow-lg hover:border-indigo-200 transition-all group cursor-default"
              >
                {/* Top row */}
                <div className="flex items-start justify-between mb-4">
                  <div className={`w-11 h-11 rounded-xl bg-gradient-to-br ${REPORT_PALETTE[idx % REPORT_PALETTE.length]} flex items-center justify-center text-white text-xl shadow-sm`}>
                    📊
                  </div>
                  <span className="flex items-center gap-1.5 text-xs bg-emerald-50 text-emerald-700 px-2.5 py-1 rounded-full font-medium border border-emerald-100">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block" />
                    {r.status === "ready" ? "Prêt" : r.status}
                  </span>
                </div>

                {/* Title & description */}
                <h3 className="font-semibold text-slate-900 text-sm mb-1.5 group-hover:text-indigo-700 transition-colors">{r.title}</h3>
                <p className="text-xs text-slate-500 leading-relaxed mb-4">{r.description}</p>

                {/* Meta */}
                <div className="flex items-center justify-between text-xs text-slate-400 mb-4">
                  <span className="flex items-center gap-1">
                    <svg className="w-3.5 h-3.5" viewBox="0 0 14 14" fill="none">
                      <rect x="1" y="2" width="12" height="11" rx="2" stroke="currentColor" strokeWidth="1.2" />
                      <path d="M1 5h12" stroke="currentColor" strokeWidth="1.2" />
                      <path d="M4 1v2M10 1v2" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
                    </svg>
                    {formatDate(r.createdAt)}
                  </span>
                  <span className="flex items-center gap-1">
                    <svg className="w-3.5 h-3.5" viewBox="0 0 14 14" fill="none">
                      <path d="M3 1h6l3 3v9a1 1 0 01-1 1H3a1 1 0 01-1-1V2a1 1 0 011-1z" stroke="currentColor" strokeWidth="1.2" />
                      <path d="M9 1v3h3" stroke="currentColor" strokeWidth="1.2" strokeLinejoin="round" />
                    </svg>
                    {r.pages} pages
                  </span>
                </div>

                {/* Actions */}
                <div className="flex gap-2">
                  <button className="flex-1 flex items-center justify-center gap-1.5 bg-indigo-600 text-white py-2 rounded-lg text-xs font-medium hover:bg-indigo-700 transition-colors">
                    <svg className="w-3.5 h-3.5" viewBox="0 0 14 14" fill="none">
                      <path d="M7 1v8M4 7l3 3 3-3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                      <path d="M2 11h10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                    </svg>
                    Télécharger PDF
                  </button>
                  <button className="flex-1 flex items-center justify-center gap-1.5 border border-slate-200 text-slate-600 py-2 rounded-lg text-xs font-medium hover:bg-slate-50 hover:border-slate-300 transition-colors">
                    <svg className="w-3.5 h-3.5" viewBox="0 0 14 14" fill="none">
                      <circle cx="11" cy="3" r="1.5" stroke="currentColor" strokeWidth="1.2" />
                      <circle cx="3" cy="7" r="1.5" stroke="currentColor" strokeWidth="1.2" />
                      <circle cx="11" cy="11" r="1.5" stroke="currentColor" strokeWidth="1.2" />
                      <path d="M4.3 6.2l5.4-2.4M4.3 7.8l5.4 2.4" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
                    </svg>
                    Partager
                  </button>
                </div>
              </div>
            ))}
      </div>

      {/* AI promo banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-indigo-600 via-indigo-700 to-violet-700 p-6 flex items-center justify-between gap-6">
        {/* Background decoration */}
        <div className="absolute inset-0 pointer-events-none overflow-hidden">
          <div className="absolute -top-8 -right-8 w-48 h-48 rounded-full bg-white/5" />
          <div className="absolute -bottom-10 right-24 w-32 h-32 rounded-full bg-white/5" />
          <div className="absolute top-2 left-1/2 w-64 h-1 bg-white/10 rounded-full rotate-12" />
        </div>
        <div className="relative">
          <p className="text-xs font-semibold text-indigo-200 uppercase tracking-widest mb-1">Intelligence Artificielle</p>
          <h3 className="text-lg font-bold text-white mb-1">Laissez l&apos;IA générer votre rapport</h3>
          <p className="text-sm text-indigo-200 max-w-md">
            Obtenez une analyse concurrentielle complète en quelques secondes, basée sur toutes les données collectées.
          </p>
        </div>
        <button
          onClick={generateReport}
          disabled={generating}
          className="relative flex-shrink-0 bg-white text-indigo-700 font-semibold text-sm px-5 py-2.5 rounded-xl hover:bg-indigo-50 transition-colors disabled:opacity-70 disabled:cursor-not-allowed flex items-center gap-2 shadow-lg"
        >
          {generating ? (
            <>
              <span className="w-3.5 h-3.5 rounded-full border-2 border-indigo-300 border-t-indigo-700 animate-spin" />
              En cours…
            </>
          ) : (
            <>✦ Générer maintenant</>
          )}
        </button>
      </div>

      {/* Templates section */}
      <div>
        <div className="mb-4">
          <h3 className="text-base font-semibold text-slate-900">Créez à partir d&apos;un modèle</h3>
          <p className="text-sm text-slate-500 mt-0.5">Sélectionnez un modèle pour démarrer rapidement</p>
        </div>
        <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
          {TEMPLATES.map((t) => (
            <button
              key={t.title}
              onClick={generateReport}
              disabled={generating}
              className={`text-left border border-slate-200 rounded-xl p-4 transition-all group disabled:opacity-60 ${t.hover}`}
            >
              <span className="text-2xl block mb-3">{t.icon}</span>
              <p className={`text-sm font-semibold text-slate-800 mb-1 transition-colors ${t.color}`}>{t.title}</p>
              <p className="text-xs text-slate-500 leading-relaxed">{t.desc}</p>
              <div className="mt-3 flex items-center gap-1 text-xs text-slate-400 group-hover:text-slate-600 transition-colors">
                <svg className="w-3 h-3" viewBox="0 0 12 12" fill="none">
                  <path d="M2 6h8M7 3l3 3-3 3" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                Utiliser ce modèle
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
