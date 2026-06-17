"use client";

import { useState, useEffect } from "react";

interface Report {
  id: string;
  title: string;
  description: string;
  pages: number;
  userId: string;
  createdAt: string;
}

function formatDate(dateStr: string) {
  const date = new Date(dateStr);
  return date.toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" });
}

function ReportSkeleton() {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 animate-pulse">
      <div className="flex items-start justify-between mb-3">
        <div className="w-10 h-10 bg-slate-100 rounded-xl"></div>
        <div className="h-5 w-14 bg-slate-100 rounded-full"></div>
      </div>
      <div className="h-4 w-48 bg-slate-200 rounded mb-2"></div>
      <div className="h-3 w-full bg-slate-100 rounded mb-1"></div>
      <div className="h-3 w-3/4 bg-slate-100 rounded mb-4"></div>
      <div className="flex justify-between">
        <div className="h-3 w-20 bg-slate-100 rounded"></div>
        <div className="h-3 w-16 bg-slate-100 rounded"></div>
      </div>
    </div>
  );
}

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
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Rapports</h2>
          <p className="text-slate-500 text-sm mt-1">
            {loading
              ? "Chargement..."
              : `${reports.length} rapport${reports.length > 1 ? "s" : ""} disponible${reports.length > 1 ? "s" : ""}`}
          </p>
        </div>
        <button
          onClick={generateReport}
          disabled={generating || loading}
          className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors disabled:opacity-60 disabled:cursor-not-allowed flex items-center gap-2"
        >
          {generating ? (
            <>
              <span className="w-3 h-3 rounded-full border-2 border-white/30 border-t-white animate-spin"></span>
              Génération...
            </>
          ) : (
            "✦ Générer un rapport"
          )}
        </button>
      </div>

      <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-5">
        {loading
          ? [...Array(3)].map((_, i) => <ReportSkeleton key={i} />)
          : reports.map((r) => (
              <div key={r.id} className="bg-white rounded-xl border border-slate-200 p-5 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between mb-3">
                  <div className="w-10 h-10 bg-indigo-50 rounded-xl flex items-center justify-center text-indigo-600 text-lg">
                    📊
                  </div>
                  <span className="text-xs bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded-full font-medium">
                    Prêt
                  </span>
                </div>
                <h3 className="font-semibold text-slate-900 text-sm mb-1">{r.title}</h3>
                <p className="text-xs text-slate-500 mb-4 leading-relaxed">{r.description}</p>
                <div className="flex items-center justify-between text-xs text-slate-400">
                  <span>{formatDate(r.createdAt)}</span>
                  <span>{r.pages} pages</span>
                </div>
                <div className="flex gap-2 mt-4">
                  <button className="flex-1 bg-indigo-600 text-white py-2 rounded-lg text-xs font-medium hover:bg-indigo-700 transition-colors">
                    Télécharger PDF
                  </button>
                  <button className="flex-1 border border-slate-200 text-slate-600 py-2 rounded-lg text-xs font-medium hover:bg-slate-50 transition-colors">
                    Partager
                  </button>
                </div>
              </div>
            ))}
      </div>

      {/* Report templates */}
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <h3 className="font-semibold text-slate-900 mb-4">Modèles de rapports</h3>
        <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
          {[
            { title: "Analyse concurrentielle complète", desc: "Vue d'ensemble de tous vos concurrents", icon: "🏆" },
            { title: "Comparaison des prix", desc: "Focus sur les stratégies tarifaires", icon: "💰" },
            { title: "Rapport de fonctionnalités", desc: "Matrice de comparaison des fonctionnalités", icon: "⚡" },
            { title: "Rapport de menaces", desc: "Identification des risques concurrentiels", icon: "⚠️" },
            { title: "Tendances du marché", desc: "Évolutions et opportunités du secteur", icon: "📈" },
            { title: "Rapport exécutif", desc: "Synthèse pour la direction", icon: "📋" },
          ].map((t) => (
            <button
              key={t.title}
              onClick={generateReport}
              disabled={generating}
              className="text-left border border-slate-200 rounded-xl p-4 hover:border-indigo-300 hover:bg-indigo-50 transition-all group disabled:opacity-60"
            >
              <span className="text-2xl block mb-2">{t.icon}</span>
              <p className="text-sm font-medium text-slate-800 group-hover:text-indigo-700">{t.title}</p>
              <p className="text-xs text-slate-500 mt-1">{t.desc}</p>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
