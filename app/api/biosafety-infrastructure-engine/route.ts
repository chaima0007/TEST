import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[biosafety-infrastructure-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Biosafety Infrastructure Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/biosafety-infrastructure-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Biosafety Infrastructure Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Biosafety Infrastructure Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "BI-001", name: "Chine — Wuhan BSL-4 & Opacité", country: "Asie", sector: "Institut de Virologie Wuhan & Gain-of-Function Non-Transparent", composite_score: 90.85, biosafety_compliance_gap_score: 92.0, gain_of_function_opacity_score: 95.0, laboratory_proliferation_score: 85.0, international_oversight_deficit_score: 90.0, risk_level: "critique", primary_pattern: "risque_fuite_critique", key_signals: ["Risque de fuite laboratoire critique dans Chine — standards BSL insuffisants et opacité totale", "Recherche gain-of-function sans supervision internationale adéquate — pathogènes renforcés non-contrôlés", "Prolifération incontrôlée de laboratoires BSL — capacités biologique sans gouvernance internationale"], estimated_biosafety_risk_index: 9.09, last_updated: "2026-06-20" },
    { id: "BI-002", name: "Russie — Biopreparat Héritage Soviétique", country: "Europe de l'Est", sector: "Vecteurs Biologiques Militaires & Laboratoires Non-Inspectés", composite_score: 85.45, biosafety_compliance_gap_score: 88.0, gain_of_function_opacity_score: 85.0, laboratory_proliferation_score: 82.0, international_oversight_deficit_score: 88.0, risk_level: "critique", primary_pattern: "risque_fuite_critique", key_signals: ["Risque de fuite laboratoire critique dans Russie — standards BSL insuffisants et opacité totale", "Recherche gain-of-function sans supervision internationale adéquate — pathogènes renforcés non-contrôlés", "Prolifération incontrôlée de laboratoires BSL — capacités biologique sans gouvernance internationale"], estimated_biosafety_risk_index: 8.55, last_updated: "2026-06-20" },
    { id: "BI-003", name: "Pays en Développement — BSL Non-Certifiés", country: "Global Sud", sector: "Laboratoires BSL-2/3 sans Standards Internationaux", composite_score: 79.85, biosafety_compliance_gap_score: 80.0, gain_of_function_opacity_score: 72.0, laboratory_proliferation_score: 88.0, international_oversight_deficit_score: 78.0, risk_level: "critique", primary_pattern: "proliferation_non_supervisee", key_signals: ["Risque de fuite laboratoire critique dans Pays en Développement — standards BSL insuffisants et opacité totale", "Recherche gain-of-function sans supervision internationale adéquate — pathogènes renforcés non-contrôlés", "Prolifération incontrôlée de laboratoires BSL — capacités biologique sans gouvernance internationale"], estimated_biosafety_risk_index: 7.99, last_updated: "2026-06-20" },
    { id: "BI-004", name: "Iran — Programme Biologique Dual-Use", country: "MENA", sector: "Recherche Biologique Militaire & Civile Non-Démêlée", composite_score: 79.1, biosafety_compliance_gap_score: 78.0, gain_of_function_opacity_score: 82.0, laboratory_proliferation_score: 75.0, international_oversight_deficit_score: 80.0, risk_level: "critique", primary_pattern: "risque_fuite_critique", key_signals: ["Risque de fuite laboratoire critique dans Iran — standards BSL insuffisants et opacité totale", "Recherche gain-of-function sans supervision internationale adéquate — pathogènes renforcés non-contrôlés", "Prolifération incontrôlée de laboratoires BSL — capacités biologique sans gouvernance internationale"], estimated_biosafety_risk_index: 7.91, last_updated: "2026-06-20" },
    { id: "BI-005", name: "USA — Gain-of-Function Controversé", country: "Amérique du Nord", sector: "NIH Financement GOF & Moratorium Partiel Insuffisant", composite_score: 63.35, biosafety_compliance_gap_score: 60.0, gain_of_function_opacity_score: 70.0, laboratory_proliferation_score: 65.0, international_oversight_deficit_score: 58.0, risk_level: "élevé", primary_pattern: "gouvernance_inadequate", key_signals: ["Gouvernance biosécurité inadéquate dans USA — supervision insuffisante des recherches risquées", "Standards de sécurité BSL non-harmonisés — incidents containment non-déclarés probables", "Cadre légal insuffisant pour superviser la recherche sur les agents pathogènes à risque"], estimated_biosafety_risk_index: 6.34, last_updated: "2026-06-20" },
    { id: "BI-006", name: "Afrique — Capacités Biosécurité Limitées", country: "Afrique", sector: "Lacunes Standards BSL & Dépendance Expertise Étrangère", composite_score: 54.1, biosafety_compliance_gap_score: 55.0, gain_of_function_opacity_score: 48.0, laboratory_proliferation_score: 62.0, international_oversight_deficit_score: 52.0, risk_level: "élevé", primary_pattern: "gouvernance_inadequate", key_signals: ["Gouvernance biosécurité inadéquate dans Afrique — supervision insuffisante des recherches risquées", "Standards de sécurité BSL non-harmonisés — incidents containment non-déclarés probables", "Cadre légal insuffisant pour superviser la recherche sur les agents pathogènes à risque"], estimated_biosafety_risk_index: 5.41, last_updated: "2026-06-20" },
    { id: "BI-007", name: "France & Allemagne — Standards Stricts", country: "Europe", sector: "Régulation Européenne Robuste mais Perfectible", composite_score: 26.25, biosafety_compliance_gap_score: 28.0, gain_of_function_opacity_score: 25.0, laboratory_proliferation_score: 30.0, international_oversight_deficit_score: 22.0, risk_level: "modéré", primary_pattern: "lacunes_reglementaires", key_signals: ["Lacunes réglementaires biosécurité dans France & Allemagne — supervision partielle mais améliorable", "Transparence insuffisante sur les recherches à double usage — risque de détournement civil/militaire", "Coopération internationale biosécurité existante mais incomplète"], estimated_biosafety_risk_index: 2.63, last_updated: "2026-06-20" },
    { id: "BI-008", name: "UK & Suisse — Biosécurité Exemplaire", country: "Europe", sector: "Porton Down & Spiez — Transparence et Supervision Maximale", composite_score: 7.75, biosafety_compliance_gap_score: 8.0, gain_of_function_opacity_score: 6.0, laboratory_proliferation_score: 12.0, international_oversight_deficit_score: 5.0, risk_level: "faible", primary_pattern: "biosecurite_exemplaire", key_signals: ["UK & Suisse maintient une biosécurité exemplaire — standards stricts, transparence et supervision maximale", "Inspections régulières des laboratoires BSL et données partagées avec les organisations internationales", "Modèle de gouvernance biosécurité à diffuser pour prévenir les pandémies d'origine laboratoire"], estimated_biosafety_risk_index: 0.78, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { risque_fuite_critique: 3, proliferation_non_supervisee: 1, gouvernance_inadequate: 2, lacunes_reglementaires: 1, biosecurite_exemplaire: 1 },
    top_risk_entities: ["Chine — Wuhan BSL-4 & Opacité", "Russie — Biopreparat Héritage Soviétique", "Pays en Développement — BSL Non-Certifiés"],
    critical_alerts: ["Chine: risque fuite critique", "Russie: risque fuite critique", "Pays Dev.: prolifération non supervisée", "Iran: risque fuite critique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "biosafety",
    confidence_score: 0.69,
    data_sources: ["nuclear_threat_initiative_bio_index", "who_ihhr_compliance_tracker", "ghs_index"],
    entities,
    avg_estimated_biosafety_risk_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
