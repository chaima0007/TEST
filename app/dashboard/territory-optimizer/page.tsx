"use client";

import { useEffect, useState, useCallback } from "react";

// ─── Types ──────────────────────────────────────────────────────────────────

type TerritoryHealth = "optimal" | "balanced" | "imbalanced" | "critical";
type TerritoryAction = "maintain" | "rebalance" | "hire" | "split" | "merge";
type CoverageRisk = "low" | "medium" | "high" | "critical";

interface Territory {
  territory_id: string;
  territory_name: string;
  region: string;
  rep_name: string;
  territory_health: TerritoryHealth;
  territory_action: TerritoryAction;
  coverage_risk: CoverageRisk;
  balance_score: number;
  quota_attainment_pct: number;
  pipeline_coverage_ratio: number;
  white_space_pct: number;
  strengths: string[];
  gaps: string[];
  recommendations: string[];
  territory_kpis: {
    pipeline_coverage_ratio: number;
    quota_attainment_pct: number;
    white_space_pct: number;
    active_account_pct: number;
    avg_account_health: number;
    qbr_coverage_pct: number;
    market_penetration_pct: number;
    deals_in_flight: number;
    accounts_at_risk: number;
    closed_won_ytd_eur: number;
  };
}

interface Summary {
  total: number;
  health_counts: Record<string, number>;
  action_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  avg_balance_score: number;
  avg_quota_attainment_pct: number;
  needs_rebalance_count: number;
  optimal_count: number;
  critical_count: number;
}

interface ApiResponse {
  territories: Territory[];
  summary: Summary;
}

// ─── Helpers ────────────────────────────────────────────────────────────────

function fmtEur(n: number) {
  if (n >= 1_000_000) return `€${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `€${Math.round(n / 1_000)}k`;
  return `€${n}`;
}

function healthBg(h: TerritoryHealth) {
  if (h === "optimal") return "bg-emerald-500/15 text-emerald-300 border border-emerald-500/30";
  if (h === "balanced") return "bg-sky-500/15 text-sky-300 border border-sky-500/30";
  if (h === "imbalanced") return "bg-amber-500/15 text-amber-300 border border-amber-500/30";
  return "bg-red-500/15 text-red-300 border border-red-500/30";
}

function healthRingColor(h: TerritoryHealth) {
  if (h === "optimal") return "#10b981";
  if (h === "balanced") return "#38bdf8";
  if (h === "imbalanced") return "#f59e0b";
  return "#ef4444";
}

function actionBg(a: TerritoryAction) {
  if (a === "maintain") return "bg-emerald-500/20 text-emerald-200";
  if (a === "rebalance") return "bg-amber-500/20 text-amber-200";
  if (a === "hire") return "bg-indigo-500/20 text-indigo-200";
  if (a === "split") return "bg-orange-500/20 text-orange-200";
  return "bg-slate-500/20 text-slate-200";
}

function riskBg(r: CoverageRisk) {
  if (r === "low") return "bg-emerald-500/15 text-emerald-300 border border-emerald-500/30";
  if (r === "medium") return "bg-amber-500/15 text-amber-300 border border-amber-500/30";
  if (r === "high") return "bg-orange-500/15 text-orange-300 border border-orange-500/30";
  return "bg-red-500/15 text-red-300 border border-red-500/30";
}

function healthLabel(h: TerritoryHealth) {
  if (h === "optimal") return "Optimal";
  if (h === "balanced") return "Équilibré";
  if (h === "imbalanced") return "Déséquilibré";
  return "Critique";
}

function actionLabel(a: TerritoryAction) {
  if (a === "maintain") return "Maintenir";
  if (a === "rebalance") return "Rebalancer";
  if (a === "hire") return "Recruter";
  if (a === "split") return "Diviser";
  return "Fusionner";
}

function riskLabel(r: CoverageRisk) {
  if (r === "low") return "Faible";
  if (r === "medium") return "Moyen";
  if (r === "high") return "Élevé";
  return "Critique";
}

function regionLabel(r: string) {
  if (r === "emea") return "EMEA";
  if (r === "amer") return "AMER";
  return "APAC";
}

function attainmentColor(pct: number) {
  if (pct >= 100) return "text-emerald-400";
  if (pct >= 75) return "text-sky-400";
  if (pct >= 50) return "text-amber-400";
  return "text-red-400";
}

// ─── Balance Ring ─────────────────────────────────────────────────────────────

function BalanceRing({ score, health }: { score: number; health: TerritoryHealth }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;

  return (
    <svg viewBox="0 0 80 80" className="w-20 h-20" aria-hidden="true">
      <circle cx="40" cy="40" r={r} fill="none" stroke="#1e293b" strokeWidth="7" />
      <circle
        cx="40"
        cy="40"
        r={r}
        fill="none"
        stroke={healthRingColor(health)}
        strokeWidth="7"
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform="rotate(-90 40 40)"
      />
      <text x="40" y="44" textAnchor="middle" fontSize="15" fontWeight="700" fill="#f1f5f9">
        {score}
      </text>
    </svg>
  );
}

// ─── Health Distribution Bar ──────────────────────────────────────────────────

function HealthDistBar({ summary }: { summary: Summary }) {
  const n = summary.total || 1;
  const opt = summary.health_counts["optimal"] || 0;
  const bal = summary.health_counts["balanced"] || 0;
  const imb = summary.health_counts["imbalanced"] || 0;
  const crit = summary.health_counts["critical"] || 0;
  return (
    <div className="flex h-2 rounded-full overflow-hidden gap-px bg-slate-800">
      {opt > 0 && <div className="bg-emerald-500 h-full" style={{ width: `${(opt / n) * 100}%` }} />}
      {bal > 0 && <div className="bg-sky-500 h-full" style={{ width: `${(bal / n) * 100}%` }} />}
      {imb > 0 && <div className="bg-amber-500 h-full" style={{ width: `${(imb / n) * 100}%` }} />}
      {crit > 0 && <div className="bg-red-500 h-full" style={{ width: `${(crit / n) * 100}%` }} />}
    </div>
  );
}

// ─── KPI Mini Bar ─────────────────────────────────────────────────────────────

function MiniBar({ label, value, max, color }: { label: string; value: number; max: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs mb-0.5">
        <span className="text-slate-500">{label}</span>
        <span className="text-slate-400">{value}%</span>
      </div>
      <div className="h-1 bg-slate-700 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${Math.min(100, (value / max) * 100)}%` }} />
      </div>
    </div>
  );
}

