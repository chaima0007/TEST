import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[corporate-tax-evasion-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

export const revalidate = 30;

export async function GET() {
  if (!SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse({ error: "SWARM_API_URL not configured" }), { status: 502 }));
  }
  try {
    const res = await fetch(`${SWARM_API_URL}/api/corporate-tax-evasion-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(sealResponse({ engine: "CTE_ENGINE", entities: [] }), { status: 502 }));
  }
}
