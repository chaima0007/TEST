"use client";
import { useEffect, useState } from "react";

type Entity = {
  entity_id: string;
  ip_domain: string;
  region: string;
  theft_score: number;
  monopoly_score: number;
  access_score: number;
  geopolitical_score: number;
  composite_score: number;
  risk_level: string;
  patterns_detected: string[];
  severity: string;
  action_required: string;
  signal: string;
  estimated_ip_warfare_index: number;
  metadata: {
    state_IP_theft_intensity: number;
    geopolitical_IP_weaponization: number;
    pharmaceutical_evergreening: number;
  };
};

type Summary = {
  module_id: number;
  module_name: string;
  total: number;
  critical: number;
  high: number;
  moderate: number;
  low: number;
  avg_composite: number;
  distributions: {
    risk: Record<string, number>;
    pattern: Record<string, number>;
  };
  avg_estimated_ip_warfare_index: number;
  theft_avg: number;
  monopoly_avg: number;
  access_avg: number;
};

// ── color maps ─────────────────────────────────────────────────────────────────
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
  state_IP_espionage_campaign:   "#ef4444",
  patent_monopoly_capture:       "#a855f7",
  pharmaceutical_access_blockade:"#f97316",
  geopolitical_IP_warfare:       "#0ea5e9",
  global_south_IP_exclusion:     "#84cc16",
};

// ── GaugeRing ──────────────────────────────────────────────────────────────────
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
      <span className="text-xs text-indigo-300/70 text-center leading-tight">{label}</span>
    </div>
  );
}

