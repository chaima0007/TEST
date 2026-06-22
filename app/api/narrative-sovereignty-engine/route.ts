import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[narrative-sovereignty-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Narrative Sovereignty Engine Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/narrative-sovereignty-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Narrative Sovereignty Engine Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Narrative Sovereignty Engine Agent"), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    { id: "NR-001", name: "Afrique Francophone", country: "Afrique", sector: "Colonisation Narrative Totale", composite_score: 88.75, narrative_dependency_score: 92.0, counter_narrative_vulnerability_score: 88.0, cultural_infrastructure_deficit_score: 90.0, narrative_production_gap_score: 85.0, risk_level: "critique", primary_pattern: "colonisation_narrative", key_signals: ["Colonisation narrative critique de Afrique Francophone — récits identitaires sous contrôle étranger", "Absence d'industrie culturelle nationale compétitive — dépendance aux contenus importés", "Vulnérabilité aux contre-récits et à la manipulation narrative étrangère"], estimated_narrative_index: 8.88, last_updated: "2026-06-20" },
    { id: "NR-002", name: "MENA — Dépendance Narrative", country: "Moyen-Orient", sector: "Récits Occidentaux Dominants", composite_score: 83.75, narrative_dependency_score: 85.0, counter_narrative_vulnerability_score: 82.0, cultural_infrastructure_deficit_score: 88.0, narrative_production_gap_score: 80.0, risk_level: "critique", primary_pattern: "colonisation_narrative", key_signals: ["Colonisation narrative critique de MENA — récits identitaires sous contrôle étranger", "Absence d'industrie culturelle nationale compétitive — dépendance aux contenus importés", "Vulnérabilité aux contre-récits et à la manipulation narrative étrangère"], estimated_narrative_index: 8.38, last_updated: "2026-06-20" },
    { id: "NR-003", name: "Asie du Sud-Est", country: "Asie", sector: "Sandwich USA/Chine Narratif", composite_score: 78.75, narrative_dependency_score: 80.0, counter_narrative_vulnerability_score: 78.0, cultural_infrastructure_deficit_score: 82.0, narrative_production_gap_score: 75.0, risk_level: "critique", primary_pattern: "dependance_culturelle_structurelle", key_signals: ["Colonisation narrative critique de Asie du Sud-Est — récits identitaires sous contrôle étranger", "Absence d'industrie culturelle nationale compétitive — dépendance aux contenus importés", "Vulnérabilité aux contre-récits et à la manipulation narrative étrangère"], estimated_narrative_index: 7.88, last_updated: "2026-06-20" },
    { id: "NR-004", name: "Amérique Latine", country: "Amériques", sector: "Soft Power Américain Dominant", composite_score: 69.75, narrative_dependency_score: 72.0, counter_narrative_vulnerability_score: 68.0, cultural_infrastructure_deficit_score: 70.0, narrative_production_gap_score: 65.0, risk_level: "critique", primary_pattern: "dependance_culturelle_structurelle", key_signals: ["Colonisation narrative critique de Amérique Latine — récits identitaires sous contrôle étranger", "Absence d'industrie culturelle nationale compétitive — dépendance aux contenus importés", "Vulnérabilité aux contre-récits et à la manipulation narrative étrangère"], estimated_narrative_index: 6.98, last_updated: "2026-06-20" },
    { id: "NR-005", name: "Inde — Bollywood & Résistance", country: "Asie du Sud", sector: "Puissance Narrative Émergente", composite_score: 43.75, narrative_dependency_score: 45.0, counter_narrative_vulnerability_score: 42.0, cultural_infrastructure_deficit_score: 48.0, narrative_production_gap_score: 40.0, risk_level: "élevé", primary_pattern: "guerre_recits", key_signals: ["Dépendance culturelle avancée dans Inde — influence narrative étrangère dominante", "Infrastructure narrative insuffisante — production locale dépassée par l'import culturel", "Guerre des récits défavorable — difficulté à faire rayonner les valeurs nationales"], estimated_narrative_index: 4.38, last_updated: "2026-06-20" },
    { id: "NR-006", name: "Europe — Dépendance GAFA", country: "Europe", sector: "Récits Technologiques US Dominants", composite_score: 37.0, narrative_dependency_score: 38.0, counter_narrative_vulnerability_score: 35.0, cultural_infrastructure_deficit_score: 42.0, narrative_production_gap_score: 32.0, risk_level: "modéré", primary_pattern: "tension_narrative", key_signals: ["Tensions narratives modérées dans Europe — influence étrangère partielle sur les récits", "Industries créatives en développement mais compétitivité mondiale encore limitée", "Soft power narratif en construction — potentiel de souveraineté à consolider"], estimated_narrative_index: 3.70, last_updated: "2026-06-20" },
    { id: "NR-007", name: "Russie — Narratif Alternatif", country: "Europe de l'Est", sector: "Contre-Récit Mondial Partiel", composite_score: 24.0, narrative_dependency_score: 25.0, counter_narrative_vulnerability_score: 22.0, cultural_infrastructure_deficit_score: 28.0, narrative_production_gap_score: 20.0, risk_level: "modéré", primary_pattern: "tension_narrative", key_signals: ["Tensions narratives modérées dans Russie — influence étrangère partielle sur les récits", "Industries créatives en développement mais compétitivité mondiale encore limitée", "Soft power narratif en construction — potentiel de souveraineté à consolider"], estimated_narrative_index: 2.40, last_updated: "2026-06-20" },
    { id: "NR-008", name: "USA & Chine — Duopole Narratif", country: "Global", sector: "Souveraineté Narrative Absolue", composite_score: 5.75, narrative_dependency_score: 5.0, counter_narrative_vulnerability_score: 8.0, cultural_infrastructure_deficit_score: 4.0, narrative_production_gap_score: 6.0, risk_level: "faible", primary_pattern: "souverainete_narrative", key_signals: ["USA & Chine — Duopole Narratif jouit d'une souveraineté narrative consolidée — puissance culturelle rayonnante", "Production narrative exportée mondialement — capacité à fixer les récits dominants", "Infrastructure culturelle robuste — résistance naturelle aux contre-récits étrangers"], estimated_narrative_index: 0.58, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 1, "modéré": 2, faible: 1 },
    pattern_distribution: { colonisation_narrative: 2, dependance_culturelle_structurelle: 2, guerre_recits: 1, tension_narrative: 2, souverainete_narrative: 1 },
    top_risk_entities: ["Afrique Francophone", "MENA — Dépendance Narrative", "Asie du Sud-Est"],
    critical_alerts: ["Afrique Francophone: colonisation narrative", "MENA: colonisation narrative", "Asie du Sud-Est: dépendance culturelle structurelle", "Amérique Latine: dépendance culturelle structurelle"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "narrative",
    confidence_score: 0.76,
    data_sources: ["cultural_power_index", "soft_power_tracker", "narrative_influence_monitor"],
    entities,
    avg_estimated_narrative_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
