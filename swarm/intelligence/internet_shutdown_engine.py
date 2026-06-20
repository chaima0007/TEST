"""
Internet Shutdown Engine — Caelum Partners Intelligence Platform
Auteure: Chaima Mhadbi | Bruxelles
Moteur d'analyse des coupures internet comme outil de répression : blackouts, throttling et censure systémique
"""

from dataclasses import dataclass, field
from typing import List, Dict

PATTERNS: Dict[str, Dict[str, str]] = {
    "blackout_total_repression": {
        "severity_fr": "Blackout Internet Total Répressionnel",
        "action_fr": "Activer les mécanismes du Conseil des droits de l'homme ONU sur l'accès à internet et sanctionner les équipementiers complices",
        "signal_fr": "Blackout internet total à des fins de répression — coupure complète d'internet pendant des manifestations, élections ou opérations militaires pour empêcher la documentation des abus",
    },
    "censure_plateforme_systematique": {
        "severity_fr": "Censure Systématique des Plateformes",
        "action_fr": "Engager Cloudflare/ISOC pour contournement technique et saisir le Rapporteur ONU sur la liberté d'expression",
        "signal_fr": "Censure systématique des plateformes — blocage permanent de réseaux sociaux, médias indépendants et outils de communication chiffrée par un appareil technique étatique",
    },
    "surveillance_reseau_massive": {
        "severity_fr": "Surveillance Réseau Massive",
        "action_fr": "Activer les mécanismes des Nations Unies sur la vie privée numérique et soutenir les ONG développant des outils de contournement sécurisés",
        "signal_fr": "Surveillance réseau massive — interception systématique des communications numériques des citoyens avec arsenal d'espionnage étatique sans base légale ni supervision judiciaire",
    },
    "throttling_elections_coups": {
        "severity_fr": "Throttling Electoral & Coups d'État",
        "action_fr": "Mobiliser les observateurs internationaux munis d'outils de mesure de débit et alerter Access Now NetBlocks en temps réel",
        "signal_fr": "Throttling électoral et pendant coups d'État — ralentissement ciblé des réseaux pendant les élections ou troubles politiques pour limiter l'information sans coupure totale détectable",
    },
    "liberte_numerique_exemplaire": {
        "severity_fr": "Liberté Numérique Exemplaire",
        "action_fr": "Partager les cadres légaux protégeant la neutralité du net et financer les outils de contournement pour les pays sous censure",
        "signal_fr": "Liberté numérique exemplaire — internet ouvert et non censuré, absence de blackouts, protection légale du chiffrement et accès universel sans discrimination",
    },
}


@dataclass
class InternetShutdownActor:
    entity_id: str
    name: str
    country: str
    sector: str
    shutdown_frequency_severity_score: float
    platform_censorship_scale_score: float
    network_surveillance_score: float
    digital_repression_impunity_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.shutdown_frequency_severity_score * 0.30
            + self.platform_censorship_scale_score * 0.25
            + self.network_surveillance_score * 0.25
            + self.digital_repression_impunity_score * 0.20,
            2,
        )

    @property
    def risk_level(self) -> str:
        s = self.composite_score
        if s >= 60:
            return "critique"
        if s >= 40:
            return "élevé"
        if s >= 20:
            return "modéré"
        return "faible"

    @property
    def primary_pattern(self) -> str:
        scores = {
            "blackout_total_repression": self.shutdown_frequency_severity_score,
            "censure_plateforme_systematique": self.platform_censorship_scale_score,
            "surveillance_reseau_massive": self.network_surveillance_score,
            "throttling_elections_coups": self.digital_repression_impunity_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        p = PATTERNS.get(self.primary_pattern, PATTERNS["blackout_total_repression"])
        base = p["signal_fr"]
        return [
            f"{base} de {self.name.split('/')[0] if '/' in self.name else self.name}",
            "Droit à l'information violé — les coupures internet privent les citoyens de l'accès aux informations vitales et empêchent la documentation des violations des droits humains",
            p["action_fr"],
        ]

    @property
    def estimated_internet_shutdown_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "shutdown_frequency_severity_score": self.shutdown_frequency_severity_score,
            "platform_censorship_scale_score": self.platform_censorship_scale_score,
            "network_surveillance_score": self.network_surveillance_score,
            "digital_repression_impunity_score": self.digital_repression_impunity_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_internet_shutdown_index": self.estimated_internet_shutdown_index,
            "last_updated": "2026-06-20",
        }


