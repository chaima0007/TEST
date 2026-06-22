import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// ── Module 392 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
// Aging Infrastructure & Physical System Collapse Intelligence Engine
// 8 entities covering all 5 patterns and all 4 risk levels.

interface AieInput {
  id: string;
  infrastructure_type: string;
  region: string;
  structural_deterioration_rate: number;
  maintenance_deficit_severity: number;
  bridge_dam_collapse_risk: number;
  water_pipe_failure_rate: number;
  power_grid_aging_vulnerability: number;
  transport_network_degradation: number;
  investment_deficit_chronic: number;
  population_exposure_risk: number;
  failure_cascade_potential: number;
  regulatory_inspection_gap: number;
  climate_accelerated_aging: number;
  critical_failure_imminent: number;
  emergency_repair_capacity: number;
  insurance_withdrawal_risk: number;
  public_safety_exposure: number;
  economic_productivity_loss: number;
  political_will_deficit: number;
}

const MOCK_ENTITIES: AieInput[] = [
  // AIE-001 — NOAM, pont_routier → critical, critical_infrastructure_imminent_failure
  // critical_failure_imminent>0.85 AND structural_deterioration_rate>0.80 → critical_infrastructure_imminent_failure
  // composite≥60 → critical
  {
    id: "AIE-001", infrastructure_type: "pont_routier", region: "NOAM",
    structural_deterioration_rate: 0.88,
    maintenance_deficit_severity: 0.75,
    bridge_dam_collapse_risk: 0.78,
    water_pipe_failure_rate: 0.55,
    power_grid_aging_vulnerability: 0.60,
    transport_network_degradation: 0.82,
    investment_deficit_chronic: 0.70,
    population_exposure_risk: 0.72,
    failure_cascade_potential: 0.68,
    regulatory_inspection_gap: 0.65,
    climate_accelerated_aging: 0.70,
    critical_failure_imminent: 0.90,
    emergency_repair_capacity: 0.55,
    insurance_withdrawal_risk: 0.65,
    public_safety_exposure: 0.80,
    economic_productivity_loss: 0.70,
    political_will_deficit: 0.65,
  },
  // AIE-002 — EMEA, réseau_eau → low, none
  // All low values → composite<20, no pattern triggered
  {
    id: "AIE-002", infrastructure_type: "réseau_eau", region: "EMEA",
    structural_deterioration_rate: 0.10,
    maintenance_deficit_severity: 0.08,
    bridge_dam_collapse_risk: 0.08,
    water_pipe_failure_rate: 0.10,
    power_grid_aging_vulnerability: 0.10,
    transport_network_degradation: 0.08,
    investment_deficit_chronic: 0.10,
    population_exposure_risk: 0.08,
    failure_cascade_potential: 0.08,
    regulatory_inspection_gap: 0.10,
    climate_accelerated_aging: 0.08,
    critical_failure_imminent: 0.08,
    emergency_repair_capacity: 0.10,
    insurance_withdrawal_risk: 0.08,
    public_safety_exposure: 0.10,
    economic_productivity_loss: 0.08,
    political_will_deficit: 0.10,
  },
  // AIE-003 — LATAM, réseau_électrique → critical, investment_deficit_crisis
  // investment_deficit_chronic>0.85 AND maintenance_deficit_severity>0.80 → investment_deficit_crisis
  // critical_failure_imminent=0.60≤0.85 → avoids critical_infrastructure_imminent_failure
  // composite≥60 → critical
  {
    id: "AIE-003", infrastructure_type: "réseau_électrique", region: "LATAM",
    structural_deterioration_rate: 0.72,
    maintenance_deficit_severity: 0.88,
    bridge_dam_collapse_risk: 0.65,
    water_pipe_failure_rate: 0.60,
    power_grid_aging_vulnerability: 0.75,
    transport_network_degradation: 0.68,
    investment_deficit_chronic: 0.90,
    population_exposure_risk: 0.70,
    failure_cascade_potential: 0.65,
    regulatory_inspection_gap: 0.72,
    climate_accelerated_aging: 0.68,
    critical_failure_imminent: 0.60,
    emergency_repair_capacity: 0.55,
    insurance_withdrawal_risk: 0.70,
    public_safety_exposure: 0.65,
    economic_productivity_loss: 0.72,
    political_will_deficit: 0.75,
  },
  // AIE-004 — APAC, canalisation_eau → high, water_power_grid_collapse
  // water_pipe_failure_rate>0.85 AND power_grid_aging_vulnerability>0.80 → water_power_grid_collapse
  // critical_failure_imminent=0.50≤0.85 → avoids critical_infrastructure_imminent_failure
  // investment_deficit_chronic=0.55≤0.85 → avoids investment_deficit_crisis
  // composite in [40,60) → high
  {
    id: "AIE-004", infrastructure_type: "canalisation_eau", region: "APAC",
    structural_deterioration_rate: 0.55,
    maintenance_deficit_severity: 0.50,
    bridge_dam_collapse_risk: 0.55,
    water_pipe_failure_rate: 0.88,
    power_grid_aging_vulnerability: 0.85,
    transport_network_degradation: 0.52,
    investment_deficit_chronic: 0.55,
    population_exposure_risk: 0.60,
    failure_cascade_potential: 0.55,
    regulatory_inspection_gap: 0.50,
    climate_accelerated_aging: 0.55,
    critical_failure_imminent: 0.50,
    emergency_repair_capacity: 0.48,
    insurance_withdrawal_risk: 0.52,
    public_safety_exposure: 0.55,
    economic_productivity_loss: 0.50,
    political_will_deficit: 0.48,
  },
  // AIE-005 — MEA, barrage → critical, bridge_dam_catastrophe_risk
  // bridge_dam_collapse_risk>0.80 AND population_exposure_risk>0.75 → bridge_dam_catastrophe_risk
  // critical_failure_imminent=0.65≤0.85 → avoids critical_infrastructure_imminent_failure
  // investment_deficit_chronic=0.60≤0.85 → avoids investment_deficit_crisis
  // water_pipe_failure_rate=0.55≤0.85 → avoids water_power_grid_collapse
  // composite≥60 → critical
  {
    id: "AIE-005", infrastructure_type: "barrage", region: "MEA",
    structural_deterioration_rate: 0.75,
    maintenance_deficit_severity: 0.72,
    bridge_dam_collapse_risk: 0.88,
    water_pipe_failure_rate: 0.55,
    power_grid_aging_vulnerability: 0.58,
    transport_network_degradation: 0.70,
    investment_deficit_chronic: 0.60,
    population_exposure_risk: 0.82,
    failure_cascade_potential: 0.72,
    regulatory_inspection_gap: 0.68,
    climate_accelerated_aging: 0.65,
    critical_failure_imminent: 0.65,
    emergency_repair_capacity: 0.50,
    insurance_withdrawal_risk: 0.72,
    public_safety_exposure: 0.78,
    economic_productivity_loss: 0.75,
    political_will_deficit: 0.68,
  },
  // AIE-006 — NOAM, réseau_routier → moderate, none
  // composite in [20,40), no pattern triggered
  {
    id: "AIE-006", infrastructure_type: "réseau_routier", region: "NOAM",
    structural_deterioration_rate: 0.28,
    maintenance_deficit_severity: 0.25,
    bridge_dam_collapse_risk: 0.22,
    water_pipe_failure_rate: 0.25,
    power_grid_aging_vulnerability: 0.28,
    transport_network_degradation: 0.25,
    investment_deficit_chronic: 0.28,
    population_exposure_risk: 0.22,
    failure_cascade_potential: 0.20,
    regulatory_inspection_gap: 0.25,
    climate_accelerated_aging: 0.22,
    critical_failure_imminent: 0.20,
    emergency_repair_capacity: 0.28,
    insurance_withdrawal_risk: 0.22,
    public_safety_exposure: 0.22,
    economic_productivity_loss: 0.20,
    political_will_deficit: 0.25,
  },
  // AIE-007 — EMEA, infrastructure_ferroviaire → high, failure_cascade_systemic
  // failure_cascade_potential>0.80 AND climate_accelerated_aging>0.75 → failure_cascade_systemic
  // critical_failure_imminent=0.45≤0.85 → avoids critical_infrastructure_imminent_failure
  // investment_deficit_chronic=0.50≤0.85 → avoids investment_deficit_crisis
  // water_pipe_failure_rate=0.42≤0.85 → avoids water_power_grid_collapse
  // bridge_dam_collapse_risk=0.55≤0.80 → avoids bridge_dam_catastrophe_risk
  // composite in [40,60) → high
  {
    id: "AIE-007", infrastructure_type: "infrastructure_ferroviaire", region: "EMEA",
    structural_deterioration_rate: 0.55,
    maintenance_deficit_severity: 0.52,
    bridge_dam_collapse_risk: 0.55,
    water_pipe_failure_rate: 0.42,
    power_grid_aging_vulnerability: 0.48,
    transport_network_degradation: 0.58,
    investment_deficit_chronic: 0.50,
    population_exposure_risk: 0.55,
    failure_cascade_potential: 0.85,
    regulatory_inspection_gap: 0.52,
    climate_accelerated_aging: 0.80,
    critical_failure_imminent: 0.45,
    emergency_repair_capacity: 0.48,
    insurance_withdrawal_risk: 0.52,
    public_safety_exposure: 0.50,
    economic_productivity_loss: 0.55,
    political_will_deficit: 0.48,
  },
  // AIE-008 — APAC, réseau_eau_urbain → low, none
  // All low values → composite<20, no pattern triggered
  {
    id: "AIE-008", infrastructure_type: "réseau_eau_urbain", region: "APAC",
    structural_deterioration_rate: 0.08,
    maintenance_deficit_severity: 0.10,
    bridge_dam_collapse_risk: 0.08,
    water_pipe_failure_rate: 0.10,
    power_grid_aging_vulnerability: 0.08,
    transport_network_degradation: 0.10,
    investment_deficit_chronic: 0.08,
    population_exposure_risk: 0.10,
    failure_cascade_potential: 0.08,
    regulatory_inspection_gap: 0.08,
    climate_accelerated_aging: 0.10,
    critical_failure_imminent: 0.08,
    emergency_repair_capacity: 0.10,
    insurance_withdrawal_risk: 0.08,
    public_safety_exposure: 0.08,
    economic_productivity_loss: 0.10,
    political_will_deficit: 0.08,
  },
];

