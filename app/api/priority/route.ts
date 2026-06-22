import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[priority] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

type LeadPriority = "hot" | "warm" | "cold" | "dormant";

interface LeadSignals {
  lead_id: string;
  name: string;
  company: string;
  sector: string;
  days_since_last_contact: number;
  response_rate: number;
  deal_value_eur: number;
  days_in_pipeline: number;
  open_rate: number;
  meetings_completed: number;
  proposal_sent: boolean;
}

interface PrioritizedLead {
  signals: LeadSignals;
  priority_score: number;
  priority_tier: LeadPriority;
  score_breakdown: {
    recency: number;
    responsiveness: number;
    deal_value: number;
    engagement: number;
    activity: number;
    pipeline_health: number;
  };
  action_items: string[];
  risk_flags: string[];
}

const ACTION_ITEMS: Record<LeadPriority, string[]> = {
  hot:     ["Appeler dans les 24h", "Proposer une date de signature", "Préparer les documents contractuels"],
  warm:    ["Relancer par email cette semaine", "Planifier une démo ou un appel de qualification", "Envoyer un cas client similaire"],
  cold:    ["Séquence de réactivation automatique", "Requalifier les besoins", "Ajuster le positionnement tarifaire si nécessaire"],
  dormant: ["Email breakup — fermer ou archiver", "Vérifier si le contact a changé de poste", "Remettre en liste froide pour 90 jours"],
};

const MOCK_LEADS: LeadSignals[] = [
  { lead_id: "p001", name: "Marc Dupont",       company: "Cabinet Dupont",       sector: "avocat",       days_since_last_contact: 1,  response_rate: 0.90, deal_value_eur: 1290, days_in_pipeline: 8,  open_rate: 0.80, meetings_completed: 4, proposal_sent: true  },
  { lead_id: "p002", name: "Lucie Martin",      company: "Plomberie Martin",     sector: "artisan",      days_since_last_contact: 3,  response_rate: 0.65, deal_value_eur: 380,  days_in_pipeline: 12, open_rate: 0.60, meetings_completed: 2, proposal_sent: false },
  { lead_id: "p003", name: "Thomas Léger",      company: "Cabinet Léger & Ass.", sector: "comptable",    days_since_last_contact: 6,  response_rate: 0.55, deal_value_eur: 960,  days_in_pipeline: 18, open_rate: 0.50, meetings_completed: 3, proposal_sent: true  },
  { lead_id: "p004", name: "Sophie Moreau",     company: "Dr. Moreau",           sector: "médecin",      days_since_last_contact: 15, response_rate: 0.30, deal_value_eur: 540,  days_in_pipeline: 28, open_rate: 0.25, meetings_completed: 1, proposal_sent: false },
  { lead_id: "p005", name: "Antoine Zinc",      company: "Brasserie Le Zinc",    sector: "restaurant",   days_since_last_contact: 20, response_rate: 0.15, deal_value_eur: 420,  days_in_pipeline: 42, open_rate: 0.12, meetings_completed: 0, proposal_sent: false },
  { lead_id: "p006", name: "Claire Blanc",      company: "Étude Notariale Blanc",sector: "notaire",      days_since_last_contact: 2,  response_rate: 0.80, deal_value_eur: 1140, days_in_pipeline: 6,  open_rate: 0.72, meetings_completed: 3, proposal_sent: true  },
  { lead_id: "p007", name: "Romain Horizon",    company: "Agence Horizon",       sector: "immobilier",   days_since_last_contact: 9,  response_rate: 0.40, deal_value_eur: 720,  days_in_pipeline: 22, open_rate: 0.35, meetings_completed: 1, proposal_sent: false },
  { lead_id: "p008", name: "Isabelle Sas",      company: "PME Solutions SAS",    sector: "pme",          days_since_last_contact: 1,  response_rate: 0.88, deal_value_eur: 890,  days_in_pipeline: 5,  open_rate: 0.78, meetings_completed: 5, proposal_sent: true  },
  { lead_id: "p009", name: "Éric Durand",       company: "Électricité Durand",   sector: "artisan",      days_since_last_contact: 30, response_rate: 0.05, deal_value_eur: 290,  days_in_pipeline: 60, open_rate: 0.04, meetings_completed: 0, proposal_sent: false },
  { lead_id: "p010", name: "Nathalie Vue",      company: "Hôtel Belle Vue",      sector: "hôtel",        days_since_last_contact: 7,  response_rate: 0.45, deal_value_eur: 680,  days_in_pipeline: 16, open_rate: 0.40, meetings_completed: 2, proposal_sent: false },
  { lead_id: "p011", name: "Pascal Fontaine",   company: "Dr. Fontaine Dentiste",sector: "dentiste",     days_since_last_contact: 10, response_rate: 0.35, deal_value_eur: 560,  days_in_pipeline: 25, open_rate: 0.30, meetings_completed: 1, proposal_sent: true  },
  { lead_id: "p012", name: "Véronique Élég.",   company: "Coiffure Élégance",    sector: "coiffeur",     days_since_last_contact: 25, response_rate: 0.08, deal_value_eur: 190,  days_in_pipeline: 50, open_rate: 0.07, meetings_completed: 0, proposal_sent: false },
];

