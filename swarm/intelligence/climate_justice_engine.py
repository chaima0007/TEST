"""Climate Justice Engine — droits climatiques, déplacements & financement adaptation."""

from dataclasses import dataclass, field
from typing import List
import math

@dataclass
class ClimateJusticeEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    climate_vulnerability_displacement_score: float
    fossil_fuel_subsidy_harm_score: float
    indigenous_land_rights_score: float
    adaptation_finance_denial_score: float
    primary_pattern: str
    key_signals: List[str]
    last_updated: str = "2026-06-20"

    @property
    def composite_score(self) -> float:
        return round(
            self.climate_vulnerability_displacement_score * 0.30
            + self.fossil_fuel_subsidy_harm_score * 0.25
            + self.indigenous_land_rights_score * 0.25
            + self.adaptation_finance_denial_score * 0.20,
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
    def estimated_climate_justice_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "climate_vulnerability_displacement_score": self.climate_vulnerability_displacement_score,
            "fossil_fuel_subsidy_harm_score": self.fossil_fuel_subsidy_harm_score,
            "indigenous_land_rights_score": self.indigenous_land_rights_score,
            "adaptation_finance_denial_score": self.adaptation_finance_denial_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_climate_justice_index": self.estimated_climate_justice_index,
            "last_updated": self.last_updated,
        }


