import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[nomadic-peoples-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Nomadic Peoples Rights Engine Agent",
  domain: "nomadic_peoples_rights",
  total_entities: 8,
  avg_composite: 61.03,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { discrimination_service_access_denial: 2, legal_recognition_land_rights_gap: 2, forced_sedentarization_displacement_scale: 2, cultural_identity_assimilation_pressure: 2 },
  top_risk_entities: [
    "Roms Europe — 10-12M Personnes, 80% Pauvreté, Expulsions Forcées & Discrimination Institutionnelle",
    "Touaregs Sahel — Mali/Niger/Burkina, Rébellions Réprimées, Pastoralisme Menacé & Déplacements",
    "Bédouins Israël/Neguev — 90K Maisons Illégales, Démolitions Rahat & Plan Begin Non Reconnu",
  ],
  critical_alerts: [
    "Roms Europe: discrimination_service_access_denial",
    "Touaregs Sahel: legal_recognition_land_rights_gap",
    "Bédouins Israël/Neguev: forced_sedentarization_displacement_scale",
    "Penan Bornéo/Malaisie: cultural_identity_assimilation_pressure",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_nomadic_peoples_rights_index: 6.1,
  data_sources: [
    "european_roma_rights_centre_annual_report_forced_evictions",
    "minority_rights_group_nomadic_peoples_under_threat_report",
    "un_dnudpa_nomadic_indigenous_peoples_rights_implementation",
  ],
  entities: [
    { entity_id: "NP-001", name: "Roms Europe — 10-12M Personnes, 80% Pauvreté, Expulsions Forcées & Discrimination Institutionnelle", country: "Europe", composite_score: 91.85, forced_sedentarization_displacement_scale_score: 92.0, legal_recognition_land_rights_gap_score: 90.0, discrimination_service_access_denial_score: 95.0, cultural_identity_assimilation_pressure_score: 90.0, risk_level: "critique", primary_pattern: "discrimination_service_access_denial", estimated_nomadic_peoples_rights_index: 9.19, last_updated: "2026-06-21" },
    { entity_id: "NP-002", name: "Touaregs Sahel — Mali/Niger/Burkina, Rébellions Réprimées, Pastoralisme Menacé & Déplacements", country: "Afrique de l'Ouest", composite_score: 89.6, forced_sedentarization_displacement_scale_score: 90.0, legal_recognition_land_rights_gap_score: 92.0, discrimination_service_access_denial_score: 88.0, cultural_identity_assimilation_pressure_score: 88.0, risk_level: "critique", primary_pattern: "legal_recognition_land_rights_gap", estimated_nomadic_peoples_rights_index: 8.96, last_updated: "2026-06-21" },
    { entity_id: "NP-003", name: "Bédouins Israël/Neguev — 90K Maisons Illégales, Démolitions Rahat & Plan Begin Non Reconnu", country: "Moyen-Orient", composite_score: 87.3, forced_sedentarization_displacement_scale_score: 88.0, legal_recognition_land_rights_gap_score: 90.0, discrimination_service_access_denial_score: 88.0, cultural_identity_assimilation_pressure_score: 82.0, risk_level: "critique", primary_pattern: "forced_sedentarization_displacement_scale", estimated_nomadic_peoples_rights_index: 8.73, last_updated: "2026-06-21" },
    { entity_id: "NP-004", name: "Penan Bornéo/Malaisie — Forêt Déforestée, Chasseurs-Cueilleurs Expulsés & Mines Illégales", country: "Asie du Sud-Est", composite_score: 85.0, forced_sedentarization_displacement_scale_score: 85.0, legal_recognition_land_rights_gap_score: 85.0, discrimination_service_access_denial_score: 85.0, cultural_identity_assimilation_pressure_score: 85.0, risk_level: "critique", primary_pattern: "cultural_identity_assimilation_pressure", estimated_nomadic_peoples_rights_index: 8.5, last_updated: "2026-06-21" },
    { entity_id: "NP-005", name: "Maasai Kenya/Tanzanie — Déplacements Parcs Touristiques, Perte Pâturages & Discrimination", country: "Afrique de l'Est", composite_score: 53.5, forced_sedentarization_displacement_scale_score: 52.0, legal_recognition_land_rights_gap_score: 55.0, discrimination_service_access_denial_score: 55.0, cultural_identity_assimilation_pressure_score: 52.0, risk_level: "élevé", primary_pattern: "forced_sedentarization_displacement_scale", estimated_nomadic_peoples_rights_index: 5.35, last_updated: "2026-06-21" },
    { entity_id: "NP-006", name: "Roms/Gens du Voyage France — 600+ Évacuations/An, Scolarité Difficile & Loi Besson Stigma", country: "Europe", composite_score: 50.75, forced_sedentarization_displacement_scale_score: 48.0, legal_recognition_land_rights_gap_score: 52.0, discrimination_service_access_denial_score: 55.0, cultural_identity_assimilation_pressure_score: 48.0, risk_level: "élevé", primary_pattern: "discrimination_service_access_denial", estimated_nomadic_peoples_rights_index: 5.08, last_updated: "2026-06-21" },
    { entity_id: "NP-007", name: "ERRC/OSCE — European Roma Rights Centre, Monitoring Expulsions & Advocacy Conseil Europe", country: "Global", composite_score: 25.85, forced_sedentarization_displacement_scale_score: 22.0, legal_recognition_land_rights_gap_score: 28.0, discrimination_service_access_denial_score: 25.0, cultural_identity_assimilation_pressure_score: 30.0, risk_level: "modéré", primary_pattern: "legal_recognition_land_rights_gap", estimated_nomadic_peoples_rights_index: 2.59, last_updated: "2026-06-21" },
    { entity_id: "NP-008", name: "ONU/DNUDPA — Déclaration Droits Peuples Autochtones Nomades, CERD Roms & ICCPR Art.27", country: "Global", composite_score: 4.4, forced_sedentarization_displacement_scale_score: 4.0, legal_recognition_land_rights_gap_score: 5.0, discrimination_service_access_denial_score: 3.0, cultural_identity_assimilation_pressure_score: 6.0, risk_level: "faible", primary_pattern: "cultural_identity_assimilation_pressure", estimated_nomadic_peoples_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/nomadic-peoples-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
