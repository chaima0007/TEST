from datetime import date


class StatelessnessEntity:
    def __init__(self, entity_id, name, country, sector,
                 denationalization_rate_score,
                 birth_registration_denial_score,
                 stateless_detention_risk_score,
                 documentation_access_failure_score,
                 risk_level, primary_pattern, key_signals, last_updated=None):
        self.entity_id = entity_id
        self.name = name
        self.country = country
        self.sector = sector
        self.denationalization_rate_score = denationalization_rate_score
        self.birth_registration_denial_score = birth_registration_denial_score
        self.stateless_detention_risk_score = stateless_detention_risk_score
        self.documentation_access_failure_score = documentation_access_failure_score
        self.composite_score = round(
            denationalization_rate_score * 0.30 +
            birth_registration_denial_score * 0.25 +
            stateless_detention_risk_score * 0.25 +
            documentation_access_failure_score * 0.20, 2
        )
        self.risk_level = risk_level
        self.primary_pattern = primary_pattern
        self.key_signals = key_signals
        self.estimated_statelessness_index = round(self.composite_score / 100 * 10, 2)
        self.last_updated = last_updated or str(date.today())

    def to_dict(self):
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "denationalization_rate_score": self.denationalization_rate_score,
            "birth_registration_denial_score": self.birth_registration_denial_score,
            "stateless_detention_risk_score": self.stateless_detention_risk_score,
            "documentation_access_failure_score": self.documentation_access_failure_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_statelessness_index": self.estimated_statelessness_index,
            "last_updated": self.last_updated,
        }


