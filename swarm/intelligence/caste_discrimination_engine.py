from datetime import date


class CasteDiscriminationEntity:
    def __init__(self, entity_id, name, country, sector,
                 untouchability_practice_rate_score,
                 occupational_segregation_score,
                 caste_violence_impunity_score,
                 intermarriage_prohibition_score,
                 risk_level, primary_pattern, key_signals, last_updated=None):
        self.entity_id = entity_id
        self.name = name
        self.country = country
        self.sector = sector
        self.untouchability_practice_rate_score = untouchability_practice_rate_score
        self.occupational_segregation_score = occupational_segregation_score
        self.caste_violence_impunity_score = caste_violence_impunity_score
        self.intermarriage_prohibition_score = intermarriage_prohibition_score
        self.composite_score = round(
            untouchability_practice_rate_score * 0.30 +
            occupational_segregation_score * 0.25 +
            caste_violence_impunity_score * 0.25 +
            intermarriage_prohibition_score * 0.20, 2
        )
        self.risk_level = risk_level
        self.primary_pattern = primary_pattern
        self.key_signals = key_signals
        self.estimated_caste_discrimination_index = round(self.composite_score / 100 * 10, 2)
        self.last_updated = last_updated or str(date.today())

    def to_dict(self):
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "untouchability_practice_rate_score": self.untouchability_practice_rate_score,
            "occupational_segregation_score": self.occupational_segregation_score,
            "caste_violence_impunity_score": self.caste_violence_impunity_score,
            "intermarriage_prohibition_score": self.intermarriage_prohibition_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_caste_discrimination_index": self.estimated_caste_discrimination_index,
            "last_updated": self.last_updated,
        }


