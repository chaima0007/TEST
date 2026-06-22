"use client";
import { useEffect, useState } from "react";

const ACCENT = "#4a2c0a";

function GaugeRing({ value, color }: { value: number; color: string }) {
  const r = 36, cx = 44, cy = 44;
  const circ = 2 * Math.PI * r;
  const offset = circ - (value / 100) * circ;
  return (
    <svg viewBox="0 0 88 88" className="w-full h-full">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={8}
        strokeDasharray={circ} strokeDashoffset={offset}
        strokeLinecap="round" transform="rotate(-90 44 44)" />
    </svg>
  );
}

interface EngineData {
  agent: string;
  domain: string;
  total_entities: number;
  avg_composite: number;
  confidence_score: number;
  avg_estimated_leather_tannery_chromium_rights_index: number;
  risk_distribution: { critique: number; "élevé": number; modéré: number; faible: number };
  data_sources: string[];
  critical_alerts: unknown[];
  entities: unknown[];
}

export default function LeatherTanneryChromiumRightsDashboard() {
  const [data, setData] = useState<EngineData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"overview" | "distribution" | "sources">("overview");

  useEffect(() => {
    fetch("/api/leather-tannery-chromium-rights")
      .then((r) => r.json())
      .then((d) => {
        setData(d.payload ?? d);
        setLoading(false);
      })
      .catch(() => {
        setError("Erreur de chargement");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-400 text-lg">Chargement...</div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-red-400 text-lg">{error ?? "Données indisponibles"}</div>
      </div>
    );
  }

  const composite = data.avg_composite ?? 0;
  const index = data.avg_estimated_leather_tannery_chromium_rights_index ?? 0;
  const confidence = (data.confidence_score ?? 0) * 100;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div className="border-l-4 pl-6" style={{ borderColor: ACCENT }}>
          <h1 className="text-3xl font-bold text-white">
            Droits — Tanneries et Chrome Hexavalent
          </h1>
          <p className="text-slate-400 mt-2">
            Chromium Pollution · Tannery Workers · Occupational Health · Environmental Rights
          </p>
          <p className="text-slate-500 text-sm mt-1">{data.agent}</p>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-slate-900 rounded-2xl p-6 flex flex-col items-center">
            <div className="w-32 h-32 mb-4">
              <GaugeRing value={composite} color="#ef4444" />
            </div>
            <div className="text-4xl font-bold text-white">{composite.toFixed(2)}</div>
            <div className="text-slate-400 text-sm mt-1">Score Composite Moyen</div>
          </div>

          <div className="bg-slate-900 rounded-2xl p-6 flex flex-col items-center">
            <div className="w-32 h-32 mb-4">
              <GaugeRing value={index * 10} color="#f97316" />
            </div>
            <div className="text-4xl font-bold text-white">{index.toFixed(2)}</div>
            <div className="text-slate-400 text-sm mt-1">Indice Tanneries &amp; Chrome</div>
          </div>

          <div className="bg-slate-900 rounded-2xl p-6 flex flex-col items-center">
            <div className="w-32 h-32 mb-4">
              <GaugeRing value={confidence} color="#0ea5e9" />
            </div>
            <div className="text-4xl font-bold text-white">{confidence.toFixed(0)}%</div>
            <div className="text-slate-400 text-sm mt-1">Score de Confiance</div>
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-slate-900 rounded-2xl p-6">
          <div className="flex gap-4 mb-6 border-b border-slate-800 pb-4">
            {(["overview", "distribution", "sources"] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                style={{
                  color: activeTab === tab ? "#f97316" : "#94a3b8",
                  borderBottom: activeTab === tab ? "2px solid #f97316" : "2px solid transparent",
                  paddingBottom: "4px",
                  fontWeight: activeTab === tab ? 600 : 400,
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                  fontSize: "0.95rem",
                }}
              >
                {tab === "overview" ? "Vue d&apos;ensemble" : tab === "distribution" ? "Distribution" : "Sources"}
              </button>
            ))}
          </div>

          {activeTab === "overview" && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-slate-800 rounded-xl p-4 text-center">
                <div className="text-2xl font-bold text-white">{data.total_entities}</div>
                <div className="text-slate-400 text-sm mt-1">Entités Analysées</div>
              </div>
              <div className="bg-slate-800 rounded-xl p-4 text-center">
                <div className="text-2xl font-bold text-red-400">{data.risk_distribution.critique}</div>
                <div className="text-slate-400 text-sm mt-1">Risque Critique</div>
              </div>
              <div className="bg-slate-800 rounded-xl p-4 text-center">
                <div className="text-2xl font-bold text-orange-400">{data.risk_distribution["élevé"]}</div>
                <div className="text-slate-400 text-sm mt-1">Risque Élevé</div>
              </div>
              <div className="bg-slate-800 rounded-xl p-4 text-center">
                <div className="text-2xl font-bold text-green-400">{data.risk_distribution.faible}</div>
                <div className="text-slate-400 text-sm mt-1">Risque Faible</div>
              </div>
            </div>
          )}

          {activeTab === "distribution" && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-red-950/40 border border-red-800/30 rounded-xl p-4 text-center">
                <div className="text-3xl font-bold text-red-400">{data.risk_distribution.critique}</div>
                <div className="text-red-300/70 text-sm mt-1">Critique</div>
              </div>
              <div className="bg-orange-950/40 border border-orange-800/30 rounded-xl p-4 text-center">
                <div className="text-3xl font-bold text-orange-400">{data.risk_distribution["élevé"]}</div>
                <div className="text-orange-300/70 text-sm mt-1">Élevé</div>
              </div>
              <div className="bg-yellow-950/40 border border-yellow-800/30 rounded-xl p-4 text-center">
                <div className="text-3xl font-bold text-yellow-400">{data.risk_distribution.modéré}</div>
                <div className="text-yellow-300/70 text-sm mt-1">Modéré</div>
              </div>
              <div className="bg-green-950/40 border border-green-800/30 rounded-xl p-4 text-center">
                <div className="text-3xl font-bold text-green-400">{data.risk_distribution.faible}</div>
                <div className="text-green-300/70 text-sm mt-1">Faible</div>
              </div>
            </div>
          )}

          {activeTab === "sources" && (
            <div className="flex flex-wrap gap-2">
              {data.data_sources.map((source) => (
                <span
                  key={source}
                  className="px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300 border border-slate-700"
                >
                  {source}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Meta */}
        <div className="text-slate-600 text-xs text-right">
          Domaine : {data.domain} · Entités : {data.total_entities}
        </div>
      </div>
    </div>
  );
}
