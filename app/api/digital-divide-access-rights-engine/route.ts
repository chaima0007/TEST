import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[digital-divide-access-rights-engine] SWARM_API_URL is not set — using mock data");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_ENTITIES = [
  {
    id: "DDA-001",
    name: "Afrique Sub-Saharienne — 28% Connexion Internet, Coût 1 Go = 20% Salaire, Électricité 40% Rurale & Femmes 25% Moins Connectées",
    country: "Afrique",
    sector: "Exclusion Numérique Infrastructure",
    internet_access_exclusion_infrastructure_severity_score: 94.0,
    affordability_economic_digital_barrier_scale_score: 92.0,
    digital_literacy_skills_gap_score: 93.0,
    platform_language_content_inclusion_deficit_gap_score: 91.0,
    primary_pattern: "internet_access_exclusion_infrastructure_severity",
  },
  {
    id: "DDA-002",
    name: "Myanmar/Rural Asie — Coupures Internet Post-Coup, 50% Population Non-Connectée, Zones Rurales 3G Absente & Contenu Langue Maternelle 0%",
    country: "Myanmar",
    sector: "Coupures Internet Autoritaires",
    internet_access_exclusion_infrastructure_severity_score: 90.0,
    affordability_economic_digital_barrier_scale_score: 89.0,
    digital_literacy_skills_gap_score: 88.0,
    platform_language_content_inclusion_deficit_gap_score: 91.0,
    primary_pattern: "internet_access_exclusion_infrastructure_severity",
  },
  {
    id: "DDA-003",
    name: "Inde/Rurale — 800M Sans Internet Régulier, 5G Urbain vs 2G Rural, Femmes 67% Moins Accès & Hindi 90% Contenu Langue",
    country: "Inde",
    sector: "Fracture Rurale-Urbaine Linguistique",
    internet_access_exclusion_infrastructure_severity_score: 87.0,
    affordability_economic_digital_barrier_scale_score: 85.0,
    digital_literacy_skills_gap_score: 88.0,
    platform_language_content_inclusion_deficit_gap_score: 86.0,
    primary_pattern: "platform_language_content_inclusion_deficit_gap",
  },
  {
    id: "DDA-004",
    name: "USA/Zones Rurales — 21M Américains Sans Haut Débit, FCC Data Inexacte, Bibliothèques Seul Accès & Fracture Raciale Digitale Persistante",
    country: "USA",
    sector: "Fracture Numérique Rurale Pays Développé",
    internet_access_exclusion_infrastructure_severity_score: 83.0,
    affordability_economic_digital_barrier_scale_score: 82.0,
    digital_literacy_skills_gap_score: 84.0,
    platform_language_content_inclusion_deficit_gap_score: 81.0,
    primary_pattern: "affordability_economic_digital_barrier_scale",
  },
  {
    id: "DDA-005",
    name: "Europe/DESI — 13% UE Sans Compétences Numériques Basiques, Personnes Âgées 60%+ Exclusion, PME Lag Numérique & Inégalités Régions",
    country: "Europe",
    sector: "Compétences Numériques Inclusion Sociale",
    internet_access_exclusion_infrastructure_severity_score: 56.0,
    affordability_economic_digital_barrier_scale_score: 54.0,
    digital_literacy_skills_gap_score: 55.0,
    platform_language_content_inclusion_deficit_gap_score: 57.0,
    primary_pattern: "digital_literacy_skills_gap",
  },
  {
    id: "DDA-006",
    name: "Brésil/Favelas — 40% Sans Internet Fixe, Mobile Only Limitation, Contenu Portugais Dominant & Éducation Distance Inégale COVID",
    country: "Brésil",
    sector: "Fracture Mobile-Fixe Inégalités Urbaines",
    internet_access_exclusion_infrastructure_severity_score: 52.0,
    affordability_economic_digital_barrier_scale_score: 51.0,
    digital_literacy_skills_gap_score: 54.0,
    platform_language_content_inclusion_deficit_gap_score: 53.0,
    primary_pattern: "affordability_economic_digital_barrier_scale",
  },
  {
    id: "DDA-007",
    name: "ITU/A4AI — Union Internationale Télécommunications, Alliance Affordable Internet, Web Foundation & Digital Rights Charter",
    country: "Global",
    sector: "Plaidoyer Droits Numériques",
    internet_access_exclusion_infrastructure_severity_score: 27.0,
    affordability_economic_digital_barrier_scale_score: 25.0,
    digital_literacy_skills_gap_score: 28.0,
    platform_language_content_inclusion_deficit_gap_score: 26.0,
    primary_pattern: "affordability_economic_digital_barrier_scale",
  },
  {
    id: "DDA-008",
    name: "ONU/SDG9c — SDG 9.c Connectivité Universelle 2030, Déclaration WSIS, Droit Internet Résolution ONU & ITU Connect 2030",
    country: "Global",
    sector: "Cadre Normatif Connectivité Universelle",
    internet_access_exclusion_infrastructure_severity_score: 4.0,
    affordability_economic_digital_barrier_scale_score: 4.0,
    digital_literacy_skills_gap_score: 4.0,
    platform_language_content_inclusion_deficit_gap_score: 4.0,
    primary_pattern: "internet_access_exclusion_infrastructure_severity",
  },
];

