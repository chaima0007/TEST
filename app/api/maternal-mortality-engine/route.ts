import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[maternal-mortality-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Maternal Mortality Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/maternal-mortality-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Maternal Mortality Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Maternal Mortality Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "MM-001", name: "Sierra Leone — Mortalité Maternelle Record", country: "Afrique de l'Ouest", sector: "1er Taux Mondial — 443 Décès/100k Naissances Vivantes", composite_score: 86.15, healthcare_system_collapse_score: 92.0, gender_inequality_score: 88.0, obstetric_access_deficit_score: 90.0, conflict_health_impact_score: 78.0, risk_level: "critique", primary_pattern: "crise_humanitaire_maternelle", key_signals: ["Crise de mortalité maternelle en Sierra Leone — décès obstétriques évitables massifs révélant une faillite de l'État", "Inégalité de genre systémique — femmes exclues de l'accès aux soins obstétriques de base", "Système de santé en effondrement — manque de sages-femmes qualifiées et d'infrastructures obstétriques"], estimated_maternal_risk_index: 8.62, last_updated: "2026-06-20" },
    { entity_id: "MM-002", name: "Tchad & Niger — Sahel Obstétrical", country: "Afrique Subsaharienne", sector: "Crise Obstétricale Silencieuse dans les Déserts Médicaux", composite_score: 85.9, healthcare_system_collapse_score: 88.0, gender_inequality_score: 85.0, obstetric_access_deficit_score: 87.0, conflict_health_impact_score: 82.0, risk_level: "critique", primary_pattern: "crise_humanitaire_maternelle", key_signals: ["Crise de mortalité maternelle en Tchad & Niger — décès obstétriques évitables massifs révélant une faillite de l'État", "Inégalité de genre systémique — femmes exclues de l'accès aux soins obstétriques de base", "Système de santé en effondrement — manque de sages-femmes qualifiées et d'infrastructures obstétriques"], estimated_maternal_risk_index: 8.59, last_updated: "2026-06-20" },
    { entity_id: "MM-003", name: "Somalie & RDC — Conflit & Maternité", country: "Afrique de l'Est/Centrale", sector: "Conflits Armés Détruisant les Infrastructures Obstétriques", composite_score: 83.4, healthcare_system_collapse_score: 85.0, gender_inequality_score: 80.0, obstetric_access_deficit_score: 82.0, conflict_health_impact_score: 92.0, risk_level: "critique", primary_pattern: "crise_humanitaire_maternelle", key_signals: ["Crise de mortalité maternelle en Somalie & RDC — décès obstétriques évitables massifs révélant une faillite de l'État", "Inégalité de genre systémique — femmes exclues de l'accès aux soins obstétriques de base", "Système de santé en effondrement — manque de sages-femmes qualifiées et d'infrastructures obstétriques"], estimated_maternal_risk_index: 8.34, last_updated: "2026-06-20" },
    { entity_id: "MM-004", name: "Afghanistan — Régime Taliban & Santé Féminine", country: "Asie Centrale", sector: "Interdiction des Soignantes Féminines — Crise Obstétricale Délibérée", composite_score: 82.65, healthcare_system_collapse_score: 78.0, gender_inequality_score: 95.0, obstetric_access_deficit_score: 85.0, conflict_health_impact_score: 70.0, risk_level: "critique", primary_pattern: "desengagement_etatique", key_signals: ["Crise de mortalité maternelle en Afghanistan — décès obstétriques évitables massifs révélant une faillite de l'État", "Inégalité de genre systémique — femmes exclues de l'accès aux soins obstétriques de base", "Système de santé en effondrement — manque de sages-femmes qualifiées et d'infrastructures obstétriques"], estimated_maternal_risk_index: 8.27, last_updated: "2026-06-20" },
    { entity_id: "MM-005", name: "Haïti — Effondrement Sanitaire Post-Séisme", country: "Amériques", sector: "Gangs Bloquant l'Accès aux Maternités — Crise Urbaine", composite_score: 73.6, healthcare_system_collapse_score: 72.0, gender_inequality_score: 68.0, obstetric_access_deficit_score: 75.0, conflict_health_impact_score: 80.0, risk_level: "critique", primary_pattern: "fragilite_systemique", key_signals: ["Crise de mortalité maternelle en Haïti — décès obstétriques évitables massifs révélant une faillite de l'État", "Inégalité de genre systémique — femmes exclues de l'accès aux soins obstétriques de base", "Système de santé en effondrement — manque de sages-femmes qualifiées et d'infrastructures obstétriques"], estimated_maternal_risk_index: 7.36, last_updated: "2026-06-20" },
    { entity_id: "MM-006", name: "Inde — Disparités Rurales Persistantes", country: "Asie du Sud", sector: "Mortalité Maternelle Concentrée en Zones Rurales et Dalits", composite_score: 50.9, healthcare_system_collapse_score: 45.0, gender_inequality_score: 58.0, obstetric_access_deficit_score: 62.0, conflict_health_impact_score: 35.0, risk_level: "élevé", primary_pattern: "fragilite_systemique", key_signals: ["Fragilité obstétricale grave dans Inde — mortalité maternelle élevée malgré des ressources disponibles", "Accès aux soins anténataux insuffisant — couverture rurale et zones de conflit déficitaires", "Inégalités de genre freinant le recours aux soins — barrières culturelles et économiques persistantes"], estimated_maternal_risk_index: 5.09, last_updated: "2026-06-20" },
    { entity_id: "MM-007", name: "Brésil & Mexique — Inégalités Raciales", country: "Amériques", sector: "Mortalité Maternelle Disproportionnée chez les Femmes Noires/Indigènes", composite_score: 37.9, healthcare_system_collapse_score: 38.0, gender_inequality_score: 42.0, obstetric_access_deficit_score: 40.0, conflict_health_impact_score: 28.0, risk_level: "modéré", primary_pattern: "lacunes_rurales", key_signals: ["Lacunes persistantes en santé maternelle dans Brésil & Mexique — disparités rural-urbain et inégalités sociales", "Progrès insuffisants vers les objectifs ODD de réduction de mortalité maternelle", "Formation des personnels de santé obstétricaux insuffisante dans les zones reculées"], estimated_maternal_risk_index: 3.79, last_updated: "2026-06-20" },
    { entity_id: "MM-008", name: "Scandinavie & Canada — Excellence Obstétricale", country: "Global Nord", sector: "Mortalité Maternelle Quasi-Nulle — Modèles Universels", composite_score: 4.75, healthcare_system_collapse_score: 5.0, gender_inequality_score: 8.0, obstetric_access_deficit_score: 4.0, conflict_health_impact_score: 3.0, risk_level: "faible", primary_pattern: "systeme_performant", key_signals: ["Scandinavie & Canada maintient un système de santé maternelle performant — mortalité maternelle maîtrisée", "Couverture obstétricale universelle avec accès équitable aux soins anténataux et postnataux", "Modèle de santé maternelle à diffuser — investissement public fort et approche genrée des soins"], estimated_maternal_risk_index: 0.48, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 5, "élevé": 1, "modéré": 1, faible: 1 },
    pattern_distribution: { crise_humanitaire_maternelle: 3, desengagement_etatique: 1, fragilite_systemique: 2, lacunes_rurales: 1, systeme_performant: 1 },
    top_risk_entities: ["Sierra Leone — Mortalité Maternelle Record", "Tchad & Niger — Sahel Obstétrical", "Somalie & RDC — Conflit & Maternité"],
    critical_alerts: ["Sierra Leone: crise humanitaire maternelle", "Tchad & Niger: crise humanitaire maternelle", "Somalie & RDC: crise humanitaire maternelle", "Afghanistan: désengagement étatique", "Haïti: fragilité systémique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "maternal_mortality",
    confidence_score: 0.91,
    data_sources: ["who_maternal_mortality_estimates", "unfpa_obstetric_fistula_tracker", "unicef_antenatal_care_coverage"],
    entities,
    avg_estimated_maternal_risk_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
