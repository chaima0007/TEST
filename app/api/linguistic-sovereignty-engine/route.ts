import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[linguistic-sovereignty-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Linguistic Sovereignty Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/linguistic-sovereignty-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Linguistic Sovereignty Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Linguistic Sovereignty Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "LS-001", name: "Langues Autochtones Australie", country: "Océanie", sector: "250 Langues Aborigènes en Extinction Terminale", composite_score: 91.25, speakers_collapse_score: 95.0, intergenerational_transmission_failure_score: 92.0, digital_language_exclusion_score: 90.0, colonial_language_dominance_score: 88.0, risk_level: "critique", primary_pattern: "extinction_linguistique", key_signals: ["Extinction linguistique imminente pour Langues Autochtones Australie — dernier locuteurs âgés, aucune transmission aux jeunes", "Perte irréversible de systèmes de connaissance — taxonomies écologiques et architectures conceptuelles", "Domination de la langue coloniale effaçant l'identité culturelle et la souveraineté épistémique"], estimated_linguistic_risk_index: 9.13, last_updated: "2026-06-20" },
    { entity_id: "LS-002", name: "Amazonie — Langues des Peuples Premiers", country: "Amériques", sector: "400+ Langues Amazoniennes sous Pression Déforestation", composite_score: 89.65, speakers_collapse_score: 90.0, intergenerational_transmission_failure_score: 88.0, digital_language_exclusion_score: 85.0, colonial_language_dominance_score: 92.0, risk_level: "critique", primary_pattern: "domination_coloniale_linguistique", key_signals: ["Extinction linguistique imminente pour Amazonie — dernier locuteurs âgés, aucune transmission aux jeunes", "Perte irréversible de systèmes de connaissance — taxonomies écologiques et architectures conceptuelles", "Domination de la langue coloniale effaçant l'identité culturelle et la souveraineté épistémique"], estimated_linguistic_risk_index: 8.97, last_updated: "2026-06-20" },
    { entity_id: "LS-003", name: "Afrique Subsaharienne — Langues Bantoues", country: "Afrique", sector: "Français/Anglais Colonial Effaçant 2000 Langues", composite_score: 80.35, speakers_collapse_score: 75.0, intergenerational_transmission_failure_score: 72.0, digital_language_exclusion_score: 80.0, colonial_language_dominance_score: 88.0, risk_level: "critique", primary_pattern: "domination_coloniale_linguistique", key_signals: ["Extinction linguistique imminente pour Afrique Subsaharienne — dernier locuteurs âgés, aucune transmission aux jeunes", "Perte irréversible de systèmes de connaissance — taxonomies écologiques et architectures conceptuelles", "Domination de la langue coloniale effaçant l'identité culturelle et la souveraineté épistémique"], estimated_linguistic_risk_index: 8.04, last_updated: "2026-06-20" },
    { entity_id: "LS-004", name: "Sibérie & Arctique — Langues Autochtones", country: "Russie/Arctique", sector: "Russification & Exodus Rural Tuant les Langues", composite_score: 77.3, speakers_collapse_score: 78.0, intergenerational_transmission_failure_score: 80.0, digital_language_exclusion_score: 78.0, colonial_language_dominance_score: 72.0, risk_level: "critique", primary_pattern: "extinction_linguistique", key_signals: ["Extinction linguistique imminente pour Sibérie & Arctique — dernier locuteurs âgés, aucune transmission aux jeunes", "Perte irréversible de systèmes de connaissance — taxonomies écologiques et architectures conceptuelles", "Domination de la langue coloniale effaçant l'identité culturelle et la souveraineté épistémique"], estimated_linguistic_risk_index: 7.73, last_updated: "2026-06-20" },
    { entity_id: "LS-005", name: "Asie du Sud-Est — Minorités Linguistiques", country: "Asie du Sud-Est", sector: "Assimilation Forcée aux Langues Nationales Officielles", composite_score: 63.75, speakers_collapse_score: 62.0, intergenerational_transmission_failure_score: 65.0, digital_language_exclusion_score: 70.0, colonial_language_dominance_score: 60.0, risk_level: "élevé", primary_pattern: "erosion_acceleree", key_signals: ["Érosion linguistique accélérée dans Asie du Sud-Est — jeunes générations migrant vers la langue dominante", "Exclusion numérique — langue absente des plateformes digitales et IA, accélérant l'abandon", "Politique linguistique insuffisante face à la pression économique vers l'assimilation"], estimated_linguistic_risk_index: 6.38, last_updated: "2026-06-20" },
    { entity_id: "LS-006", name: "Europe — Langues Régionales", country: "Europe", sector: "Occitan, Breton, Basque — Résistance vs Homogénéisation", composite_score: 36.0, speakers_collapse_score: 40.0, intergenerational_transmission_failure_score: 38.0, digital_language_exclusion_score: 35.0, colonial_language_dominance_score: 30.0, risk_level: "modéré", primary_pattern: "pression_linguistique", key_signals: ["Pression linguistique significative dans Europe — concurrence avec langue dominante en cours", "Transmission intergénérationnelle fragilisée mais encore active dans contextes familiaux", "Présence numérique limitée — renforcement des espaces digitaux nécessaire pour la survie"], estimated_linguistic_risk_index: 3.6, last_updated: "2026-06-20" },
    { entity_id: "LS-007", name: "Québec & Catalogne — Langues en Résistance", country: "Amériques/Europe", sector: "Politiques Actives de Préservation et Revendication", composite_score: 20.5, speakers_collapse_score: 22.0, intergenerational_transmission_failure_score: 18.0, digital_language_exclusion_score: 25.0, colonial_language_dominance_score: 15.0, risk_level: "modéré", primary_pattern: "pression_linguistique", key_signals: ["Pression linguistique significative dans Québec & Catalogne — concurrence avec langue dominante en cours", "Transmission intergénérationnelle fragilisée mais encore active dans contextes familiaux", "Présence numérique limitée — renforcement des espaces digitaux nécessaire pour la survie"], estimated_linguistic_risk_index: 2.05, last_updated: "2026-06-20" },
    { entity_id: "LS-008", name: "Finlande & Pays Basque — Vitalité Exemplaire", country: "Europe", sector: "Politiques d'Immersion et Bilinguisme Officiel", composite_score: 7.75, speakers_collapse_score: 8.0, intergenerational_transmission_failure_score: 5.0, digital_language_exclusion_score: 12.0, colonial_language_dominance_score: 6.0, risk_level: "faible", primary_pattern: "vitalite_preservee", key_signals: ["Finlande & Pays Basque préserve sa vitalité linguistique — transmission intergénérationnelle active et politique de soutien", "Diversité linguistique maintenue — modèle de coexistence entre langues locales et globales", "Leadership mondial sur la protection du patrimoine linguistique et de la souveraineté culturelle"], estimated_linguistic_risk_index: 0.78, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 1, "modéré": 2, faible: 1 },
    pattern_distribution: { extinction_linguistique: 2, domination_coloniale_linguistique: 2, erosion_acceleree: 1, pression_linguistique: 2, vitalite_preservee: 1 },
    top_risk_entities: ["Langues Autochtones Australie", "Amazonie — Langues des Peuples Premiers", "Afrique Subsaharienne — Langues Bantoues"],
    critical_alerts: ["Australie autochtone: extinction linguistique", "Amazonie: domination coloniale linguistique", "Afrique Subsaharienne: domination coloniale linguistique", "Sibérie & Arctique: extinction linguistique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "linguistic_sovr",
    confidence_score: 0.81,
    data_sources: ["ethnologue_language_status", "unesco_endangered_languages", "digital_language_inclusion_index"],
    entities,
    avg_estimated_linguistic_risk_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
