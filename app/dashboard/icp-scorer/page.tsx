"use client";

import { useState, useEffect, useRef } from "react";

interface CompanyResult {
  company_id: string;
  company_name: string;
  industry: string;
  company_size: string;
  employee_count: number;
  annual_revenue_eur: number;
  growth_stage: string;
  icp_score: number;
  icp_tier: string;
  firmographic_score: number;
  intent_score: number;
  strategic_score: number;
  risk_penalty: number;
  outreach_recommendation: string;
  estimated_deal_size_eur: number;
  priority_rank: number;
  fit_signals: string[];
  risk_signals: string[];
}

interface Summary {
  total: number;
  tier_counts: Record<string, number>;
  rec_counts: Record<string, number>;
  avg_icp_score: number;
  total_pipeline_eur: number;
}

const TIER_TABS = [
  { key: "all", label: "Tous" },
  { key: "perfect", label: "Parfait" },
  { key: "strong", label: "Fort" },
  { key: "moderate", label: "Modéré" },
  { key: "weak", label: "Faible" },
  { key: "disqualified", label: "Disqualifié" },
];

const TIER_COLORS: Record<string, string> = {
  perfect: "#6366f1",
  strong: "#22c55e",
  moderate: "#f59e0b",
  weak: "#f97316",
  disqualified: "#ef4444",
};

const TIER_BG: Record<string, string> = {
  perfect: "bg-indigo-500/10 text-indigo-400 border-indigo-500/30",
  strong: "bg-green-500/10 text-green-400 border-green-500/30",
  moderate: "bg-amber-500/10 text-amber-400 border-amber-500/30",
  weak: "bg-orange-500/10 text-orange-400 border-orange-500/30",
  disqualified: "bg-red-500/10 text-red-400 border-red-500/30",
};

const TIER_LABELS: Record<string, string> = {
  perfect: "Parfait",
  strong: "Fort",
  moderate: "Modéré",
  weak: "Faible",
  disqualified: "Disqualifié",
};

const REC_LABELS: Record<string, string> = {
  prioritize: "Prioriser",
  qualify: "Qualifier",
  deprioritize: "Déprioritiser",
  reject: "Rejeter",
};

const REC_COLORS: Record<string, string> = {
  prioritize: "bg-indigo-500/10 text-indigo-400",
  qualify: "bg-amber-500/10 text-amber-400",
  deprioritize: "bg-orange-500/10 text-orange-400",
  reject: "bg-red-500/10 text-red-400",
};

const SIZE_LABELS: Record<string, string> = {
  startup: "Startup",
  smb: "PME",
  mid_market: "Mid-Market",
  enterprise: "Enterprise",
  large_enterprise: "Grande Ent.",
};

const GROWTH_LABELS: Record<string, string> = {
  hyper_growth: "Hyper-croissance",
  fast_growth: "Forte croissance",
  moderate_growth: "Croissance modérée",
  stable: "Stable",
  declining: "Déclin",
};

