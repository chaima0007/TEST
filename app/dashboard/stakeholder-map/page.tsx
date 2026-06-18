"use client";

import { useState, useEffect, useCallback } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

type Stakeholder = {
  stakeholder_id: string;
  deal_id: string;
  account_id: string;
  account_name: string;
  name: string;
  title: string;
  influence_score: number;
  engagement_level: string;
  relationship_status: string;
  stakeholder_role: string;
  coverage_risk: string;
  engagement_gap: number;
  is_at_risk: boolean;
  priority_rank: number;
  recommended_action: string;
  risk_factors: string[];
  strengths: string[];
  recommended_approach: string;
};

type Summary = {
  total: number;
  role_counts: Record<string, number>;
  engagement_counts: Record<string, number>;
  relationship_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  avg_influence_score: number;
  avg_engagement_gap: number;
  champions_count: number;
  economic_buyers_count: number;
  at_risk_count: number;
  covered_count: number;
  critical_stakeholders_count: number;
};

// ── Helpers ───────────────────────────────────────────────────────────────────

const ROLE_LABELS: Record<string, string> = {
  economic_buyer:  "Décideur Budget",
  champion:        "Champion",
  technical_buyer: "Acheteur Technique",
  end_user:        "Utilisateur Final",
  blocker:         "Bloqueur",
  influencer:      "Influenceur",
  unknown:         "Inconnu",
};

const ENGAGEMENT_LABELS: Record<string, string> = {
  strong:   "Fort",
  moderate: "Modéré",
  weak:     "Faible",
  none:     "Aucun",
  hostile:  "Hostile",
};

const RELATIONSHIP_LABELS: Record<string, string> = {
  sponsor:  "Sponsor",
  ally:     "Allié",
  neutral:  "Neutre",
  skeptic:  "Sceptique",
  opponent: "Opposant",
};

const RISK_LABELS: Record<string, string> = {
  covered:  "Couvert",
  partial:  "Partiel",
  at_risk:  "À Risque",
  critical: "Critique",
};

function engagementColor(level: string) {
  return {
    strong:   "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
    moderate: "bg-blue-500/20 text-blue-300 border-blue-500/30",
    weak:     "bg-amber-500/20 text-amber-300 border-amber-500/30",
    none:     "bg-slate-500/20 text-slate-300 border-slate-500/30",
    hostile:  "bg-red-500/20 text-red-300 border-red-500/30",
  }[level] ?? "bg-slate-500/20 text-slate-300 border-slate-500/30";
}

function roleColor(role: string) {
  return {
    economic_buyer:  "bg-violet-500/20 text-violet-300 border-violet-500/30",
    champion:        "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
    technical_buyer: "bg-blue-500/20 text-blue-300 border-blue-500/30",
    end_user:        "bg-slate-500/20 text-slate-300 border-slate-500/30",
    blocker:         "bg-red-500/20 text-red-300 border-red-500/30",
    influencer:      "bg-amber-500/20 text-amber-300 border-amber-500/30",
    unknown:         "bg-slate-600/20 text-slate-400 border-slate-600/30",
  }[role] ?? "bg-slate-500/20 text-slate-300 border-slate-500/30";
}

function riskColor(risk: string) {
  return {
    covered:  "text-emerald-400",
    partial:  "text-amber-400",
    at_risk:  "text-orange-400",
    critical: "text-red-400",
  }[risk] ?? "text-slate-400";
}

function relationshipColor(status: string) {
  return {
    sponsor:  "bg-violet-500/20 text-violet-300",
    ally:     "bg-emerald-500/20 text-emerald-300",
    neutral:  "bg-slate-500/20 text-slate-300",
    skeptic:  "bg-amber-500/20 text-amber-300",
    opponent: "bg-red-500/20 text-red-300",
  }[status] ?? "bg-slate-500/20 text-slate-300";
}

// ── InfluenceRing ─────────────────────────────────────────────────────────────

