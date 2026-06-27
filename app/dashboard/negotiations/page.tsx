"use client";

import { useEffect, useState } from "react";

// ── Types ──────────────────────────────────────────────────────────────────────

type NegStatus = "opened" | "in_progress" | "agreed" | "failed" | "abandoned";
type OfferParty = "us" | "prospect";
type ConcessionType = "price" | "scope" | "timeline" | "payment" | "other";

interface Offer {
  round_number: number;
  party: OfferParty;
  amount: number;
  concession_type: ConcessionType;
  note: string;
  proposed_at: string;
}

interface Negotiation {
  negotiation_id: string;
  prospect_id: string;
  company_name: string;
  sector: string;
  asking_price: number;
  current_amount: number;
  final_amount: number | null;
  discount_pct: number;
  total_concession_eur: number;
  status: NegStatus;
  rounds: number;
  duration_days: number;
  failure_reason: string;
  opened_at: string;
  closed_at: string | null;
  offers: Offer[];
}

interface Summary {
  total: number;
  active: number;
  agreed: number;
  failed_or_abandoned: number;
  win_rate_pct: number;
  avg_discount_pct: number;
  avg_rounds: number;
  avg_duration_days: number;
  total_agreed_eur: number;
  total_conceded_eur: number;
}

interface Data {
  source: string;
  negotiations: Negotiation[];
  summary: Summary;
}

// ── Constants ──────────────────────────────────────────────────────────────────

