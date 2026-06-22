import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[enricher] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

// ── Enrichment logic mirroring Python ProspectEnricher ────────────────────────

const SECTOR_ICP: Record<string, number> = {
  restaurant: 0.95, hôtel: 0.95, plombier: 0.90, électricien: 0.90,
  artisan: 0.88, médecin: 0.85, dentiste: 0.85, avocat: 0.82,
  comptable: 0.80, notaire: 0.80, architecte: 0.78, immobilier: 0.75,
  coiffeur: 0.72, auto: 0.70, garage: 0.70, fleuriste: 0.65, boulanger: 0.60,
  logiciel: 0.30, saas: 0.25, startup: 0.25, "agence web": 0.10,
};

const SIZE_SIGNALS: Record<string, string> = {
  sarl: "PME", sas: "PME", eurl: "TPE", "ei ": "TPE",
  "auto-entrepreneur": "TPE", "micro-entreprise": "TPE",
  "sa ": "ETI", groupe: "ETI", holding: "ETI",
};

function scoreIcp(sector: string): number {
  const s = sector.toLowerCase();
  for (const [key, val] of Object.entries(SECTOR_ICP)) {
    if (s.includes(key)) return val;
  }
  return 0.45;
}

function scoreUrgency(pagespeed: number): [number, string] {
  if (pagespeed <= 29) return [1.0, "critique"];
  if (pagespeed <= 49) return [0.85, "mauvais"];
  if (pagespeed <= 69) return [0.60, "moyen"];
  if (pagespeed <= 89) return [0.30, "acceptable"];
  return [0.05, "bon"];
}

function detectSize(name: string, website: string): string {
  const combined = (name + " " + website).toLowerCase();
  for (const [signal, size] of Object.entries(SIZE_SIGNALS)) {
    if (combined.includes(signal)) return size;
  }
  return "PME";
}

function estimateRevenueImpact(load_time_ms: number, size: string): number {
  const sizeBase: Record<string, number> = { TPE: 80_000, PME: 400_000, ETI: 2_000_000 };
  const base = (sizeBase[size] ?? 400_000) * 0.15;
  const extraSec = Math.max(0, (load_time_ms - 1000) / 1000);
  const lossRate = Math.min(0.7, extraSec * 0.07);
  return Math.round(base * lossRate / 100) * 100;
}

function computePriority(icp: number, urgency: number): number {
  return Math.max(0, Math.min(100, Math.round((icp * 0.55 + urgency * 0.45) * 100)));
}

function assignTier(score: number): string {
  if (score >= 70) return "A";
  if (score >= 45) return "B";
  return "C";
}

function enrich(fiche: {
  company_id: string; name: string; sector: string; website?: string;
  contact_email?: string; pagespeed_score: number; load_time_ms: number;
}) {
  const icp = scoreIcp(fiche.sector);
  const [urgency, urgency_label] = scoreUrgency(fiche.pagespeed_score);
  const company_size = detectSize(fiche.name, fiche.website ?? "");
  const priority_score = computePriority(icp, urgency);
  const tier = assignTier(priority_score);
  const estimated_revenue_impact_eur = estimateRevenueImpact(fiche.load_time_ms, company_size);

  const enrichment_notes: string[] = [];
  if (fiche.pagespeed_score < 30) enrichment_notes.push("PageSpeed critique — contact urgent recommandé");
  if (icp >= 0.85) enrichment_notes.push(`Secteur à forte valeur ICP (${fiche.sector})`);
  if (estimated_revenue_impact_eur > 10_000) enrichment_notes.push(`Impact revenu estimé : ${estimated_revenue_impact_eur.toLocaleString("fr-FR")}€/an`);
  if (priority_score >= 70) enrichment_notes.push("Priorité A — traitement immédiat");

  return {
    ...fiche,
    icp_fit: Math.round(icp * 1000) / 1000,
    urgency: Math.round(urgency * 1000) / 1000,
    company_size,
    priority_score,
    tier,
    sector_score: icp,
    urgency_label,
    estimated_revenue_impact_eur,
    enrichment_notes,
  };
}

// ── Mock raw prospects ─────────────────────────────────────────────────────────

