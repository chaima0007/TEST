import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[transitional-justice-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Transitional Justice Engine Agent",
  domain: "transitional_justice",
  total_entities: 8,
  avg_composite: 60.69,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { amnesty_impunity_bloc: 2, reparations_implementation_gap: 3, truth_commission_absence: 2, institutional_reform_failure: 1 },
  top_risk_entities: [
    "Syrie — Aucune CVR, Assad Impuni, 100K+ Disparus & Justice Internationale Bloquée Veto",
    "Myanmar — Junta Post-Coup, Génocide Rohingya Non Jugé & CIJ Procédure Sans Exécution",
    "Cambodge/Khmers Rouges — CETC Trop Tardif, Rares Condamnations & Génération Victime Vieillie",
  ],
  critical_alerts: [
    "Syrie: amnesty_impunity_bloc",
    "Myanmar: amnesty_impunity_bloc",
    "Cambodge/Khmers Rouges: reparations_implementation_gap",
    "Sri Lanka: truth_commission_absence",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_transitional_justice_index: 6.07,
  data_sources: [
    "ictj_transitional_justice_global_survey_annual_report",
    "un_special_rapporteur_truth_justice_reparations_guarantees_non_recurrence",
    "icc_rome_statute_state_parties_compliance_review",
  ],
  entities: [
    { entity_id: "TJ-001", name: "Syrie — Aucune CVR, Assad Impuni, 100K+ Disparus & Justice Internationale Bloquée Veto", country: "Moyen-Orient", composite_score: 93.65, truth_commission_absence_score: 95.0, reparations_implementation_gap_score: 92.0, amnesty_impunity_bloc_score: 95.0, institutional_reform_failure_score: 92.0, risk_level: "critique", primary_pattern: "amnesty_impunity_bloc", estimated_transitional_justice_index: 9.37, last_updated: "2026-06-21" },
    { entity_id: "TJ-002", name: "Myanmar — Junta Post-Coup, Génocide Rohingya Non Jugé & CIJ Procédure Sans Exécution", country: "Asie du Sud-Est", composite_score: 89.6, truth_commission_absence_score: 90.0, reparations_implementation_gap_score: 88.0, amnesty_impunity_bloc_score: 92.0, institutional_reform_failure_score: 88.0, risk_level: "critique", primary_pattern: "amnesty_impunity_bloc", estimated_transitional_justice_index: 8.96, last_updated: "2026-06-21" },
    { entity_id: "TJ-003", name: "Cambodge/Khmers Rouges — CETC Trop Tardif, Rares Condamnations & Génération Victime Vieillie", country: "Asie du Sud-Est", composite_score: 85.6, truth_commission_absence_score: 85.0, reparations_implementation_gap_score: 88.0, amnesty_impunity_bloc_score: 82.0, institutional_reform_failure_score: 88.0, risk_level: "critique", primary_pattern: "reparations_implementation_gap", estimated_transitional_justice_index: 8.56, last_updated: "2026-06-21" },
    { entity_id: "TJ-004", name: "Sri Lanka — CVR Promises Non Tenues, Crimes Guerre Tamouls Impunis & Résistance Militaire", country: "Asie du Sud", composite_score: 82.25, truth_commission_absence_score: 82.0, reparations_implementation_gap_score: 85.0, amnesty_impunity_bloc_score: 80.0, institutional_reform_failure_score: 82.0, risk_level: "critique", primary_pattern: "truth_commission_absence", estimated_transitional_justice_index: 8.23, last_updated: "2026-06-21" },
    { entity_id: "TJ-005", name: "Colombie — JEP Fonctionnelle Mais Lente, FARC Réintégration Partielle & Dissidences Actives", country: "Amérique Latine", composite_score: 52.85, truth_commission_absence_score: 52.0, reparations_implementation_gap_score: 55.0, amnesty_impunity_bloc_score: 50.0, institutional_reform_failure_score: 55.0, risk_level: "élevé", primary_pattern: "reparations_implementation_gap", estimated_transitional_justice_index: 5.29, last_updated: "2026-06-21" },
    { entity_id: "TJ-006", name: "Tunisie — IVD Sabotée, Reparations Non Versées & Contre-Réforme Autoritaire Saïed", country: "Afrique du Nord", composite_score: 51.35, truth_commission_absence_score: 50.0, reparations_implementation_gap_score: 55.0, amnesty_impunity_bloc_score: 52.0, institutional_reform_failure_score: 48.0, risk_level: "élevé", primary_pattern: "reparations_implementation_gap", estimated_transitional_justice_index: 5.14, last_updated: "2026-06-21" },
    { entity_id: "TJ-007", name: "ICTJ/No Peace Without Justice — Expertise Mondiale CVR, Réparations & Réforme Institutionnelle", country: "Global", composite_score: 25.85, truth_commission_absence_score: 22.0, reparations_implementation_gap_score: 25.0, amnesty_impunity_bloc_score: 28.0, institutional_reform_failure_score: 30.0, risk_level: "modéré", primary_pattern: "truth_commission_absence", estimated_transitional_justice_index: 2.59, last_updated: "2026-06-21" },
    { entity_id: "TJ-008", name: "ONU/HCDH — Principes de Base Réparations, Rapporteur Justice Transitionnelle & Résolutions", country: "Global", composite_score: 4.4, truth_commission_absence_score: 4.0, reparations_implementation_gap_score: 5.0, amnesty_impunity_bloc_score: 3.0, institutional_reform_failure_score: 6.0, risk_level: "faible", primary_pattern: "institutional_reform_failure", estimated_transitional_justice_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/transitional-justice-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
