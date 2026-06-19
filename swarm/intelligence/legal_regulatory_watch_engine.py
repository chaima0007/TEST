"""
Module 237 — International Legal & Regulatory Watch Engine
Monitors jurisdictional compliance, litigation risk, licensing exposure, and
regulatory change velocity — then recommends the right legal response before
exposure becomes irreversible.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class LegalRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class RegulatoryPattern(str, Enum):
    none                  = "none"
    compliance_gap        = "compliance_gap"
    regulatory_change     = "regulatory_change"
    litigation_risk       = "litigation_risk"
    licensing_breach      = "licensing_breach"
    cross_border_conflict = "cross_border_conflict"


class LegalSeverity(str, Enum):
    compliant = "compliant"
    watch     = "watch"
    exposed   = "exposed"
    critical  = "critical"


class LegalAction(str, Enum):
    no_action                = "no_action"
    regulatory_monitoring    = "regulatory_monitoring"
    compliance_review        = "compliance_review"
    legal_counsel_alert      = "legal_counsel_alert"
    regulatory_filing        = "regulatory_filing"
    licensing_remediation    = "licensing_remediation"
    litigation_response      = "litigation_response"
    emergency_compliance     = "emergency_compliance"
    regulatory_shutdown      = "regulatory_shutdown"


@dataclass
class LegalInput:
    jurisdiction_id: str
    domain: str                          # tax/labor/data_privacy/trade/financial/environmental/healthcare
    region: str
    compliance_score: float              # 0-1 (1=fully compliant)
    regulatory_change_velocity: float    # 0-1 (1=fast-changing)
    pending_regulatory_deadlines: int    # count
    missed_filing_count: int
    litigation_pending_count: int
    litigation_loss_rate: float          # 0-1
    licensing_expiry_days: int           # days until expiry, 0=expired
    license_coverage_pct: float          # 0-1
    cross_border_conflict_score: float   # 0-1
    trade_restriction_exposure: float    # 0-1
    environmental_penalty_risk: float    # 0-1
    labor_law_violation_count: int
    data_privacy_gap_score: float        # 0-1
    contract_enforceability_score: float # 0-1 (1=fully enforceable)
    internal_legal_capacity_score: float # 0-1 (1=well staffed)
    regulatory_relationship_score: float # 0-1 (1=excellent)
    legal_spend_efficiency_score: float  # 0-1 (1=efficient)


@dataclass
class LegalResult:
    jurisdiction_id: str
    region: str
    legal_risk: str
    regulatory_pattern: str
    legal_severity: str
    recommended_action: str
    compliance_score_out: float
    litigation_score: float
    licensing_score: float
    regulatory_score: float
    legal_composite: float
    has_legal_exposure: bool
    requires_immediate_counsel: bool
    estimated_legal_risk_index: float
    legal_signal: str

    def to_dict(self) -> Dict:
        return {
            "jurisdiction_id":            self.jurisdiction_id,
            "region":                     self.region,
            "legal_risk":                 self.legal_risk,
            "regulatory_pattern":         self.regulatory_pattern,
            "legal_severity":             self.legal_severity,
            "recommended_action":         self.recommended_action,
            "compliance_score_out":       self.compliance_score_out,
            "litigation_score":           self.litigation_score,
            "licensing_score":            self.licensing_score,
            "regulatory_score":           self.regulatory_score,
            "legal_composite":            self.legal_composite,
            "has_legal_exposure":         self.has_legal_exposure,
            "requires_immediate_counsel": self.requires_immediate_counsel,
            "estimated_legal_risk_index": self.estimated_legal_risk_index,
            "legal_signal":               self.legal_signal,
        }


class LegalRegulatoryWatchEngine:
    def __init__(self) -> None:
        self._results: List[LegalResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────────

    def _compliance_score_out(self, i: LegalInput) -> float:
        s = 0
        if   i.compliance_score <= 0.40: s += 40
        elif i.compliance_score <= 0.65: s += 22
        elif i.compliance_score <= 0.80: s += 8

        if   i.missed_filing_count >= 5: s += 35
        elif i.missed_filing_count >= 2: s += 18
        elif i.missed_filing_count >= 1: s += 6

        if   i.data_privacy_gap_score >= 0.60: s += 25
        elif i.data_privacy_gap_score >= 0.35: s += 12
        return min(s, 100)

    def _litigation_score(self, i: LegalInput) -> float:
        s = 0
        if   i.litigation_pending_count >= 5: s += 40
        elif i.litigation_pending_count >= 2: s += 22
        elif i.litigation_pending_count >= 1: s += 8

        if   i.litigation_loss_rate >= 0.60: s += 35
        elif i.litigation_loss_rate >= 0.35: s += 18
        elif i.litigation_loss_rate >= 0.15: s += 6

        if   i.contract_enforceability_score <= 0.40: s += 25
        elif i.contract_enforceability_score <= 0.65: s += 12
        return min(s, 100)

    def _licensing_score(self, i: LegalInput) -> float:
        s = 0
        if   i.licensing_expiry_days <= 0:  s += 45
        elif i.licensing_expiry_days <= 30:  s += 28
        elif i.licensing_expiry_days <= 90:  s += 12

        if   i.license_coverage_pct <= 0.50: s += 35
        elif i.license_coverage_pct <= 0.75: s += 18
        elif i.license_coverage_pct <= 0.90: s += 6

        if   i.labor_law_violation_count >= 3: s += 20
        elif i.labor_law_violation_count >= 1: s += 10
        return min(s, 100)

    def _regulatory_score(self, i: LegalInput) -> float:
        s = 0
        if   i.pending_regulatory_deadlines >= 8: s += 40
        elif i.pending_regulatory_deadlines >= 4: s += 22
        elif i.pending_regulatory_deadlines >= 2: s += 8

        if   i.regulatory_change_velocity >= 0.75: s += 35
        elif i.regulatory_change_velocity >= 0.50: s += 18
        elif i.regulatory_change_velocity >= 0.25: s += 6

        if   i.cross_border_conflict_score >= 0.60: s += 25
        elif i.cross_border_conflict_score >= 0.35: s += 12
        return min(s, 100)

    def _composite(self, comp: float, lit: float, lic: float, reg: float) -> float:
        return min(round(comp * 0.30 + lit * 0.25 + lic * 0.25 + reg * 0.20, 2), 100.0)

    def _risk(self, c: float) -> LegalRisk:
        if c >= 60: return LegalRisk.critical
        if c >= 40: return LegalRisk.high
        if c >= 20: return LegalRisk.moderate
        return LegalRisk.low

    def _severity(self, c: float) -> LegalSeverity:
        if c >= 60: return LegalSeverity.critical
        if c >= 40: return LegalSeverity.exposed
        if c >= 20: return LegalSeverity.watch
        return LegalSeverity.compliant

    def _pattern(self, i: LegalInput) -> RegulatoryPattern:
        if i.litigation_pending_count >= 3 or i.litigation_loss_rate >= 0.50:
            return RegulatoryPattern.litigation_risk
        if i.compliance_score <= 0.40 or i.missed_filing_count >= 3:
            return RegulatoryPattern.compliance_gap
        if i.licensing_expiry_days <= 0 or i.license_coverage_pct <= 0.50:
            return RegulatoryPattern.licensing_breach
        if i.regulatory_change_velocity >= 0.70 and i.pending_regulatory_deadlines >= 4:
            return RegulatoryPattern.regulatory_change
        if i.cross_border_conflict_score >= 0.60 or i.trade_restriction_exposure >= 0.55:
            return RegulatoryPattern.cross_border_conflict
        return RegulatoryPattern.none

    def _action(self, risk: LegalRisk, pat: RegulatoryPattern) -> LegalAction:
        if risk == LegalRisk.critical:
            if pat == RegulatoryPattern.litigation_risk:
                return LegalAction.emergency_compliance
            if pat == RegulatoryPattern.compliance_gap:
                return LegalAction.emergency_compliance
            if pat == RegulatoryPattern.licensing_breach:
                return LegalAction.regulatory_shutdown
            return LegalAction.regulatory_filing
        if risk == LegalRisk.high:
            if pat == RegulatoryPattern.litigation_risk:
                return LegalAction.litigation_response
            if pat == RegulatoryPattern.compliance_gap:
                return LegalAction.legal_counsel_alert
            if pat == RegulatoryPattern.licensing_breach:
                return LegalAction.licensing_remediation
            if pat == RegulatoryPattern.regulatory_change:
                return LegalAction.regulatory_filing
            return LegalAction.compliance_review
        if risk == LegalRisk.moderate:
            return LegalAction.regulatory_monitoring
        return LegalAction.no_action

    def _signal(self, i: LegalInput, pat: RegulatoryPattern, comp: float) -> str:
        if comp < 20:
            return (
                "Conformité juridique solide — aucun litige, licences à jour, "
                "conformité réglementaire maintenue"
            )
        labels = {
            RegulatoryPattern.litigation_risk:       "Risque litige",
            RegulatoryPattern.compliance_gap:        "Écart conformité",
            RegulatoryPattern.licensing_breach:      "Violation licence",
            RegulatoryPattern.regulatory_change:     "Changement réglementaire",
            RegulatoryPattern.cross_border_conflict: "Conflit transfrontalier",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — "
            f"conformité {i.compliance_score * 100:.0f}% — "
            f"litiges {i.litigation_pending_count} — "
            f"expiration licence {i.licensing_expiry_days}j — "
            f"composite {comp:.0f}"
        )

    def _has_legal_exposure(self, i: LegalInput, comp: float) -> bool:
        return (
            comp >= 40
            or i.litigation_pending_count >= 2
            or i.licensing_expiry_days <= 30
            or i.compliance_score <= 0.45
        )

    def _requires_immediate_counsel(self, i: LegalInput, comp: float) -> bool:
        return (
            comp >= 25
            or i.litigation_pending_count >= 1
            or i.licensing_expiry_days <= 0
            or i.labor_law_violation_count >= 2
        )

    def _legal_risk_index(self, i: LegalInput, comp: float) -> float:
        return round(min(comp / 100 * (1 - i.internal_legal_capacity_score + 0.01) * 10, 10.0), 2)

    # ── public API ────────────────────────────────────────────────────────────

    def assess(self, i: LegalInput) -> LegalResult:
        comp_s = self._compliance_score_out(i)
        lit_s  = self._litigation_score(i)
        lic_s  = self._licensing_score(i)
        reg_s  = self._regulatory_score(i)
        comp   = self._composite(comp_s, lit_s, lic_s, reg_s)
        risk   = self._risk(comp)
        sev    = self._severity(comp)
        pat    = self._pattern(i)
        act    = self._action(risk, pat)
        result = LegalResult(
            jurisdiction_id=i.jurisdiction_id,
            region=i.region,
            legal_risk=risk.value,
            regulatory_pattern=pat.value,
            legal_severity=sev.value,
            recommended_action=act.value,
            compliance_score_out=comp_s,
            litigation_score=lit_s,
            licensing_score=lic_s,
            regulatory_score=reg_s,
            legal_composite=comp,
            has_legal_exposure=self._has_legal_exposure(i, comp),
            requires_immediate_counsel=self._requires_immediate_counsel(i, comp),
            estimated_legal_risk_index=self._legal_risk_index(i, comp),
            legal_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[LegalInput]) -> List[LegalResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_legal_composite": 0.0,
                "legal_exposure_count": 0,
                "immediate_counsel_count": 0,
                "avg_compliance_score": 0.0,
                "avg_litigation_score": 0.0,
                "avg_licensing_score": 0.0,
                "avg_regulatory_score": 0.0,
                "avg_estimated_legal_risk_index": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        t_comp = t_comp_s = t_lit = t_lic = t_reg = t_idx = 0.0
        exp_c = coun_c = 0
        for r in self._results:
            rc[r.legal_risk]          = rc.get(r.legal_risk, 0)          + 1
            pc[r.regulatory_pattern]  = pc.get(r.regulatory_pattern, 0)  + 1
            sc[r.legal_severity]      = sc.get(r.legal_severity, 0)      + 1
            ac[r.recommended_action]  = ac.get(r.recommended_action, 0)  + 1
            t_comp   += r.legal_composite
            t_comp_s += r.compliance_score_out
            t_lit    += r.litigation_score
            t_lic    += r.licensing_score
            t_reg    += r.regulatory_score
            t_idx    += r.estimated_legal_risk_index
            if r.has_legal_exposure:         exp_c  += 1
            if r.requires_immediate_counsel: coun_c += 1
        return {
            "total":                          n,
            "risk_counts":                    rc,
            "pattern_counts":                 pc,
            "severity_counts":                sc,
            "action_counts":                  ac,
            "avg_legal_composite":            round(t_comp / n, 1),
            "legal_exposure_count":           exp_c,
            "immediate_counsel_count":        coun_c,
            "avg_compliance_score":           round(t_comp_s / n, 1),
            "avg_litigation_score":           round(t_lit / n, 1),
            "avg_licensing_score":            round(t_lic / n, 1),
            "avg_regulatory_score":           round(t_reg / n, 1),
            "avg_estimated_legal_risk_index": round(t_idx / n, 2),
        }


# ── mock data & smoke test ────────────────────────────────────────────────────

def _mock_jurisdictions() -> List[LegalInput]:
    return [
        LegalInput(
            jurisdiction_id="LR-001", domain="tax", region="EMEA",
            compliance_score=0.15, regulatory_change_velocity=0.80,
            pending_regulatory_deadlines=5, missed_filing_count=6,
            litigation_pending_count=3, litigation_loss_rate=0.70,
            licensing_expiry_days=0, license_coverage_pct=0.60,
            cross_border_conflict_score=0.50, trade_restriction_exposure=0.40,
            environmental_penalty_risk=0.20, labor_law_violation_count=1,
            data_privacy_gap_score=0.55, contract_enforceability_score=0.50,
            internal_legal_capacity_score=0.30, regulatory_relationship_score=0.25,
            legal_spend_efficiency_score=0.35,
        ),
        LegalInput(
            jurisdiction_id="LR-002", domain="labor", region="NAMER",
            compliance_score=0.97, regulatory_change_velocity=0.10,
            pending_regulatory_deadlines=0, missed_filing_count=0,
            litigation_pending_count=0, litigation_loss_rate=0.00,
            licensing_expiry_days=365, license_coverage_pct=0.99,
            cross_border_conflict_score=0.05, trade_restriction_exposure=0.05,
            environmental_penalty_risk=0.02, labor_law_violation_count=0,
            data_privacy_gap_score=0.05, contract_enforceability_score=0.96,
            internal_legal_capacity_score=0.92, regulatory_relationship_score=0.95,
            legal_spend_efficiency_score=0.90,
        ),
        LegalInput(
            jurisdiction_id="LR-003", domain="data_privacy", region="APAC",
            compliance_score=0.55, regulatory_change_velocity=0.82,
            pending_regulatory_deadlines=7, missed_filing_count=1,
            litigation_pending_count=1, litigation_loss_rate=0.20,
            licensing_expiry_days=120, license_coverage_pct=0.80,
            cross_border_conflict_score=0.65, trade_restriction_exposure=0.45,
            environmental_penalty_risk=0.15, labor_law_violation_count=0,
            data_privacy_gap_score=0.62, contract_enforceability_score=0.70,
            internal_legal_capacity_score=0.55, regulatory_relationship_score=0.60,
            legal_spend_efficiency_score=0.65,
        ),
        LegalInput(
            jurisdiction_id="LR-004", domain="financial", region="LATAM",
            compliance_score=0.94, regulatory_change_velocity=0.15,
            pending_regulatory_deadlines=1, missed_filing_count=0,
            litigation_pending_count=0, litigation_loss_rate=0.00,
            licensing_expiry_days=280, license_coverage_pct=0.97,
            cross_border_conflict_score=0.08, trade_restriction_exposure=0.10,
            environmental_penalty_risk=0.05, labor_law_violation_count=0,
            data_privacy_gap_score=0.08, contract_enforceability_score=0.92,
            internal_legal_capacity_score=0.88, regulatory_relationship_score=0.92,
            legal_spend_efficiency_score=0.85,
        ),
        LegalInput(
            jurisdiction_id="LR-005", domain="trade", region="EMEA",
            compliance_score=0.60, regulatory_change_velocity=0.55,
            pending_regulatory_deadlines=3, missed_filing_count=1,
            litigation_pending_count=2, litigation_loss_rate=0.60,
            licensing_expiry_days=90, license_coverage_pct=0.70,
            cross_border_conflict_score=0.82, trade_restriction_exposure=0.78,
            environmental_penalty_risk=0.20, labor_law_violation_count=0,
            data_privacy_gap_score=0.25, contract_enforceability_score=0.55,
            internal_legal_capacity_score=0.45, regulatory_relationship_score=0.40,
            legal_spend_efficiency_score=0.50,
        ),
        LegalInput(
            jurisdiction_id="LR-006", domain="environmental", region="NAMER",
            compliance_score=0.70, regulatory_change_velocity=0.65,
            pending_regulatory_deadlines=3, missed_filing_count=1,
            litigation_pending_count=0, litigation_loss_rate=0.10,
            licensing_expiry_days=180, license_coverage_pct=0.85,
            cross_border_conflict_score=0.20, trade_restriction_exposure=0.25,
            environmental_penalty_risk=0.45, labor_law_violation_count=0,
            data_privacy_gap_score=0.20, contract_enforceability_score=0.78,
            internal_legal_capacity_score=0.70, regulatory_relationship_score=0.68,
            legal_spend_efficiency_score=0.72,
        ),
        LegalInput(
            jurisdiction_id="LR-007", domain="healthcare", region="APAC",
            compliance_score=0.68, regulatory_change_velocity=0.50,
            pending_regulatory_deadlines=2, missed_filing_count=2,
            litigation_pending_count=1, litigation_loss_rate=0.25,
            licensing_expiry_days=15, license_coverage_pct=0.45,
            cross_border_conflict_score=0.30, trade_restriction_exposure=0.20,
            environmental_penalty_risk=0.10, labor_law_violation_count=2,
            data_privacy_gap_score=0.38, contract_enforceability_score=0.65,
            internal_legal_capacity_score=0.50, regulatory_relationship_score=0.55,
            legal_spend_efficiency_score=0.60,
        ),
        LegalInput(
            jurisdiction_id="LR-008", domain="tax", region="MEA",
            compliance_score=0.28, regulatory_change_velocity=0.60,
            pending_regulatory_deadlines=4, missed_filing_count=3,
            litigation_pending_count=7, litigation_loss_rate=0.72,
            licensing_expiry_days=45, license_coverage_pct=0.65,
            cross_border_conflict_score=0.40, trade_restriction_exposure=0.35,
            environmental_penalty_risk=0.15, labor_law_violation_count=1,
            data_privacy_gap_score=0.50, contract_enforceability_score=0.30,
            internal_legal_capacity_score=0.25, regulatory_relationship_score=0.20,
            legal_spend_efficiency_score=0.30,
        ),
    ]


if __name__ == "__main__":
    engine = LegalRegulatoryWatchEngine()
    results = engine.assess_batch(_mock_jurisdictions())
    print("=== LegalRegulatoryWatchEngine Smoke Test ===")
    for r in results:
        d = r.to_dict()
        assert len(d) == 15, f"Expected 15 keys, got {len(d)}"
        print(
            f"{r.jurisdiction_id}  risk={r.legal_risk:<8}  pattern={r.regulatory_pattern:<22}"
            f"  composite={r.legal_composite:5.1f}  action={r.recommended_action}"
        )
    s = engine.summary()
    assert len(s) == 13, f"Expected 13 summary keys, got {len(s)}"
    print(f"\nSummary ({len(s)} keys): {s}")
    print("PASSED")
