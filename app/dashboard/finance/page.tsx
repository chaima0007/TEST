"use client";

import { useEffect, useState } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface DailyRevenue {
  date: string;
  revenue: number;
  transactions: number;
}

interface SectorRevenue {
  sector: string;
  revenue: number;
  deals: number;
  avg: number;
}

interface PricingTier {
  tier: string;
  price: number;
  count: number;
  revenue: number;
  description: string;
}

interface Transaction {
  id: string;
  company: string;
  sector: string;
  amount: number;
  status: "paid" | "pending" | "refunded";
  agent: string;
  date: string;
}

interface FinanceSummary {
  revenue_today: number;
  revenue_week: number;
  revenue_month: number;
  transactions_today: number;
  transactions_week: number;
  avg_deal_size: number;
  best_sector: string;
  best_sector_revenue: number;
}

interface FinanceData {
  source: string;
  summary: FinanceSummary;
  daily_revenue: DailyRevenue[];
  top_sectors: SectorRevenue[];
  pricing_tiers: PricingTier[];
  recent_transactions: Transaction[];
}

// ── Components ────────────────────────────────────────────────────────────────

function KpiCard({ label, value, sub, color = "#6366f1" }: {
  label: string; value: string; sub?: string; color?: string;
}) {
  return (
    <div className="bg-white/3 border border-white/8 rounded-2xl p-5">
      <p className="text-xs text-gray-400 mb-2">{label}</p>
      <p className="text-3xl font-bold" style={{ color }}>{value}</p>
      {sub && <p className="text-xs text-gray-500 mt-1">{sub}</p>}
    </div>
  );
}

function RevenueBar({ day, maxRevenue }: { day: DailyRevenue; maxRevenue: number }) {
  const pct = maxRevenue > 0 ? (day.revenue / maxRevenue) * 100 : 0;
  const date = new Date(day.date).toLocaleDateString("fr-FR", { weekday: "short", day: "numeric" });
  return (
    <div className="flex flex-col items-center gap-1 flex-1">
      <p className="text-xs font-semibold text-white">{day.revenue.toLocaleString("fr-FR")}€</p>
      <div className="w-full bg-white/5 rounded-full overflow-hidden" style={{ height: 80 }}>
        <div
          className="w-full rounded-full bg-indigo-500 transition-all duration-700"
          style={{ height: `${pct}%`, marginTop: `${100 - pct}%` }}
        />
      </div>
      <p className="text-xs text-gray-500 text-center">{date}</p>
      <p className="text-xs text-gray-600">{day.transactions} deals</p>
    </div>
  );
}

const STATUS_STYLE: Record<string, { label: string; bg: string; text: string }> = {
  paid:     { label: "Payé",    bg: "bg-emerald-500/10", text: "text-emerald-400" },
  pending:  { label: "Attente", bg: "bg-amber-500/10",   text: "text-amber-400"   },
  refunded: { label: "Remboursé",bg: "bg-red-500/10",    text: "text-red-400"     },
};

function TransactionRow({ tx }: { tx: Transaction }) {
  const s = STATUS_STYLE[tx.status] || STATUS_STYLE.paid;
  const date = new Date(tx.date).toLocaleDateString("fr-FR", {
    day: "numeric", month: "short", hour: "2-digit", minute: "2-digit",
  });
  return (
    <div className="flex items-center gap-3 px-4 py-3 border-b border-white/5 last:border-0 hover:bg-white/3 transition-colors">
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-white truncate">{tx.company}</p>
        <p className="text-xs text-gray-500">{tx.sector}</p>
      </div>
      <span className="text-xs text-gray-500 font-mono shrink-0">{date}</span>
      <span className={`text-xs px-2 py-0.5 rounded-full ${s.bg} ${s.text} shrink-0`}>{s.label}</span>
      <span className="text-xs text-gray-500 shrink-0 font-mono">Agent {tx.agent}</span>
      <span className={`text-sm font-bold shrink-0 w-16 text-right ${
        tx.status === "refunded" ? "text-red-400 line-through" : "text-white"
      }`}>
        {tx.amount}€
      </span>
    </div>
  );
}

// ── Page ─────────────────────────────────────────────────────────────────────

