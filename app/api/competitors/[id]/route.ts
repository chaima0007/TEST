import { NextRequest, NextResponse } from "next/server";
import { competitors } from "@/lib/data";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[competitors/[id]] SWARM_API_URL non défini — mode local");
}

export async function GET(
  _req: NextRequest,
  props: { params: Promise<{ id: string }> }
) {
  const { id } = await props.params;
  const competitor = competitors.find((c) => c.id === id);

  if (!competitor) {
    return NextResponse.json(sealResponse({ error: "Competitor not found" }), { status: 404 });
  }

  return NextResponse.json(sealResponse(competitor));
}

export async function PATCH(
  req: NextRequest,
  props: { params: Promise<{ id: string }> }
) {
  const { id } = await props.params;
  const competitor = competitors.find((c) => c.id === id);
  if (!competitor) return NextResponse.json(sealResponse({ error: "Competitor not found" }), { status: 404 });

  const body = await req.json() as {
    name?: string; website?: string; industry?: string;
    description?: string; threatLevel?: string;
  };

  const updated = {
    ...competitor,
    ...(body.name && { name: body.name }),
    ...(body.website && { website: body.website }),
    ...(body.industry !== undefined && { industry: body.industry }),
    ...(body.description !== undefined && { description: body.description }),
    ...(body.threatLevel && { threatLevel: body.threatLevel as "high" | "medium" | "low" }),
    lastUpdated: new Date().toISOString().split("T")[0],
  };

  return NextResponse.json(sealResponse(updated));
}

export async function DELETE(
  _req: NextRequest,
  props: { params: Promise<{ id: string }> }
) {
  const { id } = await props.params;
  const competitor = competitors.find((c) => c.id === id);

  if (!competitor) {
    return NextResponse.json(sealResponse({ error: "Competitor not found" }), { status: 404 });
  }

  return NextResponse.json(sealResponse({ success: true }));
}
