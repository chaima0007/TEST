import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[longevity-inequality-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Longevity Inequality Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/longevity-inequality-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Longevity Inequality Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Longevity Inequality Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "LI-001", name: "États-Unis — Santé Privatisée", country: "Amérique du Nord", sector: "Inégalité Sanitaire Maximale", composite_score: 87.0, lifespan_gap_score: 88.0, health_access_inequality_score: 90.0, longevity_tech_exclusion_score: 85.0, demographic_bifurcation_score: 82.0, risk_level: "critique", primary_pattern: "exclusion_longevite", key_signals: ["Bifurcation mortelle critique aux États-Unis — classes biologiques émergentes par accès aux soins", "Écarts d'espérance de vie de 20+ ans entre groupes socio-économiques", "Technologies de longévité réservées aux ultra-riches — inégalité biologique institutionnalisée"], estimated_longevity_fracture_index: 8.70, last_updated: "2026-06-20" },
    { id: "LI-002", name: "Afrique Subsaharienne — Accès Zéro", country: "Afrique", sector: "Exclusion Totale Soins & Longévité", composite_score: 89.0, lifespan_gap_score: 92.0, health_access_inequality_score: 88.0, longevity_tech_exclusion_score: 95.0, demographic_bifurcation_score: 80.0, risk_level: "critique", primary_pattern: "bifurcation_mortelle", key_signals: ["Bifurcation mortelle critique en Afrique Subsaharienne — classes biologiques émergentes par accès aux soins", "Écarts d'espérance de vie de 20+ ans entre groupes socio-économiques", "Technologies de longévité réservées aux ultra-riches — inégalité biologique institutionnalisée"], estimated_longevity_fracture_index: 8.90, last_updated: "2026-06-20" },
    { id: "LI-003", name: "Chine — Dualisme Urbain/Rural", country: "Asie", sector: "Fracture Sanitaire Géographique", composite_score: 77.5, lifespan_gap_score: 78.0, health_access_inequality_score: 82.0, longevity_tech_exclusion_score: 75.0, demographic_bifurcation_score: 72.0, risk_level: "critique", primary_pattern: "exclusion_longevite", key_signals: ["Bifurcation mortelle critique en Chine — classes biologiques émergentes par accès aux soins", "Écarts d'espérance de vie de 20+ ans entre groupes socio-économiques", "Technologies de longévité réservées aux ultra-riches — inégalité biologique institutionnalisée"], estimated_longevity_fracture_index: 7.75, last_updated: "2026-06-20" },
    { id: "LI-004", name: "Inde — Inégalité Sanitaire Extrême", country: "Asie du Sud", sector: "Castes & Accès aux Soins", composite_score: 79.0, lifespan_gap_score: 82.0, health_access_inequality_score: 85.0, longevity_tech_exclusion_score: 78.0, demographic_bifurcation_score: 70.0, risk_level: "critique", primary_pattern: "exclusion_longevite", key_signals: ["Bifurcation mortelle critique en Inde — classes biologiques émergentes par accès aux soins", "Écarts d'espérance de vie de 20+ ans entre groupes socio-économiques", "Technologies de longévité réservées aux ultra-riches — inégalité biologique institutionnalisée"], estimated_longevity_fracture_index: 7.90, last_updated: "2026-06-20" },
    { id: "LI-005", name: "Brésil — Fracture Raciale & Sanitaire", country: "Amériques", sector: "Inégalités Structurelles de Longévité", composite_score: 67.25, lifespan_gap_score: 68.0, health_access_inequality_score: 72.0, longevity_tech_exclusion_score: 65.0, demographic_bifurcation_score: 62.0, risk_level: "critique", primary_pattern: "fracture_sante_profonde", key_signals: ["Exclusion de longévité avancée au Brésil — accès inégal aux soins et thérapies", "Fracture sanitaire profonde entre classes sociales — mortalité prématurée évitable", "Accumulation d'inégalités biologiques compromettant la cohésion sociale"], estimated_longevity_fracture_index: 6.73, last_updated: "2026-06-20" },
    { id: "LI-006", name: "Europe Centrale & Orientale", country: "Europe", sector: "Fracture Est/Ouest de Longévité", composite_score: 44.0, lifespan_gap_score: 45.0, health_access_inequality_score: 48.0, longevity_tech_exclusion_score: 42.0, demographic_bifurcation_score: 40.0, risk_level: "élevé", primary_pattern: "fracture_sante_profonde", key_signals: ["Exclusion de longévité avancée en Europe Centrale & Orientale — accès inégal aux soins et thérapies", "Fracture sanitaire profonde entre classes sociales — mortalité prématurée évitable", "Accumulation d'inégalités biologiques compromettant la cohésion sociale"], estimated_longevity_fracture_index: 4.40, last_updated: "2026-06-20" },
    { id: "LI-007", name: "Europe Occidentale — Accès Partiel", country: "Europe", sector: "Systèmes Universels Sous Pression", composite_score: 24.5, lifespan_gap_score: 25.0, health_access_inequality_score: 28.0, longevity_tech_exclusion_score: 22.0, demographic_bifurcation_score: 20.0, risk_level: "modéré", primary_pattern: "disparite_croissante", key_signals: ["Disparités de longévité croissantes en Europe Occidentale — signaux précoces à surveiller", "Accès aux soins préventifs inégalement réparti — risque de bifurcation future", "Régulation des bio-inégalités émergentes nécessaire"], estimated_longevity_fracture_index: 2.45, last_updated: "2026-06-20" },
    { id: "LI-008", name: "Nordiques & Japon — Modèle Équité", country: "Europe du Nord/Asie", sector: "Longévité Équitable Exemplaire", composite_score: 7.75, lifespan_gap_score: 8.0, health_access_inequality_score: 10.0, longevity_tech_exclusion_score: 6.0, demographic_bifurcation_score: 5.0, risk_level: "faible", primary_pattern: "acces_equitable", key_signals: ["Nordiques & Japon — Modèle Équité maintient un accès équitable à la longévité — système de santé universel opérationnel", "Écarts d'espérance de vie limités et tendances à la convergence", "Modèle d'équité sanitaire à préserver et à exporter"], estimated_longevity_fracture_index: 0.78, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 5, "élevé": 1, "modéré": 1, faible: 1 },
    pattern_distribution: { bifurcation_mortelle: 1, exclusion_longevite: 3, fracture_sante_profonde: 2, disparite_croissante: 1, acces_equitable: 1 },
    top_risk_entities: ["Afrique Subsaharienne — Accès Zéro", "États-Unis — Santé Privatisée", "Inde — Inégalité Sanitaire Extrême"],
    critical_alerts: ["Afrique: bifurcation mortelle", "États-Unis: exclusion longévité", "Inde: exclusion longévité", "Chine: exclusion longévité", "Brésil: fracture santé profonde"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "longevity_ineq",
    confidence_score: 0.80,
    data_sources: ["who_lifespan_data", "health_inequality_tracker", "longevity_tech_access_monitor"],
    entities,
    avg_estimated_longevity_fracture_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
