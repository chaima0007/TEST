"use client";

import { useEffect, useState } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface Summary {
  campaigns: number;
  emails_sent: number;
  open_rate: number;
  reply_rate: number;
  total_opens: number;
  total_replies: number;
}

interface CampaignRow {
  campaign_id: string;
  agent_id: string;
  sector: string;
  sent: number;
  opens: number;
  clicks: number;
  replies: number;
  open_rate: number;
  click_rate: number;
  reply_rate: number;
  conversion_score: number;
}

interface AgentRow {
  agent_id: string;
  campaigns: number;
  total_sent: number;
  total_opens: number;
  total_replies: number;
  conversion_score: number;
}

interface TrackingData {
  source: string;
  summary: Summary;
  top_campaigns: CampaignRow[];
  agent_leaderboard: AgentRow[];
}

// ── Helpers ───────────────────────────────────────────────────────────────────

function pct(n: number) {
  return `${(n * 100).toFixed(1)}%`;
}

function convColor(score: number): string {
  if (score >= 0.15) return "text-emerald-400";
  if (score >= 0.10) return "text-indigo-400";
  if (score >= 0.06) return "text-amber-400";
  return "text-gray-500";
}

// ── Components ────────────────────────────────────────────────────────────────

function MetricBar({ value, max = 1, color = "bg-indigo-500" }: { value: number; max?: number; color?: string }) {
  const pct = Math.min((value / max) * 100, 100);
  return (
    <div className="w-full h-1.5 bg-white/8 rounded-full overflow-hidden">
      <div className={`h-full rounded-full transition-all ${color}`} style={{ width: `${pct}%` }} />
    </div>
  );
}

function StatCard({ label, value, sub, color = "text-white" }: { label: string; value: string | number; sub?: string; color?: string }) {
  return (
    <div className="bg-white/3 border border-white/8 rounded-xl p-4">
      <p className="text-xs text-gray-400 mb-1">{label}</p>
      <p className={`text-2xl font-bold ${color}`}>{value}</p>
      {sub && <p className="text-xs text-gray-500 mt-0.5">{sub}</p>}
    </div>
  );
}

function RankBadge({ rank }: { rank: number }) {
  const style =
    rank === 1 ? "text-amber-300 bg-amber-400/10 border-amber-400/20"
    : rank === 2 ? "text-gray-300 bg-gray-400/10 border-gray-400/20"
    : rank === 3 ? "text-orange-300 bg-orange-400/10 border-orange-400/20"
    : "text-gray-600 bg-white/3 border-white/5";
  return (
    <span className={`text-xs font-mono px-1.5 py-0.5 rounded border ${style}`}>
      #{rank}
    </span>
  );
}

// ── Page ─────────────────────────────────────────────────────────────────────

