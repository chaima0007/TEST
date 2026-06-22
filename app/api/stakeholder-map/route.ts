import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[stakeholder-map] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockStakeholders = [
  {
    stakeholder_id: "sh_001",
    deal_id: "deal_001",
    account_id: "acc_001",
    account_name: "TechCorp SA",
    name: "Philippe Renaud",
    title: "Directeur Financier (CFO)",
    influence_score: 95.0,
    engagement_level: "strong",
    relationship_status: "sponsor",
    stakeholder_role: "economic_buyer",
    coverage_risk: "covered",
    engagement_gap: 0.0,
    is_at_risk: false,
    priority_rank: 5,
    recommended_action:
      "Maintenir l'engagement — briefings réguliers et updates exécutifs",
    risk_factors: [],
    strengths: [
      "Champion identifié — défenseur interne de la solution",
      "Alignement confirmé — a exprimé sa préférence pour notre solution",
      "Engagement fort — 5 réunions, activité régulière",
      "Sponsor actif — soutien exécutif acquis",
      "Profil gagnant — 4 victoire(s) avec ce type de persona",
      "Sentiment très positif — forte affinité avec la solution",
    ],
    recommended_approach:
      "Focus ROI et valeur stratégique — présenter le business case chiffré",
  },
  {
    stakeholder_id: "sh_002",
    deal_id: "deal_001",
    account_id: "acc_001",
    account_name: "TechCorp SA",
    name: "Amandine Leroux",
    title: "Responsable IT",
    influence_score: 53.0,
    engagement_level: "strong",
    relationship_status: "ally",
    stakeholder_role: "champion",
    coverage_risk: "covered",
    engagement_gap: 0.0,
    is_at_risk: false,
    priority_rank: 6,
    recommended_action:
      "Activer comme ambassadeur — fournir les outils de conviction",
    risk_factors: [],
    strengths: [
      "Champion identifié — défenseur interne de la solution",
      "Alignement confirmé — a exprimé sa préférence pour notre solution",
      "Engagement fort — 4 réunions, activité régulière",
      "Profil gagnant — 2 victoire(s) avec ce type de persona",
    ],
    recommended_approach:
      "Co-créer la vision — fournir des arguments et outils pour vendre en interne",
  },
  {
    stakeholder_id: "sh_003",
    deal_id: "deal_002",
    account_id: "acc_002",
    account_name: "GlobalFinance SARL",
    name: "Bertrand Dupuis",
    title: "CEO",
    influence_score: 100.0,
    engagement_level: "none",
    relationship_status: "neutral",
    stakeholder_role: "economic_buyer",
    coverage_risk: "critical",
    engagement_gap: 80.0,
    is_at_risk: true,
    priority_rank: 1,
    recommended_action:
      "Escalade exécutive urgente — aligner sur la valeur business",
    risk_factors: [
      "Stakeholder clé non engagé — couverture critique",
      "Décideur budget faiblement engagé — deal en risque",
      "Aucune réponse aux emails — revoir l'approche de communication",
    ],
    strengths: [],
    recommended_approach:
      "Focus ROI et valeur stratégique — présenter le business case chiffré",
  },
  {
    stakeholder_id: "sh_004",
    deal_id: "deal_002",
    account_id: "acc_002",
    account_name: "GlobalFinance SARL",
    name: "Caroline Morin",
    title: "DSI",
    influence_score: 73.0,
    engagement_level: "hostile",
    relationship_status: "opponent",
    stakeholder_role: "blocker",
    coverage_risk: "critical",
    engagement_gap: 58.4,
    is_at_risk: true,
    priority_rank: 2,
    recommended_action:
      "Neutraliser — identifier les préoccupations et adresser les objections",
    risk_factors: [
      "Blocage actif identifié — peut stopper la décision",
      "Silence prolongé (42j) — relation en danger",
      "Sentiment très négatif — risque d'opposition",
      "Stakeholder clé non engagé — couverture critique",
    ],
    strengths: [],
    recommended_approach:
      "Discovery des objections — comprendre les craintes et proposer des garanties",
  },
  {
    stakeholder_id: "sh_005",
    deal_id: "deal_003",
    account_id: "acc_003",
    account_name: "MediaGroup SAS",
    name: "Sylvie Tremblay",
    title: "VP Marketing",
    influence_score: 65.0,
    engagement_level: "moderate",
    relationship_status: "ally",
    stakeholder_role: "influencer",
    coverage_risk: "partial",
    engagement_gap: 22.75,
    is_at_risk: false,
    priority_rank: 3,
    recommended_action:
      "Renforcer l'alliance — impliquer dans le processus de décision",
    risk_factors: [],
    strengths: [
      "Alignement confirmé — a exprimé sa préférence pour notre solution",
      "Profil gagnant — 1 victoire(s) avec ce type de persona",
    ],
    recommended_approach:
      "Capitaliser sur l'engagement — accélérer vers la décision",
  },
  {
    stakeholder_id: "sh_006",
    deal_id: "deal_003",
    account_id: "acc_003",
    account_name: "MediaGroup SAS",
    name: "Marc Fontaine",
    title: "Responsable Technique",
    influence_score: 53.0,
    engagement_level: "moderate",
    relationship_status: "neutral",
    stakeholder_role: "technical_buyer",
    coverage_risk: "at_risk",
    engagement_gap: 18.55,
    is_at_risk: true,
    priority_rank: 4,
    recommended_action:
      "Adresser les doutes — démonstration de valeur et références clients",
    risk_factors: [
      "Silence prolongé (25j) — relation en danger",
    ],
    strengths: [
      "Profil gagnant — 1 victoire(s) avec ce type de persona",
    ],
    recommended_approach:
      "Démonstration technique approfondie — répondre aux critères d'évaluation",
  },
  {
    stakeholder_id: "sh_007",
    deal_id: "deal_004",
    account_id: "acc_004",
    account_name: "RetailChain Nord",
    name: "Émile Garnier",
    title: "Directeur Général Adjoint",
    influence_score: 80.0,
    engagement_level: "weak",
    relationship_status: "skeptic",
    stakeholder_role: "economic_buyer",
    coverage_risk: "at_risk",
    engagement_gap: 44.0,
    is_at_risk: true,
    priority_rank: 3,
    recommended_action:
      "Escalade exécutive urgente — aligner sur la valeur business",
    risk_factors: [
      "Décideur budget faiblement engagé — deal en risque",
    ],
    strengths: [],
    recommended_approach:
      "Focus ROI et valeur stratégique — présenter le business case chiffré",
  },
  {
    stakeholder_id: "sh_008",
    deal_id: "deal_004",
    account_id: "acc_004",
    account_name: "RetailChain Nord",
    name: "Isabelle Caron",
    title: "Analyste Opérations",
    influence_score: 10.0,
    engagement_level: "strong",
    relationship_status: "ally",
    stakeholder_role: "end_user",
    coverage_risk: "covered",
    engagement_gap: 0.0,
    is_at_risk: false,
    priority_rank: 8,
    recommended_action:
      "Maintenir le contact régulier et partager les updates pertinentes",
    risk_factors: [],
    strengths: [
      "Alignement confirmé — a exprimé sa préférence pour notre solution",
      "Engagement fort — 3 réunions, activité régulière",
      "Sentiment très positif — forte affinité avec la solution",
    ],
    recommended_approach:
      "Approche consultative — comprendre les enjeux et proposer de la valeur",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const role       = searchParams.get("role");
  const engagement = searchParams.get("engagement");
  const risk       = searchParams.get("risk");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/stakeholder-map`);
      if (role)       url.searchParams.set("role", role);
      if (engagement) url.searchParams.set("engagement", engagement);
      if (risk)       url.searchParams.set("risk", risk);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let stakeholders = [...mockStakeholders];
  if (role)       stakeholders = stakeholders.filter((s) => s.stakeholder_role === role);
  if (engagement) stakeholders = stakeholders.filter((s) => s.engagement_level === engagement);
  if (risk)       stakeholders = stakeholders.filter((s) => s.coverage_risk === risk);

  const role_counts:       Record<string, number> = {};
  const engagement_counts: Record<string, number> = {};
  const relationship_counts: Record<string, number> = {};
  const risk_counts:       Record<string, number> = {};
  let total_influence = 0, total_gap = 0;

  for (const s of mockStakeholders) {
    role_counts[s.stakeholder_role]           = (role_counts[s.stakeholder_role] || 0) + 1;
    engagement_counts[s.engagement_level]     = (engagement_counts[s.engagement_level] || 0) + 1;
    relationship_counts[s.relationship_status] = (relationship_counts[s.relationship_status] || 0) + 1;
    risk_counts[s.coverage_risk]              = (risk_counts[s.coverage_risk] || 0) + 1;
    total_influence += s.influence_score;
    total_gap       += s.engagement_gap;
  }

  const n = mockStakeholders.length;

  return sealResponse(NextResponse.json({
    stakeholders,
    summary: {
      total: n,
      role_counts,
      engagement_counts,
      relationship_counts,
      risk_counts,
      avg_influence_score:   Math.round((total_influence / n) * 10) / 10,
      avg_engagement_gap:    Math.round((total_gap / n) * 10) / 10,
      champions_count:       mockStakeholders.filter((s) => s.stakeholder_role === "champion").length,
      economic_buyers_count: mockStakeholders.filter((s) => s.stakeholder_role === "economic_buyer").length,
      at_risk_count:         mockStakeholders.filter((s) => s.is_at_risk).length,
      covered_count:         mockStakeholders.filter((s) => s.coverage_risk === "covered").length,
      critical_stakeholders_count: mockStakeholders.filter((s) => s.coverage_risk === "critical").length,
    },
  }));
}
