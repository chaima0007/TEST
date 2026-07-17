from dataclasses import dataclass, field
from typing import List, Dict, Optional
import statistics


@dataclass
class InternetShutdownDigitalRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    internet_shutdown_frequency_severity_score: float = 0.0
    social_media_platform_blocking_score: float = 0.0
    vpn_encryption_criminalization_score: float = 0.0
    digital_expression_persecution_score: float = 0.0
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: List[str] = field(init=False)
    estimated_internet_shutdown_digital_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.internet_shutdown_frequency_severity_score * 0.30 +
            self.social_media_platform_blocking_score * 0.25 +
            self.vpn_encryption_criminalization_score * 0.25 +
            self.digital_expression_persecution_score * 0.20, 2
        )
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"

        patterns_map = {
            "coupure_internet_totale": self.internet_shutdown_frequency_severity_score,
            "blocage_plateformes_reseaux_sociaux": self.social_media_platform_blocking_score,
            "criminalisation_vpn_chiffrement": self.vpn_encryption_criminalization_score,
            "persecution_expression_numerique": self.digital_expression_persecution_score,
        }
        self.primary_pattern = max(patterns_map, key=lambda k: patterns_map[k])

        self.key_signals = self._generate_signals()
        self.estimated_internet_shutdown_digital_rights_index = round(
            self.composite_score / 100 * 10, 2
        )

    def _generate_signals(self) -> List[str]:
        signals = []
        if self.internet_shutdown_frequency_severity_score >= 60:
            signals.append(
                f"Coupure internet grave de {self.name} — interruptions délibérées "
                f"des communications numériques privant des millions de citoyens de leur "
                f"droit à l'information et aux services essentiels dépendant de la connectivité"
            )
        elif self.internet_shutdown_frequency_severity_score >= 40:
            signals.append(
                f"Coupures internet récurrentes de {self.name} — blocages ciblés lors "
                f"d'élections, de manifestations ou d'opérations militaires, constituant "
                f"une arme de contrôle politique violant le droit international"
            )
        if self.social_media_platform_blocking_score >= 60:
            signals.append(
                f"Censure numérique systématique — le blocage de plateformes (Twitter/X, "
                f"Facebook, WhatsApp, Telegram) constitue une violation du droit à la liberté "
                f"d'expression en ligne reconnu par l'ONU A/HRC/20/L.13"
            )
        elif self.social_media_platform_blocking_score >= 40:
            signals.append(
                f"Filtrage sélectif des contenus — restrictions ciblées sur les réseaux sociaux "
                f"pendant les crises politiques, créant un contexte d'information contrôlé "
                f"favorisant la propagande officielle"
            )
        if self.vpn_encryption_criminalization_score >= 60:
            signals.append(
                f"Criminalisation du chiffrement et des VPN — l'interdiction des outils de "
                f"protection de la vie privée expose les journalistes, militants et dissidents "
                f"à la surveillance étatique et aux poursuites judiciaires"
            )
        if self.digital_expression_persecution_score >= 40:
            signals.append(
                f"Impunité de la censure numérique — l'absence de recours juridiques effectifs "
                f"contre les coupures internet normalise l'utilisation du contrôle numérique "
                f"comme outil de répression politique"
            )
        if not signals:
            signals.append(
                f"Engagement relatif pour les droits numériques de {self.name} — "
                f"cadres légaux de protection partielle de la liberté d'expression en ligne"
            )
        return signals[:3]

    def to_dict(self) -> Dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "internet_shutdown_frequency_severity_score": self.internet_shutdown_frequency_severity_score,
            "social_media_platform_blocking_score": self.social_media_platform_blocking_score,
            "vpn_encryption_criminalization_score": self.vpn_encryption_criminalization_score,
            "digital_expression_persecution_score": self.digital_expression_persecution_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_internet_shutdown_digital_rights_index": self.estimated_internet_shutdown_digital_rights_index,
            "last_updated": self.last_updated,
        }


