import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[undersea-cable-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Undersea Cable Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/undersea-cable-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Undersea Cable Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Undersea Cable Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "UC-001", name: "Chine — HMN Tech & 20% Câbles Sous-Marins Mondiaux", country: "Asie", sector: "HMN Technologies Ex-Huawei Marine, PEACE Cable Afrique-Asie & Exclusion Projets USA/EU", composite_score: 86.55, cable_chokepoint_control_score: 88.0, submarine_sabotage_capability_score: 82.0, landing_station_surveillance_score: 85.0, cable_build_monopoly_score: 92.0, risk_level: "critique", primary_pattern: "controle_infrastructure_internet", key_signals: ["Contrôle des infrastructures numériques critiques par Chine — maîtrise des chokepoints câbles et des landing stations mondiales", "Weaponisation des câbles sous-marins — capacité de sabotage, d'interception et de coupure des artères numériques intercontinentales", "Vulnérabilité systémique mondiale — les coupures ciblées pourraient paralyser les marchés financiers et les communications militaires"], estimated_undersea_cable_index: 8.66, last_updated: "2026-06-20" },
    { entity_id: "UC-002", name: "USA — SubCom & Five Eyes Surveillance Câbles", country: "Amérique du Nord", sector: "SubCom 500K km Câbles, GCHQ/NSA Taps Câbles Transatlantiques & FCC Exclusion HMN", composite_score: 84.4, cable_chokepoint_control_score: 85.0, submarine_sabotage_capability_score: 80.0, landing_station_surveillance_score: 90.0, cable_build_monopoly_score: 82.0, risk_level: "critique", primary_pattern: "controle_infrastructure_internet", key_signals: ["Contrôle des infrastructures numériques critiques par USA — maîtrise des chokepoints câbles et des landing stations mondiales", "Weaponisation des câbles sous-marins — capacité de sabotage, d'interception et de coupure des artères numériques intercontinentales", "Vulnérabilité systémique mondiale — les coupures ciblées pourraient paralyser les marchés financiers et les communications militaires"], estimated_undersea_cable_index: 8.44, last_updated: "2026-06-20" },
    { entity_id: "UC-003", name: "Russie — AS-12 Losharik & Sabotage Baltique", country: "Europe de l'Est", sector: "Losharik Sous-Marin Spécial 6000m, BCS East-West Interlink Coupure Oct 2023 & Yantar Navire", composite_score: 78.5, cable_chokepoint_control_score: 75.0, submarine_sabotage_capability_score: 92.0, landing_station_surveillance_score: 80.0, cable_build_monopoly_score: 65.0, risk_level: "critique", primary_pattern: "sabotage_sous_marin_strategique", key_signals: ["Contrôle des infrastructures numériques critiques par Russie — maîtrise des chokepoints câbles et des landing stations mondiales", "Weaponisation des câbles sous-marins — capacité de sabotage, d'interception et de coupure des artères numériques intercontinentales", "Vulnérabilité systémique mondiale — les coupures ciblées pourraient paralyser les marchés financiers et les communications militaires"], estimated_undersea_cable_index: 7.85, last_updated: "2026-06-20" },
    { entity_id: "UC-004", name: "UK & France — GCHQ, Alcatel & Surveillance UKUSA", country: "Europe", sector: "GCHQ Programme Tempora, Alcatel Submarine 200K km & Five Eyes Landing Stations UK", composite_score: 76.2, cable_chokepoint_control_score: 72.0, submarine_sabotage_capability_score: 68.0, landing_station_surveillance_score: 88.0, cable_build_monopoly_score: 78.0, risk_level: "critique", primary_pattern: "course_domination_numerique", key_signals: ["Contrôle des infrastructures numériques critiques par UK & France — maîtrise des chokepoints câbles et des landing stations mondiales", "Weaponisation des câbles sous-marins — capacité de sabotage, d'interception et de coupure des artères numériques intercontinentales", "Vulnérabilité systémique mondiale — les coupures ciblées pourraient paralyser les marchés financiers et les communications militaires"], estimated_undersea_cable_index: 7.62, last_updated: "2026-06-20" },
    { entity_id: "UC-005", name: "Turquie & Détroit Bosphore — Chokepoint Maritime", country: "MENA/Europe", sector: "Bosphore 0km Câbles Alternatifs, Transit Obligatoire & Contrôle Passage Naval Convention Montreux", composite_score: 53.4, cable_chokepoint_control_score: 58.0, submarine_sabotage_capability_score: 52.0, landing_station_surveillance_score: 48.0, cable_build_monopoly_score: 55.0, risk_level: "élevé", primary_pattern: "course_domination_numerique", key_signals: ["Course à la domination numérique de Turquie — investissements stratégiques dans les câbles comme levier de contrôle informationnel", "Diplomatie des câbles — utilisation de la construction de câbles comme outil d'influence et de dépendance des pays partenaires", "Risque de concentration — dépendance croissante à des opérateurs de câbles non alliés pour les flux de données critiques"], estimated_undersea_cable_index: 5.34, last_updated: "2026-06-20" },
    { entity_id: "UC-006", name: "Singapour & Dubaï — Hubs Régionaux Câbles", country: "Asie/MENA", sector: "Singapore Cable Hub Asie-Pacifique, Equinix LD5 London & Dubaï Télécom Landing Stations", composite_score: 50.6, cable_chokepoint_control_score: 52.0, submarine_sabotage_capability_score: 45.0, landing_station_surveillance_score: 55.0, cable_build_monopoly_score: 50.0, risk_level: "élevé", primary_pattern: "course_domination_numerique", key_signals: ["Course à la domination numérique de Singapour & Dubaï — investissements stratégiques dans les câbles comme levier de contrôle informationnel", "Diplomatie des câbles — utilisation de la construction de câbles comme outil d'influence et de dépendance des pays partenaires", "Risque de concentration — dépendance croissante à des opérateurs de câbles non alliés pour les flux de données critiques"], estimated_undersea_cable_index: 5.06, last_updated: "2026-06-20" },
    { entity_id: "UC-007", name: "Taïwan — 14 Câbles Essentiels & Vulnérabilité Stratégique", country: "Asie", sector: "14 Câbles Sous-Marins Vitaux, 2 Coupés par Navires Chinois 2023 & Aucune Redondance Terrestre", composite_score: 29.75, cable_chokepoint_control_score: 30.0, submarine_sabotage_capability_score: 28.0, landing_station_surveillance_score: 35.0, cable_build_monopoly_score: 25.0, risk_level: "modéré", primary_pattern: "course_domination_numerique", key_signals: ["Vulnérabilité câbles de Taïwan — dépendance critique aux câbles sous-marins sans capacité de protection ou redondance adéquate", "Absence de redondance — rupture d'un seul câble peut isoler une région entière des communications numériques mondiales", "Risque d'interception — landing stations peu sécurisées exposant les données nationales à des taps par des puissances adverses"], estimated_undersea_cable_index: 2.98, last_updated: "2026-06-20" },
    { entity_id: "UC-008", name: "ITU & ICPC — Gouvernance Internationale Câbles", country: "Global", sector: "ITU Convention Câbles 1884 Révisée, ICPC Standards & Zones Protection Câbles IMO", composite_score: 4.45, cable_chokepoint_control_score: 5.0, submarine_sabotage_capability_score: 4.0, landing_station_surveillance_score: 3.0, cable_build_monopoly_score: 6.0, risk_level: "faible", primary_pattern: "gouvernance_multilaterale_cables", key_signals: ["ITU & ICPC contribue à la gouvernance multilatérale des câbles — protection légale, coopération internationale et normes de sécurité", "Cadre juridique international — Convention ITU sur la protection des câbles modernisée et attribution rapide des actes de sabotage", "Modèle de résilience à partager — redondance des routes, diversification des propriétaires et plans d'urgence documentés"], estimated_undersea_cable_index: 0.45, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { controle_infrastructure_internet: 2, sabotage_sous_marin_strategique: 1, monopole_construction_cables: 0, course_domination_numerique: 4, gouvernance_multilaterale_cables: 1 },
    top_risk_entities: ["Chine — HMN Tech & 20% Câbles Sous-Marins Mondiaux", "USA — SubCom & Five Eyes Surveillance Câbles", "Russie — AS-12 Losharik & Sabotage Baltique"],
    critical_alerts: ["Chine: contrôle infrastructure internet", "USA: contrôle infrastructure internet", "Russie: sabotage sous-marin stratégique", "UK & France: course domination numérique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "undersea_cable",
    confidence_score: 0.77,
    data_sources: ["telegeography_submarine_cable_map", "submarine_cable_networks_pctelecommunications", "csis_undersea_cable_security"],
    entities,
    avg_estimated_undersea_cable_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
