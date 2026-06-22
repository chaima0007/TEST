import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sectors] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_SECTORS = {
  source: "mock",
  total_addressable_market: 2927000,
  sectors: [
    { name: "Artisans & Bâtiment",              market_size_fr: 620000,  avg_pagespeed: 28, competition_density: 0.15, avg_revenue_impact_eur: 32000, outreach_roi_multiplier: 2.8, icp_priority: "S", recommended_volume: 170, tags: ["plombier","électricien","maçon","menuisier","couvreur"] },
    { name: "Restauration & Hôtellerie",         market_size_fr: 185000,  avg_pagespeed: 32, competition_density: 0.25, avg_revenue_impact_eur: 58000, outreach_roi_multiplier: 2.6, icp_priority: "S", recommended_volume: 139, tags: ["restaurant","hôtel","brasserie","traiteur"] },
    { name: "Médical & Cabinets de Soin",        market_size_fr: 280000,  avg_pagespeed: 35, competition_density: 0.20, avg_revenue_impact_eur: 45000, outreach_roi_multiplier: 2.4, icp_priority: "A", recommended_volume: 168, tags: ["médecin","dentiste","kiné","ophtalmo"] },
    { name: "Services Juridiques & Comptabilité",market_size_fr: 95000,   avg_pagespeed: 40, competition_density: 0.22, avg_revenue_impact_eur: 28000, outreach_roi_multiplier: 2.2, icp_priority: "A", recommended_volume: 148, tags: ["avocat","notaire","comptable"] },
    { name: "Garages & Concessionnaires",        market_size_fr: 42000,   avg_pagespeed: 38, competition_density: 0.30, avg_revenue_impact_eur: 22000, outreach_roi_multiplier: 2.1, icp_priority: "A", recommended_volume: 147, tags: ["garage","carrosserie","concessionnaire"] },
    { name: "Agences Immobilières",              market_size_fr: 30000,   avg_pagespeed: 42, competition_density: 0.40, avg_revenue_impact_eur: 35000, outreach_roi_multiplier: 1.9, icp_priority: "B", recommended_volume: 90,  tags: ["agence immo","immobilier"] },
    { name: "Boutiques & Beauté",                market_size_fr: 120000,  avg_pagespeed: 36, competition_density: 0.28, avg_revenue_impact_eur: 14000, outreach_roi_multiplier: 1.8, icp_priority: "B", recommended_volume: 172, tags: ["coiffeur","esthéticienne","boutique"] },
    { name: "Écoles & Organismes de Formation",  market_size_fr: 55000,   avg_pagespeed: 44, competition_density: 0.35, avg_revenue_impact_eur: 18000, outreach_roi_multiplier: 1.7, icp_priority: "B", recommended_volume: 143, tags: ["école","formation","auto-école"] },
    { name: "Associations & Loisirs",            market_size_fr: 1500000, avg_pagespeed: 29, competition_density: 0.08, avg_revenue_impact_eur: 5000,  outreach_roi_multiplier: 1.2, icp_priority: "C", recommended_volume: 200, tags: ["association","club","sport"] },
  ],
  weekly_outreach_plan: {
    "Artisans & Bâtiment": 170,
    "Restauration & Hôtellerie": 139,
    "Médical & Cabinets de Soin": 168,
    "Services Juridiques & Comptabilité": 148,
    "Garages & Concessionnaires": 147,
    "Agences Immobilières": 90,
    "Boutiques & Beauté": 172,
    "Écoles & Organismes de Formation": 143,
    "Associations & Loisirs": 200,
  },
};

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/sectors/report`, {
        next: { revalidate: 300 },
      });
      if (res.ok) {
        return sealResponse(NextResponse.json({ source: "live", ...(await res.json()) }));
      }
    } catch {
      // fall through to mock
    }
  }
  return sealResponse(NextResponse.json(MOCK_SECTORS));
}
