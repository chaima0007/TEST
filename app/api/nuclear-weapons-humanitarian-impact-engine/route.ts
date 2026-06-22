import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[nuclear-weapons-humanitarian-impact-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "nuclear_weapons_humanitarian_impact_engine",
  domain: "nuclear_weapons_humanitarian_impact",
  total_entities: 8,
  avg_composite: 62.19,
  confidence_score: 0.91,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: {
    proliferation_violation: 3,
    escalation_doctrine: 2,
    humanitarian_impact: 2,
    disarmament_treaty: 1,
  },
  top_risk_entities: [
    { id: "NWH-001", name: "Corée du Nord — Tests NPT, 50+ Ogives Estimées", score: 94.1, risk: "critique" },
    { id: "NWH-002", name: "Russie — Menaces Nucléaires Ukraine 2022-24, Retrait New START", score: 91.45, risk: "critique" },
    { id: "NWH-003", name: "Pakistan — 100+ Ogives, Instabilité Civilo-Militaire", score: 86.2, risk: "critique" },
  ],
  critical_alerts: [
    "NWH-001: Corée du Nord — Tests NPT, 50+ Ogives Estimées — composite 94.1",
    "NWH-002: Russie — Menaces Nucléaires Ukraine 2022-24, Retrait New START — composite 91.45",
    "NWH-003: Pakistan — 100+ Ogives, Instabilité Civilo-Militaire — composite 86.2",
    "NWH-004: Inde/Pakistan — Tensions Kashmir, Doctrines Nucléaires — composite 84.4",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_nuclear_weapons_humanitarian_impact_index: 6.22,
  data_sources: [
    "sipri_nuclear_forces_2023",
    "ican_global_status_2023",
    "bulletin_atomic_scientists_2023",
    "un_tpnw_implementation_2023",
  ],
  entities: [
    {
      id: "NWH-001",
      name: "Corée du Nord — Tests NPT, 50+ Ogives Estimées",
      country: "Corée du Nord",
      nuclear_threat_proliferation_severity_score: 95.0,
      civilian_humanitarian_impact_risk_score: 92.0,
      arms_control_treaty_violation_scale_score: 96.0,
      nuclear_doctrine_escalation_risk_score: 93.0,
      composite_score: 94.1,
      risk_level: "critique",
      primary_pattern: "Violation NPT systématique, tests missiles balistiques intercontinentaux, menace régionale",
      estimated_nuclear_weapons_humanitarian_impact_index: 9.41,
      last_updated: "2026-06-21",
    },
    {
      id: "NWH-002",
      name: "Russie — Menaces Nucléaires Ukraine 2022-24, Retrait New START",
      country: "Russie",
      nuclear_threat_proliferation_severity_score: 92.0,
      civilian_humanitarian_impact_risk_score: 90.0,
      arms_control_treaty_violation_scale_score: 91.0,
      nuclear_doctrine_escalation_risk_score: 93.0,
      composite_score: 91.45,
      risk_level: "critique",
      primary_pattern: "Rhétorique nucléaire guerre Ukraine, retrait New START 2023, 6000 ogives arsenal",
      estimated_nuclear_weapons_humanitarian_impact_index: 9.14,
      last_updated: "2026-06-21",
    },
    {
      id: "NWH-003",
      name: "Pakistan — 100+ Ogives, Instabilité Civilo-Militaire",
      country: "Pakistan",
      nuclear_threat_proliferation_severity_score: 88.0,
      civilian_humanitarian_impact_risk_score: 86.0,
      arms_control_treaty_violation_scale_score: 82.0,
      nuclear_doctrine_escalation_risk_score: 89.0,
      composite_score: 86.2,
      risk_level: "critique",
      primary_pattern: "Instabilité civilo-militaire, prolifération réseau AQ Khan, first-use doctrine",
      estimated_nuclear_weapons_humanitarian_impact_index: 8.62,
      last_updated: "2026-06-21",
    },
    {
      id: "NWH-004",
      name: "Inde/Pakistan — Tensions Kashmir, Doctrines Nucléaires",
      country: "Inde/Pakistan",
      nuclear_threat_proliferation_severity_score: 85.0,
      civilian_humanitarian_impact_risk_score: 88.0,
      arms_control_treaty_violation_scale_score: 78.0,
      nuclear_doctrine_escalation_risk_score: 87.0,
      composite_score: 84.4,
      risk_level: "critique",
      primary_pattern: "Conflit Kashmir latent, doctrines dissuasion antagonistes, risque escalade accidentelle",
      estimated_nuclear_weapons_humanitarian_impact_index: 8.44,
      last_updated: "2026-06-21",
    },
    {
      id: "NWH-005",
      name: "Iran — Enrichissement 60% Uranium, Breakout Capacity",
      country: "Iran",
      nuclear_threat_proliferation_severity_score: 58.0,
      civilian_humanitarian_impact_risk_score: 55.0,
      arms_control_treaty_violation_scale_score: 62.0,
      nuclear_doctrine_escalation_risk_score: 56.0,
      composite_score: 57.85,
      risk_level: "élevé",
      primary_pattern: "Enrichissement uranium 60% proche seuil armement, JCPOA effondré, capacité breakout 2 semaines",
      estimated_nuclear_weapons_humanitarian_impact_index: 5.79,
      last_updated: "2026-06-21",
    },
    {
      id: "NWH-006",
      name: "Israël — Ambiguïté Nucléaire, 90 Ogives Estimées Negev",
      country: "Israël",
      nuclear_threat_proliferation_severity_score: 52.0,
      civilian_humanitarian_impact_risk_score: 50.0,
      arms_control_treaty_violation_scale_score: 58.0,
      nuclear_doctrine_escalation_risk_score: 53.0,
      composite_score: 53.2,
      risk_level: "élevé",
      primary_pattern: "Politique ambiguïté nucléaire officielle, installation Negev, non-signataire NPT",
      estimated_nuclear_weapons_humanitarian_impact_index: 5.32,
      last_updated: "2026-06-21",
    },
    {
      id: "NWH-007",
      name: "Chine — Modernisation Arsenal, Opacité Doctrine",
      country: "Chine",
      nuclear_threat_proliferation_severity_score: 28.0,
      civilian_humanitarian_impact_risk_score: 26.0,
      arms_control_treaty_violation_scale_score: 24.0,
      nuclear_doctrine_escalation_risk_score: 27.0,
      composite_score: 26.3,
      risk_level: "modéré",
      primary_pattern: "Modernisation rapide arsenal vers 1500 ogives 2035, opacité doctrine NFU, silos Xinjiang",
      estimated_nuclear_weapons_humanitarian_impact_index: 2.63,
      last_updated: "2026-06-21",
    },
    {
      id: "NWH-008",
      name: "TPNW — Traité Interdiction Armes Nucléaires 2021, 68 États",
      country: "International",
      nuclear_threat_proliferation_severity_score: 4.0,
      civilian_humanitarian_impact_risk_score: 4.0,
      arms_control_treaty_violation_scale_score: 4.0,
      nuclear_doctrine_escalation_risk_score: 4.0,
      composite_score: 4.0,
      risk_level: "faible",
      primary_pattern: "68 États signataires TPNW 2021, aucune puissance nucléaire adhérente, pression normative humanitaire",
      estimated_nuclear_weapons_humanitarian_impact_index: 0.4,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/nuclear-weapons-humanitarian-impact-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
