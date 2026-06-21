import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[housing-eviction-displacement-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Housing Eviction Displacement Rights Engine Agent",
  domain: "housing_eviction_displacement_rights",
  total_entities: 8,
  avg_composite: 62.09,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { forced_eviction_land_grabbing_severity: 3, discriminatory_housing_segregation: 2, housing_affordability_social_protection_deficit_gap: 2, homelessness_inadequate_housing_scale: 1 },
  top_risk_entities: [
    "Éthiopie/Tigré — Déplacements Massifs Conflits, Villages Brûlés & 2M Déplacés Internes",
    "Chine/Urbanisation Forcée — 250M Ruraux Déplacés, Expulsions Sans Compensation & Hukou Discrimination",
    "Inde/Adivasis — Expulsions Projets Barrages & Mines, 50M Déplacés Développement Sans Réinstallation",
  ],
  critical_alerts: [
    "Éthiopie/Tigré: forced_eviction_land_grabbing_severity",
    "Chine/Urbanisation Forcée: forced_eviction_land_grabbing_severity",
    "Zimbabwe/Opération Murambatsvina: housing_affordability_social_protection_deficit_gap",
    "Inde/Adivasis: discriminatory_housing_segregation",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_housing_eviction_displacement_rights_index: 6.21,
  data_sources: [
    "un_special_rapporteur_adequate_housing_forced_evictions_annual_report",
    "cohre_centre_housing_rights_evictions_global_survey_forced_evictions",
    "un_pidesc_general_comment_4_right_adequate_housing_implementation_guide",
  ],
  entities: [
    { id: "HEDR-001", name: "Chine/Urbanisation Forcée — 250M Ruraux Déplacés, Expulsions Sans Compensation & Hukou Discrimination", country: "Asie du Nord-Est", composite_score: 89.1, forced_eviction_land_grabbing_severity_score: 92.0, homelessness_inadequate_housing_scale_score: 88.0, discriminatory_housing_segregation_score: 90.0, housing_affordability_social_protection_deficit_gap_score: 85.0, risk_level: "critique", primary_pattern: "forced_eviction_land_grabbing_severity", estimated_housing_eviction_displacement_rights_index: 8.91, last_updated: "2026-06-21" },
    { id: "HEDR-002", name: "Éthiopie/Tigré — Déplacements Massifs Conflits, Villages Brûlés & 2M Déplacés Internes", country: "Afrique de l'Est", composite_score: 91.5, forced_eviction_land_grabbing_severity_score: 95.0, homelessness_inadequate_housing_scale_score: 92.0, discriminatory_housing_segregation_score: 88.0, housing_affordability_social_protection_deficit_gap_score: 90.0, risk_level: "critique", primary_pattern: "forced_eviction_land_grabbing_severity", estimated_housing_eviction_displacement_rights_index: 9.15, last_updated: "2026-06-21" },
    { id: "HEDR-003", name: "Inde/Adivasis — Expulsions Projets Barrages & Mines, 50M Déplacés Développement Sans Réinstallation", country: "Asie du Sud", composite_score: 88.25, forced_eviction_land_grabbing_severity_score: 88.0, homelessness_inadequate_housing_scale_score: 85.0, discriminatory_housing_segregation_score: 92.0, housing_affordability_social_protection_deficit_gap_score: 88.0, risk_level: "critique", primary_pattern: "discriminatory_housing_segregation", estimated_housing_eviction_displacement_rights_index: 8.83, last_updated: "2026-06-21" },
    { id: "HEDR-004", name: "Zimbabwe/Opération Murambatsvina — 700k Expulsés 2005, Bidonvilles Démolis & Sans-Abrisme Massif", country: "Afrique Australe", composite_score: 87.65, forced_eviction_land_grabbing_severity_score: 85.0, homelessness_inadequate_housing_scale_score: 90.0, discriminatory_housing_segregation_score: 85.0, housing_affordability_social_protection_deficit_gap_score: 92.0, risk_level: "critique", primary_pattern: "housing_affordability_social_protection_deficit_gap", estimated_housing_eviction_displacement_rights_index: 8.77, last_updated: "2026-06-21" },
    { id: "HEDR-005", name: "USA/Crise Logement Abordable — 600k SDF, Expulsions Moratoriums Levés & Gentrification Communautés", country: "Amérique du Nord", composite_score: 55.95, forced_eviction_land_grabbing_severity_score: 52.0, homelessness_inadequate_housing_scale_score: 60.0, discriminatory_housing_segregation_score: 55.0, housing_affordability_social_protection_deficit_gap_score: 58.0, risk_level: "élevé", primary_pattern: "homelessness_inadequate_housing_scale", estimated_housing_eviction_displacement_rights_index: 5.6, last_updated: "2026-06-21" },
    { id: "HEDR-006", name: "Brésil/Favelas JO — Expulsions Rio & São Paulo, Gentrification Événements Sportifs & Déficit Logement", country: "Amérique Latine", composite_score: 54.0, forced_eviction_land_grabbing_severity_score: 55.0, homelessness_inadequate_housing_scale_score: 52.0, discriminatory_housing_segregation_score: 58.0, housing_affordability_social_protection_deficit_gap_score: 50.0, risk_level: "élevé", primary_pattern: "discriminatory_housing_segregation", estimated_housing_eviction_displacement_rights_index: 5.4, last_updated: "2026-06-21" },
    { id: "HEDR-007", name: "HIC/COHRE Habitat International Coalition — Documentation Expulsions Forcées & Plaidoyer Droit Logement", country: "Global", composite_score: 24.7, forced_eviction_land_grabbing_severity_score: 22.0, homelessness_inadequate_housing_scale_score: 26.0, discriminatory_housing_segregation_score: 24.0, housing_affordability_social_protection_deficit_gap_score: 28.0, risk_level: "modéré", primary_pattern: "housing_affordability_social_protection_deficit_gap", estimated_housing_eviction_displacement_rights_index: 2.47, last_updated: "2026-06-21" },
    { id: "HEDR-008", name: "ONU/PIDESC Art.11 — Droit Logement Adéquat, Rapporteur Spécial & Principes Directeurs Expulsions", country: "Global", composite_score: 5.6, forced_eviction_land_grabbing_severity_score: 5.0, homelessness_inadequate_housing_scale_score: 6.0, discriminatory_housing_segregation_score: 4.0, housing_affordability_social_protection_deficit_gap_score: 8.0, risk_level: "faible", primary_pattern: "forced_eviction_land_grabbing_severity", estimated_housing_eviction_displacement_rights_index: 0.56, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/housing-eviction-displacement-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
