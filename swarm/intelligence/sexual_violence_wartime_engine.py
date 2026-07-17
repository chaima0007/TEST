from datetime import date


class SexualViolenceWartimeEntity:
    def __init__(self, entity_id, name, country, sector,
                 systematic_rape_targeting_score,
                 state_actor_perpetration_score,
                 survivor_access_justice_score,
                 conflict_zone_impunity_score,
                 risk_level, primary_pattern, key_signals, last_updated=None):
        self.entity_id = entity_id
        self.name = name
        self.country = country
        self.sector = sector
        self.systematic_rape_targeting_score = systematic_rape_targeting_score
        self.state_actor_perpetration_score = state_actor_perpetration_score
        self.survivor_access_justice_score = survivor_access_justice_score
        self.conflict_zone_impunity_score = conflict_zone_impunity_score
        self.composite_score = round(
            systematic_rape_targeting_score * 0.30 +
            state_actor_perpetration_score * 0.25 +
            survivor_access_justice_score * 0.25 +
            conflict_zone_impunity_score * 0.20, 2
        )
        self.risk_level = risk_level
        self.primary_pattern = primary_pattern
        self.key_signals = key_signals
        self.estimated_sexual_violence_wartime_index = round(self.composite_score / 100 * 10, 2)
        self.last_updated = last_updated or str(date.today())

    def to_dict(self):
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "systematic_rape_targeting_score": self.systematic_rape_targeting_score,
            "state_actor_perpetration_score": self.state_actor_perpetration_score,
            "survivor_access_justice_score": self.survivor_access_justice_score,
            "conflict_zone_impunity_score": self.conflict_zone_impunity_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_sexual_violence_wartime_index": self.estimated_sexual_violence_wartime_index,
            "last_updated": self.last_updated,
        }


