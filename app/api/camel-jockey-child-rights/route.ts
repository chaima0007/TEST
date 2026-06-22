import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[camel-jockey-child-rights] SWARM_API_URL non défini");
}

export async function GET() {
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/camel_jockey_child_rights_engine`,
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
