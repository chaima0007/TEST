#!/usr/bin/env python3
import json
from dataclasses import dataclass, field


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1_journalist_killings_imprisonment: float
    sub2_state_media_censorship: float
    sub3_legal_intimidation_slapp: float
    sub4_digital_surveillance_press: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_media_freedom_journalist_protection_index: float = field(init=False)

    def __post_init__(self):
        self.composite_score = round(
            (
                self.sub1_journalist_killings_imprisonment * 0.30
                + self.sub2_state_media_censorship * 0.25
                + self.sub3_legal_intimidation_slapp * 0.25
                + self.sub4_digital_surveillance_press * 0.20
            ) * 10,
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
        self.estimated_media_freedom_journalist_protection_index = round(
            self.composite_score / 100 * 10, 2
        )


def run():
    entities = [
        # 4 critique (composite_score >= 60)
        EntityScore(
            entity_id="ERI",
            name="Érythrée",
            sub1_journalist_killings_imprisonment=9.2,
            sub2_state_media_censorship=9.5,
            sub3_legal_intimidation_slapp=8.8,
            sub4_digital_surveillance_press=8.0,
        ),
        EntityScore(
            entity_id="PRK",
            name="Corée du Nord",
            sub1_journalist_killings_imprisonment=9.0,
            sub2_state_media_censorship=9.8,
            sub3_legal_intimidation_slapp=9.0,
            sub4_digital_surveillance_press=8.5,
        ),
        EntityScore(
            entity_id="TKM",
            name="Turkménistan",
            sub1_journalist_killings_imprisonment=8.5,
            sub2_state_media_censorship=9.2,
            sub3_legal_intimidation_slapp=8.5,
            sub4_digital_surveillance_press=8.2,
        ),
        EntityScore(
            entity_id="RUS",
            name="Russie",
            sub1_journalist_killings_imprisonment=8.0,
            sub2_state_media_censorship=8.5,
            sub3_legal_intimidation_slapp=8.0,
            sub4_digital_surveillance_press=8.8,
        ),
        # 2 élevé (40 <= composite_score < 60)
        EntityScore(
            entity_id="CHN",
            name="Chine",
            sub1_journalist_killings_imprisonment=5.5,
            sub2_state_media_censorship=6.5,
            sub3_legal_intimidation_slapp=5.8,
            sub4_digital_surveillance_press=6.2,
        ),
        EntityScore(
            entity_id="MMR",
            name="Myanmar",
            sub1_journalist_killings_imprisonment=5.8,
            sub2_state_media_censorship=5.5,
            sub3_legal_intimidation_slapp=5.2,
            sub4_digital_surveillance_press=5.0,
        ),
        # 1 modéré (20 <= composite_score < 40)
        EntityScore(
            entity_id="MEX",
            name="Mexique",
            sub1_journalist_killings_imprisonment=3.8,
            sub2_state_media_censorship=2.5,
            sub3_legal_intimidation_slapp=3.2,
            sub4_digital_surveillance_press=2.8,
        ),
        # 1 faible (composite_score < 20)
        EntityScore(
            entity_id="FIN",
            name="Finlande",
            sub1_journalist_killings_imprisonment=0.3,
            sub2_state_media_censorship=0.4,
            sub3_legal_intimidation_slapp=0.5,
            sub4_digital_surveillance_press=0.4,
        ),
    ]

    results = []
    for e in entities:
        results.append(
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_media_freedom_journalist_protection_index": e.estimated_media_freedom_journalist_protection_index,
            }
        )

    avg_composite = round(
        sum(r["composite_score"] for r in results) / len(results), 2
    )
    distribution = {}
    for r in results:
        distribution[r["risk_level"]] = distribution.get(r["risk_level"], 0) + 1

    output = {
        "engine": "media_freedom_journalist_protection_engine",
        "wave": 150,
        "total_entities": len(results),
        "avg_composite": avg_composite,
        "distribution": distribution,
        "estimated_avg_index": round(avg_composite / 100 * 10, 2),
        "entities": results,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run()
