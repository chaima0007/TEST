import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";
const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) console.warn("[corporate-impunity-rights-engine] SWARM_API_URL not set");
export async function GET() {
  try {
    const upstream = await fetch(`${SWARM_API_URL}/corporate-impunity-rights-engine`, { next: { revalidate: 30 } });
    const data = await upstream.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse({ error: "upstream_unavailable" }), { status: 502 });
  }
}
