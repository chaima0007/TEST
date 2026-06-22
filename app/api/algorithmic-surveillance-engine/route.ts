import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[algorithmic-surveillance-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Algorithmic Surveillance Engine Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/algorithmic-surveillance-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Algorithmic Surveillance Engine Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Algorithmic Surveillance Engine Agent"), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    { id: "AS-001", name: "Chine — État de Surveillance Totale", country: "Asie", sector: "Crédit Social, Xinjiang & Export Technologie Surveillance Autoritaire", composite_score: 93.65, biometric_surveillance_score: 98.0, social_scoring_score: 95.0, mass_metadata_collection_score: 90.0, civil_liberties_erosion_score: 92.0, risk_level: "critique", primary_pattern: "totalitarisme_numerique", key_signals: ["Surveillance algorithmique de masse dans Chine — État de Surveillance Totale — contrôle numérique total des populations", "Reconnaissance faciale omniprésente — chaque mouvement dans l'espace public tracé et analysé en temps réel", "Libertés civiles numériques érodées — dissidence, association et expression sous surveillance constante"], estimated_surveillance_index: 9.37, last_updated: "2026-06-20" },
    { id: "AS-002", name: "Corée du Nord — Surveillance Analogique Totale", country: "Asie", sector: "Contrôle Total Non-Numérique mais Intégration Technologie Chinoise", composite_score: 83.4, biometric_surveillance_score: 80.0, social_scoring_score: 88.0, mass_metadata_collection_score: 72.0, civil_liberties_erosion_score: 92.0, risk_level: "critique", primary_pattern: "export_technologie_surveillance", key_signals: ["Surveillance algorithmique de masse dans Corée du Nord — Surveillance Analogique Totale — contrôle numérique total des populations", "Reconnaissance faciale omniprésente — chaque mouvement dans l'espace public tracé et analysé en temps réel", "Libertés civiles numériques érodées — dissidence, association et expression sous surveillance constante"], estimated_surveillance_index: 8.34, last_updated: "2026-06-20" },
    { id: "AS-003", name: "Russie — SORM & Surveillance FSB", country: "Europe de l'Est", sector: "SORM-3 Surveillance Totale Télécoms & Reconnaissance Faciale Moscou", composite_score: 83.9, biometric_surveillance_score: 85.0, social_scoring_score: 78.0, mass_metadata_collection_score: 88.0, civil_liberties_erosion_score: 82.0, risk_level: "critique", primary_pattern: "totalitarisme_numerique", key_signals: ["Surveillance algorithmique de masse dans Russie — SORM & Surveillance FSB — contrôle numérique total des populations", "Reconnaissance faciale omniprésente — chaque mouvement dans l'espace public tracé et analysé en temps réel", "Libertés civiles numériques érodées — dissidence, association et expression sous surveillance constante"], estimated_surveillance_index: 8.39, last_updated: "2026-06-20" },
    { id: "AS-004", name: "Iran — État de Surveillance Islamique", country: "MENA", sector: "Surveillance Numérique des Opposants & Contrôle VPN & Réseaux Sociaux", composite_score: 79.25, biometric_surveillance_score: 78.0, social_scoring_score: 80.0, mass_metadata_collection_score: 75.0, civil_liberties_erosion_score: 85.0, risk_level: "critique", primary_pattern: "export_technologie_surveillance", key_signals: ["Surveillance algorithmique de masse dans Iran — État de Surveillance Islamique — contrôle numérique total des populations", "Reconnaissance faciale omniprésente — chaque mouvement dans l'espace public tracé et analysé en temps réel", "Libertés civiles numériques érodées — dissidence, association et expression sous surveillance constante"], estimated_surveillance_index: 7.93, last_updated: "2026-06-20" },
    { id: "AS-005", name: "USA — PRISM & Surveillance Globale NSA", country: "Amérique du Nord", sector: "XKeyscore, PRISM & Palantir — Surveillance Sécuritaire sans Garanties", composite_score: 52.9, biometric_surveillance_score: 50.0, social_scoring_score: 38.0, mass_metadata_collection_score: 72.0, civil_liberties_erosion_score: 52.0, risk_level: "élevé", primary_pattern: "surveillance_securitaire_excessive", key_signals: ["Surveillance avancée dans USA — PRISM & Surveillance Globale NSA — systèmes de collecte massive de données sans garanties suffisantes", "Programmes de surveillance sécuritaire dépassant les limites légales et les droits fondamentaux", "Risque de dérive autoritaire — technologies de surveillance sans supervision judiciaire indépendante"], estimated_surveillance_index: 5.29, last_updated: "2026-06-20" },
    { id: "AS-006", name: "Inde — Aadhaar & NATGRID", country: "Asie du Sud", sector: "Base Biométrique 1.4Mds Citoyens & Système de Surveillance NATGRID", composite_score: 49.6, biometric_surveillance_score: 55.0, social_scoring_score: 42.0, mass_metadata_collection_score: 52.0, civil_liberties_erosion_score: 48.0, risk_level: "élevé", primary_pattern: "surveillance_securitaire_excessive", key_signals: ["Surveillance avancée dans Inde — Aadhaar & NATGRID — systèmes de collecte massive de données sans garanties suffisantes", "Programmes de surveillance sécuritaire dépassant les limites légales et les droits fondamentaux", "Risque de dérive autoritaire — technologies de surveillance sans supervision judiciaire indépendante"], estimated_surveillance_index: 4.96, last_updated: "2026-06-20" },
    { id: "AS-007", name: "Europe — RGPD vs Surveillance Commerciale", country: "Europe", sector: "RGPD Insuffisant face aux GAFAM & Surveillance Commerciale Légale", composite_score: 34.75, biometric_surveillance_score: 35.0, social_scoring_score: 20.0, mass_metadata_collection_score: 55.0, civil_liberties_erosion_score: 38.0, risk_level: "modéré", primary_pattern: "derive_commerciale", key_signals: ["Surveillance partielle dans Europe — RGPD vs Surveillance Commerciale — collecte de données sans encadrement légal suffisant", "Plateformes commerciales collectant des biométriques sans consentement éclairé et supervision", "Risque de normalisation — technologies de surveillance tolérées sans débat démocratique"], estimated_surveillance_index: 3.48, last_updated: "2026-06-20" },
    { id: "AS-008", name: "Islande & Estonie — Démocraties Numériques", country: "Europe du Nord", sector: "e-Résidence, Données Chiffrées & Cadre Légal Anti-Surveillance Exemplaire", composite_score: 8.15, biometric_surveillance_score: 8.0, social_scoring_score: 5.0, mass_metadata_collection_score: 12.0, civil_liberties_erosion_score: 6.0, risk_level: "faible", primary_pattern: "cadre_protecteur", key_signals: ["Islande & Estonie — Démocraties Numériques maintient un cadre protecteur contre la surveillance algorithmique excessive", "Régulation stricte de la biométrie et droits numériques effectifs pour les citoyens", "Modèle de gouvernance algorithmique à partager — transparence, contrôle citoyen et supervision judiciaire"], estimated_surveillance_index: 0.82, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { totalitarisme_numerique: 2, export_technologie_surveillance: 2, surveillance_securitaire_excessive: 2, derive_commerciale: 1, cadre_protecteur: 1 },
    top_risk_entities: ["Chine — État de Surveillance Totale", "Russie — SORM & Surveillance FSB", "Corée du Nord — Surveillance Analogique Totale"],
    critical_alerts: ["Chine: totalitarisme numérique", "Corée du Nord: export technologie surveillance", "Russie: totalitarisme numérique", "Iran: export technologie surveillance"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "algorithmic_surveillance",
    confidence_score: 0.84,
    data_sources: ["carnegie_ai_global_surveillance_index", "citizen_lab_surveillance_tracker", "access_now_digital_rights_monitor"],
    entities,
    avg_estimated_surveillance_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