function InfluenceRing({ score }: { score: number }) {
  const r = 38, cx = 48, cy = 48;
  const circ = 2 * Math.PI * r;
  const arc  = (score / 100) * circ;
  const strokeColor =
    score >= 75 ? "#a78bfa" : score >= 50 ? "#60a5fa" : score >= 25 ? "#f59e0b" : "#f87171";

  return (
    <svg width="96" height="96" viewBox="0 0 96 96">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
      <circle
        cx={cx} cy={cy} r={r}
        fill="none" stroke={strokeColor} strokeWidth="8"
        strokeLinecap="round"
        strokeDasharray={`${arc} ${circ - arc}`}
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy - 4} textAnchor="middle" fill="white" fontSize="14" fontWeight="bold">
        {score}
      </text>
      <text x={cx} y={cy + 12} textAnchor="middle" fill="#94a3b8" fontSize="8">
        Influence
      </text>
    </svg>
  );
}

// ── RoleDistBar ───────────────────────────────────────────────────────────────

function RoleDistBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const palette: Record<string, string> = {
    economic_buyer:  "#a78bfa",
    champion:        "#34d399",
    technical_buyer: "#60a5fa",
    influencer:      "#f59e0b",
    end_user:        "#94a3b8",
    blocker:         "#f87171",
    unknown:         "#475569",
  };
  const entries = Object.entries(counts).sort((a, b) => b[1] - a[1]);

  return (
    <div className="space-y-2">
      {entries.map(([role, count]) => (
        <div key={role} className="flex items-center gap-2">
          <span className="w-32 text-xs text-slate-400 truncate">
            {ROLE_LABELS[role] ?? role}
          </span>
          <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full transition-all"
              style={{
                width: total ? `${(count / total) * 100}%` : "0%",
                backgroundColor: palette[role] ?? "#64748b",
              }}
            />
          </div>
          <span className="w-5 text-xs text-slate-400 text-right">{count}</span>
        </div>
      ))}
    </div>
  );
}

// ── StakeholderCard ───────────────────────────────────────────────────────────

