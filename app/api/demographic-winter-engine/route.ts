import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[demographic-winter-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Demographic Winter Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/demographic-winter-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Demographic Winter Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Demographic Winter Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "DW-001", name: "Institut Démographique du Japon", country: "Japon", sector: "Démographie Nationale", composite_score: 84.60, fertility_decline_score: 92, aging_index: 88, migration_pressure: 72, labor_shortage_score: 85, risk_level: "critique", primary_pattern: "Effondrement Natalité", key_signals: ["TFR 1.0 — effondrement natalité absolu", "Population 65+ dépasse 30% — record mondial", "Ratio actifs/retraités < 1.8 — insoutenable"], estimated_demographic_index: 8.46, last_updated: "2026-06-20" },
    { id: "DW-002", name: "Bureau Démographique Corée du Sud", country: "Corée du Sud", sector: "Politique Sociale", composite_score: 79.50, fertility_decline_score: 88, aging_index: 82, migration_pressure: 68, labor_shortage_score: 78, risk_level: "critique", primary_pattern: "Effondrement Natalité", key_signals: ["TFR 0.72 — le plus bas au monde", "Villes secondaires en dépopulation rapide", "Pénurie soignants critiques d'ici 2030"], estimated_demographic_index: 7.95, last_updated: "2026-06-20" },
    { id: "DW-003", name: "Observatoire Démographique Italie", country: "Italie", sector: "Économie Publique", composite_score: 71.15, fertility_decline_score: 78, aging_index: 75, migration_pressure: 60, labor_shortage_score: 70, risk_level: "critique", primary_pattern: "Effondrement Natalité", key_signals: ["TFR 1.2 — sous seuil de remplacement depuis 50 ans", "Mezzogiorno en désertification démographique", "Dette retraite > 15% PIB projeté 2040"], estimated_demographic_index: 7.12, last_updated: "2026-06-20" },
    { id: "DW-004", name: "Agence Fédérale Démographie Allemagne", country: "Allemagne", sector: "Marché du Travail", composite_score: 62.15, fertility_decline_score: 60, aging_index: 72, migration_pressure: 55, labor_shortage_score: 62, risk_level: "critique", primary_pattern: "Vieillissement Accéléré", key_signals: ["Déficit annuel 400 000 travailleurs qualifiés", "TFR 1.46 — légère hausse mais insuffisante", "Vieillissement industrie manufacturière critique"], estimated_demographic_index: 6.22, last_updated: "2026-06-20" },
    { id: "DW-005", name: "Instituto Nacional de Estadística Espagne", country: "Espagne", sector: "Démographie Nationale", composite_score: 52.25, fertility_decline_score: 50, aging_index: 60, migration_pressure: 45, labor_shortage_score: 55, risk_level: "élevé", primary_pattern: "Pénurie Main-d'Œuvre", key_signals: ["TFR 1.16 — déclin accéléré post-crise", "Exode rural vers Madrid et Barcelone", "Secteur agricole manque 120 000 saisonniers/an"], estimated_demographic_index: 5.23, last_updated: "2026-06-20" },
    { id: "DW-006", name: "Office Statistique Grèce", country: "Grèce", sector: "Politique Sociale", composite_score: 51.10, fertility_decline_score: 55, aging_index: 58, migration_pressure: 42, labor_shortage_score: 48, risk_level: "élevé", primary_pattern: "Déclin Démographique Structurel", key_signals: ["Émigration des jeunes diplômés vers l'UE nord", "TFR 1.30 — stagnation post-austérité", "Îles en dépopulation — 20 fermées depuis 2010"], estimated_demographic_index: 5.11, last_updated: "2026-06-20" },
    { id: "DW-007", name: "Institut National d'Études Démographiques France", country: "France", sector: "Économie Publique", composite_score: 31.90, fertility_decline_score: 30, aging_index: 38, migration_pressure: 28, labor_shortage_score: 32, risk_level: "modéré", primary_pattern: "Déclin Démographique Structurel", key_signals: ["TFR 1.68 — meilleur d'Europe mais en baisse", "Réforme retraites 2023 — tension sociale persistante", "Déserts médicaux en zones rurales croissants"], estimated_demographic_index: 3.19, last_updated: "2026-06-20" },
    { id: "DW-008", name: "Statistics Sweden — SCB", country: "Suède", sector: "Démographie Nationale", composite_score: 12.65, fertility_decline_score: 12, aging_index: 15, migration_pressure: 10, labor_shortage_score: 14, risk_level: "faible", primary_pattern: "Stabilité Démographique", key_signals: ["TFR 1.67 — politique familiale efficace", "Immigration nette positive et intégrée", "Marché travail flexible — faible chômage structurel"], estimated_demographic_index: 1.27, last_updated: "2026-06-20" },
  ];

  const n = entities.length;
  const avg_composite = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / n * 100) / 100;

  const summary = {
    total_entities: n,
    avg_composite,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { "Effondrement Natalité": 3, "Vieillissement Accéléré": 1, "Pénurie Main-d'Œuvre": 1, "Déclin Démographique Structurel": 2, "Stabilité Démographique": 1 },
    top_risk_entities: ["Institut Démographique du Japon", "Bureau Démographique Corée du Sud", "Observatoire Démographique Italie"],
    critical_alerts: 4,
    last_analysis: "2026-06-20",
    engine_version: "2.1.0",
    domain: "demographic",
    confidence_score: 87.5,
    data_sources: ["ONU — Division de la Population 2025", "Eurostat — Démographie et Migration 2026", "OCDE — Perspectives Démographiques Mondiales"],
    entities,
    avg_estimated_demographic_index: Math.round(avg_composite / 100 * 10 * 100) / 100,
  };

  return summary;
}
