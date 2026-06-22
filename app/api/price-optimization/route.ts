import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[price-optimization] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "po_001",
    account_name: "CloudScale Technologies",
    segment: "enterprise",
    list_price_eur: 240000,
    proposed_price_eur: 216000,
    optimized_price_eur: 204000,
    recommended_discount_pct: 15.0,
    max_acceptable_discount_pct: 45.0,
    pricing_strategy: "value_based",
    discount_risk: "low",
    pricing_action: "hold",
    revenue_impact: "neutral",
    price_optimization_score: 88.0,
    pricing_rationale: [
      "Stratégie value based recommandée — remise optimale : 15.0% vs remise actuelle : 10.0%",
      "Engagement pluriannuel : bonus remise de +4% accordé",
      "ICP fit élevé : valeur perçue forte — défendre le prix liste",
    ],
    negotiation_guardrails: [
      "Ne jamais descendre en dessous de 45% de remise sans approbation manager",
      "Remise cible recommandée : 15.0% — toute remise supérieure nécessite une validation",
      "Toute remise > 15% doit être accompagnée d'un engagement (volume, durée ou expansion)",
    ],
    value_anchors: [
      "ROI documenté clients similaires — présenter avant toute discussion prix",
      "Potentiel d'expansion élevé (85%) — valeur lifetime client multiplied",
      "Engagement multi-annuel : coût total inférieur avec visibilité tarifaire garantie",
      "Coût de migration concurrente — switching cost à quantifier et présenter",
      "Support & SLA premium inclus — valeur cachée à rendre visible",
    ],
    bundle_options: [
      "Bundle 2 ans : remise -5% + formation offerte + SLA premium",
      "Bundle 3 ans : remise -8% + CSM dédié + QBR trimestriels",
      "Bundle expansion : licences additionnelles à -10% incluses dans le deal initial",
      "Bundle enterprise : API + SSO + audit de sécurité inclus sans surcoût",
      "Bundle success : onboarding accéléré + certification utilisateurs inclus",
    ],
  },
  {
    deal_id: "po_002",
    account_name: "DataVault Partners",
    segment: "enterprise",
    list_price_eur: 180000,
    proposed_price_eur: 166500,
    optimized_price_eur: 162000,
    recommended_discount_pct: 10.0,
    max_acceptable_discount_pct: 35.0,
    pricing_strategy: "premium",
    discount_risk: "low",
    pricing_action: "increase",
    revenue_impact: "positive",
    price_optimization_score: 82.0,
    pricing_rationale: [
      "Stratégie premium recommandée — remise optimale : 10.0% vs remise actuelle : 7.5%",
      "ICP fit élevé : valeur perçue forte — défendre le prix liste",
    ],
    negotiation_guardrails: [
      "Ne jamais descendre en dessous de 35% de remise sans approbation manager",
      "Remise cible recommandée : 10.0% — toute remise supérieure nécessite une validation",
      "Toute remise > 15% doit être accompagnée d'un engagement",
    ],
    value_anchors: [
      "ROI documenté clients similaires — présenter avant toute discussion prix",
      "Coût de migration concurrente — switching cost à quantifier et présenter",
      "Support & SLA premium inclus — valeur cachée à rendre visible",
    ],
    bundle_options: [
      "Bundle enterprise : API + SSO + audit de sécurité inclus sans surcoût",
      "Bundle success : onboarding accéléré + certification utilisateurs inclus",
    ],
  },
  {
    deal_id: "po_003",
    account_name: "NexaRetail Group",
    segment: "enterprise",
    list_price_eur: 150000,
    proposed_price_eur: 127500,
    optimized_price_eur: 130500,
    recommended_discount_pct: 13.0,
    max_acceptable_discount_pct: 40.0,
    pricing_strategy: "competitive",
    discount_risk: "low",
    pricing_action: "bundle",
    revenue_impact: "positive",
    price_optimization_score: 74.0,
    pricing_rationale: [
      "Stratégie competitive recommandée — remise optimale : 13.0% vs remise actuelle : 15.0%",
      "Pression concurrentielle détectée — remise compétitive justifiée",
      "Engagement pluriannuel : bonus remise de +4% accordé",
    ],
    negotiation_guardrails: [
      "Ne jamais descendre en dessous de 40% de remise sans approbation manager",
      "Remise cible recommandée : 13.0% — toute remise supérieure nécessite une validation",
      "Toute remise > 15% doit être accompagnée d'un engagement",
    ],
    value_anchors: [
      "ROI documenté clients similaires — présenter avant toute discussion prix",
      "Potentiel d'expansion élevé (75%) — valeur lifetime client multiplied",
      "Engagement multi-annuel : coût total inférieur avec visibilité tarifaire garantie",
      "Coût de migration concurrente — switching cost à quantifier et présenter",
      "Support & SLA premium inclus — valeur cachée à rendre visible",
    ],
    bundle_options: [
      "Bundle 2 ans : remise -5% + formation offerte + SLA premium",
      "Bundle 3 ans : remise -8% + CSM dédié + QBR trimestriels",
      "Bundle expansion : licences additionnelles à -10% incluses dans le deal initial",
      "Bundle enterprise : API + SSO + audit de sécurité inclus sans surcoût",
      "Bundle success : onboarding accéléré + certification utilisateurs inclus",
    ],
  },
  {
    deal_id: "po_004",
    account_name: "HealthBridge Systems",
    segment: "mid_market",
    list_price_eur: 96000,
    proposed_price_eur: 80640,
    optimized_price_eur: 85440,
    recommended_discount_pct: 11.0,
    max_acceptable_discount_pct: 33.0,
    pricing_strategy: "value_based",
    discount_risk: "medium",
    pricing_action: "hold",
    revenue_impact: "positive",
    price_optimization_score: 68.0,
    pricing_rationale: [
      "Stratégie value based recommandée — remise optimale : 11.0% vs remise actuelle : 16.0%",
      "ICP fit élevé : valeur perçue forte — défendre le prix liste",
    ],
    negotiation_guardrails: [
      "Ne jamais descendre en dessous de 33% de remise sans approbation manager",
      "Remise cible recommandée : 11.0% — toute remise supérieure nécessite une validation",
      "Toute remise > 15% doit être accompagnée d'un engagement",
    ],
    value_anchors: [
      "ROI documenté clients similaires — présenter avant toute discussion prix",
      "Coût de migration concurrente — switching cost à quantifier et présenter",
      "Support & SLA premium inclus — valeur cachée à rendre visible",
    ],
    bundle_options: [
      "Bundle success : onboarding accéléré + certification utilisateurs inclus",
    ],
  },
  {
    deal_id: "po_005",
    account_name: "FinCore Solutions",
    segment: "mid_market",
    list_price_eur: 72000,
    proposed_price_eur: 57600,
    optimized_price_eur: 64800,
    recommended_discount_pct: 10.0,
    max_acceptable_discount_pct: 28.0,
    pricing_strategy: "competitive",
    discount_risk: "high",
    pricing_action: "bundle",
    revenue_impact: "positive",
    price_optimization_score: 54.0,
    pricing_rationale: [
      "Stratégie competitive recommandée — remise optimale : 10.0% vs remise actuelle : 20.0%",
      "Pression concurrentielle détectée — remise compétitive justifiée",
      "Fin de trimestre : bonus tactique de +2% pour accélérer le closing",
    ],
    negotiation_guardrails: [
      "Ne jamais descendre en dessous de 28% de remise sans approbation manager",
      "Remise cible recommandée : 10.0% — toute remise supérieure nécessite une validation",
      "Fin de trimestre : ne pas sacrifier la marge pour un deal qui peut attendre",
      "Toute remise > 15% doit être accompagnée d'un engagement",
    ],
    value_anchors: [
      "ROI documenté clients similaires — présenter avant toute discussion prix",
      "Potentiel d'expansion élevé (72%) — valeur lifetime client multiplied",
      "Coût de migration concurrente — switching cost à quantifier et présenter",
      "Support & SLA premium inclus — valeur cachée à rendre visible",
    ],
    bundle_options: [
      "Bundle expansion : licences additionnelles à -10% incluses dans le deal initial",
      "Bundle success : onboarding accéléré + certification utilisateurs inclus",
    ],
  },
  {
    deal_id: "po_006",
    account_name: "LogiFlux GmbH",
    segment: "mid_market",
    list_price_eur: 60000,
    proposed_price_eur: 42000,
    optimized_price_eur: 52800,
    recommended_discount_pct: 12.0,
    max_acceptable_discount_pct: 28.0,
    pricing_strategy: "penetration",
    discount_risk: "excessive",
    pricing_action: "restructure",
    revenue_impact: "positive",
    price_optimization_score: 36.0,
    pricing_rationale: [
      "Stratégie penetration recommandée — remise optimale : 12.0% vs remise actuelle : 30.0%",
      "Client fidèle (3+ ans) : remise fidélité de +2% incluse",
    ],
    negotiation_guardrails: [
      "Ne jamais descendre en dessous de 28% de remise sans approbation manager",
      "Remise cible recommandée : 12.0% — toute remise supérieure nécessite une validation",
      "Historique : remise précédente à 28.0% — attention à l'effet cliquet",
      "Toute remise > 15% doit être accompagnée d'un engagement",
    ],
    value_anchors: [
      "ROI documenté clients similaires — présenter avant toute discussion prix",
      "Coût de migration concurrente — switching cost à quantifier et présenter",
      "Support & SLA premium inclus — valeur cachée à rendre visible",
    ],
    bundle_options: [
      "Bundle success : onboarding accéléré + certification utilisateurs inclus",
    ],
  },
  {
    deal_id: "po_007",
    account_name: "EduSpark Ltd",
    segment: "smb",
    list_price_eur: 24000,
    proposed_price_eur: 19200,
    optimized_price_eur: 21600,
    recommended_discount_pct: 10.0,
    max_acceptable_discount_pct: 20.0,
    pricing_strategy: "penetration",
    discount_risk: "medium",
    pricing_action: "discount",
    revenue_impact: "positive",
    price_optimization_score: 45.0,
    pricing_rationale: [
      "Stratégie penetration recommandée — remise optimale : 10.0% vs remise actuelle : 20.0%",
    ],
    negotiation_guardrails: [
      "Ne jamais descendre en dessous de 20% de remise sans approbation manager",
      "Remise cible recommandée : 10.0% — toute remise supérieure nécessite une validation",
      "Toute remise > 15% doit être accompagnée d'un engagement",
    ],
    value_anchors: [
      "ROI documenté clients similaires — présenter avant toute discussion prix",
      "Coût de migration concurrente — switching cost à quantifier et présenter",
      "Support & SLA premium inclus — valeur cachée à rendre visible",
    ],
    bundle_options: [
      "Bundle success : onboarding accéléré + certification utilisateurs inclus",
    ],
  },
  {
    deal_id: "po_008",
    account_name: "PropLink AG",
    segment: "smb",
    list_price_eur: 12000,
    proposed_price_eur: 9600,
    optimized_price_eur: 10800,
    recommended_discount_pct: 10.0,
    max_acceptable_discount_pct: 20.0,
    pricing_strategy: "penetration",
    discount_risk: "high",
    pricing_action: "restructure",
    revenue_impact: "positive",
    price_optimization_score: 28.0,
    pricing_rationale: [
      "Stratégie penetration recommandée — remise optimale : 10.0% vs remise actuelle : 20.0%",
      "Pression concurrentielle détectée — remise compétitive justifiée",
    ],
    negotiation_guardrails: [
      "Ne jamais descendre en dessous de 20% de remise sans approbation manager",
      "Remise cible recommandée : 10.0% — toute remise supérieure nécessite une validation",
      "Toute remise > 15% doit être accompagnée d'un engagement",
    ],
    value_anchors: [
      "ROI documenté clients similaires — présenter avant toute discussion prix",
      "Coût de migration concurrente — switching cost à quantifier et présenter",
      "Support & SLA premium inclus — valeur cachée à rendre visible",
    ],
    bundle_options: [
      "Bundle success : onboarding accéléré + certification utilisateurs inclus",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk = searchParams.get("risk");
  const action = searchParams.get("action");
  const strategy = searchParams.get("strategy");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/price-optimization`);
      if (risk) url.searchParams.set("risk", risk);
      if (action) url.searchParams.set("action", action);
      if (strategy) url.searchParams.set("strategy", strategy);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let deals = [...mockDeals];
  if (risk) deals = deals.filter((d) => d.discount_risk === risk);
  if (action) deals = deals.filter((d) => d.pricing_action === action);
  if (strategy) deals = deals.filter((d) => d.pricing_strategy === strategy);

  const risk_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  const strategy_counts: Record<string, number> = {};
  const impact_counts: Record<string, number> = {};
  let total_score = 0;
  let revenue_at_risk = 0;

  for (const d of mockDeals) {
    risk_counts[d.discount_risk] = (risk_counts[d.discount_risk] || 0) + 1;
    action_counts[d.pricing_action] = (action_counts[d.pricing_action] || 0) + 1;
    strategy_counts[d.pricing_strategy] = (strategy_counts[d.pricing_strategy] || 0) + 1;
    impact_counts[d.revenue_impact] = (impact_counts[d.revenue_impact] || 0) + 1;
    total_score += d.price_optimization_score;
    if (d.discount_risk === "high" || d.discount_risk === "excessive") {
      revenue_at_risk += d.list_price_eur - d.proposed_price_eur;
    }
  }

  const n = mockDeals.length;

  return sealResponse(NextResponse.json({
    deals,
    summary: {
      total: n,
      risk_counts,
      action_counts,
      strategy_counts,
      revenue_impact_counts: impact_counts,
      avg_optimization_score: Math.round((total_score / n) * 10) / 10,
      excessive_discount_count: mockDeals.filter((d) => d.discount_risk === "excessive").length,
      restructure_count: mockDeals.filter((d) => d.pricing_action === "restructure").length,
      total_revenue_at_risk_eur: revenue_at_risk,
    },
  }));
}
