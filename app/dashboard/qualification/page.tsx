"use client";

import { useEffect, useState } from "react";

// ── Types ──────────────────────────────────────────────────────────────────────

type AuthorityLevel = "unknown" | "influencer" | "manager" | "director" | "owner";
type Timeline = "unknown" | "no_timeline" | "next_year" | "next_quarter" | "this_quarter" | "immediate";
type QTier = "hot" | "warm" | "cool" | "cold";

interface BANT {
  budget_eur: number;
  budget_confirmed: boolean;
  authority_level: AuthorityLevel;
  need_severity: number;
  need_articulated: boolean;
  timeline: Timeline;
  budget_pts: number;
  authority_pts: number;
  need_pts: number;
  timeline_pts: number;
  total: number;
  tier: QTier;
}

interface QualRecord {
  record_id: string;
  prospect_id: string;
  company_name: string;
  sector: string;
  contact_name: string;
  contact_role: string;
  notes: string;
  qualified_at: string;
  last_updated: string;
  bant: BANT;
}

interface DimAvgs { budget: number; authority: number; need: number; timeline: number; }

interface Summary {
  total: number;
  tier_hot: number;
  tier_warm: number;
  tier_cool: number;
  tier_cold: number;
  avg_score: number;
  weakest_bant: string;
  dimension_avgs: DimAvgs;
}

interface Data {
  source: string;
  records: QualRecord[];
  summary: Summary;
}

// ── Constants ──────────────────────────────────────────────────────────────────

const TIER_META: Record<QTier, { label: string; color: string; dot: string }> = {
  hot:  { label: "HOT",  color: "bg-red-500/20 text-red-300 border-red-500/30",           dot: "bg-red-500"     },
  warm: { label: "WARM", color: "bg-amber-500/20 text-amber-300 border-amber-500/30",     dot: "bg-amber-500"   },
  cool: { label: "COOL", color: "bg-blue-500/20 text-blue-300 border-blue-500/30",        dot: "bg-blue-500"    },
  cold: { label: "COLD", color: "bg-gray-500/20 text-gray-400 border-gray-500/30",        dot: "bg-gray-500"    },
};

const AUTH_LABELS: Record<AuthorityLevel, string> = {
  unknown:    "Inconnu", influencer: "Influenceur", manager: "Manager",
  director: "Directeur", owner: "Propriétaire",
};

const TL_LABELS: Record<Timeline, string> = {
  unknown:      "Inconnu",    no_timeline:   "Pas de délai",
  next_year:    "Année proch.", next_quarter: "Prochain trim.",
  this_quarter: "Ce trimestre", immediate:    "Immédiat",
};

const DIM_LABELS: Record<keyof DimAvgs, string> = {
  budget: "Budget", authority: "Autorité", need: "Besoin", timeline: "Délai",
};

// ── Helpers ────────────────────────────────────────────────────────────────────

function eur(n: number) { return `${n.toLocaleString("fr-FR", { maximumFractionDigits: 0 })} €`; }
function cap(s: string) { return s.charAt(0).toUpperCase() + s.slice(1); }

function ScoreRing({ score }: { score: number }) {
  const color = score >= 75 ? "text-red-400" : score >= 50 ? "text-amber-400" : score >= 25 ? "text-blue-400" : "text-gray-500";
  return (
    <div className={`w-12 h-12 rounded-full border-2 flex items-center justify-center font-bold text-sm ${color} border-current`}>
      {score}
    </div>
  );
}

function BANTBar({ label, pts, max = 25 }: { label: string; pts: number; max?: number }) {
  const pct = Math.round(pts / max * 100);
  const color = pct >= 80 ? "bg-emerald-500" : pct >= 60 ? "bg-blue-500" : pct >= 40 ? "bg-amber-500" : "bg-red-500";
  return (
    <div className="flex items-center gap-2">
      <span className="text-[10px] text-gray-500 w-16 flex-shrink-0">{label}</span>
      <div className="flex-1 h-1.5 bg-white/[0.05] rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-[10px] text-gray-400 font-mono w-8 text-right">{pts}/25</span>
    </div>
  );
}

// ── Record modal ───────────────────────────────────────────────────────────────

