import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[journalism-safety-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Journalism Safety Rights Engine Agent",
  domain: "journalism_safety_rights",
  total_entities: 8,
  avg_composite: 60.04,
  confidence_score: 0.88,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    journalist_killings: 3,
    arbitrary_detention_press: 2,
    surveillance_intimidation: 2,
    censorship_suppression: 1,
  },
  top_risk_entities: [
    "Chine — 108 Journalistes Emprisonnés, Grand Pare-feu & Surveillance Pegasus/Spyware Ciblée",
    "Mexique — Pays le Plus Meurtrier Hors Zone Guerre, 15+ Journalistes Tués/An & Impunité Cartels",
    "Russie — Journalistes Emprisonnés, Novaya Gazeta & Assassinats d'État Documentés",
  ],
  critical_alerts: [
    "Mexique — Pays le Plus Meurtrier Hors Zone Guerre, 15+ Journalistes Tués/An & Impunité Cartels: journalist_killings",
    "Russie — Journalistes Emprisonnés, Novaya Gazeta & Assassinats d'État Documentés: arbitrary_detention_press",
    "Chine — 108 Journalistes Emprisonnés, Grand Pare-feu & Surveillance Pegasus/Spyware Ciblée: arbitrary_detention_press",
    "Syrie — Guerre la Plus Meurtrière pour la Presse, 150+ Journalistes Tués & Impunité Totale: journalist_killings",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_journalism_safety_rights_index: 6.0,
  data_sources: [
    "rsf_world_press_freedom_index_2024",
    "cpj_journalists_imprisoned_database_2024",
    "cpj_journalists_killed_database_2024",
    "citizen_lab_surveillance_reports_2024",
    "case_anti_slapp_observatory_europe_2024",
  ],
  entities: [
    {
      entity_id: "JSR-001",
      name: "Mexique — Pays le Plus Meurtrier Hors Zone Guerre, 15+ Journalistes Tués/An & Impunité Cartels",
      country: "Mexique",
      sector: "15+ journalistes tués par an CPJ 2023-2024, impunité 95% meurtres journalistes",
      composite_score: 86.65,
      journalist_killings_score: 95.0,
      arbitrary_detention_press_score: 78.0,
      censorship_suppression_score: 82.0,
      surveillance_intimidation_score: 90.0,
      risk_level: "critique",
      primary_pattern: "journalist_killings",
      estimated_journalism_safety_rights_index: 8.67,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "JSR-002",
      name: "Russie — Journalistes Emprisonnés, Novaya Gazeta & Assassinats d'État Documentés",
      country: "Russie",
      sector: "64 journalistes emprisonnés CPJ 2024, Novaya Gazeta suspendu 2022, Evan Gershkovich WSJ 16 mois détention",
      composite_score: 89.7,
      journalist_killings_score: 84.0,
      arbitrary_detention_press_score: 92.0,
      censorship_suppression_score: 93.0,
      surveillance_intimidation_score: 89.0,
      risk_level: "critique",
      primary_pattern: "arbitrary_detention_press",
      estimated_journalism_safety_rights_index: 8.97,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "JSR-003",
      name: "Chine — 108 Journalistes Emprisonnés, Grand Pare-feu & Surveillance Pegasus/Spyware Ciblée",
      country: "Chine",
      sector: "108 journalistes emprisonnés CPJ 2024 (plus grand geôlier mondial), Grand Pare-feu censurant 70% internet mondial",
      composite_score: 87.95,
      journalist_killings_score: 65.0,
      arbitrary_detention_press_score: 95.0,
      censorship_suppression_score: 98.0,
      surveillance_intimidation_score: 92.0,
      risk_level: "critique",
      primary_pattern: "arbitrary_detention_press",
      estimated_journalism_safety_rights_index: 8.8,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "JSR-004",
      name: "Syrie — Guerre la Plus Meurtrière pour la Presse, 150+ Journalistes Tués & Impunité Totale",
      country: "Syrie",
      sector: "150+ journalistes tués depuis 2011 CPJ, conflit armé le plus meurtrier pour la presse de l'histoire récente",
      composite_score: 83.45,
      journalist_killings_score: 92.0,
      arbitrary_detention_press_score: 82.0,
      censorship_suppression_score: 76.0,
      surveillance_intimidation_score: 79.0,
      risk_level: "critique",
      primary_pattern: "journalist_killings",
      estimated_journalism_safety_rights_index: 8.35,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "JSR-005",
      name: "Arabie Saoudite — Jamal Khashoggi, Journalistes Critiques Emprisonnés & Surveillance MBS",
      country: "Arabie Saoudite",
      sector: "Assassinat Jamal Khashoggi consulat Istanbul octobre 2018, surveillance Pegasus activistes/journalistes confirmée Citizen Lab",
      composite_score: 59.75,
      journalist_killings_score: 55.0,
      arbitrary_detention_press_score: 62.0,
      censorship_suppression_score: 58.0,
      surveillance_intimidation_score: 65.0,
      risk_level: "élevé",
      primary_pattern: "surveillance_intimidation",
      estimated_journalism_safety_rights_index: 5.98,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "JSR-006",
      name: "Inde — RSF Rang 159/180, UAPA Contre Journalistes Kashmir & Climat d'Autocensure",
      country: "Inde",
      sector: "RSF classement 159/180 en 2024, UAPA utilisé contre journalistes kashmiris, Siddique Kappan détenu 28 mois",
      composite_score: 50.0,
      journalist_killings_score: 45.0,
      arbitrary_detention_press_score: 52.0,
      censorship_suppression_score: 55.0,
      surveillance_intimidation_score: 48.0,
      risk_level: "élevé",
      primary_pattern: "censorship_suppression",
      estimated_journalism_safety_rights_index: 5.0,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "JSR-007",
      name: "UE — Daphne Caruana Galizia (Malte), SLAPP & Journalistes d'Investigation Menacés",
      country: "Union Européenne (Malte/Bulgarie)",
      sector: "Assassinat Daphne Caruana Galizia Malte octobre 2017, 570 procédures SLAPP contre journalistes EU documentées CASE 2024",
      composite_score: 24.5,
      journalist_killings_score: 20.0,
      arbitrary_detention_press_score: 22.0,
      censorship_suppression_score: 28.0,
      surveillance_intimidation_score: 30.0,
      risk_level: "modéré",
      primary_pattern: "surveillance_intimidation",
      estimated_journalism_safety_rights_index: 2.45,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "JSR-008",
      name: "Norvège/Finlande/Danemark — RSF Rang 1-3, Protection Presse & Meilleure Pratique Mondiale",
      country: "Scandinavie",
      sector: "Norvège RSF rang 1/180, Finlande RSF rang 2/180, Danemark RSF rang 3/180 en 2024, aucun journaliste emprisonné",
      composite_score: 1.7,
      journalist_killings_score: 1.0,
      arbitrary_detention_press_score: 2.0,
      censorship_suppression_score: 1.0,
      surveillance_intimidation_score: 3.0,
      risk_level: "faible",
      primary_pattern: "journalist_killings",
      estimated_journalism_safety_rights_index: 0.17,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/api/journalism-safety-rights-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
