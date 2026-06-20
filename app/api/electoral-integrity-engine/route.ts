import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[electoral-integrity-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Electoral Integrity Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/electoral-integrity-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Electoral Integrity Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Electoral Integrity Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    {
      entity_id: "EL-001",
      name: "Commission Électorale du Myanmar",
      country: "Myanmar",
      sector: "Institutions Électorales",
      composite_score: 81.85,
      voter_suppression_score: 88.0,
      electoral_fraud_score: 82.0,
      media_manipulation_score: 79.0,
      institutional_capture_score: 76.0,
      risk_level: "critique",
      primary_pattern: "Suppression Électorale",
      key_signals: [
        "Suppression massive des listes électorales dans les minorités ethniques",
        "Résultats officiels contradictoires avec les observateurs indépendants",
        "Médias d'État monopolisés pour la propagande pro-gouvernementale",
      ],
      estimated_electoral_index: 8.19,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "EL-002",
      name: "Autorité Électorale Centrale du Venezuela",
      country: "Venezuela",
      sector: "Institutions Électorales",
      composite_score: 76.6,
      voter_suppression_score: 85.0,
      electoral_fraud_score: 78.0,
      media_manipulation_score: 72.0,
      institutional_capture_score: 68.0,
      risk_level: "critique",
      primary_pattern: "Suppression Électorale",
      key_signals: [
        "Intimidation systématique des opposants lors des inscriptions",
        "Procès-verbaux falsifiés dans 34% des bureaux de vote contrôlés",
        "Accès aux médias refusé aux partis d'opposition",
      ],
      estimated_electoral_index: 7.66,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "EL-003",
      name: "Conseil Constitutionnel Électoral du Belarus",
      country: "Belarus",
      sector: "Institutions Électorales",
      composite_score: 69.65,
      voter_suppression_score: 75.0,
      electoral_fraud_score: 71.0,
      media_manipulation_score: 68.0,
      institutional_capture_score: 62.0,
      risk_level: "critique",
      primary_pattern: "Suppression Électorale",
      key_signals: [
        "Arrestation de 1 200 observateurs électoraux indépendants",
        "Bourrage d'urnes documenté par des témoins dans 18 régions",
        "Résultats annoncés avant la fermeture des bureaux de vote",
      ],
      estimated_electoral_index: 6.97,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "EL-004",
      name: "Commission Indépendante Électorale du Bangladesh",
      country: "Bangladesh",
      sector: "Institutions Électorales",
      composite_score: 59.5,
      voter_suppression_score: 58.0,
      electoral_fraud_score: 60.0,
      media_manipulation_score: 62.0,
      institutional_capture_score: 58.0,
      risk_level: "élevé",
      primary_pattern: "Manipulation Médiatique",
      key_signals: [
        "Violence politique lors des campagnes électorales rurales",
        "Pression sur les juges électoraux pour validation de résultats contestés",
        "Désinformation coordonnée sur les réseaux sociaux pro-gouvernementaux",
      ],
      estimated_electoral_index: 5.95,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "EL-005",
      name: "Commission Nationale Électorale du Niger",
      country: "Niger",
      sector: "Institutions Électorales",
      composite_score: 53.85,
      voter_suppression_score: 52.0,
      electoral_fraud_score: 55.0,
      media_manipulation_score: 58.0,
      institutional_capture_score: 50.0,
      risk_level: "élevé",
      primary_pattern: "Désinformation Virale",
      key_signals: [
        "Accès limité aux zones rurales pour l'enregistrement des électeurs",
        "Financement opaque des campagnes électorales non audité",
        "Pressions militaires sur les commissions locales de dépouillement",
      ],
      estimated_electoral_index: 5.39,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "EL-006",
      name: "Agence Centrale Électorale de Tunisie",
      country: "Tunisie",
      sector: "Institutions Électorales",
      composite_score: 29.4,
      voter_suppression_score: 35.0,
      electoral_fraud_score: 30.0,
      media_manipulation_score: 28.0,
      institutional_capture_score: 22.0,
      risk_level: "modéré",
      primary_pattern: "Aucun",
      key_signals: [
        "Réduction des délais d'inscription favorisant les candidats sortants",
        "Financement inégal des partis d'opposition versus majorité",
        "Pressions administratives sur les candidatures indépendantes",
      ],
      estimated_electoral_index: 2.94,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "EL-007",
      name: "Commission Électorale Fédérale d'Allemagne",
      country: "Allemagne",
      sector: "Institutions Électorales",
      composite_score: 9.8,
      voter_suppression_score: 10.0,
      electoral_fraud_score: 8.0,
      media_manipulation_score: 12.0,
      institutional_capture_score: 9.0,
      risk_level: "faible",
      primary_pattern: "Aucun",
      key_signals: [
        "Système de vote papier vérifiable avec piste d'audit complète",
        "Observateurs multipartites présents dans 100% des bureaux",
        "Médias indépendants garantis par cadre constitutionnel renforcé",
      ],
      estimated_electoral_index: 0.98,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "EL-008",
      name: "Conseil Électoral Permanent de Nouvelle-Zélande",
      country: "Nouvelle-Zélande",
      sector: "Institutions Électorales",
      composite_score: 11.3,
      voter_suppression_score: 14.0,
      electoral_fraud_score: 12.0,
      media_manipulation_score: 10.0,
      institutional_capture_score: 8.0,
      risk_level: "faible",
      primary_pattern: "Aucun",
      key_signals: [
        "Taux de participation électorale de 82% avec inscription automatique",
        "Transparence totale des financements de campagne en temps réel",
        "Système de vote anticipé multi-canal sans obstacles administratifs",
      ],
      estimated_electoral_index: 1.13,
      last_updated: "2026-06-20",
    },
  ];

  const summary = {
    total_entities: 8,
    avg_composite: 48.99,
    risk_distribution: { critique: 3, "élevé": 2, "modéré": 1, faible: 2 },
    pattern_distribution: {
      "Suppression Électorale": 3,
      "Fraude Systémique": 2,
      "Manipulation Médiatique": 3,
      "Capture Institutionnelle": 2,
      "Désinformation Virale": 5,
    },
    top_risk_entities: [
      "Commission Électorale du Myanmar",
      "Autorité Électorale Centrale du Venezuela",
      "Conseil Constitutionnel Électoral du Belarus",
    ],
    critical_alerts: [
      "ALERTE CRITIQUE: Commission Électorale du Myanmar (Myanmar) — score 81.85/100",
      "ALERTE CRITIQUE: Autorité Électorale Centrale du Venezuela (Venezuela) — score 76.60/100",
      "ALERTE CRITIQUE: Conseil Constitutionnel Électoral du Belarus (Belarus) — score 69.65/100",
    ],
    last_analysis: "2026-06-20T00:00:00Z",
    engine_version: "1.0.0",
    domain: "electoral",
    confidence_score: 87.5,
    data_sources: [
      "International IDEA Electoral Integrity Database",
      "NDI Election Observation Reports",
      "Freedom House Electoral Process Indicators",
      "OSCE/ODIHR Mission Reports",
    ],
    entities,
    avg_estimated_electoral_index: 4.9,
  };

  return { entities, summary };
}
