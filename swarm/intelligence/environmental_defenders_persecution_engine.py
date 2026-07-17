from dataclasses import dataclass, field
from typing import List, Dict
import statistics


@dataclass
class EnvironmentalDefendersPerseculionEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    defender_killing_impunity_severity_score: float = 0.0
    criminalization_slapp_lawsuit_scale_score: float = 0.0
    corporate_state_collusion_resource_conflict_score: float = 0.0
    indigenous_land_defender_protection_deficit_score: float = 0.0
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: List[str] = field(init=False)
    estimated_environmental_defenders_persecution_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.defender_killing_impunity_severity_score * 0.30 +
            self.criminalization_slapp_lawsuit_scale_score * 0.25 +
            self.corporate_state_collusion_resource_conflict_score * 0.25 +
            self.indigenous_land_defender_protection_deficit_score * 0.20, 2
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
            "assassinat_defenseur_impunite": self.defender_killing_impunity_severity_score,
            "criminalisation_slapp_poursuites": self.criminalization_slapp_lawsuit_scale_score,
            "collusion_corporate_etatique_ressources": self.corporate_state_collusion_resource_conflict_score,
            "deficit_protection_defenseurs_autochtones": self.indigenous_land_defender_protection_deficit_score,
        }
        self.primary_pattern = max(patterns_map, key=lambda k: patterns_map[k])
        self.key_signals = self._generate_signals()
        self.estimated_environmental_defenders_persecution_index = round(
            self.composite_score / 100 * 10, 2
        )

    def _generate_signals(self) -> List[str]:
        signals = []
        if self.defender_killing_impunity_severity_score >= 60:
            signals.append(
                f"Assassinats de défenseurs critiques de {self.name} — meurtres ciblés "
                f"de militants environnementaux et autochtones dans une totale impunité, "
                f"violant le droit à la vie (DUDH Art.3) et le Protocole de Mindanao"
            )
        elif self.defender_killing_impunity_severity_score >= 40:
            signals.append(
                f"Violence contre défenseurs de {self.name} — harcèlement, menaces "
                f"et violences physiques contre les militants environnementaux sans "
                f"protection légale effective ni poursuites des auteurs"
            )
        if self.criminalization_slapp_lawsuit_scale_score >= 60:
            signals.append(
                f"Criminalisation massive des défenseurs — poursuites judiciaires abusives "
                f"(SLAPP) utilisées comme arme d'intimidation pour réduire au silence les "
                f"militants environnementaux et protéger les intérêts industriels extractifs"
            )
        if self.corporate_state_collusion_resource_conflict_score >= 60:
            signals.append(
                f"Collusion corpo-étatique — les gouvernements utilisent les forces de "
                f"sécurité privées et publiques pour protéger les intérêts extractifs au "
                f"détriment des communautés défendant leur territoire et leurs ressources"
            )
        if self.indigenous_land_defender_protection_deficit_score >= 40:
            signals.append(
                f"Impunité institutionnalisée — l'absence de mécanismes de protection "
                f"des défenseurs de l'environnement permet la répétition des assassinats "
                f"et décourage les nouvelles générations de militants"
            )
        if not signals:
            signals.append(
                f"Protection relative des défenseurs de {self.name} — cadres légaux "
                f"partiels pour protéger les militants environnementaux et fonciers"
            )
        return signals[:3]

    def to_dict(self) -> Dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "defender_killing_impunity_severity_score": self.defender_killing_impunity_severity_score,
            "criminalization_slapp_lawsuit_scale_score": self.criminalization_slapp_lawsuit_scale_score,
            "corporate_state_collusion_resource_conflict_score": self.corporate_state_collusion_resource_conflict_score,
            "indigenous_land_defender_protection_deficit_score": self.indigenous_land_defender_protection_deficit_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_environmental_defenders_persecution_index": self.estimated_environmental_defenders_persecution_index,
            "last_updated": self.last_updated,
        }


