import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[geoengineering-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Geoengineering Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/geoengineering-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Geoengineering Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Geoengineering Agent"), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    {
      id: "GE-001",
      name: "Programme HAARP Russie — Division Climatique",
      country: "Russie",
      sector: "Géo-ingénierie Militaire",
      composite_score: 84.35,
      unilateral_deployment_score: 90.0,
      ecological_risk_score: 85.0,
      governance_deficit_score: 82.0,
      dual_use_weaponization_score: 78.0,
      risk_level: "critique",
      primary_pattern: "Déploiement Unilatéral",
      key_signals: [
        "Expériences d'ionosphère non déclarées affectant les précipitations en Europe de l'Est",
        "Programme militaire double usage modifiant les courants atmosphériques",
        "Absence totale de notification internationale préalable aux déploiements",
      ],
      estimated_geoengineering_index: 8.44,
      last_updated: "2026-06-20",
    },
    {
      id: "GE-002",
      name: "SolarShield Technologies Corp",
      country: "États-Unis",
      sector: "Géo-ingénierie Privée",
      composite_score: 78.5,
      unilateral_deployment_score: 82.0,
      ecological_risk_score: 78.0,
      governance_deficit_score: 80.0,
      dual_use_weaponization_score: 72.0,
      risk_level: "critique",
      primary_pattern: "Déploiement Unilatéral",
      key_signals: [
        "Dispersion d'aérosols stratosphériques sans autorisation gouvernementale",
        "Brevets déposés sur des technologies de modification climatique à usage commercial",
        "Financement par fonds spéculatifs ciblant des marchés carbone artificiels",
      ],
      estimated_geoengineering_index: 7.85,
      last_updated: "2026-06-20",
    },
    {
      id: "GE-003",
      name: "Programme National de Pluie Artificielle Chine",
      country: "Chine",
      sector: "Géo-ingénierie Étatique",
      composite_score: 72.4,
      unilateral_deployment_score: 76.0,
      ecological_risk_score: 74.0,
      governance_deficit_score: 70.0,
      dual_use_weaponization_score: 68.0,
      risk_level: "critique",
      primary_pattern: "Déploiement Unilatéral",
      key_signals: [
        "1,5 million km² sous couverture d'ensemencement des nuages actif sans accord régional",
        "Détournement des précipitations affectant les pays voisins (Inde, Vietnam, Kazakhstan)",
        "Technologies duales utilisables pour priver les adversaires de ressources en eau",
      ],
      estimated_geoengineering_index: 7.24,
      last_updated: "2026-06-20",
    },
    {
      id: "GE-004",
      name: "Make Sunsets LLC",
      country: "États-Unis",
      sector: "Géo-ingénierie Privée",
      composite_score: 61.85,
      unilateral_deployment_score: 60.0,
      ecological_risk_score: 64.0,
      governance_deficit_score: 65.0,
      dual_use_weaponization_score: 58.0,
      risk_level: "élevé",
      primary_pattern: "Vide Gouvernanciel",
      key_signals: [
        "Lancement de ballons dispersant du dioxyde de soufre au-dessus du Mexique sans accord",
        "Modèle commercial vendant des 'crédits de refroidissement' non réglementés",
        "Absence de protocole d'évaluation des impacts sur les populations locales",
      ],
      estimated_geoengineering_index: 6.19,
      last_updated: "2026-06-20",
    },
    {
      id: "GE-005",
      name: "Projet IROAM — Fertilisation Océanique Atlantique",
      country: "Canada",
      sector: "Géo-ingénierie Océanique",
      composite_score: 56.9,
      unilateral_deployment_score: 55.0,
      ecological_risk_score: 58.0,
      governance_deficit_score: 62.0,
      dual_use_weaponization_score: 52.0,
      risk_level: "élevé",
      primary_pattern: "Vide Gouvernanciel",
      key_signals: [
        "Dispersion de 100 tonnes de sulfate de fer en Pacifique Nord sans autorisation NOAA",
        "Risques d'hypoxie sous-marine non évalués sur les zones de pêche internationales",
        "Financement opaque via des entreprises-coquilles dans des paradis fiscaux",
      ],
      estimated_geoengineering_index: 5.69,
      last_updated: "2026-06-20",
    },
    {
      id: "GE-006",
      name: "Programme SCoPEx — Harvard University",
      country: "États-Unis",
      sector: "Recherche Géo-ingénierie",
      composite_score: 29.4,
      unilateral_deployment_score: 35.0,
      ecological_risk_score: 30.0,
      governance_deficit_score: 28.0,
      dual_use_weaponization_score: 22.0,
      risk_level: "modéré",
      primary_pattern: "Aucun",
      key_signals: [
        "Expériences stratosphériques en phase de test nécessitant un cadre de gouvernance",
        "Financement partiellement privé créant des conflits d'intérêts potentiels",
        "Débat scientifique non résolu sur les effets secondaires régionaux des aérosols",
      ],
      estimated_geoengineering_index: 2.94,
      last_updated: "2026-06-20",
    },
    {
      id: "GE-007",
      name: "Groupe Intergouvernemental Experts Climat (GIEC)",
      country: "International",
      sector: "Gouvernance Climatique",
      composite_score: 9.8,
      unilateral_deployment_score: 10.0,
      ecological_risk_score: 12.0,
      governance_deficit_score: 8.0,
      dual_use_weaponization_score: 9.0,
      risk_level: "faible",
      primary_pattern: "Aucun",
      key_signals: [
        "Protocole de surveillance multilatérale des expériences géo-ingénierie actif",
        "Recommandations de moratoire adoptées par 152 États membres de l'ONU",
        "Transparence totale des données scientifiques avec peer-review international",
      ],
      estimated_geoengineering_index: 0.98,
      last_updated: "2026-06-20",
    },
    {
      id: "GE-008",
      name: "Alliance Géo-ingénierie Responsable — Union Européenne",
      country: "Union Européenne",
      sector: "Gouvernance Climatique",
      composite_score: 11.2,
      unilateral_deployment_score: 12.0,
      ecological_risk_score: 10.0,
      governance_deficit_score: 14.0,
      dual_use_weaponization_score: 8.0,
      risk_level: "faible",
      primary_pattern: "Aucun",
      key_signals: [
        "Cadre réglementaire EU interdisant les expériences non autorisées au-dessus de l'Europe",
        "Comité d'éthique transnational supervisant tous les projets de recherche",
        "Protocole de partage de données obligatoire avec les pays tiers affectés",
      ],
      estimated_geoengineering_index: 1.12,
      last_updated: "2026-06-20",
    },
  ];

  const summary = {
    total_entities: 8,
    avg_composite: 50.55,
    risk_distribution: { critique: 3, "élevé": 2, "modéré": 1, faible: 2 },
    pattern_distribution: {
      "Déploiement Unilatéral": 3,
      "Risque Écosystémique": 3,
      "Vide Gouvernanciel": 4,
      "Militarisation Climatique": 2,
      "Expérimentation Non Consentie": 5,
    },
    top_risk_entities: [
      "Programme HAARP Russie — Division Climatique",
      "SolarShield Technologies Corp",
      "Programme National de Pluie Artificielle Chine",
    ],
    critical_alerts: [
      "ALERTE CRITIQUE: Programme HAARP Russie — Division Climatique (Russie) — score géo-ingénierie 84.35/100",
      "ALERTE CRITIQUE: SolarShield Technologies Corp (États-Unis) — score géo-ingénierie 78.50/100",
      "ALERTE CRITIQUE: Programme National de Pluie Artificielle Chine (Chine) — score géo-ingénierie 72.40/100",
    ],
    last_analysis: "2026-06-20T00:00:00Z",
    engine_version: "1.0.0",
    domain: "geoengineering",
    confidence_score: 82.0,
    data_sources: [
      "IPCC Geoengineering Assessment Reports",
      "Carnegie Climate Governance Initiative",
      "ETC Group Geoengineering Monitor",
      "Oxford Geoengineering Programme Database",
    ],
    entities,
    avg_estimated_geoengineering_index: 5.06,
  };

  return { entities, summary };
}
