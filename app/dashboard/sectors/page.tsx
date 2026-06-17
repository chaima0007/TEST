"use client";

import { useEffect, useState, useCallback } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface SectorProfile {
  name: string;
  market_size_fr: number;
  avg_pagespeed: number;
  competition_density: number;
  avg_revenue_impact_eur: number;
  outreach_roi_multiplier: number;
  icp_priority: "S" | "A" | "B" | "C";
  recommended_volume: number;
  tags: string[];
}

interface SectorsData {
  source: string;
  total_addressable_market: number;
  sectors: SectorProfile[];
  weekly_outreach_plan: Record<string, number>;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

const PRIORITY_STYLE: Record<string, string> = {
  S: "text-amber-300 bg-amber-400/10 border-amber-400/25",
  A: "text-emerald-300 bg-emerald-400/10 border-emerald-400/25",
  B: "text-indigo-300 bg-indigo-400/10 border-indigo-400/25",
  C: "text-gray-400 bg-gray-400/8 border-gray-400/15",
};

function PageSpeedColor(score: number): string {
  if (score < 30) return "text-red-400";
  if (score < 45) return "text-orange-400";
  if (score < 60) return "text-amber-400";
  return "text-emerald-400";
}

function CompetitionBar({ density }: { density: number }) {
  const color = density <= 0.20 ? "bg-emerald-500" : density <= 0.35 ? "bg-amber-500" : "bg-red-500";
  return (
    <div className="flex items-center gap-2">
      <div className="w-16 h-1.5 bg-white/8 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${density * 100}%` }} />
      </div>
      <span className="text-xs font-mono text-gray-400">{(density * 100).toFixed(0)}%</span>
    </div>
  );
}

function ROIBadge({ multiplier }: { multiplier: number }) {
  const color = multiplier >= 2.5 ? "text-emerald-300 bg-emerald-400/10 border-emerald-400/20"
    : multiplier >= 2.0 ? "text-indigo-300 bg-indigo-400/10 border-indigo-400/20"
    : "text-gray-400 bg-gray-400/8 border-gray-400/15";
  return (
    <span className={`text-xs font-mono px-2 py-0.5 rounded border ${color}`}>
      ×{multiplier.toFixed(1)}
    </span>
  );
}

// ── Components ────────────────────────────────────────────────────────────────

function SectorCard({ s }: { s: SectorProfile }) {
  const totalWeeklyEmails = s.recommended_volume;
  return (
    <div className="bg-white/3 border border-white/8 rounded-xl p-4 hover:bg-white/5 transition-colors">
      <div className="flex items-start justify-between gap-2 mb-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <span className={`text-xs font-bold px-2 py-0.5 rounded border ${PRIORITY_STYLE[s.icp_priority]}`}>
              {s.icp_priority}
            </span>
            <ROIBadge multiplier={s.outreach_roi_multiplier} />
          </div>
          <p className="text-sm font-semibold text-white">{s.name}</p>
        </div>
        <div className="text-right shrink-0">
          <p className={`text-lg font-bold font-mono ${PageSpeedColor(s.avg_pagespeed)}`}>{s.avg_pagespeed}</p>
          <p className="text-xs text-gray-500">PageSpeed</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 text-xs mb-3">
        <div>
          <p className="text-gray-500">Marché France</p>
          <p className="text-gray-200 font-semibold">{(s.market_size_fr / 1000).toFixed(0)}k entreprises</p>
        </div>
        <div>
          <p className="text-gray-500">Impact/an</p>
          <p className="text-amber-300 font-semibold">{(s.avg_revenue_impact_eur / 1000).toFixed(0)}k€</p>
        </div>
      </div>

      <div className="mb-3">
        <p className="text-xs text-gray-500 mb-1">Saturation concurrence</p>
        <CompetitionBar density={s.competition_density} />
      </div>

      <div className="flex items-center justify-between text-xs">
        <div className="flex flex-wrap gap-1">
          {s.tags.slice(0, 3).map((tag) => (
            <span key={tag} className="text-gray-500 bg-white/5 px-1.5 py-0.5 rounded text-[10px]">
              {tag}
            </span>
          ))}
        </div>
        <span className="text-indigo-300 font-mono shrink-0">{totalWeeklyEmails} /sem</span>
      </div>
    </div>
  );
}

// ── Page ─────────────────────────────────────────────────────────────────────

export default function SectorsPage() {
  const [data, setData] = useState<SectorsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState<"priority" | "market" | "roi" | "competition">("priority");

  const load = useCallback(() => {
    setLoading(true);
    fetch("/api/sectors")
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => { load(); }, [load]);

  const sorted = data
    ? [...data.sectors].sort((a, b) => {
        if (sortBy === "priority") {
          const order = { S: 0, A: 1, B: 2, C: 3 };
          return order[a.icp_priority] - order[b.icp_priority];
        }
        if (sortBy === "market") return b.market_size_fr - a.market_size_fr;
        if (sortBy === "roi") return b.outreach_roi_multiplier - a.outreach_roi_multiplier;
        if (sortBy === "competition") return a.competition_density - b.competition_density;
        return 0;
      })
    : [];

  const totalWeekly = data ? Object.values(data.weekly_outreach_plan).reduce((a, b) => a + b, 0) : 0;

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white p-6 space-y-5">

      {/* Header */}
      <div className="flex items-center justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-3 mb-1">
            <span className="text-2xl">🏢</span>
            <h1 className="text-2xl font-bold">Intelligence Sectorielle</h1>
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
            Marché adressable, densité concurrentielle et ROI outreach par secteur
          </p>
        </div>
      </div>

      {/* TAM + Weekly */}
      {data && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div className="bg-white/3 border border-white/8 rounded-xl p-4">
            <p className="text-xs text-gray-400 mb-1">Marché Total (TAM)</p>
            <p className="text-2xl font-bold text-white">{(data.total_addressable_market / 1000).toFixed(0)}k</p>
            <p className="text-xs text-gray-500 mt-0.5">entreprises en France</p>
          </div>
          <div className="bg-indigo-500/5 border border-indigo-500/15 rounded-xl p-4">
            <p className="text-xs text-indigo-400 mb-1">Emails / semaine</p>
            <p className="text-2xl font-bold text-indigo-300">{totalWeekly.toLocaleString("fr-FR")}</p>
            <p className="text-xs text-gray-500 mt-0.5">plan d&apos;outreach</p>
          </div>
          <div className="bg-amber-500/5 border border-amber-500/15 rounded-xl p-4">
            <p className="text-xs text-amber-400 mb-1">Secteurs Priorité S</p>
            <p className="text-2xl font-bold text-amber-300">
              {data.sectors.filter((s) => s.icp_priority === "S").length}
            </p>
            <p className="text-xs text-gray-500 mt-0.5">opportunité maximale</p>
          </div>
          <div className="bg-emerald-500/5 border border-emerald-500/15 rounded-xl p-4">
            <p className="text-xs text-emerald-400 mb-1">ROI Moyen</p>
            <p className="text-2xl font-bold text-emerald-300">
              ×{(data.sectors.reduce((a, s) => a + s.outreach_roi_multiplier, 0) / data.sectors.length).toFixed(1)}
            </p>
            <p className="text-xs text-gray-500 mt-0.5">multiplicateur outreach</p>
          </div>
        </div>
      )}

      {/* Sort controls */}
      <div className="flex items-center gap-2 flex-wrap">
        <span className="text-xs text-gray-500">Trier par :</span>
        {(["priority", "market", "roi", "competition"] as const).map((s) => (
          <button
            key={s}
            onClick={() => setSortBy(s)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
              sortBy === s
                ? "bg-indigo-600/30 border-indigo-500/40 text-indigo-200"
                : "bg-white/3 border-white/8 text-gray-400 hover:bg-white/5"
            }`}
          >
            {{
              priority: "Priorité ICP",
              market: "Taille marché",
              roi: "ROI outreach",
              competition: "Moins saturé",
            }[s]}
          </button>
        ))}
      </div>

      {/* Sector grid */}
      {loading ? (
        <div className="text-center py-16 text-gray-500 text-sm animate-pulse">Chargement de l&apos;intelligence sectorielle…</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
          {sorted.map((s) => (
            <SectorCard key={s.name} s={s} />
          ))}
        </div>
      )}

      {/* Legend */}
      <div className="bg-white/2 border border-white/6 rounded-xl p-4 text-xs text-gray-500 space-y-1">
        <p className="font-semibold text-gray-400">Légende</p>
        <p><span className="text-amber-300 font-mono">S</span> = Score ICP max — appel direct / <span className="text-emerald-300 font-mono">A</span> = Tier A email / <span className="text-indigo-300 font-mono">B</span> = Email masse / <span className="text-gray-300 font-mono">C</span> = Nurturing</p>
        <p>Concurrence : <span className="text-emerald-400">faible (≤20%)</span> / <span className="text-amber-400">moyenne (≤35%)</span> / <span className="text-red-400">saturée (&gt;35%)</span></p>
        <p>ROI × = multiplicateur du taux de réponse vs baseline secteur neutre</p>
      </div>

    </div>
  );
}