const RAW_PROSPECTS = [
  { company_id: "e001", name: "Restaurant Le Vieux Port SARL", sector: "restaurant", website: "levieuxport.fr", contact_email: "contact@levieuxport.fr", pagespeed_score: 18, load_time_ms: 7200 },
  { company_id: "e002", name: "Plomberie Lefort SAS", sector: "plombier", website: "plomberie-lefort.fr", contact_email: "lefort@plomberie.fr", pagespeed_score: 25, load_time_ms: 6800 },
  { company_id: "e003", name: "Électricité Garnier EURL", sector: "électricien", website: "electricite-garnier.fr", contact_email: "garnier@elec.fr", pagespeed_score: 22, load_time_ms: 7400 },
  { company_id: "e004", name: "Hôtel des Cèdres", sector: "hôtel", website: "hotel-cedres.fr", contact_email: "info@hotelcedres.fr", pagespeed_score: 31, load_time_ms: 5900 },
  { company_id: "e005", name: "Cabinet Dr Fontaine", sector: "médecin", website: "dr-fontaine.fr", contact_email: "cabinet@drfontaine.fr", pagespeed_score: 27, load_time_ms: 6100 },
  { company_id: "e006", name: "Dentiste Rivière & Associés SAS", sector: "dentiste", website: "dentiste-riviere.fr", contact_email: "info@dentiste-riviere.fr", pagespeed_score: 35, load_time_ms: 5400 },
  { company_id: "e007", name: "Maître Dupuis Avocat", sector: "avocat", website: "dupuis-avocat.fr", contact_email: "contact@dupuis-avocat.fr", pagespeed_score: 42, load_time_ms: 4800 },
  { company_id: "e008", name: "Cabinet Comptable Martin & Fils", sector: "comptable", website: "martin-compta.fr", contact_email: "martin@compta.fr", pagespeed_score: 48, load_time_ms: 4200 },
  { company_id: "e009", name: "Garage Auto Bernard", sector: "garage", website: "garage-bernard.fr", contact_email: "bernard@garage.fr", pagespeed_score: 55, load_time_ms: 3600 },
  { company_id: "e010", name: "Agence Immobilier Blanche", sector: "immobilier", website: "immobilier-blanche.fr", contact_email: "contact@immo-blanche.fr", pagespeed_score: 58, load_time_ms: 3300 },
  { company_id: "e011", name: "Coiffure Élégance", sector: "coiffeur", website: "coiffure-elegance.fr", contact_email: "elegance@coiffure.fr", pagespeed_score: 63, load_time_ms: 2900 },
  { company_id: "e012", name: "Boulangerie Artisanale Dupont", sector: "boulanger", website: "boulangerie-dupont.fr", contact_email: "dupont@boulangerie.fr", pagespeed_score: 67, load_time_ms: 2700 },
  { company_id: "e013", name: "SaaS PulseMetrics", sector: "saas", website: "pulsemetrics.io", contact_email: "hello@pulsemetrics.io", pagespeed_score: 82, load_time_ms: 1200 },
  { company_id: "e014", name: "Agence WebPulse Groupe SA", sector: "agence web", website: "webpulse.fr", contact_email: "contact@webpulse.fr", pagespeed_score: 88, load_time_ms: 900 },
  { company_id: "e015", name: "Startup InnoTech Holding", sector: "startup", website: "innotech.io", contact_email: "hello@innotech.io", pagespeed_score: 79, load_time_ms: 1500 },
];

const ENRICHED = RAW_PROSPECTS
  .map(enrich)
  .sort((a, b) => b.priority_score - a.priority_score);

function buildSummary() {
  const tiers = { A: 0, B: 0, C: 0 };
  let totalScore = 0;
  let totalRevImpact = 0;
  const urgencyDist: Record<string, number> = {};
  const sectors: Record<string, number[]> = {};

  for (const p of ENRICHED) {
    tiers[p.tier as keyof typeof tiers]++;
    totalScore += p.priority_score;
    totalRevImpact += p.estimated_revenue_impact_eur;
    urgencyDist[p.urgency_label] = (urgencyDist[p.urgency_label] ?? 0) + 1;
    (sectors[p.sector] ??= []).push(p.priority_score);
  }
  const n = ENRICHED.length || 1;
  return {
    total: ENRICHED.length,
    tier_A: tiers.A, tier_B: tiers.B, tier_C: tiers.C,
    avg_priority: Math.round((totalScore / n) * 10) / 10,
    total_revenue_impact_eur: totalRevImpact,
    urgency_distribution: urgencyDist,
    sector_breakdown: Object.fromEntries(
      Object.entries(sectors).map(([s, scores]) => [
        s,
        { count: scores.length, avg_priority: Math.round((scores.reduce((a, b) => a + b, 0) / scores.length) * 10) / 10 },
      ])
    ),
  };
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const tier = searchParams.get("tier");
  const limit = searchParams.get("limit");

  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/enrich/batch`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prospects: RAW_PROSPECTS }),
        cache: "no-store",
      });
      if (res.ok) {
        const data = await res.json();
        return sealResponse(NextResponse.json({ prospects: data.prospects, summary: buildSummary(), source: "live" }));
      }
    } catch { /* fall through */ }
  }

  let prospects = ENRICHED;
  if (tier) prospects = prospects.filter((p) => p.tier === tier.toUpperCase());
  if (limit) prospects = prospects.slice(0, parseInt(limit));

  return sealResponse(NextResponse.json({ prospects, summary: buildSummary(), source: "mock" }));
}

export async function POST(request: Request) {
  const body = await request.json();
  if (!body.company_id) return sealResponse(NextResponse.json({ error: "company_id required" }, { status: 400 }));
  return sealResponse(NextResponse.json(enrich(body)));
}
