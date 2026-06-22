import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[retention] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

type ChurnRisk = "low" | "medium" | "high" | "critical";

interface CustomerSignals {
  customer_id: string;
  name: string;
  company: string;
  sector: string;
  days_since_last_login: number;
  open_support_tickets: number;
  contract_months_remaining: number;
  engagement_trend: number;
  nps_score: number;
  avg_monthly_revenue_eur: number;
  months_as_customer: number;
}

interface RetentionProfile {
  signals: CustomerSignals;
  churn_score: number;
  churn_risk: ChurnRisk;
  ltv_eur: number;
  predicted_months_remaining: number;
  risk_factors: string[];
  retention_actions: string[];
  score_breakdown: {
    login_recency: number;
    support_tickets: number;
    contract_health: number;
    engagement_trend: number;
    nps_score: number;
  };
}

const RETENTION_ACTIONS: Record<ChurnRisk, string[]> = {
  critical: ["Appel de rétention immédiat — directeur de compte", "Proposer une remise ou une extension de contrat", "Escalader en interne — risque de perte imminent"],
  high:     ["Planifier un QBR (Quarterly Business Review)", "Envoyer un rapport de valeur personnalisé", "Identifier le décisionnaire et le recontacter"],
  medium:   ["Email de check-in mensuel automatique", "Proposer une session d'onboarding avancé", "Partager des cas d'usage similaires à leur secteur"],
  low:      ["Identifier les opportunités d'upsell", "Inviter au programme ambassadeur", "Recueillir un témoignage ou une étude de cas"],
};

const MOCK_CUSTOMERS: CustomerSignals[] = [
  { customer_id: "cu001", name: "Marc Dupont",      company: "Cabinet Dupont",       sector: "avocat",      days_since_last_login: 1,  open_support_tickets: 0, contract_months_remaining: 18, engagement_trend: 0.8,  nps_score: 70,  avg_monthly_revenue_eur: 1290, months_as_customer: 24 },
  { customer_id: "cu002", name: "Lucie Martin",     company: "Plomberie Martin",     sector: "artisan",     days_since_last_login: 22, open_support_tickets: 3, contract_months_remaining: 2,  engagement_trend: -0.6, nps_score: -25, avg_monthly_revenue_eur: 380,  months_as_customer: 6  },
  { customer_id: "cu003", name: "Thomas Léger",     company: "Cabinet Léger",        sector: "comptable",   days_since_last_login: 5,  open_support_tickets: 1, contract_months_remaining: 8,  engagement_trend: 0.3,  nps_score: 30,  avg_monthly_revenue_eur: 960,  months_as_customer: 18 },
  { customer_id: "cu004", name: "Sophie Moreau",    company: "Dr. Moreau",           sector: "médecin",     days_since_last_login: 18, open_support_tickets: 2, contract_months_remaining: 1,  engagement_trend: -0.4, nps_score: -10, avg_monthly_revenue_eur: 540,  months_as_customer: 9  },
  { customer_id: "cu005", name: "Antoine Zinc",     company: "Brasserie Le Zinc",    sector: "restaurant",  days_since_last_login: 40, open_support_tickets: 5, contract_months_remaining: 0,  engagement_trend: -0.9, nps_score: -60, avg_monthly_revenue_eur: 420,  months_as_customer: 4  },
  { customer_id: "cu006", name: "Claire Blanc",     company: "Étude Notariale",      sector: "notaire",     days_since_last_login: 2,  open_support_tickets: 0, contract_months_remaining: 24, engagement_trend: 0.9,  nps_score: 80,  avg_monthly_revenue_eur: 1140, months_as_customer: 36 },
  { customer_id: "cu007", name: "Romain Horizon",   company: "Agence Horizon",       sector: "immobilier",  days_since_last_login: 10, open_support_tickets: 1, contract_months_remaining: 5,  engagement_trend: 0.1,  nps_score: 15,  avg_monthly_revenue_eur: 720,  months_as_customer: 12 },
  { customer_id: "cu008", name: "Isabelle Sas",     company: "PME Solutions SAS",    sector: "pme",         days_since_last_login: 3,  open_support_tickets: 0, contract_months_remaining: 12, engagement_trend: 0.6,  nps_score: 50,  avg_monthly_revenue_eur: 890,  months_as_customer: 30 },
  { customer_id: "cu009", name: "Éric Durand",      company: "Électricité Durand",   sector: "artisan",     days_since_last_login: 55, open_support_tickets: 4, contract_months_remaining: 1,  engagement_trend: -0.8, nps_score: -50, avg_monthly_revenue_eur: 290,  months_as_customer: 3  },
  { customer_id: "cu010", name: "Nathalie Vue",     company: "Hôtel Belle Vue",      sector: "hôtel",       days_since_last_login: 8,  open_support_tickets: 0, contract_months_remaining: 6,  engagement_trend: 0.2,  nps_score: 20,  avg_monthly_revenue_eur: 680,  months_as_customer: 15 },
];

