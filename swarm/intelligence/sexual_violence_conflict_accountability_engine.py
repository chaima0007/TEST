#!/usr/bin/env python3
"""
Wave 147 — Sexual Violence in Conflict: Accountability Rights Intelligence Engine
Caelum Partners Swarm Intelligence Platform

Assesses severity of conflict-related sexual violence (CRSV) and gaps in
accountability, survivor justice, and reparation for affected populations.
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
"""

from dataclasses import dataclass, field
import json
import statistics


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # Prevalence & scale of CRSV (0–10)
    sub2: float  # Impunity & accountability gap (0–10)
    sub3: float  # Survivor access to justice & services (0–10)
    sub4: float  # Reparation & recognition deficit (0–10)
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
            entity_id="SD-RSF-001",
            name="Sudan / RSF — Darfur & Khartoum",
            sub1=9.2,  # mass rape documented by UN as weapon of war since 2023
            sub2=9.4,  # RSF perpetrators face zero accountability
            sub3=9.3,  # survivors trapped in active conflict zones
            sub4=9.1,  # no reparation mechanism, ICC stalled
        ),
        EntityScore(
            entity_id="CD-M23-002",
            name="DRC / M23 — Eastern Congo",
            sub1=9.0,  # decades of systematic CRSV, 2023-24 surge
            sub2=9.2,  # chronic impunity for armed groups and military
            sub3=8.9,  # health services overwhelmed, fistula clinics under attack
            sub4=8.7,  # reparations law exists but unimplemented
        ),
        EntityScore(
            entity_id="MM-003",
            name="Myanmar — Military Junta (Tatmadaw)",
            sub1=8.8,  # CRSV systematically used against Rohingya and ethnic groups
            sub2=9.0,  # junta immunity, ICC referral blocked by China/Russia
            sub3=8.7,  # refugees in Bangladesh camps lack judicial access
            sub4=8.5,  # no acknowledgment or reparation to survivors
        ),
        EntityScore(
            entity_id="UA-RU-004",
            name="Russia — Ukraine Conflict CRSV",
            sub1=8.2,  # UN documented widespread rape in occupied territories
            sub2=8.6,  # Russian state impunity, ICC arrest warrant for Putin only
            sub3=8.0,  # Ukrainian survivors accessing justice domestically
            sub4=7.8,  # reparation fund theorized but not operational
        ),
        # 2 élevé
        EntityScore(
            entity_id="ML-005",
            name="Mali — Sahel Armed Groups",
            sub1=5.2,  # jihadist groups using sexual violence as control
            sub2=5.8,  # MINUSMA withdrawal reduced accountability pressure
            sub3=5.5,  # isolated survivors in conflict zones
            sub4=4.9,  # transitional government has no CRSV accountability plan
        ),
        EntityScore(
            entity_id="HT-006",
            name="Haiti — Gang Violence CRSV",
            sub1=5.6,  # gang-controlled areas: mass rape as territorial control
            sub2=5.4,  # state collapse — no functioning justice system
            sub3=5.8,  # MSF & NGOs operating under siege conditions
            sub4=4.7,  # no reparation or recognition framework in place
        ),
        # 1 modéré
        EntityScore(
            entity_id="CO-007",
            name="Colombia — Post-Accord Accountability",
            sub1=3.4,  # JEP (Special Jurisdiction for Peace) active, cases advancing
            sub2=3.8,  # partial accountability via JEP — dissidents still active
            sub3=3.5,  # truth commission report published 2022
            sub4=3.2,  # reparations ongoing but slow, survivors re-victimized
        ),
        # 1 faible
        EntityScore(
            entity_id="RW-008",
            name="Rwanda — Post-Genocide Reconciliation",
            sub1=1.1,  # active CRSV largely ended post-1994
            sub2=1.5,  # Gacaca courts addressed many cases; ICC trials completed
            sub3=1.3,  # survivor support organizations institutionalized
            sub4=1.8,  # reparation programs exist, though under-resourced
        ),
    ]

    results = []
    for e in entities:
        results.append({
            "entity_id": e.entity_id,
            "name": e.name,
            "sub1_crsv_prevalence": e.sub1,
            "sub2_impunity_gap": e.sub2,
            "sub3_survivor_access_justice": e.sub3,
            "sub4_reparation_deficit": e.sub4,
            "composite_score": e.composite_score,
            "risk_level": e.risk_level,
            "estimated_crsv_accountability_index": e.estimated_index,
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
        "engine": "sexual_violence_conflict_accountability_engine",
        "wave": 147,
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
