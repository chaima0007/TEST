"""
Caelum Partners — State Terrorism Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Terrorisme d'État : quand les gouvernements deviennent les bourreaux de leurs citoyens.
Le terrorisme d'État désigne l'utilisation délibérée de la violence, de la terreur
et de la répression par un gouvernement contre sa propre population ou des populations
étrangères. Contrairement au terrorisme non étatique, il bénéficie de l'impunité
structurelle de la souveraineté étatique.

La Corée du Nord représente l'expression la plus totale du terrorisme d'État :
camps de prisonniers politiques (kwanliso) contenant 80 000 à 120 000 détenus
selon le Commissariat aux droits de l'homme de l'ONU, exécutions publiques comme
outil de contrôle social, disparitions forcées systématiques et torture
institutionnalisée. La Commission d'enquête de l'ONU de 2014 a conclu à des
crimes contre l'humanité.

La Syrie sous Assad a utilisé l'appareil d'État comme machine de terreur : torture
de masse dans les prisons secrètes (rapport Caesar — 55 000 photographies de
victimes), bombardements délibérés de populations civiles avec des armes chimiques,
disparitions forcées de 150 000+ personnes. L'Iran combine police des mœurs,
IRGC et assassinats judiciaires pour maintenir la terreur d'État.

Risk levels (terrorisme d'État et répression systémique) :
  critique  -> composite >= 60  (terrorisme d'État — exécutions, torture et disparitions comme politique)
  élevé     -> composite >= 40  (répression systémique — violence d'État documentée contre opposants)
  modéré    -> composite >= 20  (autoritarisme répressif — restrictions avec incidents de violence isolés)
  faible    -> composite < 20   (état de droit exemplaire — garanties judiciaires effectives)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "terrorisme_etat_systematique": {
        "severity_fr": "Critique",
        "action_fr": "Tribunal pénal international d'urgence — mandat CPI pour les dirigeants, isolement diplomatique total et fonds d'indemnisation des victimes financé par gel des avoirs souverains",
        "signal_fr": "extrajudicial_killings_score > 85 — exécutions extrajudiciaires systématiques utilisées comme instrument de gouvernance et répression politique par l'appareil d'État",
    },
    "disparitions_forcees_institutionnalisees": {
        "severity_fr": "Critique",
        "action_fr": "Mécanisme ONU disparitions — liste nominative des disparus, sanctions ciblées sur agents responsables et pression diplomatique sur gouvernements complices",
        "signal_fr": "forced_disappearances_score > 85 — disparitions forcées institutionnalisées comme outil de terreur: enlèvements par forces de sécurité sans reconnaissance de la détention",
    },
    "torture_systematique_etat": {
        "severity_fr": "Critique",
        "action_fr": "Convention ONU torture renforcée — OPCAT imposé aux États défaillants, tribunaux spéciaux pour tortureurs et réhabilitation complète des victimes",
        "signal_fr": "systematic_torture_score > 85 — torture institutionnalisée dans les lieux de détention étatiques avec infrastructures dédiées et formation des agents répressifs",
    },
    "repression_politique_massive": {
        "severity_fr": "Élevé",
        "action_fr": "Conditionnalité diplomatique — suspension accords coopération sécuritaire, rapport spécial rapporteur ONU et soutien aux défenseurs des droits humains",
        "signal_fr": "Répression politique massive — emprisonnements politiques de masse et persécution des opposants sans atteindre le seuil du terrorisme d'État systémique",
    },
    "etat_de_droit_exemplaire": {
        "severity_fr": "Faible",
        "action_fr": "Exporter l'état de droit — coopération judiciaire internationale, formation forces sécurité aux droits humains et aide aux États en transition démocratique",
        "signal_fr": "composite_score < 20 — état de droit effectif: indépendance judiciaire, responsabilité des forces de sécurité et garanties constitutionnelles des libertés",
    },
}


@dataclass
class StateTerrorismEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    extrajudicial_killings_score: float
    forced_disappearances_score: float
    systematic_torture_score: float
    political_mass_imprisonment_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_state_terrorism_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.extrajudicial_killings_score * 0.30
            + self.forced_disappearances_score * 0.25
            + self.systematic_torture_score * 0.25
            + self.political_mass_imprisonment_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_state_terrorism_index = round(self.composite_score / 100 * 10, 2)

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
        if self.extrajudicial_killings_score >= 85:
            return "terrorisme_etat_systematique"
        if self.forced_disappearances_score >= 85:
            return "disparitions_forcees_institutionnalisees"
        if self.systematic_torture_score >= 85:
            return "torture_systematique_etat"
        if self.composite_score >= 20:
            return "repression_politique_massive"
        return "etat_de_droit_exemplaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Terrorisme d'État critique de {n} — exécutions extrajudiciaires, disparitions forcées et torture utilisées comme instruments délibérés de gouvernance par l'appareil sécuritaire",
                "Crimes contre l'humanité documentés — les violations systématiques et généralisées des droits fondamentaux constituent des crimes contre l'humanité selon le Statut de Rome",
                "Culture de l'impunité institutionnalisée — l'absence de responsabilité judiciaire des agents de l'État perpétue les cycles de violence et décourage la dénonciation",
            ]
        if self.risk_level == "élevé":
            return [
                f"Répression politique systémique de {n} — persécution documentée des opposants politiques, journalistes et défenseurs des droits humains par les forces de sécurité",
                "Système judiciaire instrumentalisé — tribunaux d'exception, procès politiques inéquitables et emprisonnements arbitraires servant à neutraliser les opposants",
                "Résistance civile réprimée — manifestations dispersées par la force, ONG dissoutes et espaces civiques réduits à néant par la législation sécuritaire abusive",
            ]
        if self.risk_level == "modéré":
            return [
                f"Autoritarisme répressif de {n} — restrictions des libertés fondamentales avec incidents isolés de violence d'État sans politique systémique de terreur",
                "Tensions institutions-société civile — confrontations récurrentes entre forces de sécurité et manifestants sans atteindre la répression institutionnalisée",
                "Risque de dérive autoritaire — l'affaiblissement des contre-pouvoirs crée des conditions propices à l'escalade répressive",
            ]
        return [
            f"{n} incarne l'état de droit exemplaire — indépendance judiciaire effective, responsabilité des forces de sécurité et garanties constitutionnelles des libertés fondamentales",
            "Mécanismes de contrôle démocratique — commissions d'enquête indépendantes, tribunaux administratifs actifs et protection des lanceurs d'alerte",
            "Modèle de gouvernance sécuritaire à exporter — coopération judiciaire internationale et formation des forces de sécurité aux droits humains",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "extrajudicial_killings_score": self.extrajudicial_killings_score,
            "forced_disappearances_score": self.forced_disappearances_score,
            "systematic_torture_score": self.systematic_torture_score,
            "political_mass_imprisonment_score": self.political_mass_imprisonment_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_state_terrorism_index": self.estimated_state_terrorism_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[StateTerrorismEntity] = [
    StateTerrorismEntity("ST-001", "RPDC/Kim Jong-un — Kwanliso, Exécutions Publiques & Terreur Totale", "Asie du Nord-Est", "80-120K Détenus Camps Politiques, Exécutions Publiques Masse, ONU Crimes Humanité 2014 & Famines Induites", 95.0, 92.0, 90.0, 88.0),
    StateTerrorismEntity("ST-002", "Syrie/Assad — Rapport Caesar, Armes Chimiques & Prisons Secrètes", "MENA", "55 000 Photos Torture Caesar, 150K+ Disparus, Sarin Ghouta 2013 & Saydnaya Prison Abattoir Documentée", 83.0, 90.0, 88.0, 82.0),
    StateTerrorismEntity("ST-003", "Iran/IRGC — Novichok Dissidents, Evin Prison & Exécutions Masse", "MENA", "500+ Exécutés 2023 Record, Assassinats Diaspora Europe, Evin Torture Systémique & Mahsa Amini Répression", 82.0, 82.0, 85.0, 80.0),
    StateTerrorismEntity("ST-004", "Chine/DSN — Sécurité Nationale, Ouïghours & Répression Interne", "Asie", "Xinjiang Disparitions Forcées, Hong Kong 10000+ Arrêtés, Falun Gong Organes & Minorités Emprisonnements Masse", 80.0, 75.0, 78.0, 90.0),
    StateTerrorismEntity("ST-005", "Russie/FSB — Opposants Empoisonnés, Navalny & Répression Anti-Guerre", "Europe de l'Est", "Navalny Assassiné Colonie Pénitentiaire, 19000+ Anti-Guerre Arrêtés, Journalistes Tués & Torture Documentée", 55.0, 52.0, 58.0, 62.0),
    StateTerrorismEntity("ST-006", "Arabie Saoudite/MBS — Khashoggi, Dissidents & Minorité Chiite", "MENA", "Khashoggi Assassinat Ambassade 2018, 81 Exécutions Jour 2022, Nimr Al-Nimr & Chiites Répression Est", 52.0, 48.0, 55.0, 58.0),
    StateTerrorismEntity("ST-007", "Venezuela/Maduro — SEBIN, Colectivos & Opposition Liquidée", "Amérique du Sud", "SEBIN Torture Politique, Colectivos Paramilitaires État, Leopoldo López Emprisonné & 800+ Arbitraires 2019", 28.0, 25.0, 32.0, 35.0),
    StateTerrorismEntity("ST-008", "CPI/CDH ONU — Responsabilité Universelle & État de Droit", "Global", "CPI 124 États Parties, CDH Procédures Spéciales 44 Mandataires, Convention Torture 173 États & OPCAT", 5.0, 4.0, 3.0, 6.0),
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
        "domain": "state_terrorism",
        "confidence_score": 0.85,
        "data_sources": ["amnesty_international_annual_report", "human_rights_watch_world_report", "un_special_rapporteur_torture_reports"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_state_terrorism_index": round(avg / 100 * 10, 2),
    }


def analyze_state_terrorism() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"State Terrorism Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} -> {e.risk_level} ({e.composite_score})")
