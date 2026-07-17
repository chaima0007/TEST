"""
Caelum Partners — Internet Freedom & Digital Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Liberté internet et droits numériques : censure, surveillance de masse, coupures, lois répressives.

La liberté d'internet est devenue une condition fondamentale de l'exercice des droits
civils et politiques au XXIe siècle. L'accès à un internet ouvert, non censuré et sécurisé
est reconnu par les Nations Unies comme un droit humain (Résolution HRC 20/8, 2012).
Pourtant, selon Freedom House, plus de 70 % des utilisateurs d'internet dans le monde
vivent dans des pays où l'accès est limité, surveillé ou contrôlé.

La Chine maintient le "Grand Firewall", le système de censure internet le plus sophistiqué
au monde, bloquant Google, Facebook, WhatsApp et des milliers de sites. La Corée du Nord
a remplacé internet par un intranet national (Kwangmyong) inaccessible depuis l'étranger.
L'Iran, la Russie et de nombreux régimes autoritaires ont intensifié le blocage d'applications
et les coupures internet lors de mouvements de contestation populaire.

Les lois de cybersécurité répressives — instrumentalisées pour criminaliser journalistes,
activistes et dissidents — constituent un mécanisme de contrôle numérique en expansion
rapide, souvent sous couvert de lutte contre la "désinformation" ou le "terrorisme".

Risk levels (censure, surveillance masse, shutdowns, lois cybersécurité répressives) :
  critique  -> composite >= 60  (censure systémique — internet contrôlé, dissidents criminalisés)
  élevé     -> composite >= 40  (restrictions actives — shutdowns, surveillance, lois répressives)
  modéré    -> composite >= 20  (surveillance légale encadrée — libertés partiellement limitées)
  faible    -> composite < 20   (internet libre — protections légales solides, vie privée respectée)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class InternetFreedomDigitalRightsEntity:
    entity_id: str
    name: str
    country: str
    regime_type: str
    sub1_censorship_level: float
    sub2_surveillance_mass: float
    sub3_shutdown_frequency: float
    sub4_legal_framework_repression: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_internet_freedom_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.sub1_censorship_level * 0.30
            + self.sub2_surveillance_mass * 0.25
            + self.sub3_shutdown_frequency * 0.25
            + self.sub4_legal_framework_repression * 0.20,
            2,
        )
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_internet_freedom_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "regime_type": self.regime_type,
            "composite_score": self.composite_score,
            "sub1_censorship_level": self.sub1_censorship_level,
            "sub2_surveillance_mass": self.sub2_surveillance_mass,
            "sub3_shutdown_frequency": self.sub3_shutdown_frequency,
            "sub4_legal_framework_repression": self.sub4_legal_framework_repression,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_internet_freedom_index": self.estimated_internet_freedom_index,
            "last_updated": self.last_updated,
        }


@dataclass
class InternetFreedomDigitalRightsEngineResult:
    agent: str = "Internet Freedom & Digital Rights Engine Agent"
    domain: str = "internet_freedom_digital_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.88
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_internet_freedom_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[InternetFreedomDigitalRightsEntity] = field(default_factory=list)


def run_internet_freedom_digital_rights_engine() -> InternetFreedomDigitalRightsEngineResult:
    entities = [
        InternetFreedomDigitalRightsEntity(
            entity_id="IFD-001",
            name="Chine (Great Firewall niveau maximal — 1,4 Mrd d'utilisateurs sous censure systémique)",
            country="Chine",
            regime_type="Autoritarisme numérique",
            sub1_censorship_level=99.0,
            sub2_surveillance_mass=97.0,
            sub3_shutdown_frequency=93.0,
            sub4_legal_framework_repression=93.0,
            primary_pattern="sub1_censorship_level",
            key_signals=[
                "Grand Firewall bloque Google, Facebook, WhatsApp, YouTube",
                "Système crédit social couplé à surveillance numérique",
                "VPN illégaux — utilisateurs poursuivis pénalement",
                "Xinjiang : surveillance biométrique totale",
            ],
        ),
        InternetFreedomDigitalRightsEntity(
            entity_id="IFD-002",
            name="Corée du Nord (internet = intranet Kwangmyong — isolement numérique total)",
            country="Corée du Nord",
            regime_type="Totalitarisme numérique",
            sub1_censorship_level=100.0,
            sub2_surveillance_mass=98.0,
            sub3_shutdown_frequency=99.0,
            sub4_legal_framework_repression=95.0,
            primary_pattern="sub1_censorship_level",
            key_signals=[
                "Intranet national Kwangmyong — 0 accès internet mondial",
                "Accès internet réservé à élite politique et militaire",
                "Peine de mort possible pour accès médias étrangers",
                "Aucune plateforme internationale accessible",
            ],
        ),
        InternetFreedomDigitalRightsEntity(
            entity_id="IFD-003",
            name="Iran (filtrage + shutdown Mahsa Amini 2022 — 79 M d'utilisateurs impactés)",
            country="Iran",
            regime_type="Théocratie autoritaire numérique",
            sub1_censorship_level=86.0,
            sub2_surveillance_mass=83.0,
            sub3_shutdown_frequency=82.0,
            sub4_legal_framework_repression=81.0,
            primary_pattern="sub1_censorship_level",
            key_signals=[
                "Instagram et WhatsApp bloqués depuis 2022",
                "Shutdown total pendant protests Mahsa Amini",
                "FATA (cyberpolice) criminalise contenu en ligne",
                "VPN utilisé par 40% population malgré interdiction",
            ],
        ),
        InternetFreedomDigitalRightsEntity(
            entity_id="IFD-004",
            name="Russie (Runet + blocages 2022-2024 — internet souverain post-Ukraine)",
            country="Russie",
            regime_type="Autoritarisme numérique hybride",
            sub1_censorship_level=79.0,
            sub2_surveillance_mass=76.0,
            sub3_shutdown_frequency=73.0,
            sub4_legal_framework_repression=77.0,
            primary_pattern="sub4_legal_framework_repression",
            key_signals=[
                "Instagram, Facebook, Twitter bloqués depuis mars 2022",
                "Loi Runet 2019 : internet souverain déconnectable",
                "Roskomnadzor — +300 000 sites bloqués",
                "Loi 'fake news militaires' : 15 ans de prison",
            ],
        ),
        InternetFreedomDigitalRightsEntity(
            entity_id="IFD-005",
            name="Myanmar (shutdowns militaires post-coup 2021 — 53 M d'utilisateurs affectés)",
            country="Myanmar",
            regime_type="Junte militaire",
            sub1_censorship_level=62.0,
            sub2_surveillance_mass=58.0,
            sub3_shutdown_frequency=60.0,
            sub4_legal_framework_repression=56.0,
            primary_pattern="sub3_shutdown_frequency",
            key_signals=[
                "Shutdown total 77+ jours après coup d'état 2021",
                "Loi cybersécurité 2021 crimininalise 'déstabilisation'",
                "Broadband coupé dans zones résistance armée",
                "Journalistes arrêtés pour publications Facebook",
            ],
        ),
        InternetFreedomDigitalRightsEntity(
            entity_id="IFD-006",
            name="Inde (shutdowns Cachemire — 550+ coupures depuis 2012, record mondial)",
            country="Inde",
            regime_type="Démocratie à restrictions croissantes",
            sub1_censorship_level=49.0,
            sub2_surveillance_mass=47.0,
            sub3_shutdown_frequency=50.0,
            sub4_legal_framework_repression=43.0,
            primary_pattern="sub3_shutdown_frequency",
            key_signals=[
                "Record mondial shutdowns : 550+ depuis 2012",
                "Cachemire : shutdown 552 jours consécutifs 2019-2020",
                "IT Act Section 66A instrumentalisé contre activistes",
                "Projet NATGRID : surveillance centralisée citoyens",
            ],
        ),
        InternetFreedomDigitalRightsEntity(
            entity_id="IFD-007",
            name="France (surveillance LPMPM — encadrement légal mais capacités étendues)",
            country="France",
            regime_type="Démocratie libérale",
            sub1_censorship_level=26.0,
            sub2_surveillance_mass=27.0,
            sub3_shutdown_frequency=20.0,
            sub4_legal_framework_repression=28.0,
            primary_pattern="sub2_surveillance_mass",
            key_signals=[
                "LPMPM 2013-2023 : surveillance électronique étendue",
                "Loi sécurité globale 2021 : filtrages DNS préventifs",
                "CNIL contrôle insuffisant selon La Quadrature du Net",
                "Renseignement : collecte metadata sans mandat judiciaire",
            ],
        ),
        InternetFreedomDigitalRightsEntity(
            entity_id="IFD-008",
            name="Islande (liberté numérique totale — havres de données et protection journalistes)",
            country="Islande",
            regime_type="Démocratie numérique ouverte",
            sub1_censorship_level=7.0,
            sub2_surveillance_mass=8.0,
            sub3_shutdown_frequency=5.0,
            sub4_legal_framework_repression=12.0,
            primary_pattern="sub4_legal_framework_repression",
            key_signals=[
                "Freedom House: 'internet libre' score maximal",
                "IMMI : lois protection journalistes et lanceurs d'alerte",
                "0 blocage de contenu — neutralité nette constitutionnelle",
                "Datacenter WikiLeaks hébergé légalement",
            ],
        ),
    ]

    composites = [e.composite_score for e in entities]
    avg_composite = round(statistics.mean(composites), 2)

    risk_dist: dict = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1

    pattern_dist: dict = {}
    for e in entities:
        pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1

    sorted_entities = sorted(entities, key=lambda x: x.composite_score, reverse=True)
    top_risk = [e.name for e in sorted_entities[:3]]
    alerts = [
        f"{e.name.split('(')[0].strip()}: {e.primary_pattern}"
        for e in sorted_entities[:4]
    ]

    return InternetFreedomDigitalRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_internet_freedom_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "freedom_house_freedom_on_the_net_annual_report_2024",
            "citizen_lab_internet_censorship_country_reports",
            "article_19_digital_rights_global_expression_2024",
            "netblocks_internet_shutdown_observatory_data",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_internet_freedom_digital_rights_engine()
    print(f"=== Internet Freedom & Digital Rights Engine — Wave 161 ===")
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_internet_freedom_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    print()
    for e in result.entities:
        print(f"  {e.entity_id}: composite={e.composite_score} [{e.risk_level}] | index={e.estimated_internet_freedom_index}")
    print()
    assert result.risk_distribution.get("critique", 0) == 4, f"ERREUR: critique={result.risk_distribution.get('critique',0)} (attendu 4)"
    assert result.risk_distribution.get("élevé", 0) == 2, f"ERREUR: élevé={result.risk_distribution.get('élevé',0)} (attendu 2)"
    assert result.risk_distribution.get("modéré", 0) == 1, f"ERREUR: modéré={result.risk_distribution.get('modéré',0)} (attendu 1)"
    assert result.risk_distribution.get("faible", 0) == 1, f"ERREUR: faible={result.risk_distribution.get('faible',0)} (attendu 1)"
    print("✓ Distribution validée : 4 critique / 2 élevé / 1 modéré / 1 faible")
