import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[leads] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

// ── Scoring logic mirroring Python LeadScorer ─────────────────────────────────

const SECTOR_DEMAND: Record<string, number> = {
  artisan: 0.95, plombier: 0.95, électricien: 0.90, restaurant: 0.90,
  hôtel: 0.88, médecin: 0.85, médical: 0.85, dentiste: 0.82,
  kinésithérapeute: 0.80, garage: 0.85, concessionnaire: 0.80,
  immobilier: 0.78, "agence immo": 0.78, avocat: 0.80, comptable: 0.75,
  notaire: 0.75, école: 0.70, formation: 0.68, boulangerie: 0.72,
  coiffeur: 0.65, beauté: 0.65, photographe: 0.60, association: 0.45,
  "agence web": 0.05, digital: 0.05, marketing: 0.10,
};

const SIZE_WEIGHT: Record<string, number> = { TPE: 0.60, PME: 1.00, ETI: 0.80 };

const WEIGHTS = {
  pagespeed: 0.30, load_time: 0.15, icp_fit: 0.25,
  sector: 0.15, size: 0.10, engagement: 0.05,
};

const GRADE_THRESHOLDS: [number, string][] = [
  [85, "S"], [70, "A"], [50, "B"], [30, "C"], [0, "D"],
];

const ACTIONS: Record<string, string> = {
  S: "Appel téléphonique immédiat — proposition commerciale",
  A: "Email personnalisé Tier A — Agent 2.1",
  B: "Email de masse secteur — Agent 2.4",
  C: "Nurturing séquence 3 emails — Division 2",
  D: "Exclure du pipeline courant",
};

function sectorDemand(sector: string): number {
  const s = sector.toLowerCase();
  for (const [key, val] of Object.entries(SECTOR_DEMAND)) {
    if (s.includes(key)) return val;
  }
  return 0.50;
}

function calcGrade(score: number): string {
  for (const [threshold, grade] of GRADE_THRESHOLDS) {
    if (score >= threshold) return grade;
  }
  return "D";
}

function scoreLead(
  company_id: string,
  pagespeed_score: number,
  load_time_ms: number,
  icp_fit: number,
  sector: string,
  company_size: string,
  open_rate: number,
  reply_signal: number,
) {
  const speedFeat = Math.max(0, Math.min(1, (100 - pagespeed_score) / 100));
  const ltFeat = Math.max(0, Math.min(1, load_time_ms / 8000));
  const icpFeat = Math.max(0, Math.min(1, icp_fit));
  const secFeat = sectorDemand(sector);
  const sizeFeat = SIZE_WEIGHT[company_size.toUpperCase()] ?? 0.70;
  const engFeat = Math.min(1, open_rate * 0.3 + reply_signal * 0.7);

  const raw = speedFeat * WEIGHTS.pagespeed + ltFeat * WEIGHTS.load_time +
    icpFeat * WEIGHTS.icp_fit + secFeat * WEIGHTS.sector +
    sizeFeat * WEIGHTS.size + engFeat * WEIGHTS.engagement;

  const action_score = Math.round(raw * 10000) / 100;
  const grade = calcGrade(action_score);
  return {
    company_id,
    action_score,
    grade,
    feature_contributions: {
      pagespeed: parseFloat((speedFeat * WEIGHTS.pagespeed).toFixed(4)),
      load_time: parseFloat((ltFeat * WEIGHTS.load_time).toFixed(4)),
      icp_fit: parseFloat((icpFeat * WEIGHTS.icp_fit).toFixed(4)),
      sector: parseFloat((secFeat * WEIGHTS.sector).toFixed(4)),
      company_size: parseFloat((sizeFeat * WEIGHTS.size).toFixed(4)),
      engagement: parseFloat((engFeat * WEIGHTS.engagement).toFixed(4)),
    },
    recommended_action: ACTIONS[grade],
  };
}

// ── Raw leads ─────────────────────────────────────────────────────────────────

