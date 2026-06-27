"""
Caelum Partners — Diaspora Weaponization Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
L'instrumentalisation des diasporas comme bras armé de la politique
étrangère : les États autoritaires ont découvert que leurs ressortissants
à l'étranger constituent un réseau d'influence, de surveillance et de
coercition sans précédent. Loin d'être de simples émigrants, les diasporas
deviennent des agents involontaires ou consentants des régimes qu'ils ont
fuis — ou prolongent leur soutien aux gouvernements d'origine.

La Chine opère un réseau mondial de "postes de police" (stations de service
communautaires) recensés dans 53 pays par Safeguard Defenders — utilisés
pour intimider, surveiller et rapatrier de force les dissidents chinois à
l'étranger. L'Iran harcèle, surveille et planifie des assassinats contre
les Irano-Américains critiques du régime. La Turquie mobilise les Turco-
Belges et Turco-Allemands pour voter aux référendums d'Erdoğan et signale
les opposants aux ambassades. La Russie orchestre les "compatriotes"
(sootechiestvenniki) à travers le Fonds Poutine — utilisant les
russophones comme prétexte d'intervention (Crimée, Géorgie, Ukraine).

Les transferts d'argent (remittances) constituent un levier sous-estimé :
en contrôlant ou menaçant de bloquer les transferts de fonds, les régimes
peuvent contraindre leur diaspora à se soumettre ou à subventionner
le régime pour protéger leurs familles restées au pays.

Risk levels (instrumentalisation et répression transnationale des diasporas) :
  critique  → composite ≥ 60  (répression transnationale systémique — persécutions avérées)
  élevé     → composite ≥ 40  (pression politique diasporique significative — surveillance)
  modéré    → composite ≥ 20  (instrumentalisation partielle — mobilisation sans harcèlement)
  faible    → composite < 20  (protection des diasporas — cadre légal anti-répression)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "surveillance_diaspora_totale": {
        "severity_fr": "Critique",
        "action_fr": "Fermeture des postes de police étrangers illicites et sanctions contre les États pratiquant la répression transnationale",
        "signal_fr": "diaspora_political_mobilization_score > 80 AND transnational_surveillance_score > 80 — surveillance et contrôle total de la diaspora",
    },
    "instrumentalisation_remittances": {
        "severity_fr": "Critique",
        "action_fr": "Protection des canaux de transfert de fonds et sanctions contre l'utilisation des remittances comme levier de coercition",
        "signal_fr": "Instrumentalisation des remittances — contrôle des transferts d'argent comme outil de pression sur la diaspora",
    },
    "levier_diaspora_politique": {
        "severity_fr": "Élevé",
        "action_fr": "Encadrement légal des activités politiques étrangères dans les pays d'accueil et protection des membres de diaspora",
        "signal_fr": "Levier diaspora politique — mobilisation des communautés immigrées à des fins de politique étrangère du pays d'origine",
    },
    "diaspora_conflict_export": {
        "severity_fr": "Modéré",
        "action_fr": "Surveillance des conflits ethniques et politiques exportés via les diasporas et soutien aux communautés menacées",
        "signal_fr": "Export de conflits — tensions politiques ou ethniques du pays d'origine transposées dans les communautés diasporiques",
    },
    "protection_diaspora_droits": {
        "severity_fr": "Faible",
        "action_fr": "Partager les modèles de protection des diasporas et renforcer les législations anti-répression transnationale",
        "signal_fr": "composite_score < 20 — cadre légal protégeant les droits des membres de diaspora contre les ingérences étrangères",
    },
}


@dataclass
class DiasporaWeaponizationEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    diaspora_political_mobilization_score: float
    transnational_surveillance_score: float
    remittance_leverage_score: float
    diaspora_espionage_recruitment_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_diaspora_weapon_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.diaspora_political_mobilization_score * 0.30
            + self.transnational_surveillance_score * 0.25
            + self.remittance_leverage_score * 0.25
            + self.diaspora_espionage_recruitment_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_diaspora_weapon_index = round(self.composite_score / 100 * 10, 2)

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
        if self.diaspora_political_mobilization_score >= 80 and self.transnational_surveillance_score >= 80:
            return "surveillance_diaspora_totale"
        if self.remittance_leverage_score >= 80:
            return "instrumentalisation_remittances"
        if self.composite_score >= 40:
            return "levier_diaspora_politique"
        if self.composite_score >= 20:
            return "diaspora_conflict_export"
        return "protection_diaspora_droits"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Répression transnationale systémique par {n} — surveillance, harcèlement et coercition des diasporas à l'étranger",
                "Postes de police étrangers illicites — agents consulaires ou associatifs utilisés pour surveiller et intimider les dissidents expatriés",
                "Weaponisation des familles restées au pays — menaces sur les proches utilisées pour forcer les membres de diaspora à se soumettre",
            ]
        if self.risk_level == "élevé":
            return [
                f"Pression politique diasporique significative par {n} — mobilisation et surveillance des communautés immigrées",
                "Ingérence électorale via diaspora — vote diasporique influencé par pressions consulaires et mobilisation identitaire",
                "Transferts d'argent conditionnés — pression informelle sur les remittances pour discipliner les membres non-conformes",
            ]
        if self.risk_level == "modéré":
            return [
                f"Instrumentalisation partielle de la diaspora de {n} — tensions politiques exportées sans harcèlement systématique",
                "Conflits d'identité communautaires — factions politiques du pays d'origine reproduites dans les associations diasporiques",
                "Surveillance informelle — réseaux de signalement communautaires sans organisation étatique formelle",
            ]
        return [
            f"{n} protège les membres de diaspora contre les ingérences étrangères — cadre légal anti-répression transnationale",
            "Législation FARA/anti-ingérence étrangère appliquée — postes de police illicites identifiés et démantelés",
            "Modèle de protection des droits diasporiques — espace sûr pour les communautés immigrées sans coercition d'origine",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "diaspora_political_mobilization_score": self.diaspora_political_mobilization_score,
            "transnational_surveillance_score": self.transnational_surveillance_score,
            "remittance_leverage_score": self.remittance_leverage_score,
            "diaspora_espionage_recruitment_score": self.diaspora_espionage_recruitment_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_diaspora_weapon_index": self.estimated_diaspora_weapon_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[DiasporaWeaponizationEntity] = [
    DiasporaWeaponizationEntity("DW-001", "Chine — Postes Police Étrangère & OCI Mondial", "Asie", "53 Postes Police Illicites dans 53 Pays & Surveillance Chinois d'Outre-Mer", 90.0, 92.0, 85.0, 88.0),
    DiasporaWeaponizationEntity("DW-002", "Iran — IRGC & Harcèlement Irano-Américains", "MENA", "Réseaux IRGC Traquant Dissidents Irano-Américains & Plans Assassinats", 82.0, 88.0, 75.0, 85.0),
    DiasporaWeaponizationEntity("DW-003", "Russie — Compatriotes & Manipulation Russophones", "Europe de l'Est", "Fonds Poutine 'Compatriotes' & Diaspora Russe comme Levier Géopolitique", 85.0, 82.0, 78.0, 80.0),
    DiasporaWeaponizationEntity("DW-004", "Turquie — Diaspora Belge/Allemande Erdoğan", "MENA/Europe", "DITIB Mobilisant Turco-Européens pour Référendums & Signalement Opposants", 80.0, 72.0, 82.0, 75.0),
    DiasporaWeaponizationEntity("DW-005", "Maroc — CCME & Instrumentalisation MRE", "MENA/Europe", "CCME Outil Soft Power & Comunautés Marocaines Europe sous Influence Rabat", 58.0, 55.0, 60.0, 48.0),
    DiasporaWeaponizationEntity("DW-006", "Inde — Diaspora BJP & Hindutva Exporté", "Asie du Sud", "Modi Diaspora Events & Hindutva Exporté aux USA/UK via Communautés Indiennes", 52.0, 45.0, 48.0, 55.0),
    DiasporaWeaponizationEntity("DW-007", "Éthiopie — Diaspora Mobilisée Guerre Tigré", "Afrique de l'Est", "Diaspora Éthiopienne Divisée & Financement Conflit Tigré depuis Diasporas", 32.0, 28.0, 35.0, 25.0),
    DiasporaWeaponizationEntity("DW-008", "Canada & Allemagne — Protections Anti-Répression", "Global", "FARA Canadien & BfV Allemand Démantèlent Réseaux de Surveillance Étrangers", 6.0, 4.0, 5.0, 3.0),
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
        "domain": "diaspora_weapon",
        "confidence_score": 0.80,
        "data_sources": ["freedom_house_transnational_repression", "safeguard_defenders_police_stations", "ndi_diaspora_political_influence"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_diaspora_weapon_index": round(avg / 100 * 10, 2),
    }


def analyze_diaspora_weaponization() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Diaspora Weaponization Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
