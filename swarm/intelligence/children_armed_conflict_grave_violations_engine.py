#!/usr/bin/env python3
"""
Wave 147 — Children in Armed Conflict: Grave Violations Rights Intelligence Engine
Caelum Partners Swarm Intelligence Platform

Assesses severity of six grave violations against children in armed conflict
(MRM framework: killing, maiming, recruitment, sexual violence, abduction,
attacks on schools/hospitals, denial of humanitarian access) and accountability gaps.
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
"""

from dataclasses import dataclass, field
import json
import statistics


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # Frequency & scale of grave violations (0–10)
    sub2: float  # Child recruitment & use by armed actors (0–10)
    sub3: float  # Child protection systems & accountability (0–10)
    sub4: float  # Reintegration & psychosocial recovery access (0–10)
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
            entity_id="SD-001",
            name="Sudan — RSF & SAF Conflict",
            sub1=9.3,  # thousands of children killed, maimed; attacks on hospitals
            sub2=9.1,  # RSF recruiting children, documented UN MRM 2023-24
            sub3=9.2,  # no functioning child protection authority
            sub4=9.0,  # 14M children displaced, reintegration nonexistent
        ),
        EntityScore(
            entity_id="CD-002",
            name="DRC — Eastern Congo (M23 / FDLR)",
            sub1=8.9,  # persistent grave violations across 30+ armed groups
            sub2=9.0,  # M23 & FDLR extensively recruit and abduct children
            sub3=8.8,  # MRM monitoring disrupted, agencies expelled
            sub4=8.6,  # DDRR programs chronically underfunded
        ),
        EntityScore(
            entity_id="MM-003",
            name="Myanmar — Junta & Armed Groups",
            sub1=8.7,  # airstrikes on schools, child conscription since 2021 coup
            sub2=8.9,  # Tatmadaw listed by UN SG for grave violations repeatedly
            sub3=8.8,  # zero accountability since coup, UNICEF expelled from areas
            sub4=8.4,  # over 600K children displaced with minimal support
        ),
        EntityScore(
            entity_id="YE-004",
            name="Yemen — Houthi & Coalition Forces",
            sub1=8.5,  # decade of violations: 11,000+ children casualties verified
            sub2=8.7,  # Houthis listed Party to Conflict; mass child recruitment
            sub3=8.4,  # Sanaa/Houthi-controlled: MRM access near-zero
            sub4=8.2,  # reintegration centers destroyed, 21M children in need
        ),
        # 2 élevé
        EntityScore(
            entity_id="SO-005",
            name="Somalia — Al-Shabaab & Clan Violence",
            sub1=5.1,  # al-Shabaab uses children as soldiers and suicide bombers
            sub2=5.6,  # recruitment normalized in al-Shabaab controlled zones
            sub3=5.3,  # federal government MRM exists but weak enforcement
            sub4=4.8,  # reintegration programs patchy, stigmatization high
        ),
        EntityScore(
            entity_id="ML-006",
            name="Mali — Sahel Jihadist Groups",
            sub1=4.9,  # JNIM and GSIM increasingly recruiting youth
            sub2=5.3,  # child recruitment accelerated post-MINUSMA withdrawal
            sub3=5.0,  # transitional government suspended MRM cooperation
            sub4=4.5,  # reintegration centers in Bamako overwhelmed
        ),
        # 1 modéré
        EntityScore(
            entity_id="CO-007",
            name="Colombia — FARC Dissidents & ELN",
            sub1=3.3,  # dissidents & ELN recruit children in border areas
            sub2=3.7,  # recruitment continues despite JEP investigations
            sub3=3.6,  # ICBF active, National Reintegration Agency functioning
            sub4=3.1,  # psychosocial support exists but underfunded in rural zones
        ),
        # 1 faible
        EntityScore(
            entity_id="SL-008",
            name="Sierra Leone — Post-War Recovery Model",
            sub1=0.9,  # active conflict ended 2002; isolated incidents only
            sub2=1.0,  # no active recruitment; armed groups dissolved
            sub3=1.3,  # Truth & Reconciliation Commission landmark
            sub4=1.6,  # former child soldiers reintegration programs model for Africa
        ),
    ]

    results = []
    for e in entities:
        results.append({
            "entity_id": e.entity_id,
            "name": e.name,
            "sub1_grave_violations_scale": e.sub1,
            "sub2_child_recruitment": e.sub2,
            "sub3_child_protection_accountability": e.sub3,
            "sub4_reintegration_recovery": e.sub4,
            "composite_score": e.composite_score,
            "risk_level": e.risk_level,
            "estimated_children_conflict_index": e.estimated_index,
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
        "engine": "children_armed_conflict_grave_violations_engine",
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
