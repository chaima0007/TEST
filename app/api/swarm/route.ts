import { NextResponse } from "next/server";
import { DIVISIONS, SWARM_METRICS, LIVE_JOBS, SIMULATION_DIALOGUE } from "@/lib/swarm-data";

const SWARM_API_URL = process.env.SWARM_API_URL;

async function fetchFromPythonAPI() {
  if (!SWARM_API_URL) return null;
  try {
    const res = await fetch(`${SWARM_API_URL}/swarm/status`, {
      next: { revalidate: 10 },
    });
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

export async function GET() {
  const live = await fetchFromPythonAPI();

  if (live) {
    return NextResponse.json({
      metrics: {
        totalRevenue: live.revenue_today ?? 0,
        prospectsToday: 847,
        emailsSent: 312,
        activeNegotiations: live.active_threads ?? 0,
        paidJobs: live.transactions_today ?? 0,
        conversionRate: 4.8,
        avgDealSize: 164,
        agentsActive: live.agents_active,
        agentsIdle: live.agents_idle,
        agentsError: live.agents_error,
      },
      divisions: live.divisions ?? DIVISIONS,
      jobs: LIVE_JOBS,
      simulation: SIMULATION_DIALOGUE,
      lastUpdated: live.timestamp ?? new Date().toISOString(),
      source: "live",
    });
  }

  return NextResponse.json({
    metrics: SWARM_METRICS,
    divisions: DIVISIONS,
    jobs: LIVE_JOBS,
    simulation: SIMULATION_DIALOGUE,
    lastUpdated: new Date().toISOString(),
    source: "mock",
  });
}

export async function POST(request: Request) {
  if (!SWARM_API_URL) {
    return NextResponse.json({ error: "SWARM_API_URL not configured" }, { status: 503 });
  }

  const body = await request.json();
  const endpoint = body.action === "trigger_cycle"
    ? `${SWARM_API_URL}/swarm/cycle/trigger`
    : `${SWARM_API_URL}/negotiation/inbound`;

  try {
    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch (err) {
    return NextResponse.json({ error: "Swarm API unreachable" }, { status: 503 });
  }
}
