import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";
if (!process.env.SWARM_API_URL) { console.warn("[psychiatric-abuse-rights-engine] SWARM_API_URL is not set"); }
export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/psychiatric-abuse-rights-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream error: ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({ error: "Upstream unavailable" }, { status: 502 }));
  }
}