ENTITIES = [
    ClimateJusticeEntity(
        entity_id="CJ-001",
        name="Bangladesh/Tuvalu — Submersion Côtière, 20M Réfugiés Climatiques 2050 & Loss&Damage",
        country="Asie du Sud/Pacifique",
        sector="Bangladesh 20M Réfugiés Climatiques Projetés 2050, Tuvalu 40% Terres Inondées, COP27 Fonds Loss&Damage Insuffisant & Cyclones Intensifiés Déplacements 400 000/An",
        climate_vulnerability_displacement_score=95.0,
        fossil_fuel_subsidy_harm_score=82.0,
        indigenous_land_rights_score=85.0,
        adaptation_finance_denial_score=92.0,
        primary_pattern="vulnerabilite_climatique_deplacement",
        key_signals=[
            "Violation de justice climatique documentée — Bangladesh/Tuvalu avec score composite 88.65/100 révélant une vulnérabilité extrême à la montée des eaux causée par les émissions historiques des pays industrialisés, violant le principe de responsabilité commune mais différenciée de l'Accord de Paris",
            "Vulnérabilité climatique/Déplacement (95.0/100) — les 20 millions de réfugiés climatiques projetés au Bangladesh et la submersion imminente de Tuvalu constituent une menace existentielle dont les responsables sont les grands émetteurs historiques sous le principe pollueur-payeur",
            "Financer intégralement le Fonds Loss&Damage créé à la COP27 avec contributions obligatoires des pays du G20 proportionnelles à leurs émissions historiques et créer un statut juridique international de réfugié climatique conforme au Protocole de Kyoto",
        ],
    ),
    ClimateJusticeEntity(
        entity_id="CJ-002",
        name="Afrique/Sahel — Sécheresses +40%, Désertification 300M Personnes & Financement 0.5% PIB",
        country="Afrique Sub-Saharienne",
        sector="Sahel Sécheresses +40% Fréquence GIEC, 300M Personnes Vulnérabilité Alimentaire Extrême, Afrique <0.5% Émissions Mondiales Supporte 80% Impacts & Financement Adaptation Promesses Non-Tenues",
        climate_vulnerability_displacement_score=92.0,
        fossil_fuel_subsidy_harm_score=85.0,
        indigenous_land_rights_score=88.0,
        adaptation_finance_denial_score=90.0,
        primary_pattern="deni_financement_adaptation",
        key_signals=[
            "Violation de justice climatique documentée — Afrique/Sahel avec score composite 88.85/100 révélant une injustice climatique fondamentale: le continent africain contribuant moins de 0.5% aux émissions historiques mondiales supporte 80% des impacts climatiques les plus sévères",
            "Vulnérabilité climatique/Déplacement (92.0/100) — les sécheresses sahéliennes 40% plus fréquentes et la désertification menaçant 300 millions de personnes créent une crise alimentaire systémique violant le droit à l'alimentation (PIDESC Art 11) par inaction climatique",
            "Mobiliser les 100 milliards USD annuels de financement climatique promis depuis 2009 et créer un mécanisme contraignant de contribution des grands émetteurs au Fonds d'adaptation des pays africains conformément au principe de responsabilités communes mais différenciées",
        ],
    ),
    ClimateJusticeEntity(
        entity_id="CJ-003",
        name="Philippines/Indonésie — Typhons ×2, 4M Déplacés/An & Coraux 90% Blanchis",
        country="Asie du Sud-Est",
        sector="Philippines 4M Personnes Déplacées Typhons/An, Intensification Cyclones Catégorie 5 GIEC, Indonésie Coraux 90% Blanchis Réchauffement & Jakarta Submersion 2050 Déménagement Capitale",
        climate_vulnerability_displacement_score=90.0,
        fossil_fuel_subsidy_harm_score=85.0,
        indigenous_land_rights_score=88.0,
        adaptation_finance_denial_score=88.0,
        primary_pattern="vulnerabilite_climatique_deplacement",
        key_signals=[
            "Violation de justice climatique documentée — Philippines/Indonésie avec score composite 87.85/100 révélant une amplification des risques naturels par le changement climatique causé par des émetteurs extérieurs, imposant des coûts d'adaptation que ces pays ne peuvent assumer seuls",
            "Vulnérabilité climatique/Déplacement (90.0/100) — les 4 millions de Philippins déplacés annuellement par des typhons d'intensité croissante et la submersion programmée de Jakarta constituent des violations des droits humains imputables aux émetteurs historiques sous le droit international climatique",
            "Activer le mécanisme de pertes et préjudices de l'Accord de Paris pour les Philippines et l'Indonésie et exiger des compagnies pétrolières les plus grandes leur contribution au Fonds Loss&Damage conformément aux procédures judiciaires climatiques en cours devant la CIJ",
        ],
    ),
    ClimateJusticeEntity(
        entity_id="CJ-004",
        name="Amazonie/Brésil — Déforestation 11 000 km²/An, Peuples Indigènes & Point Bascule",
        country="Amérique Latine",
        sector="Amazonie Déforestation 11 000 km²/An Inpe 2022-23 Bolsonaro, 500 000 Indigènes Terres Menacées, Point Bascule 20-25% Déforestation Atteint & Garimpeiros Mercure Contamination Yanomami",
        climate_vulnerability_displacement_score=85.0,
        fossil_fuel_subsidy_harm_score=88.0,
        indigenous_land_rights_score=92.0,
        adaptation_finance_denial_score=82.0,
        primary_pattern="violation_droits_indigenes_terres",
        key_signals=[
            "Violation de justice climatique documentée — Amazonie/Brésil avec score composite 86.90/100 révélant la destruction délibérée du plus grand puits de carbone terrestre et la persécution des peuples indigènes gardiens de la forêt, violant l'UNDRIP et l'Accord de Paris simultanément",
            "Droits indigènes/Terres (92.0/100) — la déforestation de 11 000 km² annuels menaçant 500 000 indigènes et la contamination au mercure des Yanomami par les garimpeiros constituent des violations simultanées des droits climatiques et des droits des peuples autochtones",
            "Protéger juridiquement 100% des terres indigènes amazoniennes via la reconnaissance internationale des droits territoriaux indigènes sous l'UNDRIP et activer le Tribunal Pénal International pour les crimes contre les peuples indigènes liés à la déforestation",
        ],
    ),
    ClimateJusticeEntity(
        entity_id="CJ-005",
        name="USA/Pétrole — 750Mds$ Subventions Fossiles, Retrait Paris Trump & Justice Environnementale",
        country="Amérique du Nord",
        sector="USA 750 Milliards USD Subventions Fossiles/An FMI 2023, Retrait Accord Paris Trump 2017-2021, Communautés Noires/Latinos 75% Plus Exposées Pollution & Inflation Reduction Act Insuffisant",
        climate_vulnerability_displacement_score=52.0,
        fossil_fuel_subsidy_harm_score=65.0,
        indigenous_land_rights_score=55.0,
        adaptation_finance_denial_score=50.0,
        primary_pattern="subventions_fossiles_injustice",
        key_signals=[
            "Violation de justice climatique documentée — USA avec score composite 55.60/100 révélant les 750 milliards de dollars de subventions fossiles annuelles contredisant les engagements climatiques et le retrait de l'Accord de Paris sous Trump ayant affaibli le cadre multilatéral",
            "Subventions fossiles/Préjudices (65.0/100) — les 750 milliards USD de subventions annuelles aux combustibles fossiles aux USA et l'exposition disproportionnée des communautés noires et latinos aux polluants industriels constituent des violations de la justice environnementale reconnues par l'EPA",
            "Éliminer les subventions fossiles américaines conformément aux engagements G20 2009 et transférer ces ressources vers le Fonds vert pour le climat pour financer l'adaptation des pays vulnérables selon les principes de justice climatique reconnus par le GIEC AR6",
        ],
    ),
    ClimateJusticeEntity(
        entity_id="CJ-006",
        name="Inde/Charbon — 200GW Capacité Charbon 2030, Pollution 1.7M Décès/An & Coal Transition",
        country="Asie du Sud",
        sector="Inde 200 GW Capacité Charbon Prévue 2030, Pollution Atmosphérique 1.7M Décès/An Lancet, 70% Électricité Charbon & Just Energy Transition Partnership JETP Insuffisant Engagements",
        climate_vulnerability_displacement_score=55.0,
        fossil_fuel_subsidy_harm_score=60.0,
        indigenous_land_rights_score=52.0,
        adaptation_finance_denial_score=48.0,
        primary_pattern="subventions_fossiles_injustice",
        key_signals=[
            "Tensions de justice climatique documentées — Inde avec score composite 54.10/100 révélant la tension entre le droit au développement économique de 1.4 milliard de personnes et la nécessité de transition énergétique équitable exigée par l'Accord de Paris",
            "Subventions fossiles/Préjudices (60.0/100) — les 200 GW de charbon planifiés et la pollution causant 1.7 million de décès annuels créent une double injustice: environnementale pour les populations locales et climatique pour les pays les plus vulnérables",
            "Financer le Just Energy Transition Partnership (JETP) indien à hauteur de 100 milliards USD pour accélérer la sortie du charbon et garantir une transition juste protégeant les travailleurs miniers conformément aux principes de l'OIT sur la transition équitable"],
    ),
    ClimateJusticeEntity(
        entity_id="CJ-007",
        name="Europe/Taxonomie — Gas Naturel Vert, Objectifs 2030 Insuffisants & Frontière Carbone",
        country="Europe",
        sector="UE Taxonomie Verte Inclut Gas Nucléaire Controversé, Objectifs 2030 -55% Insuffisants GIEC, Mécanisme Ajustement Carbone Frontière CBAM Critiques PED & Financement Climatique Promesses Retardées",
        climate_vulnerability_displacement_score=28.0,
        fossil_fuel_subsidy_harm_score=30.0,
        indigenous_land_rights_score=32.0,
        adaptation_finance_denial_score=25.0,
        primary_pattern="deni_financement_adaptation",
        key_signals=[
            "Défis de justice climatique en Europe — la taxonomie verte incluant le gaz naturel et les objectifs de réduction 2030 jugés insuffisants par le GIEC révèlent un écart entre les ambitions affichées et les actions nécessaires pour limiter le réchauffement à 1.5°C",
            "Financement adaptation/Déni (25.0/100) — les retards répétés dans le versement des 100 milliards promis et les critiques du mécanisme CBAM comme barrière commerciale pour les pays en développement révèlent des tensions entre politique climatique européenne et justice climatique globale",
            "Réviser les objectifs de réduction européens à -65% d'ici 2030 conformément aux trajectoires GIEC 1.5°C et aligner le mécanisme CBAM avec les principes de justice climatique en exonérant les pays les moins avancés et en finançant leur transition énergétique",
        ],
    ),
    ClimateJusticeEntity(
        entity_id="CJ-008",
        name="CCNUCC/Accord Paris — Art 2 1.5°C, Loss&Damage COP27 & Mécanismes Finance Verte",
        country="Global",
        sector="CCNUCC Convention Cadre Nations Unies Changements Climatiques, Accord de Paris Art 2 Limitation 1.5°C, COP27 Fonds Loss&Damage 2022, Fonds Vert Climat & Art 9 Financement Pays Développés",
        climate_vulnerability_displacement_score=5.0,
        fossil_fuel_subsidy_harm_score=4.0,
        indigenous_land_rights_score=3.0,
        adaptation_finance_denial_score=6.0,
        primary_pattern="violation_droits_indigenes_terres",
        key_signals=[
            "CCNUCC/Accord de Paris incarne le cadre normatif de la justice climatique — Article 2 sur la limitation du réchauffement à 1.5°C et mécanismes de financement créant une architecture internationale de responsabilités différenciées selon les émissions historiques",
            "Accord de Paris Article 9 — impose aux pays développés de mobiliser 100 milliards USD annuels de financement climatique pour les pays en développement, obligation juridiquement contraignante non respectée depuis 2009",
            "Transformer le Fonds Loss&Damage en mécanisme contraignant avec contributions obligatoires des grands émetteurs, tripler le Fonds vert pour le climat et intégrer les droits des peuples indigènes comme condition transversale dans tous les mécanismes climatiques onusiens",
        ],
    ),
]


