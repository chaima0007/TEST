import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[deep-sea-mining-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Deep Sea Mining Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/deep-sea-mining-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Deep Sea Mining Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Deep Sea Mining Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "DS-001", name: "Chine — Zone ZCC Pacifique & Robots Miniers Autonomes", country: "Asie", sector: "5 Contrats ISA, Robots Miniers COMRA & 70% Terres Rares — Domination Minière Globale", composite_score: 86.85, seabed_territorial_claim_score: 92.0, polymetallic_nodule_extraction_score: 88.0, submarine_infrastructure_control_score: 85.0, isa_governance_capture_score: 80.0, risk_level: "critique", primary_pattern: "course_fonds_marins_active", key_signals: ["Course aux fonds marins critique de Chine — programmes d'exploration avancés et stratégie de capture des ressources minières de la Zone", "Robots miniers autonomes déployés — technologies d'extraction des nodules polymétalliques et des sulfures hydrothermaux opérationnelles", "Capture de gouvernance ISA — influence disproportionnée sur l'Autorité Internationale des Fonds Marins pour accélérer les licences d'exploitation"], estimated_deep_sea_index: 8.69, last_updated: "2026-06-20" },
    { entity_id: "DS-002", name: "USA — NOAA & Infrastructure Deep Sea Monopole", country: "Amérique du Nord", sector: "NOAA Exploration, Lockheed Martin Licences & Veto UNCLOS Ratification", composite_score: 82.9, seabed_territorial_claim_score: 85.0, polymetallic_nodule_extraction_score: 90.0, submarine_infrastructure_control_score: 82.0, isa_governance_capture_score: 72.0, risk_level: "critique", primary_pattern: "course_fonds_marins_active", key_signals: ["Course aux fonds marins critique de USA — programmes d'exploration avancés et stratégie de capture des ressources minières de la Zone", "Robots miniers autonomes déployés — technologies d'extraction des nodules polymétalliques et des sulfures hydrothermaux opérationnelles", "Capture de gouvernance ISA — influence disproportionnée sur l'Autorité Internationale des Fonds Marins pour accélérer les licences d'exploitation"], estimated_deep_sea_index: 8.29, last_updated: "2026-06-20" },
    { entity_id: "DS-003", name: "Russie — Zone Atlantique Nord & Câbles Sous-Marins", country: "Europe de l'Est", sector: "ISA Contrat Atlantique, Sous-Marins Surveillance Câbles & Infrastructure Dual-Use", composite_score: 80.35, seabed_territorial_claim_score: 80.0, polymetallic_nodule_extraction_score: 75.0, submarine_infrastructure_control_score: 88.0, isa_governance_capture_score: 78.0, risk_level: "critique", primary_pattern: "infrastructure_sous_marine", key_signals: ["Course aux fonds marins critique de Russie — programmes d'exploration avancés et stratégie de capture des ressources minières de la Zone", "Robots miniers autonomes déployés — technologies d'extraction des nodules polymétalliques et des sulfures hydrothermaux opérationnelles", "Capture de gouvernance ISA — influence disproportionnée sur l'Autorité Internationale des Fonds Marins pour accélérer les licences d'exploitation"], estimated_deep_sea_index: 8.04, last_updated: "2026-06-20" },
    { entity_id: "DS-004", name: "Nauru — Activation Règle 2 Ans & Sponsored Mining", country: "Pacifique", sector: "Nauru Ocean Resources & NORI Déclenchant Règle 2 Ans pour Contourner Moratoire ISA", composite_score: 75.6, seabed_territorial_claim_score: 72.0, polymetallic_nodule_extraction_score: 80.0, submarine_infrastructure_control_score: 68.0, isa_governance_capture_score: 85.0, risk_level: "critique", primary_pattern: "extraction_opportuniste", key_signals: ["Course aux fonds marins critique de Nauru — programmes d'exploration avancés et stratégie de capture des ressources minières de la Zone", "Robots miniers autonomes déployés — technologies d'extraction des nodules polymétalliques et des sulfures hydrothermaux opérationnelles", "Capture de gouvernance ISA — influence disproportionnée sur l'Autorité Internationale des Fonds Marins pour accélérer les licences d'exploitation"], estimated_deep_sea_index: 7.56, last_updated: "2026-06-20" },
    { entity_id: "DS-005", name: "Norvège — Ouverture Fonds Marins Arctique", country: "Europe du Nord", sector: "Licences Arctiques Controversées & 38Md$ Ressources Estimées Malgré Opposition Scientifique", composite_score: 52.15, seabed_territorial_claim_score: 58.0, polymetallic_nodule_extraction_score: 55.0, submarine_infrastructure_control_score: 48.0, isa_governance_capture_score: 45.0, risk_level: "élevé", primary_pattern: "extraction_opportuniste", key_signals: ["Extraction opportuniste significative dans Norvège — contrats d'exploration actifs sans garanties environnementales suffisantes", "Licences ISA exploitées — zones d'exploration étendues sans partage équitable des bénéfices avec les pays en développement", "Risque environnemental élevé — panaches de sédiments et destruction d'écosystèmes endémiques des grands fonds non évalués"], estimated_deep_sea_index: 5.22, last_updated: "2026-06-20" },
    { entity_id: "DS-006", name: "France — Zone Clipperton & IFREMER", country: "Europe/Pacifique", sector: "Zone Clipperton, IFREMER Robotique & Projet Minerve d'Exploitation Fonds Marins", composite_score: 46.85, seabed_territorial_claim_score: 52.0, polymetallic_nodule_extraction_score: 48.0, submarine_infrastructure_control_score: 45.0, isa_governance_capture_score: 40.0, risk_level: "élevé", primary_pattern: "extraction_opportuniste", key_signals: ["Extraction opportuniste significative dans France — contrats d'exploration actifs sans garanties environnementales suffisantes", "Licences ISA exploitées — zones d'exploration étendues sans partage équitable des bénéfices avec les pays en développement", "Risque environnemental élevé — panaches de sédiments et destruction d'écosystèmes endémiques des grands fonds non évalués"], estimated_deep_sea_index: 4.69, last_updated: "2026-06-20" },
    { entity_id: "DS-007", name: "Petits États Insulaires Pacifique — Moratoire ISA", country: "Pacifique", sector: "Coalition Fidji/Palau/Micronésie pour Moratoire & Protection Patrimoine Commun Humanité", composite_score: 26.15, seabed_territorial_claim_score: 28.0, polymetallic_nodule_extraction_score: 22.0, submarine_infrastructure_control_score: 25.0, isa_governance_capture_score: 30.0, risk_level: "modéré", primary_pattern: "resistance_gouvernance", key_signals: ["Résistance à la gouvernance par Petits États Insulaires Pacifique — plaidoyer pour un moratoire sur l'exploitation commerciale des fonds marins", "Protection des écosystèmes prioritaire — opposition scientifique et communautaire à l'extraction industrielle des nodules", "Coalition moratoire — alliances des petits États insulaires et ONG pour préserver le principe de patrimoine commun de l'humanité"], estimated_deep_sea_index: 2.62, last_updated: "2026-06-20" },
    { entity_id: "DS-008", name: "ISA/UNCLOS — Gouvernance Internationale Fonds Marins", country: "Global", sector: "Autorité Fonds Marins — 31 Contrats Exploration, Code Minier en Négociation & Réforme Governance", composite_score: 5.6, seabed_territorial_claim_score: 5.0, polymetallic_nodule_extraction_score: 4.0, submarine_infrastructure_control_score: 6.0, isa_governance_capture_score: 8.0, risk_level: "faible", primary_pattern: "gouvernance_multilaterale", key_signals: ["ISA/UNCLOS préserve le cadre multilatéral des fonds marins — gouvernance équitable et transparente de la Zone internationale", "UNCLOS comme bouclier multilatéral — principe de patrimoine commun de l'humanité défendu contre les captures unilatérales", "Modèle de gouvernance des communs à étendre — ISA réformé et indépendant des intérêts miniers nationaux"], estimated_deep_sea_index: 0.56, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { course_fonds_marins_active: 2, infrastructure_sous_marine: 1, extraction_opportuniste: 3, resistance_gouvernance: 1, gouvernance_multilaterale: 1 },
    top_risk_entities: ["Chine — Zone ZCC Pacifique & Robots Miniers Autonomes", "USA — NOAA & Infrastructure Deep Sea Monopole", "Russie — Zone Atlantique Nord & Câbles Sous-Marins"],
    critical_alerts: ["Chine: course fonds marins active", "USA: course fonds marins active", "Russie: infrastructure sous marine", "Nauru: extraction opportuniste"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "deep_sea_mining",
    confidence_score: 0.74,
    data_sources: ["isa_exploration_contracts_registry", "deepgreenmetals_seabed_tracker", "greenpeace_deep_sea_mining_watch"],
    entities,
    avg_estimated_deep_sea_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