// ── DistBar ───────────────────────────────────────────────────────────────────
function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-indigo-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] ?? "#475569" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-indigo-300/60">
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
      <div className="bg-slate-950 border border-indigo-500/30 rounded-2xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-start justify-between mb-4">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <GaugeRing value={entity.composite_score} label="" color={ringColor} />
              <div>
                <span className="text-lg font-bold text-white">{entity.entity_id}</span>
                <div className="flex gap-2 mt-1 flex-wrap">
                  <span className="text-indigo-400 text-xs">{entity.region}</span>
                  <span className="text-slate-500 text-xs">{entity.ip_domain.replace(/_/g, " ")}</span>
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
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-indigo-900 text-white border border-indigo-700" : "bg-slate-900 text-slate-400 hover:text-white border border-slate-800"}`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Score Vol IP",       entity.theft_score,       "#ef4444"],
              ["Score Monopole",     entity.monopoly_score,    "#a855f7"],
              ["Score Accès",        entity.access_score,      "#f59e0b"],
              ["Score Géopolitique", entity.geopolitical_score, "#0ea5e9"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-900 border border-indigo-500/20 rounded-lg p-3">
                <div className="text-indigo-300/60 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{v.toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(v, 100)}%`, background: c }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-indigo-500/20 rounded-lg p-3">
              <div className="text-indigo-300/60 text-xs mb-1">Score Composite</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="space-y-3">
            <div className="bg-slate-900 border border-indigo-500/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
              {entity.signal}
            </div>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="bg-slate-900 border border-indigo-500/20 rounded-lg p-3">
                <div className="text-indigo-300/60 mb-1">Vol IP d&apos;État</div>
                <div className="text-white font-bold">{Math.round(entity.metadata.state_IP_theft_intensity * 100)}%</div>
              </div>
              <div className="bg-slate-900 border border-indigo-500/20 rounded-lg p-3">
                <div className="text-indigo-300/60 mb-1">Arme Géopolitique IP</div>
                <div className="text-white font-bold">{Math.round(entity.metadata.geopolitical_IP_weaponization * 100)}%</div>
              </div>
              <div className="bg-slate-900 border border-indigo-500/20 rounded-lg p-3">
                <div className="text-indigo-300/60 mb-1">Evergreening Pharma</div>
                <div className="text-white font-bold">{Math.round(entity.metadata.pharmaceutical_evergreening * 100)}%</div>
              </div>
              <div className="bg-slate-900 border border-indigo-500/20 rounded-lg p-3">
                <div className="text-indigo-300/60 mb-1">Index Guerre IP</div>
                <div className="text-white font-bold">{entity.estimated_ip_warfare_index.toFixed(2)}</div>
              </div>
            </div>
            <div className="flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded border text-xs font-medium ${RISK_BADGE[entity.risk_level] ?? "bg-slate-700 text-slate-300 border-slate-600"}`}>
                {entity.risk_level}
              </span>
              <span className="px-2 py-0.5 rounded text-xs bg-slate-800 text-slate-300 border border-slate-700">
                {entity.severity}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-indigo-900/20 border border-indigo-500/30 rounded-xl p-4">
              <div className="text-indigo-300/60 text-xs uppercase tracking-wide mb-1">Action Requise</div>
              <div className="text-white font-medium">{entity.action_required}</div>
            </div>
            <div className="bg-slate-900 border border-indigo-500/20 rounded-lg p-3">
              <div className="text-indigo-300/60 text-xs mb-1">Patterns Détectés</div>
              {entity.patterns_detected.length === 0 ? (
                <div className="text-slate-400 text-xs">Aucun pattern critique</div>
              ) : (
                <div className="flex flex-wrap gap-1 mt-1">
                  {entity.patterns_detected.map(p => (
                    <span key={p} className="px-2 py-0.5 rounded text-xs font-medium border"
                      style={{ borderColor: PAT_COLORS[p] ?? "#475569", color: PAT_COLORS[p] ?? "#94a3b8", background: "rgba(0,0,0,0.3)" }}>
                      {p.replace(/_/g, " ")}
                    </span>
                  ))}
                </div>
              )}
            </div>
            <div className="bg-slate-900 border border-indigo-500/20 rounded-lg p-3">
              <div className="text-indigo-300/60 text-xs mb-1">Domaine IP</div>
              <div className="text-white font-medium capitalize">{entity.ip_domain.replace(/_/g, " ")}</div>
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
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-indigo-500/50 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3 mb-3">
        <GaugeRing value={entity.composite_score} label="" color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-bold truncate">{entity.entity_id}</div>
          <div className="text-slate-400 text-xs">{entity.ip_domain.replace(/_/g, " ")} · {entity.region}</div>
          <div className="mt-1">
            <span className={`px-2 py-0.5 rounded border text-xs font-medium ${RISK_BADGE[entity.risk_level] ?? "bg-slate-700 text-slate-300 border-slate-600"}`}>
              {entity.risk_level}
            </span>
          </div>
        </div>
      </div>
      {entity.patterns_detected.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-2">
          {entity.patterns_detected.map(p => (
            <span key={p} className="text-xs px-1.5 py-0.5 rounded"
              style={{ background: `${PAT_COLORS[p] ?? "#475569"}22`, color: PAT_COLORS[p] ?? "#94a3b8", border: `1px solid ${PAT_COLORS[p] ?? "#475569"}44` }}>
              {p.replace(/_/g, " ")}
            </span>
          ))}
        </div>
      )}
      <div className="text-xs text-amber-300/70">
        Vol: {entity.theft_score.toFixed(1)} · Monopole: {entity.monopoly_score.toFixed(1)} · Accès: {entity.access_score.toFixed(1)}
      </div>
    </div>
  );
}

// ── ALL_PATTERNS constant ─────────────────────────────────────────────────────
const ALL_PATTERNS = [
  "state_IP_espionage_campaign",
  "patent_monopoly_capture",
  "pharmaceutical_access_blockade",
  "geopolitical_IP_warfare",
  "global_south_IP_exclusion",
];

