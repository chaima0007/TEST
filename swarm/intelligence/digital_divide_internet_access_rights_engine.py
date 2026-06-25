#!/usr/bin/env python3
"""
Wave 148 — Digital Divide & Internet Access Rights Intelligence Engine
Caelum Partners Swarm Intelligence Platform

Assesses connectivity gaps, state censorship, affordability exclusion,
and digital literacy rights deficits globally.
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
"""

from dataclasses import dataclass, field
import json
import statistics


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # Connectivity gap & infrastructure exclusion (0–10)
    sub2: float  # State censorship & digital shutdown severity (0–10)
    sub3: float  # Affordability exclusion & cost barrier (0–10)
    sub4: float  # Digital literacy rights deficit (0–10)
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_index: float = field(init=False)

    def __post_init__(self):
        self.composite_score = round(
            (self.sub1 * 0.30 + self.sub2 * 0.25 + self.sub3 * 0.25 + self.sub4 * 0.20) * 10, 2
        )
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_index = round(self.composite_score / 100 * 10, 2)


def run_engine() -> dict:
    entities = [
        # 4 critique
        EntityScore(
            entity_id="DD-001",
            name="Corée du Nord — Intranet-Only Population",
            sub1=9.5,  # near-total internet blackout; global intranet (Kwangmyong) only
            sub2=9.8,  # most extreme digital censorship globally; death penalty for foreign content
            sub3=9.3,  # internet access unavailable to 99%+ of population
            sub4=8.8,  # digital literacy rights systematically denied
        ),
        EntityScore(
            entity_id="DD-002",
            name="Érythrée — Blackout Numérique Structurel",
            sub1=9.0,  # among the world's lowest internet penetration (~1%)
            sub2=9.2,  # government monopoly; foreign sites systematically blocked
            sub3=9.1,  # cost prohibitive; average monthly wage < $50
            sub4=8.5,  # digital education nearly nonexistent
        ),
        EntityScore(
            entity_id="DD-003",
            name="Turkménistan — Contrôle Internet Totalitaire",
            sub1=8.2,  # state-controlled ISP; VPN illegal
            sub2=9.5,  # OONI data shows extreme filtering; ranked worst globally by Freedom House
            sub3=8.0,  # government employees monitored; chilling effect suppresses usage
            sub4=7.8,  # digital rights education absent from national curriculum
        ),
        EntityScore(
            entity_id="DD-004",
            name="Myanmar — Shutdowns Post-Coup & Rural Exclusion",
            sub1=8.0,  # junta-ordered shutdowns in Chin, Sagaing, Kayah since 2021
            sub2=8.8,  # mobile internet cut repeatedly; 12,000+ hours of shutdown 2021–24
            sub3=7.5,  # post-coup economic collapse; data prices unaffordable for majority
            sub4=7.2,  # digital literacy programs suspended; journalists arrested
        ),
        # 2 élevé
        EntityScore(
            entity_id="DD-005",
            name="RDC Rurale — Fracture Numérique Structurelle",
            sub1=6.2,  # rural connectivity <5%; 80M+ people offline
            sub2=4.0,  # some shutdowns during elections; not systematic
            sub3=6.5,  # data costs exceed 10% of monthly income in rural areas
            sub4=5.8,  # literacy rates low; digital skills training minimal
        ),
        EntityScore(
            entity_id="DD-006",
            name="Éthiopie — Guerre du Tigré & Coupures Réseau",
            sub1=5.5,  # nationwide shutdowns 2020–23; Tigray blackout 2 years+
            sub2=5.8,  # government-ordered shutdowns verified by NetBlocks & OONI
            sub3=5.5,  # poverty-driven exclusion; rural penetration ~15%
            sub4=5.0,  # conflict displaced educators; digital skills depleted
        ),
        # 1 modéré
        EntityScore(
            entity_id="DD-007",
            name="Cuba — Accès Contrôlé et Coûteux",
            sub1=3.0,  # mobile internet launched 2018; partial access only
            sub2=3.5,  # SNS temporarily blocked during protests; not systemic compared to worst cases
            sub3=3.0,  # costs prohibitive but state subsidies partially offset for citizens
            sub4=2.5,  # digital literacy improving in urban areas; state-filtered curriculum
        ),
        # 1 faible
        EntityScore(
            entity_id="DD-008",
            name="Afrique Sub-Saharienne Urbaine — Accès Croissant",
            sub1=1.5,  # urban areas increasingly connected; mobile-first growth
            sub2=1.0,  # no systematic censorship in Accra, Lagos, Nairobi urban cores
            sub3=1.8,  # data still expensive relative to income, but declining
            sub4=1.2,  # tech hubs active; digital literacy improving rapidly
        ),
    ]

    results = []
    for e in entities:
        results.append({
            "entity_id": e.entity_id,
            "name": e.name,
            "sub1_connectivity_gap": e.sub1,
            "sub2_censorship_digital": e.sub2,
            "sub3_affordability_exclusion": e.sub3,
            "sub4_digital_literacy_rights": e.sub4,
            "composite_score": e.composite_score,
            "risk_level": e.risk_level,
            "estimated_digital_divide_internet_access_index": e.estimated_index,
        })

    composites = [e.composite_score for e in entities]
    avg_composite = round(statistics.mean(composites), 2)

    distribution = {
        "critique": sum(1 for e in entities if e.risk_level == "critique"),
        "élevé": sum(1 for e in entities if e.risk_level == "élevé"),
        "modéré": sum(1 for e in entities if e.risk_level == "modéré"),
        "faible": sum(1 for e in entities if e.risk_level == "faible"),
    }

    summary = {
        "engine": "digital_divide_internet_access_rights_engine",
        "wave": 148,
        "total_entities": len(entities),
        "avg_composite": avg_composite,
        "distribution": distribution,
        "estimated_avg_index": round(avg_composite / 100 * 10, 2),
        "entities": results,
    }

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


if __name__ == "__main__":
    run_engine()
