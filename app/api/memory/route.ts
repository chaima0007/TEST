import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[memory] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const SECTORS   = ["artisan", "restaurant", "médical", "garage", "immobilier", "juridique", "beauté"];
const STAGES    = ["contacted", "replied", "negotiating", "quoted", "won", "lost"] as const;
const SENTIMENTS = ["positif", "négatif", "neutre", "curieux", "sceptique", "méfiant"] as const;
const OBJECTIONS = ["price", "trust", "timing", "competitor", "none"] as const;
const TRENDS    = ["improving", "declining", "stable", "unknown"] as const;
const AGENTS    = ["2.1", "2.2", "3.1", "3.2", "3.3"] as const;

type Stage = typeof STAGES[number];

function rnd(min: number, max: number) { return Math.floor(Math.random() * (max - min + 1)) + min; }
function pick<T>(arr: readonly T[]): T { return arr[Math.floor(Math.random() * arr.length)]; }
function isoAgo(days: number) { return new Date(Date.now() - days * 86400000).toISOString(); }

const COMPANY_NAMES = [
  "Artisan Pro SARL", "Boulangerie Martin", "Cabinet Dr. Lefèvre", "Garage Dupont",
  "Immo Prestige", "Maître Rousseau", "Centre de Formation Top", "Salon Élite",
  "Association Solidarité", "Charpenterie Moreau", "Restaurant La Cigale",
  "Plomberie Express", "Auto Mécanique Renault", "Notaire & Associés",
];

function makeMessage(direction: "outbound" | "inbound", i: number) {
  const contents = {
    outbound: ["Bonjour, nous avons analysé votre site web...", "Suite à notre échange précédent...", "Voici notre proposition personnalisée..."],
    inbound:  ["Merci pour votre message, c'est intéressant.", "Le prix me semble élevé...", "Je suis intéressé, pouvez-vous m'en dire plus ?", "Je dois réfléchir."],
  };
  return {
    direction,
    content: pick(contents[direction]),
    timestamp: isoAgo(rnd(0, 14)),
    agent_id: direction === "outbound" ? pick(AGENTS) : "",
    sentiment: pick(SENTIMENTS),
    objection_type: direction === "inbound" ? pick(OBJECTIONS) : "none",
  };
}

function makeProspect(index: number) {
  const touchCount = rnd(1, 6);
  const replyCount = rnd(0, touchCount);
  const stage: Stage = pick(STAGES);
  const messages = [
    ...Array.from({ length: touchCount }, (_, i) => makeMessage("outbound", i)),
    ...Array.from({ length: replyCount }, (_, i) => makeMessage("inbound", i)),
  ].sort(() => Math.random() - 0.5).slice(0, 5);

  return {
    prospect_id: `p${String(index).padStart(3, "0")}`,
    company_name: pick(COMPANY_NAMES) + ` ${index}`,
    sector: pick(SECTORS),
    email: `contact${index}@prospect${index}.fr`,
    created_at: isoAgo(rnd(5, 60)),
    stage,
    touch_count: touchCount,
    reply_count: replyCount,
    latest_sentiment: pick(SENTIMENTS),
    sentiment_trend: pick(TRENDS),
    objections_seen: Array.from(new Set([pick(OBJECTIONS), pick(OBJECTIONS)])).filter(o => o !== "none"),
    tags: rnd(0, 1) ? ["hot"] : [],
    assigned_agent: pick(AGENTS),
    quote_eur: stage === "quoted" || stage === "won" ? rnd(299, 1499) : 0,
    notes: "",
    last_contacted_at: isoAgo(rnd(0, 14)),
    message_count: touchCount + replyCount,
    messages,
    sentiment_history: Array.from({ length: rnd(1, 4) }, (_, i) => ({
      sentiment: pick(SENTIMENTS),
      score: Math.round(Math.random() * 1000) / 1000,
      timestamp: isoAgo(rnd(0, 14)),
    })),
  };
}

function buildMockData() {
  const prospects = Array.from({ length: 24 }, (_, i) => makeProspect(i + 1));
  const byStage: Record<string, number> = {};
  for (const p of prospects) {
    byStage[p.stage] = (byStage[p.stage] ?? 0) + 1;
  }
  const wonRevenue = prospects.filter(p => p.stage === "won").reduce((s, p) => s + p.quote_eur, 0);

  return {
    source: "mock",
    summary: {
      total_prospects: prospects.length,
      by_stage: byStage,
      active_negotiations: (byStage["negotiating"] ?? 0) + (byStage["quoted"] ?? 0),
      won_deals: byStage["won"] ?? 0,
      total_won_revenue_eur: wonRevenue,
      total_messages: prospects.reduce((s, p) => s + p.message_count, 0),
      avg_touches: Math.round(prospects.reduce((s, p) => s + p.touch_count, 0) / prospects.length * 10) / 10,
    },
    prospects,
  };
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/memory/prospects`, { next: { revalidate: 15 } });
      if (res.ok) return sealResponse(NextResponse.json({ source: "live", ...(await res.json()) }));
    } catch { /* fall through */ }
  }
  return sealResponse(NextResponse.json(buildMockData()));
}
