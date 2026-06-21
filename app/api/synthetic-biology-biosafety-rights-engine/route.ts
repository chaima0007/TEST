import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[synthetic-biology-biosafety-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "synthetic_biology_biosafety_rights_engine",
  domain: "synthetic_biology_biosafety_rights",
  total_entities: 8,
  avg_composite: 60.89,
  confidence_score: 0.88,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: {
    dual_use_pathogen_risk: 3,
    corporate_monopoly_biotech: 2,
    ecological_irreversibility: 2,
    governance_deficit: 1,
  },
  top_risk_entities: [
    { id: "SBB-002", name: "Chine — Laboratoires Biosécurité BSL-4, Opacité Recherche Synbio", score: 90.3, risk: "critique" },
    { id: "SBB-001", name: "États-Unis — GOF Research Non Régulé, Gain-of-Function Pathogènes Militaires", score: 90.0, risk: "critique" },
    { id: "SBB-003", name: "Russie — Programme Biopréparats Héritage, Synbio Militaire Non Déclaré", score: 85.35, risk: "critique" },
  ],
  critical_alerts: [
    "SBB-001: États-Unis — GOF Research Non Régulé, Gain-of-Function Pathogènes Militaires — composite 90.0",
    "SBB-002: Chine — Laboratoires Biosécurité BSL-4, Opacité Recherche Synbio — composite 90.3",
    "SBB-003: Russie — Programme Biopréparats Héritage, Synbio Militaire Non Déclaré — composite 85.35",
    "SBB-004: Monsanto/Bayer — Gene Drive OGM, Brevetage du Vivant Sans Consentement — composite 82.35",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_synthetic_biology_biosafety_index: 6.09,
  data_sources: [
    "who_biosafety_biosecurity_report_2024",
    "johns_hopkins_chs_biosecurity_2024",
    "convention_biological_diversity_synbio_2023",
    "nature_biotechnology_dual_use_governance_2024",
  ],
  entities: [
    {
      id: "SBB-001",
      name: "États-Unis — GOF Research Non Régulé, Gain-of-Function Pathogènes Militaires",
      country: "États-Unis",
      synthetic_pathogen_dual_use_risk_score: 95.0,
      corporate_biotech_monopoly_score: 90.0,
      ecological_release_irreversibility_score: 88.0,
      community_consent_biosafety_governance_score: 85.0,
      composite_score: 90.0,
      risk_level: "critique",
      primary_pattern: "Gain-of-function research H5N1 partiellement non supervisé, DARPA biotech dual-use sans transparence, CRISPR thérapeutique breveté sans accès global",
      estimated_synthetic_biology_biosafety_index: 9.0,
      last_updated: "2026-06-21",
    },
    {
      id: "SBB-002",
      name: "Chine — Laboratoires Biosécurité BSL-4, Opacité Recherche Synbio",
      country: "Chine",
      synthetic_pathogen_dual_use_risk_score: 93.0,
      corporate_biotech_monopoly_score: 85.0,
      ecological_release_irreversibility_score: 91.0,
      community_consent_biosafety_governance_score: 92.0,
      composite_score: 90.3,
      risk_level: "critique",
      primary_pattern: "WIV opacité recherche coronavirus synthétique, programme synbio militaire PLA, absence transparence BSL-4 Wuhan sur recherches dual-use",
      estimated_synthetic_biology_biosafety_index: 9.03,
      last_updated: "2026-06-21",
    },
    {
      id: "SBB-003",
      name: "Russie — Programme Biopréparats Héritage, Synbio Militaire Non Déclaré",
      country: "Russie",
      synthetic_pathogen_dual_use_risk_score: 90.0,
      corporate_biotech_monopoly_score: 78.0,
      ecological_release_irreversibility_score: 85.0,
      community_consent_biosafety_governance_score: 88.0,
      composite_score: 85.35,
      risk_level: "critique",
      primary_pattern: "Héritage Biopréparats non déclaré Traité ABW, Vector Institute souches rétablies sans supervision internationale, synbio dual-use militaire",
      estimated_synthetic_biology_biosafety_index: 8.54,
      last_updated: "2026-06-21",
    },
    {
      id: "SBB-004",
      name: "Monsanto/Bayer — Gene Drive OGM, Brevetage du Vivant Sans Consentement",
      country: "Multinationale",
      synthetic_pathogen_dual_use_risk_score: 72.0,
      corporate_biotech_monopoly_score: 95.0,
      ecological_release_irreversibility_score: 80.0,
      community_consent_biosafety_governance_score: 85.0,
      composite_score: 82.35,
      risk_level: "critique",
      primary_pattern: "Brevets CRISPR agriculture sans partage bénéfices communautés, gene drive moustiques Afrique sans consentement communautaire, monopole semencier synbio",
      estimated_synthetic_biology_biosafety_index: 8.24,
      last_updated: "2026-06-21",
    },
    {
      id: "SBB-005",
      name: "Inde — Bt Cotton Gene Drive, Impact Agriculteurs Sans Gouvernance",
      country: "Inde",
      synthetic_pathogen_dual_use_risk_score: 55.0,
      corporate_biotech_monopoly_score: 60.0,
      ecological_release_irreversibility_score: 58.0,
      community_consent_biosafety_governance_score: 52.0,
      composite_score: 56.4,
      risk_level: "élevé",
      primary_pattern: "OGM Bt Cotton dépendance Monsanto, suicides agriculteurs liés dettes semences, absence participation communautaire décisions biotech",
      estimated_synthetic_biology_biosafety_index: 5.64,
      last_updated: "2026-06-21",
    },
    {
      id: "SBB-006",
      name: "Brésil — Amazonie Gene Drive Insectes, Risques Écosystème",
      country: "Brésil",
      synthetic_pathogen_dual_use_risk_score: 48.0,
      corporate_biotech_monopoly_score: 55.0,
      ecological_release_irreversibility_score: 65.0,
      community_consent_biosafety_governance_score: 50.0,
      composite_score: 54.4,
      risk_level: "élevé",
      primary_pattern: "Oxitec moustiques modifiés lâchés sans pleine consultation autochtones Amazonie, risques irréversibles biodiversité tropicale, gouvernance lacunaire",
      estimated_synthetic_biology_biosafety_index: 5.44,
      last_updated: "2026-06-21",
    },
    {
      id: "SBB-007",
      name: "UE — Directive OGM Révisée, Cadre NTG Nouvelles Techniques Génomiques",
      country: "Union Européenne",
      synthetic_pathogen_dual_use_risk_score: 25.0,
      corporate_biotech_monopoly_score: 28.0,
      ecological_release_irreversibility_score: 22.0,
      community_consent_biosafety_governance_score: 20.0,
      composite_score: 24.0,
      risk_level: "modéré",
      primary_pattern: "Règlement NTG 2024 avec évaluation risques, protocole Cartagena adopté, débat public OGM institutionnalisé, moratorium gene drive maintenu",
      estimated_synthetic_biology_biosafety_index: 2.4,
      last_updated: "2026-06-21",
    },
    {
      id: "SBB-008",
      name: "Nouvelle-Zélande — Loi Hazardous Substances, Précaution Synbio Exemplaire",
      country: "Nouvelle-Zélande",
      synthetic_pathogen_dual_use_risk_score: 5.0,
      corporate_biotech_monopoly_score: 5.0,
      ecological_release_irreversibility_score: 4.0,
      community_consent_biosafety_governance_score: 3.0,
      composite_score: 4.35,
      risk_level: "faible",
      primary_pattern: "HSNO Act strict sur organismes modifiés, consultation iwi Maori obligatoire synbio, ERMA évaluation indépendante, modèle précaution biosécurité mondiale",
      estimated_synthetic_biology_biosafety_index: 0.44,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/synthetic-biology-biosafety-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data.payload ?? data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }));
  }
}
