import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[criminal-state-capture-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Criminal State Capture Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/criminal-state-capture-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Criminal State Capture Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Criminal State Capture Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "CS-001", name: "Mexique — Cartels comme Co-Gouvernants", country: "Amériques", sector: "Sinaloa & CJNG Contrôlant États Entiers — Narco-État Partiel", composite_score: 86.65, criminal_territorial_control_score: 90.0, institutional_penetration_score: 85.0, illicit_economy_dominance_score: 88.0, judicial_capture_score: 82.0, risk_level: "critique", primary_pattern: "narco_etat_avere", key_signals: ["Capture criminelle avancée dans Mexique — organisations criminelles contrôlant des pans entiers de l'État", "Territoires sous contrôle criminel — État incapable d'exercer son autorité dans des zones entières", "Justice capturée — juges, procureurs et forces de l'ordre sous influence directe des organisations criminelles"], estimated_capture_index: 8.67, last_updated: "2026-06-20" },
    { id: "CS-002", name: "Guinée-Bissau — 1er Narco-État Africain", country: "Afrique de l'Ouest", sector: "Cocaïne Sud-Américaine Transitant & Finançant l'Armée au Pouvoir", composite_score: 83.85, criminal_territorial_control_score: 82.0, institutional_penetration_score: 88.0, illicit_economy_dominance_score: 85.0, judicial_capture_score: 80.0, risk_level: "critique", primary_pattern: "narco_etat_avere", key_signals: ["Capture criminelle avancée dans Guinée-Bissau — organisations criminelles contrôlant des pans entiers de l'État", "Territoires sous contrôle criminel — État incapable d'exercer son autorité dans des zones entières", "Justice capturée — juges, procureurs et forces de l'ordre sous influence directe des organisations criminelles"], estimated_capture_index: 8.39, last_updated: "2026-06-20" },
    { id: "CS-003", name: "Russie — Oligarchie Mafieuse d'État", country: "Europe de l'Est", sector: "Siloviki & Oligarques — Fusion Criminalité Organisée et Pouvoir d'État", composite_score: 79.6, criminal_territorial_control_score: 70.0, institutional_penetration_score: 80.0, illicit_economy_dominance_score: 92.0, judicial_capture_score: 78.0, risk_level: "critique", primary_pattern: "oligarchie_mafieuse", key_signals: ["Capture criminelle avancée dans Russie — organisations criminelles contrôlant des pans entiers de l'État", "Territoires sous contrôle criminel — État incapable d'exercer son autorité dans des zones entières", "Justice capturée — juges, procureurs et forces de l'ordre sous influence directe des organisations criminelles"], estimated_capture_index: 7.96, last_updated: "2026-06-20" },
    { id: "CS-004", name: "Myanmar — Junte & Économie de Drogue", country: "Asie du Sud-Est", sector: "Triangle d'Or — Armée Contrôlant Méthamphétamine comme Source de Financement", composite_score: 80.65, criminal_territorial_control_score: 85.0, institutional_penetration_score: 78.0, illicit_economy_dominance_score: 85.0, judicial_capture_score: 72.0, risk_level: "critique", primary_pattern: "narco_etat_avere", key_signals: ["Capture criminelle avancée dans Myanmar — organisations criminelles contrôlant des pans entiers de l'État", "Territoires sous contrôle criminel — État incapable d'exercer son autorité dans des zones entières", "Justice capturée — juges, procureurs et forces de l'ordre sous influence directe des organisations criminelles"], estimated_capture_index: 8.07, last_updated: "2026-06-20" },
    { id: "CS-005", name: "Honduras & El Salvador — États Post-Capture", country: "Amériques", sector: "Maras Ayant Pénétré Police & Politique — Bukele à El Salvador", composite_score: 53.0, criminal_territorial_control_score: 55.0, institutional_penetration_score: 52.0, illicit_economy_dominance_score: 50.0, judicial_capture_score: 55.0, risk_level: "élevé", primary_pattern: "infiltration_institutionnelle", key_signals: ["Infiltration institutionnelle significative dans Honduras & El Salvador — criminalité organisée corrompant les institutions clés", "Économie illicite importante — narcotrafic, contrebande ou blanchiment représentant une part du PIB", "Système judiciaire partiellement compromis — impunité des acteurs criminels connectés au pouvoir"], estimated_capture_index: 5.3, last_updated: "2026-06-20" },
    { id: "CS-006", name: "Albanie & Macédoine du Nord — Balkans Criminels", country: "Europe du Sud-Est", sector: "Trafic Drogue & Humains avec Complicité Partielle des Institutions", composite_score: 54.15, criminal_territorial_control_score: 50.0, institutional_penetration_score: 55.0, illicit_economy_dominance_score: 60.0, judicial_capture_score: 52.0, risk_level: "élevé", primary_pattern: "infiltration_institutionnelle", key_signals: ["Infiltration institutionnelle significative dans Albanie & Macédoine du Nord — criminalité organisée corrompant les institutions clés", "Économie illicite importante — narcotrafic, contrebande ou blanchiment représentant une part du PIB", "Système judiciaire partiellement compromis — impunité des acteurs criminels connectés au pouvoir"], estimated_capture_index: 5.42, last_updated: "2026-06-20" },
    { id: "CS-007", name: "Nigeria — État Fédéral Fragilisé par Boko Haram/EFCC", country: "Afrique de l'Ouest", sector: "Corruption Pétrolière & Boko Haram Contrôlant le Nord-Est — Fragilité", composite_score: 28.3, criminal_territorial_control_score: 28.0, institutional_penetration_score: 32.0, illicit_economy_dominance_score: 30.0, judicial_capture_score: 22.0, risk_level: "modéré", primary_pattern: "corruption_systemique", key_signals: ["Risques de capture criminelle dans Nigeria — corruption systémique fragilisant les institutions", "Infiltration partielle des administrations locales par des réseaux criminels organisés", "Économie grise significative — risque de normalisation de l'illicite dans les circuits économiques"], estimated_capture_index: 2.83, last_updated: "2026-06-20" },
    { id: "CS-008", name: "Suisse & Pays-Bas — Résistance Exemplaire", country: "Europe", sector: "Droit Pénal Robuste et FIOD/MROS contre Blanchiment & Crime Organisé", composite_score: 5.8, criminal_territorial_control_score: 5.0, institutional_penetration_score: 8.0, illicit_economy_dominance_score: 6.0, judicial_capture_score: 4.0, risk_level: "faible", primary_pattern: "etat_de_droit_resilient", key_signals: ["Suisse & Pays-Bas maintient un État de droit résilient — institutions indépendantes résistant à la capture criminelle", "Justice indépendante et effective contre la criminalité organisée — poursuites effectives des acteurs criminels", "Modèle de résistance à la capture criminelle — transparence institutionnelle et société civile vigilante"], estimated_capture_index: 0.58, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { narco_etat_avere: 3, oligarchie_mafieuse: 1, infiltration_institutionnelle: 2, corruption_systemique: 1, etat_de_droit_resilient: 1 },
    top_risk_entities: ["Mexique — Cartels comme Co-Gouvernants", "Guinée-Bissau — 1er Narco-État Africain", "Myanmar — Junte & Économie de Drogue"],
    critical_alerts: ["Mexique: narco-État avéré", "Guinée-Bissau: narco-État avéré", "Russie: oligarchie mafieuse", "Myanmar: narco-État avéré"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "criminal_capture",
    confidence_score: 0.79,
    data_sources: ["global_initiative_against_transnational_crime", "transparency_international_capture_index", "unodc_crime_statistics"],
    entities,
    avg_estimated_capture_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
