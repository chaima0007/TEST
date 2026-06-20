import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[civilizational-debt-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(
      sealResponse(getMockData(), "Civilizational Debt Engine Agent"),
    );
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/civilizational-debt-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Civilizational Debt Engine Agent"));
  } catch {
    return NextResponse.json(
      sealResponse(getMockData(), "Civilizational Debt Engine Agent"),
      { status: 502 },
    );
  }
}

function getMockData() {
  const entities = [
    {
      entity_id: "CD-001",
      name: "États-Unis",
      country: "États-Unis",
      sector: "Nation-État",
      composite_score: 73.5,
      ecological_debt_score: 75.0,
      financial_debt_score: 80.0,
      social_debt_score: 72.0,
      institutional_debt_score: 65.0,
      risk_level: "critique",
      primary_pattern: "effondrement_generationnel",
      key_signals: [
        "Dette écologique critique — score 75.0/100 : Effondrement générationnel imminent — les générations futures ne pourront honorer cet héritage",
        "Dette financière souveraine alarmante — 80.0/100 — engagements non financés massifs",
        "Dette sociale explosive — indice 72.0/100 : inégalités et désinvestissements structurels",
      ],
      estimated_civdebt_index: 7.35,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "CD-002",
      name: "Chine",
      country: "Chine",
      sector: "Nation-État",
      composite_score: 74.7,
      ecological_debt_score: 82.0,
      financial_debt_score: 70.0,
      social_debt_score: 68.0,
      institutional_debt_score: 78.0,
      risk_level: "critique",
      primary_pattern: "effondrement_generationnel",
      key_signals: [
        "Dette écologique critique — score 82.0/100 : Effondrement générationnel imminent — les générations futures ne pourront honorer cet héritage",
        "Dette financière souveraine alarmante — 70.0/100 — engagements non financés massifs",
        "Dette sociale explosive — indice 68.0/100 : inégalités et désinvestissements structurels",
      ],
      estimated_civdebt_index: 7.47,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "CD-003",
      name: "Brésil",
      country: "Brésil",
      sector: "Nation-État",
      composite_score: 72.4,
      ecological_debt_score: 78.0,
      financial_debt_score: 65.0,
      social_debt_score: 75.0,
      institutional_debt_score: 70.0,
      risk_level: "critique",
      primary_pattern: "effondrement_generationnel",
      key_signals: [
        "Dette écologique critique — score 78.0/100 : Effondrement générationnel imminent — les générations futures ne pourront honorer cet héritage",
        "Dette financière souveraine alarmante — 65.0/100 — engagements non financés massifs",
        "Dette sociale explosive — indice 75.0/100 : inégalités et désinvestissements structurels",
      ],
      estimated_civdebt_index: 7.24,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "CD-004",
      name: "Italie",
      country: "Italie",
      sector: "Nation-État",
      composite_score: 57.1,
      ecological_debt_score: 55.0,
      financial_debt_score: 72.0,
      social_debt_score: 52.0,
      institutional_debt_score: 48.0,
      risk_level: "élevé",
      primary_pattern: "transfert_massif_risques",
      key_signals: [
        "Dette écologique élevée — score 55.0/100 : pression environnementale forte",
        "Dette financière préoccupante — 72.0/100 — trajectoire insoutenable",
        "Dette sociale en hausse — indice 52.0/100 : tensions intergénérationnelles croissantes",
      ],
      estimated_civdebt_index: 5.71,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "CD-005",
      name: "Nigéria",
      country: "Nigéria",
      sector: "Nation-État",
      composite_score: 66.55,
      ecological_debt_score: 68.0,
      financial_debt_score: 55.0,
      social_debt_score: 80.0,
      institutional_debt_score: 62.0,
      risk_level: "critique",
      primary_pattern: "effondrement_generationnel",
      key_signals: [
        "Dette écologique critique — score 68.0/100 : Effondrement générationnel imminent — les générations futures ne pourront honorer cet héritage",
        "Dette financière souveraine alarmante — 55.0/100 — engagements non financés massifs",
        "Dette sociale explosive — indice 80.0/100 : inégalités et désinvestissements structurels",
      ],
      estimated_civdebt_index: 6.66,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "CD-006",
      name: "Allemagne",
      country: "Allemagne",
      sector: "Nation-État",
      composite_score: 42.1,
      ecological_debt_score: 42.0,
      financial_debt_score: 52.0,
      social_debt_score: 38.0,
      institutional_debt_score: 35.0,
      risk_level: "élevé",
      primary_pattern: "erosion_heritages",
      key_signals: [
        "Dette écologique élevée — score 42.0/100 : pression environnementale forte",
        "Dette financière préoccupante — 52.0/100 — trajectoire insoutenable",
        "Dette sociale en hausse — indice 38.0/100 : tensions intergénérationnelles croissantes",
      ],
      estimated_civdebt_index: 4.21,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "CD-007",
      name: "Danemark",
      country: "Danemark",
      sector: "Nation-État",
      composite_score: 21.4,
      ecological_debt_score: 28.0,
      financial_debt_score: 22.0,
      social_debt_score: 18.0,
      institutional_debt_score: 15.0,
      risk_level: "modéré",
      primary_pattern: "accumulation_silencieuse",
      key_signals: [
        "Dette écologique modérée — score 28.0/100 : surveillance maintenue",
        "Dette financière gérable — 22.0/100 — vigilance nécessaire",
        "Dette sociale contenue — indice 18.0/100 : politiques d'équité actives",
      ],
      estimated_civdebt_index: 2.14,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "CD-008",
      name: "Singapour",
      country: "Singapour",
      sector: "Nation-État",
      composite_score: 11.6,
      ecological_debt_score: 15.0,
      financial_debt_score: 12.0,
      social_debt_score: 10.0,
      institutional_debt_score: 8.0,
      risk_level: "faible",
      primary_pattern: "equilibre_intergenerationnel",
      key_signals: [
        "Dette écologique faible — score 15.0/100 : gestion durable exemplaire",
        "Dette financière maîtrisée — 12.0/100 — équilibre budgétaire intergénérationnel",
        "Dette sociale minimale — indice 10.0/100 : cohésion sociale et équité préservées",
      ],
      estimated_civdebt_index: 1.16,
      last_updated: "2026-06-20",
    },
  ];

  const avgComposite =
    Math.round((entities.reduce((s, e) => s + e.composite_score, 0) / entities.length) * 100) / 100;

  return {
    total_entities: 8,
    avg_composite: avgComposite,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: {
      effondrement_generationnel: 4,
      transfert_massif_risques: 1,
      erosion_heritages: 1,
      accumulation_silencieuse: 1,
      equilibre_intergenerationnel: 1,
    },
    top_risk_entities: ["Chine", "États-Unis", "Brésil"],
    critical_alerts: [
      "[ALERTE CRITIQUE] Chine (Chine) — Dette civilisationnelle 74.7/100 — Urgence intergénérationnelle",
      "[ALERTE CRITIQUE] États-Unis (États-Unis) — Dette civilisationnelle 73.5/100 — Urgence intergénérationnelle",
      "[ALERTE CRITIQUE] Brésil (Brésil) — Dette civilisationnelle 72.4/100 — Urgence intergénérationnelle",
      "[ALERTE CRITIQUE] Nigéria (Nigéria) — Dette civilisationnelle 66.6/100 — Urgence intergénérationnelle",
    ],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "civdebt",
    confidence_score: 0.86,
    data_sources: [
      "intergenerational_justice_index",
      "ecological_debt_tracker",
      "sovereign_debt_monitor",
    ],
    entities,
    avg_estimated_civdebt_index: Math.round((avgComposite / 100) * 10 * 100) / 100,
  };
}
