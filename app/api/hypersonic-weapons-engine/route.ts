import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[hypersonic-weapons-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData() as Record<string, unknown>, "Hypersonic Weapons Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/hypersonic-weapons-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json() as Record<string, unknown>;
    return NextResponse.json(sealResponse(data, "Hypersonic Weapons Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData() as Record<string, unknown>, "Hypersonic Weapons Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    // ── CRITIQUE (3) ──────────────────────────────────────────────────────────
    {
      entity_id: "HYP-001",
      name: "Programme Zircon Russe",
      country: "Russie",
      sector: "Missiles Hypersoniques",
      composite_score: 83.95,
      velocity_threat_score: 88.0,
      detection_evasion_score: 85.0,
      payload_lethality_score: 82.0,
      deployment_readiness_score: 79.0,
      risk_level: "critique",
      primary_pattern: "Missiles à Planeurs Hypersoniques",
      key_signals: ["velocity_threat:88.0%", "detection_evasion:85.0%", "deployment_readiness:79.0%"],
      estimated_hypersonic_index: 8.4,
      last_updated: "2026-06-20",
      alert_level: "ROUGE",
    },
    {
      entity_id: "HYP-002",
      name: "DF-17 Chinois",
      country: "Chine",
      sector: "Véhicules Planeurs",
      composite_score: 78.85,
      velocity_threat_score: 82.0,
      detection_evasion_score: 79.0,
      payload_lethality_score: 78.0,
      deployment_readiness_score: 75.0,
      risk_level: "critique",
      primary_pattern: "Ogive Manœuvrante Avancée",
      key_signals: ["velocity_threat:82.0%", "detection_evasion:79.0%", "deployment_readiness:75.0%"],
      estimated_hypersonic_index: 7.89,
      last_updated: "2026-06-20",
      alert_level: "ROUGE",
    },
    {
      entity_id: "HYP-003",
      name: "AGM-183A ARRW Américain",
      country: "États-Unis",
      sector: "Missiles Hypersoniques",
      composite_score: 71.6,
      velocity_threat_score: 75.0,
      detection_evasion_score: 72.0,
      payload_lethality_score: 70.0,
      deployment_readiness_score: 68.0,
      risk_level: "critique",
      primary_pattern: "Capacité de Frappe de Précision",
      key_signals: ["velocity_threat:75.0%", "detection_evasion:72.0%", "deployment_readiness:68.0%"],
      estimated_hypersonic_index: 7.16,
      last_updated: "2026-06-20",
      alert_level: "ROUGE",
    },
    // ── ÉLEVÉ (2) ─────────────────────────────────────────────────────────────
    {
      entity_id: "HYP-004",
      name: "BrahMos-II Indo-Russe",
      country: "Inde",
      sector: "Missiles Hypersoniques",
      composite_score: 54.0,
      velocity_threat_score: 58.0,
      detection_evasion_score: 55.0,
      payload_lethality_score: 53.0,
      deployment_readiness_score: 48.0,
      risk_level: "élevé",
      primary_pattern: "Capacité de Frappe de Précision",
      key_signals: ["velocity_threat:58.0%", "detection_evasion:55.0%", "deployment_readiness:48.0%"],
      estimated_hypersonic_index: 5.4,
      last_updated: "2026-06-20",
      alert_level: "ORANGE",
    },
    {
      entity_id: "HYP-005",
      name: "Programme HYFLOW Européen",
      country: "Allemagne",
      sector: "Recherche Hypersonique",
      composite_score: 46.0,
      velocity_threat_score: 50.0,
      detection_evasion_score: 47.0,
      payload_lethality_score: 45.0,
      deployment_readiness_score: 40.0,
      risk_level: "élevé",
      primary_pattern: "Développement en Phase Initiale",
      key_signals: ["velocity_threat:50.0%", "detection_evasion:47.0%", "deployment_readiness:40.0%"],
      estimated_hypersonic_index: 4.6,
      last_updated: "2026-06-20",
      alert_level: "ORANGE",
    },
    // ── MODÉRÉ (1) ────────────────────────────────────────────────────────────
    {
      entity_id: "HYP-006",
      name: "Systèmes ISRO India",
      country: "Inde",
      sector: "Technologies Duales",
      composite_score: 31.0,
      velocity_threat_score: 35.0,
      detection_evasion_score: 32.0,
      payload_lethality_score: 30.0,
      deployment_readiness_score: 25.0,
      risk_level: "modéré",
      primary_pattern: "Surveillance Standard",
      key_signals: ["velocity_threat:35.0%", "detection_evasion:32.0%", "deployment_readiness:25.0%"],
      estimated_hypersonic_index: 3.1,
      last_updated: "2026-06-20",
      alert_level: "JAUNE",
    },
    // ── FAIBLE (2) ────────────────────────────────────────────────────────────
    {
      entity_id: "HYP-007",
      name: "Recherche Académique MIT",
      country: "États-Unis",
      sector: "Recherche & Développement",
      composite_score: 11.6,
      velocity_threat_score: 15.0,
      detection_evasion_score: 12.0,
      payload_lethality_score: 10.0,
      deployment_readiness_score: 8.0,
      risk_level: "faible",
      primary_pattern: "Surveillance Standard",
      key_signals: ["velocity_threat:15.0%", "detection_evasion:12.0%", "deployment_readiness:8.0%"],
      estimated_hypersonic_index: 1.16,
      last_updated: "2026-06-20",
      alert_level: "VERT",
    },
    {
      entity_id: "HYP-008",
      name: "Programme Spatial Japonais JAXA",
      country: "Japon",
      sector: "Technologies Spatiales",
      composite_score: 7.95,
      velocity_threat_score: 10.0,
      detection_evasion_score: 8.0,
      payload_lethality_score: 7.0,
      deployment_readiness_score: 6.0,
      risk_level: "faible",
      primary_pattern: "Surveillance Standard",
      key_signals: ["velocity_threat:10.0%", "detection_evasion:8.0%", "deployment_readiness:6.0%"],
      estimated_hypersonic_index: 0.8,
      last_updated: "2026-06-20",
      alert_level: "VERT",
    },
  ];

  const n = entities.length;
  const avg_composite = Math.round(
    (entities.reduce((acc, e) => acc + e.composite_score, 0) / n) * 100
  ) / 100;

  const risk_distribution = {
    critique: entities.filter((e) => e.risk_level === "critique").length,
    élevé: entities.filter((e) => e.risk_level === "élevé").length,
    modéré: entities.filter((e) => e.risk_level === "modéré").length,
    faible: entities.filter((e) => e.risk_level === "faible").length,
  };

  const pattern_distribution: Record<string, number> = {};
  for (const e of entities) {
    pattern_distribution[e.primary_pattern] = (pattern_distribution[e.primary_pattern] ?? 0) + 1;
  }

  const sorted = [...entities].sort((a, b) => b.composite_score - a.composite_score);
  const top_risk_entities = sorted.slice(0, 3).map((e) => e.name);

  return {
    total_entities: n,
    avg_composite,
    risk_distribution,
    pattern_distribution,
    top_risk_entities,
    critical_alerts: risk_distribution.critique,
    last_analysis: "2026-06-20T00:00:00Z",
    engine_version: "1.0.0",
    domain: "hypersonic",
    confidence_score: 87.5,
    data_sources: ["SIPRI", "Jane's Defence", "RAND Corporation"],
    entities,
    avg_estimated_hypersonic_index: Math.round(avg_composite / 100 * 10 * 100) / 100,
  };
}
