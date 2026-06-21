import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Economic Social Rights Engine Agent",
  domain: "economic_social_rights",
  total_entities: 8,
  avg_composite: 63.60,
  confidence_score: 0.87,
  avg_estimated_economic_social_rights_index: 6.36,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "ituc_global_rights_index_2023",
    "ilo_world_employment_social_outlook_2023",
    "un_sr_extreme_poverty_2023",
    "oxfam_inequality_report_2023",
  ],
  critical_alerts: [],
  entities: [
    {
      id: "ESR-001",
      name: "Corée du Nord — Zéro Liberté Syndicale, Travail Forcé d&apos;État Systématique, Pas de Sécurité Sociale &amp; Économie Captive Régime",
      country: "Corée du Nord",
      composite_score: 97.75,
      risk_level: "critique",
      estimated_economic_social_rights_index: 9.78,
      primary_pattern: "labour_rights_union_freedom_violation",
    },
    {
      id: "ESR-002",
      name: "Yémen — Infrastructures Sanitaires Détruites à 70%, 21M Sans Soins Adéquats, Famine &amp; Effondrement Total Sécurité Sociale",
      country: "Yémen",
      composite_score: 93.30,
      risk_level: "critique",
      estimated_economic_social_rights_index: 9.33,
      primary_pattern: "social_security_healthcare_collapse",
    },
    {
      id: "ESR-003",
      name: "Venezuela — Hyperinflation Destruction Sécurité Sociale, 7M Émigrés Fuient Pauvreté &amp; Services Publics Effondrés",
      country: "Venezuela",
      composite_score: 89.15,
      risk_level: "critique",
      estimated_economic_social_rights_index: 8.92,
      primary_pattern: "social_security_healthcare_collapse",
    },
    {
      id: "ESR-004",
      name: "Zimbabwe — Effondrement Services Publics, Droit Santé Violé, Chômage 90% &amp; Travailleurs Sans Filet Social Légal",
      country: "Zimbabwe",
      composite_score: 86.55,
      risk_level: "critique",
      estimated_economic_social_rights_index: 8.66,
      primary_pattern: "economic_inequality_extreme_poverty",
    },
    {
      id: "ESR-005",
      name: "Inde — Codes Labor 2020 Régressifs, 500M Travailleurs Informels Non-Protégés &amp; Syndicats Réprimés Hindutva",
      country: "Inde",
      composite_score: 55.85,
      risk_level: "élevé",
      estimated_economic_social_rights_index: 5.59,
      primary_pattern: "labour_rights_union_freedom_violation",
    },
    {
      id: "ESR-006",
      name: "Bangladesh — Grèves Garment Réprimées, 4M Ouvrières Textiles Sans Protection Adéquate &amp; Rana Plaza Impunité Persistante",
      country: "Bangladesh",
      composite_score: 53.85,
      risk_level: "élevé",
      estimated_economic_social_rights_index: 5.39,
      primary_pattern: "state_corporate_labour_impunity",
    },
    {
      id: "ESR-007",
      name: "Brésil — Réforme Retraite Lula Partielle, Inégalités Raciales Persistantes &amp; Précarisation Travailleurs Plateforme",
      country: "Brésil",
      composite_score: 27.80,
      risk_level: "modéré",
      estimated_economic_social_rights_index: 2.78,
      primary_pattern: "economic_inequality_extreme_poverty",
    },
    {
      id: "ESR-008",
      name: "Norvège — Modèle Nordique, Droits Sociaux Constitutionnels, Syndicats 70% Adhésion &amp; Protection Universelle",
      country: "Norvège",
      composite_score: 4.55,
      risk_level: "faible",
      estimated_economic_social_rights_index: 0.46,
      primary_pattern: "labour_rights_union_freedom_violation",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[economic-social-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/economic-social-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
