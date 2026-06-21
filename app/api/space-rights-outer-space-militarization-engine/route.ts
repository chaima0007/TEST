import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[space-rights-outer-space-militarization-engine] SWARM_API_URL is not set — using mock data");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_ENTITIES = [
  {
    id: "SRM-001",
    name: "Russie — Test ASAT Nudol 2021 1 500 Débris, Orbital Bombardment System, Inspection Satellites Rapprochée & Armes Lasers Anti-Sat",
    country: "Russie",
    sector: "ASAT Débris Orbitaux",
    anti_satellite_weapons_debris_severity_score: 94.0,
    space_militarization_arms_race_scale_score: 92.0,
    space_debris_kessler_syndrome_risk_score: 93.0,
    outer_space_treaty_compliance_governance_deficit_gap_score: 91.0,
    primary_pattern: "anti_satellite_weapons_debris_severity",
  },
  {
    id: "SRM-002",
    name: "Chine — ASAT SC-19 Test 2007 3 000 Débris, Satellites Militaires 200+, Jamming GPS & Programme Espace Militaire Accéléré",
    country: "Chine",
    sector: "Programme Militaire Spatial",
    anti_satellite_weapons_debris_severity_score: 90.0,
    space_militarization_arms_race_scale_score: 89.0,
    space_debris_kessler_syndrome_risk_score: 91.0,
    outer_space_treaty_compliance_governance_deficit_gap_score: 88.0,
    primary_pattern: "space_militarization_arms_race_scale",
  },
  {
    id: "SRM-003",
    name: "USA/SpaceCom — US Space Force 2019, Starlink Usage Ukraine Militaire, X-37B Orbital, Co-Orbital ASAT & Contrôle Commercial Militarisé",
    country: "USA",
    sector: "Space Force Militarisation Commerciale",
    anti_satellite_weapons_debris_severity_score: 87.0,
    space_militarization_arms_race_scale_score: 86.0,
    space_debris_kessler_syndrome_risk_score: 85.0,
    outer_space_treaty_compliance_governance_deficit_gap_score: 88.0,
    primary_pattern: "space_militarization_arms_race_scale",
  },
  {
    id: "SRM-004",
    name: "Inde — Test ASAT Mission Shakti 2019 400+ Débris, DRDO Capacités Croissantes, Spatialisation Défense & Adhésion Partielle Traités",
    country: "Inde",
    sector: "ASAT Capacités Croissantes",
    anti_satellite_weapons_debris_severity_score: 83.0,
    space_militarization_arms_race_scale_score: 82.0,
    space_debris_kessler_syndrome_risk_score: 84.0,
    outer_space_treaty_compliance_governance_deficit_gap_score: 81.0,
    primary_pattern: "anti_satellite_weapons_debris_severity",
  },
  {
    id: "SRM-005",
    name: "Méga-Constellations — Starlink 6 000+ Satellites 42k Prévus, OneWeb Amazon Kuiper, Pollution Lumineuse Astronomie & Collision Risk 1% /An",
    country: "Global",
    sector: "Constellations Commerciales Congestion Orbitale",
    anti_satellite_weapons_debris_severity_score: 56.0,
    space_militarization_arms_race_scale_score: 54.0,
    space_debris_kessler_syndrome_risk_score: 55.0,
    outer_space_treaty_compliance_governance_deficit_gap_score: 57.0,
    primary_pattern: "space_debris_kessler_syndrome_risk",
  },
  {
    id: "SRM-006",
    name: "JAXA/ESA — Agences Civiles Pression Militarisée, Budget Défense Espace +30%, Clean Space Initiative & Nettoyage Débris Sous-Financé",
    country: "Global",
    sector: "Agences Civiles Transition Défense",
    anti_satellite_weapons_debris_severity_score: 52.0,
    space_militarization_arms_race_scale_score: 51.0,
    space_debris_kessler_syndrome_risk_score: 54.0,
    outer_space_treaty_compliance_governance_deficit_gap_score: 53.0,
    primary_pattern: "outer_space_treaty_compliance_governance_deficit_gap",
  },
  {
    id: "SRM-007",
    name: "UNOOSA/COPUOS — Committee Peaceful Uses Outer Space, Space Debris Mitigation Guidelines, LTS Guidelines & Registre ONU",
    country: "Global",
    sector: "Gouvernance Internationale Espace",
    anti_satellite_weapons_debris_severity_score: 27.0,
    space_militarization_arms_race_scale_score: 25.0,
    space_debris_kessler_syndrome_risk_score: 28.0,
    outer_space_treaty_compliance_governance_deficit_gap_score: 26.0,
    primary_pattern: "outer_space_treaty_compliance_governance_deficit_gap",
  },
  {
    id: "SRM-008",
    name: "ONU/OST 1967 — Traité Espace Extra-Atmosphérique 1967, Traité Lune 1979, Convention Responsabilité & Régime Gouvernance Lacunaire",
    country: "Global",
    sector: "Cadre Normatif Traités Spatiaux",
    anti_satellite_weapons_debris_severity_score: 4.0,
    space_militarization_arms_race_scale_score: 4.0,
    space_debris_kessler_syndrome_risk_score: 4.0,
    outer_space_treaty_compliance_governance_deficit_gap_score: 4.0,
    primary_pattern: "anti_satellite_weapons_debris_severity",
  },
];

