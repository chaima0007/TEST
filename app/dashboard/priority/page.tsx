"use client";

import { useEffect, useState } from "react";

type LeadPriority = "hot" | "warm" | "cold" | "dormant";

interface LeadSignals {
  lead_id: string;
  name: string;
  company: string;
  sector: string;
  days_since_last_contact: number;
  response_rate: number;
  deal_value_eur: number;
  days_in_pipeline: number;
  open_rate: number;
  meetings_completed: number;
  proposal_sent: boolean;
}

interface ScoreBreakdown {
  recency: number;
  responsiveness: number;
  deal_value: number;
  engagement: number;
  activity: number;
  pipeline_health: number;
}

interface PrioritizedLead {
  signals: LeadSignals;
  priority_score: number;
  priority_tier: LeadPriority;
  score_breakdown: ScoreBreakdown;
  action_items: string[];
  risk_flags: string[];
}

interface Summary {
  total: number;
  tier_counts: Record<LeadPriority, number>;
  avg_score: number;
  total_pipeline_value: number;
  at_risk_count: number;
}

interface SectorStat {
  sector: string;
  count: number;
  avg_score: number;
  hot_count: number;
  total_value_eur: number;
}

const TIER_STYLES: Record<LeadPriority, { bg: string; text: string; border: string; dot: string; label: string }> = {
  hot:     { bg: "bg-red-900/40",     text: "text-red-300",    border: "border-red-700/60",    dot: "bg-red-400",    label: "HOT" },
  warm:    { bg: "bg-orange-900/40",  text: "text-orange-300", border: "border-orange-700/60", dot: "bg-orange-400", label: "WARM" },
  cold:    { bg: "bg-blue-900/30",    text: "text-blue-300",   border: "border-blue-700/40",   dot: "bg-blue-400",   label: "COLD" },
  dormant: { bg: "bg-slate-800/60",   text: "text-slate-400",  border: "border-slate-700",     dot: "bg-slate-500",  label: "DORMANT" },
};

const DIM_LABELS: Record<keyof ScoreBreakdown, string> = {
  recency: "Récence",
  responsiveness: "Réactivité",
  deal_value: "Valeur deal",
  engagement: "Engagement",
  activity: "Activité",
  pipeline_health: "Santé pipeline",
};

function TierBadge({ tier }: { tier: LeadPriority }) {
  const s = TIER_STYLES[tier];
  return (
    <span className={`text-[10px] font-bold px-2 py-0.5 rounded border flex items-center gap-1 ${s.bg} ${s.text} ${s.border}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${s.dot}`} />
      {s.label}
    </span>
  );
}

