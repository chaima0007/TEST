"""
Caelum Partners — Sanctions Evasion Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
L'évasion des sanctions : comment les États parias contournent l'ordre économique.
Les sanctions internationales sont l'instrument de pression économique privilégié
des démocraties — mais les États sanctionnés ont développé des écosystèmes
sophistiqués pour les contourner : flotte fantôme de pétroliers opaque, réseaux
de sociétés écrans multijuridictionnels, cryptomonnaies non traçables et corridors
bancaires alternatifs hors SWIFT.

La Russie opère une flotte fantôme de 400+ pétroliers sous pavillons de complaisance
pour exporter 6,8Md$ de pétrole/mois malgré le plafond des G7. L'Iran écoule
son pétrole vers la Chine et l'Inde via des intermédiaires malaisiens et émiratis,
contournant l'architecture de sanctions de l'OFAC depuis 40 ans. La Corée du Nord
a volé 3Md$ en cryptomonnaies via le groupe Lazarus pour financer son programme
nucléaire, rendant les sanctions conventionnelles inefficaces.

Le Venezuela de Maduro utilise l'or illicite via des circuits guyanais et
dominicains. Le réseau hawala et les banques de correspondance en Turquie,
aux EAU et en Chine servent de hub d'évitement systémique pour de multiples
régimes sanctionnés. L'OFAC identifie 40+ nouvelles entités par mois — la
course-poursuite est structurellement défavorable aux sanctions.

Risk levels (évasion de sanctions et contournement financier) :
  critique  → composite ≥ 60  (évasion systématique — infrastructure organisée de contournement des sanctions)
  élevé     → composite ≥ 40  (fraude financière étatique — réseaux actifs hors-SWIFT et shadow banking)
  modéré    → composite ≥ 20  (hub de contournement régional — facilitation passive sans contrôle suffisant)
  faible    → composite < 20  (conformité sanctions — application rigoureuse des régimes OFAC/FATF)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "evasion_sanctions_systematique": {
        "severity_fr": "Critique",
        "action_fr": "Sanctions secondaires ciblant les facilitateurs — banques de correspondance, opérateurs pétroliers et armateurs complices de la flotte fantôme",
        "signal_fr": "shadow_fleet_oil_score > 85 AND shell_company_network_score > 85 — infrastructure d'évasion de sanctions systémique et organisée",
    },
    "cryptomonnaies_armes_sanctions": {
        "severity_fr": "Critique",
        "action_fr": "Régulation crypto anti-sanctions — obligations KYC/AML sur les exchanges, traçabilité blockchain obligatoire et sanctions ciblées sur les mixers",
        "signal_fr": "crypto_sanctions_bypass_score > 85 — cryptomonnaies utilisées comme vecteur principal de contournement des sanctions internationales",
    },
    "reseau_societes_ecrans": {
        "severity_fr": "Critique",
        "action_fr": "Transparence des bénéficiaires effectifs — registres publics des propriétaires réels et fermeture des juridictions opaques complices",
        "signal_fr": "shell_company_network_score > 85 — réseau de sociétés écrans multijuridictionnels pour masquer les transactions sanctionnées",
    },
    "fraude_financiere_etatique": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement des mécanismes FATF — liste grise/noire des juridictions non coopératives et pression diplomatique sur les hubs de contournement",
        "signal_fr": "Fraude financière étatique — recours à des circuits alternatifs hors-SWIFT et shadow banking pour contourner les sanctions",
    },
    "conformite_sanctions": {
        "severity_fr": "Faible",
        "action_fr": "Modèle d'application des sanctions à internationaliser — partager les mécanismes de conformité et renforcer la coopération OFAC/UE",
        "signal_fr": "composite_score < 20 — application rigoureuse des régimes de sanctions et coopération multilatérale OFAC/FATF exemplaire",
    },
}


@dataclass
class SanctionsEvasionEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    shadow_fleet_oil_score: float
    crypto_sanctions_bypass_score: float
    shell_company_network_score: float
    correspondent_banking_evasion_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_sanctions_evasion_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.shadow_fleet_oil_score * 0.30
            + self.crypto_sanctions_bypass_score * 0.25
            + self.shell_company_network_score * 0.25
            + self.correspondent_banking_evasion_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_sanctions_evasion_index = round(self.composite_score / 100 * 10, 2)

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
        if self.shadow_fleet_oil_score >= 85 and self.shell_company_network_score >= 85:
            return "evasion_sanctions_systematique"
        if self.crypto_sanctions_bypass_score >= 85:
            return "cryptomonnaies_armes_sanctions"
        if self.shell_company_network_score >= 85:
            return "reseau_societes_ecrans"
        if self.composite_score >= 20:
            return "fraude_financiere_etatique"
        return "conformite_sanctions"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Évasion de sanctions systématique par {n} — infrastructure organisée de contournement avec déni de responsabilité étatique",
                "Flotte fantôme et réseaux opaques — pétroliers sous pavillons de complaisance, sociétés écrans et corridors bancaires alternatifs",
                "Subversion de l'ordre économique international — les sanctions perdent leur effet dissuasif face à des écosystèmes d'évasion industriels",
            ]
        if self.risk_level == "élevé":
            return [
                f"Fraude financière étatique par {n} — recours actif aux circuits alternatifs SWIFT pour contourner les restrictions internationales",
                "Shadow banking et hawala — transferts informels et correspondants bancaires complices dans les juridictions non coopératives",
                "Financement d'activités proscrites — évasion des sanctions alimentant le développement d'armes et programmes proliférants",
            ]
        if self.risk_level == "modéré":
            return [
                f"Hub de contournement régional — {n} facilite passivement l'évasion de sanctions sans mécanismes de contrôle suffisants",
                "Supervision insuffisante — lacunes réglementaires permettant le transit de fonds et marchandises sanctionnées sur le territoire",
                "Risque de sanctions secondaires — exposition aux mesures punitives américaines pour facilitation d'évasion de sanctions",
            ]
        return [
            f"{n} maintient une conformité exemplaire aux régimes de sanctions — application rigoureuse OFAC/FATF et coopération internationale",
            "Registres de bénéficiaires effectifs transparents — propriété réelle vérifiable et blocage des sociétés écrans sanctionnées",
            "Modèle d'application des sanctions à diffuser — partage de renseignement financier et coordination multilatérale anti-évasion",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "shadow_fleet_oil_score": self.shadow_fleet_oil_score,
            "crypto_sanctions_bypass_score": self.crypto_sanctions_bypass_score,
            "shell_company_network_score": self.shell_company_network_score,
            "correspondent_banking_evasion_score": self.correspondent_banking_evasion_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_sanctions_evasion_index": self.estimated_sanctions_evasion_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[SanctionsEvasionEntity] = [
    SanctionsEvasionEntity("SE-001", "Russie — Shadow Fleet 400+ Pétroliers & Contournement G7", "Europe de l'Est", "Fleet Fantôme Pavillon Gabon/Palau, Pétrole via Inde/Chine & Plafond 60$/Baril Ignoré", 92.0, 85.0, 88.0, 80.0),
    SanctionsEvasionEntity("SE-002", "Iran — NIOC & 40 Ans d'Évasion OFAC Industrielle", "MENA", "Pétrole Fantôme via Malaisie/EAU, SWIFT alternatif & Or contre Marchandises Sanctionnées", 88.0, 80.0, 85.0, 82.0),
    SanctionsEvasionEntity("SE-003", "Corée du Nord — Lazarus & 3Md$ Cryptos Volés", "Asie", "Groupe Lazarus, Ronin Bridge Hack 625M$ & Mixers Tornado Cash pour Financement Nucléaire", 72.0, 95.0, 78.0, 68.0),
    SanctionsEvasionEntity("SE-004", "Venezuela — Or Illicite CLAP & Routes Caribéennes", "Amérique du Sud", "Or Illicite via Guyane/Dominique, Maduro CLAP Corruption & Cryptomonnaies Petro Étatiques", 82.0, 72.0, 88.0, 75.0),
    SanctionsEvasionEntity("SE-005", "Myanmar — Junte & Shadow Banking ASEAN", "Asie du Sud-Est", "Juntes TATMADAW, Banques Thaïlandes Complices & Jade/Rubis Illicites via Chine", 55.0, 52.0, 62.0, 58.0),
    SanctionsEvasionEntity("SE-006", "Cuba & Nicaragua — Routes Caïmans & Panama", "Amérique Centrale", "CIMEX Cuba Offshore, Bancorp Nicaragua & Remises Diaspora Contournant Sanctions OFAC", 48.0, 55.0, 52.0, 45.0),
    SanctionsEvasionEntity("SE-007", "Turquie & EAU — Hubs Régionaux de Contournement", "MENA/Europe", "Istanbul Hub Russe Post-Sanctions, Dubaï Or Russe & Correspondants Bancaires Non-Coopératifs", 32.0, 28.0, 38.0, 42.0),
    SanctionsEvasionEntity("SE-008", "OFAC & FATF — Conformité Sanctions Multilatérale", "Global", "SDN List 10000+ Entités, FATF Recommandations & Coordination G7/UE Sanctions Ciblées", 5.0, 4.0, 3.0, 6.0),
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
        "domain": "sanctions_evasion",
        "confidence_score": 0.82,
        "data_sources": ["ofac_sdn_sanctions_tracker", "fatf_grey_list_monitor", "kyckr_shadow_fleet_database"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_sanctions_evasion_index": round(avg / 100 * 10, 2),
    }


def analyze_sanctions_evasion() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Sanctions Evasion Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