// ── Page ──────────────────────────────────────────────────────────────────────
export default function IPWarfareDashboard() {
  const [data, setData]             = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filterRisk, setFilterRisk] = useState("all");
  const [filterPattern, setFilterPattern] = useState("all");
  const [selected, setSelected]     = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/ip-warfare-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-indigo-400 text-lg animate-pulse">Initialisation du Moteur Guerre IP &amp; Brevets…</div>
    </div>
  );

  const { entities, summary } = data;

  const filtered = entities.filter(e =>
    (filterRisk === "all" || e.risk_level === filterRisk) &&
    (filterPattern === "all" || e.patterns_detected.includes(filterPattern))
  );

  const espionageCount = entities.filter(e => e.patterns_detected.includes("state_IP_espionage_campaign")).length;

  const n = entities.length || 1;
  const avgTheft       = entities.reduce((s, e) => s + e.theft_score,       0) / n;
  const avgMonopoly    = entities.reduce((s, e) => s + e.monopoly_score,    0) / n;
  const avgAccess      = entities.reduce((s, e) => s + e.access_score,      0) / n;
  const avgGeopolitical= entities.reduce((s, e) => s + e.geopolitical_score, 0) / n;

  const dists = [
    {
      title: "Distribution du Risque",
      counts: summary.distributions.risk,
      colors: RISK_COLORS,
    },
    {
      title: "Patterns IP Détectés",
      counts: summary.distributions.pattern,
      colors: PAT_COLORS,
    },
    {
      title: "Vol vs Monopole vs Accès",
      counts: {
        "Vol IP":  Math.round(avgTheft),
        "Monopole": Math.round(avgMonopoly),
        "Accès":   Math.round(avgAccess),
      },
      colors: { "Vol IP": "#ef4444", "Monopole": "#a855f7", "Accès": "#f59e0b" },
    },
    {
      title: "Répartition Géopolitique",
      counts: summary.distributions.risk,
      colors: RISK_COLORS,
    },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* header */}
      <div>
        <h1 className="text-2xl font-bold text-indigo-400">
          Guerre de la Propriété Intellectuelle — Module 389
        </h1>
        <p className="text-indigo-300/50 text-sm mt-1">
          Vol IP · Monopoles Brevets · Blocage d&apos;Accès · Guerre Géopolitique IP
        </p>
      </div>

      {/* KPI Cards — 6 */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Total Domaines",      summary.total,                                           "text-indigo-400"],
          ["Espionnage IP",       espionageCount,                                          "text-red-400"],
          ["Crise Majeure",       summary.critical,                                        "text-red-400"],
          ["Composite Moyen",     summary.avg_composite.toFixed(1),                        "text-amber-400"],
          ["Index Guerre IP",     summary.avg_estimated_ip_warfare_index.toFixed(2),       "text-orange-300"],
          ["Vol Moyen",           summary.theft_avg.toFixed(1),                            "text-rose-400"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={l} className="bg-slate-900 border border-indigo-500/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-indigo-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings — 4 */}
      <div className="bg-slate-900 border border-indigo-500/30 rounded-xl p-5">
        <div className="text-sm font-semibold text-indigo-300/70 mb-4">Dimensions de la Guerre IP</div>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <GaugeRing value={avgTheft}        label="Vol"         color="#ef4444" />
          <GaugeRing value={avgMonopoly}     label="Monopole"    color="#a855f7" />
          <GaugeRing value={avgAccess}       label="Accès"       color="#f59e0b" />
          <GaugeRing value={avgGeopolitical} label="Géopolitique" color="#0ea5e9" />
        </div>
      </div>

      {/* Distribution Bars — 4 */}
      <div className="bg-slate-900 border border-indigo-500/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setFilterRisk(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              filterRisk === r
                ? "bg-indigo-900 border-indigo-700 text-white"
                : "bg-slate-900 border-indigo-500/30 text-indigo-400/70 hover:text-white"
            }`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-indigo-500/30" />
        {["all", ...ALL_PATTERNS].map(p => (
          <button key={p} onClick={() => setFilterPattern(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              filterPattern === p
                ? "bg-indigo-950 border-indigo-700 text-white"
                : "bg-slate-900 border-indigo-500/30 text-indigo-400/70 hover:text-white"
            }`}>
            {p === "all" ? "all" : p.replace(/_/g, " ")}
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
