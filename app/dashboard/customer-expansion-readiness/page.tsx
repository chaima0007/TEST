"use client";

import { useState, useEffect, useCallback } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

interface AccountData {
  account_id: string;
  account_name: string;
  industry: string;
  region: string;
  expansion_readiness_tier: string;
  expansion_motion: string;
  expansion_priority: string;
  expansion_action: string;
  product_depth_score: number;
  relationship_strength_score: number;
  financial_health_score: number;
  timing_score: number;
  expansion_readiness_score: number;
  estimated_expansion_arr: number;
  expansion_confidence_score: number;
  is_expansion_ready: boolean;
  needs_success_intervention: boolean;
  current_mrr: number;
  contract_end_months: number;
  seats_used: number;
  seats_purchased: number;
  max_seats_available: number;
  feature_adoption_rate: number;
  nps_score: number;
  avg_mau_pct: number;
}

interface Summary {
  total: number;
  tier_counts: Record<string, number>;
  motion_counts: Record<string, number>;
  priority_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_expansion_readiness_score: number;
  total_estimated_expansion_arr: number;
  ready_count: number;
  intervention_needed_count: number;
  avg_product_depth_score: number;
  avg_relationship_strength_score: number;
  avg_timing_score: number;
  avg_expansion_confidence_score: number;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

const TIER_COLOR: Record<string, string> = {
  not_ready: "text-slate-400",
  building:  "text-amber-400",
  ready:     "text-blue-400",
  primed:    "text-emerald-400",
};

const TIER_BG: Record<string, string> = {
  not_ready: "bg-slate-800/60 border-slate-700/40",
  building:  "bg-amber-900/30 border-amber-700/40",
  ready:     "bg-blue-900/30 border-blue-700/40",
  primed:    "bg-emerald-900/30 border-emerald-700/40",
};

const MOTION_COLOR: Record<string, string> = {
  seat_expansion: "text-violet-400",
  upsell_tier:    "text-blue-400",
  cross_sell:     "text-cyan-400",
  renewal_lock:   "text-amber-400",
  hold:           "text-slate-500",
};

const ACTION_BADGE: Record<string, string> = {
  maintain:        "bg-slate-800 text-slate-400 border-slate-700",
  nurture:         "bg-amber-900/50 text-amber-300 border-amber-700/50",
  engage:          "bg-blue-900/50 text-blue-300 border-blue-700/50",
  close_expansion: "bg-emerald-900/50 text-emerald-300 border-emerald-700/50",
};

function fmt$(v: number) {
  return v >= 1_000_000
    ? `$${(v / 1_000_000).toFixed(1)}M`
    : v >= 1_000
    ? `$${(v / 1_000).toFixed(0)}K`
    : `$${v.toFixed(0)}`;
}

// ── ReadinessRing SVG ─────────────────────────────────────────────────────────

function ReadinessRing({ score, tier }: { score: number; tier: string }) {
  const r = 28, cx = 36, cy = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * Math.min(1, score / 100);
  const color =
    tier === "primed"    ? "#34d399" :
    tier === "ready"     ? "#60a5fa" :
    tier === "building"  ? "#fbbf24" : "#475569";

  return (
    <svg width="72" height="72" viewBox="0 0 72 72">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth="6" />
      <circle
        cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth="6"
        strokeLinecap="round"
        strokeDasharray={`${fill} ${circ}`}
        transform={`rotate(-90 ${cx} ${cy})`}
        style={{ transition: "stroke-dasharray .5s ease" }}
      />
      <text x={cx} y={cy + 5} textAnchor="middle" fill="white" fontSize="13" fontWeight="700">
        {score.toFixed(0)}
      </text>
    </svg>
  );
}

// ── TierDistBar ───────────────────────────────────────────────────────────────

function TierDistBar({ counts }: { counts: Record<string, number> }) {
  const order = ["primed", "ready", "building", "not_ready"];
  const colors = ["#34d399", "#60a5fa", "#fbbf24", "#475569"];
  const total = Object.values(counts).reduce((s, v) => s + v, 0) || 1;
  return (
    <div className="space-y-2">
      <div className="flex h-3 rounded-full overflow-hidden">
        {order.map((k, i) => {
          const w = ((counts[k] || 0) / total) * 100;
          return w > 0 ? (
            <div key={k} style={{ width: `${w}%`, background: colors[i] }} title={`${k}: ${counts[k]}`} />
          ) : null;
        })}
      </div>
      <div className="flex flex-wrap gap-x-4 gap-y-1">
        {order.map((k, i) =>
          (counts[k] || 0) > 0 ? (
            <span key={k} className="flex items-center gap-1 text-xs text-slate-400">
              <span className="w-2 h-2 rounded-full inline-block" style={{ background: colors[i] }} />
              {k.replace("_", " ")} ({counts[k]})
            </span>
          ) : null
        )}
      </div>
    </div>
  );
}

// ── AccountModal ──────────────────────────────────────────────────────────────

function AccountModal({ account, onClose }: { account: AccountData; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "usage" | "actions">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", h);
    return () => document.removeEventListener("keydown", h);
  }, [onClose]);