// ─── Detail Modal ────────────────────────────────────────────────────────────

function TerritoryModal({ territory, onClose }: { territory: Territory; onClose: () => void }) {
  useEffect(() => {
    function onKey(e: KeyboardEvent) { if (e.key === "Escape") onClose(); }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  const kpis = territory.territory_kpis;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-6 border-b border-slate-800 flex items-start justify-between gap-4">
          <div>
            <h2 className="text-lg font-bold text-slate-100">{territory.territory_name}</h2>
            <p className="text-slate-400 text-sm mt-0.5">{regionLabel(territory.region)} · Rep: {territory.rep_name}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 transition-colors text-xl leading-none">✕</button>
        </div>

        <div className="p-6 space-y-6">
          {/* Summary row */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <div className="text-xs text-slate-500 mb-1">Santé</div>
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${healthBg(territory.territory_health)}`}>
                {healthLabel(territory.territory_health)}
              </span>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <div className="text-xs text-slate-500 mb-1">Action</div>
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${actionBg(territory.territory_action)}`}>
                {actionLabel(territory.territory_action)}
              </span>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <div className="text-xs text-slate-500 mb-1">Quota</div>
              <div className={`text-base font-bold ${attainmentColor(territory.quota_attainment_pct)}`}>
                {territory.quota_attainment_pct}%
              </div>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <div className="text-xs text-slate-500 mb-1">Pipeline</div>
              <div className="text-base font-bold text-slate-100">{territory.pipeline_coverage_ratio}x</div>
            </div>
          </div>

          {/* KPI bars */}
          <div>
            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Métriques clés</div>
            <div className="space-y-3">
              <MiniBar label="Atteinte quota" value={kpis.quota_attainment_pct} max={150} color="bg-indigo-500" />
              <MiniBar label="Comptes actifs" value={kpis.active_account_pct} max={100} color="bg-sky-500" />
              <MiniBar label="Couverture QBR" value={kpis.qbr_coverage_pct} max={100} color="bg-emerald-500" />
              <MiniBar label="Pénétration marché" value={kpis.market_penetration_pct} max={100} color="bg-amber-500" />
            </div>
          </div>

          {/* Additional KPIs */}
          <div className="grid grid-cols-3 gap-3">
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <div className="text-xs text-slate-500 mb-1">Deals actifs</div>
              <div className="text-lg font-bold text-slate-100">{kpis.deals_in_flight}</div>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <div className="text-xs text-slate-500 mb-1">Comptes à risque</div>
              <div className={`text-lg font-bold ${kpis.accounts_at_risk > 3 ? "text-red-400" : "text-slate-100"}`}>
                {kpis.accounts_at_risk}
              </div>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <div className="text-xs text-slate-500 mb-1">Won YTD</div>
              <div className="text-lg font-bold text-emerald-400">{fmtEur(kpis.closed_won_ytd_eur)}</div>
            </div>
          </div>

          {/* Strengths */}
          {territory.strengths.length > 0 && (
            <div>
              <div className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-3">Points forts</div>
              <ul className="space-y-2">
                {territory.strengths.map((s, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                    <span className="text-emerald-400 mt-0.5 shrink-0">✓</span>
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Gaps */}
          {territory.gaps.length > 0 && (
            <div>
              <div className="text-xs font-semibold text-red-400 uppercase tracking-wider mb-3">Lacunes identifiées</div>
              <ul className="space-y-2">
                {territory.gaps.map((g, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                    <span className="text-red-400 mt-0.5 shrink-0">⚠</span>
                    <span>{g}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Recommendations */}
          <div>
            <div className="text-xs font-semibold text-indigo-400 uppercase tracking-wider mb-3">Recommandations</div>
            <ul className="space-y-2">
              {territory.recommendations.map((r, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                  <span className="text-indigo-400 mt-0.5 shrink-0">→</span>
                  <span>{r}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── Territory Card ───────────────────────────────────────────────────────────

function TerritoryCard({ territory, onClick }: { territory: Territory; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="w-full text-left bg-slate-800/50 hover:bg-slate-800 border border-slate-700/50 hover:border-slate-600 rounded-2xl p-5 transition-all duration-200 group"
    >
      <div className="flex items-start gap-4">
        <BalanceRing score={territory.balance_score} health={territory.territory_health} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${healthBg(territory.territory_health)}`}>
              {healthLabel(territory.territory_health)}
            </span>
            <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${actionBg(territory.territory_action)}`}>
              {actionLabel(territory.territory_action)}
            </span>
            <span className="text-[10px] bg-slate-700/60 text-slate-400 px-2 py-0.5 rounded-full">
              {regionLabel(territory.region)}
            </span>
          </div>
          <h3 className="text-sm font-semibold text-slate-100 truncate group-hover:text-indigo-300 transition-colors">
            {territory.territory_name}
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">{territory.rep_name}</p>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-3 text-center">
        <div>
          <div className="text-xs text-slate-500 mb-0.5">Quota</div>
          <div className={`text-sm font-bold ${attainmentColor(territory.quota_attainment_pct)}`}>
            {territory.quota_attainment_pct}%
          </div>
        </div>
        <div>
          <div className="text-xs text-slate-500 mb-0.5">Pipeline</div>
          <div className="text-sm font-bold text-slate-200">{territory.pipeline_coverage_ratio}x</div>
        </div>
        <div>
          <div className="text-xs text-slate-500 mb-0.5">Vierges</div>
          <div className={`text-sm font-bold ${territory.white_space_pct > 30 ? "text-red-400" : "text-slate-200"}`}>
            {territory.white_space_pct}%
          </div>
        </div>
      </div>

      {/* Mini balance bar */}
      <div className="mt-3">
        <div className="h-1 bg-slate-700 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full ${
              territory.territory_health === "optimal" ? "bg-emerald-500" :
              territory.territory_health === "balanced" ? "bg-sky-500" :
              territory.territory_health === "imbalanced" ? "bg-amber-500" : "bg-red-500"
            }`}
            style={{ width: `${territory.balance_score}%` }}
          />
        </div>
      </div>
    </button>
  );
}

// ─── Page ────────────────────────────────────────────────────────────────────

type HealthFilter = "all" | TerritoryHealth;
type RegionFilter = "all" | "emea" | "amer" | "apac";

const HEALTH_TABS: { id: HealthFilter; label: string }[] = [
  { id: "all", label: "Tous" },
  { id: "critical", label: "Critique" },
  { id: "imbalanced", label: "Déséquilibré" },
  { id: "balanced", label: "Équilibré" },
  { id: "optimal", label: "Optimal" },
];

const REGION_TABS: { id: RegionFilter; label: string }[] = [
  { id: "all", label: "Toutes régions" },
  { id: "emea", label: "EMEA" },
  { id: "amer", label: "AMER" },
  { id: "apac", label: "APAC" },
];

export default function TerritoryOptimizerPage() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [healthFilter, setHealthFilter] = useState<HealthFilter>("all");
  const [regionFilter, setRegionFilter] = useState<RegionFilter>("all");
  const [selected, setSelected] = useState<Territory | null>(null);

  const fetchData = useCallback(async (health: HealthFilter, region: RegionFilter) => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (health !== "all") params.set("health", health);
      if (region !== "all") params.set("region", region);
      const res = await fetch(`/api/territory-optimizer${params.size ? `?${params}` : ""}`);
      if (res.ok) setData(await res.json());
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(healthFilter, regionFilter); }, [healthFilter, regionFilter, fetchData]);

  const summary = data?.summary;

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-6 lg:p-8">
      {selected && <TerritoryModal territory={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-slate-100">Optimiseur Territoire</h1>
        <p className="text-slate-400 mt-1 text-sm">Analyse et rééquilibrage des territoires commerciaux — couverture, pipeline et performance rep</p>
      </div>

      {/* KPI Strip */}
      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">Score moyen</div>
            <div className="text-2xl font-bold text-sky-400">{summary.avg_balance_score}</div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">Quota moyen</div>
            <div className={`text-2xl font-bold ${summary.avg_quota_attainment_pct >= 100 ? "text-emerald-400" : summary.avg_quota_attainment_pct >= 75 ? "text-amber-400" : "text-red-400"}`}>
              {summary.avg_quota_attainment_pct}%
            </div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">Optimaux</div>
            <div className="text-2xl font-bold text-emerald-400">{summary.optimal_count}</div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">Critiques</div>
            <div className="text-2xl font-bold text-red-400">{summary.critical_count}</div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">À rebalancer</div>
            <div className="text-2xl font-bold text-amber-400">{summary.needs_rebalance_count}</div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">Territoires</div>
            <div className="text-2xl font-bold text-slate-300">{summary.total}</div>
          </div>
        </div>
      )}

      {/* Health distribution bar */}
      {summary && (
        <div className="mb-6 bg-slate-800/30 border border-slate-700/50 rounded-xl p-4">
          <div className="flex justify-between text-xs text-slate-400 mb-2">
            <span>Distribution de santé</span>
            <span>{summary.total} territoires</span>
          </div>
          <HealthDistBar summary={summary} />
          <div className="flex gap-4 mt-2 text-xs flex-wrap">
            <span className="flex items-center gap-1.5 text-emerald-400">
              <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block" />
              Optimal {summary.health_counts["optimal"] || 0}
            </span>
            <span className="flex items-center gap-1.5 text-sky-400">
              <span className="w-2 h-2 rounded-full bg-sky-500 inline-block" />
              Équilibré {summary.health_counts["balanced"] || 0}
            </span>
            <span className="flex items-center gap-1.5 text-amber-400">
              <span className="w-2 h-2 rounded-full bg-amber-500 inline-block" />
              Déséquilibré {summary.health_counts["imbalanced"] || 0}
            </span>
            <span className="flex items-center gap-1.5 text-red-400">
              <span className="w-2 h-2 rounded-full bg-red-500 inline-block" />
              Critique {summary.health_counts["critical"] || 0}
            </span>
          </div>
        </div>
      )}

      {/* Health filter tabs */}
      <div className="flex gap-2 flex-wrap mb-3">
        {HEALTH_TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setHealthFilter(t.id)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              healthFilter === t.id
                ? "bg-indigo-600 text-white"
                : "bg-slate-800 text-slate-400 hover:text-slate-200"
            }`}
          >
            {t.label}
            {summary && t.id !== "all" && (
              <span className="ml-1.5 text-xs opacity-70">{summary.health_counts[t.id] || 0}</span>
            )}
          </button>
        ))}
      </div>

      {/* Region filter tabs */}
      <div className="flex gap-2 flex-wrap mb-6">
        {REGION_TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setRegionFilter(t.id)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              regionFilter === t.id
                ? "bg-slate-600 text-white"
                : "bg-slate-800/50 text-slate-500 hover:text-slate-300"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Territory Grid */}
      {loading ? (
        <div className="flex items-center justify-center h-48 text-slate-500">Chargement…</div>
      ) : !data?.territories.length ? (
        <div className="flex items-center justify-center h-48 text-slate-500">Aucun territoire pour ce filtre.</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
          {data.territories.map((territory) => (
            <TerritoryCard key={territory.territory_id} territory={territory} onClick={() => setSelected(territory)} />
          ))}
        </div>
      )}
    </main>
  );
}
