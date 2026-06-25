import { NextRequest, NextResponse } from "next/server";
import { reports } from "@/lib/data";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[reports] SWARM_API_URL non défini — mode local");
}

export async function GET() {
  try {
    return NextResponse.json(sealResponse(reports));
  } catch {
    return NextResponse.json(sealResponse({ error: "upstream error" }), { status: 502 });
  }
}

export async function POST(req: NextRequest) {
  try {
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

    return NextResponse.json(sealResponse(report), { status: 201 });
  } catch {
    return NextResponse.json(sealResponse({ error: "upstream error" }), { status: 502 });
  }
}
