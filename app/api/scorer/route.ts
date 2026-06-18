import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

type ThreatLevel = "low" | "medium" | "high" | "critical";

interface CompetitorProfile {
  competitor_id: string;
  name: string;
  sector: string;
  website: string;
  price_index: number;
  seo_strength: number;
  tech_quality: number;
  review_score: number;
  market_share_pct: number;
}

interface DimensionScores {
  price_threat: number;
  seo: number;
  tech: number;
  review_normalized: number;
  market: number;
}

interface ScoredCompetitor {
  profile: CompetitorProfile;
  threat_score: number;
  threat_level: ThreatLevel;
  dimension_scores: DimensionScores;
  strengths: string[];
  vulnerabilities: string[];
  recommendations: string[];
}

const WEIGHTS = { price: 0.25, seo: 0.30, tech: 0.20, reviews: 0.15, market: 0.10 };

const RECOMMENDATIONS: Record<ThreatLevel, string[]> = {
  critical: [
    "Priorité absolue : différenciation immédiate",
    "Surveiller toute baisse de prix",
    "Contre-attaquer sur les avis clients",
  ],
  high: [
    "Analyser leur positionnement prix",
    "Accélérer les optimisations SEO",
    "Mettre en avant les garanties",
  ],
  medium: [
    "Maintenir la veille mensuelle",
    "Exploiter leurs vulnérabilités identifiées",
    "Renforcer la fidélisation clients",
  ],
  low: [
    "Veille trimestrielle suffisante",
    "Opportunité de conversion de leurs clients insatisfaits",
  ],
};

const MOCK_PROFILES: CompetitorProfile[] = [
  { competitor_id: "c001", name: "WebPro Solutions",      sector: "agence web",      website: "webpro.fr",        price_index: 35, seo_strength: 88, tech_quality: 82, review_score: 4.6, market_share_pct: 18 },
  { competitor_id: "c002", name: "DigitBoost Agency",     sector: "agence web",      website: "digitboost.fr",    price_index: 55, seo_strength: 72, tech_quality: 70, review_score: 4.1, market_share_pct: 12 },
  { competitor_id: "c003", name: "RankFast SEO",          sector: "seo",             website: "rankfast.fr",      price_index: 45, seo_strength: 95, tech_quality: 60, review_score: 4.3, market_share_pct: 22 },
  { competitor_id: "c004", name: "LocalBoost",            sector: "marketing local", website: "localboost.fr",    price_index: 70, seo_strength: 55, tech_quality: 50, review_score: 3.8, market_share_pct:  8 },
  { competitor_id: "c005", name: "PageSpeed Pro",         sector: "agence web",      website: "pagespeedpro.fr",  price_index: 40, seo_strength: 78, tech_quality: 91, review_score: 4.7, market_share_pct: 15 },
  { competitor_id: "c006", name: "ArtisanWeb",            sector: "agence web",      website: "artisanweb.fr",    price_index: 80, seo_strength: 42, tech_quality: 38, review_score: 3.2, market_share_pct:  5 },
  { competitor_id: "c007", name: "MédicoDigital",         sector: "santé",           website: "medicodigital.fr", price_index: 30, seo_strength: 68, tech_quality: 75, review_score: 4.4, market_share_pct: 20 },
  { competitor_id: "c008", name: "ImmoRank",              sector: "immobilier",      website: "immorank.fr",      price_index: 50, seo_strength: 80, tech_quality: 65, review_score: 3.9, market_share_pct: 14 },
  { competitor_id: "c009", name: "JuriWeb",               sector: "juridique",       website: "juriweb.fr",       price_index: 25, seo_strength: 85, tech_quality: 72, review_score: 4.5, market_share_pct: 25 },
  { competitor_id: "c010", name: "RestoMarketing",        sector: "restauration",    website: "restomarketing.fr",price_index: 65, seo_strength: 48, tech_quality: 45, review_score: 3.5, market_share_pct:  7 },
  { competitor_id: "c011", name: "PrestaPro",             sector: "agence web",      website: "prestapro.fr",     price_index: 20, seo_strength: 90, tech_quality: 88, review_score: 4.8, market_share_pct: 28 },
  { competitor_id: "c012", name: "SiteEco",               sector: "agence web",      website: "siteeco.fr",       price_index: 85, seo_strength: 30, tech_quality: 28, review_score: 2.9, market_share_pct:  3 },
];