class StatelessnessEngine:
    VERSION = "1.0.0"
    CONFIDENCE = 0.84
    DOMAIN = "statelessness"
    DATA_SOURCES = [
        "unhcr_global_trends_statelessness_report",
        "institute_statelessness_and_inclusion_database",
        "ibelong_unhcr_campaign_data",
    ]

    def __init__(self):
        self.entities = self._build_entities()

    def _build_entities(self):
        return [
            StatelessnessEntity(
                "SL-001",
                "Myanmar/Rohingya — Loi Citoyenneté 1982, 600 000 Apatrides & Génocide Documenté ONU",
                "Asie du Sud-Est",
                "Loi Citoyenneté Myanmar 1982 Exclusion Rohingya, 600 000 Apatrides Rakhine, Opération Militaire 2017 Épuration & Registre Naissance Refusé Générations",
                95, 92, 90, 88,
                "critique", "denationalisation_massive",
                [
                    "Dénationalisation massive au Myanmar/Rohingya — loi de citoyenneté de 1982 excluant délibérément les Rohingya de la nationalité birmane, créant 600 000 apatrides dans l'État Rakhine privés de tout document d'identité",
                    "Droit fondamental violé — la nationalité est un droit humain fondamental selon l'Article 15 de la DUDH, et la dénationalisation ethnique constitue un élément du crime de génocide selon la Convention de 1948",
                    "Activer la Convention de 1954 sur les apatrides et la Convention de 1961 sur la réduction de l'apatridie pour exiger la reconnaissance de la nationalité rohingya par le Myanmar",
                ],
            ),
            StatelessnessEntity(
                "SL-002",
                "Golfe Arabe/Bidun — 100 000+ Apatrides 2e Génération Koweït/EAU & Documents Refusés",
                "MENA",
                "Bidun Kuwait 100 000+ Sans Nationalité, EAU Bidun 10 000 Apatrides, Né au Golfe Mais Refus Documentation & Generations Sans Identité Légale",
                88, 85, 90, 88,
                "critique", "echec_documentation_acces",
                [
                    "Échec d'accès aux documents d'identité Golfe/Bidun — 100 000+ Bidun au Koweït et aux EAU nés dans ces pays mais refusant tout accès à la nationalité ou aux documents malgré des générations de résidence",
                    "Droit fondamental violé — l'absence de documents d'identité prive les Bidun de l'accès aux soins, à l'éducation, à l'emploi et à la justice, constituant une violation systémique de la DUDH Article 15",
                    "Activer le Rapporteur Spécial ONU sur les droits des migrants et exiger des États du Golfe la mise en place de voies d'accès à la nationalité pour les Bidun conformément à la Convention de 1954",
                ],
            ),
            StatelessnessEntity(
                "SL-003",
                "RPDC/Réfugiés — Diaspora Apatride Chine, Détention Sans Statut & Refoulement Forcé",
                "Asie du Nord-Est",
                "Réfugiés RPDC Chine 100 000+ Sans Statut Légal, Détention Chine Sans UNHCR Accès, Refoulement Forcé Corée Nord & Persécution Retour Documentée",
                82, 95, 88, 80,
                "critique", "detention_apatrides",
                [
                    "Détention d'apatrides de fait en RPDC/Chine — 100 000+ réfugiés nord-coréens en Chine refusés par le système de protection internationale et détenus sans accès au HCR, soumis à refoulement forcé vers la RPDC",
                    "Violation du principe de non-refoulement — la Chine viole la Convention de 1951 sur les réfugiés en refoulant des Nord-Coréens vers un pays où ils font face à torture, emprisonnement et exécution",
                    "Exiger de la Chine l'accès du HCR aux réfugiés nord-coréens et la cessation des refoulements forcés violant le droit international des réfugiés",
                ],
            ),
            StatelessnessEntity(
                "SL-004",
                "Côte d'Ivoire/Dioula — Dénationalisation 700 000 & Crise Nationalité Post-Ivoirité",
                "Afrique de l'Ouest",
                "Ivoirité Politique Exclusion 700 000 Personnes, Dioula/Mandé Sans Documents Nationalité, Crise Post-Electorale 2010-11 Apatridie & Burkina/Mali Frontaliers Indocumentés",
                85, 82, 85, 80,
                "critique", "denationalisation_massive",
                [
                    "Dénationalisation massive en Côte d'Ivoire/Dioula — concept d'Ivoirité utilisé pour priver 700 000 personnes d'origine mandé de leur nationalité ivoirienne, créant une apatridie politique documentée par le HCR",
                    "Droit fondamental violé — la dénationalisation politique viole l'Article 15 de la DUDH et la Charte Africaine des Droits de l'Homme, créant une exclusion civique de populations résidant depuis des générations",
                    "Activer la Commission Africaine des Droits de l'Homme pour examiner la politique d'Ivoirité et exiger la mise en place d'un processus de documentation accessible pour toutes les personnes résidant en Côte d'Ivoire",
                ],
            ),
            StatelessnessEntity(
                "SL-005",
                "Thaïlande/Peuples des Montagnes — 480 000 Hill Tribes Sans Citoyenneté & Naissance Non-Enregistrée",
                "Asie du Sud-Est",
                "480 000 Hill Tribes Thaïlande Sans Citoyenneté, Karen/Hmong/Akha Naissance Non-Enregistrée, Accès Soins/Education Refusé & Statut Illégal Permanent",
                55, 58, 52, 55,
                "élevé", "deni_enregistrement_naissance",
                [
                    "Déni d'enregistrement des naissances en Thaïlande/Hill Tribes — 480 000 membres des peuples des montagnes (Karen, Hmong, Akha) nés en Thaïlande mais non enregistrés, créant une apatridie héréditaire de facto",
                    "Droit fondamental violé — le droit à l'enregistrement de la naissance et à une nationalité est garanti par l'Article 7 de la Convention des Droits de l'Enfant, dont la Thaïlande est signataire",
                    "Accélérer les programmes de documentation des Hill Tribes en Thaïlande et mettre en œuvre le Plan d'Action Global de l'IBelong-HCR pour l'éradication de l'apatridie d'ici 2024",
                ],
            ),
            StatelessnessEntity(
                "SL-006",
                "Kirghizistan/Ethnies — Ex-URSS Apatrides, Dissolution Soviétique & Documents Non-Transférés",
                "Asie Centrale",
                "Ex-URSS Dissolution Apatridie 100 000+ Personnes Kirghizistan/Tadjikistan, Documents Soviétiques Non-Transférés, Ethnies Minoritaires Indocumentées & HCR Campagne Active",
                52, 55, 50, 58,
                "élevé", "deni_enregistrement_naissance",
                [
                    "Déni d'enregistrement en Kirghizistan — héritage de la dissolution soviétique laissant 100 000+ personnes sans documents de nationalité valides, principalement des minorités ethniques dont les naissances n'ont jamais été correctement transférées",
                    "Lacune institutionnelle post-soviétique — l'absence de procédures claires de succession d'État pour les ressortissants des ex-républiques soviétiques a créé une apatridie structurelle violant l'Article 15 de la DUDH",
                    "Soutenir les campagnes HCR d'enregistrement rétroactif en Asie Centrale et exiger des États successeurs de l'URSS des procédures simplifiées de naturalisation pour les personnes apatrides de facto",
                ],
            ),
            StatelessnessEntity(
                "SL-007",
                "Lettonie/Estonie — 'Non-Citoyens' Russophones, 200 000 Statut Spécial & Droits Limités",
                "Europe",
                "Lettonie 200 000 Non-Citoyens Russophones, Estonie Apatrides Soviétiques, Passeport Alien Non-Citoyen & Vote Municipal Refusé UE Discrimination",
                28, 30, 28, 32,
                "modéré", "echec_documentation_acces",
                [
                    "Échec partiel d'accès aux droits en Lettonie/Estonie — 200 000 russophones de Lettonie détenant un statut de 'non-citoyen' les privant du droit de vote aux élections législatives et limitant leur mobilité intra-UE",
                    "Discrimination institutionnelle — le statut de non-citoyen crée une catégorie de résidents de longue durée aux droits réduits, soulevant des questions de compatibilité avec les standards européens des droits humains",
                    "Accélérer les procédures de naturalisation simplifiée pour les non-citoyens de Lettonie et d'Estonie et activer les mécanismes du Conseil de l'Europe pour surveiller la conformité avec les standards européens",
                ],
            ),
            StatelessnessEntity(
                "SL-008",
                "HCR/IBelong — Campagne Éradication Apatridie 2014-2024 & Conventions Protectrices",
                "Global",
                "HCR IBelong Campaign 10 Ans 2014-2024, Convention Apatrides 1954 97 États, Convention Réduction Apatridie 1961 & Plan d'Action Global 8 Mesures",
                5, 4, 3, 6,
                "faible", "deni_enregistrement_naissance",
                [
                    "HCR/IBelong incarne la protection exemplaire contre l'apatridie — campagne IBelong visant l'éradication de l'apatridie d'ici 2024 avec 8 actions prioritaires et conventions de 1954 et 1961 créant un cadre contraignant",
                    "Convention de 1954 sur le statut des apatrides — définit les droits des apatrides et oblige les États parties à leur garantir documents de voyage, accès au travail et à l'éducation",
                    "Universaliser la ratification des Conventions de 1954 et 1961 sur l'apatridie et financer les campagnes d'enregistrement civil dans les pays à forte prévalence d'apatridie",
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
            "avg_estimated_statelessness_index": round(avg / 100 * 10, 2),
        }


if __name__ == "__main__":
    import json
    engine = StatelessnessEngine()
    result = engine.summary()
    print(json.dumps({
        "domain": result["domain"],
        "total": result["total_entities"],
        "avg_composite": result["avg_composite"],
        "risk_distribution": result["risk_distribution"],
        "top_risk_entities": result["top_risk_entities"],
    }, indent=2, ensure_ascii=False))
