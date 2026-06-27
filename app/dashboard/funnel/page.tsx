"use client";

import { useEffect, useState } from "react";

// ── Types ──────────────────────────────────────────────────────────────────────

type FunnelStage = "lead" | "contacted" | "opened" | "replied" | "demo" | "quoted" | "negotiating" | "won" | "lost";

interface ProspectRecord { prospect_id: string; company_name: string; sector: string; current_stage: FunnelStage; quote_value: number; is_active: boolean; is_won: boolean; days_in_funnel: number; stages_reached: FunnelStage[]; }
interface TransitionStats { from_stage: FunnelStage; to_stage: FunnelStage; prospects_entered: number; prospects_converted: number; conversion_rate_pct: number; drop_off_rate_pct: number; }
interface Summary { total_prospects: number; active: number; won: number; lost: number; overall_cvr_pct: number; total_pipeline_eur: number; total_won_eur: number; avg_deal_size_eur: number; avg_days_to_close: number; stage_counts: Record<string, number>; }
interface Data { source: string; prospects: ProspectRecord[]; stage_report: TransitionStats[]; summary: Summary; }

// ── Constants ──────────────────────────────────────────────────────────────────

const STAGE_LABELS: Record<FunnelStage, string> = {
  lead: "Leads", contacted: "Contactés", opened: "Ouverts", replied: "Répondus",
  demo: "Démo", quoted: "Devisés", negotiating: "Négo", won: "Gagnés", lost: "Perdus",
};

const STAGE_COLORS: Record<FunnelStage, string> = {
  lead: "bg-gray-500/20 text-gray-300 border-gray-500/30",
  contacted: "bg-blue-500/20 text-blue-300 border-blue-500/30",
  opened: "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
  replied: "bg-indigo-500/20 text-indigo-300 border-indigo-500/30",
  demo: "bg-violet-500/20 text-violet-300 border-violet-500/30",
  quoted: "bg-amber-500/20 text-amber-300 border-amber-500/30",
  negotiating: "bg-orange-500/20 text-orange-300 border-orange-500/30",
  won: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
  lost: "bg-red-500/20 text-red-300 border-red-500/30",
};

const ORDERED_STAGES: FunnelStage[] = ["lead","contacted","opened","replied","demo","quoted","negotiating","won"];

// ── Helpers ────────────────────────────────────────────────────────────────────

function eur(n: number) { return `${n.toLocaleString("fr-FR", { maximumFractionDigits: 0 })} €`; }
function cap(s: string) { return s.charAt(0).toUpperCase() + s.slice(1); }

function StageBadge({ stage }: { stage: FunnelStage }) {
  return <span className={`text-xs px-2 py-0.5 rounded-full border ${STAGE_COLORS[stage]}`}>{STAGE_LABELS[stage]}</span>;
}

// ── Visual funnel ──────────────────────────────────────────────────────────────

function FunnelBar({ stage, count, max, cvr }: { stage: FunnelStage; count: number; max: number; cvr?: number }) {
  const width = max > 0 ? Math.max(5, Math.round(count / max * 100)) : 5;
  const isWon = stage === "won";
  const color = isWon ? "bg-emerald-500" : "bg-indigo-500";

  return (
    <div className="flex items-center gap-3">
      <div className="w-24 text-right text-xs text-gray-400 truncate">{STAGE_LABELS[stage]}</div>
      <div className="flex-1 relative">
        <div className="h-8 bg-white/[0.04] rounded-lg overflow-hidden">
          <div className={`h-full ${color} rounded-lg flex items-center px-3 transition-all`} style={{ width: `${width}%` }}>
            {count > 0 && <span className="text-white text-xs font-bold">{count}</span>}
          </div>
        </div>
      </div>
      {cvr !== undefined && (
        <div className="w-14 text-right text-xs">
          <span className={cvr >= 60 ? "text-emerald-400" : cvr >= 35 ? "text-amber-400" : "text-red-400"}>
            {cvr}%
          </span>
        </div>
      )}
    </div>
  );
}

// ── Prospect row modal ────────────────────────────────────────────────────────

