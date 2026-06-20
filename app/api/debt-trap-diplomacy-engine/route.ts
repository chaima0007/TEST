import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[debt-trap-diplomacy-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Debt Trap Diplomacy Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/debt-trap-diplomacy-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Debt Trap Diplomacy Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Debt Trap Diplomacy Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "DT-001", name: "Sri Lanka — Hambantota Loué 99 ans", country: "Asie du Sud", sector: "Port Stratégique Cédé à Pékin — Modèle du Piège BRI", composite_score: 91.0, bri_debt_ratio_score: 92.0, strategic_asset_collateral_score: 95.0, political_alignment_coercion_score: 85.0, repayment_capacity_deficit_score: 90.0, risk_level: "critique", primary_pattern: "souverainete_compromise", key_signals: ["Piège de la dette actif dans Sri Lanka — dette BRI insoutenable convertie en concessions souveraines à Pékin", "Actifs stratégiques hypothéqués à la Chine — ports, aéroports ou ressources naturelles sous contrôle chinois", "Souveraineté de politique étrangère compromise — alignement forcé sur Pékin dans les enceintes internationales"], estimated_debt_trap_index: 9.1, last_updated: "2026-06-20" },
    { entity_id: "DT-002", name: "Zambie — Mines de Cuivre & Aéroport Menacés", country: "Afrique Australe", sector: "Dette Chinoise 1/3 du PIB — Lusaka International Hypothéqué", composite_score: 88.25, bri_debt_ratio_score: 88.0, strategic_asset_collateral_score: 85.0, political_alignment_coercion_score: 82.0, repayment_capacity_deficit_score: 90.0, risk_level: "critique", primary_pattern: "souverainete_compromise", key_signals: ["Piège de la dette actif dans Zambie — dette BRI insoutenable convertie en concessions souveraines à Pékin", "Actifs stratégiques hypothéqués à la Chine — ports, aéroports ou ressources naturelles sous contrôle chinois", "Souveraineté de politique étrangère compromise — alignement forcé sur Pékin dans les enceintes internationales"], estimated_debt_trap_index: 8.83, last_updated: "2026-06-20" },
    { entity_id: "DT-003", name: "Pakistan — CPEC & Dépendance Structurelle", country: "Asie du Sud", sector: "Corridor Économique Chine-Pakistan — 62 Mds $ Engagés", composite_score: 85.65, bri_debt_ratio_score: 85.0, strategic_asset_collateral_score: 80.0, political_alignment_coercion_score: 88.0, repayment_capacity_deficit_score: 82.0, risk_level: "critique", primary_pattern: "dependance_infrastructurelle", key_signals: ["Piège de la dette actif dans Pakistan — dette BRI insoutenable convertie en concessions souveraines à Pékin", "Actifs stratégiques hypothéqués à la Chine — ports, aéroports ou ressources naturelles sous contrôle chinois", "Souveraineté de politique étrangère compromise — alignement forcé sur Pékin dans les enceintes internationales"], estimated_debt_trap_index: 8.57, last_updated: "2026-06-20" },
    { entity_id: "DT-004", name: "Éthiopie & Djibouti — Chemin de Fer & Port", country: "Afrique de l'Est", sector: "Chemin de Fer Addis-Djibouti et Port de Doraleh Sous Contrôle Chinois", composite_score: 81.25, bri_debt_ratio_score: 80.0, strategic_asset_collateral_score: 82.0, political_alignment_coercion_score: 78.0, repayment_capacity_deficit_score: 85.0, risk_level: "critique", primary_pattern: "dependance_infrastructurelle", key_signals: ["Piège de la dette actif dans Éthiopie & Djibouti — dette BRI insoutenable convertie en concessions souveraines à Pékin", "Actifs stratégiques hypothéqués à la Chine — ports, aéroports ou ressources naturelles sous contrôle chinois", "Souveraineté de politique étrangère compromise — alignement forcé sur Pékin dans les enceintes internationales"], estimated_debt_trap_index: 8.13, last_updated: "2026-06-20" },
    { entity_id: "DT-005", name: "Laos & Cambodge — Asie du SE Enclavée", country: "Asie du Sud-Est", sector: "Chemin de Fer Laos-Chine — 6 Mds $ pour Pays de 7 Mds PIB", composite_score: 72.85, bri_debt_ratio_score: 72.0, strategic_asset_collateral_score: 68.0, political_alignment_coercion_score: 75.0, repayment_capacity_deficit_score: 78.0, risk_level: "critique", primary_pattern: "capture_politique", key_signals: ["Piège de la dette actif dans Laos & Cambodge — dette BRI insoutenable convertie en concessions souveraines à Pékin", "Actifs stratégiques hypothéqués à la Chine — ports, aéroports ou ressources naturelles sous contrôle chinois", "Souveraineté de politique étrangère compromise — alignement forcé sur Pékin dans les enceintes internationales"], estimated_debt_trap_index: 7.29, last_updated: "2026-06-20" },
    { entity_id: "DT-006", name: "Kenya & Tanzanie — SGR Ferroviaire BRI", country: "Afrique de l'Est", sector: "Standard Gauge Railway — Ports Mombasa et Dar es Salam Exposés", composite_score: 58.75, bri_debt_ratio_score: 58.0, strategic_asset_collateral_score: 60.0, political_alignment_coercion_score: 55.0, repayment_capacity_deficit_score: 62.0, risk_level: "élevé", primary_pattern: "capture_politique", key_signals: ["Dépendance financière significative de Kenya & Tanzanie envers la Chine — BRI représentant une part critique du PIB", "Infrastructure critique financée par la Chine avec clauses de rachat opaques — risque de perte d'actifs", "Alignement politique partiel sur Pékin — pressions chinoises sur la politique étrangère du pays débiteur"], estimated_debt_trap_index: 5.88, last_updated: "2026-06-20" },
    { entity_id: "DT-007", name: "Brésil & Argentine — BRI Entrante en AL", country: "Amériques", sector: "Pénétration Croissante BRI en Amérique Latine — Soja et Lithium", composite_score: 34.1, bri_debt_ratio_score: 35.0, strategic_asset_collateral_score: 32.0, political_alignment_coercion_score: 40.0, repayment_capacity_deficit_score: 28.0, risk_level: "modéré", primary_pattern: "exposition_croissante", key_signals: ["Exposition BRI croissante dans Brésil & Argentine — projets d'infrastructure chinois sans audit suffisant des conditions", "Accumulation de dette bilatérale chinoise — ratio en hausse sans diversification des créanciers", "Risques de capture à moyen terme si la trajectoire BRI n'est pas rééquilibrée"], estimated_debt_trap_index: 3.41, last_updated: "2026-06-20" },
    { entity_id: "DT-008", name: "Inde & USA — Résistance Systémique à la BRI", country: "Global", sector: "Refus Stratégique de la BRI — Financement Alternatif PGII/IMEC", composite_score: 4.75, bri_debt_ratio_score: 5.0, strategic_asset_collateral_score: 4.0, political_alignment_coercion_score: 8.0, repayment_capacity_deficit_score: 3.0, risk_level: "faible", primary_pattern: "independance_preservee", key_signals: ["Inde & USA préserve son indépendance financière — financement diversifié et résistance aux offres BRI", "Contrats d'infrastructure transparents et refus des clauses secrètes chinoises", "Modèle de souveraineté financière — diversification active des partenaires de développement"], estimated_debt_trap_index: 0.48, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 5, "élevé": 1, "modéré": 1, faible: 1 },
    pattern_distribution: { souverainete_compromise: 2, dependance_infrastructurelle: 2, capture_politique: 2, exposition_croissante: 1, independance_preservee: 1 },
    top_risk_entities: ["Sri Lanka — Hambantota Loué 99 ans", "Zambie — Mines de Cuivre & Aéroport Menacés", "Pakistan — CPEC & Dépendance Structurelle"],
    critical_alerts: ["Sri Lanka: souveraineté compromise", "Zambie: souveraineté compromise", "Pakistan: dépendance infrastructurelle", "Éthiopie & Djibouti: dépendance infrastructurelle", "Laos & Cambodge: capture politique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "debt_trap",
    confidence_score: 0.86,
    data_sources: ["aiddata_bri_debt_tracker", "china_africa_research_initiative", "global_development_policy_center"],
    entities,
    avg_estimated_debt_trap_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
