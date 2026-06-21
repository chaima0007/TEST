import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[economic-coercion-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Economic Coercion Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/economic-coercion-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Economic Coercion Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Economic Coercion Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "EC-001", name: "Taiwan & Détroit de Formose", country: "Asie-Pacifique", sector: "Semi-conducteurs & Technologie", composite_score: 87.0, dependency_concentration_score: 92.0, sanction_exposure_score: 85.0, financial_chokepoint_score: 88.0, trade_weaponization_score: 80.0, risk_level: "critique", primary_pattern: "guerre_economique_totale", key_signals: ["Coercition économique critique — dépendances stratégiques en semi-conducteurs exploitées", "Exposition maximale aux sanctions et points de contrôle financier", "Weaponisation du commerce détectée — autonomie économique sous menace"], estimated_coercion_index: 8.70, last_updated: "2026-06-20" },
    { id: "EC-002", name: "Europe (Dépendance Énergétique)", country: "Europe", sector: "Énergie & Ressources", composite_score: 80.75, dependency_concentration_score: 85.0, sanction_exposure_score: 78.0, financial_chokepoint_score: 82.0, trade_weaponization_score: 75.0, risk_level: "critique", primary_pattern: "chantage_strategique", key_signals: ["Chantage stratégique via dépendance énergétique russe/GNL", "Concentration excessive créant des leviers de pression géopolitiques", "Diversification énergétique en cours mais vulnérabilité résiduelle critique"], estimated_coercion_index: 8.08, last_updated: "2026-06-20" },
    { id: "EC-003", name: "Pays Africains (Piège de Dette)", country: "Afrique", sector: "Infrastructure & Finance", composite_score: 74.5, dependency_concentration_score: 80.0, sanction_exposure_score: 72.0, financial_chokepoint_score: 68.0, trade_weaponization_score: 78.0, risk_level: "critique", primary_pattern: "chantage_strategique", key_signals: ["Trap diplomatique via dettes d'infrastructure — levier coercitif détecté", "Dépendance aux créanciers bilatéraux compromettant la souveraineté", "Concentration commerciale excessive sur un seul partenaire"], estimated_coercion_index: 7.45, last_updated: "2026-06-20" },
    { id: "EC-004", name: "Corée du Sud & Japon", country: "Asie du Nord-Est", sector: "High-Tech & Chaînes Valeur", composite_score: 67.25, dependency_concentration_score: 70.0, sanction_exposure_score: 65.0, financial_chokepoint_score: 72.0, trade_weaponization_score: 62.0, risk_level: "critique", primary_pattern: "pression_economique_ciblee", key_signals: ["Pression coercitive élevée — chaînes de valeur exposées", "Dépendances technologiques critiques aux semi-conducteurs et terres rares", "Risque de chantage stratégique par acteur régional dominant"], estimated_coercion_index: 6.73, last_updated: "2026-06-20" },
    { id: "EC-005", name: "Amérique Latine (Dollar Trap)", country: "Amériques", sector: "Finance & Commodités", composite_score: 59.25, dependency_concentration_score: 60.0, sanction_exposure_score: 58.0, financial_chokepoint_score: 65.0, trade_weaponization_score: 52.0, risk_level: "élevé", primary_pattern: "pression_economique_ciblee", key_signals: ["Vulnérabilité élevée — dollar dependency et sanctions secondaires", "Exposition aux chokeppoints financiers SWIFT et USD clearing", "Risque de coercition via accès aux marchés financiers internationaux"], estimated_coercion_index: 5.93, last_updated: "2026-06-20" },
    { id: "EC-006", name: "Inde & Asie du Sud-Est", country: "Asie", sector: "Diversification Stratégique", composite_score: 38.75, dependency_concentration_score: 42.0, sanction_exposure_score: 38.0, financial_chokepoint_score: 40.0, trade_weaponization_score: 35.0, risk_level: "modéré", primary_pattern: "vulnerabilite_commerciale", key_signals: ["Vulnérabilité commerciale modérée — politique de multi-alignement protectrice", "Diversification active des partenaires — résilience en construction", "Dépendances sectorielles résiduelles à surveiller"], estimated_coercion_index: 3.88, last_updated: "2026-06-20" },
    { id: "EC-007", name: "États-Unis & Canada", country: "Amérique du Nord", sector: "Autonomie Économique", composite_score: 23.75, dependency_concentration_score: 25.0, sanction_exposure_score: 22.0, financial_chokepoint_score: 28.0, trade_weaponization_score: 20.0, risk_level: "modéré", primary_pattern: "vulnerabilite_commerciale", key_signals: ["Coercibilité modérée — contrôle des chokeppoints financiers mondiaux", "Dépendances en terres rares et semi-conducteurs asiatiques à surveiller", "Position de force sur les marchés mondiaux — vulnérabilité limitée"], estimated_coercion_index: 2.38, last_updated: "2026-06-20" },
    { id: "EC-008", name: "Suisse & Nordiques", country: "Europe du Nord", sector: "Neutralité & Résilience", composite_score: 11.25, dependency_concentration_score: 12.0, sanction_exposure_score: 8.0, financial_chokepoint_score: 15.0, trade_weaponization_score: 10.0, risk_level: "faible", primary_pattern: "resilience_economique", key_signals: ["Résilience économique exemplaire — neutralité et diversification maximale", "Exposition minimale aux leviers coercitifs externes", "Capital diplomatique protecteur — veille coercitive maintenue"], estimated_coercion_index: 1.13, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 1, "modéré": 2, faible: 1 },
    pattern_distribution: { guerre_economique_totale: 1, chantage_strategique: 2, pression_economique_ciblee: 2, vulnerabilite_commerciale: 2, resilience_economique: 1 },
    top_risk_entities: ["Taiwan & Détroit de Formose", "Europe (Dépendance Énergétique)", "Pays Africains (Piège de Dette)"],
    critical_alerts: ["Taiwan: guerre économique totale", "Europe: chantage stratégique énergétique", "Afrique: piège de dette diplomatique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "coercion",
    confidence_score: 0.84,
    data_sources: ["trade_dependency_index", "sanctions_tracker", "financial_chokepoints_monitor"],
    entities,
    avg_estimated_coercion_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
