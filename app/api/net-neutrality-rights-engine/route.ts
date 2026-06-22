import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[net-neutrality-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[net-neutrality-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Net Neutrality Rights Engine Agent",
  domain: "net_neutrality_rights",
  total_entities: 8,
  avg_composite: 60.48,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Chine — Great Firewall, throttling massif & zero-rating étatique",
    "Russie — Loi Runet, blocages ciblés & DPI généralisé",
    "Iran — Internet national, étranglement des flux internationaux",
  ],
  critical_alerts: [
    "Chine: State-mandated ISP throttling & zero-rating for domestic platforms only",
    "Russie: Sovereign internet law enabling full traffic discrimination",
    "Iran: National intranet blocking international access & paid prioritization",
    "Inde: Zero-rating controversies & regional internet shutdowns",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_net_neutrality_rights_index: 6.05,
  entities: [
    {
      entity_id: "NNR-001",
      name: "Chine — Great Firewall, throttling massif & zero-rating étatique",
      country: "Chine",
      traffic_discrimination_score: 98.0,
      zero_rating_inequity_score: 96.0,
      paid_prioritization_harm_score: 94.0,
      access_inequality_score: 97.0,
      composite_score: 96.45,
      risk_level: "critique",
      primary_pattern: "State-mandated ISP throttling & zero-rating for domestic platforms only",
      estimated_net_neutrality_rights_index: 9.65,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "NNR-002",
      name: "Russie — Loi Runet, blocages ciblés & DPI généralisé",
      country: "Russie",
      traffic_discrimination_score: 90.0,
      zero_rating_inequity_score: 86.0,
      paid_prioritization_harm_score: 88.0,
      access_inequality_score: 89.0,
      composite_score: 88.45,
      risk_level: "critique",
      primary_pattern: "Sovereign internet law enabling full traffic discrimination",
      estimated_net_neutrality_rights_index: 8.85,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "NNR-003",
      name: "Iran — Internet national, étranglement des flux internationaux",
      country: "Iran",
      traffic_discrimination_score: 88.0,
      zero_rating_inequity_score: 82.0,
      paid_prioritization_harm_score: 85.0,
      access_inequality_score: 86.0,
      composite_score: 85.25,
      risk_level: "critique",
      primary_pattern: "National intranet blocking international access & paid prioritization",
      estimated_net_neutrality_rights_index: 8.53,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "NNR-004",
      name: "Inde — Zero-rating controverses & coupures internet régionales",
      country: "Inde",
      traffic_discrimination_score: 72.0,
      zero_rating_inequity_score: 68.0,
      paid_prioritization_harm_score: 70.0,
      access_inequality_score: 75.0,
      composite_score: 71.25,
      risk_level: "critique",
      primary_pattern: "Zero-rating controversies & regional internet shutdowns",
      estimated_net_neutrality_rights_index: 7.13,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "NNR-005",
      name: "USA — Abrogation règles neutralité FCC, fast lanes ISP",
      country: "États-Unis",
      traffic_discrimination_score: 55.0,
      zero_rating_inequity_score: 52.0,
      paid_prioritization_harm_score: 58.0,
      access_inequality_score: 50.0,
      composite_score: 54.0,
      risk_level: "élevé",
      primary_pattern: "FCC net neutrality repeal enabling ISP paid prioritization",
      estimated_net_neutrality_rights_index: 5.40,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "NNR-006",
      name: "Brésil — Zero-rating opérateurs, fracture numérique rurale",
      country: "Brésil",
      traffic_discrimination_score: 48.0,
      zero_rating_inequity_score: 50.0,
      paid_prioritization_harm_score: 44.0,
      access_inequality_score: 52.0,
      composite_score: 48.4,
      risk_level: "élevé",
      primary_pattern: "Operator zero-rating & rural digital divide",
      estimated_net_neutrality_rights_index: 4.84,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "NNR-007",
      name: "Canada — Surveillance conformité CRTC, trafic P2P throttling",
      country: "Canada",
      traffic_discrimination_score: 28.0,
      zero_rating_inequity_score: 25.0,
      paid_prioritization_harm_score: 30.0,
      access_inequality_score: 27.0,
      composite_score: 27.45,
      risk_level: "modéré",
      primary_pattern: "CRTC oversight with historical P2P throttling incidents",
      estimated_net_neutrality_rights_index: 2.75,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "NNR-008",
      name: "UE — Règlement Open Internet, cadre neutralité solide",
      country: "Union Européenne",
      traffic_discrimination_score: 10.0,
      zero_rating_inequity_score: 12.0,
      paid_prioritization_harm_score: 8.0,
      access_inequality_score: 14.0,
      composite_score: 10.9,
      risk_level: "faible",
      primary_pattern: "Open Internet Regulation & BEREC enforcement framework",
      estimated_net_neutrality_rights_index: 1.09,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/net-neutrality-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(
      NextResponse.json({ payload: FALLBACK_PAYLOAD }, { status: 502 })
    );
  }
}
