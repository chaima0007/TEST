import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[water-rights-access-sanitation-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = getMockData();

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/water-rights-access-sanitation-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    {
      id: "WRAS-001",
      name: "Yemen — Infrastructures Eau Détruites Guerre, Millions Sans Accès Eau Potable, Choléra Épidémique & Puits Bombardés Coalition",
      country: "Yemen",
      sector: "Conflit & Crise Humanitaire",
      water_access_denial_civilian_severity_score: 96.0,
      sanitation_infrastructure_collapse_score: 92.0,
      water_privatization_rights_erosion_score: 85.0,
      water_conflict_weaponization_score: 95.0,
      composite_score: 92.05,
      risk_level: "critique",
      primary_pattern: "crise_acces_eau_potable",
      key_signals: ["Crise eau catastrophique — millions sans accès eau potable suite aux destructions délibérées d'infrastructures hydrauliques, violant le droit à l'eau reconnu par résolution ONU A/RES/64/292 (2010)", "Armement de l'eau — bombardements de puits et systèmes de désalinisation utilisés comme tactique de guerre contre les populations civiles, violation grave du DIH", "Épidémie de choléra record — 2.5M cas documentés par l'OMS, conséquence directe de la contamination des sources d'eau"],
      estimated_water_rights_access_sanitation_index: 9.21,
      last_updated: "2026-06-21"
    },
    {
      id: "WRAS-002",
      name: "RDC — Accès Eau Potable 35% Population Zones Conflit Kivu, Cholera Endémique, Femmes 6h Transport Eau & Contamination Intentionnelle",
      country: "RDC",
      sector: "Conflit & Infrastructure Dégradée",
      water_access_denial_civilian_severity_score: 90.0,
      sanitation_infrastructure_collapse_score: 88.0,
      water_privatization_rights_erosion_score: 80.0,
      water_conflict_weaponization_score: 82.0,
      composite_score: 85.4,
      risk_level: "critique",
      primary_pattern: "effondrement_infrastructures_sanitaires",
      key_signals: ["Effondrement infrastructures eau — 65% population sans accès eau potable sûre, avec contamination bactérienne et parasitaire massive dans les zones de conflit Kivu", "Fardeau genré de l'eau — les femmes consacrent jusqu'à 6h par jour au transport d'eau, violation du droit à l'eau et discrimination genrée", "Choléra endémique — 30.000+ cas/an directement liés à l'absence d'assainissement, violation de l'article 12 du PIDESC"],
      estimated_water_rights_access_sanitation_index: 8.54,
      last_updated: "2026-06-21"
    },
    {
      id: "WRAS-003",
      name: "Gaza — Désalinisation Détruite Siège, Eau Contaminée Population Civile, Infrastructures WASH Bombardées & Accès Bloqué Humanitaire",
      country: "Palestine/Gaza",
      sector: "Siège & Droit International Humanitaire",
      water_access_denial_civilian_severity_score: 95.0,
      sanitation_infrastructure_collapse_score: 90.0,
      water_privatization_rights_erosion_score: 78.0,
      water_conflict_weaponization_score: 96.0,
      composite_score: 89.7,
      risk_level: "critique",
      primary_pattern: "eau_arme_conflit",
      key_signals: ["Eau weaponisée — destruction délibérée des infrastructures de désalinisation bloquant l'accès à l'eau potable pour 2.3M civils, crime de guerre selon Protocole I des Conventions de Genève", "Contamination de masse — eau souterraine contaminée par les eaux usées non traitées suite à l'effondrement des systèmes d'assainissement", "Crise sanitaire systémique — accès humanitaire bloqué empêchant la réparation des infrastructures WASH critiques"],
      estimated_water_rights_access_sanitation_index: 8.97,
      last_updated: "2026-06-21"
    },
    {
      id: "WRAS-004",
      name: "Somalie — Sécheresse Crise Humanitaire Eau 2022, 7M Personnes Déplacées, Pénurie Eau Pastorale & Enfants Malnutrition Déshydratation",
      country: "Somalie",
      sector: "Sécheresse & Crise Climatique",
      water_access_denial_civilian_severity_score: 88.0,
      sanitation_infrastructure_collapse_score: 84.0,
      water_privatization_rights_erosion_score: 72.0,
      water_conflict_weaponization_score: 76.0,
      composite_score: 80.6,
      risk_level: "critique",
      primary_pattern: "crise_acces_eau_potable",
      key_signals: ["Sécheresse record — 5ème saison des pluies manquée, 7M personnes déplacées par la pénurie d'eau, situation qualifiée de pré-famine par l'OCHA", "Enfants vulnérables — 1.5M enfants en malnutrition aiguë directement liée à la déshydratation et l'insécurité alimentaire hydrique", "Effondrement pastoral — les communautés pastorales perdent leur bétail sans accès aux puits, destruction des moyens de subsistance"],
      estimated_water_rights_access_sanitation_index: 8.06,
      last_updated: "2026-06-21"
    },
    {
      id: "WRAS-005",
      name: "Bolivie/Cochabamba — Guerre de l'Eau Privatisation Bechtel 1999, Contrats Illégaux, Coupures Accès Pauvres & Résistance Populaire Réprimée",
      country: "Bolivie",
      sector: "Privatisation & Résistance Populaire",
      water_access_denial_civilian_severity_score: 55.0,
      sanitation_infrastructure_collapse_score: 48.0,
      water_privatization_rights_erosion_score: 78.0,
      water_conflict_weaponization_score: 40.0,
      composite_score: 56.0,
      risk_level: "élevé",
      primary_pattern: "privatisation_eau_violation_droits",
      key_signals: ["Privatisation illégitime — contrat Bechtel/Aguas del Tunari accordant droits exclusifs sur l'eau de pluie violant le droit à l'eau des populations pauvres", "Répression de la résistance — mort de Victor Hugo Daza lors des manifestations contre la privatisation, 175 blessés, état d'urgence décrété", "Modèle de résistance — la Guerre de l'Eau de Cochabamba a inspiré la reconnaissance internationale du droit à l'eau comme droit humain fondamental"],
      estimated_water_rights_access_sanitation_index: 5.6,
      last_updated: "2026-06-21"
    },
    {
      id: "WRAS-006",
      name: "Inde/Punjab — Stress Hydrique Agriculture Intensive, Surexploitation Aquifères, Pesticides Eau Souterraine & Crise Accès Rural Dalit",
      country: "Inde",
      sector: "Agriculture Industrielle & Inégalités",
      water_access_denial_civilian_severity_score: 50.0,
      sanitation_infrastructure_collapse_score: 45.0,
      water_privatization_rights_erosion_score: 62.0,
      water_conflict_weaponization_score: 38.0,
      composite_score: 49.35,
      risk_level: "élevé",
      primary_pattern: "privatisation_eau_violation_droits",
      key_signals: ["Surexploitation aquifères — nappe phréatique en chute libre de 0.5m/an dans le Punjab, menaçant l'accès à long terme de 27M personnes", "Discrimination d'accès — les communautés Dalit ont un accès inférieur aux infrastructures d'eau potable, perpétuant les inégalités de caste", "Contamination pesticides — 76% des échantillons d'eau souterraine dépassent les normes OMS pour les pesticides agricoles"],
      estimated_water_rights_access_sanitation_index: 4.93,
      last_updated: "2026-06-21"
    },
    {
      id: "WRAS-007",
      name: "Chili — Privatisation Eau Constitutionnelle Codes 1981, Droits Propriété Eau Concentrés Agro-Industrie & Communautés Sans Accès Garanti",
      country: "Chili",
      sector: "Privatisation Constitutionnelle",
      water_access_denial_civilian_severity_score: 28.0,
      sanitation_infrastructure_collapse_score: 25.0,
      water_privatization_rights_erosion_score: 42.0,
      water_conflict_weaponization_score: 22.0,
      composite_score: 29.55,
      risk_level: "modéré",
      primary_pattern: "privatisation_eau_violation_droits",
      key_signals: ["Privatisation constitutionnelle unique — le Code des Eaux de 1981 (Pinochet) fait de l'eau un bien privé échangeable, 85% des droits détenus par l'agro-industrie et les mines", "Réforme constitutionnelle rejetée — la proposition de 2022 visant à reconnaître l'eau comme bien commun a été rejetée par référendum", "Communautés rurales vulnérables — 400.000 personnes sans accès garanti à l'eau potable dans les zones rurales andines"],
      estimated_water_rights_access_sanitation_index: 2.96,
      last_updated: "2026-06-21"
    },
    {
      id: "WRAS-008",
      name: "Pays-Bas — Eau Bien Commun Modèle Gestion Publique, Interdiction Privatisation Constitutionnelle, Standards RIVM & Accès Universel Garanti",
      country: "Pays-Bas",
      sector: "Modèle de Bonne Gouvernance",
      water_access_denial_civilian_severity_score: 5.0,
      sanitation_infrastructure_collapse_score: 4.0,
      water_privatization_rights_erosion_score: 6.0,
      water_conflict_weaponization_score: 3.0,
      composite_score: 4.6,
      risk_level: "faible",
      primary_pattern: "crise_acces_eau_potable",
      key_signals: ["Modèle de gestion publique — l'eau est un service public non-privatisable par loi depuis 2004, 99.9% de la population avec accès à l'eau potable de haute qualité", "Standards de qualité exemplaires — contrôle RIVM continu, eau du robinet de qualité supérieure à l'eau embouteillée", "Exportateur de gouvernance — expertise néerlandaise en gestion de l'eau exportée dans 30+ pays via les programmes de coopération"],
      estimated_water_rights_access_sanitation_index: 0.46,
      last_updated: "2026-06-21"
    }
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { crise_acces_eau_potable: 3, effondrement_infrastructures_sanitaires: 1, eau_arme_conflit: 1, privatisation_eau_violation_droits: 3 },
    top_risk_entities: ["Yemen — Infrastructures Eau Détruites Guerre, Millions Sans Accès Eau Potable, Choléra Épidémique & Puits Bombardés Coalition", "Gaza — Désalinisation Détruite Siège, Eau Contaminée Population Civile, Infrastructures WASH Bombardées & Accès Bloqué Humanitaire", "RDC — Accès Eau Potable 35% Population Zones Conflit Kivu, Cholera Endémique, Femmes 6h Transport Eau & Contamination Intentionnelle"],
    critical_alerts: ["Yemen — Infrastructures Eau Détruites Guerre: crise_acces_eau_potable", "Gaza — Désalinisation Détruite Siège: eau_arme_conflit", "RDC — Accès Eau Potable 35% Population: effondrement_infrastructures_sanitaires", "Somalie — Sécheresse Crise Humanitaire: crise_acces_eau_potable"],
    last_analysis: "2026-06-21",
    engine_version: "1.0.0",
    domain: "water_rights_access_sanitation",
    confidence_score: 0.87,
    data_sources: ["who_unicef_joint_water_monitoring_2023", "human_rights_watch_water_crisis_reports", "food_water_watch_privatization_database", "oxfam_water_conflict_monitor_2023"],
    entities,
    avg_estimated_water_rights_access_sanitation_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