class SexualViolenceWartimeEngine:
    VERSION = "1.0.0"
    CONFIDENCE = 0.83
    DOMAIN = "sexual_violence_wartime"
    DATA_SOURCES = [
        "un_osrsg_svc_annual_reports",
        "hrw_sexual_violence_conflict_reports",
        "icrc_women_war_protection_database",
    ]

    def __init__(self):
        self.entities = self._build_entities()

    def _build_entities(self):
        return [
            SexualViolenceWartimeEntity(
                "SV-001",
                "DRC/Est Congo — 200 000+ Victimes Viol Systématique & Capitale Mondiale Viol Conflit",
                "Afrique Centrale",
                "200 000+ Victimes Viol Documentées Est Congo 1996-2024, Dr Denis Mukwege Nobel Paix, FARDC/Maï-Maï/M23 Auteurs & Viol Outil Domination Territoriale",
                95, 88, 90, 92,
                "critique", "viol_arme_guerre_systematique",
                [
                    "Viol comme arme de guerre systématique en DRC/Est Congo — 200 000+ victimes documentées depuis 1996 faisant de l'Est du Congo la 'capitale mondiale du viol' selon l'ONU, avec FARDC, Maï-Maï et M23 comme auteurs identifiés",
                    "Crime de guerre et crime contre l'humanité — le viol systématique en temps de conflit constitue un crime de guerre selon l'Article 8 du Statut de Rome et l'ONU a qualifié les actes en RDC de crime contre l'humanité dès 2010",
                    "Activer la Résolution CS-ONU 1820 sur les violences sexuelles en conflit et renforcer le mandat de la Représentante Spéciale ONU (OSRSG-SVC) pour accès humanitaire d'urgence aux survivantes en RDC",
                ],
            ),
            SexualViolenceWartimeEntity(
                "SV-002",
                "Syrie/Assad — Viol Torture Prisons, 6 000+ Victimes Détention & Impunité Totale",
                "MENA",
                "6 000+ Victimes Violences Sexuelles Détention Assad Documentées ONU, Sednaya Viol Systématique, Hommes/Femmes/Enfants & Commission Enquête CS-ONU Preuves",
                92, 95, 88, 90,
                "critique", "ciblage_etatique_violences_sexuelles",
                [
                    "Ciblage étatique des violences sexuelles en Syrie/Assad — 6 000+ victimes documentées de violences sexuelles dans les centres de détention syriens, utilisées comme outil de torture et de terreur par des agents de l'État",
                    "Crime contre l'humanité commis par des agents étatiques — la Commission d'Enquête ONU sur la Syrie a documenté des preuves suffisantes de violences sexuelles systématiques qualifiables de crimes contre l'humanité selon le Statut de Rome",
                    "Activer le mécanisme international IIIM pour préserver les preuves et poursuivre les responsables des violences sexuelles dans les prisons syriennes, en priorité ceux identifiés par la Commission d'Enquête ONU",
                ],
            ),
            SexualViolenceWartimeEntity(
                "SV-003",
                "Bosnie/Serbie — Camps Viol 1992-95, 20 000-50 000 Victimes & TPIY Jurisprudence",
                "Europe de l'Est",
                "Camps Viol Foča/Prijedor 1992-95, 20 000-50 000 Victimes Estimées, TPIY Première Condamnation Viol Crime Guerre 1998 & Kunarac Précédent Juridique Historique",
                88, 85, 82, 88,
                "critique", "viol_arme_guerre_systematique",
                [
                    "Viol comme arme de guerre systématique en Bosnie/Serbie — 20 000 à 50 000 victimes dans les camps de viol de Foča et Prijedor entre 1992 et 1995, première qualification de viol comme crime de guerre par le TPIY en 1998 (affaire Kunarac)",
                    "Jurisprudence fondatrice — la condamnation Kunarac par le TPIY en 2001 a établi que le viol peut constituer un crime contre l'humanité quand utilisé de façon systématique comme outil de nettoyage ethnique",
                    "Honorer la jurisprudence TPIY sur les violences sexuelles et soutenir les organisations de survivantes bosniaques qui continuent de demander justice et réparation pour les crimes des années 1990",
                ],
            ),
            SexualViolenceWartimeEntity(
                "SV-004",
                "Myanmar/Rohingya — Viol Systématique 2017 Opération Clearance & CIJ/ICC Procédures",
                "Asie du Sud-Est",
                "Tatmadaw Viol Systématique Rohingya Femmes 2017, Témoignages 1 000+ Victimes ONU, Villages Brûlés Après Viol & Factfinding Mission 2018 Crimes Contre Humanité",
                85, 90, 85, 82,
                "critique", "ciblage_etatique_violences_sexuelles",
                [
                    "Ciblage étatique des violences sexuelles au Myanmar/Rohingya — Tatmadaw utilisant le viol systématique comme arme pendant l'opération Clearance de 2017 avec 1 000+ témoignages documentés et villages brûlés après les assauts",
                    "Crime contre l'humanité et élément de génocide — la Mission d'établissement des faits ONU 2018 a conclu que les violences sexuelles de la Tatmadaw constituent des crimes contre l'humanité avec intent génocidaire",
                    "Soutenir les procédures CIJ/CPI contre le Myanmar pour violences sexuelles et assurer l'accès aux soins et à la justice pour les survivantes rohingya réfugiées au Bangladesh",
                ],
            ),
            SexualViolenceWartimeEntity(
                "SV-005",
                "Inde/Manipur — Violences Sexuelles Communautaires 2023, Vidéos Virales & Impunité",
                "Asie du Sud",
                "Manipur 2023 Violences Sexuelles Communautaires Kuki-Zo/Meitei, Vidéos Défilé Forcé Virales, Arrestations Tardives Pression Internationale & Droits Humains Inquiétudes",
                55, 52, 58, 52,
                "élevé", "impunite_agresseurs_conflit",
                [
                    "Impunité des agresseurs en conflit Inde/Manipur — violences sexuelles communautaires filmées viralisées en 2023 lors des violences inter-ethniques Kuki-Zo/Meitei, avec arrestations des agresseurs seulement après pression internationale",
                    "Lacune dans la protection — les violences sexuelles lors de conflits communautaires en Inde révèlent des défaillances dans la protection des femmes des minorités et l'absence de réponse préventive de l'État",
                    "Accélérer les poursuites judiciaires contre tous les responsables des violences de Manipur et mettre en œuvre les recommandations de la Rapporteure Spéciale ONU sur les violences contre les femmes",
                ],
            ),
            SexualViolenceWartimeEntity(
                "SV-006",
                "Soudan/RSF — Violences Sexuelles Massives Darfour/Khartoum 2023-24 & Campagnes Viol",
                "Afrique de l'Est",
                "RSF Forces Paramilitaires Viol Systématique Darfour/Khartoum 2023-24, El Fasher Siège Violences Sexuelles, 1 000+ Cas UNFPA & Répétition Crimes Darfour 2003",
                52, 55, 50, 58,
                "élevé", "impunite_agresseurs_conflit",
                [
                    "Impunité des agresseurs au Soudan/RSF — Forces de Soutien Rapide utilisant le viol systématique au Darfour et à Khartoum depuis 2023, répétant le schéma des crimes documentés de 2003 avec 1 000+ cas UNFPA",
                    "Crime de guerre en cours — les violences sexuelles systématiques des RSF au Darfour et à Khartoum constituent des crimes de guerre documentés par l'ONU, exigeant une réponse juridique internationale urgente",
                    "Activer la Résolution CS-ONU 1820 et saisir la CPI pour les violences sexuelles systématiques des RSF au Soudan, en priorité pour les crimes commis à El Fasher et dans le Darfour",
                ],
            ),
            SexualViolenceWartimeEntity(
                "SV-007",
                "Ouganda/LRA — Ex-Esclaves Sexuelles Réintégration & Justice Transitionnelle Défaillante",
                "Afrique de l'Est",
                "LRA 10 000+ Femmes Enlevées Esclaves Sexuelles 1987-2006, Joseph Kony CPI Fugitif, Survivantes Stigmatisation Retour & Programmes Réintégration Insuffisants Ouganda",
                28, 30, 28, 32,
                "modéré", "reintegration_victimes_defaillante",
                [
                    "Réintégration défaillante des victimes en Ouganda/LRA — 10 000+ femmes anciennes esclaves sexuelles du LRA faisant face à stigmatisation sociale et programmes de réintégration insuffisants, pendant que Joseph Kony reste en fuite malgré son mandat CPI depuis 2005",
                    "Justice transitionnelle incomplète — l'absence de capture de Kony et les limites des programmes de réintégration laissent des milliers de survivantes sans accès à la justice et sans réparations adéquates",
                    "Renforcer les programmes de réintégration des survivantes du LRA en Ouganda et intensifier les efforts de coopération internationale pour l'appréhension de Joseph Kony conformément au mandat CPI",
                ],
            ),
            SexualViolenceWartimeEntity(
                "SV-008",
                "OSRSG-SVC/ONU — Résolution 1820 & Criminalisation Violences Sexuelles Conflit",
                "Global",
                "CS-ONU Résolution 1820 2008 Violences Sexuelles Conflit, OSRSG-SVC Mandat, Équipe Experts PSVI & Protocole International Documentation Violences Sexuelles Conflit",
                5, 4, 3, 6,
                "faible", "reintegration_victimes_defaillante",
                [
                    "OSRSG-SVC/ONU incarne la protection exemplaire — Résolution 1820 du Conseil de Sécurité qualifiant les violences sexuelles en conflit de menace à la paix et à la sécurité internationales avec mandat de Représentante Spéciale",
                    "Résolution CS-ONU 1820 (2008) — reconnaissance que le viol et autres formes de violence sexuelle constituent des tactiques de guerre et doivent être traités comme des crimes de guerre et crimes contre l'humanité",
                    "Partager le Protocole International de Documentation des Violences Sexuelles en Conflit et renforcer le financement de l'OSRSG-SVC pour documentation, poursuites et soutien aux survivant(e)s",
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
            "avg_estimated_sexual_violence_wartime_index": round(avg / 100 * 10, 2),
        }


if __name__ == "__main__":
    import json
    engine = SexualViolenceWartimeEngine()
    result = engine.summary()
    print(json.dumps({
        "domain": result["domain"],
        "total": result["total_entities"],
        "avg_composite": result["avg_composite"],
        "risk_distribution": result["risk_distribution"],
        "top_risk_entities": result["top_risk_entities"],
    }, indent=2, ensure_ascii=False))
