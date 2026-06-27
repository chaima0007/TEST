import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const SECTORS = ["artisan", "restaurant", "médical", "garage", "immobilier", "juridique", "formation", "beauté", "association"];
const AGENTS  = ["2.1", "2.2", "2.3", "2.4", "2.5"];
const PRIORITIES = ["urgent", "high", "normal", "low"] as const;
const TIERS = ["A", "B", "C"] as const;
const STATUSES = ["pending", "pending", "pending", "running", "done", "cancelled"] as const;

function rnd(min: number, max: number) { return Math.floor(Math.random() * (max - min + 1)) + min; }
function pick<T>(arr: readonly T[]): T { return arr[Math.floor(Math.random() * arr.length)]; }

function isoFuture(daysAhead: number, hour: number) {
  const d = new Date();
  d.setDate(d.getDate() + daysAhead);
  d.setHours(hour, 0, 0, 0);
  return d.toISOString();
}

function buildMockData() {
  const plans = [];
  let totalWaves = 0;
  let totalEmails = 0;
  let pending = 0, done = 0, cancelled = 0;

  for (let p = 0; p < 6; p++) {
    const sector = pick(SECTORS);
    const agent  = pick(AGENTS);
    const volume = rnd(30, 200);
    const waveCount = Math.ceil(volume / 50);
    const waves = [];

    for (let w = 0; w < waveCount; w++) {
      const count = Math.min(50, volume - w * 50);
      const status = pick(STATUSES);
      const wave = {
        wave_id: `plan_${p.toString(16).padStart(10, "0")}_w${w + 1}`,
        sector,
        agent_id: agent,
        email_count: count,
        scheduled_at: isoFuture(w * 1 + rnd(0, 2), pick([7, 8, 9, 10])),
        priority: pick(PRIORITIES),
        tier_filter: pick(TIERS),
        status,
      };
      waves.push(wave);
      if (status === "pending") pending++;
      else if (status === "done") done++;
      else if (status === "cancelled") cancelled++;
      totalEmails += count;
    }
    totalWaves += waveCount;

    plans.push({
      plan_id: `plan_${p.toString(16).padStart(10, "0")}`,
      created_at: new Date().toISOString(),
      total_emails: volume,
      total_waves: waveCount,
      sector,
      agent_id: agent,
      waves,
    });
  }

  return {
    source: "mock",
    summary: {
      total_plans: plans.length,
      total_waves: totalWaves,
      total_emails_planned: totalEmails,
      pending,
      done,
      cancelled,
    },
    plans,
  };
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/campaigns/summary`, { next: { revalidate: 15 } });
      if (res.ok) return NextResponse.json({ source: "live", ...(await res.json()) });
    } catch { /* fall through */ }
  }
  return NextResponse.json(buildMockData());
}
