import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sexual-violence-conflict-impunity-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Sexual Violence Conflict Impunity Engine Agent",
  domain: "sexual_violence_conflict_impunity",
  total_entities: 8,
  avg_composite: 63.51,
  confidence_score: 0.89,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { systematic_rape_weapon_of_war: 2, impunity_perpetrators_justice_gap: 2, survivor_stigma_secondary_victimization: 2, documentation_prosecution_failure: 2 },
  top_risk_entities: [
    "RDC — Viol de Masse Systématique Est-Congo, Militia M23, 400000+ Victimes & Quasi-Zéro Condamnation",
    "Soudan/Darfour — MSF Viol Arme Guerre RSF Milices, Camps Réfugiés Attaqués & Impunité Commandants",
    "Myanmar/Rohingya — Viol Génocidaire 2017, Soldats Tatmadaw, ONU Preuves Documentées & Aucun Jugement CPI",
  ],
  critical_alerts: [
    "RDC: systematic_rape_weapon_of_war",
    "Soudan: impunity_perpetrators_justice_gap",
    "Myanmar: systematic_rape_weapon_of_war",
    "Syrie: documentation_prosecution_failure",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_sexual_violence_conflict_impunity_index: 6.35,
  data_sources: [
    "un_action_sexual_violence_conflict_annual_report_2023",
    "human_rights_watch_sexual_violence_conflict_2023",
    "icc_sexual_gender_based_crimes_protocol_2023",
    "un_women_report_sexual_violence_armed_conflict_2023",
  ],
  entities: [
    { entity_id: "SVC-001", name: "RDC — Viol de Masse Systématique Est-Congo, Militia M23, 400000+ Victimes & Quasi-Zéro Condamnation", country: "Afrique Centrale", composite_score: 95.55, systematic_rape_weapon_of_war_score: 97.0, impunity_perpetrators_justice_gap_score: 96.0, survivor_stigma_secondary_victimization_score: 94.0, documentation_prosecution_failure_score: 95.0, risk_level: "critique", primary_pattern: "systematic_rape_weapon_of_war", estimated_sexual_violence_conflict_impunity_index: 9.56, last_updated: "2026-06-21" },
    { entity_id: "SVC-002", name: "Soudan/Darfour — MSF Viol Arme Guerre RSF Milices, Camps Réfugiés Attaqués & Impunité Commandants", country: "Afrique du Nord-Est", composite_score: 91.35, systematic_rape_weapon_of_war_score: 93.0, impunity_perpetrators_justice_gap_score: 92.0, survivor_stigma_secondary_victimization_score: 89.0, documentation_prosecution_failure_score: 91.0, risk_level: "critique", primary_pattern: "impunity_perpetrators_justice_gap", estimated_sexual_violence_conflict_impunity_index: 9.14, last_updated: "2026-06-21" },
    { entity_id: "SVC-003", name: "Myanmar/Rohingya — Viol Génocidaire 2017, Soldats Tatmadaw, ONU Preuves Documentées & Aucun Jugement CPI", country: "Asie du Sud-Est", composite_score: 87.85, systematic_rape_weapon_of_war_score: 89.0, impunity_perpetrators_justice_gap_score: 88.0, survivor_stigma_secondary_victimization_score: 86.0, documentation_prosecution_failure_score: 88.0, risk_level: "critique", primary_pattern: "systematic_rape_weapon_of_war", estimated_sexual_violence_conflict_impunity_index: 8.79, last_updated: "2026-06-21" },
    { entity_id: "SVC-004", name: "Syrie — Daech Esclavage Sexuel Yézidies, Assad Centres Détention Viols, Documentation ONU & Impunité Totale", country: "Moyen-Orient", composite_score: 84.05, systematic_rape_weapon_of_war_score: 85.0, impunity_perpetrators_justice_gap_score: 85.0, survivor_stigma_secondary_victimization_score: 82.0, documentation_prosecution_failure_score: 84.0, risk_level: "critique", primary_pattern: "documentation_prosecution_failure", estimated_sexual_violence_conflict_impunity_index: 8.41, last_updated: "2026-06-21" },
    { entity_id: "SVC-005", name: "Éthiopie/Tigray — Viol de Masse ENDF et Érythrée 2020-2022, HRW Preuves, 500000+ Victimes Estimées & Impunité", country: "Afrique de l'Est", composite_score: 55.95, systematic_rape_weapon_of_war_score: 56.0, impunity_perpetrators_justice_gap_score: 57.0, survivor_stigma_secondary_victimization_score: 54.0, documentation_prosecution_failure_score: 56.0, risk_level: "élevé", primary_pattern: "impunity_perpetrators_justice_gap", estimated_sexual_violence_conflict_impunity_index: 5.60, last_updated: "2026-06-21" },
    { entity_id: "SVC-006", name: "Ukraine — Viols Documentés Occupation Russe, Commissions ONU, Preuves Collectées & Poursuites CPI en Cours", country: "Europe de l'Est", composite_score: 52.35, systematic_rape_weapon_of_war_score: 52.0, impunity_perpetrators_justice_gap_score: 53.0, survivor_stigma_secondary_victimization_score: 51.0, documentation_prosecution_failure_score: 53.0, risk_level: "élevé", primary_pattern: "documentation_prosecution_failure", estimated_sexual_violence_conflict_impunity_index: 5.24, last_updated: "2026-06-21" },
    { entity_id: "SVC-007", name: "ONU Action VSC — Représentante Spéciale Pramila Patten, Monitoring 20 Conflits & Mécanismes Accountability", country: "Global", composite_score: 27.05, systematic_rape_weapon_of_war_score: 27.0, impunity_perpetrators_justice_gap_score: 28.0, survivor_stigma_secondary_victimization_score: 26.0, documentation_prosecution_failure_score: 27.0, risk_level: "modéré", primary_pattern: "survivor_stigma_secondary_victimization", estimated_sexual_violence_conflict_impunity_index: 2.71, last_updated: "2026-06-21" },
    { entity_id: "SVC-008", name: "CPI/Protocole SGBC — Crimes Sexuels Droit International, Jurisprudence TPIY/TPIR, Protocole Budapest & Standards ICC", country: "Global", composite_score: 6.85, systematic_rape_weapon_of_war_score: 7.0, impunity_perpetrators_justice_gap_score: 7.0, survivor_stigma_secondary_victimization_score: 6.0, documentation_prosecution_failure_score: 7.0, risk_level: "faible", primary_pattern: "documentation_prosecution_failure", estimated_sexual_violence_conflict_impunity_index: 0.69, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/sexual-violence-conflict-impunity-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