export default function TrackingPage() {
  const [data, setData] = useState<TrackingData | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"campaigns" | "agents">("campaigns");

  const load = () => {
    setLoading(true);
    fetch("/api/tracking")
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, [load]);

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white p-6 space-y-5">

      {/* Header */}
      <div className="flex items-center justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-3 mb-1">
            <span className="text-2xl">📧</span>
            <h1 className="text-2xl font-bold">Email Tracking</h1>
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
            Taux d&apos;ouverture, clics et réponses — Agent 2.x Division Rédaction
          </p>
        </div>
        <button
          onClick={load}
          className="px-4 py-2 rounded-lg bg-white/5 border border-white/10 text-sm text-gray-300 hover:bg-white/8 transition-all"
        >
          ↻ Actualiser
        </button>
      </div>

      {/* KPI Strip */}
      {data && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          <StatCard label="Campagnes" value={data.summary.campaigns} />
          <StatCard label="Emails envoyés" value={data.summary.emails_sent.toLocaleString("fr-FR")} />
          <StatCard
            label="Taux d'ouverture"
            value={pct(data.summary.open_rate)}
            color="text-indigo-300"
          />
          <StatCard
            label="Taux de réponse"
            value={pct(data.summary.reply_rate)}
            color="text-emerald-300"
          />
          <StatCard label="Ouvertures totales" value={data.summary.total_opens.toLocaleString("fr-FR")} color="text-indigo-400" />
          <StatCard label="Réponses totales" value={data.summary.total_replies.toLocaleString("fr-FR")} color="text-emerald-400" />
        </div>
      )}

      {/* Tab switcher */}
      <div className="flex gap-2">
        {(["campaigns", "agents"] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-1.5 rounded-lg text-sm font-medium border transition-all ${
              activeTab === tab
                ? "bg-indigo-600/30 border-indigo-500/40 text-indigo-200"
                : "bg-white/3 border-white/8 text-gray-400 hover:bg-white/5"
            }`}
          >
            {tab === "campaigns" ? "Top Campagnes" : "Classement Agents"}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="text-center py-16 text-gray-500 text-sm animate-pulse">Chargement des métriques…</div>
      ) : !data ? null : activeTab === "campaigns" ? (
        /* ── Campaign table ── */
        <div className="bg-white/3 border border-white/8 rounded-2xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-white/8 text-xs text-gray-500 uppercase tracking-wide">
                  <th className="text-left px-4 py-3">Campagne</th>
                  <th className="text-left px-4 py-3">Agent</th>
                  <th className="text-left px-4 py-3">Secteur</th>
                  <th className="text-right px-4 py-3">Envoyés</th>
                  <th className="px-4 py-3">Ouverture</th>
                  <th className="px-4 py-3">Clic</th>
                  <th className="px-4 py-3">Réponse</th>
                  <th className="text-right px-4 py-3">Score</th>
                </tr>
              </thead>
              <tbody>
                {data.top_campaigns.map((row, i) => (
                  <tr key={row.campaign_id} className="border-b border-white/5 hover:bg-white/3 transition-colors">
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <RankBadge rank={i + 1} />
                        <span className="text-xs font-mono text-gray-400">{row.campaign_id}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <span className="text-xs font-mono bg-indigo-500/15 text-indigo-300 border border-indigo-500/25 px-2 py-0.5 rounded">
                        {row.agent_id}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-gray-300 text-xs">{row.sector}</td>
                    <td className="px-4 py-3 text-right font-mono text-gray-300">{row.sent}</td>
                    <td className="px-4 py-3 min-w-[90px]">
                      <div className="space-y-0.5">
                        <p className="text-xs text-indigo-300 font-mono">{pct(row.open_rate)}</p>
                        <MetricBar value={row.open_rate} color="bg-indigo-500" />
                      </div>
                    </td>
                    <td className="px-4 py-3 min-w-[90px]">
                      <div className="space-y-0.5">
                        <p className="text-xs text-amber-300 font-mono">{pct(row.click_rate)}</p>
                        <MetricBar value={row.click_rate} color="bg-amber-500" />
                      </div>
                    </td>
                    <td className="px-4 py-3 min-w-[90px]">
                      <div className="space-y-0.5">
                        <p className="text-xs text-emerald-300 font-mono">{pct(row.reply_rate)}</p>
                        <MetricBar value={row.reply_rate} max={0.2} color="bg-emerald-500" />
                      </div>
                    </td>
                    <td className="px-4 py-3 text-right">
                      <span className={`text-sm font-bold font-mono ${convColor(row.conversion_score)}`}>
                        {(row.conversion_score * 100).toFixed(1)}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        /* ── Agent leaderboard ── */
        <div className="space-y-2">
          {data.agent_leaderboard.map((row, i) => (
            <div key={row.agent_id} className="bg-white/3 border border-white/8 rounded-xl p-4 flex items-center gap-4 hover:bg-white/5 transition-colors">
              <RankBadge rank={i + 1} />
              <span className="text-sm font-mono bg-indigo-500/15 text-indigo-300 border border-indigo-500/25 px-2.5 py-1 rounded shrink-0">
                Agent {row.agent_id}
              </span>
              <div className="flex-1 min-w-0 grid grid-cols-2 md:grid-cols-4 gap-3">
                <div>
                  <p className="text-xs text-gray-500">Campagnes</p>
                  <p className="text-sm font-semibold text-gray-200">{row.campaigns}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Envoyés</p>
                  <p className="text-sm font-semibold text-gray-200">{row.total_sent.toLocaleString("fr-FR")}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Ouvertures</p>
                  <p className="text-sm font-semibold text-indigo-300">{row.total_opens}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Réponses</p>
                  <p className="text-sm font-semibold text-emerald-300">{row.total_replies}</p>
                </div>
              </div>
              <div className="shrink-0 text-right">
                <p className="text-xs text-gray-500 mb-0.5">Conv. Score</p>
                <p className={`text-lg font-bold font-mono ${convColor(row.conversion_score)}`}>
                  {(row.conversion_score * 100).toFixed(1)}
                </p>
              </div>
              <div className="w-24 shrink-0">
                <MetricBar
                  value={row.conversion_score}
                  max={0.20}
                  color={
                    row.conversion_score >= 0.15 ? "bg-emerald-500"
                    : row.conversion_score >= 0.10 ? "bg-indigo-500"
                    : row.conversion_score >= 0.06 ? "bg-amber-500"
                    : "bg-gray-600"
                  }
                />
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Formula legend */}
      <div className="bg-white/2 border border-white/6 rounded-xl p-4 text-xs text-gray-500">
        <p className="font-semibold text-gray-400 mb-1">Formule Conversion Score</p>
        <p>Score = (reply_rate × 0.60) + (click_rate × 0.25) + (open_rate × 0.15)</p>
        <p className="mt-1">Priorité aux réponses (intention achat confirmée) &gt; clics &gt; ouvertures.</p>
      </div>

    </div>
  );
}
