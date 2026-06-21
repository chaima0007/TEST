"use client";
import { useEffect, useState } from "react";

interface Entity {
  entity_id: string;
  name: string;
  composite_score: number;
  risk_level: string;
  estimated_child_labor_education_rights_index: number;
}

interface EngineData {
  agent: string;
  total_entities: number;
  avg_composite: number;
  confidence_score: number;
  avg_estimated_child_labor_education_rights_index: number;
  risk_distribution: Record<string, number>;
  critical_alerts: string[];
  data_sources: string[];
  entities: Entity[];
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

function DetailModal({ entity, accent, onClose }: {
  entity: Entity; accent: string; onClose: () => void;
}) {
  const [tab, setTab] = useState<"apercu" | "metriques" | "sources">("apercu");
  const RC: Record<string, string> = {
    critique: "#ef4444", "élevé": "#f97316", modéré: "#eab308", faible: "#22c55e",
  };
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4"
      onClick={onClose}>
      <div className="bg-slate-900 rounded-2xl max-w-lg w-full p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}>
        <div className="flex justify-between items-start mb-4">
          <h3 className="text-white font-bold text-sm leading-snug pr-4">{entity.name}</h3>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl leading-none">×</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["apercu", "metriques", "sources"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded-full text-xs font-medium ${tab === t ? "text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}
              style={tab === t ? { backgroundColor: accent } : {}}>
              {t === "apercu" ? "Aperçu" : t === "metriques" ? "Métriques" : "Sources"}
            </button>
          ))}
        </div>
        {tab === "apercu" && (
          <div className="space-y-3">
            <div className="flex items-center gap-3">
              <span className="text-xs px-2 py-1 rounded-full font-medium"
                style={{ backgroundColor: RC[entity.risk_level] + "33", color: RC[entity.risk_level] }}>
                {entity.risk_level}
              </span>
              <span className="text-slate-300 text-sm">{entity.entity_id}</span>
            </div>
          </div>
        )}
        {tab === "metriques" && (
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Score composite</span>
              <span className="text-white font-bold">{entity.composite_score}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Index estimé</span>
              <span style={{ color: accent }} className="font-bold">{entity.estimated_child_labor_education_rights_index}</span>
            </div>
          </div>
        )}
        {tab === "sources" && (
          <p className="text-slate-400 text-xs">Sources disponibles via l&apos;API engine.</p>
        )}
      </div>
    </div>
  );
}

export default function ChildLaborEducationRightsPage() {
  const [data, setData] = useState<EngineData | null>(null);
  const [selected, setSelected] = useState<Entity | null>(null);
  const ACCENT = "#f97316";
  const RC: Record<string, string> = {
    critique: "#ef4444", "élevé": "#f97316", modéré: "#eab308", faible: "#22c55e",
  };

  useEffect(() => {
    fetch("/api/child-labor-education-rights-engine")
      .then(r => r.json())
      .then(d => setData(d.payload ?? d));
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400 animate-pulse">Chargement...</div>
    </div>
  );

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      {selected && (
        <DetailModal entity={selected} accent={ACCENT} onClose={() => setSelected(null)} />
      )}
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">Travail des Enfants &amp; Droits à l&apos;Éducation</h1>
            <p className="text-slate-400 text-sm mt-1">
              {data.total_entities} entités · Confiance {(data.confidence_score * 100).toFixed(0)}% · MAJ 2026-06-21
            </p>
          </div>
          <GaugeRing value={data.avg_estimated_child_labor_education_rights_index} accent={ACCENT} />
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(data.risk_distribution).map(([level, count]) => (
            <div key={level} className="bg-slate-900 rounded-xl p-4 border border-slate-800">
              <div className="text-2xl font-bold" style={{ color: RC[level] }}>{count}</div>
              <div className="text-slate-400 text-xs mt-1 capitalize">{level}</div>
            </div>
          ))}
        </div>

        {/* Entities grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.entities.map(e => (
            <button key={e.entity_id} onClick={() => setSelected(e)}
              className="bg-slate-900 rounded-xl p-4 border border-slate-800 hover:border-slate-600 text-left transition-all">
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
                </div>
                <div className="text-right shrink-0">
                  <div className="text-lg font-bold" style={{ color: ACCENT }}>{e.composite_score}</div>
                  <div className="text-slate-500 text-xs">/ 100</div>
                </div>
              </div>
            </button>
          ))}
        </div>

        {/* Alerts */}
        {data.critical_alerts.length > 0 && (
          <div className="bg-slate-900 rounded-xl p-4 border border-orange-900/30">
            <h3 className="text-orange-400 font-semibold text-sm mb-3">Alertes critiques</h3>
            <ul className="space-y-1">
              {data.critical_alerts.map((a, i) => (
                <li key={i} className="text-slate-300 text-xs flex items-start gap-2">
                  <span className="text-orange-500 mt-0.5">▲</span>{a}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Sources */}
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
