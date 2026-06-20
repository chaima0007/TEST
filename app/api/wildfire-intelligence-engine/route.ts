import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// ── Wildfire Intelligence Engine — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
// Domain: wildfire | Slug: wildfire-intelligence-engine
// 8 entities: 3 critique, 2 élevé, 1 modéré, 2 faible

if (!process.env.SWARM_API_URL) {
  console.warn("[wildfire-intelligence-engine] SWARM_API_URL non défini — mode mock activé");
}

// ── Types ──────────────────────────────────────────────────────────────────────

interface WildfireEntity {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  spread_score: number;
  prevention_score: number;
  response_score: number;
  impact_score: number;
  risk_level: "critique" | "élevé" | "modéré" | "faible";
  primary_pattern: string;
  key_signals: string[];
  estimated_wildfire_index: number;
  last_updated: string;
  recommended_action: string;
}

interface WildfireSummary {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: WildfireEntity[];
  avg_estimated_wildfire_index: number;
}

// ── Route ──────────────────────────────────────────────────────────────────────

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Wildfire Intelligence Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/wildfire-intelligence-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Wildfire Intelligence Agent"));
  } catch {
    return NextResponse.json(
      sealResponse(getMockData(), "Wildfire Intelligence Agent"),
      { status: 502 }
    );
  }
}

// ── Mock data ──────────────────────────────────────────────────────────────────

