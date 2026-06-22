import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[internet-censorship-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[internet-censorship-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Internet Censorship Rights Engine Agent",
  domain: "internet_censorship_rights",
  total_entities: 8,
  avg_composite: 62.83,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Corée du Nord — Intranet national, accès internet quasi-nul pour la population",
    "Chine — Grand Firewall, censure massive & surveillance IA",
    "Iran — Coupures internet, filtrage profond & VPN criminalisés",
  ],
  critical_alerts: [
    "Corée du Nord: Total internet blackout — only state intranet accessible",
    "Chine: Great Firewall — AI-powered mass censorship & platform coercion",
    "Iran: Internet shutdowns during protests & deep packet inspection",
    "Russie: Systematic blocking & journalist persecution post-2022",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_internet_censorship_rights_index: 6.28,
  entities: [
    {
      entity_id: "ICR-001",
      name: "Corée du Nord — Intranet national, accès internet quasi-nul",
      country: "Corée du Nord",
      content_blocking_score: 100.0,
      surveillance_censorship_score: 100.0,
      platform_coercion_score: 99.0,
      journalist_blogger_persecution_score: 100.0,
      composite_score: 99.75,
      risk_level: "critique",
      primary_pattern: "Total internet blackout — only state intranet accessible",
      estimated_internet_censorship_rights_index: 9.98,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ICR-002",
      name: "Chine — Grand Firewall, censure massive & surveillance IA",
      country: "Chine",
      content_blocking_score: 98.0,
      surveillance_censorship_score: 97.0,
      platform_coercion_score: 96.0,
      journalist_blogger_persecution_score: 95.0,
      composite_score: 96.75,
      risk_level: "critique",
      primary_pattern: "Great Firewall — AI-powered mass censorship & platform coercion",
      estimated_internet_censorship_rights_index: 9.68,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ICR-003",
      name: "Iran — Coupures internet, filtrage profond & VPN criminalisés",
      country: "Iran",
      content_blocking_score: 85.0,
      surveillance_censorship_score: 82.0,
      platform_coercion_score: 80.0,
      journalist_blogger_persecution_score: 88.0,
      composite_score: 83.85,
      risk_level: "critique",
      primary_pattern: "Internet shutdowns during protests & deep packet inspection",
      estimated_internet_censorship_rights_index: 8.39,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ICR-004",
      name: "Russie — Blocages systématiques & persécution journalistes post-2022",
      country: "Russie",
      content_blocking_score: 75.0,
      surveillance_censorship_score: 78.0,
      platform_coercion_score: 72.0,
      journalist_blogger_persecution_score: 82.0,
      composite_score: 76.35,
      risk_level: "critique",
      primary_pattern: "Systematic blocking & journalist persecution post-2022",
      estimated_internet_censorship_rights_index: 7.64,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ICR-005",
      name: "Éthiopie — Coupures internet récurrentes lors des conflits ethniques",
      country: "Éthiopie",
      content_blocking_score: 58.0,
      surveillance_censorship_score: 52.0,
      platform_coercion_score: 48.0,
      journalist_blogger_persecution_score: 62.0,
      composite_score: 55.3,
      risk_level: "élevé",
      primary_pattern: "Recurring internet shutdowns during ethnic conflicts",
      estimated_internet_censorship_rights_index: 5.53,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ICR-006",
      name: "Pakistan — Censure politique & arrestations de blogueurs",
      country: "Pakistan",
      content_blocking_score: 48.0,
      surveillance_censorship_score: 44.0,
      platform_coercion_score: 46.0,
      journalist_blogger_persecution_score: 52.0,
      composite_score: 47.4,
      risk_level: "élevé",
      primary_pattern: "Political censorship & blogger arrests",
      estimated_internet_censorship_rights_index: 4.74,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ICR-007",
      name: "Turquie — Blocage réseaux sociaux & lois anti-désinformation",
      country: "Turquie",
      content_blocking_score: 35.0,
      surveillance_censorship_score: 30.0,
      platform_coercion_score: 34.0,
      journalist_blogger_persecution_score: 38.0,
      composite_score: 34.1,
      risk_level: "modéré",
      primary_pattern: "Social media blocking & anti-disinformation laws",
      estimated_internet_censorship_rights_index: 3.41,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ICR-008",
      name: "Islande — Internet libre, liberté de presse maximale",
      country: "Islande",
      content_blocking_score: 4.0,
      surveillance_censorship_score: 3.0,
      platform_coercion_score: 2.0,
      journalist_blogger_persecution_score: 3.0,
      composite_score: 3.05,
      risk_level: "faible",
      primary_pattern: "Free internet, maximum press freedom",
      estimated_internet_censorship_rights_index: 0.31,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/internet-censorship-rights-engine`, {
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
