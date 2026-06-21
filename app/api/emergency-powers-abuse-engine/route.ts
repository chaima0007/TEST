import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[emergency-powers-abuse-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Emergency Powers Abuse Engine Agent",
  domain: "emergency_powers_abuse",
  total_entities: 8,
  avg_composite: 61.33,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { democratic_oversight_suspension: 1, rights_derogation_breadth: 3, duration_proportionality_violation: 2, accountability_mechanism_absence: 2 },
  top_risk_entities: [
    "Thaïlande — État Urgence 3 Ans Post-Coup, Art.44 Pouvoir Absolu & Lèse-Majesté",
    "Turquie/Erdogan — État Urgence 2016-18, 150K Arrêtés, 150 Médias Fermés & Décrets",
    "Égypte/Sissi — État Urgence 4 Ans Continu 2017-21, 60K Prisonniers Pol. & Tribunaux Militaires",
  ],
  critical_alerts: [
    "Thaïlande: democratic_oversight_suspension",
    "Turquie/Erdogan: rights_derogation_breadth",
    "Égypte/Sissi: rights_derogation_breadth",
    "Biélorussie/Loukachenko: duration_proportionality_violation",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_emergency_powers_abuse_index: 6.13,
  data_sources: [
    "icnl_civic_freedom_monitor_emergency_powers_tracker",
    "venice_commission_emergency_legislation_standards",
    "human_rights_watch_covid_emergency_powers_abuse_report",
  ],
  entities: [
    { entity_id: "EP-001", name: "Thaïlande — État Urgence 3 Ans Post-Coup, Art.44 Pouvoir Absolu & Lèse-Majesté", country: "Asie du Sud-Est", composite_score: 93.25, democratic_oversight_suspension_score: 95.0, rights_derogation_breadth_score: 92.0, duration_proportionality_violation_score: 95.0, accountability_mechanism_absence_score: 90.0, risk_level: "critique", primary_pattern: "democratic_oversight_suspension", estimated_emergency_powers_abuse_index: 9.33, last_updated: "2026-06-21" },
    { entity_id: "EP-002", name: "Turquie/Erdogan — État Urgence 2016-18, 150K Arrêtés, 150 Médias Fermés & Décrets", country: "Moyen-Orient", composite_score: 89.7, democratic_oversight_suspension_score: 92.0, rights_derogation_breadth_score: 88.0, duration_proportionality_violation_score: 90.0, accountability_mechanism_absence_score: 88.0, risk_level: "critique", primary_pattern: "rights_derogation_breadth", estimated_emergency_powers_abuse_index: 8.97, last_updated: "2026-06-21" },
    { entity_id: "EP-003", name: "Égypte/Sissi — État Urgence 4 Ans Continu 2017-21, 60K Prisonniers Pol. & Tribunaux Militaires", country: "Afrique du Nord", composite_score: 88.5, democratic_oversight_suspension_score: 88.0, rights_derogation_breadth_score: 90.0, duration_proportionality_violation_score: 88.0, accountability_mechanism_absence_score: 88.0, risk_level: "critique", primary_pattern: "rights_derogation_breadth", estimated_emergency_powers_abuse_index: 8.85, last_updated: "2026-06-21" },
    { entity_id: "EP-004", name: "Biélorussie/Loukachenko — Loi Extrémisme 2020, 35K Arrêtés & Répression Totale Manifestants", country: "Europe de l'Est", composite_score: 85.15, democratic_oversight_suspension_score: 85.0, rights_derogation_breadth_score: 85.0, duration_proportionality_violation_score: 88.0, accountability_mechanism_absence_score: 82.0, risk_level: "critique", primary_pattern: "duration_proportionality_violation", estimated_emergency_powers_abuse_index: 8.52, last_updated: "2026-06-21" },
    { entity_id: "EP-005", name: "Inde/AFSPA — Loi Pouvoirs Spéciaux Armée 60+ Ans Cachemire & Impunité Militaire", country: "Asie du Sud", composite_score: 54.25, democratic_oversight_suspension_score: 52.0, rights_derogation_breadth_score: 55.0, duration_proportionality_violation_score: 58.0, accountability_mechanism_absence_score: 52.0, risk_level: "élevé", primary_pattern: "duration_proportionality_violation", estimated_emergency_powers_abuse_index: 5.43, last_updated: "2026-06-21" },
    { entity_id: "EP-006", name: "UE/Covid — Pouvoirs d'Urgence Pandémie, Hongrie Orban Sans Limite & Abus Droits", country: "Europe", composite_score: 49.5, democratic_oversight_suspension_score: 48.0, rights_derogation_breadth_score: 52.0, duration_proportionality_violation_score: 50.0, accountability_mechanism_absence_score: 48.0, risk_level: "élevé", primary_pattern: "rights_derogation_breadth", estimated_emergency_powers_abuse_index: 4.95, last_updated: "2026-06-21" },
    { entity_id: "EP-007", name: "ICNL/Commission de Venise — Monitoring Pouvoirs Urgence & Standards Dérogations Légales", country: "Global", composite_score: 25.85, democratic_oversight_suspension_score: 22.0, rights_derogation_breadth_score: 25.0, duration_proportionality_violation_score: 28.0, accountability_mechanism_absence_score: 30.0, risk_level: "modéré", primary_pattern: "accountability_mechanism_absence", estimated_emergency_powers_abuse_index: 2.59, last_updated: "2026-06-21" },
    { entity_id: "EP-008", name: "ONU/CCPR — Art.4 PIDCP Dérogations, Proportionnalité & Droits Non-Dérogeables", country: "Global", composite_score: 4.4, democratic_oversight_suspension_score: 4.0, rights_derogation_breadth_score: 5.0, duration_proportionality_violation_score: 3.0, accountability_mechanism_absence_score: 6.0, risk_level: "faible", primary_pattern: "accountability_mechanism_absence", estimated_emergency_powers_abuse_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/emergency-powers-abuse-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
