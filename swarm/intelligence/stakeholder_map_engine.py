from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class StakeholderRole(str, Enum):
    ECONOMIC_BUYER = "economic_buyer"
    CHAMPION = "champion"
    TECHNICAL_BUYER = "technical_buyer"
    END_USER = "end_user"
    BLOCKER = "blocker"
    INFLUENCER = "influencer"
    UNKNOWN = "unknown"


class EngagementLevel(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    NONE = "none"
    HOSTILE = "hostile"


class RelationshipStatus(str, Enum):
    SPONSOR = "sponsor"
    ALLY = "ally"
    NEUTRAL = "neutral"
    SKEPTIC = "skeptic"
    OPPONENT = "opponent"


class CoverageRisk(str, Enum):
    COVERED = "covered"
    PARTIAL = "partial"
    AT_RISK = "at_risk"
    CRITICAL = "critical"


@dataclass
class StakeholderInput:
    stakeholder_id: str
    account_id: str
    deal_id: str
    seniority: int                 # 1–5 (5 = C-suite)
    activities_30d: int            # CRM activities last 30 days
    meetings_held: int
    emails_sent: int
    emails_responded: int
    last_contact_days: int         # days since last contact
    sentiment_score: float         # 0–1 (1 = very positive)
    is_economic_buyer: bool
    is_champion: bool
    is_technical_buyer: bool
    is_end_user: bool
    is_blocker: bool
    has_budget_authority: bool
    deal_stage: str                # prospecting/discovery/demo/proposal/negotiation/closing
    prior_wins: int                # historical wins with this persona
    days_in_deal: int
    aligned_with_vendor: bool      # has expressed preference for our solution


@dataclass
class StakeholderResult:
    stakeholder_id: str
    account_id: str
    deal_id: str
    influence_score: float
    engagement_level: EngagementLevel
    relationship_status: RelationshipStatus
    stakeholder_role: StakeholderRole
    coverage_risk: CoverageRisk
    engagement_gap: float
    is_at_risk: bool
    priority_rank: int
    recommended_action: str
    risk_factors: list[str]
    strengths: list[str]
    recommended_approach: str

    def to_dict(self) -> dict:
        return {
            "stakeholder_id":     self.stakeholder_id,
            "account_id":         self.account_id,
            "deal_id":            self.deal_id,
            "influence_score":    self.influence_score,
            "engagement_level":   self.engagement_level.value,
            "relationship_status": self.relationship_status.value,
            "stakeholder_role":   self.stakeholder_role.value,
            "coverage_risk":      self.coverage_risk.value,
            "engagement_gap":     self.engagement_gap,
            "is_at_risk":         self.is_at_risk,
            "priority_rank":      self.priority_rank,
            "recommended_action": self.recommended_action,
            "risk_factors":       self.risk_factors,
            "strengths":          self.strengths,
            "recommended_approach": self.recommended_approach,
        }


class StakeholderMapEngine:
    def __init__(self) -> None:
        self._results: list[StakeholderResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: StakeholderInput) -> StakeholderResult:
        influence  = self._influence_score(inp)
        engagement = self._engagement_score(inp)
        level      = self._engagement_level(inp, engagement)
        status     = self._relationship_status(inp, engagement)
        role       = self._stakeholder_role(inp)
        gap        = self._engagement_gap(influence, engagement)
        risk       = self._coverage_risk(influence, engagement)
        is_at_risk = risk in (CoverageRisk.AT_RISK, CoverageRisk.CRITICAL)
        action     = self._recommended_action(inp, role, level, status, risk, influence, engagement)
        approach   = self._recommended_approach(inp, role, status, level)
        rf         = self._risk_factors(inp, level, risk)
        st         = self._strengths(inp, level, status)

        result = StakeholderResult(
            stakeholder_id=inp.stakeholder_id,
            account_id=inp.account_id,
            deal_id=inp.deal_id,
            influence_score=influence,
            engagement_level=level,
            relationship_status=status,
            stakeholder_role=role,
            coverage_risk=risk,
            engagement_gap=gap,
            is_at_risk=is_at_risk,
            priority_rank=0,
            recommended_action=action,
            risk_factors=rf,
            strengths=st,
            recommended_approach=approach,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[StakeholderInput]) -> list[StakeholderResult]:
        results = [self.analyze(inp) for inp in inputs]
        sorted_by_gap = sorted(results, key=lambda r: r.engagement_gap, reverse=True)
        for rank, r in enumerate(sorted_by_gap, 1):
            r.priority_rank = rank
        return results

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def analyzed_stakeholders(self) -> list[StakeholderResult]:
        return list(self._results)

    @property
    def at_risk_stakeholders(self) -> list[StakeholderResult]:
        return [r for r in self._results if r.is_at_risk]

    @property
    def champions(self) -> list[StakeholderResult]:
        return [r for r in self._results if r.stakeholder_role == StakeholderRole.CHAMPION]

    @property
    def economic_buyers(self) -> list[StakeholderResult]:
        return [r for r in self._results if r.stakeholder_role == StakeholderRole.ECONOMIC_BUYER]

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _influence_score(self, inp: StakeholderInput) -> float:
        base_map = {1: 10, 2: 25, 3: 45, 4: 65, 5: 85}
        score = float(base_map.get(max(1, min(5, inp.seniority)), 10))
        if inp.is_economic_buyer:   score += 15
        if inp.has_budget_authority: score += 15
        if inp.is_champion:         score += 10
        if inp.is_technical_buyer:  score += 8
        if inp.is_blocker:          score -= 10
        if inp.prior_wins > 2:      score += 5
        return round(max(0.0, min(100.0, score)), 1)

    def _engagement_score(self, inp: StakeholderInput) -> float:
        response_rate  = inp.emails_responded / max(1, inp.emails_sent)
        activity_base  = min(30.0, inp.activities_30d * 3.0)
        meeting_base   = min(20.0, inp.meetings_held * 5.0)
        response_base  = min(20.0, response_rate * 20.0)
        score = activity_base + meeting_base + response_base

        if   inp.last_contact_days <= 7:  score += 15
        elif inp.last_contact_days <= 14: score += 5
        elif inp.last_contact_days > 30:  score -= 20
        elif inp.last_contact_days > 21:  score -= 10

        if   inp.sentiment_score > 0.7:  score += 10
        elif inp.sentiment_score < 0.3:  score -= 15

        return round(max(0.0, min(100.0, score)), 1)

    def _engagement_level(self, inp: StakeholderInput, engagement: float) -> EngagementLevel:
        if inp.sentiment_score < 0.25 and inp.last_contact_days > 7 and inp.activities_30d == 0:
            return EngagementLevel.HOSTILE
        if engagement >= 70: return EngagementLevel.STRONG
        if engagement >= 45: return EngagementLevel.MODERATE
        if engagement >= 20: return EngagementLevel.WEAK
        return EngagementLevel.NONE

    def _relationship_status(self, inp: StakeholderInput, engagement: float) -> RelationshipStatus:
        if inp.is_blocker or inp.sentiment_score < 0.2:
            return RelationshipStatus.OPPONENT
        if inp.sentiment_score < 0.4:
            return RelationshipStatus.SKEPTIC
        if inp.aligned_with_vendor and inp.is_champion and engagement >= 60:
            return RelationshipStatus.SPONSOR
        if inp.aligned_with_vendor or (inp.is_champion and engagement >= 40):
            return RelationshipStatus.ALLY
        return RelationshipStatus.NEUTRAL

    def _stakeholder_role(self, inp: StakeholderInput) -> StakeholderRole:
        if inp.is_economic_buyer or inp.has_budget_authority:
            return StakeholderRole.ECONOMIC_BUYER
        if inp.is_champion:
            return StakeholderRole.CHAMPION
        if inp.is_technical_buyer:
            return StakeholderRole.TECHNICAL_BUYER
        if inp.is_blocker:
            return StakeholderRole.BLOCKER
        if inp.is_end_user:
            return StakeholderRole.END_USER
        if inp.seniority >= 3:
            return StakeholderRole.INFLUENCER
        return StakeholderRole.UNKNOWN

    def _engagement_gap(self, influence: float, engagement: float) -> float:
        gap = max(0.0, 80.0 - engagement) * (influence / 100.0)
        return round(max(0.0, min(100.0, gap)), 1)

    def _coverage_risk(self, influence: float, engagement: float) -> CoverageRisk:
        if influence >= 70 and engagement < 30:  return CoverageRisk.CRITICAL
        if influence >= 50 and engagement < 50:  return CoverageRisk.AT_RISK
        if engagement < 60:                      return CoverageRisk.PARTIAL
        return CoverageRisk.COVERED

    def _recommended_action(
        self,
        inp: StakeholderInput,
        role: StakeholderRole,
        level: EngagementLevel,
        status: RelationshipStatus,
        risk: CoverageRisk,
        influence: float,
        engagement: float,
    ) -> str:
        if status == RelationshipStatus.OPPONENT:
            return "Neutraliser — identifier les préoccupations et adresser les objections"
        if role == StakeholderRole.ECONOMIC_BUYER and engagement < 50:
            return "Escalade exécutive urgente — aligner sur la valeur business"
        if status == RelationshipStatus.SPONSOR:
            return "Maintenir l'engagement — briefings réguliers et updates exécutifs"
        if role == StakeholderRole.CHAMPION and engagement >= 70:
            return "Activer comme ambassadeur — fournir les outils de conviction"
        if level in (EngagementLevel.HOSTILE, EngagementLevel.NONE) and influence >= 60:
            return "Réengagement prioritaire — approche personnalisée C-level"
        if risk == CoverageRisk.CRITICAL:
            return "Action urgente — engagement direct requis"
        if risk == CoverageRisk.AT_RISK and role == StakeholderRole.ECONOMIC_BUYER:
            return "Planifier réunion stratégique immédiate"
        if status == RelationshipStatus.SKEPTIC:
            return "Adresser les doutes — démonstration de valeur et références clients"
        if status == RelationshipStatus.ALLY:
            return "Renforcer l'alliance — impliquer dans le processus de décision"
        return "Maintenir le contact régulier et partager les updates pertinentes"

    def _recommended_approach(
        self,
        inp: StakeholderInput,
        role: StakeholderRole,
        status: RelationshipStatus,
        level: EngagementLevel,
    ) -> str:
        if role == StakeholderRole.ECONOMIC_BUYER:
            return "Focus ROI et valeur stratégique — présenter le business case chiffré"
        if role == StakeholderRole.CHAMPION:
            return "Co-créer la vision — fournir des arguments et outils pour vendre en interne"
        if role == StakeholderRole.TECHNICAL_BUYER:
            return "Démonstration technique approfondie — répondre aux critères d'évaluation"
        if role == StakeholderRole.BLOCKER:
            return "Discovery des objections — comprendre les craintes et proposer des garanties"
        if status == RelationshipStatus.SKEPTIC:
            return "Partager des références et études de cas similaires — réduire le risque perçu"
        if level == EngagementLevel.STRONG:
            return "Capitaliser sur l'engagement — accélérer vers la décision"
        return "Approche consultative — comprendre les enjeux et proposer de la valeur"

    def _risk_factors(
        self, inp: StakeholderInput, level: EngagementLevel, risk: CoverageRisk
    ) -> list[str]:
        factors: list[str] = []
        if inp.is_blocker:
            factors.append("Blocage actif identifié — peut stopper la décision")
        if inp.last_contact_days > 30:
            factors.append(
                f"Silence prolongé ({inp.last_contact_days}j) — relation en danger"
            )
        if inp.sentiment_score < 0.3:
            factors.append("Sentiment très négatif — risque d'opposition")
        if risk == CoverageRisk.CRITICAL:
            factors.append("Stakeholder clé non engagé — couverture critique")
        if inp.is_economic_buyer and level in (
            EngagementLevel.WEAK, EngagementLevel.NONE, EngagementLevel.HOSTILE
        ):
            factors.append("Décideur budget faiblement engagé — deal en risque")
        if inp.emails_sent > 5 and inp.emails_responded == 0:
            factors.append(
                "Aucune réponse aux emails — revoir l'approche de communication"
            )
        return factors

    def _strengths(
        self, inp: StakeholderInput, level: EngagementLevel, status: RelationshipStatus
    ) -> list[str]:
        st: list[str] = []
        if inp.is_champion:
            st.append("Champion identifié — défenseur interne de la solution")
        if inp.aligned_with_vendor:
            st.append("Alignement confirmé — a exprimé sa préférence pour notre solution")
        if level == EngagementLevel.STRONG:
            st.append(f"Engagement fort — {inp.meetings_held} réunions, activité régulière")
        if status == RelationshipStatus.SPONSOR:
            st.append("Sponsor actif — soutien exécutif acquis")
        if inp.prior_wins > 0:
            st.append(f"Profil gagnant — {inp.prior_wins} victoire(s) avec ce type de persona")
        if inp.sentiment_score > 0.7:
            st.append("Sentiment très positif — forte affinité avec la solution")
        return st

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total": 0,
                "role_counts": {},
                "engagement_counts": {},
                "relationship_counts": {},
                "risk_counts": {},
                "avg_influence_score": 0.0,
                "avg_engagement_gap": 0.0,
                "champions_count": 0,
                "economic_buyers_count": 0,
                "at_risk_count": 0,
                "covered_count": 0,
                "critical_stakeholders_count": 0,
            }

        role_counts: dict[str, int] = {}
        eng_counts:  dict[str, int] = {}
        rel_counts:  dict[str, int] = {}
        risk_counts: dict[str, int] = {}
        total_influence = 0.0
        total_gap       = 0.0

        for r in self._results:
            role_counts[r.stakeholder_role.value]   = role_counts.get(r.stakeholder_role.value, 0) + 1
            eng_counts[r.engagement_level.value]    = eng_counts.get(r.engagement_level.value, 0) + 1
            rel_counts[r.relationship_status.value] = rel_counts.get(r.relationship_status.value, 0) + 1
            risk_counts[r.coverage_risk.value]      = risk_counts.get(r.coverage_risk.value, 0) + 1
            total_influence += r.influence_score
            total_gap       += r.engagement_gap

        return {
            "total":                   n,
            "role_counts":             role_counts,
            "engagement_counts":       eng_counts,
            "relationship_counts":     rel_counts,
            "risk_counts":             risk_counts,
            "avg_influence_score":     round(total_influence / n, 1),
            "avg_engagement_gap":      round(total_gap / n, 1),
            "champions_count":         len(self.champions),
            "economic_buyers_count":   len(self.economic_buyers),
            "at_risk_count":           len(self.at_risk_stakeholders),
            "covered_count":           sum(1 for r in self._results if r.coverage_risk == CoverageRisk.COVERED),
            "critical_stakeholders_count": sum(1 for r in self._results if r.coverage_risk == CoverageRisk.CRITICAL),
        }
