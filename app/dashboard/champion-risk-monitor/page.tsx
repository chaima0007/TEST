"use client";

import { useEffect, useState, useCallback } from "react";

// ── types ────────────────────────────────────────────────────────────────────
interface Deal {
  deal_id: string;
  deal_name: string;
  rep_id: string;
  champion_status: string;
  champion_risk: string;
  influence_level: string;
  champion_action: string;
  engagement_score: number;
  influence_score: number;
  stability_score: number;
  deal_protection_score: number;
  champion_composite: number;
  departure_probability: number;
  deal_at_risk_score: number;
  is_champion_stable: boolean;
  needs_backup_champion: boolean;
  region: string;
}

interface Summary {
  total: number;
  status_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  influence_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_champion_composite: number;
  avg_departure_probability: number;
  stable_count: number;
  backup_needed_count: number;
  avg_engagement_score: number;
  avg_influence_score: number;
  avg_stability_score: number;
  avg_deal_at_risk_score: number;
}

// ── helpers ──────────────────────────────────────────────────────────────────
const STATUS_COLOR: Record<string, string> = {
  active_advocate: "text-emerald-400",
  engaged:         "text-sky-400",
  cooling:         "text-amber-400",
  silent:          "text-orange-400",
  departed:        "text-rose-400",
};
const STATUS_BG: Record<string, string> = {
  active_advocate: "bg-emerald-500/20 border-emerald-500/40",
  engaged:         "bg-sky-500/20 border-sky-500/40",
  cooling:         "bg-amber-500/20 border-amber-500/40",
  silent:          "bg-orange-500/20 border-orange-500/40",
  departed:        "bg-rose-500/20 border-rose-500/40",
};
const RISK_COLOR: Record<string, string> = {
  low:      "text-emerald-400",
  moderate: "text-amber-400",
  high:     "text-orange-400",
  critical: "text-rose-400",
};
const STATUS_ICON: Record<string, string> = {
  active_advocate: "🦁",
  engaged:         "🤝",
  cooling:         "❄️",
  silent:          "🔇",
  departed:        "🚪",
};

