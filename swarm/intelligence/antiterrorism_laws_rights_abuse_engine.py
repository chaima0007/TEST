"""
Caelum Partners — Antiterrorism Laws Rights Abuse Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Lois antiterroristes et abus des droits — lois CTL utilisées contre dissidents,
journalistes, minorités, opposants politiques.

Les législations antiterroristes, conçues initialement pour répondre à des menaces
sécuritaires réelles, ont été progressivement détournées par de nombreux États pour
réprimer l'opposition politique, criminaliser les journalistes et museler les
défenseurs des droits humains. Les lois de lutte contre le terrorisme (CTL) offrent
des définitions larges et floues du "terrorisme" permettant leur application arbitraire.

En Chine, le cadre antiterroriste au Xinjiang a permis la détention de plus d'un million
d'Ouïghours dans des "centres de rééducation". En Égypte, la loi de 2015 classe les
opposants politiques comme terroristes pour justifier plus de 60 000 emprisonnements.
En Turquie, l'étiquette PKK "terroriste" a conduit à 150 000 purges post-coup. La
surveillance de masse, les tribunaux secrets et la détention indéfinie sans charge sont
devenus des outils de gouvernance autoritaire normalisés sous couverture sécuritaire.

Risk levels (weaponisation CTL, surveillance, détention secrète, profilage) :
  critique  -> composite >= 60  (CTL = instrument répression systémique — opposants, minorités)
  élevé     -> composite >= 40  (abus documentés — surveillance masse, arrestations politiques)
  modéré    -> composite >= 20  (dérives contrôlées — excès encadrés, débat démocratique actif)
  faible    -> composite < 20   (cadre équilibré — contrôle parlementaire, droits garantis)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class AntiterrorismLawsRightsAbuseEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    counterterrorism_law_political_weaponization_score: float
    mass_surveillance_datamining_rights_score: float
    indefinite_detention_secret_courts_score: float
    minority_profiling_collective_punishment_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_antiterrorism_laws_rights_abuse_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.counterterrorism_law_political_weaponization_score * 0.30
            + self.mass_surveillance_datamining_rights_score * 0.25
            + self.indefinite_detention_secret_courts_score * 0.25
            + self.minority_profiling_collective_punishment_score * 0.20,
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
        self.estimated_antiterrorism_laws_rights_abuse_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "counterterrorism_law_political_weaponization_score": self.counterterrorism_law_political_weaponization_score,
            "mass_surveillance_datamining_rights_score": self.mass_surveillance_datamining_rights_score,
            "indefinite_detention_secret_courts_score": self.indefinite_detention_secret_courts_score,
            "minority_profiling_collective_punishment_score": self.minority_profiling_collective_punishment_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_antiterrorism_laws_rights_abuse_index": self.estimated_antiterrorism_laws_rights_abuse_index,
            "last_updated": self.last_updated,
        }


@dataclass
class AntiterrorismLawsRightsAbuseEngineResult:
    agent: str = "Antiterrorism Laws Rights Abuse Engine Agent"
    domain: str = "antiterrorism_laws_rights_abuse"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_antiterrorism_laws_rights_abuse_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[AntiterrorismLawsRightsAbuseEntity] = field(default_factory=list)


def run_antiterrorism_laws_rights_abuse_engine() -> AntiterrorismLawsRightsAbuseEngineResult:
    entities = [
        AntiterrorismLawsRightsAbuseEntity(
            entity_id="ATL-001",
            name="Chine — Xinjiang 'Antiterrorisme' = 1M+ Ouïghours Détenus, DNA Databases, Apps Obligatoires",
            country="Chine",
            sector="Répression Ethno-Religieuse sous CTL",
            counterterrorism_law_political_weaponization_score=98.0,
            mass_surveillance_datamining_rights_score=97.0,
            indefinite_detention_secret_courts_score=96.0,
            minority_profiling_collective_punishment_score=97.0,
            primary_pattern="minority_profiling_collective_punishment",
            key_signals=[
                "1M+ Ouïghours détenus dans camps rééducation",
                "Collecte ADN, biométrie, applis espionnage obligatoires",
                "Tribunaux secrets sans représentation légale",
                "Interdiction pratiques religieuses islamiques ordinaires",
            ],
        ),
        AntiterrorismLawsRightsAbuseEntity(
            entity_id="ATL-002",
            name="Égypte — Loi Terrorisme 2015 = Opposants Classés Terroristes, 60K+ Prisonniers Politiques",
            country="Égypte",
            sector="Répression Opposition Politique sous CTL",
            counterterrorism_law_political_weaponization_score=93.0,
            mass_surveillance_datamining_rights_score=88.0,
            indefinite_detention_secret_courts_score=91.0,
            minority_profiling_collective_punishment_score=89.0,
            primary_pattern="counterterrorism_law_political_weaponization",
            key_signals=[
                "60 000+ prisonniers politiques depuis 2013",
                "Tribunaux d'exception antiterroristes permanents",
                "Al-Sissi utilise CTL pour écraser Frères Musulmans et laïcs",
                "Détention préventive illimitée sans inculpation",
            ],
        ),
        AntiterrorismLawsRightsAbuseEntity(
            entity_id="ATL-003",
            name="Russie — Lois Extrémisme Contre Témoins Jéhovah, Opposition Navalny, Journalistes",
            country="Russie",
            sector="Criminalisation Dissidence sous CTL",
            counterterrorism_law_political_weaponization_score=88.0,
            mass_surveillance_datamining_rights_score=85.0,
            indefinite_detention_secret_courts_score=86.0,
            minority_profiling_collective_punishment_score=83.0,
            primary_pattern="counterterrorism_law_political_weaponization",
            key_signals=[
                "Témoins de Jéhovah classés organisation extrémiste",
                "Fonds Anti-Corruption Navalny désigné extrémiste",
                "Journalistes arrêtés pour discours anticonstitutionnel",
                "SORM surveillance de masse sans mandat judiciaire",
            ],
        ),
        AntiterrorismLawsRightsAbuseEntity(
            entity_id="ATL-004",
            name="Turquie — Label PKK Terroriste = 150K+ Purges, Membres HDP Kurdish Party Arrêtés",
            country="Turquie",
            sector="Criminalisation Politique Kurde sous CTL",
            counterterrorism_law_political_weaponization_score=83.0,
            mass_surveillance_datamining_rights_score=80.0,
            indefinite_detention_secret_courts_score=81.0,
            minority_profiling_collective_punishment_score=78.0,
            primary_pattern="counterterrorism_law_political_weaponization",
            key_signals=[
                "150 000+ purges post-coup 2016 sous décrets CTL",
                "Co-présidents HDP Selahattin Demirtas emprisonné 4 ans",
                "Définition PKK-terrorisme étendue aux journalistes kurdes",
                "Condamnation ECtHR ignorée par Ankara",
            ],
        ),
        AntiterrorismLawsRightsAbuseEntity(
            entity_id="ATL-005",
            name="USA — PATRIOT Act, NSA Mass Surveillance Snowden, COINTELPRO Legacy, Muslim Registry",
            country="USA",
            sector="Surveillance de Masse & Profilage Religieux",
            counterterrorism_law_political_weaponization_score=55.0,
            mass_surveillance_datamining_rights_score=62.0,
            indefinite_detention_secret_courts_score=53.0,
            minority_profiling_collective_punishment_score=58.0,
            primary_pattern="mass_surveillance_datamining_rights",
            key_signals=[
                "NSA PRISM collecte métadonnées citoyens américains",
                "FISA courts secrets sans contrôle public",
                "CVE program profilage communautés musulmanes",
                "Guantanamo : détention indéfinie sans jugement",
            ],
        ),
        AntiterrorismLawsRightsAbuseEntity(
            entity_id="ATL-006",
            name="France — État d'Urgence 2015 Normalisé, Perquisitions Préventives, Fichage Mosquées",
            country="France",
            sector="Normalisation Mesures d'Exception CTL",
            counterterrorism_law_political_weaponization_score=50.0,
            mass_surveillance_datamining_rights_score=53.0,
            indefinite_detention_secret_courts_score=48.0,
            minority_profiling_collective_punishment_score=55.0,
            primary_pattern="minority_profiling_collective_punishment",
            key_signals=[
                "État urgence 2015-2017 intégré dans droit commun",
                "4 000+ perquisitions administratives sans mandat juge",
                "Algorithme surveillance automatique réseaux sociaux",
                "Dissolution associations musulmanes par décret préfectoral",
            ],
        ),
        AntiterrorismLawsRightsAbuseEntity(
            entity_id="ATL-007",
            name="Inde — UAPA Unlawful Activities = Militants Droits Humains Emprisonnés, Bhima Koregaon",
            country="Inde",
            sector="Criminalisation Activisme sous CTL",
            counterterrorism_law_political_weaponization_score=35.0,
            mass_surveillance_datamining_rights_score=32.0,
            indefinite_detention_secret_courts_score=30.0,
            minority_profiling_collective_punishment_score=33.0,
            primary_pattern="counterterrorism_law_political_weaponization",
            key_signals=[
                "Affaire Bhima Koregaon : 16 activistes/académiciens arrêtés",
                "UAPA permet détention sans charge jusqu'à 6 mois",
                "Journalistes kashmiri sous UAPA pour reportages",
                "NRC registre national citoyenneté cible musulmans",
            ],
        ),
        AntiterrorismLawsRightsAbuseEntity(
            entity_id="ATL-008",
            name="Allemagne — BfV Surveillance Légale Encadrée, G10 Oversight, mais Interdiction Partis Légale",
            country="Allemagne",
            sector="Cadre CTL Équilibré avec Contrôle Démocratique",
            counterterrorism_law_political_weaponization_score=10.0,
            mass_surveillance_datamining_rights_score=13.0,
            indefinite_detention_secret_courts_score=9.0,
            minority_profiling_collective_punishment_score=12.0,
            primary_pattern="mass_surveillance_datamining_rights",
            key_signals=[
                "Commission G10 contrôle parlementaire surveillance BfV",
                "BVerfG contrôle constitutionnel lois antiterroristes",
                "Interdiction NPD refusée 2 fois — principe proportionnalité",
                "RGPD protège données personnelles contre surveillance abusive",
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
        f"{e.name.split('—')[0].strip()}: {e.primary_pattern}"
        for e in sorted_entities[:4]
    ]

    return AntiterrorismLawsRightsAbuseEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_antiterrorism_laws_rights_abuse_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "amnesty_international_counterterrorism_rights_2023",
            "human_rights_watch_antiterrorism_abuses_2023",
            "international_commission_jurists_emergency_powers_2023",
            "un_special_rapporteur_counterterrorism_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_antiterrorism_laws_rights_abuse_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_antiterrorism_laws_rights_abuse_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