function fmtEur(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}k€`;
  return `${n}€`;
}

function fmtNum(n: number) {
  if (n >= 1000) return `${(n / 1000).toFixed(1)}k`;
  return `${n}`;
}

function ICPRing({ score, tier }: { score: number; tier: string }) {
  const r = 28;
  const circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  const color = TIER_COLORS[tier] || "#6366f1";

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
    value >= 75 ? "#22c55e" : value >= 50 ? "#6366f1" : value >= 30 ? "#f59e0b" : "#ef4444";
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

function CompanyModal({ co, onClose }: { co: CompanyResult; onClose: () => void }) {
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

  const tierColor = TIER_COLORS[co.icp_tier] || "#6366f1";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div
        ref={ref}
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto"
      >
        <div className="p-6 border-b border-slate-800 flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 flex-wrap">
              <h2 className="text-xl font-bold text-slate-100">{co.company_name}</h2>
              <span
                className={`text-xs px-2 py-0.5 rounded-full border font-medium ${TIER_BG[co.icp_tier]}`}
              >
                {TIER_LABELS[co.icp_tier]}
              </span>
              <span
                className={`text-xs px-2 py-0.5 rounded-full font-medium ${REC_COLORS[co.outreach_recommendation]}`}
              >
                {REC_LABELS[co.outreach_recommendation]}
              </span>
            </div>
            <p className="text-sm text-slate-400 mt-1">
              {co.industry} · {SIZE_LABELS[co.company_size] ?? co.company_size}
            </p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200 text-xl shrink-0">
            ✕
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* KPIs */}
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {[
              { label: "CA annuel", value: fmtEur(co.annual_revenue_eur) },
              { label: "Effectif", value: fmtNum(co.employee_count) },
              {
                label: "Croissance",
                value: GROWTH_LABELS[co.growth_stage] ?? co.growth_stage,
              },
              {
                label: "Deal estimé",
                value: fmtEur(co.estimated_deal_size_eur),
                color: "text-indigo-400",
              },
            ].map((kpi) => (
              <div key={kpi.label} className="bg-slate-800/50 rounded-xl p-3 text-center">
                <div className={`text-base font-bold ${kpi.color ?? "text-slate-100"} leading-tight`}>
                  {kpi.value}
                </div>
                <div className="text-xs text-slate-400 mt-0.5">{kpi.label}</div>
              </div>
            ))}
          </div>

          {/* ICP ring + score */}
          <div className="flex items-center gap-6 bg-slate-800/30 rounded-xl p-4">
            <ICPRing score={co.icp_score} tier={co.icp_tier} />
            <div className="flex-1 min-w-0">
              <div className="flex items-baseline gap-2 mb-1">
                <span className="text-2xl font-bold" style={{ color: tierColor }}>
                  {co.icp_score.toFixed(1)}
                </span>
                <span className="text-sm text-slate-400">/ 100 — score ICP</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-slate-400">
                Rang priorité :
                <span className="font-bold text-slate-200 ml-1">#{co.priority_rank}</span>
              </div>
              {co.risk_penalty > 0 && (
                <div className="text-xs text-red-400 mt-1">
                  Pénalité risque : -{co.risk_penalty} pts
                </div>
              )}
            </div>
          </div>

          {/* Score dimensions */}
          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-slate-300">Dimensions ICP</h3>
            <ScoreBar label="Firmographique" value={co.firmographic_score} />
            <ScoreBar label="Intention / Signaux" value={co.intent_score} />
            <ScoreBar label="Fit stratégique" value={co.strategic_score} />
          </div>

          {/* Fit signals */}
          {co.fit_signals.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-green-400 mb-2">Signaux positifs</h3>
              <ul className="space-y-1">
                {co.fit_signals.map((s, i) => (
                  <li key={i} className="text-xs text-slate-300 flex gap-2">
                    <span className="text-green-400 shrink-0">✓</span>
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Risk signals */}
          {co.risk_signals.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-red-400 mb-2">Signaux de risque</h3>
              <ul className="space-y-1">
                {co.risk_signals.map((s, i) => (
                  <li key={i} className="text-xs text-slate-300 flex gap-2">
                    <span className="text-red-400 shrink-0">⚠</span>
                    <span>{s}</span>
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

function CompanyCard({ co, onClick }: { co: CompanyResult; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-2xl p-5 text-left hover:border-slate-600 transition-all hover:bg-slate-800/40 group"
    >
      <div className="flex items-start gap-4">
        <div className="flex flex-col items-center gap-1 shrink-0">
          <ICPRing score={co.icp_score} tier={co.icp_tier} />
          <span className="text-xs text-slate-500">#{co.priority_rank}</span>
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span className="font-semibold text-slate-100 truncate">{co.company_name}</span>
            <span
              className={`text-xs px-2 py-0.5 rounded-full border font-medium shrink-0 ${TIER_BG[co.icp_tier]}`}
            >
              {TIER_LABELS[co.icp_tier]}
            </span>
          </div>
          <p className="text-xs text-slate-400 mb-3">
            {co.industry} · {SIZE_LABELS[co.company_size] ?? co.company_size}
          </p>

          <div className="flex flex-wrap gap-2 text-xs">
            <span className="bg-slate-800 rounded-lg px-2 py-1 text-slate-300">
              CA {fmtEur(co.annual_revenue_eur)}
            </span>
            <span className={`rounded-lg px-2 py-1 font-medium ${REC_COLORS[co.outreach_recommendation]}`}>
              {REC_LABELS[co.outreach_recommendation]}
            </span>
            <span className="bg-indigo-500/10 text-indigo-400 rounded-lg px-2 py-1">
              Deal ~{fmtEur(co.estimated_deal_size_eur)}
            </span>
          </div>
        </div>
      </div>

      {/* Mini dimension bars */}
      <div className="mt-4 space-y-2">
        {[
          { label: "Firmo.", v: co.firmographic_score },
          { label: "Intent", v: co.intent_score },
          { label: "Stratégie", v: co.strategic_score },
        ].map((d) => {
          const c =
            d.v >= 75 ? "#22c55e" : d.v >= 50 ? "#6366f1" : d.v >= 30 ? "#f59e0b" : "#ef4444";
          return (
            <div key={d.label} className="flex items-center gap-2">
              <span className="text-xs text-slate-500 w-16 shrink-0">{d.label}</span>
              <div className="flex-1 h-1 rounded-full bg-slate-800 overflow-hidden">
                <div
                  className="h-full rounded-full"
                  style={{ width: `${d.v}%`, backgroundColor: c }}
                />
              </div>
              <span className="text-xs w-6 text-right shrink-0" style={{ color: c }}>
                {Math.round(d.v)}
              </span>
            </div>
          );
        })}
      </div>

      {/* Growth stage */}
      <div className="mt-3 text-xs text-slate-500">
        {GROWTH_LABELS[co.growth_stage] ?? co.growth_stage} ·{" "}
        {co.employee_count.toLocaleString()} employés
      </div>
    </button>
  );
}

export default function ICPScorerPage() {
  const [companies, setCompanies] = useState<CompanyResult[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [activeTier, setActiveTier] = useState("all");
  const [selected, setSelected] = useState<CompanyResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        if (activeTier !== "all") params.set("tier", activeTier);
        const res = await fetch(`/api/icp-scorer?${params}`);
        const data = await res.json();
        setCompanies(data.companies ?? []);
        setSummary(data.summary ?? null);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [activeTier]);

  return (
    <div className="min-h-screen bg-slate-950 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Scoring ICP</h1>
          <p className="text-sm text-slate-400 mt-1">
            Qualification des entreprises par fit Ideal Customer Profile — firmographique, intention et fit stratégique
          </p>
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {[
              {
                label: "Entreprises analysées",
                value: `${summary.total}`,
                sub: `${(summary.tier_counts["perfect"] || 0) + (summary.tier_counts["strong"] || 0)} à prioriser`,
                color: "text-slate-100",
              },
              {
                label: "Score ICP moyen",
                value: `${summary.avg_icp_score}/100`,
                sub: `${summary.tier_counts["disqualified"] || 0} disqualifiés`,
                color:
                  summary.avg_icp_score >= 70
                    ? "text-green-400"
                    : summary.avg_icp_score >= 50
                    ? "text-amber-400"
                    : "text-red-400",
              },
              {
                label: "Pipeline qualifié",
                value: fmtEur(summary.total_pipeline_eur),
                sub: "Deals estimés (PERFECT + STRONG)",
                color: "text-indigo-400",
              },
              {
                label: "Taux qualification",
                value: `${Math.round(((summary.rec_counts["prioritize"] || 0) / summary.total) * 100)}%`,
                sub: `${summary.rec_counts["prioritize"] || 0} prioritaires`,
                color: "text-green-400",
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

        {/* Tier filter tabs */}
        <div className="flex flex-wrap gap-2">
          {TIER_TABS.map((t) => {
            const count =
              t.key === "all" ? summary?.total : summary?.tier_counts[t.key];
            return (
              <button
                key={t.key}
                onClick={() => setActiveTier(t.key)}
                className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-all ${
                  activeTier === t.key
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

        {/* Tier distribution bar */}
        {summary && activeTier === "all" && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
            <p className="text-xs text-slate-400 mb-3">Répartition des tiers ICP</p>
            <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
              {(["perfect", "strong", "moderate", "weak", "disqualified"] as const).map((tier) => {
                const pct =
                  summary.total > 0
                    ? ((summary.tier_counts[tier] || 0) / summary.total) * 100
                    : 0;
                return pct > 0 ? (
                  <div
                    key={tier}
                    className="h-full transition-all"
                    style={{ width: `${pct}%`, backgroundColor: TIER_COLORS[tier] }}
                    title={`${TIER_LABELS[tier]}: ${summary.tier_counts[tier] || 0}`}
                  />
                ) : null;
              })}
            </div>
            <div className="flex flex-wrap gap-3 mt-2">
              {(["perfect", "strong", "moderate", "weak", "disqualified"] as const).map((tier) => (
                <div key={tier} className="flex items-center gap-1.5 text-xs text-slate-400">
                  <div
                    className="w-2 h-2 rounded-full"
                    style={{ backgroundColor: TIER_COLORS[tier] }}
                  />
                  {TIER_LABELS[tier]} ({summary.tier_counts[tier] || 0})
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Company grid */}
        {loading ? (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="h-64 bg-slate-900 border border-slate-800 rounded-2xl animate-pulse" />
            ))}
          </div>
        ) : companies.length === 0 ? (
          <div className="text-center py-20 text-slate-500">Aucune entreprise pour ce filtre</div>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {companies.map((co) => (
              <CompanyCard
                key={co.company_id}
                co={co}
                onClick={() => setSelected(co)}
              />
            ))}
          </div>
        )}
      </div>

      {selected && <CompanyModal co={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
