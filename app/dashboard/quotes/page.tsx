"use client";

import { useEffect, useState } from "react";

// ── Types ──────────────────────────────────────────────────────────────────────

interface QuotePackage { code: string; name: string; base_price_eur: number; }

interface QuoteRecord {
  prospect_id: string;
  company_name: string;
  sector: string;
  pagespeed_score: number;
  load_time_ms: number;
  mobile_responsive: boolean;
  issue_count: number;
  severity: number;
  package: QuotePackage;
  sector_multiplier: number;
  discount_pct: number;
  urgency_bonus_eur: number;
  subtotal_eur: number;
  total_ht_eur: number;
  tva_eur: number;
  total_ttc_eur: number;
}

interface PricingData {
  source: string;
  summary: { total_quotes: number; total_pipeline_eur: number; average_quote_eur: number; by_package: Record<string, number> };
  quotes: QuoteRecord[];
}

// ── Colour maps ────────────────────────────────────────────────────────────────

const PKG_COLORS: Record<string, string> = {
  starter:    "bg-gray-500/20 text-gray-300 border-gray-500/30",
  standard:   "bg-indigo-500/20 text-indigo-300 border-indigo-500/30",
  premium:    "bg-amber-500/20 text-amber-300 border-amber-500/30",
  enterprise: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
};

// ── Helpers ────────────────────────────────────────────────────────────────────

function eur(n: number) { return `${n.toLocaleString("fr-FR", { maximumFractionDigits: 0 })} €`; }
function cap(s: string) { return s.charAt(0).toUpperCase() + s.slice(1); }

function SeverityBar({ severity }: { severity: number }) {
  const pct = Math.round(severity * 100);
  const color = pct >= 75 ? "bg-red-500" : pct >= 55 ? "bg-orange-500" : pct >= 30 ? "bg-amber-500" : "bg-emerald-500";
  const textColor = pct >= 75 ? "text-red-400" : pct >= 55 ? "text-orange-400" : pct >= 30 ? "text-amber-400" : "text-emerald-400";
  return (
    <div className="flex items-center gap-2">
      <div className="w-14 h-1.5 bg-white/[0.05] rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className={`text-xs ${textColor}`}>{pct}%</span>
    </div>
  );
}

// ── Modal ─────────────────────────────────────────────────────────────────────

