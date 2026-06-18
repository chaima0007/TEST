import { NextResponse } from "next/server";

type Health = "healthy" | "degraded" | "critical" | "offline";

interface AgentStats {
  agent_id: string;
  division: number;
  tasks_completed: number;
  tasks_failed: number;
  tasks_queued: number;
  error_rate: number;
  avg_response_time_ms: number;
  health: Health;
  last_error: string | null;
}

const DIVISION_NAMES: Record<number, string> = {
  1: "Détection & Scouting",
  2: "Rédaction & Outreach",
  3: "Relation & Négociation",
  4: "Production & Design",
  5: "Finance & Paiement",
  6: "Personal Branding",
};

function health(error_rate: number, offline = false): Health {
  if (offline) return "offline";
  if (error_rate >= 0.25) return "critical";
  if (error_rate >= 0.10) return "degraded";
  return "healthy";
}

function agent(
  div: number,
  idx: number,
  completed: number,
  failed: number,
  queued: number,
  response_ms: number,
  offline = false,
  last_error: string | null = null,
): AgentStats {
  const error_rate = offline ? 0 : Math.round((failed / Math.max(completed + failed, 1)) * 100) / 100;
  return {
    agent_id: `${div}.${idx}`,
    division: div,
    tasks_completed: offline ? 0 : completed,
    tasks_failed: offline ? 0 : failed,
    tasks_queued: offline ? 0 : queued,
    error_rate: offline ? 0 : error_rate,
    avg_response_time_ms: offline ? 0 : response_ms,
    health: health(error_rate, offline),
    last_error: offline ? "Agent hors ligne — connexion perdue" : last_error,
  };
}

const AGENTS: AgentStats[] = [
  agent(1, 0, 312, 4,  8,  240, false, null),
  agent(1, 1, 287, 3,  5,  215, false, null),
  agent(1, 2, 354, 5,  9,  198, false, null),
  agent(1, 3, 401, 6,  12, 222, false, null),
  agent(1, 4, 278, 3,  4,  231, false, null),
  agent(1, 5, 315, 4,  7,  209, false, null),
  agent(1, 6, 292, 2,  6,  243, false, null),
  agent(1, 7, 338, 5,  10, 217, false, null),
  agent(1, 8, 267, 3,  3,  228, false, null),
  agent(1, 9, 389, 4,  8,  204, false, null),

  agent(2, 0, 189, 12, 6,  310, false, null),
  agent(2, 1, 204, 18, 8,  298, false, "Délai de réponse SMTP dépassé"),
  agent(2, 2, 176, 15, 5,  322, false, null),
  agent(2, 3, 211, 11, 7,  305, false, null),
  agent(2, 4, 198, 22, 9,  289, false, "Quota journalier atteint"),
  agent(2, 5, 183, 14, 6,  316, false, null),
  agent(2, 6, 167, 19, 4,  331, false, "Taux de rebond élevé"),
  agent(2, 7, 221, 13, 8,  294, false, null),
  agent(2, 8, 195, 16, 7,  308, false, null),
  agent(2, 9, 208, 10, 5,  301, false, null),

  agent(3, 0, 143, 8,  4,  480, false, null),
  agent(3, 1, 156, 9,  5,  462, false, null),
  agent(3, 2, 138, 7,  3,  495, false, null),
  agent(3, 3, 161, 10, 6,  471, false, null),
  agent(3, 4, 149, 8,  4,  488, false, null),
  agent(3, 5, 134, 6,  3,  502, false, null),
  agent(3, 6, 158, 9,  5,  467, false, null),
  agent(3, 7, 142, 7,  4,  491, false, null),
  agent(3, 8, 165, 11, 6,  458, false, null),
  agent(3, 9, 137, 8,  3,  499, false, null),

  agent(4, 0, 112, 4,  3,  820, false, null),
  agent(4, 1, 98,  28, 5,  904, false, "Erreur génération image — timeout GPU"),
  agent(4, 2, 125, 6,  4,  798, false, null),
  agent(4, 3, 108, 5,  3,  834, false, null),
  agent(4, 4, 119, 4,  2,  812, false, null),
  agent(4, 5, 103, 5,  4,  856, false, null),
  agent(4, 6, 131, 7,  5,  784, false, null),
  agent(4, 7, 115, 4,  3,  828, false, null),
  agent(4, 8, 107, 6,  4,  841, false, null),
  agent(4, 9, 122, 5,  3,  807, false, null),

  agent(5, 0, 87,  5,  2,  620, false, null),
  agent(5, 1, 92,  7,  3,  604, false, null),
  agent(5, 2, 0,   0,  0,  0,   true,  null),
  agent(5, 3, 79,  4,  2,  638, false, null),
  agent(5, 4, 94,  8,  3,  598, false, null),
  agent(5, 5, 83,  6,  2,  615, false, null),
  agent(5, 6, 88,  7,  3,  609, false, null),
  agent(5, 7, 76,  5,  2,  641, false, null),
  agent(5, 8, 91,  6,  3,  602, false, null),
  agent(5, 9, 85,  5,  2,  618, false, null),

  agent(6, 0, 64,  5,  2,  740, false, null),
  agent(6, 1, 0,   0,  0,  0,   true,  null),
  agent(6, 2, 58,  14, 3,  768, false, "Erreur API réseau social — rate limit"),
  agent(6, 3, 71,  6,  2,  724, false, null),
  agent(6, 4, 67,  5,  2,  736, false, null),
  agent(6, 5, 73,  7,  3,  718, false, null),
  agent(6, 6, 61,  4,  2,  752, false, null),
  agent(6, 7, 69,  6,  3,  728, false, null),
  agent(6, 8, 55,  4,  1,  776, false, null),
  agent(6, 9, 72,  5,  2,  731, false, null),
];

