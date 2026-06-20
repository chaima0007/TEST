import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[cognitive-enhancement-engine] SWARM_API_URL non défini — mode mock activé");
}

// ── Pre-computed mock entity data ─────────────────────────────────────────────
// 8 entities: 3 critique, 2 élevé, 1 modéré, 2 faible
// composite_score = neuro_risk_score*0.30 + ethical_concern_score*0.25
//                 + regulatory_gap_score*0.25 + social_inequality_score*0.20
// estimated_cognitive_index = round(composite_score / 100 * 10, 2)
// pattern_severity: from PATTERNS lookup

const MOCK_ENTITIES = [
  // COG-001 — critique — Interface Neurale Non Régulée
  // 88*0.30 + 82*0.25 + 85*0.25 + 78*0.20 = 26.4+20.5+21.25+15.6 = 83.75
  {
    entity_id: "COG-001",
    name: "NeuraTech Dynamics",
    country: "USA",
    sector: "Biotechnologie",
    composite_score: 83.75,
    neuro_risk_score: 88.0,
    ethical_concern_score: 82.0,
    regulatory_gap_score: 85.0,
    social_inequality_score: 78.0,
    risk_level: "critique",
    primary_pattern: "Interface Neurale Non Régulée",
    key_signals: [
      "BCI implantée sans approbation FDA",
      "Modification génétique neuronale",
      "Accès limité au 0.1% populace",
    ],
    estimated_cognitive_index: 8.38,
    last_updated: "2026-06-20",
    pattern_severity: "critique",
  },
  // COG-002 — critique — Convergence BCI-IA Incontrôlée
  // 82*0.30 + 78*0.25 + 80*0.25 + 72*0.20 = 24.6+19.5+20.0+14.4 = 78.5
  {
    entity_id: "COG-002",
    name: "CognAI Solutions",
    country: "Chine",
    sector: "Intelligence Artificielle",
    composite_score: 78.5,
    neuro_risk_score: 82.0,
    ethical_concern_score: 78.0,
    regulatory_gap_score: 80.0,
    social_inequality_score: 72.0,
    risk_level: "critique",
    primary_pattern: "Convergence BCI-IA Incontrôlée",
    key_signals: [
      "IA intégrée directement dans cortex",
      "Surveillance cognitive population",
      "Brevet monopolistique BCI-IA",
    ],
    estimated_cognitive_index: 7.85,
    last_updated: "2026-06-20",
    pattern_severity: "modéré",
  },
  // COG-003 — critique — Vide Réglementaire Nootropique
  // 75*0.30 + 80*0.25 + 78*0.25 + 65*0.20 = 22.5+20.0+19.5+13.0 = 75.0
  {
    entity_id: "COG-003",
    name: "PharmaCog Industries",
    country: "Suisse",
    sector: "Pharmaceutique",
    composite_score: 75.0,
    neuro_risk_score: 75.0,
    ethical_concern_score: 80.0,
    regulatory_gap_score: 78.0,
    social_inequality_score: 65.0,
    risk_level: "critique",
    primary_pattern: "Vide Réglementaire Nootropique",
    key_signals: [
      "Distribution nootropiques non homologués",
      "Essais cliniques lacunaires",
      "Marché noir cognitif émergent",
    ],
    estimated_cognitive_index: 7.5,
    last_updated: "2026-06-20",
    pattern_severity: "élevé",
  },
  // COG-004 — élevé — Augmentation Cognitive Inégalitaire
  // 59*0.30 + 55*0.25 + 58*0.25 + 70*0.20 = 17.7+13.75+14.5+14.0 = 59.95
  {
    entity_id: "COG-004",
    name: "AugMind Corp",
    country: "Royaume-Uni",
    sector: "Neurotechnologie",
    composite_score: 59.95,
    neuro_risk_score: 59.0,
    ethical_concern_score: 55.0,
    regulatory_gap_score: 58.0,
    social_inequality_score: 70.0,
    risk_level: "élevé",
    primary_pattern: "Augmentation Cognitive Inégalitaire",
    key_signals: [
      "Tarification prohibitive BCI",
      "Exclusion démographique validée",
      "Lobbying anti-régulation actif",
    ],
    estimated_cognitive_index: 6.0,
    last_updated: "2026-06-20",
    pattern_severity: "élevé",
  },
  // COG-005 — élevé — Dépendance Cognitive Induite
  // 55*0.30 + 62*0.25 + 50*0.25 + 58*0.20 = 16.5+15.5+12.5+11.6 = 56.1
  {
    entity_id: "COG-005",
    name: "MindBoost Laboratories",
    country: "Allemagne",
    sector: "Recherche Médicale",
    composite_score: 56.1,
    neuro_risk_score: 55.0,
    ethical_concern_score: 62.0,
    regulatory_gap_score: 50.0,
    social_inequality_score: 58.0,
    risk_level: "élevé",
    primary_pattern: "Dépendance Cognitive Induite",
    key_signals: [
      "Taux dépendance nootropique 35%",
      "Effets long-terme non étudiés",
      "Pression performance professionnelle",
    ],
    estimated_cognitive_index: 5.61,
    last_updated: "2026-06-20",
    pattern_severity: "modéré",
  },
  // COG-006 — modéré — Dépendance Cognitive Induite
  // 40*0.30 + 38*0.25 + 35*0.25 + 42*0.20 = 12.0+9.5+8.75+8.4 = 38.65
  {
    entity_id: "COG-006",
    name: "BrainWave Institut",
    country: "France",
    sector: "Neurosciences",
    composite_score: 38.65,
    neuro_risk_score: 40.0,
    ethical_concern_score: 38.0,
    regulatory_gap_score: 35.0,
    social_inequality_score: 42.0,
    risk_level: "modéré",
    primary_pattern: "Dépendance Cognitive Induite",
    key_signals: [
      "Usage modéré neurostimulation",
      "Protocole éthique partiel",
      "Accès progressif recherche",
    ],
    estimated_cognitive_index: 3.87,
    last_updated: "2026-06-20",
    pattern_severity: "modéré",
  },
  // COG-007 — faible — Interface Neurale Non Régulée
  // 12*0.30 + 10*0.25 + 15*0.25 + 18*0.20 = 3.6+2.5+3.75+3.6 = 13.45
  {
    entity_id: "COG-007",
    name: "NeurEthics Foundation",
    country: "Canada",
    sector: "Éthique & Recherche",
    composite_score: 13.45,
    neuro_risk_score: 12.0,
    ethical_concern_score: 10.0,
    regulatory_gap_score: 15.0,
    social_inequality_score: 18.0,
    risk_level: "faible",
    primary_pattern: "Interface Neurale Non Régulée",
    key_signals: [
      "Cadre éthique robuste",
      "Accès universel promu",
      "Transparence totale",
    ],
    estimated_cognitive_index: 1.35,
    last_updated: "2026-06-20",
    pattern_severity: "critique",
  },
  // COG-008 — faible — Vide Réglementaire Nootropique
  // 8*0.30 + 12*0.25 + 10*0.25 + 15*0.20 = 2.4+3.0+2.5+3.0 = 10.9
  {
    entity_id: "COG-008",
    name: "CogSafe Initiative",
    country: "Suède",
    sector: "Santé Publique",
    composite_score: 10.9,
    neuro_risk_score: 8.0,
    ethical_concern_score: 12.0,
    regulatory_gap_score: 10.0,
    social_inequality_score: 15.0,
    risk_level: "faible",
    primary_pattern: "Vide Réglementaire Nootropique",
    key_signals: [
      "Régulation proactive exemplaire",
      "Essais cliniques rigoureux",
      "Distribution équitable garantie",
    ],
    estimated_cognitive_index: 1.09,
    last_updated: "2026-06-20",
    pattern_severity: "élevé",
  },
];

