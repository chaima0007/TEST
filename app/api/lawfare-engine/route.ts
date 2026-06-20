import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[lawfare-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Lawfare Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/lawfare-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Lawfare Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Lawfare Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "LW-001", name: "USA — FCPA, OFAC & Extraterritorialité Judiciaire Mondiale", country: "Amérique du Nord", sector: "FCPA BNP 8.9Md$/Alstom 772M$/Airbus 3.9Md$, OFAC Mondial & Juridiction Universelle DOJ", composite_score: 87.65, international_court_manipulation_score: 88.0, sanctions_legal_weaponization_score: 82.0, extraterritoriality_abuse_score: 95.0, treaty_weaponization_score: 85.0, risk_level: "critique", primary_pattern: "extraterritorialite_hegemonique", key_signals: ["Lawfare systémique de USA — instrumentalisation active du droit international comme arme de pression géopolitique", "Weaponisation judiciaire — manipulation des cours internationales, extraterritorialité abusive et pièges de traités d'investissement", "Érosion de l'ordre juridique international — asymétrie délibérée entre puissants capables d'imposer leur droit et États soumis à ses effets"], estimated_lawfare_index: 8.77, last_updated: "2026-06-20" },
    { entity_id: "LW-002", name: "Russie — Veto CSNU & Procédures CIJ Détournées", country: "Europe de l'Est", sector: "50+ Vetos CSNU 2011-2024, CIJ Affaire Ukraine Blockage & Réclusions Arbitrales Sélectives", composite_score: 83.75, international_court_manipulation_score: 90.0, sanctions_legal_weaponization_score: 85.0, extraterritoriality_abuse_score: 78.0, treaty_weaponization_score: 80.0, risk_level: "critique", primary_pattern: "lawfare_systemique", key_signals: ["Lawfare systémique de Russie — instrumentalisation active du droit international comme arme de pression géopolitique", "Weaponisation judiciaire — manipulation des cours internationales, extraterritorialité abusive et pièges de traités d'investissement", "Érosion de l'ordre juridique international — asymétrie délibérée entre puissants capables d'imposer leur droit et États soumis à ses effets"], estimated_lawfare_index: 8.38, last_updated: "2026-06-20" },
    { entity_id: "LW-003", name: "Chine — Rejet La Haye & Arbitrage BRI Alternatif", country: "Asie", sector: "Rejet CPA 2016 Mer Chine Sud, Tribunaux BRI Alternatifs & ISDS Asymétrique Partenaires", composite_score: 81.85, international_court_manipulation_score: 85.0, sanctions_legal_weaponization_score: 80.0, extraterritoriality_abuse_score: 75.0, treaty_weaponization_score: 88.0, risk_level: "critique", primary_pattern: "pieges_traites", key_signals: ["Lawfare systémique de Chine — instrumentalisation active du droit international comme arme de pression géopolitique", "Weaponisation judiciaire — manipulation des cours internationales, extraterritorialité abusive et pièges de traités d'investissement", "Érosion de l'ordre juridique international — asymétrie délibérée entre puissants capables d'imposer leur droit et États soumis à ses effets"], estimated_lawfare_index: 8.19, last_updated: "2026-06-20" },
    { entity_id: "LW-004", name: "Israël & Hamas — Guerre Juridique Gaza CIJ/CPI", country: "MENA", sector: "Procédures CIJ Génocide Afrique du Sud, Mandat CPI Netanyahu & Contre-Lawfare Légitimité", composite_score: 78.5, international_court_manipulation_score: 82.0, sanctions_legal_weaponization_score: 78.0, extraterritoriality_abuse_score: 80.0, treaty_weaponization_score: 72.0, risk_level: "critique", primary_pattern: "manœuvres_juridiques_offensives", key_signals: ["Lawfare systémique de Israël & Hamas — instrumentalisation active du droit international comme arme de pression géopolitique", "Weaponisation judiciaire — manipulation des cours internationales, extraterritorialité abusive et pièges de traités d'investissement", "Érosion de l'ordre juridique international — asymétrie délibérée entre puissants capables d'imposer leur droit et États soumis à ses effets"], estimated_lawfare_index: 7.85, last_updated: "2026-06-20" },
    { entity_id: "LW-005", name: "Turquie & Hongrie — Vetos Juridiques OTAN/UE", country: "MENA/Europe", sector: "Veto Adhésion Suède OTAN, Blocages Fonds UE Hongrois & Violation État de Droit Documentée", composite_score: 53.55, international_court_manipulation_score: 58.0, sanctions_legal_weaponization_score: 55.0, extraterritoriality_abuse_score: 48.0, treaty_weaponization_score: 52.0, risk_level: "élevé", primary_pattern: "manœuvres_juridiques_offensives", key_signals: ["Manœuvres juridiques offensives de Turquie & Hongrie — utilisation des procédures internationales à fins géopolitiques", "Forum shopping agressif — sélection opportuniste des juridictions les plus favorables pour maximiser l'effet de pression", "Contre-droit comme stratégie — création de normes alternatives et contestation des mécanismes universels de règlement des différends"], estimated_lawfare_index: 5.36, last_updated: "2026-06-20" },
    { entity_id: "LW-006", name: "Qatar & EAU — Arbitrage ISDS & Lobbying Juridique", country: "MENA", sector: "700+ Traités BIT, Arbitrages CIRDI Offensifs & Sports/Cultura Soft Power via Droit", composite_score: 52.95, international_court_manipulation_score: 52.0, sanctions_legal_weaponization_score: 48.0, extraterritoriality_abuse_score: 55.0, treaty_weaponization_score: 58.0, risk_level: "élevé", primary_pattern: "manœuvres_juridiques_offensives", key_signals: ["Manœuvres juridiques offensives de Qatar & EAU — utilisation des procédures internationales à fins géopolitiques", "Forum shopping agressif — sélection opportuniste des juridictions les plus favorables pour maximiser l'effet de pression", "Contre-droit comme stratégie — création de normes alternatives et contestation des mécanismes universels de règlement des différends"], estimated_lawfare_index: 5.3, last_updated: "2026-06-20" },
    { entity_id: "LW-007", name: "UE — Forum Shopping & Fragmentation Normative", country: "Europe", sector: "RGPD Extraterritorialité Limitée, DSA/DMA Régulation & Tensions Juridictions USA/UE Tech", composite_score: 30.15, international_court_manipulation_score: 28.0, sanctions_legal_weaponization_score: 32.0, extraterritoriality_abuse_score: 35.0, treaty_weaponization_score: 25.0, risk_level: "modéré", primary_pattern: "manœuvres_juridiques_offensives", key_signals: ["Forum shopping de UE — exploitation des lacunes juridictionnelles sans stratégie lawfare cohérente", "Fragmentation normative — multiplication des règles spéciales au détriment de la cohérence du droit international", "Déficit de capacités juridiques — exposition aux procédures adversaires faute de ressources contentieuses suffisantes"], estimated_lawfare_index: 3.02, last_updated: "2026-06-20" },
    { entity_id: "LW-008", name: "CIJ & CPA — Gouvernance Juridique Internationale", country: "Global", sector: "CIJ 15 Juges, CPA 157 États Parties & Cour Pénale Internationale 124 États Membres", composite_score: 4.45, international_court_manipulation_score: 5.0, sanctions_legal_weaponization_score: 4.0, extraterritoriality_abuse_score: 3.0, treaty_weaponization_score: 6.0, risk_level: "faible", primary_pattern: "etat_de_droit_cooperatif", key_signals: ["CIJ & CPA incarne l'état de droit coopératif — contribution sincère aux institutions juridiques internationales et respect des décisions", "Règlement pacifique des différends — recours aux mécanismes de médiation, arbitrage et juridictions multilatérales de bonne foi", "Modèle de coopération juridique à diffuser — financement des cours internationales et formation au droit international pour les États vulnérables"], estimated_lawfare_index: 0.45, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { lawfare_systemique: 1, extraterritorialite_hegemonique: 1, pieges_traites: 1, "manœuvres_juridiques_offensives": 4, etat_de_droit_cooperatif: 1 },
    top_risk_entities: ["USA — FCPA, OFAC & Extraterritorialité Judiciaire Mondiale", "Russie — Veto CSNU & Procédures CIJ Détournées", "Chine — Rejet La Haye & Arbitrage BRI Alternatif"],
    critical_alerts: ["USA: extraterritorialité hégémonique", "Russie: lawfare systémique", "Chine: pièges traités", "Israël & Hamas: manœuvres juridiques offensives"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "lawfare",
    confidence_score: 0.80,
    data_sources: ["icc_international_criminal_court_monitor", "pcacases_arbitration_tracker", "us_doj_fcpa_resource_guide"],
    entities,
    avg_estimated_lawfare_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
