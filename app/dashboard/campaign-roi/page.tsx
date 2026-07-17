"use client";

import { useEffect, useState, useRef } from "react";

type CampaignStatus = "excellent" | "good" | "average" | "poor" | "failing";
type ChannelType = "email" | "linkedin" | "webinar" | "content" | "paid" | "outbound" | "event";

interface CampaignMetrics {
  campaign_id: string;
  campaign_name: string;
  channel: ChannelType;
  start_date: string;
  duration_days: number;
  budget_eur: number;
  total_spent_eur: number;
  total_contacts: number;
  emails_sent: number;
  opens: number;
  clicks: number;
  unsubscribes: number;
  leads_generated: number;
  mqls: number;
  sqls: number;
  opportunities_created: number;
  deals_won: number;
  pipeline_value_eur: number;
  closed_revenue_eur: number;
  avg_deal_size_eur: number;
}

interface CampaignResult {
  campaign: CampaignMetrics;
  roi_pct: number;
  roi_score: number;
  reach_efficiency: number;
  conversion_quality: number;
  cost_efficiency: number;
  overall_score: number;
  status: CampaignStatus;
  cost_per_lead_eur: number;
  cost_per_sql_eur: number;
  cost_per_deal_eur: number;
  open_rate_pct: number;
  click_rate_pct: number;
  lead_to_opp_rate_pct: number;
  opp_to_won_rate_pct: number;
  key_insights: string[];
  recommendations: string[];
  benchmark_vs_channel: number;
}

interface Summary {
  total: number;
  status_counts: Record<string, number>;
  channel_counts: Record<string, number>;
  avg_overall_score: number;
  avg_roi_pct: number;
  total_pipeline_eur: number;
  total_closed_revenue_eur: number;
  total_spent_eur: number;
}

const STATUS_META: Record<CampaignStatus, { label: string; color: string; bg: string; dot: string }> = {
  excellent: { label: "EXCELLENT", color: "text-emerald-400", bg: "bg-emerald-500/10 border-emerald-500/30", dot: "bg-emerald-400" },
  good: { label: "BON", color: "text-blue-400", bg: "bg-blue-500/10 border-blue-500/30", dot: "bg-blue-400" },
  average: { label: "MOYEN", color: "text-yellow-400", bg: "bg-yellow-500/10 border-yellow-500/30", dot: "bg-yellow-400" },
  poor: { label: "FAIBLE", color: "text-orange-400", bg: "bg-orange-500/10 border-orange-500/30", dot: "bg-orange-400" },
  failing: { label: "ÉCHEC", color: "text-red-400", bg: "bg-red-500/10 border-red-500/30", dot: "bg-red-400" },
};

const CHANNEL_META: Record<ChannelType, { label: string; icon: string }> = {
  email: { label: "Email", icon: "✉️" },
  linkedin: { label: "LinkedIn", icon: "💼" },
  webinar: { label: "Webinaire", icon: "🎥" },
  content: { label: "Contenu", icon: "📝" },
  paid: { label: "Paid Ads", icon: "📢" },
  outbound: { label: "Outbound", icon: "📞" },
  event: { label: "Événement", icon: "🎪" },
};

const STATUS_TABS: { id: CampaignStatus | "all"; label: string }[] = [
  { id: "all", label: "Toutes" },
  { id: "excellent", label: "Excellent" },
  { id: "good", label: "Bon" },
  { id: "average", label: "Moyen" },
  { id: "poor", label: "Faible" },
  { id: "failing", label: "Échec" },
];

