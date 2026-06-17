import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

const DEMO_USER_EMAIL = "demo@competeiq.com";

export async function GET() {
  const user = await prisma.user.findUnique({
    where: { email: DEMO_USER_EMAIL },
  });

  if (!user) {
    return NextResponse.json({ error: "User not found" }, { status: 404 });
  }

  const [competitors, alerts, reports] = await Promise.all([
    prisma.competitor.count({ where: { userId: user.id } }),
    prisma.alert.count({ where: { userId: user.id, isRead: false } }),
    prisma.report.count({ where: { userId: user.id } }),
  ]);

  return NextResponse.json({
    competitors,
    alerts,
    reports,
    marketScore: 74,
  });
}
