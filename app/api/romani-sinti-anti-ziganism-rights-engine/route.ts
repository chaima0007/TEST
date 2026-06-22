import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[romani-sinti-anti-ziganism-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "romani_sinti_anti_ziganism_rights_engine",
  domain: "romani_sinti_anti_ziganism_rights",
  total_entities: 8,
  avg_composite: 58.94,
  confidence_score: 0.90,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: {
    educational_segregation: 3,
    forced_eviction: 2,
    anti_ziganism_institutional: 2,
    rights_protection_deficit: 1,
  },
  top_risk_entities: [
    { id: "RSA-001", name: "Slovaquie — Ségrégation Scolaire Roms, 50% Classes Spéciales", score: 90.7, risk: "critique" },
    { id: "RSA-002", name: "Bulgarie — Évictions Forcées Quartiers Roms, Mahala Démolis", score: 86.85, risk: "critique" },
    { id: "RSA-003", name: "France — 15 000 Roms Expulsés 2023, Circulaire Valls", score: 82.85, risk: "critique" },
  ],
  critical_alerts: [
    "RSA-001: Slovaquie — Ségrégation Scolaire Roms, 50% Classes Spéciales — composite 90.7",
    "RSA-002: Bulgarie — Évictions Forcées Quartiers Roms, Mahala Démolis — composite 86.85",
    "RSA-003: France — 15 000 Roms Expulsés 2023, Circulaire Valls — composite 82.85",
    "RSA-004: Hongrie — Orban Anti-Roms, Stérilisation Forcée Historique — composite 79.5",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_romani_rights_index: 5.89,
  data_sources: [
    "fra_roma_inclusion_report_2023",
    "council_europe_ecri_reports_2023",
    "errc_european_roma_rights_centre_2023",
    "cedh_arrêts_roms_2021_2023",
  ],
  entities: [
    {
      id: "RSA-001",
      name: "Slovaquie — Ségrégation Scolaire Roms, 50% Classes Spéciales",
      country: "Slovaquie",
      segregation_exclusion_score: 93.0,
      eviction_displacement_score: 88.0,
      anti_ziganism_state_complicity_score: 91.0,
      rights_protection_enforcement_deficit_score: 89.0,
      composite_score: 90.7,
      risk_level: "critique",
      primary_pattern: "50% enfants roms classes spéciales, arrêt CEDH 2021 ignoré, discrimination institutionnelle éducation, ghettos scolaires",
      estimated_romani_rights_index: 9.07,
      last_updated: "2026-06-21",
    },
    {
      id: "RSA-002",
      name: "Bulgarie — Évictions Forcées Quartiers Roms, Mahala Démolis",
      country: "Bulgarie",
      segregation_exclusion_score: 88.0,
      eviction_displacement_score: 90.0,
      anti_ziganism_state_complicity_score: 85.0,
      rights_protection_enforcement_deficit_score: 84.0,
      composite_score: 86.85,
      risk_level: "critique",
      primary_pattern: "Mahala démolis sans relogement, discrimination systémique emploi/logement, anti-ziganism médiatique normalisé",
      estimated_romani_rights_index: 8.69,
      last_updated: "2026-06-21",
    },
    {
      id: "RSA-003",
      name: "France — 15 000 Roms Expulsés 2023, Circulaire Valls",
      country: "France",
      segregation_exclusion_score: 83.0,
      eviction_displacement_score: 86.0,
      anti_ziganism_state_complicity_score: 82.0,
      rights_protection_enforcement_deficit_score: 80.0,
      composite_score: 82.85,
      risk_level: "critique",
      primary_pattern: "15 000 expulsions 2023, circulaire Valls persistante, camps démantelés sans relogement, Roms citoyens UE discriminés",
      estimated_romani_rights_index: 8.29,
      last_updated: "2026-06-21",
    },
    {
      id: "RSA-004",
      name: "Hongrie — Orban Anti-Roms, Stérilisation Forcée Historique",
      country: "Hongrie",
      segregation_exclusion_score: 81.0,
      eviction_displacement_score: 78.0,
      anti_ziganism_state_complicity_score: 80.0,
      rights_protection_enforcement_deficit_score: 77.0,
      composite_score: 79.5,
      risk_level: "critique",
      primary_pattern: "Rhétorique Orban anti-roms, stérilisation forcée historique non réparée, exclusion marché travail 70%, ségrégation écoles",
      estimated_romani_rights_index: 7.95,
      last_updated: "2026-06-21",
    },
    {
      id: "RSA-005",
      name: "République Tchèque — Stérilisations Forcées, 90 000 Cas Documentés",
      country: "République Tchèque",
      segregation_exclusion_score: 55.0,
      eviction_displacement_score: 50.0,
      anti_ziganism_state_complicity_score: 53.0,
      rights_protection_enforcement_deficit_score: 51.0,
      composite_score: 52.8,
      risk_level: "élevé",
      primary_pattern: "90 000 cas stérilisations forcées documentés, indemnisations 2021 partielles, mémoire collective niée, ségrégation persistante",
      estimated_romani_rights_index: 5.28,
      last_updated: "2026-06-21",
    },
    {
      id: "RSA-006",
      name: "Roumanie — Exclusion Sanitaire COVID, Logement Sous-Standard",
      country: "Roumanie",
      segregation_exclusion_score: 49.0,
      eviction_displacement_score: 46.0,
      anti_ziganism_state_complicity_score: 47.0,
      rights_protection_enforcement_deficit_score: 45.0,
      composite_score: 47.0,
      risk_level: "élevé",
      primary_pattern: "Discrimination accès vaccins COVID, logement sous-standard 85% Roms ruraux, exclusion système santé, pauvreté 80%",
      estimated_romani_rights_index: 4.7,
      last_updated: "2026-06-21",
    },
    {
      id: "RSA-007",
      name: "Espagne — Plan Inclusion Nationale PNAIN 2021-2030",
      country: "Espagne",
      segregation_exclusion_score: 26.0,
      eviction_displacement_score: 24.0,
      anti_ziganism_state_complicity_score: 25.0,
      rights_protection_enforcement_deficit_score: 23.0,
      composite_score: 24.85,
      risk_level: "modéré",
      primary_pattern: "PNAIN 2021-2030 actif, accès école 85% enfants roms, institutions romani cultura, discrimination résiduelle marché travail",
      estimated_romani_rights_index: 2.49,
      last_updated: "2026-06-21",
    },
    {
      id: "RSA-008",
      name: "Finlande — Roms Citoyens Intégrés, Programme Culture & Langue",
      country: "Finlande",
      segregation_exclusion_score: 8.0,
      eviction_displacement_score: 7.0,
      anti_ziganism_state_complicity_score: 8.0,
      rights_protection_enforcement_deficit_score: 9.0,
      composite_score: 7.95,
      risk_level: "faible",
      primary_pattern: "Programme national langue romani, discrimination réduite, citoyenneté pleine, conseil consultatif roms gouvernemental",
      estimated_romani_rights_index: 0.8,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/romani-sinti-anti-ziganism-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
