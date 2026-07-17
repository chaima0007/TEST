import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[tcfdreporting] SWARM_API_URL non défini — vérifier .env");
}

export async function GET() {
  try {
    const upstream = process.env.SWARM_API_URL
      ? await fetch(`${process.env.SWARM_API_URL}/api/tcfdreporting`, {
          next: { revalidate: 30 },
        }).then((r) => r.json())
      : null;

    const data = upstream ?? {
      domain: "tcfdreporting",
      estimated_tcfdreporting_index: 6.1,
      avg_composite: 61.03,
      risk_level: "critique",
      entities: [],
    };

    return NextResponse.json(sealResponse(data));
  } catch {
    return NextResponse.json(sealResponse({ error: "tcfdreporting unavailable" }), { status: 502 });
  }
}
