import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[resource-curse-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Resource Curse Engine Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/resource-curse-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Resource Curse Engine Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Resource Curse Engine Agent"), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    { id: "RC-001", name: "Venezuela — Effondrement Pétrolier", country: "Amériques", sector: "Malédiction Pétrolière Totale", composite_score: 91.35, resource_dependency_score: 95.0, institutional_degradation_score: 92.0, dutch_disease_score: 90.0, elite_capture_score: 88.0, risk_level: "critique", primary_pattern: "malediction_ressources_totale", key_signals: ["Malédiction des ressources totale pour Venezuela — institutions corrompues par la rente", "Dépendance mono-produit extrême — économie non diversifiée et vulnérable aux chocs", "Capture de la rente par les élites — inégalités structurelles et instabilité chronique"], estimated_curse_index: 9.14, last_updated: "2026-06-20" },
    { id: "RC-002", name: "Nigeria — Pétrole & Corruption", country: "Afrique", sector: "Delta du Niger & Rente Confisquée", composite_score: 87.75, resource_dependency_score: 88.0, institutional_degradation_score: 85.0, dutch_disease_score: 82.0, elite_capture_score: 90.0, risk_level: "critique", primary_pattern: "malediction_ressources_totale", key_signals: ["Malédiction des ressources totale pour Nigeria — institutions corrompues par la rente", "Dépendance mono-produit extrême — économie non diversifiée et vulnérable aux chocs", "Capture de la rente par les élites — inégalités structurelles et instabilité chronique"], estimated_curse_index: 8.78, last_updated: "2026-06-20" },
    { id: "RC-003", name: "RDC — Minerais & Guerre", country: "Afrique", sector: "Coltan, Or & Conflits Armés Perpétuels", composite_score: 86.5, resource_dependency_score: 85.0, institutional_degradation_score: 90.0, dutch_disease_score: 78.0, elite_capture_score: 92.0, risk_level: "critique", primary_pattern: "malediction_ressources_totale", key_signals: ["Malédiction des ressources totale pour RDC — institutions corrompues par la rente", "Dépendance mono-produit extrême — économie non diversifiée et vulnérable aux chocs", "Capture de la rente par les élites — inégalités structurelles et instabilité chronique"], estimated_curse_index: 8.65, last_updated: "2026-06-20" },
    { id: "RC-004", name: "Angola — Pétrole & Oligarchie", country: "Afrique", sector: "Rente Pétrolière & Exclusion Massive", composite_score: 81.25, resource_dependency_score: 82.0, institutional_degradation_score: 80.0, dutch_disease_score: 75.0, elite_capture_score: 85.0, risk_level: "critique", primary_pattern: "malediction_ressources_totale", key_signals: ["Malédiction des ressources totale pour Angola — institutions corrompues par la rente", "Dépendance mono-produit extrême — économie non diversifiée et vulnérable aux chocs", "Capture de la rente par les élites — inégalités structurelles et instabilité chronique"], estimated_curse_index: 8.13, last_updated: "2026-06-20" },
    { id: "RC-005", name: "Irak — Pétrodépendance Totale", country: "MENA", sector: "Pétrole & Instabilité Politique Chronique", composite_score: 74.0, resource_dependency_score: 78.0, institutional_degradation_score: 72.0, dutch_disease_score: 70.0, elite_capture_score: 75.0, risk_level: "critique", primary_pattern: "dependance_rentiere_critique", key_signals: ["Dépendance rentière avancée dans Irak — syndrome hollandais en cours", "Désindustrialisation liée à la rente — secteurs non-ressources en déclin", "Capture partielle de la rente — institutions fragilisées mais non effondrées"], estimated_curse_index: 7.4, last_updated: "2026-06-20" },
    { id: "RC-006", name: "Arabie Saoudite — Vision 2030", country: "MENA", sector: "Transition Difficile de la Rente Pétrolière", composite_score: 65.95, resource_dependency_score: 72.0, institutional_degradation_score: 58.0, dutch_disease_score: 65.0, elite_capture_score: 60.0, risk_level: "élevé", primary_pattern: "syndrome_hollandais", key_signals: ["Dépendance rentière avancée dans Arabie Saoudite — syndrome hollandais en cours", "Désindustrialisation liée à la rente — secteurs non-ressources en déclin", "Capture partielle de la rente — institutions fragilisées mais non effondrées"], estimated_curse_index: 6.6, last_updated: "2026-06-20" },
    { id: "RC-007", name: "Botswana — Diamants Bien Gérés", country: "Afrique", sector: "Réussite Partielle de Diversification", composite_score: 34.35, resource_dependency_score: 40.0, institutional_degradation_score: 30.0, dutch_disease_score: 35.0, elite_capture_score: 28.0, risk_level: "modéré", primary_pattern: "rente_moderee", key_signals: ["Rente modérée dans Botswana — risque de syndrome hollandais à surveiller", "Diversification en cours mais dépendance aux ressources encore significative", "Institutions sous pression de la rente — réformes nécessaires"], estimated_curse_index: 3.44, last_updated: "2026-06-20" },
    { id: "RC-008", name: "Norvège — Modèle de Gestion", country: "Europe du Nord", sector: "Fonds Souverain & Diversification Exemplaire", composite_score: 18.7, resource_dependency_score: 35.0, institutional_degradation_score: 12.0, dutch_disease_score: 18.0, elite_capture_score: 10.0, risk_level: "faible", primary_pattern: "diversification_reussie", key_signals: ["Norvège a réussi à transformer la richesse en ressources en développement durable", "Fonds souverain et discipline budgétaire permettant la diversification", "Modèle de gestion des ressources à étudier et diffuser"], estimated_curse_index: 1.87, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 5, "élevé": 1, "modéré": 1, faible: 1 },
    pattern_distribution: { malediction_ressources_totale: 4, dependance_rentiere_critique: 1, syndrome_hollandais: 1, rente_moderee: 1, diversification_reussie: 1 },
    top_risk_entities: ["Venezuela — Effondrement Pétrolier", "Nigeria — Pétrole & Corruption", "RDC — Minerais & Guerre"],
    critical_alerts: ["Venezuela: malédiction ressources totale", "Nigeria: malédiction ressources totale", "RDC: malédiction ressources totale", "Angola: malédiction ressources totale", "Irak: dépendance rentière critique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "resource_curse",
    confidence_score: 0.83,
    data_sources: ["natural_resource_governance_index", "imf_resource_tracker", "transparency_international"],
    entities,
    avg_estimated_curse_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