const RAW_LEADS: {
  company_id: string; company_name: string; sector: string; city: string;
  pagespeed_score: number; load_time_ms: number; icp_fit: number;
  company_size: string; open_rate: number; reply_signal: number;
}[] = [
  { company_id: "l001", company_name: "Plomberie Dupont", sector: "plombier", city: "Lyon", pagespeed_score: 22, load_time_ms: 6800, icp_fit: 0.92, company_size: "TPE", open_rate: 0.0, reply_signal: 0.0 },
  { company_id: "l002", company_name: "Restaurant Le Vieux Moulin", sector: "restaurant", city: "Paris", pagespeed_score: 31, load_time_ms: 5200, icp_fit: 0.90, company_size: "PME", open_rate: 0.6, reply_signal: 0.0 },
  { company_id: "l003", company_name: "Électricité Moreau SARL", sector: "électricien", city: "Bordeaux", pagespeed_score: 18, load_time_ms: 7400, icp_fit: 0.88, company_size: "PME", open_rate: 0.0, reply_signal: 1.0 },
  { company_id: "l004", company_name: "Hôtel des Alpes", sector: "hôtel", city: "Grenoble", pagespeed_score: 35, load_time_ms: 4900, icp_fit: 0.87, company_size: "PME", open_rate: 0.8, reply_signal: 0.0 },
  { company_id: "l005", company_name: "Cabinet Dr. Martin", sector: "médecin", city: "Toulouse", pagespeed_score: 28, load_time_ms: 6100, icp_fit: 0.85, company_size: "TPE", open_rate: 0.0, reply_signal: 0.0 },
  { company_id: "l006", company_name: "Auto Garage Lefort", sector: "garage", city: "Nantes", pagespeed_score: 42, load_time_ms: 4200, icp_fit: 0.80, company_size: "TPE", open_rate: 0.5, reply_signal: 0.0 },
  { company_id: "l007", company_name: "Maçonnerie Bernard", sector: "artisan", city: "Marseille", pagespeed_score: 55, load_time_ms: 3100, icp_fit: 0.75, company_size: "TPE", open_rate: 0.0, reply_signal: 0.0 },
  { company_id: "l008", company_name: "Coiffeur Sylvie", sector: "coiffeur", city: "Lille", pagespeed_score: 48, load_time_ms: 3800, icp_fit: 0.70, company_size: "TPE", open_rate: 0.4, reply_signal: 0.0 },
  { company_id: "l009", company_name: "Immobilier Blanche Fontaine", sector: "immobilier", city: "Nice", pagespeed_score: 60, load_time_ms: 2800, icp_fit: 0.72, company_size: "PME", open_rate: 0.3, reply_signal: 0.0 },
  { company_id: "l010", company_name: "Notaire Chartier & Associés", sector: "notaire", city: "Strasbourg", pagespeed_score: 65, load_time_ms: 2400, icp_fit: 0.68, company_size: "PME", open_rate: 0.0, reply_signal: 0.0 },
  { company_id: "l011", company_name: "Boulangerie Legrand", sector: "boulangerie", city: "Rennes", pagespeed_score: 70, load_time_ms: 1900, icp_fit: 0.60, company_size: "TPE", open_rate: 0.2, reply_signal: 0.0 },
  { company_id: "l012", company_name: "Photographe Artstudio", sector: "photographe", city: "Montpellier", pagespeed_score: 72, load_time_ms: 2100, icp_fit: 0.58, company_size: "TPE", open_rate: 0.1, reply_signal: 0.0 },
  { company_id: "l013", company_name: "Association Entraide 34", sector: "association", city: "Toulon", pagespeed_score: 68, load_time_ms: 2300, icp_fit: 0.42, company_size: "TPE", open_rate: 0.0, reply_signal: 0.0 },
  { company_id: "l014", company_name: "Agence WebPulse", sector: "agence web", city: "Paris", pagespeed_score: 85, load_time_ms: 900, icp_fit: 0.12, company_size: "PME", open_rate: 0.0, reply_signal: 0.0 },
  { company_id: "l015", company_name: "SaaS StartCorp", sector: "digital", city: "Paris", pagespeed_score: 88, load_time_ms: 800, icp_fit: 0.08, company_size: "ETI", open_rate: 0.0, reply_signal: 0.0 },
];

// Pre-compute scores
const SCORED_LEADS = RAW_LEADS
  .map((l) => ({
    ...scoreLead(l.company_id, l.pagespeed_score, l.load_time_ms, l.icp_fit, l.sector, l.company_size, l.open_rate, l.reply_signal),
    company_name: l.company_name,
    sector: l.sector,
    city: l.city,
    pagespeed_score: l.pagespeed_score,
    load_time_ms: l.load_time_ms,
    icp_fit: l.icp_fit,
    company_size: l.company_size,
    open_rate: l.open_rate,
    reply_signal: l.reply_signal,
  }))
  .sort((a, b) => b.action_score - a.action_score);

function buildSummary() {
  const grades = { S: 0, A: 0, B: 0, C: 0, D: 0 };
  let totalScore = 0;
  const sectors: Record<string, number[]> = {};
  for (const l of SCORED_LEADS) {
    grades[l.grade as keyof typeof grades]++;
    totalScore += l.action_score;
    (sectors[l.sector] ??= []).push(l.action_score);
  }
  const n = SCORED_LEADS.length || 1;
  return {
    total: SCORED_LEADS.length,
    grade_S: grades.S, grade_A: grades.A, grade_B: grades.B,
    grade_C: grades.C, grade_D: grades.D,
    avg_score: Math.round((totalScore / n) * 10) / 10,
    sector_breakdown: Object.fromEntries(
      Object.entries(sectors).map(([s, scores]) => [
        s,
        { count: scores.length, avg_score: Math.round((scores.reduce((a, b) => a + b, 0) / scores.length) * 10) / 10 },
      ])
    ),
    weights: WEIGHTS,
  };
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const grade = searchParams.get("grade");
  const limit = searchParams.get("limit");

  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/leads/weights`, { cache: "no-store" });
      if (res.ok) {
        const weightData = await res.json();
        return sealResponse(NextResponse.json({ leads: SCORED_LEADS, summary: buildSummary(), ...weightData }));
      }
    } catch { /* fall through */ }
  }

  let leads = SCORED_LEADS;
  if (grade) leads = leads.filter((l) => l.grade === grade.toUpperCase());
  if (limit) leads = leads.slice(0, parseInt(limit));

  return sealResponse(NextResponse.json({ leads, summary: buildSummary() }));
}

export async function POST(request: Request) {
  const body = await request.json();
  const { company_id, pagespeed_score, load_time_ms, icp_fit, sector,
    company_size = "PME", open_rate = 0.0, reply_signal = 0.0 } = body;
  if (!company_id) return sealResponse(NextResponse.json({ error: "company_id required" }, { status: 400 }));
  const result = scoreLead(company_id, pagespeed_score ?? 50, load_time_ms ?? 3000,
    icp_fit ?? 0.5, sector ?? "artisan", company_size, open_rate, reply_signal);
  return sealResponse(NextResponse.json(result));
}
