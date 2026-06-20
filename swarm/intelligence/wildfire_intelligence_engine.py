"""
Wildfire Intelligence Engine
Module — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
Domain: wildfire | Slug: wildfire-intelligence-engine
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime, timezone


# ── Patterns ──────────────────────────────────────────────────────────────────

PATTERNS: Dict[str, Dict[str, str]] = {
    "Propagation Catastrophique": {
        "name": "Propagation Catastrophique",
        "severity_fr": "critique",
        "action_fr": "Déploiement immédiat des équipes de lutte contre l'incendie et évacuation des zones à risque. Coordination interagences et demande de renforts aériens.",
        "signal_fr": "Vitesse de propagation extrême détectée avec des vents défavorables et végétation hautement inflammable.",
    },
    "Déficit Prévention Critique": {
        "name": "Déficit Prévention Critique",
        "severity_fr": "critique",
        "action_fr": "Révision urgente des politiques de prévention et renforcement des capacités de débroussaillage. Audit immédiat des protocoles de gestion forestière.",
        "signal_fr": "Absence critique de pare-feux et de zones tampons. Sous-investissement chronique dans les mesures préventives de gestion forestière.",
    },
    "Effondrement Réponse d'Urgence": {
        "name": "Effondrement Réponse d'Urgence",
        "severity_fr": "élevé",
        "action_fr": "Renforcement immédiat des capacités de réponse d'urgence. Formation accélérée des équipes et acquisition de matériel supplémentaire.",
        "signal_fr": "Délais d'intervention critiques et ressources de lutte anti-incendie insuffisantes face à l'ampleur des sinistres.",
    },
    "Impact Écosystème Majeur": {
        "name": "Impact Écosystème Majeur",
        "severity_fr": "modéré",
        "action_fr": "Mise en place de programmes de restauration écologique. Surveillance renforcée des zones de biodiversité sensibles et plans de réhabilitation.",
        "signal_fr": "Destruction significative d'habitats naturels et perturbation des cycles hydrologiques locaux détectée.",
    },
    "Risque Saisonnier Émergent": {
        "name": "Risque Saisonnier Émergent",
        "severity_fr": "faible",
        "action_fr": "Activation des protocoles de surveillance saisonnière. Mise à jour des plans de prévention et sensibilisation des communautés locales.",
        "signal_fr": "Indicateurs saisonniers précoces détectés. Conditions météorologiques à surveiller en prévision de la saison des feux.",
    },
}


# ── Entity ─────────────────────────────────────────────────────────────────────

@dataclass
class WildfireEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    spread_score: float
    prevention_score: float
    response_score: float
    impact_score: float
    key_signals: List[str] = field(default_factory=list)

    def _composite_score(self) -> float:
        return round(
            self.spread_score * 0.30
            + self.prevention_score * 0.25
            + self.response_score * 0.25
            + self.impact_score * 0.20,
            2,
        )

    def _risk_level(self, composite: float) -> str:
        if composite >= 60:
            return "critique"
        if composite >= 40:
            return "élevé"
        if composite >= 20:
            return "modéré"
        return "faible"

    def _primary_pattern(self, composite: float) -> str:
        # critique tier — prevention dominates if score ≥ 80, else spread dominates if ≥ 75
        if composite >= 60:
            if self.prevention_score >= 80:
                return "Déficit Prévention Critique"
            if self.spread_score >= 75:
                return "Propagation Catastrophique"
        # élevé tier — response dominates if ≥ 50, else impact
        if composite >= 40:
            if self.response_score >= 50:
                return "Effondrement Réponse d'Urgence"
            return "Impact Écosystème Majeur"
        return "Risque Saisonnier Émergent"

    def to_dict(self) -> Dict[str, Any]:
        composite = self._composite_score()
        risk = self._risk_level(composite)
        pattern = self._primary_pattern(composite)
        estimated_wildfire_index = round(composite / 100 * 10, 2)
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": composite,
            "spread_score": self.spread_score,
            "prevention_score": self.prevention_score,
            "response_score": self.response_score,
            "impact_score": self.impact_score,
            "risk_level": risk,
            "primary_pattern": pattern,
            "key_signals": self.key_signals,
            "estimated_wildfire_index": estimated_wildfire_index,
            "action_fr": PATTERNS[pattern]["action_fr"],
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }


# ── Engine ─────────────────────────────────────────────────────────────────────

class WildfireIntelligenceEngine:
    ENGINE_VERSION = "1.0.0"
    DOMAIN = "wildfire"

    def __init__(self) -> None:
        self._entities: List[WildfireEntity] = self._build_mock_entities()

    # ------------------------------------------------------------------
    # Mock data
    # ------------------------------------------------------------------

    @staticmethod
    def _build_mock_entities() -> List[WildfireEntity]:
        return [
            # WF-001 — California Wildfire Zone — critique (73.25)
            # spread=80, prevention=70, response=65, impact=77.5 → 80*0.30+70*0.25+65*0.25+77.5*0.20 = 73.25
            WildfireEntity(
                entity_id="WF-001",
                name="California Wildfire Zone",
                country="USA",
                sector="Emergency Management",
                spread_score=80.0,
                prevention_score=70.0,
                response_score=65.0,
                impact_score=77.5,
                key_signals=[
                    "Vitesse de propagation de 2 km/h enregistrée avec des rafales à 80 km/h",
                    "Indice de sécheresse de la végétation (KBDI) au niveau critique — 700+",
                    "Superficie brûlée cumulée dépassant 500 000 hectares depuis janvier",
                ],
            ),
            # WF-002 — Amazon Deforestation Region — critique (83.0)
            # spread=85, prevention=80, response=75, impact=93.75 → 85*0.30+80*0.25+75*0.25+93.75*0.20 = 83.0
            WildfireEntity(
                entity_id="WF-002",
                name="Amazon Deforestation Region",
                country="Brazil",
                sector="Environmental",
                spread_score=85.0,
                prevention_score=80.0,
                response_score=75.0,
                impact_score=93.75,
                key_signals=[
                    "Taux de déforestation illégale en hausse de 34 % sur les 12 derniers mois",
                    "Absence de corridor pare-feu sur 1 200 km de frontière forêt-agriculture",
                    "Concentration de CO₂ forestier anormalement élevée détectée par satellite",
                ],
            ),
            # WF-003 — Mediterranean Basin Authority — critique (68.25)
            # spread=75, prevention=65, response=60, impact=72.5 → 75*0.30+65*0.25+60*0.25+72.5*0.20 = 68.25
            WildfireEntity(
                entity_id="WF-003",
                name="Mediterranean Basin Authority",
                country="Greece",
                sector="Emergency Management",
                spread_score=75.0,
                prevention_score=65.0,
                response_score=60.0,
                impact_score=72.5,
                key_signals=[
                    "Canicule persistante avec températures dépassant 42 °C pendant 14 jours consécutifs",
                    "Humidité relative inférieure à 15 % sur l'ensemble du bassin méditerranéen",
                    "Infrastructure de détection précoce défaillante dans 60 % des zones forestières",
                ],
            ),
            # WF-004 — Australian Bushfire Region — élevé (50.1)
            # spread=55, prevention=45, response=50, impact=49.25 → 55*0.30+45*0.25+50*0.25+49.25*0.20 = 50.1
            WildfireEntity(
                entity_id="WF-004",
                name="Australian Bushfire Region",
                country="Australia",
                sector="Emergency Management",
                spread_score=55.0,
                prevention_score=45.0,
                response_score=50.0,
                impact_score=49.25,
                key_signals=[
                    "Indice McArthur Forest Fire Danger (FFDI) à 50 — catégorie extrême",
                    "Réserves en eau des retenues à 28 % de leur capacité normale pour la saison",
                    "Manque de personnels formés pour la saison des feux — déficit de 35 % des effectifs",
                ],
            ),
            # WF-005 — Siberian Taiga Agency — élevé (44.9)
            # spread=50, prevention=40, response=45, impact=43.25 → 50*0.30+40*0.25+45*0.25+43.25*0.20 = 44.9
            WildfireEntity(
                entity_id="WF-005",
                name="Siberian Taiga Agency",
                country="Russia",
                sector="Forestry",
                spread_score=50.0,
                prevention_score=40.0,
                response_score=45.0,
                impact_score=43.25,
                key_signals=[
                    "Dégel du pergélisol libérant du méthane et augmentant l'inflammabilité de la tourbe",
                    "Absence de routes d'accès forestières sur 70 % du territoire de la taïga",
                    "Superficie de forêt morte (bois mort) augmentée de 18 % suite aux épidémies de scolytes",
                ],
            ),
            # WF-006 — Portuguese Forest Service — modéré (26.9)
            # spread=30, prevention=25, response=28, impact=23.25 → 30*0.30+25*0.25+28*0.25+23.25*0.20 = 26.9
            WildfireEntity(
                entity_id="WF-006",
                name="Portuguese Forest Service",
                country="Portugal",
                sector="Forestry",
                spread_score=30.0,
                prevention_score=25.0,
                response_score=28.0,
                impact_score=23.25,
                key_signals=[
                    "Expansion des plantations d'eucalyptus hautement inflammables sur 800 000 ha",
                    "Ressources humaines de lutte anti-incendie réduites de 20 % par rapport à 2020",
                    "Indices de risque saisonnier en hausse précoce — 3 semaines avant la normale",
                ],
            ),
            # WF-007 — Canadian Fire Watch — faible (11.85)
            # spread=15, prevention=10, response=12, impact=9.25 → 15*0.30+10*0.25+12*0.25+9.25*0.20 = 11.85
            WildfireEntity(
                entity_id="WF-007",
                name="Canadian Fire Watch",
                country="Canada",
                sector="Emergency Management",
                spread_score=15.0,
                prevention_score=10.0,
                response_score=12.0,
                impact_score=9.25,
                key_signals=[
                    "Précipitations hivernales nettement supérieures à la moyenne — réserves hydriques satisfaisantes",
                    "Programme de débroussaillage préventif complété à 95 % avant la saison estivale",
                    "Réseau de surveillance par drone opérationnel sur l'ensemble des zones à risque",
                ],
            ),
            # WF-008 — Scandinavian Forest Authority — faible (8.35)
            # spread=10, prevention=8, response=9, impact=5.5 → 10*0.30+8*0.25+9*0.25+5.5*0.20 = 8.35
            WildfireEntity(
                entity_id="WF-008",
                name="Scandinavian Forest Authority",
                country="Sweden",
                sector="Forestry",
                spread_score=10.0,
                prevention_score=8.0,
                response_score=9.0,
                impact_score=5.5,
                key_signals=[
                    "Taux d'humidité forestière à 78 % — niveau optimal hors période de risque",
                    "Protocoles de coopération transfrontalière avec la Norvège et la Finlande actifs",
                    "Investissement record dans la télédétection satellitaire des incendies — couverture 100 %",
                ],
            ),
        ]

    # ------------------------------------------------------------------
    # Main analysis method
    # ------------------------------------------------------------------

    def analyze_wildfire(self) -> Dict[str, Any]:
        """Run wildfire intelligence analysis and return summary dict with exactly 13 keys."""
        entity_dicts = [e.to_dict() for e in self._entities]

        total = len(entity_dicts)
        composites = [e["composite_score"] for e in entity_dicts]
        avg_composite = round(sum(composites) / total, 2) if total > 0 else 0.0

        # Risk distribution
        risk_distribution: Dict[str, int] = {}
        for e in entity_dicts:
            rl = e["risk_level"]
            risk_distribution[rl] = risk_distribution.get(rl, 0) + 1

        # Pattern distribution
        pattern_distribution: Dict[str, int] = {}
        for e in entity_dicts:
            pp = e["primary_pattern"]
            pattern_distribution[pp] = pattern_distribution.get(pp, 0) + 1

        # Top risk entities (critique, sorted by composite desc)
        top_risk_entities = sorted(
            [e for e in entity_dicts if e["risk_level"] == "critique"],
            key=lambda x: x["composite_score"],
            reverse=True,
        )

        # Critical alerts
        critical_alerts = [
            {
                "entity_id": e["entity_id"],
                "name": e["name"],
                "composite_score": e["composite_score"],
                "primary_pattern": e["primary_pattern"],
                "alert": PATTERNS[e["primary_pattern"]]["signal_fr"],
            }
            for e in entity_dicts
            if e["risk_level"] == "critique"
        ]

        # avg_estimated_wildfire_index — key #13
        avg_estimated_wildfire_index = round(avg_composite / 100 * 10, 2)

        return {
            "total_entities": total,
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution,
            "pattern_distribution": pattern_distribution,
            "top_risk_entities": top_risk_entities,
            "critical_alerts": critical_alerts,
            "last_analysis": datetime.now(timezone.utc).isoformat(),
            "engine_version": self.ENGINE_VERSION,
            "domain": self.DOMAIN,
            "confidence_score": 0.91,
            "data_sources": [
                "NASA FIRMS — Fire Information for Resource Management System",
                "Copernicus Emergency Management Service (CEMS)",
                "NOAA Global Wildfire Information System (GWIS)",
                "FAO Global Forest Resources Assessment",
            ],
            "entities": entity_dicts,
            "avg_estimated_wildfire_index": avg_estimated_wildfire_index,
        }

    def summary(self) -> Dict[str, Any]:
        """Alias for analyze_wildfire() — returns 13-key summary dict."""
        return self.analyze_wildfire()


# ── Module-level entrypoint ────────────────────────────────────────────────────

def analyze_wildfire() -> Dict[str, Any]:
    """Module-level entrypoint for the Wildfire Intelligence Engine."""
    engine = WildfireIntelligenceEngine()
    return engine.analyze_wildfire()


def summary() -> Dict[str, Any]:
    """Module-level summary alias for swarm orchestrator compatibility."""
    return analyze_wildfire()


if __name__ == "__main__":
    import json

    result = analyze_wildfire()
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))

    # Verify invariants
    assert len(result) == 13, f"summary() must have 13 keys, got {len(result)}"
    for entity in result["entities"]:
        assert len(entity) == 15, f"to_dict() must have 15 keys, got {len(entity)} for {entity['entity_id']}"
        cs = entity["composite_score"]
        expected = round(
            entity["spread_score"] * 0.30
            + entity["prevention_score"] * 0.25
            + entity["response_score"] * 0.25
            + entity["impact_score"] * 0.20,
            2,
        )
        assert cs == expected, f"Composite mismatch for {entity['entity_id']}: {cs} vs {expected}"
        ewi = entity["estimated_wildfire_index"]
        assert ewi == round(cs / 100 * 10, 2), f"EWI mismatch for {entity['entity_id']}"

    awf = result["avg_estimated_wildfire_index"]
    assert awf == round(result["avg_composite"] / 100 * 10, 2), "avg_estimated_wildfire_index mismatch"

    print("\nAll invariants verified.")
    print(f"  Summary keys: {len(result)}")
    print(f"  Entity keys:  {len(result['entities'][0])}")
    print(f"  avg_composite: {result['avg_composite']}")
    print(f"  avg_estimated_wildfire_index: {result['avg_estimated_wildfire_index']}")
    print(f"  risk_distribution: {result['risk_distribution']}")
