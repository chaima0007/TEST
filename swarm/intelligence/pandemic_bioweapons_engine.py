"""
Caelum Partners — Pandemic & Bioweapons Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La menace biologique : entre pandémies naturelles et armes de destruction massive.
Les agents pathogènes constituent la menace la plus asymétrique qui soit — une
quantité microscopique d'un agent bien choisi peut tuer des millions de personnes
à un coût infinitésimal. La Convention sur les Armes Biologiques (CAB 1972)
interdit la mise au point, la production et le stockage d'armes biologiques, mais
sans mécanisme de vérification contraignant, elle reste partiellement inefficace.

La Russie a hérité du programme soviétique Biopreparat — 60 000 chercheurs,
des agents pathogènes modifiés génétiquement (anthrax, variole, Yersinia pestis)
et des installations classifiées toujours actives selon les services de
renseignement occidentaux. La Chine dispose de 4 laboratoires BSL-4 dont Wuhan,
foyer de la pandémie Covid-19 dont l'origine (fuite de laboratoire vs zoonose)
reste disputée et sous enquête internationale. Les USA financent la recherche
de gain de fonction malgré son interdiction temporaire de 2014-2017 via des
agences comme DTRA et BARDA.

La Corée du Nord est suspectée de posséder des capacités de guerre biologique
incluant anthrax, variole et botulinum selon l'USGOV. L'IRGC iranien maintient
un programme BW suspecté. La pandémie Covid-19 a exposé les lacunes critiques
de préparation mondiale — 7 millions de morts officiels, probablement 15+ millions
en excès de mortalité.

Risk levels (biosécurité et risques de bioarmes) :
  critique  → composite ≥ 60  (bioarmes étatiques — programme dual-use offensif documenté ou hautement suspecté)
  élevé     → composite ≥ 40  (risque biologique élevé — capacités BW suspectées ou arsenaux hérités)
  modéré    → composite ≥ 20  (vulnérabilité biosécurité — lacunes critiques de préparation pandémique)
  faible    → composite < 20  (résilience biosécurité — cadres robustes de prévention et réponse)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "bioarmes_etatiques_actives": {
        "severity_fr": "Critique",
        "action_fr": "Mécanisme de vérification CAB — protocole additionnel obligatoire avec inspections sur site et sanctions ciblées contre les États contrevenants",
        "signal_fr": "dual_use_research_score > 85 AND biosafety_breach_score > 85 — programme de bioarmes étatiques actif avec couverture dual-use",
    },
    "programme_dual_use_offensif": {
        "severity_fr": "Critique",
        "action_fr": "Contrôle international du gain de fonction — moratoire mondial sur la recherche à risque de pandémie et supervision AIEA-Bio des laboratoires BSL-4",
        "signal_fr": "bio_weapons_proliferation_score > 85 — prolifération de capacités de bioarmes via des programmes de recherche dual-use non supervisés",
    },
    "vulnerabilite_biosecurite_critique": {
        "severity_fr": "Critique",
        "action_fr": "Hardening biosécurité d'urgence — audit des laboratoires BSL-3/BSL-4, formation obligatoire et protocoles de confinement renforcés",
        "signal_fr": "biosafety_breach_score > 85 — vulnérabilités critiques de biosécurité exposant à des incidents de confinement à haut risque",
    },
    "risque_pandemique_emergent": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement du RSI — Règlement Sanitaire International révisé, fonds pandémique de l'OMS doté et réseau mondial de surveillance épidémique",
        "signal_fr": "Risque pandemique émergent — lacunes de biosécurité, programmes BW suspectés ou faibles capacités de surveillance épidémique",
    },
    "resilience_biosecurite": {
        "severity_fr": "Faible",
        "action_fr": "Partager les modèles de résilience biosécurité — financer la préparation pandémique mondiale et universaliser les protocoles OMS",
        "signal_fr": "composite_score < 20 — résilience biosécurité exemplaire — cadres de prévention pandémique robustes et transparence épidémique",
    },
}


@dataclass
class PandemicBioweaponsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    dual_use_research_score: float
    biosafety_breach_score: float
    bio_weapons_proliferation_score: float
    pandemic_preparedness_deficit_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_pandemic_bioweapons_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.dual_use_research_score * 0.30
            + self.biosafety_breach_score * 0.25
            + self.bio_weapons_proliferation_score * 0.25
            + self.pandemic_preparedness_deficit_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_pandemic_bioweapons_index = round(self.composite_score / 100 * 10, 2)

    def _risk(self) -> str:
        s = self.composite_score
        if s >= 60:
            return "critique"
        if s >= 40:
            return "élevé"
        if s >= 20:
            return "modéré"
        return "faible"

    def _pattern(self) -> str:
        if self.dual_use_research_score >= 85 and self.biosafety_breach_score >= 85:
            return "bioarmes_etatiques_actives"
        if self.bio_weapons_proliferation_score >= 85:
            return "programme_dual_use_offensif"
        if self.biosafety_breach_score >= 85:
            return "vulnerabilite_biosecurite_critique"
        if self.composite_score >= 20:
            return "risque_pandemique_emergent"
        return "resilience_biosecurite"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Programme bioarmes étatique de {n} — recherche dual-use à des fins offensives avec déni de responsabilité institutionnel",
                "Arsenal biologique hérité ou développé — agents pathogènes modifiés génétiquement, production clandestine et vecteurs de dissémination",
                "Violation de la Convention des Armes Biologiques — absence de transparence, refus d'inspections et non-déclaration des installations",
            ]
        if self.risk_level == "élevé":
            return [
                f"Risque biologique élevé de {n} — capacités BW suspectées ou arsenaux hérités non vérifiés par les instances internationales",
                "Lacunes de biosécurité critiques — laboratoires BSL insuffisamment sécurisés exposant à des fuites accidentelles ou intentionnelles",
                "Prolifération d'agents pathogènes dangereux — transferts suspects de matériaux biologiques sans contrôle adéquat de l'AIEA-Bio",
            ]
        if self.risk_level == "modéré":
            return [
                f"Vulnérabilité biosécurité de {n} — lacunes dans la préparation pandémique et les capacités de surveillance épidémique",
                "Faiblesse institutionnelle — systèmes de santé publique insuffisants pour détecter et contenir une émergence épidémique précoce",
                "Non-conformité RSI — obligations de notification internationale non respectées dans les délais requis par l'OMS",
            ]
        return [
            f"{n} incarne la résilience biosécurité — cadres robustes de prévention, détection et réponse aux menaces biologiques",
            "Transparence épidémique exemplaire — notification immédiate à l'OMS et coopération internationale sur la surveillance pathogénique",
            "Modèle de préparation pandémique à universaliser — stockages stratégiques, plans de continuité et chaînes de distribution vaccinales",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "dual_use_research_score": self.dual_use_research_score,
            "biosafety_breach_score": self.biosafety_breach_score,
            "bio_weapons_proliferation_score": self.bio_weapons_proliferation_score,
            "pandemic_preparedness_deficit_score": self.pandemic_preparedness_deficit_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_pandemic_bioweapons_index": self.estimated_pandemic_bioweapons_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[PandemicBioweaponsEntity] = [
    PandemicBioweaponsEntity("PB-001", "Russie — Biopreparat & Arsenal BW Soviétique Hérité", "Europe de l'Est", "Biopreparat 60K Chercheurs, Anthrax/Variole Modifiés & Installations Classifiées Toujours Actives", 88.0, 92.0, 90.0, 75.0),
    PandemicBioweaponsEntity("PB-002", "Chine — BSL-4 Wuhan & Gain de Fonction Controversé", "Asie", "WIV Wuhan BSL-4, EcoHealth Alliance Subventions & Origine Covid-19 Non Résolue Sous Enquête", 85.0, 88.0, 82.0, 80.0),
    PandemicBioweaponsEntity("PB-003", "USA — DTRA, BARDA & Gain de Fonction Externalisé", "Amérique du Nord", "DTRA Laboratoires Géorgie/Ukraine, Gain de Fonction via EcoHealth & Programme Biodefense Dual", 82.0, 80.0, 78.0, 85.0),
    PandemicBioweaponsEntity("PB-004", "RPDC — Programme BW Clandestin Anthrax/Variole", "Asie", "Anthrax, Variole, Botulinum & Yersinia Suspectés — USGOV Estimations DIA Corée du Nord", 75.0, 72.0, 88.0, 68.0),
    PandemicBioweaponsEntity("PB-005", "Iran — IRGC Capacités BW & Dual-Use Biologique", "MENA", "Instituts Pasteur Iran, IRGC Recherche BW Suspectée & Programme Vaccinal Dual-Use", 52.0, 55.0, 62.0, 48.0),
    PandemicBioweaponsEntity("PB-006", "Syrie & Irak — Restes Arsenaux Chimio-Bio", "MENA", "Sarin Syrien Non Déclaré, Moutarde Soufre Daesh & Installations Non Démantelées OIAC", 48.0, 58.0, 55.0, 45.0),
    PandemicBioweaponsEntity("PB-007", "Pays Émergents — Gaps Biosécurité Régionaux", "Global", "GHS Index Lacunes Afrique/Asie du Sud, BSL-2 Sous-Standards & Surveillance Épidémique Déficiente", 28.0, 32.0, 25.0, 38.0),
    PandemicBioweaponsEntity("PB-008", "OMS & BARDA — Résilience Biosécurité Multilatérale", "Global", "RSI Révisé 2024, BARDA BPARDA, CEPI Vaccins & Fonds Pandémique G20 Doté 1.4Md$", 5.0, 4.0, 3.0, 6.0),
]


def summary() -> dict[str, Any]:
    entities = MOCK_ENTITIES
    n = len(entities)
    avg = round(sum(e.composite_score for e in entities) / n, 2)

    risk_dist: dict[str, int] = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    pattern_dist: dict[str, int] = {k: 0 for k in PATTERNS}
    critical_alerts: list[str] = []
    top_risk: list[str] = []

    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
        pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1
        if e.risk_level == "critique":
            critical_alerts.append(f"{e.name}: {e.primary_pattern.replace('_', ' ')}")
            top_risk.append(e.name)

    return {
        "total_entities": n,
        "avg_composite": avg,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": top_risk,
        "critical_alerts": critical_alerts,
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "pandemic_bioweapons",
        "confidence_score": 0.75,
        "data_sources": ["ghs_index_global_biosecurity", "nuclear_threat_initiative_bio", "who_ihr_monitoring_framework"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_pandemic_bioweapons_index": round(avg / 100 * 10, 2),
    }


def analyze_pandemic_bioweapons() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Pandemic Bioweapons Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
