"use client";
import { useState, useEffect } from "react";

const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

const ACCENT = "#a16207";

interface Entity {
  id: string;
  name: string;
  composite_score: number;
  estimated_land_rights_index: number;
  risk_level: string;
  [key: string]: unknown;
}

interface DashData {
  total_entities?: number;
  avg_composite?: number;
  avg_estimated_land_rights_index?: number;
  risk_distribution?: Record<string, number>;
  confidence_score?: number;
  entities?: Entity[];
  [key: string]: unknown;
}

function GaugeRing({ value, label, color }: { value: number; label: string; color?: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - Math.min(value, 100) / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color || ACCENT} strokeWidth={8}
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {value.toFixed(1)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

export default function SettlerColonialismLandRightsDashboard() {
  const [raw, setRaw] = useState<DashData | null>(null);
  const [selected, setSelected] = useState<Entity | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");

  useEffect(() => {
    fetch("/api/settler-colonialism-land-rights-engine")
      .then((r) => r.json())
      .then((d) => setRaw(d.payload ?? d))
      .catch(console.error);
  }, []);

  if (!raw) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-yellow-700 text-lg animate-pulse">Initialisation du Moteur Colonialisme de Peuplement &amp; Droits Fonciers...</div>
    </div>
  );

  const entities: Entity[] = raw.entities ?? [];
  const n = entities.length || 1;
  const avgComposite = raw.avg_composite ?? (entities.reduce((s, e) => s + e.composite_score, 0) / n);
  const avgIndex = raw.avg_estimated_land_rights_index ?? (entities.reduce((s, e) => s + e.estimated_land_rights_index, 0) / n);
  const dist: Record<string, number> = raw.risk_distribution ?? {};

  const filtered = entities.filter((e) => riskFilter === "all" || e.risk_level === riskFilter);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-300 p-6 space-y-6">
      {/* Modal */}
      {selected && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4" onClick={() => setSelected(null)}>
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl p-6" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-start justify-between mb-4">
              <div>
                <h2 className="text-lg font-bold text-white">{selected.name}</h2>
                <span className={`text-xs font-semibold uppercase ${RC[selected.risk_level] ?? "text-slate-400"}`}>{selected.risk_level}</span>
              </div>
              <button onClick={() => setSelected(null)} className="text-slate-400 hover:text-white text-2xl leading-none">&times;</button>
            </div>
            <div className="grid grid-cols-2 gap-3 mb-4">
              <div className="bg-slate-800/50 rounded-xl p-4 text-center">
                <div className="text-3xl font-bold" style={{ color: ACCENT }}>{selected.composite_score.toFixed(1)}</div>
                <div className="text-xs text-slate-400 mt-1">Score Composite</div>
              </div>
              <div className="bg-slate-800/50 rounded-xl p-4 text-center">
                <div className="text-3xl font-bold" style={{ color: ACCENT }}>{selected.estimated_land_rights_index.toFixed(2)}</div>
                <div className="text-xs text-slate-400 mt-1">Index Droits Fonciers /10</div>
              </div>
            </div>
            <div className="bg-slate-800/50 rounded-xl p-3">
              <div className="text-xs text-slate-400 mb-1">ID</div>
              <div className="text-white font-mono text-sm">{selected.id}</div>
            </div>
          </div>
        </div>
      )}

      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold" style={{ color: ACCENT }}>Colonialisme de Peuplement &amp; Droits Fonciers</h1>
        <p className="text-slate-400 text-sm mt-1">
          Accaparement Terres · Droits Autochtones · Déplacements Forcés · Restitution Foncière — Intelligence SCL — Caelum Partners
        </p>
        <p className="text-slate-500 text-xs mt-0.5">Chaima Mhadbi — Bruxelles</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          ["Total Entités", entities.length, "text-slate-300"],
          ["Composite Moyen", avgComposite.toFixed(1), "text-yellow-700"],
          ["Index Foncier Moyen", avgIndex.toFixed(2) + "/10", "text-yellow-600"],
          ["Risque Critique", dist["critique"] ?? 0, "text-red-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-yellow-900/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-yellow-900/30 rounded-xl p-5">
        <p className="text-xs text-slate-500 mb-4 font-medium">Distribution des Risques</p>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(dist).map(([level, count]) => (
            <GaugeRing
              key={level}
              value={(count / n) * 100}
              label={`${level} (${count})`}
              color={level === "critique" ? "#ef4444" : level === "élevé" ? "#f97316" : level === "modéré" ? "#eab308" : "#10b981"}
            />
          ))}
        </div>
      </div>

      {/* Risk Distribution Bar */}
      <div className="bg-slate-900 border border-yellow-900/30 rounded-xl p-5">
        <p className="text-xs text-slate-500 mb-3 font-medium">Répartition par Niveau de Risque</p>
        <div className="flex h-3 rounded overflow-hidden gap-px mb-2">
          {Object.entries(dist).map(([level, count]) => (
            <div
              key={level}
              style={{
                width: `${(count / n) * 100}%`,
                background: level === "critique" ? "#ef4444" : level === "élevé" ? "#f97316" : level === "modéré" ? "#eab308" : "#10b981"
              }}
              title={`${level}: ${count}`}
            />
          ))}
        </div>
        <div className="flex flex-wrap gap-x-4 gap-y-1">
          {Object.entries(dist).map(([level, count]) => (
            <span key={level} className="text-xs text-slate-400">
              <span style={{ color: level === "critique" ? "#ef4444" : level === "élevé" ? "#f97316" : level === "modéré" ? "#eab308" : "#10b981" }}>■</span> {level} {count}
            </span>
          ))}
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-2">
        {["all", "critique", "élevé", "modéré", "faible"].map((r) => (
          <button key={r} onClick={() => setRiskFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${riskFilter === r ? "text-white" : "bg-slate-900 text-slate-400 hover:text-white"}`}
            style={riskFilter === r ? { background: ACCENT, borderColor: ACCENT } : { borderColor: "#713f12" }}>
            {r === "all" ? "Tous risques" : r}
          </button>
        ))}
      </div>

      {/* Entity Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map((e) => (
          <div key={e.id} onClick={() => setSelected(e)}
            className={`bg-slate-900 border rounded-xl p-4 cursor-pointer hover:border-yellow-700/50 transition-colors ${RB[e.risk_level] ?? "border-slate-800"}`}>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs text-slate-500 font-mono">{e.id}</span>
              <span className={`text-xs font-semibold uppercase ${RC[e.risk_level] ?? "text-slate-400"}`}>{e.risk_level}</span>
            </div>
            <div className="font-semibold text-white text-sm mb-3 leading-tight">{e.name}</div>
            <div className="flex items-end justify-between">
              <div>
                <div className="text-2xl font-black" style={{ color: ACCENT }}>{e.composite_score.toFixed(1)}</div>
                <div className="text-xs text-slate-500">composite</div>
              </div>
              <div className="text-right">
                <div className="text-lg font-bold text-yellow-600">{e.estimated_land_rights_index.toFixed(2)}</div>
                <div className="text-xs text-slate-500">index /10</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
