import { NextResponse } from "next/server";
import { prisma } from "@/lib/db";
import { outreach } from "@/lib/outreach/config";

// GET /api/outreach/stats — tableau de bord de la prospection.
export async function GET() {
  const now = new Date();
  // Minuit locale (début de la journée en cours)
  const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate());

  const [grouped, totalProspects, draftMessages, sentToday, lastRuns] =
    await Promise.all([
      prisma.prospect.groupBy({
        by: ["status"],
        _count: { _all: true },
      }),
      prisma.prospect.count(),
      prisma.outreachMessage.count({ where: { status: "draft" } }),
      prisma.outreachMessage.count({
        where: { sentAt: { gte: startOfToday } },
      }),
      prisma.agentRun.findMany({
        orderBy: { startedAt: "desc" },
        take: 10,
      }),
    ]);

  const byStatus: Record<string, number> = {};
  for (const group of grouped) {
    byStatus[group.status] = group._count._all;
  }

  return NextResponse.json({
    byStatus,
    totalProspects,
    draftMessages,
    sentToday,
    dryRun: outreach.dryRun,
    lastRuns,
  });
}
