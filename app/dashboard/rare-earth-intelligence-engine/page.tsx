"use client";
import { useEffect, useState } from "react";

type Entity = {
  entity_id: string;
  material_category: string;
  region: string;
  supply_score: number;
  geopolitical_score: number;
  demand_score: number;
  resilience_score: number;
  composite_score: number;
  risk_level: string;
  material_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  supply_concentration_monopoly_risk: number;
  export_restriction_weaponization_risk: number;
};

type Summary = {
  module_id: number;
  module_name: string;
  total_entities: number;
  critical_count: number;
  high_count: number;
  moderate_count: number;
  low_count: number;
  avg_composite: number;
  pattern_distribution: Record<string, number>;
  risk_distribution: Record<string, number>;
  severity_distribution: Record<string, number>;
  action_distribution: Record<string, number>;
  avg_estimated_material_risk_index: number;
};

// ── color maps ────────────────────────────────────────────────────────────────
const RISK_COLORS: Record<string, string> = {
  low:      "#10b981",
  moderate: "#f59e0b",
  high:     "#f97316",
  critical: "#ef4444",
};

const RISK_BADGE: Record<string, string> = {
  low:      "bg-emerald-900/60 text-emerald-300 border-emerald-700/50",
  moderate: "bg-amber-900/60 text-amber-300 border-amber-700/50",
  high:     "bg-orange-900/60 text-orange-300 border-orange-700/50",
  critical: "bg-red-950/80 text-red-400 border-red-700/50",
};

const PAT_COLORS: Record<string, string> = {
  none:                       "#10b981",
  rare_earth_monopoly_crisis: "#ef4444",
  export_weapon_deployment:   "#f97316",
  green_tech_material_crunch: "#84cc16",
  conflict_mineral_cascade:   "#a855f7",
  supply_chain_collapse:      "#0ea5e9",
};

const SEV_COLORS: Record<string, string> = {
  "approvisionnement_sous_surveillance":  "#10b981",
  "tension_approvisionnement_critique":   "#f59e0b",
  "pénurie_stratégique_majeure":          "#f97316",
  "crise_matières_critiques_systémique":  "#ef4444",
};

const ACTION_COLORS: Record<string, string> = {
  "veille_matières_critiques_continue":                  "#10b981",
  "renforcement_résilience_chaînes_approvisionnement":   "#f59e0b",
  "diversification_stratégique_accélérée":               "#f97316",
  "sécurisation_urgente_approvisionnements_critiques":   "#ef4444",
};

// ── GaugeRing ─────────────────────────────────────────────────────────────────
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
      <span className="text-xs text-emerald-300/70 text-center leading-tight">{label}</span>
    </div>
  );
}