  const bar = (label: string, val: number) => {
    const color = val >= 70 ? "bg-emerald-500" : val >= 45 ? "bg-blue-500" : "bg-amber-500";
    return (
      <div>
        <div className="flex justify-between text-xs mb-1">
          <span className="text-slate-400">{label}</span>
          <span className="text-white font-medium">{val.toFixed(1)}</span>
        </div>
        <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
          <div className={`h-full rounded-full ${color} transition-all duration-500`} style={{ width: `${val}%` }} />
        </div>
      </div>
    );
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/70 backdrop-blur-sm" />
      <div
        className="relative bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-5 border-b border-slate-800">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h2 className="text-white font-bold text-lg">{account.account_name}</h2>
              <p className="text-slate-400 text-sm">{account.industry} · {account.region}</p>
            </div>
            <div className="flex items-center gap-2">
              <span className={`px-2 py-0.5 rounded-full text-xs font-semibold border ${ACTION_BADGE[account.expansion_action]}`}>
                {account.expansion_action.replace("_", " ")}
              </span>
              <button onClick={onClose} className="text-slate-500 hover:text-white transition-colors text-xl leading-none">×</button>
            </div>
          </div>
          <div className="flex gap-2 mt-3">
            {(["scores", "usage", "actions"] as const).map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`px-3 py-1 rounded-lg text-xs font-medium transition-colors capitalize ${tab === t ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white hover:bg-slate-800"}`}
              >
                {t === "scores" ? "Readiness Scores" : t === "usage" ? "Usage & Health" : "Expansion Plan"}
              </button>
            ))}
          </div>
        </div>

        <div className="p-5 overflow-y-auto max-h-[60vh]">
          {tab === "scores" && (
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <ReadinessRing score={account.expansion_readiness_score} tier={account.expansion_readiness_tier} />
                <div className="flex-1 space-y-1">
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Tier</span>
                    <span className={`font-semibold capitalize ${TIER_COLOR[account.expansion_readiness_tier]}`}>
                      {account.expansion_readiness_tier.replace("_", " ")}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Motion</span>
                    <span className={`font-medium capitalize ${MOTION_COLOR[account.expansion_motion]}`}>
                      {account.expansion_motion.replace("_", " ")}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Est. Expansion ARR</span>
                    <span className="text-emerald-400 font-bold">{account.estimated_expansion_arr > 0 ? fmt$(account.estimated_expansion_arr) : "—"}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Confidence</span>
                    <span className="text-white font-medium">{account.expansion_confidence_score.toFixed(0)}%</span>
                  </div>
                </div>
              </div>
              <div className="space-y-3">
                {bar("Product Depth Score", account.product_depth_score)}
                {bar("Relationship Strength", account.relationship_strength_score)}
                {bar("Financial Health", account.financial_health_score)}
                {bar("Timing Score", account.timing_score)}
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className={`rounded-lg p-3 border ${account.is_expansion_ready ? "bg-emerald-900/30 border-emerald-700/40" : "bg-slate-800/50 border-slate-700/40"}`}>
                  <p className="text-xs text-slate-500">Expansion Ready</p>
                  <p className={`text-sm font-semibold mt-0.5 ${account.is_expansion_ready ? "text-emerald-400" : "text-slate-400"}`}>
                    {account.is_expansion_ready ? "Yes" : "Not yet"}
                  </p>
                </div>
                <div className={`rounded-lg p-3 border ${account.needs_success_intervention ? "bg-red-900/30 border-red-700/40" : "bg-slate-800/50 border-slate-700/40"}`}>
                  <p className="text-xs text-slate-500">CS Intervention</p>
                  <p className={`text-sm font-semibold mt-0.5 ${account.needs_success_intervention ? "text-red-400" : "text-emerald-400"}`}>
                    {account.needs_success_intervention ? "Required" : "Not needed"}
                  </p>
                </div>
              </div>
            </div>
          )}

          {tab === "usage" && (
            <div className="space-y-4">
              <div className="grid grid-cols-3 gap-3">
                <div className="bg-slate-800/50 border border-slate-700/40 rounded-lg p-3 text-center">
                  <p className="text-xs text-slate-500">Current MRR</p>
                  <p className="text-lg font-bold text-white mt-1">{fmt$(account.current_mrr)}</p>
                </div>
                <div className="bg-slate-800/50 border border-slate-700/40 rounded-lg p-3 text-center">
                  <p className="text-xs text-slate-500">Seats Used</p>
                  <p className="text-lg font-bold text-white mt-1">{account.seats_used}/{account.seats_purchased}</p>
                </div>
                <div className="bg-slate-800/50 border border-slate-700/40 rounded-lg p-3 text-center">
                  <p className="text-xs text-slate-500">Renewal In</p>
                  <p className={`text-lg font-bold mt-1 ${account.contract_end_months <= 4 ? "text-red-400" : account.contract_end_months <= 8 ? "text-amber-400" : "text-white"}`}>
                    {account.contract_end_months}mo
                  </p>
                </div>
              </div>
              <div className="space-y-3">
                {[
                  { label: "Feature Adoption Rate", val: account.feature_adoption_rate },
                  { label: "Monthly Active Users", val: account.avg_mau_pct },
                  { label: "NPS Score (normalized)", val: (account.nps_score + 100) / 2 },
                ].map((m) => bar(m.label, m.val))}
              </div>
            </div>
          )}

          {tab === "actions" && (
            <div className="space-y-3">
              <div className={`rounded-lg p-4 border ${ACTION_BADGE[account.expansion_action]}`}>
                <p className="text-xs font-semibold uppercase tracking-wider opacity-70 mb-1">Recommended Action</p>
                <p className="text-lg font-bold capitalize">{account.expansion_action.replace("_", " ")}</p>
                <p className="text-xs opacity-60 mt-1">Motion: {account.expansion_motion.replace("_", " ")} · Priority: {account.expansion_priority}</p>
              </div>
              {account.expansion_action === "close_expansion" && (
                <ul className="space-y-2 text-sm text-slate-300">
                  <li className="flex gap-2"><span className="text-emerald-400">•</span> Schedule expansion proposal presentation this week</li>
                  <li className="flex gap-2"><span className="text-emerald-400">•</span> Prepare ROI-focused business case for {account.expansion_motion.replace("_", " ")}</li>
                  <li className="flex gap-2"><span className="text-emerald-400">•</span> Engage executive sponsor for contract amendment</li>
                  <li className="flex gap-2"><span className="text-emerald-400">•</span> Lock in expansion before renewal window closes</li>
                </ul>
              )}
              {account.expansion_action === "engage" && (
                <ul className="space-y-2 text-sm text-slate-300">
                  <li className="flex gap-2"><span className="text-blue-400">•</span> Schedule discovery call to identify expansion scope</li>
                  <li className="flex gap-2"><span className="text-blue-400">•</span> Share case studies relevant to {account.expansion_motion.replace("_", " ")} motion</li>
                  <li className="flex gap-2"><span className="text-blue-400">•</span> Run QBR focused on value realized and next goals</li>
                </ul>
              )}
              {account.expansion_action === "nurture" && (
                <ul className="space-y-2 text-sm text-slate-300">
                  <li className="flex gap-2"><span className="text-amber-400">•</span> Focus on customer success and product adoption first</li>
                  <li className="flex gap-2"><span className="text-amber-400">•</span> Increase feature adoption through training/enablement</li>
                  <li className="flex gap-2"><span className="text-amber-400">•</span> Re-evaluate expansion readiness in 60-90 days</li>
                  {account.needs_success_intervention && (
                    <li className="flex gap-2"><span className="text-red-400">•</span> CS escalation required — address health issues first</li>
                  )}
                </ul>
              )}
              {account.expansion_action === "maintain" && (
                <ul className="space-y-2 text-sm text-slate-300">
                  <li className="flex gap-2"><span className="text-slate-400">•</span> Account not yet ready for expansion outreach</li>
                  <li className="flex gap-2"><span className="text-slate-400">•</span> Continue standard success cadence and monitoring</li>
                  <li className="flex gap-2"><span className="text-slate-400">•</span> Revisit when product depth score exceeds 50</li>
                </ul>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── AccountCard ───────────────────────────────────────────────────────────────

function AccountCard({ account, onClick }: { account: AccountData; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className={`rounded-xl border p-4 cursor-pointer hover:border-slate-600 transition-all ${TIER_BG[account.expansion_readiness_tier]}`}
    >
      <div className="flex items-start justify-between gap-2 mb-3">
        <div>
          <p className="text-white font-semibold text-sm">{account.account_name}</p>
          <p className="text-slate-500 text-xs">{account.industry} · {account.region}</p>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className={`text-xs font-bold uppercase ${TIER_COLOR[account.expansion_readiness_tier]}`}>
            {account.expansion_readiness_tier.replace("_", " ")}
          </span>
          <span className={`text-xs capitalize ${MOTION_COLOR[account.expansion_motion]}`}>
            {account.expansion_motion.replace("_", " ")}
          </span>
        </div>
      </div>

      <div className="flex items-center gap-3 mb-3">
        <ReadinessRing score={account.expansion_readiness_score} tier={account.expansion_readiness_tier} />
        <div className="flex-1 space-y-1">
          <div className="flex justify-between text-xs">
            <span className="text-slate-500">Product Depth</span>
            <span className="text-slate-300">{account.product_depth_score.toFixed(0)}</span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-slate-500">Relationship</span>
            <span className="text-slate-300">{account.relationship_strength_score.toFixed(0)}</span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-slate-500">Timing</span>
            <span className="text-slate-300">{account.timing_score.toFixed(0)}</span>
          </div>
          {account.estimated_expansion_arr > 0 && (
            <div className="flex justify-between text-xs">
              <span className="text-slate-500">Est. ARR</span>
              <span className="text-emerald-400 font-medium">{fmt$(account.estimated_expansion_arr)}</span>
            </div>
          )}
        </div>
      </div>

      <div className="flex items-center justify-between">
        <span className={`text-xs px-2 py-0.5 rounded-full border ${ACTION_BADGE[account.expansion_action]}`}>
          {account.expansion_action.replace("_", " ")}
        </span>
        <div className="flex gap-2">
          {account.is_expansion_ready && (
            <span className="text-xs text-emerald-400 font-medium">✓ Ready</span>
          )}
          {account.needs_success_intervention && (
            <span className="text-xs text-red-400 font-bold">⚠ CS Alert</span>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function CustomerExpansionReadinessPage() {
  const [data, setData] = useState<{ accounts: AccountData[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<AccountData | null>(null);
  const [filterTier, setFilterTier]     = useState("all");
  const [filterMotion, setFilterMotion] = useState("all");
  const [filterRegion, setFilterRegion] = useState("all");

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filterTier !== "all")   params.set("tier", filterTier);
      if (filterMotion !== "all") params.set("motion", filterMotion);
      if (filterRegion !== "all") params.set("region", filterRegion);
      const res = await fetch(`/api/customer-expansion-readiness?${params}`);
      if (res.ok) setData(await res.json());
    } catch {}
    setLoading(false);
  }, [filterTier, filterMotion, filterRegion]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const s = data?.summary;
  const tierOrder = ["primed", "ready", "building", "not_ready"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Customer Expansion Readiness</h1>
          <p className="text-slate-400 text-sm mt-1">Score existing accounts for upsell, cross-sell, and seat expansion opportunities</p>
        </div>

        {/* KPI Strip */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Accounts Analyzed", value: s?.total ?? "—", sub: "in scope" },
            { label: "Expansion Ready", value: s?.ready_count ?? "—", sub: "primed + ready", green: true },
            { label: "CS Intervention", value: s?.intervention_needed_count ?? "—", sub: "health alert", danger: (s?.intervention_needed_count ?? 0) > 0 },
            { label: "Total Expansion ARR", value: s ? fmt$(s.total_estimated_expansion_arr) : "—", sub: "estimated pipeline", green: true },
          ].map((k) => (
            <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <p className="text-slate-500 text-xs">{k.label}</p>
              <p className={`text-2xl font-bold mt-1 ${k.danger ? "text-red-400" : k.green ? "text-emerald-400" : "text-white"}`}>
                {k.value}
              </p>
              <p className="text-slate-600 text-xs mt-0.5">{k.sub}</p>
            </div>
          ))}
        </div>

        {/* Score Averages */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Avg Readiness Score", value: s?.avg_expansion_readiness_score.toFixed(1) ?? "—" },
            { label: "Avg Product Depth", value: s?.avg_product_depth_score.toFixed(1) ?? "—" },
            { label: "Avg Relationship Strength", value: s?.avg_relationship_strength_score.toFixed(1) ?? "—" },
            { label: "Avg Confidence", value: s?.avg_expansion_confidence_score.toFixed(1) ?? "—" },
          ].map((k) => (
            <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <p className="text-slate-500 text-xs">{k.label}</p>
              <p className="text-xl font-bold text-white mt-1">{k.value}</p>
            </div>
          ))}
        </div>

        {/* Tier Distribution */}
        {s && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-3">Expansion Readiness Distribution</h2>
            <TierDistBar counts={s.tier_counts} />
          </div>
        )}

        {/* Filters */}
        <div className="flex flex-wrap gap-3">
          <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-lg p-1">
            {["all", "primed", "ready", "building", "not_ready"].map((v) => (
              <button
                key={v}
                onClick={() => setFilterTier(v)}
                className={`px-3 py-1 rounded text-xs font-medium transition-colors ${filterTier === v ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"}`}
              >
                {v === "all" ? "All Tiers" : v.replace("_", " ")}
              </button>
            ))}
          </div>
          <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-lg p-1">
            {["all", "seat_expansion", "upsell_tier", "cross_sell", "renewal_lock", "hold"].map((v) => (
              <button
                key={v}
                onClick={() => setFilterMotion(v)}
                className={`px-3 py-1 rounded text-xs font-medium transition-colors ${filterMotion === v ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"}`}
              >
                {v === "all" ? "All Motions" : v.replace("_", " ")}
              </button>
            ))}
          </div>
          <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-lg p-1">
            {["all", "NAMER", "EMEA", "APAC", "LATAM"].map((v) => (
              <button
                key={v}
                onClick={() => setFilterRegion(v)}
                className={`px-3 py-1 rounded text-xs font-medium transition-colors ${filterRegion === v ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"}`}
              >
                {v === "all" ? "All Regions" : v}
              </button>
            ))}
          </div>
        </div>

        {/* Account grid */}
        {loading ? (
          <div className="text-center py-12 text-slate-500">Loading expansion readiness data...</div>
        ) : (
          <>
            {data && data.accounts.filter((a) => a.expansion_action === "close_expansion").length > 0 && (
              <div className="bg-emerald-950/40 border border-emerald-800/50 rounded-xl p-4 flex items-center gap-3">
                <span className="text-emerald-400 text-xl">💡</span>
                <p className="text-emerald-300 text-sm font-medium">
                  {data.accounts.filter((a) => a.expansion_action === "close_expansion").length} account(s) are primed for expansion — take action this week.
                </p>
              </div>
            )}
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
              {data?.accounts
                .slice()
                .sort((a, b) => tierOrder.indexOf(a.expansion_readiness_tier) - tierOrder.indexOf(b.expansion_readiness_tier))
                .map((acc) => (
                  <AccountCard key={acc.account_id} account={acc} onClick={() => setSelected(acc)} />
                ))}
            </div>
            {data?.accounts.length === 0 && (
              <p className="text-center text-slate-500 py-8">No accounts match current filters.</p>
            )}
          </>
        )}
      </div>

      {selected && <AccountModal account={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
