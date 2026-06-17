import { NextResponse } from "next/server";
import { PORTFOLIO_PROJECTS, PORTFOLIO_SKILLS, PORTFOLIO_STATS } from "@/lib/portfolio-data";

export async function GET() {
  return NextResponse.json({
    stats: PORTFOLIO_STATS,
    projects: PORTFOLIO_PROJECTS,
    skills: PORTFOLIO_SKILLS,
  });
}
