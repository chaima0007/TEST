import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

type AuthorityLevel = "unknown" | "influencer" | "manager" | "director" | "owner";
type Timeline = "unknown" | "no_timeline" | "next_year" | "next_quarter" | "this_quarter" | "immediate";
type QTier = "hot" | "warm" | "cool" | "cold";

interface BANT {
  budget_eur: number;
  budget_confirmed: boolean;
  authority_level: AuthorityLevel;
  need_severity: number;
  need_articulated: boolean;
  timeline: Timeline;
  budget_pts: number;
  authority_pts: number;
  need_pts: number;
  timeline_pts: number;
  total: number;
  tier: QTier;
}

interface QualRecord {
  record_id: string;
  prospect_id: string;
  company_name: string;
  sector: string;
  contact_name: string;
  contact_role: string;
  notes: string;
  qualified_at: string;
  last_updated: string;
  bant: BANT;
}

interface DimAvgs { budget: number; authority: number; need: number; timeline: number; }

interface Summary {
  total: number;
  tier_hot: number;
  tier_warm: number;
  tier_cool: number;
  tier_cold: number;
  avg_score: number;
  weakest_bant: string;
  dimension_avgs: DimAvgs;
}

interface Data {
  source: string;
  records: QualRecord[];
  summary: Summary;
}

function mkBant(
  budget_eur: number, budget_confirmed: boolean,
  authority_level: AuthorityLevel,
  need_severity: number, need_articulated: boolean,
  timeline: Timeline,
): BANT {
  const AUTH: Record<AuthorityLevel, number> = { unknown: 5, influencer: 10, manager: 15, director: 20, owner: 25 };
  const TL:   Record<Timeline, number>      = { unknown: 5, no_timeline: 5, next_year: 8, next_quarter: 15, this_quarter: 20, immediate: 25 };
  const budgetRaw = budget_eur >= 1200 ? 25 : budget_eur >= 960 ? 20 : budget_eur >= 600 ? 16 : budget_eur >= 360 ? 10 : budget_eur > 0 ? 5 : 0;
  const budget_pts = budget_confirmed ? budgetRaw : Math.max(2, Math.floor(budgetRaw / 2));
  const authority_pts = AUTH[authority_level];
  const clamp = Math.max(1, Math.min(5, need_severity));
  const need_pts = Math.min(25, clamp * 4 + (need_articulated ? 5 : 0));
  const timeline_pts = TL[timeline];
  const total = budget_pts + authority_pts + need_pts + timeline_pts;
  const tier: QTier = total >= 75 ? "hot" : total >= 50 ? "warm" : total >= 25 ? "cool" : "cold";
  return { budget_eur, budget_confirmed, authority_level, need_severity, need_articulated, timeline,
           budget_pts, authority_pts, need_pts, timeline_pts, total, tier };
}

