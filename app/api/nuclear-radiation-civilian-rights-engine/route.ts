import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[nuclear-radiation-civilian-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Nuclear Radiation Civilian Rights Engine Agent",
  domain: "nuclear_radiation_civilian_rights",
  total_entities: 8,
  avg_composite: 61.58,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    nuclear_testing_civilian_contamination_severity: 3,
    nuclear_waste_indigenous_land_disposal: 2,
    reactor_accident_compensation_denial_scale: 1,
    radiation_information_transparency_deficit_gap: 2,
  },
  top_risk_entities: [
    "France/Polynésie — 193 Essais Nucléaires Polynésie, Vétérans Irradiés Non Indemnisés, Cancers Cachés & Dépollution Refusée",
    "USA/Marshall Islands — Bikini Atoll 67 Tests, Populations Déplacées Non Retournables, Castle Bravo & Fonds Compensation Épuisé",
    "URSS/Kazakhstan — Semipalatinsk 456 Essais, 1.5M Exposés, Maladies Génération & Dépollution Insuffisante Post-URSS",
  ],
  critical_alerts: [
    "France/Polynésie: nuclear_testing_civilian_contamination_severity",
    "USA/Marshall Islands: nuclear_waste_indigenous_land_disposal",
    "URSS/Kazakhstan: nuclear_testing_civilian_contamination_severity",
    "Japon/Fukushima: reactor_accident_compensation_denial_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_nuclear_radiation_civilian_rights_index: 6.16,
  data_sources: [
    "greenpeace_nuclear_testing_contamination_report",
    "ippnw_nuclear_weapons_humanitarian_impact_study",
    "iaea_radiation_protection_standards_review",
  ],
  entities: [
    {
      id: "NRC-001",
      name: "France/Polynésie — 193 Essais Nucléaires Polynésie, Vétérans Irradiés Non Indemnisés, Cancers Cachés & Dépollution Refusée",
      country: "France/Polynésie",
      nuclear_testing_civilian_contamination_severity_score: 95.0,
      reactor_accident_compensation_denial_scale_score: 93.0,
      nuclear_waste_indigenous_land_disposal_score: 93.0,
      radiation_information_transparency_deficit_gap_score: 91.0,
      composite_score: 93.2,
      risk_level: "critique",
      primary_pattern: "nuclear_testing_civilian_contamination_severity",
      estimated_nuclear_radiation_civilian_rights_index: 9.32,
      last_updated: "2026-06-21",
    },
    {
      id: "NRC-002",
      name: "USA/Marshall Islands — Bikini Atoll 67 Tests, Populations Déplacées Non Retournables, Castle Bravo & Fonds Compensation Épuisé",
      country: "USA/Marshall Islands",
      nuclear_testing_civilian_contamination_severity_score: 92.0,
      reactor_accident_compensation_denial_scale_score: 90.0,
      nuclear_waste_indigenous_land_disposal_score: 90.0,
      radiation_information_transparency_deficit_gap_score: 88.0,
      composite_score: 90.2,
      risk_level: "critique",
      primary_pattern: "nuclear_waste_indigenous_land_disposal",
      estimated_nuclear_radiation_civilian_rights_index: 9.02,
      last_updated: "2026-06-21",
    },
    {
      id: "NRC-003",
      name: "URSS/Kazakhstan — Semipalatinsk 456 Essais, 1.5M Exposés, Maladies Génération & Dépollution Insuffisante Post-URSS",
      country: "Kazakhstan",
      nuclear_testing_civilian_contamination_severity_score: 89.0,
      reactor_accident_compensation_denial_scale_score: 87.0,
      nuclear_waste_indigenous_land_disposal_score: 87.0,
      radiation_information_transparency_deficit_gap_score: 85.0,
      composite_score: 87.2,
      risk_level: "critique",
      primary_pattern: "nuclear_testing_civilian_contamination_severity",
      estimated_nuclear_radiation_civilian_rights_index: 8.72,
      last_updated: "2026-06-21",
    },
    {
      id: "NRC-004",
      name: "Japon/Fukushima — Évacuations Forcées 154 000, Compensation Tepco Insuffisante, Eaux Traitées Pacifique & Zones Exclusion",
      country: "Japon",
      nuclear_testing_civilian_contamination_severity_score: 86.0,
      reactor_accident_compensation_denial_scale_score: 84.0,
      nuclear_waste_indigenous_land_disposal_score: 84.0,
      radiation_information_transparency_deficit_gap_score: 82.0,
      composite_score: 84.2,
      risk_level: "critique",
      primary_pattern: "reactor_accident_compensation_denial_scale",
      estimated_nuclear_radiation_civilian_rights_index: 8.42,
      last_updated: "2026-06-21",
    },
    {
      id: "NRC-005",
      name: "Inde/Pakistan — Tests Pokhran/Chagai Sans TICE, Mines Uranium Travailleurs Exposés, Prolifération & Sans Traité Interdiction",
      country: "Inde/Pakistan",
      nuclear_testing_civilian_contamination_severity_score: 57.0,
      reactor_accident_compensation_denial_scale_score: 55.0,
      nuclear_waste_indigenous_land_disposal_score: 55.0,
      radiation_information_transparency_deficit_gap_score: 53.0,
      composite_score: 55.2,
      risk_level: "élevé",
      primary_pattern: "radiation_information_transparency_deficit_gap",
      estimated_nuclear_radiation_civilian_rights_index: 5.52,
      last_updated: "2026-06-21",
    },
    {
      id: "NRC-006",
      name: "Australie — Essais Maralinga Aborigènes Exposés, Décontamination Incomplète, Veterans Irradiés & Uranium Mines Kakadu",
      country: "Australie",
      nuclear_testing_civilian_contamination_severity_score: 54.0,
      reactor_accident_compensation_denial_scale_score: 52.0,
      nuclear_waste_indigenous_land_disposal_score: 52.0,
      radiation_information_transparency_deficit_gap_score: 50.0,
      composite_score: 52.2,
      risk_level: "élevé",
      primary_pattern: "nuclear_waste_indigenous_land_disposal",
      estimated_nuclear_radiation_civilian_rights_index: 5.22,
      last_updated: "2026-06-21",
    },
    {
      id: "NRC-007",
      name: "AIEA/IPPNW — Normes Radioprotection, Médecins Prevention Guerre Nucléaire & Traité Interdiction Armes Nucléaires 2017",
      country: "Global",
      nuclear_testing_civilian_contamination_severity_score: 27.0,
      reactor_accident_compensation_denial_scale_score: 26.0,
      nuclear_waste_indigenous_land_disposal_score: 26.0,
      radiation_information_transparency_deficit_gap_score: 25.0,
      composite_score: 26.1,
      risk_level: "modéré",
      primary_pattern: "nuclear_testing_civilian_contamination_severity",
      estimated_nuclear_radiation_civilian_rights_index: 2.61,
      last_updated: "2026-06-21",
    },
    {
      id: "NRC-008",
      name: "ONU/TNP — Traité Non-Prolifération, TICE Moratoire, Article VI Désarmement & SDG 16 Paix Justice",
      country: "Global",
      nuclear_testing_civilian_contamination_severity_score: 5.0,
      reactor_accident_compensation_denial_scale_score: 4.0,
      nuclear_waste_indigenous_land_disposal_score: 4.0,
      radiation_information_transparency_deficit_gap_score: 4.0,
      composite_score: 4.3,
      risk_level: "faible",
      primary_pattern: "radiation_information_transparency_deficit_gap",
      estimated_nuclear_radiation_civilian_rights_index: 0.43,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/nuclear-radiation-civilian-rights-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