// ── DistBar ───────────────────────────────────────────────────────────────────
function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-emerald-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] ?? "#475569" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-emerald-300/60">
            <span style={{ color: colors[k] ?? "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

// ── DetailModal ───────────────────────────────────────────────────────────────
function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const ringColor = RISK_COLORS[entity.risk_level] ?? "#64748b";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm" onClick={onClose}>
      <div className="bg-slate-950 border border-emerald-500/30 rounded-2xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-start justify-between mb-4">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <GaugeRing value={entity.composite_score} label="" color={ringColor} />
              <div>
                <span className="text-lg font-bold text-white">{entity.entity_id}</span>
                <div className="flex gap-2 mt-1 flex-wrap">
                  <span className="text-emerald-400 text-xs">{entity.region}</span>
                  <span className="text-slate-500 text-xs">{entity.material_category.replace(/_/g, " ")}</span>
                </div>
                <div className="mt-1">
                  <span className={`px-2 py-0.5 rounded border text-xs font-medium ${RISK_BADGE[entity.risk_level] ?? "bg-slate-700 text-slate-300 border-slate-600"}`}>
                    {entity.risk_level}
                  </span>
                </div>
              </div>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-emerald-900 text-white border border-emerald-700" : "bg-slate-900 text-slate-400 hover:text-white border border-slate-800"}`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Score Approvisionnement", entity.supply_score,       "#10b981"],
              ["Score Géopolitique",      entity.geopolitical_score, "#f97316"],
              ["Score Demande",           entity.demand_score,       "#f59e0b"],
              ["Score Résilience",        entity.resilience_score,   "#0ea5e9"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-900 border border-emerald-500/20 rounded-lg p-3">
                <div className="text-emerald-300/60 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{v.toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(v, 100)}%`, background: c }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-emerald-500/20 rounded-lg p-3">
              <div className="text-emerald-300/60 text-xs mb-1">Score Composite</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="space-y-3">
            <div className="bg-slate-900 border border-emerald-500/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
              {entity.signal}
            </div>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="bg-slate-900 border border-emerald-500/20 rounded-lg p-3">
                <div className="text-emerald-300/60 mb-1">Concentration Monopole</div>
                <div className="text-white font-bold">{Math.round(entity.supply_concentration_monopoly_risk * 100)}%</div>
              </div>
              <div className="bg-slate-900 border border-emerald-500/20 rounded-lg p-3">
                <div className="text-emerald-300/60 mb-1">Arme Export</div>
                <div className="text-white font-bold">{Math.round(entity.export_restriction_weaponization_risk * 100)}%</div>
              </div>
            </div>
            <div className="flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded border text-xs font-medium ${RISK_BADGE[entity.risk_level] ?? "bg-slate-700 text-slate-300 border-slate-600"}`}>
                {entity.risk_level}
              </span>
              <span className="px-2 py-0.5 rounded text-xs bg-slate-800 text-slate-300 border border-slate-700">
                {entity.severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-emerald-900/20 border border-emerald-500/30 rounded-xl p-4">
              <div className="text-emerald-300/60 text-xs uppercase tracking-wide mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-emerald-500/20 rounded-lg p-3">
              <div className="text-emerald-300/60 text-xs mb-1">Pattern Détecté</div>
              <div className="text-white font-medium capitalize">{entity.material_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-emerald-500/20 rounded-lg p-3">
              <div className="text-emerald-300/60 text-xs mb-1">Catégorie Matériau</div>
              <div className="text-white font-medium capitalize">{entity.material_category.replace(/_/g, " ")}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── EntityCard ────────────────────────────────────────────────────────────────
function EntityCard({ entity, onClick }: { entity: Entity; onClick: () => void }) {
  const ringColor = RISK_COLORS[entity.risk_level] ?? "#64748b";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-emerald-500/50 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3 mb-3">
        <GaugeRing value={entity.composite_score} label="" color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-bold truncate">{entity.entity_id}</div>
          <div className="text-slate-400 text-xs">{entity.material_category.replace(/_/g, " ")} · {entity.region}</div>
          <div className="mt-1">
            <span className={`px-2 py-0.5 rounded border text-xs font-medium ${RISK_BADGE[entity.risk_level] ?? "bg-slate-700 text-slate-300 border-slate-600"}`}>
              {entity.risk_level}
            </span>
          </div>
        </div>
      </div>
      <div className="text-xs text-emerald-300/60 mb-1 capitalize">{entity.material_pattern.replace(/_/g, " ")}</div>
      <div className="text-xs text-orange-300/70">
        Appro: {entity.supply_score.toFixed(1)} · Géopol: {entity.geopolitical_score.toFixed(1)} · Demand: {entity.demand_score.toFixed(1)}
      </div>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────
export default function RareEarthIntelligenceDashboard() {
  const [data, setData]       = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filterRisk, setFilterRisk] = useState("all");
  const [filterPattern, setFilterPattern] = useState("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/rare-earth-intelligence-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-emerald-400 text-lg animate-pulse">Initialisation du Moteur Terres Rares & Matières Critiques…</div>
    </div>
  );

  const { entities, summary } = data;

  const filtered = entities.filter(e =>
    (filterRisk === "all" || e.risk_level === filterRisk) &&
    (filterPattern === "all" || e.material_pattern === filterPattern)
  );

  const dists = [
    { title: "Distribution du Risque",      counts: summary.risk_distribution,     colors: RISK_COLORS   },
    { title: "Patterns Matières Critiques",  counts: summary.pattern_distribution,  colors: PAT_COLORS    },
    { title: "Sévérité Approvisionnement",   counts: summary.severity_distribution, colors: SEV_COLORS    },
    { title: "Actions Prescrites",           counts: summary.action_distribution,   colors: ACTION_COLORS },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* header */}
      <div>
        <h1 className="text-2xl font-bold text-emerald-400">
          Terres Rares &amp; Géopolitique Matières Critiques — Module 347
        </h1>
        <p className="text-emerald-300/50 text-sm mt-1">
          Concentration Monopole · Arme Export · Demande GreenTech · Résilience Chaînes d&apos;Approvisionnement
        </p>
      </div>

      {/* KPI Cards — 6 */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Total Matériaux",         summary.total_entities,                               "text-emerald-400"],
          ["Crise Systémique",        summary.critical_count,                               "text-red-400"],
          ["Pénurie Majeure",         summary.high_count,                                   "text-orange-400"],
          ["Composite Moyen",         summary.avg_composite.toFixed(1),                     "text-amber-400"],
          ["Index Risque Matériaux",  summary.avg_estimated_material_risk_index.toFixed(2), "text-orange-300"],
          ["Approvisionnement Moyen", (entities.reduce((s, e) => s + e.supply_score, 0) / (entities.length || 1)).toFixed(1), "text-emerald-300"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={l} className="bg-slate-900 border border-emerald-500/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-emerald-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings — 4 */}
      {(() => {
        const n = entities.length || 1;
        const avgSupply     = entities.reduce((s, e) => s + e.supply_score,      0) / n;
        const avgGeo        = entities.reduce((s, e) => s + e.geopolitical_score, 0) / n;
        const avgDemand     = entities.reduce((s, e) => s + e.demand_score,       0) / n;
        const avgResilience = entities.reduce((s, e) => s + e.resilience_score,   0) / n;
        return (
          <div className="bg-slate-900 border border-emerald-500/30 rounded-xl p-5">
            <div className="text-sm font-semibold text-emerald-300/70 mb-4">Dimensions des Matières Critiques</div>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <GaugeRing value={avgSupply}     label="Approvisionnement" color="#10b981" />
              <GaugeRing value={avgGeo}        label="Géopolitique"      color="#f97316" />
              <GaugeRing value={avgDemand}     label="Demande"           color="#f59e0b" />
              <GaugeRing value={avgResilience} label="Résilience"        color="#0ea5e9" />
            </div>
          </div>
        );
      })()}

      {/* Distribution Bars — 4 */}
      <div className="bg-slate-900 border border-emerald-500/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setFilterRisk(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              filterRisk === r
                ? "bg-emerald-900 border-emerald-700 text-white"
                : "bg-slate-900 border-emerald-500/30 text-emerald-400/70 hover:text-white"
            }`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-emerald-500/30" />
        {["all", "none", "rare_earth_monopoly_crisis", "export_weapon_deployment", "green_tech_material_crunch", "conflict_mineral_cascade", "supply_chain_collapse"].map(p => (
          <button key={p} onClick={() => setFilterPattern(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              filterPattern === p
                ? "bg-emerald-950 border-emerald-700 text-white"
                : "bg-slate-900 border-emerald-500/30 text-emerald-400/70 hover:text-white"
            }`}>
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards */}
      {filtered.length === 0 ? (
        <div className="text-slate-500 text-center py-16">Aucune entité ne correspond aux filtres.</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map(e => (
            <EntityCard key={e.entity_id} entity={e} onClick={() => setSelected(e)} />
          ))}
        </div>
      )}
    </div>
  );
}
