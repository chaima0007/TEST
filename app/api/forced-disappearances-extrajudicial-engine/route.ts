import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[forced-disappearances-extrajudicial-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Forced Disappearances Extrajudicial Engine Agent",
  domain: "forced_disappearances_extrajudicial",
  total_entities: 8,
  avg_composite: 61.96,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { state_enforced_disappearance_severity: 3, family_notification_denial_body_concealment_scale: 1, impunity_perpetrators_accountability_gap: 2, truth_commission_reparation_mechanism_deficit_gap: 2 },
  top_risk_entities: ["Syrie/Assad — 130 000 Disparus Confirmés, Centres Détention Secrets, Familles Sans Informations & Charniers Découverts Post-Chute", "Argentine 1976-83 — 30 000 Disparus Junte, ESMA Torture, Enfants Volés Adoptions Forcées & Mères Plaza Mayo", "Mexique/Cartels — 100 000 Disparus 2006-24, 50 000 Corps Non-Identifiés, Étudiants Ayotzinapa 43 & Police Complicité"],
  critical_alerts: ["Syrie/Assad: state_enforced_disappearance_severity", "Argentine 1976-83: family_notification_denial_body_concealment_scale", "Mexique/Cartels: impunity_perpetrators_accountability_gap", "Chine/Xinjiang: state_enforced_disappearance_severity"],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_forced_disappearances_extrajudicial_index: 6.2,
  data_sources: ["un_committee_enforced_disappearances_report", "fedefam_latin_america_disappearances_report", "human_rights_watch_enforced_disappearances"],
  entities: [
    { id: "FDE-001", name: "Syrie/Assad — 130 000 Disparus Confirmés, Centres Détention Secrets, Familles Sans Informations & Charniers Découverts Post-Chute", country: "Syrie", composite_score: 94.55, state_enforced_disappearance_severity_score: 96.0, family_notification_denial_body_concealment_scale_score: 94.0, impunity_perpetrators_accountability_gap_score: 93.0, truth_commission_reparation_mechanism_deficit_gap_score: 95.0, risk_level: "critique", primary_pattern: "state_enforced_disappearance_severity", estimated_forced_disappearances_extrajudicial_index: 9.46, last_updated: "2026-06-21" },
    { id: "FDE-002", name: "Argentine 1976-83 — 30 000 Disparus Junte, ESMA Torture, Enfants Volés Adoptions Forcées & Mères Plaza Mayo", country: "Argentine", composite_score: 91.55, state_enforced_disappearance_severity_score: 92.0, family_notification_denial_body_concealment_scale_score: 93.0, impunity_perpetrators_accountability_gap_score: 90.0, truth_commission_reparation_mechanism_deficit_gap_score: 91.0, risk_level: "critique", primary_pattern: "family_notification_denial_body_concealment_scale", estimated_forced_disappearances_extrajudicial_index: 9.15, last_updated: "2026-06-21" },
    { id: "FDE-003", name: "Mexique/Cartels — 100 000 Disparus 2006-24, 50 000 Corps Non-Identifiés, Étudiants Ayotzinapa 43 & Police Complicité", country: "Mexique", composite_score: 87.55, state_enforced_disappearance_severity_score: 88.0, family_notification_denial_body_concealment_scale_score: 86.0, impunity_perpetrators_accountability_gap_score: 89.0, truth_commission_reparation_mechanism_deficit_gap_score: 87.0, risk_level: "critique", primary_pattern: "impunity_perpetrators_accountability_gap", estimated_forced_disappearances_extrajudicial_index: 8.75, last_updated: "2026-06-21" },
    { id: "FDE-004", name: "Chine/Xinjiang — Disparitions Forcées Uyghures, Avocats 709 Disparus, Silence Familles Étranger Menacées & Localisation Inconnue", country: "Chine", composite_score: 83.55, state_enforced_disappearance_severity_score: 84.0, family_notification_denial_body_concealment_scale_score: 82.0, impunity_perpetrators_accountability_gap_score: 85.0, truth_commission_reparation_mechanism_deficit_gap_score: 83.0, risk_level: "critique", primary_pattern: "state_enforced_disappearance_severity", estimated_forced_disappearances_extrajudicial_index: 8.36, last_updated: "2026-06-21" },
    { id: "FDE-005", name: "Sri Lanka — Disparus Guerre Civile 2009, Tamouls Remis Armée Disparus, Commission Vérité Bloquée & Familles Manifester Interdit", country: "Sri Lanka", composite_score: 55.45, state_enforced_disappearance_severity_score: 56.0, family_notification_denial_body_concealment_scale_score: 54.0, impunity_perpetrators_accountability_gap_score: 55.0, truth_commission_reparation_mechanism_deficit_gap_score: 57.0, risk_level: "élevé", primary_pattern: "truth_commission_reparation_mechanism_deficit_gap", estimated_forced_disappearances_extrajudicial_index: 5.54, last_updated: "2026-06-21" },
    { id: "FDE-006", name: "Russie/Tchétchénie — Disparitions Tchétchènes 2000-24, Kadyrov Ennemis Disparus, Memorial Fermé & Familles Intimidées", country: "Russie", composite_score: 52.45, state_enforced_disappearance_severity_score: 52.0, family_notification_denial_body_concealment_scale_score: 51.0, impunity_perpetrators_accountability_gap_score: 54.0, truth_commission_reparation_mechanism_deficit_gap_score: 53.0, risk_level: "élevé", primary_pattern: "impunity_perpetrators_accountability_gap", estimated_forced_disappearances_extrajudicial_index: 5.25, last_updated: "2026-06-21" },
    { id: "FDE-007", name: "FEDEFAM/ASFADDES — Fédération Latinoaméricaine Associations Familles Disparus, Colombie ASFADDES & Réseau International Disparus", country: "Global", composite_score: 26.55, state_enforced_disappearance_severity_score: 27.0, family_notification_denial_body_concealment_scale_score: 25.0, impunity_perpetrators_accountability_gap_score: 28.0, truth_commission_reparation_mechanism_deficit_gap_score: 26.0, risk_level: "modéré", primary_pattern: "truth_commission_reparation_mechanism_deficit_gap", estimated_forced_disappearances_extrajudicial_index: 2.66, last_updated: "2026-06-21" },
    { id: "FDE-008", name: "ONU/Conv 2006 — Convention Internationale Disparitions Forcées 2006, Comité Disparitions Forcées & SDG 16.3 Justice", country: "Global", composite_score: 4.0, state_enforced_disappearance_severity_score: 4.0, family_notification_denial_body_concealment_scale_score: 4.0, impunity_perpetrators_accountability_gap_score: 4.0, truth_commission_reparation_mechanism_deficit_gap_score: 4.0, risk_level: "faible", primary_pattern: "state_enforced_disappearance_severity", estimated_forced_disappearances_extrajudicial_index: 0.4, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/forced-disappearances-extrajudicial-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
