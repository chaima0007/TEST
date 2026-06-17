import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_REPORT = {
  source: "mock",
  started_at: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
  total_sent: 1247,
  total_replied: 231,
  winner: {
    agent_id: "2.7",
    tone_name: "Secteur Premium",
    sent: 158,
    opened: 89,
    replied: 42,
    paid: 11,
    open_rate: 56.3,
    reply_rate: 26.6,
    conversion_rate: 7.0,
  },
  variants: [
    { agent_id: "2.7", tone_name: "Secteur Premium",     sent: 158, opened: 89, replied: 42, paid: 11, open_rate: 56.3, reply_rate: 26.6, conversion_rate: 7.0,  alpha: 43.0, beta: 59.0  },
    { agent_id: "2.1", tone_name: "Le Factuel",          sent: 142, opened: 71, replied: 34, paid:  8, open_rate: 50.0, reply_rate: 23.9, conversion_rate: 5.6,  alpha: 35.0, beta: 72.0  },
    { agent_id: "2.6", tone_name: "Paris & IDF",         sent: 134, opened: 65, replied: 31, paid:  7, open_rate: 48.5, reply_rate: 23.1, conversion_rate: 5.2,  alpha: 32.0, beta: 68.0  },
    { agent_id: "2.2", tone_name: "L'Amical",            sent: 149, opened: 68, replied: 33, paid:  6, open_rate: 45.6, reply_rate: 22.1, conversion_rate: 4.0,  alpha: 34.0, beta: 81.0  },
    { agent_id: "2.5", tone_name: "Région Sud",          sent: 128, opened: 55, replied: 27, paid:  5, open_rate: 43.0, reply_rate: 21.1, conversion_rate: 3.9,  alpha: 28.0, beta: 73.0  },
    { agent_id: "2.8", tone_name: "Artisans & TPE",      sent: 121, opened: 50, replied: 24, paid:  4, open_rate: 41.3, reply_rate: 19.8, conversion_rate: 3.3,  alpha: 25.0, beta: 73.0  },
    { agent_id: "2.4", tone_name: "Région Nord",         sent: 118, opened: 47, replied: 21, paid:  3, open_rate: 39.8, reply_rate: 17.8, conversion_rate: 2.5,  alpha: 22.0, beta: 75.0  },
    { agent_id: "2.9", tone_name: "Relance & Suivi",     sent: 109, opened: 38, replied: 14, paid:  2, open_rate: 34.9, reply_rate: 12.8, conversion_rate: 1.8,  alpha: 15.0, beta: 70.0  },
    { agent_id: "2.3", tone_name: "Le Client Perdu",     sent: 88,  opened: 31, replied: 9,  paid:  1, open_rate: 35.2, reply_rate: 10.2, conversion_rate: 1.1,  alpha: 10.0, beta: 59.0  },
  ],
};

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/abtesting/report`, {
        next: { revalidate: 60 },
      });
      if (res.ok) {
        const data = await res.json();
        return NextResponse.json({ source: "live", ...data });
      }
    } catch {
      // fall through to mock
    }
  }
  return NextResponse.json(MOCK_REPORT);
}

export async function POST(req: Request) {
  const { agent_id, opened, replied, paid } = await req.json();
  if (SWARM_API_URL) {
    try {
      const params = new URLSearchParams({
        agent_id,
        opened: String(!!opened),
        replied: String(!!replied),
        paid: String(!!paid),
      });
      await fetch(`${SWARM_API_URL}/abtesting/record?${params}`, { method: "POST" });
    } catch {
      // ignore
    }
  }
  return NextResponse.json({ status: "recorded", agent_id });
}
