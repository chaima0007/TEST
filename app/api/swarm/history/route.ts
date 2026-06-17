import { NextResponse } from "next/server";
import { PrismaClient } from "@/lib/generated/prisma/client";
import { PrismaLibSql } from "@prisma/adapter-libsql";

const adapter = new PrismaLibSql({ url: process.env.DATABASE_URL ?? "file:./dev.db" });
const prisma = new PrismaClient({ adapter } as any);

export async function GET() {
  try {
    const [cycles, transactions, prospects] = await Promise.all([
      prisma.swarmCycle.findMany({
        orderBy: { startedAt: "desc" },
        take: 10,
        include: {
          jobs: {
            select: { status: true, quoteEur: true, paymentConfirmed: true },
          },
        },
      }),
      prisma.swarmTransaction.findMany({
        orderBy: { createdAt: "desc" },
        take: 20,
      }),
      prisma.swarmProspect.findMany({
        orderBy: { pagespeedScore: "asc" },
        take: 20,
        where: { blacklisted: false },
      }),
    ]);

    const cyclesOut = cycles.map((c) => ({
      id: c.id,
      cycleKey: c.cycleKey,
      startedAt: c.startedAt,
      completedAt: c.completedAt,
      prospectsFound: c.prospectsFound,
      emailsSent: c.emailsSent,
      revenueEur: c.revenueEur,
      jobCount: c.jobs.length,
      paidCount: c.jobs.filter((j) => j.paymentConfirmed).length,
      successCount: c.jobs.filter((j) => j.status === "success").length,
      totalQuoteEur: c.jobs.reduce((s, j) => s + (j.quoteEur ?? 0), 0),
    }));

    return NextResponse.json({ cycles: cyclesOut, transactions, prospects });
  } catch (err) {
    return NextResponse.json(
      { cycles: [], transactions: [], prospects: [], error: "DB unavailable" },
      { status: 200 }
    );
  }
}
