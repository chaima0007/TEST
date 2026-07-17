"""Sales Territory Optimizer — balances territory assignments to maximize coverage, fairness, and pipeline potential."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional


class TerritoryHealth(str, Enum):
    OPTIMAL = "optimal"         # balance_score >= 80
    BALANCED = "balanced"       # balance_score >= 60
    IMBALANCED = "imbalanced"   # balance_score >= 35
    CRITICAL = "critical"       # balance_score < 35


class TerritoryAction(str, Enum):
    MAINTAIN = "maintain"           # healthy, no changes needed
    REBALANCE = "rebalance"         # accounts should be redistributed
    HIRE = "hire"                   # territory is too large for one rep
    SPLIT = "split"                 # territory should be divided into two
    MERGE = "merge"                 # territory is too small, consolidate with neighbor


class CoverageRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class TerritoryInput:
    territory_id: str
    territory_name: str
    region: str                     # emea / amer / apac
    rep_name: str
    rep_tenure_months: int          # how long the rep has been on the territory

    # Volume & pipeline
    total_accounts: int
    active_accounts: int            # accounts with activity in last 90d
    total_pipeline_eur: float
    weighted_pipeline_eur: float
    closed_won_ytd_eur: float
    quota_eur: float

    # Engagement
    avg_account_health: float       # 0-100, avg health score across accounts
    accounts_with_qbr_pct: float    # 0-100, % of accounts with QBR in last 90d
    accounts_at_risk_count: int     # accounts flagged at-risk
    white_space_accounts: int       # untouched / uncontacted accounts

    # Rep capacity signals
    avg_deal_cycle_days: int
    deals_in_flight: int            # active open deals
    rep_quota_attainment_pct: float # 0-200+, current quota attainment
    rep_ramp_complete: bool         # whether rep is fully ramped

    # Market signals
    tam_eur: float                  # total addressable market in territory
    market_penetration_pct: float   # 0-100, how much of TAM is captured
    competitive_intensity: float    # 0-100, competitor presence


@dataclass
class TerritoryResult:
    territory_id: str
    territory_name: str
    region: str
    rep_name: str

    territory_health: TerritoryHealth
    territory_action: TerritoryAction
    coverage_risk: CoverageRisk
    balance_score: float            # 0-100

    quota_attainment_pct: float
    pipeline_coverage_ratio: float  # weighted_pipeline / quota
    white_space_pct: float          # white_space / total_accounts * 100

    strengths: list[str]
    gaps: list[str]
    recommendations: list[str]
    territory_kpis: dict

    def to_dict(self) -> dict:
        d = asdict(self)
        d["territory_health"] = self.territory_health.value
        d["territory_action"] = self.territory_action.value
        d["coverage_risk"] = self.coverage_risk.value
        return d


# ─── Scoring helpers ──────────────────────────────────────────────────────────

def _pipeline_coverage(inp: TerritoryInput) -> float:
    if inp.quota_eur <= 0:
        return 0.0
    return round(inp.weighted_pipeline_eur / inp.quota_eur, 2)

def _white_space_pct(inp: TerritoryInput) -> float:
    if inp.total_accounts <= 0:
        return 0.0
    return round(inp.white_space_accounts / inp.total_accounts * 100, 1)

def _balance_score(inp: TerritoryInput) -> float:
    score = 0.0

    # Pipeline coverage (0-30 pts): ideal 3-5x coverage
    pc = _pipeline_coverage(inp)
    if pc >= 3.0:
        score += 30.0
    elif pc >= 2.0:
        score += 22.0
    elif pc >= 1.5:
        score += 14.0
    elif pc >= 1.0:
        score += 8.0
    else:
        score += 0.0

    # Account health (0-20 pts)
    score += min(20.0, inp.avg_account_health * 0.20)

    # QBR coverage (0-15 pts)
    score += min(15.0, inp.accounts_with_qbr_pct * 0.15)

    # Quota attainment signal (0-20 pts)
    att = inp.rep_quota_attainment_pct
    if att >= 100:
        score += 20.0
    elif att >= 75:
        score += 15.0
    elif att >= 50:
        score += 8.0
    else:
        score += 0.0

    # White space exploitation (0-15 pts): low white space = better (already covered)
    ws = _white_space_pct(inp)
    if ws <= 10:
        score += 15.0
    elif ws <= 25:
        score += 10.0
    elif ws <= 40:
        score += 5.0
    else:
        score += 0.0

    return round(max(0.0, min(100.0, score)), 1)


def _territory_health(score: float) -> TerritoryHealth:
    if score >= 80:
        return TerritoryHealth.OPTIMAL
    if score >= 60:
        return TerritoryHealth.BALANCED
    if score >= 35:
        return TerritoryHealth.IMBALANCED
    return TerritoryHealth.CRITICAL


def _coverage_risk(inp: TerritoryInput, ws_pct: float) -> CoverageRisk:
    risk_score = 0
    if ws_pct > 40:
        risk_score += 2
    elif ws_pct > 25:
        risk_score += 1
    if inp.accounts_at_risk_count > 5:
        risk_score += 2
    elif inp.accounts_at_risk_count > 2:
        risk_score += 1
    if inp.accounts_with_qbr_pct < 30:
        risk_score += 2
    elif inp.accounts_with_qbr_pct < 50:
        risk_score += 1
    if not inp.rep_ramp_complete:
        risk_score += 2

    if risk_score >= 5:
        return CoverageRisk.CRITICAL
    if risk_score >= 3:
        return CoverageRisk.HIGH
    if risk_score >= 1:
        return CoverageRisk.MEDIUM
    return CoverageRisk.LOW


def _territory_action(
    inp: TerritoryInput,
    health: TerritoryHealth,
    coverage: CoverageRisk,
    pc: float,
    ws_pct: float,
) -> TerritoryAction:
    if health == TerritoryHealth.OPTIMAL and coverage == CoverageRisk.LOW:
        return TerritoryAction.MAINTAIN
    if inp.total_accounts > 150 and pc < 2.0:
        return TerritoryAction.SPLIT
    if inp.total_accounts > 100 and (coverage == CoverageRisk.CRITICAL or health == TerritoryHealth.CRITICAL):
        return TerritoryAction.HIRE
    if health in (TerritoryHealth.CRITICAL, TerritoryHealth.IMBALANCED):
        return TerritoryAction.REBALANCE
    if inp.total_accounts < 20 and inp.quota_eur < 200000:
        return TerritoryAction.MERGE
    if health == TerritoryHealth.BALANCED and coverage in (CoverageRisk.HIGH, CoverageRisk.CRITICAL):
        return TerritoryAction.REBALANCE
    return TerritoryAction.MAINTAIN


def _build_strengths(inp: TerritoryInput, pc: float, ws_pct: float) -> list[str]:
    out: list[str] = []
    if pc >= 3.0:
        out.append(f"Couverture pipeline excellente — {pc:.1f}x le quota")
    elif pc >= 2.0:
        out.append(f"Bonne couverture pipeline — {pc:.1f}x le quota")
    if inp.rep_quota_attainment_pct >= 100:
        out.append(f"Atteinte quota à {inp.rep_quota_attainment_pct:.0f}% — performance commerciale au niveau")
    elif inp.rep_quota_attainment_pct >= 75:
        out.append(f"Progression quota solide — {inp.rep_quota_attainment_pct:.0f}% d'atteinte")
    if inp.avg_account_health >= 70:
        out.append(f"Santé comptes élevée ({inp.avg_account_health:.0f}/100) — portefeuille stable")
    if ws_pct <= 15:
        out.append(f"Excellent taux de pénétration — seulement {ws_pct:.0f}% de comptes vierges")
    if inp.accounts_with_qbr_pct >= 70:
        out.append(f"Cadence QBR forte — {inp.accounts_with_qbr_pct:.0f}% des comptes suivis")
    if inp.market_penetration_pct >= 40:
        out.append(f"Pénétration marché significative — {inp.market_penetration_pct:.0f}% du TAM capturé")
    if inp.rep_tenure_months >= 18:
        out.append(f"Rep expérimenté — {inp.rep_tenure_months} mois sur le territoire, connaissance approfondie")
    return out


def _build_gaps(inp: TerritoryInput, pc: float, ws_pct: float, health: TerritoryHealth) -> list[str]:
    gaps: list[str] = []
    if pc < 1.5:
        gaps.append(f"Pipeline insuffisant — seulement {pc:.1f}x le quota (objectif ≥ 3x)")
    if ws_pct > 30:
        gaps.append(f"{ws_pct:.0f}% de comptes non couverts — potentiel commercial inexploité")
    if inp.accounts_with_qbr_pct < 40:
        gaps.append(f"Cadence QBR faible ({inp.accounts_with_qbr_pct:.0f}%) — risque de décrochage clients")
    if inp.accounts_at_risk_count > 3:
        gaps.append(f"{inp.accounts_at_risk_count} comptes à risque — ARR exposé à identifier")
    if inp.rep_quota_attainment_pct < 50:
        gaps.append(f"Atteinte quota à {inp.rep_quota_attainment_pct:.0f}% — sous-performance critique")
    if not inp.rep_ramp_complete:
        gaps.append("Rep en cours de ramp — pleine capacité pas encore atteinte")
    if inp.market_penetration_pct < 15:
        gaps.append(f"Faible pénétration marché ({inp.market_penetration_pct:.0f}%) — TAM largement inexploité")
    if inp.competitive_intensity > 70:
        gaps.append(f"Pression concurrentielle forte ({inp.competitive_intensity:.0f}/100) — perte de comptes risquée")
    if inp.total_accounts > 130:
        gaps.append(f"Territoire surchargé — {inp.total_accounts} comptes difficiles à couvrir correctement")
    return gaps


def _build_recommendations(
    inp: TerritoryInput,
    action: TerritoryAction,
    ws_pct: float,
    pc: float,
) -> list[str]:
    recs: list[str] = []

    if action == TerritoryAction.SPLIT:
        recs.append(f"Diviser le territoire — {inp.total_accounts} comptes dépasse la capacité d'un seul rep")
        recs.append("Prioriser la division par verticale ou géographie pour minimiser la disruption")

    elif action == TerritoryAction.HIRE:
        recs.append("Recruter un rep additionnel — charge de travail actuelle dépasse la capacité")
        recs.append("Définir les critères de partage du territoire avant l'embauche")

    elif action == TerritoryAction.MERGE:
        recs.append(f"Fusionner avec un territoire adjacent — {inp.total_accounts} comptes insuffisants pour justifier un rep dédié")

    elif action == TerritoryAction.REBALANCE:
        recs.append("Rebalancer la couverture — prioriser les comptes à fort potentiel non couverts")
        if ws_pct > 25:
            recs.append(f"Lancer une campagne de prospection sur les {inp.white_space_accounts} comptes vierges")

    if pc < 2.0:
        recs.append(f"Accélérer la génération pipeline — objectif couverture 3x quota (actuellement {pc:.1f}x)")
    if inp.accounts_with_qbr_pct < 50:
        recs.append("Planifier des QBRs pour les comptes sans revue depuis 90j+")
    if inp.accounts_at_risk_count > 2:
        recs.append(f"Déployer une intervention CS sur les {inp.accounts_at_risk_count} comptes à risque")
    if inp.market_penetration_pct < 20 and inp.tam_eur > 0:
        recs.append(f"Cartographier le TAM résiduel — {inp.market_penetration_pct:.0f}% de pénétration laisse {100-inp.market_penetration_pct:.0f}% d'opportunités")
    if not inp.rep_ramp_complete:
        recs.append("Accélérer le ramp — buddy system avec un rep senior pour montée en puissance")

    return recs


def _territory_kpis(inp: TerritoryInput, pc: float, ws_pct: float) -> dict:
    return {
        "pipeline_coverage_ratio": pc,
        "quota_attainment_pct": round(inp.rep_quota_attainment_pct, 1),
        "white_space_pct": ws_pct,
        "active_account_pct": round(inp.active_accounts / max(1, inp.total_accounts) * 100, 1),
        "avg_account_health": round(inp.avg_account_health, 1),
        "qbr_coverage_pct": round(inp.accounts_with_qbr_pct, 1),
        "market_penetration_pct": round(inp.market_penetration_pct, 1),
        "deals_in_flight": inp.deals_in_flight,
        "accounts_at_risk": inp.accounts_at_risk_count,
        "closed_won_ytd_eur": inp.closed_won_ytd_eur,
    }


class TerritoryOptimizerEngine:
    """Analyzes and optimizes sales territory assignments."""

    def __init__(self) -> None:
        self._results: dict[str, TerritoryResult] = {}

    def analyze(self, inp: TerritoryInput) -> TerritoryResult:
        pc = _pipeline_coverage(inp)
        ws = _white_space_pct(inp)
        score = _balance_score(inp)
        health = _territory_health(score)
        risk = _coverage_risk(inp, ws)
        action = _territory_action(inp, health, risk, pc, ws)
        strengths = _build_strengths(inp, pc, ws)
        gaps = _build_gaps(inp, pc, ws, health)
        recs = _build_recommendations(inp, action, ws, pc)
        kpis = _territory_kpis(inp, pc, ws)

        result = TerritoryResult(
            territory_id=inp.territory_id,
            territory_name=inp.territory_name,
            region=inp.region,
            rep_name=inp.rep_name,
            territory_health=health,
            territory_action=action,
            coverage_risk=risk,
            balance_score=score,
            quota_attainment_pct=round(inp.rep_quota_attainment_pct, 1),
            pipeline_coverage_ratio=pc,
            white_space_pct=ws,
            strengths=strengths,
            gaps=gaps,
            recommendations=recs,
            territory_kpis=kpis,
        )
        self._results[inp.territory_id] = result
        return result

    def analyze_batch(self, inputs: list[TerritoryInput]) -> list[TerritoryResult]:
        return sorted(
            [self.analyze(inp) for inp in inputs],
            key=lambda r: r.balance_score,
            reverse=True,
        )

    def get(self, territory_id: str) -> Optional[TerritoryResult]:
        return self._results.get(territory_id)

    def all_territories(self) -> list[TerritoryResult]:
        return sorted(self._results.values(), key=lambda r: r.balance_score, reverse=True)

    def by_health(self, health: TerritoryHealth) -> list[TerritoryResult]:
        return [r for r in self.all_territories() if r.territory_health == health]

    def by_action(self, action: TerritoryAction) -> list[TerritoryResult]:
        return [r for r in self.all_territories() if r.territory_action == action]

    def by_region(self, region: str) -> list[TerritoryResult]:
        return [r for r in self.all_territories() if r.region == region]

    def needs_rebalance(self) -> list[TerritoryResult]:
        return [r for r in self.all_territories()
                if r.territory_action in (TerritoryAction.REBALANCE, TerritoryAction.SPLIT, TerritoryAction.HIRE)]

    def optimal(self) -> list[TerritoryResult]:
        return self.by_health(TerritoryHealth.OPTIMAL)

    def critical(self) -> list[TerritoryResult]:
        return self.by_health(TerritoryHealth.CRITICAL)

    def total_pipeline_eur(self) -> float:
        return round(sum(r.territory_kpis.get("closed_won_ytd_eur", 0) for r in self._results.values()), 2)

    def avg_balance_score(self) -> float:
        vals = list(self._results.values())
        if not vals:
            return 0.0
        return round(sum(r.balance_score for r in vals) / len(vals), 1)

    def avg_quota_attainment(self) -> float:
        vals = list(self._results.values())
        if not vals:
            return 0.0
        return round(sum(r.quota_attainment_pct for r in vals) / len(vals), 1)

    def summary(self) -> dict:
        all_r = list(self._results.values())
        if not all_r:
            return {
                "total": 0,
                "health_counts": {},
                "action_counts": {},
                "risk_counts": {},
                "avg_balance_score": 0.0,
                "avg_quota_attainment_pct": 0.0,
                "needs_rebalance_count": 0,
                "optimal_count": 0,
                "critical_count": 0,
            }
        health_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        risk_counts: dict[str, int] = {}
        for r in all_r:
            health_counts[r.territory_health.value] = health_counts.get(r.territory_health.value, 0) + 1
            action_counts[r.territory_action.value] = action_counts.get(r.territory_action.value, 0) + 1
            risk_counts[r.coverage_risk.value] = risk_counts.get(r.coverage_risk.value, 0) + 1
        return {
            "total": len(all_r),
            "health_counts": health_counts,
            "action_counts": action_counts,
            "risk_counts": risk_counts,
            "avg_balance_score": self.avg_balance_score(),
            "avg_quota_attainment_pct": self.avg_quota_attainment(),
            "needs_rebalance_count": len(self.needs_rebalance()),
            "optimal_count": len(self.optimal()),
            "critical_count": len(self.critical()),
        }

    def reset(self) -> None:
        self._results.clear()