function QuoteModal({ q, onClose }: { q: QuoteRecord; onClose: () => void }) {
  const diagnostics = [
    { label: "PageSpeed", value: `${q.pagespeed_score}/100`, ok: q.pagespeed_score >= 60 },
    { label: "Chargement", value: `${(q.load_time_ms/1000).toFixed(1)}s`, ok: q.load_time_ms < 3000 },
    { label: "Mobile", value: q.mobile_responsive ? "OK" : "Problème", ok: q.mobile_responsive },
    { label: "Problèmes", value: String(q.issue_count), ok: q.issue_count === 0 },
  ];
  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-[#0f1117] border border-white/[0.08] rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
        <div className="flex items-start justify-between p-5 border-b border-white/[0.06]">
          <div>
            <h2 className="font-bold text-lg">{q.company_name}</h2>
            <p className="text-sm text-gray-500">{cap(q.sector)}</p>
          </div>
          <button onClick={onClose} className="text-gray-500 hover:text-white text-xl leading-none">×</button>
        </div>
        <div className="p-5 space-y-5">
          <div className="flex gap-3 items-center">
            <span className={`text-sm px-3 py-1 rounded-full border ${PKG_COLORS[q.package.code]}`}>{q.package.name}</span>
            <SeverityBar severity={q.severity} />
          </div>
          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Diagnostics</p>
            <div className="grid grid-cols-2 gap-2">
              {diagnostics.map(d => (
                <div key={d.label} className={`rounded-xl p-3 border ${d.ok ? "bg-emerald-500/10 border-emerald-500/20" : "bg-red-500/10 border-red-500/20"}`}>
                  <p className="text-xs text-gray-500">{d.label}</p>
                  <p className={`font-semibold text-sm mt-0.5 ${d.ok ? "text-emerald-400" : "text-red-400"}`}>{d.value}</p>
                </div>
              ))}
            </div>
          </div>
          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Détail du devis</p>
            <div className="bg-white/[0.03] rounded-xl p-4 space-y-2 text-sm">
              <div className="flex justify-between"><span className="text-gray-400">Package de base</span><span>{eur(q.package.base_price_eur)}</span></div>
              {q.sector_multiplier !== 1.0 && <div className="flex justify-between text-xs text-gray-500"><span>Mult. secteur</span><span>×{q.sector_multiplier.toFixed(2)}</span></div>}
              <div className="flex justify-between"><span className="text-gray-400">Sous-total</span><span>{eur(q.subtotal_eur)}</span></div>
              {q.discount_pct > 0 && <div className="flex justify-between text-emerald-400"><span>Remise ({q.discount_pct}%)</span><span>−{eur(q.subtotal_eur * q.discount_pct / 100)}</span></div>}
              {q.urgency_bonus_eur > 0 && <div className="flex justify-between text-amber-400"><span>Urgence +10%</span><span>+{eur(q.urgency_bonus_eur)}</span></div>}
              <div className="flex justify-between border-t border-white/[0.08] pt-2"><span className="text-gray-400">Total HT</span><span className="font-semibold">{eur(q.total_ht_eur)}</span></div>
              <div className="flex justify-between text-gray-500 text-xs"><span>TVA 20%</span><span>{eur(q.tva_eur)}</span></div>
              <div className="flex justify-between border-t border-white/[0.08] pt-2 text-emerald-400 font-bold text-base"><span>Total TTC</span><span>{eur(q.total_ttc_eur)}</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Page ───────────────────────────────────────────────────────────────────────

export default function QuotesPage() {
  const [data, setData]       = useState<PricingData | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<QuoteRecord | null>(null);
  const [pkgFilter, setPkgFilter] = useState("all");
  const [sortBy, setSortBy]   = useState<"ttc"|"severity"|"sector">("ttc");

  useEffect(() => {
    fetch("/api/pricing").then(r => r.json()).then(setData).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex items-center justify-center h-64"><div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" /></div>;
  if (!data) return <p className="text-gray-500 p-8">Erreur de chargement.</p>;

  const { summary, quotes } = data;
  const filtered = quotes
    .filter(q => pkgFilter === "all" || q.package.code === pkgFilter)
    .sort((a, b) => sortBy === "ttc" ? b.total_ttc_eur - a.total_ttc_eur : sortBy === "severity" ? b.severity - a.severity : a.sector.localeCompare(b.sector));

  const premEnt = (summary.by_package["premium"] ?? 0) + (summary.by_package["enterprise"] ?? 0);

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      {selected && <QuoteModal q={selected} onClose={() => setSelected(null)} />}

      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Pipeline Devis</h1>
          <p className="text-sm text-gray-500 mt-0.5">Devis dynamiques générés par le moteur de tarification</p>
        </div>
        {data.source === "mock" && <span className="text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2 py-1 rounded-full">Données démo</span>}
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: "Total devis", value: String(summary.total_quotes), color: "text-white" },
          { label: "Pipeline TTC", value: eur(summary.total_pipeline_eur), color: "text-emerald-400" },
          { label: "Devis moyen", value: eur(summary.average_quote_eur), color: "text-indigo-400" },
          { label: "Premium+Enterprise", value: `${premEnt} / ${Math.round(premEnt / Math.max(summary.total_quotes, 1) * 100)}%`, color: "text-amber-400" },
        ].map(k => (
          <div key={k.label} className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">{k.label}</p>
            <p className={`text-2xl font-bold ${k.color}`}>{k.value}</p>
          </div>
        ))}
      </div>

      {/* Filters & Sort */}
      <div className="flex flex-wrap gap-4 items-center">
        <div className="flex gap-2 flex-wrap">
          {["all","starter","standard","premium","enterprise"].map(f => (
            <button key={f} onClick={() => setPkgFilter(f)} className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${pkgFilter === f ? "bg-indigo-600 border-indigo-500 text-white" : "bg-white/[0.03] border-white/[0.07] text-gray-400 hover:text-white"}`}>
              {f === "all" ? "Tous" : cap(f)}
            </button>
          ))}
        </div>
        <div className="flex gap-2">
          {([["ttc","Prix TTC"],["severity","Sévérité"],["sector","Secteur"]] as const).map(([v,l]) => (
            <button key={v} onClick={() => setSortBy(v)} className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${sortBy === v ? "bg-white/[0.08] border-white/[0.15] text-white" : "bg-white/[0.03] border-white/[0.07] text-gray-400 hover:text-white"}`}>{l}</button>
          ))}
        </div>
      </div>

      {/* Table */}
      <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[640px]">
            <thead>
              <tr className="border-b border-white/[0.06]">
                {["Entreprise","Package","Sévérité","Mult.","Total HT","Total TTC"].map(h => (
                  <th key={h} className="text-left py-3 px-4 text-xs text-gray-500 uppercase tracking-wider font-medium">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 ? (
                <tr><td colSpan={6} className="text-center py-10 text-gray-600 text-sm">Aucun devis.</td></tr>
              ) : filtered.map(q => (
                <tr key={q.prospect_id} className="border-b border-white/[0.04] hover:bg-white/[0.02] cursor-pointer" onClick={() => setSelected(q)}>
                  <td className="py-3 px-4"><p className="font-medium text-sm">{q.company_name}</p><p className="text-xs text-gray-500">{cap(q.sector)}</p></td>
                  <td className="py-3 px-4"><span className={`text-xs px-2 py-0.5 rounded-full border ${PKG_COLORS[q.package.code]}`}>{q.package.name}</span></td>
                  <td className="py-3 px-4"><SeverityBar severity={q.severity} /></td>
                  <td className="py-3 px-4 text-xs text-gray-400">×{q.sector_multiplier.toFixed(2)}</td>
                  <td className="py-3 px-4 text-sm text-right font-mono">{eur(q.total_ht_eur)}</td>
                  <td className="py-3 px-4 text-sm text-right font-bold text-emerald-400 font-mono">{eur(q.total_ttc_eur)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <p className="text-xs text-gray-600 text-center">{filtered.length} devis — Cliquer pour le détail</p>
    </div>
  );
}
