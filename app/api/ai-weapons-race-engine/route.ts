import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[ai-weapons-race-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "AI Weapons Race Engine Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/ai-weapons-race-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "AI Weapons Race Engine Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "AI Weapons Race Engine Agent"), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    { id: "AW-001", name: "USA — DARPA AI Next & F-16 Autonome", country: "Amérique du Nord", sector: "Projet MAVEN, X-62A VISTA & Essaims Drones Tueurs Autonomes Pentagone", composite_score: 84.0, lethal_autonomous_weapons_score: 85.0, ai_decision_loop_integration_score: 88.0, cyber_ai_offensive_score: 82.0, regulation_deficit_score: 80.0, risk_level: "critique", primary_pattern: "suprematie_ia_militaire", key_signals: ["Course aux armes autonomes létales critique dans USA — DARPA AI Next & F-16 Autonome — LAWS déployés ou testés en conditions opérationnelles", "IA dans la boucle de ciblage — systèmes militaires délégant des décisions létales à des algorithmes sans contrôle humain", "Absence de responsabilité — les crimes de guerre commis par des machines autonomes sans traité d'interdiction opérationnel"], estimated_ai_weapons_index: 8.4, last_updated: "2026-06-20" },
    { id: "AW-002", name: "Chine — Sharp Sword & Drones Autonomes DF-17", country: "Asie", sector: "Drones UCAV Autonomes Mer de Chine, Missiles IA & Algorithmes Ciblage Gaza-Style", composite_score: 85.85, lethal_autonomous_weapons_score: 90.0, ai_decision_loop_integration_score: 85.0, cyber_ai_offensive_score: 88.0, regulation_deficit_score: 78.0, risk_level: "critique", primary_pattern: "suprematie_ia_militaire", key_signals: ["Course aux armes autonomes létales critique dans Chine — Sharp Sword & Drones Autonomes DF-17 — LAWS déployés ou testés en conditions opérationnelles", "IA dans la boucle de ciblage — systèmes militaires délégant des décisions létales à des algorithmes sans contrôle humain", "Absence de responsabilité — les crimes de guerre commis par des machines autonomes sans traité d'interdiction opérationnel"], estimated_ai_weapons_index: 8.59, last_updated: "2026-06-20" },
    { id: "AW-003", name: "Russie — Uran-9 & Poseidon Nucléaire Autonome", country: "Europe de l'Est", sector: "Char Uran-9, Missile Nucléaire Poseidon Autonome & SORM-IA Intégré", composite_score: 79.65, lethal_autonomous_weapons_score: 78.0, ai_decision_loop_integration_score: 82.0, cyber_ai_offensive_score: 75.0, regulation_deficit_score: 85.0, risk_level: "critique", primary_pattern: "integration_ia_decision", key_signals: ["Course aux armes autonomes létales critique dans Russie — Uran-9 & Poseidon Nucléaire Autonome — LAWS déployés ou testés en conditions opérationnelles", "IA dans la boucle de ciblage — systèmes militaires délégant des décisions létales à des algorithmes sans contrôle humain", "Absence de responsabilité — les crimes de guerre commis par des machines autonomes sans traité d'interdiction opérationnel"], estimated_ai_weapons_index: 7.97, last_updated: "2026-06-20" },
    { id: "AW-004", name: "Israël — Harpy & Système Lavender Gaza", country: "MENA", sector: "Drones Autonomes Harpy, Système IA Lavender 37000 Cibles & Iron Dome IA", composite_score: 75.1, lethal_autonomous_weapons_score: 80.0, ai_decision_loop_integration_score: 72.0, cyber_ai_offensive_score: 78.0, regulation_deficit_score: 68.0, risk_level: "critique", primary_pattern: "cyberguerre_ia_offensive", key_signals: ["Course aux armes autonomes létales critique dans Israël — Harpy & Système Lavender Gaza — LAWS déployés ou testés en conditions opérationnelles", "IA dans la boucle de ciblage — systèmes militaires délégant des décisions létales à des algorithmes sans contrôle humain", "Absence de responsabilité — les crimes de guerre commis par des machines autonomes sans traité d'interdiction opérationnel"], estimated_ai_weapons_index: 7.51, last_updated: "2026-06-20" },
    { id: "AW-005", name: "Corée du Sud/Corée du Nord — Course LAWS Péninsule", country: "Asie", sector: "SGR-A1 Robot Sentinelle Autonome vs DPRK Drones Suicide Autonomes", composite_score: 53.5, lethal_autonomous_weapons_score: 55.0, ai_decision_loop_integration_score: 52.0, cyber_ai_offensive_score: 48.0, regulation_deficit_score: 60.0, risk_level: "élevé", primary_pattern: "proliferation_drones_autonomes", key_signals: ["Prolifération de drones autonomes dans Corée du Sud/Corée du Nord — Course LAWS Péninsule — exportation de LAWS sans régulation éthique ou traçabilité", "Course à l'IA militaire — investissements massifs en essaims de drones autonomes et systèmes de ciblage algorithmique", "Normalisation des LAWS — seuil psychologique de la décision létale autonome abaissé sans consensus international"], estimated_ai_weapons_index: 5.35, last_updated: "2026-06-20" },
    { id: "AW-006", name: "Turquie — Bayraktar TB2 & Export LAWS", country: "MENA/Europe", sector: "TB2 Nagorno-Karabakh, Aksungur & Export Drones Autonomes 30+ Pays", composite_score: 48.35, lethal_autonomous_weapons_score: 52.0, ai_decision_loop_integration_score: 45.0, cyber_ai_offensive_score: 42.0, regulation_deficit_score: 55.0, risk_level: "élevé", primary_pattern: "proliferation_drones_autonomes", key_signals: ["Prolifération de drones autonomes dans Turquie — Bayraktar TB2 & Export LAWS — exportation de LAWS sans régulation éthique ou traçabilité", "Course à l'IA militaire — investissements massifs en essaims de drones autonomes et systèmes de ciblage algorithmique", "Normalisation des LAWS — seuil psychologique de la décision létale autonome abaissé sans consensus international"], estimated_ai_weapons_index: 4.84, last_updated: "2026-06-20" },
    { id: "AW-007", name: "UE — Débat Fragmentation Réglementaire LAWS", country: "Europe", sector: "IA Act EU sans Volet Militaire & Positions Nationales Contradictoires LAWS", composite_score: 27.5, lethal_autonomous_weapons_score: 25.0, ai_decision_loop_integration_score: 30.0, cyber_ai_offensive_score: 22.0, regulation_deficit_score: 35.0, risk_level: "modéré", primary_pattern: "regulation_ia_militaire", key_signals: ["Débat LAWS insuffisant dans UE — Débat Fragmentation Réglementaire LAWS — réglementation intérieure insuffisante face aux risques des armes autonomes", "Fragmentation réglementaire — absence de position nationale claire sur l'interdiction des LAWS offensifs", "Risque de retard réglementaire — la course technologique dépasse les capacités normatives nationales et internationales"], estimated_ai_weapons_index: 2.75, last_updated: "2026-06-20" },
    { id: "AW-008", name: "ICRC & Stop Killer Robots — Normes Anti-LAWS", country: "Global", sector: "Campagne 200 ONG & Négociations ONU depuis 2014 — Plaidoyer Interdiction", composite_score: 4.6, lethal_autonomous_weapons_score: 5.0, ai_decision_loop_integration_score: 4.0, cyber_ai_offensive_score: 6.0, regulation_deficit_score: 3.0, risk_level: "faible", primary_pattern: "regulation_ia_militaire", key_signals: ["ICRC & Stop Killer Robots — Normes Anti-LAWS soutient activement l'interdiction des LAWS — plaidoyer pour le contrôle humain meaningful", "Engagement pour un traité LAWS contraignant — participation aux négociations ONU et soutien à la Campagne Stop Killer Robots", "Modèle de régulation éthique de l'IA militaire — principes d'utilisation responsable de l'IA en contexte de conflit"], estimated_ai_weapons_index: 0.46, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { suprematie_ia_militaire: 2, integration_ia_decision: 1, cyberguerre_ia_offensive: 1, proliferation_drones_autonomes: 2, regulation_ia_militaire: 2 },
    top_risk_entities: ["Chine — Sharp Sword & Drones Autonomes DF-17", "USA — DARPA AI Next & F-16 Autonome", "Russie — Uran-9 & Poseidon Nucléaire Autonome"],
    critical_alerts: ["USA: suprématie IA militaire", "Chine: suprématie IA militaire", "Russie: intégration IA décision", "Israël: cyberguerre IA offensive"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "ai_weapons",
    confidence_score: 0.79,
    data_sources: ["sipri_military_ai_database", "campaign_stop_killer_robots", "icrc_autonomous_weapons_report"],
    entities,
    avg_estimated_ai_weapons_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
