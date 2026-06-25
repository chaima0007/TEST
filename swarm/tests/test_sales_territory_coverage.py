"""
Tests for SalesTerritoryCoverageIntelligenceEngine
"""
import pytest
from dataclasses import fields as dc_fields
from intelligence.sales_territory_coverage_intelligence_engine import (
    SalesTerritoryCoverageIntelligenceEngine,
    SalesTerritoryConverageIntelligenceEngine,
    TerritoryCoverageInput,
    TerritoryCoverageResult,
    CoverageRisk,
    CoveragePattern,
    CoverageSeverity,
    CoverageAction,
)


@pytest.fixture
def engine():
    return SalesTerritoryCoverageIntelligenceEngine()


@pytest.fixture
def healthy_input():
    return TerritoryCoverageInput(
        total_accounts=100,
        active_accounts=85,
        whitespace_accounts=5,
        churned_accounts_last_90d=2,
        top_account_revenue_pct=20.0,
        geographic_zones=4,
        zones_with_activity=4,
        avg_visits_per_account=3.5,
        accounts_no_contact_90d=5,
        new_accounts_added=12,
        accounts_at_risk=5,
        total_revenue=600000.0,
        top_3_accounts_revenue=100000.0,
        segment_a_coverage_pct=90.0,
        segment_b_coverage_pct=80.0,
        segment_c_coverage_pct=70.0,
        competitor_wins_in_territory=1,
        pipeline_coverage_ratio=3.0,
        territory_quota=600000.0,
        quota_attainment_pct=100.0,
        expansion_opportunities=20,
        account_health_score_avg=82.0,
    )


@pytest.fixture
def risky_input():
    return TerritoryCoverageInput(
        total_accounts=100,
        active_accounts=40,
        whitespace_accounts=50,
        churned_accounts_last_90d=15,
        top_account_revenue_pct=70.0,
        geographic_zones=6,
        zones_with_activity=2,
        avg_visits_per_account=1.0,
        accounts_no_contact_90d=30,
        new_accounts_added=1,
        accounts_at_risk=25,
        total_revenue=200000.0,
        top_3_accounts_revenue=130000.0,
        segment_a_coverage_pct=50.0,
        segment_b_coverage_pct=30.0,
        segment_c_coverage_pct=10.0,
        competitor_wins_in_territory=8,
        pipeline_coverage_ratio=1.0,
        territory_quota=500000.0,
        quota_attainment_pct=40.0,
        expansion_opportunities=5,
        account_health_score_avg=40.0,
    )


# ── Result structure ──────────────────────────────────────────────────────────

