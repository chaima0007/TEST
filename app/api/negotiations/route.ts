import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

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

function daysAgo(d: number) {
  const dt = new Date();
  dt.setDate(dt.getDate() - d);
  return dt.toISOString();
}

function buildMockData(): Data {
  const negotiations: Negotiation[] = [
    {
      negotiation_id: "neg_00001",
      prospect_id: "p001",
      company_name: "Plomberie Martin SARL",
      sector: "artisan",
      asking_price: 598.80,
      current_amount: 558.80,
      final_amount: 558.80,
      discount_pct: 6.7,
      total_concession_eur: 40.0,
      status: "agreed",
      rounds: 3,
      duration_days: 4.0,
      failure_reason: "",
      opened_at: daysAgo(22),
      closed_at: daysAgo(18),
      offers: [
        { round_number: 1, party: "prospect", amount: 499.00, concession_type: "price", note: "Trop cher pour nous", proposed_at: daysAgo(22) },
        { round_number: 2, party: "us",       amount: 578.80, concession_type: "price", note: "Effort de 20€",       proposed_at: daysAgo(21) },
        { round_number: 3, party: "prospect", amount: 558.80, concession_type: "price", note: "Accord sur ce prix",  proposed_at: daysAgo(20) },
      ],
    },
    {
      negotiation_id: "neg_00002",
      prospect_id: "p002",
      company_name: "Restaurant La Cigale",
      sector: "restaurant",
      asking_price: 958.80,
      current_amount: 878.80,
      final_amount: null,
      discount_pct: 8.3,
      total_concession_eur: 80.0,
      status: "in_progress",
      rounds: 2,
      duration_days: 5.0,
      failure_reason: "",
      opened_at: daysAgo(12),
      closed_at: null,
      offers: [
        { round_number: 1, party: "prospect", amount: 799.00, concession_type: "price",   note: "Budget serré",        proposed_at: daysAgo(12) },
        { round_number: 2, party: "us",       amount: 878.80, concession_type: "payment", note: "Paiement en 3× sans frais", proposed_at: daysAgo(10) },
      ],
    },
    {
      negotiation_id: "neg_00003",
      prospect_id: "p003",
      company_name: "Cabinet Dr. Lefèvre",
      sector: "médical",
      asking_price: 778.80,
      current_amount: 778.80,
      final_amount: 778.80,
      discount_pct: 0.0,
      total_concession_eur: 0.0,
      status: "agreed",
      rounds: 1,
      duration_days: 2.0,
      failure_reason: "",
      opened_at: daysAgo(10),
      closed_at: daysAgo(8),
      offers: [
        { round_number: 1, party: "prospect", amount: 778.80, concession_type: "price", note: "Prix OK", proposed_at: daysAgo(10) },
      ],
    },
    {
      negotiation_id: "neg_00004",
      prospect_id: "p004",
      company_name: "Garage Dupont",
      sector: "garage",
      asking_price: 598.80,
      current_amount: 598.80,
      final_amount: null,
      discount_pct: 0.0,
      total_concession_eur: 0.0,
      status: "opened",
      rounds: 0,
      duration_days: 1.0,
      failure_reason: "",
      opened_at: daysAgo(5),
      closed_at: null,
      offers: [],
    },
    {
      negotiation_id: "neg_00005",
      prospect_id: "p005",
      company_name: "Immo Prestige",
      sector: "immobilier",
      asking_price: 958.80,
      current_amount: 918.80,
      final_amount: 918.80,
      discount_pct: 4.2,
      total_concession_eur: 40.0,
      status: "agreed",
      rounds: 2,
      duration_days: 6.0,
      failure_reason: "",
      opened_at: daysAgo(28),
      closed_at: daysAgo(22),
      offers: [
        { round_number: 1, party: "prospect", amount: 880.00, concession_type: "price",    note: "Concurrent moins cher", proposed_at: daysAgo(28) },
        { round_number: 2, party: "us",       amount: 918.80, concession_type: "scope",    note: "On ajoute module reporting", proposed_at: daysAgo(26) },
      ],
    },
    {
      negotiation_id: "neg_00006",
      prospect_id: "p010",
      company_name: "BTP Expert SARL",
      sector: "artisan",
      asking_price: 598.80,
      current_amount: 598.80,
      final_amount: null,
      discount_pct: 0.0,
      total_concession_eur: 0.0,
      status: "failed",
      rounds: 2,
      duration_days: 7.0,
      failure_reason: "Prix non acceptable",
      opened_at: daysAgo(16),
      closed_at: daysAgo(9),
      offers: [
        { round_number: 1, party: "prospect", amount: 399.00, concession_type: "price", note: "On a pas ce budget", proposed_at: daysAgo(16) },
        { round_number: 2, party: "us",       amount: 549.00, concession_type: "price", note: "Effort max de notre côté", proposed_at: daysAgo(14) },
      ],
    },
    {
      negotiation_id: "neg_00007",
      prospect_id: "p011",
      company_name: "Notaire & Associés",
      sector: "juridique",
      asking_price: 1078.80,
      current_amount: 998.80,
      final_amount: null,
      discount_pct: 7.4,
      total_concession_eur: 80.0,
      status: "in_progress",
      rounds: 3,
      duration_days: 8.0,
      failure_reason: "",
      opened_at: daysAgo(10),
      closed_at: null,
      offers: [
        { round_number: 1, party: "prospect", amount: 900.00, concession_type: "price",    note: "Trop élevé vs concurrent",  proposed_at: daysAgo(10) },
        { round_number: 2, party: "us",       amount: 1028.80, concession_type: "scope",   note: "On retire module avancé",    proposed_at: daysAgo(8) },
        { round_number: 3, party: "prospect", amount: 998.80, concession_type: "timeline", note: "OK si démarrage immédiat",   proposed_at: daysAgo(6) },
      ],
    },
    {
      negotiation_id: "neg_00008",
      prospect_id: "p014",
      company_name: "Artisan Pro SARL",
      sector: "artisan",
      asking_price: 538.80,
      current_amount: 498.80,
      final_amount: null,
      discount_pct: 7.4,
      total_concession_eur: 40.0,
      status: "in_progress",
      rounds: 1,
      duration_days: 3.0,
      failure_reason: "",
      opened_at: daysAgo(15),
      closed_at: null,
      offers: [
        { round_number: 1, party: "prospect", amount: 498.80, concession_type: "price", note: "Limite haute acceptable", proposed_at: daysAgo(15) },
      ],
    },
    {
      negotiation_id: "neg_00009",
      prospect_id: "p008",
      company_name: "Salon Élite",
      sector: "beauté",
      asking_price: 358.80,
      current_amount: 358.80,
      final_amount: 358.80,
      discount_pct: 0.0,
      total_concession_eur: 0.0,
      status: "agreed",
      rounds: 0,
      duration_days: 1.0,
      failure_reason: "",
      opened_at: daysAgo(15),
      closed_at: daysAgo(14),
      offers: [],
    },
    {
      negotiation_id: "neg_00010",
      prospect_id: "p013",
      company_name: "Boulangerie Martin",
      sector: "restaurant",
      asking_price: 358.80,
      current_amount: 358.80,
      final_amount: null,
      discount_pct: 0.0,
      total_concession_eur: 0.0,
      status: "abandoned",
      rounds: 1,
      duration_days: 5.0,
      failure_reason: "Prospect injoignable",
      opened_at: daysAgo(11),
      closed_at: daysAgo(6),
      offers: [
        { round_number: 1, party: "us", amount: 358.80, concession_type: "price", note: "Offre initiale", proposed_at: daysAgo(11) },
      ],
    },
  ];

  const total = negotiations.length;
  const agreed = negotiations.filter(n => n.status === "agreed");
  const active = negotiations.filter(n => n.status === "opened" || n.status === "in_progress");
  const failedOrAbandoned = negotiations.filter(n => n.status === "failed" || n.status === "abandoned");
  const closed = [...agreed, ...failedOrAbandoned];
  const winRate = closed.length > 0 ? Math.round(agreed.length / closed.length * 1000) / 10 : 0;
  const avgDiscount = agreed.length > 0
    ? Math.round(agreed.reduce((s, n) => s + n.discount_pct, 0) / agreed.length * 10) / 10
    : 0;
  const avgRounds = total > 0
    ? Math.round(negotiations.reduce((s, n) => s + n.rounds, 0) / total * 10) / 10
    : 0;
  const closedWithDays = negotiations.filter(n => n.closed_at);
  const avgDuration = closedWithDays.length > 0
    ? Math.round(closedWithDays.reduce((s, n) => s + n.duration_days, 0) / closedWithDays.length * 10) / 10
    : 0;
  const totalAgreedEur = Math.round(agreed.reduce((s, n) => s + n.current_amount, 0) * 100) / 100;
  const totalConceded = Math.round(agreed.reduce((s, n) => s + n.total_concession_eur, 0) * 100) / 100;

  const summary: Summary = {
    total,
    active: active.length,
    agreed: agreed.length,
    failed_or_abandoned: failedOrAbandoned.length,
    win_rate_pct: winRate,
    avg_discount_pct: avgDiscount,
    avg_rounds: avgRounds,
    avg_duration_days: avgDuration,
    total_agreed_eur: totalAgreedEur,
    total_conceded_eur: totalConceded,
  };

  return { source: "mock", negotiations, summary };
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const [listRes, sumRes] = await Promise.all([
        fetch(`${SWARM_API_URL}/negotiations`, { next: { revalidate: 15 } }),
        fetch(`${SWARM_API_URL}/negotiations/summary`, { next: { revalidate: 15 } }),
      ]);
      if (listRes.ok && sumRes.ok) {
        return NextResponse.json({
          source: "live",
          negotiations: await listRes.json(),
          summary: await sumRes.json(),
        });
      }
    } catch { /* fall through */ }
  }
  return NextResponse.json(buildMockData());
}
