"use client";

import { useEffect, useState } from "react";

type EngagementVelocity = "accelerating" | "steady" | "decelerating" | "stalled" | "cold";
type IntentLevel        = "hot" | "warm" | "lukewarm" | "cold";
type EngagementRisk     = "low" | "moderate" | "high" | "critical";
type EngagementAction   = "nurture" | "advance" | "reactivate" | "disqualify";

interface Prospect {
  prospect_id: string;
  prospect_name: string;
  company_name: string;
  rep_id: string;
  region: string;
  engagement_velocity: EngagementVelocity;
  intent_level: IntentLevel;
  engagement_risk: EngagementRisk;
  engagement_action: EngagementAction;
  email_engagement_score: number;
  meeting_engagement_score: number;
  digital_engagement_score: number;
  velocity_trend_score: number;
  engagement_composite: number;
  days_to_re_engage: number;
  is_high_intent: boolean;
  needs_reactivation: boolean;
  primary_signal: string;
}

interface Summary {
  total: number;
  velocity_counts: Record<string, number>;
  intent_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_engagement_composite: number;
  high_intent_count: number;
  reactivation_count: number;
  avg_email_engagement_score: number;
  avg_meeting_engagement_score: number;
  avg_digital_engagement_score: number;
  avg_velocity_trend_score: number;
  avg_days_to_re_engage: number;
}

const VELOCITY_COLOR: Record<EngagementVelocity, string> = {
  accelerating: "text-emerald-400",
  steady:       "text-indigo-400",
  decelerating: "text-amber-400",
  stalled:      "text-orange-400",
  cold:         "text-red-400",
};

const INTENT_COLOR: Record<IntentLevel, string> = {
  hot:      "bg-red-500/20     text-red-300",
  warm:     "bg-amber-500/20   text-amber-300",
  lukewarm: "bg-slate-500/20   text-slate-300",
  cold:     "bg-blue-500/20    text-blue-300",
};

const RISK_COLOR: Record<EngagementRisk, string> = {
  low:      "bg-emerald-500/20 text-emerald-300",
  moderate: "bg-amber-500/20   text-amber-300",
  high:     "bg-orange-500/20  text-orange-300",
  critical: "bg-red-500/20     text-red-300",
};

function compositeColor(v: number): string {
  if (v >= 70) return "#34d399";
  if (v >= 50) return "#818cf8";
  if (v >= 30) return "#fbbf24";
  return "#f87171";
}

