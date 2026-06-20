import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[port-logistics-capture-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Port Logistics Capture Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/port-logistics-capture-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Port Logistics Capture Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Port Logistics Capture Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "PL-001", name: "Sri Lanka — Hambantota Cédé 99 Ans à Chine", country: "Asie du Sud", sector: "Piège Dette CPEC — Hambantota à China Merchants Holdings 99 Ans en 2017", composite_score: 89.1, chinese_port_acquisition_score: 92.0, strategic_chokepoint_control_score: 88.0, logistics_dependency_score: 90.0, dual_use_infrastructure_score: 85.0, risk_level: "critique", primary_pattern: "capture_portuaire_strategique", key_signals: ["Capture portuaire critique dans Sri Lanka — Hambantota Cédé 99 Ans à Chine — infrastructure stratégique sous contrôle ou influence étrangère décisive", "Cession souveraine d'infrastructure logistique — port ou terminal concédé à long terme à un acteur étatique étranger", "Risque de double usage — infrastructure portuaire potentiellement utilisable pour projection militaire adverse"], estimated_port_capture_index: 8.91, last_updated: "2026-06-20" },
    { entity_id: "PL-002", name: "Pakistan — Gwadar CPEC & Présence Navale Chinoise", country: "Asie du Sud", sector: "62Md$ CPEC, Gwadar Port Opéré par Chine & Flotte PLAN en Expansion", composite_score: 86.05, chinese_port_acquisition_score: 88.0, strategic_chokepoint_control_score: 85.0, logistics_dependency_score: 88.0, dual_use_infrastructure_score: 82.0, risk_level: "critique", primary_pattern: "capture_portuaire_strategique", key_signals: ["Capture portuaire critique dans Pakistan — Gwadar CPEC & Présence Navale Chinoise — infrastructure stratégique sous contrôle ou influence étrangère décisive", "Cession souveraine d'infrastructure logistique — port ou terminal concédé à long terme à un acteur étatique étranger", "Risque de double usage — infrastructure portuaire potentiellement utilisable pour projection militaire adverse"], estimated_port_capture_index: 8.61, last_updated: "2026-06-20" },
    { entity_id: "PL-003", name: "Grèce — Pirée COSCO 51% — Porte de l'UE", country: "Europe du Sud", sector: "COSCO 51% Pirée depuis 2016 — Premier Port Européen Sous Contrôle Chinois", composite_score: 79.0, chinese_port_acquisition_score: 80.0, strategic_chokepoint_control_score: 82.0, logistics_dependency_score: 78.0, dual_use_infrastructure_score: 75.0, risk_level: "critique", primary_pattern: "penetration_logistique", key_signals: ["Capture portuaire critique dans Grèce — Pirée COSCO 51% — Porte de l'UE — infrastructure stratégique sous contrôle ou influence étrangère décisive", "Cession souveraine d'infrastructure logistique — port ou terminal concédé à long terme à un acteur étatique étranger", "Risque de double usage — infrastructure portuaire potentiellement utilisable pour projection militaire adverse"], estimated_port_capture_index: 7.9, last_updated: "2026-06-20" },
    { entity_id: "PL-004", name: "Djibouti — Base Militaire Chinoise & Bab-el-Mandeb", country: "Afrique de l'Est", sector: "1ère Base Militaire Chinoise à l'Étranger & 12% Commerce Mondial en Transit", composite_score: 85.25, chinese_port_acquisition_score: 78.0, strategic_chokepoint_control_score: 92.0, logistics_dependency_score: 85.0, dual_use_infrastructure_score: 88.0, risk_level: "critique", primary_pattern: "chokepoint_naval_dual", key_signals: ["Capture portuaire critique dans Djibouti — Base Militaire Chinoise & Bab-el-Mandeb — infrastructure stratégique sous contrôle ou influence étrangère décisive", "Cession souveraine d'infrastructure logistique — port ou terminal concédé à long terme à un acteur étatique étranger", "Risque de double usage — infrastructure portuaire potentiellement utilisable pour projection militaire adverse"], estimated_port_capture_index: 8.53, last_updated: "2026-06-20" },
    { entity_id: "PL-005", name: "Israël — Haïfa SIPG & Pression USA", country: "MENA", sector: "Concession SIPG Port Haïfa — USA Alarmés par Présence Chinoise Côte Maritime", composite_score: 59.6, chinese_port_acquisition_score: 60.0, strategic_chokepoint_control_score: 55.0, logistics_dependency_score: 65.0, dual_use_infrastructure_score: 58.0, risk_level: "élevé", primary_pattern: "penetration_logistique", key_signals: ["Pénétration logistique significative dans Israël — Haïfa SIPG & Pression USA — participations étrangères créant des dépendances stratégiques", "Acquisitions portuaires partielles — prise de positions minoritaires dans des nœuds logistiques critiques", "Surveillance déficiente des investissements étrangers — insuffisance des mécanismes de screening géopolitique"], estimated_port_capture_index: 5.96, last_updated: "2026-06-20" },
    { entity_id: "PL-006", name: "Italie — Trieste & Augusta dans BRI", country: "Europe du Sud", sector: "Mémorandums BRI Ports Trieste/Augusta — Avant Retrait Meloni sous Pression OTAN", composite_score: 53.4, chinese_port_acquisition_score: 55.0, strategic_chokepoint_control_score: 48.0, logistics_dependency_score: 58.0, dual_use_infrastructure_score: 52.0, risk_level: "élevé", primary_pattern: "penetration_logistique", key_signals: ["Pénétration logistique significative dans Italie — Trieste & Augusta dans BRI — participations étrangères créant des dépendances stratégiques", "Acquisitions portuaires partielles — prise de positions minoritaires dans des nœuds logistiques critiques", "Surveillance déficiente des investissements étrangers — insuffisance des mécanismes de screening géopolitique"], estimated_port_capture_index: 5.34, last_updated: "2026-06-20" },
    { entity_id: "PL-007", name: "Allemagne — Hamburg COSCO 24% Réduit", country: "Europe", sector: "Débat National COSCO 35%→24% Hambourg — Compromis sous Pression Sécuritaire", composite_score: 33.1, chinese_port_acquisition_score: 35.0, strategic_chokepoint_control_score: 30.0, logistics_dependency_score: 38.0, dual_use_infrastructure_score: 28.0, risk_level: "modéré", primary_pattern: "vulnerabilite_partielle", key_signals: ["Vulnérabilité portuaire partielle dans Allemagne — Hamburg COSCO 24% Réduit — expositions limitées aux acquisitions étrangères sensibles", "Débat national sur la souveraineté logistique — réévaluation des concessions portuaires sous pression géopolitique", "Mécanismes de screening à renforcer — cadre réglementaire insuffisant face aux stratégies d'acquisition étrangères"], estimated_port_capture_index: 3.31, last_updated: "2026-06-20" },
    { entity_id: "PL-008", name: "USA & Australie — Five Eyes Résistance Acquisitions", country: "Global/Pacifique", sector: "CFIUS/FIRB Bloquant Acquisitions Chinoises & Infrastructure Defense Hardening", composite_score: 5.85, chinese_port_acquisition_score: 6.0, strategic_chokepoint_control_score: 5.0, logistics_dependency_score: 8.0, dual_use_infrastructure_score: 4.0, risk_level: "faible", primary_pattern: "resilience_portuaire", key_signals: ["USA & Australie — Five Eyes Résistance Acquisitions maintient une résilience portuaire exemplaire — résistance aux acquisitions étrangères stratégiques", "Screening rigoureux des investissements dans les infrastructures critiques — blocage des acquisitions géopolitiquement sensibles", "Modèle de souveraineté logistique à partager — gouvernance transparente et indépendante des infrastructures portuaires"], estimated_port_capture_index: 0.59, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { capture_portuaire_strategique: 2, chokepoint_naval_dual: 1, penetration_logistique: 3, vulnerabilite_partielle: 1, resilience_portuaire: 1 },
    top_risk_entities: ["Sri Lanka — Hambantota Cédé 99 Ans à Chine", "Djibouti — Base Militaire Chinoise & Bab-el-Mandeb", "Pakistan — Gwadar CPEC & Présence Navale Chinoise"],
    critical_alerts: ["Sri Lanka: capture portuaire stratégique", "Pakistan: capture portuaire stratégique", "Grèce: pénétration logistique", "Djibouti: chokepoint naval dual"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "port_logistics_capture",
    confidence_score: 0.83,
    data_sources: ["csis_china_port_tracker", "occrp_bri_port_investigation", "c4ads_strategic_infrastructure_monitor"],
    entities,
    avg_estimated_port_capture_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
