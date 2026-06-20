"""
Caelum Partners — Organ Trafficking Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Le trafic d'organes : la face cachée de la médecine mondiale à 1,7 milliard de dollars.
Le trafic d'organes génère 1,7 milliard de dollars annuellement selon l'OMS,
avec 10 000 reins vendus illégalement chaque année. C'est le crime le plus
rentable après le trafic de drogues et d'êtres humains, et il prospère dans les
zones de vulnérabilité extrême : prisonniers politiques, réfugiés, populations
appauvries contraintes de vendre leurs organes pour survivre.

La Chine est le cas le plus documenté et le plus alarmant : le Tribunal Indépendant
sur les Prélèvements Forcés d'Organes en Chine (2019) a conclu "au-delà de tout
doute raisonnable" que des prisonniers de conscience — Falun Gong, Ouïghours,
chrétiens — sont exécutés pour prélèvement d'organes à la demande, avec des délais
d'attente de "1 à 2 semaines" impossible à expliquer autrement que par des banques
vivantes de donneurs. Pékin a annoncé des réformes en 2015 mais aucune
vérification indépendante n'a pu les confirmer.

Le tourisme de transplantation illegal prospère au Pakistan, en Égypte et en
Inde, où des "agents" recrutent des donneurs vivants parmi les populations
pauvres pour 1 000-3 000$ par rein revendu 150 000-200 000$ sur le marché
noir. La Moldavie, l'Ukraine et le Brésil sont des zones de prédation pour
des réseaux criminels transnationaux utilisant des donneurs sous contrainte.

Risk levels (trafic d'organes et prélèvements forcés) :
  critique  → composite ≥ 60  (prélèvements forcés — programme étatique ou réseau criminel organisé à grande échelle)
  élevé     → composite ≥ 40  (tourisme transplantation actif — trafic d'organes structuré sans mandat étatique)
  modéré    → composite ≥ 20  (vulnérabilité donneur — populations exposées au recrutement forcé sans réseau structuré)
  faible    → composite < 20  (régulation exemplaire — liste nationale transparente, contrôle strict des transplantations)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "prelevement_organes_force": {
        "severity_fr": "Critique",
        "action_fr": "Coalition internationale anti-trafic organes — sanctions ciblées contre les centres de transplantation, interdiction de visa aux chirurgiens impliqués et réforme obligatoire des systèmes nationaux de transplantation",
        "signal_fr": "forced_organ_harvesting_score > 85 AND state_complicity_organ_trade_score > 85 — prélèvements d'organes forcés avec complicité ou organisation étatique directe sur des prisonniers de conscience",
    },
    "tourisme_transplantation_illicite": {
        "severity_fr": "Critique",
        "action_fr": "Déclaration d'Istanbul renforcée — criminalisation du tourisme de transplantation, traçabilité obligatoire des organes et coopération judiciaire internationale contre les réseaux de courtiers",
        "signal_fr": "transplant_tourism_infrastructure_score > 85 — infrastructure active de tourisme de transplantation illicite attirant des patients internationaux vers des organes obtenus de manière criminelle",
    },
    "marche_noir_organes": {
        "severity_fr": "Critique",
        "action_fr": "Task force OMS/INTERPOL organes — registres obligatoires des transplantations, contrôles bancaires sur les transactions suspectes et protection juridique des donneurs sous contrainte",
        "signal_fr": "black_market_organ_network_score > 85 — réseau criminalisé de marché noir des organes opérant à grande échelle avec des filières internationales établies",
    },
    "trafic_organes_actif": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement Protocole de Palerme — inclusion explicite du trafic d'organes, financement des enquêtes INTERPOL et soutien aux procureurs nationaux anti-trafic",
        "signal_fr": "Trafic d'organes actif — réseaux de recrutement de donneurs contraints et courtiers en organes actifs sans mandat étatique direct",
    },
    "regulation_organes_exemplaire": {
        "severity_fr": "Faible",
        "action_fr": "Exporter le modèle opt-out — systèmes de consentement présumé, listes nationales transparentes et coopération internationale pour éliminer les marchés noirs alimentés par la pénurie",
        "signal_fr": "composite_score < 20 — régulation exemplaire des transplantations, liste d'attente nationale transparente et conformité totale à la Déclaration d'Istanbul",
    },
}


@dataclass
class OrganTraffickingEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    forced_organ_harvesting_score: float
    transplant_tourism_infrastructure_score: float
    state_complicity_organ_trade_score: float
    black_market_organ_network_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_organ_trafficking_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.forced_organ_harvesting_score * 0.30
            + self.transplant_tourism_infrastructure_score * 0.25
            + self.state_complicity_organ_trade_score * 0.25
            + self.black_market_organ_network_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_organ_trafficking_index = round(self.composite_score / 100 * 10, 2)

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
        if self.forced_organ_harvesting_score >= 85 and self.state_complicity_organ_trade_score >= 85:
            return "prelevement_organes_force"
        if self.transplant_tourism_infrastructure_score >= 85:
            return "tourisme_transplantation_illicite"
        if self.black_market_organ_network_score >= 85:
            return "marche_noir_organes"
        if self.composite_score >= 20:
            return "trafic_organes_actif"
        return "regulation_organes_exemplaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Trafic d'organes critique de {n} — programme de prélèvement forcé, réseau criminel organisé ou infrastructure de tourisme de transplantation illicite à grande échelle",
                "Crime contre l'humanité potentiel — les prélèvements forcés sur des prisonniers de conscience constituent une violation grave du droit international humanitaire",
                "Demande insatiable mondiale — 100 000 transplantations légales par an pour 2 millions de patients en attente crée une pression criminelle systémique",
            ]
        if self.risk_level == "élevé":
            return [
                f"Trafic d'organes actif de {n} — réseaux de courtiers opérationnels recrutant des donneurs sous contrainte économique pour des patients internationaux fortunés",
                "Exploitation des vulnérabilités — réfugiés, déplacés et populations extrêmement pauvres ciblés pour la vente contrainte d'organes à 1 000-3 000$",
                "Infrastructures médicales complices — cliniques et chirurgiens participant sciemment à l'écosystème criminel des transplantations illicites",
            ]
        if self.risk_level == "modéré":
            return [
                f"Vulnérabilité donneur de {n} — populations exposées au recrutement par des réseaux de trafic d'organes sans infrastructure criminelle pleinement structurée",
                "Déficits réglementaires — absence de registre national transparent et contrôles insuffisants sur les activités de transplantation créant des opportunités criminelles",
                "Risque de glissement — la pauvreté endémique et la faiblesse des institutions judiciaires attirent les réseaux criminels de trafic d'organes",
            ]
        return [
            f"{n} incarne la régulation exemplaire des transplantations — consentement présumé, liste nationale transparente et zéro tolérance pour le tourisme de transplantation",
            "Système de don éthique — registre national public, temps d'attente équitables et coopération internationale contre les marchés noirs d'organes",
            "Modèle anti-trafic à diffuser — financement INTERPOL sur le trafic d'organes, formation des procureurs et aide aux pays en déficit de régulation",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "forced_organ_harvesting_score": self.forced_organ_harvesting_score,
            "transplant_tourism_infrastructure_score": self.transplant_tourism_infrastructure_score,
            "state_complicity_organ_trade_score": self.state_complicity_organ_trade_score,
            "black_market_organ_network_score": self.black_market_organ_network_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_organ_trafficking_index": self.estimated_organ_trafficking_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[OrganTraffickingEntity] = [
    OrganTraffickingEntity("OT-001", "Chine — Prélèvements Forcés Falun Gong/Ouïghours & Exécutions", "Asie", "Tribunal Indépendant 2019 'Au-Delà Tout Doute', Délais 1-2 Semaines Impossibles, Camps Xinjiang & ETAC", 92.0, 88.0, 95.0, 82.0),
    OrganTraffickingEntity("OT-002", "Pakistan — Tourisme Transplantation & Reins Vendus 3000$", "Asie du Sud", "10 000 Reins Vendus/An Pakistan, Donneurs Contrainte Économique Punjab, Cliniques Karachi Offshore & Réseau Courtiers", 72.0, 90.0, 65.0, 80.0),
    OrganTraffickingEntity("OT-003", "Égypte & Moyen-Orient — Marché Noir Organes Région", "MENA", "Réfugiés Syriens/Yéménites Donneurs Forcés, Cliniques Privées Istanbul/Le Caire, 150K$ Rein Revendu", 80.0, 78.0, 72.0, 88.0),
    OrganTraffickingEntity("OT-004", "Philippines & Asie du Sud-Est — Hub Tourisme Transplantation", "Asie du Sud-Est", "Manille Hub Transplantation Illicite, Donneurs Ruraux 2000$, Touristes Médicaux Asie/Moyen-Orient & Interdiction 2008 Contournée", 68.0, 88.0, 62.0, 78.0),
    OrganTraffickingEntity("OT-005", "Turquie & Irak — Transit Organes & Réfugiés Vulnérables", "MENA/Europe", "Transit Organes Syrie/Irak, Camps Réfugiés Recrutement, Istanbul Marché Intermédiaire & Chirurgiens Offshore", 55.0, 52.0, 58.0, 62.0),
    OrganTraffickingEntity("OT-006", "Inde & Bangladesh — Industrie Rein & Donneurs Pauvreté", "Asie du Sud", "Villages Rein Bihar/Bengale, Donneurs 1000$ Exploités, Cliniques Chennai Offshore & Prohibition 1994 Contournée", 52.0, 48.0, 55.0, 58.0),
    OrganTraffickingEntity("OT-007", "Moldova & Ukraine — Zones Recrutement Réseaux Europe", "Europe de l'Est", "Crise Post-Soviétique Donneur Désespéré, Réseaux Criminels Est-Ouest, Conflits Armés Exposent Populations", 28.0, 25.0, 32.0, 35.0),
    OrganTraffickingEntity("OT-008", "OMS & Conseil Europe — Régulation Transplantation Mondiale", "Global", "Déclaration d'Istanbul 2008, Convention Oviedo, INTERPOL Operation Libertad & OMS Principes Directeurs Transplantation", 5.0, 4.0, 3.0, 6.0),
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
        "domain": "organ_trafficking",
        "confidence_score": 0.78,
        "data_sources": ["who_organ_trafficking_monitor", "istanbul_declaration_custodian_group", "china_tribunal_2019_report"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_organ_trafficking_index": round(avg / 100 * 10, 2),
    }


def analyze_organ_trafficking() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Organ Trafficking Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