function recencyScore(days: number): number {
  if (days <= 3) return 100;
  if (days <= 7) return 85;
  return Math.max(0, 85 - (days - 7) * 3);
}

function valueScore(eur: number): number { return Math.min(100, eur / 20); }
function activityScore(meetings: number): number { return Math.min(100, meetings * 20); }
function pipelineHealthScore(days: number, proposalSent: boolean): number {
  let base = proposalSent ? 100 : 70;
  if (days > 30) base = Math.max(0, base - (days - 30) * 2);
  return base;
}

function computeBreakdown(s: LeadSignals) {
  return {
    recency:         recencyScore(s.days_since_last_contact),
    responsiveness:  s.response_rate * 100,
    deal_value:      valueScore(s.deal_value_eur),
    engagement:      s.open_rate * 100,
    activity:        activityScore(s.meetings_completed),
    pipeline_health: pipelineHealthScore(s.days_in_pipeline, s.proposal_sent),
  };
}

function computeScore(b: ReturnType<typeof computeBreakdown>): number {
  const raw = b.recency * 0.20 + b.responsiveness * 0.25 + b.deal_value * 0.20 +
              b.engagement * 0.15 + b.activity * 0.10 + b.pipeline_health * 0.10;
  return Math.round(Math.max(0, Math.min(100, raw)) * 100) / 100;
}

function classifyTier(score: number): LeadPriority {
  if (score >= 70) return "hot";
  if (score >= 50) return "warm";
  if (score >= 30) return "cold";
  return "dormant";
}

function computeRiskFlags(s: LeadSignals): string[] {
  const flags: string[] = [];
  if (s.days_since_last_contact > 14) flags.push(`Pas de contact depuis ${s.days_since_last_contact} jours`);
  if (s.response_rate < 0.20) flags.push("Taux de réponse très faible (< 20%)");
  if (s.days_in_pipeline > 45) flags.push(`En pipeline depuis ${s.days_in_pipeline} jours — risque de stagnation`);
  if (!s.proposal_sent && s.days_in_pipeline > 20) flags.push("Aucun devis envoyé après 20 jours");
  if (s.open_rate < 0.15) flags.push("Faible taux d'ouverture des emails");
  return flags;
}

function prioritizeLead(s: LeadSignals): PrioritizedLead {
  const breakdown = computeBreakdown(s);
  const score = computeScore(breakdown);
  const tier = classifyTier(score);
  return {
    signals: s,
    priority_score: score,
    priority_tier: tier,
    score_breakdown: breakdown,
    action_items: ACTION_ITEMS[tier],
    risk_flags: computeRiskFlags(s),
  };
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/priority`, { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch { /* fall through */ }
  }

  const leads = MOCK_LEADS.map(prioritizeLead).sort((a, b) => b.priority_score - a.priority_score);

  const tierCounts = { hot: 0, warm: 0, cold: 0, dormant: 0 };
  let totalValue = 0;
  let atRisk = 0;
  for (const l of leads) {
    tierCounts[l.priority_tier]++;
    totalValue += l.signals.deal_value_eur;
    if (l.risk_flags.length > 0) atRisk++;
  }

  const avgScore = leads.reduce((s, l) => s + l.priority_score, 0) / leads.length;

  const sectorMap: Record<string, { count: number; total: number; hot: number; value: number }> = {};
  for (const l of leads) {
    const sec = l.signals.sector;
    if (!sectorMap[sec]) sectorMap[sec] = { count: 0, total: 0, hot: 0, value: 0 };
    sectorMap[sec].count++;
    sectorMap[sec].total += l.priority_score;
    if (l.priority_tier === "hot") sectorMap[sec].hot++;
    sectorMap[sec].value += l.signals.deal_value_eur;
  }
  const sector_stats = Object.entries(sectorMap).map(([sector, d]) => ({
    sector,
    count: d.count,
    avg_score: Math.round((d.total / d.count) * 100) / 100,
    hot_count: d.hot,
    total_value_eur: Math.round(d.value),
  })).sort((a, b) => b.avg_score - a.avg_score);

  return sealResponse(NextResponse.json({
    leads,
    summary: {
      total: leads.length,
      tier_counts: tierCounts,
      avg_score: Math.round(avgScore * 100) / 100,
      total_pipeline_value: Math.round(totalValue),
      at_risk_count: atRisk,
    },
    sector_stats,
  }));
}
