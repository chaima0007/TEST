import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[rare-earth-dominance-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Rare Earth Dominance Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/rare-earth-dominance-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Rare Earth Dominance Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Rare Earth Dominance Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "RE-001", name: "UE — Dépendance Industrielle Critique", country: "Europe", sector: "Industrie Automobile & Éolienne 95% Dépendante REE Chinoises", composite_score: 86.55, chinese_supply_dependency_score: 88.0, processing_monopoly_score: 90.0, strategic_sector_exposure_score: 85.0, alternative_source_deficit_score: 82.0, risk_level: "critique", primary_pattern: "monopole_extraction_total", key_signals: ["Vulnérabilité stratégique majeure de UE — dépendance critique aux terres rares chinoises", "Monopole chinois du raffinage REE — aucune alternative industrielle à l'échelle pour les secteurs critiques", "Exposition militaire et technologique — défense, véhicules électriques et semi-conducteurs sous dépendance REE"], estimated_ree_vulnerability_index: 8.66, last_updated: "2026-06-20" },
    { id: "RE-002", name: "USA — Défense & Semi-Conducteurs Exposés", country: "Amérique du Nord", sector: "Missiles Guidés, Moteurs F-35 et Puces TSMC sous REE Chinoises", composite_score: 80.6, chinese_supply_dependency_score: 75.0, processing_monopoly_score: 82.0, strategic_sector_exposure_score: 88.0, alternative_source_deficit_score: 78.0, risk_level: "critique", primary_pattern: "capture_technologique", key_signals: ["Vulnérabilité stratégique majeure de USA — dépendance critique aux terres rares chinoises", "Monopole chinois du raffinage REE — aucune alternative industrielle à l'échelle pour les secteurs critiques", "Exposition militaire et technologique — défense, véhicules électriques et semi-conducteurs sous dépendance REE"], estimated_ree_vulnerability_index: 8.06, last_updated: "2026-06-20" },
    { id: "RE-003", name: "Japon — Leçon 2010 Non Oubliée", country: "Asie", sector: "Embargo REE Chine 2010 — Diversification Partielle mais Incomplète", composite_score: 70.25, chinese_supply_dependency_score: 65.0, processing_monopoly_score: 80.0, strategic_sector_exposure_score: 75.0, alternative_source_deficit_score: 60.0, risk_level: "critique", primary_pattern: "capture_technologique", key_signals: ["Vulnérabilité stratégique majeure de Japon — dépendance critique aux terres rares chinoises", "Monopole chinois du raffinage REE — aucune alternative industrielle à l'échelle pour les secteurs critiques", "Exposition militaire et technologique — défense, véhicules électriques et semi-conducteurs sous dépendance REE"], estimated_ree_vulnerability_index: 7.03, last_updated: "2026-06-20" },
    { id: "RE-004", name: "Corée du Sud & Taïwan — Semi-Conducteurs REE", country: "Asie", sector: "TSMC/Samsung Dépendant des REE Chinoises pour Wafers & Magnets", composite_score: 74.45, chinese_supply_dependency_score: 72.0, processing_monopoly_score: 75.0, strategic_sector_exposure_score: 82.0, alternative_source_deficit_score: 68.0, risk_level: "critique", primary_pattern: "dependance_sectorielle", key_signals: ["Vulnérabilité stratégique majeure de Corée du Sud & Taïwan — dépendance critique aux terres rares chinoises", "Monopole chinois du raffinage REE — aucune alternative industrielle à l'échelle pour les secteurs critiques", "Exposition militaire et technologique — défense, véhicules électriques et semi-conducteurs sous dépendance REE"], estimated_ree_vulnerability_index: 7.45, last_updated: "2026-06-20" },
    { id: "RE-005", name: "Inde — Extraction Sous-Développée", country: "Asie du Sud", sector: "Réserves REE Conséquentes mais Raffinage Inexistant — Paradoxe", composite_score: 58.1, chinese_supply_dependency_score: 55.0, processing_monopoly_score: 68.0, strategic_sector_exposure_score: 52.0, alternative_source_deficit_score: 58.0, risk_level: "élevé", primary_pattern: "dependance_sectorielle", key_signals: ["Dépendance significative de Inde aux terres rares chinoises — secteurs critiques vulnérables", "Concentration du raffinage REE en Chine — chaînes d'approvisionnement fragiles en cas de tensions", "Diversification insuffisante — alternatives australiennes, canadiennes et africaines encore insuffisantes"], estimated_ree_vulnerability_index: 5.81, last_updated: "2026-06-20" },
    { id: "RE-006", name: "Australie & Canada — Alternatives en Transition", country: "Global Occident", sector: "Mines Pilbara & Québec — Alternatives en Construction sous Pression", composite_score: 50.5, chinese_supply_dependency_score: 52.0, processing_monopoly_score: 58.0, strategic_sector_exposure_score: 48.0, alternative_source_deficit_score: 42.0, risk_level: "élevé", primary_pattern: "transition_en_cours", key_signals: ["Dépendance significative de Australie & Canada aux terres rares chinoises — secteurs critiques vulnérables", "Concentration du raffinage REE en Chine — chaînes d'approvisionnement fragiles en cas de tensions", "Diversification insuffisante — alternatives australiennes, canadiennes et africaines encore insuffisantes"], estimated_ree_vulnerability_index: 5.05, last_updated: "2026-06-20" },
    { id: "RE-007", name: "Afrique — Réserves sans Chaîne de Valeur", country: "Afrique", sector: "RDC/Malawi/Tanzanie Riches en REE — Exportation Brute sans Raffinage", composite_score: 23.0, chinese_supply_dependency_score: 22.0, processing_monopoly_score: 28.0, strategic_sector_exposure_score: 20.0, alternative_source_deficit_score: 22.0, risk_level: "modéré", primary_pattern: "transition_en_cours", key_signals: ["Exposition REE modérée dans Afrique — transition de diversification en cours mais incomplète", "Investissements en cours dans des sources alternatives mais délais industriels longs", "Recyclage REE en développement — réduction progressive de la dépendance aux nouvelles extractions"], estimated_ree_vulnerability_index: 2.3, last_updated: "2026-06-20" },
    { id: "RE-008", name: "Chine — Monopole Mondial REE", country: "Asie", sector: "85% du Raffinage Mondial — Producteur Dominant sans Vulnérabilité REE", composite_score: 5.35, chinese_supply_dependency_score: 5.0, processing_monopoly_score: 8.0, strategic_sector_exposure_score: 5.0, alternative_source_deficit_score: 3.0, risk_level: "faible", primary_pattern: "souverainete_minerale", key_signals: ["Chine préserve sa souveraineté minérale — diversification REE robuste et production domestique", "Sources d'approvisionnement REE diversifiées — pas de dépendance critique à un fournisseur unique", "Modèle de souveraineté minérale à partager — investissements précoces dans l'extraction et le recyclage REE"], estimated_ree_vulnerability_index: 0.54, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { monopole_extraction_total: 1, capture_technologique: 2, dependance_sectorielle: 2, transition_en_cours: 2, souverainete_minerale: 1 },
    top_risk_entities: ["UE — Dépendance Industrielle Critique", "USA — Défense & Semi-Conducteurs Exposés", "Corée du Sud & Taïwan — Semi-Conducteurs REE"],
    critical_alerts: ["UE: monopole extraction total", "USA: capture technologique", "Japon: capture technologique", "Corée du Sud & Taïwan: dépendance sectorielle"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "rare_earth",
    confidence_score: 0.85,
    data_sources: ["usgs_mineral_resources_survey", "iea_critical_minerals_tracker", "roskill_rare_earth_outlook"],
    entities,
    avg_estimated_ree_vulnerability_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
