import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[dedup] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const REASONS = ["opt_out", "bounce", "spam", "unreachable", "competitor", "client"] as const;
type Reason = typeof REASONS[number];

function rnd(min: number, max: number) { return Math.floor(Math.random() * (max - min + 1)) + min; }
function pick<T>(arr: readonly T[]): T { return arr[Math.floor(Math.random() * arr.length)]; }

function mockSuppression(n: number) {
  return Array.from({ length: n }, (_, i) => ({
    key: `contact${i}@suppressed-company${i}.fr`,
    key_type: i % 5 === 0 ? "domain" : "email",
    reason: pick(REASONS) as Reason,
    added_at: new Date(Date.now() - rnd(1, 90) * 86400000).toISOString(),
    note: "",
  }));
}

function buildMockData() {
  const emailsContacted = rnd(420, 950);
  const domainsContacted = rnd(180, 400);
  const suppressionSize  = rnd(12, 60);

  return {
    source: "mock",
    summary: {
      unique_emails_contacted: emailsContacted,
      unique_domains_contacted: domainsContacted,
      suppression_list_size: suppressionSize,
      fingerprints_seen: emailsContacted + rnd(0, 50),
      total_contact_events: emailsContacted + rnd(50, 300),
    },
    entries: mockSuppression(suppressionSize),
  };
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/dedup/suppression-list`, { next: { revalidate: 30 } });
      if (res.ok) return sealResponse(NextResponse.json({ source: "live", ...(await res.json()) }));
    } catch { /* fall through */ }
  }
  return sealResponse(NextResponse.json(buildMockData()));
}
