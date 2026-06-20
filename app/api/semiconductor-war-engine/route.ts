import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[semiconductor-war-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Semiconductor War Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/semiconductor-war-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Semiconductor War Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Semiconductor War Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "SW-001", name: "Taiwan/TSMC — 92% Puces Avancées ≤7nm Mondiales", country: "Asie", sector: "TSMC N2/N3 Process, Apple/Nvidia/AMD Clients & Île Stratégique sous Menace Militaire Chine", composite_score: 86.55, chip_design_monopoly_score: 88.0, fab_technology_control_score: 95.0, export_control_weaponization_score: 72.0, supply_chain_concentration_score: 92.0, risk_level: "critique", primary_pattern: "concentration_fab_critique", key_signals: ["Monopole technologique de Taiwan/TSMC — contrôle de nœuds critiques de la chaîne de valeur semi-conducteurs mondiale", "Weaponisation des puces — semi-conducteurs utilisés comme instrument de pression géopolitique et levier de coercition économique", "Vulnérabilité systémique — concentration extrême exposant l'économie mondiale à des ruptures d'approvisionnement catastrophiques"], estimated_semiconductor_war_index: 8.66, last_updated: "2026-06-20" },
    { entity_id: "SW-002", name: "USA — CHIPS Act & Weaponisation Contrôles Export", country: "Amérique du Nord", sector: "Nvidia H100/B200, ASML EUV Restriction, Entity List Huawei/SMIC & CHIPS Act 52Md$ Intel/TSMC", composite_score: 86.85, chip_design_monopoly_score: 92.0, fab_technology_control_score: 82.0, export_control_weaponization_score: 95.0, supply_chain_concentration_score: 75.0, risk_level: "critique", primary_pattern: "weaponisation_technologique", key_signals: ["Monopole technologique de USA — contrôle de nœuds critiques de la chaîne de valeur semi-conducteurs mondiale", "Weaponisation des puces — semi-conducteurs utilisés comme instrument de pression géopolitique et levier de coercition économique", "Vulnérabilité systémique — concentration extrême exposant l'économie mondiale à des ruptures d'approvisionnement catastrophiques"], estimated_semiconductor_war_index: 8.69, last_updated: "2026-06-20" },
    { entity_id: "SW-003", name: "Chine — SMIC & Plan 150Md$ Autosuffisance 2030", country: "Asie", sector: "SMIC 7nm Limité, Huawei Kirin IA, Plan Made in China 2025 Révisé & Équipements EUV Bloqués", composite_score: 75.6, chip_design_monopoly_score: 85.0, fab_technology_control_score: 68.0, export_control_weaponization_score: 62.0, supply_chain_concentration_score: 88.0, risk_level: "critique", primary_pattern: "course_puces_strategique", key_signals: ["Monopole technologique de Chine — contrôle de nœuds critiques de la chaîne de valeur semi-conducteurs mondiale", "Weaponisation des puces — semi-conducteurs utilisés comme instrument de pression géopolitique et levier de coercition économique", "Vulnérabilité systémique — concentration extrême exposant l'économie mondiale à des ruptures d'approvisionnement catastrophiques"], estimated_semiconductor_war_index: 7.56, last_updated: "2026-06-20" },
    { entity_id: "SW-004", name: "Corée du Sud — Samsung & SK Hynix DRAM HBM", country: "Asie", sector: "Samsung Gate-All-Around 3nm, SK Hynix HBM3E pour IA & Alliance Chip4 sous Pression", composite_score: 77.6, chip_design_monopoly_score: 80.0, fab_technology_control_score: 88.0, export_control_weaponization_score: 72.0, supply_chain_concentration_score: 68.0, risk_level: "critique", primary_pattern: "monopole_fabrication_avancee", key_signals: ["Monopole technologique de Corée du Sud — contrôle de nœuds critiques de la chaîne de valeur semi-conducteurs mondiale", "Weaponisation des puces — semi-conducteurs utilisés comme instrument de pression géopolitique et levier de coercition économique", "Vulnérabilité systémique — concentration extrême exposant l'économie mondiale à des ruptures d'approvisionnement catastrophiques"], estimated_semiconductor_war_index: 7.76, last_updated: "2026-06-20" },
    { entity_id: "SW-005", name: "Pays-Bas — ASML EUV Seul Fabricant Mondial", country: "Europe", sector: "ASML EUV 0.33NA & 0.55NA Monopole, Restriction Export Chine & Pression USA sur DUV", composite_score: 57.35, chip_design_monopoly_score: 55.0, fab_technology_control_score: 60.0, export_control_weaponization_score: 65.0, supply_chain_concentration_score: 48.0, risk_level: "élevé", primary_pattern: "course_puces_strategique", key_signals: ["Course technologique de Pays-Bas — investissements massifs dans les semi-conducteurs pour réduire la dépendance stratégique", "Rattrapage technologique — développement de capacités nationales face aux restrictions d'exportation adversaires", "Risque de décalage technologique — fossé croissant avec les leaders mondiaux des puces avancées (2nm et inférieur)"], estimated_semiconductor_war_index: 5.74, last_updated: "2026-06-20" },
    { entity_id: "SW-006", name: "Japon — Shin-Etsu, Tokyo Electron & Matériaux", country: "Asie", sector: "Shin-Etsu Silicone 30% Part Mondiale, Tokyo Electron Équipements & Photolithographie Nikon", composite_score: 52.85, chip_design_monopoly_score: 52.0, fab_technology_control_score: 55.0, export_control_weaponization_score: 58.0, supply_chain_concentration_score: 45.0, risk_level: "élevé", primary_pattern: "course_puces_strategique", key_signals: ["Course technologique de Japon — investissements massifs dans les semi-conducteurs pour réduire la dépendance stratégique", "Rattrapage technologique — développement de capacités nationales face aux restrictions d'exportation adversaires", "Risque de décalage technologique — fossé croissant avec les leaders mondiaux des puces avancées (2nm et inférieur)"], estimated_semiconductor_war_index: 5.29, last_updated: "2026-06-20" },
    { entity_id: "SW-007", name: "Inde — Fab21 Tata & Stratégie Semi-Conducteurs", country: "Asie du Sud", sector: "Tata Semiconductor Fab21 Dholera, Micron Mémoire Gujarat & Plan India Semiconductor Mission", composite_score: 29.65, chip_design_monopoly_score: 28.0, fab_technology_control_score: 25.0, export_control_weaponization_score: 32.0, supply_chain_concentration_score: 35.0, risk_level: "modéré", primary_pattern: "course_puces_strategique", key_signals: ["Dépendance structurelle de Inde — vulnérabilité aux disruptions d'approvisionnement en semi-conducteurs avancés", "Absence de capacité de fabrication domestique — dépendance aux importations pour les puces critiques des infrastructures", "Risque de découplage — exposition aux restrictions d'exportation et aux guerres commerciales technologiques"], estimated_semiconductor_war_index: 2.97, last_updated: "2026-06-20" },
    { entity_id: "SW-008", name: "OECD Chip Alliance — Standards & Coopération", country: "Global", sector: "Chip 4 Alliance USA/Japon/Corée/Taiwan, CHIPS EU Act & Standards JEDEC Ouverts", composite_score: 4.6, chip_design_monopoly_score: 5.0, fab_technology_control_score: 6.0, export_control_weaponization_score: 4.0, supply_chain_concentration_score: 3.0, risk_level: "faible", primary_pattern: "resilience_technologique", key_signals: ["OECD Chip Alliance incarne la coopération technologique — standards ouverts, chaînes d'approvisionnement diversifiées et partage de brevets", "Résilience multi-source — approvisionnement diversifié et accords de réciprocité technologique avec les partenaires alliés", "Modèle d'interdépendance saine — commerce libre des technologies non-sensibles et contrôles ciblés sur les applications militaires"], estimated_semiconductor_war_index: 0.46, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { concentration_fab_critique: 1, weaponisation_technologique: 1, monopole_fabrication_avancee: 1, course_puces_strategique: 4, resilience_technologique: 1 },
    top_risk_entities: ["USA — CHIPS Act & Weaponisation Contrôles Export", "Taiwan/TSMC — 92% Puces Avancées ≤7nm Mondiales", "Corée du Sud — Samsung & SK Hynix DRAM HBM"],
    critical_alerts: ["Taiwan/TSMC: concentration fab critique", "USA: weaponisation technologique", "Chine: course puces stratégique", "Corée du Sud: monopole fabrication avancée"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "semiconductor_war",
    confidence_score: 0.81,
    data_sources: ["chips_act_monitor_semianalysis", "semiconductor_industry_association_reports", "csis_tech_war_tracker"],
    entities,
    avg_estimated_semiconductor_war_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
