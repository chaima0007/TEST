import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[treaty-erosion-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Treaty Erosion Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/treaty-erosion-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Treaty Erosion Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Treaty Erosion Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "TE-001", name: "Russie — Droit International Baffoué", country: "Europe de l'Est", sector: "Violations du Droit International & Veto ONU", composite_score: 89.75, treaty_withdrawal_score: 90.0, international_law_violation_score: 95.0, multilateral_institution_undermining_score: 88.0, normative_fragmentation_score: 85.0, risk_level: "critique", primary_pattern: "erosion_systematique", key_signals: ["Désintégration de l'ordre multilatéral par Russie — retrait systématique des traités fondateurs", "Violations répétées du droit international sans accountability — impunité normative", "Sabotage des institutions multilatérales — ONU, OMC, CPI neutralisées par veto ou boycott"], estimated_erosion_index: 8.98, last_updated: "2026-06-20" },
    { entity_id: "TE-002", name: "USA — Unilatéralisme Sélectif", country: "Amérique du Nord", sector: "Retrait Traités & Sanctions Extraterritoriales", composite_score: 80.35, treaty_withdrawal_score: 85.0, international_law_violation_score: 75.0, multilateral_institution_undermining_score: 80.0, normative_fragmentation_score: 82.0, risk_level: "critique", primary_pattern: "desintegration_multilaterale", key_signals: ["Désintégration de l'ordre multilatéral par USA — retrait systématique des traités fondateurs", "Violations répétées du droit international sans accountability — impunité normative", "Sabotage des institutions multilatérales — ONU, OMC, CPI neutralisées par veto ou boycott"], estimated_erosion_index: 8.04, last_updated: "2026-06-20" },
    { entity_id: "TE-003", name: "Chine — Droit de la Mer Contesté", country: "Asie", sector: "Rejet UNCLOS & Prétentions Unilatérales", composite_score: 79.35, treaty_withdrawal_score: 78.0, international_law_violation_score: 82.0, multilateral_institution_undermining_score: 75.0, normative_fragmentation_score: 80.0, risk_level: "critique", primary_pattern: "erosion_systematique", key_signals: ["Désintégration de l'ordre multilatéral par Chine — retrait systématique des traités fondateurs", "Violations répétées du droit international sans accountability — impunité normative", "Sabotage des institutions multilatérales — ONU, OMC, CPI neutralisées par veto ou boycott"], estimated_erosion_index: 7.94, last_updated: "2026-06-20" },
    { entity_id: "TE-004", name: "Turquie — OTAN & Droit Humanitaire", country: "Europe/MENA", sector: "Réinterprétation Sélective des Obligations Traités", composite_score: 65.85, treaty_withdrawal_score: 65.0, international_law_violation_score: 68.0, multilateral_institution_undermining_score: 70.0, normative_fragmentation_score: 62.0, risk_level: "élevé", primary_pattern: "fragmentation_normative", key_signals: ["Fragmentation normative grave dans Turquie — ordres juridiques concurrents en construction", "Sélectivité dans l'application du droit international — deux poids deux mesures institutionnalisés", "Institutions multilatérales fragilisées — légitimité et capacité d'action en déclin"], estimated_erosion_index: 6.59, last_updated: "2026-06-20" },
    { entity_id: "TE-005", name: "Israël — CPI & Résolutions ONU", country: "MENA", sector: "Non-Reconnaissance des Juridictions Internationales", composite_score: 63.85, treaty_withdrawal_score: 60.0, international_law_violation_score: 72.0, multilateral_institution_undermining_score: 65.0, normative_fragmentation_score: 55.0, risk_level: "élevé", primary_pattern: "fragmentation_normative", key_signals: ["Fragmentation normative grave dans Israël — ordres juridiques concurrents en construction", "Sélectivité dans l'application du droit international — deux poids deux mesures institutionnalisés", "Institutions multilatérales fragilisées — légitimité et capacité d'action en déclin"], estimated_erosion_index: 6.39, last_updated: "2026-06-20" },
    { entity_id: "TE-006", name: "Brésil — Accord de Paris & Amazon", country: "Amériques", sector: "Tension Souveraineté Nationale vs Engagements Climato", composite_score: 42.25, treaty_withdrawal_score: 45.0, international_law_violation_score: 38.0, multilateral_institution_undermining_score: 40.0, normative_fragmentation_score: 42.0, risk_level: "élevé", primary_pattern: "tensions_institutionnelles", key_signals: ["Tensions institutionnelles dans Brésil — pressions sur les traités mais ordre préservé", "Remise en question partielle du multilatéralisme — réformes nécessaires pour restaurer la confiance", "Fragmentation normative naissante — blocs régionaux testant les limites du droit international"], estimated_erosion_index: 4.23, last_updated: "2026-06-20" },
    { entity_id: "TE-007", name: "Inde — Multilatéralisme Pragmatique", country: "Asie du Sud", sector: "Engagement Sélectif selon les Intérêts Nationaux", composite_score: 28.75, treaty_withdrawal_score: 30.0, international_law_violation_score: 28.0, multilateral_institution_undermining_score: 32.0, normative_fragmentation_score: 25.0, risk_level: "modéré", primary_pattern: "tensions_institutionnelles", key_signals: ["Tensions institutionnelles dans Inde — pressions sur les traités mais ordre préservé", "Remise en question partielle du multilatéralisme — réformes nécessaires pour restaurer la confiance", "Fragmentation normative naissante — blocs régionaux testant les limites du droit international"], estimated_erosion_index: 2.88, last_updated: "2026-06-20" },
    { entity_id: "TE-008", name: "Union Européenne — Défenseur Multilatéral", country: "Europe", sector: "Champion du Multilatéralisme & du Droit International", composite_score: 11.5, treaty_withdrawal_score: 12.0, international_law_violation_score: 10.0, multilateral_institution_undermining_score: 15.0, normative_fragmentation_score: 8.0, risk_level: "faible", primary_pattern: "ancrage_multilateral", key_signals: ["Union Européenne maintient un ancrage multilatéral exemplaire — respect des traités et des institutions", "Investissement actif dans le système multilatéral — réformateur constructif de l'ordre international", "Modèle de diplomatie multilatérale à valoriser et à diffuser pour renforcer la paix"], estimated_erosion_index: 1.15, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 3, "élevé": 3, "modéré": 1, faible: 1 },
    pattern_distribution: { desintegration_multilaterale: 1, erosion_systematique: 2, fragmentation_normative: 2, tensions_institutionnelles: 2, ancrage_multilateral: 1 },
    top_risk_entities: ["Russie — Droit International Baffoué", "USA — Unilatéralisme Sélectif", "Chine — Droit de la Mer Contesté"],
    critical_alerts: ["Russie: érosion systématique", "USA: désintégration multilatérale", "Chine: érosion systématique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "treaty_erosion",
    confidence_score: 0.85,
    data_sources: ["un_treaty_registry", "icj_case_tracker", "multilateral_commitment_index"],
    entities,
    avg_estimated_erosion_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