function buildMockData(): Data {
  const now = new Date().toISOString();
  const records: QualRecord[] = [
    { record_id: "qual_00001", prospect_id: "p001", company_name: "Plomberie Martin SARL", sector: "artisan",    contact_name: "Pierre Martin", contact_role: "Gérant",            notes: "Problème urgent avant saison hiver",         qualified_at: now, last_updated: now, bant: mkBant(600,  true,  "owner",      4, true,  "immediate")     },
    { record_id: "qual_00002", prospect_id: "p002", company_name: "Restaurant La Cigale",  sector: "restaurant", contact_name: "Sophie Blanc",  contact_role: "Directrice",         notes: "Budget confirmé, décision avant fin mars",   qualified_at: now, last_updated: now, bant: mkBant(960,  true,  "director",   5, true,  "this_quarter")  },
    { record_id: "qual_00003", prospect_id: "p003", company_name: "Cabinet Dr. Lefèvre",   sector: "médical",    contact_name: "Dr. Lefèvre",   contact_role: "Médecin associé",   notes: "Besoin confirmé, délai flexible",             qualified_at: now, last_updated: now, bant: mkBant(780,  true,  "owner",      4, true,  "next_quarter")  },
    { record_id: "qual_00004", prospect_id: "p004", company_name: "Garage Dupont",         sector: "garage",     contact_name: "Michel Dupont", contact_role: "Propriétaire",       notes: "Intéressé mais budget à valider",            qualified_at: now, last_updated: now, bant: mkBant(600,  false, "owner",      3, true,  "this_quarter")  },
    { record_id: "qual_00005", prospect_id: "p005", company_name: "Immo Prestige",         sector: "immobilier", contact_name: "Claire Morin",  contact_role: "Directrice Comm.",  notes: "Très motivée, budget validé par conseil",    qualified_at: now, last_updated: now, bant: mkBant(1200, true,  "director",   5, true,  "immediate")     },
    { record_id: "qual_00006", prospect_id: "p006", company_name: "Maître Rousseau",       sector: "juridique",  contact_name: "Me. Rousseau",  contact_role: "Avocat associé",    notes: "Doit valider avec associés",                 qualified_at: now, last_updated: now, bant: mkBant(1000, false, "influencer", 4, true,  "next_quarter")  },
    { record_id: "qual_00007", prospect_id: "p007", company_name: "Centre Formation Top",  sector: "formation",  contact_name: "Lucie Bernard", contact_role: "Responsable form.", notes: "Budget annuel non confirmé",                 qualified_at: now, last_updated: now, bant: mkBant(360,  false, "manager",    3, false, "next_year")     },
    { record_id: "qual_00008", prospect_id: "p008", company_name: "Salon Élite",           sector: "beauté",     contact_name: "Amélie Koch",   contact_role: "Gérante",           notes: "Décision rapide souhaitée",                  qualified_at: now, last_updated: now, bant: mkBant(360,  true,  "owner",      3, true,  "this_quarter")  },
    { record_id: "qual_00009", prospect_id: "p009", company_name: "Charpenterie Moreau",   sector: "artisan",    contact_name: "René Moreau",   contact_role: "Chef d'atelier",    notes: "Décision côté patron, pas encore contacté",  qualified_at: now, last_updated: now, bant: mkBant(0,    false, "unknown",    2, false, "unknown")       },
    { record_id: "qual_00010", prospect_id: "p011", company_name: "Notaire & Associés",    sector: "juridique",  contact_name: "Me. Fontaine",  contact_role: "Notaire principale", notes: "Budget voté en conseil, timeline précise",   qualified_at: now, last_updated: now, bant: mkBant(1080, true,  "director",   4, true,  "this_quarter")  },
    { record_id: "qual_00011", prospect_id: "p012", company_name: "Auto Mécanique Renault",sector: "garage",     contact_name: "Thomas Rey",    contact_role: "Responsable SAV",   notes: "Doit convaincre sa direction",               qualified_at: now, last_updated: now, bant: mkBant(600,  false, "influencer", 3, true,  "next_quarter")  },
    { record_id: "qual_00012", prospect_id: "p014", company_name: "Artisan Pro SARL",      sector: "artisan",    contact_name: "Jacques Petit", contact_role: "Gérant",            notes: "Toutes cases cochées",                       qualified_at: now, last_updated: now, bant: mkBant(540,  true,  "owner",      4, true,  "this_quarter")  },
  ];

  const total = records.length;
  const tierCounts = { hot: 0, warm: 0, cool: 0, cold: 0 };
  let totalScore = 0;
  const dimTotals = { budget: 0, authority: 0, need: 0, timeline: 0 };
  for (const r of records) {
    tierCounts[r.bant.tier]++;
    totalScore += r.bant.total;
    dimTotals.budget    += r.bant.budget_pts;
    dimTotals.authority += r.bant.authority_pts;
    dimTotals.need      += r.bant.need_pts;
    dimTotals.timeline  += r.bant.timeline_pts;
  }
  const avgScore = Math.round(totalScore / total * 10) / 10;
  const dimAvgs: DimAvgs = {
    budget:    Math.round(dimTotals.budget    / total * 10) / 10,
    authority: Math.round(dimTotals.authority / total * 10) / 10,
    need:      Math.round(dimTotals.need      / total * 10) / 10,
    timeline:  Math.round(dimTotals.timeline  / total * 10) / 10,
  };
  const weakest = (Object.entries(dimAvgs) as [string, number][]).sort((a, b) => a[1] - b[1])[0][0];

  const summary: Summary = {
    total,
    tier_hot:  tierCounts.hot,
    tier_warm: tierCounts.warm,
    tier_cool: tierCounts.cool,
    tier_cold: tierCounts.cold,
    avg_score: avgScore,
    weakest_bant: weakest,
    dimension_avgs: dimAvgs,
  };

  return { source: "mock", records, summary };
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const [listRes, sumRes] = await Promise.all([
        fetch(`${SWARM_API_URL}/qualification`, { next: { revalidate: 15 } }),
        fetch(`${SWARM_API_URL}/qualification/summary`, { next: { revalidate: 15 } }),
      ]);
      if (listRes.ok && sumRes.ok) {
        return NextResponse.json({
          source: "live",
          records: await listRes.json(),
          summary: await sumRes.json(),
        });
      }
    } catch { /* fall through */ }
  }
  return NextResponse.json(buildMockData());
}
