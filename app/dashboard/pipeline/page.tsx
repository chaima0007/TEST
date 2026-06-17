"use client";

import { useEffect, useState, useCallback } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface FunnelStage {
  stage: string;
  count: number;
  value_eur: number;
  color: string;
  icon: string;
}

interface Conversion {
  detected_to_qualified: number;
  qualified_to_emailed: number;
  emailed_to_open: number;
  open_to_reply: number;
  reply_to_negotiation: number;
  negotiation_to_payment: number;
  payment_to_delivery: number;
  end_to_end: number;
}

interface GradeRow {
  grade: string;
  count: number;
  avg_score: number;
  recommended_action: string;
}

interface TopLead {
  company_id: string;
  name: string;
  action_score: number;
  grade: string;
  sector: string;
  stage: string;
}

interface PipelineData {
  source: string;
  updated_at: string;
  funnel: FunnelStage[];
  conversions: Conversion;
  grade_breakdown: GradeRow[];
  top_leads: TopLead[];
}

// ── Helpers ────────────────────────────────────────────────────────────────────

const COLOR_MAP: Record<string, { bar: string; text: string; bg: string; border: string }> = {
  indigo:  { bar: "bg-indigo-500",  text: "text-indigo-300",  bg: "bg-indigo-500/10",  border: "border-indigo-500/20" },
  blue:    { bar: "bg-blue-500",    text: "text-blue-300",    bg: "bg-blue-500/10",    border: "border-blue-500/20"   },
  violet:  { bar: "bg-violet-500",  text: "text-violet-300",  bg: "bg-violet-500/10",  border: "border-violet-500/20" },
  purple:  { bar: "bg-purple-500",  text: "text-purple-300",  bg: "bg-purple-500/10",  border: "border-purple-500/20" },
  fuchsia: { bar: "bg-fuchsia-500", text: "text-fuchsia-300", bg: "bg-fuchsia-500/10", border: "border-fuchsia-500/20"},
  pink:    { bar: "bg-pink-500",    text: "text-pink-300",    bg: "bg-pink-500/10",    border: "border-pink-500/20"   },
  emerald: { bar: "bg-emerald-500", text: "text-emerald-300", bg: "bg-emerald-500/10", border: "border-emerald-500/20"},
  green:   { bar: "bg-green-500",   text: "text-green-300",   bg: "bg-green-500/10",   border: "border-green-500/20"  },
};

const GRADE_STYLE: Record<string, string> = {
  S: "text-amber-300 bg-amber-400/10 border-amber-400/25",
  A: "text-emerald-300 bg-emerald-400/10 border-emerald-400/25",
  B: "text-indigo-300 bg-indigo-400/10 border-indigo-400/25",
  C: "text-gray-300 bg-gray-400/8 border-gray-400/15",
  D: "text-red-400 bg-red-400/8 border-red-400/15",
};

const STAGE_STYLE: Record<string, string> = {
  "Livré":    "text-green-400",
  "Payé":     "text-emerald-400",
  "En négo":  "text-fuchsia-400",
  "Répondu":  "text-purple-400",
  "Ouvert":   "text-indigo-400",
  "Emailés":  "text-blue-400",
};

function pct(n: number) {
  return `${(n * 100).toFixed(1)}%`;
}

// ── Components ────────────────────────────────────────────────────────────────

function FunnelBar({ stage, maxCount }: { stage: FunnelStage; maxCount: number }) {
  const c = COLOR_MAP[stage.color] || COLOR_MAP.indigo;
  const width = maxCount > 0 ? Math.max(6, (stage.count / maxCount) * 100) : 6;

  return (
    <div className="group flex items-center gap-3">
      <span className="text-lg w-6 shrink-0">{stage.icon}</span>
      <div className="w-28 shrink-0">
        <p className="text-xs text-gray-400 truncate">{stage.stage}</p>
      </div>
      <div className="flex-1 h-7 bg-white/5 rounded-lg overflow-hidden relative">
        <div
          className={`h-full rounded-lg transition-all duration-500 ${c.bar} opacity-80`}
          style={{ width: `${width}%` }}
        />
        <span className={`absolute inset-0 flex items-center px-3 text-xs font-mono font-semibold ${c.text}`}>
          {stage.count.toLocaleString("fr-FR")}
        </span>
      </div>
      {stage.value_eur > 0 && (
        <span className="text-xs font-mono text-amber-300 shrink-0">
          {(stage.value_eur / 1000).toFixed(0)}k€
        </span>
      )}
    </div>
  );
}

function ConversionRow({ label, value }: { label: string; value: number }) {
  const color = value >= 0.5 ? "text-emerald-400" : value >= 0.3 ? "text-amber-400" : "text-red-400";
  return (
    <div className="flex items-center justify-between text-xs py-1.5 border-b border-white/5 last:border-0">
      <span className="text-gray-400">{label}</span>
      <span className={`font-mono font-semibold ${color}`}>{pct(value)}</span>
    </div>
  );
}

// ── Page ─────────────────────────────────────────────────────────────────────

