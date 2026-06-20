import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[seed-sovereignty-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Seed Sovereignty Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/seed-sovereignty-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Seed Sovereignty Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Seed Sovereignty Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "SS-001", name: "Amérique Centrale & Caraïbes", country: "Amériques", sector: "Monocultures OGM & Brevets Monsanto/Bayer", composite_score: 88.5, corporate_seed_control_score: 92.0, genetic_erosion_score: 88.0, farmer_seed_rights_violation_score: 90.0, gmo_dependency_score: 85.0, risk_level: "critique", primary_pattern: "dependance_semenciere_totale", key_signals: ["Dépendance semencière totale dans Amérique Centrale — souveraineté alimentaire confisquée par les multinationales", "Érosion génétique irréversible — variétés ancestrales disparaissant sous brevets corporatifs", "Agriculteurs condamnés à acheter des semences chaque saison — fin du droit millénaire de replanter"], estimated_seed_risk_index: 8.85, last_updated: "2026-06-20" },
    { entity_id: "SS-002", name: "Afrique Subsaharienne — Semences Hybrides", country: "Afrique", sector: "Green Revolution 2.0 & Perte Variétés Ancestrales", composite_score: 83.5, corporate_seed_control_score: 85.0, genetic_erosion_score: 82.0, farmer_seed_rights_violation_score: 88.0, gmo_dependency_score: 78.0, risk_level: "critique", primary_pattern: "dependance_semenciere_totale", key_signals: ["Dépendance semencière totale dans Afrique Subsaharienne — souveraineté alimentaire confisquée par les multinationales", "Érosion génétique irréversible — variétés ancestrales disparaissant sous brevets corporatifs", "Agriculteurs condamnés à acheter des semences chaque saison — fin du droit millénaire de replanter"], estimated_seed_risk_index: 8.35, last_updated: "2026-06-20" },
    { entity_id: "SS-003", name: "Inde — Coton OGM & Suicide des Agriculteurs", country: "Asie du Sud", sector: "Bt Cotton Monopoly & Dépendance Chimique Totale", composite_score: 83.25, corporate_seed_control_score: 80.0, genetic_erosion_score: 85.0, farmer_seed_rights_violation_score: 82.0, gmo_dependency_score: 88.0, risk_level: "critique", primary_pattern: "erosion_genetique_critique", key_signals: ["Dépendance semencière totale dans Inde — souveraineté alimentaire confisquée par les multinationales", "Érosion génétique irréversible — variétés ancestrales disparaissant sous brevets corporatifs", "Agriculteurs condamnés à acheter des semences chaque saison — fin du droit millénaire de replanter"], estimated_seed_risk_index: 8.33, last_updated: "2026-06-20" },
    { entity_id: "SS-004", name: "USA — Berceau de l'Oligopole Semencier", country: "Amérique du Nord", sector: "Bayer/Corteva/Syngenta/BASF Dominant le Marché", composite_score: 79.6, corporate_seed_control_score: 90.0, genetic_erosion_score: 72.0, farmer_seed_rights_violation_score: 75.0, gmo_dependency_score: 80.0, risk_level: "critique", primary_pattern: "dependance_semenciere_totale", key_signals: ["Dépendance semencière totale dans USA — souveraineté alimentaire confisquée par les multinationales", "Érosion génétique irréversible — variétés ancestrales disparaissant sous brevets corporatifs", "Agriculteurs condamnés à acheter des semences chaque saison — fin du droit millénaire de replanter"], estimated_seed_risk_index: 7.96, last_updated: "2026-06-20" },
    { entity_id: "SS-005", name: "Brésil — Agrobusiness & Soja OGM", country: "Amériques", sector: "96% Soja OGM & Dépendance aux Géants Semenciers", composite_score: 74.6, corporate_seed_control_score: 78.0, genetic_erosion_score: 68.0, farmer_seed_rights_violation_score: 72.0, gmo_dependency_score: 82.0, risk_level: "critique", primary_pattern: "oligopole_semencier", key_signals: ["Oligopole semencier dominant dans Brésil — dépendance croissante aux 4 géants mondiaux", "Biodiversité agricole en déclin accéléré — homogénéisation génétique fragilisant la résilience", "Droits paysans sur les semences érodés par la pression commerciale et les brevets"], estimated_seed_risk_index: 7.46, last_updated: "2026-06-20" },
    { entity_id: "SS-006", name: "Europe — Résistance au Tout-OGM", country: "Europe", sector: "Réglementation OGM Stricte mais Concentration Croissante", composite_score: 41.25, corporate_seed_control_score: 50.0, genetic_erosion_score: 42.0, farmer_seed_rights_violation_score: 38.0, gmo_dependency_score: 35.0, risk_level: "élevé", primary_pattern: "pression_biodiversite", key_signals: ["Pression sur la biodiversité agricole dans Europe — équilibre fragile semences commerciales/paysannes", "Concentration semencière partielle — variétés locales encore présentes mais menacées", "Législation semencière insuffisante pour protéger pleinement la souveraineté des agriculteurs"], estimated_seed_risk_index: 4.13, last_updated: "2026-06-20" },
    { entity_id: "SS-007", name: "Pérou & Bolivie — Patrimoine Andin", country: "Amériques", sector: "Protection des Variétés Ancestrales de Pomme de Terre", composite_score: 24.0, corporate_seed_control_score: 28.0, genetic_erosion_score: 25.0, farmer_seed_rights_violation_score: 22.0, gmo_dependency_score: 18.0, risk_level: "modéré", primary_pattern: "pression_biodiversite", key_signals: ["Pression sur la biodiversité agricole dans Pérou & Bolivie — équilibre fragile semences commerciales/paysannes", "Concentration semencière partielle — variétés locales encore présentes mais menacées", "Législation semencière insuffisante pour protéger pleinement la souveraineté des agriculteurs"], estimated_seed_risk_index: 2.4, last_updated: "2026-06-20" },
    { entity_id: "SS-008", name: "Suisse (FiBL) & Pays-Bas (Wageningen)", country: "Europe", sector: "Recherche Semencière Publique & Biodiversité Exemplaire", composite_score: 11.5, corporate_seed_control_score: 15.0, genetic_erosion_score: 10.0, farmer_seed_rights_violation_score: 12.0, gmo_dependency_score: 8.0, risk_level: "faible", primary_pattern: "souverainete_preservee", key_signals: ["Suisse & Pays-Bas préserve sa souveraineté semencière — biodiversité agricole et droits paysans protégés", "Banques de semences actives et programmes de sélection paysanne opérationnels", "Modèle de résistance à l'oligopole semencier à valoriser et diffuser mondialement"], estimated_seed_risk_index: 1.15, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 5, "élevé": 1, "modéré": 1, faible: 1 },
    pattern_distribution: { dependance_semenciere_totale: 3, erosion_genetique_critique: 1, oligopole_semencier: 1, pression_biodiversite: 2, souverainete_preservee: 1 },
    top_risk_entities: ["Amérique Centrale & Caraïbes", "Afrique Subsaharienne — Semences Hybrides", "Inde — Coton OGM & Suicide des Agriculteurs"],
    critical_alerts: ["Amérique Centrale: dépendance semencière totale", "Afrique Subsaharienne: dépendance semencière totale", "Inde: érosion génétique critique", "USA: dépendance semencière totale", "Brésil: oligopole semencier"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "seed_sovr",
    confidence_score: 0.84,
    data_sources: ["grain_seed_sovereignty_index", "fao_plant_genetic_resources", "eto_corporate_seed_tracker"],
    entities,
    avg_estimated_seed_risk_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
