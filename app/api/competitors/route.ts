import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getDemoUser } from "@/lib/auth";

export async function GET() {
  const user = await getDemoUser();
  if (!user) return NextResponse.json({ error: "User not found" }, { status: 404 });

  const competitors = await prisma.competitor.findMany({
    where: { userId: user.id },
    include: { pricingPlans: true, features: true, news: true },
    orderBy: { createdAt: "desc" },
  });

  return NextResponse.json(competitors);
}

export async function POST(req: NextRequest) {
  const user = await getDemoUser();
  if (!user) return NextResponse.json({ error: "User not found" }, { status: 404 });

  const body = await req.json();
  const { name, website, industry, description, threatLevel } = body;

  if (!name || !website) {
    return NextResponse.json({ error: "Name and website are required" }, { status: 400 });
  }

  const competitor = await prisma.competitor.create({
    data: {
      name,
      website,
      industry: industry || "Non spécifié",
      description: description || "",
      threatLevel: threatLevel || "medium",
      logo: name.slice(0, 2).toUpperCase(),
      lastUpdated: new Date().toISOString().split("T")[0],
      userId: user.id,
    },
  });

  return NextResponse.json(competitor, { status: 201 });
}
