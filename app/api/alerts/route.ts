import { NextRequest, NextResponse } from "next/server";
import { alerts } from "@/lib/data";

export async function GET() {
  return NextResponse.json(alerts);
}

export async function PATCH(req: NextRequest) {
  const body = await req.json();

  if (body.markAllRead) {
    return NextResponse.json({ success: true });
  }

  if (body.id) {
    const alert = alerts.find((a) => a.id === body.id);
    if (!alert) return NextResponse.json({ error: "Alert not found" }, { status: 404 });
    return NextResponse.json({ ...alert, isRead: true });
  }

  return NextResponse.json({ error: "Invalid request" }, { status: 400 });
}
