from dataclasses import dataclass, field
from typing import List, Dict, Optional
import statistics


@dataclass
class IndigenousLandRightsTerritoralSovereigntyEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    land_dispossession_territorial_erasure_score: float = 0.0
    free_prior_informed_consent_violation_score: float = 0.0
    indigenous_defender_criminalization_score: float = 0.0
    legal_land_title_recognition_deficit_score: float = 0.0
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: List[str] = field(init=False)
    estimated_indigenous_land_rights_territorial_sovereignty_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.land_dispossession_territorial_erasure_score * 0.30 +
            self.free_prior_informed_consent_violation_score * 0.25 +
            self.indigenous_defender_criminalization_score * 0.25 +
            self.legal_land_title_recognition_deficit_score * 0.20, 2
        )
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"

        patterns_map = {
            "depossession_fonciere_effacement_territorial": self.land_dispossession_territorial_erasure_score,
            "violation_consentement_libre_prealable_eclaire": self.free_prior_informed_consent_violation_score,
            "criminalisation_defenseurs_autochtones": self.indigenous_defender_criminalization_score,
            "deficit_reconnaissance_titre_foncier_legal": self.legal_land_title_recognition_deficit_score,
        }
        self.primary_pattern = max(patterns_map, key=lambda k: patterns_map[k])

        self.key_signals = self._generate_signals()
        self.estimated_indigenous_land_rights_territorial_sovereignty_index = round(
            self.composite_score / 100 * 10, 2
        )

    def _generate_signals(self) -> List[str]:
        signals = []
        if self.land_dispossession_territorial_erasure_score >= 60:
            signals.append(
                f"Dépossession foncière massive et effacement territorial à {self.name} — "
                f"accaparement systématique des terres ancestrales autochtones par des acteurs "
                f"étatiques et corporatifs, en violation de la Déclaration ONU sur les Droits "
                f"des Peuples Autochtones (UNDRIP 2007) et du droit coutumier international "
                f"reconnaissant la souveraineté territoriale des peuples premiers"
            )
        elif self.land_dispossession_territorial_erasure_score >= 40:
            signals.append(
                f"Pression foncière significative sur les terres autochtones à {self.name} — "
                f"empiètements progressifs par projets extractifs et agricoles menaçant "
                f"l'intégrité territoriale et les modes de vie traditionnels des communautés"
            )
        if self.free_prior_informed_consent_violation_score >= 60:
            signals.append(
                f"Violations systématiques du Consentement Libre, Préalable et Éclairé (CLPE) — "
                f"projets miniers, pétroliers et forestiers imposés sans consultation authentique "
                f"des peuples autochtones concernés, contrevenant directement aux articles 10, "
                f"19 et 32 de l'UNDRIP et aux Principes Directeurs de l'ONU sur les Entreprises "
                f"et les Droits de l'Homme"
            )
        if self.indigenous_defender_criminalization_score >= 60:
            signals.append(
                f"Criminalisation et assassinats de défenseurs autochtones des terres — "
                f"les militants autochtones qui défendent leurs territoires font face à des "
                f"arrestations arbitraires, des poursuites judiciaires abusives et des assassinats "
                f"documentés par Global Witness, constituant une attaque directe contre le droit "
                f"à défendre les droits humains reconnu par la résolution ONU 53/144"
            )
        if self.legal_land_title_recognition_deficit_score >= 40:
            signals.append(
                f"Déficit de reconnaissance légale des titres fonciers autochtones — l'absence "
                f"de cadres juridiques effectifs pour la reconnaissance et la protection des droits "
                f"territoriaux ancestraux laisse les communautés autochtones sans protection contre "
                f"l'accaparement des terres et l'exploitation des ressources naturelles sans consentement"
            )
        if not signals:
            signals.append(
                f"Mécanismes partiels de protection des droits fonciers autochtones à {self.name} — "
                f"progrès institutionnels avec lacunes persistantes dans l'application effective"
            )
        return signals[:3]

    def to_dict(self) -> Dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "land_dispossession_territorial_erasure_score": self.land_dispossession_territorial_erasure_score,
            "free_prior_informed_consent_violation_score": self.free_prior_informed_consent_violation_score,
            "indigenous_defender_criminalization_score": self.indigenous_defender_criminalization_score,
            "legal_land_title_recognition_deficit_score": self.legal_land_title_recognition_deficit_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_indigenous_land_rights_territorial_sovereignty_index": self.estimated_indigenous_land_rights_territorial_sovereignty_index,
            "last_updated": self.last_updated,
        }


