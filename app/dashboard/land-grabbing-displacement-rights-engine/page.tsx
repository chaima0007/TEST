"use client";
import { useEffect, useState } from "react";

interface Entity {
  entity_id: string; name: string; country: string;
  composite_score: number; risk_level: string; primary_pattern: string;
  [key: string]: unknown;
}
interface EngineData {
  agent: string; total_entities: number; avg_composite: number;
  confidence_score: number; risk_distribution: Record<string, number>;
  data_sources: string[]; critical_alerts: string[]; entities: Entity[];
  [key: string]: unknown;
}

function GaugeRing({ value, accent }: { value: number; accent: string }) {
  const r = 36, cx = 44, cy = 44, stroke = 8;
  const circ = 2 * Math.PI * r;
  const pct = Math.min(Math.max(value / 10, 0), 1);
  return (
    <svg viewBox="0 0 88 88" className="w-24 h-24">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={stroke} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={accent} strokeWidth={stroke}
        strokeDasharray={`${pct * circ} ${circ}`} strokeLinecap="round"
        transform="rotate(-90 44 44)" />
      <text x={cx} y={cy} textAnchor="middle" dominantBaseline="central"
        fill="white" fontSize="14" fontWeight="bold">{value.toFixed(1)}</text>
    </svg>
  );
}

export default function LandGrabbingDisplacementRightsPage() {
  const [data, setData] = useState<EngineData | null>(null);
  const ACCENT = "#422006";
  const RC: Record<string, string> = { critique: "#ef4444", "élevé": "#f97316", "modéré": "#eab308", faible: "#22c55e" };

  useEffect(() => {
    fetch("/api/land-grabbing-displacement-rights-engine").then(r => r.json()).then(d => setData(d.payload ?? d));
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400 animate-pulse">Chargement...</div>
    </div>
  );

  const indexValue = (data["avg_estimated_land_grabbing_displacement_rights_index"] as number) ?? 0;

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      <div className="max-w-6xl mx-auto space-y-6">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">{data.agent}</h1>
            <p className="text-slate-400 text-sm mt-1">{data.total_entities} entités · Confiance {((data.confidence_score ?? 0) * 100).toFixed(0)}% · MAJ 2026-06-21</p>
          </div>
          <GaugeRing value={indexValue} accent={ACCENT} />
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(data.risk_distribution).map(([level, count]) => (
            <div key={level} className="bg-slate-900 rounded-xl p-4 border border-slate-800">
              <div className="text-2xl font-bold" style={{ color: RC[level] }}>{count}</div>
              <div className="text-slate-400 text-xs mt-1 capitalize">{level}</div>
            </div>
          ))}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.entities.map(e => (
            <div key={e.entity_id} className="bg-slate-900 rounded-xl p-4 border border-slate-800">
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-xs px-2 py-0.5 rounded-full font-medium"
                      style={{ backgroundColor: RC[e.risk_level] + "33", color: RC[e.risk_level] }}>
                      {e.risk_level}
                    </span>
                    <span className="text-slate-500 text-xs">{e.entity_id}</span>
                  </div>
                  <p className="text-white text-sm font-medium leading-snug line-clamp-2">{e.name}</p>
                  <p className="text-slate-500 text-xs mt-1">{e.primary_pattern.replace(/_/g, " ")}</p>
                </div>
                <div className="text-right shrink-0">
                  <div className="text-lg font-bold" style={{ color: ACCENT }}>{e.composite_score}</div>
                  <div className="text-slate-500 text-xs">/ 100</div>
                </div>
              </div>
            </div>
          ))}
        </div>
        {data.critical_alerts && data.critical_alerts.length > 0 && (
          <div className="bg-slate-900 rounded-xl p-4 border border-red-900/30">
            <h3 className="text-red-400 font-semibold text-sm mb-3">Alertes critiques</h3>
            <ul className="space-y-1">
              {data.critical_alerts.map((a, i) => (
                <li key={i} className="text-slate-300 text-xs flex items-start gap-2">
                  <span className="text-red-500 mt-0.5">▲</span>{a}
                </li>
              ))}
            </ul>
          </div>
        )}
        <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
          <h3 className="text-slate-400 font-semibold text-xs mb-2 uppercase tracking-wider">Sources de données</h3>
          <div className="flex flex-wrap gap-2">
            {data.data_sources.map((s, i) => (
              <span key={i} className="text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded-lg">{s}</span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