class TestResultStructure:
    def test_result_has_15_fields(self):
        assert len(dc_fields(TerritoryCoverageResult)) == 15

    def test_to_dict_has_15_keys(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert len(r.to_dict()) == 15

    def test_to_dict_keys(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        expected = {
            "composite_score", "risk", "pattern", "severity", "action",
            "account_breadth_score", "account_prioritization_score",
            "whitespace_exploitation_score", "churn_prevention_score",
            "has_coverage_gap", "requires_territory_rebalance",
            "estimated_revenue_at_risk", "signal",
            "coverage_gap_pct", "whitespace_penetration_pct",
        }
        assert set(d.keys()) == expected


# ── Healthy territory ─────────────────────────────────────────────────────────

class TestHealthyTerritory:
    def test_healthy_returns_low_risk(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.risk == CoverageRisk.low

    def test_healthy_returns_optimal_severity(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.severity == CoverageSeverity.optimal

    def test_healthy_composite_above_75(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.composite_score >= 75

    def test_healthy_no_coverage_gap(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert not r.has_coverage_gap

    def test_healthy_signal_contains_healthy(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert "healthy" in r.signal.lower()

    def test_healthy_action_maintain(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.action == CoverageAction.maintain


# ── Risky territory ───────────────────────────────────────────────────────────

class TestRiskyTerritory:
    def test_risky_returns_high_or_critical(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.risk in (CoverageRisk.high, CoverageRisk.critical)

    def test_risky_composite_below_55(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.composite_score < 55

    def test_risky_has_coverage_gap(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.has_coverage_gap

    def test_risky_requires_rebalance(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.requires_territory_rebalance

    def test_risky_revenue_at_risk_positive(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.estimated_revenue_at_risk > 0


# ── Score boundaries ──────────────────────────────────────────────────────────

class TestScoreBoundaries:
    def test_composite_between_0_and_100(self, engine):
        for inp in [
            TerritoryCoverageInput(),
            TerritoryCoverageInput(total_accounts=0),
            TerritoryCoverageInput(active_accounts=0, whitespace_accounts=100, churned_accounts_last_90d=50),
        ]:
            r = engine.assess(inp)
            assert 0.0 <= r.composite_score <= 100.0

    def test_sub_scores_bounded(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        for score in [r.account_breadth_score, r.account_prioritization_score,
                      r.whitespace_exploitation_score, r.churn_prevention_score]:
            assert 0.0 <= score <= 100.0

    def test_zero_accounts_does_not_crash(self, engine):
        r = engine.assess(TerritoryCoverageInput(total_accounts=0))
        assert isinstance(r, TerritoryCoverageResult)


# ── Pattern detection ─────────────────────────────────────────────────────────

class TestPatternDetection:
    def test_top_heavy_detected(self, engine):
        inp = TerritoryCoverageInput(
            total_revenue=100000.0,
            top_3_accounts_revenue=60000.0,
        )
        r = engine.assess(inp)
        assert r.pattern == CoveragePattern.top_heavy_territory

    def test_geographic_concentration_detected(self, engine):
        inp = TerritoryCoverageInput(
            geographic_zones=6,
            zones_with_activity=2,
            top_3_accounts_revenue=10000.0,
            total_revenue=100000.0,
        )
        r = engine.assess(inp)
        assert r.pattern == CoveragePattern.geographic_concentration

    def test_whitespace_neglect_detected(self, engine):
        inp = TerritoryCoverageInput(
            total_accounts=100,
            whitespace_accounts=80,
            geographic_zones=4,
            zones_with_activity=4,
            top_3_accounts_revenue=20000.0,
            total_revenue=100000.0,
        )
        r = engine.assess(inp)
        assert r.pattern == CoveragePattern.whitespace_neglect


# ── Risk tiers ────────────────────────────────────────────────────────────────

class TestRiskTiers:
    def test_risk_low_when_score_75_plus(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        if r.composite_score >= 75:
            assert r.risk == CoverageRisk.low

    def test_severity_maps_risk(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        severity_map = {
            CoverageRisk.low: CoverageSeverity.optimal,
            CoverageRisk.moderate: CoverageSeverity.suboptimal,
            CoverageRisk.high: CoverageSeverity.degraded,
            CoverageRisk.critical: CoverageSeverity.critical,
        }
        assert r.severity == severity_map[r.risk]


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

    def test_summary_total_territories(self, engine, healthy_input, risky_input):
        results = engine.batch([healthy_input, risky_input])
        s = engine.summary(results)
        assert s["total_territories"] == 2

    def test_summary_avg_score_between_0_and_100(self, engine, healthy_input, risky_input):
        results = engine.batch([healthy_input, risky_input])
        s = engine.summary(results)
        assert 0 <= s["avg_composite_score"] <= 100


# ── Alias ─────────────────────────────────────────────────────────────────────

class TestAlias:
    def test_alias_exists(self):
        assert SalesTerritoryConverageIntelligenceEngine is SalesTerritoryCoverageIntelligenceEngine

    def test_alias_works(self, healthy_input):
        engine = SalesTerritoryConverageIntelligenceEngine()
        r = engine.assess(healthy_input)
        assert isinstance(r, TerritoryCoverageResult)


# ── Enum values ───────────────────────────────────────────────────────────────

class TestEnums:
    def test_coverage_risk_values(self):
        assert set(CoverageRisk) == {CoverageRisk.low, CoverageRisk.moderate, CoverageRisk.high, CoverageRisk.critical}

    def test_coverage_pattern_values(self):
        patterns = {p.value for p in CoveragePattern}
        assert "none" in patterns
        assert "geographic_concentration" in patterns
        assert "whitespace_neglect" in patterns

    def test_coverage_action_values(self):
        actions = {a.value for a in CoverageAction}
        assert "maintain" in actions
        assert "expand_whitespace" in actions
        assert "rebalance_territory" in actions

    def test_action_values_in_result(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.action in CoverageAction

    def test_risk_values_in_result(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.risk in CoverageRisk

    def test_pattern_values_in_result(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.pattern in CoveragePattern
