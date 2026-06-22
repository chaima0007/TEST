import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[transgender-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}
const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) console.warn("[transgender-rights-engine] SWARM_API_URL not set");
export async function GET() {
  try {
    const upstream = await fetch(`${SWARM_API_URL}/transgender-rights-engine`, { next: { revalidate: 30 } });
    const data = await upstream.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse({ error: "upstream_unavailable" }), { status: 502 }));
  }
}
