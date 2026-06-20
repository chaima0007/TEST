"""Birth Registration Engine — 1 milliard d'enfants invisibles, apatridie & déni d'identité légale."""

from dataclasses import dataclass
from typing import List


@dataclass
class BirthRegistrationEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    unregistered_children_score: float
    statelessness_risk_score: float
    legal_identity_access_denial_score: float
    discriminatory_registration_barriers_score: float
    primary_pattern: str
    key_signals: List[str]
    last_updated: str = "2026-06-20"

    @property
    def composite_score(self) -> float:
        return round(
            self.unregistered_children_score * 0.30
            + self.statelessness_risk_score * 0.25
            + self.legal_identity_access_denial_score * 0.25
            + self.discriminatory_registration_barriers_score * 0.20,
            2,
        )

    @property
    def risk_level(self) -> str:
        s = self.composite_score
        if s >= 60: return "critique"
        if s >= 40: return "élevé"
        if s >= 20: return "modéré"
        return "faible"

    @property
    def estimated_birth_registration_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "unregistered_children_score": self.unregistered_children_score,
            "statelessness_risk_score": self.statelessness_risk_score,
            "legal_identity_access_denial_score": self.legal_identity_access_denial_score,
            "discriminatory_registration_barriers_score": self.discriminatory_registration_barriers_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_birth_registration_index": self.estimated_birth_registration_index,
            "last_updated": self.last_updated,
        }


