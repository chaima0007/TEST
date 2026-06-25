"""Digital Rights Engine — Wave 38"""

from dataclasses import dataclass
from typing import List


@dataclass
class DigitalRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    internet_censorship_shutdown_score: float
    surveillance_privacy_violation_score: float
    digital_expression_suppression_score: float
    algorithmic_discrimination_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.internet_censorship_shutdown_score * 0.30
            + self.surveillance_privacy_violation_score * 0.25
            + self.digital_expression_suppression_score * 0.25
            + self.algorithmic_discrimination_score * 0.20,
            2,
        )

    @property
    def risk_level(self) -> str:
        s = self.composite_score
        if s >= 60: return "critique"
        if s >= 40: return "élevé"
        if s >= 20: return "modéré"
        return "faible"

    @property
    def primary_pattern(self) -> str:
        scores = {
            "censure_coupure_internet": self.internet_censorship_shutdown_score,
            "surveillance_violation_vie_privee": self.surveillance_privacy_violation_score,
            "suppression_expression_numerique": self.digital_expression_suppression_score,
            "discrimination_algorithmique": self.algorithmic_discrimination_score,
        }
        return max(scores, key=scores.get)

    @property
    def estimated_digital_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "internet_censorship_shutdown_score": self.internet_censorship_shutdown_score,
            "surveillance_privacy_violation_score": self.surveillance_privacy_violation_score,
            "digital_expression_suppression_score": self.digital_expression_suppression_score,
            "algorithmic_discrimination_score": self.algorithmic_discrimination_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_digital_rights_index": self.estimated_digital_rights_index,
            "last_updated": "2026-06-20",
        }

    @property
    def key_signals(self) -> List[str]:
        return [
            f"Violation des droits numériques documentée — {self.name} avec score composite {self.composite_score}/100 révélant des restrictions systémiques violant l'Article 19 du PIDCP sur la liberté d'expression en ligne et la Résolution ONU A/HRC/32/L.20 sur la promotion des droits humains sur Internet",
            f"Censure/Coupure Internet ({self.internet_censorship_shutdown_score}/100) — le blocage ou la coupure délibérée d'Internet constituent des violations directes de l'Article 19 PIDCP et des standards ONU sur la liberté d'expression en ligne (Résolution CDH 2016)",
            "Activer le Rapporteur Spécial ONU sur la liberté d'expression pour enquête sur les coupures Internet et exiger l'application de la Résolution CDH 32/13 reconnaissant que les droits hors ligne doivent être protégés en ligne",
        ]


ENTITIES = [
    DigitalRightsEntity("DR-001", "Chine/Grand Firewall — 1.4Md Censurés, Surveillance IA Totale & WeChat Monitoring", "Asie du Nord-Est", "Grand Firewall Chine 1.4Md Personnes, 300 000+ Sites Bloqués, WeChat Surveillance Messages, Système Crédit Social & IA Reconnaissance Faciale 1Md Visages Base Données Sécurité", 95, 95, 92, 88),
    DigitalRightsEntity("DR-002", "Corée du Nord — Internet 0.1% Population, Kwangmyong Intranet & Peines Mort Contenu", "Asie du Nord-Est", "RPDC 0.1% Population Internet Mondial, Kwangmyong Intranet Contrôlé État, Clé USB Contenu Étranger Peine Mort, Téléphones Inspectés & Complète Isolation Numérique Population", 95, 90, 95, 82),
    DigitalRightsEntity("DR-003", "Iran — 50%+ Contenu Bloqué, Pegasus Activistes & Coupe Internet Manifestations 2022", "MENA", "Iran 50%+ Internet Bloqué Instagram/WhatsApp, Pegasus Spyware Journalistes/Activistes, Coupure Internet Totale Manifestations Mahsa 2022 & Cyber Police FATA Arrestations Contenus", 88, 92, 88, 82),
    DigitalRightsEntity("DR-004", "Russie — RuNet Loi 2019, VPN Bloqués, Telegram Censure & Surveillance SORM-3", "Europe de l'Est", "Russie RuNet Souverain Loi 2019, SORM-3 Surveillance Totale Communications, VPN Massifs Bloqués 2022, Telegram Banni Débloqué & 100+ Domaines Médias Bloqués Post-Guerre", 85, 90, 88, 80),
    DigitalRightsEntity("DR-005", "USA/Big Tech — NSA PRISM, Section 702 FISA & Facial Recognition Minorités Ciblées", "Amérique du Nord", "USA NSA PRISM Surveillance 1Md+ Personnes Snowden 2013, Section 702 FISA Renouvellement 2024, Reconnaissance Faciale Faux Positifs Noirs 35×, TikTok Ban & Cloud Act Données", 50, 58, 48, 62),
    DigitalRightsEntity("DR-006", "Inde — Internet Shutdowns Record 84/An, Cachemire Coupure 552 Jours & Pegasus Opposants", "Asie du Sud", "Inde 84 Coupures Internet 2023 Record Mondial SFC, Cachemire 552 Jours Coupure Totale 2019-21, Pegasus Spyware Journalistes/Opposants & IT Act Section 66A Inconstitutionnelle", 58, 52, 55, 50),
    DigitalRightsEntity("DR-007", "UE/RGPD — Cambridge Analytica, DSA Lacunes & Algorithmes Plateformes Non-Régulés", "Europe", "UE RGPD 2018 Progrès Mais Cambridge Analytica 87M Profils, Meta 1.2Md Amende RGPD 2023, DSA Digital Services Act Lacunes Application & Algorithmes Recommandation Non-Transparents", 28, 32, 30, 35),
    DigitalRightsEntity("DR-008", "CDH-ONU/EFF — Résolution 32/13 Droits Internet & Principes Nécessité-Proportionnalité", "Global", "Résolution CDH-ONU 32/13 Droits Hors Ligne En Ligne, Rapporteur Spécial ONU Expression Art 19, Electronic Frontier Foundation, AccessNow & Principes Nécessité-Proportionnalité Surveillance", 5, 4, 3, 6),
]


def summary() -> dict:
    entities_data = [e.to_dict() for e in ENTITIES]
    avg = round(sum(e.composite_score for e in ENTITIES) / len(ENTITIES), 2)
    risk_dist = {}
    pattern_dist = {}
    for e in ENTITIES:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
        pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1
    top = sorted(ENTITIES, key=lambda x: x.composite_score, reverse=True)[:3]
    critical = [e for e in ENTITIES if e.risk_level == "critique"]
    return {
        "total_entities": len(ENTITIES),
        "avg_composite": avg,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": [e.name for e in top],
        "critical_alerts": [f"{e.name.split('—')[0].strip()}: {e.primary_pattern.replace('_', ' ')}" for e in critical],
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "digital_rights",
        "confidence_score": 0.85,
        "data_sources": [
            "freedom_house_freedom_on_the_net_annual_report",
            "accessnow_keepiton_internet_shutdown_tracker",
            "citizen_lab_targeted_threats_surveillance_research",
        ],
        "entities": entities_data,
        "avg_estimated_digital_rights_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Entities: {s['total_entities']}, Avg: {s['avg_composite']}, Dist: {s['risk_distribution']}")
    for e in ENTITIES:
        print(f"  {e.entity_id} {e.risk_level:8} {e.composite_score:6.2f} {e.name[:60]}")