export default function PipelinePage() {
  const [data, setData] = useState<PipelineData | null>(null);
  const [loading, setLoading] = useState(true);

  const load = useCallback(() => {
    setLoading(true);
    fetch("/api/pipeline")
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => { load(); }, [load]);

  const maxCount = data ? Math.max(...data.funnel.map((s) => s.count)) : 1;

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white p-6 space-y-5">

      {/* Header */}
      <div className="flex items-center justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-3 mb-1">
            <span className="text-2xl">🏗️</span>
            <h1 className="text-2xl font-bold">Pipeline Commercial</h1>
            {data && (
              <span className={`text-xs px-2.5 py-1 rounded-full border font-medium ${
                data.source === "live"
                  ? "text-emerald-400 bg-emerald-400/10 border-emerald-400/20"
                  : "text-amber-400 bg-amber-400/10 border-amber-400/20"
              }`}>
                {data.source === "live" ? "● Live" : "◎ Demo"}
              </span>
            )}
          </div>
          <p className="text-sm text-gray-400">
            Funnel complet : Détection → Qualification → Outreach → Paiement → Livraison
          </p>
        </div>
        <button
          onClick={load}
          className="px-4 py-2 rounded-lg bg-white/5 border border-white/10 text-sm text-gray-300 hover:bg-white/8 transition-all"
        >
          ↻ Actualiser
        </button>
      </div>

      {loading ? (
        <div className="text-center py-16 text-gray-500 text-sm animate-pulse">Chargement du pipeline…</div>
      ) : !data ? null : (
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-5">

          {/* ── Funnel ── */}
          <div className="xl:col-span-2 bg-white/3 border border-white/8 rounded-2xl p-5 space-y-3">
            <h2 className="text-sm font-semibold text-gray-300 mb-4">Entonnoir de conversion</h2>
            {data.funnel.map((stage) => (
              <FunnelBar key={stage.stage} stage={stage} maxCount={maxCount} />
            ))}
            <div className="pt-3 border-t border-white/8">
              <p className="text-xs text-gray-500">
                Conversion bout-en-bout :{" "}
                <span className="font-mono text-amber-300 font-semibold">
                  {pct(data.conversions.end_to_end)}
                </span>
                {" "}— {data.funnel[0].count} prospects → {data.funnel[data.funnel.length - 1].count} livrés
              </p>
            </div>
          </div>

          {/* ── Conversion rates ── */}
          <div className="bg-white/3 border border-white/8 rounded-2xl p-5">
            <h2 className="text-sm font-semibold text-gray-300 mb-3">Taux de conversion / étape</h2>
            <ConversionRow label="Détectés → Qualifiés" value={data.conversions.detected_to_qualified} />
            <ConversionRow label="Qualifiés → Emailés" value={data.conversions.qualified_to_emailed} />
            <ConversionRow label="Emailés → Ouvert" value={data.conversions.emailed_to_open} />
            <ConversionRow label="Ouvert → Répondu" value={data.conversions.open_to_reply} />
            <ConversionRow label="Répondu → En négo" value={data.conversions.reply_to_negotiation} />
            <ConversionRow label="Négo → Paiement" value={data.conversions.negotiation_to_payment} />
            <ConversionRow label="Paiement → Livré" value={data.conversions.payment_to_delivery} />
          </div>

          {/* ── Grade breakdown ── */}
          <div className="bg-white/3 border border-white/8 rounded-2xl p-5">
            <h2 className="text-sm font-semibold text-gray-300 mb-4">Répartition par grade (LeadScorer)</h2>
            <div className="space-y-3">
              {data.grade_breakdown.map((row) => (
                <div key={row.grade} className="flex items-center gap-3">
                  <span className={`text-xs font-bold px-2 py-1 rounded border min-w-[28px] text-center ${GRADE_STYLE[row.grade]}`}>
                    {row.grade}
                  </span>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-0.5">
                      <span className="text-xs text-gray-400 truncate max-w-[140px]">{row.recommended_action}</span>
                      <span className="text-xs font-mono text-gray-300">{row.count}</span>
                    </div>
                    <div className="w-full h-1.5 bg-white/8 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full ${GRADE_STYLE[row.grade].split(" ")[0].replace("text-", "bg-")}`}
                        style={{ width: `${(row.count / 850) * 100}%` }}
                      />
                    </div>
                  </div>
                  <span className="text-xs font-mono text-gray-500 shrink-0">{row.avg_score.toFixed(1)}</span>
                </div>
              ))}
            </div>
          </div>

          {/* ── Top Leads ── */}
          <div className="xl:col-span-2 bg-white/3 border border-white/8 rounded-2xl p-5">
            <h2 className="text-sm font-semibold text-gray-300 mb-4">Top Leads — Score le plus haut</h2>
            <div className="space-y-2">
              {data.top_leads.map((lead) => (
                <div key={lead.company_id} className="flex items-center gap-3 p-3 bg-white/3 rounded-xl hover:bg-white/5 transition-colors">
                  <span className={`text-xs font-bold px-2 py-0.5 rounded border ${GRADE_STYLE[lead.grade]}`}>
                    {lead.grade}
                  </span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold text-white truncate">{lead.name}</p>
                    <p className="text-xs text-gray-500 truncate">{lead.sector}</p>
                  </div>
                  <span className={`text-xs font-medium shrink-0 ${STAGE_STYLE[lead.stage] || "text-gray-400"}`}>
                    {lead.stage}
                  </span>
                  <div className="shrink-0 text-right">
                    <p className="text-sm font-bold font-mono text-indigo-300">{lead.action_score.toFixed(1)}</p>
                    <p className="text-xs text-gray-500">score</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>
      )}
    </div>
  );
}