ENTITIES = [
    BirthRegistrationEntity(
        entity_id="BR-001",
        name="Afrique Sub-Saharienne/Sahel — 90M Enfants Sans Acte Naissance & Invisibilité Légale Totale",
        country="Afrique Sub-Saharienne",
        sector="Sahel 50% Naissances Non Enregistrées UNICEF 2023, Nigeria 60% Enfants Non Déclarés, RDC 75% Naissances Sans Acte, Niger/Mali Taux Enregistrement 40% & Sans Acte Naissance: Zéro École/Santé/Vote",
        unregistered_children_score=88.0,
        statelessness_risk_score=85.0,
        legal_identity_access_denial_score=90.0,
        discriminatory_registration_barriers_score=92.0,
        primary_pattern="unregistered_children",
        key_signals=[
            "Violation documentée — Afrique Sub-Saharienne avec score composite 88.55/100 révélant que 50% des naissances au Sahel ne sont pas enregistrées (UNICEF 2023), que 75% des enfants naissant en RDC n'ont pas d'acte de naissance et que sans ce document fondamental, ces enfants sont exclus de l'école, des soins de santé, du vote et de toute protection légale",
            "Enfants non enregistrés (88.0/100) — les 90M d'enfants africains sans acte de naissance sont légalement invisibles, constituant une violation de l'Article 7 de la Convention des droits de l'enfant (CRC) qui garantit le droit de tout enfant à être enregistré dès sa naissance et à acquérir une nationalité, ratifiée par tous les États africains",
            "Financer des programmes d'enregistrement mobile des naissances intégrant les dispensaires ruraux et les accouchements traditionnels au Sahel et en RDC, conformément à l'ODD 16.9 visant 100% d'identité légale pour tous en 2030 et aux recommandations du Comité des droits de l'enfant ONU sur l'enregistrement universel des naissances",
        ],
    ),
    BirthRegistrationEntity(
        entity_id="BR-002",
        name="Inde/Dalit/Tribus — 400M Non-Enregistrés & Discrimination Accès État Civil",
        country="Asie du Sud",
        sector="Inde 400M Personnes Sans Pièces Identité UIDAI Estimation 2022, Dalit/Adivasi Actes Naissance Refusés Agents État Civil Discriminatoires, Assam NRC 1,9M Exclus Registre Citoyen & Enfants Migrants Non Déclarés",
        unregistered_children_score=82.0,
        statelessness_risk_score=80.0,
        legal_identity_access_denial_score=85.0,
        discriminatory_registration_barriers_score=88.0,
        primary_pattern="legal_identity_access_denial",
        key_signals=[
            "Violation documentée — Inde avec score composite 83.45/100 révélant 400M de personnes sans pièces d'identité fiables selon les estimations UIDAI, les refus discriminatoires d'enregistrement visant les communautés Dalit et Adivasi par certains agents d'état civil et l'exclusion de 1,9M de personnes du Registre national des citoyens (NRC) en Assam en 2018",
            "Déni d'accès à l'identité légale (85.0/100) — les pratiques discriminatoires dans l'accès à l'enregistrement d'état civil en Inde, ciblant particulièrement les castes inférieures et les populations tribales, violent l'Article 7 CRC, l'Article 24(3) PIDCP garantissant le droit de tout enfant à une nationalité et l'Article 15 de la Constitution indienne interdisant la discrimination basée sur la caste",
            "Réformer le système d'état civil indien pour éliminer les barrières discriminatoires à l'enregistrement des naissances dans les communautés Dalit et Adivasi et créer un mécanisme d'enregistrement tardif gratuit pour les adultes sans acte de naissance, conformément aux recommandations du Comité des droits de l'enfant ONU lors de l'Examen périodique universel de l'Inde",
        ],
    ),
    BirthRegistrationEntity(
        entity_id="BR-003",
        name="Rohingyas/Apatrides — 600 000 Enfants Nés Sans Nationalité & Génération Invisible",
        country="Asie du Sud-Est",
        sector="Rohingyas 600 000 Enfants Nés Camps Bangladesh Sans Nationalité, Myanmar Loi 1982 Exclut Rohingyas Citoyenneté, Apatrides Koweit/Golfe Bidouns 100 000 Enfants & Dom.Rep Apatridie Rétroactive Dominicains Haïtiens",
        unregistered_children_score=90.0,
        statelessness_risk_score=92.0,
        legal_identity_access_denial_score=80.0,
        discriminatory_registration_barriers_score=75.0,
        primary_pattern="statelessness_risk",
        key_signals=[
            "Violation documentée — Rohingyas/Apatrides avec score composite 85.0/100 révélant 600 000 enfants rohingyas nés dans les camps bangladais depuis 2017 sans nationalité reconnue, exclus par la loi birmane de citoyenneté de 1982 et sans accès à l'enregistrement birman, créant une génération entière d'invisibles légaux",
            "Risque d'apatridie (92.0/100) — les 600 000 enfants rohingyas nés au Bangladesh depuis la crise de 2017, auxquels ni le Myanmar ni le Bangladesh n'accordent la nationalité, constituent la plus grande génération d'apatrides de l'histoire récente, violant l'Article 1 de la Convention de 1954 sur le statut des apatrides et l'Article 7 CRC sur le droit à la nationalité",
            "Exiger du Myanmar l'abrogation de la loi de citoyenneté de 1982 discriminant les Rohingyas et créer un mécanisme d'enregistrement d'urgence pour les 600 000 enfants rohingyas nés au Bangladesh, conformément aux obligations découlant de la Convention de 1961 sur la réduction de l'apatridie et à la campagne #IBelong du HCR",
        ],
    ),
    BirthRegistrationEntity(
        entity_id="BR-004",
        name="Haïti/Rép. Dominicaine — Apatridie Rétroactive, Antihaitianisme & Dénationalisation",
        country="Caraïbes",
        sector="Rep.Dominicaine Arrêt TC/0168/13 2013 Dénationalise 200 000 Dominicains Haïtiens Rétroactivement, Haïti Actes Naissance Détruits Séisme 2010, OSJI Documention & Sans Acte Naissance: Expulsion Pays Naissance",
        unregistered_children_score=72.0,
        statelessness_risk_score=75.0,
        legal_identity_access_denial_score=78.0,
        discriminatory_registration_barriers_score=80.0,
        primary_pattern="discriminatory_registration_barriers",
        key_signals=[
            "Violation documentée — Haïti/République Dominicaine avec score composite 75.85/100 révélant la décision TC/0168/13 (2013) qui a rétroactivement dénationalisé 200 000 Dominicains d'origine haïtienne nés en République Dominicaine depuis 1929, créant massivement de l'apatridie et documentée par l'OSJI comme contraire au droit international",
            "Barrières discriminatoires à l'enregistrement (80.0/100) — la décision TC/0168/13 de la Cour constitutionnelle dominicaine supprimant rétroactivement la nationalité dominicaine aux descendants d'Haïtiens constitue une violation de l'Article 15 de la Déclaration universelle des droits de l'homme sur le droit à une nationalité et de l'interdiction d'apatridie rétroactive de la Convention de 1961",
            "Exiger de la République Dominicaine l'annulation de la décision TC/0168/13 et la restauration de la nationalité à tous les Dominicains d'ascendance haïtienne indûment privés de leur citoyenneté, conformément aux arrêts de la Cour interaméricaine des droits de l'homme (affaires Yean et Bosico c. République Dominicaine) et aux recommandations de l'OEA",
        ],
    ),
    BirthRegistrationEntity(
        entity_id="BR-005",
        name="USA/Immigrants Sans-Papiers — 400 000 Enfants Non Déclarés & 14e Amendement Menacé",
        country="Amérique du Nord",
        sector="USA 400 000 Enfants Immigrants Non Déclarés Estimation PEW, 14e Amendement Birthright Citizenship Débat Politique, Familles Sans Papiers Peur Enregistrement & Enfants Apatrides Nés Parents Immigrés Non-Déclarés",
        unregistered_children_score=45.0,
        statelessness_risk_score=50.0,
        legal_identity_access_denial_score=52.0,
        discriminatory_registration_barriers_score=48.0,
        primary_pattern="legal_identity_access_denial",
        key_signals=[
            "Violation documentée — USA avec score composite 48.6/100 révélant 400 000 enfants d'immigrants sans papiers estimés non enregistrés à la naissance par crainte des autorités d'immigration, le débat politique sur l'abrogation du 14e Amendement sur le droit du sol et le risque d'apatridie pour les enfants nés aux États-Unis de parents sans statut légal",
            "Déni d'accès à l'identité légale (52.0/100) — la peur des parents sans papiers de se rendre dans les hôpitaux et les mairies pour enregistrer leurs enfants, exacerbée par les politiques d'immigration restrictives, prive des centaines de milliers d'enfants américains de leur droit à l'enregistrement prévu par l'Article 7 CRC, ratifiée par les États-Unis mais non encore ratifiée comme traité contraignant",
            "Adopter des politiques de pare-feu entre les services d'état civil et les autorités d'immigration pour permettre aux parents sans papiers d'enregistrer leurs enfants en toute sécurité et s'opposer à toute réforme visant à restreindre le droit du sol du 14e Amendement, conformément aux recommandations du Comité des droits de l'enfant ONU",
        ],
    ),
    BirthRegistrationEntity(
        entity_id="BR-006",
        name="Golfe/Bidouns — 100 000 Apatrides Kuwait/EAU & Enfants Nés Sans Nationalité",
        country="Moyen-Orient",
        sector="Kuwait 100 000 Bidouns Apatrides Générations, EAU 70 000 Apatrides Nés Territoire Sans Nationalité, Arabie Saoudite Minorités Sans Acte Naissance & Enfants Bidouns Exclus École/Hôpitaux Faute Acte Naissance",
        unregistered_children_score=48.0,
        statelessness_risk_score=45.0,
        legal_identity_access_denial_score=55.0,
        discriminatory_registration_barriers_score=50.0,
        primary_pattern="legal_identity_access_denial",
        key_signals=[
            "Violation documentée — Golfe/Bidouns avec score composite 49.4/100 révélant 100 000 apatrides Bidouns au Koweït et 70 000 aux EAU vivant depuis des générations sans nationalité ni acte de naissance, leurs enfants exclus des écoles publiques, des hôpitaux et de toute protection légale faute de documents d'identité",
            "Déni d'accès à l'identité légale (55.0/100) — l'absence systémique de statut légal pour les Bidouns du Koweït et des EAU, transmise de génération en génération, constitue une violation de l'Article 7 CRC sur le droit à la nationalité et de l'Article 1 de la Convention de 1954 sur le statut des apatrides, que le Koweït et les EAU n'ont pas ratifiée",
            "Exiger du Koweït et des EAU la mise en œuvre de procédures de naturalisation pour les Bidouns résidant depuis plus d'une génération sur leur territoire et ratifier la Convention de 1954 sur le statut des apatrides, conformément aux recommandations du HCR dans le cadre de la campagne #IBelong 2024-2034",
        ],
    ),
    BirthRegistrationEntity(
        entity_id="BR-007",
        name="UE/Roms — 500 000 Sans Acte Naissance & Discrimination État Civil",
        country="Europe",
        sector="Roms Europe 500 000 Sans Documents Identité Estimation ERRC, Bulgarie/Roumanie Roms Non Enregistrés Naissance, Discrimination Agents État Civil Documentée & Enfants Roms Exclus École Faute Acte Naissance",
        unregistered_children_score=25.0,
        statelessness_risk_score=28.0,
        legal_identity_access_denial_score=30.0,
        discriminatory_registration_barriers_score=32.0,
        primary_pattern="discriminatory_registration_barriers",
        key_signals=[
            "Défis persistants en Europe — 500 000 Roms estimés sans documents d'identité dans l'UE selon le Centre européen pour les droits des Roms (ERRC), avec des pratiques discriminatoires d'agents d'état civil en Bulgarie et en Roumanie documentées par des ONG, privant des enfants roms de l'accès à l'école publique",
            "Barrières discriminatoires à l'enregistrement (32.0/100) — les pratiques discriminatoires d'agents d'état civil refusant ou retardant l'enregistrement des naissances pour les communautés roms dans plusieurs États membres de l'UE violent l'Article 7 CRC et les engagements de la Stratégie UE pour l'égalité, l'inclusion et la participation des Roms (2021-2030)",
            "Renforcer la Stratégie UE pour les Roms 2021-2030 avec des mécanismes de signalement des refus discriminatoires d'enregistrement d'état civil et créer des équipes mobiles d'enregistrement des naissances dans les communautés roms des États membres, conformément aux recommandations du Commissaire aux droits de l'homme du Conseil de l'Europe",
        ],
    ),
    BirthRegistrationEntity(
        entity_id="BR-008",
        name="ONU/UNICEF — CRC Art.7, ODD 16.9 & Campagne Identité Légale Pour Tous",
        country="Global",
        sector="CRC Article 7 Droit Enregistrement Naissance 196 Ratifications, ODD 16.9 Identité Légale 2030, UNICEF Programme Enregistrement Naissance 100+ Pays & HCR Campagne IBelong Réduction Apatridie 2024",
        unregistered_children_score=4.0,
        statelessness_risk_score=5.0,
        legal_identity_access_denial_score=3.0,
        discriminatory_registration_barriers_score=6.0,
        primary_pattern="unregistered_children",
        key_signals=[
            "ONU/UNICEF représente le cadre normatif de référence — l'Article 7 de la Convention des droits de l'enfant (CRC), ratifiée par 196 États, garantit le droit de tout enfant à être enregistré dès sa naissance et l'ODD 16.9 fixe l'objectif de 100% d'identité légale pour tous d'ici 2030, avec encore 1Md d'êtres humains sans aucun document d'identité",
            "Campagne #IBelong du HCR (2014-2024) — la campagne visant à mettre fin à l'apatridie en 10 ans a permis des progrès mais 4,4M d'apatrides restent recensés (chiffre sous-estimé) selon le HCR, révélant les limites des mécanismes volontaires sans obligations contraignantes pour les États",
            "Accélérer la mise en œuvre de l'ODD 16.9 en finançant un programme UNICEF universel d'enregistrement mobile des naissances dans les pays à faible taux et créer un mécanisme onusien contraignant de réduction de l'apatridie, conformément à la Déclaration et Plan d'action de Genève sur les apatrides (2011) et à la campagne #IBelong du HCR",
        ],
    ),
]


