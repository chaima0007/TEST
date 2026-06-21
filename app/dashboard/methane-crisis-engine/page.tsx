"use client";
import { useEffect, useState } from "react";

type MCEEntity = {
  id: string;
  name: string;
  country: string;
  sector: string;
  score1: number;
  score2: number;
  score3: number;
  score4: number;
  composite_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string;
  recommended_action: string;
  estimated_methane_index: number;
  last_updated: string;
};

type MCESummary = {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: Array<{ id: string; name: string; composite_score: number }>;
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: MCEEntity[];
  avg_estimated_methane_index: number;
};

const RISK_COLORS: Record<string, string> = {
  critique: "#ef4444",
  eleve:    "#f97316",
  modere:   "#eab308",
  faible:   "#22c55e",
};

const RISK_LABELS: Record<string, string> = {
  critique: "Critique",
  eleve:    "Élevé",
  modere:   "Modéré",
  faible:   "Faible",
};

function GaugeRing({ value, max = 100, color, label, sub }: {
  value: number; max?: number; color: string; label: string; sub: string;
}) {
  const pct = Math.min(value / max, 1);
  const r = 36;
  const circ = 2 * Math.PI * r;
  const dash = pct * circ;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="96" height="96" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle
          cx="48" cy="48" r={r} fill="none"
          stroke={color} strokeWidth="8"
          strokeDasharray={`${dash} ${circ - dash}`}
          strokeLinecap="round"
          transform="rotate(-90 48 48)"
        />
        <text x="48" y="53" textAnchor="middle" fill="white" fontSize="14" fontWeight="bold">
          {value.toFixed(0)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
      <span className="text-xs text-slate-500 text-center">{sub}</span>
    </div>
  );
}

function DistBar({ label, value, max, color }: { label: string; value: number; max: number; color: string }) {
  const pct = max > 0 ? (value / max) * 100 : 0;
  return (
    <div className="flex items-center gap-2 mb-1">
      <span className="text-xs text-slate-400 w-32 truncate">{label}</span>
      <div className="flex-1 bg-slate-800 rounded h-2">
        <div className="h-2 rounded" style={{ width: `${pct}%`, backgroundColor: color }} />
      </div>
      <span className="text-xs text-slate-300 w-8 text-right">{value}</span>
    </div>
  );
}

function RiskBadge({ level }: { level: string }) {
  return (
    <span
      className="text-xs px-2 py-0.5 rounded-full font-semibold"
      style={{ backgroundColor: RISK_COLORS[level] + "33", color: RISK_COLORS[level], border: `1px solid ${RISK_COLORS[level]}55` }}
    >
      {RISK_LABELS[level] ?? level}
    </span>
  );
}

