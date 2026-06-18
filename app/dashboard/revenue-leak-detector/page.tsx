"use client";

import { useEffect, useState, useCallback } from "react";

interface Account {
  account_id: string;
  account_name: string;
  csm_id: string;
  leak_severity: string;
  leak_pattern: string;
  retention_outlook: string;
  leak_action: string;
  discount_risk_score: number;
  renewal_risk_score: number;
  expansion_health_score: number;
  relationship_score: number;
  leak_composite: number;
  estimated_arr_at_risk: number;
  arr_expansion_potential: number;
  is_leaking: boolean;
  needs_executive_save: boolean;
  current_arr: number;
  region: string;
}

interface Summary {
  total: number;
  severity_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  outlook_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_leak_composite: number;
  total_arr_at_risk: number;
  leaking_count: number;
  executive_save_count: number;
  avg_discount_risk_score: number;
  avg_renewal_risk_score: number;
  avg_expansion_health_score: number;
  avg_relationship_score: number;
}

const SEVERITY_COLOR: Record<string, string> = {
  critical:    "#f87171",
  significant: "#fb923c",
  moderate:    "#facc15",
  contained:   "#34d399",
};

const SEVERITY_BG: Record<string, string> = {
  critical:    "bg-red-500/20 border-red-500/40",
  significant: "bg-orange-500/20 border-orange-500/40",
  moderate:    "bg-yellow-500/20 border-yellow-500/40",
  contained:   "bg-emerald-500/20 border-emerald-500/40",
};

const PATTERN_ICONS: Record<string, string> = {
  healthy:          "✅",
  discount_creep:   "📉",
  renewal_risk:     "⏰",
  expansion_stall:  "🚧",
  champion_erosion: "👤",
  multi_leak:       "🚨",
};

const ACTION_LABELS: Record<string, string> = {
  monitor:           "Monitor",
  protect_expansion: "Protect Expansion",
  retention_play:    "Retention Play",
  executive_save:    "Executive Save",
};

function LeakRing({ composite, severity }: { composite: number; severity: string }) {
  const r = 52;
  const circ = 2 * Math.PI * r;
  const fill = (composite / 100) * circ;
  const color = SEVERITY_COLOR[severity] || "#64748b";
  return (
    <svg width="128" height="128" viewBox="0 0 128 128">
      <circle cx="64" cy="64" r={r} fill="none" stroke="#1e293b" strokeWidth="12" />
      <circle
        cx="64" cy="64" r={r} fill="none"
        stroke={color} strokeWidth="12"
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        transform="rotate(-90 64 64)"
      />
      <text x="64" y="60" textAnchor="middle" fill={color} fontSize="22" fontWeight="bold">{composite}</text>
      <text x="64" y="78" textAnchor="middle" fill="#94a3b8" fontSize="10">Leak Risk</text>
    </svg>
  );
}

