import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[arms-transfer-accountability-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Arms Transfer Accountability Engine Agent",
  domain: "arms_transfer_accountability",
  total_entities: 8,
  avg_composite: 58.13,
  confidence_score: 0.82,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { transfers_to_abusers: 1, parliamentary_oversight_absence: 4, victim_accountability_failure: 3 },
  top_risk_entities: [
    "USA — Arabie Saoudite/Israël/Égypte : 52B$/An & Complicit Yémen Gaza",
    "France — Égypte/EAU/Arabie Saoudite : Rafale & Silence des Victimes du Yémen",
    "Russie/Chine — Syrie/Myanmar/Iran : Veto ONU & Armement des Dictatures",
  ],
  critical_alerts: [
    "USA: transfers_to_abusers",
    "France: parliamentary_oversight_absence",
    "Russie/Chine: parliamentary_oversight_absence",
    "Royaume-Uni: parliamentary_oversight_absence",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_arms_transfer_accountability_index: 5.81,
  data_sources: [
    "sipri_arms_transfers_database_annual_report",
    "amnesty_international_blood_money_arms_transfers_reports",
    "un_group_of_governmental_experts_arms_transfer_transparency",
  ],
  entities: [
    {
      id: "AT-001",
      name: "USA — Arabie Saoudite/Israël/Égypte : 52B$/An & Complicit Yémen Gaza",
      country: "Amérique du Nord",
      composite_score: 88.85,
      transfers_to_abusers_score: 92.0,
      end_use_monitoring_failure_score: 88.0,
      parliamentary_oversight_absence_score: 85.0,
      victim_accountability_failure_score: 90.0,
      risk_level: "critique",
      primary_pattern: "transfers_to_abusers",
      estimated_arms_transfer_accountability_index: 8.89,
      last_updated: "2026-06-20",
    },
    {
      id: "AT-002",
      name: "France — Égypte/EAU/Arabie Saoudite : Rafale & Silence des Victimes du Yémen",
      country: "Europe Occidentale",
      composite_score: 84.15,
      transfers_to_abusers_score: 88.0,
      end_use_monitoring_failure_score: 82.0,
      parliamentary_oversight_absence_score: 85.0,
      victim_accountability_failure_score: 80.0,
      risk_level: "critique",
      primary_pattern: "parliamentary_oversight_absence",
      estimated_arms_transfer_accountability_index: 8.42,
      last_updated: "2026-06-20",
    },
    {
      id: "AT-003",
      name: "Russie/Chine — Syrie/Myanmar/Iran : Veto ONU & Armement des Dictatures",
      country: "Eurasie",
      composite_score: 83.55,
      transfers_to_abusers_score: 78.0,
      end_use_monitoring_failure_score: 85.0,
      parliamentary_oversight_absence_score: 90.0,
      victim_accountability_failure_score: 82.0,
      risk_level: "critique",
      primary_pattern: "parliamentary_oversight_absence",
      estimated_arms_transfer_accountability_index: 8.36,
      last_updated: "2026-06-20",
    },
    {
      id: "AT-004",
      name: "Royaume-Uni — Arabie Saoudite Licence Suspendue/Rétablie & Opacité Juridique",
      country: "Europe Occidentale",
      composite_score: 76.10,
      transfers_to_abusers_score: 72.0,
      end_use_monitoring_failure_score: 78.0,
      parliamentary_oversight_absence_score: 80.0,
      victim_accountability_failure_score: 75.0,
      risk_level: "critique",
      primary_pattern: "parliamentary_oversight_absence",
      estimated_arms_transfer_accountability_index: 7.61,
      last_updated: "2026-06-20",
    },
    {
      id: "AT-005",
      name: "Allemagne/UE — Exports Double Usage, Critères Communs & Violations Persistantes",
      country: "Europe",
      composite_score: 49.85,
      transfers_to_abusers_score: 45.0,
      end_use_monitoring_failure_score: 52.0,
      parliamentary_oversight_absence_score: 55.0,
      victim_accountability_failure_score: 48.0,
      risk_level: "élevé",
      primary_pattern: "parliamentary_oversight_absence",
      estimated_arms_transfer_accountability_index: 4.99,
      last_updated: "2026-06-20",
    },
    {
      id: "AT-006",
      name: "Israël — Technologie Surveillance/Drones Exportés à 100 Régimes Répressifs",
      country: "Moyen-Orient",
      composite_score: 49.75,
      transfers_to_abusers_score: 48.0,
      end_use_monitoring_failure_score: 50.0,
      parliamentary_oversight_absence_score: 45.0,
      victim_accountability_failure_score: 58.0,
      risk_level: "élevé",
      primary_pattern: "victim_accountability_failure",
      estimated_arms_transfer_accountability_index: 4.98,
      last_updated: "2026-06-20",
    },
    {
      id: "AT-007",
      name: "TCA/ATT — Traité Commerce des Armes, Lacunes & 113 États Parties",
      country: "Global",
      composite_score: 28.40,
      transfers_to_abusers_score: 25.0,
      end_use_monitoring_failure_score: 30.0,
      parliamentary_oversight_absence_score: 28.0,
      victim_accountability_failure_score: 32.0,
      risk_level: "modéré",
      primary_pattern: "victim_accountability_failure",
      estimated_arms_transfer_accountability_index: 2.84,
      last_updated: "2026-06-20",
    },
    {
      id: "AT-008",
      name: "ONU/Registre — Armes Conventionnelles, Panel Experts & Standards Transparence",
      country: "Global",
      composite_score: 4.40,
      transfers_to_abusers_score: 4.0,
      end_use_monitoring_failure_score: 5.0,
      parliamentary_oversight_absence_score: 3.0,
      victim_accountability_failure_score: 6.0,
      risk_level: "faible",
      primary_pattern: "victim_accountability_failure",
      estimated_arms_transfer_accountability_index: 0.44,
      last_updated: "2026-06-20",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/arms-transfer-accountability-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
