"use client";

import { useEffect, useState } from "react";

// ── types ────────────────────────────────────────────────────────────────────
interface JurisdictionRecord {
  jurisdiction_id: string;
  domain: string;
  region: string;
  legal_risk: string;
  regulatory_pattern: string;
  legal_severity: string;
  recommended_action: string;
  compliance_score_out: number;
  litigation_score: number;
  licensing_score: number;
  regulatory_score: number;
  legal_composite: number;
  has_legal_exposure: boolean;
  requires_immediate_counsel: boolean;
  estimated_legal_risk_index: number;
  legal_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_legal_composite: number;
  legal_exposure_count: number;
  immediate_counsel_count: number;
  avg_compliance_score: number;
  avg_litigation_score: number;
  avg_licensing_score: number;
  avg_regulatory_score: number;
  avg_estimated_legal_risk_index: number;
}

// ── helpers ──────────────────────────────────────────────────────────────────
const RISK_COLOR: Record<string, string> = {
  critical: "text-rose-400",
  high:     "text-orange-400",
  moderate: "text-indigo-400",
  low:      "text-slate-400",
};

const RISK_BG: Record<string, string> = {
  critical: "bg-rose-500/20 border-rose-500/40",
  high:     "bg-orange-500/20 border-orange-500/40",
  moderate: "bg-indigo-500/20 border-indigo-500/40",
  low:      "bg-slate-500/20 border-slate-500/40",
};

const SEVERITY_COLOR: Record<string, string> = {
  critical:  "text-rose-400",
  exposed:   "text-orange-400",
  watch:     "text-indigo-400",
  compliant: "text-slate-400",
};

const PATTERN_ICON: Record<string, string> = {
  litigation_risk:       "⚖️",
  compliance_gap:        "📋",
  regulatory_change:     "🔄",
  licensing_breach:      "🔑",
  cross_border_conflict: "🌐",
  none:                  "—",
};

