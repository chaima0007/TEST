"use client";

import { useEffect, useState } from "react";

// ── types ────────────────────────────────────────────────────────────────────
interface CrisisIncident {
  incident_id: string;
  brand_entity: string;
  region: string;
  crisis_risk: string;
  crisis_pattern: string;
  crisis_severity: string;
  recommended_action: string;
  media_score: number;
  social_score: number;
  legal_score: number;
  reputation_score: number;
  crisis_composite: number;
  has_active_crisis: boolean;
  requires_executive_response: boolean;
  estimated_reputation_damage_score: number;
  crisis_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_crisis_composite: number;
  active_crisis_count: number;
  executive_response_count: number;
  avg_media_score: number;
  avg_social_score: number;
  avg_legal_score: number;
  avg_reputation_score: number;
  avg_estimated_reputation_damage_score: number;
}

// ── helpers ──────────────────────────────────────────────────────────────────
const RISK_COLOR: Record<string, string> = {
  critical: "text-rose-400",
  high:     "text-pink-400",
  moderate: "text-fuchsia-400",
  low:      "text-slate-400",
};

const RISK_BG: Record<string, string> = {
  critical: "bg-rose-500/20 border-rose-500/40",
  high:     "bg-pink-500/20 border-pink-500/40",
  moderate: "bg-fuchsia-500/20 border-fuchsia-500/40",
  low:      "bg-slate-500/20 border-slate-500/40",
};

const SEVERITY_COLOR: Record<string, string> = {
  emergency: "text-rose-400",
  crisis:    "text-pink-400",
  elevated:  "text-fuchsia-400",
  nominal:   "text-slate-400",
};

const PATTERN_ICON: Record<string, string> = {
  reputational_attack:  "🎯",
  media_escalation:     "📺",
  social_media_storm:   "🌪️",
  regulatory_scrutiny:  "⚖️",
  executive_misconduct: "👔",
  none:                 "—",
};

function CompositeRing({ score, color }: { score: number; color: string }) {
  const r = 36, circ = 2 * Math.PI * r;
  const fill = (Math.min(score, 100) / 100) * circ;
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
  const order  = ["critical", "high", "moderate", "low"];
  const colors = ["bg-rose-500", "bg-pink-500", "bg-fuchsia-500", "bg-slate-500"];
  const total  = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
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

// ── IncidentModal ─────────────────────────────────────────────────────────────
function IncidentModal({ incident, onClose }: { incident: CrisisIncident; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "scores" | "response">("overview");

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);

  const ringColor =
    incident.crisis_composite >= 60 ? "#f43f5e"
    : incident.crisis_composite >= 40 ? "#ec4899"
    : incident.crisis_composite >= 20 ? "#a855f7"
    : "#64748b";

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
          <CompositeRing score={incident.crisis_composite} color={ringColor} />
          <div className="flex-1 min-w-0">
            <h2 className="text-white font-bold text-lg truncate">{incident.brand_entity}</h2>
            <p className="text-slate-400 text-sm">{incident.incident_id} · {incident.region}</p>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[incident.crisis_risk]}`}>
                {incident.crisis_risk} risk
              </span>
              <span className={`text-xs font-medium ${SEVERITY_COLOR[incident.crisis_severity]}`}>
                {incident.crisis_severity}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-800">
          {(["overview", "scores", "response"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t ? "text-rose-400 border-b-2 border-rose-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "overview" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Pattern",         PATTERN_ICON[incident.crisis_pattern] + " " + incident.crisis_pattern.replace(/_/g, " ")],
                  ["Damage Index",    incident.estimated_reputation_damage_score.toFixed(2) + " / 10"],
                  ["Active Crisis",   incident.has_active_crisis ? "🚨 Yes" : "No"],
                  ["Exec Response",   incident.requires_executive_response ? "⚡ Yes" : "No"],
                ].map(([label, value]) => (
                  <div key={label as string} className="bg-slate-800/60 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{label}</div>
                    <div className="text-white font-semibold mt-0.5 text-sm">{value}</div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Crisis Signal</div>
                <div className="text-rose-300 text-sm leading-relaxed">{incident.crisis_signal}</div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Media"      value={incident.media_score}      color="bg-rose-500" />
              <ScoreBar label="Social"     value={incident.social_score}     color="bg-pink-500" />
              <ScoreBar label="Legal"      value={incident.legal_score}      color="bg-fuchsia-500" />
              <ScoreBar label="Reputation" value={incident.reputation_score} color="bg-purple-500" />
            </div>
          )}

          {tab === "response" && (
            <div className="space-y-3">
              <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-4">
                <div className="text-xs text-rose-400 uppercase tracking-wide mb-1">Recommended Response</div>
                <div className="text-white font-bold text-lg capitalize">
                  {incident.recommended_action.replace(/_/g, " ")}
                </div>
              </div>
              {incident.requires_executive_response && (
                <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-3 text-sm text-amber-300">
                  ⚡ Executive response required — escalate to C-suite immediately
                </div>
              )}
              {incident.has_active_crisis && (
                <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-3 text-sm text-rose-300">
                  🚨 Active crisis detected — engage communications team now
                </div>
              )}
              {!incident.has_active_crisis && (
                <div className="bg-slate-800/60 rounded-xl p-3 text-sm text-slate-400">
                  ✅ No active crisis — continue routine monitoring
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── IncidentCard ──────────────────────────────────────────────────────────────
function IncidentCard({ incident, onClick }: { incident: CrisisIncident; onClick: () => void }) {
  const ringColor =
    incident.crisis_composite >= 60 ? "#f43f5e"
    : incident.crisis_composite >= 40 ? "#ec4899"
    : incident.crisis_composite >= 20 ? "#a855f7"
    : "#64748b";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-rose-500/50 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3">
        <CompositeRing score={incident.crisis_composite} color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-semibold truncate">{incident.brand_entity}</div>
          <div className="text-slate-400 text-xs">{incident.incident_id} · {incident.region}</div>
          <div className="flex gap-2 mt-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[incident.crisis_risk]}`}>
              {incident.crisis_risk}
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          {incident.requires_executive_response && <div className="text-xs text-amber-400">⚡ Exec</div>}
          <div className={`text-sm font-bold mt-1 ${SEVERITY_COLOR[incident.crisis_severity]}`}>
            {incident.crisis_severity}
          </div>
          {incident.has_active_crisis && (
            <div className="text-xs text-rose-400 mt-1">🚨</div>
          )}
        </div>
      </div>
      <div className="mt-2 text-xs text-slate-400">
        {PATTERN_ICON[incident.crisis_pattern]} {incident.crisis_pattern.replace(/_/g, " ")} · dmg: {incident.estimated_reputation_damage_score.toFixed(2)}
      </div>
    </div>
  );
}

