import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;
export const revalidate = 30;

export async function GET() {
  if (!SWARM_API_URL) return NextResponse.json(sealResponse({ error: "SWARM_API_URL not configured" }), { status: 502 });
  try {
    const res = await fetch(`${SWARM_API_URL}/api/pharmaceutical-access-patents-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data));
  } catch {
    return NextResponse.json(sealResponse({ engine: "PAP_ENGINE", entities: [] }), { status: 502 });
  }
}
