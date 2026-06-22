import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[toxic-waste-environmental-racism-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Toxic Waste Environmental Racism Rights Engine Agent",
  domain: "toxic_waste_environmental_racism_rights",
  total_entities: 8,
  avg_composite: 59.14,
  confidence_score: 0.87,
  avg_estimated_toxic_waste_environmental_racism_rights_index: 5.91,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_sr_toxics_report_2023",
    "hrw_environmental_racism_2022",
    "earthjustice_environmental_justice_2023",
    "who_chemical_waste_health_2022",
  ],
  critical_alerts: [
    "Nigeria: proximite_dechets_toxiques_communautes_marginalisees",
    "Ghana: impunite_entreprises_defaillance_reglementaire",
    "USA: impacts_sanitaires_communautes_noires",
    "Inde: contamination_chronique_post_1984",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  entities: [
    {
      id: "TWR-001",
      name: "Nigeria (Delta du Niger) — déversements pétroliers Shell/Chevron, communautés Ogoni et Ijaw",
      country: "Nigeria",
      proximite_dechets_toxiques_communautes_marginalisees_score: 95.0,
      impunite_entreprises_defaillance_reglementaire_score: 90.0,
      impacts_sanitaires_acces_soins_populations_exposees_score: 88.0,
      capacite_recours_juridique_representation_victimes_score: 85.0,
      composite_score: 90.00,
      risk_level: "critique",
      primary_pattern: "proximite_dechets_toxiques_communautes_marginalisees",
      estimated_toxic_waste_environmental_racism_rights_index: 9.00,
      last_updated: "2026-06-21",
    },
    {
      id: "TWR-002",
      name: "Ghana (Agbogbloshie) — décharge e-waste, travailleurs informels et plomb atmosphérique",
      country: "Ghana",
      proximite_dechets_toxiques_communautes_marginalisees_score: 88.0,
      impunite_entreprises_defaillance_reglementaire_score: 84.0,
      impacts_sanitaires_acces_soins_populations_exposees_score: 86.0,
      capacite_recours_juridique_representation_victimes_score: 78.0,
      composite_score: 84.50,
      risk_level: "critique",
      primary_pattern: "impacts_sanitaires_acces_soins_populations_exposees",
      estimated_toxic_waste_environmental_racism_rights_index: 8.45,
      last_updated: "2026-06-21",
    },
    {
      id: "TWR-003",
      name: "États-Unis (Cancer Alley, Louisiane) — complexe pétrochimique, communautés noires rurales",
      country: "États-Unis",
      proximite_dechets_toxiques_communautes_marginalisees_score: 80.0,
      impunite_entreprises_defaillance_reglementaire_score: 75.0,
      impacts_sanitaires_acces_soins_populations_exposees_score: 82.0,
      capacite_recours_juridique_representation_victimes_score: 70.0,
      composite_score: 77.25,
      risk_level: "critique",
      primary_pattern: "impacts_sanitaires_acces_soins_populations_exposees",
      estimated_toxic_waste_environmental_racism_rights_index: 7.72,
      last_updated: "2026-06-21",
    },
    {
      id: "TWR-004",
      name: "Inde (Bhopal, Madhya Pradesh) — héritage Union Carbide, contamination chronique post-1984",
      country: "Inde",
      proximite_dechets_toxiques_communautes_marginalisees_score: 78.0,
      impunite_entreprises_defaillance_reglementaire_score: 80.0,
      impacts_sanitaires_acces_soins_populations_exposees_score: 76.0,
      capacite_recours_juridique_representation_victimes_score: 72.0,
      composite_score: 76.80,
      risk_level: "critique",
      primary_pattern: "impunite_entreprises_defaillance_reglementaire",
      estimated_toxic_waste_environmental_racism_rights_index: 7.68,
      last_updated: "2026-06-21",
    },
    {
      id: "TWR-005",
      name: "Zambie (Copperbelt) — contamination au plomb et au cuivre autour des mines Glencore",
      country: "Zambie",
      proximite_dechets_toxiques_communautes_marginalisees_score: 55.0,
      impunite_entreprises_defaillance_reglementaire_score: 52.0,
      impacts_sanitaires_acces_soins_populations_exposees_score: 58.0,
      capacite_recours_juridique_representation_victimes_score: 46.0,
      composite_score: 53.20,
      risk_level: "élevé",
      primary_pattern: "impacts_sanitaires_acces_soins_populations_exposees",
      estimated_toxic_waste_environmental_racism_rights_index: 5.32,
      last_updated: "2026-06-21",
    },
    {
      id: "TWR-006",
      name: "Brésil (Complexe de Cubatão) — pollution industrielle, communautés riveraines pauvres",
      country: "Brésil",
      proximite_dechets_toxiques_communautes_marginalisees_score: 50.0,
      impunite_entreprises_defaillance_reglementaire_score: 48.0,
      impacts_sanitaires_acces_soins_populations_exposees_score: 52.0,
      capacite_recours_juridique_representation_victimes_score: 44.0,
      composite_score: 48.80,
      risk_level: "élevé",
      primary_pattern: "proximite_dechets_toxiques_communautes_marginalisees",
      estimated_toxic_waste_environmental_racism_rights_index: 4.88,
      last_updated: "2026-06-21",
    },
    {
      id: "TWR-007",
      name: "Roumanie (Copsa Mica) — héritage industriel soviet, minorité rom surexposée",
      country: "Roumanie",
      proximite_dechets_toxiques_communautes_marginalisees_score: 32.0,
      impunite_entreprises_defaillance_reglementaire_score: 30.0,
      impacts_sanitaires_acces_soins_populations_exposees_score: 28.0,
      capacite_recours_juridique_representation_victimes_score: 26.0,
      composite_score: 29.30,
      risk_level: "modéré",
      primary_pattern: "proximite_dechets_toxiques_communautes_marginalisees",
      estimated_toxic_waste_environmental_racism_rights_index: 2.93,
      last_updated: "2026-06-21",
    },
    {
      id: "TWR-008",
      name: "Pays-Bas (Rotterdam) — exposition portuaire, cadre réglementaire UE protecteur",
      country: "Pays-Bas",
      proximite_dechets_toxiques_communautes_marginalisees_score: 14.0,
      impunite_entreprises_defaillance_reglementaire_score: 10.0,
      impacts_sanitaires_acces_soins_populations_exposees_score: 12.0,
      capacite_recours_juridique_representation_victimes_score: 18.0,
      composite_score: 13.30,
      risk_level: "faible",
      primary_pattern: "capacite_recours_juridique_representation_victimes",
      estimated_toxic_waste_environmental_racism_rights_index: 1.33,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/toxic-waste-environmental-racism-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
