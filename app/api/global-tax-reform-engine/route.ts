import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[global-tax-reform-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Global Tax Reform Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/global-tax-reform-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Global Tax Reform Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Global Tax Reform Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    {
      entity_id: "TX-001",
      name: "Apple Inc. — Structures Fiscales EMEA",
      country: "Irlande",
      sector: "Technologie",
      composite_score: 85.7,
      tax_haven_exposure_score: 92.0,
      profit_shifting_score: 88.0,
      treaty_abuse_score: 82.0,
      regulatory_arbitrage_score: 78.0,
      risk_level: "critique",
      primary_pattern: "Évasion Fiscale Agressive",
      key_signals: [
        "Structure 'Double Irlandais' détournant 14 Mds USD de bénéfices vers les îles Caïmans",
        "Taux effectif d'imposition de 0,005% en Irlande documenté par la Commission Européenne",
        "Utilisation de 22 entités-coquilles sans substance économique réelle",
      ],
      estimated_tax_index: 8.57,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "TX-002",
      name: "Glencore International AG",
      country: "Suisse",
      sector: "Matières Premières & Négoce",
      composite_score: 79.9,
      tax_haven_exposure_score: 85.0,
      profit_shifting_score: 82.0,
      treaty_abuse_score: 78.0,
      regulatory_arbitrage_score: 72.0,
      risk_level: "critique",
      primary_pattern: "Évasion Fiscale Agressive",
      key_signals: [
        "Prix de transfert intra-groupe exploitant 42 juridictions à fiscalité réduite",
        "Bénéfices de l'extraction minière africaine rapatriés via Guernesey et Bermudes",
        "Condamné à 1,1 Md USD d'amendes fiscales au Royaume-Uni et aux États-Unis",
      ],
      estimated_tax_index: 7.99,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "TX-003",
      name: "Amazon EU SARL — Luxembourg Division",
      country: "Luxembourg",
      sector: "Commerce & Logistique",
      composite_score: 71.9,
      tax_haven_exposure_score: 78.0,
      profit_shifting_score: 72.0,
      treaty_abuse_score: 70.0,
      regulatory_arbitrage_score: 65.0,
      risk_level: "critique",
      primary_pattern: "Évasion Fiscale Agressive",
      key_signals: [
        "Accord fiscal secret avec le Luxembourg invalidé par la Commission Européenne",
        "250 Mds EUR de ventes européennes déclarées au Luxembourg (taux IS 1,5%)",
        "Structure de redevances PI détournant les bénéfices vers le Luxembourg depuis 2003",
      ],
      estimated_tax_index: 7.19,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "TX-004",
      name: "TotalEnergies SE — Division Trading",
      country: "France",
      sector: "Énergie & Pétrochimie",
      composite_score: 61.35,
      tax_haven_exposure_score: 60.0,
      profit_shifting_score: 65.0,
      treaty_abuse_score: 62.0,
      regulatory_arbitrage_score: 58.0,
      risk_level: "élevé",
      primary_pattern: "Transfert de Bénéfices",
      key_signals: [
        "Trading pétrolier centralisé à Genève exploitant le régime fiscal helvétique",
        "Filiales en Angola et Nigeria avec taux effectif de 5% via conventions fiscales",
        "Instruments hybrides opacifiant la frontière entre dette et capitaux propres",
      ],
      estimated_tax_index: 6.14,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "TX-005",
      name: "Stellantis NV — Holding Néerlandaise",
      country: "Pays-Bas",
      sector: "Automobile",
      composite_score: 57.4,
      tax_haven_exposure_score: 55.0,
      profit_shifting_score: 60.0,
      treaty_abuse_score: 62.0,
      regulatory_arbitrage_score: 52.0,
      risk_level: "élevé",
      primary_pattern: "Abus de Conventions Fiscales",
      key_signals: [
        "Holding domicilié aux Pays-Bas exploitant le réseau de 79 conventions fiscales",
        "Redevances PI versées à une entité néerlandaise réduisant l'assiette fiscale en France",
        "Financement intra-groupe à des taux non conformes aux règles de pleine concurrence",
      ],
      estimated_tax_index: 5.74,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "TX-006",
      name: "Carrefour SA — Structures Internationales",
      country: "France",
      sector: "Distribution & Retail",
      composite_score: 30.8,
      tax_haven_exposure_score: 38.0,
      profit_shifting_score: 32.0,
      treaty_abuse_score: 28.0,
      regulatory_arbitrage_score: 22.0,
      risk_level: "modéré",
      primary_pattern: "Opacité Fiscale",
      key_signals: [
        "Optimisation fiscale via des structures de franchise dans des pays à fiscalité réduite",
        "Montages immobiliers sale-and-leaseback réduisant l'assiette imposable",
        "Reporting fiscal incomplet dans 8 pays sur 30 où le groupe opère",
      ],
      estimated_tax_index: 3.08,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "TX-007",
      name: "Danone SA — Gouvernance Fiscale",
      country: "France",
      sector: "Agroalimentaire",
      composite_score: 9.8,
      tax_haven_exposure_score: 10.0,
      profit_shifting_score: 8.0,
      treaty_abuse_score: 12.0,
      regulatory_arbitrage_score: 9.0,
      risk_level: "faible",
      primary_pattern: "Aucun",
      key_signals: [
        "Politique fiscale responsable publiée alignée sur les principes OCDE BEPS",
        "Taux effectif d'imposition de 26% conforme aux taux nominaux des pays d'opération",
        "Rapport pays par pays volontairement publié avec données de substance économique",
      ],
      estimated_tax_index: 0.98,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "TX-008",
      name: "IKEA Foundation — Structures Suédoises",
      country: "Suède",
      sector: "Ameublement & Retail",
      composite_score: 11.3,
      tax_haven_exposure_score: 14.0,
      profit_shifting_score: 12.0,
      treaty_abuse_score: 10.0,
      regulatory_arbitrage_score: 8.0,
      risk_level: "faible",
      primary_pattern: "Aucun",
      key_signals: [
        "Réforme de la structure fondation garantissant la conformité fiscale européenne",
        "Engagement public d'alignement sur la directive Pilier 2 OCDE dès 2024",
        "Audit fiscal externe indépendant publié annuellement par cabinet Big 4 distinct",
      ],
      estimated_tax_index: 1.13,
      last_updated: "2026-06-20",
    },
  ];

  const summary = {
    total_entities: 8,
    avg_composite: 51.02,
    risk_distribution: { critique: 3, "élevé": 2, "modéré": 1, faible: 2 },
    pattern_distribution: {
      "Évasion Fiscale Agressive": 3,
      "Transfert de Bénéfices": 3,
      "Abus de Conventions Fiscales": 3,
      "Arbitrage Réglementaire": 2,
      "Opacité Fiscale": 5,
    },
    top_risk_entities: [
      "Apple Inc. — Structures Fiscales EMEA",
      "Glencore International AG",
      "Amazon EU SARL — Luxembourg Division",
    ],
    critical_alerts: [
      "ALERTE CRITIQUE: Apple Inc. — Structures Fiscales EMEA (Irlande) — score fiscal 85.70/100",
      "ALERTE CRITIQUE: Glencore International AG (Suisse) — score fiscal 79.90/100",
      "ALERTE CRITIQUE: Amazon EU SARL — Luxembourg Division (Luxembourg) — score fiscal 71.90/100",
    ],
    last_analysis: "2026-06-20T00:00:00Z",
    engine_version: "1.0.0",
    domain: "tax",
    confidence_score: 91.0,
    data_sources: [
      "OCDE BEPS Action Plan Database",
      "EU Tax Observatory Multinational Reports",
      "Tax Justice Network Financial Secrecy Index",
      "ICIJ OffshoreLeaks & Luxembourg Leaks Database",
    ],
    entities,
    avg_estimated_tax_index: 5.1,
  };

  return { entities, summary };
}
