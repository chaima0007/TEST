"use client";

import { useState, useEffect, useRef } from "react";

interface CompetitorResult {
  competitor_id: string;
  competitor_name: string;
  competitor_type: string;
  threat_score: number;
  threat_level: string;
  market_score: number;
  product_score: number;
  gtm_score: number;
  weakness_score: number;
  recommended_action: string;
  win_probability_vs_this: number;
  threat_signals: string[];
  opportunity_signals: string[];
  battle_card_tips: string[];
}

interface Summary {
  total: number;
  level_counts: Record<string, number>;
  type_counts: Record<string, number>;
  avg_threat_score: number;
  avg_win_probability: number;
}

const LEVEL_TABS = [
  { key: "all", label: "Tous" },
  { key: "critical", label: "Critique" },
  { key: "high", label: "Élevé" },
  { key: "medium", label: "Moyen" },
  { key: "low", label: "Faible" },
  { key: "minimal", label: "Minimal" },
];

const LEVEL_COLORS: Record<string, string> = {
  critical: "#ef4444",
  high: "#f97316",
  medium: "#f59e0b",
  low: "#6366f1",
  minimal: "#64748b",
};

const LEVEL_BG: Record<string, string> = {
  critical: "bg-red-500/10 text-red-400 border-red-500/30",
  high: "bg-orange-500/10 text-orange-400 border-orange-500/30",
  medium: "bg-amber-500/10 text-amber-400 border-amber-500/30",
  low: "bg-indigo-500/10 text-indigo-400 border-indigo-500/30",
  minimal: "bg-slate-500/10 text-slate-400 border-slate-500/30",
};

const LEVEL_LABELS: Record<string, string> = {
  critical: "Critique",
  high: "Élevé",
  medium: "Moyen",
  low: "Faible",
  minimal: "Minimal",
};

const TYPE_LABELS: Record<string, string> = {
  direct: "Direct",
  indirect: "Indirect",
  emerging: "Émergent",
  legacy: "Legacy",
  niche: "Niche",
};

const ACTION_LABELS: Record<string, string> = {
  preempt: "Préempter",
  respond: "Répondre",
  differentiate: "Différencier",
  monitor: "Surveiller",
  ignore: "Ignorer",
};

const ACTION_COLORS: Record<string, string> = {
  preempt: "bg-red-500/10 text-red-400",
  respond: "bg-orange-500/10 text-orange-400",
  differentiate: "bg-indigo-500/10 text-indigo-400",
  monitor: "bg-slate-700 text-slate-300",
  ignore: "bg-slate-800 text-slate-500",
};

function ThreatRing({ score, level }: { score: number; level: string }) {
  const r = 28;
  const circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  const color = LEVEL_COLORS[level] || "#6366f1";

  return (
    <svg width="72" height="72" viewBox="0 0 72 72" className="shrink-0">
      <circle cx="36" cy="36" r={r} fill="none" stroke="#1e293b" strokeWidth="6" />
      <circle
        cx="36"
        cy="36"
        r={r}
        fill="none"
        stroke={color}
        strokeWidth="6"
        strokeDasharray={`${fill} ${circ - fill}`}
        strokeLinecap="round"
        transform="rotate(-90 36 36)"
      />
      <text x="36" y="40" textAnchor="middle" fontSize="13" fontWeight="700" fill={color}>
        {Math.round(score)}
      </text>
    </svg>
  );
}

