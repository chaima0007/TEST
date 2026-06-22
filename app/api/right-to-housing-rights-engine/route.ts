import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[right-to-housing-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Right To Housing Rights Engine Agent",
  domain: "right_to_housing_rights",
  total_entities: 8,
  avg_composite: 60.23,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Cambodge — Boeung Kak Lake Expulsions, 10 000 Familles Sans Recours, PM Hun Sen",
    "Soudan du Sud — Déplacements Guerre, 2M de Personnes Sans Abri, IDP Camps",
    "Brésil Favelas — Opérations Militaires Rio, Démolitions Copa/JO Sans Relogement",
  ],
  critical_alerts: [
    "Cambodge: forced_eviction",
    "Soudan du Sud: conflict_displacement",
    "Brésil Favelas: forced_eviction",
    "Inde: indigenous_land_displacement",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_right_to_housing_rights_index: 6.02,
  entities: [
    {
      entity_id: "RTH-001",
      name: "Cambodge — Boeung Kak Lake Expulsions, 10 000 Familles Sans Recours, PM Hun Sen",
      country: "Cambodge",
      forced_eviction_score: 96.0,
      homelessness_criminalization_score: 94.0,
      housing_affordability_crisis_score: 93.0,
      indigenous_land_displacement_score: 95.0,
      composite_score: 94.75,
      risk_level: "critique",
      primary_pattern: "forced_eviction",
      estimated_right_to_housing_rights_index: 9.48,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTH-002",
      name: "Soudan du Sud — Déplacements Guerre, 2M de Personnes Sans Abri, IDP Camps",
      country: "Soudan du Sud",
      forced_eviction_score: 90.0,
      homelessness_criminalization_score: 88.0,
      housing_affordability_crisis_score: 92.0,
      indigenous_land_displacement_score: 87.0,
      composite_score: 89.45,
      risk_level: "critique",
      primary_pattern: "conflict_displacement",
      estimated_right_to_housing_rights_index: 8.95,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTH-003",
      name: "Brésil Favelas — Opérations Militaires Rio, Démolitions Copa/JO Sans Relogement",
      country: "Brésil",
      forced_eviction_score: 84.0,
      homelessness_criminalization_score: 82.0,
      housing_affordability_crisis_score: 85.0,
      indigenous_land_displacement_score: 80.0,
      composite_score: 82.95,
      risk_level: "critique",
      primary_pattern: "forced_eviction",
      estimated_right_to_housing_rights_index: 8.3,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTH-004",
      name: "Inde — Mumbai Slums, 1M Expulsés Dharavi, Dalits Sans Titre Foncier",
      country: "Inde",
      forced_eviction_score: 76.0,
      homelessness_criminalization_score: 74.0,
      housing_affordability_crisis_score: 78.0,
      indigenous_land_displacement_score: 72.0,
      composite_score: 75.2,
      risk_level: "critique",
      primary_pattern: "indigenous_land_displacement",
      estimated_right_to_housing_rights_index: 7.52,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTH-005",
      name: "USA — 650 000 Sans-Abri, Lois Anti-Camping 187 Villes, Criminalisation SDF",
      country: "USA",
      forced_eviction_score: 54.0,
      homelessness_criminalization_score: 58.0,
      housing_affordability_crisis_score: 56.0,
      indigenous_land_displacement_score: 50.0,
      composite_score: 54.7,
      risk_level: "élevé",
      primary_pattern: "homelessness_criminalization",
      estimated_right_to_housing_rights_index: 5.47,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTH-006",
      name: "UK — Section 21 Expulsions, Crise Location, 300 000 Sans-Abri Estimation",
      country: "UK",
      forced_eviction_score: 52.0,
      homelessness_criminalization_score: 50.0,
      housing_affordability_crisis_score: 56.0,
      indigenous_land_displacement_score: 48.0,
      composite_score: 51.6,
      risk_level: "élevé",
      primary_pattern: "housing_affordability_crisis",
      estimated_right_to_housing_rights_index: 5.16,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTH-007",
      name: "France — Droit Opposable Logement (DALO) Insuffisant, 4M Mal-Logés",
      country: "France",
      forced_eviction_score: 26.0,
      homelessness_criminalization_score: 28.0,
      housing_affordability_crisis_score: 30.0,
      indigenous_land_displacement_score: 22.0,
      composite_score: 26.7,
      risk_level: "modéré",
      primary_pattern: "housing_affordability_crisis",
      estimated_right_to_housing_rights_index: 2.67,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTH-008",
      name: "Finlande/Autriche — Housing First Modèle, SDF Quasi-Éliminés, Droit Constitutionnel",
      country: "Finlande/Autriche",
      forced_eviction_score: 7.0,
      homelessness_criminalization_score: 6.0,
      housing_affordability_crisis_score: 8.0,
      indigenous_land_displacement_score: 5.0,
      composite_score: 6.65,
      risk_level: "faible",
      primary_pattern: "forced_eviction",
      estimated_right_to_housing_rights_index: 0.67,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/right-to-housing-rights-engine`, {
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