function ProspectModal({ p, onClose }: { p: ProspectRecord; onClose: () => void }) {
  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-[#0f1117] border border-white/[0.08] rounded-2xl w-full max-w-md" onClick={e => e.stopPropagation()}>
        <div className="flex items-start justify-between p-5 border-b border-white/[0.06]">
          <div>
            <h2 className="font-bold text-lg">{p.company_name}</h2>
            <p className="text-sm text-gray-500">{cap(p.sector)}</p>
          </div>
          <button onClick={onClose} className="text-gray-500 hover:text-white text-xl">×</button>
        </div>
        <div className="p-5 space-y-4">
          <div className="flex gap-2 items-center">
            <StageBadge stage={p.current_stage} />
            <span className="text-xs text-gray-500">{p.days_in_funnel} j. dans le funnel</span>
          </div>
          {p.quote_value > 0 && (
            <div className="bg-white/[0.03] rounded-xl p-3 border border-white/[0.07]">
              <p className="text-xs text-gray-500">Valeur devis</p>
              <p className="text-xl font-bold text-amber-400">{eur(p.quote_value)}</p>
            </div>
          )}
          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Progression</p>
            <div className="flex flex-wrap gap-1">
              {ORDERED_STAGES.map(s => {
                const reached = p.stages_reached.includes(s);
                const current = p.current_stage === s;
                return (
                  <span key={s} className={`text-[10px] px-2 py-0.5 rounded-full border ${current ? STAGE_COLORS[s] : reached ? "bg-white/[0.04] border-white/[0.08] text-gray-400" : "bg-transparent border-transparent text-gray-700"}`}>
                    {STAGE_LABELS[s]}
                  </span>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Page ───────────────────────────────────────────────────────────────────────

export default function FunnelPage() {
  const [data, setData]       = useState<Data | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<ProspectRecord | null>(null);
  const [stageFilter, setStageFilter] = useState<FunnelStage | "all">("all");

  useEffect(() => {
    fetch("/api/funnel").then(r => r.json()).then(setData).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex items-center justify-center h-64"><div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" /></div>;
  if (!data)   return <p className="text-gray-500 p-8">Erreur de chargement.</p>;

  const { summary, prospects, stage_report } = data;
  const max = Math.max(...ORDERED_STAGES.map(s => summary.stage_counts[s] ?? 0), 1);

  const filtered = stageFilter === "all"
    ? prospects
    : prospects.filter(p => p.current_stage === stageFilter);

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      {selected && <ProspectModal p={selected} onClose={() => setSelected(null)} />}

      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Funnel de Conversion</h1>
          <p className="text-sm text-gray-500 mt-0.5">Progression des prospects de Lead à Client</p>
        </div>
        {data.source === "mock" && <span className="text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2 py-1 rounded-full">Données démo</span>}
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: "Total prospects",  value: String(summary.total_prospects),            color: "text-white"       },
          { label: "Taux de closing",  value: `${summary.overall_cvr_pct}%`,              color: "text-emerald-400" },
          { label: "Pipeline TTC",     value: eur(summary.total_pipeline_eur),            color: "text-amber-400"   },
          { label: "CA gagné",         value: eur(summary.total_won_eur),                 color: "text-indigo-400"  },
        ].map(k => (
          <div key={k.label} className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">{k.label}</p>
            <p className={`text-2xl font-bold ${k.color}`}>{k.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Visual funnel */}
        <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-5">
          <h2 className="text-sm font-semibold text-gray-300 mb-4">Entonnoir de conversion</h2>
          <div className="space-y-2">
            {ORDERED_STAGES.map((stage, i) => {
              const count = summary.stage_counts[stage] ?? 0;
              const trans = stage_report.find(r => r.from_stage === stage);
              return <FunnelBar key={stage} stage={stage} count={count} max={max} cvr={trans?.conversion_rate_pct} />;
            })}
          </div>
          <p className="text-[10px] text-gray-600 mt-3 text-right">% = taux de passage vers l'étape suivante</p>
        </div>

        {/* Stage transition table */}
        <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-5">
          <h2 className="text-sm font-semibold text-gray-300 mb-4">Taux de conversion par étape</h2>
          <div className="space-y-2">
            {stage_report.map(t => (
              <div key={`${t.from_stage}-${t.to_stage}`} className="flex items-center gap-2 text-xs">
                <span className="text-gray-500 w-20 truncate">{STAGE_LABELS[t.from_stage as FunnelStage]}</span>
                <span className="text-gray-700">→</span>
                <span className="text-gray-400 w-20 truncate">{STAGE_LABELS[t.to_stage as FunnelStage]}</span>
                <div className="flex-1">
                  <div className="h-1.5 bg-white/[0.05] rounded-full overflow-hidden">
                    <div className={`h-full rounded-full ${t.conversion_rate_pct >= 60 ? "bg-emerald-500" : t.conversion_rate_pct >= 35 ? "bg-amber-500" : "bg-red-500"}`}
                      style={{ width: `${t.conversion_rate_pct}%` }} />
                  </div>
                </div>
                <span className={`w-10 text-right font-mono ${t.conversion_rate_pct >= 60 ? "text-emerald-400" : t.conversion_rate_pct >= 35 ? "text-amber-400" : "text-red-400"}`}>
                  {t.conversion_rate_pct}%
                </span>
                <span className="text-gray-600 w-14 text-right">{t.prospects_converted}/{t.prospects_entered}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Secondary KPIs */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: "Deal moyen",       value: eur(summary.avg_deal_size_eur),             color: "text-white"       },
          { label: "Jours → closing",  value: `${summary.avg_days_to_close}j`,            color: "text-gray-300"    },
          { label: "Actifs",           value: String(summary.active),                     color: "text-indigo-400"  },
          { label: "Perdus",           value: String(summary.lost),                       color: "text-red-400"     },
        ].map(k => (
          <div key={k.label} className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">{k.label}</p>
            <p className={`text-2xl font-bold ${k.color}`}>{k.value}</p>
          </div>
        ))}
      </div>

      {/* Stage filter tabs */}
      <div className="flex gap-2 flex-wrap">
        <button onClick={() => setStageFilter("all")}
          className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${stageFilter === "all" ? "bg-indigo-600 border-indigo-500 text-white" : "bg-white/[0.03] border-white/[0.07] text-gray-400 hover:text-white"}`}>
          Tous ({summary.total_prospects})
        </button>
        {ORDERED_STAGES.map(s => {
          const cnt = summary.stage_counts[s] ?? 0;
          return (
            <button key={s} onClick={() => setStageFilter(s)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${stageFilter === s ? "bg-indigo-600 border-indigo-500 text-white" : "bg-white/[0.03] border-white/[0.07] text-gray-400 hover:text-white"}`}>
              {STAGE_LABELS[s]} {cnt > 0 ? `(${cnt})` : ""}
            </button>
          );
        })}
      </div>

      {/* Prospect table */}
      <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[600px]">
            <thead>
              <tr className="border-b border-white/[0.06]">
                {["Entreprise","Secteur","Étape","Valeur devis","Jours"].map(h => (
                  <th key={h} className="text-left py-3 px-4 text-xs text-gray-500 uppercase tracking-wider font-medium">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 ? (
                <tr><td colSpan={5} className="text-center py-10 text-gray-600 text-sm">Aucun prospect.</td></tr>
              ) : filtered.map(p => (
                <tr key={p.prospect_id} className="border-b border-white/[0.04] hover:bg-white/[0.02] cursor-pointer" onClick={() => setSelected(p)}>
                  <td className="py-3 px-4">
                    <p className="font-medium text-sm">{p.company_name}</p>
                    <p className="text-xs text-gray-600">{p.prospect_id}</p>
                  </td>
                  <td className="py-3 px-4 text-xs text-gray-400">{cap(p.sector)}</td>
                  <td className="py-3 px-4"><StageBadge stage={p.current_stage} /></td>
                  <td className="py-3 px-4 text-sm font-mono text-right">
                    {p.quote_value > 0 ? <span className="text-amber-400">{eur(p.quote_value)}</span> : <span className="text-gray-700">—</span>}
                  </td>
                  <td className="py-3 px-4 text-xs text-gray-500 text-center">{p.days_in_funnel}j</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <p className="text-xs text-gray-600 text-center">{filtered.length} prospect(s) — Cliquer pour le détail</p>
    </div>
  );
}
