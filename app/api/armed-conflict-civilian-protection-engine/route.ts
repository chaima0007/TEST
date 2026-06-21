import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[armed-conflict-civilian-protection-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Armed Conflict Civilian Protection Engine Agent",
  domain: "armed_conflict_civilian_protection",
  total_entities: 8,
  avg_composite: 61.98,
  confidence_score: 0.87,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    civilian_targeting_indiscriminate_attack_severity: 3,
    siege_starvation_collective_punishment_scale: 2,
    hospital_school_infrastructure_attack: 1,
    humanitarian_access_aid_blockage_deficit_gap: 2,
  },
  top_risk_entities: [
    "Gaza/Israël 2023-24 — 40 000 Civils Tués, 70% Femmes/Enfants, Hôpitaux Bombardés & Blocus Humanitaire Total",
    "Syrie/Assad-Russie — 500 000 Morts Civils, Barils Explosifs Alep, Hôpitaux M2020 Ciblés & Chlore Attaques Chimiques",
    "Yemen/Coalition — 24 000 Frappes Documentées, Mariages/Funérailles Bombardés, Blocus Port Hodeidah & Choléra 2.5M Cas",
  ],
  critical_alerts: [
    "Palestine: civilian_targeting_indiscriminate_attack_severity",
    "Syrie: siege_starvation_collective_punishment_scale",
    "Yemen: humanitarian_access_aid_blockage_deficit_gap",
    "Ukraine: civilian_targeting_indiscriminate_attack_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_armed_conflict_civilian_protection_index: 6.20,
  data_sources: [
    "icrc_international_humanitarian_law_report",
    "airwaves_civilian_harm_monitoring_report",
    "un_ocha_humanitarian_access_report",
  ],
  entities: [
    {
      entity_id: "ACP-001",
      name: "Gaza/Israël 2023-24 — 40 000 Civils Tués, 70% Femmes/Enfants, Hôpitaux Bombardés & Blocus Humanitaire Total",
      country: "Palestine",
      civilian_targeting_indiscriminate_attack_severity_score: 96.0,
      siege_starvation_collective_punishment_scale_score: 94.0,
      hospital_school_infrastructure_attack_score: 95.0,
      humanitarian_access_aid_blockage_deficit_gap_score: 93.0,
      composite_score: 94.65,
      risk_level: "critique",
      primary_pattern: "civilian_targeting_indiscriminate_attack_severity",
      estimated_armed_conflict_civilian_protection_index: 9.46,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ACP-002",
      name: "Syrie/Assad-Russie — 500 000 Morts Civils, Barils Explosifs Alep, Hôpitaux M2020 Ciblés & Chlore Attaques Chimiques",
      country: "Syrie",
      civilian_targeting_indiscriminate_attack_severity_score: 92.0,
      siege_starvation_collective_punishment_scale_score: 93.0,
      hospital_school_infrastructure_attack_score: 90.0,
      humanitarian_access_aid_blockage_deficit_gap_score: 91.0,
      composite_score: 91.55,
      risk_level: "critique",
      primary_pattern: "siege_starvation_collective_punishment_scale",
      estimated_armed_conflict_civilian_protection_index: 9.15,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ACP-003",
      name: "Yemen/Coalition — 24 000 Frappes Documentées, Mariages/Funérailles Bombardés, Blocus Port Hodeidah & Choléra 2.5M Cas",
      country: "Yemen",
      civilian_targeting_indiscriminate_attack_severity_score: 88.0,
      siege_starvation_collective_punishment_scale_score: 86.0,
      hospital_school_infrastructure_attack_score: 89.0,
      humanitarian_access_aid_blockage_deficit_gap_score: 87.0,
      composite_score: 87.55,
      risk_level: "critique",
      primary_pattern: "humanitarian_access_aid_blockage_deficit_gap",
      estimated_armed_conflict_civilian_protection_index: 8.75,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ACP-004",
      name: "Ukraine/Russie — Bucha Massacres, Zaporizhzhia Centrales Nucléaires Ciblées, Missiles Résidentiels & Déportations Forcées Enfants",
      country: "Ukraine",
      civilian_targeting_indiscriminate_attack_severity_score: 84.0,
      siege_starvation_collective_punishment_scale_score: 82.0,
      hospital_school_infrastructure_attack_score: 85.0,
      humanitarian_access_aid_blockage_deficit_gap_score: 83.0,
      composite_score: 83.55,
      risk_level: "critique",
      primary_pattern: "civilian_targeting_indiscriminate_attack_severity",
      estimated_armed_conflict_civilian_protection_index: 8.36,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ACP-005",
      name: "Myanmar/Tatmadaw — Villages Brûlés Civils, Jade/Chin Populations Ciblées, Aide Bloquée & Médecins Arrêtés",
      country: "Myanmar",
      civilian_targeting_indiscriminate_attack_severity_score: 56.0,
      siege_starvation_collective_punishment_scale_score: 54.0,
      hospital_school_infrastructure_attack_score: 55.0,
      humanitarian_access_aid_blockage_deficit_gap_score: 57.0,
      composite_score: 55.45,
      risk_level: "élevé",
      primary_pattern: "hospital_school_infrastructure_attack",
      estimated_armed_conflict_civilian_protection_index: 5.54,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ACP-006",
      name: "Éthiopie/Tigré — Blocus Alimentaire 900 Jours, Massacres Axum/Mahbere Dego, Accès Humanitaire Refusé & Violences Sexuelles Arme Guerre",
      country: "Éthiopie",
      civilian_targeting_indiscriminate_attack_severity_score: 53.0,
      siege_starvation_collective_punishment_scale_score: 51.0,
      hospital_school_infrastructure_attack_score: 54.0,
      humanitarian_access_aid_blockage_deficit_gap_score: 52.0,
      composite_score: 52.55,
      risk_level: "élevé",
      primary_pattern: "siege_starvation_collective_punishment_scale",
      estimated_armed_conflict_civilian_protection_index: 5.25,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ACP-007",
      name: "CICR/MSF — Droit International Humanitaire, Médecins Sans Frontières Protection & Comité CICR Supervision Conflits Armés",
      country: "Global",
      civilian_targeting_indiscriminate_attack_severity_score: 27.0,
      siege_starvation_collective_punishment_scale_score: 25.0,
      hospital_school_infrastructure_attack_score: 28.0,
      humanitarian_access_aid_blockage_deficit_gap_score: 26.0,
      composite_score: 26.55,
      risk_level: "modéré",
      primary_pattern: "humanitarian_access_aid_blockage_deficit_gap",
      estimated_armed_conflict_civilian_protection_index: 2.66,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ACP-008",
      name: "ONU/Genève IV — Conventions Genève 1949 & Protocoles Additionnels, Rome Statute ICC & Standards DIH Minimaux",
      country: "Global",
      civilian_targeting_indiscriminate_attack_severity_score: 4.0,
      siege_starvation_collective_punishment_scale_score: 4.0,
      hospital_school_infrastructure_attack_score: 4.0,
      humanitarian_access_aid_blockage_deficit_gap_score: 4.0,
      composite_score: 4.0,
      risk_level: "faible",
      primary_pattern: "civilian_targeting_indiscriminate_attack_severity",
      estimated_armed_conflict_civilian_protection_index: 0.4,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/armed-conflict-civilian-protection-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
