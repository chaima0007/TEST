from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class VelocityTier(str, Enum):
    ELITE = "elite"        # top 10% — velocity engine running at full
    HIGH = "high"          # above average — strong momentum
    AVERAGE = "average"    # within normal range
    LOW = "low"            # below average — needs acceleration
    STALLED = "stalled"    # velocity near zero — critical issue


class VelocityAction(str, Enum):
    CELEBRATE = "celebrate"      # elite — replicate the playbook
    ACCELERATE = "accelerate"    # high — push to elite
    OPTIMIZE = "optimize"        # average — target specific lever
    RESCUE = "rescue"            # low — urgent velocity improvement
    RESET = "reset"              # stalled — fundamental change needed


class VelocityDriver(str, Enum):
    OPPORTUNITIES = "opportunities"   # #opps is the constraint
    WIN_RATE = "win_rate"             # conversion is the constraint
    DEAL_SIZE = "deal_size"           # avg value is the constraint
    CYCLE_TIME = "cycle_time"         # speed is the constraint
    BALANCED = "balanced"             # no single dominant constraint


@dataclass
class VelocityInput:
    rep_id: str
    rep_name: str
    region: str
    segment: str
    period_days: int              # measurement period (e.g. 90 for quarter)
    # The 4 velocity levers
    opportunities_created: int    # # new opps in period
    win_rate_pct: float           # historical win rate 0-100
    avg_deal_size_eur: float      # average closed deal value
    avg_sales_cycle_days: int     # average days from open to close
    # Context
    quota_eur: float
    closed_won_eur: float         # actual closed in period
    # Benchmarks (team/segment averages)
    benchmark_opps: int
    benchmark_win_rate_pct: float
    benchmark_deal_size_eur: float
    benchmark_cycle_days: int
    # Pipeline signals
    pipeline_total_eur: float
    deals_advancing_pct: float    # % of deals advancing stage in last 30d (0-100)
    avg_days_in_stage: float      # average days deals sit in current stage
    # Activity
    outreach_activities_30d: int
    connect_rate_pct: float       # % outreach that got a response 0-100


@dataclass
class VelocityResult:
    rep_id: str
    rep_name: str
    region: str
    segment: str
    velocity_eur_per_day: float    # main metric: EUR/day
    velocity_tier: VelocityTier
    velocity_action: VelocityAction
    primary_driver: VelocityDriver
    velocity_score: float          # 0-100 composite
    opportunity_index: float       # rep/benchmark ratio
    win_rate_index: float
    deal_size_index: float
    cycle_time_index: float        # inverted: higher = faster
    quota_attainment_pct: float
    projected_arr_eur: float       # extrapolated to 365 days
    velocity_gaps: list[str]       # what's dragging velocity
    velocity_levers: list[str]     # how to improve
    benchmark_velocity_eur_per_day: float

    def to_dict(self) -> dict:
        return {
            "rep_id": self.rep_id,
            "rep_name": self.rep_name,
            "region": self.region,
            "segment": self.segment,
            "velocity_eur_per_day": self.velocity_eur_per_day,
            "velocity_tier": self.velocity_tier.value,
            "velocity_action": self.velocity_action.value,
            "primary_driver": self.primary_driver.value,
            "velocity_score": self.velocity_score,
            "opportunity_index": self.opportunity_index,
            "win_rate_index": self.win_rate_index,
            "deal_size_index": self.deal_size_index,
            "cycle_time_index": self.cycle_time_index,
            "quota_attainment_pct": self.quota_attainment_pct,
            "projected_arr_eur": self.projected_arr_eur,
            "velocity_gaps": self.velocity_gaps,
            "velocity_levers": self.velocity_levers,
            "benchmark_velocity_eur_per_day": self.benchmark_velocity_eur_per_day,
        }


def _velocity_eur_per_day(inp: VelocityInput) -> float:
    if inp.period_days <= 0:
        return 0.0
    return round(inp.closed_won_eur / inp.period_days, 2)


