import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[space-warfare-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Space Warfare Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/space-warfare-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Space Warfare Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Space Warfare Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "SW-001", name: "USA — Space Force ASAT & Constellation GPS/Starlink", country: "Amérique du Nord", sector: "Space Force 2019 16Md$ Budget, GPS 31 Satellites Critiques, Starlink 6000+ & ASAT Direct Ascent", composite_score: 86.5, anti_satellite_capability_score: 92.0, orbital_dominance_score: 95.0, space_debris_weaponization_score: 75.0, gps_jamming_spoofing_score: 82.0, risk_level: "critique", primary_pattern: "domination_orbitale_militaire", key_signals: ["Domination orbitale militaire de USA — Space Force opérationnel avec capacités ASAT et constellation Starlink offrant surveillance et communications sécurisées sans équivalent", "Weaponisation de l'orbite — satellites co-orbitaux offensifs, GPS spoofing tactique et arsenal de destruction orbitale prêt à l'emploi", "Course aux armements spatiaux systémique — investissements massifs dans le Space Force, lasers orbitaux et missiles ASAT de nouvelle génération"], estimated_space_warfare_index: 8.65, last_updated: "2026-06-20" },
    { id: "SW-002", name: "Chine — ASAT SC-19 & Satellites Co-Orbitaux Furtifs", country: "Asie", sector: "Test ASAT 2007 3000 Débris, Satellites Co-Orbitaux Offensifs, BeiDou 35 Satellites & Lasers Anti-Satellite", composite_score: 84.15, anti_satellite_capability_score: 88.0, orbital_dominance_score: 85.0, space_debris_weaponization_score: 82.0, gps_jamming_spoofing_score: 80.0, risk_level: "critique", primary_pattern: "domination_orbitale_militaire", key_signals: ["Domination orbitale militaire de Chine — ASAT SC-19 opérationnel, satellites co-orbitaux furtifs et BeiDou comme alternative stratégique au GPS américain", "Weaponisation de l'orbite — satellites co-orbitaux offensifs, GPS spoofing tactique et arsenal de destruction orbitale prêt à l'emploi", "Course aux armements spatiaux systémique — investissements massifs dans le Space Force, lasers orbitaux et missiles ASAT de nouvelle génération"], estimated_space_warfare_index: 8.42, last_updated: "2026-06-20" },
    { id: "SW-003", name: "Russie — Nudol ASAT & Guerre Électronique Orbitale", country: "Europe de l'Est", sector: "Test Nudol 2021 1500 Débris, GLONASS Spoofing Syrie/Finlande, Satellites Espion Kosmos & Brouilleurs GPS", composite_score: 83.0, anti_satellite_capability_score: 85.0, orbital_dominance_score: 78.0, space_debris_weaponization_score: 92.0, gps_jamming_spoofing_score: 75.0, risk_level: "critique", primary_pattern: "destruction_anti_satellite", key_signals: ["Domination orbitale militaire de Russie — test Nudol 2021 créant 1500 débris dangereux pour l'ISS, brouillage GPS actif en Syrie et Finlande", "Weaponisation de l'orbite — satellites co-orbitaux offensifs, GPS spoofing tactique et arsenal de destruction orbitale prêt à l'emploi", "Course aux armements spatiaux systémique — investissements massifs dans le Space Force, lasers orbitaux et missiles ASAT de nouvelle génération"], estimated_space_warfare_index: 8.3, last_updated: "2026-06-20" },
    { id: "SW-004", name: "Inde — Mission Shakti & Programme Spatial Militaire", country: "Asie du Sud", sector: "Mission Shakti ASAT 2019, ISRO Militarisation Croissante, Satellites ISR & Défense Anti-Missiles Orbitale", composite_score: 65.35, anti_satellite_capability_score: 72.0, orbital_dominance_score: 68.0, space_debris_weaponization_score: 55.0, gps_jamming_spoofing_score: 65.0, risk_level: "critique", primary_pattern: "competition_spatiale_strategique", key_signals: ["Domination orbitale militaire de Inde — Mission Shakti ASAT 2019 en orbite basse et programme spatial militaire croissant via l'ISRO", "Weaponisation de l'orbite — satellites co-orbitaux offensifs, GPS spoofing tactique et arsenal de destruction orbitale prêt à l'emploi", "Course aux armements spatiaux systémique — investissements massifs dans le Space Force, lasers orbitaux et missiles ASAT de nouvelle génération"], estimated_space_warfare_index: 6.54, last_updated: "2026-06-20" },
    { id: "SW-005", name: "Iran & RPDC — Satellites Militaires & GPS Spoofing", country: "MENA/Asie", sector: "RPDC Satellite Reconn. Malligyong-1, Iran Pars 1 Militaire, GPS Spoofing Golfe Persique & Cyber Orbital", composite_score: 46.8, anti_satellite_capability_score: 48.0, orbital_dominance_score: 42.0, space_debris_weaponization_score: 38.0, gps_jamming_spoofing_score: 62.0, risk_level: "élevé", primary_pattern: "competition_spatiale_strategique", key_signals: ["Compétition spatiale stratégique de Iran & RPDC — développement actif de capacités offensives spatiales sans domination orbitale établie", "Militarisation croissante — satellites de renseignement, capacités de brouillage GPS et missiles anti-satellites en cours de développement", "Risque d'escalade orbitale — toute destruction de satellite pourrait créer des débris menaçant l'ensemble des actifs spatiaux civils et militaires"], estimated_space_warfare_index: 4.68, last_updated: "2026-06-20" },
    { id: "SW-006", name: "France & UE — Espace Militaire Émergent", country: "Europe", sector: "Syracuse 4A/4B Militaires, Composante Spatiale Opérationnelle, Laser DEW Sirius & Surveillance Orbitale", composite_score: 40.65, anti_satellite_capability_score: 40.0, orbital_dominance_score: 45.0, space_debris_weaponization_score: 28.0, gps_jamming_spoofing_score: 52.0, risk_level: "élevé", primary_pattern: "competition_spatiale_strategique", key_signals: ["Compétition spatiale stratégique de France & UE — investissement dans une Composante Spatiale Opérationnelle et capacités de surveillance orbitale défensives", "Militarisation croissante — satellites de renseignement, capacités de brouillage GPS et missiles anti-satellites en cours de développement", "Risque d'escalade orbitale — toute destruction de satellite pourrait créer des débris menaçant l'ensemble des actifs spatiaux civils et militaires"], estimated_space_warfare_index: 4.07, last_updated: "2026-06-20" },
    { id: "SW-007", name: "Japon & Australie — Partenaires Spatiaux USA", country: "Asie-Pacifique", sector: "JAXA Dual-Use Spatial, Australie Space Command, Accords Five Eyes Spatiale & Satellites ISR Partagés", composite_score: 28.5, anti_satellite_capability_score: 30.0, orbital_dominance_score: 28.0, space_debris_weaponization_score: 22.0, gps_jamming_spoofing_score: 35.0, risk_level: "modéré", primary_pattern: "competition_spatiale_strategique", key_signals: ["Émergence spatiale militaire de Japon & Australie — investissements spatiaux défensifs sans capacités ASAT avérées mais trajectoire inquiétante", "Dépendance satellite croissante — vulnérabilité aux attaques sur les infrastructures spatiales dans un contexte de militarisation accélérée", "Risque de prolifération ASAT — pression pour développer des capacités autonomes face aux menaces des grandes puissances spatiales"], estimated_space_warfare_index: 2.85, last_updated: "2026-06-20" },
    { id: "SW-008", name: "UIT & COPUOS — Gouvernance Spatiale Internationale", country: "Global", sector: "Outer Space Treaty 1967, COPUOS Lignes Directrices Débris, UIT Fréquences & Rescue Agreement Astronautes", composite_score: 4.45, anti_satellite_capability_score: 5.0, orbital_dominance_score: 4.0, space_debris_weaponization_score: 3.0, gps_jamming_spoofing_score: 6.0, risk_level: "faible", primary_pattern: "cooperation_spatiale_exemplaire", key_signals: ["UIT & COPUOS incarne la coopération spatiale exemplaire — respect de l'Outer Space Treaty, transparence des activités spatiales et désarmement orbital", "Usage pacifique de l'espace — satellites civils, coopération scientifique et refus de développer des capacités offensives anti-satellites", "Modèle de gouvernance spatiale — promotion des normes de comportement responsable et financement des mécanismes de déconfliction orbitale"], estimated_space_warfare_index: 0.45, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { domination_orbitale_militaire: 2, destruction_anti_satellite: 1, debris_espace_tactique: 0, competition_spatiale_strategique: 4, cooperation_spatiale_exemplaire: 1 },
    top_risk_entities: ["USA — Space Force ASAT & Constellation GPS/Starlink", "Chine — ASAT SC-19 & Satellites Co-Orbitaux Furtifs", "Russie — Nudol ASAT & Guerre Électronique Orbitale"],
    critical_alerts: ["USA: domination orbitale militaire", "Chine: domination orbitale militaire", "Russie: destruction anti satellite", "Inde: compétition spatiale stratégique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "space_warfare",
    confidence_score: 0.79,
    data_sources: ["secure_world_foundation_space_security", "unidir_space_security_monitor", "us_space_force_strategic_digest"],
    entities,
    avg_estimated_space_warfare_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
