import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[dark-patterns-engine] SWARM_API_URL non défini — mode mock activé");
}

function getMockData() {
  const entities = [
    {
      entity_id: "DKP-001",
      name: "DarkClick Media",
      country: "USA",
      sector: "Publicité Numérique",
      composite_score: 86.65,
      manipulation_score: 90.0,
      consent_violation_score: 88.0,
      financial_harm_score: 85.0,
      regulatory_risk_score: 82.0,
      risk_level: "critique",
      primary_pattern: "Manipulation Consentement Forcé",
      key_signals: [
        "Opt-out impossible conçu délibérément",
        "Publicités déguisées en contenu éditorial",
        "Données vendues 47 courtiers sans consentement",
      ],
      estimated_darkpattern_index: 8.67,
      recommended_action: "Mise en demeure CNIL/DPA immédiate et audit UX obligatoire",
      last_updated: "2026-06-20",
    },
    {
      entity_id: "DKP-002",
      name: "SubTrap Platform",
      country: "Irlande",
      sector: "SaaS & Abonnements",
      composite_score: 83.1,
      manipulation_score: 85.0,
      consent_violation_score: 80.0,
      financial_harm_score: 88.0,
      regulatory_risk_score: 78.0,
      risk_level: "critique",
      primary_pattern: "Piège Abonnement Caché",
      key_signals: [
        "Renouvellement auto sans alerte",
        "Annulation 17 étapes requises",
        "Frais cachés découverts post-souscription",
      ],
      estimated_darkpattern_index: 8.31,
      recommended_action: "Remboursement automatique utilisateurs et rectification interface",
      last_updated: "2026-06-20",
    },
    {
      entity_id: "DKP-003",
      name: "ConfirmShame App",
      country: "Royaume-Uni",
      sector: "Applications Mobile",
      composite_score: 79.1,
      manipulation_score: 82.0,
      consent_violation_score: 78.0,
      financial_harm_score: 80.0,
      regulatory_risk_score: 75.0,
      risk_level: "critique",
      primary_pattern: "Déceptivité Interface Systémique",
      key_signals: [
        "Bouton refus labellisé négativement",
        "Interface de désabonnement introuvable",
        "Pop-up consentement pré-coché systématique",
      ],
      estimated_darkpattern_index: 7.91,
      recommended_action: "Redesign UX supervisé par autorité régulation numérique",
      last_updated: "2026-06-20",
    },
    {
      entity_id: "DKP-004",
      name: "HiddenFee Commerce",
      country: "Allemagne",
      sector: "E-commerce",
      composite_score: 54.0,
      manipulation_score: 55.0,
      consent_violation_score: 52.0,
      financial_harm_score: 58.0,
      regulatory_risk_score: 50.0,
      risk_level: "élevé",
      primary_pattern: "Violation DSA Répétée",
      key_signals: [
        "Frais livraison ajoutés au checkout",
        "Prix barré fictif systématique",
        "Injonction DSA reçue mars 2026",
      ],
      estimated_darkpattern_index: 5.4,
      recommended_action: "Plan de conformité DSA accéléré avec deadline 90 jours",
      last_updated: "2026-06-20",
    },
    {
      entity_id: "DKP-005",
      name: "DataHarvest Social",
      country: "Luxembourg",
      sector: "Réseaux Sociaux",
      composite_score: 51.75,
      manipulation_score: 50.0,
      consent_violation_score: 58.0,
      financial_harm_score: 45.0,
      regulatory_risk_score: 55.0,
      risk_level: "élevé",
      primary_pattern: "Monétisation Données Occulte",
      key_signals: [
        "Paramètres vie privée enfouis",
        "Consentement bundlé illégalement",
        "Revente données santé non déclarée",
      ],
      estimated_darkpattern_index: 5.18,
      recommended_action: "Transparence politique de données et opt-out simplifié",
      last_updated: "2026-06-20",
    },
    {
      entity_id: "DKP-006",
      name: "GrayUX Solutions",
      country: "France",
      sector: "Design UX/UI",
      composite_score: 39.1,
      manipulation_score: 42.0,
      consent_violation_score: 38.0,
      financial_harm_score: 40.0,
      regulatory_risk_score: 35.0,
      risk_level: "modéré",
      primary_pattern: "Monétisation Données Occulte",
      key_signals: [
        "Patterns ambigus partiellement corrigés",
        "CNIL en dialogue",
        "Conformité RGPD en cours",
      ],
      estimated_darkpattern_index: 3.91,
      recommended_action: "Transparence politique de données et opt-out simplifié",
      last_updated: "2026-06-20",
    },
    {
      entity_id: "DKP-007",
      name: "EthicalUX Collective",
      country: "Suède",
      sector: "Design Éthique",
      composite_score: 8.8,
      manipulation_score: 8.0,
      consent_violation_score: 10.0,
      financial_harm_score: 6.0,
      regulatory_risk_score: 12.0,
      risk_level: "faible",
      primary_pattern: "Violation DSA Répétée",
      key_signals: [
        "Certifié conforme DSA",
        "Interface transparence primée",
        "Open source patterns éthiques",
      ],
      estimated_darkpattern_index: 0.88,
      recommended_action: "Plan de conformité DSA accéléré avec deadline 90 jours",
      last_updated: "2026-06-20",
    },
    {
      entity_id: "DKP-008",
      name: "TrustFirst Digital",
      country: "Danemark",
      sector: "Services Numériques",
      composite_score: 7.05,
      manipulation_score: 6.0,
      consent_violation_score: 8.0,
      financial_harm_score: 5.0,
      regulatory_risk_score: 10.0,
      risk_level: "faible",
      primary_pattern: "Piège Abonnement Caché",
      key_signals: [
        "Annulation en un clic",
        "Alerte renouvellement J-30",
        "Prix tout inclus garantis",
      ],
      estimated_darkpattern_index: 0.71,
      recommended_action: "Remboursement automatique utilisateurs et rectification interface",
      last_updated: "2026-06-20",
    },
  ];

  const summary = {
    total_entities: 8,
    avg_composite: 51.19,
    risk_distribution: {
      critique: 3,
      élevé: 2,
      modéré: 1,
      faible: 2,
    },
    pattern_distribution: {
      "Manipulation Consentement Forcé": 1,
      "Piège Abonnement Caché": 2,
      "Déceptivité Interface Systémique": 1,
      "Violation DSA Répétée": 2,
      "Monétisation Données Occulte": 2,
    },
    top_risk_entities: ["DarkClick Media", "SubTrap Platform", "ConfirmShame App"],
    critical_alerts: 3,
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "darkpattern",
    confidence_score: 0.91,
    data_sources: [
      "DSA Compliance Reports",
      "CNIL/DPA Enforcement Database",
      "UX Audit Intelligence Feed",
      "GDPR Violation Registry",
      "Consumer Protection Agency Data",
    ],
    entities,
    avg_estimated_darkpattern_index: 5.12,
  };

  return { entities, summary };
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Dark Patterns Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/dark-patterns-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Dark Patterns Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Dark Patterns Agent"), { status: 502 });
  }
}
