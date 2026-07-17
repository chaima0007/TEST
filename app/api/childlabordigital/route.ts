import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) console.warn("[childlabordigital] SWARM_API_URL is not set");

export async function GET() {
  try {
    if (!SWARM_API_URL) throw new Error("SWARM_API_URL not configured");
    const res = await fetch(`${SWARM_API_URL}/childlabordigital`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream error: ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data.payload ?? data));
  } catch {
    return sealResponse(NextResponse.json({ error: "Service unavailable" }, { status: 502 }));
  }
}
