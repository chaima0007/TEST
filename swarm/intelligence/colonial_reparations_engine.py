from datetime import date


class ColonialReparationsEntity:
    def __init__(self, entity_id, name, country, sector,
                 historical_atrocity_magnitude_score,
                 reparation_refusal_persistence_score,
                 ongoing_structural_impact_score,
                 accountability_recognition_failure_score,
                 risk_level, primary_pattern, key_signals, last_updated=None):
        self.entity_id = entity_id
        self.name = name
        self.country = country
        self.sector = sector
        self.historical_atrocity_magnitude_score = historical_atrocity_magnitude_score
        self.reparation_refusal_persistence_score = reparation_refusal_persistence_score
        self.ongoing_structural_impact_score = ongoing_structural_impact_score
        self.accountability_recognition_failure_score = accountability_recognition_failure_score
        self.composite_score = round(
            historical_atrocity_magnitude_score * 0.30 +
            reparation_refusal_persistence_score * 0.25 +
            ongoing_structural_impact_score * 0.25 +
            accountability_recognition_failure_score * 0.20, 2
        )
        self.risk_level = risk_level
        self.primary_pattern = primary_pattern
        self.key_signals = key_signals
        self.estimated_colonial_reparations_index = round(self.composite_score / 100 * 10, 2)
        self.last_updated = last_updated or str(date.today())

    def to_dict(self):
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "historical_atrocity_magnitude_score": self.historical_atrocity_magnitude_score,
            "reparation_refusal_persistence_score": self.reparation_refusal_persistence_score,
            "ongoing_structural_impact_score": self.ongoing_structural_impact_score,
            "accountability_recognition_failure_score": self.accountability_recognition_failure_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_colonial_reparations_index": self.estimated_colonial_reparations_index,
            "last_updated": self.last_updated,
        }


