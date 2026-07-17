import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[schooltoprisonpipeline] SWARM_API_URL non défini — mode local");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/schooltoprisonpipeline`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error("upstream");
    const data = await res.json();
    return NextResponse.json(sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "schooltoprisonpipeline unavailable" }),
      { status: 502 }
    );
  }
}
