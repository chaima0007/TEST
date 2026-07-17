from datetime import date


class PoliceBrutalityEntity:
    def __init__(self, entity_id, name, country, sector,
                 extrajudicial_killing_rate_score,
                 racial_ethnic_targeting_score,
                 accountability_oversight_failure_score,
                 protest_repression_score,
                 risk_level, primary_pattern, key_signals, last_updated=None):
        self.entity_id = entity_id
        self.name = name
        self.country = country
        self.sector = sector
        self.extrajudicial_killing_rate_score = extrajudicial_killing_rate_score
        self.racial_ethnic_targeting_score = racial_ethnic_targeting_score
        self.accountability_oversight_failure_score = accountability_oversight_failure_score
        self.protest_repression_score = protest_repression_score
        self.composite_score = round(
            extrajudicial_killing_rate_score * 0.30 +
            racial_ethnic_targeting_score * 0.25 +
            accountability_oversight_failure_score * 0.25 +
            protest_repression_score * 0.20, 2
        )
        self.risk_level = risk_level
        self.primary_pattern = primary_pattern
        self.key_signals = key_signals
        self.estimated_police_brutality_index = round(self.composite_score / 100 * 10, 2)
        self.last_updated = last_updated or str(date.today())

    def to_dict(self):
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "extrajudicial_killing_rate_score": self.extrajudicial_killing_rate_score,
            "racial_ethnic_targeting_score": self.racial_ethnic_targeting_score,
            "accountability_oversight_failure_score": self.accountability_oversight_failure_score,
            "protest_repression_score": self.protest_repression_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_police_brutality_index": self.estimated_police_brutality_index,
            "last_updated": self.last_updated,
        }


