import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_ENTITIES = [
  // NWE-001 — critical, repository_failure_crisis (containment_integrity<0.15, repository_capacity<0.20)
  {
    entity_id: "NWE-001", waste_category: "haute_activité", region: "Europe_Est",
    containment_integrity: 0.10, repository_capacity: 0.12, geological_stability: 0.15,
    cooling_system_safety: 0.12, governance_effectiveness: 0.20, regulatory_independence: 0.22,
    transparency_index: 0.18, public_trust: 0.15, intergenerational_equity: 0.22,
    time_horizon_planning: 0.20, proliferation_risk: 0.75, security_measures: 0.22,
    transport_safety: 0.20, worker_exposure: 0.75, emergency_preparedness: 0.18,
    community_consent: 0.20, decommissioning_readiness: 0.15,
  },
  // NWE-002 — critical, intergenerational_justice_void (intergenerational_equity<0.15, time_horizon_planning<0.20)
  {
    entity_id: "NWE-002", waste_category: "moyenne_activité", region: "Asie_Pacifique",
    containment_integrity: 0.20, repository_capacity: 0.22, geological_stability: 0.18,
    cooling_system_safety: 0.20, governance_effectiveness: 0.22, regulatory_independence: 0.20,
    transparency_index: 0.18, public_trust: 0.20, intergenerational_equity: 0.10,
    time_horizon_planning: 0.12, proliferation_risk: 0.78, security_measures: 0.20,
    transport_safety: 0.22, worker_exposure: 0.72, emergency_preparedness: 0.20,
    community_consent: 0.18, decommissioning_readiness: 0.20,
  },
  // NWE-003 — critical, proliferation_leakage_risk (proliferation_risk>0.85, security_measures<0.20)
  {
    entity_id: "NWE-003", waste_category: "matières_fissiles", region: "Moyen_Orient",
    containment_integrity: 0.18, repository_capacity: 0.20, geological_stability: 0.20,
    cooling_system_safety: 0.18, governance_effectiveness: 0.18, regulatory_independence: 0.20,
    transparency_index: 0.15, public_trust: 0.18, intergenerational_equity: 0.20,
    time_horizon_planning: 0.22, proliferation_risk: 0.92, security_measures: 0.12,
    transport_safety: 0.18, worker_exposure: 0.70, emergency_preparedness: 0.18,
    community_consent: 0.20, decommissioning_readiness: 0.18,
  },
  // NWE-004 — high, regulatory_capture_collapse (regulatory_independence<0.15, governance_effectiveness<0.20)
  {
    entity_id: "NWE-004", waste_category: "faible_activité", region: "Amérique_Latine",
    containment_integrity: 0.50, repository_capacity: 0.52, geological_stability: 0.55,
    cooling_system_safety: 0.50, governance_effectiveness: 0.12, regulatory_independence: 0.10,
    transparency_index: 0.18, public_trust: 0.20, intergenerational_equity: 0.45,
    time_horizon_planning: 0.48, proliferation_risk: 0.40, security_measures: 0.48,
    transport_safety: 0.50, worker_exposure: 0.40, emergency_preparedness: 0.45,
    community_consent: 0.42, decommissioning_readiness: 0.45,
  },
  // NWE-005 — high, legacy_contamination_spread (worker_exposure>0.80, decommissioning_readiness<0.25)
  {
    entity_id: "NWE-005", waste_category: "déchets_anciens", region: "Europe_Occidentale",
    containment_integrity: 0.48, repository_capacity: 0.50, geological_stability: 0.52,
    cooling_system_safety: 0.45, governance_effectiveness: 0.50, regulatory_independence: 0.48,
    transparency_index: 0.50, public_trust: 0.45, intergenerational_equity: 0.48,
    time_horizon_planning: 0.50, proliferation_risk: 0.38, security_measures: 0.50,
    transport_safety: 0.52, worker_exposure: 0.85, emergency_preparedness: 0.45,
    community_consent: 0.48, decommissioning_readiness: 0.20,
  },
  // NWE-006 — moderate, none
  {
    entity_id: "NWE-006", waste_category: "très_faible_activité", region: "Afrique",
    containment_integrity: 0.65, repository_capacity: 0.68, geological_stability: 0.70,
    cooling_system_safety: 0.65, governance_effectiveness: 0.68, regulatory_independence: 0.65,
    transparency_index: 0.70, public_trust: 0.65, intergenerational_equity: 0.68,
    time_horizon_planning: 0.70, proliferation_risk: 0.25, security_measures: 0.68,
    transport_safety: 0.70, worker_exposure: 0.28, emergency_preparedness: 0.65,
    community_consent: 0.68, decommissioning_readiness: 0.65,
  },
  // NWE-007 — low, none
  {
    entity_id: "NWE-007", waste_category: "stockage_géologique", region: "Amérique_Nord",
    containment_integrity: 0.88, repository_capacity: 0.85, geological_stability: 0.90,
    cooling_system_safety: 0.88, governance_effectiveness: 0.88, regulatory_independence: 0.90,
    transparency_index: 0.85, public_trust: 0.88, intergenerational_equity: 0.85,
    time_horizon_planning: 0.88, proliferation_risk: 0.08, security_measures: 0.90,
    transport_safety: 0.88, worker_exposure: 0.08, emergency_preparedness: 0.88,
    community_consent: 0.85, decommissioning_readiness: 0.88,
  },
  // NWE-008 — low, none
  {
    entity_id: "NWE-008", waste_category: "déchets_hospitaliers", region: "Scandinavie",
    containment_integrity: 0.90, repository_capacity: 0.88, geological_stability: 0.92,
    cooling_system_safety: 0.90, governance_effectiveness: 0.90, regulatory_independence: 0.88,
    transparency_index: 0.92, public_trust: 0.90, intergenerational_equity: 0.88,
    time_horizon_planning: 0.90, proliferation_risk: 0.06, security_measures: 0.92,
    transport_safety: 0.90, worker_exposure: 0.06, emergency_preparedness: 0.90,
    community_consent: 0.88, decommissioning_readiness: 0.90,
  },
];

