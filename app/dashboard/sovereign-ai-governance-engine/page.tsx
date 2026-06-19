"use client";
import { useEffect, useState } from "react";

type AISystem = {
  system_id: string; ai_domain: string; region: string;
  governance_risk: string; governance_pattern: string;
  governance_severity: string; recommended_action: string;
  alignment_risk_score: number; transparency_score: number;
  compliance_score: number; sovereignty_score: number;
  governance_composite: number; has_misalignment_signal: boolean;
  requires_immediate_intervention: boolean; estimated_misalignment_severity_index: number;
  governance_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_governance_composite: number;
  misalignment_signal_count: number; immediate_intervention_count: number;
  avg_alignment_risk_score: number; avg_transparency_score: number;
  avg_compliance_score: number; avg_sovereignty_score: number;
  avg_estimated_misalignment_severity_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36; const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8"/>
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"/>
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string,number>; colors: Record<string,string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-slate-400 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${v / total * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`}/>
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-slate-400">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS  = { low: "#10b981", moderate: "#f59e0b", high: "#f97316", critical: "#ef4444" };
const PAT_COLORS   = { none: "#10b981", alignment_failure: "#ef4444", opacity_crisis: "#a855f7", regulatory_breach: "#dc2626", sovereignty_erosion: "#f97316", bias_amplification: "#ec4899" };
const SEV_COLORS   = { aligned: "#10b981", monitored: "#f59e0b", at_risk: "#f97316", misaligned: "#ef4444" };
const ACT_COLORS   = { no_action: "#10b981", ai_monitoring: "#06b6d4", governance_audit: "#3b82f6", bias_remediation: "#a855f7", alignment_reset: "#f97316", emergency_shutdown: "#7f1d1d" };
const RISK_BADGE   = { low: "bg-emerald-900 text-emerald-300", moderate: "bg-amber-900 text-amber-300", high: "bg-orange-900 text-orange-300", critical: "bg-red-900 text-red-300" };
const SEV_BADGE    = { aligned: "bg-emerald-900 text-emerald-300", monitored: "bg-amber-900 text-amber-300", at_risk: "bg-orange-900 text-orange-300", misaligned: "bg-red-900 text-red-300" };

function DetailModal({ system, onClose }: { system: AISystem; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-blue-500/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{system.system_id}</span>
            <span className="ml-2 text-sky-400 text-xs">{system.ai_domain}</span>
            <span className="ml-2 text-slate-500 text-xs">{system.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-sky-700 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Alignment Risk",  system.alignment_risk_score,  "#ef4444"],
              ["Transparency",    system.transparency_score,    "#a855f7"],
              ["Compliance",      system.compliance_score,      "#f97316"],
              ["Sovereignty",     system.sovereignty_score,     "#0ea5e9"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: c }}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Governance Composite</div>
              <div className="text-white font-bold text-2xl">{system.governance_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {system.governance_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[system.governance_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>{system.governance_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[system.governance_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>{system.governance_severity}</span>
            </div>
          </div>
        )}
        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Recommended Action</div>
              <div className="text-white font-medium">{system.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Misalignment Severity Index</div>
              <div className="text-white font-bold">{system.estimated_misalignment_severity_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {system.has_misalignment_signal        && <span className="px-2 py-1 rounded bg-amber-900 text-amber-300 text-xs font-medium">MISALIGNED</span>}
              {system.requires_immediate_intervention && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">INTERVENTION</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function SovereignAIGovernanceDashboard() {
  const [data, setData]         = useState<{ systems: AISystem[]; summary: Summary } | null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<AISystem | null>(null);

  useEffect(() => {
    fetch("/api/sovereign-ai-governance-engine")
      .then(r => r.json()).then(setData).catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-sky-400 text-lg animate-pulse">Loading Sovereign AI Governance Engine...</div>
    </div>
  );

  const { systems, summary } = data;
  const filtered = systems.filter(s =>
    (filter    === "all" || s.governance_risk    === filter) &&
    (patFilter === "all" || s.governance_pattern === patFilter)
  );

  const dists: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    { title: "Risk",     counts: summary.risk_counts,     colors: RISK_COLORS },
    { title: "Pattern",  counts: summary.pattern_counts,  colors: PAT_COLORS  },
    { title: "Severity", counts: summary.severity_counts, colors: SEV_COLORS  },
    { title: "Action",   counts: summary.action_counts,   colors: ACT_COLORS  },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal system={selected} onClose={() => setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Sovereign AI Governance & Alignment Audit Engine</h1>
        <p className="text-slate-400 text-sm mt-1">Alignment · Transparency · Compliance · Sovereignty — auditing AI governance across deployed systems</p>
      </div>

      {/* 6 KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["AI Systems",      summary.total,                                                            "text-sky-400"],
          ["Avg Composite",   summary.avg_governance_composite,                                         "text-blue-400"],
          ["Misaligned",      summary.misalignment_signal_count,                                        "text-amber-400"],
          ["Intervention",    summary.immediate_intervention_count,                                     "text-red-400"],
          ["Avg Sev Index",   `${summary.avg_estimated_misalignment_severity_index.toFixed(1)}/10`,     "text-sky-400"],
          ["Avg Alignment",   `${Math.round(summary.avg_alignment_risk_score)}`,                        "text-blue-400"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-blue-500/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* 4 GaugeRings */}
      <div className="bg-slate-900 border border-blue-500/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_alignment_risk_score}  label="Alignment Risk"  color="#ef4444"/>
          <GaugeRing value={summary.avg_transparency_score}    label="Transparency"    color="#a855f7"/>
          <GaugeRing value={summary.avg_compliance_score}      label="Compliance"      color="#f97316"/>
          <GaugeRing value={summary.avg_sovereignty_score}     label="Sovereignty"     color="#0ea5e9"/>
        </div>
      </div>

      {/* 4 DistBars */}
      <div className="bg-slate-900 border border-blue-500/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filter pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter === r ? "bg-sky-700 border-sky-600 text-white" : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all", "none", "alignment_failure", "opacity_crisis", "regulatory_breach", "sovereignty_erosion", "bias_amplification"].map(p => (
          <button key={p} onClick={() => setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-blue-900 border-blue-800 text-white" : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* System cards grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(s => (
          <div key={s.system_id} onClick={() => setSelected(s)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-sky-700 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{s.system_id}</span>
              <span className="text-xs text-slate-400">{s.region}</span>
            </div>
            <div className="text-xs text-sky-400 mb-2">{s.ai_domain.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[s.governance_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>{s.governance_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[s.governance_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>{s.governance_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{s.governance_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{s.governance_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-sky-400 font-medium mb-2">Sev Index: {s.estimated_misalignment_severity_index.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {s.has_misalignment_signal        && <span className="px-1.5 py-0.5 rounded bg-amber-900 text-amber-300 text-xs">MISALIGNED</span>}
              {s.requires_immediate_intervention && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">INTERVENTION</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
