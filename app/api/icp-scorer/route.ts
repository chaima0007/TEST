import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockCompanies = [
  {
    company_id: "co_001",
    company_name: "CloudScale SaaS",
    industry: "saas",
    company_size: "enterprise",
    employee_count: 1200,
    annual_revenue_eur: 24000000,
    growth_stage: "fast_growth",
    icp_score: 91.4,
    icp_tier: "perfect",
    firmographic_score: 88.5,
    intent_score: 92.0,
    strategic_score: 95.0,
    risk_penalty: 0,
    outreach_recommendation: "prioritize",
    estimated_deal_size_eur: 48000,
    priority_rank: 1,
    fit_signals: [
      "Lead entrant — forte intention d'achat",
      "Point de douleur aligné avec notre proposition de valeur",
      "Budget confirmé — décision d'achat imminente",
      "Décideur accessible — cycle de vente raccourci",
      "Timeline de décision favorable (<6 mois)",
      "Financement récent — budget disponible",
    ],
    risk_signals: [],
  },
  {
    company_id: "co_002",
    company_name: "FinTech Ventures",
    industry: "fintech",
    company_size: "mid_market",
    employee_count: 320,
    annual_revenue_eur: 8000000,
    growth_stage: "hyper_growth",
    icp_score: 84.2,
    icp_tier: "strong",
    firmographic_score: 82.1,
    intent_score: 78.0,
    strategic_score: 80.0,
    risk_penalty: 0,
    outreach_recommendation: "prioritize",
    estimated_deal_size_eur: 28000,
    priority_rank: 2,
    fit_signals: [
      "Point de douleur aligné avec notre proposition de valeur",
      "Recrutement commercial actif — en croissance",
      "Utilise un CRM — culture data-driven",
      "Participant à un événement — engagement prouvé",
    ],
    risk_signals: [],
  },
  {
    company_id: "co_003",
    company_name: "MarTech Solutions",
    industry: "martech",
    company_size: "smb",
    employee_count: 85,
    annual_revenue_eur: 2400000,
    growth_stage: "fast_growth",
    icp_score: 78.8,
    icp_tier: "strong",
    firmographic_score: 76.4,
    intent_score: 75.0,
    strategic_score: 70.0,
    risk_penalty: 0,
    outreach_recommendation: "prioritize",
    estimated_deal_size_eur: 14000,
    priority_rank: 3,
    fit_signals: [
      "Engagement avec notre contenu — intérêt démontré",
      "Financement récent — budget disponible",
      "Utilise un CRM — culture data-driven",
      "Client concurrent — opportunité de switcher",
    ],
    risk_signals: [],
  },
  {
    company_id: "co_004",
    company_name: "EcomBoost",
    industry: "ecommerce",
    company_size: "mid_market",
    employee_count: 450,
    annual_revenue_eur: 12000000,
    growth_stage: "moderate_growth",
    icp_score: 61.5,
    icp_tier: "moderate",
    firmographic_score: 64.2,
    intent_score: 55.0,
    strategic_score: 60.0,
    risk_penalty: 10,
    outreach_recommendation: "qualify",
    estimated_deal_size_eur: 18000,
    priority_rank: 4,
    fit_signals: [
      "Point de douleur aligné avec notre proposition de valeur",
      "Utilise un CRM — culture data-driven",
    ],
    risk_signals: ["Sensibilité prix élevée — négociation complexe"],
  },
  {
    company_id: "co_005",
    company_name: "HealthCare Digital",
    industry: "healthtech",
    company_size: "enterprise",
    employee_count: 2800,
    annual_revenue_eur: 45000000,
    growth_stage: "stable",
    icp_score: 57.3,
    icp_tier: "moderate",
    firmographic_score: 62.8,
    intent_score: 48.0,
    strategic_score: 55.0,
    risk_penalty: 23,
    outreach_recommendation: "qualify",
    estimated_deal_size_eur: 32000,
    priority_rank: 5,
    fit_signals: [
      "Décideur accessible — cycle de vente raccourci",
      "Participant à un événement — engagement prouvé",
    ],
    risk_signals: [
      "Industrie à fort taux de churn — risque de non-renouvellement",
      "Cycle de vente long — effort commercial important",
    ],
  },
  {
    company_id: "co_006",
    company_name: "LogiTrack",
    industry: "logistics",
    company_size: "smb",
    employee_count: 150,
    annual_revenue_eur: 3500000,
    growth_stage: "stable",
    icp_score: 42.6,
    icp_tier: "moderate",
    firmographic_score: 48.0,
    intent_score: 40.0,
    strategic_score: 35.0,
    risk_penalty: 8,
    outreach_recommendation: "qualify",
    estimated_deal_size_eur: 8000,
    priority_rank: 6,
    fit_signals: ["Utilise un CRM — culture data-driven"],
    risk_signals: ["Cycle de vente long — effort commercial important"],
  },
  {
    company_id: "co_007",
    company_name: "RetailOld Co",
    industry: "retail",
    company_size: "smb",
    employee_count: 60,
    annual_revenue_eur: 1200000,
    growth_stage: "declining",
    icp_score: 28.4,
    icp_tier: "weak",
    firmographic_score: 32.5,
    intent_score: 22.0,
    strategic_score: 15.0,
    risk_penalty: 25,
    outreach_recommendation: "deprioritize",
    estimated_deal_size_eur: 2000,
    priority_rank: 7,
    fit_signals: [],
    risk_signals: [
      "Industrie à fort taux de churn — risque de non-renouvellement",
      "Sensibilité prix élevée — négociation complexe",
    ],
  },
  {
    company_id: "co_008",
    company_name: "GovAgency",
    industry: "government",
    company_size: "large_enterprise",
    employee_count: 8000,
    annual_revenue_eur: 0,
    growth_stage: "stable",
    icp_score: 14.2,
    icp_tier: "disqualified",
    firmographic_score: 22.0,
    intent_score: 10.0,
    strategic_score: 5.0,
    risk_penalty: 30,
    outreach_recommendation: "reject",
    estimated_deal_size_eur: 500,
    priority_rank: 8,
    fit_signals: [],
    risk_signals: [
      "Profil hors ICP — ne pas prioriser les ressources",
      "Industrie à fort taux de churn — risque de non-renouvellement",
      "Sensibilité prix élevée — négociation complexe",
      "Cycle de vente long — effort commercial important",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const tier = searchParams.get("tier");
  const recommendation = searchParams.get("recommendation");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/icp-scorer`);
      if (tier) url.searchParams.set("tier", tier);
      if (recommendation) url.searchParams.set("recommendation", recommendation);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let companies = [...mockCompanies];
  if (tier) companies = companies.filter((c) => c.icp_tier === tier);
  if (recommendation) companies = companies.filter((c) => c.outreach_recommendation === recommendation);

  const tier_counts: Record<string, number> = {
    perfect: 0, strong: 0, moderate: 0, weak: 0, disqualified: 0,
  };
  const rec_counts: Record<string, number> = {};
  let total_score = 0;
  let total_pipeline = 0;

  for (const c of mockCompanies) {
    tier_counts[c.icp_tier] = (tier_counts[c.icp_tier] || 0) + 1;
    rec_counts[c.outreach_recommendation] = (rec_counts[c.outreach_recommendation] || 0) + 1;
    total_score += c.icp_score;
    if (c.outreach_recommendation === "prioritize") total_pipeline += c.estimated_deal_size_eur;
  }

  const n = mockCompanies.length;

  return NextResponse.json({
    companies,
    summary: {
      total: n,
      tier_counts,
      rec_counts,
      avg_icp_score: Math.round((total_score / n) * 10) / 10,
      total_pipeline_eur: total_pipeline,
    },
  });
}