const DOMAIN_ICON: Record<string, string> = {
  tax:          "💰",
  labor:        "👷",
  data_privacy: "🔒",
  trade:        "🚢",
  financial:    "🏦",
  environmental:"🌿",
  healthcare:   "🏥",
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
  const colors = ["bg-rose-500", "bg-orange-500", "bg-indigo-500", "bg-slate-500"];
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

// ── distributions panel ───────────────────────────────────────────────────────
function DistributionPanel({ title, counts, colors }: {
  title: string;
  counts: Record<string, number>;
  colors: Record<string, string>;
}) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
      <div className="text-xs text-slate-400 font-medium mb-3">{title}</div>
      <div className="space-y-2">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k}>
            <div className="flex justify-between text-xs mb-1">
              <span className={colors[k] ?? "text-slate-400"}>{k.replace(/_/g, " ")}</span>
              <span className="text-slate-500">{v}</span>
            </div>
            <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full ${
                  colors[k]?.replace("text-", "bg-").replace("-400", "-500") ?? "bg-slate-500"
                }`}
                style={{ width: `${(v / total) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── JurisdictionModal ─────────────────────────────────────────────────────────
function JurisdictionModal({ jur, onClose }: { jur: JurisdictionRecord; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);

  const ringColor =
    jur.legal_composite >= 60 ? "#f43f5e"
    : jur.legal_composite >= 40 ? "#f97316"
    : jur.legal_composite >= 20 ? "#6366f1"
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
          <CompositeRing score={jur.legal_composite} color={ringColor} />
          <div className="flex-1 min-w-0">
            <h2 className="text-white font-bold text-lg truncate">
              {DOMAIN_ICON[jur.domain] ?? "⚖️"} {jur.domain.replace(/_/g, " ")}
            </h2>
            <p className="text-slate-400 text-sm">{jur.jurisdiction_id} · {jur.region}</p>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[jur.legal_risk]}`}>
                {jur.legal_risk} risk
              </span>
              <span className={`text-xs font-medium ${SEVERITY_COLOR[jur.legal_severity]}`}>
                {jur.legal_severity}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-800">
          {(["overview", "scores", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t
                  ? "text-indigo-400 border-b-2 border-indigo-400"
                  : "text-slate-500 hover:text-slate-300"
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
                  ["Pattern",          PATTERN_ICON[jur.regulatory_pattern] + " " + jur.regulatory_pattern.replace(/_/g, " ")],
                  ["Risk Index",       jur.estimated_legal_risk_index.toFixed(2) + " / 10"],
                  ["Legal Exposure",   jur.has_legal_exposure ? "🚨 Yes" : "No"],
                  ["Immediate Counsel",jur.requires_immediate_counsel ? "⚡ Yes" : "No"],
                ].map(([label, value]) => (
                  <div key={label as string} className="bg-slate-800/60 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{label}</div>
                    <div className="text-white font-semibold mt-0.5 text-sm">{value}</div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Legal Signal</div>
                <div className="text-indigo-300 text-sm leading-relaxed">{jur.legal_signal}</div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Compliance"  value={jur.compliance_score_out} color="bg-indigo-500" />
              <ScoreBar label="Litigation"  value={jur.litigation_score}     color="bg-rose-500" />
              <ScoreBar label="Licensing"   value={jur.licensing_score}      color="bg-orange-500" />
              <ScoreBar label="Regulatory"  value={jur.regulatory_score}     color="bg-blue-500" />
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-3">
              <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-xl p-4">
                <div className="text-xs text-indigo-400 uppercase tracking-wide mb-1">Recommended Action</div>
                <div className="text-white font-bold text-lg capitalize">
                  {jur.recommended_action.replace(/_/g, " ")}
                </div>
              </div>
              {jur.requires_immediate_counsel && (
                <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-3 text-sm text-amber-300">
                  ⚡ Immediate legal counsel required — escalate to legal team now
                </div>
              )}
              {jur.has_legal_exposure && (
                <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-3 text-sm text-rose-300">
                  🚨 Legal exposure detected — initiate compliance review immediately
                </div>
              )}
              {!jur.has_legal_exposure && (
                <div className="bg-slate-800/60 rounded-xl p-3 text-sm text-slate-400">
                  ✅ No legal exposure — continue routine regulatory monitoring
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── JurisdictionCard ──────────────────────────────────────────────────────────
function JurisdictionCard({ jur, onClick }: { jur: JurisdictionRecord; onClick: () => void }) {
  const ringColor =
    jur.legal_composite >= 60 ? "#f43f5e"
    : jur.legal_composite >= 40 ? "#f97316"
    : jur.legal_composite >= 20 ? "#6366f1"
    : "#64748b";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-indigo-700 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3">
        <CompositeRing score={jur.legal_composite} color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-semibold truncate">
            {DOMAIN_ICON[jur.domain] ?? "⚖️"} {jur.domain.replace(/_/g, " ")}
          </div>
          <div className="text-slate-400 text-xs">{jur.jurisdiction_id} · {jur.region}</div>
          <div className="flex gap-2 mt-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[jur.legal_risk]}`}>
              {jur.legal_risk}
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          {jur.requires_immediate_counsel && <div className="text-xs text-amber-400">⚡ Counsel</div>}
          <div className={`text-sm font-bold mt-1 ${SEVERITY_COLOR[jur.legal_severity]}`}>
            {jur.legal_severity}
          </div>
          {jur.has_legal_exposure && (
            <div className="text-xs text-rose-400 mt-1">🚨</div>
          )}
        </div>
      </div>
      <div className="mt-2 text-xs text-slate-400">
        {PATTERN_ICON[jur.regulatory_pattern]} {jur.regulatory_pattern.replace(/_/g, " ")} · risk idx: {jur.estimated_legal_risk_index.toFixed(2)}
      </div>
    </div>
  );
}

