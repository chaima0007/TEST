from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ChampionStatus(str, Enum):
    ACTIVE_ADVOCATE     = "active_advocate"
    ENGAGED             = "engaged"
    COOLING             = "cooling"
    SILENT              = "silent"
    DEPARTED            = "departed"


class ChampionRisk(str, Enum):
    LOW         = "low"
    MODERATE    = "moderate"
    HIGH        = "high"
    CRITICAL    = "critical"


class InfluenceLevel(str, Enum):
    HIGH_INFLUENCE  = "high_influence"
    MODERATE_INFLUENCE = "moderate_influence"
    LOW_INFLUENCE   = "low_influence"
    UNKNOWN         = "unknown"


class ChampionAction(str, Enum):
    MAINTAIN            = "maintain"
    RE_ENGAGE           = "re_engage"
    FIND_BACKUP         = "find_backup"
    ESCALATE_EXEC       = "escalate_exec"


@dataclass
class ChampionRiskInput:
    deal_id:                        str
    deal_name:                      str
    rep_id:                         str
    champion_name:                  str
    days_since_champion_contact:    int     # days since last contact with champion
    champion_reply_rate_pct:        float   # % of outreach champion replies to (0-100)
    champion_meetings_last_30d:     int     # meetings attended by champion last 30 days
    champion_meetings_prior_30d:    int     # meetings attended by champion prior 30 days
    champion_intro_count:           int     # # of internal intros champion made (execs, IT, legal)
    champion_created_internal_urgency: int  # 1 if champion pushed for internal deadline
    champion_job_change_signal:     int     # 1 if LinkedIn/signals suggest job change
    champion_promotion_signal:      int     # 1 if champion was recently promoted (risk of scope change)
    champion_title_level:           int     # 1=IC, 2=manager, 3=director, 4=VP, 5=C-level
    champion_budget_authority:      int     # 1 if champion controls budget
    backup_champion_identified:     int     # 1 if a backup champion exists
    deal_stage_numeric:             int     # 1-6, current deal stage
    deal_size_usd:                  float
    days_to_close:                  int     # remaining days to close date
    executive_relationship_score:   float   # 0-100, how strong is exec relationship in acct
    multi_threaded_contacts:        int     # total contacts engaged in the deal
    last_positive_signal_days_ago:  int     # days since last positive buying signal
    deal_age_days:                  int     # total age of deal


@dataclass
class ChampionRiskResult:
    deal_id:                str
    deal_name:              str
    champion_status:        ChampionStatus
    champion_risk:          ChampionRisk
    influence_level:        InfluenceLevel
    champion_action:        ChampionAction
    engagement_score:       float   # 0-100
    influence_score:        float   # 0-100
    stability_score:        float   # 0-100
    deal_protection_score:  float   # 0-100
    champion_composite:     float   # 0-100
    departure_probability:  float   # 0-100
    deal_at_risk_score:     float   # 0-100 (deal risk from champion issues)
    is_champion_stable:     bool
    needs_backup_champion:  bool

    def to_dict(self) -> dict:
        return {
            "deal_id":                  self.deal_id,
            "deal_name":                self.deal_name,
            "champion_status":          self.champion_status.value,
            "champion_risk":            self.champion_risk.value,
            "influence_level":          self.influence_level.value,
            "champion_action":          self.champion_action.value,
            "engagement_score":         self.engagement_score,
            "influence_score":          self.influence_score,
            "stability_score":          self.stability_score,
            "deal_protection_score":    self.deal_protection_score,
            "champion_composite":       self.champion_composite,
            "departure_probability":    self.departure_probability,
            "deal_at_risk_score":       self.deal_at_risk_score,
            "is_champion_stable":       self.is_champion_stable,
            "needs_backup_champion":    self.needs_backup_champion,
        }


