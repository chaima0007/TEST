from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # ×0.30 — amplification discours haineux
    sub2: float  # ×0.25 — défaillances modération contenu
    sub3: float  # ×0.25 — dommages algorithmiques (radicalisation)
    sub4: float  # ×0.20 — transparence rapports & coopération

    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_platform_accountability_index: float = field(init=False)

    def __post_init__(self):
        self.composite_score = round(
            self.sub1 * 0.30 + self.sub2 * 0.25 + self.sub3 * 0.25 + self.sub4 * 0.20, 2
        )
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_platform_accountability_index = round(self.composite_score / 100 * 10, 2)


def run_engine() -> List[EntityScore]:
    entities = [
        EntityScore(
            entity_id="SMP-001",
            name="Meta (Myanmar genocide enabler)",
            sub1=92.0, sub2=88.0, sub3=85.0, sub4=84.0
        ),
        EntityScore(
            entity_id="SMP-002",
            name="TikTok (propagande État + enfants)",
            sub1=84.0, sub2=82.0, sub3=80.0, sub4=78.0
        ),
        EntityScore(
            entity_id="SMP-003",
            name="Telegram (terrorisme + trafic humain)",
            sub1=80.0, sub2=78.0, sub3=76.0, sub4=72.0
        ),
        EntityScore(
            entity_id="SMP-004",
            name="X/Twitter (post-Musk: modération effondrée)",
            sub1=78.0, sub2=74.0, sub3=72.0, sub4=68.0
        ),
        EntityScore(
            entity_id="SMP-005",
            name="YouTube (radicalisation algorithme)",
            sub1=58.0, sub2=56.0, sub3=60.0, sub4=52.0
        ),
        EntityScore(
            entity_id="SMP-006",
            name="WhatsApp (Inde: mob lynchings)",
            sub1=52.0, sub2=48.0, sub3=46.0, sub4=44.0
        ),
        EntityScore(
            entity_id="SMP-007",
            name="Facebook EU (DSA compliance partielle)",
            sub1=32.0, sub2=30.0, sub3=28.0, sub4=36.0
        ),
        EntityScore(
            entity_id="SMP-008",
            name="Signal (chiffrement + privacy)",
            sub1=8.0, sub2=10.0, sub3=9.0, sub4=10.0
        ),
    ]
    return entities


def main():
    entities = run_engine()

    print("=" * 60)
    print("SOCIAL MEDIA PLATFORM ACCOUNTABILITY ENGINE — Wave 164")
    print("=" * 60)

    dist: Dict[str, int] = {}
    total = 0.0

    for e in entities:
        dist[e.risk_level] = dist.get(e.risk_level, 0) + 1
        total += e.composite_score
        print(
            f"[{e.risk_level.upper():8s}] {e.name[:50]:<50s} "
            f"composite={e.composite_score:.2f}  index={e.estimated_platform_accountability_index:.2f}"
        )

    avg = total / len(entities)

    print()
    print(f"avg_composite : {avg:.2f}")
    print(f"Distribution  : critique={dist.get('critique',0)} | élevé={dist.get('élevé',0)} | modéré={dist.get('modéré',0)} | faible={dist.get('faible',0)}")
    ok = (dist.get('critique',0)==4 and dist.get('élevé',0)==2 and dist.get('modéré',0)==1 and dist.get('faible',0)==1)
    print(f"Distribution OK : {'✓' if ok else '✗'}")

    assert ok, "Distribution incorrecte — ajuster les sous-scores"

    output = {
        "engine": "social_media_platform_accountability_engine",
        "wave": 164,
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "sub1_hate_speech_amplification": e.sub1,
                "sub2_content_moderation_failure": e.sub2,
                "sub3_algorithmic_harm": e.sub3,
                "sub4_transparency_reporting": e.sub4,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_platform_accountability_index": e.estimated_platform_accountability_index,
            }
            for e in entities
        ],
        "avg_composite": round(avg, 2),
        "distribution": dist,
    }
    print()
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
