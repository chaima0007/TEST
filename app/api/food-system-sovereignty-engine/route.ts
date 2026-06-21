import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[food-system-sovereignty-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Food System Sovereignty Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/food-system-sovereignty-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Food System Sovereignty Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Food System Sovereignty Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    {
      id: "FS-001",
      name: "Bayer-Monsanto Agro Division",
      country: "États-Unis",
      sector: "Agrochimie & Semences",
      composite_score: 83.75,
      corporate_monopoly_score: 88.0,
      seed_patent_control_score: 85.0,
      import_dependency_score: 82.0,
      smallholder_displacement_score: 78.0,
      risk_level: "critique",
      primary_pattern: "Monopole Alimentaire",
      key_signals: [
        "Contrôle de 62% du marché mondial des semences OGM brevetées",
        "Contrats de licence imposant des restrictions sévères aux agriculteurs",
        "Rachat de 14 entreprises semencières indépendantes en 5 ans",
      ],
      estimated_food_index: 8.38,
      last_updated: "2026-06-20",
    },
    {
      id: "FS-002",
      name: "Cargill Global Food Systems",
      country: "États-Unis",
      sector: "Négoce Alimentaire",
      composite_score: 78.35,
      corporate_monopoly_score: 84.0,
      seed_patent_control_score: 79.0,
      import_dependency_score: 76.0,
      smallholder_displacement_score: 72.0,
      risk_level: "critique",
      primary_pattern: "Monopole Alimentaire",
      key_signals: [
        "Contrôle de 25% du commerce mondial des céréales et oléagineux",
        "Accaparement foncier de 2,3 millions d'hectares en Amérique du Sud",
        "Dépendance créée via des contrats d'intégration verticale pour 800 000 producteurs",
      ],
      estimated_food_index: 7.84,
      last_updated: "2026-06-20",
    },
    {
      id: "FS-003",
      name: "Gouvernement du Yémen — Sécurité Alimentaire",
      country: "Yémen",
      sector: "Souveraineté Alimentaire Nationale",
      composite_score: 70.8,
      corporate_monopoly_score: 76.0,
      seed_patent_control_score: 72.0,
      import_dependency_score: 68.0,
      smallholder_displacement_score: 65.0,
      risk_level: "critique",
      primary_pattern: "Monopole Alimentaire",
      key_signals: [
        "Dépendance à 90% des importations alimentaires pour nourrir la population",
        "Destruction de 78% des capacités agricoles locales par le conflit",
        "Famine touchant 21 millions de personnes sur 30 millions d'habitants",
      ],
      estimated_food_index: 7.08,
      last_updated: "2026-06-20",
    },
    {
      id: "FS-004",
      name: "Système Alimentaire Éthiopien",
      country: "Éthiopie",
      sector: "Souveraineté Alimentaire Nationale",
      composite_score: 60.85,
      corporate_monopoly_score: 60.0,
      seed_patent_control_score: 62.0,
      import_dependency_score: 63.0,
      smallholder_displacement_score: 58.0,
      risk_level: "élevé",
      primary_pattern: "Fragilité Systémique",
      key_signals: [
        "Privatisation des terres agricoles au profit d'investisseurs étrangers",
        "Introduction forcée de variétés hybrides remplaçant les semences traditionnelles",
        "Subventions agricoles favorisant les exportateurs au détriment des paysans locaux",
      ],
      estimated_food_index: 6.09,
      last_updated: "2026-06-20",
    },
    {
      id: "FS-005",
      name: "Chaîne Alimentaire des Philippines",
      country: "Philippines",
      sector: "Souveraineté Alimentaire Nationale",
      composite_score: 56.5,
      corporate_monopoly_score: 55.0,
      seed_patent_control_score: 58.0,
      import_dependency_score: 62.0,
      smallholder_displacement_score: 50.0,
      risk_level: "élevé",
      primary_pattern: "Fragilité Systémique",
      key_signals: [
        "Import de riz représentant 15% de la consommation nationale malgré terres agricoles",
        "Concentration de la distribution alimentaire dans 3 conglomérats familiaux",
        "Programme de semences OGM imposé par conditionnalité des prêts internationaux",
      ],
      estimated_food_index: 5.65,
      last_updated: "2026-06-20",
    },
    {
      id: "FS-006",
      name: "Secteur Agricole du Maroc",
      country: "Maroc",
      sector: "Souveraineté Alimentaire Nationale",
      composite_score: 31.2,
      corporate_monopoly_score: 38.0,
      seed_patent_control_score: 32.0,
      import_dependency_score: 28.0,
      smallholder_displacement_score: 24.0,
      risk_level: "modéré",
      primary_pattern: "Fragilité Systémique",
      key_signals: [
        "Dépendance croissante aux importations de blé tendre (35% de la consommation)",
        "Pression foncière sur les petits agriculteurs dans les zones d'agri-business",
        "Adoption progressive de semences certifiées limitant la reproduction paysanne",
      ],
      estimated_food_index: 3.12,
      last_updated: "2026-06-20",
    },
    {
      id: "FS-007",
      name: "Système Alimentaire Français",
      country: "France",
      sector: "Souveraineté Alimentaire Nationale",
      composite_score: 9.8,
      corporate_monopoly_score: 10.0,
      seed_patent_control_score: 8.0,
      import_dependency_score: 12.0,
      smallholder_displacement_score: 9.0,
      risk_level: "faible",
      primary_pattern: "Aucun",
      key_signals: [
        "Politique agricole commune garantissant la diversité des exploitations",
        "Banques de semences nationales préservant 12 000 variétés locales",
        "Taux d'autosuffisance alimentaire supérieur à 70% pour les denrées de base",
      ],
      estimated_food_index: 0.98,
      last_updated: "2026-06-20",
    },
    {
      id: "FS-008",
      name: "Système Alimentaire Uruguayen",
      country: "Uruguay",
      sector: "Souveraineté Alimentaire Nationale",
      composite_score: 11.05,
      corporate_monopoly_score: 14.0,
      seed_patent_control_score: 11.0,
      import_dependency_score: 10.0,
      smallholder_displacement_score: 8.0,
      risk_level: "faible",
      primary_pattern: "Aucun",
      key_signals: [
        "Loi sur la souveraineté semencière garantissant les droits des agriculteurs",
        "Diversification des cultures préservant 80% de la surface en production locale",
        "Coopératives agricoles contrôlant 45% de la transformation alimentaire nationale",
      ],
      estimated_food_index: 1.11,
      last_updated: "2026-06-20",
    },
  ];

  const summary = {
    total_entities: 8,
    avg_composite: 50.29,
    risk_distribution: { critique: 3, "élevé": 2, "modéré": 1, faible: 2 },
    pattern_distribution: {
      "Monopole Alimentaire": 3,
      "Brevetage Semencier": 3,
      "Dépendance Importations": 3,
      "Éviction des Paysans": 3,
      "Fragilité Systémique": 5,
    },
    top_risk_entities: [
      "Bayer-Monsanto Agro Division",
      "Cargill Global Food Systems",
      "Gouvernement du Yémen — Sécurité Alimentaire",
    ],
    critical_alerts: [
      "ALERTE CRITIQUE: Bayer-Monsanto Agro Division (États-Unis) — score souveraineté 83.75/100",
      "ALERTE CRITIQUE: Cargill Global Food Systems (États-Unis) — score souveraineté 78.35/100",
      "ALERTE CRITIQUE: Gouvernement du Yémen — Sécurité Alimentaire (Yémen) — score souveraineté 70.80/100",
    ],
    last_analysis: "2026-06-20T00:00:00Z",
    engine_version: "1.0.0",
    domain: "food",
    confidence_score: 85.0,
    data_sources: [
      "FAO Food Security Indicators Database",
      "ETC Group Seed Industry Reports",
      "GRAIN Land Grabbing Database",
      "IPES-Food Systems Analysis Reports",
    ],
    entities,
    avg_estimated_food_index: 5.03,
  };

  return { entities, summary };
}