class ChampionRiskMonitor:
    def __init__(self) -> None:
        self._results: list[ChampionRiskResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def monitor(self, inp: ChampionRiskInput) -> ChampionRiskResult:
        engagement  = self._engagement_score(inp)
        influence   = self._influence_score(inp)
        stability   = self._stability_score(inp)
        protection  = self._deal_protection_score(inp)
        composite   = self._composite(engagement, influence, stability, protection)
        status      = self._champion_status(inp, composite)
        risk        = self._champion_risk(composite, inp)
        infl_level  = self._influence_level(inp)
        depart_prob = self._departure_probability(inp)
        deal_risk   = self._deal_at_risk_score(inp, composite)
        is_stable   = composite >= 55 and inp.champion_job_change_signal == 0
        needs_backup = (
            inp.backup_champion_identified == 0
            and (composite < 40 or inp.champion_job_change_signal == 1)
        )
        action = self._champion_action(risk, needs_backup, inp)

        result = ChampionRiskResult(
            deal_id=inp.deal_id,
            deal_name=inp.deal_name,
            champion_status=status,
            champion_risk=risk,
            influence_level=infl_level,
            champion_action=action,
            engagement_score=engagement,
            influence_score=influence,
            stability_score=stability,
            deal_protection_score=protection,
            champion_composite=composite,
            departure_probability=depart_prob,
            deal_at_risk_score=deal_risk,
            is_champion_stable=is_stable,
            needs_backup_champion=needs_backup,
        )
        self._results.append(result)
        return result

    def monitor_batch(self, inputs: list[ChampionRiskInput]) -> list[ChampionRiskResult]:
        return [self.monitor(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ──────────────────────────────────────────────────────────────

    @property
    def stable_champions(self) -> list[ChampionRiskResult]:
        return [r for r in self._results if r.is_champion_stable]

    @property
    def backup_needed_queue(self) -> list[ChampionRiskResult]:
        return [r for r in self._results if r.needs_backup_champion]

    @property
    def avg_champion_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.champion_composite for r in self._results) / len(self._results), 1)

    @property
    def avg_departure_probability(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.departure_probability for r in self._results) / len(self._results), 1)

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _engagement_score(self, inp: ChampionRiskInput) -> float:
        score = 0.0
        # Days since contact
        d = inp.days_since_champion_contact
        if d <= 3:
            score += 35.0
        elif d <= 7:
            score += 25.0
        elif d <= 14:
            score += 12.0
        elif d <= 30:
            score += 4.0
        # Reply rate
        rr = inp.champion_reply_rate_pct
        if rr >= 70:
            score += 30.0
        elif rr >= 50:
            score += 20.0
        elif rr >= 30:
            score += 10.0
        # Meeting trend
        if inp.champion_meetings_last_30d >= inp.champion_meetings_prior_30d and inp.champion_meetings_last_30d >= 2:
            score += 25.0
        elif inp.champion_meetings_last_30d >= 1:
            score += 12.0
        # Internal intros = high engagement signal
        if inp.champion_intro_count >= 3:
            score += 10.0
        elif inp.champion_intro_count >= 1:
            score += 5.0
        return round(max(0.0, min(100.0, score)), 1)

    def _influence_score(self, inp: ChampionRiskInput) -> float:
        score = 0.0
        # Title level (weight 40 pts)
        lvl = inp.champion_title_level
        if lvl >= 4:
            score += 40.0
        elif lvl == 3:
            score += 28.0
        elif lvl == 2:
            score += 16.0
        else:
            score += 6.0
        # Budget authority (weight 30 pts)
        if inp.champion_budget_authority:
            score += 30.0
        # Intros made (weight 20 pts)
        if inp.champion_intro_count >= 4:
            score += 20.0
        elif inp.champion_intro_count >= 2:
            score += 12.0
        elif inp.champion_intro_count >= 1:
            score += 6.0
        # Internal urgency creation
        if inp.champion_created_internal_urgency:
            score += 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _stability_score(self, inp: ChampionRiskInput) -> float:
        score = 80.0  # assume stable baseline
        # Job change signal = major risk
        if inp.champion_job_change_signal:
            score -= 50.0
        # Promotion signal = moderate risk (scope/priority change)
        if inp.champion_promotion_signal:
            score -= 15.0
        # Silent for too long
        if inp.days_since_champion_contact >= 21:
            score -= 25.0
        elif inp.days_since_champion_contact >= 14:
            score -= 12.0
        # Backup champion cushions risk
        if inp.backup_champion_identified:
            score = min(100.0, score + 15.0)
        # Multi-threaded = more stable
        if inp.multi_threaded_contacts >= 5:
            score = min(100.0, score + 10.0)
        elif inp.multi_threaded_contacts >= 3:
            score = min(100.0, score + 5.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _deal_protection_score(self, inp: ChampionRiskInput) -> float:
        score = 0.0
        # Executive relationship = deal protected if champion departs
        er = inp.executive_relationship_score
        if er >= 70:
            score += 35.0
        elif er >= 50:
            score += 22.0
        elif er >= 30:
            score += 12.0
        # Multi-threaded contacts
        mc = inp.multi_threaded_contacts
        if mc >= 6:
            score += 30.0
        elif mc >= 4:
            score += 20.0
        elif mc >= 2:
            score += 10.0
        # Backup champion
        if inp.backup_champion_identified:
            score += 20.0
        # Late-stage deal = more protected by progress
        if inp.deal_stage_numeric >= 5:
            score += 15.0
        elif inp.deal_stage_numeric >= 4:
            score += 8.0
        return round(max(0.0, min(100.0, score)), 1)

    def _composite(
        self,
        engagement: float,
        influence: float,
        stability: float,
        protection: float,
    ) -> float:
        composite = engagement * 0.35 + influence * 0.25 + stability * 0.25 + protection * 0.15
        return round(max(0.0, min(100.0, composite)), 1)

    def _champion_status(self, inp: ChampionRiskInput, composite: float) -> ChampionStatus:
        if inp.champion_job_change_signal:
            return ChampionStatus.DEPARTED
        if inp.days_since_champion_contact >= 21 or composite < 20:
            return ChampionStatus.SILENT
        if composite >= 70 and inp.champion_intro_count >= 2:
            return ChampionStatus.ACTIVE_ADVOCATE
        if composite >= 50:
            return ChampionStatus.ENGAGED
        return ChampionStatus.COOLING

    def _champion_risk(self, composite: float, inp: ChampionRiskInput) -> ChampionRisk:
        if inp.champion_job_change_signal or composite < 20:
            return ChampionRisk.CRITICAL
        if composite < 35 or inp.days_since_champion_contact >= 21:
            return ChampionRisk.HIGH
        if composite < 55:
            return ChampionRisk.MODERATE
        return ChampionRisk.LOW

    def _influence_level(self, inp: ChampionRiskInput) -> InfluenceLevel:
        score = inp.champion_title_level * 15 + (30 if inp.champion_budget_authority else 0) + inp.champion_intro_count * 5
        if score >= 80:
            return InfluenceLevel.HIGH_INFLUENCE
        if score >= 50:
            return InfluenceLevel.MODERATE_INFLUENCE
        if score >= 20:
            return InfluenceLevel.LOW_INFLUENCE
        return InfluenceLevel.UNKNOWN

    def _departure_probability(self, inp: ChampionRiskInput) -> float:
        prob = 0.0
        if inp.champion_job_change_signal:
            prob += 70.0
        if inp.champion_promotion_signal:
            prob += 20.0
        if inp.days_since_champion_contact >= 21:
            prob += 15.0
        elif inp.days_since_champion_contact >= 14:
            prob += 8.0
        if inp.champion_reply_rate_pct < 20:
            prob += 10.0
        return round(max(0.0, min(100.0, prob)), 1)

    def _deal_at_risk_score(self, inp: ChampionRiskInput, composite: float) -> float:
        base = 100.0 - composite
        # High-value deals at higher risk if champion unstable
        if inp.deal_size_usd >= 200_000 and inp.champion_job_change_signal:
            base = min(100.0, base + 15.0)
        # Late stage = even higher risk if champion departs now
        if inp.deal_stage_numeric >= 5 and inp.champion_job_change_signal:
            base = min(100.0, base + 10.0)
        # Close soon + at-risk = very dangerous
        if inp.days_to_close <= 14 and composite < 40:
            base = min(100.0, base + 10.0)
        return round(max(0.0, min(100.0, base)), 1)

    def _champion_action(
        self,
        risk: ChampionRisk,
        needs_backup: bool,
        inp: ChampionRiskInput,
    ) -> ChampionAction:
        if risk == ChampionRisk.CRITICAL:
            return ChampionAction.ESCALATE_EXEC
        if needs_backup:
            return ChampionAction.FIND_BACKUP
        if risk == ChampionRisk.HIGH:
            return ChampionAction.RE_ENGAGE
        if risk == ChampionRisk.MODERATE:
            return ChampionAction.RE_ENGAGE
        return ChampionAction.MAINTAIN

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                        0,
                "status_counts":                {},
                "risk_counts":                  {},
                "influence_counts":             {},
                "action_counts":                {},
                "avg_champion_composite":       0.0,
                "avg_departure_probability":    0.0,
                "stable_count":                 0,
                "backup_needed_count":          0,
                "avg_engagement_score":         0.0,
                "avg_influence_score":          0.0,
                "avg_stability_score":          0.0,
                "avg_deal_at_risk_score":       0.0,
            }

        status_counts:    dict[str, int] = {}
        risk_counts:      dict[str, int] = {}
        influence_counts: dict[str, int] = {}
        action_counts:    dict[str, int] = {}
        total_comp = 0.0; total_dep = 0.0; total_eng = 0.0
        total_inf  = 0.0; total_sta = 0.0; total_dar = 0.0

        for r in self._results:
            status_counts[r.champion_status.value]      = status_counts.get(r.champion_status.value, 0) + 1
            risk_counts[r.champion_risk.value]          = risk_counts.get(r.champion_risk.value, 0) + 1
            influence_counts[r.influence_level.value]   = influence_counts.get(r.influence_level.value, 0) + 1
            action_counts[r.champion_action.value]      = action_counts.get(r.champion_action.value, 0) + 1
            total_comp += r.champion_composite
            total_dep  += r.departure_probability
            total_eng  += r.engagement_score
            total_inf  += r.influence_score
            total_sta  += r.stability_score
            total_dar  += r.deal_at_risk_score

        return {
            "total":                        n,
            "status_counts":                status_counts,
            "risk_counts":                  risk_counts,
            "influence_counts":             influence_counts,
            "action_counts":                action_counts,
            "avg_champion_composite":       round(total_comp / n, 1),
            "avg_departure_probability":    round(total_dep / n, 1),
            "stable_count":                 len(self.stable_champions),
            "backup_needed_count":          len(self.backup_needed_queue),
            "avg_engagement_score":         round(total_eng / n, 1),
            "avg_influence_score":          round(total_inf / n, 1),
            "avg_stability_score":          round(total_sta / n, 1),
            "avg_deal_at_risk_score":       round(total_dar / n, 1),
        }
