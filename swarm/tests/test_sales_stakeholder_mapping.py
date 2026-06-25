"""
Tests for SalesStakeholderMappingIntelligenceEngine
"""
import pytest
from dataclasses import fields as dc_fields
from intelligence.sales_stakeholder_mapping_intelligence_engine import (
    SalesStakeholderMappingIntelligenceEngine,
    StakeholderMappingInput,
    StakeholderMappingResult,
    StakeholderRisk,
    StakeholderPattern,
    StakeholderSeverity,
    StakeholderAction,
)


@pytest.fixture
def engine():
    return SalesStakeholderMappingIntelligenceEngine()


@pytest.fixture
def healthy_input():
    return StakeholderMappingInput(
        total_stakeholders_identified=6,
        stakeholders_actively_engaged=5,
        economic_buyers_identified=2,
        economic_buyers_engaged=2,
        champions_identified=2,
        champion_strength_score=80.0,
        blockers_identified=1,
        blockers_mapped=1,
        executive_contacts=2,
        executive_meetings_last_30d=2,
        technical_contacts=2,
        end_user_contacts=1,
        days_since_last_contact_avg=7.0,
        deal_value=80000.0,
        deal_stage=4,
        multi_threaded=True,
        buying_committee_size_estimate=7,
        stakeholder_sentiment_avg=80.0,
        internal_sponsor=True,
        procurement_contact=True,
        legal_contact=False,
        finance_contact=True,
    )


@pytest.fixture
def risky_input():
    return StakeholderMappingInput(
        total_stakeholders_identified=1,
        stakeholders_actively_engaged=1,
        economic_buyers_identified=1,
        economic_buyers_engaged=0,
        champions_identified=0,
        champion_strength_score=20.0,
        blockers_identified=2,
        blockers_mapped=0,
        executive_contacts=0,
        executive_meetings_last_30d=0,
        technical_contacts=0,
        end_user_contacts=1,
        days_since_last_contact_avg=30.0,
        deal_value=100000.0,
        deal_stage=4,
        multi_threaded=False,
        buying_committee_size_estimate=8,
        stakeholder_sentiment_avg=40.0,
        internal_sponsor=False,
        procurement_contact=False,
        legal_contact=False,
        finance_contact=False,
    )


# ── Result structure ──────────────────────────────────────────────────────────