function DetailModal({ entity, onClose }: { entity: MCEEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");
  const color = RISK_COLORS[entity.risk_level] ?? "#f97316";
  const tabs = [
    { key: "scores",  label: "Scores" },
    { key: "signaux", label: "Signaux" },
    { key: "actions", label: "Actions" },
  ] as const;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-xl p-6 w-full max-w-lg shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-start justify-between mb-4">
          <div>
            <div className="text-xs text-slate-500 mb-1">{entity.id} — {entity.country}</div>
            <div className="text-white font-bold text-lg leading-tight">{entity.name}</div>
            <div className="text-xs text-slate-400 mt-1">{entity.sector}</div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl ml-4">✕</button>
        </div>

        <div className="flex gap-1 mb-4">
          {tabs.map(t => (
            <button
              key={t.key}
              onClick={() => setTab(t.key)}
              className={`px-3 py-1.5 rounded text-xs font-semibold transition-colors ${
                tab === t.key
                  ? "text-white"
                  : "text-slate-400 hover:text-slate-200 bg-slate-800"
              }`}
              style={tab === t.key ? { backgroundColor: color } : {}}
            >
              {t.label}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-4">
            <GaugeRing value={entity.score1} color="#f97316" label="Intensité Émission" sub="score 1" />
            <GaugeRing value={entity.score2} color="#ea580c" label="Gap Détection Fuites" sub="score 2" />
            <GaugeRing value={entity.score3} color="#c2410c" label="Gap Réglementaire" sub="score 3" />
            <GaugeRing value={entity.score4} color="#9a3412" label="Risque Rétroaction" sub="score 4" />
            <div className="col-span-2 flex justify-center">
              <GaugeRing value={entity.composite_score} color={color} label="Score Composite" sub="global" />
            </div>
          </div>
        )}

        {tab === "signaux" && (
          <div className="space-y-3">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-xs text-slate-400 mb-1">Signaux clés</div>
              <div className="text-sm text-slate-200">{entity.key_signals}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-xs text-slate-400 mb-1">Patron primaire</div>
              <div className="text-sm text-slate-200 font-mono">{entity.primary_pattern}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-xs text-slate-400 mb-1">Indice Méthane</div>
              <div className="text-sm text-slate-200 font-bold">{entity.estimated_methane_index.toFixed(2)}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-xs text-slate-400 mb-1">Niveau de risque</div>
              <RiskBadge level={entity.risk_level} />
            </div>
          </div>
        )}

        {tab === "actions" && (
          <div className="space-y-3">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-xs text-slate-400 mb-1">Action recommandée</div>
              <div className="text-sm text-slate-200 font-mono">{entity.recommended_action}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-xs text-slate-400 mb-1">Dernière analyse</div>
              <div className="text-xs text-slate-300">{new Date(entity.last_updated).toLocaleString("fr-FR")}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function MethaneCrisisDashboard() {
  const [data, setData] = useState<MCESummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>("tous");
  const [selected, setSelected] = useState<MCEEntity | null>(null);

  useEffect(() => {
    fetch("/api/methane-crisis-engine")
      .then(r => r.json())
      .then(j => {
        setData(j);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-400 text-lg">Chargement Methane Crisis Engine…</div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-red-400 text-lg">Erreur de chargement des données</div>
      </div>
    );
  }

  const filterPills = ["tous", "critique", "eleve", "modere", "faible"];
  const filtered = filter === "tous"
    ? data.entities
    : data.entities.filter(e => e.risk_level === filter);

  const maxPattern = Math.max(...Object.values(data.pattern_distribution), 1);

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="mb-8">
        <div className="text-xs text-orange-400 font-mono mb-1">MODULE 345 — CAELUM PARTNERS</div>
        <h1 className="text-3xl font-bold text-white mb-2">
          Methane Crisis & Arctic Methane Bomb Intelligence Engine
        </h1>
        <div className="text-slate-400 text-sm">
          Crise Méthane & Bombe Méthane Arctique — v{data.engine_version}
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
        <div className="bg-slate-900 border border-slate-700 rounded-xl p-4">
          <div className="text-xs text-slate-400 mb-1">Entités</div>
          <div className="text-2xl font-bold text-white">{data.total_entities}</div>
        </div>
        <div className="bg-slate-900 border border-red-900 rounded-xl p-4">
          <div className="text-xs text-red-400 mb-1">Critique</div>
          <div className="text-2xl font-bold text-red-400">{data.risk_distribution["critique"] ?? 0}</div>
        </div>
        <div className="bg-slate-900 border border-orange-900 rounded-xl p-4">
          <div className="text-xs text-orange-400 mb-1">Élevé</div>
          <div className="text-2xl font-bold text-orange-400">{data.risk_distribution["eleve"] ?? 0}</div>
        </div>
        <div className="bg-slate-900 border border-yellow-900 rounded-xl p-4">
          <div className="text-xs text-yellow-400 mb-1">Modéré</div>
          <div className="text-2xl font-bold text-yellow-400">{data.risk_distribution["modere"] ?? 0}</div>
        </div>
        <div className="bg-slate-900 border border-slate-700 rounded-xl p-4">
          <div className="text-xs text-slate-400 mb-1">Composite Moy.</div>
          <div className="text-2xl font-bold text-orange-400">{data.avg_composite.toFixed(1)}</div>
        </div>
        <div className="bg-slate-900 border border-slate-700 rounded-xl p-4">
          <div className="text-xs text-slate-400 mb-1">Idx Méthane</div>
          <div className="text-2xl font-bold text-orange-300">{data.avg_estimated_methane_index.toFixed(2)}</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* Pattern Distribution */}
        <div className="bg-slate-900 border border-slate-700 rounded-xl p-5">
          <div className="text-sm font-semibold text-slate-300 mb-4">Distribution des Patrons</div>
          {Object.entries(data.pattern_distribution).map(([pat, cnt]) => (
            <DistBar key={pat} label={pat.replace(/_/g, " ")} value={cnt} max={maxPattern} color="#f97316" />
          ))}
        </div>

        {/* Critical Alerts */}
        <div className="bg-slate-900 border border-red-900/50 rounded-xl p-5 lg:col-span-2">
          <div className="text-sm font-semibold text-red-400 mb-4">Alertes Critiques</div>
          {data.critical_alerts.length === 0 ? (
            <div className="text-slate-500 text-sm">Aucune alerte critique</div>
          ) : (
            <div className="space-y-2">
              {data.critical_alerts.map((alert, i) => (
                <div key={i} className="bg-red-950/30 border border-red-900/50 rounded-lg p-3 text-sm text-red-200">
                  {alert}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Filter Pills */}
      <div className="flex gap-2 mb-4 flex-wrap">
        {filterPills.map(f => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-3 py-1.5 rounded-full text-xs font-semibold transition-colors ${
              filter === f
                ? "bg-orange-600 text-white"
                : "bg-slate-800 text-slate-400 hover:bg-slate-700"
            }`}
          >
            {f === "tous" ? "Tous" : RISK_LABELS[f]}
            {f !== "tous" && data.risk_distribution[f] !== undefined && (
              <span className="ml-1 opacity-70">({data.risk_distribution[f]})</span>
            )}
          </button>
        ))}
      </div>

      {/* Entity Table */}
      <div className="bg-slate-900 border border-slate-700 rounded-xl overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-700 bg-slate-800/50">
              <th className="text-left p-4 text-slate-400 font-medium">ID</th>
              <th className="text-left p-4 text-slate-400 font-medium">Entité</th>
              <th className="text-left p-4 text-slate-400 font-medium">Pays</th>
              <th className="text-left p-4 text-slate-400 font-medium">Risque</th>
              <th className="text-left p-4 text-slate-400 font-medium">Composite</th>
              <th className="text-left p-4 text-slate-400 font-medium">Patron</th>
              <th className="text-left p-4 text-slate-400 font-medium">Action</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((e, i) => (
              <tr
                key={e.id}
                className={`border-b border-slate-800 cursor-pointer hover:bg-slate-800/50 transition-colors ${
                  i % 2 === 0 ? "" : "bg-slate-900/50"
                }`}
                onClick={() => setSelected(e)}
              >
                <td className="p-4 font-mono text-xs text-slate-500">{e.id}</td>
                <td className="p-4">
                  <div className="font-medium text-white">{e.name}</div>
                  <div className="text-xs text-slate-500">{e.sector}</div>
                </td>
                <td className="p-4 text-slate-300">{e.country}</td>
                <td className="p-4"><RiskBadge level={e.risk_level} /></td>
                <td className="p-4">
                  <div className="font-bold" style={{ color: RISK_COLORS[e.risk_level] }}>
                    {e.composite_score.toFixed(1)}
                  </div>
                </td>
                <td className="p-4 font-mono text-xs text-slate-400">{e.primary_pattern}</td>
                <td className="p-4 text-xs text-slate-500 max-w-xs truncate">{e.recommended_action}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Footer */}
      <div className="mt-6 flex items-center justify-between text-xs text-slate-500">
        <div>Sources: {data.data_sources.join(", ")}</div>
        <div>Confiance: {(data.confidence_score * 100).toFixed(0)}% — {new Date(data.last_analysis).toLocaleString("fr-FR")}</div>
      </div>
    </div>
  );
}