type DDAInput = (typeof MOCK_ENTITIES)[0];

function computeComposite(e: DDAInput): number {
  return Math.round(
    (e.internet_access_exclusion_infrastructure_severity_score * 0.30
    + e.affordability_economic_digital_barrier_scale_score * 0.25
    + e.digital_literacy_skills_gap_score * 0.25
    + e.platform_language_content_inclusion_deficit_gap_score * 0.20) * 100
  ) / 100;
}

function riskLevel(composite: number): string {
  if (composite >= 60) return "critique";
  if (composite >= 40) return "élevé";
  if (composite >= 20) return "modéré";
  return "faible";
}

function severity(composite: number): string {
  if (composite >= 60) return "crise_exclusion_numérique_systémique";
  if (composite >= 40) return "crise_barrières_économiques_numériques_majeure";
  if (composite >= 20) return "risque_fossé_compétences_numériques_structurel";
  return "surveillance_objectifs_connectivité_universelle";
}

function recommendedAction(risk: string): string {
  if (risk === "critique") return "intervention_urgente_infrastructure_accès_universel";
  if (risk === "élevé") return "réduction_coûts_internet_abordable_prioritaire";
  if (risk === "modéré") return "programmes_formation_numérique_inclusion";
  return "veille_sdg9c_connectivité_universelle_continue";
}

function signal(risk: string): string {
  if (risk === "critique") return "CRITIQUE — Crise exclusion numérique systémique — droits fondamentaux niés";
  if (risk === "élevé") return "ÉLEVÉ — Crise barrières économiques numériques majeure détectée";
  if (risk === "modéré") return "MODÉRÉ — Risque fossé compétences numériques structurel actif";
  return "FAIBLE — Surveillance objectifs connectivité universelle continue";
}

function estimatedIndex(composite: number): number {
  return Math.round(composite / 100 * 10 * 100) / 100;
}

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map((e) => {
      const composite = computeComposite(e);
      const risk = riskLevel(composite);
      return {
        id: e.entity_id,
        name: e.name,
        country: e.country,
        sector: e.sector,
        internet_access_exclusion_infrastructure_severity_score: e.internet_access_exclusion_infrastructure_severity_score,
        affordability_economic_digital_barrier_scale_score: e.affordability_economic_digital_barrier_scale_score,
        digital_literacy_skills_gap_score: e.digital_literacy_skills_gap_score,
        platform_language_content_inclusion_deficit_gap_score: e.platform_language_content_inclusion_deficit_gap_score,
        composite_score: composite,
        risk_level: risk,
        primary_pattern: e.primary_pattern,
        severity: severity(composite),
        recommended_action: recommendedAction(risk),
        signal: signal(risk),
        estimated_digital_divide_access_rights_index: estimatedIndex(composite),
        last_updated: "2026-06-21",
      };
    });

    const risk_distribution: Record<string, number> = {};
    const pattern_distribution: Record<string, number> = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number> = {};
    let totalComposite = 0;
    let critiqueCount = 0, élevéCount = 0, modéréCount = 0, faibleCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level] = (risk_distribution[ent.risk_level] || 0) + 1;
      pattern_distribution[ent.primary_pattern] = (pattern_distribution[ent.primary_pattern] || 0) + 1;
      severity_distribution[ent.severity] = (severity_distribution[ent.severity] || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      totalComposite += ent.composite_score;
      if (ent.risk_level === "critique") critiqueCount++;
      else if (ent.risk_level === "élevé") élevéCount++;
      else if (ent.risk_level === "modéré") modéréCount++;
      else faibleCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(totalComposite / n * 100) / 100;

    const summary = {
      module_id: 983,
      module_name: "Digital Divide Access Rights Intelligence Engine",
      agent: "Digital Divide Access Rights Engine Agent",
      domain: "digital_divide_access_rights",
      total: n,
      critique: critiqueCount,
      élevé: élevéCount,
      modéré: modéréCount,
      faible: faibleCount,
      avg_composite: avgComposite,
      avg_estimated_digital_divide_access_rights_index: estimatedIndex(avgComposite),
      risk_distribution,
      pattern_distribution,
      severity_distribution,
      action_distribution,
      confidence_score: 0.83,
      data_sources: [
        "itu_measuring_digital_development_report",
        "a4ai_affordability_report",
        "web_foundation_digital_rights_report",
      ],
      last_analysis: "2026-06-21",
      engine_version: "1.0.0",
    };

    return sealResponse(NextResponse.json(
      sealResponse({ entities, summary } as Record<string, unknown>)
    ));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/digital-divide-access-rights-engine`);
    const res = await fetch(url.toString(), { next: { revalidate: 30 } });
    if (res.ok) return sealResponse(NextResponse.json(sealResponse(await res.json())));
  } catch {}
  return sealResponse(NextResponse.json(
    sealResponse({ entities: [], summary: {} } as Record<string, unknown>),
    { status: 502 }
  ));
}
