import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[arctic-geopolitics-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Arctic Geopolitics Engine Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/arctic-geopolitics-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Arctic Geopolitics Engine Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Arctic Geopolitics Engine Agent"), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    { id: "AG-001", name: "Russie — Remilitarisation Arctique & Route du Nord-Est", country: "Europe de l'Est/Arctique", sector: "6 Bases Arctiques, S-400 Polaires, RPMA & Revendications Plateau Continental", composite_score: 88.95, territorial_sovereignty_dispute_score: 92.0, military_buildup_score: 90.0, resource_extraction_rush_score: 85.0, arctic_route_control_score: 88.0, risk_level: "critique", primary_pattern: "militarisation_arctique_active", key_signals: ["Militarisation arctique critique impliquant Russie — Remilitarisation Arctique & Route du Nord-Est — déploiements militaires et revendications souveraines conflictuelles", "Course aux ressources polaires — extraction accélérée d'hydrocarbures et terres rares sous la glace fondante", "Contrôle des routes maritimes arctiques — enjeu stratégique de la Route du Nord-Est et du Passage du Nord-Ouest"], estimated_arctic_tension_index: 8.9, last_updated: "2026-06-20" },
    { id: "AG-002", name: "Chine — Puissance Quasi-Arctique Auto-Proclamée", country: "Asie", sector: "Brise-Glaces Xuelong, Mines Groenland & Route Polaire Maritime Arctique", composite_score: 76.4, territorial_sovereignty_dispute_score: 78.0, military_buildup_score: 72.0, resource_extraction_rush_score: 80.0, arctic_route_control_score: 75.0, risk_level: "critique", primary_pattern: "course_ressources_arctiques", key_signals: ["Militarisation arctique critique impliquant Chine — Puissance Quasi-Arctique Auto-Proclamée — déploiements militaires et revendications souveraines conflictuelles", "Course aux ressources polaires — extraction accélérée d'hydrocarbures et terres rares sous la glace fondante", "Contrôle des routes maritimes arctiques — enjeu stratégique de la Route du Nord-Est et du Passage du Nord-Ouest"], estimated_arctic_tension_index: 7.64, last_updated: "2026-06-20" },
    { id: "AG-003", name: "USA — Alaska, Space Force & Arctic Strategy", country: "Amérique du Nord", sector: "Fort Greely, NORAD Modernisé & Stratégie Arctique Pentagon 2022", composite_score: 74.5, territorial_sovereignty_dispute_score: 75.0, military_buildup_score: 80.0, resource_extraction_rush_score: 72.0, arctic_route_control_score: 70.0, risk_level: "critique", primary_pattern: "positionnement_strategique_arctique", key_signals: ["Militarisation arctique critique impliquant USA — Alaska, Space Force & Arctic Strategy — déploiements militaires et revendications souveraines conflictuelles", "Course aux ressources polaires — extraction accélérée d'hydrocarbures et terres rares sous la glace fondante", "Contrôle des routes maritimes arctiques — enjeu stratégique de la Route du Nord-Est et du Passage du Nord-Ouest"], estimated_arctic_tension_index: 7.45, last_updated: "2026-06-20" },
    { id: "AG-004", name: "Canada — Passage du Nord-Ouest Souverain Contesté", country: "Amériques", sector: "Revendication Eaux Intérieures vs USA + Rangers Canadiens & Bases Nordiques", composite_score: 65.1, territorial_sovereignty_dispute_score: 65.0, military_buildup_score: 58.0, resource_extraction_rush_score: 70.0, arctic_route_control_score: 68.0, risk_level: "critique", primary_pattern: "positionnement_strategique_arctique", key_signals: ["Militarisation arctique critique impliquant Canada — Passage du Nord-Ouest Souverain Contesté — déploiements militaires et revendications souveraines conflictuelles", "Course aux ressources polaires — extraction accélérée d'hydrocarbures et terres rares sous la glace fondante", "Contrôle des routes maritimes arctiques — enjeu stratégique de la Route du Nord-Est et du Passage du Nord-Ouest"], estimated_arctic_tension_index: 6.51, last_updated: "2026-06-20" },
    { id: "AG-005", name: "Norvège — OTAN Arctique & Svalbard sous Pression Russe", country: "Europe du Nord", sector: "Svalbard Militarisé, Frigates F310 & Surveillance Sous-Marine Arctique", composite_score: 53.1, territorial_sovereignty_dispute_score: 52.0, military_buildup_score: 58.0, resource_extraction_rush_score: 48.0, arctic_route_control_score: 55.0, risk_level: "élevé", primary_pattern: "positionnement_strategique_arctique", key_signals: ["Positionnement stratégique arctique de Norvège — OTAN Arctique & Svalbard sous Pression Russe — investissements capacitaires polaires sans conflit ouvert", "Infrastructure polaire duale — brise-glaces, bases et réseaux de surveillance à double usage civil-militaire", "Diplomatie arctique active — négociations sur les plateaux continentaux, ressources et droits de passage"], estimated_arctic_tension_index: 5.31, last_updated: "2026-06-20" },
    { id: "AG-006", name: "Danemark/Groenland — Terres Rares & Indépendance Arctique", country: "Europe du Nord", sector: "Terres Rares Groenlandaises Convoitées — Uranium & Néodyme sous les Glaces", composite_score: 51.5, territorial_sovereignty_dispute_score: 55.0, military_buildup_score: 48.0, resource_extraction_rush_score: 52.0, arctic_route_control_score: 50.0, risk_level: "élevé", primary_pattern: "positionnement_strategique_arctique", key_signals: ["Positionnement stratégique arctique de Danemark/Groenland — Terres Rares & Indépendance Arctique — investissements capacitaires polaires sans conflit ouvert", "Infrastructure polaire duale — brise-glaces, bases et réseaux de surveillance à double usage civil-militaire", "Diplomatie arctique active — négociations sur les plateaux continentaux, ressources et droits de passage"], estimated_arctic_tension_index: 5.15, last_updated: "2026-06-20" },
    { id: "AG-007", name: "Finlande & Suède — OTAN Arctique Nouveau", country: "Europe du Nord", sector: "Adhésion OTAN 2023-2024 & Capacités Défensives Arctiques Nordiques", composite_score: 31.35, territorial_sovereignty_dispute_score: 32.0, military_buildup_score: 35.0, resource_extraction_rush_score: 28.0, arctic_route_control_score: 30.0, risk_level: "modéré", primary_pattern: "integration_otan_arctique", key_signals: ["Intégration OTAN arctique pour Finlande & Suède — OTAN Arctique Nouveau — renforcement défensif face à la militarisation russe et chinoise", "Capacités polaires en développement — acquisition de brise-glaces et stations de surveillance nordiques", "Participation au Conseil Arctique — engagement diplomatique pour préserver la coopération scientifique"], estimated_arctic_tension_index: 3.14, last_updated: "2026-06-20" },
    { id: "AG-008", name: "Coopération Polaire ISA — Science sans Armes", country: "Global", sector: "Programme MOSAIC & Accords Scientifiques Polaires — Recherche Coopérative", composite_score: 5.7, territorial_sovereignty_dispute_score: 5.0, military_buildup_score: 4.0, resource_extraction_rush_score: 8.0, arctic_route_control_score: 6.0, risk_level: "faible", primary_pattern: "cooperation_polaire", key_signals: ["Coopération Polaire ISA — Science sans Armes maintient une présence arctique coopérative et scientifique — engagement non-militaire et transparent", "Respect du Traité de Svalbard et des conventions internationales polaires — multilateralisme arctique", "Modèle de coopération polaire scientifique — partage des données climatiques et environnementales arctiques"], estimated_arctic_tension_index: 0.57, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { militarisation_arctique_active: 1, course_ressources_arctiques: 1, positionnement_strategique_arctique: 4, integration_otan_arctique: 1, cooperation_polaire: 1 },
    top_risk_entities: ["Russie — Remilitarisation Arctique & Route du Nord-Est", "Chine — Puissance Quasi-Arctique Auto-Proclamée", "USA — Alaska, Space Force & Arctic Strategy"],
    critical_alerts: ["Russie: militarisation arctique active", "Chine: course ressources arctiques", "USA: positionnement stratégique arctique", "Canada: positionnement stratégique arctique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "arctic_geopolitics",
    confidence_score: 0.82,
    data_sources: ["arctic_council_monitoring_network", "sipri_arctic_military_database", "nsidc_sea_ice_change_tracker"],
    entities,
    avg_estimated_arctic_tension_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