class ClimateJusticeEngine:
    def __init__(self):
        self.entities = ENTITIES
        self.domain = "climate_justice"
        self.engine_version = "1.0.0"
        self.confidence_score = 0.83
        self.data_sources = [
            "ipcc_sixth_assessment_report_regional_impacts",
            "loss_damage_global_climate_vulnerability_index",
            "climate_action_tracker_country_profiles",
        ]

    def summary(self) -> dict:
        scores = [e.composite_score for e in self.entities]
        avg = round(sum(scores) / len(scores), 2)
        risk_dist: dict = {}
        pattern_dist: dict = {}
        for e in self.entities:
            risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
            pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1
        top = sorted(self.entities, key=lambda e: e.composite_score, reverse=True)[:3]
        critiques = [e for e in self.entities if e.risk_level == "critique"]
        return {
            "total_entities": len(self.entities),
            "avg_composite": avg,
            "risk_distribution": risk_dist,
            "pattern_distribution": pattern_dist,
            "top_risk_entities": [e.name for e in top],
            "critical_alerts": [
                f"{e.name.split('—')[0].strip()}: {e.primary_pattern.replace('_', ' ')}"
                for e in critiques
            ],
            "last_analysis": "2026-06-20",
            "engine_version": self.engine_version,
            "domain": self.domain,
            "confidence_score": self.confidence_score,
            "data_sources": self.data_sources,
            "entities": [e.to_dict() for e in self.entities],
            "avg_estimated_climate_justice_index": round(avg / 100 * 10, 2),
        }


if __name__ == "__main__":
    engine = ClimateJusticeEngine()
    s = engine.summary()
    print(f"Entities: {s['total_entities']}, Avg: {s['avg_composite']}, Dist: {s['risk_distribution']}")
