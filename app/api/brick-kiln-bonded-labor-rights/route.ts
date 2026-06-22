import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[brick-kiln-bonded-labor-rights] SWARM_API_URL non défini");
}

export async function GET() {
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/brick_kiln_bonded_labor_rights_engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(
      NextResponse.json({ error: "Upstream unavailable" }, { status: 502 })
    );
  }
}