function ScoreBar({
  label,
  value,
  color,
}: {
  label: string;
  value: number;
  color: string;
}) {
  return (
    <div>
      <div className="flex justify-between mb-0.5">
        <span className="text-[10px] text-slate-400">{label}</span>
        <span className="text-[10px] text-slate-300">{value}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full"
          style={{ width: `${value}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
}

function StakeholderCard({
  s,
  onClick,
}: {
  s: Stakeholder;
  onClick: () => void;
}) {
  return (
    <div
      onClick={onClick}
      className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-4 cursor-pointer hover:border-indigo-500/50 hover:bg-slate-800 transition-all group"
    >
      <div className="flex items-start gap-3 mb-3">
        <div className="flex-shrink-0">
          <InfluenceRing score={s.influence_score} />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2 mb-1">
            <div>
              <p className="text-sm font-semibold text-white truncate">{s.name}</p>
              <p className="text-xs text-slate-400 truncate">{s.title}</p>
              <p className="text-xs text-slate-500 truncate">{s.account_name}</p>
            </div>
            <span
              className={`text-[10px] px-2 py-0.5 rounded-full border font-medium flex-shrink-0 ${engagementColor(
                s.engagement_level
              )}`}
            >
              {ENGAGEMENT_LABELS[s.engagement_level] ?? s.engagement_level}
            </span>
          </div>
          <div className="flex flex-wrap gap-1 mt-1">
            <span
              className={`text-[10px] px-2 py-0.5 rounded-full border font-medium ${roleColor(
                s.stakeholder_role
              )}`}
            >
              {ROLE_LABELS[s.stakeholder_role] ?? s.stakeholder_role}
            </span>
            <span
              className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${relationshipColor(
                s.relationship_status
              )}`}
            >
              {RELATIONSHIP_LABELS[s.relationship_status] ?? s.relationship_status}
            </span>
          </div>
        </div>
      </div>

      <div className="space-y-1.5 mb-3">
        <ScoreBar label="Influence"       value={s.influence_score} color="#a78bfa" />
        <ScoreBar label="Gap d'engagement" value={s.engagement_gap}  color="#f87171" />
      </div>

      <div className="flex items-center justify-between">
        <span className={`text-xs font-medium ${riskColor(s.coverage_risk)}`}>
          {RISK_LABELS[s.coverage_risk] ?? s.coverage_risk}
        </span>
        <span className="text-[10px] text-slate-500">Priorité #{s.priority_rank}</span>
      </div>

      {s.is_at_risk && (
        <div className="mt-2 text-[10px] text-red-400 bg-red-900/20 rounded px-2 py-1">
          ⚠ À risque — action requise
        </div>
      )}
    </div>
  );
}

// ── StakeholderModal ──────────────────────────────────────────────────────────

function StakeholderModal({
  s,
  onClose,
}: {
  s: Stakeholder;
  onClose: () => void;
}) {
  const [tab, setTab] = useState<"action" | "strengths" | "risks">("action");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-5 border-b border-slate-800">
          <div className="flex items-start justify-between gap-3">
            <div className="flex items-center gap-3">
              <InfluenceRing score={s.influence_score} />
              <div>
                <p className="text-lg font-bold text-white">{s.name}</p>
                <p className="text-sm text-slate-400">{s.title}</p>
                <p className="text-xs text-slate-500">{s.account_name}</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-slate-500 hover:text-white text-xl leading-none"
            >
              ×
            </button>
          </div>
          <div className="flex flex-wrap gap-2 mt-3">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${engagementColor(s.engagement_level)}`}>
              {ENGAGEMENT_LABELS[s.engagement_level] ?? s.engagement_level}
            </span>
            <span className={`text-xs px-2 py-0.5 rounded-full border ${roleColor(s.stakeholder_role)}`}>
              {ROLE_LABELS[s.stakeholder_role] ?? s.stakeholder_role}
            </span>
            <span className={`text-xs px-2 py-0.5 rounded-full ${relationshipColor(s.relationship_status)}`}>
              {RELATIONSHIP_LABELS[s.relationship_status] ?? s.relationship_status}
            </span>
            <span className={`text-xs font-medium ${riskColor(s.coverage_risk)}`}>
              Couverture: {RISK_LABELS[s.coverage_risk] ?? s.coverage_risk}
            </span>
          </div>
        </div>

        {/* Scores */}
        <div className="grid grid-cols-2 gap-3 p-5 border-b border-slate-800">
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-xs text-slate-400 mb-1">Influence</p>
            <p className="text-xl font-bold text-violet-400">{s.influence_score}</p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-xs text-slate-400 mb-1">Gap d'engagement</p>
            <p className="text-xl font-bold text-red-400">{s.engagement_gap}</p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-xs text-slate-400 mb-1">Priorité</p>
            <p className="text-xl font-bold text-blue-400">#{s.priority_rank}</p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-xs text-slate-400 mb-1">Statut</p>
            <p className={`text-sm font-bold ${s.is_at_risk ? "text-red-400" : "text-emerald-400"}`}>
              {s.is_at_risk ? "À risque" : "OK"}
            </p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["action", "strengths", "risks"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-xs font-medium transition-colors ${
                tab === t
                  ? "text-indigo-400 border-b-2 border-indigo-400"
                  : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "action" ? "Plan d'action" : t === "strengths" ? "Points forts" : "Risques"}
            </button>
          ))}
        </div>

        <div className="p-5">
          {tab === "action" && (
            <div className="space-y-4">
              <div>
                <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">
                  Action recommandée
                </p>
                <p className="text-sm text-slate-200 bg-indigo-900/30 border border-indigo-700/30 rounded-lg p-3">
                  {s.recommended_action}
                </p>
              </div>
              <div>
                <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">
                  Approche conseillée
                </p>
                <p className="text-sm text-slate-300">{s.recommended_approach}</p>
              </div>
            </div>
          )}
          {tab === "strengths" && (
            <div>
              {s.strengths.length === 0 ? (
                <p className="text-sm text-slate-500 italic">Aucun point fort identifié.</p>
              ) : (
                <ul className="space-y-2">
                  {s.strengths.map((st, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                      <span className="text-emerald-400 mt-0.5">✓</span>
                      <span>{st}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
          {tab === "risks" && (
            <div>
              {s.risk_factors.length === 0 ? (
                <p className="text-sm text-slate-500 italic">Aucun risque identifié.</p>
              ) : (
                <ul className="space-y-2">
                  {s.risk_factors.map((rf, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                      <span className="text-red-400 mt-0.5">!</span>
                      <span>{rf}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function StakeholderMapPage() {
  const [data, setData] = useState<{
    stakeholders: Stakeholder[];
    summary: Summary;
  } | null>(null);
  const [loading, setLoading]           = useState(true);
  const [error, setError]               = useState<string | null>(null);
  const [roleFilter, setRoleFilter]     = useState<string>("all");
  const [engFilter, setEngFilter]       = useState<string>("all");
  const [selected, setSelected]         = useState<Stakeholder | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      if (roleFilter !== "all") params.set("role", roleFilter);
      if (engFilter  !== "all") params.set("engagement", engFilter);
      const res = await fetch(`/api/stakeholder-map?${params}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setData(await res.json());
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Erreur inconnue");
    } finally {
      setLoading(false);
    }
  }, [roleFilter, engFilter]);

  useEffect(() => { load(); }, [load]);

  const s = data?.summary;

  const kpis = s
    ? [
        { label: "Total Stakeholders",   value: s.total,                    color: "text-blue-400" },
        { label: "Champions",             value: s.champions_count,           color: "text-emerald-400" },
        { label: "Décideurs Budget",      value: s.economic_buyers_count,     color: "text-violet-400" },
        { label: "À Risque",              value: s.at_risk_count,             color: "text-red-400" },
        { label: "Couverts",              value: s.covered_count,             color: "text-emerald-400" },
        { label: "Critiques",             value: s.critical_stakeholders_count, color: "text-red-500" },
      ]
    : [];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Stakeholder Map Intelligence</h1>
        <p className="text-slate-400 text-sm mt-1">
          Cartographie du comité d'achat — influence, engagement et risques de couverture
        </p>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-900/30 border border-red-700 rounded-lg text-red-300 text-sm">
          {error}
        </div>
      )}

      {/* KPI Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
        {kpis.map((k) => (
          <div
            key={k.label}
            className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-4"
          >
            <p className="text-xs text-slate-400 mb-1">{k.label}</p>
            <p className={`text-2xl font-bold ${k.color}`}>{k.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Avg scores */}
        <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5">
          <p className="text-sm font-semibold text-white mb-4">Scores Moyens</p>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-xs text-slate-400 mb-1">Influence moy.</p>
              <p className="text-2xl font-bold text-violet-400">
                {s?.avg_influence_score ?? "—"}
              </p>
            </div>
            <div>
              <p className="text-xs text-slate-400 mb-1">Gap moy.</p>
              <p className="text-2xl font-bold text-red-400">
                {s?.avg_engagement_gap ?? "—"}
              </p>
            </div>
          </div>
        </div>

        {/* Role distribution */}
        <div className="lg:col-span-2 bg-slate-800/60 border border-slate-700/50 rounded-xl p-5">
          <p className="text-sm font-semibold text-white mb-4">Distribution des Rôles</p>
          {s ? (
            <RoleDistBar counts={s.role_counts} total={s.total} />
          ) : (
            <div className="h-24 bg-slate-700/30 rounded animate-pulse" />
          )}
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-5">
        <div className="flex flex-wrap gap-1">
          {["all", "economic_buyer", "champion", "technical_buyer", "influencer", "blocker", "end_user"].map((v) => (
            <button
              key={v}
              onClick={() => setRoleFilter(v)}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                roleFilter === v
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:bg-slate-700"
              }`}
            >
              {v === "all" ? "Tous les rôles" : (ROLE_LABELS[v] ?? v)}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-1">
          {["all", "strong", "moderate", "weak", "none", "hostile"].map((v) => (
            <button
              key={v}
              onClick={() => setEngFilter(v)}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                engFilter === v
                  ? "bg-violet-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:bg-slate-700"
              }`}
            >
              {v === "all" ? "Tout engagement" : (ENGAGEMENT_LABELS[v] ?? v)}
            </button>
          ))}
        </div>
      </div>

      {/* Cards */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="h-56 bg-slate-800/40 rounded-xl animate-pulse" />
          ))}
        </div>
      ) : (
        <>
          <p className="text-xs text-slate-500 mb-3">
            {data?.stakeholders.length ?? 0} stakeholder(s) affiché(s)
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {(data?.stakeholders ?? []).map((sh) => (
              <StakeholderCard
                key={sh.stakeholder_id}
                s={sh}
                onClick={() => setSelected(sh)}
              />
            ))}
          </div>
        </>
      )}

      {selected && (
        <StakeholderModal s={selected} onClose={() => setSelected(null)} />
      )}
    </div>
  );
}