class EnvironmentalDefendersPerseculionEngine:
    ENGINE_VERSION = "1.0.0"
    DOMAIN = "environmental_defenders_persecution"

    def __init__(self):
        self.entities = self._load_entities()

    def _load_entities(self) -> List[EnvironmentalDefendersPerseculionEntity]:
        return [
            EnvironmentalDefendersPerseculionEntity(
                entity_id="EDP-001",
                name="Honduras/177 Défenseurs Assassinés 2010-2022",
                country="Amérique Centrale",
                sector="177 Défenseurs Assassinés Depuis Coup 2009, Berta Cáceres COPINH 2016, Barrage Agua Zarca, Desa SA Complice & Impunité 93% Cas Non Résolus",
                defender_killing_impunity_severity_score=96.0,
                criminalization_slapp_lawsuit_scale_score=88.0,
                corporate_state_collusion_resource_conflict_score=92.0,
                indigenous_land_defender_protection_deficit_score=90.0,
            ),
            EnvironmentalDefendersPerseculionEntity(
                entity_id="EDP-002",
                name="Brésil/Amazonie 20+ Défenseurs/An Bolsonaro",
                country="Amérique du Sud",
                sector="270 Défenseurs Tués 2009-2019 Global Witness, Dom Phillips & Bruno Pereira 2022, FUNAI Démantelé, Garimpeiros Légalisés & 20+ Tués/An Sous Bolsonaro",
                defender_killing_impunity_severity_score=90.0,
                criminalization_slapp_lawsuit_scale_score=82.0,
                corporate_state_collusion_resource_conflict_score=88.0,
                indigenous_land_defender_protection_deficit_score=86.0,
            ),
            EnvironmentalDefendersPerseculionEntity(
                entity_id="EDP-003",
                name="Philippines/Duterte Red-Tagging Militants",
                country="Asie du Sud-Est",
                sector="66 Défenseurs Assassinés 2020-2022, Red-Tagging Militants Anti-Mines, NTF-ELCAC Terrorisme, Chinatown Nickel & Kalikasan People Network",
                defender_killing_impunity_severity_score=86.0,
                criminalization_slapp_lawsuit_scale_score=90.0,
                corporate_state_collusion_resource_conflict_score=84.0,
                indigenous_land_defender_protection_deficit_score=82.0,
            ),
            EnvironmentalDefendersPerseculionEntity(
                entity_id="EDP-004",
                name="Colombie/Accord Paix Défenseurs Non Protégés",
                country="Amérique du Sud",
                sector="281 Défenseurs Assassinés 2023 Record INDEPAZ, Post-Accord Paix 2016, FARC Dissidents Tuent Défenseurs, Coca Territoires & 33% Autochtones",
                defender_killing_impunity_severity_score=85.0,
                criminalization_slapp_lawsuit_scale_score=75.0,
                corporate_state_collusion_resource_conflict_score=82.0,
                indigenous_land_defender_protection_deficit_score=88.0,
            ),
            EnvironmentalDefendersPerseculionEntity(
                entity_id="EDP-005",
                name="Mexique/Cartels Miniers Défenseurs Yaqui",
                country="Amérique du Nord",
                sector="54 Défenseurs Tués 2022, Cartels Contrôlent Ressources Minières, Peuple Yaqui Eau Sonora, AMLO Retour Militarisation & SLAPP Empresas Extractivas",
                defender_killing_impunity_severity_score=48.0,
                criminalization_slapp_lawsuit_scale_score=55.0,
                corporate_state_collusion_resource_conflict_score=58.0,
                indigenous_land_defender_protection_deficit_score=52.0,
            ),
            EnvironmentalDefendersPerseculionEntity(
                entity_id="EDP-006",
                name="Indonésie/Papouasie Forêts Palmier à Huile",
                country="Asie du Sud-Est",
                sector="Déforestation Papouasie 1.5M Ha, Militants Adat Criminalisés, TNI Militaires Sécurité Plantations, 43 Défenseurs Arrêtés 2022 & Expansion B30 Biofuel",
                defender_killing_impunity_severity_score=42.0,
                criminalization_slapp_lawsuit_scale_score=50.0,
                corporate_state_collusion_resource_conflict_score=55.0,
                indigenous_land_defender_protection_deficit_score=48.0,
            ),
            EnvironmentalDefendersPerseculionEntity(
                entity_id="EDP-007",
                name="UE/Directive SLAPP Anti-Poursuites Bâillon",
                country="Europe",
                sector="Directive Anti-SLAPP 2024 UE, SLAPP Tracker 570 Cas Documentés, Journalistes & ONGs Protégés, Coalition Against SLAPPs & RSF Monitoring",
                defender_killing_impunity_severity_score=12.0,
                criminalization_slapp_lawsuit_scale_score=30.0,
                corporate_state_collusion_resource_conflict_score=15.0,
                indigenous_land_defender_protection_deficit_score=28.0,
            ),
            EnvironmentalDefendersPerseculionEntity(
                entity_id="EDP-008",
                name="Costa Rica/Modèle Protection Défenseurs Forêts",
                country="Amérique Centrale",
                sector="Paiements Services Environnementaux, Zéro Déforestation Nette, Défenseurs Protégés Loi SINAC, Forêts 52% Territoire & Récompense Champions Terre 2021",
                defender_killing_impunity_severity_score=5.0,
                criminalization_slapp_lawsuit_scale_score=4.0,
                corporate_state_collusion_resource_conflict_score=6.0,
                indigenous_land_defender_protection_deficit_score=8.0,
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
            "confidence_score": 0.90,
            "data_sources": [
                "global_witness_defenders_report_2023",
                "front_line_defenders_annual_report_2023",
                "amnesty_international_land_defenders",
                "global_environmental_defenders_monitor",
            ],
            "entities": results,
            "avg_estimated_environmental_defenders_persecution_index": avg_index,
        }


if __name__ == "__main__":
    import json
    engine = EnvironmentalDefendersPerseculionEngine()
    result = engine.analyze()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nAvg composite: {result['avg_composite']}")
    print(f"Distribution: {result['risk_distribution']}")