def _benchmark_velocity(inp: VelocityInput) -> float:
    if inp.benchmark_cycle_days <= 0 or inp.period_days <= 0:
        return 0.0
    bench = (
        inp.benchmark_opps
        * (inp.benchmark_win_rate_pct / 100.0)
        * inp.benchmark_deal_size_eur
        / inp.benchmark_cycle_days
    )
    return round(bench, 2)


def _opportunity_index(inp: VelocityInput) -> float:
    if inp.benchmark_opps <= 0:
        return 1.0
    return round(inp.opportunities_created / inp.benchmark_opps, 2)


def _win_rate_index(inp: VelocityInput) -> float:
    if inp.benchmark_win_rate_pct <= 0:
        return 1.0
    return round(inp.win_rate_pct / inp.benchmark_win_rate_pct, 2)


def _deal_size_index(inp: VelocityInput) -> float:
    if inp.benchmark_deal_size_eur <= 0:
        return 1.0
    return round(inp.avg_deal_size_eur / inp.benchmark_deal_size_eur, 2)


def _cycle_time_index(inp: VelocityInput) -> float:
    if inp.avg_sales_cycle_days <= 0:
        return 2.0
    if inp.benchmark_cycle_days <= 0:
        return 1.0
    # Inverted: faster cycle → higher index
    return round(inp.benchmark_cycle_days / inp.avg_sales_cycle_days, 2)


def _primary_driver(opp: float, wr: float, ds: float, ct: float) -> VelocityDriver:
    indices = {
        VelocityDriver.OPPORTUNITIES: opp,
        VelocityDriver.WIN_RATE: wr,
        VelocityDriver.DEAL_SIZE: ds,
        VelocityDriver.CYCLE_TIME: ct,
    }
    min_val = min(indices.values())
    max_val = max(indices.values())
    # If spread is small, balanced
    if max_val - min_val < 0.2:
        return VelocityDriver.BALANCED
    min_driver = min(indices, key=indices.get)  # type: ignore[arg-type]
    return min_driver


def _quota_attainment_pct(inp: VelocityInput) -> float:
    if inp.quota_eur <= 0:
        return 0.0
    return round((inp.closed_won_eur / inp.quota_eur) * 100.0, 1)


def _projected_arr_eur(velocity: float) -> float:
    return round(velocity * 365, 0)


def _velocity_score(opp: float, wr: float, ds: float, ct: float, att: float) -> float:
    # Each index normalized to 0-25pts, attainment 0-25pts
    def idx_pts(v: float) -> float:
        return min(25.0, v * 25.0)
    score = idx_pts(opp) + idx_pts(wr) + idx_pts(ds) + idx_pts(ct)
    score += min(25.0, att * 0.25)
    # Bonus for being above benchmark on all 4 levers
    if opp >= 1 and wr >= 1 and ds >= 1 and ct >= 1:
        score = min(100.0, score + 5.0)
    return round(min(100.0, max(0.0, score)), 1)


def _velocity_tier(score: float) -> VelocityTier:
    if score >= 85:
        return VelocityTier.ELITE
    if score >= 65:
        return VelocityTier.HIGH
    if score >= 45:
        return VelocityTier.AVERAGE
    if score >= 25:
        return VelocityTier.LOW
    return VelocityTier.STALLED


def _velocity_action(tier: VelocityTier) -> VelocityAction:
    mapping = {
        VelocityTier.ELITE: VelocityAction.CELEBRATE,
        VelocityTier.HIGH: VelocityAction.ACCELERATE,
        VelocityTier.AVERAGE: VelocityAction.OPTIMIZE,
        VelocityTier.LOW: VelocityAction.RESCUE,
        VelocityTier.STALLED: VelocityAction.RESET,
    }
    return mapping[tier]


