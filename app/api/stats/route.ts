import { NextRequest, NextResponse } from "next/server";
import { competitors, alerts, reports, stats } from "@/lib/data";

const ALLOWED_ORIGIN = process.env.NEXT_PUBLIC_APP_URL ?? "";

const SECURITY_HEADERS = {
  "X-Content-Type-Options": "nosniff",
  "Cache-Control": "no-store",
};

export async function GET(req: NextRequest) {
  const origin = req.headers.get("origin");
  if (origin && ALLOWED_ORIGIN && origin !== ALLOWED_ORIGIN) {
    return NextResponse.json(
      { error: "Forbidden" },
      { status: 403, headers: SECURITY_HEADERS }
    );
  }

  const recentAlerts = alerts
    .filter((a) => !a.isRead)
    .slice(0, 3)
    .map((a) => ({
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

  return NextResponse.json(
    {
      competitors: stats.competitorsTracked,
      alerts: stats.activeAlerts,
      reports: reports.length,
      marketScore: stats.marketScore,
      recentAlerts,
      recentCompetitors,
    },
    { headers: SECURITY_HEADERS }
  );
}
