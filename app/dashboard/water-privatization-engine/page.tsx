"use client";
import { useEffect, useState } from "react";

// Water Privatization & Bien Commun Hydrique — Caelum Partners

type RiskLevel = "critique" | "élevé" | "modéré" | "faible";

interface WPEEntity {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  score1: number;
  score2: number;
  score3: number;
  score4: number;
  risk_level: RiskLevel;
  primary_pattern: string;
  key_signals: string;
  estimated_water_index: number;
  last_updated: string;
}

interface WPESummary {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: WPEEntity[];
  avg_estimated_water_index: number;
}

const ACCENT = "#3b82f6";

const RISK_META: Record<RiskLevel, { label: string; badge: string; color: string }> = {
  critique: { label: "Critique", badge: "bg-red-900/60 text-red-300 border border-red-700",         color: "#ef4444" },
  élevé:    { label: "Élevé",    badge: "bg-orange-900/60 text-orange-300 border border-orange-700", color: "#f97316" },
  modéré:   { label: "Modéré",   badge: "bg-amber-900/60 text-amber-300 border border-amber-700",   color: "#f59e0b" },
  faible:   { label: "Faible",   badge: "bg-emerald-900/60 text-emerald-300 border border-emerald-700", color: "#10b981" },
};

const RISK_COLORS: Record<string, string> = {
  critique: "#ef4444", élevé: "#f97316", modéré: "#f59e0b", faible: "#10b981",
};

