import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[ai-bias-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(
      sealResponse(getMockData(), "AI Bias Engine Agent"),
    );
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/ai-bias-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "AI Bias Engine Agent"));
  } catch {
    return NextResponse.json(
      sealResponse(getMockData(), "AI Bias Engine Agent"),
      { status: 502 },
    );
  }
}

function getMockData() {
  // Realistic mock matching Python summary() - 13 keys
  // Include all 8 entities in the `entities` array
  return {
    total_entities: 8,
    avg_composite: 44.36,
    risk_distribution: {
      critique: 3,
      élevé: 2,
      modéré: 1,
      faible: 2,
    },
    pattern_distribution: {
      biais_algorithmique: 3,
      biais_données: 0,
      impact_discriminatoire: 0,
      opacite_systematique: 0,
      equilibre_biais: 5,
    },
    top_risk_entities: ["AlgoDecide Corp", "HireAI Systems", "CreditBot Finance"],
    critical_alerts: [
      "ALERTE CRITIQUE — AlgoDecide Corp (États-Unis) : score composite 77.1/100, pattern 'biais_algorithmique' détecté",
      "ALERTE CRITIQUE — HireAI Systems (Royaume-Uni) : score composite 70.5/100, pattern 'biais_algorithmique' détecté",
      "ALERTE CRITIQUE — CreditBot Finance (Allemagne) : score composite 64.0/100, pattern 'biais_algorithmique' détecté",
    ],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "bias",
    confidence_score: 0.91,
    data_sources: ["audit_reports", "model_registries", "discrimination_complaints"],
    entities: [
      {
        entity_id: "ENT-001",
        name: "AlgoDecide Corp",
        country: "États-Unis",
        sector: "Justice & Juridique",
        composite_score: 77.1,
        algorithmic_score: 85.0,
        data_score: 80.0,
        impact_score: 72.0,
        transparency_score: 68.0,
        risk_level: "critique",
        primary_pattern: "biais_algorithmique",
        key_signals: [
          "Taux de faux positifs 3× plus élevé pour les minorités ethniques",
          "Absence de mécanisme d'appel algorithmique documenté",
          "Opacité totale sur les variables de prédiction de récidive",
        ],
        estimated_bias_index: 7.71,
        last_updated: "2026-06-20",
        model_count: 47,
      },
      {
        entity_id: "ENT-002",
        name: "HireAI Systems",
        country: "Royaume-Uni",
        sector: "Ressources Humaines",
        composite_score: 70.5,
        algorithmic_score: 75.0,
        data_score: 72.0,
        impact_score: 68.0,
        transparency_score: 65.0,
        risk_level: "critique",
        primary_pattern: "biais_algorithmique",
        key_signals: [
          "Sous-représentation féminine dans les profils sélectionnés (+40%)",
          "Données d'entraînement issues de 92% d'hommes blancs",
          "Aucun audit externe d'équité réalisé depuis 2023",
        ],
        estimated_bias_index: 7.05,
        last_updated: "2026-06-20",
        model_count: 23,
      },
      {
        entity_id: "ENT-003",
        name: "CreditBot Finance",
        country: "Allemagne",
        sector: "Services Financiers",
        composite_score: 64.0,
        algorithmic_score: 70.0,
        data_score: 66.0,
        impact_score: 62.0,
        transparency_score: 55.0,
        risk_level: "critique",
        primary_pattern: "biais_algorithmique",
        key_signals: [
          "Discrimination indirecte basée sur le code postal",
          "Score de crédit défavorable corrélé à l'origine nationale",
          "Absence d'explication individuelle des refus de prêt",
        ],
        estimated_bias_index: 6.4,
        last_updated: "2026-06-20",
        model_count: 89,
      },
      {
        entity_id: "ENT-004",
        name: "MedPredict AI",
        country: "France",
        sector: "Santé & Médical",
        composite_score: 53.6,
        algorithmic_score: 55.0,
        data_score: 58.0,
        impact_score: 52.0,
        transparency_score: 48.0,
        risk_level: "élevé",
        primary_pattern: "equilibre_biais",
        key_signals: [
          "Sous-représentation des femmes dans les essais cliniques sources",
          "Biais de confirmation dans les diagnostics assistés",
          "Données manquantes pour les populations âgées de plus de 75 ans",
        ],
        estimated_bias_index: 5.36,
        last_updated: "2026-06-20",
        model_count: 12,
      },
      {
        entity_id: "ENT-005",
        name: "PolicePredAI",
        country: "Pays-Bas",
        sector: "Sécurité Publique",
        composite_score: 45.9,
        algorithmic_score: 48.0,
        data_score: 50.0,
        impact_score: 44.0,
        transparency_score: 40.0,
        risk_level: "élevé",
        primary_pattern: "equilibre_biais",
        key_signals: [
          "Surpopulation de certains quartiers dans les données de surveillance",
          "Boucle de rétroaction amplifiant les biais historiques",
          "Validation limitée sur populations culturellement diversifiées",
        ],
        estimated_bias_index: 4.59,
        last_updated: "2026-06-20",
        model_count: 8,
      },
      {
        entity_id: "ENT-006",
        name: "AdTargetML",
        country: "Espagne",
        sector: "Marketing & Publicité",
        composite_score: 31.2,
        algorithmic_score: 35.0,
        data_score: 32.0,
        impact_score: 30.0,
        transparency_score: 26.0,
        risk_level: "modéré",
        primary_pattern: "equilibre_biais",
        key_signals: [
          "Ciblage différentiel selon genre pour offres d'emploi",
          "Exclusion partielle de segments démographiques vulnérables",
          "Profils comportementaux non audités pour équité",
        ],
        estimated_bias_index: 3.12,
        last_updated: "2026-06-20",
        model_count: 156,
      },
      {
        entity_id: "ENT-007",
        name: "FairLens Analytics",
        country: "Suède",
        sector: "Recherche & Développement",
        composite_score: 13.65,
        algorithmic_score: 15.0,
        data_score: 14.0,
        impact_score: 13.0,
        transparency_score: 12.0,
        risk_level: "faible",
        primary_pattern: "equilibre_biais",
        key_signals: [
          "Protocoles d'équité intégrés dans le cycle de développement",
          "Audits internes trimestriels d'équité algorithmique",
          "Publication transparente des métriques de biais",
        ],
        estimated_bias_index: 1.37,
        last_updated: "2026-06-20",
        model_count: 5,
      },
      {
        entity_id: "ENT-008",
        name: "EthicAI Solutions",
        country: "Canada",
        sector: "Conseil & Audit",
        composite_score: 8.65,
        algorithmic_score: 10.0,
        data_score: 9.0,
        impact_score: 8.0,
        transparency_score: 7.0,
        risk_level: "faible",
        primary_pattern: "equilibre_biais",
        key_signals: [
          "Certification ISO/IEC 42001 obtenue en 2025",
          "Comité d'éthique indépendant actif depuis la création",
          "Données d'entraînement diversifiées et documentées publiquement",
        ],
        estimated_bias_index: 0.87,
        last_updated: "2026-06-20",
        model_count: 3,
      },
    ],
    avg_estimated_bias_index: 4.44,
  };
}