class IndigenousLandRightsTerritoralSovereigntyEngine:
    ENGINE_VERSION = "1.0.0"
    DOMAIN = "indigenous_land_rights_territorial_sovereignty"

    def __init__(self):
        self.entities = self._load_entities()

    def _load_entities(self) -> List[IndigenousLandRightsTerritoralSovereigntyEntity]:
        return [
            IndigenousLandRightsTerritoralSovereigntyEntity(
                entity_id="ILRTS-001",
                name="Brésil/Amazonie Garimpeiros Invasion",
                country="Amérique du Sud",
                sector="20 000+ Garimpeiros Envahissent Territoires Yanomami, Mercure Contamination, 570 Morts Évitables 2022 & Démarcation Terres Bloquée Bolsonaro Era",
                land_dispossession_territorial_erasure_score=90.0,
                free_prior_informed_consent_violation_score=88.0,
                indigenous_defender_criminalization_score=85.0,
                legal_land_title_recognition_deficit_score=82.0,
            ),
            IndigenousLandRightsTerritoralSovereigntyEntity(
                entity_id="ILRTS-002",
                name="Philippines/Lumad Mindanao Déplacement",
                country="Asie du Sud-Est",
                sector="Lumad Mindanao Déplacements Forcés Opérations Militaires, Écoles Fermées Armée, 2 000 Défenseurs Menacés & Mines Agribusiness Sans Consentement",
                land_dispossession_territorial_erasure_score=85.0,
                free_prior_informed_consent_violation_score=82.0,
                indigenous_defender_criminalization_score=88.0,
                legal_land_title_recognition_deficit_score=80.0,
            ),
            IndigenousLandRightsTerritoralSovereigntyEntity(
                entity_id="ILRTS-003",
                name="Honduras/Lenca Cáceres Assassinats",
                country="Amérique Centrale",
                sector="Berta Cáceres Assassinée 2016, Plus Meurtres Défenseurs/Capita Monde, Barrage Agua Zarca Sans CLPE & Impunité Systémique Assassins",
                land_dispossession_territorial_erasure_score=88.0,
                free_prior_informed_consent_violation_score=80.0,
                indigenous_defender_criminalization_score=90.0,
                legal_land_title_recognition_deficit_score=75.0,
            ),
            IndigenousLandRightsTerritoralSovereigntyEntity(
                entity_id="ILRTS-004",
                name="Canada/Réconciliation Défaillante",
                country="Amérique du Nord",
                sector="94 Appels Action CVR Non Complétés, Pipelines Trans Mountain Sans Consentement, Disparitions Femmes Autochtones & Eau Potable 34 Avis Longue Durée",
                land_dispossession_territorial_erasure_score=72.0,
                free_prior_informed_consent_violation_score=75.0,
                indigenous_defender_criminalization_score=68.0,
                legal_land_title_recognition_deficit_score=70.0,
            ),
            IndigenousLandRightsTerritoralSovereigntyEntity(
                entity_id="ILRTS-005",
                name="Australie/Terra Nullius Héritage Spoliation",
                country="Océanie",
                sector="Terra Nullius Doctrine Héritage, Native Title Act 1993 Partiel, Mining Veto Aboli 1998 & Closing the Gap Inégalités Persistantes Terres",
                land_dispossession_territorial_erasure_score=52.0,
                free_prior_informed_consent_violation_score=55.0,
                indigenous_defender_criminalization_score=48.0,
                legal_land_title_recognition_deficit_score=50.0,
            ),
            IndigenousLandRightsTerritoralSovereigntyEntity(
                entity_id="ILRTS-006",
                name="Pérou/Extractivisme Amazonie CLPE",
                country="Amérique du Sud",
                sector="Loi Consulta Previa 2011 Faible Application, Concessions Minières Pétrolières Sans Consentement, Défenseurs Menacés & Conflits Socio-Environnementaux",
                land_dispossession_territorial_erasure_score=48.0,
                free_prior_informed_consent_violation_score=50.0,
                indigenous_defender_criminalization_score=55.0,
                legal_land_title_recognition_deficit_score=45.0,
            ),
            IndigenousLandRightsTerritoralSovereigntyEntity(
                entity_id="ILRTS-007",
                name="Nouvelle-Zélande/Traité Waitangi Partiel",
                country="Océanie",
                sector="Traité Waitangi 1840 Reconnaissance Partielle, Tribunal Waitangi Recommandations Non Contraignantes, Confiscations Terres Maori Partiellement Réparées",
                land_dispossession_territorial_erasure_score=25.0,
                free_prior_informed_consent_violation_score=28.0,
                indigenous_defender_criminalization_score=20.0,
                legal_land_title_recognition_deficit_score=22.0,
            ),
            IndigenousLandRightsTerritoralSovereigntyEntity(
                entity_id="ILRTS-008",
                name="Finlande/Sámi Parlement Consultatif",
                country="Europe du Nord",
                sector="Parlement Sámi Consultatif Sans Droit Veto, Loi Sámi 2023 Adoptée, ILO 169 Non Ratifié & Droits Pêche Reindeer Partiellement Protégés",
                land_dispossession_territorial_erasure_score=5.0,
                free_prior_informed_consent_violation_score=8.0,
                indigenous_defender_criminalization_score=4.0,
                legal_land_title_recognition_deficit_score=6.0,
            ),
        ]

    def analyze(self) -> Dict:
        results = [e.to_dict() for e in self.entities]
        scores = [e.composite_score for e in self.entities]
        avg_composite = round(statistics.mean(scores), 2)
        risk_dist = {}
        pattern_dist = {}
        for e in self.entities:
            risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
            pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1

        top_risk = sorted(self.entities, key=lambda e: e.composite_score, reverse=True)[:4]
        critical_alerts = [
            f"{e.name}: {e.primary_pattern}" for e in self.entities if e.risk_level == "critique"
        ]
        avg_index = round(avg_composite / 100 * 10, 2)

        return {
            "total_entities": len(results),
            "avg_composite": avg_composite,
            "risk_distribution": risk_dist,
            "pattern_distribution": pattern_dist,
            "top_risk_entities": [e.name for e in top_risk],
            "critical_alerts": critical_alerts,
            "last_analysis": "2026-06-21",
            "engine_version": self.ENGINE_VERSION,
            "domain": self.DOMAIN,
            "confidence_score": 0.88,
            "data_sources": [
                "un_special_rapporteur_indigenous_peoples_2023",
                "forest_peoples_programme_land_rights_2023",
                "global_witness_land_defenders_killed_2023",
                "cultural_survival_quarterly_indigenous_land_2023",
            ],
            "entities": results,
            "avg_estimated_indigenous_land_rights_territorial_sovereignty_index": avg_index,
        }


def run_indigenous_land_rights_territorial_sovereignty_engine() -> Dict:
    engine = IndigenousLandRightsTerritoralSovereigntyEngine()
    return engine.analyze()


if __name__ == "__main__":
    import json
    engine = IndigenousLandRightsTerritoralSovereigntyEngine()
    result = engine.analyze()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nAvg composite: {result['avg_composite']}")
    print(f"Risk distribution: {result['risk_distribution']}")