function ScoreBar({ label, value }: { label: string; value: number }) {
  const color = value >= 70 ? "bg-emerald-500" : value >= 50 ? "bg-amber-400" : value >= 30 ? "bg-orange-400" : "bg-red-500";
  return (
    <div>
      <div className="flex justify-between text-[10px] text-slate-400 mb-0.5">
        <span>{label}</span>
        <span className="font-mono">{Math.round(value)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full ${color} rounded-full`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

function KpiCard({ label, value, sub, accent }: { label: string; value: string | number; sub?: string; accent?: string }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
      <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-1">{label}</p>
      <p className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</p>
      {sub && <p className="text-xs text-slate-500 mt-0.5">{sub}</p>}
    </div>
  );
}

function LeadModal({ lead, onClose }: { lead: PrioritizedLead; onClose: () => void }) {
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const s = TIER_STYLES[lead.priority_tier];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60" onClick={onClose}>
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="px-6 py-4 border-b border-slate-800 flex items-start justify-between gap-3">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <h2 className="text-lg font-bold text-white">{lead.signals.name}</h2>
              <TierBadge tier={lead.priority_tier} />
            </div>
            <p className="text-xs text-slate-500">{lead.signals.company} · {lead.signals.sector}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none flex-shrink-0">×</button>
        </div>

        <div className="p-6 space-y-5">
          {/* Priority score */}
          <div className={`rounded-xl p-4 border ${s.bg} ${s.border} text-center`}>
            <p className="text-xs text-slate-400 mb-1">Score de priorité</p>
            <p className={`text-4xl font-bold ${s.text}`}>{lead.priority_score}</p>
            <p className="text-xs text-slate-500 mt-1">/100</p>
          </div>

          {/* Score breakdown */}
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-3">Détail du score</p>
            <div className="space-y-2">
              {(Object.entries(lead.score_breakdown) as [keyof ScoreBreakdown, number][]).map(([k, v]) => (
                <ScoreBar key={k} label={DIM_LABELS[k]} value={v} />
              ))}
            </div>
          </div>

          {/* Risk flags */}
          {lead.risk_flags.length > 0 && (
            <div>
              <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-2">Signaux de risque</p>
              <ul className="space-y-1.5">
                {lead.risk_flags.map((f, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-red-400 flex-shrink-0 mt-0.5">⚠</span>
                    {f}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Action items */}
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-2">Actions recommandées</p>
            <ul className="space-y-1.5">
              {lead.action_items.map((a, i) => (
                <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                  <span className="text-indigo-400 flex-shrink-0 mt-0.5">→</span>
                  {a}
                </li>
              ))}
            </ul>
          </div>

          {/* Raw signals */}
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-2">Données brutes</p>
            <div className="grid grid-cols-2 gap-2 text-xs">
              {[
                ["Dernier contact", `${lead.signals.days_since_last_contact}j`],
                ["Taux de réponse", `${Math.round(lead.signals.response_rate * 100)}%`],
                ["Valeur deal", `${lead.signals.deal_value_eur.toLocaleString("fr-FR")}€`],
                ["Jours pipeline", `${lead.signals.days_in_pipeline}j`],
                ["Taux ouverture", `${Math.round(lead.signals.open_rate * 100)}%`],
                ["Réunions", `${lead.signals.meetings_completed}`],
                ["Devis envoyé", lead.signals.proposal_sent ? "Oui" : "Non"],
              ].map(([k, v]) => (
                <div key={String(k)} className="bg-slate-800 rounded-lg px-3 py-2">
                  <p className="text-slate-500">{k}</p>
                  <p className="text-white font-mono font-medium">{v}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function PriorityPage() {
  const [data, setData] = useState<{
    leads: PrioritizedLead[];
    summary: Summary;
    sector_stats: SectorStat[];
  } | null>(null);
  const [loading, setLoading] = useState(true);
  const [tierFilter, setTierFilter] = useState<LeadPriority | "all">("all");
  const [selected, setSelected] = useState<PrioritizedLead | null>(null);

  useEffect(() => {
    fetch("/api/priority")
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-6 text-slate-500 text-center py-16">Chargement…</div>;
  if (!data) return null;

  const { leads, summary, sector_stats } = data;

  const filtered = tierFilter === "all" ? leads : leads.filter((l) => l.priority_tier === tierFilter);

  const tierTabs: { key: LeadPriority | "all"; label: string }[] = [
    { key: "all",     label: `Tous (${summary.total})` },
    { key: "hot",     label: `HOT (${summary.tier_counts.hot})` },
    { key: "warm",    label: `WARM (${summary.tier_counts.warm})` },
    { key: "cold",    label: `COLD (${summary.tier_counts.cold})` },
    { key: "dormant", label: `DORMANT (${summary.tier_counts.dormant})` },
  ];

  return (
    <div className="p-6 space-y-6 text-slate-100">
      {selected && <LeadModal lead={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-white">Priorité Leads</h1>
        <p className="text-slate-400 text-sm mt-1">
          Classement par urgence — récence, réactivité, valeur, engagement, activité, santé pipeline
        </p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard label="Leads en pipeline" value={summary.total} />
        <KpiCard
          label="Score moyen"
          value={summary.avg_score}
          sub="/100"
          accent={summary.avg_score >= 70 ? "text-red-400" : summary.avg_score >= 50 ? "text-orange-400" : "text-amber-400"}
        />
        <KpiCard
          label="Valeur totale pipeline"
          value={`${summary.total_pipeline_value.toLocaleString("fr-FR")}€`}
          accent="text-emerald-400"
        />
        <KpiCard
          label="Leads à risque"
          value={summary.at_risk_count}
          accent={summary.at_risk_count > 0 ? "text-red-400" : "text-white"}
          sub="signaux de risque actifs"
        />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-4 gap-6">
        {/* Main lead list */}
        <div className="xl:col-span-3 space-y-4">
          {/* Tier filter tabs */}
          <div className="flex flex-wrap gap-2">
            {tierTabs.map((t) => (
              <button
                key={t.key}
                onClick={() => setTierFilter(t.key)}
                className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${
                  tierFilter === t.key ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-white"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>

          {/* Lead rows */}
          <div className="space-y-2">
            {filtered.map((lead, idx) => {
              const s = TIER_STYLES[lead.priority_tier];
              const hasRisk = lead.risk_flags.length > 0;
              return (
                <button
                  key={lead.signals.lead_id}
                  onClick={() => setSelected(lead)}
                  className={`w-full text-left bg-slate-900 border rounded-xl p-4 hover:border-slate-600 transition-colors ${
                    hasRisk && lead.priority_tier === "hot" ? "border-red-800/60" :
                    hasRisk ? "border-amber-800/40" : "border-slate-800"
                  }`}
                >
                  <div className="flex items-start gap-4">
                    {/* Rank */}
                    <div className="flex-shrink-0 w-7 h-7 rounded-full bg-slate-800 flex items-center justify-center text-xs font-bold text-slate-500">
                      {idx + 1}
                    </div>

                    {/* Lead info */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap mb-1">
                        <p className="text-sm font-semibold text-white">{lead.signals.name}</p>
                        <TierBadge tier={lead.priority_tier} />
                        {hasRisk && (
                          <span className="text-[10px] text-red-400 font-medium">
                            {lead.risk_flags.length} risque{lead.risk_flags.length > 1 ? "s" : ""}
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-slate-500 mb-2">
                        {lead.signals.company} · {lead.signals.sector} ·{" "}
                        <span className="font-medium text-slate-400">
                          {lead.signals.deal_value_eur.toLocaleString("fr-FR")}€
                        </span>
                      </p>

                      {/* Mini dimension bars */}
                      <div className="grid grid-cols-3 md:grid-cols-6 gap-x-4 gap-y-1.5">
                        {(Object.entries(lead.score_breakdown) as [keyof ScoreBreakdown, number][]).map(([k, v]) => (
                          <div key={k}>
                            <div className="text-[9px] text-slate-600 mb-0.5 truncate">{DIM_LABELS[k]}</div>
                            <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                              <div
                                className={`h-full rounded-full ${v >= 70 ? "bg-emerald-500" : v >= 50 ? "bg-amber-400" : v >= 30 ? "bg-orange-400" : "bg-red-500"}`}
                                style={{ width: `${v}%` }}
                              />
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Score */}
                    <div className="flex-shrink-0 text-right">
                      <p className={`text-2xl font-bold ${s.text}`}>{lead.priority_score}</p>
                      <p className="text-[10px] text-slate-600">/100</p>
                    </div>
                  </div>
                </button>
              );
            })}
            {filtered.length === 0 && (
              <div className="text-center py-12 text-slate-500">Aucun lead pour ce filtre</div>
            )}
          </div>
        </div>

        {/* Sector stats sidebar */}
        <div className="space-y-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-3">Stats par secteur</p>
            <div className="space-y-3">
              {sector_stats.map((s) => (
                <div key={s.sector}>
                  <div className="flex justify-between text-xs mb-0.5">
                    <span className="text-slate-300 font-medium truncate mr-2">{s.sector}</span>
                    <span className="text-slate-500 flex-shrink-0">{s.count}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full ${s.avg_score >= 70 ? "bg-red-400" : s.avg_score >= 50 ? "bg-orange-400" : s.avg_score >= 30 ? "bg-amber-400" : "bg-slate-500"}`}
                        style={{ width: `${s.avg_score}%` }}
                      />
                    </div>
                    <span className="text-[10px] font-mono text-slate-400 flex-shrink-0 w-8 text-right">{s.avg_score}</span>
                  </div>
                  <p className="text-[10px] text-slate-600 mt-0.5">
                    {s.total_value_eur.toLocaleString("fr-FR")}€
                    {s.hot_count > 0 && <span className="text-red-400 ml-1">· {s.hot_count} hot</span>}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Tier distribution */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-3">Distribution</p>
            <div className="space-y-2">
              {(["hot", "warm", "cold", "dormant"] as LeadPriority[]).map((tier) => {
                const count = summary.tier_counts[tier];
                const pct = summary.total > 0 ? (count / summary.total) * 100 : 0;
                const style = TIER_STYLES[tier];
                return (
                  <div key={tier}>
                    <div className="flex justify-between text-[10px] mb-0.5">
                      <span className={style.text}>{style.label}</span>
                      <span className="text-slate-500">{count}</span>
                    </div>
                    <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full ${
                          tier === "hot" ? "bg-red-400" : tier === "warm" ? "bg-orange-400" : tier === "cold" ? "bg-blue-400" : "bg-slate-500"
                        }`}
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
