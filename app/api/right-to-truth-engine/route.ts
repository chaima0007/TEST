import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[right-to-truth-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Right to Truth Engine Agent",
  domain: "right_to_truth",
  total_entities: 8,
  avg_composite: 59.27,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { official_denial_obstruction: 2, truth_commission_absence: 2, victim_silencing: 2, archive_destruction: 2 },
  top_risk_entities: [
    "Syrie — 100 000 Disparus, Déni Officiel Assad & Destruction Preuves Chimiques",
    "Amérique Latine/Cône Sud — Juntes, 30 000 Disparus & Vérité Post-Dictature Incomplète",
    "Sri Lanka — 40 000 Civils Tamouls Tués, Vérité Sabotée & Commissions Paralysées",
  ],
  critical_alerts: [
    "Syrie: official_denial_obstruction",
    "Amérique Latine/Cône Sud: truth_commission_absence",
    "Sri Lanka: victim_silencing",
    "Rwanda/Post-Génocide: archive_destruction",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_right_to_truth_index: 5.93,
  data_sources: [
    "ictj_international_center_transitional_justice_truth_commissions_database",
    "un_special_rapporteur_truth_reparation_guarantees_non_recurrence_annual_report",
    "amnesty_international_truth_justice_reparation_annual_report",
  ],
  entities: [
    { entity_id: "RT-001", name: "Syrie — 100 000 Disparus, Déni Officiel Assad & Destruction Preuves Chimiques", country: "Moyen-Orient", composite_score: 90.25, truth_commission_absence_score: 88.0, official_denial_obstruction_score: 95.0, victim_silencing_score: 90.0, archive_destruction_score: 88.0, risk_level: "critique", primary_pattern: "official_denial_obstruction", estimated_right_to_truth_index: 9.03, last_updated: "2026-06-20" },
    { entity_id: "RT-002", name: "Amérique Latine/Cône Sud — Juntes, 30 000 Disparus & Vérité Post-Dictature Incomplète", country: "Amérique Latine", composite_score: 87.85, truth_commission_absence_score: 90.0, official_denial_obstruction_score: 88.0, victim_silencing_score: 85.0, archive_destruction_score: 88.0, risk_level: "critique", primary_pattern: "truth_commission_absence", estimated_right_to_truth_index: 8.79, last_updated: "2026-06-20" },
    { entity_id: "RT-003", name: "Sri Lanka — 40 000 Civils Tamouls Tués, Vérité Sabotée & Commissions Paralysées", country: "Asie du Sud", composite_score: 81.45, truth_commission_absence_score: 82.0, official_denial_obstruction_score: 85.0, victim_silencing_score: 80.0, archive_destruction_score: 78.0, risk_level: "critique", primary_pattern: "victim_silencing", estimated_right_to_truth_index: 8.15, last_updated: "2026-06-20" },
    { entity_id: "RT-004", name: "Rwanda/Post-Génocide — Gacaca, TPIR & Révisionnisme Négationniste Persistant", country: "Afrique Sub-Saharienne", composite_score: 75.25, truth_commission_absence_score: 70.0, official_denial_obstruction_score: 75.0, victim_silencing_score: 78.0, archive_destruction_score: 80.0, risk_level: "critique", primary_pattern: "archive_destruction", estimated_right_to_truth_index: 7.53, last_updated: "2026-06-20" },
    { entity_id: "RT-005", name: "Algérie/Maroc — Années de Plomb, Disparus & Commission Vérité Partielle Sans Réparation", country: "Afrique du Nord", composite_score: 53.85, truth_commission_absence_score: 52.0, official_denial_obstruction_score: 58.0, victim_silencing_score: 55.0, archive_destruction_score: 50.0, risk_level: "élevé", primary_pattern: "official_denial_obstruction", estimated_right_to_truth_index: 5.39, last_updated: "2026-06-20" },
    { entity_id: "RT-006", name: "Russie/Tchétchénie — Disparus Deux Guerres, FSB Bloque Enquêtes & Archives Classifiées", country: "Europe de l'Est", composite_score: 52.75, truth_commission_absence_score: 48.0, official_denial_obstruction_score: 55.0, victim_silencing_score: 52.0, archive_destruction_score: 58.0, risk_level: "élevé", primary_pattern: "victim_silencing", estimated_right_to_truth_index: 5.28, last_updated: "2026-06-20" },
    { entity_id: "RT-007", name: "Espagne — Loi Mémoire Historique, Fosses Communes Franco & Résistance Partis Droite", country: "Europe", composite_score: 28.4, truth_commission_absence_score: 25.0, official_denial_obstruction_score: 30.0, victim_silencing_score: 28.0, archive_destruction_score: 32.0, risk_level: "modéré", primary_pattern: "truth_commission_absence", estimated_right_to_truth_index: 2.84, last_updated: "2026-06-20" },
    { entity_id: "RT-008", name: "ONU/HCDH — Rapporteur Vérité, Principes Joinet-Orentlicher & Base de Données Disparitions", country: "Global", composite_score: 4.4, truth_commission_absence_score: 4.0, official_denial_obstruction_score: 5.0, victim_silencing_score: 3.0, archive_destruction_score: 6.0, risk_level: "faible", primary_pattern: "archive_destruction", estimated_right_to_truth_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/right-to-truth-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
