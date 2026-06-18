import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

type ActionType =
  | "call"
  | "email"
  | "demo"
  | "send_quote"
  | "follow_quote"
  | "negotiate"
  | "check_in"
  | "close"
  | "skip";

type Priority = "urgent" | "high" | "medium" | "low";

interface FollowUpTask {
  prospect_id: string;
  company_name: string;
  sector: string;
  current_stage: string;
  urgency_score: number;
  priority: Priority;
  recommended_action: ActionType;
  days_since_contact: number;
  bant_score: number;
  touches: number;
  quote_value: number;
  notes: string;
  created_at: string;
}

// Mirrors Python urgency calculation
function recencyUrgency(days: number): number {
  if (days >= 14) return 40;
  if (days >= 7) return 30;
  if (days >= 3) return 15;
  if (days >= 1) return 8;
  return 0;
}

const STAGE_URGENCY: Record<string, number> = {
  negotiating: 25,
  quoted: 20,
  demo: 18,
  replied: 15,
  opened: 10,
  contacted: 8,
  lead: 5,
  won: 0,
  lost: 0,
};

const STAGE_ACTION: Record<string, ActionType> = {
  lead: "email",
  contacted: "email",
  opened: "email",
  replied: "call",
  demo: "demo",
  quoted: "follow_quote",
  negotiating: "negotiate",
  won: "skip",
  lost: "skip",
};

function bantUrgency(bant: number): number {
  return Math.round(bant / 4);
}

function touchesPenalty(touches: number): number {
  if (touches >= 8) return -20;
  if (touches >= 5) return -10;
  if (touches >= 3) return -3;
  return 0;
}

function calcUrgency(stage: string, days: number, bant: number, touches: number): number {
  const raw =
    recencyUrgency(days) +
    (STAGE_URGENCY[stage] ?? 0) +
    bantUrgency(bant) +
    touchesPenalty(touches);
  return Math.max(0, Math.min(100, raw));
}

function calcPriority(score: number): Priority {
  if (score >= 75) return "urgent";
  if (score >= 50) return "high";
  if (score >= 25) return "medium";
  return "low";
}

function mk(
  id: string,
  company: string,
  sector: string,
  stage: string,
  days: number,
  bant: number,
  touches: number,
  quote: number,
  notes = ""
): FollowUpTask {
  const score = calcUrgency(stage, days, bant, touches);
  return {
    prospect_id: id,
    company_name: company,
    sector,
    current_stage: stage,
    urgency_score: score,
    priority: calcPriority(score),
    recommended_action: STAGE_ACTION[stage] ?? "email",
    days_since_contact: days,
    bant_score: bant,
    touches,
    quote_value: quote,
    notes,
    created_at: new Date().toISOString(),
  };
}

const MOCK_TASKS: FollowUpTask[] = [
  mk("p001", "Plomberie Martin", "artisan", "negotiating", 14, 95, 2, 1_490.0, "Attend réponse sur délai"),
  mk("p002", "Électricité Dubois", "artisan", "quoted", 10, 85, 1, 980.0, "Devis envoyé il y a 10j"),
  mk("p003", "SAS Rénovation Plus", "PME", "negotiating", 8, 90, 3, 3_200.0),
  mk("p004", "Menuiserie Bernard", "artisan", "demo", 9, 78, 2, 760.0),
  mk("p005", "Couverture Lefebvre", "artisan", "replied", 7, 70, 1, 540.0),
  mk("p006", "Chauffage Moreau", "artisan", "quoted", 12, 82, 2, 1_150.0),
  mk("p007", "BTP Solutions SARL", "PME", "negotiating", 16, 88, 1, 5_800.0),
  mk("p008", "Carrelage Petit", "artisan", "replied", 8, 65, 2, 430.0, "Intéressé, attendre rappel"),
  mk("p009", "Peinture Durand", "artisan", "demo", 6, 72, 1, 620.0),
  mk("p010", "Maçonnerie Roux", "artisan", "quoted", 15, 76, 0, 890.0),
  mk("p011", "Isolation Thomas", "artisan", "contacted", 4, 55, 2, 0),
  mk("p012", "Menuiserie Garnier", "artisan", "opened", 3, 40, 1, 0),
  mk("p013", "Élagage Fontaine", "artisan", "lead", 5, 30, 0, 0),
  mk("p014", "Climatisation Simon", "artisan", "lead", 2, 25, 1, 0),
  mk("p015", "Serrurerie Mercier", "artisan", "contacted", 6, 48, 3, 0),
];

const TASKS_SORTED = [...MOCK_TASKS].sort((a, b) => b.urgency_score - a.urgency_score);

function buildSummary(tasks: FollowUpTask[]) {
  const dist: Record<Priority, number> = { urgent: 0, high: 0, medium: 0, low: 0 };
  const actionDist: Record<string, number> = {};
  let totalScore = 0;
  let pipeline = 0;

  for (const t of tasks) {
    dist[t.priority]++;
    actionDist[t.recommended_action] = (actionDist[t.recommended_action] ?? 0) + 1;
    totalScore += t.urgency_score;
    if (t.quote_value > 0) pipeline += t.quote_value;
  }

  return {
    total: tasks.length,
    urgent: dist.urgent,
    high: dist.high,
    medium: dist.medium,
    low: dist.low,
    avg_urgency_score: tasks.length ? Math.round((totalScore / tasks.length) * 10) / 10 : 0,
    overdue_7d: tasks.filter((t) => t.days_since_contact >= 7).length,
    overdue_14d: tasks.filter((t) => t.days_since_contact >= 14).length,
    total_pipeline_eur: Math.round(pipeline * 100) / 100,
    action_breakdown: actionDist,
  };
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const action = searchParams.get("action");
  const priority = searchParams.get("priority");
  const stage = searchParams.get("stage");
  const limit = searchParams.get("limit");
  const overdue = searchParams.get("overdue");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/followup`);
      searchParams.forEach((v, k) => url.searchParams.set(k, v));
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {
      // fall through to mock
    }
  }

  let tasks = TASKS_SORTED;

  if (action) tasks = tasks.filter((t) => t.recommended_action === action);
  if (priority) tasks = tasks.filter((t) => t.priority === priority);
  if (stage) tasks = tasks.filter((t) => t.current_stage === stage);
  if (overdue) {
    const threshold = parseFloat(overdue);
    tasks = tasks.filter((t) => t.days_since_contact >= threshold);
  }
  if (limit) tasks = tasks.slice(0, parseInt(limit));

  const summary = buildSummary(TASKS_SORTED);

  return NextResponse.json({ tasks, summary });
}

export async function POST(request: Request) {
  if (SWARM_API_URL) {
    try {
      const body = await request.json();
      const res = await fetch(`${SWARM_API_URL}/followup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
        cache: "no-store",
      });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {
      // fall through
    }
  }
  return NextResponse.json({ error: "SWARM_API_URL not configured" }, { status: 501 });
}

export async function DELETE() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/followup/reset`, {
        method: "DELETE",
        cache: "no-store",
      });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {
      // fall through
    }
  }
  return NextResponse.json({ reset: true });
}
