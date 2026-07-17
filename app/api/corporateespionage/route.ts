import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[corporateespionage] SWARM_API_URL is not defined");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/corporateespionage`, {
      next: { revalidate: 30 },
    });
    const d = await res.json();
    return await sealResponse(NextResponse.json(d.payload ?? d));
  } catch {
    return await sealResponse(
      NextResponse.json({ error: "Corporate Espionage service unavailable" }, { status: 502 })
    );
  }
}
