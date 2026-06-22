import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[disability-rights-ableism-engine] SWARM_API_URL is not set — falling back to mock data");
}

function getMockData() {
  return {
    agent: "Disability Rights Ableism Engine Agent",
    domain: "disability_rights_ableism",
    total_entities: 8,
    avg_composite: 57.12,
    confidence_score: 0.86,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { institutionnalisation_forcee: 3, discrimination_emploi_acces: 1, deficit_application_protection_legale: 3, modele_medical_droits_negation: 1 },
    top_risk_entities: [
      "Russie/Psychushka — Internement Psychiatrique Opposants Politiques Classifiés Handicapés, Déni Autonomie Systémique, Aucun Recours Légal Effectif & Conditions Dégradantes Documentées",
      "Chine/Ankang — Institutions Psychiatriques Sécurité Contrôlées Police, Dissidents Diagnostiqués 'Paranoïa Querulante', Traitement Forcé & Famille Sans Information Détention",
      "Inde/600M Personnes Handicap — Zéro Accessibilité Infrastructure Urbaine, Exclusion Emploi Formel 97%, Écoles Non Inclusives & RPWD 2016 Application Quasi Nulle",
    ],
    critical_alerts: [
      "Russie/Psychushka: institutionnalisation_forcee",
      "Chine/Ankang: institutionnalisation_forcee",
      "Inde/600M Personnes Handicap: discrimination_emploi_acces",
      "USA/Olmstead: institutionnalisation_forcee",
    ],
    last_analysis: "2026-06-21",
    engine_version: "1.0.0",
    avg_estimated_disability_rights_ableism_index: 5.71,
    data_sources: [
      "un_crpd_committee_concluding_observations_2023",
      "disability_rights_international_reports",
      "who_world_disability_report_2023",
      "european_disability_forum_annual_report",
    ],
    entities: [
      { id: "DRA-001", name: "Russie/Psychushka — Internement Psychiatrique Opposants Politiques Classifiés Handicapés, Déni Autonomie Systémique, Aucun Recours Légal Effectif & Conditions Dégradantes Documentées", country: "Russie", sector: "Institutionnalisation Forcée Politique", forced_institutionalization_autonomy_denial_score: 92.0, disability_discrimination_employment_access_score: 88.0, medical_model_rights_based_deficit_score: 90.0, disability_legal_protection_enforcement_gap_score: 85.0, composite_score: 89.1, risk_level: "critique", primary_pattern: "institutionnalisation_forcee", key_signals: ["Psychiatrisation politique — opposants classifiés comme malades mentaux et internés de force dans les Psychushka, réactivant les pratiques soviétiques de répression par le handicap diagnostiqué", "Zéro autonomie — détenus sous tutelle médicale permanente sans droit de refuser les traitements, violant l'article 12 de la CDPH sur la capacité juridique égale", "Impunité systémique — aucune poursuite contre les psychiatres complices, aucun mécanisme de recours indépendant accessible aux victimes"], estimated_disability_rights_ableism_index: 8.91, last_updated: "2026-06-21" },
      { id: "DRA-002", name: "Chine/Ankang — Institutions Psychiatriques Sécurité Contrôlées Police, Dissidents Diagnostiqués 'Paranoïa Querulante', Traitement Forcé & Famille Sans Information Détention", country: "Chine", sector: "Psychiatrie Sécuritaire", forced_institutionalization_autonomy_denial_score: 90.0, disability_discrimination_employment_access_score: 85.0, medical_model_rights_based_deficit_score: 88.0, disability_legal_protection_enforcement_gap_score: 82.0, composite_score: 86.65, risk_level: "critique", primary_pattern: "institutionnalisation_forcee", key_signals: ["Ankang comme outil politique — 30+ établissements psychiatriques sécuritaires sous contrôle policier utilisant le diagnostic 'paranoïa quérulante' pour interner les pétitionnaires et militants", "Traitement forcé sans consentement — médicaments antipsychotiques administrés de force, isolation complète de la famille, aucun accès à un avocat", "Absence totale de contrôle indépendant — inspections internes uniquement, aucun mécanisme ONU n'a accès aux Ankang"], estimated_disability_rights_ableism_index: 8.67, last_updated: "2026-06-21" },
      { id: "DRA-003", name: "Inde/600M Personnes Handicap — Zéro Accessibilité Infrastructure Urbaine, Exclusion Emploi Formel 97%, Écoles Non Inclusives & RPWD 2016 Application Quasi Nulle", country: "Inde", sector: "Accessibilité & Emploi", forced_institutionalization_autonomy_denial_score: 72.0, disability_discrimination_employment_access_score: 85.0, medical_model_rights_based_deficit_score: 75.0, disability_legal_protection_enforcement_gap_score: 80.0, composite_score: 77.6, risk_level: "critique", primary_pattern: "discrimination_emploi_acces", key_signals: ["Exclusion massive de l'emploi — 97% des personnes handicapées en Inde sont exclues de l'emploi formel, violant l'article 27 de la CDPH ratifiée en 2007", "Infrastructure inaccessible — 99.5% des stations de métro, transports en commun et bâtiments publics restent inaccessibles malgré la loi RPWD 2016", "Éducation ségrégée — 85% des enfants handicapés exclus du système scolaire ordinaire, maintenus dans des établissements spéciaux sans perspectives d'inclusion"], estimated_disability_rights_ableism_index: 7.76, last_updated: "2026-06-21" },
      { id: "DRA-004", name: "USA/Olmstead — Désinstitutionnalisation Inachevée 40 États, 400K Personnes Institutions, Listes Attente Communautaires 10+ Ans & Financement Medicaid Biaisé Institutions", country: "USA", sector: "Désinstitutionnalisation Inachevée", forced_institutionalization_autonomy_denial_score: 68.0, disability_discrimination_employment_access_score: 72.0, medical_model_rights_based_deficit_score: 65.0, disability_legal_protection_enforcement_gap_score: 70.0, composite_score: 68.65, risk_level: "critique", primary_pattern: "institutionnalisation_forcee", key_signals: ["Décision Olmstead non appliquée — malgré la décision SCOTUS 1999 exigeant l'intégration communautaire, 400.000 personnes restent institutionnalisées dans 40 États", "Listes d'attente décennales — délais de 10-25 ans pour accéder aux services communautaires dans certains États, forçant la famille à choisir l'institution", "Financement pervers — Medicaid finance à 100% l'institutionnalisation mais plafonne les services communautaires, créant une incitation structurelle à l'institutionnalisation"], estimated_disability_rights_ableism_index: 6.87, last_updated: "2026-06-21" },
      { id: "DRA-005", name: "Brésil/Loi Handicap 2015 — Application Partielle IBGE 18% Population Handicapée, Accessibilité Transport Inexistante Villes Secondaires & Guichets Emploi Non Adaptés", country: "Brésil", sector: "Législation Partiellement Appliquée", forced_institutionalization_autonomy_denial_score: 48.0, disability_discrimination_employment_access_score: 55.0, medical_model_rights_based_deficit_score: 52.0, disability_legal_protection_enforcement_gap_score: 50.0, composite_score: 51.15, risk_level: "élevé", primary_pattern: "deficit_application_protection_legale", key_signals: ["Loi Lei Brasileira de Inclusão ambitieuse mais sous-financée — 18% de la population handicapée (38M personnes) confrontée à un gap majeur entre droits légaux et réalité", "Transport inaccessible — 73% des municipalités brésiliennes sans aucun transport adapté, isolant les personnes handicapées des opportunités économiques", "Quota emploi non respecté — loi de 2% à 5% de travailleurs handicapés dans les entreprises 100+ employés respectée dans seulement 12% des entreprises contrôlées"], estimated_disability_rights_ableism_index: 5.11, last_updated: "2026-06-21" },
      { id: "DRA-006", name: "Maroc/Exclusion Totale Emploi Formel — Personnes Handicap 2.6M Sans Couverture Sociale, Infrastructure Inexistante, Modèle Médical Dominant & Législation 2016 Non Appliquée", country: "Maroc", sector: "Exclusion Systémique", forced_institutionalization_autonomy_denial_score: 45.0, disability_discrimination_employment_access_score: 58.0, medical_model_rights_based_deficit_score: 48.0, disability_legal_protection_enforcement_gap_score: 52.0, composite_score: 50.4, risk_level: "élevé", primary_pattern: "modele_medical_droits_negation", key_signals: ["Exclusion économique totale — 90% des 2.6M personnes handicapées sans emploi formel ni protection sociale, perpétuant la pauvreté intergénérationnelle", "Modèle médical dominant — les politiques marocaines traitent le handicap comme une pathologie médicale et non comme une question de droits humains et d'accessibilité", "Ratification CDPH sans application — ratifiée en 2009, la convention est sans mécanisme de suivi national fonctionnel ni budget dédié à l'accessibilité"], estimated_disability_rights_ableism_index: 5.04, last_updated: "2026-06-21" },
      { id: "DRA-007", name: "UE/Convention CDPH Ratifiée — Gaps Application Significatifs États Membres, Institutionnalisation Persistante 5 États, Plaintes Comité ONU Non Suivies & Ajustements Raisonnables Partiels", country: "Union Européenne", sector: "Gaps Application Régionale", forced_institutionalization_autonomy_denial_score: 25.0, disability_discrimination_employment_access_score: 30.0, medical_model_rights_based_deficit_score: 28.0, disability_legal_protection_enforcement_gap_score: 35.0, composite_score: 29.0, risk_level: "modéré", primary_pattern: "deficit_application_protection_legale", key_signals: ["Institutionnalisation persistante — 5 États membres (Hongrie, Bulgarie, Roumanie, Pologne, Lettonie) maintiennent des institutions résidentielles malgré les obligations CDPH", "Plaintes ONU sans suite — le Comité CDPH a rendu des recommandations contre 3 États membres non suivies d'effets, illustrant les limites du mécanisme de contrôle", "Stratégie Handicap UE 2021-2030 — cadre ambitieux mais non-contraignant, avec des écarts significatifs entre États nordiques et États d'Europe centrale"], estimated_disability_rights_ableism_index: 2.9, last_updated: "2026-06-21" },
      { id: "DRA-008", name: "Suède/Modèle Inclusion LSS — Droits Personnels Assistance Reconnus, Taux Emploi Handicap 60%, Accessibilité Universelle Infrastructure & Désinstitutionnalisation Quasi Complète", country: "Suède", sector: "Modèle d'Inclusion", forced_institutionalization_autonomy_denial_score: 4.0, disability_discrimination_employment_access_score: 5.0, medical_model_rights_based_deficit_score: 3.0, disability_legal_protection_enforcement_gap_score: 6.0, composite_score: 4.4, risk_level: "faible", primary_pattern: "deficit_application_protection_legale", key_signals: ["Droit à l'assistance personnelle légalement garanti — la loi LSS donne à chaque personne handicapée le droit à des heures d'assistance choisies librement, finançant l'autonomie", "Désinstitutionnalisation quasi complète — moins de 500 personnes en institutions en 2023 pour un pays de 10M, modèle exporté dans 15 pays nordiques et baltes", "Design universel comme standard — toute construction publique et transport doit être accessible, avec amendes effectives pour non-conformité"], estimated_disability_rights_ableism_index: 0.44, last_updated: "2026-06-21" },
    ],
  };
}

const MOCK = getMockData();

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/disability-rights-ableism-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