class PoliceBrutalityEngine:
    VERSION = "1.0.0"
    CONFIDENCE = 0.82
    DOMAIN = "police_brutality"
    DATA_SOURCES = [
        "amnesty_international_police_violence_reports",
        "hrw_excessive_force_database",
        "mapping_police_violence_project",
    ]

    def __init__(self):
        self.entities = self._build_entities()

    def _build_entities(self):
        return [
            PoliceBrutalityEntity(
                "PB-001",
                "Philippines/Duterte — War on Drugs 6 000+ Morts EJK & Impunité Totale PNP",
                "Asie du Sud-Est",
                "War on Drugs 6 000+ Morts EJK PNP 2016-22, 12 000+ Morts Estimés Vigilantes, Aucune Poursuite Agents & ICC Enquête Préliminaire Crimes Humanité",
                95, 82, 90, 88,
                "critique", "meurtres_extrajudiciaires",
                [
                    "Meurtres extrajudiciaires massifs aux Philippines/Duterte — 6 000+ morts officiels dans la War on Drugs par la PNP avec 12 000+ tués par des vigilantes, aucune poursuite contre des agents malgré l'ouverture d'une enquête ICC",
                    "Crime contre l'humanité — la Commission ICC a conclu en 2021 à des preuves raisonnables de crimes contre l'humanité dans la conduite de la War on Drugs philippine, engageant la responsabilité étatique",
                    "Soutenir la compétence de la CPI pour poursuivre les responsables de la War on Drugs philippine et exiger un mécanisme d'accountability indépendant pour les meurtres extrajudiciaires",
                ],
            ),
            PoliceBrutalityEntity(
                "PB-002",
                "Brésil/PMERJ — 6 000+ Tués Police/An Favelas & Racisme Structurel Documenté",
                "Amérique du Sud",
                "6 000+ Tués Police Brésil/An PMERJ/PM, Noirs 75% Victimes Police, Favelas Zones Impunité & Opération Maré 2022 80 Morts 1 Jour Condamnée ONU",
                92, 88, 85, 82,
                "critique", "meurtres_extrajudiciaires",
                [
                    "Meurtres extrajudiciaires massifs au Brésil/PMERJ — 6 000+ tués par la police chaque année, dont 75% de Noirs, avec des opérations de favelas comme l'Opération Maré 2022 (80 morts en un jour) condamnées par l'ONU",
                    "Racisme structurel documenté — le ciblage des Noirs brésiliens par la police constitue une discrimination raciale systémique violant la Convention Internationale pour l'Élimination de toutes les formes de Discrimination Raciale",
                    "Activer le Comité CERD pour examen urgent de la brutalité policière raciale au Brésil et soutenir le projet de loi national de contrôle de la violence policière en favelas",
                ],
            ),
            PoliceBrutalityEntity(
                "PB-003",
                "USA/BLM — 1 000+ Tués Police/An, Racisme Systémique & George Floyd Moment Mondial",
                "Amérique du Nord",
                "1 000+ Américains Tués Police/An, Noirs 2.5x Plus Tués Que Blancs, George Floyd Minneapolis 2020 & Rapport ONU Racisme Systémique Police Documenté",
                80, 95, 82, 85,
                "critique", "ciblage_racial_ethnique",
                [
                    "Ciblage racial systémique USA/Police — 1 000+ personnes tuées par la police chaque année dont les Noirs américains 2.5 fois plus susceptibles d'être tués que les Blancs, documenté par le Rapport ONU sur le racisme systémique en 2021",
                    "Discrimination raciale institutionnalisée — le ciblage racial par la police américaine viole le 14e Amendement et les obligations des États-Unis sous la Convention CERD, créant une inégalité devant la loi basée sur la race",
                    "Activer le Comité CERD pour examen de la brutalité policière raciale aux États-Unis et soutenir les réformes systémiques d'accountability policière incluant caméras-corps, interdiction des prises d'étranglement et formations anti-biais",
                ],
            ),
            PoliceBrutalityEntity(
                "PB-004",
                "Iran/IRGC — Manifestations Mahsa Amini 500+ Morts & Basij Tirs Basse Altitude",
                "MENA",
                "Mahsa Amini Mort Garde Morale 2022, 500+ Manifestants Tués IRGC/Basij, Plombs Visage/Yeux Tirs Délibérés & Répression 15 000+ Arrestations Vagues",
                85, 82, 88, 80,
                "critique", "repression_protestataires",
                [
                    "Répression violente des protestations en Iran/IRGC — 500+ manifestants tués après la mort de Mahsa Amini avec des tirs délibérés de plombs au niveau des yeux par le Basij, documentés comme violations graves des droits humains",
                    "Répression étatique des droits fondamentaux — la violence contre les manifestants iraniens viole les droits à la vie, à la liberté d'expression et d'assemblée garantis par le PIDCP ratifié par l'Iran",
                    "Activer la Mission internationale d'établissement des faits ONU sur les manifestations iraniennes et poursuivre les responsables des tirs létaux et non-létaux contre les manifestants pacifiques",
                ],
            ),
            PoliceBrutalityEntity(
                "PB-005",
                "Kenya/GSU — Manifestations Juin 2024, 50+ Morts & Tirs Réels Manifestants Pacifiques",
                "Afrique de l'Est",
                "Kenya Manifestations Génération Z Juin 2024, 50+ Morts GSU Tirs Réels, Parlement Envahi Impunité Policière & IPOA Enquête Indépendante Demandée",
                55, 52, 55, 50,
                "élevé", "impunite_policiers_accountability",
                [
                    "Impunité policière au Kenya — 50+ manifestants tués lors des protestations anti-fiscal de juin 2024 avec des tirs réels contre des manifestants pacifiques par la General Service Unit sans accountabilité immédiate",
                    "Violation du droit à la vie — l'usage de tirs réels contre des manifestants pacifiques viole le Principe Directeur ONU sur l'Usage de la Force et les obligations du Kenya sous le PIDCP",
                    "Activer l'IPOA pour enquête indépendante sur les meurtres de manifestants kenyans de juin 2024 et mettre en place des réformes d'accountability policière conformes aux Standards Minimum ONU",
                ],
            ),
            PoliceBrutalityEntity(
                "PB-006",
                "France/LBD — Gilets Jaunes 25+ Yeux Perdus, LBD40 Controversé & IGPN Insuffisante",
                "Europe",
                "Gilets Jaunes 25+ Manifestants Yeux Perdus LBD40, 5+ Mains Arrachées Grenades, IGPN 0 Poursuites Agents & Comité ONU CAT France Violences Policières 2022",
                48, 55, 50, 52,
                "élevé", "repression_protestataires",
                [
                    "Répression violente des protestations en France/LBD — 25+ manifestants gilets jaunes ayant perdu un œil suite aux tirs de LBD40, 5+ mains arrachées par grenades GLI-F4, avec l'IGPN n'ayant conduit à aucune poursuite d'agents",
                    "Violation des standards européens — le Comité ONU contre la Torture a critiqué la France en 2022 pour les violences policières lors des manifestations, soulevant des questions de conformité avec la Convention EDH",
                    "Engager une réforme de l'IGPN vers un contrôle indépendant effectif de la police et suspendre l'usage du LBD40 contre les manifestants conformément aux recommandations du Comité des Droits de l'Homme ONU",
                ],
            ),
            PoliceBrutalityEntity(
                "PB-007",
                "Royaume-Uni/Metropolitan — Affaires Wayne Couzens, Sarah Everard & Misogynie Institutionnelle",
                "Europe",
                "Wayne Couzens Policier Violeur Meurtrier 2021, Enquête Casey Misogynie Institutionnelle Met Police, 1 000+ Agents Crimes Sexuels Passé & IOPC Réformes Lentes",
                28, 30, 28, 25,
                "modéré", "impunite_policiers_accountability",
                [
                    "Impunité policière modérée au Royaume-Uni/Metropolitan — rapport Casey révélant misogynie, racisme et homophobie institutionnels dans la Met avec 1 000+ agents ayant des antécédents de crimes sexuels encore en service",
                    "Défaillance systémique d'accountability — l'affaire Couzens illustre l'échec des mécanismes de contrôle interne à détecter et expulser des policiers aux comportements criminels avant qu'ils ne commettent des crimes graves",
                    "Mettre en œuvre intégralement les recommandations du Rapport Casey sur la Metropolitan Police et renforcer l'IOPC pour qu'il devienne un organe de contrôle véritablement indépendant et efficace",
                ],
            ),
            PoliceBrutalityEntity(
                "PB-008",
                "IPCC/ONU — Principes Fondamentaux Usage Force & Mécanismes Accountability Policière",
                "Global",
                "Principes Fondamentaux ONU Usage Force Armes Feu 1990, Protocole Minnesota Meurtres, Code Conduite Police ONU & Rapporteur Spécial Exécutions Extrajudiciaires",
                5, 4, 3, 6,
                "faible", "impunite_policiers_accountability",
                [
                    "IPCC/ONU incarnent l'accountability policière exemplaire — Principes Fondamentaux ONU sur l'Usage de la Force, Protocole du Minnesota sur les meurtres et Code de Conduite des Nations Unies pour les agents chargés de l'application des lois",
                    "Principes ONU sur l'Usage de la Force (1990) — obligation de nécessité, proportionnalité et précaution dans tout usage de la force par la police, avec responsabilité individuelle et étatique pour les violations",
                    "Universaliser l'application des Principes ONU sur l'Usage de la Force et financer des mécanismes d'accountability policière indépendants dans les pays à haute prévalence de violences policières",
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
            "avg_estimated_police_brutality_index": round(avg / 100 * 10, 2),
        }


if __name__ == "__main__":
    import json
    engine = PoliceBrutalityEngine()
    result = engine.summary()
    print(json.dumps({
        "domain": result["domain"],
        "total": result["total_entities"],
        "avg_composite": result["avg_composite"],
        "risk_distribution": result["risk_distribution"],
        "top_risk_entities": result["top_risk_entities"],
    }, indent=2, ensure_ascii=False))
