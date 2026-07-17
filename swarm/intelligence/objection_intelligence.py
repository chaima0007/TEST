"""Objection Intelligence — tracks and scores sales objections to guide deal progression."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional


class ObjectionBurden(str, Enum):
    CLEAR = "clear"        # score 0-20 — minimal objections, deal advancing
    MODERATE = "moderate"  # score 21-45 — some friction, manageable
    HEAVY = "heavy"        # score 46-70 — significant barriers to close
    CRITICAL = "critical"  # score 71-100 — deal at serious risk


class ObjectionAction(str, Enum):
    ADVANCE = "advance"    # low burden, push to next stage
    ADDRESS = "address"    # specific objections to tackle before advancing
    ESCALATE = "escalate"  # needs executive or specialist involvement
    REASSESS = "reassess"  # deal viability in question, reconsider pursuit


# Weights reflect how damaging each objection type is to win probability
_OBJECTION_WEIGHTS: dict[str, int] = {
    "price": 22,
    "competitor": 18,
    "authority": 16,
    "trust": 15,
    "timing": 15,
    "implementation": 14,
}

_MAX_RAW = sum(w * 2 for w in _OBJECTION_WEIGHTS.values())  # = 200, cap each type at 2x weight


@dataclass
class ObjectionInput:
    deal_id: str
    deal_name: str
    account_name: str
    arr_eur: float
    stage: str  # qualification / demo / proposal / negotiation / closing

    # Active unresolved objection counts per type
    price_objections: int          # "too expensive", "over budget"
    competitor_objections: int     # "evaluating X", "X does it cheaper"
    authority_objections: int      # "need to involve others", "not my decision"
    timing_objections: int         # "not now", "bad timing"
    implementation_objections: int # "too complex", "integration concerns"
    trust_objections: int          # "don't know you", "need references"

    # Session context
    objections_handled_this_session: int  # resolved in latest meeting
    days_oldest_unresolved: int           # age of longest-standing objection

    # Mitigating factors
    budget_confirmed: bool
    champion_vouched: bool         # champion explicitly backed vendor internally
    case_study_shared: bool
    proof_of_concept_done: bool
    references_provided: bool
    executive_sponsor_engaged: bool
    timeline_agreed: bool
    competitor_named: bool         # specific competitor identified
    evaluated_alternatives: int    # number of alternatives being considered


@dataclass
class ObjectionResult:
    deal_id: str
    deal_name: str
    account_name: str
    arr_eur: float
    stage: str

    objection_burden: ObjectionBurden
    objection_action: ObjectionAction
    burden_score: float          # 0-100, higher = more burden
    total_active_objections: int
    resolution_score: float      # 0-100, how effectively objections are handled
    primary_objection_type: str  # dominant objection category
    deal_impact_eur: float       # ARR at risk = arr_eur * burden_score / 100

    risk_factors: list[str]
    mitigating_factors: list[str]
    recommended_tactics: list[str]

    def to_dict(self) -> dict:
        d = asdict(self)
        d["objection_burden"] = self.objection_burden.value
        d["objection_action"] = self.objection_action.value
        return d


def _burden_score(inp: ObjectionInput) -> tuple[float, str, int]:
    """Returns (burden_score 0-100, primary_objection_type, total_active)."""
    counts = {
        "price": inp.price_objections,
        "competitor": inp.competitor_objections,
        "authority": inp.authority_objections,
        "trust": inp.trust_objections,
        "timing": inp.timing_objections,
        "implementation": inp.implementation_objections,
    }
    total = sum(counts.values())
    if total > 0:
        primary = max(counts, key=lambda k: counts[k] * _OBJECTION_WEIGHTS[k])
    else:
        primary = "none"

    raw = sum(min(count * _OBJECTION_WEIGHTS[k], _OBJECTION_WEIGHTS[k] * 2) for k, count in counts.items())
    score = (raw / _MAX_RAW) * 100

    score += min(15.0, inp.days_oldest_unresolved * 1.5)

    reductions = 0.0
    if inp.budget_confirmed:         reductions += 12.0
    if inp.champion_vouched:         reductions += 10.0
    if inp.proof_of_concept_done:    reductions += 8.0
    if inp.executive_sponsor_engaged: reductions += 8.0
    if inp.timeline_agreed:          reductions += 6.0
    if inp.case_study_shared:        reductions += 6.0
    if inp.references_provided:      reductions += 5.0
    score -= reductions

    return round(max(0.0, min(100.0, score)), 2), primary, total


def _resolution_score(inp: ObjectionInput, total: int) -> float:
    if total == 0:
        return 100.0
    handled = min(inp.objections_handled_this_session, total)
    base = (handled / total) * 50.0
    if inp.budget_confirmed:         base += 12.0
    if inp.champion_vouched:         base += 10.0
    if inp.proof_of_concept_done:    base += 10.0
    if inp.timeline_agreed:          base += 8.0
    if inp.case_study_shared:        base += 6.0
    if inp.references_provided:      base += 4.0
    return round(max(0.0, min(100.0, base)), 2)


def _objection_burden(score: float) -> ObjectionBurden:
    if score <= 20:
        return ObjectionBurden.CLEAR
    if score <= 45:
        return ObjectionBurden.MODERATE
    if score <= 70:
        return ObjectionBurden.HEAVY
    return ObjectionBurden.CRITICAL


def _objection_action(inp: ObjectionInput, burden: ObjectionBurden) -> ObjectionAction:
    if burden == ObjectionBurden.CRITICAL:
        return ObjectionAction.REASSESS
    if burden == ObjectionBurden.HEAVY and (
        inp.authority_objections > 0 or inp.competitor_objections > 1 or inp.evaluated_alternatives >= 2
    ):
        return ObjectionAction.ESCALATE
    if burden in (ObjectionBurden.MODERATE, ObjectionBurden.HEAVY):
        return ObjectionAction.ADDRESS
    return ObjectionAction.ADVANCE


def _build_signals(
    inp: ObjectionInput,
    burden: ObjectionBurden,
    total: int,
    primary: str,
) -> tuple[list[str], list[str], list[str]]:
    risks: list[str] = []
    mitigations: list[str] = []
    tactics: list[str] = []

    # Risk factors
    if inp.price_objections > 0:
        risks.append(f"Objection prix active ({inp.price_objections}x) — budget non confirmé" if not inp.budget_confirmed else f"Objection prix active ({inp.price_objections}x)")
    if inp.competitor_objections > 0:
        named = f" ({inp.evaluated_alternatives} alternative(s) évaluée(s))" if inp.evaluated_alternatives > 0 else ""
        risks.append(f"Concurrent identifié{' nommé' if inp.competitor_named else ''} en évaluation{named}")
    if inp.authority_objections > 0:
        risks.append(f"Objection d'autorité — {inp.authority_objections} partie(s) prenante(s) non engagée(s)")
    if inp.timing_objections > 0:
        risks.append(f"Objection de timing — deal bloqué temporellement ({inp.timing_objections}x)")
    if inp.implementation_objections > 0:
        risks.append(f"Inquiétudes d'implémentation actives ({inp.implementation_objections}x)")
    if inp.trust_objections > 0:
        risks.append(f"Confiance insuffisante — {inp.trust_objections} objection(s) de crédibilité")
    if inp.days_oldest_unresolved > 14:
        risks.append(f"Objection non résolue depuis {inp.days_oldest_unresolved}j — risque de stagnation")
    elif inp.days_oldest_unresolved > 7:
        risks.append(f"Objection persistante depuis {inp.days_oldest_unresolved}j sans résolution")
    if inp.evaluated_alternatives >= 3:
        risks.append(f"Forte concurrence — {inp.evaluated_alternatives} alternatives en évaluation")
    if burden == ObjectionBurden.CRITICAL and not inp.executive_sponsor_engaged:
        risks.append("Sponsor exécutif non activé — deal en situation critique")

    # Mitigating factors
    if inp.budget_confirmed:
        mitigations.append("Budget confirmé — objections prix partiellement levées")
    if inp.champion_vouched:
        mitigations.append("Champion a explicitement soutenu la solution en interne")
    if inp.proof_of_concept_done:
        mitigations.append("POC complété — preuves techniques établies")
    if inp.executive_sponsor_engaged:
        mitigations.append("Sponsor exécutif engagé — niveau décisionnel couvert")
    if inp.case_study_shared:
        mitigations.append("Business case partagé — ROI démontré")
    if inp.references_provided:
        mitigations.append("Références clients fournies — crédibilité renforcée")
    if inp.timeline_agreed:
        mitigations.append("Timeline convenu — objections de timing levées")
    if inp.objections_handled_this_session > 0:
        mitigations.append(f"{inp.objections_handled_this_session} objection(s) traitée(s) lors de la dernière session")

    # Recommended tactics
    if inp.price_objections > 0 and not inp.budget_confirmed:
        tactics.append("Clarifier la valeur ROI et confirmer l'enveloppe budgétaire disponible")
    if inp.competitor_objections > 0:
        if inp.competitor_named:
            tactics.append("Préparer une battle card comparative pour le concurrent identifié")
        else:
            tactics.append("Identifier le concurrent et positionner les différenciateurs clés")
    if inp.authority_objections > 0 and not inp.executive_sponsor_engaged:
        tactics.append("Activer le sponsor exécutif pour atteindre les décideurs finaux")
    if inp.timing_objections > 0 and not inp.timeline_agreed:
        tactics.append("Co-construire un business case urgency avec le champion pour débloquer le timing")
    if inp.implementation_objections > 0 and not inp.proof_of_concept_done:
        tactics.append("Proposer un POC ou workshop technique pour lever les inquiétudes d'implémentation")
    if inp.trust_objections > 0 and not inp.references_provided:
        tactics.append("Fournir des références clients du même secteur et organiser des peer calls")
    if inp.trust_objections > 0 and not inp.case_study_shared:
        tactics.append("Partager un business case de référence avec ROI mesurable")
    if inp.days_oldest_unresolved > 7:
        tactics.append(f"Planifier un appel de suivi dédié pour résoudre l'objection persistante ({inp.days_oldest_unresolved}j)")
    if inp.evaluated_alternatives >= 2:
        tactics.append("Demander les critères de sélection et positionner l'avantage concurrentiel différenciant")
    if burden == ObjectionBurden.CRITICAL:
        tactics.append("Evaluer si le deal répond aux critères ICP — envisager une pause stratégique")
    if total == 0 and inp.stage in ("proposal", "negotiation", "closing"):
        tactics.append("Aucune objection active — proposer les prochaines étapes contractuelles")

    return risks, mitigations, tactics


class ObjectionIntelligenceEngine:
    """Tracks and scores sales objections to guide deal progression strategy."""

    def __init__(self) -> None:
        self._results: dict[str, ObjectionResult] = {}

    def analyze(self, inp: ObjectionInput) -> ObjectionResult:
        score, primary, total = _burden_score(inp)
        resolution = _resolution_score(inp, total)
        burden = _objection_burden(score)
        action = _objection_action(inp, burden)
        risks, mitigations, tactics = _build_signals(inp, burden, total, primary)

        result = ObjectionResult(
            deal_id=inp.deal_id,
            deal_name=inp.deal_name,
            account_name=inp.account_name,
            arr_eur=inp.arr_eur,
            stage=inp.stage,
            objection_burden=burden,
            objection_action=action,
            burden_score=score,
            total_active_objections=total,
            resolution_score=resolution,
            primary_objection_type=primary,
            deal_impact_eur=round(inp.arr_eur * score / 100.0, 2),
            risk_factors=risks,
            mitigating_factors=mitigations,
            recommended_tactics=tactics,
        )
        self._results[inp.deal_id] = result
        return result

    def analyze_batch(self, inputs: list[ObjectionInput]) -> list[ObjectionResult]:
        return sorted(
            [self.analyze(inp) for inp in inputs],
            key=lambda r: r.burden_score,
            reverse=True,
        )

    def get(self, deal_id: str) -> Optional[ObjectionResult]:
        return self._results.get(deal_id)

    def all_deals(self) -> list[ObjectionResult]:
        return sorted(self._results.values(), key=lambda r: r.burden_score, reverse=True)

    def by_burden(self, burden: ObjectionBurden) -> list[ObjectionResult]:
        return [r for r in self.all_deals() if r.objection_burden == burden]

    def critical(self) -> list[ObjectionResult]:
        return self.by_burden(ObjectionBurden.CRITICAL)

    def heavy(self) -> list[ObjectionResult]:
        return self.by_burden(ObjectionBurden.HEAVY)

    def at_risk(self) -> list[ObjectionResult]:
        return [r for r in self.all_deals() if r.objection_burden in (
            ObjectionBurden.CRITICAL, ObjectionBurden.HEAVY
        )]

    def clear(self) -> list[ObjectionResult]:
        return self.by_burden(ObjectionBurden.CLEAR)

    def needs_escalation(self) -> list[ObjectionResult]:
        return [r for r in self.all_deals() if r.objection_action in (
            ObjectionAction.ESCALATE, ObjectionAction.REASSESS
        )]

    def ready_to_advance(self) -> list[ObjectionResult]:
        return [r for r in self.all_deals() if r.objection_action == ObjectionAction.ADVANCE]

    def total_arr_impacted_eur(self) -> float:
        return round(sum(r.deal_impact_eur for r in self._results.values()), 2)

    def total_arr_at_risk_eur(self) -> float:
        return round(sum(r.arr_eur for r in self.at_risk()), 2)

    def avg_burden_score(self) -> float:
        deals = list(self._results.values())
        if not deals:
            return 0.0
        return round(sum(r.burden_score for r in deals) / len(deals), 1)

    def avg_resolution_score(self) -> float:
        deals = list(self._results.values())
        if not deals:
            return 0.0
        return round(sum(r.resolution_score for r in deals) / len(deals), 1)

    def by_primary_objection(self, objection_type: str) -> list[ObjectionResult]:
        return [r for r in self.all_deals() if r.primary_objection_type == objection_type]

    def top_n_by_impact(self, n: int) -> list[ObjectionResult]:
        return sorted(self._results.values(), key=lambda r: r.deal_impact_eur, reverse=True)[:n]

    def summary(self) -> dict:
        all_r = list(self._results.values())
        if not all_r:
            return {
                "total": 0,
                "burden_counts": {},
                "action_counts": {},
                "avg_burden_score": 0.0,
                "avg_resolution_score": 0.0,
                "total_arr_impacted_eur": 0.0,
                "total_arr_at_risk_eur": 0.0,
                "critical_count": 0,
                "escalation_count": 0,
                "advance_ready_count": 0,
            }
        burden_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in all_r:
            burden_counts[r.objection_burden.value] = burden_counts.get(r.objection_burden.value, 0) + 1
            action_counts[r.objection_action.value] = action_counts.get(r.objection_action.value, 0) + 1
        return {
            "total": len(all_r),
            "burden_counts": burden_counts,
            "action_counts": action_counts,
            "avg_burden_score": self.avg_burden_score(),
            "avg_resolution_score": self.avg_resolution_score(),
            "total_arr_impacted_eur": self.total_arr_impacted_eur(),
            "total_arr_at_risk_eur": self.total_arr_at_risk_eur(),
            "critical_count": len(self.critical()),
            "escalation_count": len(self.needs_escalation()),
            "advance_ready_count": len(self.ready_to_advance()),
        }

    def reset(self) -> None:
        self._results.clear()
