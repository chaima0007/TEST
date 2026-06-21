import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[protest-freedom-assembly-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Protest Freedom Assembly Rights Engine Agent",
  domain: "protest_freedom_assembly_rights",
  total_entities: 8,
  avg_composite: 64.03,
  confidence_score: 0.87,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { protest_criminalization_mass_arrest: 2, lethal_force_crowd_dispersal: 2, surveillance_protest_infiltration: 2, security_force_impunity_protest: 2 },
  top_risk_entities: [
    "Myanmar — Coup 2021, Milliers Manifestants Tués, 20000+ Arrêtés & Criminalisation Totale Dissidence",
    "Iran — Mahsa Amini 2022, 500+ Morts, 15000+ Arrestations & Exécutions Militants",
    "Russie — Loi Anti-Manifestation, 16000+ Arrêtés Protestation Ukraine & Opposants Torturés",
  ],
  critical_alerts: [
    "Myanmar: lethal_force_crowd_dispersal",
    "Iran: protest_criminalization_mass_arrest",
    "Russie: protest_criminalization_mass_arrest",
    "Chine: surveillance_protest_infiltration",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_protest_freedom_assembly_rights_index: 6.40,
  data_sources: [
    "civicus_monitor_civic_space_2023",
    "amnesty_international_protest_rights_2023",
    "human_rights_watch_protest_repression_2023",
    "un_special_rapporteur_peaceful_assembly_2023",
  ],
  entities: [
    { id: "PFA-001", name: "Myanmar — Coup 2021, Milliers Manifestants Tués, 20000+ Arrêtés & Criminalisation Totale Dissidence", country: "Asie du Sud-Est", composite_score: 96.45, protest_criminalization_mass_arrest_score: 97.0, lethal_force_crowd_dispersal_score: 98.0, surveillance_protest_infiltration_score: 95.0, security_force_impunity_protest_score: 95.0, risk_level: "critique", primary_pattern: "lethal_force_crowd_dispersal", estimated_protest_freedom_assembly_rights_index: 9.65, last_updated: "2026-06-21" },
    { id: "PFA-002", name: "Iran — Mahsa Amini 2022, 500+ Morts, 15000+ Arrestations & Exécutions Militants", country: "Moyen-Orient", composite_score: 93.25, protest_criminalization_mass_arrest_score: 94.0, lethal_force_crowd_dispersal_score: 95.0, surveillance_protest_infiltration_score: 92.0, security_force_impunity_protest_score: 92.0, risk_level: "critique", primary_pattern: "protest_criminalization_mass_arrest", estimated_protest_freedom_assembly_rights_index: 9.33, last_updated: "2026-06-21" },
    { id: "PFA-003", name: "Russie — Loi Anti-Manifestation, 16000+ Arrêtés Protestation Ukraine & Opposants Torturés", country: "Europe de l'Est", composite_score: 89.85, protest_criminalization_mass_arrest_score: 92.0, lethal_force_crowd_dispersal_score: 88.0, surveillance_protest_infiltration_score: 90.0, security_force_impunity_protest_score: 89.0, risk_level: "critique", primary_pattern: "protest_criminalization_mass_arrest", estimated_protest_freedom_assembly_rights_index: 8.99, last_updated: "2026-06-21" },
    { id: "PFA-004", name: "Chine — Mouvement Parapluie Hong Kong, Loi Sécurité Nationale, Surveillance Massive & Zéro Manifestation", country: "Asie du Nord-Est", composite_score: 85.55, protest_criminalization_mass_arrest_score: 86.0, lethal_force_crowd_dispersal_score: 84.0, surveillance_protest_infiltration_score: 89.0, security_force_impunity_protest_score: 83.0, risk_level: "critique", primary_pattern: "surveillance_protest_infiltration", estimated_protest_freedom_assembly_rights_index: 8.56, last_updated: "2026-06-21" },
    { id: "PFA-005", name: "USA — Black Lives Matter Répression, Gaz Lacrymogènes Autorisés, Arrestations 14000+ 2020 & Lois Anti-Manifestation", country: "Amérique du Nord", composite_score: 54.75, protest_criminalization_mass_arrest_score: 55.0, lethal_force_crowd_dispersal_score: 58.0, surveillance_protest_infiltration_score: 53.0, security_force_impunity_protest_score: 53.0, risk_level: "élevé", primary_pattern: "lethal_force_crowd_dispersal", estimated_protest_freedom_assembly_rights_index: 5.48, last_updated: "2026-06-21" },
    { id: "PFA-006", name: "Biélorussie — Répression 2020 Post-Élection, 35000+ Arrêtés, Torture Systématique & Exil Opposants", country: "Europe de l'Est", composite_score: 51.85, protest_criminalization_mass_arrest_score: 52.0, lethal_force_crowd_dispersal_score: 50.0, surveillance_protest_infiltration_score: 54.0, security_force_impunity_protest_score: 51.0, risk_level: "élevé", primary_pattern: "surveillance_protest_infiltration", estimated_protest_freedom_assembly_rights_index: 5.19, last_updated: "2026-06-21" },
    { id: "PFA-007", name: "CIVICUS — Moniteur Espace Civique, 196 Pays, Tendances Rétrécissement & Plaidoyer Liberté Réunion", country: "Global", composite_score: 27.55, protest_criminalization_mass_arrest_score: 28.0, lethal_force_crowd_dispersal_score: 26.0, surveillance_protest_infiltration_score: 29.0, security_force_impunity_protest_score: 27.0, risk_level: "modéré", primary_pattern: "protest_criminalization_mass_arrest", estimated_protest_freedom_assembly_rights_index: 2.76, last_updated: "2026-06-21" },
    { id: "PFA-008", name: "ONU/Rapporteur Spécial — Droits Réunion Pacifique, Standards Internationaux, Rapports & Recommandations États", country: "Global", composite_score: 9.0, protest_criminalization_mass_arrest_score: 9.0, lethal_force_crowd_dispersal_score: 8.0, surveillance_protest_infiltration_score: 10.0, security_force_impunity_protest_score: 9.0, risk_level: "faible", primary_pattern: "security_force_impunity_protest", estimated_protest_freedom_assembly_rights_index: 0.9, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/protest-freedom-assembly-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
