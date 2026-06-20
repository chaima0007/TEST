import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[amr-global-response-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(
      sealResponse(getMockData(), "AMR Global Response Engine Agent"),
    );
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/amr-global-response-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "AMR Global Response Engine Agent"));
  } catch {
    return NextResponse.json(
      sealResponse(getMockData(), "AMR Global Response Engine Agent"),
      { status: 502 },
    );
  }
}

function getMockData() {
  const entities = [
    {
      entity_id: "ENT-001",
      name: "WHO AMR Task Force",
      country: "Suisse",
      sector: "Santé Mondiale",
      composite_score: 73.2,
      detection_score: 80.0,
      treatment_score: 72.0,
      containment_score: 68.0,
      cooperation_score: 71.0,
      risk_level: "critique",
      primary_pattern: "resistance_totale",
      key_signals: [
        "Détection AMR critique — score 80.0/100 : Résistance totale détectée — tous antibiotiques de dernier recours inefficaces",
        "Pipeline thérapeutique en déficit sévère — 72.0/100 traitements disponibles",
        "Coopération mondiale insuffisante — indice 71.0/100 : coordination AMR urgente",
      ],
      estimated_amr_index: 7.32,
      last_updated: "2026-06-20",
      outbreak_count: 47,
    },
    {
      entity_id: "ENT-002",
      name: "South Asia AMR Hub",
      country: "Inde",
      sector: "Santé Publique",
      composite_score: 68.45,
      detection_score: 76.0,
      treatment_score: 65.0,
      containment_score: 68.0,
      cooperation_score: 62.0,
      risk_level: "critique",
      primary_pattern: "resistance_totale",
      key_signals: [
        "Détection AMR critique — score 76.0/100 : Résistance totale détectée — tous antibiotiques de dernier recours inefficaces",
        "Pipeline thérapeutique en déficit sévère — 65.0/100 traitements disponibles",
        "Coopération mondiale insuffisante — indice 62.0/100 : coordination AMR urgente",
      ],
      estimated_amr_index: 6.85,
      last_updated: "2026-06-20",
      outbreak_count: 312,
    },
    {
      entity_id: "ENT-003",
      name: "African Resistance Network",
      country: "Nigeria",
      sector: "Épidémiologie",
      composite_score: 61.7,
      detection_score: 68.0,
      treatment_score: 62.0,
      containment_score: 60.0,
      cooperation_score: 54.0,
      risk_level: "critique",
      primary_pattern: "reponse_amr_coordonnee",
      key_signals: [
        "Détection AMR critique — score 68.0/100 : Coordination AMR opérationnelle — systèmes de veille actifs",
        "Pipeline thérapeutique en déficit sévère — 62.0/100 traitements disponibles",
        "Coopération mondiale insuffisante — indice 54.0/100 : coordination AMR urgente",
      ],
      estimated_amr_index: 6.17,
      last_updated: "2026-06-20",
      outbreak_count: 189,
    },
    {
      entity_id: "ENT-004",
      name: "EU AMR Action Plan",
      country: "Belgique",
      sector: "Politique Sanitaire",
      composite_score: 51.9,
      detection_score: 56.0,
      treatment_score: 52.0,
      containment_score: 50.0,
      cooperation_score: 48.0,
      risk_level: "élevé",
      primary_pattern: "reponse_amr_coordonnee",
      key_signals: [
        "Détection AMR élevée — score 56.0/100 : surveillance renforcée requise",
        "Pipeline thérapeutique sous tension — 52.0/100 options thérapeutiques",
        "Coopération internationale partielle — indice 48.0/100 : renforcement nécessaire",
      ],
      estimated_amr_index: 5.19,
      last_updated: "2026-06-20",
      outbreak_count: 23,
    },
    {
      entity_id: "ENT-005",
      name: "LATAM Health Consortium",
      country: "Brésil",
      sector: "Recherche Clinique",
      composite_score: 45.0,
      detection_score: 50.0,
      treatment_score: 44.0,
      containment_score: 44.0,
      cooperation_score: 40.0,
      risk_level: "élevé",
      primary_pattern: "reponse_amr_coordonnee",
      key_signals: [
        "Détection AMR élevée — score 50.0/100 : surveillance renforcée requise",
        "Pipeline thérapeutique sous tension — 44.0/100 options thérapeutiques",
        "Coopération internationale partielle — indice 40.0/100 : renforcement nécessaire",
      ],
      estimated_amr_index: 4.5,
      last_updated: "2026-06-20",
      outbreak_count: 78,
    },
    {
      entity_id: "ENT-006",
      name: "Nordic AMR Institute",
      country: "Suède",
      sector: "Recherche & Développement",
      composite_score: 28.8,
      detection_score: 32.0,
      treatment_score: 28.0,
      containment_score: 28.0,
      cooperation_score: 26.0,
      risk_level: "modéré",
      primary_pattern: "reponse_amr_coordonnee",
      key_signals: [
        "Détection AMR modérée — score 32.0/100 : veille épidémiologique maintenue",
        "Pipeline thérapeutique opérationnel — 28.0/100 traitements en développement",
        "Coopération internationale satisfaisante — indice 26.0/100 : protocoles actifs",
      ],
      estimated_amr_index: 2.88,
      last_updated: "2026-06-20",
      outbreak_count: 8,
    },
    {
      entity_id: "ENT-007",
      name: "Singapore Biomed Centre",
      country: "Singapour",
      sector: "Biotechnologie",
      composite_score: 13.7,
      detection_score: 16.0,
      treatment_score: 14.0,
      containment_score: 12.0,
      cooperation_score: 12.0,
      risk_level: "faible",
      primary_pattern: "reponse_amr_coordonnee",
      key_signals: [
        "Détection AMR faible — score 16.0/100 : situation sous contrôle",
        "Pipeline thérapeutique solide — 14.0/100 antimicrobiens disponibles",
        "Coopération internationale forte — indice 12.0/100 : réponse coordonnée",
      ],
      estimated_amr_index: 1.37,
      last_updated: "2026-06-20",
      outbreak_count: 3,
    },
    {
      entity_id: "ENT-008",
      name: "Swiss Precision Health",
      country: "Suisse",
      sector: "Médecine de Précision",
      composite_score: 8.05,
      detection_score: 9.0,
      treatment_score: 8.0,
      containment_score: 7.0,
      cooperation_score: 8.0,
      risk_level: "faible",
      primary_pattern: "reponse_amr_coordonnee",
      key_signals: [
        "Détection AMR faible — score 9.0/100 : situation sous contrôle",
        "Pipeline thérapeutique solide — 8.0/100 antimicrobiens disponibles",
        "Coopération internationale forte — indice 8.0/100 : réponse coordonnée",
      ],
      estimated_amr_index: 0.81,
      last_updated: "2026-06-20",
      outbreak_count: 1,
    },
  ];

  const avgComposite = Math.round(
    (entities.reduce((s, e) => s + e.composite_score, 0) / entities.length) * 100
  ) / 100;

  return {
    total_entities: 8,
    avg_composite: avgComposite,
    risk_distribution: { critique: 3, "élevé": 2, "modéré": 1, faible: 2 },
    pattern_distribution: {
      resistance_totale: 2,
      pipeline_vide: 0,
      confinement_echoue: 0,
      cooperation_absente: 0,
      reponse_amr_coordonnee: 6,
    },
    top_risk_entities: ["WHO AMR Task Force", "South Asia AMR Hub", "African Resistance Network"],
    critical_alerts: [
      "[ALERTE CRITIQUE] WHO AMR Task Force (Suisse) — Score 73.2 — Foyers: 47",
      "[ALERTE CRITIQUE] South Asia AMR Hub (Inde) — Score 68.5 — Foyers: 312",
      "[ALERTE CRITIQUE] African Resistance Network (Nigeria) — Score 61.7 — Foyers: 189",
    ],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "amr",
    confidence_score: 0.89,
    data_sources: ["who_surveillance", "clinical_trials_db", "resistance_monitoring"],
    entities,
    avg_estimated_amr_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
  };
}