type SRMInput = (typeof MOCK_ENTITIES)[0];

function computeComposite(e: SRMInput): number {
  return Math.round(
    (e.anti_satellite_weapons_debris_severity_score * 0.30
    + e.space_militarization_arms_race_scale_score * 0.25
    + e.space_debris_kessler_syndrome_risk_score * 0.25
    + e.outer_space_treaty_compliance_governance_deficit_gap_score * 0.20) * 100
  ) / 100;
}

function riskLevel(composite: number): string {
  if (composite >= 60) return "critique";
  if (composite >= 40) return "élevé";
  if (composite >= 20) return "modéré";
  return "faible";
}

function severity(composite: number): string {
  if (composite >= 60) return "crise_militarisation_orbitale_systémique";
  if (composite >= 40) return "crise_course_armements_spatiaux_majeure";
  if (composite >= 20) return "risque_congestion_orbitale_structurel";
  return "surveillance_traités_spatiaux";
}

function recommendedAction(risk: string): string {
  if (risk === "critique") return "intervention_urgente_moratoire_asat_debris";
  if (risk === "élevé") return "renforcement_traités_espace_pacifique";
  if (risk === "modéré") return "révision_gouvernance_constellations_commerciales";
  return "veille_compliance_outer_space_treaty_continue";
}

function signal(risk: string): string {
  if (risk === "critique") return "CRITIQUE — Crise militarisation orbitale systémique — débris & ASAT en escalade";
  if (risk === "élevé") return "ÉLEVÉ — Crise course armements spatiaux majeure détectée";
  if (risk === "modéré") return "MODÉRÉ — Risque congestion orbitale structurel actif";
  return "FAIBLE — Surveillance traités spatiaux continue";
}

function estimatedIndex(composite: number): number {
  return Math.round(composite / 100 * 10 * 100) / 100;
}

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map((e) => {
      const composite = computeComposite(e);
      const risk = riskLevel(composite);
      return {
        id: e.entity_id,
        name: e.name,
        country: e.country,
        sector: e.sector,
        anti_satellite_weapons_debris_severity_score: e.anti_satellite_weapons_debris_severity_score,
        space_militarization_arms_race_scale_score: e.space_militarization_arms_race_scale_score,
        space_debris_kessler_syndrome_risk_score: e.space_debris_kessler_syndrome_risk_score,
        outer_space_treaty_compliance_governance_deficit_gap_score: e.outer_space_treaty_compliance_governance_deficit_gap_score,
        composite_score: composite,
        risk_level: risk,
        primary_pattern: e.primary_pattern,
        severity: severity(composite),
        recommended_action: recommendedAction(risk),
        signal: signal(risk),
        estimated_space_rights_outer_space_militarization_index: estimatedIndex(composite),
        last_updated: "2026-06-21",
      };
    });

    const risk_distribution: Record<string, number> = {};
    const pattern_distribution: Record<string, number> = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number> = {};
    let totalComposite = 0;
    let critiqueCount = 0, élevéCount = 0, modéréCount = 0, faibleCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level] = (risk_distribution[ent.risk_level] || 0) + 1;
      pattern_distribution[ent.primary_pattern] = (pattern_distribution[ent.primary_pattern] || 0) + 1;
      severity_distribution[ent.severity] = (severity_distribution[ent.severity] || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      totalComposite += ent.composite_score;
      if (ent.risk_level === "critique") critiqueCount++;
      else if (ent.risk_level === "élevé") élevéCount++;
      else if (ent.risk_level === "modéré") modéréCount++;
      else faibleCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(totalComposite / n * 100) / 100;

    const summary = {
      module_id: 982,
      module_name: "Space Rights Outer Space Militarization Intelligence Engine",
      agent: "Space Rights Outer Space Militarization Engine Agent",
      domain: "space_rights_outer_space_militarization",
      total: n,
      critique: critiqueCount,
      élevé: élevéCount,
      modéré: modéréCount,
      faible: faibleCount,
      avg_composite: avgComposite,
      avg_estimated_space_rights_outer_space_militarization_index: estimatedIndex(avgComposite),
      risk_distribution,
      pattern_distribution,
      severity_distribution,
      action_distribution,
      confidence_score: 0.84,
      data_sources: [
        "unoosa_space_debris_environment_report",
        "secure_world_foundation_space_threat_assessment",
        "un_group_experts_outer_space_security",
      ],
      last_analysis: "2026-06-21",
      engine_version: "1.0.0",
    };

    return NextResponse.json(
      sealResponse({ entities, summary } as Record<string, unknown>)
    );
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/space-rights-outer-space-militarization-engine`);
    const res = await fetch(url.toString(), { next: { revalidate: 30 } });
    if (res.ok) return NextResponse.json(sealResponse(await res.json()));
  } catch {}
  return NextResponse.json(
    sealResponse({ entities: [], summary: {} } as Record<string, unknown>),
    { status: 502 }
  );
}
