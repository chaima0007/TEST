import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[solitary-confinement-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[solitary-confinement-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Solitary Confinement Rights Engine Agent",
  domain: "solitary_confinement_rights",
  total_entities: 8,
  avg_composite: 61.56,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "USA — 80 000 détenus en isolement prolongé, SHU systémique",
    "Corée du Nord — Isolement indéfini dans camps politiques kwanliso",
    "Chine — Isolement des dissidents & minorités en centres secrets",
  ],
  critical_alerts: [
    "USA: 80,000+ prisoners in prolonged solitary — systematic SHU use",
    "Corée du Nord: Indefinite isolation in kwanliso political prison camps",
    "Chine: Secret detention facilities for dissidents & Uyghurs",
    "Turquie: F-type isolation prisons for political prisoners post-coup",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_solitary_confinement_rights_index: 6.16,
  entities: [
    {
      entity_id: "SCR-001",
      name: "USA — 80 000 détenus en isolement prolongé, SHU systémique",
      country: "États-Unis",
      prolonged_isolation_score: 88.0,
      psychological_torture_score: 85.0,
      judicial_oversight_absence_score: 82.0,
      vulnerable_population_isolation_score: 90.0,
      composite_score: 86.35,
      risk_level: "critique",
      primary_pattern: "Systemic SHU use with 80,000+ in prolonged solitary",
      estimated_solitary_confinement_rights_index: 8.64,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SCR-002",
      name: "Corée du Nord — Isolement indéfini dans camps kwanliso",
      country: "Corée du Nord",
      prolonged_isolation_score: 98.0,
      psychological_torture_score: 97.0,
      judicial_oversight_absence_score: 99.0,
      vulnerable_population_isolation_score: 96.0,
      composite_score: 97.55,
      risk_level: "critique",
      primary_pattern: "Indefinite isolation in political prison camps with no oversight",
      estimated_solitary_confinement_rights_index: 9.76,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SCR-003",
      name: "Chine — Centres de détention secrets pour dissidents & Ouïghours",
      country: "Chine",
      prolonged_isolation_score: 90.0,
      psychological_torture_score: 88.0,
      judicial_oversight_absence_score: 94.0,
      vulnerable_population_isolation_score: 92.0,
      composite_score: 91.0,
      risk_level: "critique",
      primary_pattern: "Secret detention & prolonged isolation of political dissidents",
      estimated_solitary_confinement_rights_index: 9.1,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SCR-004",
      name: "Turquie — Prisons F-type & isolement post-coup pour opposants",
      country: "Turquie",
      prolonged_isolation_score: 80.0,
      psychological_torture_score: 78.0,
      judicial_oversight_absence_score: 76.0,
      vulnerable_population_isolation_score: 82.0,
      composite_score: 79.1,
      risk_level: "critique",
      primary_pattern: "F-type isolation prisons for post-coup political prisoners",
      estimated_solitary_confinement_rights_index: 7.91,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SCR-005",
      name: "Russie — Isolement punitif & conditions dégradantes en SIZO",
      country: "Russie",
      prolonged_isolation_score: 58.0,
      psychological_torture_score: 55.0,
      judicial_oversight_absence_score: 52.0,
      vulnerable_population_isolation_score: 56.0,
      composite_score: 55.35,
      risk_level: "élevé",
      primary_pattern: "Punitive isolation in SIZO pre-trial detention facilities",
      estimated_solitary_confinement_rights_index: 5.54,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SCR-006",
      name: "Brésil — Isolement dans établissements fédéraux RDD",
      country: "Brésil",
      prolonged_isolation_score: 46.0,
      psychological_torture_score: 44.0,
      judicial_oversight_absence_score: 42.0,
      vulnerable_population_isolation_score: 48.0,
      composite_score: 44.9,
      risk_level: "élevé",
      primary_pattern: "RDD federal isolation regime with limited judicial review",
      estimated_solitary_confinement_rights_index: 4.49,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SCR-007",
      name: "Australie — Isolement immigration centres de rétention offshore",
      country: "Australie",
      prolonged_isolation_score: 28.0,
      psychological_torture_score: 26.0,
      judicial_oversight_absence_score: 24.0,
      vulnerable_population_isolation_score: 30.0,
      composite_score: 27.1,
      risk_level: "modéré",
      primary_pattern: "Immigration detention isolation with limited oversight",
      estimated_solitary_confinement_rights_index: 2.71,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SCR-008",
      name: "Scandinavie — Réforme isolement, alternatives communautaires",
      country: "Scandinavie",
      prolonged_isolation_score: 10.0,
      psychological_torture_score: 8.0,
      judicial_oversight_absence_score: 6.0,
      vulnerable_population_isolation_score: 9.0,
      composite_score: 8.35,
      risk_level: "faible",
      primary_pattern: "Isolation reform with community-based detention alternatives",
      estimated_solitary_confinement_rights_index: 0.84,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/solitary-confinement-rights-engine`, {
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
