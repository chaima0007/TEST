"use client";

import { useEffect, useState } from "react";

// ── Types ──────────────────────────────────────────────────────────────────────

interface CampaignWave {
  wave_id: string;
  sector: string;
  agent_id: string;
  email_count: number;
  scheduled_at: string;
  priority: "urgent" | "high" | "normal" | "low";
  tier_filter: string;
  status: "pending" | "running" | "done" | "cancelled";
}

interface CampaignPlan {
  plan_id: string;
  created_at: string;
  total_emails: number;
  total_waves: number;
  sector: string;
  agent_id: string;
  waves: CampaignWave[];
}

interface Summary {
  total_plans: number;
  total_waves: number;
  total_emails_planned: number;
  pending: number;
  done: number;
  cancelled: number;
}

interface CampaignsData {
  source: string;
  summary: Summary;
  plans: CampaignPlan[];
}

// ── Colour maps ────────────────────────────────────────────────────────────────

const PRIORITY_COLORS: Record<string, string> = {
  urgent: "bg-red-500/20 text-red-400 border-red-500/30",
  high:   "bg-amber-500/20 text-amber-400 border-amber-500/30",
  normal: "bg-indigo-500/20 text-indigo-400 border-indigo-500/30",
  low:    "bg-gray-500/20 text-gray-400 border-gray-500/30",
};

const STATUS_COLORS: Record<string, string> = {
  pending:   "bg-blue-500/20 text-blue-400",
  running:   "bg-emerald-500/20 text-emerald-400",
  done:      "bg-gray-500/20 text-gray-400",
  cancelled: "bg-red-500/20 text-red-400",
};

const TIER_COLORS: Record<string, string> = {
  A: "text-emerald-400",
  B: "text-indigo-400",
  C: "text-gray-400",
};

// ── Helpers ────────────────────────────────────────────────────────────────────

