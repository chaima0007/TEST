import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[urban-heat-crisis-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Urban Heat Crisis Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/urban-heat-crisis-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Urban Heat Crisis Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Urban Heat Crisis Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "UH-001", name: "Baghdad & Bassora — Villes au-delà du Vivable", country: "MENA", sector: "50°C Estivaux & Coupures Électriques Chroniques — Exode Thermique", composite_score: 90.0, peak_temperature_score: 95.0, cooling_infrastructure_deficit_score: 90.0, social_vulnerability_score: 88.0, energy_grid_saturation_score: 85.0, risk_level: "critique", primary_pattern: "zone_inhabitabilite_imminente", key_signals: ["Crise de chaleur urbaine critique dans Baghdad & Bassora — températures extrêmes menaçant la vie humaine et la stabilité", "Déficit d'infrastructure de refroidissement — populations vulnérables sans accès à la climatisation ou à l'eau", "Spirale thermique-énergétique — demande de refroidissement saturant les réseaux et amplifiant le réchauffement"], estimated_heat_crisis_index: 9.0, last_updated: "2026-06-20" },
    { id: "UH-002", name: "Karachi & Delhi — Méga-Cités Thermiques", country: "Asie du Sud", sector: "Canicules Meurtrières 45-50°C — Bidonvilles sans Climatisation", composite_score: 87.25, peak_temperature_score: 90.0, cooling_infrastructure_deficit_score: 85.0, social_vulnerability_score: 92.0, energy_grid_saturation_score: 80.0, risk_level: "critique", primary_pattern: "migration_thermique_forcee", key_signals: ["Crise de chaleur urbaine critique dans Karachi & Delhi — températures extrêmes menaçant la vie humaine et la stabilité", "Déficit d'infrastructure de refroidissement — populations vulnérables sans accès à la climatisation ou à l'eau", "Spirale thermique-énergétique — demande de refroidissement saturant les réseaux et amplifiant le réchauffement"], estimated_heat_crisis_index: 8.73, last_updated: "2026-06-20" },
    { id: "UH-003", name: "Phoenix & Las Vegas — Déserts Urbanisés", country: "Amérique du Nord", sector: "55°C Sol, Étalement Urbain & Dépendance Totale à la Climatisation", composite_score: 80.15, peak_temperature_score: 88.0, cooling_infrastructure_deficit_score: 78.0, social_vulnerability_score: 65.0, energy_grid_saturation_score: 90.0, risk_level: "critique", primary_pattern: "zone_inhabitabilite_imminente", key_signals: ["Crise de chaleur urbaine critique dans Phoenix & Las Vegas — températures extrêmes menaçant la vie humaine et la stabilité", "Déficit d'infrastructure de refroidissement — populations vulnérables sans accès à la climatisation ou à l'eau", "Spirale thermique-énergétique — demande de refroidissement saturant les réseaux et amplifiant le réchauffement"], estimated_heat_crisis_index: 8.02, last_updated: "2026-06-20" },
    { id: "UH-004", name: "Lagos & Accra — Côtes d'Afrique Tropicale", country: "Afrique de l'Ouest", sector: "Chaleur Tropicale & Humidité — Villes de 15M+ sans Infrastructure Froide", composite_score: 82.25, peak_temperature_score: 82.0, cooling_infrastructure_deficit_score: 88.0, social_vulnerability_score: 85.0, energy_grid_saturation_score: 72.0, risk_level: "critique", primary_pattern: "zone_inhabitabilite_imminente", key_signals: ["Crise de chaleur urbaine critique dans Lagos & Accra — températures extrêmes menaçant la vie humaine et la stabilité", "Déficit d'infrastructure de refroidissement — populations vulnérables sans accès à la climatisation ou à l'eau", "Spirale thermique-énergétique — demande de refroidissement saturant les réseaux et amplifiant le réchauffement"], estimated_heat_crisis_index: 8.23, last_updated: "2026-06-20" },
    { id: "UH-005", name: "Shanghai & Chongqing — Fours Urbains", country: "Asie", sector: "45°C Estivaux & 400M de Climatiseurs — Spirale Énergétique-Thermique", composite_score: 47.75, peak_temperature_score: 50.0, cooling_infrastructure_deficit_score: 45.0, social_vulnerability_score: 42.0, energy_grid_saturation_score: 55.0, risk_level: "élevé", primary_pattern: "stress_energetique_thermique", key_signals: ["Stress thermique urbain sévère dans Shanghai & Chongqing — vagues de chaleur récurrentes sans adaptation suffisante", "Inégalités d'accès au refroidissement — pauvres surexposés à la chaleur dans des logements non-climatisés", "Réseau électrique sous tension maximale lors des pics de chaleur — risques de pannes en cascade"], estimated_heat_crisis_index: 4.78, last_updated: "2026-06-20" },
    { id: "UH-006", name: "Madrid & Athènes — Méditerranée Brûlante", country: "Europe du Sud", sector: "Canicules Annuelles & Vieux Bâtiments Non-Isolés — Mortalité Estivale", composite_score: 43.25, peak_temperature_score: 45.0, cooling_infrastructure_deficit_score: 42.0, social_vulnerability_score: 45.0, energy_grid_saturation_score: 40.0, risk_level: "élevé", primary_pattern: "stress_energetique_thermique", key_signals: ["Stress thermique urbain sévère dans Madrid & Athènes — vagues de chaleur récurrentes sans adaptation suffisante", "Inégalités d'accès au refroidissement — pauvres surexposés à la chaleur dans des logements non-climatisés", "Réseau électrique sous tension maximale lors des pics de chaleur — risques de pannes en cascade"], estimated_heat_crisis_index: 4.33, last_updated: "2026-06-20" },
    { id: "UH-007", name: "São Paulo & Rio — Chaleur Inégalitaire", country: "Amériques", sector: "Favelas Surchauffées vs Quartiers Climatisés — Apartheid Thermique", composite_score: 37.25, peak_temperature_score: 35.0, cooling_infrastructure_deficit_score: 38.0, social_vulnerability_score: 45.0, energy_grid_saturation_score: 30.0, risk_level: "modéré", primary_pattern: "inegalites_thermiques", key_signals: ["Risques de chaleur urbaine dans São Paulo & Rio — tendances au réchauffement nécessitant adaptation préventive", "Végétalisation urbaine insuffisante — manque d'espaces verts aggravant l'effet d'îlot de chaleur", "Plans d'adaptation climatique en développement — délais de mise en œuvre à accélérer"], estimated_heat_crisis_index: 3.73, last_updated: "2026-06-20" },
    { id: "UH-008", name: "Singapour & Rotterdam — Adaptation Exemplaire", country: "Asie/Europe", sector: "Architecture Bioclimatique, Toits Verts & Refroidissement District", composite_score: 12.5, peak_temperature_score: 18.0, cooling_infrastructure_deficit_score: 12.0, social_vulnerability_score: 10.0, energy_grid_saturation_score: 8.0, risk_level: "faible", primary_pattern: "adaptation_reussie", key_signals: ["Singapour & Rotterdam a réussi son adaptation urbaine à la chaleur — végétalisation, architecture bioclimatique et réseaux résilients", "Infrastructure de refroidissement accessible à tous — climatisation publique et espaces rafraîchissants inclusifs", "Modèle d'adaptation thermique urbaine à partager — réduction de l'îlot de chaleur par design urbain"], estimated_heat_crisis_index: 1.25, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { zone_inhabitabilite_imminente: 3, migration_thermique_forcee: 1, stress_energetique_thermique: 2, inegalites_thermiques: 1, adaptation_reussie: 1 },
    top_risk_entities: ["Baghdad & Bassora — Villes au-delà du Vivable", "Lagos & Accra — Côtes d'Afrique Tropicale", "Karachi & Delhi — Méga-Cités Thermiques"],
    critical_alerts: ["Baghdad & Bassora: zone d'inhabitabilité imminente", "Lagos & Accra: zone d'inhabitabilité imminente", "Karachi & Delhi: migration thermique forcée", "Phoenix & Las Vegas: zone d'inhabitabilité imminente"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "urban_heat",
    confidence_score: 0.87,
    data_sources: ["copernicus_climate_change_service", "urban_heat_island_effect_monitor", "who_heat_health_action_plans"],
    entities,
    avg_estimated_heat_crisis_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
