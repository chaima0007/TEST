import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

// ── Mock entity input data ────────────────────────────────────────────────────

const MOCK_ENTITIES = [
  // SCF-001: EMEA, semiconductor_chain → critical risk, single_source_crisis
  {
    id: "SCF-001", chain_type: "semiconductor_chain", region: "EMEA",
    single_source_dependency: 0.82, just_in_time_vulnerability: 0.55,
    geopolitical_chokepoint_exposure: 0.78, logistics_network_fragility: 0.60,
    supplier_financial_fragility: 0.50, inventory_buffer_adequacy: 0.25,
    demand_shock_sensitivity: 0.55, nearshoring_readiness: 0.20,
    digital_supply_chain_risk: 0.52, counterfeit_infiltration_risk: 0.60,
    port_concentration_risk: 0.72, regulatory_divergence_burden: 0.58,
    natural_disaster_exposure: 0.48, cybersecurity_supply_risk: 0.55,
    ESG_compliance_gap: 0.42, labor_disruption_potential: 0.45,
    cross_border_friction: 0.50,
  },
  // SCF-002: APAC, food_supply_chain → low risk, none pattern
  {
    id: "SCF-002", chain_type: "food_supply_chain", region: "APAC",
    single_source_dependency: 0.12, just_in_time_vulnerability: 0.18,
    geopolitical_chokepoint_exposure: 0.15, logistics_network_fragility: 0.20,
    supplier_financial_fragility: 0.15, inventory_buffer_adequacy: 0.80,
    demand_shock_sensitivity: 0.22, nearshoring_readiness: 0.75,
    digital_supply_chain_risk: 0.15, counterfeit_infiltration_risk: 0.18,
    port_concentration_risk: 0.14, regulatory_divergence_burden: 0.20,
    natural_disaster_exposure: 0.28, cybersecurity_supply_risk: 0.12,
    ESG_compliance_gap: 0.15, labor_disruption_potential: 0.20,
    cross_border_friction: 0.18,
  },
  // SCF-003: NOAM, pharmaceutical_chain → high risk, jit_shock_cascade
  {
    id: "SCF-003", chain_type: "pharmaceutical_chain", region: "NOAM",
    single_source_dependency: 0.48, just_in_time_vulnerability: 0.75,
    geopolitical_chokepoint_exposure: 0.45, logistics_network_fragility: 0.55,
    supplier_financial_fragility: 0.40, inventory_buffer_adequacy: 0.35,
    demand_shock_sensitivity: 0.72, nearshoring_readiness: 0.38,
    digital_supply_chain_risk: 0.50, counterfeit_infiltration_risk: 0.55,
    port_concentration_risk: 0.42, regulatory_divergence_burden: 0.48,
    natural_disaster_exposure: 0.30, cybersecurity_supply_risk: 0.48,
    ESG_compliance_gap: 0.35, labor_disruption_potential: 0.40,
    cross_border_friction: 0.45,
  },
  // SCF-004: LATAM, agricultural_chain → low risk, none pattern
  {
    id: "SCF-004", chain_type: "agricultural_chain", region: "LATAM",
    single_source_dependency: 0.15, just_in_time_vulnerability: 0.22,
    geopolitical_chokepoint_exposure: 0.18, logistics_network_fragility: 0.25,
    supplier_financial_fragility: 0.20, inventory_buffer_adequacy: 0.72,
    demand_shock_sensitivity: 0.25, nearshoring_readiness: 0.70,
    digital_supply_chain_risk: 0.18, counterfeit_infiltration_risk: 0.15,
    port_concentration_risk: 0.18, regulatory_divergence_burden: 0.22,
    natural_disaster_exposure: 0.35, cybersecurity_supply_risk: 0.15,
    ESG_compliance_gap: 0.20, labor_disruption_potential: 0.25,
    cross_border_friction: 0.22,
  },
  // SCF-005: MEA, energy_supply_chain → critical risk, cyber_supply_attack
  {
    id: "SCF-005", chain_type: "energy_supply_chain", region: "MEA",
    single_source_dependency: 0.60, just_in_time_vulnerability: 0.58,
    geopolitical_chokepoint_exposure: 0.72, logistics_network_fragility: 0.65,
    supplier_financial_fragility: 0.55, inventory_buffer_adequacy: 0.30,
    demand_shock_sensitivity: 0.60, nearshoring_readiness: 0.25,
    digital_supply_chain_risk: 0.78, counterfeit_infiltration_risk: 0.55,
    port_concentration_risk: 0.68, regulatory_divergence_burden: 0.62,
    natural_disaster_exposure: 0.55, cybersecurity_supply_risk: 0.82,
    ESG_compliance_gap: 0.50, labor_disruption_potential: 0.58,
    cross_border_friction: 0.60,
  },
  // SCF-006: EMEA, automotive_chain → moderate risk, none pattern
  {
    id: "SCF-006", chain_type: "automotive_chain", region: "EMEA",
    single_source_dependency: 0.35, just_in_time_vulnerability: 0.42,
    geopolitical_chokepoint_exposure: 0.38, logistics_network_fragility: 0.38,
    supplier_financial_fragility: 0.30, inventory_buffer_adequacy: 0.55,
    demand_shock_sensitivity: 0.40, nearshoring_readiness: 0.52,
    digital_supply_chain_risk: 0.35, counterfeit_infiltration_risk: 0.32,
    port_concentration_risk: 0.30, regulatory_divergence_burden: 0.38,
    natural_disaster_exposure: 0.28, cybersecurity_supply_risk: 0.30,
    ESG_compliance_gap: 0.32, labor_disruption_potential: 0.35,
    cross_border_friction: 0.38,
  },
  // SCF-007: APAC, electronics_chain → high risk, supplier_bankruptcy_wave
  {
    id: "SCF-007", chain_type: "electronics_chain", region: "APAC",
    single_source_dependency: 0.55, just_in_time_vulnerability: 0.60,
    geopolitical_chokepoint_exposure: 0.52, logistics_network_fragility: 0.58,
    supplier_financial_fragility: 0.75, inventory_buffer_adequacy: 0.30,
    demand_shock_sensitivity: 0.55, nearshoring_readiness: 0.35,
    digital_supply_chain_risk: 0.55, counterfeit_infiltration_risk: 0.62,
    port_concentration_risk: 0.50, regulatory_divergence_burden: 0.52,
    natural_disaster_exposure: 0.40, cybersecurity_supply_risk: 0.52,
    ESG_compliance_gap: 0.48, labor_disruption_potential: 0.50,
    cross_border_friction: 0.48,
  },
  // SCF-008: NOAM, critical_minerals_chain → critical risk, regulatory_fragmentation
  {
    id: "SCF-008", chain_type: "critical_minerals_chain", region: "NOAM",
    single_source_dependency: 0.65, just_in_time_vulnerability: 0.62,
    geopolitical_chokepoint_exposure: 0.70, logistics_network_fragility: 0.65,
    supplier_financial_fragility: 0.58, inventory_buffer_adequacy: 0.28,
    demand_shock_sensitivity: 0.60, nearshoring_readiness: 0.22,
    digital_supply_chain_risk: 0.62, counterfeit_infiltration_risk: 0.55,
    port_concentration_risk: 0.65, regulatory_divergence_burden: 0.82,
    natural_disaster_exposure: 0.45, cybersecurity_supply_risk: 0.62,
    ESG_compliance_gap: 0.60, labor_disruption_potential: 0.55,
    cross_border_friction: 0.78,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

// ── Scoring helpers ───────────────────────────────────────────────────────────

function concentrationScore(e: Entity): number {
  return (e.single_source_dependency * 0.40 + e.port_concentration_risk * 0.35 + e.geopolitical_chokepoint_exposure * 0.25) * 100;
}
function fragilityScore(e: Entity): number {
  return (e.just_in_time_vulnerability * 0.40 + e.logistics_network_fragility * 0.35 + (1 - e.inventory_buffer_adequacy) * 0.25) * 100;
}
function riskScore(e: Entity): number {
  return (e.cybersecurity_supply_risk * 0.40 + e.counterfeit_infiltration_risk * 0.35 + e.supplier_financial_fragility * 0.25) * 100;
}
function adaptationScore(e: Entity): number {
  return ((1 - e.nearshoring_readiness) * 0.40 + e.regulatory_divergence_burden * 0.35 + e.cross_border_friction * 0.25) * 100;
}
function compositeScore(c: number, f: number, r: number, a: number): number {
  return c * 0.30 + f * 0.25 + r * 0.25 + a * 0.20;
}
function chainRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}
function chainPattern(e: Entity): string {
  if (e.single_source_dependency >= 0.70 && e.geopolitical_chokepoint_exposure >= 0.65) return "single_source_crisis";
  if (e.just_in_time_vulnerability >= 0.70 && e.demand_shock_sensitivity >= 0.65) return "jit_shock_cascade";
  if (e.supplier_financial_fragility >= 0.70 && e.inventory_buffer_adequacy <= 0.40) return "supplier_bankruptcy_wave";
  if (e.cybersecurity_supply_risk >= 0.70 && e.digital_supply_chain_risk >= 0.65) return "cyber_supply_attack";
  if (e.regulatory_divergence_burden >= 0.70 && e.cross_border_friction >= 0.65) return "regulatory_fragmentation";
  return "none";
}
function chainSeverity(comp: number): string {
  if (comp >= 75) return "supply_emergency";
  if (comp >= 50) return "high_fragility";
  if (comp >= 25) return "supply_tension";
  return "chain_robust";
}
function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "emergency_supply_rerouting";
  if (risk === "high" && pattern === "single_source_crisis") return "supply_diversification";
  if (risk === "high") return "resilience_buffer_program";
  if (risk === "moderate") return "supply_monitoring";
  return "no_action";
}
function chainSignal(e: Entity, pattern: string, risk: string, comp: number): string {
  if (risk === "low") return `Chaîne d'approvisionnement ${e.chain_type} résiliente — composite fragilité ${Math.round(comp)} — aucune rupture détectée`;
  const patternSignals: Record<string, string> = {
    single_source_crisis:    `Crise source unique détectée — dépendance mono-fournisseur ${e.single_source_dependency.toFixed(2)} combinée à exposition goulot géopolitique ${e.geopolitical_chokepoint_exposure.toFixed(2)} — risque rupture totale`,
    jit_shock_cascade:       `Cascade JIT sous choc — vulnérabilité flux tendu ${e.just_in_time_vulnerability.toFixed(2)}, sensibilité choc demande ${e.demand_shock_sensitivity.toFixed(2)} — effondrement synchronisé probable`,
    supplier_bankruptcy_wave:`Vague de défaillances fournisseurs — fragilité financière ${e.supplier_financial_fragility.toFixed(2)}, buffer stocks insuffisant ${e.inventory_buffer_adequacy.toFixed(2)} — risque rupture critique`,
    cyber_supply_attack:     `Attaque cybersécurité chaîne — risque cyber ${e.cybersecurity_supply_risk.toFixed(2)}, exposition numérique ${e.digital_supply_chain_risk.toFixed(2)} — compromission infrastructure approvisionnement`,
    regulatory_fragmentation:`Fragmentation réglementaire — divergence normative ${e.regulatory_divergence_burden.toFixed(2)}, friction transfrontalière ${e.cross_border_friction.toFixed(2)} — blocage flux commerciaux`,
  };
  const base = patternSignals[pattern] ?? `Fragilité chaîne ${e.chain_type} détectée — composite ${Math.round(comp)}`;
  return `${base} — risque ${risk} — région ${e.region}`;
}

