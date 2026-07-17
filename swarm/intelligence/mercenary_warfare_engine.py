"""
Caelum Partners — Mercenary Warfare Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La privatisation de la violence : les armées fantômes des États autoritaires.
Les sociétés militaires privées (PMC) sont devenues le vecteur privilégié
des puissances révisionnistes pour projeter leur influence militaire sans
les contraintes du droit international humanitaire, de la responsabilité
parlementaire ou de l'opinion publique. Un mercenaire ne rentre pas dans
un cercueil — il n'y a pas de cérémonie nationale, pas de comptage officiel.

Le Groupe Wagner (aujourd'hui Africa Corps sous GRU) a opéré dans 30+ pays :
Syrie (or, pétrole, soutien Assad), Libye (puits de pétrole), Mali (or),
République Centrafricaine (diamants, uranium), Soudan (or), Mozambique,
et bien sûr Ukraine où il a perdu 30 000 combattants selon les estimations
occidentales. La formule: resources contre sécurité, sans conditionner
l'aide au respect des droits humains ou à la gouvernance démocratique.

Blackwater/Academi (USA) a opéré en Irak (massacre de Nisour Square 2007,
17 civils tués), Afghanistan et a vendu ses services au Pentagone pour
900M$ de contrats. Les EAU/Turquie financent des PMC syriennes, libyennes
et africaines pour leurs guerres par procuration sans engager leurs propres
armées. Au Congo-Kivu, les milices FDLR, M23 et ADF sont financées par les
rentes minières du cobalt, du coltan et de l'or — un nexus minerais-milices
qui alimente à la fois le conflit et les chaînes d'approvisionnement mondiales.

Risk levels (privatisation de la violence et impunité des mercenaires) :
  critique  → composite ≥ 60  (déploiement PMC systémique — guerre privée par procuration avérée)
  élevé     → composite ≥ 40  (instrumentalisation des mercenaires — conflits régionaux nourris)
  modéré    → composite ≥ 20  (prolifération PMC — présence sans doctrine d'accountability)
  faible    → composite < 20  (régulation PMC — cadre légal international en construction)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "deploiement_pmc_etatique": {
        "severity_fr": "Critique",
        "action_fr": "Designation des PMC étatiques comme organisations criminelles et sanctions contre les États commanditaires, avec gel des avoirs",
        "signal_fr": "pmc_deployment_scale_score > 85 AND state_deniability_score > 85 — déploiement PMC étatique systémique avec déni plausible avéré",
    },
    "milices_ressources": {
        "severity_fr": "Critique",
        "action_fr": "Due diligence minerais de sang obligatoire dans les chaînes d'approvisionnement mondiales et sanctions contre les entreprises finançant les milices",
        "signal_fr": "Milices-ressources — financement des forces paramilitaires par les rentes extractives dans les zones de conflit (cobalt, or, coltan, pétrole)",
    },
    "impunite_criminelle_pmc": {
        "severity_fr": "Critique",
        "action_fr": "Juridiction universelle pour les crimes de guerre des mercenaires et ratification du document de Montreux par tous les États déployeurs",
        "signal_fr": "Impunité criminelle PMC — atrocités documentées sans poursuites pénales ni responsabilité devant le droit international humanitaire",
    },
    "instrumentalisation_mercenaires": {
        "severity_fr": "Élevé",
        "action_fr": "Transparence des contrats PMC, registres publics des déploiements et mécanismes de responsabilité parlementaire pour les opérations privées",
        "signal_fr": "Instrumentalisation des mercenaires — forces privées utilisées pour contourner les contraintes politiques et juridiques des armées régulières",
    },
    "regulation_pmc_emergeante": {
        "severity_fr": "Faible",
        "action_fr": "Accélérer la ratification et l'application du Document de Montreux et développer une convention internationale contraignante sur les PMC",
        "signal_fr": "composite_score < 20 — cadre réglementaire PMC en construction — document de Montreux et normes ICoCA comme modèle de régulation",
    },
}


@dataclass
class MercenaryWarfareEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    pmc_deployment_scale_score: float
    state_deniability_score: float
    atrocity_impunity_score: float
    resource_extraction_violence_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_mercenary_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.pmc_deployment_scale_score * 0.30
            + self.state_deniability_score * 0.25
            + self.atrocity_impunity_score * 0.25
            + self.resource_extraction_violence_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_mercenary_index = round(self.composite_score / 100 * 10, 2)

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
        if self.pmc_deployment_scale_score >= 85 and self.state_deniability_score >= 85:
            return "deploiement_pmc_etatique"
        if self.resource_extraction_violence_score >= 85:
            return "milices_ressources"
        if self.atrocity_impunity_score >= 85:
            return "impunite_criminelle_pmc"
        if self.composite_score >= 20:
            return "instrumentalisation_mercenaires"
        return "regulation_pmc_emergeante"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Déploiement PMC systémique par {n} — armées privées projetées en zones de conflit avec déni étatique institutionnalisé",
                "Crimes de guerre sans responsabilité — massacres, tortures et pillages commis par des forces privées sans poursuites pénales",
                "Nexus minerais-milices — ressources extractives financent directement le recrutement et l'armement des forces paramilitaires",
            ]
        if self.risk_level == "élevé":
            return [
                f"Instrumentalisation des mercenaires par {n} — forces privées contournant les contraintes politiques des armées régulières",
                "Guerres par délégation — conflits régionaux alimentés par des PMC permettant la projection d'influence sans engagement officiel",
                "Impunité partielle — mécanismes de responsabilité insuffisants face aux abus documentés des contractuels militaires privés",
            ]
        if self.risk_level == "modéré":
            return [
                f"Prolifération PMC dans {n} — présence de forces privées sans cadre légal et accountability adéquats",
                "Zone grise juridique — contractuels militaires opérant dans des espaces où le droit international humanitaire est mal appliqué",
                "Risque d'escalade — PMC sans doctrine d'engagement claire pouvant déclencher des incidents non souhaités",
            ]
        return [
            f"{n} développe un cadre de régulation PMC fondé sur le Document de Montreux et les normes ICoCA",
            "Transparence contractuelle — registres publics des déploiements de PMC et mécanismes de responsabilité parlementaire",
            "Modèle de régulation à internationaliser — convention contraignante sur les PMC en gestation multilatérale",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "pmc_deployment_scale_score": self.pmc_deployment_scale_score,
            "state_deniability_score": self.state_deniability_score,
            "atrocity_impunity_score": self.atrocity_impunity_score,
            "resource_extraction_violence_score": self.resource_extraction_violence_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_mercenary_index": self.estimated_mercenary_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[MercenaryWarfareEntity] = [
    MercenaryWarfareEntity("MW-001", "Russie — Wagner/Africa Corps & 30 Pays Déployés", "Europe de l'Est", "Africa Corps GRU (ex-Wagner), RCA/Mali/Libye/Ukraine & Ressources contre Sécurité", 92.0, 90.0, 88.0, 82.0),
    MercenaryWarfareEntity("MW-002", "USA — Blackwater/Academi & Contrats Pentagone", "Amérique du Nord", "Academi ex-Blackwater, Nisour Square 17 Civils & 900M$ Contrats Iraq/Afghanistan", 72.0, 85.0, 88.0, 68.0),
    MercenaryWarfareEntity("MW-003", "EAU & Turquie — PMC Régionales Syrie/Libye", "MENA", "SNA Turquie Syrie, Milices Libyennes EAU & PMC Azerbaïdjan Nagorno-Karabakh", 88.0, 88.0, 75.0, 72.0),
    MercenaryWarfareEntity("MW-004", "Congo-Kivu — Milices Cobalt, Or & Coltan", "Afrique Centrale", "FDLR, M23 & ADF Financés par Minerais Sang — Cobalt Batteries EV via Milices", 82.0, 78.0, 75.0, 90.0),
    MercenaryWarfareEntity("MW-005", "Sahel — Africa Corps & Gouvernements Militaires", "Afrique de l'Ouest", "Mali/Burkina/Niger Juntes Contractant Africa Corps Contre Or & Uranium", 58.0, 52.0, 60.0, 55.0),
    MercenaryWarfareEntity("MW-006", "Libye — Marché PMC Fragmenté Multi-Acteurs", "MENA", "PMC Turques, Russes, Émiraties & Tchadiennes en Concurrence sur Pétrole Libyen", 52.0, 48.0, 55.0, 50.0),
    MercenaryWarfareEntity("MW-007", "Ukraine — Légion Étrangère & Volontaires Régulés", "Europe", "Légion Étrangère Ukraine, ITAR Limites & Tentative de Régulation des Combattants", 30.0, 28.0, 35.0, 22.0),
    MercenaryWarfareEntity("MW-008", "ICRC & Document Montreux — Régulation PMC", "Global", "Document Montreux 2008, ICoCA & Droit International Humanitaire PMC en Négociation", 5.0, 4.0, 6.0, 4.0),
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
        "domain": "mercenary_warfare",
        "confidence_score": 0.79,
        "data_sources": ["acled_armed_conflict_pmc_tracker", "geneva_academy_mercenary_monitor", "private_security_monitor_uk"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_mercenary_index": round(avg / 100 * 10, 2),
    }


def analyze_mercenary_warfare() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Mercenary Warfare Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