function getMockData() {
  const entities = MOCK_ENTITIES;
  const n = entities.length;
  const avgComposite =
    Math.round((entities.reduce((s, e) => s + e.composite_score, 0) / n) * 100) / 100;

  const riskDistribution: Record<string, number> = {
    critique: 0,
    élevé: 0,
    modéré: 0,
    faible: 0,
  };
  const patternDistribution: Record<string, number> = {};

  for (const e of entities) {
    riskDistribution[e.risk_level] = (riskDistribution[e.risk_level] || 0) + 1;
    patternDistribution[e.primary_pattern] =
      (patternDistribution[e.primary_pattern] || 0) + 1;
  }

  const sorted = [...entities].sort((a, b) => b.composite_score - a.composite_score);
  const topRiskEntities = sorted.slice(0, 3).map((e) => e.name);
  const avgEstimatedCognitiveIndex =
    Math.round((avgComposite / 100) * 10 * 100) / 100;

  const summary = {
    total_entities: n,
    avg_composite: avgComposite,
    risk_distribution: riskDistribution,
    pattern_distribution: patternDistribution,
    top_risk_entities: topRiskEntities,
    critical_alerts: riskDistribution["critique"] || 0,
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "cognitive",
    confidence_score: 0.87,
    data_sources: [
      "WHO Neuroethics Reports",
      "FDA Brain-Computer Interface Registry",
      "EMA Nootropics Surveillance",
      "IEEE Brain Initiative Database",
      "Nature Neuroscience Publications",
    ],
    entities,
    avg_estimated_cognitive_index: avgEstimatedCognitiveIndex,
  };

  return { entities, summary };
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Cognitive Enhancement Agent"));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/cognitive-enhancement-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Cognitive Enhancement Agent"));
  } catch {
    return NextResponse.json(
      sealResponse(getMockData(), "Cognitive Enhancement Agent"),
      { status: 502 }
    );
  }
}
