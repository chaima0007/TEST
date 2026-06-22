import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[space-militarization-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Space Militarization Engine Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/space-militarization-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Space Militarization Engine Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Space Militarization Engine Agent"), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    { id: "SM-001", name: "USA — Space Force & Domination Orbitale", country: "Amérique du Nord", sector: "GPS Militaire, Satellites Espions & Armes Co-Orbitales X-37B", composite_score: 86.5, asat_capability_score: 88.0, orbital_weapons_score: 82.0, space_surveillance_dominance_score: 95.0, debris_creation_risk_score: 75.0, risk_level: "critique", primary_pattern: "domination_orbitale", key_signals: ["Arsenal militaire spatial critique dans USA — Space Force & Domination Orbitale — capacités anti-satellite menaçant les orbites globales", "Armes co-orbitales déployées ou en test — satellites-tueurs capables de neutraliser des actifs adverses", "Risque de cascade Kessler — tests ASAT créant des débris qui pourraient rendre des orbites inutilisables"], estimated_space_conflict_index: 8.65, last_updated: "2026-06-20" },
    { id: "SM-002", name: "Chine — Programme ASAT & Lune Stratégique", country: "Asie", sector: "Test ASAT 2007, Satellites-Tueurs & Ambitions Lunaires Militaires", composite_score: 86.25, asat_capability_score: 90.0, orbital_weapons_score: 85.0, space_surveillance_dominance_score: 80.0, debris_creation_risk_score: 90.0, risk_level: "critique", primary_pattern: "arsenal_asat_actif", key_signals: ["Arsenal militaire spatial critique dans Chine — Programme ASAT & Lune Stratégique — capacités anti-satellite menaçant les orbites globales", "Armes co-orbitales déployées ou en test — satellites-tueurs capables de neutraliser des actifs adverses", "Risque de cascade Kessler — tests ASAT créant des débris qui pourraient rendre des orbites inutilisables"], estimated_space_conflict_index: 8.63, last_updated: "2026-06-20" },
    { id: "SM-003", name: "Russie — Arsenal Spatial Héritage Soviétique", country: "Europe de l'Est", sector: "Cosmos 2543 Satellite-Tueur & Système Nudol Anti-Satellite", composite_score: 84.5, asat_capability_score: 85.0, orbital_weapons_score: 88.0, space_surveillance_dominance_score: 75.0, debris_creation_risk_score: 85.0, risk_level: "critique", primary_pattern: "arsenal_asat_actif", key_signals: ["Arsenal militaire spatial critique dans Russie — Arsenal Spatial Héritage Soviétique — capacités anti-satellite menaçant les orbites globales", "Armes co-orbitales déployées ou en test — satellites-tueurs capables de neutraliser des actifs adverses", "Risque de cascade Kessler — tests ASAT créant des débris qui pourraient rendre des orbites inutilisables"], estimated_space_conflict_index: 8.45, last_updated: "2026-06-20" },
    { id: "SM-004", name: "Inde — Club ASAT 2019 Mission Shakti", country: "Asie du Sud", sector: "Test ASAT Mars 2019 — 4e Puissance Spatiale Militaire Mondiale", composite_score: 64.85, asat_capability_score: 65.0, orbital_weapons_score: 58.0, space_surveillance_dominance_score: 60.0, debris_creation_risk_score: 72.0, risk_level: "critique", primary_pattern: "course_spatiale_militaire", key_signals: ["Arsenal militaire spatial critique dans Inde — Club ASAT 2019 Mission Shakti — capacités anti-satellite menaçant les orbites globales", "Armes co-orbitales déployées ou en test — satellites-tueurs capables de neutraliser des actifs adverses", "Risque de cascade Kessler — tests ASAT créant des débris qui pourraient rendre des orbites inutilisables"], estimated_space_conflict_index: 6.49, last_updated: "2026-06-20" },
    { id: "SM-005", name: "France & UK — Commandements Spatiaux OTAN", country: "Europe", sector: "Commandements Spatiaux Nationaux & Satellites Militaires Syracuse/Skynet", composite_score: 50.85, asat_capability_score: 52.0, orbital_weapons_score: 48.0, space_surveillance_dominance_score: 60.0, debris_creation_risk_score: 42.0, risk_level: "élevé", primary_pattern: "course_spatiale_militaire", key_signals: ["Capacités spatiales militaires avancées dans France & UK — Commandements Spatiaux OTAN — programme actif de guerre spatiale", "Investissements massifs en satellites militaires et systèmes de surveillance orbitale", "Participation à la course aux armements spatiaux — déploiement de capacités d'interférence spatiale"], estimated_space_conflict_index: 5.09, last_updated: "2026-06-20" },
    { id: "SM-006", name: "Israël — Renseignement Satellitaire Avancé", country: "MENA", sector: "Ofek/EROS — Surveillance Régionale & Capacités Cyber Spatiales", composite_score: 44.25, asat_capability_score: 45.0, orbital_weapons_score: 40.0, space_surveillance_dominance_score: 58.0, debris_creation_risk_score: 35.0, risk_level: "élevé", primary_pattern: "course_spatiale_militaire", key_signals: ["Capacités spatiales militaires avancées dans Israël — Renseignement Satellitaire Avancé — programme actif de guerre spatiale", "Investissements massifs en satellites militaires et systèmes de surveillance orbitale", "Participation à la course aux armements spatiaux — déploiement de capacités d'interférence spatiale"], estimated_space_conflict_index: 4.43, last_updated: "2026-06-20" },
    { id: "SM-007", name: "Iran & Corée du Nord — Programmes Spatiaux Duaux", country: "MENA/Asie", sector: "Missiles Balistiques Déguisés en Lanceurs Spatiaux — Dual-Use Évident", composite_score: 35.1, asat_capability_score: 35.0, orbital_weapons_score: 38.0, space_surveillance_dominance_score: 28.0, debris_creation_risk_score: 42.0, risk_level: "modéré", primary_pattern: "capacites_emergentes", key_signals: ["Programme spatial militaire émergent dans Iran & Corée du Nord — Programmes Spatiaux Duaux — capacités ASAT en développement", "Investissements en technologies duales espace civil/militaire — potentiel de conversion militaire", "Intégration partielle dans les systèmes de navigation et communication militaires par satellite"], estimated_space_conflict_index: 3.51, last_updated: "2026-06-20" },
    { id: "SM-008", name: "Luxembourg & Japon — Coopération Civile", country: "Global", sector: "JAXA Coopération Civile & Luxembourg Space Hub — Usage Non-Militaire", composite_score: 9.25, asat_capability_score: 8.0, orbital_weapons_score: 5.0, space_surveillance_dominance_score: 15.0, debris_creation_risk_score: 6.0, risk_level: "faible", primary_pattern: "cooperation_spatiale", key_signals: ["Luxembourg & Japon — Coopération Civile maintient une utilisation spatiale coopérative — programmes essentiellement civils et transparents", "Participation aux accords internationaux de durabilité spatiale et lutte contre les débris", "Modèle de coopération spatiale à encourager — science et exploration sans militarisation"], estimated_space_conflict_index: 0.93, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { arsenal_asat_actif: 2, domination_orbitale: 1, course_spatiale_militaire: 3, capacites_emergentes: 1, cooperation_spatiale: 1 },
    top_risk_entities: ["USA — Space Force & Domination Orbitale", "Chine — Programme ASAT & Lune Stratégique", "Russie — Arsenal Spatial Héritage Soviétique"],
    critical_alerts: ["USA: domination orbitale", "Chine: arsenal ASAT actif", "Russie: arsenal ASAT actif", "Inde: course spatiale militaire"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "space_militarization",
    confidence_score: 0.78,
    data_sources: ["secure_world_foundation_space_threat", "us_space_command_space_surveillance", "ucs_satellite_database"],
    entities,
    avg_estimated_space_conflict_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
