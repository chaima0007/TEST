import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const SECTORS = ["artisan", "restaurant", "médical", "garage", "immobilier", "juridique", "formation", "beauté", "association"];
const PACKAGES = ["starter", "standard", "premium", "enterprise"] as const;
const COMPANY_NAMES = [
  "Artisan Pro SARL", "Boulangerie Martin", "Cabinet Dr. Lefèvre", "Garage Dupont",
  "Immo Prestige", "Maître Rousseau", "Centre Formation Top", "Salon Élite",
  "Association Solidarité", "Charpenterie Moreau", "Restaurant La Cigale",
  "Plomberie Express", "Auto Mécanique Renault", "Notaire & Associés", "BTP Expert SARL",
];

const SECTOR_MULTIPLIERS: Record<string, number> = {
  médical: 1.30, juridique: 1.25, immobilier: 1.20, formation: 1.15,
  restaurant: 1.10, artisan: 1.05, garage: 1.05, beauté: 1.00, association: 0.85,
};

const BASE_PRICES: Record<string, number> = { starter: 99, standard: 249, premium: 449, enterprise: 799 };

type Pkg = typeof PACKAGES[number];

function rnd(min: number, max: number) { return Math.floor(Math.random() * (max - min + 1)) + min; }
function pick<T>(arr: readonly T[]): T { return arr[Math.floor(Math.random() * arr.length)]; }

function makeSeverity(pagespeed: number, loadMs: number, mobile: boolean, issues: number) {
  const ps  = Math.max(0, (100 - pagespeed) / 100) * 0.40;
  const lt  = Math.min(1, Math.max(0, (loadMs - 1000) / 9000)) * 0.30;
  const mob = mobile ? 0 : 0.20;
  const iss = Math.min(1, issues / 10) * 0.10;
  return ps + lt + mob + iss;
}

function recommendPackage(severity: number): Pkg {
  if (severity >= 0.75) return "enterprise";
  if (severity >= 0.55) return "premium";
  if (severity >= 0.30) return "standard";
  return "starter";
}

function makeQuote(index: number) {
  const sector = pick(SECTORS);
  const pagespeed = rnd(8, 55);
  const loadMs    = rnd(2500, 9000);
  const mobile    = Math.random() < 0.4;
  const issues    = rnd(0, 8);
  const severity  = makeSeverity(pagespeed, loadMs, mobile, issues);
  const pkgCode   = recommendPackage(severity) as Pkg;
  const mult      = SECTOR_MULTIPLIERS[sector] ?? 1.0;
  const basePrice = BASE_PRICES[pkgCode] * mult;
  const discount  = Math.random() < 0.2 ? Math.random() * 0.15 : 0;
  const urgency   = Math.random() < 0.15;
  const urgencyBonus = urgency ? basePrice * 0.10 : 0;
  const subtotal  = Math.round(basePrice * 100) / 100;
  const discountAmt = Math.round(subtotal * discount * 100) / 100;
  const totalHT   = Math.round((subtotal - discountAmt + urgencyBonus) * 100) / 100;
  const tvAmt     = Math.round(totalHT * 0.20 * 100) / 100;
  const totalTTC  = Math.round((totalHT + tvAmt) * 100) / 100;

  return {
    prospect_id: `p${String(index).padStart(3, "0")}`,
    company_name: `${pick(COMPANY_NAMES)} ${index}`,
    sector,
    pagespeed_score: pagespeed,
    load_time_ms: loadMs,
    mobile_responsive: mobile,
    issue_count: issues,
    severity: Math.round(severity * 1000) / 1000,
    package: {
      code: pkgCode,
      name: pkgCode.charAt(0).toUpperCase() + pkgCode.slice(1),
      base_price_eur: BASE_PRICES[pkgCode],
    },
    sector_multiplier: mult,
    discount_pct: Math.round(discount * 1000) / 10,
    urgency_bonus_eur: Math.round(urgencyBonus * 100) / 100,
    subtotal_eur: subtotal,
    total_ht_eur: totalHT,
    tva_eur: tvAmt,
    total_ttc_eur: totalTTC,
  };
}

function buildMockData() {
  const quotes = Array.from({ length: 18 }, (_, i) => makeQuote(i + 1));
  const byPackage = quotes.reduce((acc, q) => {
    acc[q.package.code] = (acc[q.package.code] ?? 0) + 1;
    return acc;
  }, {} as Record<string, number>);
  const totalPipeline = quotes.reduce((s, q) => s + q.total_ttc_eur, 0);
  const avgQuote = totalPipeline / quotes.length;

  return {
    source: "mock",
    summary: {
      total_quotes: quotes.length,
      total_pipeline_eur: Math.round(totalPipeline * 100) / 100,
      average_quote_eur: Math.round(avgQuote * 100) / 100,
      by_package: byPackage,
    },
    quotes,
  };
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/pricing/summary`, { next: { revalidate: 15 } });
      if (res.ok) return NextResponse.json({ source: "live", ...(await res.json()) });
    } catch { /* fall through */ }
  }
  return NextResponse.json(buildMockData());
}
