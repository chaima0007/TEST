import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getDemoUser } from "@/lib/auth";

export async function GET() {
  const user = await getDemoUser();
  if (!user) return NextResponse.json({ error: "User not found" }, { status: 404 });

  const reports = await prisma.report.findMany({
    where: { userId: user.id },
    orderBy: { createdAt: "desc" },
  });

  return NextResponse.json(reports);
}

export async function POST(req: NextRequest) {
  const user = await getDemoUser();
  if (!user) return NextResponse.json({ error: "User not found" }, { status: 404 });

  const body = await req.json().catch(() => ({}));
  const { title, description, pages } = body as {
    title?: string;
    description?: string;
    pages?: number;
  };

  const now = new Date();
  const dateStr = now.toISOString().split("T")[0];

  const report = await prisma.report.create({
    data: {
      title: title || `Rapport Concurrentiel — ${dateStr}`,
      description:
        description ||
        "Rapport généré automatiquement avec les dernières données du marché.",
      pages: pages || 15,
      userId: user.id,
    },
  });

  return NextResponse.json(report, { status: 201 });
}
