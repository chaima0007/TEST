import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[gender-based-violence-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Gender Based Violence Engine Agent",
  domain: "gender_based_violence",
  total_entities: 8,
  avg_composite: 61.02,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { physical_sexual_violence: 3, legal_impunity_perpetrators: 2, institutional_response_failure: 2, structural_systemic_discrimination: 1 },
  top_risk_entities: [
    "Afghanistan/Talibans — Interdiction Éducation Filles, Mariage Forcé & Violence Conjugale Légalisée",
    "RDC/Conflits Armés — Viol Arme de Guerre, 400 000 Viols/An & Impunité Totale",
    "Yémen/Soudan — VBG en Conflits, Femmes Déplacées & Violences Sexuelles Soldats",
  ],
  critical_alerts: [
    "Afghanistan/Talibans: physical_sexual_violence",
    "RDC/Conflits Armés: physical_sexual_violence",
    "Inde/Asie du Sud: legal_impunity_perpetrators",
    "Yémen/Soudan: physical_sexual_violence",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_gender_based_violence_index: 6.10,
  data_sources: [
    "un_women_global_database_violence_against_women",
    "who_global_status_report_violence_prevention",
    "un_special_rapporteur_violence_against_women_country_reports",
  ],
  entities: [
    {
      entity_id: "GBV-001",
      name: "Afghanistan/Talibans — Interdiction Éducation Filles, Mariage Forcé & Violence Conjugale Légalisée",
      country: "Asie Centrale",
      sector: "Afghanistan Talibans Femmes Interdites Éducation/Travail 2021, Mariage Forcé Filles Dès 9 Ans Légal, Code Moral Taliban Violence Conjugale Non Criminalisée & 4M Filles Hors École",
      composite_score: 95.55,
      physical_sexual_violence_score: 98.0,
      legal_impunity_perpetrators_score: 95.0,
      institutional_response_failure_score: 96.0,
      structural_systemic_discrimination_score: 92.0,
      risk_level: "critique",
      primary_pattern: "physical_sexual_violence",
      estimated_gender_based_violence_index: 9.56,
      last_updated: "2026-06-20",
      key_signals: [
        "Violation grave des droits des femmes documentée — Afghanistan avec score composite 95.55/100 révélant l'interdiction totale de l'éducation des filles depuis 2021, la légalisation du mariage forcé dès 9 ans par le code moral taliban, 4M de filles hors école et la non-criminalisation de la violence conjugale constituant un apartheid de genre",
        "Violence physique/sexuelle (98.0/100) — l'interdiction par les talibans de l'éducation, du travail et de la liberté de mouvement des femmes afghanes, combinée à la légalisation des mariages précoces et forcés, constitue un système d'apartheid de genre violant la CEDAW (ratifiée par l'Afghanistan en 2003) et l'Article 5 de la Déclaration sur l'élimination de la violence contre les femmes",
        "Activer la procédure de l'Article 29 CEDAW pour violations systémiques par l'Afghanistan et sanctionner les talibans via le Conseil de sécurité ONU pour apartheid de genre, conformément à la résolution 2404 (2018) et aux recommandations du Rapporteur Spécial ONU sur les droits des femmes en Afghanistan",
      ],
    },
    {
      entity_id: "GBV-002",
      name: "RDC/Conflits Armés — Viol Arme de Guerre, 400 000 Viols/An & Impunité Totale",
      country: "Afrique Sub-Saharienne",
      sector: "RDC 400 000 Viols/An Est Congo OMS 2011, Milices M23/FDLR Viols Systématiques, Mukwege Nobel Panzi Hospital 85 000 Survivantes & Impunité 90% Auteurs Jamais Poursuivis",
      composite_score: 89.10,
      physical_sexual_violence_score: 92.0,
      legal_impunity_perpetrators_score: 88.0,
      institutional_response_failure_score: 90.0,
      structural_systemic_discrimination_score: 85.0,
      risk_level: "critique",
      primary_pattern: "physical_sexual_violence",
      estimated_gender_based_violence_index: 8.91,
      last_updated: "2026-06-20",
      key_signals: [
        "Violation documentée — RDC avec score composite 89.1/100 révélant 400 000 viols annuels selon l'OMS dans l'Est du Congo, les viols systématiques comme arme de guerre par les milices M23 et FDLR documentés par la MONUSCO et 90% d'impunité pour les auteurs malgré le travail du Dr Mukwege (Nobel 2018) à l'hôpital Panzi",
        "Violence physique/sexuelle (92.0/100) — l'utilisation systématique du viol comme arme de guerre dans l'Est de la RDC par les milices armées constitue un crime contre l'humanité selon l'Article 7 du Statut de Rome et les Résolutions du CSNU 1820 (2008) et 1888 (2009) sur les violences sexuelles dans les conflits",
        "Activer la compétence de la CPI pour les viols systématiques comme crimes contre l'humanité en RDC et financer le Fonds en faveur des victimes de la CPI pour les survivantes de l'hôpital Panzi, conformément à la résolution 1888 du CSNU et aux recommandations de l'Experte ONU des Nations Unies sur les violences sexuelles dans les conflits",
      ],
    },
    {
      entity_id: "GBV-003",
      name: "Inde/Asie du Sud — Féminicides, Dots, Crimes Honneur & 7 000 Meurtres Dots/An",
      country: "Asie du Sud",
      sector: "Inde 7000 Meurtres Liés Dot NCRB 2023, Crimes Honneur Pakistan/Bangladesh, Infanticide Féminin 50M Femmes Manquantes Démographie Asie & Acide Attacks 1500/An Bangladesh/Inde",
      composite_score: 81.75,
      physical_sexual_violence_score: 72.0,
      legal_impunity_perpetrators_score: 90.0,
      institutional_response_failure_score: 85.0,
      structural_systemic_discrimination_score: 82.0,
      risk_level: "critique",
      primary_pattern: "legal_impunity_perpetrators",
      estimated_gender_based_violence_index: 8.18,
      last_updated: "2026-06-20",
      key_signals: [
        "Violation documentée — Inde/Asie du Sud avec score composite 81.75/100 révélant 7 000 meurtres liés à la dot par an en Inde (NCRB 2023), les crimes d'honneur au Pakistan et au Bangladesh, 50M de femmes démographiquement manquantes en Asie révélant le féminicide systémique et 1 500 attaques à l'acide annuelles au Bangladesh et en Inde",
        "Impunité légale des auteurs (90.0/100) — les 7 000 meurtres liés à la dot annuels en Inde avec un faible taux de condamnation, les crimes d'honneur au Pakistan et au Bangladesh rarement poursuivis et les 50M de femmes manquantes révèlent un système d'impunité institutionnalisée pour les violences basées sur le genre, violant l'Article 2 CEDAW sur l'obligation d'éliminer la discrimination",
        "Réformer en profondeur les lois anti-dot indiennes (Dowry Prohibition Act) pour criminaliser effectivement les meurtres liés à la dot avec des peines minimales et créer des tribunaux spécialisés violences domestiques dans les 28 États indiens, conformément aux recommandations du Comité CEDAW et aux résolutions ONU sur les crimes contre les femmes",
      ],
    },
    {
      entity_id: "GBV-004",
      name: "Yémen/Soudan — VBG en Conflits, Femmes Déplacées & Violences Sexuelles Soldats",
      country: "MENA/Afrique",
      sector: "Yémen Mariage Enfants 66% Filles Avant 18 Ans, Soudan RSF Violences Sexuelles Systématiques 2023 Darfour, 4M PDI Yémen Femmes Vulnérables & Filles Hors École Zones Conflit",
      composite_score: 84.15,
      physical_sexual_violence_score: 88.0,
      legal_impunity_perpetrators_score: 82.0,
      institutional_response_failure_score: 85.0,
      structural_systemic_discrimination_score: 80.0,
      risk_level: "critique",
      primary_pattern: "physical_sexual_violence",
      estimated_gender_based_violence_index: 8.42,
      last_updated: "2026-06-20",
      key_signals: [
        "Violation documentée — Yémen/Soudan avec score composite 84.15/100 révélant 66% de mariages précoces des filles avant 18 ans au Yémen, les violences sexuelles systématiques des RSF au Darfour en 2023 documentées par l'ONU et 4M de femmes déplacées au Yémen exposées à des violences dans les camps sans protection adéquate",
        "Violence physique/sexuelle (88.0/100) — les violences sexuelles systématiques commises par les Forces de soutien rapide (RSF) au Soudan en 2023 documentées par la Mission d'enquête ONU constituent des crimes contre l'humanité selon l'Article 7 du Statut de Rome et les résolutions 1820 et 1888 du CSNU sur les violences sexuelles dans les conflits",
        "Déployer d'urgence des équipes ONU Women dans les camps de déplacés au Yémen et au Soudan pour documenter et prévenir les violences sexuelles et activer le mécanisme de la résolution 1888 du CSNU avec une Représentante spéciale sur les violences sexuelles dans les conflits disposant de ressources suffisantes",
      ],
    },
    {
      entity_id: "GBV-005",
      name: "USA — Violences Domestiques, Inégalités Raciales & Recul Droits Reproductifs",
      country: "Amérique du Nord",
      sector: "USA 1/4 Femmes Victimes Violences Conjugales CDC, Arrêt Dobbs 2022 Avortement Interdit 13 États, Femmes Noires 3x Plus à Risque Mort Maternelle & 10M Dossiers Violence Domestique/An FBI",
      composite_score: 52.60,
      physical_sexual_violence_score: 45.0,
      legal_impunity_perpetrators_score: 50.0,
      institutional_response_failure_score: 60.0,
      structural_systemic_discrimination_score: 58.0,
      risk_level: "élevé",
      primary_pattern: "institutional_response_failure",
      estimated_gender_based_violence_index: 5.26,
      last_updated: "2026-06-20",
      key_signals: [
        "Violations documentées aux USA — score composite 52.6/100 révélant 1/4 des femmes victimes de violences conjugales (CDC), l'arrêt Dobbs (2022) interdisant l'avortement dans 13 États, les femmes noires 3x plus exposées à la mortalité maternelle et 10M de dossiers de violence domestique traités par le FBI annuellement",
        "Échec institutionnel (60.0/100) — les disparités raciales dans la réponse aux violences domestiques aux USA, avec les femmes afro-américaines et autochtones disproportionnellement victimes et moins protégées par le système judiciaire, révèlent une violation de l'Article 2(d) CEDAW sur l'obligation d'éliminer la discrimination dans les institutions publiques",
        "Réautoriser le Violence Against Women Act avec des financements accrus pour les refuges et services aux survivantes et adopter des politiques de réduction des inégalités raciales dans les réponses aux violences domestiques conformément aux recommandations du Comité CEDAW et à la Déclaration de Beijing+30 sur l'élimination de la violence contre les femmes",
      ],
    },
    {
      entity_id: "GBV-006",
      name: "Mexique/Amérique Latine — Féminicides 10/Jour, Búsqueda & Impunité 99%",
      country: "Amérique Latine",
      sector: "Mexique 10 Féminicides/Jour SESNSP 2023, Búsqueda Mexique Collectifs Femmes Cherchant Disparues, Impunité 99% Féminicides Non Résolus, Guatemala 98% Impunité & Argentine Mouvement Ni Una Menos",
      composite_score: 53.00,
      physical_sexual_violence_score: 45.0,
      legal_impunity_perpetrators_score: 50.0,
      institutional_response_failure_score: 48.0,
      structural_systemic_discrimination_score: 75.0,
      risk_level: "élevé",
      primary_pattern: "structural_systemic_discrimination",
      estimated_gender_based_violence_index: 5.30,
      last_updated: "2026-06-20",
      key_signals: [
        "Violations documentées au Mexique/Amérique Latine — score composite 53.0/100 révélant 10 féminicides par jour au Mexique (SESNSP 2023), 99% d'impunité pour les féminicides non résolus, les collectifs Búsqueda de familles cherchant leurs disparues et 98% d'impunité au Guatemala pour les crimes contre les femmes",
        "Discrimination systémique structurelle (75.0/100) — les 10 féminicides quotidiens au Mexique avec 99% d'impunité révèlent une normalisation sociale et institutionnelle de la violence contre les femmes, violant l'obligation mexicaine d'éliminer la violence en vertu de la Convention de Belém do Pará (1994) et de l'Article 7(b) exigeant d'agir avec la diligence voulue",
        "Mettre en œuvre intégralement la loi mexicaine Alerta de Violencia de Género et créer un mécanisme régional latino-américain de suivi des féminicides conforme à la Convention de Belém do Pará et aux recommandations du Comité CEDAW adressées au Mexique lors de sa session de 2018",
      ],
    },
    {
      entity_id: "GBV-007",
      name: "UE/CEDAW — Directive Violence Femmes, Istanbul & Lacunes États Membres",
      country: "Europe",
      sector: "UE Directive Violence Faite aux Femmes 2024 Adoptée, Convention Istanbul 46 États, 1/3 Femmes UE Victimes Violences Physiques/Sexuelles Vie & Lacunes Mise En Oeuvre Pologne/Hongrie",
      composite_score: 27.60,
      physical_sexual_violence_score: 22.0,
      legal_impunity_perpetrators_score: 32.0,
      institutional_response_failure_score: 28.0,
      structural_systemic_discrimination_score: 30.0,
      risk_level: "modéré",
      primary_pattern: "legal_impunity_perpetrators",
      estimated_gender_based_violence_index: 2.76,
      last_updated: "2026-06-20",
      key_signals: [
        "Défis persistants en Europe — 1/3 des femmes européennes victimes de violences physiques ou sexuelles au cours de leur vie (FRA 2014), les lacunes dans la mise en œuvre de la Convention d'Istanbul dans certains États membres et les reculs en Pologne et en Hongrie révèlent des vulnérabilités persistantes",
        "Impunité persistante (32.0/100) — malgré le cadre légal européen (Directive 2024, Convention Istanbul), les taux de condamnation pour violences sexuelles restent faibles dans plusieurs États membres, révélant des lacunes dans l'application de l'obligation de poursuivre les auteurs prévue par l'Article 7 de la Directive UE sur la violence à l'égard des femmes",
        "Accélérer la transposition de la Directive UE 2024 sur la violence faite aux femmes dans tous les États membres et renforcer le mécanisme de suivi de la Convention d'Istanbul avec des visites pays obligatoires, conformément aux recommandations du GREVIO (Groupe d'experts sur la lutte contre la violence à l'égard des femmes)",
      ],
    },
    {
      entity_id: "GBV-008",
      name: "ONU/CEDAW — Convention Droits Femmes, Rapporteur Spécial & Pékin+30",
      country: "Global",
      sector: "CEDAW Convention Droits Femmes 189 Ratifications 1979, Rapporteur Spécial VBG ONU, Plateforme Action Beijing 1995 +30 Ans Révision 2025 & ONU Women Mécanisme Intergouvernemental",
      composite_score: 4.40,
      physical_sexual_violence_score: 4.0,
      legal_impunity_perpetrators_score: 3.0,
      institutional_response_failure_score: 5.0,
      structural_systemic_discrimination_score: 6.0,
      risk_level: "faible",
      primary_pattern: "structural_systemic_discrimination",
      estimated_gender_based_violence_index: 0.44,
      last_updated: "2026-06-20",
      key_signals: [
        "ONU/CEDAW représente le cadre normatif de référence — la CEDAW (1979) ratifiée par 189 États constitue la charte internationale des droits des femmes et son Protocole facultatif (1999) permet les plaintes individuelles pour violations du droit à l'égalité et à la protection contre la violence basée sur le genre",
        "Rapporteur Spécial ONU sur les violences contre les femmes — depuis 1994, ce mécanisme documente les violations systémiques dans 190 pays, soumet des rapports aux pays visités et contribue à développer les standards internationaux sur la violence basée sur le genre, l'autonomie des femmes et la responsabilité des États",
        "Beijing+30 (2025) — la révision de la Plateforme d'action de Beijing constitue l'occasion de renforcer les engagements mondiaux sur l'élimination de la violence basée sur le genre avec des mécanismes de suivi contraignants, conformément aux ODD 5 (égalité des sexes) et 16 (justice et institutions efficaces)",
      ],
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/gender-based-violence-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
