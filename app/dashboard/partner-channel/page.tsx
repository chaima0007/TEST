"use client";

import { useEffect, useState } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface Partner {
  partner_id: string;
  partner_name: string;
  partner_type: string;
  current_tier: string;
  recommended_tier: string;
  region: string;
  channel_health: string;
  partner_action: string;
  engagement_score: number;
  performance_score: number;
  pipeline_contribution: number;
  win_rate: number;
  certification_rate: number;
  quota_attainment: number;
  is_strategic: boolean;
  needs_intervention: boolean;
  closed_won_value: number;
  pipeline_value: number;
  deals_registered: number;
  deals_closed_won: number;
  joint_campaigns: number;
  nps_score: number;
  years_as_partner: number;
}

interface Summary {
  total: number;
  tier_counts: Record<string, number>;
  type_counts: Record<string, number>;
  health_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_engagement_score: number;
  avg_performance_score: number;
  avg_win_rate: number;
  avg_quota_attainment: number;
  strategic_count: number;
  at_risk_count: number;
  top_performer_count: number;
  needs_intervention_count: number;
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function healthColor(h: string) {
  return (
    {
      excellent:        "text-emerald-400",
      healthy:          "text-blue-400",
      needs_attention:  "text-amber-400",
      at_risk:          "text-orange-400",
      inactive:         "text-red-400",
    }[h] ?? "text-slate-400"
  );
}

function healthBg(h: string) {
  return (
    {
      excellent:        "bg-emerald-900/30 border-emerald-700/50",
      healthy:          "bg-blue-900/30 border-blue-700/50",
      needs_attention:  "bg-amber-900/30 border-amber-700/50",
      at_risk:          "bg-orange-900/30 border-orange-700/50",
      inactive:         "bg-red-900/30 border-red-700/50",
    }[h] ?? "bg-slate-800 border-slate-700"
  );
}

function tierBadge(tier: string) {
  const map: Record<string, string> = {
    platinum: "bg-cyan-900/50 text-cyan-300 border border-cyan-700/50",
    gold:     "bg-amber-900/50 text-amber-300 border border-amber-700/50",
    silver:   "bg-slate-700/50 text-slate-300 border border-slate-600/50",
    bronze:   "bg-orange-900/50 text-orange-300 border border-orange-700/50",
    prospect: "bg-violet-900/50 text-violet-300 border border-violet-700/50",
  };
  return map[tier] ?? "bg-slate-700 text-slate-300";
}

function actionBadge(action: string) {
  const map: Record<string, string> = {
    invest_and_grow:      "bg-emerald-900/50 text-emerald-300 border border-emerald-700/50",
    enable_and_train:     "bg-blue-900/50 text-blue-300 border border-blue-700/50",
    joint_campaign:       "bg-violet-900/50 text-violet-300 border border-violet-700/50",
    review_and_reset:     "bg-amber-900/50 text-amber-300 border border-amber-700/50",
    reactivate:           "bg-orange-900/50 text-orange-300 border border-orange-700/50",
    offboard:             "bg-red-900/50 text-red-300 border border-red-700/50",
  };
  return map[action] ?? "bg-slate-700 text-slate-300";
}

function fmtLabel(s: string) {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function fmtMoney(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000)     return `${(n / 1_000).toFixed(0)}k€`;
  return `${n.toFixed(0)}€`;
}

// ── Partner Score Ring ────────────────────────────────────────────────────────

function PartnerRing({ score, size = 52 }: { score: number; size?: number }) {
  const cx   = size / 2;
  const cy   = size / 2;
  const r    = size * 0.38;
  const circ = 2 * Math.PI * r;
  const arc  = (score / 100) * circ;
  const color =
    score >= 75 ? "#34d399" :
    score >= 55 ? "#60a5fa" :
    score >= 35 ? "#fbbf24" : "#f87171";

  return (
    <svg width={size} height={size} className="flex-shrink-0">
      <circle cx={cx} cy={cy} r={r} stroke="#1e293b" strokeWidth={size * 0.12} fill="none" />
      <circle
        cx={cx} cy={cy} r={r}
        stroke={color} strokeWidth={size * 0.12} fill="none"
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy + 1} textAnchor="middle" dominantBaseline="middle"
        fill={color} fontSize={size * 0.22} fontWeight="700">
        {Math.round(score)}
      </text>
    </svg>
  );
}

