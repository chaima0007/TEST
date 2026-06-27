import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

// ── Mock data ─────────────────────────────────────────────────────────────────

const MOCK_FINANCE = {
  source: "mock",
  summary: {
    revenue_today: 2237,
    revenue_week: 14280,
    revenue_month: 58420,
    transactions_today: 7,
    transactions_week: 44,
    avg_deal_size: 319,
    best_sector: "Plomberie & Artisans",
    best_sector_revenue: 4920,
  },
  daily_revenue: [
    { date: "2026-06-11", revenue: 1840, transactions: 6 },
    { date: "2026-06-12", revenue: 2100, transactions: 7 },
    { date: "2026-06-13", revenue: 980,  transactions: 3 },
    { date: "2026-06-14", revenue: 2450, transactions: 8 },
    { date: "2026-06-15", revenue: 1680, transactions: 5 },
    { date: "2026-06-16", revenue: 2993, transactions: 9 },
    { date: "2026-06-17", revenue: 2237, transactions: 7 },
  ],
  top_sectors: [
    { sector: "Plomberie & Artisans", revenue: 12840, deals: 27, avg: 476 },
    { sector: "Restaurants & Hôtels", revenue: 9720,  deals: 24, avg: 405 },
    { sector: "Médical & Dentaire",   revenue: 8400,  deals: 14, avg: 600 },
    { sector: "Immobilier",           revenue: 7200,  deals: 12, avg: 600 },
    { sector: "Coiffure & Beauté",    revenue: 5040,  deals: 18, avg: 280 },
    { sector: "Auto & Garage",        revenue: 4680,  deals: 13, avg: 360 },
  ],
  pricing_tiers: [
    { tier: "Essentiel",    price: 149, count: 28, revenue: 4172,  description: "Site mobile optimisé" },
    { tier: "Performance",  price: 299, count: 22, revenue: 6578,  description: "+ SEO + rapport" },
    { tier: "Premium",      price: 490, count: 12, revenue: 5880,  description: "+ Maintenance 3 mois" },
    { tier: "Entreprise",   price: 890, count:  4, revenue: 3560,  description: "Solution sur mesure" },
  ],
  recent_transactions: [
    { id: "txn_001", company: "Plomberie Leblanc",   sector: "Artisan", amount: 299, status: "paid",    agent: "5.1", date: "2026-06-17T14:23:00Z" },
    { id: "txn_002", company: "Resto Le Gaulois",    sector: "Restaurant", amount: 490, status: "paid", agent: "5.1", date: "2026-06-17T11:42:00Z" },
    { id: "txn_003", company: "Dr. Marchand",        sector: "Médical", amount: 490, status: "paid",    agent: "5.1", date: "2026-06-17T09:15:00Z" },
    { id: "txn_004", company: "Auto Garage Martin",  sector: "Auto", amount: 149, status: "paid",       agent: "5.2", date: "2026-06-17T08:03:00Z" },
    { id: "txn_005", company: "Coiff & Style",       sector: "Coiffure", amount: 149, status: "pending", agent: "5.3", date: "2026-06-16T17:55:00Z" },
    { id: "txn_006", company: "Immo Provence",       sector: "Immobilier", amount: 890, status: "paid", agent: "5.1", date: "2026-06-16T15:30:00Z" },
    { id: "txn_007", company: "Boulangerie Dupain",  sector: "Alimentation", amount: 149, status: "refunded", agent: "5.4", date: "2026-06-15T10:00:00Z" },
  ],
};

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/finance/report`, {
        next: { revalidate: 120 },
      });
      if (res.ok) {
        const data = await res.json();
        return NextResponse.json({ source: "live", ...data });
      }
    } catch {
      // fall through to mock
    }
  }
  return NextResponse.json(MOCK_FINANCE);
}
