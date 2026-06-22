import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";
if (!process.env.SWARM_API_URL) { console.warn("[climate-displacement-rights] SWARM_API_URL non défini"); }
export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/climate_displacement_rights_engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream error: ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({ error: "Upstream unavailable" }, { status: 502 }));
  }
}