const STATUS_META: Record<NegStatus, { label: string; color: string }> = {
  opened:      { label: "Ouverte",    color: "bg-gray-500/20 text-gray-300 border-gray-500/30" },
  in_progress: { label: "En cours",   color: "bg-blue-500/20 text-blue-300 border-blue-500/30" },
  agreed:      { label: "Accord",     color: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30" },
  failed:      { label: "Échouée",    color: "bg-red-500/20 text-red-300 border-red-500/30" },
  abandoned:   { label: "Abandonnée", color: "bg-orange-500/20 text-orange-300 border-orange-500/30" },
};

const CONCESSION_LABELS: Record<ConcessionType, string> = {
  price:    "Prix",
  scope:    "Périmètre",
  timeline: "Délai",
  payment:  "Paiement",
  other:    "Autre",
};

// ── Helpers ────────────────────────────────────────────────────────────────────

function eur(n: number) { return `${n.toLocaleString("fr-FR", { maximumFractionDigits: 0 })} €`; }
function cap(s: string) { return s.charAt(0).toUpperCase() + s.slice(1); }

function StatusBadge({ status }: { status: NegStatus }) {
  const m = STATUS_META[status];
  return <span className={`text-xs px-2 py-0.5 rounded-full border ${m.color}`}>{m.label}</span>;
}

function DiscountBar({ pct }: { pct: number }) {
  const color = pct === 0 ? "bg-emerald-500" : pct < 5 ? "bg-blue-500" : pct < 10 ? "bg-amber-500" : "bg-red-500";
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 bg-white/[0.05] rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${Math.min(pct * 5, 100)}%` }} />
      </div>
      <span className={`text-xs font-mono w-10 text-right ${pct === 0 ? "text-emerald-400" : pct < 5 ? "text-blue-400" : pct < 10 ? "text-amber-400" : "text-red-400"}`}>
        -{pct}%
      </span>
    </div>
  );
}

// ── Offer timeline ─────────────────────────────────────────────────────────────

function OfferTimeline({ offers }: { offers: Offer[] }) {
  if (offers.length === 0) {
    return <p className="text-xs text-gray-600 italic">Aucune offre échangée</p>;
  }
  return (
    <div className="space-y-2">
      {offers.map(o => {
        const isUs = o.party === "us";
        return (
          <div key={o.round_number} className={`flex gap-3 ${isUs ? "flex-row-reverse" : ""}`}>
            <div className={`flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold ${isUs ? "bg-indigo-600 text-white" : "bg-white/[0.08] text-gray-300"}`}>
              {o.round_number}
            </div>
            <div className={`flex-1 max-w-xs rounded-xl p-3 border ${isUs ? "bg-indigo-950/50 border-indigo-500/20 text-right" : "bg-white/[0.03] border-white/[0.08]"}`}>
              <div className="flex items-center gap-2 justify-between mb-1">
                <span className="text-[10px] text-gray-500">{isUs ? "Nous" : "Prospect"}</span>
                <span className="text-[10px] text-gray-500">{CONCESSION_LABELS[o.concession_type]}</span>
              </div>
              <p className="text-base font-bold text-white">{eur(o.amount)}</p>
              {o.note && <p className="text-xs text-gray-400 mt-1 italic">"{o.note}"</p>}
            </div>
          </div>
        );
      })}
    </div>
  );
}

// ── Negotiation modal ──────────────────────────────────────────────────────────

function NegotiationModal({ neg, onClose }: { neg: Negotiation; onClose: () => void }) {
  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-[#0f1117] border border-white/[0.08] rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
        <div className="flex items-start justify-between p-5 border-b border-white/[0.06] sticky top-0 bg-[#0f1117] z-10">
          <div>
            <h2 className="font-bold text-lg">{neg.company_name}</h2>
            <p className="text-sm text-gray-500">{cap(neg.sector)} · {neg.negotiation_id}</p>
          </div>
          <button onClick={onClose} className="text-gray-500 hover:text-white text-xl ml-4">×</button>
        </div>

        <div className="p-5 space-y-5">
          <div className="flex gap-3 flex-wrap">
            <StatusBadge status={neg.status} />
            <span className="text-xs text-gray-500">{neg.rounds} tour{neg.rounds !== 1 ? "s" : ""} · {neg.duration_days}j</span>
            {neg.failure_reason && (
              <span className="text-xs text-red-400 bg-red-500/10 border border-red-500/20 px-2 py-0.5 rounded-full">{neg.failure_reason}</span>
            )}
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-3">
              <p className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Prix demandé</p>
              <p className="text-lg font-bold text-white">{eur(neg.asking_price)}</p>
            </div>
            <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-3">
              <p className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Prix actuel</p>
              <p className={`text-lg font-bold ${neg.status === "agreed" ? "text-emerald-400" : "text-amber-400"}`}>{eur(neg.current_amount)}</p>
            </div>
            <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-3">
              <p className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Concession</p>
              <p className={`text-lg font-bold ${neg.discount_pct === 0 ? "text-emerald-400" : "text-red-400"}`}>-{eur(neg.total_concession_eur)}</p>
            </div>
          </div>

          <div>
            <p className="text-xs text-gray-500 mb-2">Remise accordée</p>
            <DiscountBar pct={neg.discount_pct} />
          </div>

          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-3">Historique des offres</p>
            <OfferTimeline offers={neg.offers} />
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Page ───────────────────────────────────────────────────────────────────────

export default function NegotiationsPage() {
  const [data, setData]       = useState<Data | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Negotiation | null>(null);
  const [statusFilter, setStatusFilter] = useState<NegStatus | "all">("all");

  useEffect(() => {
    fetch("/api/negotiations").then(r => r.json()).then(setData).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex items-center justify-center h-64"><div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" /></div>;
  if (!data)   return <p className="text-gray-500 p-8">Erreur de chargement.</p>;

  const { summary, negotiations } = data;

  const filtered = statusFilter === "all"
    ? negotiations
    : negotiations.filter(n => n.status === statusFilter);

  const statusCounts: Partial<Record<NegStatus | "all", number>> = {
    all:         negotiations.length,
    opened:      negotiations.filter(n => n.status === "opened").length,
    in_progress: negotiations.filter(n => n.status === "in_progress").length,
    agreed:      negotiations.filter(n => n.status === "agreed").length,
    failed:      negotiations.filter(n => n.status === "failed").length,
    abandoned:   negotiations.filter(n => n.status === "abandoned").length,
  };

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      {selected && <NegotiationModal neg={selected} onClose={() => setSelected(null)} />}

      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Négociations</h1>
          <p className="text-sm text-gray-500 mt-0.5">Suivi des offres et contre-offres par prospect</p>
        </div>
        {data.source === "mock" && <span className="text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2 py-1 rounded-full">Données démo</span>}
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
        {[
          { label: "Total",         value: String(summary.total),           color: "text-white"       },
          { label: "Taux de gain",  value: `${summary.win_rate_pct}%`,      color: "text-emerald-400" },
          { label: "CA conclu",     value: eur(summary.total_agreed_eur),   color: "text-indigo-400"  },
          { label: "Remise moy.",   value: `-${summary.avg_discount_pct}%`, color: "text-amber-400"   },
          { label: "Concédé total", value: eur(summary.total_conceded_eur), color: "text-red-400"     },
        ].map(k => (
          <div key={k.label} className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">{k.label}</p>
            <p className={`text-2xl font-bold ${k.color}`}>{k.value}</p>
          </div>
        ))}
      </div>

      {/* Secondary KPIs */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: "Actives",          value: String(summary.active),              color: "text-blue-400"    },
          { label: "Accordées",        value: String(summary.agreed),              color: "text-emerald-400" },
          { label: "Échouées/Aband.", value: String(summary.failed_or_abandoned),  color: "text-red-400"     },
          { label: "Tours moy.",       value: `${summary.avg_rounds}`,             color: "text-gray-300"    },
        ].map(k => (
          <div key={k.label} className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">{k.label}</p>
            <p className={`text-2xl font-bold ${k.color}`}>{k.value}</p>
          </div>
        ))}
      </div>

      {/* Status filter tabs */}
      <div className="flex gap-2 flex-wrap">
        {(["all", "opened", "in_progress", "agreed", "failed", "abandoned"] as const).map(s => {
          const cnt = statusCounts[s] ?? 0;
          const label = s === "all" ? "Toutes" : STATUS_META[s].label;
          return (
            <button key={s} onClick={() => setStatusFilter(s)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${statusFilter === s ? "bg-indigo-600 border-indigo-500 text-white" : "bg-white/[0.03] border-white/[0.07] text-gray-400 hover:text-white"}`}>
              {label} {cnt > 0 ? `(${cnt})` : ""}
            </button>
          );
        })}
      </div>

      {/* Table */}
      <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[720px]">
            <thead>
              <tr className="border-b border-white/[0.06]">
                {["Entreprise", "Secteur", "Statut", "Prix demandé", "Prix actuel", "Remise", "Tours", "Durée"].map(h => (
                  <th key={h} className="text-left py-3 px-4 text-xs text-gray-500 uppercase tracking-wider font-medium">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 ? (
                <tr><td colSpan={8} className="text-center py-10 text-gray-600 text-sm">Aucune négociation.</td></tr>
              ) : filtered.map(neg => (
                <tr key={neg.negotiation_id} className="border-b border-white/[0.04] hover:bg-white/[0.02] cursor-pointer" onClick={() => setSelected(neg)}>
                  <td className="py-3 px-4">
                    <p className="font-medium text-sm">{neg.company_name}</p>
                    <p className="text-xs text-gray-600">{neg.negotiation_id}</p>
                  </td>
                  <td className="py-3 px-4 text-xs text-gray-400">{cap(neg.sector)}</td>
                  <td className="py-3 px-4"><StatusBadge status={neg.status} /></td>
                  <td className="py-3 px-4 text-sm font-mono text-gray-400">{eur(neg.asking_price)}</td>
                  <td className="py-3 px-4 text-sm font-mono font-bold">
                    <span className={neg.status === "agreed" ? "text-emerald-400" : "text-white"}>{eur(neg.current_amount)}</span>
                  </td>
                  <td className="py-3 px-4 w-32"><DiscountBar pct={neg.discount_pct} /></td>
                  <td className="py-3 px-4 text-xs text-gray-500 text-center">{neg.rounds}</td>
                  <td className="py-3 px-4 text-xs text-gray-500 text-center">{neg.duration_days}j</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <p className="text-xs text-gray-600 text-center">{filtered.length} négociation(s) — Cliquer pour le détail</p>
    </div>
  );
}
