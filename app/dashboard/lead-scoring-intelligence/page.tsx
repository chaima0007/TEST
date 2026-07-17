"use client";

import { useEffect, useState } from "react";

interface Lead {
  lead_id: string;
  company: string;
  contact_name: string;
  segment: string;
  lead_source: string;
  lead_score: number;
  fit_score_label: string;
  intent_signal: string;
  tier: string;
  action: string;
  fit_breakdown: { icp: number; engagement: number; qualification: number };
  strengths: string[];
  weaknesses: string[];
  recommended_steps: string[];
  disqualification_reasons: string[];
}

interface Summary {
  total: number;
  tier_counts: Record<string, number>;
  action_counts: Record<string, number>;
  intent_counts: Record<string, number>;
  fit_counts: Record<string, number>;
  avg_lead_score: number;
  hot_count: number;
  call_now_count: number;
  disqualified_count: number;
  hot_rate_pct: number;
}

const TIER_COLOR: Record<string, string> = {
  hot: "#ef4444",
  warm: "#f59e0b",
  cold: "#38bdf8",
  dead: "#64748b",
};

const TIER_BADGE: Record<string, string> = {
  hot: "bg-red-900/60 text-red-300 border-red-700",
  warm: "bg-amber-900/60 text-amber-300 border-amber-700",
  cold: "bg-sky-900/60 text-sky-300 border-sky-700",
  dead: "bg-slate-800 text-slate-400 border-slate-600",
};

const ACTION_BADGE: Record<string, string> = {
  call_now: "bg-red-900/60 text-red-300 border-red-700",
  assign_ae: "bg-violet-900/60 text-violet-300 border-violet-700",
  qualify: "bg-indigo-900/60 text-indigo-300 border-indigo-700",
  nurture: "bg-sky-900/60 text-sky-300 border-sky-700",
  disqualify: "bg-slate-800 text-slate-400 border-slate-600",
};

const INTENT_BADGE: Record<string, string> = {
  high_intent: "bg-emerald-900/60 text-emerald-300 border-emerald-700",
  medium_intent: "bg-amber-900/60 text-amber-300 border-amber-700",
  low_intent: "bg-slate-800 text-slate-300 border-slate-600",
  no_intent: "bg-slate-800 text-slate-500 border-slate-700",
};

function ScoreRing({ score, tier }: { score: number; tier: string }) {
  const r = 40;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;
  const stroke = TIER_COLOR[tier] || "#64748b";
  return (
    <svg width="96" height="96" viewBox="0 0 96 96">
      <circle cx="48" cy="48" r={r} fill="none" stroke="#1e293b" strokeWidth="10" />
      <circle
        cx="48"
        cy="48"
        r={r}
        fill="none"
        stroke={stroke}
        strokeWidth="10"
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform="rotate(-90 48 48)"
      />
      <text x="48" y="53" textAnchor="middle" fill="#f1f5f9" fontSize="18" fontWeight="bold">
        {Math.round(score)}
      </text>
    </svg>
  );
}

function TierBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  if (!total) return null;
  const segments = [
    { key: "hot", label: "Hot", color: "bg-red-500" },
    { key: "warm", label: "Warm", color: "bg-amber-500" },
    { key: "cold", label: "Cold", color: "bg-sky-500" },
    { key: "dead", label: "Dead", color: "bg-slate-600" },
  ];
  return (
    <div className="mb-6">
      <div className="flex rounded-full overflow-hidden h-3 mb-2">
        {segments.map(({ key, color }) => {
          const pct = ((counts[key] || 0) / total) * 100;
          return pct > 0 ? (
            <div key={key} className={`${color} h-3`} style={{ width: `${pct}%` }} title={`${key}: ${counts[key]}`} />
          ) : null;
        })}
      </div>
      <div className="flex gap-4 text-xs text-slate-400">
        {segments.map(({ key, label, color }) => (
          <span key={key} className="flex items-center gap-1">
            <span className={`inline-block w-2 h-2 rounded-full ${color}`} />
            {label} ({counts[key] || 0})
          </span>
        ))}
      </div>
    </div>
  );
}

function actionLabel(action: string) {
  const map: Record<string, string> = {
    call_now: "Appeler",
    assign_ae: "Assigner AE",
    qualify: "Qualifier",
    nurture: "Nurture",
    disqualify: "Disqualifier",
  };
  return map[action] || action;
}

function intentLabel(intent: string) {
  const map: Record<string, string> = {
    high_intent: "Forte intention",
    medium_intent: "Intention modérée",
    low_intent: "Faible intention",
    no_intent: "Pas d'intention",
  };
  return map[intent] || intent;
}

function sourceLabel(source: string) {
  const map: Record<string, string> = {
    inbound: "Inbound",
    outbound: "Outbound",
    referral: "Referral",
    event: "Événement",
    content: "Contenu",
  };
  return map[source] || source;
}

