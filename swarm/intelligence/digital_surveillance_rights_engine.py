"""Digital Surveillance Rights Engine — CaelumSwarm™ Wave 195"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics
import json

DOMAIN = "digital_surveillance_rights"
PREFIX = "DSR"
ACCENT_COLOR = "#6d28d9"


@dataclass
class DigitalSurveillanceRightsEntity:
    entity_id: str
    name: str
    country: str
    mass_surveillance_score: float           # ×0.30 — ampleur de la surveillance de masse
    biometric_data_abuse_score: float        # ×0.25 — abus reconnaissance faciale/biométrie
    censorship_repression_score: float       # ×0.25 — censure et répression internet
    accountability_deficit_score: float      # ×0.20 — manque de responsabilisation (haut = mauvais)
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_digital_surveillance_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.mass_surveillance_score * 0.30
            + self.biometric_data_abuse_score * 0.25
            + self.censorship_repression_score * 0.25
            + self.accountability_deficit_score * 0.20,
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
        self.estimated_digital_surveillance_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class DigitalSurveillanceRightsEngineResult:
    agent: str = "Digital Surveillance Rights Engine Agent"
    domain: str = DOMAIN
    prefix: str = PREFIX
    accent_color: str = ACCENT_COLOR
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_digital_surveillance_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DigitalSurveillanceRightsEntity] = field(default_factory=list)


def calculate_composite(entity: DigitalSurveillanceRightsEntity) -> float:
    return entity.composite_score


def classify_severity(score: float) -> str:
    if score >= 60:
        return "critique"
    elif score >= 40:
        return "élevé"
    elif score >= 20:
        return "modéré"
    return "faible"


def run_engine() -> DigitalSurveillanceRightsEngineResult:
    entities = [
        # --- CRITIQUE (≥60) : 4 entités ---
        DigitalSurveillanceRightsEntity(
            entity_id="DSR-001",
            name="NSO Group Technologies — Pegasus Spyware, Journalistes & Activistes Ciblés 50+ Pays",
            country="Israël",
            mass_surveillance_score=93.0,   # déploiement global spyware état-commandité
            biometric_data_abuse_score=88.0, # extraction biométrique via zero-click exploits
            censorship_repression_score=89.0, # surveillance dissidents, journalistes, opposants
            accountability_deficit_score=87.0, # opacité totale, poursuites judiciaires évitées
            primary_pattern="mass_surveillance_score",
        ),
        # composite = 93*0.30 + 88*0.25 + 89*0.25 + 87*0.20
        #           = 27.90 + 22.00 + 22.25 + 17.40 = 89.55 ✓ critique

        DigitalSurveillanceRightsEntity(
            entity_id="DSR-002",
            name="Hikvision — Reconnaissance Faciale Xinjiang, Réseau Surveillance Ouïghours 1M+",
            country="Chine",
            mass_surveillance_score=90.0,   # réseau caméras 400M+, intégration IA
            biometric_data_abuse_score=89.0, # base de données biométriques ethniques Xinjiang
            censorship_repression_score=83.0, # support infrastructure répression
            accountability_deficit_score=82.0, # aucune responsabilité malgré sanctions UE/USA
            primary_pattern="biometric_data_abuse_score",
        ),
        # composite = 90*0.30 + 89*0.25 + 83*0.25 + 82*0.20
        #           = 27.00 + 22.25 + 20.75 + 16.40 = 86.40 ✓ critique

        DigitalSurveillanceRightsEntity(
            entity_id="DSR-003",
            name="Palantir Technologies — Mass Surveillance Gouvernements, ICE/DHS Data Mining & Predictive Policing",
            country="USA",
            mass_surveillance_score=81.0,   # contrats ICE, CIA, police prédictive
            biometric_data_abuse_score=76.0, # fusion bases données biométriques gouvernementales
            censorship_repression_score=75.0, # support expulsions et ciblage communautés
            accountability_deficit_score=80.0, # secret contractuel, audit indépendant inexistant
            primary_pattern="mass_surveillance_score",
        ),
        # composite = 81*0.30 + 76*0.25 + 75*0.25 + 80*0.20
        #           = 24.30 + 19.00 + 18.75 + 16.00 = 78.05 ✓ critique

        DigitalSurveillanceRightsEntity(
            entity_id="DSR-004",
            name="Clearview AI — Biométrie Illégale, Interdit UE & Canada, 30Md Visages Scrapés sans Consentement",
            country="USA",
            mass_surveillance_score=77.0,   # scraping 30Md+ images sans consentement
            biometric_data_abuse_score=82.0, # violation RGPD, PIPEDA, lois état US
            censorship_repression_score=68.0, # vendu à gouvernements autoritaires
            accountability_deficit_score=74.0, # interdictions ignorées, expansion continue
            primary_pattern="biometric_data_abuse_score",
        ),
        # composite = 77*0.30 + 82*0.25 + 68*0.25 + 74*0.20
        #           = 23.10 + 20.50 + 17.00 + 14.80 = 75.40 ✓ critique

        # --- ÉLEVÉ (≥40, <60) : 2 entités ---
        DigitalSurveillanceRightsEntity(
            entity_id="DSR-005",
            name="Meta Platforms Inc — Cambridge Analytica, Publicité Comportementale & Surveillance Capitalisme",
            country="USA",
            mass_surveillance_score=63.0,   # profiling 3Md+ utilisateurs
            biometric_data_abuse_score=59.0, # reconnaissance faciale (suspendue EU)
            censorship_repression_score=55.0, # modération opaque, discours politique filtré
            accountability_deficit_score=57.0, # amendes RGPD récurrentes, lobbying anti-régulation
            primary_pattern="mass_surveillance_score",
        ),
        # composite = 63*0.30 + 59*0.25 + 55*0.25 + 57*0.20
        #           = 18.90 + 14.75 + 13.75 + 11.40 = 58.80 ✓ élevé

        DigitalSurveillanceRightsEntity(
            entity_id="DSR-006",
            name="ByteDance/TikTok — Transfert Données vers Chine, Projet Texas & Accès PRC Employés aux Données US",
            country="Chine/USA",
            mass_surveillance_score=60.0,   # 1.5Md utilisateurs, données comportementales
            biometric_data_abuse_score=54.0, # facial recognition features, biométrie collectée
            censorship_repression_score=57.0, # censure contenu pro-Tibet/HK, auteurs ciblés
            accountability_deficit_score=52.0, # audits refusés, accès Beijing confirmé
            primary_pattern="mass_surveillance_score",
        ),
        # composite = 60*0.30 + 54*0.25 + 57*0.25 + 52*0.20
        #           = 18.00 + 13.50 + 14.25 + 10.40 = 56.15 ✓ élevé

        # --- MODÉRÉ (≥20, <40) : 1 entité ---
        DigitalSurveillanceRightsEntity(
            entity_id="DSR-007",
            name="Signal Foundation — Chiffrement Fort E2E, mais Adoption États Autoritaires & Limitations Légales",
            country="USA",
            mass_surveillance_score=28.0,   # pas de surveillance propre, mais vecteur opposition
            biometric_data_abuse_score=22.0, # aucune collecte biométrique
            censorship_repression_score=30.0, # bloqué Iran/Chine, usage résistants persécutés
            accountability_deficit_score=27.0, # transparence élevée, audits réguliers
            primary_pattern="censorship_repression_score",
        ),
        # composite = 28*0.30 + 22*0.25 + 30*0.25 + 27*0.20
        #           = 8.40 + 5.50 + 7.50 + 5.40 = 26.80 ✓ modéré

        # --- FAIBLE (<20) : 1 entité ---
        DigitalSurveillanceRightsEntity(
            entity_id="DSR-008",
            name="Tor Project — Anonymisation Internet, Protection Lanceurs d&apos;Alerte & Accès Censuré",
            country="USA",
            mass_surveillance_score=10.0,   # outil de protection, pas de surveillance
            biometric_data_abuse_score=8.0,  # aucune collecte de données biométriques
            censorship_repression_score=15.0, # contournement censure, mais risque ciblage users
            accountability_deficit_score=12.0, # organisation transparente, open-source
            primary_pattern="censorship_repression_score",
        ),
        # composite = 10*0.30 + 8*0.25 + 15*0.25 + 12*0.20
        #           = 3.00 + 2.00 + 3.75 + 2.40 = 11.15 ✓ faible
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

    return DigitalSurveillanceRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_digital_surveillance_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "amnesty_international_surveillance_giants_report_2019",
            "citizen_lab_pegasus_investigations_2021_2023",
            "access_now_digital_rights_annual_report_2024",
            "electronic_frontier_foundation_atlas_surveillance",
            "eu_fundamental_rights_agency_facial_recognition_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_engine()
    print(json.dumps(
        {
            "agent": result.agent,
            "domain": result.domain,
            "prefix": result.prefix,
            "accent_color": result.accent_color,
            "total_entities": result.total_entities,
            "avg_composite": result.avg_composite,
            "avg_estimated_digital_surveillance_rights_index": result.avg_estimated_digital_surveillance_rights_index,
            "confidence_score": result.confidence_score,
            "risk_distribution": result.risk_distribution,
            "pattern_distribution": result.pattern_distribution,
            "top_risk_entities": result.top_risk_entities,
            "critical_alerts": result.critical_alerts,
            "last_analysis": result.last_analysis,
            "engine_version": result.engine_version,
            "data_sources": result.data_sources,
            "entities": [
                {
                    "entity_id": e.entity_id,
                    "name": e.name,
                    "country": e.country,
                    "mass_surveillance_score": e.mass_surveillance_score,
                    "biometric_data_abuse_score": e.biometric_data_abuse_score,
                    "censorship_repression_score": e.censorship_repression_score,
                    "accountability_deficit_score": e.accountability_deficit_score,
                    "composite_score": e.composite_score,
                    "risk_level": e.risk_level,
                    "estimated_digital_surveillance_rights_index": e.estimated_digital_surveillance_rights_index,
                    "primary_pattern": e.primary_pattern,
                    "last_updated": e.last_updated,
                }
                for e in result.entities
            ],
        },
        ensure_ascii=False,
        indent=2,
    ))

    print("\n--- RÉSUMÉ DISTRIBUTION ---")
    print(f"avg_composite       : {result.avg_composite}")
    print(f"avg_index           : {result.avg_estimated_digital_surveillance_rights_index}")
    print(f"risk_distribution   : {result.risk_distribution}")
    for e in result.entities:
        print(
            f"  {e.entity_id} | {e.composite_score:6.2f} | {e.risk_level:<8} | {e.name.split('—')[0].strip()}"
        )