function processEntity(e: Entity) {
  const c = concentrationScore(e);
  const f = fragilityScore(e);
  const r = riskScore(e);
  const a = adaptationScore(e);
  const comp = compositeScore(c, f, r, a);
  const risk = chainRisk(comp);
  const pat  = chainPattern(e);
  const sev  = chainSeverity(comp);
  const act  = recommendedAction(risk, pat);
  return {
    id:                    e.entity_id,
    region:                       e.region,
    chain_type:                   e.chain_type,
    chain_risk:                   risk,
    chain_pattern:                pat,
    chain_severity:               sev,
    recommended_action:           act,
    concentration_score:          Math.round(c * 100) / 100,
    fragility_score:              Math.round(f * 100) / 100,
    risk_score:                   Math.round(r * 100) / 100,
    adaptation_score:             Math.round(a * 100) / 100,
    chain_composite:              Math.round(comp * 100) / 100,
    is_chain_crisis:              comp >= 60,
    requires_chain_intervention:  comp >= 40,
    chain_signal:                 chainSignal(e, pat, risk, comp),
  };
}

export async function GET() {
  if (!SWARM_API_URL) {
    return NextResponse.json(sealResponse({ error: "SWARM_API_URL not configured" } as Record<string, unknown>), { status: 502 });
  }

  const entities = MOCK_ENTITIES.map(processEntity);
  const n = entities.length;

  const riskDist: Record<string, number> = { low: 0, moderate: 0, high: 0, critical: 0 };
  const patternCounts: Record<string, number> = {};
  let totalComp = 0, criticalC = 0, highC = 0, crisisC = 0, interventionC = 0;

  for (const ent of entities) {
    riskDist[ent.chain_risk] = (riskDist[ent.chain_risk] || 0) + 1;
    patternCounts[ent.chain_pattern] = (patternCounts[ent.chain_pattern] || 0) + 1;
    totalComp += ent.chain_composite;
    if (ent.chain_risk === "critical") criticalC++;
    if (ent.chain_risk === "high") highC++;
    if (ent.is_chain_crisis) crisisC++;
    if (ent.requires_chain_intervention) interventionC++;
  }

  const avgComp = totalComp / n;
  const dominantPattern = Object.entries(patternCounts).sort((a, b) => b[1] - a[1])[0]?.[0] ?? "none";
  const avgFragilityIndex = Math.round((avgComp / 100) * 10 * 100) / 100;

  return NextResponse.json(sealResponse({
    module:                             "Module 311",
    engine:                             "Global Supply Chain Fragility Intelligence Engine",
    analyst:                            "Chaima Mhadbi, Fondatrice, Caelum Partners, Bruxelles",
    timestamp:                          new Date().toISOString(),
    total_entities_assessed:            n,
    critical_chains:                    criticalC,
    high_risk_chains:                   highC,
    chain_crises_detected:              crisisC,
    requires_intervention:              interventionC,
    dominant_pattern:                   dominantPattern,
    avg_estimated_chain_fragility_index: avgFragilityIndex,
    risk_distribution:                  riskDist,
    entities,
  } as Record<string, unknown>), "supply-chain-fragility-engine");
}
