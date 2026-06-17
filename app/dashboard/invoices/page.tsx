"use client";

import { useEffect, useState } from "react";

// ── Types ──────────────────────────────────────────────────────────────────────

type InvoiceStatus = "draft" | "sent" | "partially_paid" | "paid" | "overdue" | "cancelled";
type PaymentMethod = "stripe" | "bank_transfer" | "cheque" | "cash" | "other";

interface Payment {
  payment_id: string;
  amount: number;
  method: PaymentMethod;
  received_at: string;
  reference: string;
}

interface Invoice {
  invoice_id: string;
  prospect_id: string;
  company_name: string;
  sector: string;
  amount_ht: number;
  tva_pct: number;
  amount_ttc: number;
  tva_amount: number;
  amount_paid: number;
  amount_remaining: number;
  status: InvoiceStatus;
  due_days: number;
  created_at: string;
  sent_at: string | null;
  due_at: string | null;
  paid_at: string | null;
  cancelled_at: string | null;
  notes: string;
  payments: Payment[];
}

interface Summary {
  total: number;
  draft: number;
  sent: number;
  partially_paid: number;
  paid: number;
  overdue: number;
  cancelled: number;
  total_invoiced_ttc: number;
  total_collected_ttc: number;
  total_outstanding_ttc: number;
  total_overdue_ttc: number;
  collection_rate_pct: number;
  avg_days_to_pay: number | null;
}

interface Data {
  source: string;
  invoices: Invoice[];
  summary: Summary;
}

// ── Constants ──────────────────────────────────────────────────────────────────

const STATUS_META: Record<InvoiceStatus, { label: string; color: string }> = {
  draft:          { label: "Brouillon",      color: "bg-gray-500/20 text-gray-300 border-gray-500/30" },
  sent:           { label: "Envoyée",        color: "bg-blue-500/20 text-blue-300 border-blue-500/30" },
  partially_paid: { label: "Partiel",        color: "bg-cyan-500/20 text-cyan-300 border-cyan-500/30" },
  paid:           { label: "Payée",          color: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30" },
  overdue:        { label: "En retard",      color: "bg-red-500/20 text-red-300 border-red-500/30" },
  cancelled:      { label: "Annulée",        color: "bg-orange-500/20 text-orange-400 border-orange-500/30" },
};

const METHOD_LABELS: Record<PaymentMethod, string> = {
  stripe:         "Stripe",
  bank_transfer:  "Virement",
  cheque:         "Chèque",
  cash:           "Espèces",
  other:          "Autre",
};

// ── Helpers ────────────────────────────────────────────────────────────────────

function eur(n: number) { return `${n.toLocaleString("fr-FR", { maximumFractionDigits: 0 })} €`; }
function cap(s: string) { return s.charAt(0).toUpperCase() + s.slice(1); }
function fmtDate(iso: string | null) {
  if (!iso) return "—";
  return new Date(iso).toLocaleDateString("fr-FR", { day: "2-digit", month: "short", year: "numeric" });
}

function StatusBadge({ status }: { status: InvoiceStatus }) {
  const m = STATUS_META[status];
  return <span className={`text-xs px-2 py-0.5 rounded-full border ${m.color}`}>{m.label}</span>;
}

function CollectBar({ paid, total }: { paid: number; total: number }) {
  const pct = total > 0 ? Math.min(100, (paid / total) * 100) : 0;
  const color = pct >= 100 ? "bg-emerald-500" : pct >= 50 ? "bg-blue-500" : pct > 0 ? "bg-amber-500" : "bg-white/[0.08]";
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 bg-white/[0.05] rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-xs font-mono text-gray-400 w-8 text-right">{Math.round(pct)}%</span>
    </div>
  );
}

// ── Invoice modal ──────────────────────────────────────────────────────────────

