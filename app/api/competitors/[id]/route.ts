import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getDemoUser } from "@/lib/auth";

export async function GET(
  _req: NextRequest,
  props: { params: Promise<{ id: string }> }
) {
  const { id } = await props.params;
  const user = await getDemoUser();
  if (!user) return NextResponse.json({ error: "User not found" }, { status: 404 });

  const competitor = await prisma.competitor.findFirst({
    where: { id, userId: user.id },
    include: { pricingPlans: true, features: true, news: true },
  });

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
  const user = await getDemoUser();
  if (!user) return NextResponse.json({ error: "User not found" }, { status: 404 });

  const competitor = await prisma.competitor.findFirst({ where: { id, userId: user.id } });
  if (!competitor) return NextResponse.json({ error: "Competitor not found" }, { status: 404 });

  const body = await req.json() as {
    name?: string; website?: string; industry?: string;
    description?: string; threatLevel?: string;
  };

  const updated = await prisma.competitor.update({
    where: { id },
    data: {
      ...(body.name && { name: body.name }),
      ...(body.website && { website: body.website }),
      ...(body.industry !== undefined && { industry: body.industry }),
      ...(body.description !== undefined && { description: body.description }),
      ...(body.threatLevel && { threatLevel: body.threatLevel }),
      lastUpdated: new Date().toISOString().split("T")[0],
    },
  });

  return NextResponse.json(updated);
}

export async function DELETE(
  _req: NextRequest,
  props: { params: Promise<{ id: string }> }
) {
  const { id } = await props.params;
  const user = await getDemoUser();
  if (!user) return NextResponse.json({ error: "User not found" }, { status: 404 });

  const competitor = await prisma.competitor.findFirst({
    where: { id, userId: user.id },
  });

  if (!competitor) {
    return NextResponse.json({ error: "Competitor not found" }, { status: 404 });
  }

  await prisma.competitor.delete({ where: { id } });

  return NextResponse.json({ success: true });
}
