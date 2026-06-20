import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[water-wars-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Water Wars Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/water-wars-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Water Wars Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Water Wars Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "WW-001", name: "Égypte/Éthiopie/Soudan — Guerre du Nil GERD", country: "Afrique de l'Est", sector: "GERD Barrage 145Mds m³ Menaçant l'Existence Hydrique de l'Égypte", composite_score: 86.25, transboundary_water_dispute_score: 88.0, dam_weaponization_score: 92.0, water_scarcity_political_score: 85.0, riparian_conflict_score: 78.0, risk_level: "critique", primary_pattern: "guerre_eau_active", key_signals: ["Guerre de l'eau imminente autour de Égypte/Éthiopie/Soudan — Guerre du Nil GERD — conflits hydriques menaçant la survie et la stabilité régionale", "Weaponisation des barrages — réduction unilatérale des débits fluviaux comme levier de coercition géopolitique", "Stress hydrique existentiel — populations et économies entières dépendant d'un fleuve contesté ou capturé"], estimated_water_conflict_index: 8.63, last_updated: "2026-06-20" },
    { entity_id: "WW-002", name: "Inde/Pakistan — Traité Indus sous Tension Nucléaire", country: "Asie du Sud", sector: "Traité 1960 Contesté — Conflits Himalayens & Guerres de l'Eau Nucléaires", composite_score: 81.35, transboundary_water_dispute_score: 82.0, dam_weaponization_score: 75.0, water_scarcity_political_score: 88.0, riparian_conflict_score: 80.0, risk_level: "critique", primary_pattern: "crise_eau_vitale", key_signals: ["Guerre de l'eau imminente autour de Inde/Pakistan — Traité Indus sous Tension Nucléaire — conflits hydriques menaçant la survie et la stabilité régionale", "Weaponisation des barrages — réduction unilatérale des débits fluviaux comme levier de coercition géopolitique", "Stress hydrique existentiel — populations et économies entières dépendant d'un fleuve contesté ou capturé"], estimated_water_conflict_index: 8.14, last_updated: "2026-06-20" },
    { entity_id: "WW-003", name: "Turquie — Barrages Atatürk & Contrôle Euphrate-Tigre", country: "MENA", sector: "Ilısu & Atatürk Réduisant le Débit Irakien et Syrien à Sa Guise", composite_score: 81.5, transboundary_water_dispute_score: 80.0, dam_weaponization_score: 88.0, water_scarcity_political_score: 82.0, riparian_conflict_score: 75.0, risk_level: "critique", primary_pattern: "guerre_eau_active", key_signals: ["Guerre de l'eau imminente autour de Turquie — Barrages Atatürk & Contrôle Euphrate-Tigre — conflits hydriques menaçant la survie et la stabilité régionale", "Weaponisation des barrages — réduction unilatérale des débits fluviaux comme levier de coercition géopolitique", "Stress hydrique existentiel — populations et économies entières dépendant d'un fleuve contesté ou capturé"], estimated_water_conflict_index: 8.15, last_updated: "2026-06-20" },
    { entity_id: "WW-004", name: "Chine — Maître des Sources des Grands Fleuves Asiatiques", country: "Asie", sector: "8 Fleuves Majeurs (Mékong, Brahmapoutre) Contrôlés & Barrages en Cascade", composite_score: 80.0, transboundary_water_dispute_score: 85.0, dam_weaponization_score: 82.0, water_scarcity_political_score: 72.0, riparian_conflict_score: 80.0, risk_level: "critique", primary_pattern: "guerre_eau_active", key_signals: ["Guerre de l'eau imminente autour de Chine — Maître des Sources des Grands Fleuves Asiatiques — conflits hydriques menaçant la survie et la stabilité régionale", "Weaponisation des barrages — réduction unilatérale des débits fluviaux comme levier de coercition géopolitique", "Stress hydrique existentiel — populations et économies entières dépendant d'un fleuve contesté ou capturé"], estimated_water_conflict_index: 8.0, last_updated: "2026-06-20" },
    { entity_id: "WW-005", name: "Israël/Palestine/Jordanie — Aquifère Cisjordanie Capturé", country: "MENA", sector: "Eau comme Outil de Contrôle — Colons 3x Plus d'Eau que Palestiniens", composite_score: 58.4, transboundary_water_dispute_score: 60.0, dam_weaponization_score: 55.0, water_scarcity_political_score: 65.0, riparian_conflict_score: 52.0, risk_level: "élevé", primary_pattern: "stress_hydrique_conflictuel", key_signals: ["Stress hydrique politisé dans Israël/Palestine/Jordanie — Aquifère Cisjordanie Capturé — tensions bilatérales sévères sur le partage des ressources en eau", "Contestation des traités hydrauliques — remise en cause des accords de partage sous pression démographique et climatique", "Risque d'escalade hydrique — incidents frontaliers autour des infrastructures hydrauliques stratégiques"], estimated_water_conflict_index: 5.84, last_updated: "2026-06-20" },
    { entity_id: "WW-006", name: "Mexique/USA — Colorado River Épuisé Avant la Mer", country: "Amériques", sector: "Conflits Frontaliers Hydrique & Delta Colorado Mort — Traité de 1944 Obsolète", composite_score: 46.9, transboundary_water_dispute_score: 48.0, dam_weaponization_score: 42.0, water_scarcity_political_score: 52.0, riparian_conflict_score: 45.0, risk_level: "élevé", primary_pattern: "stress_hydrique_conflictuel", key_signals: ["Stress hydrique politisé dans Mexique/USA — Colorado River Épuisé Avant la Mer — tensions bilatérales sévères sur le partage des ressources en eau", "Contestation des traités hydrauliques — remise en cause des accords de partage sous pression démographique et climatique", "Risque d'escalade hydrique — incidents frontaliers autour des infrastructures hydrauliques stratégiques"], estimated_water_conflict_index: 4.69, last_updated: "2026-06-20" },
    { entity_id: "WW-007", name: "Espagne/Portugal — Tensions Ibériques Tejo-Douro", country: "Europe du Sud", sector: "Sécheresses Ibériques & Conventions de l'Albufeira Insuffisantes", composite_score: 26.9, transboundary_water_dispute_score: 28.0, dam_weaponization_score: 22.0, water_scarcity_political_score: 32.0, riparian_conflict_score: 25.0, risk_level: "modéré", primary_pattern: "tensions_ripariennes", key_signals: ["Tensions ripariennes dans Espagne/Portugal — Tensions Ibériques Tejo-Douro — conflits d'usage gérés mais vulnérables à la pression climatique", "Négociations hydrauliques fragiles — cadre institutionnel insuffisant face aux besoins croissants en eau", "Surveillance hydrologique nécessaire — risques de dérapage sous pression de la sécheresse et de la croissance démographique"], estimated_water_conflict_index: 2.69, last_updated: "2026-06-20" },
    { entity_id: "WW-008", name: "Suisse/UE — Gestion Exemplaire des Alpes Hydrauliques", country: "Europe", sector: "Convention de l'UNECE & Gestion Coopérative des Bassins Versants Alpins", composite_score: 7.35, transboundary_water_dispute_score: 8.0, dam_weaponization_score: 5.0, water_scarcity_political_score: 10.0, riparian_conflict_score: 6.0, risk_level: "faible", primary_pattern: "cooperation_hydraulique", key_signals: ["Suisse/UE — Gestion Exemplaire des Alpes Hydrauliques gère ses ressources hydriques de manière coopérative et équitable", "Conventions de bassin versant respectées — partage transparent et institutionnalisé des eaux transfrontalières", "Modèle de coopération hydraulique internationale à diffuser — gouvernance inclusive et durable de l'eau"], estimated_water_conflict_index: 0.74, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { guerre_eau_active: 3, crise_eau_vitale: 1, stress_hydrique_conflictuel: 2, tensions_ripariennes: 1, cooperation_hydraulique: 1 },
    top_risk_entities: ["Égypte/Éthiopie/Soudan — Guerre du Nil GERD", "Turquie — Barrages Atatürk & Contrôle Euphrate-Tigre", "Inde/Pakistan — Traité Indus sous Tension Nucléaire"],
    critical_alerts: ["Égypte/Éthiopie/Soudan: guerre eau active", "Inde/Pakistan: crise eau vitale", "Turquie: guerre eau active", "Chine: guerre eau active"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "water_war",
    confidence_score: 0.85,
    data_sources: ["fao_aquastat_water_resources", "world_resources_institute_aqueduct", "pacific_institute_water_conflict_chronology"],
    entities,
    avg_estimated_water_conflict_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
