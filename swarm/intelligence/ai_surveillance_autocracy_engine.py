"""
Caelum Partners — AI Surveillance Autocracy Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
L'IA au service de l'autocratie : la surveillance de masse comme outil de contrôle.
L'intelligence artificielle a transformé la capacité des régimes autoritaires à
surveiller, contrôler et réprimer leurs citoyens à une échelle et une précision
sans précédent dans l'histoire. La reconnaissance faciale en temps réel, le
traitement du langage naturel pour monitorer les médias sociaux et le scoring
comportemental créent un appareil de surveillance totalitaire d'une efficacité
opérationnelle redoutable.

La Chine a déployé 600+ millions de caméras (1 caméra pour 2,3 habitants), un
système de crédit social multi-dimensionnel ciblant 1,4Md personnes, et exporte
sa technologie de surveillance à 80+ pays via Hikvision, Dahua, ZTE et Huawei.
La Russie exploite le système SORM permettant aux FSB un accès aux communications
sans mandat judiciaire, et a déployé le réseau Orwell de reconnaissance faciale
dans le métro de Moscou. La Corée du Nord maintient un intranet national (Kwangmyong)
isolé d'internet mondial avec une surveillance totale des échanges.

L'Iran a instauré un filtrage internet (Halal Internet) bloquant 50%+ des sites
web, et l'IRGC monitore les communications via des systèmes fournis par la Chine.
Les EAU ont utilisé NSO Pegasus pour cibler des opposants politiques dans 50+
pays. Cette exportation de la surveillance constitue une menace directe pour les
démocraties qui accueillent des dissidents de ces régimes.

Risk levels (surveillance IA et autoritarisme numérique) :
  critique  → composite ≥ 60  (surveillance totale — appareil de contrôle IA systémique et exportation active)
  élevé     → composite ≥ 40  (autoritarisme numérique — surveillance politique ciblée et censure structurelle)
  modéré    → composite ≥ 20  (dérive surveillance — expansion des capacités sans contre-pouvoirs adéquats)
  faible    → composite < 20  (protection libertés numériques — RGPD fort, supervision indépendante, limites légales)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "surveillance_totale_citoyens": {
        "severity_fr": "Critique",
        "action_fr": "Coalition technodémocratique — interdiction des exportations de surveillance vers les régimes autoritaires et sanctions ciblées sur les entreprises de surveillance exportatrices",
        "signal_fr": "social_credit_score > 85 AND biometric_mass_surveillance_score > 85 — surveillance totale citoyens avec scoring comportemental IA et biométrie de masse",
    },
    "isolation_numerique_etatique": {
        "severity_fr": "Critique",
        "action_fr": "Internet ouvert universel — financement de technologies de contournement (VPN, Tor, Starlink) et pression diplomatique contre les shutdown internet",
        "signal_fr": "internet_shutdown_censorship_score > 85 — isolation numérique étatique systémique: coupure internet, filtrage profond et réseau intranet national",
    },
    "exportation_surveillance_autocratique": {
        "severity_fr": "Critique",
        "action_fr": "Régulation exportation surveillance — Wassenaar Arrangement étendu aux technologies de surveillance IA et mécanismes de diligence raisonnable obligatoire",
        "signal_fr": "surveillance_export_score > 85 — exportation active de technologies de surveillance autocratique à des régimes répressifs partenaires",
    },
    "autoritarisme_numerique_emergent": {
        "severity_fr": "Élevé",
        "action_fr": "Conditionnalité technologique — aide au développement numérique liée au respect de normes de droits numériques et formation aux contre-pouvoirs technologiques",
        "signal_fr": "Autoritarisme numérique émergent — surveillance politique ciblée, censure et restrictions progressives des libertés numériques",
    },
    "protection_libertes_numeriques": {
        "severity_fr": "Faible",
        "action_fr": "Exporter le modèle RGPD — financement des régulateurs de protection des données et coopération multilatérale sur les normes de surveillance proportionnée",
        "signal_fr": "composite_score < 20 — protection exemplaire des libertés numériques — RGPD fort, supervision indépendante et limites légales strictes",
    },
}


@dataclass
class AISurveillanceAutocracyEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    social_credit_score: float
    biometric_mass_surveillance_score: float
    surveillance_export_score: float
    internet_shutdown_censorship_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_ai_surveillance_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.social_credit_score * 0.30
            + self.biometric_mass_surveillance_score * 0.25
            + self.surveillance_export_score * 0.25
            + self.internet_shutdown_censorship_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_ai_surveillance_index = round(self.composite_score / 100 * 10, 2)

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
        if self.social_credit_score >= 85 and self.biometric_mass_surveillance_score >= 85:
            return "surveillance_totale_citoyens"
        if self.internet_shutdown_censorship_score >= 85:
            return "isolation_numerique_etatique"
        if self.surveillance_export_score >= 85:
            return "exportation_surveillance_autocratique"
        if self.composite_score >= 20:
            return "autoritarisme_numerique_emergent"
        return "protection_libertes_numeriques"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Surveillance totale par {n} — appareil de contrôle IA systémique ciblant comportements, déplacements et communications de la population",
                "IA au service de la répression — reconnaissance faciale en temps réel, NLP surveillance réseaux sociaux et scoring prédictif de la dissidence",
                "Exportation du modèle autoritaire — transfert technologique de surveillance à des régimes partenaires pour consolider les autocraties mondiales",
            ]
        if self.risk_level == "élevé":
            return [
                f"Autoritarisme numérique de {n} — surveillance politique ciblée et censure structurelle sans surveillance totale généralisée",
                "Restriction progressive des libertés — censure des médias, fermeture des applications VPN et filtrage du contenu politique contestataire",
                "Répression numérique des opposants — ciblage des journalistes, militants et minorités via des outils de surveillance IA",
            ]
        if self.risk_level == "modéré":
            return [
                f"Dérive surveillance de {n} — expansion des capacités de surveillance sans contre-pouvoirs judiciaires ou législatifs adéquats",
                "Zone grise réglementaire — technologies de surveillance déployées sans cadre légal clair sur la proportionnalité et les droits",
                "Risque de glissement autoritaire — capacités techniques disponibles pour une répression si le contexte politique change",
            ]
        return [
            f"{n} incarne la protection des libertés numériques — RGPD strict, supervision indépendante et limites légales à la surveillance",
            "Contre-pouvoirs institutionnels — autorités de protection des données dotées de pouvoirs réels et indépendantes du pouvoir politique",
            "Modèle de surveillance proportionnée à diffuser — surveillance ciblée sur décision judiciaire, transparence et droits de recours effectifs",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "social_credit_score": self.social_credit_score,
            "biometric_mass_surveillance_score": self.biometric_mass_surveillance_score,
            "surveillance_export_score": self.surveillance_export_score,
            "internet_shutdown_censorship_score": self.internet_shutdown_censorship_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_ai_surveillance_index": self.estimated_ai_surveillance_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[AISurveillanceAutocracyEntity] = [
    AISurveillanceAutocracyEntity("AS-001", "Chine — Grand Firewall & Exportation Surveillance 80 Pays", "Asie", "600M Caméras, Crédit Social 1.4Md Personnes, Hikvision/Dahua Export & SenseTime Reconnaissance Faciale", 95.0, 92.0, 88.0, 90.0),
    AISurveillanceAutocracyEntity("AS-002", "Russie — SORM, RuNet & Surveillance Orwell Moscou", "Europe de l'Est", "SORM-3 Accès FSB Sans Mandat, Réseau Orwell Moscou Métro, RuNet Isolation 2019 & SIZO Numérique", 85.0, 82.0, 80.0, 88.0),
    AISurveillanceAutocracyEntity("AS-003", "Corée du Nord — Kwangmyong Intranet Total Isolation", "Asie", "Kwangmyong Intranet 28 Sites, Surveillance Totale Électronique, Koryolink 5M Abonnés Contrôlés", 92.0, 88.0, 55.0, 95.0),
    AISurveillanceAutocracyEntity("AS-004", "Iran — Halal Internet & Surveillance IRGC Politique", "MENA", "Filtrage 50%+ Sites Web, IRGC Cyber Army, Pegasus Iranien DARIS & Shutdown 2019/2022 Protestations", 80.0, 78.0, 72.0, 85.0),
    AISurveillanceAutocracyEntity("AS-005", "EAU & Arabie Saoudite — NSO Pegasus & Smart City Panoptique", "MENA", "Pegasus 50+ Pays Clients, NEOM Smart City Surveillance & Project Raven Ex-NSA Ciblage Opposants", 55.0, 58.0, 65.0, 48.0),
    AISurveillanceAutocracyEntity("AS-006", "Turquie & Azerbaïdjan — Surveillance Politique Ciblée", "MENA/Europe", "Turquie 400K+ Poursuites Réseaux Sociaux, AZ Pegasus Opposition & Coupures Internet Électorales", 48.0, 52.0, 58.0, 45.0),
    AISurveillanceAutocracyEntity("AS-007", "Inde — NATGRID & Surveillance Biométrique Aadhaar", "Asie du Sud", "Aadhaar 1.4Md Biométries, NATGRID 21 Bases Données & Shutdown Cachemire 552 Jours Record Mondial", 30.0, 32.0, 28.0, 38.0),
    AISurveillanceAutocracyEntity("AS-008", "Suède & Islande — Protection Données RGPD+ Modèle", "Europe du Nord", "RGPD Application Exemplaire, DPA Indépendants, Transparence Algorithmique & Internet Ouvert Garanti", 5.0, 4.0, 3.0, 2.0),
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
        "domain": "ai_surveillance_autocracy",
        "confidence_score": 0.83,
        "data_sources": ["freedom_house_freedom_net", "citizenlab_surveillance_tracker", "carnegie_ai_global_surveillance_index"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_ai_surveillance_index": round(avg / 100 * 10, 2),
    }


def analyze_ai_surveillance_autocracy() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"AI Surveillance Autocracy Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