function getMockData(): WildfireSummary {
  const now = new Date().toISOString();

  const entities: WildfireEntity[] = [
    // WF-001 — California Wildfire Zone — critique (73.25)
    {
      entity_id: "WF-001",
      name: "California Wildfire Zone",
      country: "USA",
      sector: "Emergency Management",
      spread_score: 80,
      prevention_score: 70,
      response_score: 65,
      impact_score: 77.5,
      composite_score: 73.25,
      risk_level: "critique",
      primary_pattern: "Propagation Catastrophique",
      key_signals: [
        "Vitesse de propagation de 2 km/h enregistrée avec des rafales à 80 km/h",
        "Indice de sécheresse de la végétation (KBDI) au niveau critique — 700+",
        "Superficie brûlée cumulée dépassant 500 000 hectares depuis janvier",
      ],
      estimated_wildfire_index: 7.33, // round(73.25/100*10,2)
      recommended_action: "déploiement_immédiat_équipes_lutte_incendie",
      last_updated: now,
    },
    // WF-002 — Amazon Deforestation Region — critique (83.0)
    {
      entity_id: "WF-002",
      name: "Amazon Deforestation Region",
      country: "Brazil",
      sector: "Environmental",
      spread_score: 85,
      prevention_score: 80,
      response_score: 75,
      impact_score: 93.75,
      composite_score: 83.0,
      risk_level: "critique",
      primary_pattern: "Déficit Prévention Critique",
      key_signals: [
        "Taux de déforestation illégale en hausse de 34 % sur les 12 derniers mois",
        "Absence de corridor pare-feu sur 1 200 km de frontière forêt-agriculture",
        "Concentration de CO₂ forestier anormalement élevée détectée par satellite",
      ],
      estimated_wildfire_index: 8.3,
      recommended_action: "déploiement_immédiat_équipes_lutte_incendie",
      last_updated: now,
    },
    // WF-003 — Mediterranean Basin Authority — critique (68.25)
    {
      entity_id: "WF-003",
      name: "Mediterranean Basin Authority",
      country: "Greece",
      sector: "Emergency Management",
      spread_score: 75,
      prevention_score: 65,
      response_score: 60,
      impact_score: 72.5,
      composite_score: 68.25,
      risk_level: "critique",
      primary_pattern: "Propagation Catastrophique",
      key_signals: [
        "Canicule persistante avec températures dépassant 42 °C pendant 14 jours consécutifs",
        "Humidité relative inférieure à 15 % sur l'ensemble du bassin méditerranéen",
        "Infrastructure de détection précoce défaillante dans 60 % des zones forestières",
      ],
      estimated_wildfire_index: 6.83,
      recommended_action: "déploiement_immédiat_équipes_lutte_incendie",
      last_updated: now,
    },
    // WF-004 — Australian Bushfire Region — élevé (50.1)
    {
      entity_id: "WF-004",
      name: "Australian Bushfire Region",
      country: "Australia",
      sector: "Emergency Management",
      spread_score: 55,
      prevention_score: 45,
      response_score: 50,
      impact_score: 49.25,
      composite_score: 50.1,
      risk_level: "élevé",
      primary_pattern: "Effondrement Réponse d'Urgence",
      key_signals: [
        "Indice McArthur Forest Fire Danger (FFDI) à 50 — catégorie extrême",
        "Réserves en eau des retenues à 28 % de leur capacité normale pour la saison",
        "Manque de personnels formés pour la saison des feux — déficit de 35 % des effectifs",
      ],
      estimated_wildfire_index: 5.01,
      recommended_action: "renforcement_capacités_réponse_urgence",
      last_updated: now,
    },
    // WF-005 — Siberian Taiga Agency — élevé (44.9)
    {
      entity_id: "WF-005",
      name: "Siberian Taiga Agency",
      country: "Russia",
      sector: "Forestry",
      spread_score: 50,
      prevention_score: 40,
      response_score: 45,
      impact_score: 43.25,
      composite_score: 44.9,
      risk_level: "élevé",
      primary_pattern: "Impact Écosystème Majeur",
      key_signals: [
        "Dégel du pergélisol libérant du méthane et augmentant l'inflammabilité de la tourbe",
        "Absence de routes d'accès forestières sur 70 % du territoire de la taïga",
        "Superficie de forêt morte (bois mort) augmentée de 18 % suite aux épidémies de scolytes",
      ],
      estimated_wildfire_index: 4.49,
      recommended_action: "programme_restauration_écologique_surveillance",
      last_updated: now,
    },
    // WF-006 — Portuguese Forest Service — modéré (26.9)
    {
      entity_id: "WF-006",
      name: "Portuguese Forest Service",
      country: "Portugal",
      sector: "Forestry",
      spread_score: 30,
      prevention_score: 25,
      response_score: 28,
      impact_score: 23.25,
      composite_score: 26.9,
      risk_level: "modéré",
      primary_pattern: "Risque Saisonnier Émergent",
      key_signals: [
        "Expansion des plantations d'eucalyptus hautement inflammables sur 800 000 ha",
        "Ressources humaines de lutte anti-incendie réduites de 20 % par rapport à 2020",
        "Indices de risque saisonnier en hausse précoce — 3 semaines avant la normale",
      ],
      estimated_wildfire_index: 2.69,
      recommended_action: "activation_protocoles_surveillance_saisonnière",
      last_updated: now,
    },
    // WF-007 — Canadian Fire Watch — faible (11.85)
    {
      entity_id: "WF-007",
      name: "Canadian Fire Watch",
      country: "Canada",
      sector: "Emergency Management",
      spread_score: 15,
      prevention_score: 10,
      response_score: 12,
      impact_score: 9.25,
      composite_score: 11.85,
      risk_level: "faible",
      primary_pattern: "Risque Saisonnier Émergent",
      key_signals: [
        "Précipitations hivernales nettement supérieures à la moyenne — réserves hydriques satisfaisantes",
        "Programme de débroussaillage préventif complété à 95 % avant la saison estivale",
        "Réseau de surveillance par drone opérationnel sur l'ensemble des zones à risque",
      ],
      estimated_wildfire_index: 1.19,
      recommended_action: "activation_protocoles_surveillance_saisonnière",
      last_updated: now,
    },
    // WF-008 — Scandinavian Forest Authority — faible (8.35)
    {
      entity_id: "WF-008",
      name: "Scandinavian Forest Authority",
      country: "Sweden",
      sector: "Forestry",
      spread_score: 10,
      prevention_score: 8,
      response_score: 9,
      impact_score: 5.5,
      composite_score: 8.35,
      risk_level: "faible",
      primary_pattern: "Risque Saisonnier Émergent",
      key_signals: [
        "Taux d'humidité forestière à 78 % — niveau optimal hors période de risque",
        "Protocoles de coopération transfrontalière avec la Norvège et la Finlande actifs",
        "Investissement record dans la télédétection satellitaire des incendies — couverture 100 %",
      ],
      estimated_wildfire_index: 0.83,
      recommended_action: "activation_protocoles_surveillance_saisonnière",
      last_updated: now,
    },
  ];

  // avg_composite = (73.25 + 83.0 + 68.25 + 50.1 + 44.9 + 26.9 + 11.85 + 8.35) / 8 = 45.83
  const avg_composite = 45.83;
  // avg_estimated_wildfire_index = round(45.83 / 100 * 10, 2) = 4.58
  const avg_estimated_wildfire_index = 4.58;

  const top_risk_entities: string[] = entities
    .filter((e) => e.risk_level === "critique")
    .sort((a, b) => b.composite_score - a.composite_score)
    .map((e) => e.name);

  const critical_alerts: string[] = entities
    .filter((e) => e.risk_level === "critique")
    .map((e) => e.name);

  return {
    total_entities: 8,
    avg_composite,
    risk_distribution: {
      critique: 3,
      élevé: 2,
      modéré: 1,
      faible: 2,
    },
    pattern_distribution: {
      "Propagation Catastrophique": 2,
      "Déficit Prévention Critique": 1,
      "Effondrement Réponse d'Urgence": 1,
      "Impact Écosystème Majeur": 1,
      "Risque Saisonnier Émergent": 3,
    },
    top_risk_entities,
    critical_alerts,
    last_analysis: now,
    engine_version: "1.0.0",
    domain: "wildfire",
    confidence_score: 0.91,
    data_sources: [
      "NASA FIRMS — Fire Information for Resource Management System",
      "Copernicus Emergency Management Service (CEMS)",
      "NOAA Global Wildfire Information System (GWIS)",
      "FAO Global Forest Resources Assessment",
    ],
    entities,
    avg_estimated_wildfire_index,
  };
}