// ── Health Distribution Bar ───────────────────────────────────────────────────

function HealthDistBar({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((s, n) => s + n, 0);
  if (total === 0) return null;
  const order  = ["excellent", "healthy", "needs_attention", "at_risk", "inactive"];
  const colors: Record<string, string> = {
    excellent:       "bg-emerald-500",
    healthy:         "bg-blue-500",
    needs_attention: "bg-amber-500",
    at_risk:         "bg-orange-500",
    inactive:        "bg-red-500",
  };
  const entries = order.filter((k) => counts[k] != null).map((k) => [k, counts[k]] as [string, number]);

  return (
    <div className="space-y-1.5">
      <div className="flex h-2.5 rounded-full overflow-hidden gap-px">
        {entries.map(([k, v]) => (
          <div
            key={k}
            className={`${colors[k]} transition-all`}
            style={{ width: `${(v / total) * 100}%` }}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {entries.map(([k, v]) => (
          <span key={k} className="flex items-center gap-1 text-xs text-slate-400">
            <span className={`w-2 h-2 rounded-full ${colors[k]}`} />
            {fmtLabel(k)} <span className="text-slate-300 font-medium">{v}</span>
          </span>
        ))}
      </div>
    </div>
  );
}

// ── Partner Modal ─────────────────────────────────────────────────────────────

function PartnerModal({ partner, onClose }: { partner: Partner; onClose: () => void }) {
  const [tab, setTab] = useState<"performance" | "engagement" | "metrics">("performance");

  useEffect(() => {
    const fn = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    document.addEventListener("keydown", fn);
    return () => document.removeEventListener("keydown", fn);
  }, [onClose]);

  const tierChanged = partner.recommended_tier !== partner.current_tier;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-xl max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-5 border-b border-slate-800">
          <div className="flex items-start justify-between gap-3">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                <h2 className="text-slate-100 font-bold text-lg">{partner.partner_name}</h2>
                {partner.is_strategic && (
                  <span className="px-1.5 py-0.5 bg-indigo-900/50 text-indigo-300 border border-indigo-700/50 rounded text-xs font-medium">
                    Strategic
                  </span>
                )}
                {partner.needs_intervention && (
                  <span className="px-1.5 py-0.5 bg-red-900/50 text-red-300 border border-red-700/50 rounded text-xs font-medium">
                    Intervention
                  </span>
                )}
              </div>
              <p className="text-slate-400 text-sm mt-0.5">
                {fmtLabel(partner.partner_type)} · {partner.region} · {partner.years_as_partner.toFixed(1)}y
              </p>
            </div>
            <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl leading-none flex-shrink-0">✕</button>
          </div>
          <div className="flex items-center gap-2 mt-3 flex-wrap">
            <span className={`px-2 py-0.5 rounded text-xs font-medium ${tierBadge(partner.current_tier)}`}>
              {fmtLabel(partner.current_tier)}
            </span>
            {tierChanged && (
              <span className="text-slate-500 text-xs">
                → <span className={`font-medium ${tierBadge(partner.recommended_tier)} px-1.5 py-0.5 rounded`}>
                  {fmtLabel(partner.recommended_tier)}
                </span>
              </span>
            )}
            <span className={`px-2 py-0.5 rounded text-xs font-medium ${actionBadge(partner.partner_action)}`}>
              {fmtLabel(partner.partner_action)}
            </span>
          </div>
        </div>

        {/* KPIs */}
        <div className="grid grid-cols-3 gap-px bg-slate-800 border-b border-slate-800">
          {[
            ["Engagement",   `${partner.engagement_score}/100`],
            ["Performance",  `${partner.performance_score}/100`],
            ["Quota",        `${partner.quota_attainment}%`],
          ].map(([label, val]) => (
            <div key={label} className="bg-slate-900 px-4 py-3 text-center">
              <div className="text-slate-400 text-xs">{label}</div>
              <div className="text-slate-100 font-bold text-base">{val}</div>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["performance", "engagement", "metrics"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium transition-colors ${
                tab === t
                  ? "text-indigo-400 border-b-2 border-indigo-500"
                  : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "performance" ? "Performance" : t === "engagement" ? "Engagement" : "Details"}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "performance" && (
            <div className="space-y-3">
              {[
                { label: "Revenue Won",       value: fmtMoney(partner.closed_won_value), bar: Math.min(100, (partner.closed_won_value / 600000) * 100), color: "bg-emerald-500" },
                { label: "Pipeline Value",    value: fmtMoney(partner.pipeline_value),   bar: Math.min(100, (partner.pipeline_value / 700000) * 100),   color: "bg-indigo-500" },
                { label: "Win Rate",          value: `${(partner.win_rate * 100).toFixed(1)}%`, bar: partner.win_rate * 100, color: "bg-blue-500" },
                { label: "Deals Registered",  value: `${partner.deals_registered} deals`, bar: Math.min(100, (partner.deals_registered / 25) * 100), color: "bg-violet-500" },
              ].map(({ label, value, bar, color }) => (
                <div key={label} className="space-y-1">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-slate-300">{label}</span>
                    <span className="text-slate-100 font-semibold">{value}</span>
                  </div>
                  <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div className={`h-full ${color} rounded-full`} style={{ width: `${bar}%` }} />
                  </div>
                </div>
              ))}
              <div className="flex items-center justify-between py-2 border-t border-slate-800 mt-2">
                <span className="text-slate-400 text-sm">NPS Score</span>
                <span className={`font-bold text-sm ${partner.nps_score >= 30 ? "text-emerald-400" : partner.nps_score >= 0 ? "text-amber-400" : "text-red-400"}`}>
                  {partner.nps_score > 0 ? "+" : ""}{partner.nps_score}
                </span>
              </div>
            </div>
          )}

          {tab === "engagement" && (
            <div className="space-y-3">
              {[
                { label: "Certification Rate",  value: `${(partner.certification_rate * 100).toFixed(0)}%` },
                { label: "Joint Campaigns",     value: `${partner.joint_campaigns}` },
                { label: "Pipeline Contribution", value: `${partner.pipeline_contribution}%` },
                { label: "Deals Closed Won",    value: `${partner.deals_closed_won} of ${partner.deals_registered}` },
              ].map(({ label, value }) => (
                <div key={label} className="flex items-center justify-between py-2 border-b border-slate-800/60 last:border-0">
                  <span className="text-slate-400 text-sm">{label}</span>
                  <span className="text-slate-100 font-semibold text-sm">{value}</span>
                </div>
              ))}
              <div className={`mt-3 p-3 rounded-lg ${healthBg(partner.channel_health)}`}>
                <div className="text-xs font-medium mb-1">Channel Health</div>
                <div className={`font-bold ${healthColor(partner.channel_health)}`}>{fmtLabel(partner.channel_health)}</div>
              </div>
            </div>
          )}

          {tab === "metrics" && (
            <div className="grid grid-cols-2 gap-3">
              {[
                ["Partner Type",   fmtLabel(partner.partner_type)],
                ["Region",         partner.region],
                ["Tenure",         `${partner.years_as_partner.toFixed(1)} years`],
                ["Current Tier",   fmtLabel(partner.current_tier)],
                ["Rec. Tier",      fmtLabel(partner.recommended_tier)],
                ["Engagement",     `${partner.engagement_score}/100`],
              ].map(([label, val]) => (
                <div key={label} className="bg-slate-800/50 rounded-lg p-3">
                  <div className="text-slate-500 text-xs mb-1">{label}</div>
                  <div className="text-slate-100 font-semibold text-sm">{val}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Partner Card ──────────────────────────────────────────────────────────────

function PartnerCard({ partner, onClick }: { partner: Partner; onClick: () => void }) {
  const composite = (partner.engagement_score * 0.4 + partner.performance_score * 0.6);

  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-4 rounded-xl border transition-all hover:border-indigo-500/50 hover:bg-slate-800/80 ${healthBg(partner.channel_health)}`}
    >
      <div className="flex items-start gap-3">
        <PartnerRing score={composite} size={52} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-0.5">
            <span className="text-slate-100 font-semibold text-sm truncate">{partner.partner_name}</span>
            {partner.is_strategic && (
              <span className="px-1 py-0.5 bg-indigo-900/50 text-indigo-300 border border-indigo-700/50 rounded text-[10px] font-medium">
                STRATEGIC
              </span>
            )}
          </div>
          <p className="text-slate-400 text-xs">{fmtLabel(partner.partner_type)} · {partner.region}</p>
          <div className="flex items-center gap-2 mt-1.5 flex-wrap">
            <span className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${tierBadge(partner.current_tier)}`}>
              {fmtLabel(partner.current_tier)}
            </span>
            <span className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${actionBadge(partner.partner_action)}`}>
              {fmtLabel(partner.partner_action)}
            </span>
          </div>
        </div>
        <div className="text-right flex-shrink-0">
          <div className="text-indigo-300 font-bold text-sm">{fmtMoney(partner.closed_won_value)}</div>
          <div className={`text-xs mt-0.5 ${healthColor(partner.channel_health)}`}>{fmtLabel(partner.channel_health)}</div>
        </div>
      </div>

      {/* Score bars */}
      <div className="mt-3 space-y-1.5">
        <div className="flex items-center gap-2">
          <span className="text-slate-600 text-[10px] w-16">Engage</span>
          <div className="flex-1 h-1 bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full bg-violet-500 rounded-full" style={{ width: `${partner.engagement_score}%` }} />
          </div>
          <span className="text-slate-500 text-[10px] w-6 text-right">{Math.round(partner.engagement_score)}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-slate-600 text-[10px] w-16">Perform</span>
          <div className="flex-1 h-1 bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${partner.performance_score}%` }} />
          </div>
          <span className="text-slate-500 text-[10px] w-6 text-right">{Math.round(partner.performance_score)}</span>
        </div>
      </div>
    </button>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function PartnerChannelPage() {
  const [data, setData]         = useState<{ partners: Partner[]; summary: Summary } | null>(null);
  const [loading, setLoading]   = useState(true);
  const [tierFilter, setTierFilter]     = useState("");
  const [healthFilter, setHealthFilter] = useState("");
  const [regionFilter, setRegionFilter] = useState("");
  const [selected, setSelected] = useState<Partner | null>(null);

  async function load() {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        if (tierFilter)   params.set("tier", tierFilter);
        if (healthFilter) params.set("health", healthFilter);
        if (regionFilter) params.set("region", regionFilter);
        const res = await fetch(`/api/partner-channel?${params}`);
        if (res.ok) setData(await res.json());
      } finally {
        setLoading(false);
      }
  }

  useEffect(() => {
    load();
  }, [tierFilter, healthFilter, regionFilter]);

  const s        = data?.summary;
  const partners = data?.partners ?? [];

  const tiers   = ["platinum", "gold", "silver", "bronze", "prospect"];
  const healths = ["excellent", "healthy", "needs_attention", "at_risk", "inactive"];
  const regions = ["EMEA", "APAC", "Americas"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Partner Channel</h1>
          <p className="text-slate-400 text-sm mt-1">Partner health, tier management & channel optimization</p>
        </div>
        <button
          onClick={load}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition-colors"
        >
          Refresh
        </button>
      </div>

      {/* KPI Strip */}
      {s && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { label: "Partners",         value: String(s.total),                       sub: `${s.strategic_count} strategic` },
            { label: "Avg Performance",  value: `${s.avg_performance_score}/100`,      sub: `avg quota ${s.avg_quota_attainment}%` },
            { label: "Top Performers",   value: String(s.top_performer_count),         sub: "excellent + healthy" },
            { label: "Need Attention",   value: String(s.at_risk_count + s.needs_intervention_count), sub: `${s.needs_intervention_count} intervention` },
          ].map(({ label, value, sub }) => (
            <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="text-slate-400 text-xs">{label}</div>
              <div className="text-slate-100 font-bold text-xl mt-1">{value}</div>
              <div className="text-slate-500 text-xs mt-0.5">{sub}</div>
            </div>
          ))}
        </div>
      )}

      {/* Health Distribution */}
      {s && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <h2 className="text-slate-300 text-sm font-semibold mb-3">Channel Health Distribution</h2>
          <HealthDistBar counts={s.health_counts} />
        </div>
      )}

      {/* Filters */}
      <div className="flex gap-2 flex-wrap">
        {/* Tier */}
        <div className="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded-lg px-2 py-1">
          <span className="text-slate-500 text-xs">Tier:</span>
          <div className="flex gap-1">
            {["", ...tiers].map((t) => (
              <button
                key={t}
                onClick={() => setTierFilter(t)}
                className={`px-2 py-0.5 rounded text-xs font-medium transition-colors ${
                  tierFilter === t ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {t ? fmtLabel(t) : "All"}
              </button>
            ))}
          </div>
        </div>

        {/* Health */}
        <div className="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded-lg px-2 py-1">
          <span className="text-slate-500 text-xs">Health:</span>
          <div className="flex gap-1">
            {["", ...healths].map((h) => (
              <button
                key={h}
                onClick={() => setHealthFilter(h)}
                className={`px-2 py-0.5 rounded text-xs font-medium transition-colors ${
                  healthFilter === h ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {h ? fmtLabel(h) : "All"}
              </button>
            ))}
          </div>
        </div>

        {/* Region */}
        <div className="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded-lg px-2 py-1">
          <span className="text-slate-500 text-xs">Region:</span>
          <div className="flex gap-1">
            {["", ...regions].map((r) => (
              <button
                key={r}
                onClick={() => setRegionFilter(r)}
                className={`px-2 py-0.5 rounded text-xs font-medium transition-colors ${
                  regionFilter === r ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {r || "All"}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Partner Cards */}
      {loading ? (
        <div className="flex items-center justify-center py-16">
          <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {partners.map((p) => (
            <PartnerCard key={p.partner_id} partner={p} onClick={() => setSelected(p)} />
          ))}
          {partners.length === 0 && (
            <div className="col-span-full text-center py-12 text-slate-500">
              No partners match the selected filters.
            </div>
          )}
        </div>
      )}

      {/* Actions + Tier Summary */}
      {s && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <h2 className="text-slate-300 text-sm font-semibold mb-3">Recommended Actions</h2>
            <div className="space-y-2">
              {Object.entries(s.action_counts)
                .sort((a, b) => b[1] - a[1])
                .map(([action, count]) => (
                  <div key={action} className="flex items-center justify-between">
                    <span className={`px-2 py-0.5 rounded text-xs font-medium ${actionBadge(action)}`}>
                      {fmtLabel(action)}
                    </span>
                    <span className="text-slate-300 text-sm font-medium">{count}</span>
                  </div>
                ))}
            </div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <h2 className="text-slate-300 text-sm font-semibold mb-3">Tier Distribution</h2>
            <div className="space-y-2">
              {Object.entries(s.tier_counts)
                .sort((a, b) => b[1] - a[1])
                .map(([tier, count]) => (
                  <div key={tier} className="flex items-center justify-between">
                    <span className={`px-2 py-0.5 rounded text-xs font-medium ${tierBadge(tier)}`}>
                      {fmtLabel(tier)}
                    </span>
                    <span className="text-slate-300 text-sm font-medium">{count}</span>
                  </div>
                ))}
            </div>
            <div className="mt-3 pt-3 border-t border-slate-800 grid grid-cols-2 gap-2">
              <div className="bg-slate-800/50 rounded-lg p-2">
                <div className="text-slate-500 text-[10px]">Avg Win Rate</div>
                <div className="text-slate-100 font-bold text-sm">{(s.avg_win_rate * 100).toFixed(1)}%</div>
              </div>
              <div className="bg-slate-800/50 rounded-lg p-2">
                <div className="text-slate-500 text-[10px]">Avg Engagement</div>
                <div className="text-slate-100 font-bold text-sm">{s.avg_engagement_score}/100</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Modal */}
      {selected && <PartnerModal partner={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
