from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class PlatformEconomyEntity:
    entity_id: str
    platform_sector: str
    region: str
    # 17 float fields (0-1)
    wage_theft_index: float
    algorithmic_management_intensity: float
    benefit_denial_rate: float
    misclassification_prevalence: float
    platform_market_concentration: float
    worker_bargaining_power: float
    regulatory_compliance: float
    social_protection_gap: float
    income_volatility: float
    surveillance_score: float
    deactivation_risk: float
    minimum_earnings_gap: float
    union_access_barrier: float
    data_portability: float
    cross_platform_competition: float
    transparency_score: float
    legal_protection_effectiveness: float

    def exploitation_score(self) -> float:
        raw = (self.wage_theft_index + self.algorithmic_management_intensity) / 2 * 100
        return round(raw * 100) / 100

    def precarity_score(self) -> float:
        raw = (
            self.benefit_denial_rate
            + self.social_protection_gap
            + self.income_volatility
            + self.deactivation_risk
            + self.minimum_earnings_gap
        ) / 5 * 100
        return round(raw * 100) / 100

    def monopoly_score(self) -> float:
        raw = (
            self.platform_market_concentration
            + self.union_access_barrier
            + (1 - self.data_portability)
            + (1 - self.cross_platform_competition)
        ) / 4 * 100
        return round(raw * 100) / 100

    def misclassification_score(self) -> float:
        raw = (
            self.misclassification_prevalence
            + (1 - self.regulatory_compliance)
            + (1 - self.legal_protection_effectiveness)
        ) / 3 * 100
        return round(raw * 100) / 100

    def composite_score(self) -> float:
        exp = self.exploitation_score()
        pre = self.precarity_score()
        mon = self.monopoly_score()
        mis = self.misclassification_score()
        return round(
            (exp * 0.30 + pre * 0.25 + mon * 0.25 + mis * 0.20) * 100
        ) / 100

    def risk_level(self) -> str:
        c = self.composite_score()
        if c >= 60:
            return "critical"
        if c >= 40:
            return "high"
        if c >= 20:
            return "moderate"
        return "low"

    def dominant_pattern(self) -> str:
        if self.surveillance_score > 0.7:
            return "surveillance_control_dystopia"
        exp = self.exploitation_score()
        pre = self.precarity_score()
        mon = self.monopoly_score()
        mis = self.misclassification_score()
        scores = {
            "algorithmic_wage_theft": exp,
            "benefits_denial_systematic": pre,
            "platform_monopoly_capture": mon,
            "misclassification_fraud": mis,
        }
        return max(scores, key=lambda k: scores[k])

    def patterns_detected(self) -> List[str]:
        patterns = []
        if self.exploitation_score() > 50:
            patterns.append("algorithmic_wage_theft")
        if self.precarity_score() > 50:
            patterns.append("benefits_denial_systematic")
        if self.monopoly_score() > 50:
            patterns.append("platform_monopoly_capture")
        if self.misclassification_score() > 50:
            patterns.append("misclassification_fraud")
        if self.surveillance_score > 0.7:
            if "surveillance_control_dystopia" not in patterns:
                patterns.append("surveillance_control_dystopia")
        return patterns

    def severity(self) -> str:
        c = self.composite_score()
        if c >= 60:
            return "critique"
        if c >= 40:
            return "élevée"
        if c >= 20:
            return "modérée"
        return "faible"

    def action(self) -> str:
        risk = self.risk_level()
        if risk == "critical":
            return "intervention_urgente_droits_travailleurs_plateformes_critiques"
        if risk == "high":
            return "renforcement_protection_sociale_gig_economy_accéléré"
        if risk == "moderate":
            return "audit_conditions_travail_plateforme_et_reclassification"
        return "veille_économie_plateformes_continue"

    def signal(self) -> str:
        risk = self.risk_level()
        if risk == "critical":
            return "🔴 Exploitation systémique travailleurs gig — droits fondamentaux en péril"
        if risk == "high":
            return "🟠 Précarité structurelle majeure détectée — protection sociale insuffisante"
        if risk == "moderate":
            return "🟡 Risque modéré économie plateforme — surveillance active requise"
        return "🟢 Économie plateforme sous surveillance — droits travailleurs stables"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "platform_sector": self.platform_sector,
            "region": self.region,
            "exploitation_score": self.exploitation_score(),
            "precarity_score": self.precarity_score(),
            "monopoly_score": self.monopoly_score(),
            "misclassification_score": self.misclassification_score(),
            "composite_score": self.composite_score(),
            "risk_level": self.risk_level(),
            "dominant_pattern": self.dominant_pattern(),
            "patterns_detected": self.patterns_detected(),
            "severity": self.severity(),
            "action": self.action(),
            "signal": self.signal(),
            "surveillance_score": self.surveillance_score,
        }


