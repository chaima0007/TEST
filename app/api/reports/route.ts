import { NextRequest, NextResponse } from "next/server";
import { reports } from "@/lib/data";

export async function GET() {
  return NextResponse.json(reports);
}

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => ({}));
  const { title, description, pages } = body as {
    title?: string; description?: string; pages?: number;
  };

  const now = new Date();
  const dateStr = now.toISOString().split("T")[0];

  const report = {
    id: String(Date.now()),
    title: title || `Rapport Concurrentiel — ${dateStr}`,
    description: description || "Rapport généré automatiquement avec les dernières données du marché.",
    createdAt: dateStr,
    pages: pages || 15,
    status: "ready",
  };

  return NextResponse.json(report, { status: 201 });
}