function loginRisk(days: number): number {
  if (days <= 3) return 0;
  if (days <= 14) return (days - 3) * 5;
  return Math.min(100, 55 + (days - 14) * 2.5);
}

function ticketRisk(tickets: number): number { return Math.min(100, tickets * 25); }

function contractRisk(months: number): number {
  if (months >= 12) return 0;
  if (months >= 6)  return 20;
  if (months >= 3)  return 50;
  if (months >= 1)  return 75;
  return 100;
}

function engagementRisk(trend: number): number {
  const c = Math.max(-1, Math.min(1, trend));
  return (1 - c) * 50;
}

function npsRisk(nps: number): number {
  const c = Math.max(-100, Math.min(100, nps));
  return (100 - c) / 2;
}

function computeBreakdown(s: CustomerSignals) {
  return {
    login_recency:     loginRisk(s.days_since_last_login),
    support_tickets:   ticketRisk(s.open_support_tickets),
    contract_health:   contractRisk(s.contract_months_remaining),
    engagement_trend:  engagementRisk(s.engagement_trend),
    nps_score:         npsRisk(s.nps_score),
  };
}

function computeChurnScore(b: ReturnType<typeof computeBreakdown>): number {
  const raw = b.login_recency * 0.25 + b.support_tickets * 0.20 +
              b.contract_health * 0.20 + b.engagement_trend * 0.20 + b.nps_score * 0.15;
  return Math.round(Math.max(0, Math.min(100, raw)) * 100) / 100;
}

function classifyChurn(score: number): ChurnRisk {
  if (score >= 75) return "critical";
  if (score >= 55) return "high";
  if (score >= 35) return "medium";
  return "low";
}

function predictedMonths(churnScore: number, contractMonths: number): number {
  const survival = Math.max(0, 1 - churnScore / 100);
  return Math.max(0, Math.floor(contractMonths * survival + 12 * survival));
}

function upsellMultiplier(trend: number, nps: number): number {
  if (trend > 0.5 && nps > 30) return 1.30;
  if (trend > 0 && nps >= 0) return 1.10;
  if (trend < -0.3 || nps < -20) return 0.80;
  return 1.0;
}

function computeLtv(s: CustomerSignals, months: number): number {
  return Math.round(s.avg_monthly_revenue_eur * months * upsellMultiplier(s.engagement_trend, s.nps_score) * 100) / 100;
}

function computeRiskFactors(s: CustomerSignals, b: ReturnType<typeof computeBreakdown>): string[] {
  const factors: string[] = [];
  if (b.login_recency > 50) factors.push(`Inactif depuis ${s.days_since_last_login} jours`);
  if (s.open_support_tickets >= 3) factors.push(`${s.open_support_tickets} tickets support ouverts`);
  if (s.contract_months_remaining <= 3) factors.push(`Contrat expire dans ${s.contract_months_remaining} mois`);
  if (s.engagement_trend < -0.3) factors.push("Tendance d'engagement en déclin");
  if (s.nps_score < 0) factors.push(`NPS négatif (${s.nps_score})`);
  return factors;
}

function analyzeCustomer(s: CustomerSignals): RetentionProfile {
  const breakdown = computeBreakdown(s);
  const churn_score = computeChurnScore(breakdown);
  const churn_risk = classifyChurn(churn_score);
  const predicted = predictedMonths(churn_score, s.contract_months_remaining);
  return {
    signals: s,
    churn_score,
    churn_risk,
    ltv_eur: computeLtv(s, predicted),
    predicted_months_remaining: predicted,
    risk_factors: computeRiskFactors(s, breakdown),
    retention_actions: RETENTION_ACTIONS[churn_risk],
    score_breakdown: breakdown,
  };
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/retention`, { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch { /* fall through */ }
  }

  const customers = MOCK_CUSTOMERS.map(analyzeCustomer).sort((a, b) => b.churn_score - a.churn_score);

  const riskCounts = { critical: 0, high: 0, medium: 0, low: 0 };
  let totalLtv = 0;
  let totalMrr = 0;
  let atRiskRevenue = 0;

  for (const c of customers) {
    riskCounts[c.churn_risk]++;
    totalLtv += c.ltv_eur;
    totalMrr += c.signals.avg_monthly_revenue_eur;
    if (c.churn_risk === "high" || c.churn_risk === "critical") {
      atRiskRevenue += c.signals.avg_monthly_revenue_eur;
    }
  }

  const avgChurn = customers.reduce((s, c) => s + c.churn_score, 0) / customers.length;

  const expiringCount = customers.filter((c) => c.signals.contract_months_remaining <= 3).length;

  return sealResponse(NextResponse.json({
    customers,
    summary: {
      total: customers.length,
      risk_counts: riskCounts,
      avg_churn_score: Math.round(avgChurn * 100) / 100,
      total_ltv_eur: Math.round(totalLtv),
      total_monthly_revenue_eur: Math.round(totalMrr),
      at_risk_revenue_eur: Math.round(atRiskRevenue),
      expiring_soon_count: expiringCount,
    },
  }));
}
