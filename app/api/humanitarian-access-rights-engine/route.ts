import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[humanitarian-access-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Humanitarian Access Rights Engine Agent",
  domain: "humanitarian_access_rights",
  total_entities: 8,
  avg_composite: 62.94,
  confidence_score: 0.89,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    civilian_siege: 2,
    aid_blockade: 4,
    humanitarian_worker_attacks: 2,
  },
  top_risk_entities: [
    "Gaza/Palestine — Blocus Total, 0 Aide Humanitaire & Hôpitaux Bombardés, Famine Artificielle",
    "Soudan — Blocage Aide Darfour/Khartoum, MSF Expulsé & Famine Artificielle RSF/SAF",
    "Myanmar — Armée Bloquant CICR, Rakhine/Chin States & Criminalisation Aide Humanitaire",
  ],
  critical_alerts: [
    "Gaza/Palestine — Blocus Total, 0 Aide Humanitaire & Hôpitaux Bombardés, Famine Artificielle: civilian_siege",
    "Soudan — Blocage Aide Darfour/Khartoum, MSF Expulsé & Famine Artificielle RSF/SAF: aid_blockade",
    "Yémen — Coalition Saoudienne Bloquant Ports, ONU Empêchée & Famine Structurelle: aid_blockade",
    "Myanmar — Armée Bloquant CICR, Rakhine/Chin States & Criminalisation Aide Humanitaire: aid_blockade",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_humanitarian_access_rights_index: 6.29,
  data_sources: [
    "ocha_humanitarian_access_monitoring_2024",
    "icrc_annual_report_armed_conflicts_2024",
    "msf_activity_report_2023",
    "un_security_council_resolutions_humanitarian_access",
    "who_health_cluster_attacks_on_healthcare_database",
  ],
  entities: [
    {
      entity_id: "HUA-001",
      name: "Gaza/Palestine — Blocus Total, 0 Aide Humanitaire & Hôpitaux Bombardés, Famine Artificielle",
      country: "Palestine/Gaza",
      sector: "Blocus total depuis octobre 2023, aide humanitaire zéro pendant périodes prolongées, 36 hôpitaux mis hors service OMS 2024",
      composite_score: 97.0,
      aid_blockade_score: 98.0,
      humanitarian_worker_attacks_score: 95.0,
      civilian_siege_score: 98.0,
      medical_neutrality_violation_score: 97.0,
      risk_level: "critique",
      primary_pattern: "civilian_siege",
      estimated_humanitarian_access_rights_index: 9.7,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HUA-002",
      name: "Soudan — Blocage Aide Darfour/Khartoum, MSF Expulsé & Famine Artificielle RSF/SAF",
      country: "Soudan",
      sector: "Blocus aide humanitaire Darfour/Khartoum depuis avril 2023, famine artificielle Darfour IPC phase 5",
      composite_score: 89.9,
      aid_blockade_score: 92.0,
      humanitarian_worker_attacks_score: 88.0,
      civilian_siege_score: 90.0,
      medical_neutrality_violation_score: 88.0,
      risk_level: "critique",
      primary_pattern: "aid_blockade",
      estimated_humanitarian_access_rights_index: 8.99,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HUA-003",
      name: "Yémen — Coalition Saoudienne Bloquant Ports, ONU Empêchée & Famine Structurelle",
      country: "Yémen",
      sector: "Coalition saoudienne contrôlant port Hodeida bloquant 70% importations alimentaires",
      composite_score: 80.2,
      aid_blockade_score: 84.0,
      humanitarian_worker_attacks_score: 78.0,
      civilian_siege_score: 80.0,
      medical_neutrality_violation_score: 76.0,
      risk_level: "critique",
      primary_pattern: "aid_blockade",
      estimated_humanitarian_access_rights_index: 8.02,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HUA-004",
      name: "Myanmar — Armée Bloquant CICR, Rakhine/Chin States & Criminalisation Aide Humanitaire",
      country: "Myanmar",
      sector: "Tatmadaw bloquant accès CICR et MSF depuis 2021, loi anti-terroriste criminalisant aide populations",
      composite_score: 81.85,
      aid_blockade_score: 85.0,
      humanitarian_worker_attacks_score: 80.0,
      civilian_siege_score: 82.0,
      medical_neutrality_violation_score: 78.0,
      risk_level: "critique",
      primary_pattern: "aid_blockade",
      estimated_humanitarian_access_rights_index: 8.19,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HUA-005",
      name: "Éthiopie/Tigré — Gouvernement Bloquant Convois, ONG Expulsées & Siège Délibéré",
      country: "Éthiopie",
      sector: "Gouvernement éthiopien bloquant convois humanitaires Tigré 2020-2022, 22 ONG expulsées novembre 2021",
      composite_score: 50.3,
      aid_blockade_score: 54.0,
      humanitarian_worker_attacks_score: 48.0,
      civilian_siege_score: 52.0,
      medical_neutrality_violation_score: 46.0,
      risk_level: "élevé",
      primary_pattern: "civilian_siege",
      estimated_humanitarian_access_rights_index: 5.03,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HUA-006",
      name: "Syrie — 255 Hôpitaux Bombardés (OMS), Corridors Refusés & Système Al-Nusra/Assad",
      country: "Syrie",
      sector: "255 bombardements hôpitaux documentés OMS 2012-2024, corridors humanitaires refusés par Assad et Russie",
      composite_score: 56.05,
      aid_blockade_score: 55.0,
      humanitarian_worker_attacks_score: 60.0,
      civilian_siege_score: 52.0,
      medical_neutrality_violation_score: 58.0,
      risk_level: "élevé",
      primary_pattern: "humanitarian_worker_attacks",
      estimated_humanitarian_access_rights_index: 5.61,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HUA-007",
      name: "CICR/MSF — Neutralité Humanitaire, Accès Partiel & Difficultés de Négociation Globales",
      country: "Global",
      sector: "CICR refus d'accès dans 45% des conflits actifs rapport 2024, 3 500 travailleurs humanitaires tués depuis 2000",
      composite_score: 36.1,
      aid_blockade_score: 35.0,
      humanitarian_worker_attacks_score: 42.0,
      civilian_siege_score: 30.0,
      medical_neutrality_violation_score: 38.0,
      risk_level: "modéré",
      primary_pattern: "humanitarian_worker_attacks",
      estimated_humanitarian_access_rights_index: 3.61,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HUA-008",
      name: "Ukraine — Couloirs Humanitaires Fonctionnels, Accès CICR Relatif & Meilleure Pratique",
      country: "Ukraine",
      sector: "Couloirs humanitaires négociés évacuation civils 2022-2024, aide internationale massivement mobilisée",
      composite_score: 12.6,
      aid_blockade_score: 12.0,
      humanitarian_worker_attacks_score: 15.0,
      civilian_siege_score: 10.0,
      medical_neutrality_violation_score: 14.0,
      risk_level: "faible",
      primary_pattern: "aid_blockade",
      estimated_humanitarian_access_rights_index: 1.26,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/api/humanitarian-access-rights-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
