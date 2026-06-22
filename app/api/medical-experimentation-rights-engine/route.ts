import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[medical-experimentation-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Medical Experimentation Rights Engine Agent",
  domain: "medical_experimentation_rights",
  total_entities: 8,
  avg_composite: 60.58,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Chine — Expérimentation forcée sur prisonniers & minorités",
    "Corée du Nord — Essais sur détenus politiques sans consentement",
    "Syrie — Armes chimiques & expérimentations en zones de conflit",
  ],
  critical_alerts: [
    "Chine: Forced organ harvesting & non-consensual trials on Uyghurs",
    "Corée du Nord: State-run human experimentation on political prisoners",
    "Syrie: Chemical weapon exposure & undocumented medical trials",
    "Guatemala/USA (historique): Legacy non-consensual STD experiments",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_medical_experimentation_rights_index: 6.06,
  entities: [
    {
      entity_id: "MER-001",
      name: "Chine — Expérimentation forcée sur prisonniers Ouïghours",
      country: "Chine",
      non_consensual_experimentation_score: 96.0,
      vulnerable_population_targeting_score: 97.0,
      regulatory_oversight_gap_score: 92.0,
      accountability_impunity_score: 95.0,
      composite_score: 95.05,
      risk_level: "critique",
      primary_pattern: "State-sponsored non-consensual trials on ethnic minorities",
      estimated_medical_experimentation_rights_index: 9.51,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "MER-002",
      name: "Corée du Nord — Essais biologiques sur détenus politiques",
      country: "Corée du Nord",
      non_consensual_experimentation_score: 94.0,
      vulnerable_population_targeting_score: 96.0,
      regulatory_oversight_gap_score: 98.0,
      accountability_impunity_score: 97.0,
      composite_score: 96.15,
      risk_level: "critique",
      primary_pattern: "Political prisoner experimentation with total impunity",
      estimated_medical_experimentation_rights_index: 9.62,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "MER-003",
      name: "Syrie — Armes chimiques & essais non déclarés en zone de conflit",
      country: "Syrie",
      non_consensual_experimentation_score: 88.0,
      vulnerable_population_targeting_score: 85.0,
      regulatory_oversight_gap_score: 90.0,
      accountability_impunity_score: 87.0,
      composite_score: 87.7,
      risk_level: "critique",
      primary_pattern: "Conflict-zone chemical exposure & undocumented trials",
      estimated_medical_experimentation_rights_index: 8.77,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "MER-004",
      name: "Guatemala — Héritage expériences IST non consenties (modèle USA)",
      country: "Guatemala",
      non_consensual_experimentation_score: 82.0,
      vulnerable_population_targeting_score: 80.0,
      regulatory_oversight_gap_score: 78.0,
      accountability_impunity_score: 85.0,
      composite_score: 81.35,
      risk_level: "critique",
      primary_pattern: "Legacy non-consensual STD experiments on prisoners & soldiers",
      estimated_medical_experimentation_rights_index: 8.14,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "MER-005",
      name: "Inde — Essais cliniques non éthiques sur populations rurales vulnérables",
      country: "Inde",
      non_consensual_experimentation_score: 55.0,
      vulnerable_population_targeting_score: 62.0,
      regulatory_oversight_gap_score: 58.0,
      accountability_impunity_score: 50.0,
      composite_score: 56.65,
      risk_level: "élevé",
      primary_pattern: "Underpowered regulatory oversight in rural clinical trials",
      estimated_medical_experimentation_rights_index: 5.67,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "MER-006",
      name: "Afrique subsaharienne — Essais pharmaceutiques à approbation accélérée",
      country: "Afrique subsaharienne",
      non_consensual_experimentation_score: 48.0,
      vulnerable_population_targeting_score: 55.0,
      regulatory_oversight_gap_score: 52.0,
      accountability_impunity_score: 44.0,
      composite_score: 49.85,
      risk_level: "élevé",
      primary_pattern: "Pharmaceutical fast-track trials with weak informed consent",
      estimated_medical_experimentation_rights_index: 4.99,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "MER-007",
      name: "Brésil — Lacunes consentement éclairé dans essais OGM & vaccins",
      country: "Brésil",
      non_consensual_experimentation_score: 28.0,
      vulnerable_population_targeting_score: 30.0,
      regulatory_oversight_gap_score: 26.0,
      accountability_impunity_score: 24.0,
      composite_score: 27.3,
      risk_level: "modéré",
      primary_pattern: "Informed consent gaps in GMO and vaccine trials",
      estimated_medical_experimentation_rights_index: 2.73,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "MER-008",
      name: "UE — Cadre Helsinki + RGPD, contrôle éthique renforcé",
      country: "Union Européenne",
      non_consensual_experimentation_score: 10.0,
      vulnerable_population_targeting_score: 8.0,
      regulatory_oversight_gap_score: 6.0,
      accountability_impunity_score: 9.0,
      composite_score: 8.35,
      risk_level: "faible",
      primary_pattern: "Helsinki Declaration & GDPR-compliant ethical oversight",
      estimated_medical_experimentation_rights_index: 0.84,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/medical-experimentation-rights-engine`, {
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
