import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[anti-corruption-human-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Anti Corruption Human Rights Engine Agent",
  domain: "anti_corruption_human_rights",
  total_entities: 8,
  avg_composite: 60.01,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Soudan du Sud — Corruption systémique, 4Md$ détournés depuis indépendance, famine résultante",
    "Venezuela — Maduro kleptocracie, 30Md$ PDVSA détournés, CPI 14/100",
    "Libye — Fonds pétroliers pillés milices, LNA vs GNU corruption bi-latérale",
  ],
  critical_alerts: [
    "Soudan du Sud: public_resource_embezzlement",
    "Venezuela: judicial_corruption",
    "Libye: public_resource_embezzlement",
    "Afghanistan: civil_society_repression",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_anti_corruption_human_rights_index: 6.00,
  entities: [
    {
      entity_id: "ACH-001",
      name: "Soudan du Sud — Corruption systémique, 4Md$ détournés depuis indépendance, famine résultante",
      country: "Soudan du Sud",
      public_resource_embezzlement_score: 97.0,
      judicial_corruption_score: 96.0,
      impunity_of_officials_score: 95.0,
      civil_society_repression_score: 94.0,
      composite_score: 95.65,
      risk_level: "critique",
      primary_pattern: "public_resource_embezzlement",
      estimated_anti_corruption_human_rights_index: 9.57,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ACH-002",
      name: "Venezuela — Maduro kleptocracie, 30Md$ PDVSA détournés, CPI 14/100",
      country: "Venezuela",
      public_resource_embezzlement_score: 91.0,
      judicial_corruption_score: 89.0,
      impunity_of_officials_score: 90.0,
      civil_society_repression_score: 88.0,
      composite_score: 89.7,
      risk_level: "critique",
      primary_pattern: "judicial_corruption",
      estimated_anti_corruption_human_rights_index: 8.97,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ACH-003",
      name: "Libye — Fonds pétroliers pillés milices, LNA vs GNU corruption bi-latérale",
      country: "Libye",
      public_resource_embezzlement_score: 85.0,
      judicial_corruption_score: 83.0,
      impunity_of_officials_score: 84.0,
      civil_society_repression_score: 82.0,
      composite_score: 83.7,
      risk_level: "critique",
      primary_pattern: "public_resource_embezzlement",
      estimated_anti_corruption_human_rights_index: 8.37,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ACH-004",
      name: "Afghanistan — Taliban corruption + héritage Ghani, aide humanitaire détournée",
      country: "Afghanistan",
      public_resource_embezzlement_score: 76.0,
      judicial_corruption_score: 78.0,
      impunity_of_officials_score: 74.0,
      civil_society_repression_score: 80.0,
      composite_score: 76.7,
      risk_level: "critique",
      primary_pattern: "civil_society_repression",
      estimated_anti_corruption_human_rights_index: 7.67,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ACH-005",
      name: "Nigéria — NNPC 6Md$ non-comptabilisés, EFCC impuissante, gouverneurs immunisés",
      country: "Nigéria",
      public_resource_embezzlement_score: 55.0,
      judicial_corruption_score: 57.0,
      impunity_of_officials_score: 58.0,
      civil_society_repression_score: 52.0,
      composite_score: 55.65,
      risk_level: "élevé",
      primary_pattern: "impunity_of_officials",
      estimated_anti_corruption_human_rights_index: 5.57,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ACH-006",
      name: "Brésil — Lava Jato partiellement réversé, Bolsonaro immunité, corruption institutionnelle",
      country: "Brésil",
      public_resource_embezzlement_score: 44.0,
      judicial_corruption_score: 46.0,
      impunity_of_officials_score: 48.0,
      civil_society_repression_score: 42.0,
      composite_score: 45.1,
      risk_level: "élevé",
      primary_pattern: "impunity_of_officials",
      estimated_anti_corruption_human_rights_index: 4.51,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ACH-007",
      name: "Italie — Mafia Cosa Nostra/Ndrangheta, flux financiers illicites, lenteur judiciaire",
      country: "Italie",
      public_resource_embezzlement_score: 28.0,
      judicial_corruption_score: 30.0,
      impunity_of_officials_score: 26.0,
      civil_society_repression_score: 24.0,
      composite_score: 27.1,
      risk_level: "modéré",
      primary_pattern: "judicial_corruption",
      estimated_anti_corruption_human_rights_index: 2.71,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ACH-008",
      name: "Danemark/Nouvelle-Zélande — CPI 90+/100, whistleblowers protégés, tribunaux indépendants",
      country: "Danemark/Nouvelle-Zélande",
      public_resource_embezzlement_score: 6.0,
      judicial_corruption_score: 7.0,
      impunity_of_officials_score: 5.0,
      civil_society_repression_score: 8.0,
      composite_score: 6.45,
      risk_level: "faible",
      primary_pattern: "civil_society_repression",
      estimated_anti_corruption_human_rights_index: 0.65,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/anti-corruption-human-rights-engine`, {
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
