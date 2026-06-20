from datetime import date


class PrisonTortureEntity:
    def __init__(self, entity_id, name, country, sector,
                 systematic_torture_rate_score,
                 detention_condition_severity_score,
                 impunity_perpetrators_score,
                 medical_care_denial_score,
                 risk_level, primary_pattern, key_signals, last_updated=None):
        self.entity_id = entity_id
        self.name = name
        self.country = country
        self.sector = sector
        self.systematic_torture_rate_score = systematic_torture_rate_score
        self.detention_condition_severity_score = detention_condition_severity_score
        self.impunity_perpetrators_score = impunity_perpetrators_score
        self.medical_care_denial_score = medical_care_denial_score
        self.composite_score = round(
            systematic_torture_rate_score * 0.30 +
            detention_condition_severity_score * 0.25 +
            impunity_perpetrators_score * 0.25 +
            medical_care_denial_score * 0.20, 2
        )
        self.risk_level = risk_level
        self.primary_pattern = primary_pattern
        self.key_signals = key_signals
        self.estimated_prison_torture_index = round(self.composite_score / 100 * 10, 2)
        self.last_updated = last_updated or str(date.today())

    def to_dict(self):
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "systematic_torture_rate_score": self.systematic_torture_rate_score,
            "detention_condition_severity_score": self.detention_condition_severity_score,
            "impunity_perpetrators_score": self.impunity_perpetrators_score,
            "medical_care_denial_score": self.medical_care_denial_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_prison_torture_index": self.estimated_prison_torture_index,
            "last_updated": self.last_updated,
        }