function ChampionRing({ score, color }: { score: number; color: string }) {
  const r = 36, circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  return (
    <svg width={88} height={88} viewBox="0 0 88 88">
      <circle cx={44} cy={44} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle
        cx={44} cy={44} r={r} fill="none"
        stroke={color} strokeWidth={8}
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        transform="rotate(-90 44 44)"
      />
      <text x={44} y={49} textAnchor="middle" fill="white" fontSize={14} fontWeight="bold">
        {Math.round(score)}
      </text>
    </svg>
  );
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span><span>{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

function RiskDistBar({ counts }: { counts: Record<string, number> }) {
  const order = ["low", "moderate", "high", "critical"];
  const colors = ["bg-emerald-500", "bg-amber-500", "bg-orange-500", "bg-rose-500"];
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex gap-1 h-3 rounded-full overflow-hidden">
      {order.map((k, i) => (
        <div
          key={k}
          className={colors[i]}
          style={{ width: `${((counts[k] || 0) / total) * 100}%` }}
          title={`${k}: ${counts[k] || 0}`}
        />
      ))}
    </div>
  );
}

// ── DealModal ────────────────────────────────────────────────────────────────
function DealModal({ deal, onClose }: { deal: Deal; onClose: () => void }) {
  const [tab, setTab] = useState<"signals" | "scores" | "actions">("signals");

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);

  const ringColor =
    deal.champion_composite >= 70 ? "#10b981"
    : deal.champion_composite >= 50 ? "#38bdf8"
    : deal.champion_composite >= 30 ? "#f59e0b"
    : "#f43f5e";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* header */}
        <div className="flex items-center gap-4 p-5 border-b border-slate-800">
          <ChampionRing score={deal.champion_composite} color={ringColor} />
          <div className="flex-1 min-w-0">
            <h2 className="text-white font-bold text-lg truncate">{deal.deal_name}</h2>
            <p className="text-slate-400 text-sm">{deal.rep_id} · {deal.region}</p>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${STATUS_BG[deal.champion_status]}`}>
                {STATUS_ICON[deal.champion_status]} {deal.champion_status.replace(/_/g, " ")}
              </span>
              <span className={`text-xs font-semibold ${RISK_COLOR[deal.champion_risk]}`}>
                {deal.champion_risk.toUpperCase()} RISK
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-800">
          {(["signals", "scores", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "signals" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Influence Level", deal.influence_level.replace(/_/g, " ")],
                  ["Departure Prob.", deal.departure_probability.toFixed(0) + "%"],
                  ["Champion Stable", deal.is_champion_stable ? "✅ Yes" : "❌ No"],
                  ["Backup Needed",   deal.needs_backup_champion ? "⚠️ Yes" : "✅ No"],
                ].map(([label, value]) => (
                  <div key={label as string} className="bg-slate-800/60 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{label}</div>
                    <div className="text-white font-semibold mt-0.5">{value}</div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Deal At Risk Score</div>
                <div className="flex items-center gap-3">
                  <span className="text-2xl font-bold text-white">{deal.deal_at_risk_score.toFixed(1)}</span>
                  <div className="flex-1 h-2 bg-slate-700 rounded-full">
                    <div
                      className="h-full rounded-full bg-rose-500"
                      style={{ width: `${deal.deal_at_risk_score}%` }}
                    />
                  </div>
                </div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Engagement"       value={deal.engagement_score}      color="bg-indigo-500" />
              <ScoreBar label="Influence"        value={deal.influence_score}       color="bg-violet-500" />
              <ScoreBar label="Stability"        value={deal.stability_score}       color="bg-sky-500" />
              <ScoreBar label="Deal Protection"  value={deal.deal_protection_score} color="bg-emerald-500" />
            </div>
          )}

          {tab === "actions" && (
            <div className="space-y-3">
              <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-xl p-4">
                <div className="text-xs text-indigo-400 uppercase tracking-wide mb-1">Recommended Action</div>
                <div className="text-white font-bold text-lg capitalize">
                  {deal.champion_action.replace(/_/g, " ")}
                </div>
              </div>
              {deal.champion_status === "departed" && (
                <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-3 text-sm text-rose-300">
                  🚪 Champion departed — escalate to executive immediately
                </div>
              )}
              {deal.needs_backup_champion && (
                <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-3 text-sm text-amber-300">
                  🛡️ Find backup champion — single-threaded deal is high risk
                </div>
              )}
              {deal.is_champion_stable && deal.champion_composite >= 75 && (
                <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-3 text-sm text-emerald-300">
                  🦁 Strong active advocate — leverage champion for exec sponsorship
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── DealCard ─────────────────────────────────────────────────────────────────
function DealCard({ deal, onClick }: { deal: Deal; onClick: () => void }) {
  const ringColor =
    deal.champion_composite >= 70 ? "#10b981"
    : deal.champion_composite >= 50 ? "#38bdf8"
    : deal.champion_composite >= 30 ? "#f59e0b"
    : "#f43f5e";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-indigo-500/50 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3">
        <ChampionRing score={deal.champion_composite} color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-semibold truncate">{deal.deal_name}</div>
          <div className="text-slate-400 text-xs">{deal.rep_id} · {deal.region}</div>
          <div className="flex gap-2 mt-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${STATUS_BG[deal.champion_status]}`}>
              {STATUS_ICON[deal.champion_status]} {deal.champion_status.replace(/_/g, " ")}
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          <div className={`text-sm font-bold ${RISK_COLOR[deal.champion_risk]}`}>
            {deal.departure_probability.toFixed(0)}%
          </div>
          <div className="text-xs text-slate-500">depart</div>
          {deal.needs_backup_champion && (
            <div className="text-xs text-amber-400 mt-1">🛡️ backup</div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── page ─────────────────────────────────────────────────────────────────────
export default function ChampionRiskMonitorPage() {
  const [deals, setDeals]       = useState<Deal[]>([]);
  const [summary, setSummary]   = useState<Summary | null>(null);
  const [loading, setLoading]   = useState(true);
  const [selected, setSelected] = useState<Deal | null>(null);
  const [filterStatus, setFilterStatus] = useState("all");
  const [filterRisk,   setFilterRisk]   = useState("all");
  const [filterRegion, setFilterRegion] = useState("all");

  const load = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (filterStatus !== "all") params.set("status", filterStatus);
    if (filterRisk   !== "all") params.set("risk",   filterRisk);
    if (filterRegion !== "all") params.set("region", filterRegion);
    const res = await fetch(`/api/champion-risk-monitor?${params}`);
    const data = await res.json();
    setDeals(data.deals);
    setSummary(data.summary);
    setLoading(false);
  }, [filterStatus, filterRisk, filterRegion]);

  useEffect(() => { load(); }, [load]);

  const criticalDeals = deals.filter((d) => d.champion_risk === "critical");

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Champion Risk Monitor</h1>
          <p className="text-slate-400 text-sm mt-1">
            Tracks champion engagement, stability, and departure risk before they derail your close
          </p>
        </div>

        {/* critical alert */}
        {criticalDeals.length > 0 && (
          <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-4 flex items-center gap-3">
            <span className="text-2xl">🚪</span>
            <div>
              <div className="text-rose-300 font-semibold">
                {criticalDeals.length} deal{criticalDeals.length > 1 ? "s" : ""} with critical champion risk
              </div>
              <div className="text-rose-400/70 text-xs mt-0.5">
                {criticalDeals.map((d) => d.deal_name).join(" · ")}
              </div>
            </div>
          </div>
        )}

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { label: "Total Deals",     value: summary.total },
              { label: "Stable",          value: summary.stable_count,       color: "text-emerald-400" },
              { label: "Backup Needed",   value: summary.backup_needed_count, color: "text-amber-400" },
              { label: "Avg Composite",   value: summary.avg_champion_composite.toFixed(1), color: "text-indigo-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <div className="text-xs text-slate-400">{label}</div>
                <div className={`text-2xl font-bold mt-1 ${color ?? "text-white"}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* risk dist bar */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-400 mb-2">Champion Risk Distribution</div>
            <RiskDistBar counts={summary.risk_counts} />
            <div className="flex gap-4 mt-2 text-xs text-slate-500">
              {["low","moderate","high","critical"].map((k) => (
                <span key={k} className={RISK_COLOR[k]}>{k}: {summary.risk_counts[k] || 0}</span>
              ))}
            </div>
          </div>
        )}

        {/* filters */}
        <div className="flex flex-wrap gap-2">
          {[
            { label: "All Statuses",    val: "all",            setter: setFilterStatus, current: filterStatus },
            { label: "🦁 Advocate",     val: "active_advocate", setter: setFilterStatus, current: filterStatus },
            { label: "🤝 Engaged",      val: "engaged",         setter: setFilterStatus, current: filterStatus },
            { label: "❄️ Cooling",       val: "cooling",         setter: setFilterStatus, current: filterStatus },
            { label: "🔇 Silent",        val: "silent",          setter: setFilterStatus, current: filterStatus },
            { label: "🚪 Departed",      val: "departed",        setter: setFilterStatus, current: filterStatus },
          ].map(({ label, val, setter, current }) => (
            <button
              key={val}
              onClick={() => setter(val)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                current === val
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {label}
            </button>
          ))}
          <select
            value={filterRegion}
            onChange={(e) => setFilterRegion(e.target.value)}
            className="px-3 py-1.5 rounded-lg text-xs bg-slate-800 text-slate-300 border border-slate-700"
          >
            <option value="all">All Regions</option>
            {["NAMER","EMEA","APAC","LATAM"].map((r) => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>

        {/* deals grid */}
        {loading ? (
          <div className="text-slate-400 text-center py-16">Loading champion data…</div>
        ) : deals.length === 0 ? (
          <div className="text-slate-500 text-center py-16">No deals match your filters.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {deals.map((d) => (
              <DealCard key={d.deal_id} deal={d} onClick={() => setSelected(d)} />
            ))}
          </div>
        )}

        {/* avg score bars */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="text-sm font-semibold text-slate-300 mb-4">Average Score Breakdown</div>
            <div className="space-y-3">
              <ScoreBar label="Engagement"      value={summary.avg_engagement_score}   color="bg-indigo-500" />
              <ScoreBar label="Influence"       value={summary.avg_influence_score}    color="bg-violet-500" />
              <ScoreBar label="Stability"       value={summary.avg_stability_score}    color="bg-sky-500" />
              <ScoreBar label="Deal at Risk"    value={summary.avg_deal_at_risk_score} color="bg-rose-500" />
            </div>
          </div>
        )}
      </div>

      {selected && <DealModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