function formatDate(iso: string) {
  const d = new Date(iso);
  return d.toLocaleString("fr-FR", { weekday: "short", day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit" });
}

function capitalise(s: string) { return s.charAt(0).toUpperCase() + s.slice(1); }

// ── Sub-components ─────────────────────────────────────────────────────────────

function KpiCard({ label, value, color }: { label: string; value: string | number; color?: string }) {
  return (
    <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
      <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">{label}</p>
      <p className={`text-2xl font-bold ${color ?? "text-white"}`}>{value}</p>
    </div>
  );
}

function StatusBar({ summary }: { summary: Summary }) {
  const total = summary.total_waves || 1;
  const pendPct    = (summary.pending   / total) * 100;
  const donePct    = (summary.done      / total) * 100;
  const cancelPct  = (summary.cancelled / total) * 100;
  const runPct     = 100 - pendPct - donePct - cancelPct;
  return (
    <div className="rounded-xl overflow-hidden flex h-3 w-full mt-4">
      <div className="bg-blue-500"   style={{ width: `${pendPct}%` }} title="Pending" />
      <div className="bg-emerald-500" style={{ width: `${runPct > 0 ? runPct : 0}%` }} title="Running" />
      <div className="bg-gray-600"   style={{ width: `${donePct}%` }} title="Done" />
      <div className="bg-red-500"    style={{ width: `${cancelPct}%` }} title="Cancelled" />
    </div>
  );
}

function WaveRow({ wave }: { wave: CampaignWave }) {
  return (
    <tr className="border-b border-white/[0.04] hover:bg-white/[0.02] transition-colors">
      <td className="py-2 px-3 text-xs font-mono text-gray-500">{wave.wave_id.split("_").slice(-1)[0]}</td>
      <td className="py-2 px-3 text-sm">{capitalise(wave.sector)}</td>
      <td className="py-2 px-3 text-sm font-mono text-indigo-400">{wave.agent_id}</td>
      <td className="py-2 px-3 text-sm text-right font-semibold">{wave.email_count}</td>
      <td className={`py-2 px-3 text-sm font-bold ${TIER_COLORS[wave.tier_filter] ?? "text-gray-400"}`}>
        Tier {wave.tier_filter}
      </td>
      <td className="py-2 px-3">
        <span className={`text-xs px-2 py-0.5 rounded-full border ${PRIORITY_COLORS[wave.priority]}`}>
          {wave.priority}
        </span>
      </td>
      <td className="py-2 px-3 text-xs text-gray-400">{formatDate(wave.scheduled_at)}</td>
      <td className="py-2 px-3">
        <span className={`text-xs px-2 py-0.5 rounded-full ${STATUS_COLORS[wave.status]}`}>
          {wave.status}
        </span>
      </td>
    </tr>
  );
}

function PlanCard({ plan, expanded, onToggle }: { plan: CampaignPlan; expanded: boolean; onToggle: () => void }) {
  const doneWaves = plan.waves.filter(w => w.status === "done").length;
  const progress  = plan.total_waves > 0 ? (doneWaves / plan.total_waves) * 100 : 0;

  return (
    <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl overflow-hidden">
      <button
        className="w-full flex items-center justify-between px-5 py-4 hover:bg-white/[0.02] transition-colors"
        onClick={onToggle}
      >
        <div className="flex items-center gap-4 text-left">
          <div>
            <p className="font-semibold text-sm">{capitalise(plan.sector)}</p>
            <p className="text-xs text-gray-500 font-mono">{plan.plan_id}</p>
          </div>
          <div className="hidden sm:flex gap-3 text-xs text-gray-400">
            <span>{plan.total_emails.toLocaleString()} emails</span>
            <span>·</span>
            <span>{plan.total_waves} vague{plan.total_waves > 1 ? "s" : ""}</span>
            <span>·</span>
            <span className="font-mono text-indigo-400">Agent {plan.agent_id}</span>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className="w-24 hidden md:block">
            <div className="h-1.5 bg-white/[0.05] rounded-full overflow-hidden">
              <div className="h-full bg-emerald-500 rounded-full transition-all" style={{ width: `${progress}%` }} />
            </div>
            <p className="text-xs text-gray-500 mt-1 text-right">{doneWaves}/{plan.total_waves}</p>
          </div>
          <svg
            className={`w-4 h-4 text-gray-500 transition-transform ${expanded ? "rotate-180" : ""}`}
            fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </button>

      {expanded && (
        <div className="px-5 pb-5 overflow-x-auto">
          <table className="w-full min-w-[640px]">
            <thead>
              <tr className="border-b border-white/[0.06]">
                {["Vague", "Secteur", "Agent", "Emails", "Tier", "Priorité", "Planifié", "Statut"].map(h => (
                  <th key={h} className="text-left py-2 px-3 text-xs text-gray-500 uppercase tracking-wider font-medium">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {plan.waves.map(w => <WaveRow key={w.wave_id} wave={w} />)}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

// ── Page ───────────────────────────────────────────────────────────────────────

export default function CampaignsPage() {
  const [data, setData]       = useState<CampaignsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState<Set<string>>(new Set());
  const [filter, setFilter]   = useState<"all" | "pending" | "running" | "done" | "cancelled">("all");

  useEffect(() => {
    fetch("/api/campaigns")
      .then(r => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  const toggle = (id: string) =>
    setExpanded(prev => { const s = new Set(prev); s.has(id) ? s.delete(id) : s.add(id); return s; });

  const filteredPlans = data?.plans.filter(plan => {
    if (filter === "all") return true;
    return plan.waves.some(w => w.status === filter);
  }) ?? [];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!data) return <p className="text-gray-500 p-8">Erreur de chargement.</p>;

  const { summary } = data;

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Campagnes</h1>
          <p className="text-sm text-gray-500 mt-0.5">Planification des vagues d'outreach par secteur</p>
        </div>
        {data.source === "mock" && (
          <span className="text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2 py-1 rounded-full">
            Données démo
          </span>
        )}
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        <KpiCard label="Plans" value={summary.total_plans} />
        <KpiCard label="Vagues" value={summary.total_waves} />
        <KpiCard label="Emails planifiés" value={summary.total_emails_planned.toLocaleString()} color="text-indigo-400" />
        <KpiCard label="En attente" value={summary.pending} color="text-blue-400" />
        <KpiCard label="Terminées" value={summary.done} color="text-emerald-400" />
        <KpiCard label="Annulées" value={summary.cancelled} color="text-red-400" />
      </div>

      {/* Global progress bar */}
      <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
        <div className="flex justify-between text-xs text-gray-500 mb-2">
          <span>Progression globale</span>
          <span>{summary.done} / {summary.total_waves} vagues terminées</span>
        </div>
        <StatusBar summary={summary} />
        <div className="flex gap-4 mt-2 text-xs text-gray-500">
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-blue-500 inline-block"/>En attente</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-emerald-500 inline-block"/>Terminée</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-gray-600 inline-block"/>En cours</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-red-500 inline-block"/>Annulée</span>
        </div>
      </div>

      {/* Filter tabs */}
      <div className="flex gap-2 flex-wrap">
        {(["all", "pending", "running", "done", "cancelled"] as const).map(f => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors border ${
              filter === f
                ? "bg-indigo-600 border-indigo-500 text-white"
                : "bg-white/[0.03] border-white/[0.07] text-gray-400 hover:text-white"
            }`}
          >
            {f === "all" ? "Tous" : capitalise(f)}
          </button>
        ))}
      </div>

      {/* Plan cards */}
      <div className="space-y-3">
        {filteredPlans.length === 0 ? (
          <p className="text-gray-500 text-sm py-8 text-center">Aucun plan pour ce filtre.</p>
        ) : (
          filteredPlans.map(plan => (
            <PlanCard
              key={plan.plan_id}
              plan={plan}
              expanded={expanded.has(plan.plan_id)}
              onToggle={() => toggle(plan.plan_id)}
            />
          ))
        )}
      </div>
    </div>
  );
}
