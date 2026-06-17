import { NextRequest, NextResponse } from "next/server";
import { competitors } from "@/lib/data";

export async function GET() {
  return NextResponse.json(competitors);
}

export async function POST(req: NextRequest) {
  const body = await req.json();
  const { name, website } = body;

  if (!name || !website) {
    return NextResponse.json({ error: "Name and website are required" }, { status: 400 });
  }

  const newCompetitor = {
    id: String(Date.now()),
    name,
    website,
    industry: body.industry || "Non spécifié",
    description: body.description || "",
    threatLevel: (body.threatLevel || "medium") as "high" | "medium" | "low",
    logo: name.slice(0, 2).toUpperCase(),
    color: "#6366f1",
    founded: new Date().getFullYear(),
    employees: "N/A",
    revenue: "N/A",
    marketShare: 0,
    lastUpdated: new Date().toISOString().split("T")[0],
    pricing: [],
    features: [],
    news: [],
    priceHistory: [],
  };

  return NextResponse.json(newCompetitor, { status: 201 });
}
