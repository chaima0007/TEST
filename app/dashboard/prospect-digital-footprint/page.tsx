"use client";

import { useEffect, useState, useCallback } from "react";

// ── types ──────────────────────────────────────────────────────────────────────
interface Prospect {
  prospect_id: string;
  company_name: string;
  rep_id: string;
  intent_tier: string;
  footprint_pattern: string;
  engagement_velocity: string;
  prospect_action: string;
  website_intent_score: number;
  content_engagement_score: number;
  social_signal_score: number;
  company_fit_score: number;
  digital_footprint_composite: number;
  lead_score: number;
  days_to_outreach: number;
  is_high_intent: boolean;
  needs_immediate_outreach: boolean;
  company_size_employees: number;
  region: string;
}

interface Summary {
  total: number;
  tier_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  velocity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_digital_footprint_composite: number;
  avg_lead_score: number;
  high_intent_count: number;
  immediate_outreach_count: number;
  avg_website_intent_score: number;
  avg_content_engagement_score: number;
  avg_social_signal_score: number;
  avg_company_fit_score: number;
}

// ── helpers ────────────────────────────────────────────────────────────────────
const TIER_COLOR: Record<string, string> = {
  cold:        "text-slate-400",
  warming:     "text-blue-400",
  hot:         "text-orange-400",
  buying_now:  "text-emerald-400",
};
const TIER_BG: Record<string, string> = {
  cold:        "bg-slate-800/60 border-slate-700",
  warming:     "bg-blue-900/30 border-blue-700",
  hot:         "bg-orange-900/30 border-orange-700",
  buying_now:  "bg-emerald-900/30 border-emerald-700",
};
const ACTION_BADGE: Record<string, string> = {
  nurture:         "bg-slate-800 text-slate-300 border-slate-600",
  warm_outreach:   "bg-blue-900/50 text-blue-300 border-blue-700",
  immediate_sdr:   "bg-orange-900/50 text-orange-300 border-orange-700",
  executive_touch: "bg-emerald-900/50 text-emerald-300 border-emerald-700",
};
const PATTERN_LABEL: Record<string, string> = {
  passive_lurker:        "Passive Lurker",
  content_consumer:      "Content Consumer",
  active_researcher:     "Active Researcher",
  intent_spiker:         "Intent Spiker",
  competitive_evaluator: "Competitive Evaluator",
  ready_to_buy:          "Ready to Buy",
};
const VELOCITY_LABEL: Record<string, string> = {
  declining: "📉 Declining",
  flat:      "➡ Flat",
  growing:   "📈 Growing",
  surging:   "🚀 Surging",
};
const TIER_LABEL: Record<string, string> = {
  cold: "Cold", warming: "Warming", hot: "Hot", buying_now: "Buying Now",
};

// ── IntentMeter ───────────────────────────────────────────────────────────────
function IntentMeter({ score, size = 80 }: { score: number; size?: number }) {
  const r = (size - 12) / 2;
  const circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  const color = score >= 75 ? "#34d399" : score >= 55 ? "#fb923c" : score >= 30 ? "#60a5fa" : "#64748b";
  return (
    <svg width={size} height={size} className="rotate-[-90deg]">
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle
        cx={size / 2} cy={size / 2} r={r}
        fill="none" stroke={color} strokeWidth={8}
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
      />
    </svg>
  );
}