class CasteDiscriminationEngine:
    VERSION = "1.0.0"
    CONFIDENCE = 0.81
    DOMAIN = "caste_discrimination"
    DATA_SOURCES = [
        "idsn_caste_based_discrimination_database",
        "human_rights_watch_caste_reports",
        "ilo_caste_discrimination_workplace_reports",
    ]

    def __init__(self):
        self.entities = self._build_entities()

    def _build_entities(self):
        return [
            CasteDiscriminationEntity(
                "CD-001",
                "Inde/Dalits — 50 000 Atrocités/An Bihar/UP, Intouchabilité Persistante & Viol Outil Oppression",
                "Asie du Sud",
                "50 000 Atrocités Dalits/An Bihar/UP, Scavenging Manuel 58 000 Encore Actifs, Viol Utilisé Punition Intercaste & Loi Atrocités 1989 Non-Appliquée",
                95, 92, 90, 88,
                "critique", "pratiques_intouchabilite",
                [
                    "Pratiques d'intouchabilité persistantes en Inde/Dalits — 50 000 atrocités documentées annuellement dans les États du Bihar et UP, avec viol utilisé comme outil de punition des Dalits qui défient la hiérarchie de caste",
                    "Discrimination intersectionnelle systémique — la discrimination de caste en Inde combine violence physique, ségrégation spatiale et économique, violant simultanément le droit à l'égalité (Article 17 Constitution), à la dignité et à l'intégrité physique",
                    "Activer le Rapporteur Spécial ONU sur les formes contemporaines de racisme pour audit spécifique sur la discrimination de caste et exiger l'application effective de la Loi de Prévention des Atrocités de 1989",
                ],
            ),
            CasteDiscriminationEntity(
                "CD-002",
                "Népal/Dalit — Discrimination Caste 40% Population, Mariages Intercaste Violence & Temple Accès Refusé",
                "Asie du Sud",
                "Mariages Intercaste Violence 2020-24 Documentée NHRC, Intouchabilité Rurale Dalits 40% Population, Temple/Puits Accès Refusé & Loi Criminalisation 2011 Non-Appliquée",
                88, 85, 90, 85,
                "critique", "pratiques_intouchabilite",
                [
                    "Pratiques d'intouchabilité persistantes au Népal/Dalit — 40% de la population Dalit subissant accès refusé aux temples, puits et lieux publics malgré l'interdiction constitutionnelle de 2007 et la loi de criminalisation de 2011",
                    "Discrimination intersectionnelle systémique — la discrimination de caste au Népal viole l'Article 24 de la Constitution népalaise et les obligations du Comité CERD, avec des violences documentées contre les couples intercaste",
                    "Activer le Comité ONU pour l'Élimination de la Discrimination Raciale (CERD) pour examiner la discrimination de caste au Népal et financer l'application effective des lois anti-discrimination",
                ],
            ),
            CasteDiscriminationEntity(
                "CD-003",
                "Yémen/Akhdam — Caste La Plus Basse, Ségrégation Sectorielle & Marginalisation Millénaire",
                "MENA",
                "Akhdam 'Serviteurs' Caste Inférieure Yemen, Ségrégation Spatiale Bidonvilles, Métiers Dégradants Assignés Générations & Mariage Intercaste Tabou Absolu",
                85, 82, 85, 82,
                "critique", "segregation_professionnelle_caste",
                [
                    "Ségrégation professionnelle de caste au Yémen/Akhdam — communauté Akhdam ('serviteurs') assignée aux métiers les plus dégradants depuis des millénaires, confinée dans des bidonvilles et exclue de l'ascension sociale par des barrières de caste implicites",
                    "Discrimination intersectionnelle — la hiérarchie de caste yéménite combine ségrégation raciale (origine africaine supposée des Akhdam) et discrimination de classe, violant les principes d'égalité de la Charte Arabe des Droits de l'Homme",
                    "Activer le Rapporteur Spécial ONU sur les formes contemporaines de racisme pour documenter la situation des Akhdam et exiger des réformes de lutte contre la discrimination de caste dans le cadre du processus de paix yéménite",
                ],
            ),
            CasteDiscriminationEntity(
                "CD-004",
                "Nigéria/Osu — Système Osu Igbo, Intouchabilité Persistante & Mariages Intercaste Tabou",
                "Afrique de l'Ouest",
                "Osu Igbo Descendants Esclaves Déités, Mariage Libre Non-Osu Tabou Communautaire, Cimetières/Églises Séparés Zones & Discrimination Éducation/Emploi Formelle",
                82, 80, 85, 80,
                "critique", "pratiques_intouchabilite",
                [
                    "Pratiques d'intouchabilité persistantes au Nigéria/Osu — système Osu chez les Igbo maintenant une caste d'intouchables descendants d'esclaves des divinités, exclus des mariages avec les non-Osu et des espaces communautaires",
                    "Discrimination intersectionnelle héréditaire — le système Osu constitue une forme de discrimination héréditaire basée sur le statut ancestral, violant les principes d'égalité de la Constitution nigériane et de la Charte Africaine des Droits de l'Homme",
                    "Activer la Commission Africaine des Droits de l'Homme pour examiner les pratiques de caste Osu et financer des programmes communautaires de sensibilisation contre la discrimination héréditaire au Nigéria",
                ],
            ),
            CasteDiscriminationEntity(
                "CD-005",
                "Japon/Burakumin — Discrimination Emploi/Mariage Persistante & Dossiers Cadastraux Caste",
                "Asie du Nord-Est",
                "Burakumin 3M Personnes Anciens Parias, Dossiers Cadastraux Caste Encore Accessibles, Discrimination Emploi/Mariage Enquêtes & Groupes Suprémacistes Dōwa Incitation",
                52, 55, 55, 50,
                "élevé", "segregation_professionnelle_caste",
                [
                    "Ségrégation professionnelle de caste persistante au Japon/Burakumin — 3 millions de descendants des anciens parias eta/hinin subissant discrimination à l'emploi et au mariage documentée par des enquêtes, malgré l'absence de loi anti-discrimination spécifique",
                    "Lacune juridique — le Japon ne dispose pas de loi interdisant explicitement la discrimination basée sur le statut de Burakumin, permettant la persistance de pratiques discriminatoires dans l'emploi, le mariage et l'accès au logement",
                    "Adopter une loi spécifique interdisant la discrimination Burakumin au Japon et criminaliser l'utilisation des anciens registres cadastraux pour identifier les descendants des quartiers historiques",
                ],
            ),
            CasteDiscriminationEntity(
                "CD-006",
                "Pakistan/Dalits Chrétiens — Scavenging Forcé, Conversions Forcées & Discrimination Légale",
                "Asie du Sud",
                "Dalits Chrétiens Pakistan 2M+ Balayeurs Forcés, Lois Blasphème Instruments Caste, Conversions Forcées Jeunes Femmes & Mariage Forcé Discrimination Légale",
                55, 52, 50, 52,
                "élevé", "pratiques_intouchabilite",
                [
                    "Pratiques d'intouchabilité persistantes au Pakistan/Dalits Chrétiens — 2 millions de Dalits chrétiens assignés au travail de nettoyage et balayage, utilisées comme instrument de discrimination de caste renforcée par les lois sur le blasphème",
                    "Discrimination intersectionnelle — la discrimination de caste au Pakistan se superpose à la discrimination religieuse, créant une double vulnérabilité pour les Dalits chrétiens et hindous soumis à des conversions forcées",
                    "Activer la Rapporteure Spéciale ONU sur la liberté religieuse et le Comité CERD pour examiner la discrimination intersectionnelle de caste et de religion visant les Dalits non-musulmans au Pakistan",
                ],
            ),
            CasteDiscriminationEntity(
                "CD-007",
                "Corée/Baekjeong — Caste Historique Abolie 1894 & Stigmate Social Résiduel",
                "Asie du Nord-Est",
                "Baekjeong Anciens Parias Coréens Abolition 1894 Gabo Reform, Stigmate Social Résiduel Noms/Quartiers, Discrimination Mariage Subtile & Intégration Substantielle Réalisée",
                28, 30, 25, 30,
                "modéré", "interdiction_mariage_intercaste",
                [
                    "Stigmate résiduel de caste en Corée/Baekjeong — discrimination de caste officiellement abolie depuis la réforme Gabo de 1894 mais stigmate social résiduel persistant dans certains mariages et communautés rurales pour les descendants Baekjeong",
                    "Progrès significatifs mais vigilance nécessaire — la Corée a réalisé une intégration sociale substantielle des Baekjeong en un siècle, mais des études documentent encore des préjugés résiduels dans les décisions matrimoniales",
                    "Maintenir les programmes éducatifs coréens sur l'histoire des castes et surveiller les cas résiduels de discrimination pour prévenir toute résurgence dans un contexte de montée du nationalisme identitaire",
                ],
            ),
            CasteDiscriminationEntity(
                "CD-008",
                "IDSN/OHCHR — Lutte Discrimination Caste & Principes Directeurs ONU",
                "Global",
                "IDSN International Dalit Solidarity Network, OHCHR Rapport Discrimination Fondée Ancêtres 2009, Principes Directeurs ONU Caste & CERD Recommandation Générale 29",
                5, 4, 3, 6,
                "faible", "violence_caste_impunite",
                [
                    "IDSN/OHCHR incarnent la protection exemplaire contre la discrimination de caste — Principes Directeurs ONU sur la discrimination fondée sur l'ascendance et Recommandation Générale 29 du CERD créant un cadre de responsabilité",
                    "Recommandation Générale 29 du CERD — interprétation explicite du CERD incluant la discrimination fondée sur l'ascendance (caste) dans le champ de la Convention pour l'Élimination de la Discrimination Raciale",
                    "Partager les méthodologies IDSN de documentation des violences de caste et renforcer la Recommandation Générale 29 du CERD pour contraindre les États à agir contre la discrimination d'ascendance",
                ],
            ),
        ]

    def summary(self):
        total = len(self.entities)
        avg = round(sum(e.composite_score for e in self.entities) / total, 2)
        risk_dist = {}
        pattern_dist = {}
        for e in self.entities:
            risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
            pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1
        sorted_e = sorted(self.entities, key=lambda x: x.composite_score, reverse=True)
        top3 = [e.name for e in sorted_e[:3]]
        critical = [
            f"{e.name.split('—')[0].strip()}: {e.primary_pattern.replace('_', ' ')}"
            for e in sorted_e if e.risk_level == "critique"
        ]
        return {
            "total_entities": total,
            "avg_composite": avg,
            "risk_distribution": risk_dist,
            "pattern_distribution": pattern_dist,
            "top_risk_entities": top3,
            "critical_alerts": critical,
            "last_analysis": str(date.today()),
            "engine_version": self.VERSION,
            "domain": self.DOMAIN,
            "confidence_score": self.CONFIDENCE,
            "data_sources": self.DATA_SOURCES,
            "entities": [e.to_dict() for e in self.entities],
            "avg_estimated_caste_discrimination_index": round(avg / 100 * 10, 2),
        }


if __name__ == "__main__":
    import json
    engine = CasteDiscriminationEngine()
    result = engine.summary()
    print(json.dumps({
        "domain": result["domain"],
        "total": result["total_entities"],
        "avg_composite": result["avg_composite"],
        "risk_distribution": result["risk_distribution"],
        "top_risk_entities": result["top_risk_entities"],
    }, indent=2, ensure_ascii=False))
