import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[workflow] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

type DivisionTarget = "1" | "2" | "3" | "4" | "5" | "6";
type WorkflowAction =
  | "send_first_email"
  | "send_followup_email"
  | "handle_objection"
  | "schedule_demo"
  | "send_quote"
  | "follow_up_quote"
  | "negotiate"
  | "close"
  | "generate_invoice"
  | "enrich_prospect"
  | "nurture"
  | "archive"
  | "escalate"
  | "wait";
type Confidence = "high" | "medium" | "low";

interface WorkflowDecision {
  prospect_id: string;
  company_name: string;
  division: DivisionTarget;
  agent_id: string;
  action: WorkflowAction;
  urgency_score: number;
  confidence: Confidence;
  reasoning: string;
  signals_used: string[];
  created_at: string;
}

interface Summary {
  total: number;
  avg_urgency_score: number;
  division_distribution: Record<string, number>;
  action_distribution: Record<string, number>;
  confidence_distribution: Record<string, number>;
}

// Mirrors Python rule engine
function recencyUrgency(days: number): number {
  if (days >= 14) return 40;
  if (days >= 7) return 30;
  if (days >= 3) return 15;
  if (days >= 1) return 8;
  return 0;
}

const STAGE_URGENCY: Record<string, number> = {
  negotiating: 25, quoted: 20, demo: 18, replied: 15,
  opened: 10, contacted: 8, lead: 5, won: 0, lost: 0,
};

function urgency(stage: string, days: number, bant: number, touches: number, buying: number): number {
  const raw = recencyUrgency(days)
    + (STAGE_URGENCY[stage] ?? 0)
    + Math.round(bant / 4)
    + (touches >= 8 ? -20 : touches >= 5 ? -10 : touches >= 3 ? -3 : 0)
    + Math.round(buying * 10);
  return Math.max(0, Math.min(100, raw));
}

