import { NextRequest, NextResponse } from "next/server";
import { competitors } from "@/lib/data";
import { authenticateShopify, unauthorizedResponse } from "@/lib/shopify/authenticate";

// Competitive-intelligence data for the embedded App Home, authenticated with
// the App Bridge session token instead of the CompeteIQ dashboard cookie.
export async function GET(request: NextRequest) {
  try {
    await authenticateShopify(request);
  } catch (error) {
    return unauthorizedResponse(error);
  }

  return NextResponse.json(
    competitors.map((c) => ({
      id: c.id,
      name: c.name,
      website: c.website,
      industry: c.industry,
      threatLevel: c.threatLevel,
      marketShare: c.marketShare,
      lastUpdated: c.lastUpdated,
      startingPrice: c.pricing.find((p) => p.price > 0)?.price ?? 0,
      latestNews: c.news[0]?.title ?? null,
    })),
  );
}
