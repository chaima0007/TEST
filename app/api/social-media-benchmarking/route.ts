import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[social-media-benchmarking] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/social_media_benchmarking`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      brands: [
        { brand: "Caelum Partners", isOurs: true, platform: "LinkedIn", engagementRate: 6.8, followers: 4200, growthRate: 12.4, sentimentScore: 84 },
        { brand: "Concurrent A", isOurs: false, platform: "LinkedIn", engagementRate: 3.2, followers: 9800, growthRate: 5.1, sentimentScore: 71 },
      ],
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