export default function FinancePage() {
  const [data, setData] = useState<FinanceData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/finance")
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-400 text-sm animate-pulse">Chargement du rapport financier…</div>
      </div>
    );
  }

  if (!data) return null;

  const { summary, daily_revenue, top_sectors, pricing_tiers, recent_transactions } = data;
  const maxRevenue = Math.max(...daily_revenue.map((d) => d.revenue), 1);
  const totalPricingRevenue = pricing_tiers.reduce((s, t) => s + t.revenue, 0);

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white p-6 space-y-6">

      {/* Header */}
      <div className="flex items-center gap-3">
        <span className="text-2xl">💰</span>
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold">Finance & Revenus</h1>
            <span className={`text-xs px-2.5 py-1 rounded-full border font-medium ${
              data.source === "live"
                ? "text-emerald-400 bg-emerald-400/10 border-emerald-400/20"
                : "text-amber-400 bg-amber-400/10 border-amber-400/20"
            }`}>
              {data.source === "live" ? "● Live" : "◎ Demo"}
            </span>
          </div>
          <p className="text-sm text-gray-400">Division 5 — Agent 5.0 Finance Manager</p>
        </div>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <KpiCard
          label="CA aujourd'hui"
          value={`${summary.revenue_today.toLocaleString("fr-FR")}€`}
          sub={`${summary.transactions_today} transactions`}
          color="#10b981"
        />
        <KpiCard
          label="CA cette semaine"
          value={`${summary.revenue_week.toLocaleString("fr-FR")}€`}
          sub={`${summary.transactions_week} deals`}
          color="#6366f1"
        />
        <KpiCard
          label="CA ce mois"
          value={`${summary.revenue_month.toLocaleString("fr-FR")}€`}
          color="#8b5cf6"
        />
        <KpiCard
          label="Panier moyen"
          value={`${summary.avg_deal_size}€`}
          sub={`Meilleur : ${summary.best_sector}`}
          color="#f59e0b"
        />
      </div>

      {/* Revenue bar chart */}
      <div className="bg-white/3 border border-white/8 rounded-2xl p-5">
        <p className="text-base font-semibold mb-4">Revenus des 7 derniers jours</p>
        <div className="flex gap-2 items-end h-28">
          {daily_revenue.map((day) => (
            <RevenueBar key={day.date} day={day} maxRevenue={maxRevenue} />
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

        {/* Top sectors */}
        <div className="bg-white/3 border border-white/8 rounded-2xl p-5">
          <p className="text-base font-semibold mb-4">Top secteurs</p>
          <div className="space-y-3">
            {top_sectors.map((s, i) => {
              const maxSectorRev = Math.max(...top_sectors.map((x) => x.revenue));
              const pct = (s.revenue / maxSectorRev) * 100;
              return (
                <div key={s.sector}>
                  <div className="flex items-center justify-between text-sm mb-1">
                    <span className="text-gray-300">{s.sector}</span>
                    <div className="flex items-center gap-3">
                      <span className="text-gray-500 text-xs">{s.deals} deals · moy. {s.avg}€</span>
                      <span className="font-bold text-white">{s.revenue.toLocaleString("fr-FR")}€</span>
                    </div>
                  </div>
                  <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-700"
                      style={{
                        width: `${pct}%`,
                        backgroundColor: i === 0 ? "#10b981" : i === 1 ? "#6366f1" : "#8b5cf6",
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Pricing tiers */}
        <div className="bg-white/3 border border-white/8 rounded-2xl p-5">
          <p className="text-base font-semibold mb-4">Grille tarifaire</p>
          <div className="space-y-2">
            {pricing_tiers.map((t) => {
              const share = totalPricingRevenue > 0 ? (t.revenue / totalPricingRevenue) * 100 : 0;
              return (
                <div key={t.tier} className="flex items-center gap-3 bg-white/3 rounded-xl px-4 py-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-0.5">
                      <span className="text-sm font-semibold text-white">{t.tier}</span>
                      <span className="text-xs text-gray-500">{t.description}</span>
                    </div>
                    <div className="h-1 bg-white/5 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-indigo-500 rounded-full"
                        style={{ width: `${share}%` }}
                      />
                    </div>
                  </div>
                  <div className="text-right shrink-0">
                    <p className="text-sm font-bold text-white">{t.price}€</p>
                    <p className="text-xs text-gray-500">{t.count} ventes</p>
                  </div>
                  <div className="text-right shrink-0 w-20">
                    <p className="text-sm font-semibold text-emerald-300">{t.revenue.toLocaleString("fr-FR")}€</p>
                    <p className="text-xs text-gray-500">{Math.round(share)}%</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

      </div>

      {/* Recent transactions */}
      <div className="bg-white/3 border border-white/8 rounded-2xl overflow-hidden">
        <div className="px-5 py-4 border-b border-white/8">
          <p className="text-base font-semibold">Transactions récentes</p>
        </div>
        <div>
          {recent_transactions.map((tx) => (
            <TransactionRow key={tx.id} tx={tx} />
          ))}
        </div>
      </div>

    </div>
  );
}
