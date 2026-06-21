import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[digital-divide-access-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Digital Divide Access Rights Engine Agent",
  domain: "digital_divide_access_rights",
  total_entities: 8,
  avg_composite: 61.21,
  confidence_score: 0.83,
  risk_distribution: { "critique": 4, "élevé": 2, "modéré": 1, "faible": 1 },
  pattern_distribution: { "internet_access_exclusion_infrastructure_severity": 3, "platform_language_content_inclusion_deficit_gap": 1, "affordability_economic_digital_barrier_scale": 3, "digital_literacy_skills_gap": 1 },
  top_risk_entities: ["Afrique Sub-Saharienne — 28% Connexion Internet, Coût 1 Go = 20% Salaire, Électricité 40% Rurale & Femmes 25% Moins Connectées", "Myanmar/Rural Asie — Coupures Internet Post-Coup, 50% Population Non-Connectée, Zones Rurales 3G Absente & Contenu Langue Maternelle 0%", "Inde/Rurale — 800M Sans Internet Régulier, 5G Urbain vs 2G Rural, Femmes 67% Moins Accès & Hindi 90% Contenu Langue"],
  critical_alerts: ["Afrique Sub-Saharienne: internet_access_exclusion_infrastructure_severity", "Myanmar/Rural Asie: internet_access_exclusion_infrastructure_severity", "Inde/Rurale: platform_language_content_inclusion_deficit_gap", "USA/Zones Rurales: affordability_economic_digital_barrier_scale"],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_digital_divide_access_rights_index: 6.12,
  data_sources: ["itu_digital_development_report", "a4ai_affordability_report", "un_broadband_commission_report"],
  entities: [
    {
,      entity_id: "DDA-001"
      name: "Afrique Sub-Saharienne — 28% Connexion Internet, Coût 1 Go = 20% Salaire, Électricité 40% Rurale & Femmes 25% Moins Connectées"
      country: "Afrique"
      internet_access_exclusion_infrastructure_severity_score: 94.0
      affordability_economic_digital_barrier_scale_score: 92.0
      digital_literacy_skills_gap_score: 93.0
      platform_language_content_inclusion_deficit_gap_score: 91.0
      composite_score: 92.65
      risk_level: "critique"
      primary_pattern: "internet_access_exclusion_infrastructure_severity"
      estimated_digital_divide_access_rights_index: 9.27
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "DDA-002"
      name: "Myanmar/Rural Asie — Coupures Internet Post-Coup, 50% Population Non-Connectée, Zones Rurales 3G Absente & Contenu Langue Maternelle 0%"
      country: "Myanmar"
      internet_access_exclusion_infrastructure_severity_score: 90.0
      affordability_economic_digital_barrier_scale_score: 89.0
      digital_literacy_skills_gap_score: 88.0
      platform_language_content_inclusion_deficit_gap_score: 91.0
      composite_score: 89.45
      risk_level: "critique"
      primary_pattern: "internet_access_exclusion_infrastructure_severity"
      estimated_digital_divide_access_rights_index: 8.95
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "DDA-003"
      name: "Inde/Rurale — 800M Sans Internet Régulier, 5G Urbain vs 2G Rural, Femmes 67% Moins Accès & Hindi 90% Contenu Langue"
      country: "Inde"
      internet_access_exclusion_infrastructure_severity_score: 87.0
      affordability_economic_digital_barrier_scale_score: 85.0
      digital_literacy_skills_gap_score: 88.0
      platform_language_content_inclusion_deficit_gap_score: 86.0
      composite_score: 86.55
      risk_level: "critique"
      primary_pattern: "platform_language_content_inclusion_deficit_gap"
      estimated_digital_divide_access_rights_index: 8.65
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "DDA-004"
      name: "USA/Zones Rurales — 21M Américains Sans Haut Débit, FCC Data Inexacte, Bibliothèques Seul Accès & Fracture Raciale Digitale Persistante"
      country: "USA"
      internet_access_exclusion_infrastructure_severity_score: 83.0
      affordability_economic_digital_barrier_scale_score: 82.0
      digital_literacy_skills_gap_score: 84.0
      platform_language_content_inclusion_deficit_gap_score: 81.0
      composite_score: 82.6
      risk_level: "critique"
      primary_pattern: "affordability_economic_digital_barrier_scale"
      estimated_digital_divide_access_rights_index: 8.26
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "DDA-005"
      name: "Europe/DESI — 13% UE Sans Compétences Numériques Basiques, Personnes Âgées 60%+ Exclusion, PME Lag Numérique & Inégalités Régions"
      country: "Europe"
      internet_access_exclusion_infrastructure_severity_score: 56.0
      affordability_economic_digital_barrier_scale_score: 54.0
      digital_literacy_skills_gap_score: 55.0
      platform_language_content_inclusion_deficit_gap_score: 57.0
      composite_score: 55.45
      risk_level: "élevé"
      primary_pattern: "digital_literacy_skills_gap"
      estimated_digital_divide_access_rights_index: 5.54
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "DDA-006"
      name: "Brésil/Favelas — 40% Sans Internet Fixe, Mobile Only Limitation, Contenu Portugais Dominant & Éducation Distance Inégale COVID"
      country: "Brésil"
      internet_access_exclusion_infrastructure_severity_score: 52.0
      affordability_economic_digital_barrier_scale_score: 51.0
      digital_literacy_skills_gap_score: 54.0
      platform_language_content_inclusion_deficit_gap_score: 53.0
      composite_score: 52.45
      risk_level: "élevé"
      primary_pattern: "affordability_economic_digital_barrier_scale"
      estimated_digital_divide_access_rights_index: 5.25
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "DDA-007"
      name: "ITU/A4AI — Union Internationale Télécommunications, Alliance Affordable Internet, Web Foundation & Digital Rights Charter"
      country: "Global"
      internet_access_exclusion_infrastructure_severity_score: 27.0
      affordability_economic_digital_barrier_scale_score: 25.0
      digital_literacy_skills_gap_score: 28.0
      platform_language_content_inclusion_deficit_gap_score: 26.0
      composite_score: 26.55
      risk_level: "modéré"
      primary_pattern: "affordability_economic_digital_barrier_scale"
      estimated_digital_divide_access_rights_index: 2.66
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "DDA-008"
      name: "ONU/SDG9c — SDG 9.c Connectivité Universelle 2030, Déclaration WSIS, Droit Internet Résolution ONU & ITU Connect 2030"
      country: "Global"
      internet_access_exclusion_infrastructure_severity_score: 4.0
      affordability_economic_digital_barrier_scale_score: 4.0
      digital_literacy_skills_gap_score: 4.0
      platform_language_content_inclusion_deficit_gap_score: 4.0
      composite_score: 4.0
      risk_level: "faible"
      primary_pattern: "internet_access_exclusion_infrastructure_severity"
      estimated_digital_divide_access_rights_index: 0.4
      last_updated: "2026-06-21"
    }
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/digital-divide-access-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