# 8 mock entities covering all 5 patterns + all 4 risk levels
# PEE-001: critical — algorithmic_wage_theft dominant
# PEE-002: critical — surveillance_control_dystopia (surveillance > 0.7)
# PEE-003: critical — misclassification_fraud dominant
# PEE-004: high    — platform_monopoly_capture dominant
# PEE-005: high    — surveillance_control_dystopia (surveillance > 0.7)
# PEE-006: moderate — benefits_denial_systematic dominant
# PEE-007: low
# PEE-008: low
MOCK_ENTITIES: List[PlatformEconomyEntity] = [
    # PEE-001 — critical, algorithmic_wage_theft dominant (exploitation very high)
    PlatformEconomyEntity(
        entity_id="PEE-001", platform_sector="ride_hailing", region="NOAM",
        wage_theft_index=0.92, algorithmic_management_intensity=0.88,
        benefit_denial_rate=0.80, misclassification_prevalence=0.78,
        platform_market_concentration=0.70, worker_bargaining_power=0.15,
        regulatory_compliance=0.22, social_protection_gap=0.75,
        income_volatility=0.72, surveillance_score=0.65,
        deactivation_risk=0.70, minimum_earnings_gap=0.68,
        union_access_barrier=0.72, data_portability=0.20,
        cross_platform_competition=0.22, transparency_score=0.18,
        legal_protection_effectiveness=0.20,
    ),
    # PEE-002 — critical, surveillance_control_dystopia (surveillance > 0.7)
    PlatformEconomyEntity(
        entity_id="PEE-002", platform_sector="food_delivery", region="EMEA",
        wage_theft_index=0.78, algorithmic_management_intensity=0.72,
        benefit_denial_rate=0.90, misclassification_prevalence=0.82,
        platform_market_concentration=0.68, worker_bargaining_power=0.12,
        regulatory_compliance=0.18, social_protection_gap=0.88,
        income_volatility=0.85, surveillance_score=0.88,
        deactivation_risk=0.82, minimum_earnings_gap=0.80,
        union_access_barrier=0.75, data_portability=0.15,
        cross_platform_competition=0.18, transparency_score=0.12,
        legal_protection_effectiveness=0.15,
    ),
    # PEE-003 — critical, misclassification_fraud dominant
    PlatformEconomyEntity(
        entity_id="PEE-003", platform_sector="freelance_marketplace", region="APAC",
        wage_theft_index=0.75, algorithmic_management_intensity=0.70,
        benefit_denial_rate=0.72, misclassification_prevalence=0.95,
        platform_market_concentration=0.65, worker_bargaining_power=0.10,
        regulatory_compliance=0.08, social_protection_gap=0.70,
        income_volatility=0.68, surveillance_score=0.60,
        deactivation_risk=0.65, minimum_earnings_gap=0.62,
        union_access_barrier=0.68, data_portability=0.25,
        cross_platform_competition=0.20, transparency_score=0.15,
        legal_protection_effectiveness=0.10,
    ),
    # PEE-004 — high, platform_monopoly_capture dominant
    PlatformEconomyEntity(
        entity_id="PEE-004", platform_sector="cloud_labor", region="LATAM",
        wage_theft_index=0.50, algorithmic_management_intensity=0.48,
        benefit_denial_rate=0.52, misclassification_prevalence=0.50,
        platform_market_concentration=0.65, worker_bargaining_power=0.28,
        regulatory_compliance=0.35, social_protection_gap=0.50,
        income_volatility=0.48, surveillance_score=0.50,
        deactivation_risk=0.45, minimum_earnings_gap=0.48,
        union_access_barrier=0.60, data_portability=0.20,
        cross_platform_competition=0.22, transparency_score=0.28,
        legal_protection_effectiveness=0.32,
    ),
    # PEE-005 — high, surveillance_control_dystopia (surveillance > 0.7)
    PlatformEconomyEntity(
        entity_id="PEE-005", platform_sector="domestic_services", region="SSA",
        wage_theft_index=0.58, algorithmic_management_intensity=0.55,
        benefit_denial_rate=0.52, misclassification_prevalence=0.50,
        platform_market_concentration=0.48, worker_bargaining_power=0.22,
        regulatory_compliance=0.32, social_protection_gap=0.50,
        income_volatility=0.48, surveillance_score=0.75,
        deactivation_risk=0.45, minimum_earnings_gap=0.48,
        union_access_barrier=0.52, data_portability=0.32,
        cross_platform_competition=0.30, transparency_score=0.28,
        legal_protection_effectiveness=0.30,
    ),
    # PEE-006 — moderate, benefits_denial_systematic dominant
    PlatformEconomyEntity(
        entity_id="PEE-006", platform_sector="microtask", region="EMEA",
        wage_theft_index=0.28, algorithmic_management_intensity=0.25,
        benefit_denial_rate=0.55, misclassification_prevalence=0.28,
        platform_market_concentration=0.30, worker_bargaining_power=0.42,
        regulatory_compliance=0.52, social_protection_gap=0.50,
        income_volatility=0.45, surveillance_score=0.32,
        deactivation_risk=0.38, minimum_earnings_gap=0.40,
        union_access_barrier=0.32, data_portability=0.48,
        cross_platform_competition=0.45, transparency_score=0.42,
        legal_protection_effectiveness=0.50,
    ),
    # PEE-007 — low
    PlatformEconomyEntity(
        entity_id="PEE-007", platform_sector="professional_services", region="NOAM",
        wage_theft_index=0.10, algorithmic_management_intensity=0.12,
        benefit_denial_rate=0.12, misclassification_prevalence=0.10,
        platform_market_concentration=0.15, worker_bargaining_power=0.75,
        regulatory_compliance=0.80, social_protection_gap=0.12,
        income_volatility=0.10, surveillance_score=0.15,
        deactivation_risk=0.10, minimum_earnings_gap=0.08,
        union_access_barrier=0.12, data_portability=0.82,
        cross_platform_competition=0.78, transparency_score=0.80,
        legal_protection_effectiveness=0.82,
    ),
    # PEE-008 — low
    PlatformEconomyEntity(
        entity_id="PEE-008", platform_sector="e_commerce_seller", region="APAC",
        wage_theft_index=0.08, algorithmic_management_intensity=0.10,
        benefit_denial_rate=0.10, misclassification_prevalence=0.08,
        platform_market_concentration=0.18, worker_bargaining_power=0.70,
        regulatory_compliance=0.75, social_protection_gap=0.10,
        income_volatility=0.12, surveillance_score=0.12,
        deactivation_risk=0.08, minimum_earnings_gap=0.10,
        union_access_barrier=0.10, data_portability=0.78,
        cross_platform_competition=0.72, transparency_score=0.75,
        legal_protection_effectiveness=0.78,
    ),
]


