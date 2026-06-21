import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[neurotech-cognitive-liberty-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "neurotech_cognitive_liberty_rights_engine",
  domain: "neurotech_cognitive_liberty_rights",
  total_entities: 8,
  avg_composite: 58.56,
  confidence_score: 0.87,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: {
    neural_data_commercialization: 3,
    cognitive_manipulation: 2,
    surveillance_mental: 2,
    regulatory_vacuum: 1,
  },
  top_risk_entities: [
    { id: "NCL-001", name: "Chine — BCI Surveillance État, Neurodonnées Citoyens Sans Consentement", score: 94.1, risk: "critique" },
    { id: "NCL-003", name: "Russie — Psychotronique Militaire, Manipulation Cognitive Dissidents", score: 86.45, risk: "critique" },
    { id: "NCL-002", name: "États-Unis — Neuralink & BigTech, Monétisation Données Cognitives", score: 86.25, risk: "critique" },
  ],
  critical_alerts: [
    "NCL-001: Chine — BCI Surveillance État, Neurodonnées Citoyens Sans Consentement — composite 94.1",
    "NCL-002: États-Unis — Neuralink & BigTech, Monétisation Données Cognitives — composite 86.25",
    "NCL-003: Russie — Psychotronique Militaire, Manipulation Cognitive Dissidents — composite 86.45",
    "NCL-004: Corée du Sud — Neuromarketing Non Régulé, BCI Consommateurs — composite 70.35",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_neurotech_cognitive_liberty_index: 5.86,
  data_sources: [
    "neurorights_foundation_report_2025",
    "ieee_brain_initiative_ethics_2024",
    "un_special_rapporteur_mental_integrity_2023",
    "nature_neuroscience_neuroethics_2024",
  ],
  entities: [
    {
      id: "NCL-001",
      name: "Chine — BCI Surveillance État, Neurodonnées Citoyens Sans Consentement",
      country: "Chine",
      neural_data_extraction_commercialization_score: 95.0,
      cognitive_manipulation_advertising_score: 91.0,
      mental_privacy_surveillance_score: 97.0,
      neurorights_regulatory_framework_score: 93.0,
      composite_score: 94.1,
      risk_level: "critique",
      primary_pattern: "Interface cerveau-ordinateur déployée en milieux professionnels, données neurales collectées sans consentement, fusion IA-surveillance cognitive étatique",
      estimated_neurotech_cognitive_liberty_index: 9.41,
      last_updated: "2026-06-21",
    },
    {
      id: "NCL-002",
      name: "États-Unis — Neuralink & BigTech, Monétisation Données Cognitives",
      country: "États-Unis",
      neural_data_extraction_commercialization_score: 88.0,
      cognitive_manipulation_advertising_score: 92.0,
      mental_privacy_surveillance_score: 85.0,
      neurorights_regulatory_framework_score: 78.0,
      composite_score: 86.25,
      risk_level: "critique",
      primary_pattern: "Extraction données neurales à des fins publicitaires, absence réglementation fédérale neurodroits, manipulation cognitive ciblée Big Tech",
      estimated_neurotech_cognitive_liberty_index: 8.63,
      last_updated: "2026-06-21",
    },
    {
      id: "NCL-003",
      name: "Russie — Psychotronique Militaire, Manipulation Cognitive Dissidents",
      country: "Russie",
      neural_data_extraction_commercialization_score: 82.0,
      cognitive_manipulation_advertising_score: 85.0,
      mental_privacy_surveillance_score: 92.0,
      neurorights_regulatory_framework_score: 88.0,
      composite_score: 86.45,
      risk_level: "critique",
      primary_pattern: "Technologies psychotroniques appliquées aux dissidents, absence droit à la liberté mentale, manipulation neurocognitive ciblée",
      estimated_neurotech_cognitive_liberty_index: 8.65,
      last_updated: "2026-06-21",
    },
    {
      id: "NCL-004",
      name: "Corée du Sud — Neuromarketing Non Régulé, BCI Consommateurs",
      country: "Corée du Sud",
      neural_data_extraction_commercialization_score: 72.0,
      cognitive_manipulation_advertising_score: 75.0,
      mental_privacy_surveillance_score: 68.0,
      neurorights_regulatory_framework_score: 65.0,
      composite_score: 70.35,
      risk_level: "critique",
      primary_pattern: "Neuromarketing intensif sans cadre légal adapté, BCI gaming-travail sans protection cognitive, données EEG non protégées",
      estimated_neurotech_cognitive_liberty_index: 7.04,
      last_updated: "2026-06-21",
    },
    {
      id: "NCL-005",
      name: "Inde — Détection Mensonge Neural Judiciaire, Absence Cadre Éthique",
      country: "Inde",
      neural_data_extraction_commercialization_score: 55.0,
      cognitive_manipulation_advertising_score: 48.0,
      mental_privacy_surveillance_score: 60.0,
      neurorights_regulatory_framework_score: 52.0,
      composite_score: 53.9,
      risk_level: "élevé",
      primary_pattern: "Tests polygraphe neural en procédures judiciaires, absence loi neurodroits, pression mentale sur accusés via technologies cognitives",
      estimated_neurotech_cognitive_liberty_index: 5.39,
      last_updated: "2026-06-21",
    },
    {
      id: "NCL-006",
      name: "Brésil — Neurotech Entreprises Sans Régulation, Travail Cognitif Forcé",
      country: "Brésil",
      neural_data_extraction_commercialization_score: 48.0,
      cognitive_manipulation_advertising_score: 52.0,
      mental_privacy_surveillance_score: 45.0,
      neurorights_regulatory_framework_score: 50.0,
      composite_score: 48.65,
      risk_level: "élevé",
      primary_pattern: "BCI milieux ouvriers sans consentement éclairé, données cognitives vendues à des tiers, lacunes législatives neurotechnologie",
      estimated_neurotech_cognitive_liberty_index: 4.87,
      last_updated: "2026-06-21",
    },
    {
      id: "NCL-007",
      name: "France — RGPD Partiel, Émergence Régulation Neurodonnées UE",
      country: "France",
      neural_data_extraction_commercialization_score: 28.0,
      cognitive_manipulation_advertising_score: 25.0,
      mental_privacy_surveillance_score: 22.0,
      neurorights_regulatory_framework_score: 20.0,
      composite_score: 24.15,
      risk_level: "modéré",
      primary_pattern: "RGPD couvre partiellement les neurodonnées, discussions AI Act UE incluant BCI, initiatives CERNA neurodroits en cours",
      estimated_neurotech_cognitive_liberty_index: 2.42,
      last_updated: "2026-06-21",
    },
    {
      id: "NCL-008",
      name: "Chili — Premier Pays Neurodroits Constitutionnels au Monde",
      country: "Chili",
      neural_data_extraction_commercialization_score: 6.0,
      cognitive_manipulation_advertising_score: 5.0,
      mental_privacy_surveillance_score: 4.0,
      neurorights_regulatory_framework_score: 3.0,
      composite_score: 4.65,
      risk_level: "faible",
      primary_pattern: "Amendement constitutionnel 2021 protégeant intégrité mentale et identité neurale, loi neurodata 2023, modèle mondial neurodroits",
      estimated_neurotech_cognitive_liberty_index: 0.47,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/neurotech-cognitive-liberty-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data.payload ?? data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }));
  }
}
