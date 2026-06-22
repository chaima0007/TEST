import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[funnel] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

type FunnelStage = "lead" | "contacted" | "opened" | "replied" | "demo" | "quoted" | "negotiating" | "won" | "lost";

interface ProspectRecord {
  prospect_id: string;
  company_name: string;
  sector: string;
  current_stage: FunnelStage;
  quote_value: number;
  is_active: boolean;
  is_won: boolean;
  days_in_funnel: number;
  stages_reached: FunnelStage[];
}

interface TransitionStats {
  from_stage: FunnelStage;
  to_stage: FunnelStage;
  prospects_entered: number;
  prospects_converted: number;
  conversion_rate_pct: number;
  drop_off_rate_pct: number;
}

function daysAgo(d: number) {
  const dt = new Date();
  dt.setDate(dt.getDate() - d);
  return dt.toISOString();
}

function buildMockData() {
  const prospects: ProspectRecord[] = [
    { prospect_id: "p001", company_name: "Plomberie Martin SARL", sector: "artisan",       current_stage: "won",          quote_value: 598.80,  is_active: false, is_won: true,  days_in_funnel: 18, stages_reached: ["lead","contacted","opened","replied","demo","quoted","negotiating","won"] },
    { prospect_id: "p002", company_name: "Restaurant La Cigale",  sector: "restaurant",     current_stage: "negotiating",  quote_value: 958.80,  is_active: true,  is_won: false, days_in_funnel: 12, stages_reached: ["lead","contacted","opened","replied","demo","quoted","negotiating"] },
    { prospect_id: "p003", company_name: "Cabinet Dr. Lefèvre",   sector: "médical",        current_stage: "quoted",       quote_value: 778.80,  is_active: true,  is_won: false, days_in_funnel: 8,  stages_reached: ["lead","contacted","opened","replied","quoted"] },
    { prospect_id: "p004", company_name: "Garage Dupont",         sector: "garage",         current_stage: "replied",      quote_value: 0,       is_active: true,  is_won: false, days_in_funnel: 5,  stages_reached: ["lead","contacted","opened","replied"] },
    { prospect_id: "p005", company_name: "Immo Prestige",         sector: "immobilier",     current_stage: "won",          quote_value: 958.80,  is_active: false, is_won: true,  days_in_funnel: 22, stages_reached: ["lead","contacted","opened","replied","demo","quoted","negotiating","won"] },
    { prospect_id: "p006", company_name: "Maître Rousseau",       sector: "juridique",      current_stage: "demo",         quote_value: 0,       is_active: true,  is_won: false, days_in_funnel: 7,  stages_reached: ["lead","contacted","opened","replied","demo"] },
    { prospect_id: "p007", company_name: "Centre Formation Top",  sector: "formation",      current_stage: "opened",       quote_value: 0,       is_active: true,  is_won: false, days_in_funnel: 3,  stages_reached: ["lead","contacted","opened"] },
    { prospect_id: "p008", company_name: "Salon Élite",           sector: "beauté",         current_stage: "won",          quote_value: 358.80,  is_active: false, is_won: true,  days_in_funnel: 14, stages_reached: ["lead","contacted","opened","replied","quoted","won"] },
    { prospect_id: "p009", company_name: "Charpenterie Moreau",   sector: "artisan",        current_stage: "contacted",    quote_value: 0,       is_active: true,  is_won: false, days_in_funnel: 2,  stages_reached: ["lead","contacted"] },
    { prospect_id: "p010", company_name: "BTP Expert SARL",       sector: "artisan",        current_stage: "lost",         quote_value: 0,       is_active: false, is_won: false, days_in_funnel: 9,  stages_reached: ["lead","contacted","opened","lost"] },
    { prospect_id: "p011", company_name: "Notaire & Associés",    sector: "juridique",      current_stage: "quoted",       quote_value: 1078.80, is_active: true,  is_won: false, days_in_funnel: 10, stages_reached: ["lead","contacted","opened","replied","demo","quoted"] },
    { prospect_id: "p012", company_name: "Auto Mécanique Renault",sector: "garage",         current_stage: "lead",         quote_value: 0,       is_active: true,  is_won: false, days_in_funnel: 1,  stages_reached: ["lead"] },
    { prospect_id: "p013", company_name: "Boulangerie Martin",    sector: "restaurant",     current_stage: "lost",         quote_value: 0,       is_active: false, is_won: false, days_in_funnel: 6,  stages_reached: ["lead","contacted","lost"] },
    { prospect_id: "p014", company_name: "Artisan Pro SARL",      sector: "artisan",        current_stage: "negotiating",  quote_value: 538.80,  is_active: true,  is_won: false, days_in_funnel: 15, stages_reached: ["lead","contacted","opened","replied","demo","quoted","negotiating"] },
    { prospect_id: "p015", company_name: "Association Solidarité",sector: "association",    current_stage: "opened",       quote_value: 0,       is_active: true,  is_won: false, days_in_funnel: 4,  stages_reached: ["lead","contacted","opened"] },
  ];

  const STAGES: FunnelStage[] = ["lead","contacted","opened","replied","demo","quoted","negotiating","won"];
  const stageCounts: Record<string, number> = {};
  for (const p of prospects) stageCounts[p.current_stage] = (stageCounts[p.current_stage] ?? 0) + 1;

  const report: TransitionStats[] = [];
  for (let i = 0; i < STAGES.length - 1; i++) {
    const from = STAGES[i];
    const to   = STAGES[i + 1];
    const entered   = prospects.filter(p => p.stages_reached.includes(from)).length;
    const converted = prospects.filter(p => p.stages_reached.includes(from) && p.stages_reached.includes(to)).length;
    const rate = entered ? Math.round(converted / entered * 1000) / 10 : 0;
    report.push({ from_stage: from, to_stage: to, prospects_entered: entered, prospects_converted: converted, conversion_rate_pct: rate, drop_off_rate_pct: Math.round((100 - rate) * 10) / 10 });
  }

  const won = prospects.filter(p => p.is_won);
  const active = prospects.filter(p => p.is_active);
  const lost = prospects.filter(p => !p.is_active && !p.is_won);
  const totalWon = won.reduce((s, p) => s + p.quote_value, 0);
  const pipeline = active.filter(p => p.quote_value > 0).reduce((s, p) => s + p.quote_value, 0);
  const avgDeal  = won.length ? totalWon / won.length : 0;
  const avgDays  = won.length ? won.reduce((s, p) => s + p.days_in_funnel, 0) / won.length : 0;
  const overall_cvr = Math.round(won.length / prospects.length * 1000) / 10;

  return {
    source: "mock",
    prospects,
    stage_report: report,
    summary: {
      total_prospects:    prospects.length,
      active:             active.length,
      won:                won.length,
      lost:               lost.length,
      overall_cvr_pct:    overall_cvr,
      total_pipeline_eur: Math.round(pipeline * 100) / 100,
      total_won_eur:      Math.round(totalWon * 100) / 100,
      avg_deal_size_eur:  Math.round(avgDeal * 100) / 100,
      avg_days_to_close:  Math.round(avgDays * 10) / 10,
      stage_counts:       stageCounts,
    },
  };
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const [sumRes, repRes] = await Promise.all([
        fetch(`${SWARM_API_URL}/funnel/summary`,    { next: { revalidate: 15 } }),
        fetch(`${SWARM_API_URL}/funnel/report`,     { next: { revalidate: 15 } }),
      ]);
      if (sumRes.ok && repRes.ok) {
        return sealResponse(NextResponse.json({
          source: "live",
          summary: await sumRes.json(),
          stage_report: await repRes.json(),
        }));
      }
    } catch { /* fall through */ }
  }
  return sealResponse(NextResponse.json(buildMockData()));
}
