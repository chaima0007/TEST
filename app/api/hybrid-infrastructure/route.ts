import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[hybrid-infrastructure] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(
      sealResponse(getMockFleetStatus(), "Hybrid Infrastructure Monitor"),
    );
  }

  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/hybrid-infrastructure`, {
      next: { revalidate: 10 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Hybrid Infrastructure Monitor"));
  } catch {
    return NextResponse.json(
      sealResponse(getMockFleetStatus(), "Hybrid Infrastructure Monitor"),
      { status: 502 },
    );
  }
}

function getMockFleetStatus() {
  const localAgents = [
    { agent_id: "surv-01", name: "Sentinel Surveillance Alpha", tier: "local", model: "mistral-nemo", turn_count: 7, max_turns: 10, is_sleeping: false, circuit_state: "closed", is_alive: true, estimated_cost_usd: 0 },
    { agent_id: "surv-02", name: "Sentinel Surveillance Beta", tier: "local", model: "mistral-nemo", turn_count: 3, max_turns: 10, is_sleeping: false, circuit_state: "closed", is_alive: true, estimated_cost_usd: 0 },
    { agent_id: "well-01", name: "Bien-Être Équipe Alpha", tier: "local", model: "mistral:7b", turn_count: 5, max_turns: 10, is_sleeping: true, circuit_state: "closed", is_alive: true, estimated_cost_usd: 0 },
    { agent_id: "well-02", name: "Bien-Être Performance Beta", tier: "local", model: "mistral:7b", turn_count: 9, max_turns: 10, is_sleeping: false, circuit_state: "closed", is_alive: true, estimated_cost_usd: 0 },
    { agent_id: "task-01", name: "Planificateur Quotidien Alpha", tier: "local", model: "mistral-nemo", turn_count: 10, max_turns: 10, is_sleeping: false, circuit_state: "open", is_alive: false, estimated_cost_usd: 0 },
    { agent_id: "task-02", name: "Rapport Journalier Beta", tier: "local", model: "mistral-nemo", turn_count: 2, max_turns: 10, is_sleeping: false, circuit_state: "closed", is_alive: true, estimated_cost_usd: 0 },
    { agent_id: "anal-01", name: "Analytique Locale Gamma", tier: "local", model: "mistral:7b", turn_count: 6, max_turns: 10, is_sleeping: false, circuit_state: "closed", is_alive: true, estimated_cost_usd: 0 },
  ];

  const directors = [
    { agent_id: "dir-01", name: "Directeur Stratégique Principal", tier: "cloud", model: "claude-sonnet-4-6", turn_count: 2, max_turns: 5, is_sleeping: false, circuit_state: "closed", is_alive: true, total_tokens: 4820, estimated_cost_usd: 0.014460 },
    { agent_id: "dir-02", name: "Arbitreur Crises & Bugs Critiques", tier: "cloud", model: "claude-sonnet-4-6", turn_count: 1, max_turns: 5, is_sleeping: false, circuit_state: "closed", is_alive: true, total_tokens: 2110, estimated_cost_usd: 0.006330 },
  ];

  return {
    orchestrator: {
      uptime_s: 3742,
      total_agents: 9,
      local_agents: 7,
      cloud_directors: 2,
      alive_local: 6,
      alive_directors: 2,
      tripped_circuits: 1,
      tripped_agent_ids: ["task-01"],
    },
    token_usage: {
      local_tokens: 0,
      cloud_tokens: 6930,
      total_cost_usd: 0.020790,
      cloud_budget_limit: 100000,
      alerts: [],
    },
    local_agents: localAgents,
    directors,
    recommendations: [
      "1 circuit déclenché — agent task-01 a atteint max_turns=10",
      "Coût cloud nominal : 0.021$ pour cette session",
      "6/7 agents locaux opérationnels — aucune escalade non planifiée",
    ],
  };
}
