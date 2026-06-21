import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[child-marriage-forced-union-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Child Marriage Forced Union Rights Engine Agent",
  domain: "child_marriage_forced_union_rights",
  total_entities: 8,
  avg_composite: 60.59,
  confidence_score: 0.89,
  avg_estimated_child_marriage_forced_union_rights_index: 6.06,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  pattern_distribution: { child_marriage_prevalence: 3, forced_union_coercion: 2, legal_age_gap: 2, crc_enforcement_failure: 1 },
  top_risk_entities: [
    "Niger/Sahel — 76% Filles Mariées Avant 18 Ans & Record Mondial Mariage Précoce",
    "Bangladesh/Rural — 59% Mariages Filles Avant 18 Ans & Loi Exceptions Mineurs",
    "Yémen/Conflit — Mariage Précoce +20% Guerre & Aucun Âge Minimum Légal",
  ],
  critical_alerts: [
    "Niger/Sahel: child_marriage_prevalence",
    "Bangladesh/Rural: legal_age_gap",
    "Yémen/Conflit: forced_union_coercion",
    "Éthiopie/Amhara: child_marriage_prevalence",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  data_sources: [
    "girls_not_brides_2023",
    "unicef_child_marriage_2023",
    "un_women_forced_marriage_2022",
    "hrw_child_marriage_2023",
  ],
  entities: [
    { entity_id: "CM-001", name: "Niger/Sahel — 76% Filles Mariées Avant 18 Ans & Record Mondial Mariage Précoce", country: "Afrique de l'Ouest", sector: "76% Filles Mariées <18 Ans Record Mondial, 28% Mariées <15 Ans, Dot Système Perpétuation & Pauvreté Facteur Principal Absence Scolarisation Filles", composite_score: 91.2, child_marriage_prevalence_score: 95.0, forced_union_coercion_score: 90.0, legal_age_gap_score: 88.0, crc_enforcement_failure_score: 92.0, risk_level: "critique", primary_pattern: "child_marriage_prevalence", key_signals: ["Prévalence record mondiale au Niger — 76% des filles mariées avant 18 ans, 28% avant 15 ans, violation flagrante CRC Article 16 et CEDAW Article 16 sur consentement libre et entier au mariage", "Système de dot perpétuant le mariage précoce — la pauvreté extrême du Sahel transforme les filles en actif économique, créant un cycle où l'absence de scolarisation renforce la vulnérabilité au mariage forcé précoce", "Activer le Comité des Droits de l'Enfant ONU et Girls Not Brides pour un plan d'action Niger ciblant l'éducation des filles et l'élimination du mariage avant 18 ans d'ici 2030"], estimated_child_marriage_forced_union_rights_index: 9.12, last_updated: "2026-06-21" },
    { entity_id: "CM-002", name: "Bangladesh/Rural — 59% Mariages Filles Avant 18 Ans & Loi Exceptions Mineurs", country: "Asie du Sud", sector: "59% Filles Mariées <18 Ans, Loi 2017 'Exceptions Spéciales' Sans Âge Minimum, Cyclones/Inondations Facteurs Déplacements & Harcèlement Scolaire Abandon", composite_score: 84.7, child_marriage_prevalence_score: 88.0, forced_union_coercion_score: 82.0, legal_age_gap_score: 85.0, crc_enforcement_failure_score: 84.0, risk_level: "critique", primary_pattern: "legal_age_gap", key_signals: ["Lacune légale dangereuse au Bangladesh — la loi de 2017 sur le mariage permet des 'exceptions spéciales' sans âge minimum légal, créant une porte ouverte aux mariages d'enfants avec accord parental et judiciaire", "Impact des catastrophes climatiques — cyclones et inondations récurrents forcent des familles à marier leurs filles pour réduire les bouches à nourrir, liant mariage précoce et vulnérabilité climatique au Bangladesh", "Abroger les 'exceptions spéciales' de la loi bangladaise de 2017 et renforcer les programmes de maintien des filles à l'école comme alternative économique au mariage précoce"], estimated_child_marriage_forced_union_rights_index: 8.47, last_updated: "2026-06-21" },
    { entity_id: "CM-003", name: "Yémen/Conflit — Mariage Précoce +20% Guerre & Aucun Âge Minimum Légal", country: "MENA", sector: "Mariage Précoce +20% Depuis 2015 Conflit, Aucun Âge Minimum Légal Filles, 32% Filles <18 Ans & Déplacement 4M Familles Facteur Vulnérabilité", composite_score: 87.3, child_marriage_prevalence_score: 90.0, forced_union_coercion_score: 88.0, legal_age_gap_score: 85.0, crc_enforcement_failure_score: 86.0, risk_level: "critique", primary_pattern: "forced_union_coercion", key_signals: ["Explosion du mariage précoce en temps de guerre au Yémen — conflit armé depuis 2015 a augmenté le mariage précoce de 20%, avec absence totale d'âge minimum légal pour les filles exploitée par familles en détresse économique", "Vide juridique absolu — le Yémen n'a fixé aucun âge minimum légal pour le mariage des filles, permettant des mariages d'enfants de tout âge avec 'consentement' du tuteur, violant CRC et CEDAW ratifiés", "Exiger que les négociations de paix yéménites incluent l'établissement d'un âge minimum légal de 18 ans pour le mariage et un programme de protection des filles dans les zones de conflit"], estimated_child_marriage_forced_union_rights_index: 8.73, last_updated: "2026-06-21" },
    { entity_id: "CM-004", name: "Éthiopie/Amhara — 40% Mariage Avant 15 Ans & Pratiques Enlèvement Culturel", country: "Afrique de l'Est", sector: "40% Filles Amhara Mariées <15 Ans, Télafa 'Enlèvement' Pratique Mariage, Loi Fédérale 18 Ans Inappliquée Régions & Kiremt Saison Mariages Forcés", composite_score: 82.1, child_marriage_prevalence_score: 85.0, forced_union_coercion_score: 88.0, legal_age_gap_score: 75.0, crc_enforcement_failure_score: 80.0, risk_level: "critique", primary_pattern: "child_marriage_prevalence", key_signals: ["Prévalence extrême en région Amhara — 40% des filles mariées avant 15 ans, pratique du Télafa (enlèvement rituel pour mariage) persistante malgré interdiction légale, violation CRC Article 19 sur protection contre violences", "Fracture entre loi fédérale et pratique régionale — l'Éthiopie fixe légalement 18 ans mais les régions rurales Amhara maintiennent des pratiques culturelles de mariage précoce, illustrant le défi de l'application effective des droits", "Renforcer les tribunaux communautaires éthiopiens pour poursuivre les mariages précoces en Amhara et financer des programmes de leadership féminin pour transformer les normes culturelles"], estimated_child_marriage_forced_union_rights_index: 8.21, last_updated: "2026-06-21" },
    { entity_id: "CM-005", name: "Inde/Rural — 23% Filles Mariées Avant 18 Ans & Prohibition Marriage Act Inappliqué", country: "Asie du Sud", sector: "23% Filles Rural Mariées <18 Ans NFHS-5, PCMA 2006 Inappliqué 80% Districts, Saison Mariage Scolaire & Discrimination Caste Mariage Précoce Dalits", composite_score: 54.8, child_marriage_prevalence_score: 55.0, forced_union_coercion_score: 52.0, legal_age_gap_score: 58.0, crc_enforcement_failure_score: 54.0, risk_level: "élevé", primary_pattern: "crc_enforcement_failure", key_signals: ["Inapplication systémique en Inde — le Prohibition of Child Marriage Act 2006 reste inappliqué dans 80% des districts ruraux, avec 23% des filles toujours mariées avant 18 ans selon NFHS-5, particulièrement chez les Dalits", "Intersection caste-genre — les filles Dalit rurales subissent mariage précoce à taux disproportionné, combinant discrimination de caste et de genre, créant double vulnérabilité aux droits humains fondamentaux", "Exiger l'application effective du PCMA 2006 via quotas de poursuites judiciaires par district et intégrer les programmes de prévention mariage précoce dans les plans de développement des Panchayats"], estimated_child_marriage_forced_union_rights_index: 5.48, last_updated: "2026-06-21" },
    { entity_id: "CM-006", name: "Brésil/Nordeste — 26% Mariages Enfants & Autorisation Judiciaire Sans Limite Âge", country: "Amérique du Sud", sector: "26% Mariages Enfants Nordeste Brésil, Code Civil Autorisation Judiciaire Sans Âge Minimum, Mariage Évite Stigma Grossesse Adolescente & Classes Rurales Pauvres", composite_score: 48.6, child_marriage_prevalence_score: 50.0, forced_union_coercion_score: 45.0, legal_age_gap_score: 55.0, crc_enforcement_failure_score: 45.0, risk_level: "élevé", primary_pattern: "legal_age_gap", key_signals: ["Lacune légale brésilienne — le Code Civil permet autorisation judiciaire de mariage sans âge minimum, utilisée pour 'légaliser' mariages précoces dans le Nordeste rural où 26% des unions impliquent des mineurs", "Stigma grossesse adolescente comme moteur — les familles brésiliennes recourent au mariage précoce pour éviter la stigmatisation sociale de la grossesse hors mariage, créant un paradoxe où la grossesse adolescente cause plus de mariages d'enfants", "Réformer le Code Civil brésilien pour établir 16 ans absolus comme âge minimum et remplacer l'autorisation judiciaire par des services de soutien aux adolescentes enceintes"], estimated_child_marriage_forced_union_rights_index: 4.86, last_updated: "2026-06-21" },
    { entity_id: "CM-007", name: "ONG Girls Not Brides — Alliance 1500 Organisations & Engagement ODD 5.3", country: "Global", composite_score: 22.4, child_marriage_prevalence_score: 22.0, forced_union_coercion_score: 20.0, legal_age_gap_score: 25.0, crc_enforcement_failure_score: 22.0, risk_level: "modéré", primary_pattern: "crc_enforcement_failure", key_signals: ["Girls Not Brides comme modèle de coordination globale — alliance de 1500 organisations dans 100 pays coordonnant l'engagement ODD 5.3 (éliminer mariage précoce d'ici 2030), représentant la société civile la plus large sur cet enjeu", "Lacunes de financement — malgré l'ampleur du problème (650 millions de femmes mariées enfants), le financement mondial reste insuffisant par rapport à d'autres enjeux de droits humains, limitant les programmes de terrain", "Doubler les contributions des gouvernements du G7 à Girls Not Brides et aux programmes UNFPA/UNICEF d'élimination du mariage précoce pour atteindre ODD 5.3"], estimated_child_marriage_forced_union_rights_index: 2.24, last_updated: "2026-06-21" },
    { entity_id: "CM-008", name: "UNICEF/ONU Femmes — CRC Art.16, CEDAW Art.16 & Cadre Juridique International Protection", country: "Global", composite_score: 4.63, child_marriage_prevalence_score: 5.0, forced_union_coercion_score: 4.0, legal_age_gap_score: 5.0, crc_enforcement_failure_score: 4.5, risk_level: "faible", primary_pattern: "crc_enforcement_failure", key_signals: ["UNICEF/ONU Femmes comme gardiens des standards — CRC Article 16 et CEDAW Article 16 établissent le consentement libre, entier et plein comme droit fondamental au mariage, créant obligations contraignantes pour 190+ États parties", "Recommandation générale CEDAW N°29 — interprétation du Comité CEDAW exigeant l'âge minimum de 18 ans sans exceptions et engagement actif des États à transformer normes culturelles perpétuant mariage précoce", "Renforcer les mécanismes de reporting CEDAW et CRC pour exiger des États des plans d'action chiffrés avec délais précis sur élimination mariage précoce et sanctions pour non-conformité"], estimated_child_marriage_forced_union_rights_index: 0.46, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/child-marriage-forced-union-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
