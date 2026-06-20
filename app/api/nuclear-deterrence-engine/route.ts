import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[nuclear-deterrence-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Nuclear Deterrence Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/nuclear-deterrence-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Nuclear Deterrence Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Nuclear Deterrence Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "ND-001", name: "Russie — Sarmat, Poseidon & Doctrine Perimeter", country: "Europe de l'Est", sector: "RS-28 Sarmat, Torpille Poseidon, Avangard Hypersonique & Dead Hand Auto-Riposte", composite_score: 89.0, nuclear_arsenal_modernization_score: 90.0, second_strike_capability_score: 88.0, nuclear_doctrine_escalation_score: 92.0, npt_violation_risk_score: 85.0, risk_level: "critique", primary_pattern: "dissuasion_nucleaire_offensive", key_signals: ["Dissuasion nucléaire offensive de Russie — modernisation arsenaux, postures de première frappe et réduction des seuils d'emploi", "Course aux armements nucléaires — missiles hypersoniques, MIRV et miniaturisation des charges nucléaires tactiques", "Érosion du droit international nucléaire — remise en cause des traités de contrôle des armements et suspension des vérifications AIEA"], estimated_nuclear_deterrence_index: 8.9, last_updated: "2026-06-20" },
    { entity_id: "ND-002", name: "USA — Triade Nucléaire & 1700Md$ Modernisation", country: "Amérique du Nord", sector: "B21-Raider, Sentinel ICBM, Columbia SSBN & Bombes B61-12 OTAN Modernisées", composite_score: 83.0, nuclear_arsenal_modernization_score: 85.0, second_strike_capability_score: 92.0, nuclear_doctrine_escalation_score: 78.0, npt_violation_risk_score: 75.0, risk_level: "critique", primary_pattern: "dissuasion_nucleaire_offensive", key_signals: ["Dissuasion nucléaire offensive de USA — modernisation arsenaux, postures de première frappe et réduction des seuils d'emploi", "Course aux armements nucléaires — missiles hypersoniques, MIRV et miniaturisation des charges nucléaires tactiques", "Érosion du droit international nucléaire — remise en cause des traités de contrôle des armements et suspension des vérifications AIEA"], estimated_nuclear_deterrence_index: 8.3, last_updated: "2026-06-20" },
    { entity_id: "ND-003", name: "RPDC — ICBM Hwasong & Arsenal Clandestin", country: "Asie", sector: "Hwasong-17 ICBM, Ogives Miniaturisées & Sous-Marins Nucléaires SINPO en Développement", composite_score: 74.1, nuclear_arsenal_modernization_score: 62.0, second_strike_capability_score: 55.0, nuclear_doctrine_escalation_score: 95.0, npt_violation_risk_score: 90.0, risk_level: "critique", primary_pattern: "proliferation_clandestine", key_signals: ["Dissuasion nucléaire offensive de RPDC — modernisation arsenaux, postures de première frappe et réduction des seuils d'emploi", "Course aux armements nucléaires — missiles hypersoniques, MIRV et miniaturisation des charges nucléaires tactiques", "Érosion du droit international nucléaire — remise en cause des traités de contrôle des armements et suspension des vérifications AIEA"], estimated_nuclear_deterrence_index: 7.41, last_updated: "2026-06-20" },
    { entity_id: "ND-004", name: "Chine — Triple Arsenal 1000 Ogives 2030", country: "Asie", sector: "DF-41 ICBM, JL-3 SLBM, H-20 Bombardier Furtif & Silos Wyoming Stratégie", composite_score: 76.15, nuclear_arsenal_modernization_score: 78.0, second_strike_capability_score: 72.0, nuclear_doctrine_escalation_score: 75.0, npt_violation_risk_score: 80.0, risk_level: "critique", primary_pattern: "course_armements_nucleaires", key_signals: ["Dissuasion nucléaire offensive de Chine — modernisation arsenaux, postures de première frappe et réduction des seuils d'emploi", "Course aux armements nucléaires — missiles hypersoniques, MIRV et miniaturisation des charges nucléaires tactiques", "Érosion du droit international nucléaire — remise en cause des traités de contrôle des armements et suspension des vérifications AIEA"], estimated_nuclear_deterrence_index: 7.62, last_updated: "2026-06-20" },
    { entity_id: "ND-005", name: "Pakistan — TNW Tactiques & Doctrine Première Frappe", country: "Asie du Sud", sector: "Nasr TNW Tactique, Babur ALCM & Doctrine Emploi en Premier contre Supériorité Conventionnelle", composite_score: 65.4, nuclear_arsenal_modernization_score: 65.0, second_strike_capability_score: 58.0, nuclear_doctrine_escalation_score: 68.0, npt_violation_risk_score: 72.0, risk_level: "élevé", primary_pattern: "course_armements_nucleaires", key_signals: ["Prolifération nucléaire régionale par Pakistan — accumulation d'arsenaux non soumis aux régimes de vérification internationale", "Instabilité stratégique — doctrines d'emploi en premier et tensions bilatérales accroissant le risque de guerre nucléaire accidentelle", "Zones de crise à risque nucléaire — théâtres d'opérations où l'escalade nucléaire n'est pas exclue comme option militaire"], estimated_nuclear_deterrence_index: 6.54, last_updated: "2026-06-20" },
    { entity_id: "ND-006", name: "Inde — Triade & No First Use sous Révision", country: "Asie du Sud", sector: "Agni-V ICBM, INS Arihant SSBN & Révision Doctrine No First Use sous Modi", composite_score: 60.85, nuclear_arsenal_modernization_score: 62.0, second_strike_capability_score: 60.0, nuclear_doctrine_escalation_score: 65.0, npt_violation_risk_score: 55.0, risk_level: "élevé", primary_pattern: "course_armements_nucleaires", key_signals: ["Prolifération nucléaire régionale par Inde — accumulation d'arsenaux non soumis aux régimes de vérification internationale", "Instabilité stratégique — doctrines d'emploi en premier et tensions bilatérales accroissant le risque de guerre nucléaire accidentelle", "Zones de crise à risque nucléaire — théâtres d'opérations où l'escalade nucléaire n'est pas exclue comme option militaire"], estimated_nuclear_deterrence_index: 6.09, last_updated: "2026-06-20" },
    { entity_id: "ND-007", name: "Iran — Seuil Nucléaire & Uranium 60% Enrichi", country: "MENA", sector: "Enrichissement 60% Fordow, Centrifugeuses IR-6 & Breakout Time Estimé <2 Semaines AIEA", composite_score: 38.9, nuclear_arsenal_modernization_score: 35.0, second_strike_capability_score: 30.0, nuclear_doctrine_escalation_score: 42.0, npt_violation_risk_score: 52.0, risk_level: "modéré", primary_pattern: "course_armements_nucleaires", key_signals: ["Ambiguïté nucléaire de Iran — programme potentiel maintenant une incertitude stratégique délibérée", "Dépendance aux garanties de sécurité étendues — couverture nucléaire d'alliés créant des vulnérabilités structurelles", "Capacités balistiques duales — vecteurs pouvant emporter des charges conventionnelles ou nucléaires selon les circonstances"], estimated_nuclear_deterrence_index: 3.89, last_updated: "2026-06-20" },
    { entity_id: "ND-008", name: "AIEA & Traité NPT — Vérification Multilatérale", country: "Global", sector: "Protocole Additionnel AIEA, NPT 191 États Parties & CTBT 186 Signataires", composite_score: 3.65, nuclear_arsenal_modernization_score: 5.0, second_strike_capability_score: 4.0, nuclear_doctrine_escalation_score: 3.0, npt_violation_risk_score: 2.0, risk_level: "faible", primary_pattern: "desarmement_cooperatif", key_signals: ["AIEA & Traité NPT incarne le désarmement coopératif — traités de vérification, transparence des arsenaux et dialogue multilatéral", "Réduction vérifiable des arsenaux — mécanismes d'inspection réciproque et démantèlement documenté des ogives", "Modèle de non-prolifération à universaliser — adhésion au CTBT, TNP renforcé et zones dénucléarisées régionales"], estimated_nuclear_deterrence_index: 0.37, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { dissuasion_nucleaire_offensive: 2, proliferation_clandestine: 1, modernisation_arsenal_strategique: 0, course_armements_nucleaires: 4, desarmement_cooperatif: 1 },
    top_risk_entities: ["Russie — Sarmat, Poseidon & Doctrine Perimeter", "USA — Triade Nucléaire & 1700Md$ Modernisation", "RPDC — ICBM Hwasong & Arsenal Clandestin"],
    critical_alerts: ["Russie: dissuasion nucléaire offensive", "USA: dissuasion nucléaire offensive", "RPDC: prolifération clandestine", "Chine: course armements nucléaires"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "nuclear_deterrence",
    confidence_score: 0.78,
    data_sources: ["sipri_nuclear_forces_database", "arms_control_association_npt_monitor", "bulletin_atomic_scientists_doomsday_clock"],
    entities,
    avg_estimated_nuclear_deterrence_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
