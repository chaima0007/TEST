import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "climate_displacement_migration_engine",
  domain: "climate_displacement_migration",
  total_entities: 8,
  avg_composite: 59.76,
  confidence_score: 0.88,
  avg_estimated_climate_displacement_migration_index: 5.98,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "unhcr_climate_displacement_2023",
    "idmc_global_report_2023",
    "ipcc_ar6_human_mobility_2022",
    "platform_disaster_displacement_2023",
  ],
  critical_alerts: [
    "Bangladesh — inondations/cyclones, 7M déplacés internes 2022, delta du Gange menacé — risk_level: critique, composite: 82.4",
    "Sahel africain — sécheresse structurelle, 2,4M déplacés climate-conflict nexus 2023 — risk_level: critique, composite: 81.5",
    "Pakistan — inondations 2022, 1/3 pays submergé, 33M sinistrés, 8M déplacés — risk_level: critique, composite: 77.5",
    "Tuvalu/Kiribati — submersion territoriale, apatridie climatique, migration permanente — risk_level: critique, composite: 76.75",
  ],
  entities: [
    {
      entity_id: "CDM-001",
      name: "Bangladesh — inondations/cyclones, 7M déplacés internes 2022, delta du Gange menacé",
      sub1: 88.0,
      sub2: 82.0,
      sub3: 78.0,
      sub4: 80.0,
      composite_score: 82.4,
      risk_level: "critique",
      estimated_climate_displacement_migration_index: 8.24,
    },
    {
      entity_id: "CDM-002",
      name: "Sahel africain — sécheresse structurelle, 2,4M déplacés climate-conflict nexus 2023",
      sub1: 85.0,
      sub2: 84.0,
      sub3: 80.0,
      sub4: 75.0,
      composite_score: 81.5,
      risk_level: "critique",
      estimated_climate_displacement_migration_index: 8.15,
    },
    {
      entity_id: "CDM-003",
      name: "Pakistan — inondations 2022, 1/3 pays submergé, 33M sinistrés, 8M déplacés",
      sub1: 82.0,
      sub2: 78.0,
      sub3: 76.0,
      sub4: 72.0,
      composite_score: 77.5,
      risk_level: "critique",
      estimated_climate_displacement_migration_index: 7.75,
    },
    {
      entity_id: "CDM-004",
      name: "Tuvalu/Kiribati — submersion territoriale, apatridie climatique, migration permanente",
      sub1: 70.0,
      sub2: 75.0,
      sub3: 72.0,
      sub4: 95.0,
      composite_score: 76.75,
      risk_level: "critique",
      estimated_climate_displacement_migration_index: 7.67,
    },
    {
      entity_id: "CDM-005",
      name: "Philippines — typhons récurrents, 4,5M déplacés/an, zones côtières vulnérables",
      sub1: 72.0,
      sub2: 58.0,
      sub3: 52.0,
      sub4: 48.0,
      composite_score: 58.7,
      risk_level: "élevé",
      estimated_climate_displacement_migration_index: 5.87,
    },
    {
      entity_id: "CDM-006",
      name: "Honduras/Guatemala — cyclones Eta/Iota 2020, migration triangulaire forcée vers USA",
      sub1: 65.0,
      sub2: 60.0,
      sub3: 55.0,
      sub4: 45.0,
      composite_score: 57.25,
      risk_level: "élevé",
      estimated_climate_displacement_migration_index: 5.72,
    },
    {
      entity_id: "CDM-007",
      name: "Fidji — politique d&apos;adaptation proactive, relocalisation villages côtiers planifiée",
      sub1: 38.0,
      sub2: 32.0,
      sub3: 28.0,
      sub4: 42.0,
      composite_score: 34.8,
      risk_level: "modéré",
      estimated_climate_displacement_migration_index: 3.48,
    },
    {
      entity_id: "CDM-008",
      name: "Union Européenne — Pacte Migration/Asile 2024, standards protection déplacés climatiques",
      sub1: 10.0,
      sub2: 8.0,
      sub3: 12.0,
      sub4: 6.0,
      composite_score: 9.2,
      risk_level: "faible",
      estimated_climate_displacement_migration_index: 0.92,
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[climate-displacement-migration-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/climate-displacement-migration-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