function fmtEur(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}k€`;
  return `${n}€`;
}

function ScoreBar({ value, color = "bg-indigo-500" }: { value: number; color?: string }) {
  return (
    <div className="h-1.5 w-full rounded-full bg-slate-700">
      <div className={`h-1.5 rounded-full transition-all ${color}`} style={{ width: `${Math.min(100, value)}%` }} />
    </div>
  );
}

function ROIRing({ score }: { score: number }) {
  const r = 28;
  const circ = 2 * Math.PI * r;
  const offset = circ - (Math.min(100, score) / 100) * circ;
  const color = score >= 80 ? "#10b981" : score >= 60 ? "#3b82f6" : score >= 40 ? "#f59e0b" : "#ef4444";
  return (
    <div className="relative flex items-center justify-center w-16 h-16">
      <svg viewBox="0 0 72 72" className="w-16 h-16 -rotate-90">
        <circle cx="36" cy="36" r={r} fill="none" stroke="#334155" strokeWidth="6" />
        <circle cx="36" cy="36" r={r} fill="none" stroke={color} strokeWidth="6"
          strokeDasharray={circ} strokeDashoffset={offset} strokeLinecap="round"
          className="transition-all duration-700" />
      </svg>
      <span className="absolute text-xs font-bold" style={{ color }}>{Math.round(score)}</span>
    </div>
  );
}

function CampaignModal({ result, onClose }: { result: CampaignResult; onClose: () => void }) {
  const modalRef = useRef<HTMLDivElement>(null);
  const meta = STATUS_META[result.status];
  const channel = CHANNEL_META[result.campaign.channel];

  useEffect(() => {
    const handler = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    const click = (e: MouseEvent) => {
      if (modalRef.current && !modalRef.current.contains(e.target as Node)) onClose();
    };
    window.addEventListener("keydown", handler);
    document.addEventListener("mousedown", click);
    return () => { window.removeEventListener("keydown", handler); document.removeEventListener("mousedown", click); };
  }, [onClose]);

  const roiPositive = result.roi_pct >= 0;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div ref={modalRef} className="relative w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-2xl bg-slate-900 border border-slate-700 shadow-2xl">
        <div className="sticky top-0 z-10 flex items-start justify-between gap-4 p-6 bg-slate-900 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${meta.bg} ${meta.color}`}>{meta.label}</span>
              <span className="text-xs text-slate-400">{channel.icon} {channel.label}</span>
              <span className="text-xs text-slate-500">{result.campaign.duration_days}j</span>
            </div>
            <h2 className="text-lg font-bold text-slate-100 leading-tight">{result.campaign.campaign_name}</h2>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200 text-xl leading-none mt-1">✕</button>
        </div>

        <div className="p-6 space-y-6">
          {/* Top KPIs */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { label: "ROI", value: `${roiPositive ? "+" : ""}${Math.round(result.roi_pct)}%`, color: roiPositive ? "text-emerald-400" : "text-red-400" },
              { label: "Pipeline généré", value: fmtEur(result.campaign.pipeline_value_eur), color: "text-slate-100" },
              { label: "Revenus closés", value: fmtEur(result.campaign.closed_revenue_eur), color: "text-emerald-400" },
              { label: "vs Benchmark", value: `×${result.benchmark_vs_channel.toFixed(1)}`, color: result.benchmark_vs_channel >= 1 ? "text-emerald-400" : "text-red-400" },
            ].map((kpi) => (
              <div key={kpi.label} className="rounded-lg bg-slate-800 border border-slate-700 p-3 text-center">
                <div className={`text-lg font-bold ${kpi.color}`}>{kpi.value}</div>
                <div className="text-xs text-slate-400">{kpi.label}</div>
              </div>
            ))}
          </div>

          {/* Dimension bars */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-3">Dimensions performance</h3>
            <div className="space-y-2">
              {[
                { label: "Score ROI", val: result.roi_score, color: "bg-emerald-500" },
                { label: "Portée & Engagement", val: result.reach_efficiency, color: "bg-blue-500" },
                { label: "Qualité conversion", val: result.conversion_quality, color: "bg-purple-500" },
                { label: "Efficacité budget", val: result.cost_efficiency, color: "bg-indigo-500" },
              ].map((d) => (
                <div key={d.label} className="flex items-center gap-3">
                  <span className="text-xs text-slate-400 w-36 shrink-0">{d.label}</span>
                  <div className="flex-1"><ScoreBar value={d.val} color={d.color} /></div>
                  <span className="text-xs text-slate-300 w-8 text-right">{Math.round(d.val)}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Funnel metrics */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-3">Entonnoir de conversion</h3>
            <div className="grid grid-cols-3 sm:grid-cols-6 gap-2 text-center">
              {[
                { label: "Contacts", val: result.campaign.total_contacts },
                { label: "Leads", val: result.campaign.leads_generated },
                { label: "MQLs", val: result.campaign.mqls },
                { label: "SQLs", val: result.campaign.sqls },
                { label: "Opps", val: result.campaign.opportunities_created },
                { label: "Deals", val: result.campaign.deals_won },
              ].map((f) => (
                <div key={f.label} className="rounded-lg bg-slate-800 border border-slate-700 p-2">
                  <div className="text-sm font-bold text-slate-100">{f.val.toLocaleString("fr-FR")}</div>
                  <div className="text-xs text-slate-400">{f.label}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Email metrics */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-3">Métriques d'envoi</h3>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {[
                { label: "Taux d'ouverture", val: `${result.open_rate_pct.toFixed(1)}%`, bench: "25%", ok: result.open_rate_pct >= 25 },
                { label: "Taux de clic", val: `${result.click_rate_pct.toFixed(1)}%`, bench: "3%", ok: result.click_rate_pct >= 3 },
                { label: "Lead → Opp", val: `${result.lead_to_opp_rate_pct.toFixed(1)}%`, bench: "15%", ok: result.lead_to_opp_rate_pct >= 15 },
                { label: "Opp → Won", val: `${result.opp_to_won_rate_pct.toFixed(1)}%`, bench: "25%", ok: result.opp_to_won_rate_pct >= 25 },
              ].map((m) => (
                <div key={m.label} className="rounded-lg bg-slate-800 border border-slate-700 p-3 text-center">
                  <div className={`text-lg font-bold ${m.ok ? "text-emerald-400" : "text-orange-400"}`}>{m.val}</div>
                  <div className="text-xs text-slate-400">{m.label}</div>
                  <div className="text-xs text-slate-500">cible: {m.bench}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Cost metrics */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-3">Coûts d'acquisition</h3>
            <div className="grid grid-cols-3 gap-3">
              {[
                { label: "Coût / Lead", val: result.cost_per_lead_eur > 0 ? `${result.cost_per_lead_eur.toFixed(0)}€` : "—", bench: 150 },
                { label: "Coût / SQL", val: result.cost_per_sql_eur > 0 ? `${result.cost_per_sql_eur.toFixed(0)}€` : "—", bench: 500 },
                { label: "Coût / Deal", val: result.cost_per_deal_eur > 0 ? `${result.cost_per_deal_eur.toFixed(0)}€` : "—", bench: 5000 },
              ].map((c) => (
                <div key={c.label} className="rounded-lg bg-slate-800 border border-slate-700 p-3 text-center">
                  <div className="text-lg font-bold text-slate-100">{c.val}</div>
                  <div className="text-xs text-slate-400">{c.label}</div>
                  <div className="text-xs text-slate-500">bench: {c.bench}€</div>
                </div>
              ))}
            </div>
          </div>

          {/* Insights */}
          {result.key_insights.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-slate-300 mb-3">Insights clés</h3>
              <ul className="space-y-2">
                {result.key_insights.map((ins, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                    <span className="text-indigo-400 mt-0.5 shrink-0">•</span>{ins}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Recommendations */}
          {result.recommendations.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-slate-300 mb-3">Recommandations</h3>
              <ul className="space-y-2">
                {result.recommendations.map((r, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                    <span className="text-emerald-400 mt-0.5 shrink-0">→</span>{r}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function CampaignCard({ result, onClick }: { result: CampaignResult; onClick: () => void }) {
  const meta = STATUS_META[result.status];
  const channel = CHANNEL_META[result.campaign.channel];
  const roiPositive = result.roi_pct >= 0;

  return (
    <div
      onClick={onClick}
      className={`cursor-pointer rounded-xl border p-5 transition-all hover:border-slate-600 hover:bg-slate-800/80 ${meta.bg}`}
    >
      <div className="flex items-start justify-between gap-3 mb-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${meta.bg} ${meta.color} flex items-center gap-1`}>
              <span className={`w-1.5 h-1.5 rounded-full ${meta.dot}`} />
              {meta.label}
            </span>
            <span className="text-xs text-slate-400">{channel.icon} {channel.label}</span>
          </div>
          <h3 className="font-semibold text-slate-100 text-sm leading-tight line-clamp-2">{result.campaign.campaign_name}</h3>
        </div>
        <ROIRing score={result.overall_score} />
      </div>

      {/* ROI + benchmark */}
      <div className="flex items-center gap-3 mb-4">
        <span className={`text-lg font-bold ${roiPositive ? "text-emerald-400" : "text-red-400"}`}>
          {roiPositive ? "+" : ""}{Math.round(result.roi_pct)}% ROI
        </span>
        <span className={`text-xs px-2 py-0.5 rounded-full border ${result.benchmark_vs_channel >= 1 ? "text-emerald-400 bg-emerald-500/10 border-emerald-500/30" : "text-red-400 bg-red-500/10 border-red-500/30"}`}>
          ×{result.benchmark_vs_channel.toFixed(1)} benchmark
        </span>
      </div>

      {/* Score bars */}
      <div className="space-y-1.5 mb-4">
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-500 w-16 shrink-0">Reach</span>
          <div className="flex-1"><ScoreBar value={result.reach_efficiency} color="bg-blue-500" /></div>
          <span className="text-xs text-slate-400 w-6 text-right">{Math.round(result.reach_efficiency)}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-500 w-16 shrink-0">Convert.</span>
          <div className="flex-1"><ScoreBar value={result.conversion_quality} color="bg-purple-500" /></div>
          <span className="text-xs text-slate-400 w-6 text-right">{Math.round(result.conversion_quality)}</span>
        </div>
      </div>

      {/* Bottom stats */}
      <div className="grid grid-cols-3 gap-2 text-center border-t border-slate-700 pt-3">
        <div>
          <div className="text-sm font-bold text-slate-200">{result.campaign.leads_generated}</div>
          <div className="text-xs text-slate-500">Leads</div>
        </div>
        <div>
          <div className="text-sm font-bold text-slate-200">{fmtEur(result.campaign.pipeline_value_eur)}</div>
          <div className="text-xs text-slate-500">Pipeline</div>
        </div>
        <div>
          <div className="text-sm font-bold text-slate-200">{fmtEur(result.campaign.total_spent_eur)}</div>
          <div className="text-xs text-slate-500">Budget</div>
        </div>
      </div>
    </div>
  );
}

export default function CampaignROIPage() {
  const [campaigns, setCampaigns] = useState<CampaignResult[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<CampaignStatus | "all">("all");
  const [selected, setSelected] = useState<CampaignResult | null>(null);

  useEffect(() => {
    fetch("/api/campaign-roi")
      .then((r) => r.json())
      .then((data) => {
        setCampaigns(data.campaigns ?? []);
        setSummary(data.summary ?? null);
      })
      .finally(() => setLoading(false));
  }, []);

  const filtered = activeTab === "all" ? campaigns : campaigns.filter((c) => c.status === activeTab);

  const failingCount = (summary?.status_counts.failing ?? 0) + (summary?.status_counts.poor ?? 0);

  return (
    <div className="min-h-screen bg-slate-950 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-100">ROI Campagnes Marketing</h1>
            <p className="text-sm text-slate-400 mt-1">
              Performance et ROI par campagne — reach, conversion, efficacité budget vs benchmark canal
            </p>
          </div>
          {failingCount > 0 && (
            <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/30 rounded-xl px-4 py-2">
              <span className="w-2 h-2 bg-red-400 rounded-full animate-pulse" />
              <span className="text-sm font-semibold text-red-400">
                {failingCount} campagne{failingCount > 1 ? "s" : ""} sous-performante{failingCount > 1 ? "s" : ""}
              </span>
            </div>
          )}
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {[
              { label: "Campagnes analysées", value: summary.total, color: "text-slate-100" },
              { label: "ROI moyen", value: `${Math.round(summary.avg_roi_pct)}%`, color: summary.avg_roi_pct > 0 ? "text-emerald-400" : "text-red-400" },
              { label: "Pipeline total", value: fmtEur(summary.total_pipeline_eur), color: "text-indigo-400" },
              { label: "Revenus closés", value: fmtEur(summary.total_closed_revenue_eur), color: "text-emerald-400" },
            ].map((kpi) => (
              <div key={kpi.label} className="rounded-xl bg-slate-900 border border-slate-800 p-4">
                <div className={`text-2xl font-bold ${kpi.color}`}>{kpi.value}</div>
                <div className="text-xs text-slate-400 mt-1">{kpi.label}</div>
              </div>
            ))}
          </div>
        )}

        {/* Channel breakdown */}
        {summary && (
          <div className="rounded-xl bg-slate-900 border border-slate-800 p-4">
            <h2 className="text-sm font-semibold text-slate-400 mb-3">Campagnes par canal</h2>
            <div className="flex flex-wrap gap-2">
              {Object.entries(summary.channel_counts).map(([ch, count]) => {
                const c = CHANNEL_META[ch as ChannelType];
                if (!c || count === 0) return null;
                return (
                  <span key={ch} className="text-xs bg-slate-800 border border-slate-700 text-slate-300 px-3 py-1.5 rounded-full">
                    {c.icon} {c.label}: <span className="font-bold text-slate-100">{count}</span>
                  </span>
                );
              })}
            </div>
          </div>
        )}

        {/* Status tabs */}
        <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-xl p-1 w-fit flex-wrap">
          {STATUS_TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === tab.id ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {tab.label}
              {summary && tab.id !== "all" && (
                <span className="ml-1.5 text-xs opacity-70">({summary.status_counts[tab.id] ?? 0})</span>
              )}
            </button>
          ))}
        </div>

        {/* Campaign grid */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="rounded-xl bg-slate-900 border border-slate-800 p-5 animate-pulse h-56" />
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center text-slate-500 py-16">Aucune campagne dans cette catégorie</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {filtered.map((r) => (
              <CampaignCard key={r.campaign.campaign_id} result={r} onClick={() => setSelected(r)} />
            ))}
          </div>
        )}
      </div>

      {selected && <CampaignModal result={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