class PlatformEconomyEngine:
    def __init__(self, entities: List[PlatformEconomyEntity] = None):
        self._entities = entities if entities is not None else MOCK_ENTITIES

    def get_entities(self) -> List[Dict[str, Any]]:
        return [e.to_dict() for e in self._entities]

    def analyze(self) -> Dict[str, Any]:
        results = self.get_entities()

        total_exploitation = 0.0
        total_precarity = 0.0
        total_monopoly = 0.0
        total_misclassification = 0.0
        total_composite = 0.0
        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0
        pattern_counts: Dict[str, int] = {}

        for r in results:
            total_exploitation += r["exploitation_score"]
            total_precarity += r["precarity_score"]
            total_monopoly += r["monopoly_score"]
            total_misclassification += r["misclassification_score"]
            total_composite += r["composite_score"]

            rl = r["risk_level"]
            if rl == "critical":
                critical_count += 1
            elif rl == "high":
                high_count += 1
            elif rl == "moderate":
                moderate_count += 1
            else:
                low_count += 1

            dp = r["dominant_pattern"]
            pattern_counts[dp] = pattern_counts.get(dp, 0) + 1

        n = len(results) or 1
        avg_exploitation = round(total_exploitation / n * 10) / 10
        avg_precarity = round(total_precarity / n * 10) / 10
        avg_monopoly = round(total_monopoly / n * 10) / 10
        avg_misclassification = round(total_misclassification / n * 10) / 10
        avg_composite = round(total_composite / n * 10) / 10
        top_pattern = max(pattern_counts, key=lambda k: pattern_counts[k]) if pattern_counts else ""
        entities_at_risk = critical_count + high_count

        summary = self.get_summary(
            results=results,
            critical_count=critical_count,
            high_count=high_count,
            moderate_count=moderate_count,
            low_count=low_count,
            avg_exploitation=avg_exploitation,
            avg_precarity=avg_precarity,
            avg_monopoly=avg_monopoly,
            avg_misclassification=avg_misclassification,
            avg_composite=avg_composite,
            top_pattern=top_pattern,
            entities_at_risk=entities_at_risk,
        )
        return {"entities": results, "summary": summary}

    def get_summary(
        self,
        results: List[Dict[str, Any]] = None,
        critical_count: int = 0,
        high_count: int = 0,
        moderate_count: int = 0,
        low_count: int = 0,
        avg_exploitation: float = 0.0,
        avg_precarity: float = 0.0,
        avg_monopoly: float = 0.0,
        avg_misclassification: float = 0.0,
        avg_composite: float = 0.0,
        top_pattern: str = "",
        entities_at_risk: int = 0,
    ) -> Dict[str, Any]:
        results = results or []
        return {
            "total_entities": len(results),
            "critical_count": critical_count,
            "high_count": high_count,
            "moderate_count": moderate_count,
            "low_count": low_count,
            "avg_exploitation": avg_exploitation,
            "avg_precarity": avg_precarity,
            "avg_monopoly": avg_monopoly,
            "avg_misclassification": avg_misclassification,
            "avg_composite": avg_composite,
            "top_pattern": top_pattern,
            "entities_at_risk": entities_at_risk,
            "avg_estimated_gig_rights_index": round(avg_composite / 100 * 10, 2),
        }


def main():
    engine = PlatformEconomyEngine()
    output = engine.analyze()
    summary = output["summary"]
    entities = output["entities"]

    print("=" * 60)
    print("Module 408 — Économie de Plateforme & Droits Travailleurs Gig")
    print("=" * 60)
    print(f"Total entités analysées : {summary['total_entities']}")
    print(f"Critique : {summary['critical_count']}")
    print(f"Élevé    : {summary['high_count']}")
    print(f"Modéré   : {summary['moderate_count']}")
    print(f"Faible   : {summary['low_count']}")
    print(f"Score composite moyen : {summary['avg_composite']}")
    print(f"Index droits gig estimé : {summary['avg_estimated_gig_rights_index']}/10")
    print(f"Patron dominant : {summary['top_pattern']}")
    print(f"Entités à risque : {summary['entities_at_risk']}")
    print()
    for e in entities:
        print(
            f"  {e['entity_id']} | {e['platform_sector']:25s} | "
            f"{e['region']:6s} | composite={e['composite_score']:5.1f} | "
            f"risque={e['risk_level']:8s} | {e['dominant_pattern']}"
        )


if __name__ == "__main__":
    main()
