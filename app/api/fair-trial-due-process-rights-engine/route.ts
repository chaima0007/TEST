import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[fair-trial-due-process-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Fair Trial Due Process Rights Engine Agent",
  domain: "fair_trial_due_process_rights",
  total_entities: 8,
  avg_composite: 61.40,
  confidence_score: 0.87,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    arbitrary_detention_prolonged_pretrial: 2,
    military_tribunal_civilian_prosecution: 2,
    mass_trial_expedited_process_denial: 2,
    torture_confession_coerced_evidence: 2,
  },
  top_risk_entities: [
    "Chine/Xinjiang — Tribunaux Secrets, Aveux Télévisés Forcés, 1M+ Détenus Sans Procès & Défenseurs Droits Condamnés",
    "Égypte/Al-Sissi — 60 000 Prisonniers Politiques, Tribunaux Militaires Civils, Détention Préventive Infinie & Torture Documentée",
    "Iran/CGRI — Procès 10 Minutes, Défenseurs Isolés, Peine Mort Manifestants & Avocats Emprisonnés Pour Défense",
  ],
  critical_alerts: [
    "Chine/Xinjiang: torture_confession_coerced_evidence",
    "Égypte/Al-Sissi: military_tribunal_civilian_prosecution",
    "Iran/CGRI: mass_trial_expedited_process_denial",
    "Russie/Navalny-Legacy: arbitrary_detention_prolonged_pretrial",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_fair_trial_due_process_rights_index: 6.14,
  data_sources: [
    "fair_trials_international_justice_index_2023",
    "amnesty_international_fair_trial_violations_2023",
    "human_rights_watch_arbitrary_detention_2023",
    "un_special_rapporteur_independence_judges_2023",
  ],
  entities: [
    {
      entity_id: "FTDP-001",
      name: "Chine/Xinjiang — Tribunaux Secrets, Aveux Télévisés Forcés, 1M+ Détenus Sans Procès & Défenseurs Droits Condamnés",
      country: "Chine",
      arbitrary_detention_prolonged_pretrial_score: 95.0,
      military_tribunal_civilian_prosecution_score: 90.0,
      mass_trial_expedited_process_denial_score: 92.0,
      torture_confession_coerced_evidence_score: 97.0,
      composite_score: 93.8,
      risk_level: "critique",
      primary_pattern: "torture_confession_coerced_evidence",
      estimated_fair_trial_due_process_rights_index: 9.38,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "FTDP-002",
      name: "Égypte/Al-Sissi — 60 000 Prisonniers Politiques, Tribunaux Militaires Civils, Détention Préventive Infinie & Torture Documentée",
      country: "Égypte",
      arbitrary_detention_prolonged_pretrial_score: 92.0,
      military_tribunal_civilian_prosecution_score: 94.0,
      mass_trial_expedited_process_denial_score: 89.0,
      torture_confession_coerced_evidence_score: 91.0,
      composite_score: 91.75,
      risk_level: "critique",
      primary_pattern: "military_tribunal_civilian_prosecution",
      estimated_fair_trial_due_process_rights_index: 9.18,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "FTDP-003",
      name: "Iran/CGRI — Procès 10 Minutes, Défenseurs Isolés, Peine Mort Manifestants & Avocats Emprisonnés Pour Défense",
      country: "Iran",
      arbitrary_detention_prolonged_pretrial_score: 88.0,
      military_tribunal_civilian_prosecution_score: 87.0,
      mass_trial_expedited_process_denial_score: 91.0,
      torture_confession_coerced_evidence_score: 89.0,
      composite_score: 88.9,
      risk_level: "critique",
      primary_pattern: "mass_trial_expedited_process_denial",
      estimated_fair_trial_due_process_rights_index: 8.89,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "FTDP-004",
      name: "Russie/Navalny-Legacy — Procès Politiques Médiatisés, Prisonniers Transférés Colonies Arctiques, 3 700 Manifestants Condamnés",
      country: "Russie",
      arbitrary_detention_prolonged_pretrial_score: 86.0,
      military_tribunal_civilian_prosecution_score: 84.0,
      mass_trial_expedited_process_denial_score: 87.0,
      torture_confession_coerced_evidence_score: 85.0,
      composite_score: 85.75,
      risk_level: "critique",
      primary_pattern: "arbitrary_detention_prolonged_pretrial",
      estimated_fair_trial_due_process_rights_index: 8.58,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "FTDP-005",
      name: "Turquie/Post-Coup — 150 000 Purges, Magistrats Révoqués, État Urgence Perpétuel & KHK Décrets Sans Recours",
      country: "Turquie",
      arbitrary_detention_prolonged_pretrial_score: 58.0,
      military_tribunal_civilian_prosecution_score: 56.0,
      mass_trial_expedited_process_denial_score: 59.0,
      torture_confession_coerced_evidence_score: 55.0,
      composite_score: 57.25,
      risk_level: "élevé",
      primary_pattern: "mass_trial_expedited_process_denial",
      estimated_fair_trial_due_process_rights_index: 5.73,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "FTDP-006",
      name: "USA/Guantánamo — Détention Indéfinie Sans Charge, Commissions Militaires, Preuves Torture & Racisme Système Pénal",
      country: "USA",
      arbitrary_detention_prolonged_pretrial_score: 55.0,
      military_tribunal_civilian_prosecution_score: 57.0,
      mass_trial_expedited_process_denial_score: 52.0,
      torture_confession_coerced_evidence_score: 54.0,
      composite_score: 54.65,
      risk_level: "élevé",
      primary_pattern: "military_tribunal_civilian_prosecution",
      estimated_fair_trial_due_process_rights_index: 5.47,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "FTDP-007",
      name: "Fair Trials International — Justice Index, Monitoring Procès Politiques, Rapports Détention Provisoire & Réforme Pénale",
      country: "Global",
      arbitrary_detention_prolonged_pretrial_score: 27.0,
      military_tribunal_civilian_prosecution_score: 26.0,
      mass_trial_expedited_process_denial_score: 25.0,
      torture_confession_coerced_evidence_score: 28.0,
      composite_score: 26.65,
      risk_level: "modéré",
      primary_pattern: "arbitrary_detention_prolonged_pretrial",
      estimated_fair_trial_due_process_rights_index: 2.67,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "FTDP-008",
      name: "ONU/Art.14 PIDCP — Droit Procès Équitable, Présomption Innocence, Indépendance Judiciaire & Principes Bangalors",
      country: "Global",
      arbitrary_detention_prolonged_pretrial_score: 5.0,
      military_tribunal_civilian_prosecution_score: 4.0,
      mass_trial_expedited_process_denial_score: 4.0,
      torture_confession_coerced_evidence_score: 5.0,
      composite_score: 4.55,
      risk_level: "faible",
      primary_pattern: "arbitrary_detention_prolonged_pretrial",
      estimated_fair_trial_due_process_rights_index: 0.46,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/fair-trial-due-process-rights-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
