import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[space-rights-outer-space-militarization-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Space Rights Outer Space Militarization Engine Agent",
  domain: "space_rights_outer_space_militarization",
  total_entities: 8,
  avg_composite: 61.22,
  confidence_score: 0.84,
  risk_distribution: { "critique": 4, "élevé": 2, "modéré": 1, "faible": 1 },
  pattern_distribution: { "anti_satellite_weapons_debris_severity": 3, "space_militarization_arms_race_scale": 2, "space_debris_kessler_syndrome_risk": 1, "outer_space_treaty_compliance_governance_deficit_gap": 2 },
  top_risk_entities: ["Russie — Test ASAT Nudol 2021 1 500 Débris, Orbital Bombardment System, Inspection Satellites Rapprochée & Armes Lasers Anti-Sat", "Chine — ASAT SC-19 Test 2007 3 000 Débris, Satellites Militaires 200+, Jamming GPS & Programme Espace Militaire Accéléré", "USA/SpaceCom — US Space Force 2019, Starlink Usage Ukraine Militaire, X-37B Orbital, Co-Orbital ASAT & Contrôle Commercial Militarisé"],
  critical_alerts: ["Russie: anti_satellite_weapons_debris_severity", "Chine: space_militarization_arms_race_scale", "USA/SpaceCom: space_militarization_arms_race_scale", "Inde: anti_satellite_weapons_debris_severity"],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_space_rights_outer_space_militarization_index: 6.12,
  data_sources: ["unoosa_space_debris_environment_report", "secure_world_foundation_space_threat_assessment", "un_group_experts_outer_space_security"],
  entities: [
    {
,      entity_id: "SRM-001"
      name: "Russie — Test ASAT Nudol 2021 1 500 Débris, Orbital Bombardment System, Inspection Satellites Rapprochée & Armes Lasers Anti-Sat"
      country: "Russie"
      anti_satellite_weapons_debris_severity_score: 94.0
      space_militarization_arms_race_scale_score: 92.0
      space_debris_kessler_syndrome_risk_score: 93.0
      outer_space_treaty_compliance_governance_deficit_gap_score: 91.0
      composite_score: 92.65
      risk_level: "critique"
      primary_pattern: "anti_satellite_weapons_debris_severity"
      estimated_space_rights_outer_space_militarization_index: 9.27
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "SRM-002"
      name: "Chine — ASAT SC-19 Test 2007 3 000 Débris, Satellites Militaires 200+, Jamming GPS & Programme Espace Militaire Accéléré"
      country: "Chine"
      anti_satellite_weapons_debris_severity_score: 90.0
      space_militarization_arms_race_scale_score: 89.0
      space_debris_kessler_syndrome_risk_score: 91.0
      outer_space_treaty_compliance_governance_deficit_gap_score: 88.0
      composite_score: 89.6
      risk_level: "critique"
      primary_pattern: "space_militarization_arms_race_scale"
      estimated_space_rights_outer_space_militarization_index: 8.96
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "SRM-003"
      name: "USA/SpaceCom — US Space Force 2019, Starlink Usage Ukraine Militaire, X-37B Orbital, Co-Orbital ASAT & Contrôle Commercial Militarisé"
      country: "USA"
      anti_satellite_weapons_debris_severity_score: 87.0
      space_militarization_arms_race_scale_score: 86.0
      space_debris_kessler_syndrome_risk_score: 85.0
      outer_space_treaty_compliance_governance_deficit_gap_score: 88.0
      composite_score: 86.45
      risk_level: "critique"
      primary_pattern: "space_militarization_arms_race_scale"
      estimated_space_rights_outer_space_militarization_index: 8.64
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "SRM-004"
      name: "Inde — Test ASAT Mission Shakti 2019 400+ Débris, DRDO Capacités Croissantes, Spatialisation Défense & Adhésion Partielle Traités"
      country: "Inde"
      anti_satellite_weapons_debris_severity_score: 83.0
      space_militarization_arms_race_scale_score: 82.0
      space_debris_kessler_syndrome_risk_score: 84.0
      outer_space_treaty_compliance_governance_deficit_gap_score: 81.0
      composite_score: 82.6
      risk_level: "critique"
      primary_pattern: "anti_satellite_weapons_debris_severity"
      estimated_space_rights_outer_space_militarization_index: 8.26
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "SRM-005"
      name: "Méga-Constellations — Starlink 6 000+ Satellites 42k Prévus, OneWeb Amazon Kuiper, Pollution Lumineuse Astronomie & Collision Risk 1% /An"
      country: "Global"
      anti_satellite_weapons_debris_severity_score: 56.0
      space_militarization_arms_race_scale_score: 54.0
      space_debris_kessler_syndrome_risk_score: 55.0
      outer_space_treaty_compliance_governance_deficit_gap_score: 57.0
      composite_score: 55.45
      risk_level: "élevé"
      primary_pattern: "space_debris_kessler_syndrome_risk"
      estimated_space_rights_outer_space_militarization_index: 5.54
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "SRM-006"
      name: "JAXA/ESA — Agences Civiles Pression Militarisée, Budget Défense Espace +30%, Clean Space Initiative & Nettoyage Débris Sous-Financé"
      country: "Global"
      anti_satellite_weapons_debris_severity_score: 52.0
      space_militarization_arms_race_scale_score: 51.0
      space_debris_kessler_syndrome_risk_score: 54.0
      outer_space_treaty_compliance_governance_deficit_gap_score: 53.0
      composite_score: 52.45
      risk_level: "élevé"
      primary_pattern: "outer_space_treaty_compliance_governance_deficit_gap"
      estimated_space_rights_outer_space_militarization_index: 5.25
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "SRM-007"
      name: "UNOOSA/COPUOS — Committee Peaceful Uses Outer Space, Space Debris Mitigation Guidelines, LTS Guidelines & Registre ONU"
      country: "Global"
      anti_satellite_weapons_debris_severity_score: 27.0
      space_militarization_arms_race_scale_score: 25.0
      space_debris_kessler_syndrome_risk_score: 28.0
      outer_space_treaty_compliance_governance_deficit_gap_score: 26.0
      composite_score: 26.55
      risk_level: "modéré"
      primary_pattern: "outer_space_treaty_compliance_governance_deficit_gap"
      estimated_space_rights_outer_space_militarization_index: 2.66
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "SRM-008"
      name: "ONU/OST 1967 — Traité Espace Extra-Atmosphérique 1967, Traité Lune 1979, Convention Responsabilité & Régime Gouvernance Lacunaire"
      country: "Global"
      anti_satellite_weapons_debris_severity_score: 4.0
      space_militarization_arms_race_scale_score: 4.0
      space_debris_kessler_syndrome_risk_score: 4.0
      outer_space_treaty_compliance_governance_deficit_gap_score: 4.0
      composite_score: 4.0
      risk_level: "faible"
      primary_pattern: "anti_satellite_weapons_debris_severity"
      estimated_space_rights_outer_space_militarization_index: 0.4
      last_updated: "2026-06-21"
    }
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/space-rights-outer-space-militarization-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
