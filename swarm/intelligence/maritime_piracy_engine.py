"""
Caelum Partners — Maritime Piracy Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La piraterie maritime moderne : de la Somalie aux Houthis, le retour de la guerre des mers.
La piraterie maritime n'est plus un phénomène cantonné aux côtes somaliennes
des années 2000. Elle s'est transformée en instrument géopolitique entre les
mains d'acteurs étatiques et paramilitaires, ciblant les routes commerciales
les plus critiques du commerce mondial.

Le Golfe de Guinée est devenu le foyer mondial de la piraterie violente : 130
incidents recensés en 2020 par le Bureau Maritime International (BMI), avec
des attaques armées jusqu'à 200 miles offshore au large du Nigeria. Les équipages
sont régulièrement pris en otage pour rançons, avec des durées de captivité
pouvant dépasser 6 mois. La corruption des forces navales nigérianes et des
États côtiers facilite l'impunité des pirates.

Les Houthis du Yémen ont redéfini la piraterie en 2023-2024 en attaquant des
navires commerciaux en mer Rouge — 27% du commerce mondial transite par Bab
el-Mandeb — avec des drones et missiles, forçant le rerouting via le Cap de
Bonne Espérance (+14 jours de transit). Cette "piraterie d'État proxy" est
soutenue par l'Iran et ciblait initialement Israël, frappant finalement des
navires de toutes nationalités.

La Chine pratique une "piraterie légalisée" en mer de Chine du Sud via des
gardes-côtes armés et des milices maritimes civiles chassant les pêcheurs
philippins et vietnamiens de leurs zones économiques exclusives. En 2023,
des garde-côtes chinois ont utilisé des canons à eau contre des navires
philippins en mission de ravitaillement légal.

Risk levels (piraterie maritime et weaponisation des voies maritimes) :
  critique  → composite ≥ 60  (piraterie systémique — attaques armées régulières ou instrumentalisation étatique des voies maritimes)
  élevé     → composite ≥ 40  (piraterie active — incidents fréquents et économie criminelle maritime structurée)
  modéré    → composite ≥ 20  (risque piraterie — zones de vulnérabilité sans incidents systémiques)
  faible    → composite < 20  (sécurité maritime coopérative — patrouilles internationales et droit de la mer respecté)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "piraterie_etatique_proxy": {
        "severity_fr": "Critique",
        "action_fr": "Coalition anti-piraterie élargie — opération navale multinationale en mer Rouge, sanctions contre les États sponsors et mécanisme de compensation pour les opérateurs maritimes victimes",
        "signal_fr": "state_sponsored_piracy_score > 85 AND chokepoint_control_score > 85 — piraterie étatique ou proxy contrôlant des points d'étranglement maritimes critiques via des forces paramilitaires",
    },
    "piraterie_violente_organisee": {
        "severity_fr": "Critique",
        "action_fr": "Renforcement de la présence navale — task force internationale dans le Golfe de Guinée, assistance à la marine nigériane et système de récompense pour les informateurs contre les réseaux pirates",
        "signal_fr": "armed_attack_frequency_score > 85 — piraterie violente organisée avec prises d'otages, attaques armées répétées et économie criminelle maritime structurée",
    },
    "controle_voie_maritime_ilicite": {
        "severity_fr": "Critique",
        "action_fr": "Application renforcée UNCLOS — tribunal international pour violations des ZEE, mécanisme de sanction contre les États obstruant les voies maritimes internationales",
        "signal_fr": "chokepoint_control_score > 85 — contrôle ilicite de voies maritimes stratégiques bloquant ou perturbant le transit commercial international",
    },
    "piraterie_active": {
        "severity_fr": "Élevé",
        "action_fr": "Coordination BMI/INTERPOL — partage du renseignement maritime, escortes navales pour les zones à risque et criminalisation internationale du financement des réseaux pirates",
        "signal_fr": "Piraterie maritime active — incidents réguliers et réseaux criminels maritimes structurés sans atteinte aux points d'étranglement stratégiques",
    },
    "securite_maritime_cooperative": {
        "severity_fr": "Faible",
        "action_fr": "Renforcer l'OMI et UNCLOS — financement des patrouilles multinationales, partage du renseignement maritime et aide aux États côtiers vulnérables pour lutter contre la piraterie",
        "signal_fr": "composite_score < 20 — engagement sincère dans la sécurité maritime coopérative et respect de la CNUDM et des conventions de l'OMI",
    },
}


@dataclass
class MaritimePiracyEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    armed_attack_frequency_score: float
    state_sponsored_piracy_score: float
    chokepoint_control_score: float
    ransomware_maritime_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_maritime_piracy_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.armed_attack_frequency_score * 0.30
            + self.state_sponsored_piracy_score * 0.25
            + self.chokepoint_control_score * 0.25
            + self.ransomware_maritime_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_maritime_piracy_index = round(self.composite_score / 100 * 10, 2)

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
        if self.state_sponsored_piracy_score >= 85 and self.chokepoint_control_score >= 85:
            return "piraterie_etatique_proxy"
        if self.armed_attack_frequency_score >= 85:
            return "piraterie_violente_organisee"
        if self.chokepoint_control_score >= 85:
            return "controle_voie_maritime_ilicite"
        if self.composite_score >= 20:
            return "piraterie_active"
        return "securite_maritime_cooperative"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Piraterie maritime critique de {n} — attaques armées systémiques, contrôle ilicite de voies commerciales ou instrumentalisation étatique de la piraterie à des fins géopolitiques",
                "Menace au commerce mondial — les attaques perturbent les chaînes d'approvisionnement mondiales, augmentent les coûts d'assurance maritime et forcent le rerouting coûteux",
                "Impunité structurelle — l'absence de poursuites efficaces crée un effet d'aubaine pour les réseaux pirates et les États sponsors de piraterie proxy",
            ]
        if self.risk_level == "élevé":
            return [
                f"Piraterie maritime active de {n} — incidents fréquents et réseaux criminels maritimes structurés représentant un risque sérieux pour la navigation commerciale",
                "Économie criminelle maritime — prise d'otages, vols de cargaisons et rackets à l'escale finançant des organisations criminelles déstabilisatrices",
                "Déficit de capacités navales — l'insuffisance des patrouilles côtières nationales et la corruption créent des zones de non-droit maritime exploitées par les pirates",
            ]
        if self.risk_level == "modéré":
            return [
                f"Risque piraterie de {n} — zone de vulnérabilité maritime avec incidents sporadiques mais sans structuration criminelle ou étatique avancée",
                "Vulnérabilités côtières — pauvreté des communautés côtières, pêche illégale étrangère et gouvernance maritime défaillante créant des conditions propices",
                "Risque d'aggravation — la dégradation des conditions économiques et la prolifération des armes légères pourraient intensifier les incidents de piraterie",
            ]
        return [
            f"{n} incarne la sécurité maritime coopérative — participation aux opérations navales multinationales, respect de l'UNCLOS et partage du renseignement maritime",
            "Gouvernance maritime exemplaire — garde-côtes efficaces, tribunaux maritimes compétents et coopération régionale contre les réseaux pirates",
            "Modèle anti-piraterie à diffuser — financement de l'OMI, formation des marines côtières et assistance judiciaire pour poursuivre les pirates capturés",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "armed_attack_frequency_score": self.armed_attack_frequency_score,
            "state_sponsored_piracy_score": self.state_sponsored_piracy_score,
            "chokepoint_control_score": self.chokepoint_control_score,
            "ransomware_maritime_score": self.ransomware_maritime_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_maritime_piracy_index": self.estimated_maritime_piracy_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[MaritimePiracyEntity] = [
    MaritimePiracyEntity("MP-001", "Golfe de Guinée — Nigeria & Piraterie Violente 200 Miles", "Afrique de l'Ouest", "130 Incidents BMI 2020, Prises Otages 6 Mois, 200M Offshore Attaques & Corruption Marine Nigériane", 92.0, 65.0, 75.0, 80.0),
    MaritimePiracyEntity("MP-002", "Houthis/Iran — Piraterie Proxy Mer Rouge & Bab el-Mandeb", "MENA", "27% Commerce Mondial Menacé, Missiles/Drones Navires Commerciaux, Rerouting Cap Bonne Esp. +14J & Iran Sponsor", 85.0, 92.0, 88.0, 72.0),
    MaritimePiracyEntity("MP-003", "Chine — Milices Maritimes & Piraterie Légalisée MCS", "Asie", "Gardes-Côtes vs Philippines Cannons Eau, Milices 3000 Bateaux Haijing, ZEE Violation Systémique & UNCLOS Rejeté", 72.0, 88.0, 95.0, 68.0),
    MaritimePiracyEntity("MP-004", "Somalie & Corne d'Afrique — Piraterie Offshore Renaissante", "Afrique de l'Est", "Piraterie Résurgence 2023 Contexte Houthis, Al-Shabaab Maritime Wing, Golfe Aden Attaques & Rançons Crypto", 80.0, 72.0, 82.0, 78.0),
    MaritimePiracyEntity("MP-005", "Iran — IRGC Marine & Saisies Navires Hormuz", "MENA", "Détroit Hormuz 20% Pétrole Mondial, Saisies IRGC Navires Commerciaux, Mines Navales & Harcelèment", 55.0, 52.0, 65.0, 62.0),
    MaritimePiracyEntity("MP-006", "Venezuela & Caraïbes — Piraterie Narco & Corruption", "Amérique du Sud", "Pirates Narco-Liés, Attaques Voiliers Tourisme, Corruption Gardes-Côtes & Transit Drogue Maritime", 52.0, 48.0, 42.0, 58.0),
    MaritimePiracyEntity("MP-007", "Détroit de Malacca & Asie Sud-Est — Faible Intensité", "Asie du Sud-Est", "Petits Vols Bateaux, Indonésie Piraterie Côtière, Capacités Régionales RECAAP Améliorées & Risque Résiduel", 28.0, 25.0, 32.0, 35.0),
    MaritimePiracyEntity("MP-008", "OMI & EU NAVFOR — Sécurité Maritime Coopérative", "Global", "OMI Convention SUA, EU NAVFOR Atalante, RECAAP Asie & Combined Maritime Forces 34 Nations Anti-Piraterie", 5.0, 4.0, 3.0, 6.0),
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
        "domain": "maritime_piracy",
        "confidence_score": 0.82,
        "data_sources": ["icc_imb_piracy_report", "unodc_maritime_crime_monitor", "eu_navfor_atalanta_reports"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_maritime_piracy_index": round(avg / 100 * 10, 2),
    }


def analyze_maritime_piracy() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Maritime Piracy Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
