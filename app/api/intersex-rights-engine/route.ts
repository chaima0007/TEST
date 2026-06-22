import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[intersex-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Intersex Rights Engine Agent",
  domain: "intersex_rights",
  total_entities: 8,
  avg_composite: 60.66,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { non_consensual_surgery_prevalence: 3, medical_pathologization_harm: 1, legal_protection_absence: 2, identity_documentation_barrier: 2 },
  top_risk_entities: [
    "USA — 2 Chirurgies/Jour Nourrissons Intersexes, Aucune Loi Fédérale & AAP Non Réformée",
    "Chine & Asie Est — Normalisations Génitales Systémiques, Absence Données & Tabou Culturel",
    "Allemagne — Pratiques Chirurgicales Persistent Malgré Loi 2021, Impunité Médicale & Sous-Déclaration",
  ],
  critical_alerts: [
    "USA: non_consensual_surgery_prevalence",
    "Chine & Asie Est: legal_protection_absence",
    "Allemagne: medical_pathologization_harm",
    "Brésil: non_consensual_surgery_prevalence",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_intersex_rights_index: 6.07,
  data_sources: [
    "oii_europe_intersex_human_rights_violations_country_report",
    "ilga_world_state_sponsored_homophobia_intersex_report",
    "un_crc_crpd_concluding_observations_intersex_children_surgery",
  ],
  entities: [
    { id: "IX-001", name: "USA — 2 Chirurgies/Jour Nourrissons Intersexes, Aucune Loi Fédérale & AAP Non Réformée", country: "Amérique du Nord", composite_score: 92.85, non_consensual_surgery_prevalence_score: 95.0, legal_protection_absence_score: 95.0, medical_pathologization_harm_score: 92.0, identity_documentation_barrier_score: 88.0, risk_level: "critique", primary_pattern: "non_consensual_surgery_prevalence", estimated_intersex_rights_index: 9.29, last_updated: "2026-06-21" },
    { id: "IX-002", name: "Allemagne — Pratiques Chirurgicales Persistent Malgré Loi 2021, Impunité Médicale & Sous-Déclaration", country: "Europe", composite_score: 87.15, non_consensual_surgery_prevalence_score: 88.0, legal_protection_absence_score: 85.0, medical_pathologization_harm_score: 90.0, identity_documentation_barrier_score: 85.0, risk_level: "critique", primary_pattern: "medical_pathologization_harm", estimated_intersex_rights_index: 8.72, last_updated: "2026-06-21" },
    { id: "IX-003", name: "Chine & Asie Est — Normalisations Génitales Systémiques, Absence Données & Tabou Culturel", country: "Asie de l'Est", composite_score: 88.35, non_consensual_surgery_prevalence_score: 90.0, legal_protection_absence_score: 90.0, medical_pathologization_harm_score: 85.0, identity_documentation_barrier_score: 88.0, risk_level: "critique", primary_pattern: "legal_protection_absence", estimated_intersex_rights_index: 8.84, last_updated: "2026-06-21" },
    { id: "IX-004", name: "Brésil — 2000 Chirurgies/An DSD Non Éthiques, Protocoles Pathologisants & Plaintes Ignorées", country: "Amérique Latine", composite_score: 83.65, non_consensual_surgery_prevalence_score: 85.0, legal_protection_absence_score: 82.0, medical_pathologization_harm_score: 85.0, identity_documentation_barrier_score: 82.0, risk_level: "critique", primary_pattern: "non_consensual_surgery_prevalence", estimated_intersex_rights_index: 8.37, last_updated: "2026-06-21" },
    { id: "IX-005", name: "France — Loi 2021 Partielle, Chirurgies Continuent Sur Mineurs & Défenseure Droits Saisie", country: "Europe", composite_score: 53.25, non_consensual_surgery_prevalence_score: 55.0, legal_protection_absence_score: 52.0, medical_pathologization_harm_score: 55.0, identity_documentation_barrier_score: 50.0, risk_level: "élevé", primary_pattern: "non_consensual_surgery_prevalence", estimated_intersex_rights_index: 5.33, last_updated: "2026-06-21" },
    { id: "IX-006", name: "Australie — Rapport Sénat 2013 Partiellement Ignoré, Tutelles Judiciaires & Réforme Lente", country: "Océanie", composite_score: 49.8, non_consensual_surgery_prevalence_score: 48.0, legal_protection_absence_score: 50.0, medical_pathologization_harm_score: 50.0, identity_documentation_barrier_score: 52.0, risk_level: "élevé", primary_pattern: "identity_documentation_barrier", estimated_intersex_rights_index: 4.98, last_updated: "2026-06-21" },
    { id: "IX-007", name: "OII/ILGA World — Campagne EndIntersexSurgeries, Standards Droits Intersexes & Monitoring États", country: "Global", composite_score: 25.85, non_consensual_surgery_prevalence_score: 22.0, legal_protection_absence_score: 28.0, medical_pathologization_harm_score: 25.0, identity_documentation_barrier_score: 30.0, risk_level: "modéré", primary_pattern: "legal_protection_absence", estimated_intersex_rights_index: 2.59, last_updated: "2026-06-21" },
    { id: "IX-008", name: "ONU/CRC & CRPD — Recommandations Chirurgies Intersexes, Art.19 Intégrité Corporelle Enfants", country: "Global", composite_score: 4.4, non_consensual_surgery_prevalence_score: 4.0, legal_protection_absence_score: 5.0, medical_pathologization_harm_score: 3.0, identity_documentation_barrier_score: 6.0, risk_level: "faible", primary_pattern: "identity_documentation_barrier", estimated_intersex_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/intersex-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