def _velocity_gaps(
    inp: VelocityInput,
    opp: float, wr: float, ds: float, ct: float,
) -> list[str]:
    gaps: list[str] = []
    if opp < 0.8:
        gaps.append(
            f"Volume d'opportunités faible — {inp.opportunities_created} vs. benchmark {inp.benchmark_opps} "
            f"({opp:.1f}x)"
        )
    if wr < 0.8:
        gaps.append(
            f"Taux de signature sous benchmark — {inp.win_rate_pct:.0f}% vs. {inp.benchmark_win_rate_pct:.0f}% "
            f"({wr:.1f}x)"
        )
    if ds < 0.8:
        gaps.append(
            f"Taille moyenne des deals faible — {inp.avg_deal_size_eur:,.0f}€ vs. {inp.benchmark_deal_size_eur:,.0f}€ "
            f"({ds:.1f}x)"
        )
    if ct < 0.8:
        gaps.append(
            f"Cycle de vente trop long — {inp.avg_sales_cycle_days}j vs. benchmark {inp.benchmark_cycle_days}j "
            f"(CT index: {ct:.1f}x)"
        )
    if inp.deals_advancing_pct < 40:
        gaps.append(
            f"Pipeline stagnant — seulement {inp.deals_advancing_pct:.0f}% des deals avancent par mois"
        )
    if inp.connect_rate_pct < 20:
        gaps.append(
            f"Taux de connexion outreach faible — {inp.connect_rate_pct:.0f}% de réponse"
        )
    if inp.avg_days_in_stage > inp.avg_sales_cycle_days * 0.5:
        gaps.append(
            f"Deals bloqués en stage — moyenne {inp.avg_days_in_stage:.0f}j sans progression"
        )
    return gaps


def _velocity_levers(
    inp: VelocityInput,
    action: VelocityAction,
    driver: VelocityDriver,
    opp: float, wr: float, ds: float, ct: float,
) -> list[str]:
    levers: list[str] = []
    if action == VelocityAction.RESET:
        levers.append("Audit complet du pipeline — identifier et éliminer les deals fantômes")
        levers.append("Reboot outbound — nouvelles séquences, nouvelles cibles ICP")
        levers.append("Session de coaching intensif — refonte du pitch et des objections")
        levers.append("Définir un plan 30j avec des jalons clairs et mesurables")
    elif action == VelocityAction.RESCUE:
        if driver == VelocityDriver.OPPORTUNITIES:
            levers.append("Intensifier la prospection — doubler le volume d'outreach cette semaine")
        if driver == VelocityDriver.WIN_RATE:
            levers.append("Requalifier les deals en pipeline — éliminer les deals à faible probabilité")
            levers.append("Travailler le closing — techniques de négociation et gestion des objections")
        if driver == VelocityDriver.DEAL_SIZE:
            levers.append("Upscaler le ciblage — prioriser les comptes avec un potentiel ARR ≥ benchmark")
        if driver == VelocityDriver.CYCLE_TIME:
            levers.append("Identifier les blocages par stage — plan d'action pour chaque deal stagnant")
        levers.append("Hebdo velocity check avec le manager — suivi des 4 leviers")
    elif action == VelocityAction.OPTIMIZE:
        if opp < 1:
            levers.append("Augmenter le volume d'opportunités — 3 nouveaux comptes par semaine")
        if wr < 1:
            levers.append("Améliorer le taux de conversion — revoir le process de qualification")
        if ds < 1:
            levers.append("Augmenter la valeur moyenne — stratégie multi-produit et upsell")
        if ct < 1:
            levers.append("Accélérer le cycle — réduire les délais inter-stages")
        levers.append("Analyser les deals gagnés récents — répliquer les patterns de succès")
    elif action == VelocityAction.ACCELERATE:
        levers.append("Capitaliser sur le momentum — augmenter le volume d'activité de 20%")
        levers.append("Chercher des opportunités de multi-threading — élargir les contacts clés")
        if inp.pipeline_total_eur > 0:
            levers.append("Accélérer les deals closing stage — revue pipeline hebdomadaire")
    else:
        levers.append("Documenter le playbook — partager les best practices avec l'équipe")
        levers.append("Mentorer les reps en dessous de la moyenne — partage de compétences")
        levers.append("Chercher à battre les benchmarks sur le levier le plus faible")
    return levers


