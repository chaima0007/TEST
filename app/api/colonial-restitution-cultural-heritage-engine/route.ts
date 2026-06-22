import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[colonial-restitution-cultural-heritage-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "colonial_restitution_cultural_heritage_engine",
  domain: "colonial_restitution_cultural_heritage",
  total_entities: 8,
  avg_composite: 59.24,
  confidence_score: 0.88,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: {
    looted_objects_retained: 4,
    restitution_refusal: 2,
    colonial_accountability: 1,
    restitution_model: 1,
  },
  top_risk_entities: [
    { id: "CRC-001", name: "UK/British Museum — 900+ Bronzes Bénin, Refus Total Restitution", score: 91.95, risk: "critique" },
    { id: "CRC-002", name: "France — Têtes Maories NZ, 15 Ans Négociations, 67 Artefacts", score: 87.0, risk: "critique" },
    { id: "CRC-003", name: "Belgique/Tervuren — 120 000 Pièces Congo, Accord 2020 Lent", score: 83.2, risk: "critique" },
  ],
  critical_alerts: [
    "CRC-001: UK/British Museum — 900+ Bronzes Bénin, Refus Total Restitution — composite 91.95",
    "CRC-002: France — Têtes Maories NZ, 15 Ans Négociations, 67 Artefacts — composite 87.0",
    "CRC-003: Belgique/Tervuren — 120 000 Pièces Congo, Accord 2020 Lent — composite 83.2",
    "CRC-004: Allemagne — Benin Bronzes Restitution 2022, Modèle Partiel 20 Objets — composite 75.45",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_restitution_index: 5.92,
  data_sources: [
    "unidroit_cultural_property_convention_2023",
    "unesco_restitution_committee_2023",
    "art_loss_register_2023",
    "colonial_legacies_network_report_2023",
  ],
  entities: [
    {
      id: "CRC-001",
      name: "UK/British Museum — 900+ Bronzes Bénin, Refus Total Restitution",
      country: "Royaume-Uni",
      looted_objects_retention_score: 94.0,
      restitution_refusal_delay_score: 92.0,
      colonial_accountability_deficit_score: 91.0,
      indigenous_community_rights_score: 90.0,
      composite_score: 91.95,
      risk_level: "critique",
      primary_pattern: "900+ bronzes bénin volés expédition punitive 1897, refus restitution absolu British Museum Act 1963, Nigéria demande depuis 1960",
      estimated_restitution_index: 9.2,
      last_updated: "2026-06-21",
    },
    {
      id: "CRC-002",
      name: "France — Têtes Maories NZ, 15 Ans Négociations, 67 Artefacts",
      country: "France",
      looted_objects_retention_score: 89.0,
      restitution_refusal_delay_score: 87.0,
      colonial_accountability_deficit_score: 86.0,
      indigenous_community_rights_score: 85.0,
      composite_score: 87.0,
      risk_level: "critique",
      primary_pattern: "15 ans négociations têtes maories toi moko, 67 artefacts restitués après bataille juridique, loi spéciale nécessaire, blocage musées",
      estimated_restitution_index: 8.7,
      last_updated: "2026-06-21",
    },
    {
      id: "CRC-003",
      name: "Belgique/Tervuren — 120 000 Pièces Congo, Accord 2020 Lent",
      country: "Belgique",
      looted_objects_retention_score: 85.0,
      restitution_refusal_delay_score: 83.0,
      colonial_accountability_deficit_score: 84.0,
      indigenous_community_rights_score: 82.0,
      composite_score: 83.6,
      risk_level: "critique",
      primary_pattern: "120 000 pièces Congo musée Tervuren, accord restitution 2020 lentement exécuté, rapatriement partiel 2023, capacité stockage RDC",
      estimated_restitution_index: 8.36,
      last_updated: "2026-06-21",
    },
    {
      id: "CRC-004",
      name: "Allemagne — Benin Bronzes Restitution 2022, Modèle Partiel 20 Objets",
      country: "Allemagne",
      looted_objects_retention_score: 77.0,
      restitution_refusal_delay_score: 74.0,
      colonial_accountability_deficit_score: 76.0,
      indigenous_community_rights_score: 72.0,
      composite_score: 75.05,
      risk_level: "critique",
      primary_pattern: "20 bronzes bénin restitués 2022, modèle partiel sous pression sociétale, autres musées allemands résistants, processus fragmenté",
      estimated_restitution_index: 7.51,
      last_updated: "2026-06-21",
    },
    {
      id: "CRC-005",
      name: "Grèce/Marbres Parthénon — 200 Ans Demandes Athènes, Prêt Refusé",
      country: "Grèce/UK",
      looted_objects_retention_score: 57.0,
      restitution_refusal_delay_score: 55.0,
      colonial_accountability_deficit_score: 54.0,
      indigenous_community_rights_score: 53.0,
      composite_score: 55.0,
      risk_level: "élevé",
      primary_pattern: "200 ans demandes restitution Athènes, proposition prêt British Museum refusée, Acropolis Museum construit pour accueil, débat UE actif",
      estimated_restitution_index: 5.5,
      last_updated: "2026-06-21",
    },
    {
      id: "CRC-006",
      name: "Pays-Bas — 478 Objets Indonésie 2023, Processus Établi Modèle UE",
      country: "Pays-Bas",
      looted_objects_retention_score: 46.0,
      restitution_refusal_delay_score: 43.0,
      colonial_accountability_deficit_score: 44.0,
      indigenous_community_rights_score: 42.0,
      composite_score: 43.95,
      risk_level: "élevé",
      primary_pattern: "478 objets restitués Indonésie 2023, processus établi avec commission indépendante, modèle UE émergent, inventaire en cours",
      estimated_restitution_index: 4.4,
      last_updated: "2026-06-21",
    },
    {
      id: "CRC-007",
      name: "USA/NAGPRA — Loi 1990, 120 000 Restes Natifs Retournés",
      country: "États-Unis",
      looted_objects_retention_score: 28.0,
      restitution_refusal_delay_score: 27.0,
      colonial_accountability_deficit_score: 26.0,
      indigenous_community_rights_score: 29.0,
      composite_score: 27.45,
      risk_level: "modéré",
      primary_pattern: "NAGPRA 1990 cadre légal établi, 120 000 restes humains retournés, 800 000 objets encore évaluation, universités non-conformes",
      estimated_restitution_index: 2.75,
      last_updated: "2026-06-21",
    },
    {
      id: "CRC-008",
      name: "Allemagne/Herero Namibie — Accord 2021, Reconnaissance Génocide €1.1Md",
      country: "Allemagne/Namibie",
      looted_objects_retention_score: 10.0,
      restitution_refusal_delay_score: 9.0,
      colonial_accountability_deficit_score: 11.0,
      indigenous_community_rights_score: 10.0,
      composite_score: 10.0,
      risk_level: "faible",
      primary_pattern: "Reconnaissance génocide Herero/Nama 2021, €1.1Md réparations 30 ans, modèle mondial accountability colonial, accord historique",
      estimated_restitution_index: 1.0,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/colonial-restitution-cultural-heritage-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
