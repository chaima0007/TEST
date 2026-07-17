"""
Caelum Partners — Algorithmic Surveillance Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La surveillance algorithmique de masse comme infrastructure du contrôle
géopolitique : l'État qui surveille numériquement chacun de ses citoyens
en temps réel dispose d'un outil de contrôle social sans précédent dans
l'histoire humaine. La reconnaissance faciale, l'analyse comportementale,
le scoring social, et la surveillance des métadonnées créent des États
omniscients capables de prédire et prévenir toute dissidence.

La Chine a déployé le Système de Crédit Social — scoring comportemental
liant notes de confiance à des privilèges ou restrictions. Xinjiang est
le laboratoire mondial de la surveillance ethno-numérique totale : 1
caméra pour 5 habitants, reconnaissance faciale obligatoire à chaque
carrefour, téléphones inspectés aux checkpoints. La technologie chinoise
de surveillance est exportée — à l'Éthiopie (Huawei), au Zimbabwe (Cloudwalk),
au Pakistan, en Équateur. Les démocraties ne sont pas à l'abri : le système
américain PRISM/XKeyscore surveille les métadonnées à l'échelle planétaire,
Palantir équipe les forces de l'ordre mondiales, et les régimes RGPD peinent
à contenir la surveillance commerciale. La liberté algorithmique est
le défi géopolitique majeur du XXIe siècle.

Risk levels (surveillance algorithmique et contrôle des populations) :
  critique  → composite ≥ 60  (surveillance de masse systémique — libertés civiles menacées)
  élevé     → composite ≥ 40  (surveillance avancée avec risques significatifs pour les droits)
  modéré    → composite ≥ 20  (surveillance partielle sans garanties suffisantes)
  faible    → composite < 20  (cadre légal protecteur et surveillance limitée et encadrée)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "totalitarisme_numerique": {
        "severity_fr": "Critique",
        "action_fr": "Sanctions contre les régimes de surveillance totale et soutien aux opposants numériques",
        "signal_fr": "biometric_surveillance_score > 80 AND social_scoring_score > 75 — totalitarisme numérique",
    },
    "export_technologie_surveillance": {
        "severity_fr": "Critique",
        "action_fr": "Contrôle strict des exportations de technologies de surveillance vers régimes autoritaires",
        "signal_fr": "Exportation de technologies de surveillance — régime autoritaire fournissant outils à d'autres",
    },
    "surveillance_securitaire_excessive": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement des garanties légales contre la surveillance de masse et supervision judiciaire",
        "signal_fr": "Surveillance sécuritaire excessive — États démocratiques dépassant les limites légales admissibles",
    },
    "derive_commerciale": {
        "severity_fr": "Modéré",
        "action_fr": "Renforcement du RGPD et réglementation stricte de l'utilisation commerciale des données biométriques",
        "signal_fr": "Dérive commerciale — surveillance exercée par des plateformes privées avec supervision insuffisante",
    },
    "cadre_protecteur": {
        "severity_fr": "Faible",
        "action_fr": "Partager les modèles de régulation de la surveillance et promouvoir les standards internationaux",
        "signal_fr": "composite_score < 20 — cadre légal protecteur avec surveillance limitée et supervision robuste",
    },
}


@dataclass
class AlgorithmicSurveillanceEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    biometric_surveillance_score: float
    social_scoring_score: float
    mass_metadata_collection_score: float
    civil_liberties_erosion_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_surveillance_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.biometric_surveillance_score * 0.30
            + self.social_scoring_score * 0.25
            + self.mass_metadata_collection_score * 0.25
            + self.civil_liberties_erosion_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_surveillance_index = round(self.composite_score / 100 * 10, 2)

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
        if self.biometric_surveillance_score >= 80 and self.social_scoring_score >= 75:
            return "totalitarisme_numerique"
        if self.civil_liberties_erosion_score >= 80:
            return "export_technologie_surveillance"
        if self.composite_score >= 40:
            return "surveillance_securitaire_excessive"
        if self.composite_score >= 20:
            return "derive_commerciale"
        return "cadre_protecteur"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Surveillance algorithmique de masse dans {n} — contrôle numérique total des populations",
                "Reconnaissance faciale omniprésente — chaque mouvement dans l'espace public tracé et analysé en temps réel",
                "Libertés civiles numériques érodées — dissidence, association et expression sous surveillance constante",
            ]
        if self.risk_level == "élevé":
            return [
                f"Surveillance avancée dans {n} — systèmes de collecte massive de données sans garanties suffisantes",
                "Programmes de surveillance sécuritaire dépassant les limites légales et les droits fondamentaux",
                "Risque de dérive autoritaire — technologies de surveillance sans supervision judiciaire indépendante",
            ]
        if self.risk_level == "modéré":
            return [
                f"Surveillance partielle dans {n} — collecte de données sans encadrement légal suffisant",
                "Plateformes commerciales collectant des biométriques sans consentement éclairé et supervision",
                "Risque de normalisation — technologies de surveillance tolérées sans débat démocratique",
            ]
        return [
            f"{n} maintient un cadre protecteur contre la surveillance algorithmique excessive",
            "Régulation stricte de la biométrie et droits numériques effectifs pour les citoyens",
            "Modèle de gouvernance algorithmique à partager — transparence, contrôle citoyen et supervision judiciaire",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "biometric_surveillance_score": self.biometric_surveillance_score,
            "social_scoring_score": self.social_scoring_score,
            "mass_metadata_collection_score": self.mass_metadata_collection_score,
            "civil_liberties_erosion_score": self.civil_liberties_erosion_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_surveillance_index": self.estimated_surveillance_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[AlgorithmicSurveillanceEntity] = [
    AlgorithmicSurveillanceEntity("AS-001", "Chine — État de Surveillance Totale", "Asie", "Crédit Social, Xinjiang & Export Technologie Surveillance Autoritaire", 98.0, 95.0, 90.0, 92.0),
    AlgorithmicSurveillanceEntity("AS-002", "Corée du Nord — Surveillance Analogique Totale", "Asie", "Contrôle Total Non-Numérique mais Intégration Technologie Chinoise", 80.0, 88.0, 72.0, 92.0),
    AlgorithmicSurveillanceEntity("AS-003", "Russie — SORM & Surveillance FSB", "Europe de l'Est", "SORM-3 Surveillance Totale Télécoms & Reconnaissance Faciale Moscou", 85.0, 78.0, 88.0, 82.0),
    AlgorithmicSurveillanceEntity("AS-004", "Iran — État de Surveillance Islamique", "MENA", "Surveillance Numérique des Opposants & Contrôle VPN & Réseaux Sociaux", 78.0, 80.0, 75.0, 85.0),
    AlgorithmicSurveillanceEntity("AS-005", "USA — PRISM & Surveillance Globale NSA", "Amérique du Nord", "XKeyscore, PRISM & Palantir — Surveillance Sécuritaire sans Garanties", 50.0, 38.0, 72.0, 52.0),
    AlgorithmicSurveillanceEntity("AS-006", "Inde — Aadhaar & NATGRID", "Asie du Sud", "Base Biométrique 1.4Mds Citoyens & Système de Surveillance NATGRID", 55.0, 42.0, 52.0, 48.0),
    AlgorithmicSurveillanceEntity("AS-007", "Europe — RGPD vs Surveillance Commerciale", "Europe", "RGPD Insuffisant face aux GAFAM & Surveillance Commerciale Légale", 35.0, 20.0, 55.0, 38.0),
    AlgorithmicSurveillanceEntity("AS-008", "Islande & Estonie — Démocraties Numériques", "Europe du Nord", "e-Résidence, Données Chiffrées & Cadre Légal Anti-Surveillance Exemplaire", 8.0, 5.0, 12.0, 6.0),
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
        "domain": "algorithmic_surveillance",
        "confidence_score": 0.84,
        "data_sources": ["carnegie_ai_global_surveillance_index", "citizen_lab_surveillance_tracker", "access_now_digital_rights_monitor"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_surveillance_index": round(avg / 100 * 10, 2),
    }


def analyze_algorithmic_surveillance() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Algorithmic Surveillance Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
