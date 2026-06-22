import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[arctic-sovereignty-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(
      sealResponse(getMockData(), "Arctic Sovereignty Engine Agent"),
    ));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/arctic-sovereignty-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Arctic Sovereignty Engine Agent")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse(getMockData(), "Arctic Sovereignty Engine Agent"),
      { status: 502 },
    ));
  }
}

function getMockData() {
  const entities = [
    {
      id: "ENT-001",
      name: "Russia Arctic Command",
      country: "Russie",
      sector: "Défense & Militaire",
      composite_score: 79.15,
      territorial_score: 88.0,
      military_score: 85.0,
      resource_score: 72.0,
      climate_score: 55.0,
      risk_level: "critique",
      primary_pattern: "tension_territoriale",
      key_signals: [
        "Revendications territoriales massives sur le plateau continental arctique",
        "Déploiement de nouvelles bases militaires en Arctique profond",
        "Contrôle stratégique des routes maritimes nordiques renforcé",
      ],
      estimated_arctic_index: 7.92,
      last_updated: "2026-06-20",
      disputed_zones: 7,
    },
    {
      id: "ENT-002",
      name: "China Arctic Silk Road",
      country: "Chine",
      sector: "Infrastructure & Commerce",
      composite_score: 67.35,
      territorial_score: 72.0,
      military_score: 65.0,
      resource_score: 75.0,
      climate_score: 52.0,
      risk_level: "critique",
      primary_pattern: "tension_territoriale",
      key_signals: [
        "Investissements massifs dans les infrastructures portuaires arctiques",
        "Route de la Soie Polaire : accès commercial aux ressources énergétiques",
        "Présence scientifique et économique croissante en Arctique",
      ],
      estimated_arctic_index: 6.74,
      last_updated: "2026-06-20",
      disputed_zones: 4,
    },
    {
      id: "ENT-003",
      name: "US Coast Guard Arctic",
      country: "États-Unis",
      sector: "Sécurité Maritime",
      composite_score: 61.35,
      territorial_score: 70.0,
      military_score: 68.0,
      resource_score: 55.0,
      climate_score: 42.0,
      risk_level: "critique",
      primary_pattern: "tension_territoriale",
      key_signals: [
        "Renforcement des patrouilles maritimes dans les eaux arctiques disputées",
        "Modernisation de la flotte brise-glace pour opérations polaires",
        "Surveillance accrue des activités russes et chinoises en Arctique",
      ],
      estimated_arctic_index: 6.14,
      last_updated: "2026-06-20",
      disputed_zones: 3,
    },
    {
      id: "ENT-004",
      name: "Norway Arctic Council",
      country: "Norvège",
      sector: "Diplomatie & Gouvernance",
      composite_score: 53.35,
      territorial_score: 58.0,
      military_score: 55.0,
      resource_score: 50.0,
      climate_score: 48.0,
      risk_level: "élevé",
      primary_pattern: "stabilite_arctique",
      key_signals: [
        "Présidence du Conseil Arctique — coordination diplomatique renforcée",
        "Tensions avec la Russie sur les droits de pêche en mer de Barents",
        "Développement des ressources pétrolières offshore en mer de Barents",
      ],
      estimated_arctic_index: 5.34,
      last_updated: "2026-06-20",
      disputed_zones: 2,
    },
    {
      id: "ENT-005",
      name: "Canada Arctic Patrol",
      country: "Canada",
      sector: "Surveillance Territoriale",
      composite_score: 47.35,
      territorial_score: 52.0,
      military_score: 48.0,
      resource_score: 45.0,
      climate_score: 42.0,
      risk_level: "élevé",
      primary_pattern: "stabilite_arctique",
      key_signals: [
        "Dispute sur le passage du Nord-Ouest avec les États-Unis",
        "Renforcement de la souveraineté canadienne dans l'archipel arctique",
        "Exploitation des ressources minières dans les territoires nordiques",
      ],
      estimated_arctic_index: 4.74,
      last_updated: "2026-06-20",
      disputed_zones: 2,
    },
    {
      id: "ENT-006",
      name: "Finland Arctic Strategy",
      country: "Finlande",
      sector: "Politique Environnementale",
      composite_score: 32.0,
      territorial_score: 35.0,
      military_score: 30.0,
      resource_score: 32.0,
      climate_score: 30.0,
      risk_level: "modéré",
      primary_pattern: "stabilite_arctique",
      key_signals: [
        "Stratégie nationale arctique centrée sur le développement durable",
        "Coopération environnementale avec les pays nordiques renforcée",
        "Surveillance des impacts climatiques sur les écosystèmes polaires",
      ],
      estimated_arctic_index: 3.2,
      last_updated: "2026-06-20",
      disputed_zones: 1,
    },
    {
      id: "ENT-007",
      name: "Denmark Greenland Authority",
      country: "Danemark",
      sector: "Administration Territoriale",
      composite_score: 16.15,
      territorial_score: 18.0,
      military_score: 15.0,
      resource_score: 16.0,
      climate_score: 14.0,
      risk_level: "faible",
      primary_pattern: "stabilite_arctique",
      key_signals: [
        "Autonomie croissante du Groenland — négociations constitutionnelles en cours",
        "Exploitation minière limitée pour préserver l'environnement arctique",
        "Coopération scientifique internationale sur le changement climatique",
      ],
      estimated_arctic_index: 1.62,
      last_updated: "2026-06-20",
      disputed_zones: 1,
    },
    {
      id: "ENT-008",
      name: "Iceland Research Station",
      country: "Islande",
      sector: "Recherche Polaire",
      composite_score: 8.85,
      territorial_score: 10.0,
      military_score: 8.0,
      resource_score: 9.0,
      climate_score: 8.0,
      risk_level: "faible",
      primary_pattern: "stabilite_arctique",
      key_signals: [
        "Recherche polaire internationale sur les variations climatiques arctiques",
        "Station d'observation des aurores boréales et phénomènes géophysiques",
        "Coopération scientifique pacifique avec les États arctiques riverains",
      ],
      estimated_arctic_index: 0.89,
      last_updated: "2026-06-20",
      disputed_zones: 0,
    },
  ];

  const avgComposite = Math.round(
    (entities.reduce((s, e) => s + e.composite_score, 0) / entities.length) * 100
  ) / 100;

  return {
    total_entities: entities.length,
    avg_composite: avgComposite,
    risk_distribution: { critique: 3, "élevé": 2, "modéré": 1, faible: 2 },
    pattern_distribution: {
      tension_territoriale: 3,
      militarisation_acceleree: 0,
      ruee_ressources: 0,
      crise_climatique_arctique: 0,
      stabilite_arctique: 5,
    },
    top_risk_entities: [
      "Russia Arctic Command",
      "China Arctic Silk Road",
      "US Coast Guard Arctic",
    ],
    critical_alerts: [
      "ALERTE CRITIQUE — Russia Arctic Command (Russie) : score composite 79.2/100",
      "ALERTE CRITIQUE — China Arctic Silk Road (Chine) : score composite 67.4/100",
      "ALERTE CRITIQUE — US Coast Guard Arctic (États-Unis) : score composite 61.4/100",
    ],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "arctic",
    confidence_score: 0.88,
    data_sources: [
      "arctic_council_reports",
      "satellite_surveillance",
      "geopolitical_risk_db",
    ],
    entities,
    avg_estimated_arctic_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
  };
}
