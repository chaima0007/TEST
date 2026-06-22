import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[platform-labor-rights-engine] SWARM_API_URL non défini — mode mock activé");
}

const entities = [
  {
    id: "LAB-001",
    name: "Uber Technologies Global",
    country: "États-Unis",
    sector: "Transport & Mobilité",
    worker_exploitation_score: 88.0,
    wage_theft_risk_score: 85.0,
    algorithmic_control_score: 82.0,
    labor_protection_gap_score: 80.0,
    composite_score: 84.15,
    risk_level: "critique",
    primary_pattern: "Exploitation Systémique des Travailleurs",
    key_signals: ["exploitation:88.0%", "vol_salaire:85.0%", "contrôle_algo:82.0%"],
    estimated_labor_index: 8.42,
    last_updated: "2026-06-20",
    alert_level: "ROUGE",
  },
  {
    id: "LAB-002",
    name: "Amazon Flex Réseau",
    country: "États-Unis",
    sector: "Livraison & Logistique",
    worker_exploitation_score: 82.0,
    wage_theft_risk_score: 80.0,
    algorithmic_control_score: 85.0,
    labor_protection_gap_score: 65.0,
    composite_score: 78.85,
    risk_level: "critique",
    primary_pattern: "Vol de Salaire Algorithmique",
    key_signals: ["exploitation:82.0%", "vol_salaire:80.0%", "contrôle_algo:85.0%"],
    estimated_labor_index: 7.89,
    last_updated: "2026-06-20",
    alert_level: "ROUGE",
  },
  {
    id: "LAB-003",
    name: "Deliveroo Europe",
    country: "Royaume-Uni",
    sector: "Livraison Alimentaire",
    worker_exploitation_score: 75.0,
    wage_theft_risk_score: 72.0,
    algorithmic_control_score: 70.0,
    labor_protection_gap_score: 62.0,
    composite_score: 70.4,
    risk_level: "critique",
    primary_pattern: "Surveillance Algorithmique Intrusive",
    key_signals: ["exploitation:75.0%", "vol_salaire:72.0%", "contrôle_algo:70.0%"],
    estimated_labor_index: 7.04,
    last_updated: "2026-06-20",
    alert_level: "ROUGE",
  },
  {
    id: "LAB-004",
    name: "Glovo Espagne & Méditerranée",
    country: "Espagne",
    sector: "Économie des Courses",
    worker_exploitation_score: 58.0,
    wage_theft_risk_score: 55.0,
    algorithmic_control_score: 52.0,
    labor_protection_gap_score: 47.0,
    composite_score: 53.55,
    risk_level: "élevé",
    primary_pattern: "Précarité Structurelle Croissante",
    key_signals: ["exploitation:58.0%", "vol_salaire:55.0%", "contrôle_algo:52.0%"],
    estimated_labor_index: 5.36,
    last_updated: "2026-06-20",
    alert_level: "ORANGE",
  },
  {
    id: "LAB-005",
    name: "TaskRabbit Plateforme",
    country: "États-Unis",
    sector: "Services à Domicile",
    worker_exploitation_score: 50.0,
    wage_theft_risk_score: 48.0,
    algorithmic_control_score: 46.0,
    labor_protection_gap_score: 42.0,
    composite_score: 46.9,
    risk_level: "élevé",
    primary_pattern: "Précarité Structurelle Croissante",
    key_signals: ["exploitation:50.0%", "vol_salaire:48.0%", "contrôle_algo:46.0%"],
    estimated_labor_index: 4.69,
    last_updated: "2026-06-20",
    alert_level: "ORANGE",
  },
  {
    id: "LAB-006",
    name: "Fiverr Pro Network",
    country: "Israël",
    sector: "Travail Créatif en Ligne",
    worker_exploitation_score: 35.0,
    wage_theft_risk_score: 30.0,
    algorithmic_control_score: 28.0,
    labor_protection_gap_score: 25.0,
    composite_score: 30.0,
    risk_level: "modéré",
    primary_pattern: "Surveillance Standard",
    key_signals: ["exploitation:35.0%", "vol_salaire:30.0%", "contrôle_algo:28.0%"],
    estimated_labor_index: 3.0,
    last_updated: "2026-06-20",
    alert_level: "JAUNE",
  },
  {
    id: "LAB-007",
    name: "Coopérative Transport Amsterdam",
    country: "Pays-Bas",
    sector: "Coopérative Numérique",
    worker_exploitation_score: 14.0,
    wage_theft_risk_score: 10.0,
    algorithmic_control_score: 10.0,
    labor_protection_gap_score: 8.0,
    composite_score: 10.8,
    risk_level: "faible",
    primary_pattern: "Surveillance Standard",
    key_signals: ["exploitation:14.0%", "vol_salaire:10.0%", "contrôle_algo:10.0%"],
    estimated_labor_index: 1.08,
    last_updated: "2026-06-20",
    alert_level: "VERT",
  },
  {
    id: "LAB-008",
    name: "Fairwork Certified Platform",
    country: "Allemagne",
    sector: "Plateforme Éthique",
    worker_exploitation_score: 10.0,
    wage_theft_risk_score: 8.0,
    algorithmic_control_score: 7.0,
    labor_protection_gap_score: 5.0,
    composite_score: 7.75,
    risk_level: "faible",
    primary_pattern: "Surveillance Standard",
    key_signals: ["exploitation:10.0%", "vol_salaire:8.0%", "contrôle_algo:7.0%"],
    estimated_labor_index: 0.78,
    last_updated: "2026-06-20",
    alert_level: "VERT",
  },
];

function getMockData() {
  return {
    total_entities: 8,
    avg_composite: 47.8,
    risk_distribution: { critique: 3, élevé: 2, modéré: 1, faible: 2 },
    pattern_distribution: {
      "Exploitation Systémique des Travailleurs": 1,
      "Vol de Salaire Algorithmique": 1,
      "Surveillance Algorithmique Intrusive": 1,
      "Précarité Structurelle Croissante": 2,
      "Surveillance Standard": 3,
    },
    top_risk_entities: ["Uber Technologies Global", "Amazon Flex Réseau", "Deliveroo Europe"],
    critical_alerts: 3,
    last_analysis: "2026-06-20T00:00:00Z",
    engine_version: "1.0.0",
    domain: "labor",
    confidence_score: 89.0,
    data_sources: ["ILO", "Fairwork Foundation", "ETUC"],
    entities,
    avg_estimated_labor_index: 4.78,
  };
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData() as unknown as Record<string, unknown>, "Platform Labor Rights Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/platform-labor-rights-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data as Record<string, unknown>, "Platform Labor Rights Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData() as unknown as Record<string, unknown>, "Platform Labor Rights Agent"), { status: 502 }));
  }
}