// ── Scoring functions (mirrors Python engine exactly) ──────────────────────────

function deteriorationScore(e: AieInput): number {
  return Math.round((e.structural_deterioration_rate * 0.4 + e.transport_network_degradation * 0.35 + e.climate_accelerated_aging * 0.25) * 100 * 100) / 100;
}

function safetyScore(e: AieInput): number {
  return Math.round((e.bridge_dam_collapse_risk * 0.4 + e.public_safety_exposure * 0.35 + e.critical_failure_imminent * 0.25) * 100 * 100) / 100;
}

function investmentScore(e: AieInput): number {
  return Math.round((e.investment_deficit_chronic * 0.4 + e.maintenance_deficit_severity * 0.35 + e.political_will_deficit * 0.25) * 100 * 100) / 100;
}

function cascadeScore(e: AieInput): number {
  return Math.round((e.failure_cascade_potential * 0.4 + e.population_exposure_risk * 0.35 + e.economic_productivity_loss * 0.25) * 100 * 100) / 100;
}

function aieComposite(det: number, saf: number, inv: number, cas: number): number {
  return Math.round((det * 0.30 + saf * 0.25 + inv * 0.25 + cas * 0.20) * 100) / 100;
}

function aieRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function aiePattern(e: AieInput): string {
  if (e.critical_failure_imminent > 0.85 && e.structural_deterioration_rate > 0.80) return "critical_infrastructure_imminent_failure";
  if (e.investment_deficit_chronic > 0.85 && e.maintenance_deficit_severity > 0.80) return "investment_deficit_crisis";
  if (e.water_pipe_failure_rate > 0.85 && e.power_grid_aging_vulnerability > 0.80) return "water_power_grid_collapse";
  if (e.bridge_dam_collapse_risk > 0.80 && e.population_exposure_risk > 0.75) return "bridge_dam_catastrophe_risk";
  if (e.failure_cascade_potential > 0.80 && e.climate_accelerated_aging > 0.75) return "failure_cascade_systemic";
  return "none";
}