// ── ScoreBar ──────────────────────────────────────────────────────────────────
function ScoreBar({ label, score, color }: { label: string; score: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-slate-400">{label}</span>
        <span className="font-semibold" style={{ color }}>{score.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all duration-500" style={{ width: `${score}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

// ── TierDistBar ───────────────────────────────────────────────────────────────
function TierDistBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const order  = ["buying_now", "hot", "warming", "cold"];
  const colors = ["#34d399", "#fb923c", "#60a5fa", "#64748b"];
  const labels = ["Buying Now", "Hot", "Warming", "Cold"];
  return (
    <div>
      <div className="flex h-4 rounded-full overflow-hidden mb-2 gap-0.5">
        {order.map((k, i) => {
          const pct = total > 0 ? ((counts[k] || 0) / total) * 100 : 0;
          return pct > 0 ? (
            <div key={k} style={{ width: `${pct}%`, backgroundColor: colors[i] }} title={labels[i]} />
          ) : null;
        })}
      </div>
      <div className="flex gap-4 flex-wrap">
        {order.map((k, i) => (
          <div key={k} className="flex items-center gap-1.5 text-xs text-slate-400">
            <span className="w-2 h-2 rounded-full inline-block" style={{ backgroundColor: colors[i] }} />
            {labels[i]}: {counts[k] || 0}
          </div>
        ))}
      </div>
    </div>
  );
}

// ── ProspectCard ──────────────────────────────────────────────────────────────
function ProspectCard({ prospect, onClick }: { prospect: Prospect; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-4 rounded-xl border transition-all hover:brightness-110 ${TIER_BG[prospect.intent_tier]}`}
    >
      <div className="flex items-start justify-between gap-2 mb-2">
        <div>
          <p className="font-semibold text-slate-100 text-sm">{prospect.company_name}</p>
          <p className="text-xs text-slate-400">{prospect.rep_id} · {prospect.region} · {prospect.company_size_employees.toLocaleString()} emp</p>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${ACTION_BADGE[prospect.prospect_action]}`}>
            {prospect.prospect_action.replace(/_/g, " ").toUpperCase()}
          </span>
          {prospect.needs_immediate_outreach && (
            <span className="text-xs text-emerald-400 font-semibold">⚡ TODAY</span>
          )}
        </div>
      </div>
      <div className="flex items-center gap-3 mt-2">
        <div className="relative flex-shrink-0">
          <IntentMeter score={prospect.digital_footprint_composite} size={52} />
          <div className="absolute inset-0 flex items-center justify-center">
            <span className={`text-xs font-bold ${TIER_COLOR[prospect.intent_tier]}`}>
              {prospect.digital_footprint_composite.toFixed(0)}
            </span>
          </div>
        </div>
        <div className="flex-1 space-y-1 text-xs text-slate-300">
          <div className="flex justify-between">
            <span>Intent</span>
            <span className={`font-semibold ${TIER_COLOR[prospect.intent_tier]}`}>{TIER_LABEL[prospect.intent_tier]}</span>
          </div>
          <div className="flex justify-between">
            <span>Pattern</span>
            <span className="font-semibold text-slate-200 text-right">{PATTERN_LABEL[prospect.footprint_pattern]}</span>
          </div>
          <div className="flex justify-between">
            <span>Lead Score</span>
            <span className="font-semibold text-violet-300">{prospect.lead_score.toFixed(0)}/100</span>
          </div>
        </div>
      </div>
    </button>
  );
}

// ── ProspectModal ─────────────────────────────────────────────────────────────
function ProspectModal({ prospect, onClose }: { prospect: Prospect; onClose: () => void }) {
  const [tab, setTab] = useState<"signals" | "profile" | "action">("signals");

  useEffect(() => {
    const fn = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl shadow-2xl overflow-hidden">
        {/* header */}
        <div className={`px-6 py-4 border-b border-slate-700 flex items-start justify-between ${TIER_BG[prospect.intent_tier]}`}>
          <div>
            <h2 className="text-lg font-bold text-slate-100">{prospect.company_name}</h2>
            <p className="text-sm text-slate-400">{prospect.rep_id} · {prospect.region} · {prospect.company_size_employees.toLocaleString()} employees</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl leading-none">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-700">
          {(["signals", "profile", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${tab === t ? "text-violet-400 border-b-2 border-violet-400" : "text-slate-400 hover:text-slate-200"}`}
            >
              {t === "signals" ? "Digital Signals" : t === "profile" ? "Footprint" : "Action Plan"}
            </button>
          ))}
        </div>

        {/* body */}
        <div className="p-6 space-y-4">
          {tab === "signals" && (
            <>
              <div className="flex items-center gap-6">
                <div className="relative">
                  <IntentMeter score={prospect.digital_footprint_composite} size={100} />
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className={`text-lg font-bold ${TIER_COLOR[prospect.intent_tier]}`}>{prospect.digital_footprint_composite.toFixed(1)}</span>
                    <span className="text-xs text-slate-400">Intent</span>
                  </div>
                </div>
                <div className="flex-1 grid grid-cols-2 gap-3 text-sm">
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">Intent Tier</p>
                    <p className={`font-bold ${TIER_COLOR[prospect.intent_tier]}`}>{TIER_LABEL[prospect.intent_tier]}</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">Lead Score</p>
                    <p className="font-bold text-violet-300">{prospect.lead_score.toFixed(0)}/100</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">Velocity</p>
                    <p className="font-bold text-slate-200 text-xs">{VELOCITY_LABEL[prospect.engagement_velocity]}</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">Outreach In</p>
                    <p className={`font-bold ${prospect.days_to_outreach === 0 ? "text-emerald-400" : "text-slate-200"}`}>
                      {prospect.days_to_outreach === 0 ? "NOW" : `${prospect.days_to_outreach}d`}
                    </p>
                  </div>
                </div>
              </div>
              {prospect.needs_immediate_outreach && (
                <div className="bg-emerald-950 border border-emerald-700 rounded-lg p-3 text-sm text-emerald-300">
                  ⚡ High-intent prospect — initiate outreach today for maximum conversion probability.
                </div>
              )}
            </>
          )}

          {tab === "profile" && (
            <div className="space-y-3">
              <div className="bg-slate-800 rounded-lg p-3 text-sm">
                <p className="text-xs text-slate-400 mb-1">Footprint Pattern</p>
                <p className="font-semibold text-slate-100">{PATTERN_LABEL[prospect.footprint_pattern]}</p>
              </div>
              <ScoreBar label="Website Intent"      score={prospect.website_intent_score}      color="#34d399" />
              <ScoreBar label="Content Engagement"  score={prospect.content_engagement_score}  color="#60a5fa" />
              <ScoreBar label="Social Signals"      score={prospect.social_signal_score}       color="#a78bfa" />
              <ScoreBar label="Company Fit"         score={prospect.company_fit_score}         color="#fb923c" />
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-3">
              <div className={`rounded-xl p-4 border ${ACTION_BADGE[prospect.prospect_action]}`}>
                <p className="text-xs font-semibold uppercase tracking-wide mb-1">Recommended Action</p>
                <p className="font-bold text-lg">{prospect.prospect_action.replace(/_/g, " ").toUpperCase()}</p>
              </div>
              {prospect.prospect_action === "executive_touch" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>This is an enterprise prospect with high intent — route to AE + executive co-sell</li>
                  <li>Personalize outreach with their specific digital signals (pricing page, competitor research)</li>
                  <li>Lead with ROI and peer case studies from similar-sized companies</li>
                  <li>Request discovery call at VP+ level — don&apos;t start at practitioner level</li>
                </ul>
              )}
              {prospect.prospect_action === "immediate_sdr" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>Route to SDR immediately — prospect showing strong buying signals today</li>
                  <li>Reference their specific actions (pricing page, demo request) in outreach</li>
                  <li>Offer demo slot within 24-48 hours while intent is at peak</li>
                </ul>
              )}
              {prospect.prospect_action === "warm_outreach" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>Prospect is researching actively — reach out within 2 days</li>
                  <li>Lead with relevant content or case study matching their research pattern</li>
                  <li>Personalize with their industry pain points, not generic pitch</li>
                </ul>
              )}
              {prospect.prospect_action === "nurture" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>Still in early awareness — keep in nurture sequence</li>
                  <li>Continue serving relevant content to build familiarity</li>
                  <li>Re-evaluate in 3-4 weeks when more digital signals accumulate</li>
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
export default function ProspectDigitalFootprintPage() {
  const [prospects, setProspects] = useState<Prospect[]>([]);
  const [summary, setSummary]     = useState<Summary | null>(null);
  const [loading, setLoading]     = useState(true);
  const [selected, setSelected]   = useState<Prospect | null>(null);
  const [tierFilter, setTierFilter]       = useState("all");
  const [patternFilter, setPatternFilter] = useState("all");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (tierFilter !== "all")    params.set("tier", tierFilter);
      if (patternFilter !== "all") params.set("pattern", patternFilter);
      const r = await fetch(`/api/prospect-digital-footprint?${params}`);
      const j = await r.json();
      setProspects(j.prospects);
      setSummary(j.summary);
    } finally {
      setLoading(false);
    }
  }, [tierFilter, patternFilter]);

  useEffect(() => { load(); }, [load]);

  const hotQueue = prospects.filter((p) => p.needs_immediate_outreach);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Prospect Digital Footprint</h1>
        <p className="text-slate-400 text-sm mt-1">Score inbound prospects by digital intent signals before any human touches them</p>
      </div>

      {/* immediate outreach alert */}
      {hotQueue.length > 0 && (
        <div className="bg-emerald-950 border border-emerald-700 rounded-xl p-4 flex items-start gap-3">
          <span className="text-emerald-400 text-xl">⚡</span>
          <div>
            <p className="text-emerald-300 font-semibold text-sm">{hotQueue.length} prospect{hotQueue.length > 1 ? "s" : ""} need outreach TODAY</p>
            <p className="text-emerald-400/80 text-xs mt-0.5">{hotQueue.map((p) => p.company_name).join(" · ")}</p>
          </div>
        </div>
      )}

      {/* KPI strip */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Total Prospects",    value: summary.total },
            { label: "High Intent",        value: `${summary.high_intent_count} / ${summary.total}` },
            { label: "Immediate Outreach", value: summary.immediate_outreach_count },
            { label: "Avg Lead Score",     value: summary.avg_lead_score.toFixed(1) },
          ].map((k) => (
            <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <p className="text-xs text-slate-400">{k.label}</p>
              <p className="text-2xl font-bold text-slate-100 mt-1">{k.value}</p>
            </div>
          ))}
        </div>
      )}

      {/* intent tier distribution */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-slate-300 mb-4">Intent Tier Distribution</h2>
          <TierDistBar counts={summary.tier_counts} total={summary.total} />
        </div>
      )}

      {/* filters */}
      <div className="flex flex-wrap gap-2">
        {["all", "buying_now", "hot", "warming", "cold"].map((t) => (
          <button
            key={t}
            onClick={() => setTierFilter(t)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
              tierFilter === t ? "bg-violet-600 border-violet-500 text-white" : "bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-500"
            }`}
          >
            {t === "all" ? "All Tiers" : TIER_LABEL[t]}
          </button>
        ))}
        <div className="w-px bg-slate-700 mx-1" />
        {["all", "ready_to_buy", "competitive_evaluator", "intent_spiker", "active_researcher", "content_consumer", "passive_lurker"].map((p) => (
          <button
            key={p}
            onClick={() => setPatternFilter(p)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
              patternFilter === p ? "bg-indigo-600 border-indigo-500 text-white" : "bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-500"
            }`}
          >
            {p === "all" ? "All Patterns" : PATTERN_LABEL[p]}
          </button>
        ))}
      </div>

      {/* avg sub-scores */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
          <h2 className="text-sm font-semibold text-slate-300">Average Digital Signal Scores</h2>
          <ScoreBar label="Website Intent"     score={summary.avg_website_intent_score}     color="#34d399" />
          <ScoreBar label="Content Engagement" score={summary.avg_content_engagement_score} color="#60a5fa" />
          <ScoreBar label="Social Signals"     score={summary.avg_social_signal_score}      color="#a78bfa" />
          <ScoreBar label="Company Fit"        score={summary.avg_company_fit_score}        color="#fb923c" />
        </div>
      )}

      {/* prospect grid */}
      {loading ? (
        <p className="text-slate-400 text-sm">Scoring prospects…</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {prospects.map((p) => (
            <ProspectCard key={p.prospect_id} prospect={p} onClick={() => setSelected(p)} />
          ))}
        </div>
      )}

      {selected && <ProspectModal prospect={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
