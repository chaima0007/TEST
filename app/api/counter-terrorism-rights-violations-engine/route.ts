import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[counter-terrorism-rights-violations-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Counter Terrorism Rights Violations Engine Agent",
  domain: "counter_terrorism_rights_violations",
  total_entities: 8,
  avg_composite: 61.68,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { antiterrorism_law_political_misuse_severity: 4, secret_detention_torture_rendition_scale: 1, mass_surveillance_privacy_violation: 1, fair_trial_rights_suspension_terrorism_deficit_gap: 2 },
  top_risk_entities: ["Chine/Xinjiang — Lois CTR Uyghurs, 1M Internés Camps Rééducation, Algorithmes Prédictifs & Famille Étrangère Détenue", "USA/GWOT — Guantanamo 700+ Détenus, Renditions CIA 50 Pays, NSA PRISM Surveillance & Torture Memos Légalisée", "Égypte/Sissi — Loi CTR 2015 ONG Criminalisées, 60k Prisonniers, Tribunaux Militaires Civils & Avocats Détenus"],
  critical_alerts: ["Chine/Xinjiang: antiterrorism_law_political_misuse_severity", "USA/GWOT: secret_detention_torture_rendition_scale", "Égypte/Sissi: antiterrorism_law_political_misuse_severity", "France/SILT: mass_surveillance_privacy_violation"],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_counter_terrorism_rights_violations_index: 6.17,
  data_sources: ["un_special_rapporteur_counter_terrorism_rights", "aclu_global_war_terror_accountability_report", "human_rights_watch_antiterrorism_law_misuse"],
  entities: [
    { entity_id: "CTR-001", name: "Chine/Xinjiang — Lois CTR Uyghurs, 1M Internés Camps Rééducation, Algorithmes Prédictifs & Famille Étrangère Détenue", country: "Chine", composite_score: 94.65, antiterrorism_law_political_misuse_severity_score: 96.0, secret_detention_torture_rendition_scale_score: 94.0, mass_surveillance_privacy_violation_score: 95.0, fair_trial_rights_suspension_terrorism_deficit_gap_score: 93.0, risk_level: "critique", primary_pattern: "antiterrorism_law_political_misuse_severity", estimated_counter_terrorism_rights_violations_index: 9.46, last_updated: "2026-06-21" }
    { entity_id: "CTR-002", name: "USA/GWOT — Guantanamo 700+ Détenus, Renditions CIA 50 Pays, NSA PRISM Surveillance & Torture Memos Légalisée", country: "USA", composite_score: 91.2, antiterrorism_law_political_misuse_severity_score: 91.0, secret_detention_torture_rendition_scale_score: 93.0, mass_surveillance_privacy_violation_score: 89.0, fair_trial_rights_suspension_terrorism_deficit_gap_score: 92.0, risk_level: "critique", primary_pattern: "secret_detention_torture_rendition_scale", estimated_counter_terrorism_rights_violations_index: 9.12, last_updated: "2026-06-21" }
    { entity_id: "CTR-003", name: "Égypte/Sissi — Loi CTR 2015 ONG Criminalisées, 60k Prisonniers, Tribunaux Militaires Civils & Avocats Détenus", country: "Égypte", composite_score: 86.65, antiterrorism_law_political_misuse_severity_score: 88.0, secret_detention_torture_rendition_scale_score: 86.0, mass_surveillance_privacy_violation_score: 87.0, fair_trial_rights_suspension_terrorism_deficit_gap_score: 85.0, risk_level: "critique", primary_pattern: "antiterrorism_law_political_misuse_severity", estimated_counter_terrorism_rights_violations_index: 8.67, last_updated: "2026-06-21" }
    { entity_id: "CTR-004", name: "France/SILT — État Urgence Permanent, Assignations Résidence Militants, DGSI Surveillance Mosquées & Critiques Perquisitions", country: "France", composite_score: 83.8, antiterrorism_law_political_misuse_severity_score: 84.0, secret_detention_torture_rendition_scale_score: 82.0, mass_surveillance_privacy_violation_score: 86.0, fair_trial_rights_suspension_terrorism_deficit_gap_score: 83.0, risk_level: "critique", primary_pattern: "mass_surveillance_privacy_violation", estimated_counter_terrorism_rights_violations_index: 8.38, last_updated: "2026-06-21" }
    { entity_id: "CTR-005", name: "Russie/Extrémisme — Loi Extrémisme Témoins Jéhovah Bannis, Novichok Navalny, FSB Provocateurs & Mosquées Surveillées", country: "Russie", composite_score: 54.65, antiterrorism_law_political_misuse_severity_score: 56.0, secret_detention_torture_rendition_scale_score: 54.0, mass_surveillance_privacy_violation_score: 55.0, fair_trial_rights_suspension_terrorism_deficit_gap_score: 53.0, risk_level: "élevé", primary_pattern: "antiterrorism_law_political_misuse_severity", estimated_counter_terrorism_rights_violations_index: 5.46, last_updated: "2026-06-21" }
    { entity_id: "CTR-006", name: "UK/Schedule 7 — Arrêtés Frontières Journalistes, Prevent Programme Écoles, GCHQ Surveillance Masse & Loi OSA Lanceurs Alertes", country: "UK", composite_score: 51.85, antiterrorism_law_political_misuse_severity_score: 52.0, secret_detention_torture_rendition_scale_score: 51.0, mass_surveillance_privacy_violation_score: 54.0, fair_trial_rights_suspension_terrorism_deficit_gap_score: 50.0, risk_level: "élevé", primary_pattern: "fair_trial_rights_suspension_terrorism_deficit_gap", estimated_counter_terrorism_rights_violations_index: 5.18, last_updated: "2026-06-21" }
    { entity_id: "CTR-007", name: "ICJ/Airwaves — Mémo Johannesburg CTR Droits, Rapporteur Spécial Droits Humains CTR & Standards Helsinki", country: "Global", composite_score: 26.6, antiterrorism_law_political_misuse_severity_score: 27.0, secret_detention_torture_rendition_scale_score: 26.0, mass_surveillance_privacy_violation_score: 28.0, fair_trial_rights_suspension_terrorism_deficit_gap_score: 25.0, risk_level: "modéré", primary_pattern: "fair_trial_rights_suspension_terrorism_deficit_gap", estimated_counter_terrorism_rights_violations_index: 2.66, last_updated: "2026-06-21" }
    { entity_id: "CTR-008", name: "ONU/Résolutions — Résolution 1373 CTR 2001, Stratégie Mondiale CTR ONU, Rapporteur Spécial & Standards Droits Fondamentaux", country: "Global", composite_score: 4.0, antiterrorism_law_political_misuse_severity_score: 4.0, secret_detention_torture_rendition_scale_score: 4.0, mass_surveillance_privacy_violation_score: 4.0, fair_trial_rights_suspension_terrorism_deficit_gap_score: 4.0, risk_level: "faible", primary_pattern: "antiterrorism_law_political_misuse_severity", estimated_counter_terrorism_rights_violations_index: 0.4, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/counter-terrorism-rights-violations-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
