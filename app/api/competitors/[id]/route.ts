import { NextRequest, NextResponse } from "next/server";
import { competitors } from "@/lib/data";

export async function GET(
  _req: NextRequest,
  props: { params: Promise<{ id: string }> }
) {
  const { id } = await props.params;
  const competitor = competitors.find((c) => c.id === id);

  if (!competitor) {
    return NextResponse.json({ error: "Competitor not found" }, { status: 404 });
  }

  return NextResponse.json(competitor);
}

export async function PATCH(
  req: NextRequest,
  props: { params: Promise<{ id: string }> }
) {
  const { id } = await props.params;
  const competitor = competitors.find((c) => c.id === id);
  if (!competitor) return NextResponse.json({ error: "Competitor not found" }, { status: 404 });

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

  return NextResponse.json(updated);
}

export async function DELETE(
  _req: NextRequest,
  props: { params: Promise<{ id: string }> }
) {
  const { id } = await props.params;
  const competitor = competitors.find((c) => c.id === id);

  if (!competitor) {
    return NextResponse.json({ error: "Competitor not found" }, { status: 404 });
  }

  return NextResponse.json({ success: true });
}
