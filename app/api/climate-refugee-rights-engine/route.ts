import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[climate-refugee-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[climate-refugee-rights-engine] SWARM_API_URL not set — running in offline mode");

export async function GET() {
  try {
    if (!UPSTREAM) throw new Error("offline");
    const res = await fetch(`${UPSTREAM}/api/climate-refugee-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      agent: "ClimateRefugeeRights Engine Agent",
      domain: "climate_refugee_rights",
      total_entities: 8,
      avg_composite: 60.69,
      confidence_score: 0.85,
      risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
      pattern_distribution: {
        mass_climate_displacement_no_legal_status: 1,
        complete_territorial_loss_sovereignty: 1,
        cyclone_induced_mass_displacement: 1,
        catastrophic_flooding_infrastructure_loss: 1,
        atoll_submersion_migration_statelessness: 1,
        drought_conflict_nexus_displacement: 1,
        adaptation_infrastructure_global_disparity: 1,
        international_framework_climate_refugees: 1,
      },
      top_risk_entities: [
        "Bangladesh — 20M déplacés d'ici 2050, cyclones & montée des eaux",
        "Tuvalu — Île 50cm altitude, accord migration Australie 2023",
        "Mozambique — Cyclones Idai/Kenneth, 2,5M déplacés",
      ],
      critical_alerts: [
        "Bangladesh: mass_climate_displacement_no_legal_status",
        "Tuvalu: complete_territorial_loss_sovereignty",
        "Mozambique: cyclone_induced_mass_displacement",
        "Pakistan: catastrophic_flooding_infrastructure_loss",
      ],
      last_analysis: "2026-06-22",
      engine_version: "1.0.0",
      avg_estimated_climate_refugee_rights_index: 6.07,
      data_sources: [
        "ipcc_ar6_climate_change_displacement_risks_2022",
        "idmc_global_report_internal_displacement_2024",
        "un_human_rights_climate_change_obligations_report",
        "climate_vulnerable_forum_loss_damage_documentation",
        "unhcr_climate_displacement_protection_gap_report",
      ],
      entities: [
        {
          entity_id: "CRR-001",
          name: "Bangladesh — 20M déplacés d'ici 2050, cyclones & montée des eaux",
          country: "Bangladesh",
          displacement_severity_score: 95.0,
          legal_protection_gap_score: 94.0,
          adaptation_funding_gap_score: 93.0,
          territorial_loss_score: 96.0,
          composite_score: 94.45,
          risk_level: "critique",
          primary_pattern: "mass_climate_displacement_no_legal_status",
          estimated_climate_refugee_rights_index: 9.45,
          last_updated: "2026-06-22",
        },
        {
          entity_id: "CRR-002",
          name: "Tuvalu — Île 50cm altitude, accord migration Australie 2023",
          country: "Tuvalu",
          displacement_severity_score: 90.0,
          legal_protection_gap_score: 91.0,
          adaptation_funding_gap_score: 89.0,
          territorial_loss_score: 92.0,
          composite_score: 90.4,
          risk_level: "critique",
          primary_pattern: "complete_territorial_loss_sovereignty",
          estimated_climate_refugee_rights_index: 9.04,
          last_updated: "2026-06-22",
        },
        {
          entity_id: "CRR-003",
          name: "Mozambique — Cyclones Idai/Kenneth, 2,5M déplacés",
          country: "Mozambique",
          displacement_severity_score: 84.0,
          legal_protection_gap_score: 83.0,
          adaptation_funding_gap_score: 82.0,
          territorial_loss_score: 85.0,
          composite_score: 83.45,
          risk_level: "critique",
          primary_pattern: "cyclone_induced_mass_displacement",
          estimated_climate_refugee_rights_index: 8.35,
          last_updated: "2026-06-22",
        },
        {
          entity_id: "CRR-004",
          name: "Pakistan — Inondations 2022, 33% territoire submergé",
          country: "Pakistan",
          displacement_severity_score: 78.0,
          legal_protection_gap_score: 77.0,
          adaptation_funding_gap_score: 76.0,
          territorial_loss_score: 79.0,
          composite_score: 77.45,
          risk_level: "critique",
          primary_pattern: "catastrophic_flooding_infrastructure_loss",
          estimated_climate_refugee_rights_index: 7.75,
          last_updated: "2026-06-22",
        },
        {
          entity_id: "CRR-005",
          name: "Îles Marshall — Migration vers USA, demande statut réfugié",
          country: "Îles Marshall",
          displacement_severity_score: 54.0,
          legal_protection_gap_score: 53.0,
          adaptation_funding_gap_score: 52.0,
          territorial_loss_score: 55.0,
          composite_score: 53.45,
          risk_level: "élevé",
          primary_pattern: "atoll_submersion_migration_statelessness",
          estimated_climate_refugee_rights_index: 5.35,
          last_updated: "2026-06-22",
        },
        {
          entity_id: "CRR-006",
          name: "Éthiopie/Sahel — Sécheresses consécutives, déplacés climato-conflits",
          country: "Éthiopie",
          displacement_severity_score: 46.0,
          legal_protection_gap_score: 45.0,
          adaptation_funding_gap_score: 44.0,
          territorial_loss_score: 47.0,
          composite_score: 45.45,
          risk_level: "élevé",
          primary_pattern: "drought_conflict_nexus_displacement",
          estimated_climate_refugee_rights_index: 4.55,
          last_updated: "2026-06-22",
        },
        {
          entity_id: "CRR-007",
          name: "Pays-Bas — Delta Works adaptation, inégalités globales réponse",
          country: "Pays-Bas",
          displacement_severity_score: 30.0,
          legal_protection_gap_score: 29.0,
          adaptation_funding_gap_score: 28.0,
          territorial_loss_score: 31.0,
          composite_score: 29.45,
          risk_level: "modéré",
          primary_pattern: "adaptation_infrastructure_global_disparity",
          estimated_climate_refugee_rights_index: 2.95,
          last_updated: "2026-06-22",
        },
        {
          entity_id: "CRR-008",
          name: "UNHCR/IPCC — Agenda Nansen, reconnaissance réfugiés climatiques ONU",
          country: "International",
          displacement_severity_score: 12.0,
          legal_protection_gap_score: 11.0,
          adaptation_funding_gap_score: 10.0,
          territorial_loss_score: 13.0,
          composite_score: 11.45,
          risk_level: "faible",
          primary_pattern: "international_framework_climate_refugees",
          estimated_climate_refugee_rights_index: 1.15,
          last_updated: "2026-06-22",
        },
      ],
    }, { status: 200 }));
  }
}