function QualModal({ rec, onClose }: { rec: QualRecord; onClose: () => void }) {
  const { bant } = rec;
  const tm = TIER_META[bant.tier];
  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-[#0f1117] border border-white/[0.08] rounded-2xl w-full max-w-md max-h-[90vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
        <div className="flex items-start justify-between p-5 border-b border-white/[0.06] sticky top-0 bg-[#0f1117]">
          <div>
            <h2 className="font-bold text-lg">{rec.company_name}</h2>
            <p className="text-sm text-gray-500">{cap(rec.sector)} · {rec.contact_name} ({rec.contact_role})</p>
          </div>
          <button onClick={onClose} className="text-gray-500 hover:text-white text-xl ml-4">×</button>
        </div>

        <div className="p-5 space-y-5">
          {/* Score + tier */}
          <div className="flex items-center gap-4">
            <ScoreRing score={bant.total} />
            <div>
              <span className={`text-xs px-2 py-0.5 rounded-full border font-bold ${tm.color}`}>{tm.label}</span>
              <p className="text-sm text-gray-400 mt-1">Score BANT global</p>
            </div>
          </div>

          {/* BANT breakdown */}
          <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4 space-y-3">
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Détail BANT</p>
            <BANTBar label="Budget"    pts={bant.budget_pts} />
            <BANTBar label="Autorité"  pts={bant.authority_pts} />
            <BANTBar label="Besoin"    pts={bant.need_pts} />
            <BANTBar label="Délai"     pts={bant.timeline_pts} />
          </div>

          {/* Key facts */}
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-3">
              <p className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Budget estimé</p>
              <p className="font-bold text-white">{bant.budget_eur > 0 ? eur(bant.budget_eur) : "N/C"}</p>
              <p className="text-[10px] text-gray-600 mt-0.5">{bant.budget_confirmed ? "Confirmé" : "Non confirmé"}</p>
            </div>
            <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-3">
              <p className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Niveau autorité</p>
              <p className="font-bold text-white text-sm">{AUTH_LABELS[bant.authority_level]}</p>
            </div>
            <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-3">
              <p className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Sévérité besoin</p>
              <div className="flex gap-0.5 mt-1">
                {[1,2,3,4,5].map(n => (
                  <div key={n} className={`w-3 h-3 rounded-sm ${n <= bant.need_severity ? "bg-indigo-500" : "bg-white/[0.06]"}`} />
                ))}
              </div>
              <p className="text-[10px] text-gray-600 mt-0.5">{bant.need_articulated ? "Problème articulé" : "Non articulé"}</p>
            </div>
            <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-3">
              <p className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Délai décision</p>
              <p className="font-bold text-white text-sm">{TL_LABELS[bant.timeline]}</p>
            </div>
          </div>

          {rec.notes && (
            <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-3">
              <p className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Notes</p>
              <p className="text-sm text-gray-300 italic">"{rec.notes}"</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Page ───────────────────────────────────────────────────────────────────────

export default function QualificationPage() {
  const [data, setData]       = useState<Data | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<QualRecord | null>(null);
  const [tierFilter, setTierFilter] = useState<QTier | "all">("all");

  useEffect(() => {
    fetch("/api/qualification").then(r => r.json()).then(setData).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex items-center justify-center h-64"><div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" /></div>;
  if (!data)   return <p className="text-gray-500 p-8">Erreur de chargement.</p>;

  const { summary, records } = data;

  const filtered = tierFilter === "all" ? records : records.filter(r => r.bant.tier === tierFilter);

  const sortedFiltered = [...filtered].sort((a, b) => b.bant.total - a.bant.total);

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      {selected && <QualModal rec={selected} onClose={() => setSelected(null)} />}

      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Qualification BANT</h1>
          <p className="text-sm text-gray-500 mt-0.5">Scoring Budget · Autorité · Besoin · Délai</p>
        </div>
        {data.source === "mock" && <span className="text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2 py-1 rounded-full">Données démo</span>}
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: "Score moyen", value: `${summary.avg_score}/100`,  color: "text-white"       },
          { label: "HOT",         value: String(summary.tier_hot),    color: "text-red-400"     },
          { label: "WARM",        value: String(summary.tier_warm),   color: "text-amber-400"   },
          { label: "Dimension +faible", value: summary.weakest_bant ? DIM_LABELS[summary.weakest_bant as keyof DimAvgs] ?? summary.weakest_bant : "—", color: "text-orange-400" },
        ].map(k => (
          <div key={k.label} className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">{k.label}</p>
            <p className={`text-2xl font-bold ${k.color}`}>{k.value}</p>
          </div>
        ))}
      </div>

      {/* Tier cards + BANT dimension avgs */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Tier breakdown */}
        <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-5">
          <h2 className="text-sm font-semibold text-gray-300 mb-4">Répartition par tier</h2>
          <div className="space-y-3">
            {(["hot","warm","cool","cold"] as QTier[]).map(tier => {
              const cnt = tier === "hot" ? summary.tier_hot : tier === "warm" ? summary.tier_warm : tier === "cool" ? summary.tier_cool : summary.tier_cold;
              const pct = summary.total > 0 ? Math.round(cnt / summary.total * 100) : 0;
              const m = TIER_META[tier];
              return (
                <div key={tier} className="flex items-center gap-3">
                  <div className={`w-2.5 h-2.5 rounded-full flex-shrink-0 ${m.dot}`} />
                  <span className="text-sm text-gray-300 w-12">{m.label}</span>
                  <div className="flex-1 h-2 bg-white/[0.05] rounded-full overflow-hidden">
                    <div className={`h-full rounded-full ${m.dot}`} style={{ width: `${pct}%` }} />
                  </div>
                  <span className="text-xs text-gray-400 font-mono w-10 text-right">{cnt} ({pct}%)</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Dimension averages */}
        <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-5">
          <h2 className="text-sm font-semibold text-gray-300 mb-4">Moyennes BANT (sur 25)</h2>
          <div className="space-y-3">
            {(Object.entries(summary.dimension_avgs) as [keyof DimAvgs, number][]).map(([dim, avg]) => (
              <div key={dim} className="flex items-center gap-3">
                <span className="text-sm text-gray-300 w-16">{DIM_LABELS[dim]}</span>
                <div className="flex-1 h-2 bg-white/[0.05] rounded-full overflow-hidden">
                  <div className={`h-full rounded-full ${avg >= 20 ? "bg-emerald-500" : avg >= 15 ? "bg-blue-500" : avg >= 10 ? "bg-amber-500" : "bg-red-500"}`}
                    style={{ width: `${Math.round(avg / 25 * 100)}%` }} />
                </div>
                <span className="text-xs font-mono text-gray-300 w-12 text-right">{avg}/25</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Tier filter tabs */}
      <div className="flex gap-2 flex-wrap">
        <button onClick={() => setTierFilter("all")}
          className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${tierFilter === "all" ? "bg-indigo-600 border-indigo-500 text-white" : "bg-white/[0.03] border-white/[0.07] text-gray-400 hover:text-white"}`}>
          Tous ({summary.total})
        </button>
        {(["hot","warm","cool","cold"] as QTier[]).map(tier => {
          const cnt = tier === "hot" ? summary.tier_hot : tier === "warm" ? summary.tier_warm : tier === "cool" ? summary.tier_cool : summary.tier_cold;
          const m = TIER_META[tier];
          return (
            <button key={tier} onClick={() => setTierFilter(tier)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${tierFilter === tier ? "bg-indigo-600 border-indigo-500 text-white" : "bg-white/[0.03] border-white/[0.07] text-gray-400 hover:text-white"}`}>
              {m.label} {cnt > 0 ? `(${cnt})` : ""}
            </button>
          );
        })}
      </div>

      {/* Prospect table */}
      <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[750px]">
            <thead>
              <tr className="border-b border-white/[0.06]">
                {["Score", "Entreprise", "Contact", "Budget", "Autorité", "Besoin", "Délai", "Tier"].map(h => (
                  <th key={h} className="text-left py-3 px-4 text-xs text-gray-500 uppercase tracking-wider font-medium">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {sortedFiltered.length === 0 ? (
                <tr><td colSpan={8} className="text-center py-10 text-gray-600 text-sm">Aucun prospect.</td></tr>
              ) : sortedFiltered.map(rec => {
                const { bant } = rec;
                const tm = TIER_META[bant.tier];
                return (
                  <tr key={rec.record_id} className="border-b border-white/[0.04] hover:bg-white/[0.02] cursor-pointer" onClick={() => setSelected(rec)}>
                    <td className="py-3 px-4">
                      <div className={`font-bold text-lg ${bant.total >= 75 ? "text-red-400" : bant.total >= 50 ? "text-amber-400" : bant.total >= 25 ? "text-blue-400" : "text-gray-500"}`}>
                        {bant.total}
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <p className="font-medium text-sm">{rec.company_name}</p>
                      <p className="text-xs text-gray-600">{cap(rec.sector)}</p>
                    </td>
                    <td className="py-3 px-4 text-xs text-gray-400">
                      <p>{rec.contact_name || "—"}</p>
                      <p className="text-gray-600">{rec.contact_role}</p>
                    </td>
                    <td className="py-3 px-4 text-xs">
                      <p className="font-mono text-gray-300">{bant.budget_eur > 0 ? eur(bant.budget_eur) : "N/C"}</p>
                      <p className="text-gray-600">{bant.budget_confirmed ? "Confirmé" : "Estimé"}</p>
                    </td>
                    <td className="py-3 px-4 text-xs text-gray-400">{AUTH_LABELS[bant.authority_level]}</td>
                    <td className="py-3 px-4">
                      <div className="flex gap-0.5">
                        {[1,2,3,4,5].map(n => (
                          <div key={n} className={`w-2.5 h-2.5 rounded-sm ${n <= bant.need_severity ? "bg-indigo-500" : "bg-white/[0.06]"}`} />
                        ))}
                      </div>
                    </td>
                    <td className="py-3 px-4 text-xs text-gray-400">{TL_LABELS[bant.timeline]}</td>
                    <td className="py-3 px-4">
                      <span className={`text-xs px-2 py-0.5 rounded-full border font-bold ${tm.color}`}>{tm.label}</span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
      <p className="text-xs text-gray-600 text-center">{sortedFiltered.length} prospect(s) — Cliquer pour le détail BANT</p>
    </div>
  );
}
