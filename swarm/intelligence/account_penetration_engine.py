"""Module 41 — Account Penetration Intelligence Engine

Analyses stakeholder coverage breadth and relationship depth across key accounts
to identify whitespace in the buying committee, score penetration risk, and
generate targeted multi-threading strategies.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


# ─── Enums ────────────────────────────────────────────────────────────────────

class PenetrationLevel(str, Enum):
    DEEP       = "deep"        # excellent multi-threaded coverage across committee
    SOLID      = "solid"       # good coverage with minor gaps
    PARTIAL    = "partial"     # key roles covered but critical gaps exist
    THIN       = "thin"        # very limited stakeholder access
    SINGLE     = "single"      # single point of contact — critical risk


class StakeholderRisk(str, Enum):
    SECURE     = "secure"      # champion-level relationship, no key person risk
    STABLE     = "stable"      # solid relationships, low turnover risk
    VULNERABLE = "vulnerable"  # key stakeholder may leave or change position
    CRITICAL   = "critical"    # champion left or is unsupportive — action needed


class CommitteeGap(str, Enum):
    NONE           = "none"            # all key roles covered
    MISSING_EXEC   = "missing_exec"    # no C-level or VP engagement
    MISSING_USER   = "missing_user"    # no end-user champion
    MISSING_TECH   = "missing_tech"    # no technical evaluator engaged
    MISSING_FINANCE = "missing_finance" # no finance/procurement contact
    MULTIPLE_GAPS  = "multiple_gaps"   # two or more of the above missing


class PenetrationAction(str, Enum):
    MAINTAIN         = "maintain"          # sustain current multi-thread cadence
    EXPAND_EXEC      = "expand_exec"       # add executive sponsor engagement
    EXPAND_USER      = "expand_user"       # activate end-user champions
    EXPAND_TECH      = "expand_tech"       # engage technical evaluator/IT
    EXPAND_FINANCE   = "expand_finance"    # connect with finance/procurement
    REBUILD_CHAMPION = "rebuild_champion"  # lost champion — find replacement
    MULTITHREAD_NOW  = "multithread_now"   # single contact — immediate broadening needed


# ─── Input ────────────────────────────────────────────────────────────────────

@dataclass
class PenetrationInput:
    account_id: str
    account_name: str
    rep_id: str
    rep_name: str
    # Committee coverage
    total_contacts_mapped: int          # total stakeholders mapped in CRM
    executive_contacts: int             # C-level / VP contacts engaged
    user_champion_contacts: int         # end-user advocates identified
    technical_evaluator_contacts: int   # IT / technical contacts engaged
    finance_procurement_contacts: int   # finance / procurement contacts
    # Relationship quality
    active_contacts_30d: int            # contacts engaged in last 30 days
    promoter_contacts: int              # NPS-style promoters (advocates)
    neutral_contacts: int
    detractor_contacts: int
    # Key person signals
    primary_champion_engaged: bool
    champion_left_or_changed: bool
    executive_sponsor_active: bool
    decision_maker_relationship_score: int   # 0–10
    # Deal metadata
    deal_size_eur: float
    deal_stage: str                     # discovery | demo | proposal | negotiation | closing
    days_in_stage: int
    prior_deal_count: int               # number of previous closed deals with account
    contract_renewal_months: Optional[int]  # months until next renewal (None if new logo)


# ─── Output ───────────────────────────────────────────────────────────────────

@dataclass
class PenetrationResult:
    account_id: str
    account_name: str
    rep_id: str
    rep_name: str
    penetration_level: str
    stakeholder_risk: str
    committee_gap: str
    penetration_action: str
    penetration_score: float          # 0–100
    coverage_score: float             # 0–100 breadth of committee coverage
    relationship_score: float         # 0–100 quality of relationships
    multithread_ratio: float          # active_30d / total_contacts_mapped
    expansion_plays: list[str]
    risk_signals: list[str]
    manager_alerts: list[str]

    def to_dict(self) -> dict:
        return {
            "account_id":          self.account_id,
            "account_name":        self.account_name,
            "rep_id":              self.rep_id,
            "rep_name":            self.rep_name,
            "penetration_level":   self.penetration_level,
            "stakeholder_risk":    self.stakeholder_risk,
            "committee_gap":       self.committee_gap,
            "penetration_action":  self.penetration_action,
            "penetration_score":   self.penetration_score,
            "coverage_score":      self.coverage_score,
            "relationship_score":  self.relationship_score,
            "multithread_ratio":   self.multithread_ratio,
            "expansion_plays":     self.expansion_plays,
            "risk_signals":        self.risk_signals,
            "manager_alerts":      self.manager_alerts,
        }


# ─── Engine ───────────────────────────────────────────────────────────────────

class AccountPenetrationEngine:

    def __init__(self) -> None:
        self._results: list[PenetrationResult] = []

    # ── Coverage scoring ───────────────────────────────────────────────────────

    def _coverage_score(self, inp: PenetrationInput) -> float:
        score = 0.0
        # Committee role coverage (each role max 20 pts)
        if inp.executive_contacts >= 2:          score += 20
        elif inp.executive_contacts == 1:         score += 12
        if inp.user_champion_contacts >= 2:       score += 20
        elif inp.user_champion_contacts == 1:     score += 12
        if inp.technical_evaluator_contacts >= 1: score += 20
        if inp.finance_procurement_contacts >= 1: score += 15
        # Breadth bonus for total contacts
        if inp.total_contacts_mapped >= 8:        score += 10
        elif inp.total_contacts_mapped >= 5:      score += 5
        elif inp.total_contacts_mapped >= 3:      score += 2
        # Activity coverage
        if inp.total_contacts_mapped > 0:
            activity_ratio = inp.active_contacts_30d / inp.total_contacts_mapped
            score += min(15, activity_ratio * 15)
        return min(100.0, score)

    def _relationship_score(self, inp: PenetrationInput) -> float:
        score = 0.0
        # Champion & exec presence
        if inp.primary_champion_engaged:     score += 25
        if inp.executive_sponsor_active:     score += 20
        # Decision maker relationship strength
        score += inp.decision_maker_relationship_score * 2   # max 20
        # Promoter balance
        total = inp.promoter_contacts + inp.neutral_contacts + inp.detractor_contacts
        if total > 0:
            promoter_ratio = inp.promoter_contacts / total
            score += promoter_ratio * 20   # max 20
        # Prior relationship depth
        score += min(15, inp.prior_deal_count * 5)
        # Penalise detractors
        if inp.detractor_contacts >= 2:      score -= 10
        if inp.champion_left_or_changed:     score -= 20
        return max(0.0, min(100.0, score))

    def _penetration_score(self, coverage: float, relationship: float) -> float:
        return round(coverage * 0.5 + relationship * 0.5, 1)

    # ── Classification ─────────────────────────────────────────────────────────

    def _penetration_level(self, score: float, inp: PenetrationInput) -> PenetrationLevel:
        if inp.total_contacts_mapped <= 1:
            return PenetrationLevel.SINGLE
        if score >= 75:
            return PenetrationLevel.DEEP
        if score >= 55:
            return PenetrationLevel.SOLID
        if score >= 35:
            return PenetrationLevel.PARTIAL
        return PenetrationLevel.THIN

    def _stakeholder_risk(self, inp: PenetrationInput) -> StakeholderRisk:
        if inp.champion_left_or_changed:
            return StakeholderRisk.CRITICAL
        if inp.detractor_contacts >= 2 or inp.total_contacts_mapped <= 1:
            return StakeholderRisk.VULNERABLE
        if inp.promoter_contacts >= 2 and inp.primary_champion_engaged and inp.executive_sponsor_active:
            return StakeholderRisk.SECURE
        return StakeholderRisk.STABLE

    def _committee_gap(self, inp: PenetrationInput) -> CommitteeGap:
        gaps = 0
        missing = []
        if inp.executive_contacts == 0:             gaps += 1; missing.append("exec")
        if inp.user_champion_contacts == 0:         gaps += 1; missing.append("user")
        if inp.technical_evaluator_contacts == 0:   gaps += 1; missing.append("tech")
        if inp.finance_procurement_contacts == 0:   gaps += 1; missing.append("finance")
        if gaps == 0:           return CommitteeGap.NONE
        if gaps >= 2:           return CommitteeGap.MULTIPLE_GAPS
        if "exec" in missing:   return CommitteeGap.MISSING_EXEC
        if "user" in missing:   return CommitteeGap.MISSING_USER
        if "tech" in missing:   return CommitteeGap.MISSING_TECH
        return CommitteeGap.MISSING_FINANCE

    def _penetration_action(
        self,
        level: PenetrationLevel,
        risk: StakeholderRisk,
        gap: CommitteeGap,
    ) -> PenetrationAction:
        if level == PenetrationLevel.SINGLE:
            return PenetrationAction.MULTITHREAD_NOW
        if risk == StakeholderRisk.CRITICAL:
            return PenetrationAction.REBUILD_CHAMPION
        if gap == CommitteeGap.MISSING_EXEC:
            return PenetrationAction.EXPAND_EXEC
        if gap == CommitteeGap.MISSING_USER:
            return PenetrationAction.EXPAND_USER
        if gap == CommitteeGap.MISSING_TECH:
            return PenetrationAction.EXPAND_TECH
        if gap == CommitteeGap.MISSING_FINANCE:
            return PenetrationAction.EXPAND_FINANCE
        if gap == CommitteeGap.MULTIPLE_GAPS:
            return PenetrationAction.MULTITHREAD_NOW
        return PenetrationAction.MAINTAIN

    # ── Expansion plays ────────────────────────────────────────────────────────

    def _expansion_plays(
        self, inp: PenetrationInput, action: PenetrationAction
    ) -> list[str]:
        plays: list[str] = []
        if action == PenetrationAction.MULTITHREAD_NOW:
            plays.append(
                "Urgence multi-threading — identifier 3+ nouveaux contacts dans le comité d'achat sous 7 jours"
            )
            plays.append(
                "Demander au contact actuel de faire des introductions internes auprès des décideurs"
            )
        if action == PenetrationAction.REBUILD_CHAMPION:
            plays.append(
                "Champion perdu — cartographier les promoteurs internes restants et en activer un nouveau"
            )
            plays.append(
                "Organiser un executive briefing pour rebâtir la relation au niveau stratégique"
            )
        if inp.executive_contacts == 0:
            plays.append(
                "Aucun contact C-level — demander une introduction via le champion existant pour un EBR"
            )
        if inp.user_champion_contacts == 0:
            plays.append(
                "Pas de champion utilisateur — organiser un atelier de découverte avec les équipes terrain"
            )
        if inp.technical_evaluator_contacts == 0:
            plays.append(
                "Évaluateur technique non engagé — planifier une session technique avec l'IT"
            )
        if inp.finance_procurement_contacts == 0 and inp.deal_stage in ("proposal", "negotiation", "closing"):
            plays.append(
                "Aucun contact Finance/Achats engagé — impératif avant la phase contractuelle"
            )
        if inp.active_contacts_30d < inp.total_contacts_mapped * 0.5 and inp.total_contacts_mapped >= 3:
            plays.append(
                f"Seulement {inp.active_contacts_30d}/{inp.total_contacts_mapped} contacts actifs en 30j — relancer les contacts dormants"
            )
        if not plays:
            plays.append(
                f"Maintenir le rythme d'engagement — {inp.total_contacts_mapped} contacts mappés, {inp.active_contacts_30d} actifs"
            )
        return plays

    # ── Risk signals ───────────────────────────────────────────────────────────

    def _risk_signals(self, inp: PenetrationInput) -> list[str]:
        risks: list[str] = []
        if inp.total_contacts_mapped <= 1:
            risks.append("Contact unique — risque critique de single-point-of-failure")
        if inp.champion_left_or_changed:
            risks.append("Champion principal a quitté ou changé de rôle — relation à reconstruire d'urgence")
        if inp.detractor_contacts >= 1:
            risks.append(
                f"{inp.detractor_contacts} détracteur(s) identifié(s) — risque de blocage interne"
            )
        if inp.executive_contacts == 0 and inp.deal_size_eur >= 50000:
            risks.append(
                f"Aucun contact exécutif sur un deal de {inp.deal_size_eur:,.0f}€ — risque de blocage décisionnel"
            )
        if inp.active_contacts_30d == 0 and inp.total_contacts_mapped > 0:
            risks.append("Aucun contact actif en 30 jours — compte en voie de désengagement")
        if inp.deal_stage in ("proposal", "negotiation") and inp.finance_procurement_contacts == 0:
            risks.append(
                "Pas de contact Finance/Achats en phase de proposition/négociation — approbation budgétaire en risque"
            )
        return risks

    # ── Manager alerts ─────────────────────────────────────────────────────────

    def _manager_alerts(
        self,
        inp: PenetrationInput,
        level: PenetrationLevel,
        risk: StakeholderRisk,
    ) -> list[str]:
        alerts: list[str] = []
        if level == PenetrationLevel.SINGLE:
            alerts.append(
                f"⚠ Contact unique sur {inp.account_name} ({inp.deal_size_eur:,.0f}€) — action multi-threading immédiate requise"
            )
        if risk == StakeholderRisk.CRITICAL:
            alerts.append(
                f"Champion perdu chez {inp.account_name} — revue manager pour plan de récupération urgent"
            )
        if level in (PenetrationLevel.THIN, PenetrationLevel.SINGLE) and inp.deal_size_eur >= 80000:
            alerts.append(
                f"Pénétration critique ({level.value}) sur deal stratégique {inp.deal_size_eur:,.0f}€ — escalade senior recommandée"
            )
        if inp.detractor_contacts >= 2:
            alerts.append(
                f"{inp.detractor_contacts} détracteurs chez {inp.account_name} — risque de blocage interne, revue stratégique requise"
            )
        return alerts

    # ── Main analysis ──────────────────────────────────────────────────────────

    def analyze(self, inp: PenetrationInput) -> PenetrationResult:
        coverage_score     = round(self._coverage_score(inp), 1)
        relationship_score = round(self._relationship_score(inp), 1)
        penetration_score  = self._penetration_score(coverage_score, relationship_score)
        level              = self._penetration_level(penetration_score, inp)
        risk               = self._stakeholder_risk(inp)
        gap                = self._committee_gap(inp)
        action             = self._penetration_action(level, risk, gap)
        multithread_ratio  = round(
            inp.active_contacts_30d / inp.total_contacts_mapped
            if inp.total_contacts_mapped > 0 else 0.0, 2
        )

        result = PenetrationResult(
            account_id         = inp.account_id,
            account_name       = inp.account_name,
            rep_id             = inp.rep_id,
            rep_name           = inp.rep_name,
            penetration_level  = level.value,
            stakeholder_risk   = risk.value,
            committee_gap      = gap.value,
            penetration_action = action.value,
            penetration_score  = penetration_score,
            coverage_score     = coverage_score,
            relationship_score = relationship_score,
            multithread_ratio  = multithread_ratio,
            expansion_plays    = self._expansion_plays(inp, action),
            risk_signals       = self._risk_signals(inp),
            manager_alerts     = self._manager_alerts(inp, level, risk),
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[PenetrationInput]) -> list[PenetrationResult]:
        results = [self.analyze(inp) for inp in inputs]
        results.sort(key=lambda r: r.penetration_score, reverse=True)
        return results

    # ── Helpers ────────────────────────────────────────────────────────────────

    def single_threaded(self) -> list[PenetrationResult]:
        return [r for r in self._results if r.penetration_level == PenetrationLevel.SINGLE.value]

    def critical_risk(self) -> list[PenetrationResult]:
        return [r for r in self._results if r.stakeholder_risk == StakeholderRisk.CRITICAL.value]

    def needs_multithread(self) -> list[PenetrationResult]:
        return [r for r in self._results if r.penetration_action == PenetrationAction.MULTITHREAD_NOW.value]

    def deep_penetration(self) -> list[PenetrationResult]:
        return [r for r in self._results if r.penetration_level == PenetrationLevel.DEEP.value]

    def has_committee_gaps(self) -> list[PenetrationResult]:
        return [r for r in self._results if r.committee_gap != CommitteeGap.NONE.value]

    def summary(self) -> dict:
        results = self._results
        n = len(results)
        if n == 0:
            return {
                "total": 0,
                "level_counts": {},
                "risk_counts": {},
                "gap_counts": {},
                "action_counts": {},
                "avg_penetration_score": 0.0,
                "avg_coverage_score": 0.0,
                "avg_relationship_score": 0.0,
                "single_threaded_count": 0,
                "critical_risk_count": 0,
            }
        level_counts:  dict[str, int] = {}
        risk_counts:   dict[str, int] = {}
        gap_counts:    dict[str, int] = {}
        action_counts: dict[str, int] = {}
        total_pen = total_cov = total_rel = 0.0

        for r in results:
            level_counts[r.penetration_level]  = level_counts.get(r.penetration_level, 0) + 1
            risk_counts[r.stakeholder_risk]     = risk_counts.get(r.stakeholder_risk, 0) + 1
            gap_counts[r.committee_gap]         = gap_counts.get(r.committee_gap, 0) + 1
            action_counts[r.penetration_action] = action_counts.get(r.penetration_action, 0) + 1
            total_pen += r.penetration_score
            total_cov += r.coverage_score
            total_rel += r.relationship_score

        return {
            "total":                   n,
            "level_counts":            level_counts,
            "risk_counts":             risk_counts,
            "gap_counts":              gap_counts,
            "action_counts":           action_counts,
            "avg_penetration_score":   round(total_pen / n, 1),
            "avg_coverage_score":      round(total_cov / n, 1),
            "avg_relationship_score":  round(total_rel / n, 1),
            "single_threaded_count":   sum(1 for r in results if r.penetration_level == PenetrationLevel.SINGLE.value),
            "critical_risk_count":     sum(1 for r in results if r.stakeholder_risk == StakeholderRisk.CRITICAL.value),
        }

    def reset(self) -> None:
        self._results = []
