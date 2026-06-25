"""
Caelum Partners — Digital Privacy & Surveillance Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Droit à la vie privée numérique face aux systèmes de surveillance de masse.
La surveillance numérique de masse est devenue l'un des instruments de contrôle les
plus redoutables des régimes autoritaires et des démocraties en dérive sécuritaire.
La reconnaissance faciale biométrique, les systèmes SORM d'interception totale, les
logiciels espions Pegasus et l'absence de lois de protection des données constituent
les quatre vecteurs principaux d'atteinte au droit à la vie privée consacré à
l'article 17 du PIDCP.

La Chine a déployé le système de Crédit Social couvrant 1.4 milliard de personnes,
600 millions de caméras de vidéosurveillance, et cible spécifiquement la minorité
ouïghoure au Xinjiang avec une surveillance biométrique, génétique et comportementale
sans précédent. La Russie maintient le système SORM-3 permettant au FSB un accès
temps réel à toutes les communications sans mandat judiciaire. L'Iran a coupé internet
pendant les manifestations de 2022 en réponse à la mort de Mahsa Amini. Les États-Unis
maintiennent le programme PRISM de collecte massive via la Section 702 du FISA.

Risk levels (vie privée numérique et surveillance) :
  critique  → composite ≥ 60  (surveillance totale — atteinte systémique au droit à la vie privée)
  élevé     → composite ≥ 40  (surveillance ciblée — violations documentées et lacunes légales)
  modéré    → composite ≥ 20  (dérive réglementaire — capacités sans contre-pouvoirs adéquats)
  faible    → composite < 20  (protection exemplaire — RGPD fort et supervision indépendante)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "surveillance_biometrique_totale": {
        "severity_fr": "Critique",
        "action_fr": "Moratoire mondial sur la reconnaissance faciale — interdiction des bases de données biométriques de masse sans consentement et sanctions contre les États exportateurs de surveillance",
        "signal_fr": "mass_surveillance_biometric_score > 85 AND spyware_score > 80 — surveillance biométrique totalitaire ciblant citoyens, minorités et journalistes",
    },
    "shutdown_internet_censure_nationale": {
        "severity_fr": "Critique",
        "action_fr": "Internet comme droit fondamental — mécanisme de responsabilité ONU pour les coupures internet et financement des technologies de contournement",
        "signal_fr": "internet_shutdown_score > 85 — coupures internet nationales systémiques utilisées comme arme de répression des manifestations",
    },
    "espionnage_cible_journalistes": {
        "severity_fr": "Critique",
        "action_fr": "Interdiction commerciale des spywares — réglementation internationale NSO Group/Pegasus et poursuites judiciaires contre les États clients",
        "signal_fr": "spyware_journalist_score > 80 — déploiement de logiciels espions contre journalistes, défenseurs des droits humains et opposants politiques",
    },
    "collecte_masse_sans_cadre_legal": {
        "severity_fr": "Élevé",
        "action_fr": "Réforme surveillance — supervision judiciaire indépendante des programmes de renseignement et loi fédérale de protection des données",
        "signal_fr": "Collecte massive de données sans cadre légal adéquat — surveillance sans mandat et absence de loi fédérale de protection des données",
    },
    "protection_vie_privee_exemplaire": {
        "severity_fr": "Faible",
        "action_fr": "Exporter le modèle RGPD — coopération internationale sur les standards de protection des données et financement des régulateurs indépendants",
        "signal_fr": "composite_score < 20 — protection exemplaire de la vie privée numérique — RGPD effectif et surveillance proportionnée",
    },
}


@dataclass
class DigitalPrivacySurveillanceRightsEntity:
    entity_id: str
    name: str
    country: str
    mass_surveillance_biometric_dragnet_severity_score: float
    internet_shutdown_censorship_scale_score: float
    spyware_targeted_surveillance_journalist_score: float
    data_protection_gdpr_enforcement_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_digital_privacy_surveillance_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.mass_surveillance_biometric_dragnet_severity_score * 0.30
            + self.internet_shutdown_censorship_scale_score * 0.25
            + self.spyware_targeted_surveillance_journalist_score * 0.25
            + self.data_protection_gdpr_enforcement_deficit_gap_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_digital_privacy_surveillance_rights_index = round(self.composite_score / 100 * 10, 2)

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
        if self.mass_surveillance_biometric_dragnet_severity_score >= 85 and self.spyware_targeted_surveillance_journalist_score >= 80:
            return "surveillance_biometrique_totale"
        if self.internet_shutdown_censorship_scale_score >= 85:
            return "shutdown_internet_censure_nationale"
        if self.spyware_targeted_surveillance_journalist_score >= 80:
            return "espionnage_cible_journalistes"
        if self.composite_score >= 20:
            return "collecte_masse_sans_cadre_legal"
        return "protection_vie_privee_exemplaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Surveillance totale par {n} — atteinte systémique au droit à la vie privée numérique de la population entière",
                "Biométrie de masse et reconnaissance faciale — identification et traçage de chaque citoyen sans consentement ni recours judiciaire",
                "Ciblage journalistes et défenseurs — spywares et interception ciblée pour réduire au silence les voix critiques",
            ]
        if self.risk_level == "élevé":
            return [
                f"Violations documentées par {n} — lacunes légales permettant la surveillance sans mandat et collecte massive de données",
                "Absence de loi fédérale de protection des données — vide réglementaire exploité par agences de renseignement et acteurs privés",
                "Surveillance ciblée opposants — utilisation de spywares et programmes de renseignement contre militants et journalistes",
            ]
        if self.risk_level == "modéré":
            return [
                f"Dérive réglementaire de {n} — capacités de surveillance croissantes sans contre-pouvoirs institutionnels adéquats",
                "RGPD en application inégale — régulation existante mais application incohérente entre États membres et secteurs",
                "Propositions de surveillance de masse — Chatcontrol et rétention des métadonnées menaçant le droit à la vie privée",
            ]
        return [
            f"{n} protège exemplarité le droit à la vie privée — RGPD strict, supervision indépendante et limites légales effectives",
            "Rapporteur spécial ONU — mécanismes de responsabilité internationale pour les violations du droit à la vie privée",
            "Article 17 PIDCP — cadre normatif universel pour la protection de la vie privée numérique dans le droit international",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "composite_score": self.composite_score,
            "mass_surveillance_biometric_dragnet_severity_score": self.mass_surveillance_biometric_dragnet_severity_score,
            "internet_shutdown_censorship_scale_score": self.internet_shutdown_censorship_scale_score,
            "spyware_targeted_surveillance_journalist_score": self.spyware_targeted_surveillance_journalist_score,
            "data_protection_gdpr_enforcement_deficit_gap_score": self.data_protection_gdpr_enforcement_deficit_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_digital_privacy_surveillance_rights_index": self.estimated_digital_privacy_surveillance_rights_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[DigitalPrivacySurveillanceRightsEntity] = [
    DigitalPrivacySurveillanceRightsEntity(
        "DPS-001",
        "Chine — Crédit Social, Reconnaissance Faciale 600M Caméras, Surveillance Ouïghours Xinjiang & Firewall",
        "Chine",
        96.0, 92.0, 88.0, 94.0,
    ),
    DigitalPrivacySurveillanceRightsEntity(
        "DPS-002",
        "Russie — SORM-3 Surveillance Totale, Blocage VPN, Journalistes Pegasus & Données Trafic FSB Obligatoire",
        "Russie",
        90.0, 88.0, 85.0, 90.0,
    ),
    DigitalPrivacySurveillanceRightsEntity(
        "DPS-003",
        "Iran — Surveillance Protestants 2022, Coupures Internet Nationales, Telegram Bloqué & Reconnaissance Faciale Hijab",
        "Iran",
        82.0, 92.0, 83.0, 88.0,
    ),
    DigitalPrivacySurveillanceRightsEntity(
        "DPS-004",
        "USA/NSA — PRISM Mass Collection, Pegasus Civils, Section 702 FISA & Absence Loi Fédérale Protection Données",
        "États-Unis",
        85.0, 72.0, 83.0, 88.0,
    ),
    DigitalPrivacySurveillanceRightsEntity(
        "DPS-005",
        "Inde — Internet Shutdown 84× En 2023, UAPA Surveillance Activistes, Aadhaar Biométrique Obligatoire & Pegasus Journalistes",
        "Inde",
        55.0, 58.0, 53.0, 50.0,
    ),
    DigitalPrivacySurveillanceRightsEntity(
        "DPS-006",
        "UE — Chatcontrol Proposé, RGPD Application Inégale, Métadonnées Stockées & Frontex Surveillance Biométrique",
        "Union Européenne",
        42.0, 45.0, 50.0, 55.0,
    ),
    DigitalPrivacySurveillanceRightsEntity(
        "DPS-007",
        "EFF/Privacy International — Rapports Surveillance, Outils Defense Numérique, Advocacy GDPR & Standards Chiffrement",
        "International",
        25.0, 26.0, 28.0, 25.0,
    ),
    DigitalPrivacySurveillanceRightsEntity(
        "DPS-008",
        "ONU/Art.17 PIDCP — Droit à la Vie Privée, Rapporteur Spécial Surveillance & SDG 16.10 Liberté Information",
        "International",
        4.0, 3.0, 4.0, 5.0,
    ),
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
        "agent": "digital_privacy_surveillance_rights_engine",
        "domain": "digital_privacy_surveillance_rights",
        "total_entities": n,
        "avg_composite": avg,
        "confidence_score": 0.85,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": top_risk,
        "critical_alerts": critical_alerts,
        "last_analysis": "2026-06-21",
        "engine_version": "1.0.0",
        "avg_estimated_digital_privacy_surveillance_rights_index": round(avg / 100 * 10, 2),
        "data_sources": [
            "privacy_international_global_surveillance_report",
            "freedom_house_freedom_net_annual_report",
            "citizen_lab_spyware_targeted_surveillance_database",
        ],
        "entities": [e.to_dict() for e in entities],
    }


def analyze_digital_privacy_surveillance_rights() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    import json
    r = summary()
    print(f"Digital Privacy & Surveillance Rights Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    print(f"Distribution: {r['risk_distribution']}")
    print(f"avg_estimated_index: {r['avg_estimated_digital_privacy_surveillance_rights_index']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name[:60]} → {e.risk_level} ({e.composite_score})")