function ScoreBar({ label, value, color, invert }: { label: string; value: number; color: string; invert?: boolean }) {
  const display = invert ? 100 - value : value;
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-slate-400">{label}</span>
        <span className="text-slate-200 font-medium">{value}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all duration-700" style={{ width: `${display}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

function SeverityDistBar({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  const order = ["critical", "significant", "moderate", "contained"];
  return (
    <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
      {order.map((k) =>
        (counts[k] || 0) > 0 ? (
          <div
            key={k}
            title={`${k}: ${counts[k]}`}
            style={{ width: `${((counts[k] || 0) / total) * 100}%`, backgroundColor: SEVERITY_COLOR[k] }}
          />
        ) : null
      )}
    </div>
  );
}

function AccountModal({ account, onClose }: { account: Account; onClose: () => void }) {
  const [tab, setTab] = useState<"signals" | "scores" | "actions">("signals");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-5 border-b border-slate-800">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h2 className="text-slate-100 font-semibold text-lg leading-tight">
                {PATTERN_ICONS[account.leak_pattern]} {account.account_name}
              </h2>
              <p className="text-slate-400 text-sm mt-0.5">
                {account.csm_id} · {account.region} · ${(account.current_arr / 1000).toFixed(0)}K ARR
              </p>
            </div>
            <span
              className={`text-xs font-bold uppercase px-2 py-1 rounded-full border ${SEVERITY_BG[account.leak_severity]}`}
              style={{ color: SEVERITY_COLOR[account.leak_severity] }}
            >
              {account.leak_severity}
            </span>
          </div>
          <div className="flex gap-2 mt-4">
            {(["signals", "scores", "actions"] as const).map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-colors ${
                  tab === t ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {t.charAt(0).toUpperCase() + t.slice(1)}
              </button>
            ))}
          </div>
        </div>

        <div className="p-5 space-y-4">
          {tab === "signals" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Pattern", `${PATTERN_ICONS[account.leak_pattern]} ${account.leak_pattern.replace(/_/g, " ")}`],
                  ["Outlook", account.retention_outlook.replace(/_/g, " ")],
                  ["ARR at Risk", `$${(account.estimated_arr_at_risk / 1000).toFixed(0)}K`],
                  ["Expansion Pot.", `$${(account.arr_expansion_potential / 1000).toFixed(0)}K`],
                ].map(([label, value]) => (
                  <div key={label} className="bg-slate-800/60 rounded-xl p-3">
                    <p className="text-xs text-slate-500">{label}</p>
                    <p className="text-sm font-semibold text-slate-100 capitalize mt-0.5">{value}</p>
                  </div>
                ))}
              </div>
              <div className="flex gap-2 flex-wrap">
                {account.is_leaking && (
                  <span className="text-xs bg-orange-500/15 text-orange-400 border border-orange-500/30 rounded-lg px-2 py-1">
                    💧 Leaking ARR
                  </span>
                )}
                {account.needs_executive_save && (
                  <span className="text-xs bg-red-500/15 text-red-400 border border-red-500/30 rounded-lg px-2 py-1">
                    🚨 Executive Save
                  </span>
                )}
              </div>
            </>
          )}
          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Discount Risk" value={account.discount_risk_score} color="#f87171" />
              <ScoreBar label="Renewal Risk" value={account.renewal_risk_score} color="#fb923c" />
              <ScoreBar label="Expansion Health" value={account.expansion_health_score} color="#34d399" />
              <ScoreBar label="Relationship Health" value={account.relationship_score} color="#818cf8" />
              <div className="pt-2 border-t border-slate-800">
                <ScoreBar label="Leak Composite" value={account.leak_composite} color={SEVERITY_COLOR[account.leak_severity]} />
              </div>
            </div>
          )}
          {tab === "actions" && (
            <div className="space-y-3">
              <div className="bg-slate-800/60 rounded-xl p-4">
                <p className="text-xs text-slate-500 mb-1">Recommended Action</p>
                <p className="text-indigo-300 font-semibold">{ACTION_LABELS[account.leak_action] || account.leak_action}</p>
              </div>
              {account.leak_action === "executive_save" && (
                <p className="bg-red-500/10 border border-red-500/20 rounded-lg p-3 text-red-300 text-xs">
                  Immediately involve VP/CRO. Assign a dedicated executive sponsor. Schedule an emergency QBR within 10 business days.
                </p>
              )}
              {account.leak_action === "retention_play" && (
                <p className="bg-orange-500/10 border border-orange-500/20 rounded-lg p-3 text-orange-300 text-xs">
                  Run a formal retention playbook. Identify the root cause of ARR risk and address it with a success plan review.
                </p>
              )}
              {account.leak_action === "protect_expansion" && (
                <p className="bg-yellow-500/10 border border-yellow-500/20 rounded-lg p-3 text-yellow-300 text-xs">
                  Focus on feature adoption and utilization before attempting expansion. Increase engagement cadence with the champion.
                </p>
              )}
              {account.leak_action === "monitor" && (
                <p className="bg-emerald-500/10 border border-emerald-500/20 rounded-lg p-3 text-emerald-300 text-xs">
                  Healthy account. Maintain regular check-ins and look for expansion opportunities to grow ARR.
                </p>
              )}
            </div>
          )}
        </div>

        <div className="p-4 border-t border-slate-800">
          <button onClick={onClose} className="w-full py-2 text-sm text-slate-400 hover:text-slate-200 transition-colors">
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

function AccountCard({ account, onClick }: { account: Account; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className={`bg-slate-900 border rounded-2xl p-4 cursor-pointer hover:border-indigo-500/50 transition-all ${SEVERITY_BG[account.leak_severity]}`}
    >
      <div className="flex items-start justify-between gap-2 mb-3">
        <div className="min-w-0">
          <p className="text-slate-100 font-semibold text-sm truncate">
            {PATTERN_ICONS[account.leak_pattern]} {account.account_name}
          </p>
          <p className="text-slate-500 text-xs mt-0.5">{account.region} · {account.csm_id}</p>
        </div>
        <span
          className="text-xs font-bold uppercase shrink-0"
          style={{ color: SEVERITY_COLOR[account.leak_severity] }}
        >
          {account.leak_severity}
        </span>
      </div>

      <div className="flex items-center gap-3 mb-3">
        <LeakRing composite={account.leak_composite} severity={account.leak_severity} />
        <div className="flex-1 space-y-2 min-w-0">
          <ScoreBar label="Discount Risk" value={account.discount_risk_score} color="#f87171" />
          <ScoreBar label="Renewal Risk" value={account.renewal_risk_score} color="#fb923c" />
          <ScoreBar label="Exp. Health" value={account.expansion_health_score} color="#34d399" />
          <ScoreBar label="Relationship" value={account.relationship_score} color="#818cf8" />
        </div>
      </div>

      <div className="flex items-center justify-between text-xs">
        <span className="text-red-400 font-medium">
          -${(account.estimated_arr_at_risk / 1000).toFixed(0)}K at risk
        </span>
        <span className="text-emerald-400 font-medium">
          +${(account.arr_expansion_potential / 1000).toFixed(0)}K potential
        </span>
      </div>
      <div className="flex gap-1 mt-2 flex-wrap">
        {account.is_leaking && (
          <span className="text-xs bg-orange-500/15 text-orange-400 rounded px-1.5 py-0.5">💧 Leaking</span>
        )}
        {account.needs_executive_save && (
          <span className="text-xs bg-red-500/15 text-red-400 rounded px-1.5 py-0.5">🚨 Exec Save</span>
        )}
        <span className="text-xs bg-slate-700/60 text-slate-400 rounded px-1.5 py-0.5">
          ${(account.current_arr / 1000).toFixed(0)}K ARR
        </span>
      </div>
    </div>
  );
}

