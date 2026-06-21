import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[satellite-constellation-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Satellite Constellation Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/satellite-constellation-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Satellite Constellation Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Satellite Constellation Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    // SAT-001 — USA, SpaceTech — critique (70.5) — kessler_syndrome_risk
    {
      id: "SAT-001",
      name: "Starlink LEO Constellation",
      country: "USA",
      sector: "SpaceTech",
      composite_score: 70.5,
      orbital_collision_risk_score: 75.0,
      signal_interference_score: 80.0,
      space_debris_accumulation_score: 60.0,
      regulatory_compliance_gap_score: 65.0,
      risk_level: "critique",
      primary_pattern: "kessler_syndrome_risk",
      key_signals: [
        "Densité critique LEO — 42 000+ satellites Starlink augmentent le risque de collision Kessler",
        "Cadence lancement SpaceX dépasse la capacité de désorbitation planifiée",
        "Manœuvres d'évitement collision actives — 5 000+ alertes conjunctions hebdomadaires",
      ],
      estimated_satellite_index: 7.05,
      last_updated: "2026-06-20",
      confidence_level: 0.88,
    },
    // SAT-002 — China, Government — critique (67.4) — signal_warfare
    {
      id: "SAT-002",
      name: "Guowang Constellation",
      country: "China",
      sector: "Government",
      composite_score: 67.4,
      orbital_collision_risk_score: 60.0,
      signal_interference_score: 75.0,
      space_debris_accumulation_score: 65.0,
      regulatory_compliance_gap_score: 72.0,
      risk_level: "critique",
      primary_pattern: "signal_warfare",
      key_signals: [
        "Brouillage systématique signaux GPS civil détecté sur bandes L1/L2 — zone Pacifique",
        "Guowang déploie 13 000 satellites en orbite basse — congestion spectre fréquences UIT",
        "Interférences satellites communication alliés OTAN documentées sur bandes Ku/Ka",
      ],
      estimated_satellite_index: 6.74,
      last_updated: "2026-06-20",
      confidence_level: 0.82,
    },
    // SAT-003 — Russia, Defense — critique (63.25) — debris_accumulation_crisis
    {
      id: "SAT-003",
      name: "Glonass-K2 Array",
      country: "Russia",
      sector: "Defense",
      composite_score: 63.25,
      orbital_collision_risk_score: 55.0,
      signal_interference_score: 60.0,
      space_debris_accumulation_score: 75.0,
      regulatory_compliance_gap_score: 65.0,
      risk_level: "critique",
      primary_pattern: "debris_accumulation_crisis",
      key_signals: [
        "Accumulation débris Glonass-K2 — fragmentation orbitale altitude 1 200 km détectée",
        "3 satellites Glonass hors service créent nuages de débris persistants en MEO",
        "Absence protocole déorbitation active — durée de vie orbitale estimée > 200 ans",
      ],
      estimated_satellite_index: 6.33,
      last_updated: "2026-06-20",
      confidence_level: 0.79,
    },
    // SAT-004 — EU, Navigation — élevé (50.75) — constellation_stable (all sub < 70)
    {
      id: "SAT-004",
      name: "Galileo Extended",
      country: "EU",
      sector: "Navigation",
      composite_score: 50.75,
      orbital_collision_risk_score: 45.0,
      signal_interference_score: 55.0,
      space_debris_accumulation_score: 50.0,
      regulatory_compliance_gap_score: 55.0,
      risk_level: "élevé",
      primary_pattern: "constellation_stable",
      key_signals: [
        "Non-conformité coordination fréquences ITU-R sur 12 nouvelles fréquences Galileo Extended",
        "Délais certification réglementaire EU Space Programme menacent service PRS militaire",
        "Litiges créneaux orbitaux GEO avec opérateurs commerciaux — procédure arbitrage ITU ouverte",
      ],
      estimated_satellite_index: 5.08,
      last_updated: "2026-06-20",
      confidence_level: 0.85,
    },
    // SAT-005 — India, Government — élevé (43.1) — kessler_syndrome_risk
    {
      id: "SAT-005",
      name: "IRNSS Expansion",
      country: "India",
      sector: "Government",
      composite_score: 43.1,
      orbital_collision_risk_score: 72.0,
      signal_interference_score: 40.0,
      space_debris_accumulation_score: 30.0,
      regulatory_compliance_gap_score: 20.0,
      risk_level: "élevé",
      primary_pattern: "kessler_syndrome_risk",
      key_signals: [
        "IRNSS Expansion Phase-2 — risque de collision altitude 36 000 km avec constellation GPS",
        "Couverture orbitale insuffisante — 4 satellites IRNSS en panne sans remplacement planifié",
        "Interférences signaux NavIC avec GLONASS sur bande L5 — impact précision positionnement",
      ],
      estimated_satellite_index: 4.31,
      last_updated: "2026-06-20",
      confidence_level: 0.76,
    },
    // SAT-006 — Japan, Navigation — modéré (28.75) — constellation_stable
    {
      id: "SAT-006",
      name: "QZSS Augmentation",
      country: "Japan",
      sector: "Navigation",
      composite_score: 28.75,
      orbital_collision_risk_score: 25.0,
      signal_interference_score: 30.0,
      space_debris_accumulation_score: 35.0,
      regulatory_compliance_gap_score: 25.0,
      risk_level: "modéré",
      primary_pattern: "constellation_stable",
      key_signals: [
        "QZSS Augmentation Phase-3 opérationnelle — coordination orbitale Japon/USA stable",
        "Faible densité satellite GEO/IGSO — risque collision minimal en orbite géostationnaire",
        "Conformité ITU certifiée — tous créneaux orbitaux QZSS homologués et coordonnés",
      ],
      estimated_satellite_index: 2.88,
      last_updated: "2026-06-20",
      confidence_level: 0.91,
    },
    // SAT-007 — Canada, Telecom — faible (13.75) — constellation_stable
    {
      id: "SAT-007",
      name: "Telesat LEO",
      country: "Canada",
      sector: "Telecom",
      composite_score: 13.75,
      orbital_collision_risk_score: 10.0,
      signal_interference_score: 15.0,
      space_debris_accumulation_score: 20.0,
      regulatory_compliance_gap_score: 10.0,
      risk_level: "faible",
      primary_pattern: "constellation_stable",
      key_signals: [
        "Telesat LEO Phase-1 — 298 satellites conformes standards débris spatial ESA-IADC",
        "Protocole déorbitation < 5 ans systématiquement respecté — modèle industrie résilience",
        "Faible densité orbitale LEO — aucune menace de collision détectée dans périmètre 50 km",
      ],
      estimated_satellite_index: 1.38,
      last_updated: "2026-06-20",
      confidence_level: 0.93,
    },
    // SAT-008 — ESA, Earth Observation — faible (8.6) — constellation_stable
    {
      id: "SAT-008",
      name: "Copernicus Sentinel",
      country: "ESA",
      sector: "Earth Observation",
      composite_score: 8.6,
      orbital_collision_risk_score: 5.0,
      signal_interference_score: 10.0,
      space_debris_accumulation_score: 12.0,
      regulatory_compliance_gap_score: 8.0,
      risk_level: "faible",
      primary_pattern: "constellation_stable",
      key_signals: [
        "Copernicus Sentinel — flotte 6 satellites observation Terre conforme traités internationaux",
        "Protocoles coordination orbitale ESA ESOC exemplaires — zéro incident collision depuis 2014",
        "Gestion optimale débris spatiaux — tous satellites Sentinel équipés propulsion déorbitation",
      ],
      estimated_satellite_index: 0.86,
      last_updated: "2026-06-20",
      confidence_level: 0.95,
    },
  ];

  const n = entities.length;
  const avgComposite = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / n * 100) / 100;
  const avgConfidence = Math.round(entities.reduce((s, e) => s + e.confidence_level, 0) / n * 100) / 100;

  const riskDist = { critique: 0, "élevé": 0, "modéré": 0, faible: 0 } as Record<string, number>;
  const patDist: Record<string, number> = {
    kessler_syndrome_risk: 0,
    signal_warfare: 0,
    debris_accumulation_crisis: 0,
    regulatory_non_compliance: 0,
    constellation_stable: 0,
  };
  for (const e of entities) {
    riskDist[e.risk_level] = (riskDist[e.risk_level] || 0) + 1;
    patDist[e.primary_pattern] = (patDist[e.primary_pattern] || 0) + 1;
  }

  const sorted = [...entities].sort((a, b) => b.composite_score - a.composite_score);

  const summary = {
    total_entities: n,
    avg_composite: avgComposite,
    risk_distribution: riskDist,
    pattern_distribution: patDist,
    top_risk_entities: sorted.slice(0, 3).map(e => e.name),
    critical_alerts: entities.filter(e => e.risk_level === "critique").map(e => e.name),
    last_analysis: "2026-06-20T00:00:00Z",
    engine_version: "1.0.0",
    domain: "satellite",
    confidence_score: avgConfidence,
    data_sources: ["ESA Space Debris Reports", "ITU Satellite Registry", "NASA Orbital Catalog"],
    entities,
    avg_estimated_satellite_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
  };

  return summary;
}