function divisionHealth(agents: AgentStats[]): Health {
  if (agents.some((a) => a.health === "critical")) return "critical";
  if (agents.some((a) => a.health === "offline")) return "degraded";
  if (agents.some((a) => a.health === "degraded")) return "degraded";
  return "healthy";
}

export async function GET() {
  const divisions = [1, 2, 3, 4, 5, 6].map((div) => {
    const divAgents = AGENTS.filter((a) => a.division === div);
    const total_tasks = divAgents.reduce((s, a) => s + a.tasks_completed, 0);
    const total_errors = divAgents.reduce((s, a) => s + a.tasks_failed, 0);
    const active = divAgents.filter((a) => a.health !== "offline");
    const avg_response_time_ms = active.length
      ? Math.round(active.reduce((s, a) => s + a.avg_response_time_ms, 0) / active.length)
      : 0;

    return {
      division: div,
      name: DIVISION_NAMES[div],
      healthy_agents: divAgents.filter((a) => a.health === "healthy").length,
      total_agents: 10,
      total_tasks,
      total_errors,
      division_error_rate:
        total_tasks + total_errors > 0
          ? Math.round((total_errors / (total_tasks + total_errors)) * 1000) / 1000
          : 0,
      avg_response_time_ms,
      health: divisionHealth(divAgents),
      agents: divAgents,
    };
  });

  const healthy_agents = AGENTS.filter((a) => a.health === "healthy").length;
  const degraded_agents = AGENTS.filter((a) => a.health === "degraded").length;
  const critical_agents = AGENTS.filter((a) => a.health === "critical").length;
  const offline_agents = AGENTS.filter((a) => a.health === "offline").length;
  const total_tasks_completed = AGENTS.reduce((s, a) => s + a.tasks_completed, 0);
  const total_tasks_failed = AGENTS.reduce((s, a) => s + a.tasks_failed, 0);
  const global_error_rate =
    total_tasks_completed + total_tasks_failed > 0
      ? Math.round((total_tasks_failed / (total_tasks_completed + total_tasks_failed)) * 1000) / 1000
      : 0;

  return NextResponse.json({
    divisions,
    summary: {
      total_agents: 60,
      healthy_agents,
      degraded_agents,
      critical_agents,
      offline_agents,
      total_tasks_completed,
      total_tasks_failed,
      global_error_rate,
      open_alerts: critical_agents + offline_agents + degraded_agents,
    },
  });
}