class TestResultStructure:
    def test_result_has_15_fields(self):
        assert len(dc_fields(StakeholderMappingResult)) == 15

    def test_to_dict_has_15_keys(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert len(r.to_dict()) == 15

    def test_to_dict_keys(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        expected = {
            "composite_score", "risk", "pattern", "severity", "action",
            "coverage_breadth_score", "buyer_alignment_score",
            "champion_development_score", "executive_access_score",
            "has_stakeholder_gap", "requires_stakeholder_coaching",
            "estimated_deal_risk", "signal",
            "coverage_ratio", "champion_score",
        }
        assert set(d.keys()) == expected


# ── Healthy deal ──────────────────────────────────────────────────────────────

class TestHealthyDeal:
    def test_healthy_returns_low_risk(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.risk == StakeholderRisk.low

    def test_healthy_returns_engaged_severity(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.severity == StakeholderSeverity.engaged

    def test_healthy_composite_above_75(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.composite_score >= 75

    def test_healthy_signal_contains_healthy(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert "healthy" in r.signal.lower()

    def test_healthy_action_maintain(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.action == StakeholderAction.maintain


# ── Risky deal ────────────────────────────────────────────────────────────────

class TestRiskyDeal:
    def test_risky_returns_high_or_critical(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.risk in (StakeholderRisk.high, StakeholderRisk.critical)

    def test_risky_composite_below_55(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.composite_score < 55

    def test_risky_has_stakeholder_gap(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.has_stakeholder_gap

    def test_risky_requires_coaching(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.requires_stakeholder_coaching

    def test_risky_deal_risk_positive(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.estimated_deal_risk > 0


# ── Score boundaries ──────────────────────────────────────────────────────────

class TestScoreBoundaries:
    def test_composite_between_0_and_100(self, engine):
        for inp in [
            StakeholderMappingInput(),
            StakeholderMappingInput(buying_committee_size_estimate=0),
            StakeholderMappingInput(champions_identified=0, champion_strength_score=0.0),
        ]:
            r = engine.assess(inp)
            assert 0.0 <= r.composite_score <= 100.0

    def test_sub_scores_bounded(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        for score in [r.coverage_breadth_score, r.buyer_alignment_score,
                      r.champion_development_score, r.executive_access_score]:
            assert 0.0 <= score <= 100.0

    def test_zero_committee_does_not_crash(self, engine):
        r = engine.assess(StakeholderMappingInput(buying_committee_size_estimate=0))
        assert isinstance(r, StakeholderMappingResult)


# ── Pattern detection ─────────────────────────────────────────────────────────

class TestPatternDetection:
    def test_single_threaded_detected(self, engine):
        inp = StakeholderMappingInput(
            multi_threaded=False,
            total_stakeholders_identified=1,
        )
        r = engine.assess(inp)
        assert r.pattern == StakeholderPattern.single_threaded

    def test_champion_missing_detected(self, engine):
        inp = StakeholderMappingInput(
            multi_threaded=True,
            total_stakeholders_identified=4,
            champions_identified=0,
            champion_strength_score=0.0,
        )
        r = engine.assess(inp)
        assert r.pattern == StakeholderPattern.champion_missing

    def test_executive_blind_spot_detected(self, engine):
        inp = StakeholderMappingInput(
            multi_threaded=True,
            total_stakeholders_identified=4,
            champions_identified=1,
            champion_strength_score=70.0,
            executive_contacts=0,
            executive_meetings_last_30d=0,
        )
        r = engine.assess(inp)
        assert r.pattern == StakeholderPattern.executive_blind_spot

    def test_blocker_unmapped_detected(self, engine):
        inp = StakeholderMappingInput(
            multi_threaded=True,
            total_stakeholders_identified=4,
            champions_identified=1,
            champion_strength_score=70.0,
            executive_contacts=2,
            executive_meetings_last_30d=1,
            blockers_identified=2,
            blockers_mapped=0,
        )
        r = engine.assess(inp)
        assert r.pattern == StakeholderPattern.blocker_unmapped


# ── Risk and severity mapping ─────────────────────────────────────────────────

class TestRiskAndSeverity:
    def test_severity_maps_correctly(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        severity_map = {
            StakeholderRisk.low: StakeholderSeverity.engaged,
            StakeholderRisk.moderate: StakeholderSeverity.developing,
            StakeholderRisk.high: StakeholderSeverity.fragile,
            StakeholderRisk.critical: StakeholderSeverity.exposed,
        }
        assert r.severity == severity_map[r.risk]

    def test_deal_risk_positive_when_score_low(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.estimated_deal_risk > 0


# ── Batch and summary ─────────────────────────────────────────────────────────

class TestBatchAndSummary:
    def test_batch_processes_all(self, engine, healthy_input, risky_input):
        results = engine.batch([healthy_input, risky_input])
        assert len(results) == 2

    def test_summary_13_keys(self, engine, healthy_input, risky_input):
        results = engine.batch([healthy_input, risky_input])
        s = engine.summary(results)
        assert len(s) == 13

    def test_summary_empty_returns_empty_dict(self, engine):
        assert engine.summary([]) == {}

    def test_summary_total_deals(self, engine, healthy_input, risky_input):
        results = engine.batch([healthy_input, risky_input])
        s = engine.summary(results)
        assert s["total_deals"] == 2

    def test_summary_avg_score_between_0_and_100(self, engine, healthy_input, risky_input):
        results = engine.batch([healthy_input, risky_input])
        s = engine.summary(results)
        assert 0 <= s["avg_composite_score"] <= 100


# ── Enum validation ───────────────────────────────────────────────────────────

class TestEnums:
    def test_stakeholder_risk_values(self):
        assert set(StakeholderRisk) == {StakeholderRisk.low, StakeholderRisk.moderate, StakeholderRisk.high, StakeholderRisk.critical}

    def test_stakeholder_pattern_values(self):
        patterns = {p.value for p in StakeholderPattern}
        assert "none" in patterns
        assert "single_threaded" in patterns
        assert "champion_missing" in patterns

    def test_stakeholder_action_values(self):
        actions = {a.value for a in StakeholderAction}
        assert "maintain" in actions
        assert "build_champion" in actions
        assert "expand_contacts" in actions

    def test_result_action_is_valid_enum(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.action in StakeholderAction

    def test_result_risk_is_valid_enum(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.risk in StakeholderRisk

    def test_coverage_ratio_between_0_and_2(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert 0.0 <= r.coverage_ratio <= 2.0

    def test_champion_score_from_input(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.champion_score == healthy_input.champion_strength_score