function LeadCard({ lead, onClick }: { lead: Lead; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className="bg-slate-800/60 border border-slate-700 rounded-xl p-5 cursor-pointer hover:border-slate-500 hover:bg-slate-800 transition-all"
    >
      <div className="flex items-start gap-4 mb-4">
        <ScoreRing score={lead.lead_score} tier={lead.tier} />
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-slate-100 text-base truncate">{lead.company}</h3>
          <p className="text-slate-400 text-sm truncate">{lead.contact_name}</p>
          <p className="text-slate-500 text-xs mt-0.5">{lead.segment} · {sourceLabel(lead.lead_source)}</p>
          <div className="flex flex-wrap gap-1 mt-2">
            <span className={`text-xs px-2 py-0.5 rounded-full border font-medium capitalize ${TIER_BADGE[lead.tier]}`}>
              {lead.tier}
            </span>
            <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${ACTION_BADGE[lead.action]}`}>
              {actionLabel(lead.action)}
            </span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-2 mb-4 text-center">
        <div className="bg-slate-900/50 rounded-lg p-2">
          <div className="text-slate-100 font-bold text-sm">{lead.fit_breakdown.icp}</div>
          <div className="text-slate-500 text-xs">ICP</div>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-2">
          <div className="text-slate-100 font-bold text-sm">{lead.fit_breakdown.engagement}</div>
          <div className="text-slate-500 text-xs">Engagement</div>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-2">
          <div className="text-slate-100 font-bold text-sm">{lead.fit_breakdown.qualification}</div>
          <div className="text-slate-500 text-xs">BANT</div>
        </div>
      </div>

      <div className={`text-xs px-2 py-1 rounded-full border text-center mb-3 ${INTENT_BADGE[lead.intent_signal]}`}>
        {intentLabel(lead.intent_signal)}
      </div>

      <div className="mt-1">
        <div className="flex justify-between text-xs text-slate-500 mb-1">
          <span>Score lead</span>
          <span>{Math.round(lead.lead_score)}/100</span>
        </div>
        <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
          <div
            className="h-1.5 rounded-full"
            style={{
              width: `${lead.lead_score}%`,
              backgroundColor: TIER_COLOR[lead.tier] || "#64748b",
            }}
          />
        </div>
      </div>
    </div>
  );
}

function LeadModal({ lead, onClose }: { lead: Lead; onClose: () => void }) {
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
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-6 border-b border-slate-800 flex items-start gap-4">
          <ScoreRing score={lead.lead_score} tier={lead.tier} />
          <div className="flex-1">
            <h2 className="text-xl font-bold text-slate-100">{lead.company}</h2>
            <p className="text-slate-400 text-sm">{lead.contact_name}</p>
            <p className="text-slate-500 text-xs">{lead.segment} · {sourceLabel(lead.lead_source)}</p>
            <div className="flex flex-wrap gap-2 mt-2">
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium capitalize ${TIER_BADGE[lead.tier]}`}>
                {lead.tier}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${ACTION_BADGE[lead.action]}`}>
                {actionLabel(lead.action)}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full border ${INTENT_BADGE[lead.intent_signal]}`}>
                {intentLabel(lead.intent_signal)}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-2xl leading-none">&times;</button>
        </div>

        <div className="p-6 space-y-5">
          <div className="grid grid-cols-3 gap-3 text-center">
            {[
              { label: "ICP Fit", value: lead.fit_breakdown.icp, max: 35, color: "indigo" },
              { label: "Engagement", value: lead.fit_breakdown.engagement, max: 35, color: "sky" },
              { label: "Qualification", value: lead.fit_breakdown.qualification, max: 30, color: "emerald" },
            ].map(({ label, value, max, color }) => (
              <div key={label} className="bg-slate-800 rounded-xl p-3">
                <div className="text-lg font-bold text-slate-100">{value}</div>
                <div className="text-xs text-slate-400 mb-1">{label}</div>
                <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
                  <div
                    className={`h-1.5 rounded-full bg-${color}-500`}
                    style={{ width: `${(value / max) * 100}%` }}
                  />
                </div>
                <div className="text-xs text-slate-600 mt-0.5">/ {max}</div>
              </div>
            ))}
          </div>

          {lead.strengths.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-emerald-400 mb-2 flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block" />
                Points forts
              </h3>
              <ul className="space-y-1.5">
                {lead.strengths.map((s, i) => (
                  <li key={i} className="text-sm text-slate-300 bg-emerald-900/20 border border-emerald-800/40 rounded-lg px-3 py-2">
                    {s}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {lead.weaknesses.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-red-400 mb-2 flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-red-400 inline-block" />
                Points faibles
              </h3>
              <ul className="space-y-1.5">
                {lead.weaknesses.map((w, i) => (
                  <li key={i} className="text-sm text-slate-300 bg-red-900/20 border border-red-800/40 rounded-lg px-3 py-2">
                    {w}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {lead.recommended_steps.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-indigo-400 mb-2 flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 inline-block" />
                Actions recommandées
              </h3>
              <ol className="space-y-1.5">
                {lead.recommended_steps.map((step, i) => (
                  <li key={i} className="text-sm text-slate-300 bg-indigo-900/20 border border-indigo-800/40 rounded-lg px-3 py-2 flex gap-2">
                    <span className="text-indigo-400 font-bold shrink-0">{i + 1}.</span>
                    {step}
                  </li>
                ))}
              </ol>
            </div>
          )}

          {lead.disqualification_reasons.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-slate-400 mb-2 flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-slate-400 inline-block" />
                Raisons de disqualification
              </h3>
              <ul className="space-y-1.5">
                {lead.disqualification_reasons.map((r, i) => (
                  <li key={i} className="text-sm text-slate-400 bg-slate-800 border border-slate-700 rounded-lg px-3 py-2">
                    {r}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div>
            <h3 className="text-sm font-semibold text-slate-400 mb-2">Fit ICP · {lead.fit_score_label}</h3>
            <div className="text-sm text-slate-500 capitalize">{lead.fit_score_label} fit</div>
          </div>
        </div>
      </div>
    </div>
  );
}

const TIERS = ["all", "hot", "warm", "cold", "dead"];
const ACTIONS = ["all", "call_now", "assign_ae", "qualify", "nurture", "disqualify"];

export default function LeadScoringIntelligencePage() {
  const [data, setData] = useState<{ leads: Lead[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);
  const [tierFilter, setTierFilter] = useState("all");
  const [actionFilter, setActionFilter] = useState("all");

  useEffect(() => {
    async function load() {
      const params = new URLSearchParams();
      if (tierFilter !== "all") params.set("tier", tierFilter);
      if (actionFilter !== "all") params.set("action", actionFilter);
      const res = await fetch(`/api/lead-scoring-intelligence?${params}`);
      const json = await res.json();
      setData(json);
      setLoading(false);
    }
    load();
  }, [tierFilter, actionFilter]);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-400 animate-pulse">Chargement scoring leads...</div>
      </div>
    );
  }

  const s = data!.summary;

  const kpis = [
    { label: "Score Moyen", value: s.avg_lead_score.toFixed(1), sub: "/ 100" },
    { label: "Hot Leads", value: s.hot_count, sub: `${s.hot_rate_pct}% du total` },
    { label: "Appeler Maintenant", value: s.call_now_count, sub: "action urgente" },
    { label: "Disqualifiés", value: s.disqualified_count, sub: "hors critères" },
    { label: "Total Leads", value: s.total, sub: "évalués" },
    { label: "Warm", value: s.tier_counts["warm"] || 0, sub: "à développer" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-100">Scoring Leads IA</h1>
          <p className="text-slate-400 mt-1">Priorisation intelligente des leads par ICP fit, engagement et signaux d'intention</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
          {kpis.map(({ label, value, sub }) => (
            <div key={label} className="bg-slate-800/60 border border-slate-700 rounded-xl p-4">
              <div className="text-2xl font-bold text-slate-100">{value}</div>
              <div className="text-xs text-slate-400 mt-0.5">{label}</div>
              <div className="text-xs text-slate-600 mt-0.5">{sub}</div>
            </div>
          ))}
        </div>

        <TierBar counts={s.tier_counts} total={s.total} />

        <div className="flex flex-wrap gap-2 mb-3">
          {TIERS.map((v) => (
            <button
              key={v}
              onClick={() => setTierFilter(v)}
              className={`text-xs px-3 py-1.5 rounded-full border transition-colors capitalize ${
                tierFilter === v
                  ? "bg-indigo-600 border-indigo-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500"
              }`}
            >
              {v === "all" ? "Tous les tiers" : v}
              {v !== "all" && s.tier_counts[v] ? ` (${s.tier_counts[v]})` : ""}
            </button>
          ))}
        </div>

        <div className="flex flex-wrap gap-2 mb-8">
          {ACTIONS.map((v) => (
            <button
              key={v}
              onClick={() => setActionFilter(v)}
              className={`text-xs px-3 py-1.5 rounded-full border transition-colors ${
                actionFilter === v
                  ? "bg-violet-600 border-violet-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500"
              }`}
            >
              {v === "all" ? "Toutes actions" : actionLabel(v)}
              {v !== "all" && s.action_counts[v] ? ` (${s.action_counts[v]})` : ""}
            </button>
          ))}
        </div>

        {data!.leads.length === 0 ? (
          <div className="text-center text-slate-500 py-20">Aucun lead pour ces filtres</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
            {data!.leads.map((lead) => (
              <LeadCard key={lead.lead_id} lead={lead} onClick={() => setSelectedLead(lead)} />
            ))}
          </div>
        )}
      </div>

      {selectedLead && <LeadModal lead={selectedLead} onClose={() => setSelectedLead(null)} />}
    </div>
  );
}
