import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

const DEMO_USER_EMAIL = "demo@competeiq.com";

async function getDemoUser() {
  return prisma.user.findUnique({ where: { email: DEMO_USER_EMAIL } });
}

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
