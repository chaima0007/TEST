import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[birth-registration-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Birth Registration Engine Agent",
  domain: "birth_registration",
  total_entities: 8,
  avg_composite: 57.96,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { unregistered_children: 2, legal_identity_access_denial: 3, statelessness_risk: 1, discriminatory_registration_barriers: 2 },
  top_risk_entities: [
    "Afrique Sub-Saharienne/Sahel — 90M Enfants Sans Acte Naissance & Invisibilité Légale Totale",
    "Rohingyas/Apatrides — 600 000 Enfants Nés Sans Nationalité & Génération Invisible",
    "Inde/Dalit/Tribus — 400M Non-Enregistrés & Discrimination Accès État Civil",
  ],
  critical_alerts: [
    "Afrique Sub-Saharienne/Sahel: unregistered_children",
    "Inde/Dalit/Tribus: legal_identity_access_denial",
    "Rohingyas/Apatrides: statelessness_risk",
    "Haïti/Rép. Dominicaine: discriminatory_registration_barriers",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_birth_registration_index: 5.80,
  data_sources: [
    "unicef_birth_registration_global_database_annual_report",
    "unhcr_global_trends_statelessness_annual_report",
    "id4d_world_bank_identification_development_initiative_data",
  ],
  entities: [
    { entity_id: "BR-001", name: "Afrique Sub-Saharienne/Sahel — 90M Enfants Sans Acte Naissance & Invisibilité Légale Totale", country: "Afrique Sub-Saharienne", composite_score: 88.55, unregistered_children_score: 88.0, statelessness_risk_score: 85.0, legal_identity_access_denial_score: 90.0, discriminatory_registration_barriers_score: 92.0, risk_level: "critique", primary_pattern: "unregistered_children", estimated_birth_registration_index: 8.86, last_updated: "2026-06-20" },
    { entity_id: "BR-002", name: "Inde/Dalit/Tribus — 400M Non-Enregistrés & Discrimination Accès État Civil", country: "Asie du Sud", composite_score: 83.45, unregistered_children_score: 82.0, statelessness_risk_score: 80.0, legal_identity_access_denial_score: 85.0, discriminatory_registration_barriers_score: 88.0, risk_level: "critique", primary_pattern: "legal_identity_access_denial", estimated_birth_registration_index: 8.35, last_updated: "2026-06-20" },
    { entity_id: "BR-003", name: "Rohingyas/Apatrides — 600 000 Enfants Nés Sans Nationalité & Génération Invisible", country: "Asie du Sud-Est", composite_score: 85.00, unregistered_children_score: 90.0, statelessness_risk_score: 92.0, legal_identity_access_denial_score: 80.0, discriminatory_registration_barriers_score: 75.0, risk_level: "critique", primary_pattern: "statelessness_risk", estimated_birth_registration_index: 8.50, last_updated: "2026-06-20" },
    { entity_id: "BR-004", name: "Haïti/Rép. Dominicaine — Apatridie Rétroactive, Antihaitianisme & Dénationalisation", country: "Caraïbes", composite_score: 75.85, unregistered_children_score: 72.0, statelessness_risk_score: 75.0, legal_identity_access_denial_score: 78.0, discriminatory_registration_barriers_score: 80.0, risk_level: "critique", primary_pattern: "discriminatory_registration_barriers", estimated_birth_registration_index: 7.59, last_updated: "2026-06-20" },
    { entity_id: "BR-005", name: "USA/Immigrants Sans-Papiers — 400 000 Enfants Non Déclarés & 14e Amendement Menacé", country: "Amérique du Nord", composite_score: 48.60, unregistered_children_score: 45.0, statelessness_risk_score: 50.0, legal_identity_access_denial_score: 52.0, discriminatory_registration_barriers_score: 48.0, risk_level: "élevé", primary_pattern: "legal_identity_access_denial", estimated_birth_registration_index: 4.86, last_updated: "2026-06-20" },
    { entity_id: "BR-006", name: "Golfe/Bidouns — 100 000 Apatrides Kuwait/EAU & Enfants Nés Sans Nationalité", country: "Moyen-Orient", composite_score: 49.40, unregistered_children_score: 48.0, statelessness_risk_score: 45.0, legal_identity_access_denial_score: 55.0, discriminatory_registration_barriers_score: 50.0, risk_level: "élevé", primary_pattern: "legal_identity_access_denial", estimated_birth_registration_index: 4.94, last_updated: "2026-06-20" },
    { entity_id: "BR-007", name: "UE/Roms — 500 000 Sans Acte Naissance & Discrimination État Civil", country: "Europe", composite_score: 28.40, unregistered_children_score: 25.0, statelessness_risk_score: 28.0, legal_identity_access_denial_score: 30.0, discriminatory_registration_barriers_score: 32.0, risk_level: "modéré", primary_pattern: "discriminatory_registration_barriers", estimated_birth_registration_index: 2.84, last_updated: "2026-06-20" },
    { entity_id: "BR-008", name: "ONU/UNICEF — CRC Art.7, ODD 16.9 & Campagne Identité Légale Pour Tous", country: "Global", composite_score: 4.40, unregistered_children_score: 4.0, statelessness_risk_score: 5.0, legal_identity_access_denial_score: 3.0, discriminatory_registration_barriers_score: 6.0, risk_level: "faible", primary_pattern: "unregistered_children", estimated_birth_registration_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/birth-registration-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