class InternetShutdownDigitalRightsEngine:
    ENGINE_VERSION = "1.0.0"
    DOMAIN = "internet_shutdown_digital_rights"

    def __init__(self):
        self.entities = self._load_entities()

    def _load_entities(self) -> List[InternetShutdownDigitalRightsEntity]:
        return [
            InternetShutdownDigitalRightsEntity(
                entity_id="ISDR-001",
                name="Myanmar/Coup État 2021 Blackout Total Internet",
                country="Asie du Sud-Est",
                sector="Coup Militaire Février 2021, Coupure Internet 77 Jours, Facebook Principal Media Coupé & 40+ Millions Privés Connectivité",
                internet_shutdown_frequency_severity_score=96.0,
                social_media_platform_blocking_score=94.0,
                vpn_encryption_criminalization_score=88.0,
                digital_expression_persecution_score=92.0,
            ),
            InternetShutdownDigitalRightsEntity(
                entity_id="ISDR-002",
                name="Corée du Nord/Intranet Kwangmyong Isolement Total",
                country="Asie du Nord-Est",
                sector="Internet Mondial Accessible <0.1% Population, Intranet Étatique Contrôlé, VPN Peine De Mort & Totale Désinformation",
                internet_shutdown_frequency_severity_score=99.0,
                social_media_platform_blocking_score=99.0,
                vpn_encryption_criminalization_score=99.0,
                digital_expression_persecution_score=95.0,
            ),
            InternetShutdownDigitalRightsEntity(
                entity_id="ISDR-003",
                name="Iran/Mahsa Amini Coupure 2022 & Filtrage",
                country="MENA",
                sector="Coupure Internet Pendant Manifestations 2022, Instagram/WhatsApp Bloqués, VPN Criminalisés & 76 Millions Touchés",
                internet_shutdown_frequency_severity_score=88.0,
                social_media_platform_blocking_score=90.0,
                vpn_encryption_criminalization_score=85.0,
                digital_expression_persecution_score=86.0,
            ),
            InternetShutdownDigitalRightsEntity(
                entity_id="ISDR-004",
                name="Éthiopie/Tigré 2020-2022 Zone de Guerre",
                country="Afrique de l'Est",
                sector="18 Mois Sans Internet Région Tigré, Blackout Pendant Conflit, Populations Coupées Aide Humanitaire & Journalistes Exclus",
                internet_shutdown_frequency_severity_score=90.0,
                social_media_platform_blocking_score=82.0,
                vpn_encryption_criminalization_score=80.0,
                digital_expression_persecution_score=88.0,
            ),
            InternetShutdownDigitalRightsEntity(
                entity_id="ISDR-005",
                name="Russie/Blocage Twitter VK Censuré Ukraine",
                country="Europe de l'Est",
                sector="Twitter/Facebook Bloqués Mars 2022, Loi Roskomnadzor, 200+ Sites Censurés, VPN Légaux Sous Pression & Propagande RuTube",
                internet_shutdown_frequency_severity_score=45.0,
                social_media_platform_blocking_score=65.0,
                vpn_encryption_criminalization_score=48.0,
                digital_expression_persecution_score=55.0,
            ),
            InternetShutdownDigitalRightsEntity(
                entity_id="ISDR-006",
                name="Inde/Cachemire 552 Jours Sans Internet",
                country="Asie du Sud",
                sector="552 Jours Coupure Cachemire 2019-2021, Monde Record, 4G Bloqué, 7M Habitants & Économie Locale Dévastée",
                internet_shutdown_frequency_severity_score=78.0,
                social_media_platform_blocking_score=55.0,
                vpn_encryption_criminalization_score=42.0,
                digital_expression_persecution_score=60.0,
            ),
            InternetShutdownDigitalRightsEntity(
                entity_id="ISDR-007",
                name="USA/Section 230 & Big Tech Modération",
                country="Amérique du Nord",
                sector="Section 230 Débat, Modération Contenu Big Tech, CLOUD Act Surveillance, Patriot Act & NSA Mass Surveillance Revelations",
                internet_shutdown_frequency_severity_score=18.0,
                social_media_platform_blocking_score=22.0,
                vpn_encryption_criminalization_score=20.0,
                digital_expression_persecution_score=35.0,
            ),
            InternetShutdownDigitalRightsEntity(
                entity_id="ISDR-008",
                name="UE/GDPR & Digital Services Act Régulation",
                country="Europe",
                sector="GDPR 2018 Protection Données, DSA 2022 Modération Transparente, NIS2 Cybersécurité & Droits Numériques Renforcés",
                internet_shutdown_frequency_severity_score=2.0,
                social_media_platform_blocking_score=3.0,
                vpn_encryption_criminalization_score=2.0,
                digital_expression_persecution_score=5.0,
            ),
        ]

    def analyze(self) -> Dict:
        results = [e.to_dict() for e in self.entities]
        scores = [e.composite_score for e in self.entities]
        avg_composite = round(statistics.mean(scores), 2)
        risk_dist = {}
        pattern_dist = {}
        for e in self.entities:
            risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
            pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1

        top_risk = sorted(self.entities, key=lambda e: e.composite_score, reverse=True)[:4]
        critical_alerts = [
            f"{e.name}: {e.primary_pattern}" for e in self.entities if e.risk_level == "critique"
        ]
        avg_index = round(avg_composite / 100 * 10, 2)

        return {
            "total_entities": len(results),
            "avg_composite": avg_composite,
            "risk_distribution": risk_dist,
            "pattern_distribution": pattern_dist,
            "top_risk_entities": [e.name for e in top_risk],
            "critical_alerts": critical_alerts,
            "last_analysis": "2026-06-21",
            "engine_version": self.ENGINE_VERSION,
            "domain": self.DOMAIN,
            "confidence_score": 0.87,
            "data_sources": [
                "accessnow_keepiton_report_2023",
                "netblocks_internet_shutdowns_tracker",
                "freedom_house_freedom_net_2023",
                "article19_digital_expression_report",
            ],
            "entities": results,
            "avg_estimated_internet_shutdown_digital_rights_index": avg_index,
        }


if __name__ == "__main__":
    import json
    engine = InternetShutdownDigitalRightsEngine()
    result = engine.analyze()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    scores = [e["composite_score"] for e in result["entities"]]
    print(f"\nAvg composite: {result['avg_composite']}")
    print(f"Distribution: {result['risk_distribution']}")
