import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[quantum-race-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Quantum Race Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/quantum-race-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Quantum Race Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Quantum Race Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "QR-001", name: "Chine — Programme Quantique Souverain & MICIUS", country: "Asie", sector: "15Md$ Investis, Satellite MICIUS QKD & Algorithmes Quantiques Militaires", composite_score: 91.6, quantum_supremacy_investment_score: 95.0, cryptographic_vulnerability_exploitation_score: 92.0, quantum_talent_monopolization_score: 90.0, quantum_weapons_integration_score: 88.0, risk_level: "critique", primary_pattern: "suprematie_quantique_course", key_signals: ["Course à la suprématie quantique critique dans Chine — Programme Quantique Souverain & MICIUS — investissements massifs menaçant la cryptographie mondiale", "Stratégie 'récolte maintenant, décrypte plus tard' — stockage de communications chiffrées en attente de la clé quantique", "Militarisation quantique — ordinateurs quantiques intégrés dans les systèmes de renseignement et d'armement offensif"], estimated_quantum_dominance_index: 9.16, last_updated: "2026-06-20" },
    { entity_id: "QR-002", name: "USA — IBM/Google Willow & NSA Post-Quantum", country: "Amérique du Nord", sector: "National Quantum Initiative 1.2Md$, Willow 105 Qubits & DARPA Quantum", composite_score: 86.65, quantum_supremacy_investment_score: 90.0, cryptographic_vulnerability_exploitation_score: 88.0, quantum_talent_monopolization_score: 85.0, quantum_weapons_integration_score: 82.0, risk_level: "critique", primary_pattern: "suprematie_quantique_course", key_signals: ["Course à la suprématie quantique critique dans USA — IBM/Google Willow & NSA Post-Quantum — investissements massifs menaçant la cryptographie mondiale", "Stratégie 'récolte maintenant, décrypte plus tard' — stockage de communications chiffrées en attente de la clé quantique", "Militarisation quantique — ordinateurs quantiques intégrés dans les systèmes de renseignement et d'armement offensif"], estimated_quantum_dominance_index: 8.67, last_updated: "2026-06-20" },
    { entity_id: "QR-003", name: "Russie — Rosatom Quantique & Intégration Défense", country: "Europe de l'Est", sector: "Institut Kurchatov & Technopolis Quantique — Intégration Systèmes Militaires", composite_score: 70.45, quantum_supremacy_investment_score: 72.0, cryptographic_vulnerability_exploitation_score: 68.0, quantum_talent_monopolization_score: 65.0, quantum_weapons_integration_score: 78.0, risk_level: "critique", primary_pattern: "militarisation_quantique", key_signals: ["Course à la suprématie quantique critique dans Russie — Rosatom Quantique & Intégration Défense — investissements massifs menaçant la cryptographie mondiale", "Stratégie 'récolte maintenant, décrypte plus tard' — stockage de communications chiffrées en attente de la clé quantique", "Militarisation quantique — ordinateurs quantiques intégrés dans les systèmes de renseignement et d'armement offensif"], estimated_quantum_dominance_index: 7.05, last_updated: "2026-06-20" },
    { entity_id: "QR-004", name: "UE — EuroQCI & Quantum Flagship 1Md€", country: "Europe", sector: "Infrastructure QCI Paneuropéenne & Partenariats IBM/Atos QuantumLeap", composite_score: 60.0, quantum_supremacy_investment_score: 65.0, cryptographic_vulnerability_exploitation_score: 60.0, quantum_talent_monopolization_score: 58.0, quantum_weapons_integration_score: 55.0, risk_level: "critique", primary_pattern: "programme_quantique_avance", key_signals: ["Course à la suprématie quantique critique dans UE — EuroQCI & Quantum Flagship 1Md€ — investissements massifs menaçant la cryptographie mondiale", "Stratégie 'récolte maintenant, décrypte plus tard' — stockage de communications chiffrées en attente de la clé quantique", "Militarisation quantique — ordinateurs quantiques intégrés dans les systèmes de renseignement et d'armement offensif"], estimated_quantum_dominance_index: 6.0, last_updated: "2026-06-20" },
    { entity_id: "QR-005", name: "Royaume-Uni — NQCC National Quantum Computing Centre", country: "Europe", sector: "Oxford/Cambridge Quantum Hub & Partenariats Défense GCHQ Quantique", composite_score: 51.0, quantum_supremacy_investment_score: 55.0, cryptographic_vulnerability_exploitation_score: 52.0, quantum_talent_monopolization_score: 50.0, quantum_weapons_integration_score: 45.0, risk_level: "élevé", primary_pattern: "programme_quantique_avance", key_signals: ["Programme quantique avancé dans Royaume-Uni — NQCC National Quantum Computing Centre — capacités significatives et course aux qubits en accélération", "Investissements en cryptographie post-quantique offensive — développement d'algorithmes quantiques de cassage", "Concentration des talents quantiques — recrutement mondial pour maintenir l'avantage technologique"], estimated_quantum_dominance_index: 5.1, last_updated: "2026-06-20" },
    { entity_id: "QR-006", name: "Inde — National Mission on Quantum Technologies", country: "Asie du Sud", sector: "6000Cr₹ Mission Quantique & IIT Recherche Algorithmes Quantiques", composite_score: 44.15, quantum_supremacy_investment_score: 48.0, cryptographic_vulnerability_exploitation_score: 42.0, quantum_talent_monopolization_score: 45.0, quantum_weapons_integration_score: 40.0, risk_level: "élevé", primary_pattern: "programme_quantique_avance", key_signals: ["Programme quantique avancé dans Inde — National Mission on Quantum Technologies — capacités significatives et course aux qubits en accélération", "Investissements en cryptographie post-quantique offensive — développement d'algorithmes quantiques de cassage", "Concentration des talents quantiques — recrutement mondial pour maintenir l'avantage technologique"], estimated_quantum_dominance_index: 4.42, last_updated: "2026-06-20" },
    { entity_id: "QR-007", name: "Canada — Périmètre Institute & D-Wave", country: "Amériques", sector: "D-Wave Recuit Quantique & Waterloo Institute for Quantum Computing", composite_score: 33.1, quantum_supremacy_investment_score: 35.0, cryptographic_vulnerability_exploitation_score: 30.0, quantum_talent_monopolization_score: 38.0, quantum_weapons_integration_score: 28.0, risk_level: "modéré", primary_pattern: "capacites_quantiques_emergentes", key_signals: ["Capacités quantiques émergentes dans Canada — Périmètre Institute & D-Wave — programme civil avec potentiel de conversion militaire", "Partenariats quantiques internationaux — accès aux ecosystèmes quantiques via alliances technologiques", "Migration post-quantique en cours — mise à jour progressive des infrastructures cryptographiques nationales"], estimated_quantum_dominance_index: 3.31, last_updated: "2026-06-20" },
    { entity_id: "QR-008", name: "Afrique & MENA — Fracture Quantique", country: "Global", sector: "Absence d'Écosystème Quantique Local — Dépendance Totale aux Fournisseurs Étrangers", composite_score: 5.95, quantum_supremacy_investment_score: 8.0, cryptographic_vulnerability_exploitation_score: 5.0, quantum_talent_monopolization_score: 6.0, quantum_weapons_integration_score: 4.0, risk_level: "faible", primary_pattern: "fracture_quantique", key_signals: ["Afrique & MENA — Fracture Quantique accuse un retard technologique quantique significatif — fracture numérique à l'ère quantique", "Dépendance aux fournisseurs quantiques étrangers — vulnérabilité souveraine dans les communications sécurisées", "Opportunité de rattrapage — coopération internationale et transferts technologiques comme leviers de montée en puissance"], estimated_quantum_dominance_index: 0.6, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { suprematie_quantique_course: 2, militarisation_quantique: 1, programme_quantique_avance: 3, capacites_quantiques_emergentes: 1, fracture_quantique: 1 },
    top_risk_entities: ["Chine — Programme Quantique Souverain & MICIUS", "USA — IBM/Google Willow & NSA Post-Quantum", "Russie — Rosatom Quantique & Intégration Défense"],
    critical_alerts: ["Chine: suprématie quantique course", "USA: suprématie quantique course", "Russie: militarisation quantique", "UE: programme quantique avancé"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "quantum_race",
    confidence_score: 0.76,
    data_sources: ["mckinsey_quantum_technology_monitor", "national_quantum_initiative_tracker", "ieee_quantum_week_proceedings"],
    entities,
    avg_estimated_quantum_dominance_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