export default function RevenueLeakDetectorPage() {
  const [data, setData] = useState<{ accounts: Account[]; summary: Summary } | null>(null);
  const [selected, setSelected] = useState<Account | null>(null);
  const [filterSeverity, setFilterSeverity] = useState("all");
  const [filterPattern, setFilterPattern] = useState("all");

  const load = useCallback(async () => {
    const params = new URLSearchParams();
    if (filterSeverity !== "all") params.set("severity", filterSeverity);
    if (filterPattern !== "all")  params.set("pattern", filterPattern);
    const res = await fetch(`/api/revenue-leak-detector?${params}`);
    setData(await res.json());
  }, [filterSeverity, filterPattern]);

  useEffect(() => { load(); }, [load]);

  const s = data?.summary;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        <div>
          <h1 className="text-2xl font-bold text-slate-100">Revenue Leak Detector</h1>
          <p className="text-slate-400 text-sm mt-1">Identify ARR silently eroding through discount creep, renewal risk, expansion stall, and champion loss</p>
        </div>

        {s && s.executive_save_count > 0 && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 flex items-center gap-3">
            <span className="text-2xl">💸</span>
            <div>
              <p className="text-red-300 font-semibold">
                {s.executive_save_count} {s.executive_save_count === 1 ? "account" : "accounts"} require executive-level save intervention
              </p>
              <p className="text-red-400/80 text-xs mt-0.5">
                Total ARR at risk: ${s ? (s.total_arr_at_risk / 1e6).toFixed(1) : "—"}M across all accounts
              </p>
            </div>
          </div>
        )}

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {[
            { label: "Total Accounts", value: s?.total ?? "—", sub: "monitored" },
            { label: "Avg Leak Risk", value: s ? `${s.avg_leak_composite}` : "—", sub: "composite score" },
            { label: "Leaking ARR", value: s?.leaking_count ?? "—", sub: "accounts" },
            { label: "Total ARR at Risk", value: s ? `$${(s.total_arr_at_risk / 1e6).toFixed(1)}M` : "—", sub: "in jeopardy" },
          ].map(({ label, value, sub }) => (
            <div key={label} className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
              <p className="text-xs text-slate-500">{label}</p>
              <p className="text-2xl font-bold text-slate-100 mt-1">{value}</p>
              <p className="text-xs text-slate-500 mt-0.5">{sub}</p>
            </div>
          ))}
        </div>

        {s && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
              <h3 className="text-sm font-semibold text-slate-300 mb-3">Severity Distribution</h3>
              <SeverityDistBar counts={s.severity_counts} />
              <div className="flex flex-wrap gap-x-4 gap-y-1 mt-3">
                {Object.entries(s.severity_counts).map(([k, v]) => (
                  <span key={k} className="text-xs" style={{ color: SEVERITY_COLOR[k] || "#94a3b8" }}>
                    {k}: {v}
                  </span>
                ))}
              </div>
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
              <h3 className="text-sm font-semibold text-slate-300 mb-3">Avg Health Scores</h3>
              <div className="space-y-2">
                <ScoreBar label="Discount Risk" value={s.avg_discount_risk_score} color="#f87171" />
                <ScoreBar label="Renewal Risk" value={s.avg_renewal_risk_score} color="#fb923c" />
                <ScoreBar label="Expansion Health" value={s.avg_expansion_health_score} color="#34d399" />
                <ScoreBar label="Relationship Health" value={s.avg_relationship_score} color="#818cf8" />
              </div>
            </div>
          </div>
        )}

        <div className="flex flex-wrap gap-2">
          <div className="flex gap-1 flex-wrap">
            {["all", "critical", "significant", "moderate", "contained"].map((sv) => (
              <button
                key={sv}
                onClick={() => setFilterSeverity(sv)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  filterSeverity === sv ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {sv === "all" ? "All Severity" : sv.charAt(0).toUpperCase() + sv.slice(1)}
              </button>
            ))}
          </div>
          <div className="flex gap-1 flex-wrap">
            {["all", "healthy", "discount_creep", "renewal_risk", "expansion_stall", "champion_erosion", "multi_leak"].map((p) => (
              <button
                key={p}
                onClick={() => setFilterPattern(p)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  filterPattern === p ? "bg-violet-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {p === "all" ? "All Patterns" : `${PATTERN_ICONS[p] || ""} ${p.replace(/_/g, " ")}`}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {data?.accounts.map((a) => (
            <AccountCard key={a.account_id} account={a} onClick={() => setSelected(a)} />
          ))}
        </div>

        {data?.accounts.length === 0 && (
          <div className="text-center py-16 text-slate-500">No accounts match the selected filters.</div>
        )}
      </div>

      {selected && <AccountModal account={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
