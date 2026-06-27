import { NextResponse } from "next/server";
import { PORTFOLIO_PROJECTS, PORTFOLIO_SKILLS, PORTFOLIO_STATS } from "@/lib/portfolio-data";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[portfolio] SWARM_API_URL non défini — mode local");
}

export async function GET() {
  try {
    return NextResponse.json(sealResponse({
      stats: PORTFOLIO_STATS,
      projects: PORTFOLIO_PROJECTS,
      skills: PORTFOLIO_SKILLS,
    }));
  } catch {
    return NextResponse.json(sealResponse({ error: "upstream error" }), { status: 502 });
  }
}
