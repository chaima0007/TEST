import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[youth-bulge-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Youth Bulge Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/youth-bulge-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Youth Bulge Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Youth Bulge Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "YB-001", name: "Sahel — Bombe Démographique Djihadiste", country: "Afrique de l'Ouest", sector: "Niger/Mali/Burkina : 50%+ de Moins de 15 ans Sans Avenir Économique", composite_score: 91.1, youth_ratio_pressure_score: 95.0, youth_unemployment_score: 90.0, political_exclusion_score: 88.0, radicalization_vectors_score: 92.0, risk_level: "critique", primary_pattern: "explosion_demographique_conflictuelle", key_signals: ["Youth bulge explosif dans Sahel — cohortes massives de jeunes sans débouchés économiques ni politiques", "Chômage structurel des jeunes alimentant recrutement par groupes armés et mouvements radicaux", "Exclusion politique de la jeunesse — frustration générationnelle convertissable en instabilité violente"], estimated_youth_instability_index: 9.11, last_updated: "2026-06-20" },
    { entity_id: "YB-002", name: "Nigeria — Génération Perdue du Pétrole", country: "Afrique de l'Ouest", sector: "220M d'Habitants — 70% Moins de 30 ans Sans Emploi Formel", composite_score: 87.5, youth_ratio_pressure_score: 90.0, youth_unemployment_score: 85.0, political_exclusion_score: 82.0, radicalization_vectors_score: 88.0, risk_level: "critique", primary_pattern: "explosion_demographique_conflictuelle", key_signals: ["Youth bulge explosif dans Nigeria — cohortes massives de jeunes sans débouchés économiques ni politiques", "Chômage structurel des jeunes alimentant recrutement par groupes armés et mouvements radicaux", "Exclusion politique de la jeunesse — frustration générationnelle convertissable en instabilité violente"], estimated_youth_instability_index: 8.75, last_updated: "2026-06-20" },
    { entity_id: "YB-003", name: "Afghanistan & Pakistan — FATA Powder Keg", country: "Asie Centrale/Sud", sector: "Jeunesse Pachtoune Sans École ni Emploi — Recrutement Taliban Facilité", composite_score: 85.5, youth_ratio_pressure_score: 85.0, youth_unemployment_score: 88.0, political_exclusion_score: 80.0, radicalization_vectors_score: 90.0, risk_level: "critique", primary_pattern: "radicalisation_structurelle", key_signals: ["Youth bulge explosif dans Afghanistan & Pakistan — cohortes massives de jeunes sans débouchés économiques ni politiques", "Chômage structurel des jeunes alimentant recrutement par groupes armés et mouvements radicaux", "Exclusion politique de la jeunesse — frustration générationnelle convertissable en instabilité violente"], estimated_youth_instability_index: 8.55, last_updated: "2026-06-20" },
    { entity_id: "YB-004", name: "Yémen & Irak — Jeunesse de Guerre", country: "MENA", sector: "Générations Entières Formées à la Guerre — Traumatisme et Radicalisation", composite_score: 80.5, youth_ratio_pressure_score: 80.0, youth_unemployment_score: 82.0, political_exclusion_score: 78.0, radicalization_vectors_score: 85.0, risk_level: "critique", primary_pattern: "radicalisation_structurelle", key_signals: ["Youth bulge explosif dans Yémen & Irak — cohortes massives de jeunes sans débouchés économiques ni politiques", "Chômage structurel des jeunes alimentant recrutement par groupes armés et mouvements radicaux", "Exclusion politique de la jeunesse — frustration générationnelle convertissable en instabilité violente"], estimated_youth_instability_index: 8.05, last_updated: "2026-06-20" },
    { entity_id: "YB-005", name: "Égypte & Algérie — Murs du Chômage Jeune", country: "MENA/Afrique du Nord", sector: "Taux Chômage Jeunes 25-30% — Printemps Arabes en Attente", composite_score: 70.75, youth_ratio_pressure_score: 72.0, youth_unemployment_score: 78.0, political_exclusion_score: 65.0, radicalization_vectors_score: 70.0, risk_level: "critique", primary_pattern: "pression_migratoire_forte", key_signals: ["Youth bulge explosif dans Égypte & Algérie — cohortes massives de jeunes sans débouchés économiques ni politiques", "Chômage structurel des jeunes alimentant recrutement par groupes armés et mouvements radicaux", "Exclusion politique de la jeunesse — frustration générationnelle convertissable en instabilité violente"], estimated_youth_instability_index: 7.08, last_updated: "2026-06-20" },
    { entity_id: "YB-006", name: "Inde — Dividende ou Bombe ?", country: "Asie du Sud", sector: "600M de Moins de 25 ans — Course Emploi vs Automatisation", composite_score: 60.65, youth_ratio_pressure_score: 65.0, youth_unemployment_score: 60.0, political_exclusion_score: 55.0, radicalization_vectors_score: 58.0, risk_level: "critique", primary_pattern: "pression_migratoire_forte", key_signals: ["Youth bulge explosif dans Inde — cohortes massives de jeunes sans débouchés économiques ni politiques", "Chômage structurel des jeunes alimentant recrutement par groupes armés et mouvements radicaux", "Exclusion politique de la jeunesse — frustration générationnelle convertissable en instabilité violente"], estimated_youth_instability_index: 6.07, last_updated: "2026-06-20" },
    { entity_id: "YB-007", name: "Brésil & Mexique — Jeunesse Périurbaine", country: "Amériques", sector: "Favelas et Périphéries Urbaines — Recrutement par Gangs Structurel", composite_score: 49.15, youth_ratio_pressure_score: 48.0, youth_unemployment_score: 52.0, political_exclusion_score: 45.0, radicalization_vectors_score: 55.0, risk_level: "élevé", primary_pattern: "pression_migratoire_forte", key_signals: ["Pression démographique jeunesse significative dans Brésil & Mexique — absorption économique insuffisante", "Taux de chômage jeunesse critique — génération entière sans perspectives formelles d'emploi", "Tensions générationnelles avec établissement politique — risque de mobilisation contestataire"], estimated_youth_instability_index: 4.92, last_updated: "2026-06-20" },
    { entity_id: "YB-008", name: "Europe & Japon — Vieillissement Inverse", country: "Global Nord", sector: "Crise de Vieillissement — Youth Bulge Inversé, Pénuries Main d'Oeuvre", composite_score: 8.85, youth_ratio_pressure_score: 8.0, youth_unemployment_score: 10.0, political_exclusion_score: 12.0, radicalization_vectors_score: 5.0, risk_level: "faible", primary_pattern: "dividende_demographique", key_signals: ["Europe & Japon capitalise son dividende démographique — jeunesse intégrée dans la croissance économique", "Marché du travail inclusif avec formations adaptées aux besoins économiques actuels", "Participation politique jeunesse active — relève générationnelle institutionnellement encadrée"], estimated_youth_instability_index: 0.89, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 6, "élevé": 1, "modéré": 0, faible: 1 },
    pattern_distribution: { explosion_demographique_conflictuelle: 2, radicalisation_structurelle: 2, pression_migratoire_forte: 3, tension_generationnelle: 0, dividende_demographique: 1 },
    top_risk_entities: ["Sahel — Bombe Démographique Djihadiste", "Nigeria — Génération Perdue du Pétrole", "Afghanistan & Pakistan — FATA Powder Keg"],
    critical_alerts: ["Sahel: explosion démographique conflictuelle", "Nigeria: explosion démographique conflictuelle", "Afghanistan & Pakistan: radicalisation structurelle", "Yémen & Irak: radicalisation structurelle", "Égypte & Algérie: pression migratoire forte", "Inde: pression migratoire forte"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "youth_bulge",
    confidence_score: 0.88,
    data_sources: ["un_population_division", "ilo_youth_unemployment_tracker", "conflict_early_warning_systems"],
    entities,
    avg_estimated_youth_instability_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
