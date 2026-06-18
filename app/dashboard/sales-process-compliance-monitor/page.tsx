"use client";

import { useEffect, useState } from "react";

type ComplianceLevel      = "full" | "partial" | "minimal" | "non_compliant";
type MethodologyAdherence = "champion" | "solid" | "improvable" | "at_risk";
type ComplianceRisk       = "low" | "moderate" | "high" | "critical";
type ComplianceAction     = "maintain" | "coach_gaps" | "process_review" | "remediate";

interface Deal {
  deal_id: string;
  rep_id: string;
  rep_name: string;
  region: string;
  compliance_level: ComplianceLevel;
  methodology_adherence: MethodologyAdherence;
  compliance_risk: ComplianceRisk;
  compliance_action: ComplianceAction;
  discovery_score: number;
  qualification_score: number;
  progression_score: number;
  crm_hygiene_score: number;
  compliance_composite: number;
  missing_steps_count: number;
  is_compliant: boolean;
  needs_process_coaching: boolean;
  key_gap: string;
  deal_stage: string;
}

interface Summary {
  total: number;
  compliance_level_counts: Record<string, number>;
  methodology_adherence_counts: Record<string, number>;
  compliance_risk_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_compliance_composite: number;
  fully_compliant_count: number;
  coaching_needed_count: number;
  avg_discovery_score: number;
  avg_qualification_score: number;
  avg_progression_score: number;
  avg_crm_hygiene_score: number;
  avg_missing_steps: number;
}

const LEVEL_COLOR: Record<ComplianceLevel, string> = {
  full:          "text-emerald-400",
  partial:       "text-indigo-400",
  minimal:       "text-amber-400",
  non_compliant: "text-red-400",
};

const RISK_COLOR: Record<ComplianceRisk, string> = {
  low:      "bg-emerald-500/20 text-emerald-300",
  moderate: "bg-amber-500/20  text-amber-300",
  high:     "bg-orange-500/20 text-orange-300",
  critical: "bg-red-500/20    text-red-300",
};

const ADH_COLOR: Record<MethodologyAdherence, string> = {
  champion:   "bg-emerald-500/20 text-emerald-300",
  solid:      "bg-indigo-500/20  text-indigo-300",
  improvable: "bg-amber-500/20   text-amber-300",
  at_risk:    "bg-red-500/20     text-red-300",
};

function fmtLabel(s: string): string {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function compositeColor(v: number): string {
  if (v >= 75) return "#34d399";
  if (v >= 55) return "#818cf8";
  if (v >= 40) return "#fbbf24";
  return "#f87171";
}

function ComplianceRing({ value, label }: { value: number; label: string }) {
  const r = 38;
  const circ = 2 * Math.PI * r;
  const fill = (value / 100) * circ;
  const color = compositeColor(value);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="92" height="92" viewBox="0 0 92 92">
        <circle cx="46" cy="46" r={r} fill="none" stroke="#1e293b" strokeWidth="9" />
        <circle cx="46" cy="46" r={r} fill="none" stroke={color} strokeWidth="9"
          strokeDasharray={`${fill} ${circ}`} strokeLinecap="round"
          transform="rotate(-90 46 46)" />
        <text x="46" y="43" textAnchor="middle" fill={color} fontSize="14" fontWeight="bold">{value}</text>
        <text x="46" y="55" textAnchor="middle" fill="#94a3b8" fontSize="7">/ 100</text>
      </svg>
      <span className="text-xs text-slate-400">{label}</span>
    </div>
  );
}

function LevelDistBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const order: ComplianceLevel[] = ["full", "partial", "minimal", "non_compliant"];
  const colors: Record<string, string> = {
    full: "bg-emerald-500", partial: "bg-indigo-500",
    minimal: "bg-amber-500", non_compliant: "bg-red-500",
  };
  return (
    <div className="space-y-2">
      <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
        {order.map((l) => {
          const pct = total > 0 ? ((counts[l] || 0) / total) * 100 : 0;
          return pct > 0 ? (
            <div key={l} className={`${colors[l]}`} style={{ width: `${pct}%` }} title={`${l}: ${counts[l] || 0}`} />
          ) : null;
        })}
      </div>
      <div className="flex flex-wrap gap-3">
        {order.map((l) => (
          <div key={l} className="flex items-center gap-1.5">
            <div className={`w-2 h-2 rounded-full ${colors[l]}`} />
            <span className="text-xs text-slate-400">{fmtLabel(l)}: {counts[l] || 0}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function DealCard({ deal, onClick }: { deal: Deal; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="w-full text-left bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-indigo-500/50 transition-all"
    >
      <div className="flex items-start justify-between mb-3">
        <div>
          <p className="font-semibold text-slate-100">{deal.rep_name}</p>
          <p className="text-xs text-slate-500">{deal.deal_id} · {deal.deal_stage} · {deal.region}</p>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className={`text-xs font-medium ${LEVEL_COLOR[deal.compliance_level]}`}>
            {fmtLabel(deal.compliance_level)}
          </span>
          <span className={`text-xs px-2 py-0.5 rounded-full ${RISK_COLOR[deal.compliance_risk]}`}>
            {deal.compliance_risk} risk
          </span>
        </div>
      </div>

      <div className="flex items-center gap-3 mb-3">
        <div className="flex-1">
          <div className="flex justify-between text-xs text-slate-500 mb-1">
            <span>Compliance score</span>
            <span>{deal.missing_steps_count} gaps</span>
          </div>
          <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full rounded-full"
              style={{ width: `${deal.compliance_composite}%`, backgroundColor: compositeColor(deal.compliance_composite) }} />
          </div>
        </div>
        <div className="text-right">
          <p className="text-lg font-bold" style={{ color: compositeColor(deal.compliance_composite) }}>
            {deal.compliance_composite}
          </p>
          <p className="text-xs text-slate-500">composite</p>
        </div>
      </div>

      <div className="flex items-center justify-between">
        <span className={`text-xs px-2 py-0.5 rounded-full ${ADH_COLOR[deal.methodology_adherence]}`}>
          {deal.methodology_adherence}
        </span>
        {deal.needs_process_coaching && (
          <span className="text-xs bg-red-500/20 text-red-300 px-2 py-0.5 rounded-full">Coaching Needed</span>
        )}
        {deal.is_compliant && !deal.needs_process_coaching && (
          <span className="text-xs bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-full">Compliant</span>
        )}
      </div>
    </button>
  );
}

function DealModal({ deal, onClose }: { deal: Deal; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "steps" | "actions">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const scores = [
    { label: "Discovery",      value: deal.discovery_score },
    { label: "Qualification",  value: deal.qualification_score },
    { label: "Progression",    value: deal.progression_score },
    { label: "CRM Hygiene",    value: deal.crm_hygiene_score },
  ];

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}>
        <div className="p-5 border-b border-slate-800">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-100">{deal.rep_name}</h2>
              <p className="text-sm text-slate-400">{deal.deal_id} · {deal.deal_stage} · {deal.region}</p>
              <div className="flex gap-2 mt-2">
                <span className={`text-xs px-2 py-0.5 rounded-full ${ADH_COLOR[deal.methodology_adherence]}`}>
                  {deal.methodology_adherence}
                </span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${RISK_COLOR[deal.compliance_risk]}`}>
                  {deal.compliance_risk} risk
                </span>
              </div>
            </div>
            <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl">×</button>
          </div>
        </div>

        <div className="flex border-b border-slate-800">
          {(["scores", "steps", "actions"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm capitalize transition-colors ${
                tab === t ? "border-b-2 border-indigo-500 text-indigo-400" : "text-slate-500 hover:text-slate-300"
              }`}>
              {t}
            </button>
          ))}
        </div>

        <div className="p-5">
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
                <span className="text-sm text-slate-300">Compliance Composite</span>
                <span className="text-2xl font-bold" style={{ color: compositeColor(deal.compliance_composite) }}>
                  {deal.compliance_composite}
                </span>
              </div>
            </div>
          )}

          {tab === "steps" && (
            <div className="space-y-3">
              <div className="bg-amber-500/10 border border-amber-500/30 rounded-lg p-3">
                <p className="text-xs text-amber-400 mb-1">Key Gap</p>
                <p className="text-sm text-amber-300">{deal.key_gap}</p>
              </div>
              {[
                { label: "Missing Steps", value: `${deal.missing_steps_count}` },
                { label: "Is Compliant", value: deal.is_compliant ? "Yes" : "No" },
                { label: "Needs Coaching", value: deal.needs_process_coaching ? "Yes" : "No" },
                { label: "Level", value: fmtLabel(deal.compliance_level) },
                { label: "Adherence", value: fmtLabel(deal.methodology_adherence) },
              ].map(({ label, value }) => (
                <div key={label} className="flex justify-between py-2 border-b border-slate-800">
                  <span className="text-sm text-slate-400">{label}</span>
                  <span className="text-sm font-medium text-slate-200">{value}</span>
                </div>
              ))}
            </div>
          )}

          {tab === "actions" && (
            <div className="space-y-4">
              <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-lg p-4">
                <p className="text-xs text-indigo-400 mb-1">Recommended Action</p>
                <p className="font-semibold text-indigo-300">{fmtLabel(deal.compliance_action)}</p>
              </div>
              <div className="space-y-2 text-sm text-slate-300">
                {deal.compliance_action === "maintain" && <p>Deal execution is exemplary. Use this deal as a coaching case study for the team.</p>}
                {deal.compliance_action === "coach_gaps" && <p>Address the key gap "{deal.key_gap}" in the next 1-on-1. Review discovery and qualification completeness.</p>}
                {deal.compliance_action === "process_review" && <p>Schedule a full deal review with the manager. Rebuild the process from the key gap forward.</p>}
                {deal.compliance_action === "remediate" && <p>Immediate intervention required. Assign a deal coach and rebuild compliance from scratch — start with: {deal.key_gap}.</p>}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function SalesProcessCompliancePage() {
  const [data, setData] = useState<{ deals: Deal[]; summary: Summary } | null>(null);
  const [level,  setLevel]  = useState("");
  const [risk,   setRisk]   = useState("");
  const [region, setRegion] = useState("");
  const [selected, setSelected] = useState<Deal | null>(null);

  useEffect(() => {
    const params = new URLSearchParams();
    if (level)  params.set("level", level);
    if (risk)   params.set("risk", risk);
    if (region) params.set("region", region);
    fetch(`/api/sales-process-compliance-monitor?${params}`)
      .then((r) => r.json())
      .then(setData);
  }, [level, risk, region]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400">Loading…</div>
    </div>
  );

  const { deals, summary } = data;

  const kpis = [
    { label: "Total Deals",       value: summary.total },
    { label: "Fully Compliant",   value: summary.fully_compliant_count, sub: `${Math.round((summary.fully_compliant_count / summary.total) * 100)}%` },
    { label: "Coaching Needed",   value: summary.coaching_needed_count },
    { label: "Avg Composite",     value: summary.avg_compliance_composite },
    { label: "Avg Missing Steps", value: summary.avg_missing_steps },
    { label: "Avg CRM Score",     value: summary.avg_crm_hygiene_score },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <div>
          <h1 className="text-2xl font-bold">Sales Process Compliance Monitor</h1>
          <p className="text-slate-400 text-sm mt-1">MEDDPICC methodology adherence tracking across all deals</p>
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
            <h2 className="text-sm font-semibold text-slate-300 mb-4">Compliance Level Distribution</h2>
            <LevelDistBar counts={summary.compliance_level_counts} total={summary.total} />
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-4">Average Scores</h2>
            <div className="flex justify-around">
              <ComplianceRing value={summary.avg_discovery_score}     label="Discovery" />
              <ComplianceRing value={summary.avg_qualification_score} label="Qualify" />
              <ComplianceRing value={summary.avg_progression_score}   label="Progress" />
              <ComplianceRing value={summary.avg_crm_hygiene_score}   label="CRM" />
            </div>
          </div>
        </div>

        <div className="flex flex-wrap gap-3">
          <select value={level} onChange={(e) => setLevel(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-slate-300 rounded-lg px-3 py-2 text-sm">
            <option value="">All Levels</option>
            {["full", "partial", "minimal", "non_compliant"].map((l) => (
              <option key={l} value={l}>{fmtLabel(l)}</option>
            ))}
          </select>
          <select value={risk} onChange={(e) => setRisk(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-slate-300 rounded-lg px-3 py-2 text-sm">
            <option value="">All Risks</option>
            {["low", "moderate", "high", "critical"].map((r) => (
              <option key={r} value={r}>{fmtLabel(r)}</option>
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
          {deals.map((deal) => (
            <DealCard key={deal.deal_id} deal={deal} onClick={() => setSelected(deal)} />
          ))}
        </div>
      </div>

      {selected && <DealModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
