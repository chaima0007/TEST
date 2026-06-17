import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getDemoUser } from "@/lib/auth";

export async function GET() {
  const user = await getDemoUser();
  if (!user) return NextResponse.json({ error: "User not found" }, { status: 404 });

  const [competitorCount, alertCount, reportCount, recentAlerts, recentCompetitors] = await Promise.all([
    prisma.competitor.count({ where: { userId: user.id } }),
    prisma.alert.count({ where: { userId: user.id, isRead: false } }),
    prisma.report.count({ where: { userId: user.id } }),
    prisma.alert.findMany({
      where: { userId: user.id, isRead: false },
      orderBy: { createdAt: "desc" },
      take: 3,
    }),
    prisma.competitor.findMany({
      where: { userId: user.id },
      orderBy: { createdAt: "desc" },
      take: 5,
      select: { id: true, name: true, industry: true, threatLevel: true, logo: true, color: true },
    }),
  ]);

  return NextResponse.json({
    competitors: competitorCount,
    alerts: alertCount,
    reports: reportCount,
    marketScore: 74,
    recentAlerts,
    recentCompetitors,
  });
}