function decide(
  pid: string, company: string, sector: string, stage: string,
  bant: number, days: number, touches: number, buying: number,
  objection: string, negStatus: string, quoteSent: boolean,
  invoiceSent: boolean, isLost: boolean
): WorkflowDecision {
  const score = urgency(stage, days, bant, touches, buying);
  const ts = new Date().toISOString();

  function make(div: DivisionTarget, agent: string, action: WorkflowAction, reasoning: string, signals: string[], conf: Confidence = "high"): WorkflowDecision {
    return { prospect_id: pid, company_name: company, division: div, agent_id: agent, action, urgency_score: score, confidence: conf, reasoning, signals_used: signals, created_at: ts };
  }

  if (isLost || stage === "lost") return make("6", "6.9", "archive", "Prospect marqué perdu — archivage.", ["is_lost", "funnel_stage"]);
  if (stage === "won") {
    if (!invoiceSent) return make("5", "5.1", "generate_invoice", "Prospect gagné — génération de la facture.", ["funnel_stage"]);
    return make("4", "4.0", "close", "Facture envoyée — lancement production.", ["funnel_stage", "invoice_sent"]);
  }
  if (stage === "negotiating" || negStatus === "opened" || negStatus === "in_progress") {
    if (negStatus === "failed") return make("3", "3.3", "nurture", "Négociation échouée — séquence empathie post-refus.", ["negotiation_status"], "medium");
    if (buying >= 0.5) return make("3", "3.5", "close", `Signal d'achat fort (${Math.round(buying * 100)}%) — closing immédiat.`, ["funnel_stage", "buying_signal"]);
    return make("3", "3.0", "negotiate", "Prospect en négociation — agent manager Division 3.", ["funnel_stage", "negotiation_status"]);
  }
  if (stage === "quoted" || quoteSent) {
    if (days >= 14) return make("3", "3.5", "follow_up_quote", `Devis sans réponse ${days}j — relance urgente.`, ["funnel_stage", "days_since_contact"]);
    if (days >= 5) return make("2", "2.5", "follow_up_quote", `Relance devis J+${days}.`, ["funnel_stage", "days_since_contact"]);
    return make("2", "2.5", "wait", "Devis récent — attente de réponse.", ["funnel_stage", "days_since_contact"], "medium");
  }
  if (stage === "demo") return make("3", "3.4", "schedule_demo", "Phase démo — planification / confirmation.", ["funnel_stage"]);
  if (stage === "replied" && buying >= 0.5) {
    if (bant >= 75) return make("5", "5.2", "send_quote", `Prospect chaud (BANT ${bant}) — envoi devis.`, ["funnel_stage", "buying_signal", "bant_score"]);
    return make("3", "3.5", "schedule_demo", `Intérêt confirmé mais BANT ${bant} — démo qualif.`, ["buying_signal", "bant_score"], "medium");
  }
  if (stage === "replied" && objection !== "none") {
    const agentMap: Record<string, [string, string]> = {
      price: ["3.1", "argumentation ROI et comparatif prix"],
      trust: ["3.2", "envoi preuves sociales et audit gratuit"],
      timing: ["3.5", "reframe coût du délai"],
      competitor: ["3.1", "différenciation concurrentielle"],
      technical: ["3.4", "démo personnalisée + onboarding"],
    };
    const [agent, reason] = agentMap[objection] ?? ["3.0", "traitement objection générique"];
    return make("3", agent, "handle_objection", `Objection '${objection}' — ${reason}.`, ["funnel_stage", "objection_type"]);
  }
  if (stage === "replied") return make("2", "2.3", "send_followup_email", "Réponse sans signal — email de qualification.", ["funnel_stage"], "medium");
  if (stage === "contacted" || stage === "opened") {
    if (days >= 7) return make("2", "2.4", "send_followup_email", `Sans réponse ${days}j — relance.`, ["funnel_stage", "days_since_contact"]);
    return make("2", "2.4", "wait", `Email récent (${days}j) — attente.`, ["funnel_stage", "days_since_contact"], "medium");
  }
  if (stage === "lead") {
    if (bant < 25) return make("1", "1.5", "enrich_prospect", `BANT faible (${bant}) — enrichissement profil.`, ["funnel_stage", "bant_score"], "medium");
    return make("2", "2.1", "send_first_email", `Lead qualifié (BANT ${bant}) — premier email.`, ["funnel_stage", "bant_score"]);
  }
  return make("2", "2.0", "wait", "Aucune règle — monitoring passif.", [], "low");
}