function ScoreBar({ label, value }: { label: string; value: number }) {
  const color =
    value >= 75 ? "#ef4444" : value >= 55 ? "#f97316" : value >= 35 ? "#f59e0b" : "#22c55e";
  return (
    <div className="flex flex-col gap-1">
      <div className="flex justify-between text-xs text-slate-400">
        <span>{label}</span>
        <span className="font-semibold" style={{ color }}>
          {Math.round(value)}
        </span>
      </div>
      <div className="h-1.5 rounded-full bg-slate-800 overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{ width: `${value}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
}

function CompetitorModal({ comp, onClose }: { comp: CompetitorResult; onClose: () => void }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) onClose();
    };
    setTimeout(() => window.addEventListener("mousedown", handler), 0);
    return () => window.removeEventListener("mousedown", handler);
  }, [onClose]);

  const levelColor = LEVEL_COLORS[comp.threat_level] || "#6366f1";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div
        ref={ref}
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto"
      >
        <div className="p-6 border-b border-slate-800 flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 flex-wrap">
              <h2 className="text-xl font-bold text-slate-100">{comp.competitor_name}</h2>
              <span
                className={`text-xs px-2 py-0.5 rounded-full border font-medium ${LEVEL_BG[comp.threat_level]}`}
              >
                {LEVEL_LABELS[comp.threat_level]}
              </span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 font-medium">
                {TYPE_LABELS[comp.competitor_type] ?? comp.competitor_type}
              </span>
            </div>
            <p className="text-sm text-slate-400 mt-1">
              Action recommandée :{" "}
              <span className={`font-semibold`} style={{ color: levelColor }}>
                {ACTION_LABELS[comp.recommended_action] ?? comp.recommended_action}
              </span>
            </p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200 text-xl shrink-0">
            ✕
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* KPIs */}
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            {[
              {
                label: "Score menace",
                value: `${comp.threat_score.toFixed(1)}/100`,
                color: comp.threat_score >= 70 ? "text-red-400" : comp.threat_score >= 50 ? "text-amber-400" : "text-green-400",
              },
              {
                label: "Prob. victoire nôtre",
                value: `${comp.win_probability_vs_this.toFixed(0)}%`,
                color: comp.win_probability_vs_this >= 55 ? "text-green-400" : comp.win_probability_vs_this >= 35 ? "text-amber-400" : "text-red-400",
              },
              {
                label: "Forces identifiées",
                value: `${comp.threat_signals.length} signaux`,
                color: "text-slate-300",
              },
            ].map((kpi) => (
              <div key={kpi.label} className="bg-slate-800/50 rounded-xl p-3 text-center">
                <div className={`text-xl font-bold ${kpi.color}`}>{kpi.value}</div>
                <div className="text-xs text-slate-400 mt-0.5">{kpi.label}</div>
              </div>
            ))}
          </div>

          {/* Threat ring + weakness */}
          <div className="flex items-center gap-6 bg-slate-800/30 rounded-xl p-4">
            <ThreatRing score={comp.threat_score} level={comp.threat_level} />
            <div className="flex-1 min-w-0">
              <div className="flex items-baseline gap-2 mb-2">
                <span className="text-2xl font-bold" style={{ color: levelColor }}>
                  {comp.threat_score.toFixed(1)}
                </span>
                <span className="text-sm text-slate-400">/ 100 — menace concurrentielle</span>
              </div>
              <div className="text-xs text-slate-400">
                Faiblesses détectées :{" "}
                <span className="text-green-400 font-semibold">
                  {comp.weakness_score.toFixed(0)}/100
                </span>
              </div>
              <div className="text-xs text-slate-400 mt-1">
                Opportunités exploitables : {comp.opportunity_signals.length}
              </div>
            </div>
          </div>

          {/* Score dimensions */}
          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-slate-300">Dimensions de menace</h3>
            <ScoreBar label="Présence marché" value={comp.market_score} />
            <ScoreBar label="Menace produit" value={comp.product_score} />
            <ScoreBar label="GTM & Ventes" value={comp.gtm_score} />
          </div>

          {/* Win probability bar */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-2">Probabilité de victoire face à eux</h3>
            <div className="flex items-center gap-3">
              <div className="flex-1 h-3 rounded-full bg-slate-800 overflow-hidden">
                <div
                  className="h-full rounded-full transition-all"
                  style={{
                    width: `${comp.win_probability_vs_this}%`,
                    backgroundColor:
                      comp.win_probability_vs_this >= 55
                        ? "#22c55e"
                        : comp.win_probability_vs_this >= 35
                        ? "#f59e0b"
                        : "#ef4444",
                  }}
                />
              </div>
              <span
                className={`text-lg font-bold w-12 text-right ${
                  comp.win_probability_vs_this >= 55
                    ? "text-green-400"
                    : comp.win_probability_vs_this >= 35
                    ? "text-amber-400"
                    : "text-red-400"
                }`}
              >
                {comp.win_probability_vs_this.toFixed(0)}%
              </span>
            </div>
          </div>

          {/* Threat signals */}
          {comp.threat_signals.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-red-400 mb-2">Menaces détectées</h3>
              <ul className="space-y-1">
                {comp.threat_signals.map((s, i) => (
                  <li key={i} className="text-xs text-slate-300 flex gap-2">
                    <span className="text-red-400 shrink-0">⚡</span>
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Opportunity signals */}
          {comp.opportunity_signals.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-green-400 mb-2">Faiblesses exploitables</h3>
              <ul className="space-y-1">
                {comp.opportunity_signals.map((s, i) => (
                  <li key={i} className="text-xs text-slate-300 flex gap-2">
                    <span className="text-green-400 shrink-0">✓</span>
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Battle card */}
          {comp.battle_card_tips.length > 0 && (
            <div className="bg-indigo-500/5 border border-indigo-500/20 rounded-xl p-4">
              <h3 className="text-sm font-semibold text-indigo-400 mb-2">
                Battle Card — Conseils de vente
              </h3>
              <ul className="space-y-1.5">
                {comp.battle_card_tips.map((tip, i) => (
                  <li key={i} className="text-xs text-slate-300 flex gap-2">
                    <span className="text-indigo-400 shrink-0">→</span>
                    <span>{tip}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function CompetitorCard({ comp, onClick }: { comp: CompetitorResult; onClick: () => void }) {
  const levelColor = LEVEL_COLORS[comp.threat_level] || "#6366f1";

  return (
    <button
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-2xl p-5 text-left hover:border-slate-600 transition-all hover:bg-slate-800/40 group"
    >
      <div className="flex items-start gap-4">
        <ThreatRing score={comp.threat_score} level={comp.threat_level} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span className="font-semibold text-slate-100 truncate">{comp.competitor_name}</span>
            <span
              className={`text-xs px-2 py-0.5 rounded-full border font-medium shrink-0 ${LEVEL_BG[comp.threat_level]}`}
            >
              {LEVEL_LABELS[comp.threat_level]}
            </span>
          </div>
          <p className="text-xs text-slate-400 mb-3">
            {TYPE_LABELS[comp.competitor_type] ?? comp.competitor_type}
          </p>

          <div className="flex flex-wrap gap-2 text-xs">
            <span
              className={`rounded-lg px-2 py-1 font-medium ${ACTION_COLORS[comp.recommended_action]}`}
            >
              {ACTION_LABELS[comp.recommended_action]}
            </span>
            <span
              className={`rounded-lg px-2 py-1 font-medium ${
                comp.win_probability_vs_this >= 55
                  ? "bg-green-500/10 text-green-400"
                  : comp.win_probability_vs_this >= 35
                  ? "bg-amber-500/10 text-amber-400"
                  : "bg-red-500/10 text-red-400"
              }`}
            >
              Win {comp.win_probability_vs_this.toFixed(0)}%
            </span>
          </div>
        </div>
      </div>

      {/* Mini dimension bars */}
      <div className="mt-4 space-y-2">
        {[
          { label: "Marché", v: comp.market_score },
          { label: "Produit", v: comp.product_score },
          { label: "GTM", v: comp.gtm_score },
        ].map((d) => {
          const c =
            d.v >= 75 ? "#ef4444" : d.v >= 55 ? "#f97316" : d.v >= 35 ? "#f59e0b" : "#22c55e";
          return (
            <div key={d.label} className="flex items-center gap-2">
              <span className="text-xs text-slate-500 w-12 shrink-0">{d.label}</span>
              <div className="flex-1 h-1 rounded-full bg-slate-800 overflow-hidden">
                <div className="h-full rounded-full" style={{ width: `${d.v}%`, backgroundColor: c }} />
              </div>
              <span className="text-xs w-6 text-right shrink-0" style={{ color: c }}>
                {Math.round(d.v)}
              </span>
            </div>
          );
        })}
      </div>

      {/* Signals count */}
      <div className="mt-3 flex gap-4 text-xs text-slate-500">
        {comp.threat_signals.length > 0 && (
          <span className="text-red-400">{comp.threat_signals.length} menaces</span>
        )}
        {comp.opportunity_signals.length > 0 && (
          <span className="text-green-400">{comp.opportunity_signals.length} faiblesses</span>
        )}
        {comp.battle_card_tips.length > 0 && (
          <span className="text-indigo-400">{comp.battle_card_tips.length} conseils</span>
        )}
      </div>
    </button>
  );
}

export default function CompetitorIntelligencePage() {
  const [competitors, setCompetitors] = useState<CompetitorResult[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [activeLevel, setActiveLevel] = useState("all");
  const [selected, setSelected] = useState<CompetitorResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        if (activeLevel !== "all") params.set("level", activeLevel);
        const res = await fetch(`/api/competitor-intelligence?${params}`);
        const data = await res.json();
        setCompetitors(data.competitors ?? []);
        setSummary(data.summary ?? null);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [activeLevel]);

  return (
    <div className="min-h-screen bg-slate-950 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Intelligence Concurrentielle</h1>
          <p className="text-sm text-slate-400 mt-1">
            Surveillance et scoring des menaces concurrentielles — battle cards et stratégies de différenciation
          </p>
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {[
              {
                label: "Concurrents suivis",
                value: `${summary.total}`,
                sub: `${(summary.level_counts["critical"] || 0) + (summary.level_counts["high"] || 0)} menaces urgentes`,
                color: "text-slate-100",
              },
              {
                label: "Menace critique",
                value: `${summary.level_counts["critical"] || 0}`,
                sub: `${summary.level_counts["high"] || 0} niveaux élevés`,
                color: (summary.level_counts["critical"] || 0) > 0 ? "text-red-400" : "text-green-400",
              },
              {
                label: "Score menace moyen",
                value: `${summary.avg_threat_score}/100`,
                sub: "Toutes typologies",
                color:
                  summary.avg_threat_score >= 60
                    ? "text-red-400"
                    : summary.avg_threat_score >= 40
                    ? "text-amber-400"
                    : "text-green-400",
              },
              {
                label: "Win rate moyen",
                value: `${summary.avg_win_probability.toFixed(0)}%`,
                sub: "Probabilité de victoire vs tous",
                color:
                  summary.avg_win_probability >= 55
                    ? "text-green-400"
                    : summary.avg_win_probability >= 35
                    ? "text-amber-400"
                    : "text-red-400",
              },
            ].map((kpi) => (
              <div
                key={kpi.label}
                className="bg-slate-900 border border-slate-800 rounded-2xl p-4"
              >
                <div className={`text-2xl font-bold ${kpi.color}`}>{kpi.value}</div>
                <div className="text-xs text-slate-400 mt-0.5">{kpi.label}</div>
                <div className="text-xs text-slate-500 mt-1">{kpi.sub}</div>
              </div>
            ))}
          </div>
        )}

        {/* Level filter tabs */}
        <div className="flex flex-wrap gap-2">
          {LEVEL_TABS.map((t) => {
            const count = t.key === "all" ? summary?.total : summary?.level_counts[t.key];
            return (
              <button
                key={t.key}
                onClick={() => setActiveLevel(t.key)}
                className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-all ${
                  activeLevel === t.key
                    ? "bg-indigo-600 border-indigo-500 text-white"
                    : "bg-slate-800/50 border-slate-700 text-slate-400 hover:border-slate-500"
                }`}
              >
                {t.label}
                {count !== undefined && (
                  <span className="ml-1.5 text-xs opacity-70">({count})</span>
                )}
              </button>
            );
          })}
        </div>

        {/* Threat distribution bar */}
        {summary && activeLevel === "all" && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
            <p className="text-xs text-slate-400 mb-3">Répartition des niveaux de menace</p>
            <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
              {(["critical", "high", "medium", "low", "minimal"] as const).map((lvl) => {
                const pct =
                  summary.total > 0
                    ? ((summary.level_counts[lvl] || 0) / summary.total) * 100
                    : 0;
                return pct > 0 ? (
                  <div
                    key={lvl}
                    className="h-full transition-all"
                    style={{ width: `${pct}%`, backgroundColor: LEVEL_COLORS[lvl] }}
                    title={`${LEVEL_LABELS[lvl]}: ${summary.level_counts[lvl] || 0}`}
                  />
                ) : null;
              })}
            </div>
            <div className="flex flex-wrap gap-3 mt-2">
              {(["critical", "high", "medium", "low", "minimal"] as const).map((lvl) => (
                <div key={lvl} className="flex items-center gap-1.5 text-xs text-slate-400">
                  <div
                    className="w-2 h-2 rounded-full"
                    style={{ backgroundColor: LEVEL_COLORS[lvl] }}
                  />
                  {LEVEL_LABELS[lvl]} ({summary.level_counts[lvl] || 0})
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Competitor grid */}
        {loading ? (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="h-64 bg-slate-900 border border-slate-800 rounded-2xl animate-pulse" />
            ))}
          </div>
        ) : competitors.length === 0 ? (
          <div className="text-center py-20 text-slate-500">Aucun concurrent pour ce filtre</div>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {competitors.map((comp) => (
              <CompetitorCard
                key={comp.competitor_id}
                comp={comp}
                onClick={() => setSelected(comp)}
              />
            ))}
          </div>
        )}
      </div>

      {selected && <CompetitorModal comp={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
