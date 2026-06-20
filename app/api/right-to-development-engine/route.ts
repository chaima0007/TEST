import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[right-to-development-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Right to Development Engine Agent",
  domain: "right_to_development",
  total_entities: 8,
  avg_composite: 58.55,
  confidence_score: 0.83,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { systemic_inequality: 2, debt_trap_dependency: 2, technology_transfer_denial: 2, participatory_governance_failure: 2 },
  top_risk_entities: [
    "Afrique Sub-Saharienne/PMA — 46 Pays, 1B$ Flux Illicites/Jour & Exclusion Développement",
    "Sri Lanka/Pakistan/Zambie — Pièges de la Dette FMI/Chine & Austérité",
    "Congo/RDC/Ressources — Paradoxe du Cobalt, 24T$ Minéraux & 75% Pauvreté",
  ],
  critical_alerts: [
    "Afrique Sub-Saharienne/PMA: systemic_inequality",
    "Sri Lanka/Pakistan/Zambie: debt_trap_dependency",
    "Congo/RDC/Ressources: technology_transfer_denial",
    "Haïti/Bangladesh/Cambodge: technology_transfer_denial",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_right_to_development_index: 5.86,
  data_sources: [
    "undp_human_development_report_annual",
    "global_financial_integrity_illicit_financial_flows_report",
    "un_high_level_task_force_right_to_development_expert_reports",
  ],
  entities: [
    {
      entity_id: "RD-001",
      name: "Afrique Sub-Saharienne/PMA — 46 Pays, 1B$ Flux Illicites/Jour & Exclusion Développement",
      country: "Afrique Sub-Saharienne",
      composite_score: 88.85,
      systemic_inequality_score: 92.0,
      debt_trap_dependency_score: 88.0,
      technology_transfer_denial_score: 85.0,
      participatory_governance_failure_score: 90.0,
      risk_level: "critique",
      primary_pattern: "systemic_inequality",
      estimated_right_to_development_index: 8.89,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "RD-002",
      name: "Sri Lanka/Pakistan/Zambie — Pièges de la Dette FMI/Chine & Austérité",
      country: "Asie du Sud/Afrique",
      composite_score: 84.90,
      systemic_inequality_score: 85.0,
      debt_trap_dependency_score: 92.0,
      technology_transfer_denial_score: 80.0,
      participatory_governance_failure_score: 82.0,
      risk_level: "critique",
      primary_pattern: "debt_trap_dependency",
      estimated_right_to_development_index: 8.49,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "RD-003",
      name: "Congo/RDC/Ressources — Paradoxe du Cobalt, 24T$ Minéraux & 75% Pauvreté",
      country: "Afrique Centrale",
      composite_score: 81.75,
      systemic_inequality_score: 80.0,
      debt_trap_dependency_score: 75.0,
      technology_transfer_denial_score: 88.0,
      participatory_governance_failure_score: 85.0,
      risk_level: "critique",
      primary_pattern: "technology_transfer_denial",
      estimated_right_to_development_index: 8.18,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "RD-004",
      name: "Haïti/Bangladesh/Cambodge — Sweatshops, Chaînes d'Approvisionnement & Travail Précaire",
      country: "Global Sud",
      composite_score: 76.10,
      systemic_inequality_score: 72.0,
      debt_trap_dependency_score: 78.0,
      technology_transfer_denial_score: 80.0,
      participatory_governance_failure_score: 75.0,
      risk_level: "critique",
      primary_pattern: "technology_transfer_denial",
      estimated_right_to_development_index: 7.61,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "RD-005",
      name: "Brésil/Inde — Émergents Inégaux, Milliardaires Record & Pauvreté Persistante",
      country: "BRICS Émergents",
      composite_score: 51.50,
      systemic_inequality_score: 55.0,
      debt_trap_dependency_score: 52.0,
      technology_transfer_denial_score: 48.0,
      participatory_governance_failure_score: 50.0,
      risk_level: "élevé",
      primary_pattern: "systemic_inequality",
      estimated_right_to_development_index: 5.15,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "RD-006",
      name: "Chine/BRI — Initiative Route Soie, Dettes Opaques & Conditionnalités Géopolitiques",
      country: "Asie du Nord-Est",
      composite_score: 52.50,
      systemic_inequality_score: 45.0,
      debt_trap_dependency_score: 62.0,
      technology_transfer_denial_score: 50.0,
      participatory_governance_failure_score: 55.0,
      risk_level: "élevé",
      primary_pattern: "debt_trap_dependency",
      estimated_right_to_development_index: 5.25,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "RD-007",
      name: "UE/OCDE — APD, CBAM & Cohérence Politiques Développement",
      country: "Europe/OCDE",
      composite_score: 28.40,
      systemic_inequality_score: 25.0,
      debt_trap_dependency_score: 30.0,
      technology_transfer_denial_score: 28.0,
      participatory_governance_failure_score: 32.0,
      risk_level: "modéré",
      primary_pattern: "participatory_governance_failure",
      estimated_right_to_development_index: 2.84,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "RD-008",
      name: "ONU/DRD 1986 — Déclaration Droit Développement, Groupe Travail & ODD",
      country: "Global",
      composite_score: 4.40,
      systemic_inequality_score: 4.0,
      debt_trap_dependency_score: 5.0,
      technology_transfer_denial_score: 3.0,
      participatory_governance_failure_score: 6.0,
      risk_level: "faible",
      primary_pattern: "participatory_governance_failure",
      estimated_right_to_development_index: 0.44,
      last_updated: "2026-06-20",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/right-to-development-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
