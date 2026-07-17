import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[digitalcolonialism] SWARM_API_URL non défini — mode local");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/digitalcolonialism`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error("upstream");
    const data = await res.json();
    return NextResponse.json(sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "digitalcolonialism unavailable" }),
      { status: 502 }
    );
  }
}