function computeDimensions(p: CompetitorProfile): DimensionScores {
  return {
    price_threat: 100 - p.price_index,
    seo: p.seo_strength,
    tech: p.tech_quality,
    review_normalized: (p.review_score / 5) * 100,
    market: p.market_share_pct,
  };
}

function computeThreatScore(d: DimensionScores): number {
  const raw =
    d.price_threat * WEIGHTS.price +
    d.seo * WEIGHTS.seo +
    d.tech * WEIGHTS.tech +
    d.review_normalized * WEIGHTS.reviews +
    d.market * WEIGHTS.market;
  return Math.round(Math.max(0, Math.min(100, raw)) * 100) / 100;
}

function classifyThreat(score: number): ThreatLevel {
  if (score >= 75) return "critical";
  if (score >= 55) return "high";
  if (score >= 35) return "medium";
  return "low";
}

function computeStrengths(d: DimensionScores, rs: number): string[] {
  const s: string[] = [];
  if (d.price_threat > 70) s.push("Prix agressif — attire les clients sensibles au coût");
  if (d.seo > 70) s.push("SEO fort — bonne visibilité Google");
  if (d.tech > 70) s.push("Stack technique moderne — UX supérieure");
  if (d.review_normalized > 70) s.push(`Excellents avis clients (${rs.toFixed(1)}/5)`);
  if (d.market > 70) s.push("Part de marché élevée — forte notoriété");
  return s;
}

function computeVulnerabilities(d: DimensionScores, rs: number): string[] {
  const v: string[] = [];
  if (d.price_threat < 40) v.push("Prix élevés — cible segment premium uniquement");
  if (d.seo < 40) v.push("Faible SEO — peu visible sur Google");
  if (d.tech < 40) v.push("Site technique médiocre — opportunité de disruption");
  if (d.review_normalized < 40) v.push(`Avis clients faibles (${rs.toFixed(1)}/5) — insatisfaction`);
  if (d.market < 40) v.push("Part de marché faible — peu d'effet réseau");
  return v;
}

function scoreProfile(p: CompetitorProfile): ScoredCompetitor {
  const dims = computeDimensions(p);
  const threat_score = computeThreatScore(dims);
  const threat_level = classifyThreat(threat_score);
  return {
    profile: p,
    threat_score,
    threat_level,
    dimension_scores: dims,
    strengths: computeStrengths(dims, p.review_score),
    vulnerabilities: computeVulnerabilities(dims, p.review_score),
    recommendations: RECOMMENDATIONS[threat_level],
  };
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/scorer`, { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch { /* fall through */ }
  }

  const scored = MOCK_PROFILES.map(scoreProfile).sort((a, b) => b.threat_score - a.threat_score);

  const levelCounts = { critical: 0, high: 0, medium: 0, low: 0 };
  for (const s of scored) levelCounts[s.threat_level]++;

  const avgThreat = scored.reduce((sum, s) => sum + s.threat_score, 0) / scored.length;

  const sectorMap: Record<string, { count: number; total: number; critical: number }> = {};
  for (const s of scored) {
    const sec = s.profile.sector;
    if (!sectorMap[sec]) sectorMap[sec] = { count: 0, total: 0, critical: 0 };
    sectorMap[sec].count++;
    sectorMap[sec].total += s.threat_score;
    if (s.threat_level === "critical") sectorMap[sec].critical++;
  }
  const sector_summary = Object.entries(sectorMap)
    .map(([sector, d]) => ({
      sector,
      count: d.count,
      avg_threat: Math.round((d.total / d.count) * 100) / 100,
      critical_count: d.critical,
    }))
    .sort((a, b) => b.avg_threat - a.avg_threat);

  return NextResponse.json({
    competitors: scored,
    summary: {
      total: scored.length,
      avg_threat_score: Math.round(avgThreat * 100) / 100,
      threat_level_distribution: levelCounts,
      top_threat_name: scored[0]?.profile.name ?? null,
      top_threat_score: scored[0]?.threat_score ?? 0,
    },
    sector_summary,
  });
}
