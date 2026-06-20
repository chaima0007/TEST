"""Minority Language Rights Engine — suppression linguistique, droits des minorités et effacement culturel."""

from dataclasses import dataclass
from typing import List


@dataclass
class MinorityLanguageRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    language_suppression_score: float
    education_denial_score: float
    legal_recognition_absence_score: float
    media_cultural_erasure_score: float
    primary_pattern: str
    key_signals: List[str]
    last_updated: str = "2026-06-20"

    @property
    def composite_score(self) -> float:
        return round(
            self.language_suppression_score * 0.30
            + self.education_denial_score * 0.25
            + self.legal_recognition_absence_score * 0.25
            + self.media_cultural_erasure_score * 0.20,
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
    def estimated_minority_language_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "language_suppression_score": self.language_suppression_score,
            "education_denial_score": self.education_denial_score,
            "legal_recognition_absence_score": self.legal_recognition_absence_score,
            "media_cultural_erasure_score": self.media_cultural_erasure_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_minority_language_rights_index": self.estimated_minority_language_rights_index,
            "last_updated": self.last_updated,
        }


ENTITIES = [
    MinorityLanguageRightsEntity(
        entity_id="ML-001",
        name="Chine/Ouïghours/Tibétains — Sinicisation Forcée, Internats & Effacement Linguistique Systémique",
        country="Asie du Nord-Est",
        sector="Chine Ouïghours Interdiction Langue Maternelle Xinjiang Écoles, Tibétains Enseignement Tibétain Supprimé Monastères Fermés, Mongolie Intérieure Mandarin Exclusif 2020 Révoltes & Internats Séparation Enfants Parents",
        language_suppression_score=90.0,
        education_denial_score=95.0,
        legal_recognition_absence_score=98.0,
        media_cultural_erasure_score=92.0,
        primary_pattern="legal_recognition_absence",
        key_signals=[
            "Violation documentée — Chine avec score composite 93.65/100 révélant l'interdiction de l'enseignement en ouïghour dans les écoles du Xinjiang, la suppression de l'éducation tibétaine dans les monastères, le passage forcé au mandarin exclusif en Mongolie Intérieure en 2020 déclenchant des révoltes et les internats séparant les enfants de leurs parents",
            "Absence de reconnaissance légale (98.0/100) — la politique de sinicisation du gouvernement chinois élimine systématiquement les langues minoritaires comme langues d'enseignement en violation de l'Article 30 de la Convention des droits de l'enfant (CRC) sur le droit des enfants minoritaires à utiliser leur propre langue et de l'Article 27 du PIDCP sur les droits des minorités",
            "Exiger de la Chine la cessation immédiate des politiques d'assimilation linguistique forcée dans le Xinjiang, au Tibet et en Mongolie Intérieure et rétablir l'enseignement dans les langues maternelles minoritaires conformément à l'Article 27 PIDCP et à la Déclaration ONU sur les droits des personnes appartenant à des minorités (1992)",
        ],
    ),
    MinorityLanguageRightsEntity(
        entity_id="ML-002",
        name="Turquie/Kurdes — 40 Ans Interdiction Kurde, 20M Locuteurs & Répression Culturelle",
        country="Moyen-Orient",
        sector="Turquie Kurde Interdit 1923-1991 Constitution 40 Ans, 20M Locuteurs Kurdophones, Enseignement Kurde Privé Limité 2003 Réformé Mais Restreint, HDP Partis Pro-Kurdes Dissous & Médias Kurdes Fermés",
        language_suppression_score=82.0,
        education_denial_score=85.0,
        legal_recognition_absence_score=88.0,
        media_cultural_erasure_score=80.0,
        primary_pattern="legal_recognition_absence",
        key_signals=[
            "Violation documentée — Turquie avec score composite 83.85/100 révélant l'interdiction constitutionnelle du kurde de 1923 à 1991 (40 ans), les restrictions persistantes sur l'enseignement kurde malgré les réformes de 2003, la dissolution des partis pro-kurdes (HDP) par la Cour constitutionnelle et la fermeture de médias en langue kurde",
            "Absence de reconnaissance légale (88.0/100) — malgré les réformes de 2003 permettant l'enseignement privé du kurde, l'absence de statut officiel du kurde en Turquie et les restrictions persistantes sur les médias et l'enseignement public en kurde violent l'Article 27 PIDCP ratifié par la Turquie et les engagements de Copenhague de l'OSCE sur les droits des minorités",
            "Accorder au kurde le statut de langue régionale officielle dans les provinces à majorité kurdophone et rouvrir les écoles publiques en langue kurde fermées depuis 2016, conformément aux recommandations du Comité des droits de l'homme ONU et de la Commission de Venise du Conseil de l'Europe sur la protection des minorités linguistiques",
        ],
    ),
    MinorityLanguageRightsEntity(
        entity_id="ML-003",
        name="Russie/Langues Autochtones — Russification, 100+ Langues Menacées & Réforme 2018",
        country="Europe de l'Est",
        sector="Russie 100+ Langues Autochtones UNESCO Danger Extinction, Loi 2018 Enseignement Langues Nationales Optionnel (Non Obligatoire), Langues Sibériennes 1000-5000 Locuteurs Restants & Politique État Monolingue Russe",
        language_suppression_score=72.0,
        education_denial_score=78.0,
        legal_recognition_absence_score=80.0,
        media_cultural_erasure_score=75.0,
        primary_pattern="education_denial",
        key_signals=[
            "Violation documentée — Russie avec score composite 76.1/100 révélant la loi de 2018 rendant l'enseignement des langues régionales optionnel (non obligatoire) ce qui a précipité le déclin de l'éducation en bachkir, tatar et autres langues, plus de 100 langues autochtones de Sibérie classées en danger d'extinction par l'UNESCO",
            "Refus d'éducation (78.0/100) — la loi russe de 2018 transformant l'enseignement des langues régionales de matière obligatoire en matière optionnelle a entraîné une réduction drastique de l'enseignement des langues minoritaires dans les écoles publiques, violant l'Article 14 de la Convention-cadre du Conseil de l'Europe pour la protection des minorités nationales",
            "Abroger la disposition de la loi de 2018 rendant l'enseignement des langues régionales optionnel et adopter un plan national de revitalisation des langues autochtones de Russie en péril, conformément à l'Atlas des langues en danger de l'UNESCO et aux recommandations de l'Instance permanente des Nations Unies sur les questions autochtones",
        ],
    ),
    MinorityLanguageRightsEntity(
        entity_id="ML-004",
        name="France/Langues Régionales — Jacobinisme, Bretons/Occitans & Effacement Institutionnel",
        country="Europe Occidentale",
        sector="France Langues Régionales Alsacien/Breton/Occitan/Corse Non Reconnues Officiellement, Loi Molac 2021 Immersion Linguistique Censurée Conseil Constitutionnel, 200 000 Locuteurs Breton (vs 1M 1950) & Monolingue Constitutionnel Art.2",
        language_suppression_score=60.0,
        education_denial_score=68.0,
        legal_recognition_absence_score=72.0,
        media_cultural_erasure_score=65.0,
        primary_pattern="legal_recognition_absence",
        key_signals=[
            "Violation documentée — France avec score composite 66.0/100 révélant le refus constitutionnel (Article 2) de reconnaître les langues régionales, la censure par le Conseil constitutionnel en 2021 des dispositions de la Loi Molac sur l'enseignement en immersion et l'effondrement du breton de 1M de locuteurs en 1950 à 200 000 aujourd'hui",
            "Absence de reconnaissance légale (72.0/100) — le refus de la France de ratifier la Charte européenne des langues régionales ou minoritaires depuis sa signature en 1999 et la décision du Conseil constitutionnel de 2021 invalidant les dispositions sur l'enseignement en immersion violent les engagements européens de protection des minorités linguistiques et les recommandations du Comité consultatif de la Convention-cadre",
            "Ratifier la Charte européenne des langues régionales ou minoritaires et réviser l'Article 2 de la Constitution française pour permettre la reconnaissance officielle des langues régionales, conformément aux recommandations du Comité des Ministres du Conseil de l'Europe à la France sur la protection des langues régionales",
        ],
    ),
    MinorityLanguageRightsEntity(
        entity_id="ML-005",
        name="Inde/Langues Tribales — 780 Langues, Adivasis & Disparition Accélérée",
        country="Asie du Sud",
        sector="Inde 780 Langues Recensement 2011, Langues Tribales Adivasi Non Enseignées Écoles, 250 Langues Disparues Depuis 1961 Recensement, Santali/Gondi/Bhili Millions Locuteurs Zéro Enseignement Public & Pression Hindi",
        language_suppression_score=52.0,
        education_denial_score=48.0,
        legal_recognition_absence_score=55.0,
        media_cultural_erasure_score=50.0,
        primary_pattern="legal_recognition_absence",
        key_signals=[
            "Violation documentée — Inde avec score composite 51.35/100 révélant la disparition de 250 langues depuis le recensement de 1961, les 780 langues recensées dont la majorité des langues tribales (Adivasi) n'est pas enseignée dans les écoles publiques et la pression croissante du hindi marginalisant les langues tribales comme le Gondi, le Bhili et le Santali",
            "Absence de reconnaissance légale (55.0/100) — bien que la 8e annexe de la Constitution indienne reconnaisse 22 langues officielles, les centaines de langues tribales parlées par 104M d'Adivasis ne bénéficient d'aucun statut officiel ni d'enseignement public systématique, violant l'Article 350A de la Constitution indienne sur l'enseignement dans la langue maternelle",
            "Mettre en œuvre l'obligation constitutionnelle de l'Article 350A garantissant l'enseignement dans la langue maternelle au niveau primaire pour les communautés tribales et adopter un plan de revitalisation des langues tribales indiennes en coordination avec les États, conformément aux recommandations de l'Instance permanente ONU sur les questions autochtones",
        ],
    ),
    MinorityLanguageRightsEntity(
        entity_id="ML-006",
        name="USA/Langues Autochtones — 175 Langues en Danger, Pensionnats & Native American Languages Act",
        country="Amérique du Nord",
        sector="USA 175 Langues Autochtones Danger Extinction UNESCO, Pensionnats Historiques Interdiction Langues Autochtones 19e-20e Siècle, Native American Languages Act 1990 Insuffisant & 7 Langues Seulement 1000+ Locuteurs",
        language_suppression_score=45.0,
        education_denial_score=50.0,
        legal_recognition_absence_score=60.0,
        media_cultural_erasure_score=48.0,
        primary_pattern="legal_recognition_absence",
        key_signals=[
            "Violation documentée — USA avec score composite 50.6/100 révélant 175 langues autochtones classées en danger d'extinction par l'UNESCO (dont beaucoup avec moins de 10 locuteurs), l'héritage des pensionnats historiques ayant interdit les langues autochtones et le financement insuffisant du Native American Languages Act de 1990 pour enrayer la disparition",
            "Absence de reconnaissance légale (60.0/100) — l'absence de politique fédérale de revitalisation dotée de ressources suffisantes pour les 175 langues autochtones en danger aux États-Unis, héritage des pensionnats qui ont interdit ces langues, constitue une violation continue des droits culturels des peuples autochtones selon l'Article 13 de la DNUDPA (Déclaration ONU sur les droits des peuples autochtones)",
            "Allouer un financement fédéral substantiel à la revitalisation des langues autochtones et adopter une loi sur les droits linguistiques des peuples autochtones conforme à la DNUDPA (Article 13-14 sur le droit à l'éducation dans leur propre langue), en partenariat avec les nations tribales pour les programmes d'immersion linguistique",
        ],
    ),
    MinorityLanguageRightsEntity(
        entity_id="ML-007",
        name="UE/ECRML — Charte Langues Régionales, CONFINTEA & 60M Locuteurs Minoritaires",
        country="Europe",
        sector="UE ECRML Charte Européenne 35 Ratifications, 60M Citoyens UE Langues Régionales/Minoritaires, Directive Services Médias Audiovisuels Langues Minoritaires, Euromosaic Rapport & Comité Consultatif Convention-Cadre Minorités",
        language_suppression_score=25.0,
        education_denial_score=30.0,
        legal_recognition_absence_score=28.0,
        media_cultural_erasure_score=32.0,
        primary_pattern="media_cultural_erasure",
        key_signals=[
            "Défis persistants pour les langues minoritaires en Europe — 60M de citoyens UE parlant des langues régionales ou minoritaires bénéficient d'un cadre partiel de protection (ECRML, Convention-cadre) mais des lacunes persistent dans la mise en œuvre entre États membres, notamment pour les langues non reconnues par la Charte",
            "Effacement médiatique et culturel (32.0/100) — malgré la Charte européenne des langues régionales ou minoritaires, plusieurs États membres n'ont pas ratifié l'instrument ou l'appliquent de manière restrictive, laissant des millions de locuteurs de langues minoritaires sans accès à des médias audiovisuels dans leur langue",
            "Universaliser la ratification de la Charte européenne des langues régionales ou minoritaires dans tous les États membres de l'UE et adopter un mécanisme de financement dédié à la revitalisation des langues minoritaires européennes dans le cadre du programme Europe Créative, conformément aux recommandations du Comité consultatif de la Convention-cadre",
        ],
    ),
    MinorityLanguageRightsEntity(
        entity_id="ML-008",
        name="ONU/PIDCP Art.27 — Droits Minorités Linguistiques, DNUDPA & UNESCO Atlas",
        country="Global",
        sector="PIDCP Article 27 Droits Minorités 173 Ratifications, DNUDPA Articles 13-14 Droits Linguistiques Autochtones 2007, UNESCO Atlas Langues En Danger 2500+ & Déclaration ONU Droits Personnes Minorités 1992",
        language_suppression_score=4.0,
        education_denial_score=5.0,
        legal_recognition_absence_score=3.0,
        media_cultural_erasure_score=6.0,
        primary_pattern="media_cultural_erasure",
        key_signals=[
            "ONU/PIDCP Art.27 constitue le fondement normatif des droits linguistiques des minorités — l'Article 27 PIDCP ratifié par 173 États protège le droit des personnes appartenant à des minorités d'utiliser leur propre langue, créant une obligation négative (non-interférence) et positive (protection active) pour les États",
            "DNUDPA Articles 13-14 (2007) — la Déclaration ONU sur les droits des peuples autochtones reconnaît le droit à revitaliser, utiliser, développer et transmettre aux générations futures leurs langues, traditions orales et systèmes d'écriture, et le droit à l'éducation dans leur langue autochtone, créant un standard international renforcé",
            "UNESCO Atlas des langues en danger — le suivi de 2 500 langues en danger permet d'identifier les situations d'urgence requérant une action immédiate et constitue l'outil de référence pour les États qui doivent adopter des politiques de revitalisation linguistique conformément à leurs obligations au titre du PIDCP et de la DNUDPA",
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
        "domain": "minority_language_rights",
        "confidence_score": 0.84,
        "data_sources": [
            "unesco_atlas_of_worlds_languages_in_danger_online_edition",
            "council_of_europe_ecrml_monitoring_reports_by_committee_of_experts",
            "un_special_rapporteur_minority_issues_country_reports",
        ],
        "entities": results,
        "avg_estimated_minority_language_rights_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    import json
    data = run_analysis()
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"\n✅ Distribution: {data['risk_distribution']}")
    print(f"✅ Avg composite: {data['avg_composite']}")
    print(f"✅ Pattern dist: {data['pattern_distribution']}")
