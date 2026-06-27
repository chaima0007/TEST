import { NextResponse } from "next/server";
import { EDITORIAL_ITEMS, WEEKLY_THEMES, TYPE_META, STATUS_META } from "@/lib/editorial-data";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[editorial] SWARM_API_URL non défini — mode local");
}

export async function GET() {
  try {
    return NextResponse.json(sealResponse({
      items: EDITORIAL_ITEMS,
      themes: WEEKLY_THEMES,
      type_meta: TYPE_META,
      status_meta: STATUS_META,
    }));
  } catch {
    return NextResponse.json(sealResponse({ error: "upstream error" }), { status: 502 });
  }
}
