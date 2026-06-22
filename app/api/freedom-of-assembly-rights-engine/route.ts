import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[freedom-of-assembly-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[freedom-of-assembly-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Freedom Of Assembly Rights Engine Agent",
  domain: "freedom_of_assembly_rights",
  total_entities: 8,
  avg_composite: 60.99,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Biélorussie — Répression 2020 Manifestations Loukachenko, 35 000 Arrestations",
    "Myanmar — Coup 2021, 5 000 Tués Manifestants, Juntes Militaires Loi Martiale",
    "Iran — Mahsa Amini 2022, 15 000 Arrestations, 500 Tués, Loi Anti-Manifestation",
  ],
  critical_alerts: [
    "Biélorussie: mass_protest_repression",
    "Myanmar: military_repression",
    "Iran: mass_protest_repression",
    "Chine: civil_society_ban",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_freedom_of_assembly_rights_index: 6.10,
  entities: [
    {
      entity_id: "FAR-001",
      name: "Biélorussie — Répression 2020 Manifestations Loukachenko, 35 000 Arrestations",
      country: "Biélorussie",
      protest_crackdown_score: 97.0,
      arbitrary_arrest_assembly_score: 96.0,
      civil_society_ban_score: 95.0,
      permit_denial_score: 94.0,
      composite_score: 95.85,
      risk_level: "critique",
      primary_pattern: "mass_protest_repression",
      estimated_freedom_of_assembly_rights_index: 9.59,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "FAR-002",
      name: "Myanmar — Coup 2021, 5 000 Tués Manifestants, Juntes Militaires Loi Martiale",
      country: "Myanmar",
      protest_crackdown_score: 91.0,
      arbitrary_arrest_assembly_score: 93.0,
      civil_society_ban_score: 90.0,
      permit_denial_score: 89.0,
      composite_score: 91.1,
      risk_level: "critique",
      primary_pattern: "military_repression",
      estimated_freedom_of_assembly_rights_index: 9.11,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "FAR-003",
      name: "Iran — Mahsa Amini 2022, 15 000 Arrestations, 500 Tués, Loi Anti-Manifestation",
      country: "Iran",
      protest_crackdown_score: 87.0,
      arbitrary_arrest_assembly_score: 88.0,
      civil_society_ban_score: 85.0,
      permit_denial_score: 84.0,
      composite_score: 86.25,
      risk_level: "critique",
      primary_pattern: "mass_protest_repression",
      estimated_freedom_of_assembly_rights_index: 8.63,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "FAR-004",
      name: "Chine — Tiananmen Héritage, Hong Kong NSL 2020, Manifestations Interdites",
      country: "Chine",
      protest_crackdown_score: 80.0,
      arbitrary_arrest_assembly_score: 78.0,
      civil_society_ban_score: 82.0,
      permit_denial_score: 77.0,
      composite_score: 79.5,
      risk_level: "critique",
      primary_pattern: "civil_society_ban",
      estimated_freedom_of_assembly_rights_index: 7.95,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "FAR-005",
      name: "Russie — Loi Anti-Manifestation 2022, OVD-Info 20 000 Arrestations, NGO Agent Étranger",
      country: "Russie",
      protest_crackdown_score: 54.0,
      arbitrary_arrest_assembly_score: 56.0,
      civil_society_ban_score: 58.0,
      permit_denial_score: 52.0,
      composite_score: 55.1,
      risk_level: "élevé",
      primary_pattern: "civil_society_ban",
      estimated_freedom_of_assembly_rights_index: 5.51,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "FAR-006",
      name: "Égypte — Loi 107/2013 Permis Refusés, 60 000 Prisonniers Politiques",
      country: "Égypte",
      protest_crackdown_score: 46.0,
      arbitrary_arrest_assembly_score: 48.0,
      civil_society_ban_score: 44.0,
      permit_denial_score: 50.0,
      composite_score: 46.7,
      risk_level: "élevé",
      primary_pattern: "permit_denial",
      estimated_freedom_of_assembly_rights_index: 4.67,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "FAR-007",
      name: "France — Loi Séparatisme + BRAV-M, Zones Interdites Gilets Jaunes, 11 000 Gardes à Vue",
      country: "France",
      protest_crackdown_score: 28.0,
      arbitrary_arrest_assembly_score: 30.0,
      civil_society_ban_score: 22.0,
      permit_denial_score: 26.0,
      composite_score: 26.7,
      risk_level: "modéré",
      primary_pattern: "arbitrary_arrest_assembly",
      estimated_freedom_of_assembly_rights_index: 2.67,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "FAR-008",
      name: "Allemagne/Canada — Droit Manifestation Constitutionnel, Plaintes Instruites, ICCPR Complet",
      country: "Allemagne/Canada",
      protest_crackdown_score: 7.0,
      arbitrary_arrest_assembly_score: 8.0,
      civil_society_ban_score: 6.0,
      permit_denial_score: 9.0,
      composite_score: 7.35,
      risk_level: "faible",
      primary_pattern: "permit_denial",
      estimated_freedom_of_assembly_rights_index: 0.74,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/freedom-of-assembly-rights-engine`, {
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