function aieSeverity(risk: string): string {
  if (risk === "critical") return "urgence_effondrement_infrastructure_physique";
  if (risk === "high") return "crise_vieillissement_infrastructure_majeure";
  if (risk === "moderate") return "dégradation_structurelle_chronique";
  return "vieillissement_infrastructure_géré";
}

function aieAction(risk: string): string {
  if (risk === "critical") return "plan_urgence_réhabilitation_infrastructure";
  if (risk === "high") return "réparation_urgente_infrastructure_critique";
  if (risk === "moderate") return "programme_maintenance_préventive_accéléré";
  return "veille_vieillissement_infrastructure_continue";
}

function aieSignal(risk: string): string {
  if (risk === "critical") return "🔴 Urgence effondrement infrastructure — défaillance physique imminente";
  if (risk === "high") return "🟠 Crise vieillissement infrastructure majeure détectée";
  if (risk === "moderate") return "🟡 Dégradation structurelle chronique active";
  return "🟢 Vieillissement infrastructure sous surveillance";
}

function analyzeEntity(e: AieInput) {
  const det = deteriorationScore(e);
  const saf = safetyScore(e);
  const inv = investmentScore(e);
  const cas = cascadeScore(e);
  const comp = aieComposite(det, saf, inv, cas);
  const risk = aieRisk(comp);
  const pattern = aiePattern(e);
  const severity = aieSeverity(risk);
  const action = aieAction(risk);
  const signal = aieSignal(risk);

  return {
    id: e.entity_id,
    infrastructure_type: e.infrastructure_type,
    region: e.region,
    deterioration_score: det,
    safety_score: saf,
    investment_score: inv,
    cascade_score: cas,
    composite_score: comp,
    risk_level: risk,
    aging_pattern: pattern,
    severity,
    recommended_action: action,
    signal,
    structural_deterioration_rate: e.structural_deterioration_rate,
    critical_failure_imminent: e.critical_failure_imminent,
  };
}