type NWEInput = (typeof MOCK_ENTITIES)[0];

function containmentScore(e: NWEInput): number {
  return Math.round(((1 - e.containment_integrity) * 0.4 + (1 - e.repository_capacity) * 0.35 + (1 - e.geological_stability) * 0.25) * 100 * 100) / 100;
}
function governanceScore(e: NWEInput): number {
  return Math.round(((1 - e.governance_effectiveness) * 0.4 + (1 - e.regulatory_independence) * 0.35 + (1 - e.transparency_index) * 0.25) * 100 * 100) / 100;
}
function intergenerationalScore(e: NWEInput): number {
  return Math.round(((1 - e.intergenerational_equity) * 0.4 + (1 - e.time_horizon_planning) * 0.35 + (1 - e.community_consent) * 0.25) * 100 * 100) / 100;
}
function proliferationScore(e: NWEInput): number {
  return Math.round((e.proliferation_risk * 0.4 + (1 - e.security_measures) * 0.35 + (1 - e.transport_safety) * 0.25) * 100 * 100) / 100;
}
function compositeScore(cont: number, gov: number, intgn: number, prol: number): number {
  return Math.round((cont * 0.30 + gov * 0.25 + intgn * 0.25 + prol * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function nuclearPattern(e: NWEInput): string {
  if (e.containment_integrity < 0.15 && e.repository_capacity < 0.20) return "repository_failure_crisis";
  if (e.intergenerational_equity < 0.15 && e.time_horizon_planning < 0.20) return "intergenerational_justice_void";
  if (e.proliferation_risk > 0.85 && e.security_measures < 0.20) return "proliferation_leakage_risk";
  if (e.regulatory_independence < 0.15 && e.governance_effectiveness < 0.20) return "regulatory_capture_collapse";
  if (e.worker_exposure > 0.80 && e.decommissioning_readiness < 0.25) return "legacy_contamination_spread";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_nucléaire_sécurité_systémique";
  if (composite >= 40) return "risque_gestion_déchets_majeur";
  if (composite >= 20) return "surveillance_confinement_active";
  return "gestion_déchets_sous_contrôle";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_sécurité_nucléaire_critique";
  if (risk === "high") return "renforcement_confinement_gouvernance_accéléré";
  if (risk === "moderate") return "surveillance_renforcée_déchets_nucléaires";
  return "veille_sécurité_long_terme_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise nucléaire systémique — sécurité long-terme en péril immédiat";
  if (risk === "high") return "🟠 Risque gestion déchets majeur détecté";
  if (risk === "moderate") return "🟡 Surveillance confinement nucléaire active";
  return "🟢 Gestion déchets nucléaires sous contrôle";
}

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const cont  = containmentScore(e);
      const gov   = governanceScore(e);
      const intgn = intergenerationalScore(e);
      const prol  = proliferationScore(e);
      const comp  = compositeScore(cont, gov, intgn, prol);
      const risk  = riskLevel(comp);
      const pat   = nuclearPattern(e);
      const sev   = severity(comp);
      const action = recommendedAction(risk);
      const sig   = signal(risk);
      return {
        entity_id:              e.entity_id,
        waste_category:         e.waste_category,
        region:                 e.region,
        containment_score:      cont,
        governance_score:       gov,
        intergenerational_score: intgn,
        proliferation_score:    prol,
        composite_score:        comp,
        risk_level:             risk,
        nuclear_pattern:        pat,
        severity:               sev,
        recommended_action:     action,
        signal:                 sig,
        containment_integrity:  e.containment_integrity,
        proliferation_risk:     e.proliferation_risk,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.nuclear_pattern]   = (pattern_distribution[ent.nuclear_pattern]   || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")      criticalCount++;
      else if (ent.risk_level === "high")     highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else                                    lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;

    const summary = {
      module_id:                         401,
      module_name:                       "Gestion Déchets Nucléaires & Sécurité Long-Terme Intelligence Engine",
      total:                             n,
      critical:                          criticalCount,
      high:                              highCount,
      moderate:                          moderateCount,
      low:                               lowCount,
      avg_composite:                     avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_nuclear_waste_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary } as Record<string, unknown>));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/nuclear-waste-engine`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return NextResponse.json(sealResponse(await res.json()));
  } catch {}
  return NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 });
}
