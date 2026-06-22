import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[agents-health] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

function randomHealth(): "healthy" | "degraded" | "critical" | "offline" {
  const r = Math.random();
  if (r < 0.78) return "healthy";
  if (r < 0.90) return "degraded";
  if (r < 0.97) return "critical";
  return "offline";
}

function makeAgent(agentId: string, division: number) {
  const completed = Math.floor(Math.random() * 200) + 10;
  const errorRate = Math.random() * 0.12;
  const failed = Math.floor(completed * errorRate);
  const health = randomHealth();
  return {
    agent_id: agentId,
    division,
    tasks_completed: completed,
    tasks_failed: failed,
    tasks_queued: Math.floor(Math.random() * 8),
    error_rate: Math.round(errorRate * 10000) / 10000,
    avg_response_time_ms: Math.round(Math.random() * 2000 + 200),
    health,
    last_error: failed > 0 ? "Connexion API timeout" : null,
    seconds_since_heartbeat: Math.floor(Math.random() * 60),
  };
}

const DIV_NAMES: Record<number, string> = {
  1: "Détection & Scouting",
  2: "Rédaction & Outreach",
  3: "Relation & Négociation",
  4: "Production & Design",
  5: "Finance & Paiement",
  6: "Personal Branding",
};

function buildMockData() {
  const divisions = [];
  let totalCompleted = 0;
  let totalFailed = 0;
  let totalHealthy = 0;
  let totalDegraded = 0;
  let totalCritical = 0;
  let totalOffline = 0;
  const allAlerts: object[] = [];

  for (let div = 1; div <= 6; div++) {
    const agents = [];
    for (let i = 0; i <= 9; i++) {
      const agentId = `${div}.${i}`;
      const agent = makeAgent(agentId, div);
      agents.push(agent);
      totalCompleted += agent.tasks_completed;
      totalFailed += agent.tasks_failed;
      if (agent.health === "healthy") totalHealthy++;
      else if (agent.health === "degraded") { totalDegraded++; allAlerts.push({ agent_id: agentId, division: div, level: "warning", message: `Agent ${agentId} dégradé — error rate ${(agent.error_rate * 100).toFixed(0)}%` }); }
      else if (agent.health === "critical") { totalCritical++; allAlerts.push({ agent_id: agentId, division: div, level: "critical", message: `Agent ${agentId} critique — intervention requise` }); }
      else totalOffline++;
    }

    const divHealth = agents.some(a => a.health === "critical") ? "critical"
      : agents.some(a => a.health === "degraded") ? "degraded"
      : agents.every(a => a.health === "offline") ? "offline"
      : "healthy";

    divisions.push({
      division: div,
      name: DIV_NAMES[div],
      healthy_agents: agents.filter(a => a.health === "healthy").length,
      total_agents: agents.length,
      total_tasks: agents.reduce((s, a) => s + a.tasks_completed, 0),
      total_errors: agents.reduce((s, a) => s + a.tasks_failed, 0),
      division_error_rate: agents.reduce((s, a) => s + a.error_rate, 0) / agents.length,
      avg_response_time_ms: agents.reduce((s, a) => s + a.avg_response_time_ms, 0) / agents.length,
      health: divHealth,
      agents,
    });
  }

  return {
    source: "mock",
    summary: {
      total_agents: 60,
      healthy_agents: totalHealthy,
      degraded_agents: totalDegraded,
      critical_agents: totalCritical,
      offline_agents: totalOffline,
      total_tasks_completed: totalCompleted,
      total_tasks_failed: totalFailed,
      global_error_rate: Math.round(totalFailed / (totalCompleted + totalFailed) * 10000) / 10000,
      open_alerts: allAlerts.length,
    },
    divisions,
    alerts: allAlerts.slice(0, 10),
  };
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/agents/health`, {
        next: { revalidate: 15 },
      });
      if (res.ok) {
        return sealResponse(NextResponse.json({ source: "live", ...(await res.json()) }));
      }
    } catch {
      // fall through to mock
    }
  }
  return sealResponse(NextResponse.json(buildMockData()));
}