const PAT_COLORS: Record<string, string> = {
  corporate_water_monopoly:      "#ef4444",
  affordability_crisis_collapse: "#f97316",
  community_access_denial:       "#a855f7",
  regulatory_capture_spiral:     "#3b82f6",
  water_commons_erosion:         "#f59e0b",
  none:                          "#10b981",
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0f172a" strokeWidth="8" />
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)" />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-blue-400/70 text-center leading-tight">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-blue-400/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${v / total * 100}%`, background: colors[k] || "#1e3a5f" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-blue-400/60">
            <span style={{ color: colors[k] || "#3b82f6" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

function DetailModal({ entity, onClose }: { entity: WPEEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");
  const meta = RISK_META[entity.risk_level];

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75" onClick={onClose}>
      <div className="bg-slate-900 border border-blue-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.name}</span>
            <span className="ml-2 text-blue-400 text-xs">{entity.country}</span>
            <span className="ml-2 text-slate-400 text-xs">{entity.sector}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signaux", "actions"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-blue-800 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signaux" ? "Signaux" : "Actions"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Pression Privatisation (×0.30)", entity.score1, "#3b82f6"],
              ["Inégalité Accès (×0.25)",        entity.score2, "#f97316"],
              ["Contrôle Corporatif (×0.25)",    entity.score3, "#a855f7"],
              ["Gap Réglementation (×0.20)",     entity.score4, "#10b981"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-800 border border-blue-700/20 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{v.toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(v, 100)}%`, background: c }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 border border-blue-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Score Composite</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signaux" && (
          <div className="bg-slate-800 border border-blue-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.key_signals}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${meta?.badge || "bg-slate-700 text-slate-300"}`}>
                {meta?.label || entity.risk_level}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-blue-300">
                {entity.primary_pattern.replace(/_/g, " ")}
              </span>
            </div>
            <div className="mt-3 grid grid-cols-2 gap-2 text-xs text-slate-400">
              <div>Index Eau: <span className="text-blue-300">{entity.estimated_water_index.toFixed(2)}/10</span></div>
              <div>Dernière Analyse: <span className="text-blue-300">{entity.last_updated}</span></div>
            </div>
          </div>
        )}

        {tab === "actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 border border-blue-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Niveau de Risque</div>
              <div className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${meta?.badge || "bg-slate-700 text-slate-300"}`}>
                {meta?.label || entity.risk_level}
              </div>
            </div>
            <div className="bg-slate-800 border border-blue-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Patron Primaire Détecté</div>
              <div className="text-white font-medium capitalize">{entity.primary_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 border border-blue-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Index Privatisation Eau</div>
              <div className="font-bold text-xl" style={{ color: ACCENT }}>{entity.estimated_water_index.toFixed(2)} <span className="text-xs text-slate-400">/ 10</span></div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function WaterPrivatizationDashboard() {
  const [data, setData] = useState<WPESummary | null>(null);
  const [riskFilter, setRisk] = useState<string>("tous");
  const [selected, setSelected] = useState<WPEEntity | null>(null);

  useEffect(() => {
    fetch("/api/water-privatization-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="animate-pulse" style={{ color: ACCENT }}>Initialisation Moteur Privatisation Eau — Caelum Partners...</div>
    </div>
  );

  const entities = data.entities ?? [];
  const filtered = entities.filter(e => riskFilter === "tous" || e.risk_level === riskFilter);

  const n = entities.length || 1;
  const avgS1 = entities.reduce((s, e) => s + e.score1, 0) / n;
  const avgS2 = entities.reduce((s, e) => s + e.score2, 0) / n;
  const avgS3 = entities.reduce((s, e) => s + e.score3, 0) / n;
  const avgS4 = entities.reduce((s, e) => s + e.score4, 0) / n;

  const critCount = data.risk_distribution["critique"] || 0;
  const elevCount = data.risk_distribution["élevé"] || 0;

  const dists = [
    { title: "Niveau de Risque", counts: data.risk_distribution,    colors: RISK_COLORS },
    { title: "Patron Hydrique",  counts: data.pattern_distribution, colors: PAT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-300 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold" style={{ color: ACCENT }}>
          Privatisation Eau &amp; Bien Commun Hydrique
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Pression Privatisation · Inégalité Accès · Contrôle Corporatif · Réglementation — Caelum Partners
        </p>
        <p className="text-slate-500 text-xs mt-0.5">Chaima Mhadbi — Bruxelles</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Total Entités",     data.total_entities,                               "text-slate-300"],
          ["Critique",          critCount,                                          "text-red-400"],
          ["Élevé",             elevCount,                                          "text-orange-400"],
          ["Composite Moyen",   data.avg_composite.toFixed(1),                     "text-blue-300"],
          ["Index Eau Moy.",    data.avg_estimated_water_index.toFixed(2) + "/10", "text-blue-400"],
          ["Confiance Moteur",  (data.confidence_score * 100).toFixed(0) + "%",    "text-sky-400"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-blue-800/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-blue-800/30 rounded-xl p-5">
        <p className="text-xs text-slate-500 mb-4 font-medium">Scores Moyens par Dimension</p>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgS1} label="Privatisation (×0.30)"   color="#3b82f6" />
          <GaugeRing value={avgS2} label="Inégalité Accès (×0.25)" color="#f97316" />
          <GaugeRing value={avgS3} label="Contrôle Corp. (×0.25)"  color="#a855f7" />
          <GaugeRing value={avgS4} label="Gap Réglem. (×0.20)"     color="#10b981" />
        </div>
      </div>

      <div className="bg-slate-900 border border-blue-800/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
        <div className="flex flex-col gap-1">
          <span className="text-xs text-slate-400 font-medium">Sources de Données</span>
          {data.data_sources.map(s => (
            <span key={s} className="text-xs text-slate-500">• {s}</span>
          ))}
        </div>
        <div className="flex flex-col gap-1">
          <span className="text-xs text-slate-400 font-medium">Alertes Critiques</span>
          {data.critical_alerts.length === 0
            ? <span className="text-xs text-emerald-400">Aucune alerte critique</span>
            : data.critical_alerts.map(a => <span key={a} className="text-xs text-red-400 truncate">• {a}</span>)
          }
        </div>
      </div>

      <div className="flex flex-wrap gap-2">
        {["tous", "critique", "élevé", "modéré", "faible"].map(r => (
          <button key={r} onClick={() => setRisk(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              riskFilter === r
                ? "bg-blue-800 border-blue-700 text-white"
                : "bg-slate-900 border-blue-800/30 text-slate-400 hover:text-white"
            }`}>
            {r === "tous" ? "Tous" : r.charAt(0).toUpperCase() + r.slice(1)}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => {
          const meta = RISK_META[e.risk_level];
          return (
            <div key={e.id} onClick={() => setSelected(e)}
              className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-blue-700/50 transition-colors">
              <div className="flex items-center justify-between mb-1">
                <span className="font-bold text-white">{e.name}</span>
                <span className="text-xs text-slate-400">{e.country}</span>
              </div>
              <div className="text-xs text-blue-400 mb-2">{e.sector}</div>
              <div className="flex gap-1 mb-3 flex-wrap">
                <span className={`px-2 py-0.5 rounded text-xs font-medium ${meta?.badge || "bg-slate-700 text-slate-300"}`}>
                  {meta?.label || e.risk_level}
                </span>
              </div>
              <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
              <div className="text-xs text-slate-500 mb-2 capitalize">{e.primary_pattern.replace(/_/g, " ")}</div>
              <div className="text-xs text-blue-400 truncate">{e.key_signals}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
