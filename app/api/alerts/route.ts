import { NextRequest, NextResponse } from "next/server";
import { alerts } from "@/lib/data";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[alerts] SWARM_API_URL non défini — mode local");
}

export async function GET() {
  try {
    return NextResponse.json(sealResponse(alerts));
  } catch {
    return NextResponse.json(sealResponse({ error: "upstream error" }), { status: 502 });
  }
}

export async function PATCH(req: NextRequest) {
  try {
    const body = await req.json();

    if (body.markAllRead) {
      return NextResponse.json(sealResponse({ success: true }));
    }

    if (body.id) {
      const alert = alerts.find((a) => a.id === body.id);
      if (!alert) return NextResponse.json(sealResponse({ error: "Alert not found" }), { status: 404 });
      return NextResponse.json(sealResponse({ ...alert, isRead: true }));
    }

    return NextResponse.json(sealResponse({ error: "Invalid request" }), { status: 400 });
  } catch {
    return NextResponse.json(sealResponse({ error: "upstream error" }), { status: 502 });
  }
}
