import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[right-to-fair-trial-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[right-to-fair-trial-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Right To Fair Trial Rights Engine Agent",
  domain: "right_to_fair_trial_rights",
  total_entities: 8,
  avg_composite: 60.61,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Arabie Saoudite — Cours Spéciales Terrorisme Sans Défenseurs, Aveux Sous Contrainte & Zéro Indépendance Judiciaire",
    "Chine — Justice Contrôlée par le PCC, Aveux Forcés Télévisés & Taux Condamnation 99,9%",
    "Russie — Tribunaux Politiques Kremlin, Procès Navalny & Taux Acquittement 0,3% Historique",
  ],
  critical_alerts: [
    "Arabie Saoudite: arbitrary_detention_score",
    "Chine: judicial_independence_score",
    "Russie: fair_trial_guarantee_score",
    "Biélorussie: judicial_independence_score",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_right_to_fair_trial_rights_index: 6.06,
  entities: [
    {
      entity_id: "RFT-001",
      name: "Arabie Saoudite — Cours Spéciales Terrorisme Sans Défenseurs, Aveux Sous Contrainte & Zéro Indépendance Judiciaire",
      country: "Arabie Saoudite",
      judicial_independence_score: 90.0,
      fair_trial_guarantee_score: 89.0,
      legal_aid_access_score: 88.0,
      arbitrary_detention_score: 91.0,
      composite_score: 89.45,
      risk_level: "critique",
      primary_pattern: "arbitrary_detention_score",
      estimated_right_to_fair_trial_rights_index: 8.95,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RFT-002",
      name: "Chine — Justice Contrôlée par le PCC, Aveux Forcés Télévisés & Taux Condamnation 99,9%",
      country: "Chine",
      judicial_independence_score: 88.0,
      fair_trial_guarantee_score: 87.0,
      legal_aid_access_score: 85.0,
      arbitrary_detention_score: 89.0,
      composite_score: 87.2,
      risk_level: "critique",
      primary_pattern: "judicial_independence_score",
      estimated_right_to_fair_trial_rights_index: 8.72,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RFT-003",
      name: "Russie — Tribunaux Politiques Kremlin, Procès Navalny & Taux Acquittement 0,3% Historique",
      country: "Russie",
      judicial_independence_score: 85.0,
      fair_trial_guarantee_score: 84.0,
      legal_aid_access_score: 82.0,
      arbitrary_detention_score: 87.0,
      composite_score: 84.4,
      risk_level: "critique",
      primary_pattern: "fair_trial_guarantee_score",
      estimated_right_to_fair_trial_rights_index: 8.44,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RFT-004",
      name: "Biélorussie — Procès Politiques Loukachenko, Avocats Défenseurs Emprisonnés & Cours Secrètes",
      country: "Biélorussie",
      judicial_independence_score: 83.0,
      fair_trial_guarantee_score: 82.0,
      legal_aid_access_score: 80.0,
      arbitrary_detention_score: 84.0,
      composite_score: 82.2,
      risk_level: "critique",
      primary_pattern: "judicial_independence_score",
      estimated_right_to_fair_trial_rights_index: 8.22,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RFT-005",
      name: "Iran — Tribunaux Révolutionnaires Islamiques, Condamnations à Mort Express & Avocats Exclus",
      country: "Iran",
      judicial_independence_score: 55.0,
      fair_trial_guarantee_score: 54.0,
      legal_aid_access_score: 50.0,
      arbitrary_detention_score: 57.0,
      composite_score: 53.9,
      risk_level: "élevé",
      primary_pattern: "arbitrary_detention_score",
      estimated_right_to_fair_trial_rights_index: 5.39,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RFT-006",
      name: "Turquie — Purge Judiciaire Post-2016, 4000 Juges Révoqués & Procès Journalistes Massifs",
      country: "Turquie",
      judicial_independence_score: 48.0,
      fair_trial_guarantee_score: 47.0,
      legal_aid_access_score: 44.0,
      arbitrary_detention_score: 50.0,
      composite_score: 47.15,
      risk_level: "élevé",
      primary_pattern: "judicial_independence_score",
      estimated_right_to_fair_trial_rights_index: 4.72,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RFT-007",
      name: "Inde — Lenteur Judiciaire Chronique, 50 Millions Affaires en Attente & Détention Préventive Prolongée",
      country: "Inde",
      judicial_independence_score: 30.0,
      fair_trial_guarantee_score: 28.0,
      legal_aid_access_score: 32.0,
      arbitrary_detention_score: 29.0,
      composite_score: 29.8,
      risk_level: "modéré",
      primary_pattern: "legal_aid_access_score",
      estimated_right_to_fair_trial_rights_index: 2.98,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RFT-008",
      name: "Danemark — Indépendance Judiciaire Référence Mondiale, Aide Juridique Universelle & Acquittements Respectés",
      country: "Danemark",
      judicial_independence_score: 11.0,
      fair_trial_guarantee_score: 10.0,
      legal_aid_access_score: 12.0,
      arbitrary_detention_score: 10.0,
      composite_score: 10.8,
      risk_level: "faible",
      primary_pattern: "legal_aid_access_score",
      estimated_right_to_fair_trial_rights_index: 1.08,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/right-to-fair-trial-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(
      NextResponse.json({ payload: FALLBACK_PAYLOAD }, { status: 502 })
    );
  }
}
