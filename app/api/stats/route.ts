import { NextResponse } from "next/server";
import { competitors, alerts, reports, stats } from "@/lib/data";

export async function GET() {
  const recentAlerts = alerts.filter((a) => !a.isRead).slice(0, 3).map((a) => ({
    id: a.id,
    type: a.type,
    message: a.message,
    createdAt: a.date,
  }));
  const recentCompetitors = competitors.slice(0, 5).map((c) => ({
    id: c.id,
    name: c.name,
    industry: c.industry,
    threatLevel: c.threatLevel,
    logo: c.logo,
    color: c.color,
  }));

  return NextResponse.json({
    competitors: stats.competitorsTracked,
    alerts: stats.activeAlerts,
    reports: reports.length,
    marketScore: stats.marketScore,
    recentAlerts,
    recentCompetitors,
  });
}