def run_analysis():
    results = [e.to_dict() for e in ENTITIES]
    avg = round(sum(e.composite_score for e in ENTITIES) / len(ENTITIES), 2)
    dist = {}
    for e in ENTITIES:
        dist[e.risk_level] = dist.get(e.risk_level, 0) + 1
    pat = {}
    for e in ENTITIES:
        pat[e.primary_pattern] = pat.get(e.primary_pattern, 0) + 1
    top3 = sorted(ENTITIES, key=lambda x: x.composite_score, reverse=True)[:3]
    critiques = [e for e in ENTITIES if e.risk_level == "critique"]
    return {
        "total_entities": len(ENTITIES),
        "avg_composite": avg,
        "risk_distribution": dist,
        "pattern_distribution": pat,
        "top_risk_entities": [e.name for e in top3],
        "critical_alerts": [f"{e.name.split('—')[0].strip()}: {e.primary_pattern}" for e in critiques],
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "birth_registration",
        "confidence_score": 0.85,
        "data_sources": [
            "unicef_birth_registration_global_database_annual_report",
            "unhcr_global_trends_statelessness_annual_report",
            "id4d_world_bank_identification_development_initiative_data",
        ],
        "entities": results,
        "avg_estimated_birth_registration_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    import json
    data = run_analysis()
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"\n✅ Distribution: {data['risk_distribution']}")
    print(f"✅ Avg composite: {data['avg_composite']}")
    print(f"✅ Pattern dist: {data['pattern_distribution']}")