function fmtLabel(s: string): string {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function EngagementRing({ value, label }: { value: number; label: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = (value / 100) * circ;
  const color = compositeColor(value);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="86" height="86" viewBox="0 0 86 86">
        <circle cx="43" cy="43" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle cx="43" cy="43" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={`${fill} ${circ}`} strokeLinecap="round"
          transform="rotate(-90 43 43)" />
        <text x="43" y="40" textAnchor="middle" fill={color} fontSize="13" fontWeight="bold">{value}</text>
        <text x="43" y="52" textAnchor="middle" fill="#94a3b8" fontSize="7">/ 100</text>
      </svg>
      <span className="text-xs text-slate-400">{label}</span>
    </div>
  );
}

function VelocityDistBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const order: EngagementVelocity[] = ["accelerating", "steady", "decelerating", "stalled", "cold"];
  const colors: Record<string, string> = {
    accelerating: "bg-emerald-500", steady: "bg-indigo-500",
    decelerating: "bg-amber-500", stalled: "bg-orange-500", cold: "bg-red-500",
  };
  return (
    <div className="space-y-2">
      <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
        {order.map((v) => {
          const pct = total > 0 ? ((counts[v] || 0) / total) * 100 : 0;
          return pct > 0 ? (
            <div key={v} className={colors[v]} style={{ width: `${pct}%` }} title={`${v}: ${counts[v] || 0}`} />
          ) : null;
        })}
      </div>
      <div className="flex flex-wrap gap-3">
        {order.map((v) => (
          <div key={v} className="flex items-center gap-1.5">
            <div className={`w-2 h-2 rounded-full ${colors[v]}`} />
            <span className="text-xs text-slate-400">{fmtLabel(v)}: {counts[v] || 0}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function ProspectCard({ prospect, onClick }: { prospect: Prospect; onClick: () => void }) {
  return (
    <button onClick={onClick}
      className="w-full text-left bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-indigo-500/50 transition-all">
      <div className="flex items-start justify-between mb-3">
        <div>
          <p className="font-semibold text-slate-100">{prospect.prospect_name}</p>
          <p className="text-xs text-slate-500">{prospect.company_name} · {prospect.region}</p>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className={`text-xs font-medium ${VELOCITY_COLOR[prospect.engagement_velocity]}`}>
            {fmtLabel(prospect.engagement_velocity)}
          </span>
          <span className={`text-xs px-2 py-0.5 rounded-full ${INTENT_COLOR[prospect.intent_level]}`}>
            {prospect.intent_level} intent
          </span>
        </div>
      </div>

      <div className="flex items-center gap-3 mb-3">
        <div className="flex-1">
          <div className="flex justify-between text-xs text-slate-500 mb-1">
            <span>Engagement composite</span>
            <span>re-engage in {prospect.days_to_re_engage}d</span>
          </div>
          <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full rounded-full"
              style={{ width: `${prospect.engagement_composite}%`, backgroundColor: compositeColor(prospect.engagement_composite) }} />
          </div>
        </div>
        <div className="text-right">
          <p className="text-lg font-bold" style={{ color: compositeColor(prospect.engagement_composite) }}>
            {prospect.engagement_composite}
          </p>
          <p className="text-xs text-slate-500">score</p>
        </div>
      </div>

      <div className="flex items-center justify-between">
        <span className={`text-xs px-2 py-0.5 rounded-full ${RISK_COLOR[prospect.engagement_risk]}`}>
          {prospect.engagement_risk} risk
        </span>
        {prospect.is_high_intent && (
          <span className="text-xs bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-full">High Intent</span>
        )}
        {prospect.needs_reactivation && (
          <span className="text-xs bg-red-500/20 text-red-300 px-2 py-0.5 rounded-full">Reactivate</span>
        )}
      </div>
    </button>
  );
}

function ProspectModal({ prospect, onClose }: { prospect: Prospect; onClose: () => void }) {
  const [tab, setTab] = useState<"signals" | "scores" | "actions">("signals");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const scores = [
    { label: "Email",    value: prospect.email_engagement_score },
    { label: "Meeting",  value: prospect.meeting_engagement_score },
    { label: "Digital",  value: prospect.digital_engagement_score },
    { label: "Velocity", value: prospect.velocity_trend_score },
  ];

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}>
        <div className="p-5 border-b border-slate-800">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-100">{prospect.prospect_name}</h2>
              <p className="text-sm text-slate-400">{prospect.company_name} · {prospect.region}</p>
              <div className="flex gap-2 mt-2">
                <span className={`text-xs px-2 py-0.5 rounded-full ${INTENT_COLOR[prospect.intent_level]}`}>
                  {prospect.intent_level} intent
                </span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${RISK_COLOR[prospect.engagement_risk]}`}>
                  {prospect.engagement_risk} risk
                </span>
              </div>
            </div>
            <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl">×</button>
          </div>
        </div>

        <div className="flex border-b border-slate-800">
          {(["signals", "scores", "actions"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm capitalize transition-colors ${
                tab === t ? "border-b-2 border-indigo-500 text-indigo-400" : "text-slate-500 hover:text-slate-300"
              }`}>
              {t}
            </button>
          ))}
        </div>

        <div className="p-5">
          {tab === "signals" && (
            <div className="space-y-3">
              <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-lg p-3">
                <p className="text-xs text-indigo-400 mb-1">Primary Signal</p>
                <p className="text-sm text-slate-200">{prospect.primary_signal}</p>
              </div>
              {[
                { label: "Engagement Velocity", value: fmtLabel(prospect.engagement_velocity) },
                { label: "Days Since Last Engagement", value: `${prospect.days_to_re_engage}d` },
                { label: "Is High Intent", value: prospect.is_high_intent ? "Yes" : "No" },
                { label: "Needs Reactivation", value: prospect.needs_reactivation ? "Yes" : "No" },
                { label: "Composite Score", value: `${prospect.engagement_composite}` },
              ].map(({ label, value }) => (
                <div key={label} className="flex justify-between py-2 border-b border-slate-800">
                  <span className="text-sm text-slate-400">{label}</span>
                  <span className="text-sm font-medium text-slate-200">{value}</span>
                </div>
              ))}
            </div>
          )}

          {tab === "scores" && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                {scores.map((s) => (
                  <div key={s.label} className="bg-slate-800/50 rounded-lg p-3">
                    <p className="text-xs text-slate-400 mb-1">{s.label}</p>
                    <p className="text-xl font-bold" style={{ color: compositeColor(s.value) }}>{s.value}</p>
                    <div className="mt-1 h-1 bg-slate-700 rounded-full overflow-hidden">
                      <div className="h-full rounded-full"
                        style={{ width: `${s.value}%`, backgroundColor: compositeColor(s.value) }} />
                    </div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/50 rounded-lg p-3 flex justify-between items-center">
                <span className="text-sm text-slate-300">Engagement Composite</span>
                <span className="text-2xl font-bold" style={{ color: compositeColor(prospect.engagement_composite) }}>
                  {prospect.engagement_composite}
                </span>
              </div>
            </div>
          )}

          {tab === "actions" && (
            <div className="space-y-4">
              <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-lg p-4">
                <p className="text-xs text-indigo-400 mb-1">Recommended Action</p>
                <p className="font-semibold text-indigo-300">{fmtLabel(prospect.engagement_action)}</p>
                <p className="text-xs text-slate-400 mt-1">Re-engage in {prospect.days_to_re_engage} day(s)</p>
              </div>
              <div className="text-sm text-slate-300">
                {prospect.engagement_action === "advance" && <p>This prospect shows strong intent signals. Move them to the next deal stage and schedule a discovery or demo call immediately.</p>}
                {prospect.engagement_action === "nurture" && <p>Maintain consistent touchpoints. Share relevant case studies or ROI data to build interest. Monitor for buying signals.</p>}
                {prospect.engagement_action === "reactivate" && <p>Use a pattern-interrupt sequence: executive outreach, new insight, or competitive trigger. Avoid generic follow-ups.</p>}
                {prospect.engagement_action === "disqualify" && <p>Engagement signals are too weak to justify continued investment. Archive and revisit in 90 days if business conditions change.</p>}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function ProspectEngagementVelocityPage() {
  const [data, setData] = useState<{ prospects: Prospect[]; summary: Summary } | null>(null);
  const [velocity, setVelocity] = useState("");
  const [intent,   setIntent]   = useState("");
  const [region,   setRegion]   = useState("");
  const [selected, setSelected] = useState<Prospect | null>(null);

  useEffect(() => {
    const params = new URLSearchParams();
    if (velocity) params.set("velocity", velocity);
    if (intent)   params.set("intent", intent);
    if (region)   params.set("region", region);
    fetch(`/api/prospect-engagement-velocity?${params}`)
      .then((r) => r.json())
      .then(setData);
  }, [velocity, intent, region]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400">Loading…</div>
    </div>
  );

  const { prospects, summary } = data;

  const kpis = [
    { label: "Total Prospects",   value: summary.total },
    { label: "High Intent",       value: summary.high_intent_count, sub: `${Math.round((summary.high_intent_count / summary.total) * 100)}%` },
    { label: "Need Reactivation", value: summary.reactivation_count },
    { label: "Avg Composite",     value: summary.avg_engagement_composite },
    { label: "Avg Re-Engage Days", value: `${summary.avg_days_to_re_engage}d` },
    { label: "Avg Velocity Trend", value: summary.avg_velocity_trend_score },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <div>
          <h1 className="text-2xl font-bold">Prospect Engagement Velocity</h1>
          <p className="text-slate-400 text-sm mt-1">Real-time engagement momentum and intent signals for every prospect</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          {kpis.map((k) => (
            <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <p className="text-xs text-slate-500 mb-1">{k.label}</p>
              <p className="text-2xl font-bold text-slate-100">{k.value}</p>
              {k.sub && <p className="text-xs text-slate-500 mt-0.5">{k.sub}</p>}
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-4">Velocity Distribution</h2>
            <VelocityDistBar counts={summary.velocity_counts} total={summary.total} />
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-4">Average Engagement Scores</h2>
            <div className="flex justify-around">
              <EngagementRing value={summary.avg_email_engagement_score}   label="Email" />
              <EngagementRing value={summary.avg_meeting_engagement_score} label="Meeting" />
              <EngagementRing value={summary.avg_digital_engagement_score} label="Digital" />
              <EngagementRing value={summary.avg_velocity_trend_score}     label="Velocity" />
            </div>
          </div>
        </div>

        <div className="flex flex-wrap gap-3">
          <select value={velocity} onChange={(e) => setVelocity(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-slate-300 rounded-lg px-3 py-2 text-sm">
            <option value="">All Velocities</option>
            {["accelerating", "steady", "decelerating", "stalled", "cold"].map((v) => (
              <option key={v} value={v}>{fmtLabel(v)}</option>
            ))}
          </select>
          <select value={intent} onChange={(e) => setIntent(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-slate-300 rounded-lg px-3 py-2 text-sm">
            <option value="">All Intent Levels</option>
            {["hot", "warm", "lukewarm", "cold"].map((i) => (
              <option key={i} value={i}>{fmtLabel(i)}</option>
            ))}
          </select>
          <select value={region} onChange={(e) => setRegion(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-slate-300 rounded-lg px-3 py-2 text-sm">
            <option value="">All Regions</option>
            {["NAMER", "EMEA", "APAC", "LATAM"].map((r) => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {prospects.map((p) => (
            <ProspectCard key={p.prospect_id} prospect={p} onClick={() => setSelected(p)} />
          ))}
        </div>
      </div>

      {selected && <ProspectModal prospect={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