// ── GET handler ────────────────────────────────────────────────────────────────

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[aging-infrastructure-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    const pattern_distribution: Record<string, number> = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number> = {};
    let tComp = 0, tDet = 0, tSaf = 0, tInv = 0, tCas = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level] = (risk_distribution[ent.risk_level] || 0) + 1;
      pattern_distribution[ent.aging_pattern] = (pattern_distribution[ent.aging_pattern] || 0) + 1;
      severity_distribution[ent.severity] = (severity_distribution[ent.severity] || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tComp += ent.composite_score;
      tDet += ent.deterioration_score;
      tSaf += ent.safety_score;
      tInv += ent.investment_score;
      tCas += ent.cascade_score;
    }

    const n = entities.length;
    const avgComp = Math.round((tComp / n) * 100) / 100;

    return sealResponse(NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id: 392,
        module_name: "Aging Infrastructure & Physical System Collapse Intelligence Engine",
        total: n,
        critical: risk_distribution["critical"] || 0,
        high: risk_distribution["high"] || 0,
        moderate: risk_distribution["moderate"] || 0,
        low: risk_distribution["low"] || 0,
        avg_composite: avgComp,
        distributions: {
          risk: risk_distribution,
          pattern: pattern_distribution,
          severity: severity_distribution,
          action: action_distribution,
        },
        avg_estimated_infrastructure_aging_index: Math.round(avgComp / 100 * 10 * 100) / 100,
        avg_deterioration_score: Math.round(tDet / n * 100) / 100,
        avg_safety_score: Math.round(tSaf / n * 100) / 100,
        avg_investment_score: Math.round(tInv / n * 100) / 100,
        avg_cascade_score: Math.round(tCas / n * 100) / 100,
      },
    } as Record<string, unknown>, "aging-infrastructure-engine")));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/aging-infrastructure-engine`, { next: { revalidate: 30 } });
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return sealResponse(NextResponse.json(sealResponse(await upstream.json() as Record<string, unknown>, "aging-infrastructure-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "SWARM_API_URL unreachable" } as Record<string, unknown>, "aging-infrastructure-engine"),
      { status: 502 }
    ));
  }
}