// ── page ─────────────────────────────────────────────────────────────────────
export default function PRCrisisManagementEnginePage() {
  const [incidents, setIncidents] = useState<CrisisIncident[]>([]);
  const [summary, setSummary]     = useState<Summary | null>(null);
  const [loading, setLoading]     = useState(true);
  const [selected, setSelected]   = useState<CrisisIncident | null>(null);
  const [filterRisk,   setFilterRisk]   = useState("all");
  const [filterRegion, setFilterRegion] = useState("all");

  useEffect(() => {
    async function load() {
        setLoading(true);
        const params = new URLSearchParams();
        if (filterRisk   !== "all") params.set("risk",   filterRisk);
        if (filterRegion !== "all") params.set("region", filterRegion);
        const res  = await fetch(`/api/pr-crisis-management-engine?${params}`);
        const data = await res.json();
        setIncidents(data.incidents);
        setSummary(data.summary);
        setLoading(false);
  }
    load();
  }, [filterRisk, filterRegion]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* header */}
        <div>
          <h1 className="text-2xl font-bold text-white">PR & Crisis Management Engine</h1>
          <p className="text-slate-400 text-sm mt-1">
            Monitors brand reputation, media escalation, social media storms, regulatory scrutiny
            and executive-misconduct signals — and prescribes the right crisis response
          </p>
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { label: "Incidents Tracked",   value: summary.total },
              { label: "Avg Composite",        value: summary.avg_crisis_composite.toFixed(1), color: "text-rose-400" },
              { label: "Active Crises",        value: summary.active_crisis_count,              color: "text-pink-400" },
              { label: "Exec Responses",       value: summary.executive_response_count,         color: "text-amber-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <div className="text-xs text-slate-400">{label}</div>
                <div className={`text-2xl font-bold mt-1 ${color ?? "text-white"}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* risk distribution bar */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-400 mb-2">Crisis Risk Distribution</div>
            <RiskDistBar counts={summary.risk_counts} />
            <div className="flex gap-4 mt-2 text-xs text-slate-500">
              {["critical", "high", "moderate", "low"].map((k) => (
                <span key={k} className={RISK_COLOR[k]}>{k}: {summary.risk_counts[k] || 0}</span>
              ))}
            </div>
          </div>
        )}

        {/* filters */}
        <div className="flex flex-wrap gap-2">
          {[
            { label: "All Risks",  val: "all" },
            { label: "🔴 Critical", val: "critical" },
            { label: "🩷 High",    val: "high" },
            { label: "🟣 Moderate", val: "moderate" },
            { label: "⚫ Low",     val: "low" },
          ].map(({ label, val }) => (
            <button
              key={val}
              onClick={() => setFilterRisk(val)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filterRisk === val
                  ? "bg-rose-600 text-white"
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
            {["NAMER", "EMEA", "APAC", "LATAM"].map((r) => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>

        {/* incidents grid */}
        {loading ? (
          <div className="text-slate-400 text-center py-16">Scanning brand reputation landscape…</div>
        ) : incidents.length === 0 ? (
          <div className="text-slate-500 text-center py-16">No incidents match your filters.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {incidents.map((c) => (
              <IncidentCard key={c.incident_id} incident={c} onClick={() => setSelected(c)} />
            ))}
          </div>
        )}

        {/* avg score bars */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="text-sm font-semibold text-slate-300 mb-4">Average Score Breakdown</div>
            <div className="space-y-3">
              <ScoreBar label="Media"      value={summary.avg_media_score}      color="bg-rose-500" />
              <ScoreBar label="Social"     value={summary.avg_social_score}     color="bg-pink-500" />
              <ScoreBar label="Legal"      value={summary.avg_legal_score}      color="bg-fuchsia-500" />
              <ScoreBar label="Reputation" value={summary.avg_reputation_score} color="bg-purple-500" />
            </div>
          </div>
        )}
      </div>

      {selected && <IncidentModal incident={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