class SalesVelocityEngine:
    def __init__(self) -> None:
        self._results: dict[str, VelocityResult] = {}

    def analyze(self, inp: VelocityInput) -> VelocityResult:
        velocity = _velocity_eur_per_day(inp)
        bench_v = _benchmark_velocity(inp)
        opp = _opportunity_index(inp)
        wr = _win_rate_index(inp)
        ds = _deal_size_index(inp)
        ct = _cycle_time_index(inp)
        driver = _primary_driver(opp, wr, ds, ct)
        att = _quota_attainment_pct(inp)
        score = _velocity_score(opp, wr, ds, ct, att)
        tier = _velocity_tier(score)
        action = _velocity_action(tier)
        projected = _projected_arr_eur(velocity)
        result = VelocityResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            region=inp.region,
            segment=inp.segment,
            velocity_eur_per_day=velocity,
            velocity_tier=tier,
            velocity_action=action,
            primary_driver=driver,
            velocity_score=score,
            opportunity_index=opp,
            win_rate_index=wr,
            deal_size_index=ds,
            cycle_time_index=ct,
            quota_attainment_pct=att,
            projected_arr_eur=projected,
            velocity_gaps=_velocity_gaps(inp, opp, wr, ds, ct),
            velocity_levers=_velocity_levers(inp, action, driver, opp, wr, ds, ct),
            benchmark_velocity_eur_per_day=bench_v,
        )
        self._results[inp.rep_id] = result
        return result

    def analyze_batch(self, reps: list[VelocityInput]) -> list[VelocityResult]:
        results = [self.analyze(r) for r in reps]
        return sorted(results, key=lambda r: r.velocity_eur_per_day, reverse=True)

    def all_reps(self) -> list[VelocityResult]:
        return sorted(self._results.values(), key=lambda r: r.velocity_eur_per_day, reverse=True)

    def by_tier(self, tier: VelocityTier) -> list[VelocityResult]:
        return [r for r in self._results.values() if r.velocity_tier == tier]

    def by_action(self, action: VelocityAction) -> list[VelocityResult]:
        return [r for r in self._results.values() if r.velocity_action == action]

    def by_driver(self, driver: VelocityDriver) -> list[VelocityResult]:
        return [r for r in self._results.values() if r.primary_driver == driver]

    def elite_reps(self) -> list[VelocityResult]:
        return self.by_tier(VelocityTier.ELITE)

    def stalled_reps(self) -> list[VelocityResult]:
        return self.by_tier(VelocityTier.STALLED)

    def needs_reset(self) -> list[VelocityResult]:
        return self.by_action(VelocityAction.RESET)

    def at_risk_reps(self) -> list[VelocityResult]:
        return [
            r for r in self._results.values()
            if r.velocity_tier in (VelocityTier.LOW, VelocityTier.STALLED)
        ]

    def avg_velocity(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.velocity_eur_per_day for r in self._results.values()) / len(self._results), 2)

    def avg_velocity_score(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.velocity_score for r in self._results.values()) / len(self._results), 1)

    def total_projected_arr_eur(self) -> float:
        return sum(r.projected_arr_eur for r in self._results.values())

    def top_velocity_rep(self) -> VelocityResult | None:
        if not self._results:
            return None
        return max(self._results.values(), key=lambda r: r.velocity_eur_per_day)

    def constraint_distribution(self) -> dict[str, int]:
        return {d.value: sum(1 for r in self._results.values() if r.primary_driver == d) for d in VelocityDriver}

    def summary(self) -> dict:
        all_r = list(self._results.values())
        n = len(all_r)
        return {
            "total": n,
            "tier_counts": {t.value: sum(1 for r in all_r if r.velocity_tier == t) for t in VelocityTier},
            "action_counts": {a.value: sum(1 for r in all_r if r.velocity_action == a) for a in VelocityAction},
            "driver_counts": self.constraint_distribution(),
            "avg_velocity_eur_per_day": self.avg_velocity(),
            "avg_velocity_score": self.avg_velocity_score(),
            "elite_count": len(self.elite_reps()),
            "stalled_count": len(self.stalled_reps()),
            "total_projected_arr_eur": self.total_projected_arr_eur(),
        }

    def reset(self) -> None:
        self._results.clear()