const MOCK_PROSPECTS = [
  { pid: "p001", c: "BTP Solutions SARL", s: "PME", stage: "negotiating", bant: 92, days: 16, touches: 2, buying: 0.75, obj: "none", neg: "in_progress", q: false, inv: false, lost: false },
  { pid: "p002", c: "Plomberie Martin", s: "artisan", stage: "quoted", bant: 85, days: 14, touches: 2, buying: 0.0, obj: "none", neg: "", q: true, inv: false, lost: false },
  { pid: "p003", c: "Électricité Dubois", s: "artisan", stage: "replied", bant: 80, days: 8, touches: 1, buying: 0.75, obj: "none", neg: "", q: false, inv: false, lost: false },
  { pid: "p004", c: "SAS Rénovation", s: "PME", stage: "replied", bant: 70, days: 6, touches: 3, buying: 0.0, obj: "price", neg: "", q: false, inv: false, lost: false },
  { pid: "p005", c: "Menuiserie Bernard", s: "artisan", stage: "demo", bant: 78, days: 9, touches: 2, buying: 0.25, obj: "none", neg: "", q: false, inv: false, lost: false },
  { pid: "p006", c: "Couverture Lefebvre", s: "artisan", stage: "replied", bant: 55, days: 7, touches: 1, buying: 0.0, obj: "trust", neg: "", q: false, inv: false, lost: false },
  { pid: "p007", c: "Maçonnerie Roux", s: "artisan", stage: "quoted", bant: 76, days: 6, touches: 2, buying: 0.0, obj: "none", neg: "", q: true, inv: false, lost: false },
  { pid: "p008", c: "Chauffage Moreau", s: "artisan", stage: "won", bant: 90, days: 1, touches: 4, buying: 1.0, obj: "none", neg: "agreed", q: true, inv: false, lost: false },
  { pid: "p009", c: "Isolation Thomas", s: "artisan", stage: "contacted", bant: 55, days: 10, touches: 2, buying: 0.0, obj: "none", neg: "", q: false, inv: false, lost: false },
  { pid: "p010", c: "Carrelage Petit", s: "artisan", stage: "replied", bant: 45, days: 5, touches: 2, buying: 0.0, obj: "timing", neg: "", q: false, inv: false, lost: false },
  { pid: "p011", c: "Peinture Durand", s: "artisan", stage: "lead", bant: 60, days: 2, touches: 0, buying: 0.0, obj: "none", neg: "", q: false, inv: false, lost: false },
  { pid: "p012", c: "Élagage Fontaine", s: "artisan", stage: "lead", bant: 15, days: 1, touches: 0, buying: 0.0, obj: "none", neg: "", q: false, inv: false, lost: false },
  { pid: "p013", c: "Climatisation Simon", s: "artisan", stage: "opened", bant: 40, days: 4, touches: 1, buying: 0.0, obj: "none", neg: "", q: false, inv: false, lost: false },
  { pid: "p014", c: "Serrurerie Mercier", s: "artisan", stage: "replied", bant: 50, days: 3, touches: 1, buying: 0.0, obj: "competitor", neg: "", q: false, inv: false, lost: false },
  { pid: "p015", c: "Maçonnerie Perrin", s: "artisan", stage: "lost", bant: 20, days: 30, touches: 6, buying: 0.0, obj: "none", neg: "failed", q: false, inv: false, lost: true },
];

const MOCK_DECISIONS: WorkflowDecision[] = MOCK_PROSPECTS
  .map(({ pid, c, s, stage, bant, days, touches, buying, obj, neg, q, inv, lost }) =>
    decide(pid, c, s, stage, bant, days, touches, buying, obj, neg, q, inv, lost)
  )
  .sort((a, b) => b.urgency_score - a.urgency_score);

function buildSummary(decisions: WorkflowDecision[]): Summary {
  const divDist: Record<string, number> = {};
  const actDist: Record<string, number> = {};
  const confDist: Record<string, number> = {};
  let totalScore = 0;

  for (const d of decisions) {
    divDist[d.division] = (divDist[d.division] ?? 0) + 1;
    actDist[d.action] = (actDist[d.action] ?? 0) + 1;
    confDist[d.confidence] = (confDist[d.confidence] ?? 0) + 1;
    totalScore += d.urgency_score;
  }

  return {
    total: decisions.length,
    avg_urgency_score: decisions.length
      ? Math.round((totalScore / decisions.length) * 10) / 10
      : 0,
    division_distribution: divDist,
    action_distribution: actDist,
    confidence_distribution: confDist,
  };
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);

  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/workflow/queue`, { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch { /* fall through */ }
  }

  const division = searchParams.get("division");
  const action = searchParams.get("action");
  const limit = searchParams.get("limit");

  let decisions = MOCK_DECISIONS;
  if (division) decisions = decisions.filter((d) => d.division === division);
  if (action) decisions = decisions.filter((d) => d.action === action);
  if (limit) decisions = decisions.slice(0, parseInt(limit));

  return sealResponse(NextResponse.json({ decisions, summary: buildSummary(MOCK_DECISIONS) }));
}

export async function POST(request: Request) {
  if (SWARM_API_URL) {
    try {
      const body = await request.json();
      const res = await fetch(`${SWARM_API_URL}/workflow/decide`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
        cache: "no-store",
      });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch { /* fall through */ }
  }
  return sealResponse(NextResponse.json({ error: "SWARM_API_URL not configured" }, { status: 501 }));
}
