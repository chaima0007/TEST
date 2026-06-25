#!/usr/bin/env python3
"""
Wave 172 — Freedom of Religion & Belief Persecution Engine
Caelum Partners SPRL — CaelumSwarm Intelligence Layer
Domaine : Liberté de religion/conviction, persécution minorités religieuses (art. 18 PIDCP)
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class ReligionBeliefPersecutionEntity:
    entity_id: str
    name: str
    country: str
    state_persecution_severity: float
    minority_violence_impunity: float
    legal_discrimination_score: float
    conversion_blasphemy_laws: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_religious_persecution_index: float = field(init=False)

    def __post_init__(self):
        self.composite_score = round(
            self.state_persecution_severity * 0.30
            + self.minority_violence_impunity * 0.25
            + self.legal_discrimination_score * 0.25
            + self.conversion_blasphemy_laws * 0.20,
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
        self.estimated_religious_persecution_index = round(self.composite_score / 100 * 10, 2)


def run_religion_belief_persecution_engine() -> dict:
    entities = [
        # CRITIQUE ≥ 60
        ReligionBeliefPersecutionEntity(
            entity_id="RBP-001",
            name="Chine/Falun Gong & Ouïghours — Camps Rééducation Xinjiang, Prélèvement Organes Prisonniers, Temples Détruits",
            country="Chine",
            state_persecution_severity=95.0,
            minority_violence_impunity=90.0,
            legal_discrimination_score=88.0,
            conversion_blasphemy_laws=82.0,
        ),
        ReligionBeliefPersecutionEntity(
            entity_id="RBP-002",
            name="Myanmar/Rohingya — Épuration Ethnique-Religieuse Bouddhiste-Musulmane, Génocide ONU Reconnu, Villages Brûlés",
            country="Myanmar",
            state_persecution_severity=92.0,
            minority_violence_impunity=95.0,
            legal_discrimination_score=85.0,
            conversion_blasphemy_laws=78.0,
        ),
        ReligionBeliefPersecutionEntity(
            entity_id="RBP-003",
            name="Pakistan/Loi Blasphème — Ahmadis Chrétiens Hindous Ciblés, Lynchages Populaires, Condamnations à Mort Fréquentes",
            country="Pakistan",
            state_persecution_severity=78.0,
            minority_violence_impunity=88.0,
            legal_discrimination_score=90.0,
            conversion_blasphemy_laws=95.0,
        ),
        ReligionBeliefPersecutionEntity(
            entity_id="RBP-004",
            name="Arabie Saoudite — Apostasie Peine de Mort, Zéro Liberté Culte Non-Musulman, Conversions Criminalisées",
            country="Arabie Saoudite",
            state_persecution_severity=85.0,
            minority_violence_impunity=75.0,
            legal_discrimination_score=95.0,
            conversion_blasphemy_laws=98.0,
        ),
        # ÉLEVÉ 40–59.9
        ReligionBeliefPersecutionEntity(
            entity_id="RBP-005",
            name="Inde/Minorités — Lynchages Anti-Musulmans Impunis, Loi CAA Discriminatoire, Montée BJP Nationalisme Hindou",
            country="Inde",
            state_persecution_severity=55.0,
            minority_violence_impunity=65.0,
            legal_discrimination_score=52.0,
            conversion_blasphemy_laws=45.0,
        ),
        ReligionBeliefPersecutionEntity(
            entity_id="RBP-006",
            name="Nigeria/Boko Haram — Persécution Chrétiens Nord, Enlèvements Filles Chibok, Conflit Interreligieux Plateau State",
            country="Nigeria",
            state_persecution_severity=48.0,
            minority_violence_impunity=70.0,
            legal_discrimination_score=42.0,
            conversion_blasphemy_laws=50.0,
        ),
        # MODÉRÉ 20–39.9
        ReligionBeliefPersecutionEntity(
            entity_id="RBP-007",
            name="France — Laïcité Controversée, Voile Scolaire Interdit, Discrimination Perçue Musulmans, Abaya Interdite 2023",
            country="France",
            state_persecution_severity=25.0,
            minority_violence_impunity=20.0,
            legal_discrimination_score=35.0,
            conversion_blasphemy_laws=10.0,
        ),
        # FAIBLE < 20
        ReligionBeliefPersecutionEntity(
            entity_id="RBP-008",
            name="Canada — Charte Droits Libertés Religieuses, Multiculturalisme Officiel, Protection Légale Minorités Robuste",
            country="Canada",
            state_persecution_severity=5.0,
            minority_violence_impunity=8.0,
            legal_discrimination_score=4.0,
            conversion_blasphemy_laws=3.0,
        ),
    ]

    distribution = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for e in entities:
        distribution[e.risk_level] += 1

    assert distribution == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, (
        f"Distribution invalide: {distribution}"
    )

    avg_composite = round(sum(e.composite_score for e in entities) / len(entities), 2)
    avg_index = round(sum(e.estimated_religious_persecution_index for e in entities) / len(entities), 2)

    return {
        "domain": "freedom_religion_belief_persecution",
        "generated_at": datetime.utcnow().isoformat(),
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "state_persecution_severity": e.state_persecution_severity,
                "minority_violence_impunity": e.minority_violence_impunity,
                "legal_discrimination_score": e.legal_discrimination_score,
                "conversion_blasphemy_laws": e.conversion_blasphemy_laws,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_religious_persecution_index": e.estimated_religious_persecution_index,
            }
            for e in entities
        ],
        "avg_composite": avg_composite,
        "avg_index": avg_index,
        "risk_distribution": distribution,
    }


if __name__ == "__main__":
    result = run_religion_belief_persecution_engine()
    print(f"Agent: Freedom Religion Belief Persecution Engine Agent")
    print(f"Total entities: {len(result['entities'])}")
    print(f"Avg composite: {result['avg_composite']}")
    print(f"Avg index: {result['avg_index']}")
    print(f"Risk distribution: {result['risk_distribution']}")
    for e in result["entities"]:
        print(f"  {e['entity_id']}: {e['composite_score']} [{e['risk_level']}] — {e['estimated_religious_persecution_index']}")
