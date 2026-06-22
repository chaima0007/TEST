import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[stateless-children-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Stateless Children Rights Engine Agent",
  domain: "stateless_children_rights",
  total_entities: 8,
  avg_composite: 60.40,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Bangladesh — Rohingyas Apatrides, 700 000 Enfants Sans Nationalité Myanmar, Enregistrements Naissance Refusés",
    "Émirats Arabes Unis — Bidun, Enfants Apatrides 2e Génération 100 000+, Certificats Naissance Systématiquement Refusés",
    "Kuwait — Bidun, 88 000 Enfants Apatrides Sans Certificats Naissance, Exclusion Totale Droits Civils",
  ],
  critical_alerts: [
    "Bangladesh: birth_registration_denial_score",
    "Émirats Arabes Unis: birth_registration_denial_score",
    "Kuwait: childhood_statelessness_score",
    "Thaïlande: birth_registration_denial_score",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_stateless_children_rights_index: 6.04,
  entities: [
    {
      entity_id: "SCR-001",
      name: "Bangladesh — Rohingyas Apatrides, 700 000 Enfants Sans Nationalité Myanmar, Enregistrements Naissance Refusés",
      country: "Bangladesh",
      birth_registration_denial_score: 95.0,
      childhood_statelessness_score: 94.0,
      education_denial_score: 92.0,
      healthcare_exclusion_score: 91.0,
      composite_score: 93.15,
      risk_level: "critique",
      primary_pattern: "birth_registration_denial_score",
      estimated_stateless_children_rights_index: 9.32,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SCR-002",
      name: "Émirats Arabes Unis — Bidun, Enfants Apatrides 2e Génération 100 000+, Certificats Naissance Systématiquement Refusés",
      country: "Émirats Arabes Unis",
      birth_registration_denial_score: 92.0,
      childhood_statelessness_score: 90.0,
      education_denial_score: 86.0,
      healthcare_exclusion_score: 88.0,
      composite_score: 89.6,
      risk_level: "critique",
      primary_pattern: "birth_registration_denial_score",
      estimated_stateless_children_rights_index: 8.96,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SCR-003",
      name: "Kuwait — Bidun, 88 000 Enfants Apatrides Sans Certificats Naissance, Exclusion Totale Droits Civils",
      country: "Kuwait",
      birth_registration_denial_score: 90.0,
      childhood_statelessness_score: 88.0,
      education_denial_score: 84.0,
      healthcare_exclusion_score: 86.0,
      composite_score: 87.2,
      risk_level: "critique",
      primary_pattern: "childhood_statelessness_score",
      estimated_stateless_children_rights_index: 8.72,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SCR-004",
      name: "Thaïlande — Enfants Tribaux des Montagnes, 200 000 Sans Papiers Apatrides, Accès Éducation et Santé Bloqué",
      country: "Thaïlande",
      birth_registration_denial_score: 84.0,
      childhood_statelessness_score: 82.0,
      education_denial_score: 80.0,
      healthcare_exclusion_score: 78.0,
      composite_score: 81.6,
      risk_level: "critique",
      primary_pattern: "birth_registration_denial_score",
      estimated_stateless_children_rights_index: 8.16,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SCR-005",
      name: "République Dominicaine — Enfants Haïtiens Déchus Nationalité Rétroactivement, 200 000 Rendus Apatrides",
      country: "République Dominicaine",
      birth_registration_denial_score: 55.0,
      childhood_statelessness_score: 52.0,
      education_denial_score: 48.0,
      healthcare_exclusion_score: 50.0,
      composite_score: 51.6,
      risk_level: "élevé",
      primary_pattern: "birth_registration_denial_score",
      estimated_stateless_children_rights_index: 5.16,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SCR-006",
      name: "Côte d'Ivoire — Apatrides Droits de Filiation, Dioula et Autres Communautés, Enregistrement Naissance Discriminatoire",
      country: "Côte d'Ivoire",
      birth_registration_denial_score: 48.0,
      childhood_statelessness_score: 45.0,
      education_denial_score: 43.0,
      healthcare_exclusion_score: 42.0,
      composite_score: 44.85,
      risk_level: "élevé",
      primary_pattern: "childhood_statelessness_score",
      estimated_stateless_children_rights_index: 4.49,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SCR-007",
      name: "USA — Enfants Sans Papiers de Parents Sans Statut, Limbes Légaux, Risque Apatridie de Facto Documenté",
      country: "USA",
      birth_registration_denial_score: 32.0,
      childhood_statelessness_score: 29.0,
      education_denial_score: 26.0,
      healthcare_exclusion_score: 28.0,
      composite_score: 28.95,
      risk_level: "modéré",
      primary_pattern: "birth_registration_denial_score",
      estimated_stateless_children_rights_index: 2.9,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SCR-008",
      name: "Finlande — Procédure Accélérée Apatridie, Meilleure Pratique UNHCR, Enregistrement Naissance Universel Garanti",
      country: "Finlande",
      birth_registration_denial_score: 8.0,
      childhood_statelessness_score: 7.0,
      education_denial_score: 6.0,
      healthcare_exclusion_score: 7.0,
      composite_score: 7.15,
      risk_level: "faible",
      primary_pattern: "birth_registration_denial_score",
      estimated_stateless_children_rights_index: 0.72,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/stateless-children-rights-engine`, {
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