ACTORS: List[InternetShutdownActor] = [
    InternetShutdownActor("IS-001", "Chine/GFW — Grand Firewall, WeChat Surveillance & VPN Illégaux", "Asie",
        "Grand Firewall 3000+ Sites Bloqués, VPN Illégaux Prison, WeChat Surveillance IA & Système Crédit Social Connecté",
        88.0, 95.0, 95.0, 85.0),
    InternetShutdownActor("IS-002", "Iran — Mahsa Amini Blackout 2022 & Filternet Permanent", "MENA",
        "Blackout 2022 Mahsa Amini Manifestations, Filternet 50% Internet Bloqué, Instagram/WhatsApp Fermés & IRGC Surveillance",
        92.0, 88.0, 85.0, 82.0),
    InternetShutdownActor("IS-003", "Myanmar — Coup 2021 Blackout Total & Réseaux Tatmadaw", "Asie du Sud-Est",
        "Coup 2021 Blackout 4 Jours Total, 18 Mois Restrictions Partielles, Zayar Thaw Emprisonné & Facebook Seul Réseau Autorisé",
        90.0, 82.0, 80.0, 88.0),
    InternetShutdownActor("IS-004", "Russie/Roskomnadzor — Ukraine Censure & Réseaux VPN Bloqués", "Europe de l'Est",
        "Facebook/Instagram Bloqués 2022, 100 000 Sites Blacklistés, Runet Isolement Projet & Journalistes VPN Criminalisés",
        82.0, 85.0, 82.0, 80.0),
    InternetShutdownActor("IS-005", "Inde/Kashmir — 552 Jours Blackout Record Mondial", "Asie du Sud",
        "552 Jours Coupure Kashmir 2019-21 Record Mondial, 4G Rétabli Partiellement, Section 144 Mobile & Économie -4B$",
        55.0, 50.0, 48.0, 58.0),
    InternetShutdownActor("IS-006", "Éthiopie/Tigré — Coupures Conflit & Blackout Tigré 2020-22", "Afrique de l'Est",
        "Tigré Région Coupée 2 Ans Conflit, Télécom Éthiopie Monopole État, Journalistes Arrêtés Connexion & Coupures Amhara 2023",
        60.0, 52.0, 48.0, 58.0),
    InternetShutdownActor("IS-007", "Cuba/Nicaragua — Internet Limité & Réseaux Sociaux Coupés Crises", "Amérique Centrale",
        "Cuba Juillet 2021 Manifestations Coupure, Nicaragua 2018 Blackout, Twitter/Facebook Bloqués Ponctuellement & VPN Populaires",
        35.0, 32.0, 28.0, 35.0),
    InternetShutdownActor("IS-008", "Access Now/ISOC — Défense Liberté Internet & Outils Contournement", "Global",
        "Access Now NetBlocks Monitoring Temps Réel, ISOC Standards Ouverts, Résolution ONU Internet Droit Humain 2016 & Tor/VPN",
        5.0, 4.0, 3.0, 6.0),
]


def analyze_internet_shutdown() -> dict:
    entities = [a.to_dict() for a in ACTORS]
    avg = round(sum(e["composite_score"] for e in entities) / len(entities), 2)
    risk_dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    pattern_dist: Dict[str, int] = {}
    for e in entities:
        risk_dist[e["risk_level"]] = risk_dist.get(e["risk_level"], 0) + 1
        pattern_dist[e["primary_pattern"]] = pattern_dist.get(e["primary_pattern"], 0) + 1

    top_risk = sorted(entities, key=lambda x: x["composite_score"], reverse=True)[:3]
    critiques = [e for e in entities if e["risk_level"] == "critique"]

    return {
        "total_entities": len(entities),
        "avg_composite": avg,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": [e["name"] for e in top_risk],
        "critical_alerts": [f"{e['name'].split('—')[0].strip()}: {PATTERNS.get(e['primary_pattern'], {}).get('severity_fr', e['primary_pattern'])}" for e in critiques],
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "internet_shutdown",
        "confidence_score": 0.86,
        "data_sources": [
            "access_now_keep_it_on_database",
            "freedom_house_freedom_net_report",
            "netblocks_internet_outage_detector",
        ],
        "entities": entities,
        "avg_estimated_internet_shutdown_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    result = analyze_internet_shutdown()
    print(f"Internet Shutdown Engine — {result['total_entities']} acteurs, avg risque: {result['avg_composite']}")
    for e in result["entities"]:
        print(f"  [{e['risk_level'].upper()}] {e['name'][:60]} — score {e['composite_score']}")
    print(f"Distribution: {result['risk_distribution']}")