// ── page ─────────────────────────────────────────────────────────────────────
export default function LegalRegulatoryWatchEnginePage() {
  const [jurisdictions, setJurisdictions] = useState<JurisdictionRecord[]>([]);
  const [summary, setSummary]             = useState<Summary | null>(null);
  const [loading, setLoading]             = useState(true);
  const [selected, setSelected]           = useState<JurisdictionRecord | null>(null);
  const [filterRisk,   setFilterRisk]     = useState("all");
  const [filterRegion, setFilterRegion]   = useState("all");

  useEffect(() => {
    async function load() {
        setLoading(true);
        const params = new URLSearchParams();
        if (filterRisk   !== "all") params.set("risk",   filterRisk);
        if (filterRegion !== "all") params.set("region", filterRegion);
        const res  = await fetch(`/api/legal-regulatory-watch-engine?${params}`);
        const data = await res.json();
        setJurisdictions(data.jurisdictions);
        setSummary(data.summary);
        setLoading(false);
  }
    load();
  }, [filterRisk, filterRegion]);

  const distributions = [
    {
      title: "Risk Distribution",
      counts: summary?.risk_counts ?? {},
      colors: { critical: "text-rose-400", high: "text-orange-400", moderate: "text-indigo-400", low: "text-slate-400" },
    },
    {
      title: "Pattern Distribution",
      counts: summary?.pattern_counts ?? {},
      colors: {
        litigation_risk: "text-rose-400", compliance_gap: "text-orange-400",
        regulatory_change: "text-indigo-400", licensing_breach: "text-amber-400",
        cross_border_conflict: "text-blue-400", none: "text-slate-400",
      },
    },
    {
      title: "Severity Distribution",
      counts: summary?.severity_counts ?? {},
      colors: { critical: "text-rose-400", exposed: "text-orange-400", watch: "text-indigo-400", compliant: "text-slate-400" },
    },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* header */}
        <div>
          <h1 className="text-2xl font-bold text-white">International Legal & Regulatory Watch Engine</h1>
          <p className="text-slate-400 text-sm mt-1">
            Monitors jurisdictional compliance, litigation exposure, licensing validity, and regulatory change
            velocity — prescribing the right legal response before exposure becomes irreversible
          </p>
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { label: "Jurisdictions Tracked",  value: summary.total },
              { label: "Avg Legal Composite",     value: summary.avg_legal_composite.toFixed(1), color: "text-indigo-400" },
              { label: "Legal Exposure",          value: summary.legal_exposure_count,            color: "text-rose-400" },
              { label: "Immediate Counsel",       value: summary.immediate_counsel_count,         color: "text-amber-400" },
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
            <div className="text-xs text-slate-400 mb-2">Legal Risk Distribution</div>
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
            { label: "All Risks",   val: "all" },
            { label: "🔴 Critical", val: "critical" },
            { label: "🟠 High",    val: "high" },
            { label: "🔵 Moderate", val: "moderate" },
            { label: "⚫ Low",     val: "low" },
          ].map(({ label, val }) => (
            <button
              key={val}
              onClick={() => setFilterRisk(val)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filterRisk === val
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
            {["NAMER", "EMEA", "APAC", "LATAM", "MEA"].map((r) => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>

        {/* jurisdictions grid */}
        {loading ? (
          <div className="text-slate-400 text-center py-16">Scanning legal & regulatory landscape…</div>
        ) : jurisdictions.length === 0 ? (
          <div className="text-slate-500 text-center py-16">No jurisdictions match your filters.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {jurisdictions.map((j) => (
              <JurisdictionCard key={j.jurisdiction_id} jur={j} onClick={() => setSelected(j)} />
            ))}
          </div>
        )}

        {/* distributions */}
        {summary && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {distributions.map((d) => (
              <DistributionPanel key={d.title} title={d.title} counts={d.counts} colors={d.colors} />
            ))}
          </div>
        )}

        {/* avg score bars */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="text-sm font-semibold text-slate-300 mb-4">Average Sub-Score Breakdown</div>
            <div className="space-y-3">
              <ScoreBar label="Compliance"  value={summary.avg_compliance_score}  color="bg-indigo-500" />
              <ScoreBar label="Litigation"  value={summary.avg_litigation_score}  color="bg-rose-500" />
              <ScoreBar label="Licensing"   value={summary.avg_licensing_score}   color="bg-orange-500" />
              <ScoreBar label="Regulatory"  value={summary.avg_regulatory_score}  color="bg-blue-500" />
            </div>
          </div>
        )}
      </div>

      {selected && <JurisdictionModal jur={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
