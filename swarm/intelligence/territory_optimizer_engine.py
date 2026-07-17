from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TerritoryHealth(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


class TerritoryAction(str, Enum):
    OPTIMIZE = "optimize"        # territory well-balanced, fine-tune
    EXPAND = "expand"            # growth opportunity, push outbound
    REBALANCE = "rebalance"      # uneven workload or coverage
    RESTRUCTURE = "restructure"  # fundamental territory issues


class CoverageGap(str, Enum):
    NONE = "none"
    MINOR = "minor"
    SIGNIFICANT = "significant"
    CRITICAL = "critical"


class WorkloadBalance(str, Enum):
    BALANCED = "balanced"         # within ±15% of target
    OVERLOADED = "overloaded"     # >30% above target
    UNDERLOADED = "underloaded"   # >30% below target
    SKEWED = "skewed"             # accounts heavily concentrated


@dataclass
class TerritoryInput:
    rep_id: str
    rep_name: str
    region: str
    segment: str
    # Quota & performance
    quota_eur: float
    attainment_pct: float          # YTD attainment 0-100+
    # Territory composition
    total_accounts: int            # accounts in territory
    icp_accounts: int              # ideal customer profile accounts
    active_accounts: int           # engaged in last 90d
    dormant_accounts: int          # no activity in 90d
    whitespace_accounts: int       # uncontacted ICP accounts
    # Workload signals
    avg_accounts_per_rep_target: int   # benchmark
    deals_in_pipeline: int
    avg_deal_size_eur: float
    # Geographic signals
    geographic_concentration_pct: float   # % revenue from top city/region 0-100
    travel_days_per_month: int
    # Market signals
    market_penetration_pct: float     # % of addressable market captured 0-100
    competitor_accounts: int          # known competitor installs in territory
    expansion_signals: int            # accounts showing intent/expansion signals
    # Activity
    outbound_activities_30d: int
    meetings_held_30d: int
    proposals_sent_30d: int


@dataclass
class TerritoryResult:
    rep_id: str
    rep_name: str
    region: str
    segment: str
    quota_eur: float
    territory_health: TerritoryHealth
    territory_action: TerritoryAction
    coverage_gap: CoverageGap
    workload_balance: WorkloadBalance
    territory_score: float           # 0-100
    coverage_pct: float              # active/total accounts
    icp_penetration_pct: float       # active ICP / total ICP
    whitespace_opportunity_eur: float # whitespace_accounts * avg_deal_size
    workload_ratio: float            # total_accounts / target_accounts
    market_penetration_pct: float
    territory_drivers: list[str]     # issues found
    territory_plays: list[str]       # recommended actions
    optimization_score: float        # 0-100, overall optimization level

    def to_dict(self) -> dict:
        return {
            "rep_id": self.rep_id,
            "rep_name": self.rep_name,
            "region": self.region,
            "segment": self.segment,
            "quota_eur": self.quota_eur,
            "territory_health": self.territory_health.value,
            "territory_action": self.territory_action.value,
            "coverage_gap": self.coverage_gap.value,
            "workload_balance": self.workload_balance.value,
            "territory_score": self.territory_score,
            "coverage_pct": self.coverage_pct,
            "icp_penetration_pct": self.icp_penetration_pct,
            "whitespace_opportunity_eur": self.whitespace_opportunity_eur,
            "workload_ratio": self.workload_ratio,
            "market_penetration_pct": self.market_penetration_pct,
            "territory_drivers": self.territory_drivers,
            "territory_plays": self.territory_plays,
            "optimization_score": self.optimization_score,
        }


def _coverage_pct(inp: TerritoryInput) -> float:
    if inp.total_accounts <= 0:
        return 0.0
    return round((inp.active_accounts / inp.total_accounts) * 100.0, 1)


def _icp_penetration_pct(inp: TerritoryInput) -> float:
    if inp.icp_accounts <= 0:
        return 0.0
    return round((min(inp.active_accounts, inp.icp_accounts) / inp.icp_accounts) * 100.0, 1)


def _whitespace_opportunity(inp: TerritoryInput) -> float:
    return round(inp.whitespace_accounts * inp.avg_deal_size_eur, 0)


def _workload_ratio(inp: TerritoryInput) -> float:
    if inp.avg_accounts_per_rep_target <= 0:
        return 1.0
    return round(inp.total_accounts / inp.avg_accounts_per_rep_target, 2)


def _workload_balance(ratio: float) -> WorkloadBalance:
    if ratio > 1.3:
        return WorkloadBalance.OVERLOADED
    if ratio < 0.7:
        return WorkloadBalance.UNDERLOADED
    return WorkloadBalance.BALANCED


def _coverage_gap(coverage: float, icp_pen: float) -> CoverageGap:
    avg = (coverage + icp_pen) / 2.0
    if avg >= 70:
        return CoverageGap.NONE
    if avg >= 50:
        return CoverageGap.MINOR
    if avg >= 30:
        return CoverageGap.SIGNIFICANT
    return CoverageGap.CRITICAL


def _territory_score(inp: TerritoryInput, coverage: float, icp_pen: float, ratio: float) -> float:
    score = 0.0
    # Coverage (30 pts)
    score += min(30.0, coverage * 0.3)
    # ICP penetration (25 pts)
    score += min(25.0, icp_pen * 0.25)
    # Attainment (20 pts)
    score += min(20.0, inp.attainment_pct * 0.2)
    # Workload balance (10 pts)
    if 0.85 <= ratio <= 1.15:
        score += 10.0
    elif 0.7 <= ratio <= 1.3:
        score += 6.0
    elif 0.5 <= ratio <= 1.5:
        score += 3.0
    # Market penetration (10 pts)
    score += min(10.0, inp.market_penetration_pct * 0.2)
    # Activity signals (5 pts)
    score += min(2.5, inp.meetings_held_30d * 0.5)
    score += min(2.5, inp.proposals_sent_30d * 0.5)
    return round(min(100.0, max(0.0, score)), 1)


def _territory_health(score: float) -> TerritoryHealth:
    if score >= 75:
        return TerritoryHealth.EXCELLENT
    if score >= 55:
        return TerritoryHealth.GOOD
    if score >= 35:
        return TerritoryHealth.FAIR
    return TerritoryHealth.POOR


def _territory_action(
    health: TerritoryHealth,
    coverage: CoverageGap,
    balance: WorkloadBalance,
) -> TerritoryAction:
    if health == TerritoryHealth.POOR or coverage == CoverageGap.CRITICAL:
        return TerritoryAction.RESTRUCTURE
    if balance in (WorkloadBalance.OVERLOADED, WorkloadBalance.UNDERLOADED) or coverage == CoverageGap.SIGNIFICANT:
        return TerritoryAction.REBALANCE
    if health == TerritoryHealth.FAIR or coverage == CoverageGap.MINOR:
        return TerritoryAction.EXPAND
    return TerritoryAction.OPTIMIZE


def _optimization_score(inp: TerritoryInput, coverage: float, ratio: float) -> float:
    score = 0.0
    # Whitespace activation (25 pts)
    ws_ratio = 1 - (inp.whitespace_accounts / max(1, inp.icp_accounts))
    score += max(0.0, min(25.0, ws_ratio * 25.0))
    # Geographic balance (20 pts)
    geo_score = max(0.0, (100 - inp.geographic_concentration_pct) * 0.2)
    score += min(20.0, geo_score)
    # Workload optimization (20 pts)
    deviation = abs(ratio - 1.0)
    score += max(0.0, 20.0 - deviation * 30.0)
    # Activity efficiency (20 pts)
    meetings_per_acc = inp.meetings_held_30d / max(1, inp.active_accounts) * 10
    score += min(10.0, meetings_per_acc * 2.0)
    props_per_meeting = inp.proposals_sent_30d / max(1, inp.meetings_held_30d) * 10
    score += min(10.0, props_per_meeting * 5.0)
    # Market capture (15 pts)
    score += min(15.0, inp.market_penetration_pct * 0.3)
    return round(min(100.0, max(0.0, score)), 1)


def _territory_drivers(
    inp: TerritoryInput,
    coverage: float,
    icp_pen: float,
    ratio: float,
    balance: WorkloadBalance,
) -> list[str]:
    drivers: list[str] = []
    if coverage < 40:
        drivers.append(f"Couverture territoire faible — seulement {coverage:.0f}% des comptes actifs")
    if icp_pen < 40:
        drivers.append(f"Pénétration ICP insuffisante — {icp_pen:.0f}% des comptes ICP engagés")
    if inp.whitespace_accounts > inp.icp_accounts * 0.3:
        drivers.append(f"{inp.whitespace_accounts} comptes whitespace non contactés — opportunité non exploitée")
    if balance == WorkloadBalance.OVERLOADED:
        drivers.append(f"Territoire surchargé — {inp.total_accounts} comptes vs. cible {inp.avg_accounts_per_rep_target}")
    if balance == WorkloadBalance.UNDERLOADED:
        drivers.append(f"Territoire sous-chargé — {inp.total_accounts} comptes vs. cible {inp.avg_accounts_per_rep_target}")
    if inp.geographic_concentration_pct > 70:
        drivers.append(f"Concentration géographique excessive — {inp.geographic_concentration_pct:.0f}% du revenu sur une zone")
    if inp.market_penetration_pct < 15:
        drivers.append(f"Pénétration marché faible — {inp.market_penetration_pct:.0f}% du marché adressable capturé")
    if inp.dormant_accounts > inp.active_accounts:
        drivers.append(f"{inp.dormant_accounts} comptes dormants > {inp.active_accounts} comptes actifs — déséquilibre")
    if inp.competitor_accounts > inp.active_accounts * 0.5:
        drivers.append(f"Forte présence concurrentielle — {inp.competitor_accounts} comptes chez la concurrence")
    if inp.outbound_activities_30d < 20:
        drivers.append(f"Activité outbound insuffisante — {inp.outbound_activities_30d} actions sur 30j")
    return drivers


def _territory_plays(
    action: TerritoryAction,
    inp: TerritoryInput,
    coverage: CoverageGap,
) -> list[str]:
    plays: list[str] = []
    if action == TerritoryAction.RESTRUCTURE:
        plays.append("Redécouper le territoire — analyse ICP et potentiel marché par zone")
        plays.append("Rééquilibrer les comptes avec le management — ajustement du portefeuille")
        plays.append("Définir les comptes prioritaires Q1 — focus sur les 20% à plus fort potentiel")
        if inp.whitespace_accounts > 5:
            plays.append("Activer le whitespace — plan d'attaque systématique sur les comptes non contactés")
    elif action == TerritoryAction.REBALANCE:
        plays.append("Rebalancer la charge de travail — identifier les comptes à transférer ou activer")
        plays.append("Prioriser les comptes ICP dormants — campagne de réactivation ciblée")
        plays.append("Optimiser les routes terrain — réduire les déplacements improductifs")
    elif action == TerritoryAction.EXPAND:
        plays.append("Étendre la couverture — 5 nouveaux comptes ICP par semaine")
        plays.append("Intensifier l'outbound sur le whitespace — ABM et séquences personnalisées")
        plays.append("Activer les signaux d'intention — prioriser les comptes avec intent data")
        if inp.expansion_signals > 0:
            plays.append(f"Capitaliser sur les {inp.expansion_signals} signaux expansion détectés")
    else:
        plays.append("Affiner la segmentation — micro-ciblage des comptes à meilleur potentiel")
        plays.append("Chercher des opportunités d'expansion sur les comptes actifs")
        plays.append("Anticiper la couverture du prochain trimestre")
    return plays


class TerritoryOptimizerEngine:
    def __init__(self) -> None:
        self._results: dict[str, TerritoryResult] = {}

    def analyze(self, inp: TerritoryInput) -> TerritoryResult:
        coverage = _coverage_pct(inp)
        icp_pen = _icp_penetration_pct(inp)
        whitespace_opp = _whitespace_opportunity(inp)
        ratio = _workload_ratio(inp)
        balance = _workload_balance(ratio)
        cov_gap = _coverage_gap(coverage, icp_pen)
        score = _territory_score(inp, coverage, icp_pen, ratio)
        health = _territory_health(score)
        action = _territory_action(health, cov_gap, balance)
        opt_score = _optimization_score(inp, coverage, ratio)
        result = TerritoryResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            region=inp.region,
            segment=inp.segment,
            quota_eur=inp.quota_eur,
            territory_health=health,
            territory_action=action,
            coverage_gap=cov_gap,
            workload_balance=balance,
            territory_score=score,
            coverage_pct=coverage,
            icp_penetration_pct=icp_pen,
            whitespace_opportunity_eur=whitespace_opp,
            workload_ratio=ratio,
            market_penetration_pct=inp.market_penetration_pct,
            territory_drivers=_territory_drivers(inp, coverage, icp_pen, ratio, balance),
            territory_plays=_territory_plays(action, inp, cov_gap),
            optimization_score=opt_score,
        )
        self._results[inp.rep_id] = result
        return result

    def analyze_batch(self, reps: list[TerritoryInput]) -> list[TerritoryResult]:
        results = [self.analyze(r) for r in reps]
        return sorted(results, key=lambda r: r.territory_score, reverse=False)

    def all_reps(self) -> list[TerritoryResult]:
        return sorted(self._results.values(), key=lambda r: r.territory_score)

    def by_health(self, health: TerritoryHealth) -> list[TerritoryResult]:
        return [r for r in self._results.values() if r.territory_health == health]

    def by_action(self, action: TerritoryAction) -> list[TerritoryResult]:
        return [r for r in self._results.values() if r.territory_action == action]

    def by_coverage_gap(self, gap: CoverageGap) -> list[TerritoryResult]:
        return [r for r in self._results.values() if r.coverage_gap == gap]

    def poor_territories(self) -> list[TerritoryResult]:
        return self.by_health(TerritoryHealth.POOR)

    def needs_restructure(self) -> list[TerritoryResult]:
        return self.by_action(TerritoryAction.RESTRUCTURE)

    def overloaded_reps(self) -> list[TerritoryResult]:
        return [r for r in self._results.values() if r.workload_balance == WorkloadBalance.OVERLOADED]

    def underloaded_reps(self) -> list[TerritoryResult]:
        return [r for r in self._results.values() if r.workload_balance == WorkloadBalance.UNDERLOADED]

    def excellent_territories(self) -> list[TerritoryResult]:
        return self.by_health(TerritoryHealth.EXCELLENT)

    def total_whitespace_eur(self) -> float:
        return sum(r.whitespace_opportunity_eur for r in self._results.values())

    def avg_territory_score(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.territory_score for r in self._results.values()) / len(self._results), 1)

    def avg_coverage_pct(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.coverage_pct for r in self._results.values()) / len(self._results), 1)

    def avg_optimization_score(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.optimization_score for r in self._results.values()) / len(self._results), 1)

    def summary(self) -> dict:
        all_r = list(self._results.values())
        n = len(all_r)
        return {
            "total": n,
            "health_counts": {h.value: sum(1 for r in all_r if r.territory_health == h) for h in TerritoryHealth},
            "action_counts": {a.value: sum(1 for r in all_r if r.territory_action == a) for a in TerritoryAction},
            "coverage_gap_counts": {g.value: sum(1 for r in all_r if r.coverage_gap == g) for g in CoverageGap},
            "avg_territory_score": self.avg_territory_score(),
            "avg_coverage_pct": self.avg_coverage_pct(),
            "avg_optimization_score": self.avg_optimization_score(),
            "poor_count": len(self.poor_territories()),
            "restructure_count": len(self.needs_restructure()),
            "total_whitespace_eur": self.total_whitespace_eur(),
        }

    def reset(self) -> None:
        self._results.clear()
