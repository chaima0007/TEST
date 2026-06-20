import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[agent-orchestrator] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(
      sealResponse(getMockData(), "Agent Orchestrator Agent"),
    );
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/agent-orchestrator`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Agent Orchestrator Agent"));
  } catch {
    return NextResponse.json(
      sealResponse(getMockData(), "Agent Orchestrator Agent"),
      { status: 502 },
    );
  }
}

function getMockData() {
  const entities = [
    {
      entity_id: "ENT-001",
      name: "SwarmAI Dynamics",
      country: "États-Unis",
      sector: "Intelligence Artificielle",
      composite_score: 74.9,
      coordination_score: 82.0,
      autonomy_score: 78.0,
      latency_score: 72.0,
      resilience_score: 64.0,
      risk_level: "critique",
      primary_pattern: "coordination_failure",
      key_signals: [
        "Coordination inter-agents critique",
        "Dérive d'autonomie détectée",
        "Latence en cascade",
      ],
      estimated_orchestration_index: 7.49,
      last_updated: "2026-06-20",
      agent_count: 847,
    },
    {
      entity_id: "ENT-002",
      name: "AgentForge Berlin",
      country: "Allemagne",
      sector: "Robotique & Automatisation",
      composite_score: 67.55,
      coordination_score: 74.0,
      autonomy_score: 70.0,
      latency_score: 65.0,
      resilience_score: 58.0,
      risk_level: "critique",
      primary_pattern: "coordination_failure",
      key_signals: [
        "Coordination inter-agents critique",
        "Dérive d'autonomie détectée",
        "Latence inter-agents élevée",
      ],
      estimated_orchestration_index: 6.76,
      last_updated: "2026-06-20",
      agent_count: 523,
    },
    {
      entity_id: "ENT-003",
      name: "Nexus Orchestral",
      country: "Royaume-Uni",
      sector: "Infrastructure Numérique",
      composite_score: 61.8,
      coordination_score: 68.0,
      autonomy_score: 64.0,
      latency_score: 60.0,
      resilience_score: 52.0,
      risk_level: "critique",
      primary_pattern: "equilibrium_stable",
      key_signals: [
        "Coordination inter-agents dégradée",
        "Autonomie agents sous surveillance",
        "Latence inter-agents élevée",
      ],
      estimated_orchestration_index: 6.18,
      last_updated: "2026-06-20",
      agent_count: 1205,
    },
    {
      entity_id: "ENT-004",
      name: "Korrelia Systems",
      country: "France",
      sector: "Logistique & Transport",
      composite_score: 51.6,
      coordination_score: 55.0,
      autonomy_score: 50.0,
      latency_score: 52.0,
      resilience_score: 48.0,
      risk_level: "élevé",
      primary_pattern: "equilibrium_stable",
      key_signals: [
        "Coordination inter-agents dégradée",
        "Autonomie agents sous surveillance",
        "Latence inter-agents élevée",
      ],
      estimated_orchestration_index: 5.16,
      last_updated: "2026-06-20",
      agent_count: 312,
    },
    {
      entity_id: "ENT-005",
      name: "Parallax Computing",
      country: "Japon",
      sector: "Systèmes Embarqués",
      composite_score: 43.2,
      coordination_score: 44.0,
      autonomy_score: 46.0,
      latency_score: 42.0,
      resilience_score: 40.0,
      risk_level: "élevé",
      primary_pattern: "equilibrium_stable",
      key_signals: [
        "Coordination inter-agents nominale",
        "Autonomie agents contrôlée",
        "Latence inter-agents acceptable",
      ],
      estimated_orchestration_index: 4.32,
      last_updated: "2026-06-20",
      agent_count: 189,
    },
    {
      entity_id: "ENT-006",
      name: "Cascade Robotics",
      country: "Canada",
      sector: "Industrie Manufacturière",
      composite_score: 27.3,
      coordination_score: 30.0,
      autonomy_score: 28.0,
      latency_score: 26.0,
      resilience_score: 24.0,
      risk_level: "modéré",
      primary_pattern: "equilibrium_stable",
      key_signals: [
        "Coordination inter-agents nominale",
        "Autonomie agents contrôlée",
        "Latence inter-agents acceptable",
      ],
      estimated_orchestration_index: 2.73,
      last_updated: "2026-06-20",
      agent_count: 67,
    },
    {
      entity_id: "ENT-007",
      name: "Harmony Agents",
      country: "Pays-Bas",
      sector: "Services Financiers",
      composite_score: 11.3,
      coordination_score: 14.0,
      autonomy_score: 12.0,
      latency_score: 10.0,
      resilience_score: 8.0,
      risk_level: "faible",
      primary_pattern: "equilibrium_stable",
      key_signals: [
        "Coordination inter-agents nominale",
        "Autonomie agents contrôlée",
        "Latence inter-agents acceptable",
      ],
      estimated_orchestration_index: 1.13,
      last_updated: "2026-06-20",
      agent_count: 23,
    },
    {
      entity_id: "ENT-008",
      name: "Equilibria Labs",
      country: "Suède",
      sector: "Recherche & Développement",
      composite_score: 7.7,
      coordination_score: 10.0,
      autonomy_score: 8.0,
      latency_score: 6.0,
      resilience_score: 6.0,
      risk_level: "faible",
      primary_pattern: "equilibrium_stable",
      key_signals: [
        "Coordination inter-agents nominale",
        "Autonomie agents contrôlée",
        "Latence inter-agents acceptable",
      ],
      estimated_orchestration_index: 0.77,
      last_updated: "2026-06-20",
      agent_count: 14,
    },
  ];

  const avg_composite = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;

  return {
    total_entities: entities.length,
    avg_composite,
    risk_distribution: {
      critique: entities.filter(e => e.risk_level === "critique").length,
      élevé: entities.filter(e => e.risk_level === "élevé").length,
      modéré: entities.filter(e => e.risk_level === "modéré").length,
      faible: entities.filter(e => e.risk_level === "faible").length,
    },
    pattern_distribution: {
      coordination_failure: entities.filter(e => e.primary_pattern === "coordination_failure").length,
      autonomy_drift: entities.filter(e => e.primary_pattern === "autonomy_drift").length,
      latency_cascade: entities.filter(e => e.primary_pattern === "latency_cascade").length,
      resilience_collapse: entities.filter(e => e.primary_pattern === "resilience_collapse").length,
      equilibrium_stable: entities.filter(e => e.primary_pattern === "equilibrium_stable").length,
    },
    top_risk_entities: entities
      .slice()
      .sort((a, b) => b.composite_score - a.composite_score)
      .slice(0, 3)
      .map(e => e.name),
    critical_alerts: entities
      .filter(e => e.risk_level === "critique")
      .map(e => `ALERTE CRITIQUE — ${e.name} (${e.country}) : composite=${e.composite_score}, pattern=${e.primary_pattern}`),
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "orchestration",
    confidence_score: 0.87,
    data_sources: ["agent_telemetry", "orchestration_logs", "latency_metrics"],
    entities,
    avg_estimated_orchestration_index: Math.round(avg_composite / 100 * 10 * 100) / 100,
  };
}