class ColonialReparationsEngine:
    VERSION = "1.0.0"
    CONFIDENCE = 0.79
    DOMAIN = "colonial_reparations"
    DATA_SOURCES = [
        "caricom_reparations_commission_report",
        "un_permanent_forum_indigenous_issues",
        "transitional_justice_database_ictj",
    ]

    def __init__(self):
        self.entities = self._build_entities()

    def _build_entities(self):
        return [
            ColonialReparationsEntity(
                "CR-001",
                "Congo Belge/Léopold II — Génocide 10M Morts, Mains Coupées & Belgique Sans Réparation",
                "Afrique Centrale",
                "Léopold II Congo 10M Morts Estimés 1885-1908, Système Mains Coupées Documenté Adam Hochschild, Ressources Extractées Sans Réparation & Belgique Reconnaissance Partielle 2002",
                95, 90, 88, 88,
                "critique", "atrocites_coloniales_masse",
                [
                    "Atrocités coloniales de masse au Congo Belge/Léopold II — 10 millions de morts estimés sous le régime de terreur de Léopold II avec système de mutilations (mains coupées) documenté par les journalistes de l'époque et sans réparations formelles de la Belgique",
                    "Justice historique imprescriptible — les atrocités du Congo Belge constituent selon de nombreux historiens le premier génocide du XXe siècle, créant une obligation morale et juridique de reconnaissance et de réparation de la Belgique",
                    "Exiger de la Belgique des réparations formelles au Congo pour les crimes de Léopold II, au-delà de la reconnaissance partielle de 2002, incluant restitution du patrimoine pillé et fonds de développement",
                ],
            ),
            ColonialReparationsEntity(
                "CR-002",
                "Namibie/Allemagne — Génocide Herero/Nama 1904-08, Reconnaissance 2021 & Réparations Insuffisantes",
                "Afrique Australe",
                "Génocide Herero/Nama 80 000+ Morts 1904-08, Premier Génocide du XXe Siècle Reconnu, Accord Allemagne-Namibie 2021 1.1Md€ & Victimes Rejettent Offre Insuffisante",
                92, 88, 85, 85,
                "critique", "genocide_colonial_non_reconnu",
                [
                    "Génocide colonial non entièrement réparé en Namibie/Allemagne — génocide Herero et Nama de 1904-08 reconnu par l'Allemagne en 2021 avec offre de 1.1 milliard d'euros mais rejetée par les représentants des victimes comme insuffisante et excluant les descendants",
                    "Premier génocide du XXe siècle — le génocide Herero/Nama constitue le premier génocide colonial documenté du siècle, créant un précédent de responsabilité d'État pour crimes coloniaux avec des implications pour d'autres nations colonisatrices",
                    "Renégocier l'accord Allemagne-Namibie de 2021 avec une représentation directe des communautés Herero et Nama et accroître substantiellement le montant des réparations pour refléter la magnitude du génocide",
                ],
            ),
            ColonialReparationsEntity(
                "CR-003",
                "Inde/Royaume-Uni — Pillage Colonial 45 Trillards £ Estimé, Famine Bengal & Zero Réparation",
                "Asie du Sud",
                "Économiste Utsa Patnaik Pillage 45 Trillards £ 1765-1938, Famines Bengal 1943 3M Morts Churchill, Kohinoor/Patrimoine Non-Restitué & Aucune Réparation Britannique",
                88, 85, 90, 82,
                "critique", "pillage_colonial_systematique",
                [
                    "Pillage colonial systématique Inde/Royaume-Uni — économiste Utsa Patnaik estimant le pillage britannique de l'Inde à 45 trillards de livres sur 173 ans, avec la Famine du Bengale de 1943 causant 3 millions de morts sous la politique de Churchill",
                    "Impact structurel persistant — le pillage colonial explique en partie les inégalités économiques actuelles entre le Royaume-Uni et l'Inde, et la non-restitution du Kohinoor et des archives coloniales perpétue l'injustice historique",
                    "Engager le débat sur les réparations coloniales britanniques à l'Inde incluant la restitution du Kohinoor, des archives coloniales et la création d'un fonds de justice historique reconnaissant les crimes de la colonisation",
                ],
            ),
            ColonialReparationsEntity(
                "CR-004",
                "Algérie/France — 132 Ans Colonisation, Guerre Indépendance 1M Morts & Torture Reconnue",
                "MENA/Europe",
                "132 Ans Colonisation Française Algérie 1830-1962, Guerre Indépendance 1 000 000 Morts Algériens Estimés, Torture Systematique 1954-62 Reconnue & Macron Reconnaissance Partielle",
                85, 82, 88, 80,
                "critique", "atrocites_coloniales_masse",
                [
                    "Atrocités coloniales de masse Algérie/France — 132 ans de colonisation avec 1 million de morts algériens estimés pendant la guerre d'indépendance (1954-62) et torture systématique reconnue par Macron en 2018 sans réparations formelles",
                    "Blessure mémorielle persistante — l'absence de reconnaissance complète et de réparations françaises pour les crimes coloniaux en Algérie entretient une fracture mémorielle affectant les relations diplomatiques et les communautés franco-algériennes",
                    "Poursuivre le processus de réconciliation mémorielle franco-algérienne avec reconnaissance formelle des crimes de la colonisation et création d'une commission bilatérale sur la mémoire incluant la question des réparations",
                ],
            ),
            ColonialReparationsEntity(
                "CR-005",
                "CARICOM/Caraïbes — Plan 10 Points Réparations, Esclavage Traite & Dettes Coloniales",
                "Caraïbes",
                "CARICOM Plan Réparations 10 Points 2014, Esclavage Transatlantique 12.5M Déportés, Haïti Dette Coloniale France 21Md$ Remboursée & Légacies Structurelles Pauvreté",
                55, 58, 55, 52,
                "élevé", "refus_reparations_persistant",
                [
                    "Refus persistant des réparations aux Caraïbes/CARICOM — Plan en 10 Points de la CARICOM demandant réparations pour l'esclavage transatlantique (12.5 millions déportés) ignoré par les anciennes puissances coloniales et dette haïtienne payée à la France pendant 122 ans",
                    "Injustice économique structurelle — la traite transatlantique et l'esclavage ont créé des inégalités économiques persistantes entre les Caraïbes et les anciennes métropoles coloniales, avec Haïti ayant payé 21 milliards de dollars de 'dette d'indépendance' à la France",
                    "Soutenir le Plan en 10 Points de la CARICOM incluant excuses formelles, programmes de développement et annulation des dettes coloniales résiduelles, en commençant par la restitution de la dette haïtienne à la France",
                ],
            ),
            ColonialReparationsEntity(
                "CR-006",
                "Australie/Générations Volées — Enfants Autochtones Enlevés 1910-70 & Sorry Day 2008",
                "Océanie",
                "Générations Volées 100 000+ Enfants Autochtones Enlevés Familles 1910-1970, Rapport Bringing Them Home 1997, Sorry Day Rudd 2008 & Réparations Financières Insuffisantes",
                52, 55, 52, 50,
                "élevé", "genocide_colonial_non_reconnu",
                [
                    "Génocide culturel partiellement reconnu Australie/Générations Volées — 100 000+ enfants autochtones enlevés à leurs familles entre 1910 et 1970 (Générations Volées), avec excuses formelles du Premier Ministre Rudd en 2008 mais réparations financières insuffisantes",
                    "Impact structurel multigénérationnel — les traumatismes intergénérationnels des Générations Volées contribuent aux inégalités persistantes en santé, éducation et espérance de vie entre Autochtones et non-Autochtones en Australie",
                    "Mettre en œuvre les recommandations du rapport Closing the Gap avec financement adéquat et négocier des réparations financières directes aux survivants des Générations Volées et leurs descendants",
                ],
            ),
            ColonialReparationsEntity(
                "CR-007",
                "USA/Esclavage — HR40 Commission Reparations, Wealth Gap Racial & Tulsa Race Massacre",
                "Amérique du Nord",
                "HR40 Bill Commission Réparations Esclavage Bloqué Congrès, Wealth Gap Racial 8x, Tulsa Race Massacre 1921 Rescapés Sans Réparation & Evanston IL Premier Programme Local",
                28, 32, 30, 28,
                "modéré", "refus_reparations_persistant",
                [
                    "Refus persistant des réparations aux États-Unis/Esclavage — le projet de loi HR40 créant une commission d'étude des réparations pour l'esclavage bloqué au Congrès depuis 1989, malgré un écart de richesse racial de 8:1 et le Massacre de Tulsa 1921 sans indemnisation des rescapés",
                    "Inégalité structurelle héritée — l'écart de richesse racial de 8:1 entre Noirs et Blancs aux États-Unis est directement lié à l'héritage de l'esclavage et à des politiques post-esclavage discriminatoires comme la ségrégation et le redlining",
                    "Soutenir l'adoption du HR40 au Congrès américain pour créer une commission d'étude des réparations pour l'esclavage et s'inspirer du programme de réparations locales d'Evanston (Illinois) comme modèle municipal",
                ],
            ),
            ColonialReparationsEntity(
                "CR-008",
                "CARICOM/ONU — Cadre Réparations Internationales & Principes Justice Transitionnelle",
                "Global",
                "Principes ONU Droit Recours Réparation Victimes 2005, Forum Permanent Peuples Autochtones ONU, Déclaration ONU Peuples Autochtones 2007 & CARICOM 10 Points Framework",
                5, 4, 3, 6,
                "faible", "refus_reparations_persistant",
                [
                    "CARICOM/ONU incarnent le cadre exemplaire des réparations — Principes ONU sur le droit à un recours et à réparation (2005) et Déclaration ONU sur les droits des peuples autochtones (2007) créant une base juridique pour les revendications de réparations coloniales",
                    "Principes ONU sur les Victimes (Résolution 60/147) — droit des victimes de crimes historiques à une restitution, indemnisation, réhabilitation, satisfaction et garanties de non-répétition, applicables aux crimes coloniaux",
                    "Partager les méthodologies CARICOM de quantification des réparations coloniales et renforcer le mandat du Forum Permanent des Nations Unies pour les questions autochtones pour documenter les impacts persistants de la colonisation",
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
            "avg_estimated_colonial_reparations_index": round(avg / 100 * 10, 2),
        }


if __name__ == "__main__":
    import json
    engine = ColonialReparationsEngine()
    result = engine.summary()
    print(json.dumps({
        "domain": result["domain"],
        "total": result["total_entities"],
        "avg_composite": result["avg_composite"],
        "risk_distribution": result["risk_distribution"],
        "top_risk_entities": result["top_risk_entities"],
    }, indent=2, ensure_ascii=False))