function InvoiceModal({ inv, onClose }: { inv: Invoice; onClose: () => void }) {
  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-[#0f1117] border border-white/[0.08] rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
        <div className="flex items-start justify-between p-5 border-b border-white/[0.06] sticky top-0 bg-[#0f1117]">
          <div>
            <h2 className="font-bold text-lg">{inv.company_name}</h2>
            <p className="text-sm text-gray-500">{inv.invoice_id} · {cap(inv.sector)}</p>
          </div>
          <button onClick={onClose} className="text-gray-500 hover:text-white text-xl ml-4">×</button>
        </div>

        <div className="p-5 space-y-5">
          {/* Status */}
          <div className="flex gap-2 flex-wrap items-center">
            <StatusBadge status={inv.status} />
            {inv.notes && <span className="text-xs text-gray-500 italic">"{inv.notes}"</span>}
          </div>

          {/* Amounts */}
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-3 col-span-2">
              <div className="flex justify-between items-center mb-2">
                <span className="text-xs text-gray-500">Montant HT</span>
                <span className="text-sm font-mono text-gray-300">{eur(inv.amount_ht)}</span>
              </div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-xs text-gray-500">TVA {inv.tva_pct}%</span>
                <span className="text-sm font-mono text-gray-500">+{eur(inv.tva_amount)}</span>
              </div>
              <div className="flex justify-between items-center border-t border-white/[0.06] pt-2 mt-2">
                <span className="text-sm font-semibold text-white">Total TTC</span>
                <span className="text-lg font-bold text-white">{eur(inv.amount_ttc)}</span>
              </div>
            </div>
            <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-3">
              <p className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Encaissé</p>
              <p className="text-xl font-bold text-emerald-400">{eur(inv.amount_paid)}</p>
            </div>
            <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-3">
              <p className="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Restant</p>
              <p className={`text-xl font-bold ${inv.amount_remaining > 0 ? "text-amber-400" : "text-emerald-400"}`}>{eur(inv.amount_remaining)}</p>
            </div>
          </div>

          {/* Collection bar */}
          <div>
            <p className="text-xs text-gray-500 mb-2">Recouvrement</p>
            <CollectBar paid={inv.amount_paid} total={inv.amount_ttc} />
          </div>

          {/* Dates */}
          <div className="grid grid-cols-3 gap-3 text-center">
            {[
              { label: "Créée le",    value: fmtDate(inv.created_at) },
              { label: "Envoyée le",  value: fmtDate(inv.sent_at) },
              { label: "Échéance",    value: fmtDate(inv.due_at) },
            ].map(d => (
              <div key={d.label} className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-2">
                <p className="text-[9px] text-gray-600 uppercase tracking-wider mb-0.5">{d.label}</p>
                <p className="text-xs text-gray-300">{d.value}</p>
              </div>
            ))}
          </div>

          {/* Payments */}
          {inv.payments.length > 0 && (
            <div>
              <p className="text-xs text-gray-500 uppercase tracking-wider mb-3">Paiements reçus</p>
              <div className="space-y-2">
                {inv.payments.map(p => (
                  <div key={p.payment_id} className="flex items-center justify-between bg-white/[0.03] border border-white/[0.06] rounded-xl px-3 py-2">
                    <div>
                      <p className="text-sm font-bold text-emerald-400">{eur(p.amount)}</p>
                      <p className="text-[10px] text-gray-600">{p.payment_id}{p.reference ? ` · ${p.reference}` : ""}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-gray-400">{METHOD_LABELS[p.method]}</p>
                      <p className="text-[10px] text-gray-600">{fmtDate(p.received_at)}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Page ───────────────────────────────────────────────────────────────────────

export default function InvoicesPage() {
  const [data, setData]       = useState<Data | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Invoice | null>(null);
  const [statusFilter, setStatusFilter] = useState<InvoiceStatus | "all">("all");

  useEffect(() => {
    fetch("/api/invoices").then(r => r.json()).then(setData).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex items-center justify-center h-64"><div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" /></div>;
  if (!data)   return <p className="text-gray-500 p-8">Erreur de chargement.</p>;

  const { summary, invoices } = data;

  const filtered = statusFilter === "all"
    ? invoices
    : invoices.filter(i => i.status === statusFilter);

  const statusCounts = {
    all:           invoices.length,
    draft:         invoices.filter(i => i.status === "draft").length,
    sent:          invoices.filter(i => i.status === "sent").length,
    partially_paid: invoices.filter(i => i.status === "partially_paid").length,
    paid:          invoices.filter(i => i.status === "paid").length,
    overdue:       invoices.filter(i => i.status === "overdue").length,
    cancelled:     invoices.filter(i => i.status === "cancelled").length,
  };

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      {selected && <InvoiceModal inv={selected} onClose={() => setSelected(null)} />}

      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Factures</h1>
          <p className="text-sm text-gray-500 mt-0.5">Suivi des encaissements et du recouvrement</p>
        </div>
        {data.source === "mock" && <span className="text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2 py-1 rounded-full">Données démo</span>}
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: "Facturé TTC",    value: eur(summary.total_invoiced_ttc),   color: "text-white"       },
          { label: "Encaissé TTC",   value: eur(summary.total_collected_ttc),  color: "text-emerald-400" },
          { label: "En attente",     value: eur(summary.total_outstanding_ttc), color: "text-amber-400"   },
          { label: "En retard",      value: eur(summary.total_overdue_ttc),    color: "text-red-400"     },
        ].map(k => (
          <div key={k.label} className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">{k.label}</p>
            <p className={`text-2xl font-bold ${k.color}`}>{k.value}</p>
          </div>
        ))}
      </div>

      {/* Secondary KPIs + collection rate */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Collection rate card */}
        <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-5 flex flex-col justify-between">
          <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Taux de recouvrement</p>
          <p className={`text-4xl font-bold mb-3 ${summary.collection_rate_pct >= 80 ? "text-emerald-400" : summary.collection_rate_pct >= 50 ? "text-amber-400" : "text-red-400"}`}>
            {summary.collection_rate_pct}%
          </p>
          <div className="h-2 bg-white/[0.05] rounded-full overflow-hidden">
            <div className={`h-full rounded-full ${summary.collection_rate_pct >= 80 ? "bg-emerald-500" : "bg-amber-500"}`}
              style={{ width: `${summary.collection_rate_pct}%` }} />
          </div>
          {summary.avg_days_to_pay !== null && (
            <p className="text-xs text-gray-500 mt-2">Délai moyen de paiement : <span className="text-white font-medium">{summary.avg_days_to_pay}j</span></p>
          )}
        </div>

        {/* Count breakdown */}
        <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-5 col-span-2">
          <p className="text-xs text-gray-500 uppercase tracking-wider mb-3">Répartition par statut</p>
          <div className="grid grid-cols-3 gap-3">
            {(["draft","sent","partially_paid","paid","overdue","cancelled"] as InvoiceStatus[]).map(s => {
              const cnt = statusCounts[s];
              const m = STATUS_META[s];
              return (
                <div key={s} className="text-center">
                  <p className={`text-2xl font-bold ${s === "paid" ? "text-emerald-400" : s === "overdue" ? "text-red-400" : s === "sent" ? "text-blue-400" : "text-gray-300"}`}>{cnt}</p>
                  <p className="text-[10px] text-gray-500 mt-0.5">{m.label}</p>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Status filter tabs */}
      <div className="flex gap-2 flex-wrap">
        {(["all", "draft", "sent", "partially_paid", "paid", "overdue", "cancelled"] as const).map(s => {
          const cnt = statusCounts[s as keyof typeof statusCounts] ?? 0;
          const label = s === "all" ? "Toutes" : STATUS_META[s as InvoiceStatus].label;
          return (
            <button key={s} onClick={() => setStatusFilter(s as InvoiceStatus | "all")}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${statusFilter === s ? "bg-indigo-600 border-indigo-500 text-white" : "bg-white/[0.03] border-white/[0.07] text-gray-400 hover:text-white"}`}>
              {label} {cnt > 0 ? `(${cnt})` : ""}
            </button>
          );
        })}
      </div>

      {/* Table */}
      <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[700px]">
            <thead>
              <tr className="border-b border-white/[0.06]">
                {["Facture", "Entreprise", "Statut", "Total TTC", "Encaissé", "Recouvrement", "Échéance"].map(h => (
                  <th key={h} className="text-left py-3 px-4 text-xs text-gray-500 uppercase tracking-wider font-medium">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 ? (
                <tr><td colSpan={7} className="text-center py-10 text-gray-600 text-sm">Aucune facture.</td></tr>
              ) : filtered.map(inv => (
                <tr key={inv.invoice_id} className="border-b border-white/[0.04] hover:bg-white/[0.02] cursor-pointer" onClick={() => setSelected(inv)}>
                  <td className="py-3 px-4">
                    <p className="font-mono text-sm text-indigo-400">{inv.invoice_id}</p>
                    <p className="text-[10px] text-gray-600">{cap(inv.sector)}</p>
                  </td>
                  <td className="py-3 px-4 font-medium text-sm">{inv.company_name}</td>
                  <td className="py-3 px-4"><StatusBadge status={inv.status} /></td>
                  <td className="py-3 px-4 text-sm font-mono font-bold text-white">{eur(inv.amount_ttc)}</td>
                  <td className="py-3 px-4 text-sm font-mono text-emerald-400">{eur(inv.amount_paid)}</td>
                  <td className="py-3 px-4 w-32"><CollectBar paid={inv.amount_paid} total={inv.amount_ttc} /></td>
                  <td className="py-3 px-4 text-xs text-gray-500">
                    <span className={inv.status === "overdue" ? "text-red-400 font-medium" : ""}>{fmtDate(inv.due_at)}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <p className="text-xs text-gray-600 text-center">{filtered.length} facture(s) — Cliquer pour le détail</p>
    </div>
  );
}