class PrisonTortureEngine:
    VERSION = "1.0.0"
    CONFIDENCE = 0.86
    DOMAIN = "prison_torture"
    DATA_SOURCES = [
        "un_cat_reports_states_parties",
        "amnesty_international_torture_reports",
        "hrw_world_report_detention_conditions",
    ]

    def __init__(self):
        self.entities = self._build_entities()

    def _build_entities(self):
        return [
            PrisonTortureEntity(
                "PT-001",
                "RPDC/Kim Jong-Un — Camps Politiques 150 000 Détenus & Torture Systématique",
                "Asie du Nord-Est",
                "Camp 14/22 Survivant Shin Dong-Hyuk, 150 000 Prisonniers Politiques OHCHR, Torture Standard Officielle & Privation Sommeil Systématique",
                95, 92, 90, 95,
                "critique", "torture_systematique_detention",
                [
                    "Torture systématique en RPDC — 150 000 détenus dans des camps politiques (kwanliso) subissant torture officielle, travaux forcés, exécutions sommaires et privation de nourriture documentés par la Commission d'Enquête ONU 2014",
                    "Crime contre l'humanité — la torture systématique et généralisée en RPDC constitue un crime contre l'humanité selon le Statut de Rome, engageant la responsabilité personnelle du dirigeant Kim Jong-Un",
                    "Activer le Rapporteur Spécial ONU sur la torture et saisir la CPI pour crimes contre l'humanité incluant torture, meurtres et disparitions forcées dans les camps politiques nord-coréens",
                ],
            ),
            PrisonTortureEntity(
                "PT-002",
                "Syrie/Assad — Sednaya 'Abattoir', 13 000 Pendus & César Photos 55 000 Victimes",
                "MENA",
                "Sednaya Prison Exécutions 2011-24, 13 000 Personnes Pendues, César Photos 55 000 Corps Victimes Torture & Rapport Amnesty 2017 Abattoir Humain",
                92, 95, 95, 88,
                "critique", "torture_systematique_detention",
                [
                    "Torture systématique en Syrie/Assad — prison Sednaya qualifiée d'abattoir humain par Amnesty avec 13 000 pendus et 55 000 photos de corps de victimes de torture (rapport César) documentant les crimes du régime",
                    "Crime contre l'humanité — la torture systématique dans les prisons syriennes constitue un crime contre l'humanité selon le Statut de Rome, avec des preuves directes documentées par les Nations Unies",
                    "Activer la Commission Internationale Indépendante d'Enquête sur la Syrie et saisir le IIIM pour poursuite des responsables de torture dans les prisons syriennes",
                ],
            ),
            PrisonTortureEntity(
                "PT-003",
                "Chine/Xinjiang — Camps Rééducation 1M+ Internés & Torture Témoignages Systématiques",
                "Asie",
                "1M+ Ouïghours Internés Camps Rééducation 2017-24, Tortures Témoignages OHCHR, Privation Sommeil & Tribunal Ouïghour Génocide Londres 2021",
                88, 85, 88, 90,
                "critique", "detention_conditions_inhumaines",
                [
                    "Conditions de détention inhumaines en Chine/Xinjiang — 1 million+ Ouïghours internés dans des camps avec témoignages systématiques de tortures, viols et privation de sommeil documentés par le rapport OHCHR 2022",
                    "Crime contre l'humanité — le Tribunal Ouïghour de Londres 2021 a conclu à des actes de torture, viol et violences sexuelles systématiques équivalant à des crimes contre l'humanité",
                    "Activer le Rapporteur Spécial ONU sur la torture et mettre en œuvre les recommandations OHCHR pour accès indépendant aux camps de détention au Xinjiang",
                ],
            ),
            PrisonTortureEntity(
                "PT-004",
                "Égypte/El-Sisi — Prison Scorpion, 60 000 Prisonniers Politiques & Torture Institutionnalisée",
                "MENA",
                "60 000 Prisonniers Politiques Sisi, Prison Scorpion Isolement Sensoriel, Détention Préventive Illimitée & HRW Torture Institutionnalisée Rapportée 2020-24",
                85, 82, 85, 82,
                "critique", "impunite_tortionnaires",
                [
                    "Impunité des tortionnaires en Égypte/El-Sisi — 60 000 prisonniers politiques avec torture institutionnalisée à la prison Scorpion, aucune poursuite contre les agents de l'État malgré les rapports HRW et Amnesty",
                    "Violation de la Convention contre la Torture — les pratiques de détention égyptiennes violent la CAT ratifiée en 1986, avec mécanisme d'examen périodique révélant une absence totale d'accountability",
                    "Activer le Comité ONU contre la Torture (CAT) pour examen d'urgence de l'Égypte et conditionner l'aide militaire américaine à l'amélioration des conditions de détention",
                ],
            ),
            PrisonTortureEntity(
                "PT-005",
                "USA/CIA — Guantanamo, Black Sites & Rapport Sénat 2014 'Enhanced Interrogation'",
                "Amérique du Nord",
                "Rapport Sénat 2014 Techniques Torture CIA Confirmées, Waterboarding 183 Fois KSM, 780 Détenus Guantanamo Sans Procès & Black Sites Thaïlande/Pologne/Roumanie",
                52, 55, 58, 55,
                "élevé", "impunite_tortionnaires",
                [
                    "Impunité des tortionnaires USA/CIA — rapport du Sénat 2014 documentant tortures (waterboarding, privation de sommeil, alimentation rectale) dans des sites noirs à travers le monde sans aucune poursuite judiciaire",
                    "Violation de la Convention contre la Torture — les techniques d'interrogatoire CIA constituent de la torture selon le droit international, et l'absence de poursuites viole l'obligation de rendre compte de la Convention CAT",
                    "Fermer Guantanamo conformément aux engagements répétés des administrations américaines et poursuivre les responsables de la conception du programme de torture CIA devant la justice",
                ],
            ),
            PrisonTortureEntity(
                "PT-006",
                "Turquie/Erdoğan — Post-Coup 150 000 Détenus & CPT Mauvais Traitements Généralisés",
                "Europe/MENA",
                "Post-Coup 2016 150 000 Détenus Purges, Rapport CPT Mauvais Traitements Généralisés 2017, Kurdes Conditions Isolement & Erdoğan Suspension Garanties CEDH",
                48, 55, 52, 50,
                "élevé", "detention_conditions_inhumaines",
                [
                    "Conditions de détention inhumaines en Turquie/Erdoğan — 150 000 détenus post-coup avec rapport CPT 2017 documentant mauvais traitements généralisés incluant coups, positions de stress et menaces lors des gardes à vue",
                    "Violation des standards européens — les pratiques de détention turques violent la Convention Européenne des Droits de l'Homme dont la Turquie est partie, entraînant de nombreuses condamnations à la Cour EDH",
                    "Activer les mécanismes du Conseil de l'Europe et conditionner les négociations d'adhésion UE à l'amélioration des conditions de détention et à la fin des mauvais traitements documentés",
                ],
            ),
            PrisonTortureEntity(
                "PT-007",
                "Brésil/PCC — Prisons Surpeuplées +70%, Massacres Nordeste & Conditions Inhumaines",
                "Amérique du Sud",
                "900 000 Détenus Brésil +70% Surpopulation, PCC/FDN Violence Inter-Gang, Nordeste Massacres Prisons 2017 & Conditions Sanitaires Inhumaines DEPEN",
                28, 32, 28, 30,
                "modéré", "detention_conditions_inhumaines",
                [
                    "Conditions de détention inhumaines au Brésil/PCC — surpopulation carcérale à +70% avec violences de gangs PCC/FDN ayant causé des massacres au Nordeste en 2017 et conditions sanitaires inhumaines documentées",
                    "Violation des droits humains — les conditions carcérales brésiliennes violent les Règles Nelson Mandela de l'ONU sur le traitement des détenus, et l'État ne garantit pas la sécurité des personnes détenues",
                    "Accélérer les réformes du système pénitentiaire brésilien conformément aux Règles Nelson Mandela et financer la réduction de la surpopulation par des alternatives à l'incarcération",
                ],
            ),
            PrisonTortureEntity(
                "PT-008",
                "CPT/CAT-ONU — Prévention Torture, Protocole OPCAT & Rapporteur Spécial",
                "Global",
                "CAT ONU Convention 173 États, OPCAT Protocole Facultatif MNP Nationaux, CPT Conseil Europe 500+ Visites Pays & Rapporteur Spécial ONU Torture Mandat",
                5, 4, 3, 6,
                "faible", "impunite_tortionnaires",
                [
                    "CPT/CAT-ONU incarnent la prévention exemplaire de la torture — Convention CAT ratifiée par 173 États, Protocole OPCAT créant des mécanismes nationaux de prévention et Rapporteur Spécial ONU avec mandat de visite",
                    "Convention ONU contre la Torture 1984 — obligation erga omnes d'interdire, prévenir, enquêter et poursuivre la torture, avec mécanisme d'examen périodique des États parties au Comité CAT",
                    "Partager les méthodologies CPT de documentation des lieux de détention et renforcer l'OPCAT pour garantir des visites indépendantes dans tous les lieux de privation de liberté",
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
            "avg_estimated_prison_torture_index": round(avg / 100 * 10, 2),
        }


if __name__ == "__main__":
    import json
    engine = PrisonTortureEngine()
    result = engine.summary()
    print(json.dumps({
        "domain": result["domain"],
        "total": result["total_entities"],
        "avg_composite": result["avg_composite"],
        "risk_distribution": result["risk_distribution"],
        "top_risk_entities": result["top_risk_entities"],
    }, indent=2, ensure_ascii=False))
