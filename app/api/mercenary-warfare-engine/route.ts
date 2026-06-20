import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[mercenary-warfare-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Mercenary Warfare Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/mercenary-warfare-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Mercenary Warfare Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Mercenary Warfare Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "MW-001", name: "Russie — Wagner/Africa Corps & 30 Pays Déployés", country: "Europe de l'Est", sector: "Africa Corps GRU (ex-Wagner), RCA/Mali/Libye/Ukraine & Ressources contre Sécurité", composite_score: 88.5, pmc_deployment_scale_score: 92.0, state_deniability_score: 90.0, atrocity_impunity_score: 88.0, resource_extraction_violence_score: 82.0, risk_level: "critique", primary_pattern: "deploiement_pmc_etatique", key_signals: ["Déploiement PMC systémique par Russie — armées privées projetées en zones de conflit avec déni étatique institutionnalisé", "Crimes de guerre sans responsabilité — massacres, tortures et pillages commis par des forces privées sans poursuites pénales", "Nexus minerais-milices — ressources extractives financent directement le recrutement et l'armement des forces paramilitaires"], estimated_mercenary_index: 8.85, last_updated: "2026-06-20" },
    { entity_id: "MW-002", name: "USA — Blackwater/Academi & Contrats Pentagone", country: "Amérique du Nord", sector: "Academi ex-Blackwater, Nisour Square 17 Civils & 900M$ Contrats Iraq/Afghanistan", composite_score: 78.45, pmc_deployment_scale_score: 72.0, state_deniability_score: 85.0, atrocity_impunity_score: 88.0, resource_extraction_violence_score: 68.0, risk_level: "critique", primary_pattern: "impunite_criminelle_pmc", key_signals: ["Déploiement PMC systémique par USA — armées privées projetées en zones de conflit avec déni étatique institutionnalisé", "Crimes de guerre sans responsabilité — massacres, tortures et pillages commis par des forces privées sans poursuites pénales", "Nexus minerais-milices — ressources extractives financent directement le recrutement et l'armement des forces paramilitaires"], estimated_mercenary_index: 7.85, last_updated: "2026-06-20" },
    { entity_id: "MW-003", name: "EAU & Turquie — PMC Régionales Syrie/Libye", country: "MENA", sector: "SNA Turquie Syrie, Milices Libyennes EAU & PMC Azerbaïdjan Nagorno-Karabakh", composite_score: 81.55, pmc_deployment_scale_score: 88.0, state_deniability_score: 88.0, atrocity_impunity_score: 75.0, resource_extraction_violence_score: 72.0, risk_level: "critique", primary_pattern: "deploiement_pmc_etatique", key_signals: ["Déploiement PMC systémique par EAU & Turquie — armées privées projetées en zones de conflit avec déni étatique institutionnalisé", "Crimes de guerre sans responsabilité — massacres, tortures et pillages commis par des forces privées sans poursuites pénales", "Nexus minerais-milices — ressources extractives financent directement le recrutement et l'armement des forces paramilitaires"], estimated_mercenary_index: 8.16, last_updated: "2026-06-20" },
    { entity_id: "MW-004", name: "Congo-Kivu — Milices Cobalt, Or & Coltan", country: "Afrique Centrale", sector: "FDLR, M23 & ADF Financés par Minerais Sang — Cobalt Batteries EV via Milices", composite_score: 80.85, pmc_deployment_scale_score: 82.0, state_deniability_score: 78.0, atrocity_impunity_score: 75.0, resource_extraction_violence_score: 90.0, risk_level: "critique", primary_pattern: "milices_ressources", key_signals: ["Déploiement PMC systémique par Congo-Kivu — armées privées projetées en zones de conflit avec déni étatique institutionnalisé", "Crimes de guerre sans responsabilité — massacres, tortures et pillages commis par des forces privées sans poursuites pénales", "Nexus minerais-milices — ressources extractives financent directement le recrutement et l'armement des forces paramilitaires"], estimated_mercenary_index: 8.09, last_updated: "2026-06-20" },
    { entity_id: "MW-005", name: "Sahel — Africa Corps & Gouvernements Militaires", country: "Afrique de l'Ouest", sector: "Mali/Burkina/Niger Juntes Contractant Africa Corps Contre Or & Uranium", composite_score: 56.4, pmc_deployment_scale_score: 58.0, state_deniability_score: 52.0, atrocity_impunity_score: 60.0, resource_extraction_violence_score: 55.0, risk_level: "élevé", primary_pattern: "instrumentalisation_mercenaires", key_signals: ["Instrumentalisation des mercenaires par Sahel — forces privées contournant les contraintes politiques des armées régulières", "Guerres par délégation — conflits régionaux alimentés par des PMC permettant la projection d'influence sans engagement officiel", "Impunité partielle — mécanismes de responsabilité insuffisants face aux abus documentés des contractuels militaires privés"], estimated_mercenary_index: 5.64, last_updated: "2026-06-20" },
    { entity_id: "MW-006", name: "Libye — Marché PMC Fragmenté Multi-Acteurs", country: "MENA", sector: "PMC Turques, Russes, Émiraties & Tchadiennes en Concurrence sur Pétrole Libyen", composite_score: 51.35, pmc_deployment_scale_score: 52.0, state_deniability_score: 48.0, atrocity_impunity_score: 55.0, resource_extraction_violence_score: 50.0, risk_level: "élevé", primary_pattern: "instrumentalisation_mercenaires", key_signals: ["Instrumentalisation des mercenaires par Libye — forces privées contournant les contraintes politiques des armées régulières", "Guerres par délégation — conflits régionaux alimentés par des PMC permettant la projection d'influence sans engagement officiel", "Impunité partielle — mécanismes de responsabilité insuffisants face aux abus documentés des contractuels militaires privés"], estimated_mercenary_index: 5.14, last_updated: "2026-06-20" },
    { entity_id: "MW-007", name: "Ukraine — Légion Étrangère & Volontaires Régulés", country: "Europe", sector: "Légion Étrangère Ukraine, ITAR Limites & Tentative de Régulation des Combattants", composite_score: 29.15, pmc_deployment_scale_score: 30.0, state_deniability_score: 28.0, atrocity_impunity_score: 35.0, resource_extraction_violence_score: 22.0, risk_level: "modéré", primary_pattern: "instrumentalisation_mercenaires", key_signals: ["Prolifération PMC dans Ukraine — présence de forces privées sans cadre légal et accountability adéquats", "Zone grise juridique — contractuels militaires opérant dans des espaces où le droit international humanitaire est mal appliqué", "Risque d'escalade — PMC sans doctrine d'engagement claire pouvant déclencher des incidents non souhaités"], estimated_mercenary_index: 2.92, last_updated: "2026-06-20" },
    { entity_id: "MW-008", name: "ICRC & Document Montreux — Régulation PMC", country: "Global", sector: "Document Montreux 2008, ICoCA & Droit International Humanitaire PMC en Négociation", composite_score: 4.8, pmc_deployment_scale_score: 5.0, state_deniability_score: 4.0, atrocity_impunity_score: 6.0, resource_extraction_violence_score: 4.0, risk_level: "faible", primary_pattern: "regulation_pmc_emergeante", key_signals: ["ICRC & Document Montreux développe un cadre de régulation PMC fondé sur le Document de Montreux et les normes ICoCA", "Transparence contractuelle — registres publics des déploiements de PMC et mécanismes de responsabilité parlementaire", "Modèle de régulation à internationaliser — convention contraignante sur les PMC en gestation multilatérale"], estimated_mercenary_index: 0.48, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { deploiement_pmc_etatique: 2, milices_ressources: 1, impunite_criminelle_pmc: 1, instrumentalisation_mercenaires: 3, regulation_pmc_emergeante: 1 },
    top_risk_entities: ["Russie — Wagner/Africa Corps & 30 Pays Déployés", "EAU & Turquie — PMC Régionales Syrie/Libye", "Congo-Kivu — Milices Cobalt, Or & Coltan"],
    critical_alerts: ["Russie: déploiement pmc étatique", "USA: impunité criminelle pmc", "EAU & Turquie: déploiement pmc étatique", "Congo-Kivu: milices ressources"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "mercenary_warfare",
    confidence_score: 0.79,
    data_sources: ["acled_armed_conflict_pmc_tracker", "geneva_academy_mercenary_monitor", "private_security_monitor_uk"],
    entities,
    avg_estimated_mercenary_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
