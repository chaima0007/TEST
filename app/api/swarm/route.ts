import { NextResponse } from "next/server";
import { DIVISIONS, SWARM_METRICS, LIVE_JOBS, SIMULATION_DIALOGUE } from "@/lib/swarm-data";

export async function GET() {
  return NextResponse.json({
    metrics: SWARM_METRICS,
    divisions: DIVISIONS,
    jobs: LIVE_JOBS,
    simulation: SIMULATION_DIALOGUE,
    lastUpdated: new Date().toISOString(),
  });
}
