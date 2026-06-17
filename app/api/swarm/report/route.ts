import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/finance/report`, {
        next: { revalidate: 60 },
      });
      if (res.ok) {
        const data = await res.json();
        return NextResponse.json(data);
      }
    } catch {}
  }

  // Mock last cycle report
  return NextResponse.json({
    cycle_id: "cycle_20260617_demo",
    generated_at: new Date().toISOString(),
    revenue_eur: 2237,
    prospects_found: 847,
    emails_sent: 312,
    paid_count: 4,
    division_status: {
      "1": "success",
      "2": "success",
      "3": "success",
      "4": "success",
      "5": "success",
      "6": "success",
    },
    errors: [],
    source: "mock",
  });
}
