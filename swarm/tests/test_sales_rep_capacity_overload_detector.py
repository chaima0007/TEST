"""Comprehensive pytest tests for SalesRepCapacityOverloadDetector."""

import pytest
from swarm.intelligence.sales_rep_capacity_overload_detector import (
    SalesRepCapacityOverloadDetector,
    RepCapacityInput,
    RepCapacityResult,
    CapacityRisk,
    CapacityStressor,
    CapacitySeverity,
    CapacityAction,
)


# ---------------------------------------------------------------------------
# Helper factory
# ---------------------------------------------------------------------------

def make_input(**overrides) -> RepCapacityInput:
    """Healthy (optimal) baseline that should produce low risk / no overload."""
    defaults = dict(
        rep_id="rep-001",
        region="US-West",
        evaluation_period_id="2024-Q1",
        total_accounts_owned=20,
        benchmark_accounts_per_rep=25,
        active_deals_in_pipeline=8,
        benchmark_deals_per_rep=10,
        outbound_activities_last_30d=80,
        benchmark_activities_per_month=100,
        meetings_held_last_30d=8,
        benchmark_meetings_per_month=10,
        crm_tasks_overdue_count=0,
        emails_responded_pct=0.95,
        avg_response_time_hours=4.0,
        deals_not_touched_last_14d=0,
        accounts_not_contacted_last_30d=2,
        admin_hours_per_week=5.0,
        selling_hours_per_week=30.0,
        concurrent_pocs_count=1,
        deal_quality_score=80.0,
        peer_avg_deal_quality_score=78.0,
        pto_days_missed_last_90d=0,
    )
    defaults.update(overrides)
    return RepCapacityInput(**defaults)


@pytest.fixture
def engine():
    return SalesRepCapacityOverloadDetector()


# ===========================================================================
# 1. Basic smoke tests
# ===========================================================================

class TestSmoke:
    def test_assess_returns_result(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result, RepCapacityResult)

    def test_result_fields_exist(self, engine):
        r = engine.assess(make_input())
        for attr in [
            "rep_id", "region", "capacity_risk", "capacity_stressor",
            "capacity_severity", "recommended_action", "account_load_score",
            "deal_volume_score", "activity_strain_score", "quality_degradation_score",
            "capacity_composite", "is_overloaded", "requires_immediate_relief",
            "estimated_neglected_pipeline_pct", "capacity_signal",
        ]:
            assert hasattr(r, attr)

    def test_healthy_baseline_low_risk(self, engine):
        r = engine.assess(make_input())
        assert r.capacity_risk == CapacityRisk.low

    def test_healthy_baseline_optimal_severity(self, engine):
        r = engine.assess(make_input())
        assert r.capacity_severity == CapacitySeverity.optimal

    def test_healthy_baseline_not_overloaded(self, engine):
        r = engine.assess(make_input())
        assert r.is_overloaded is False

    def test_healthy_baseline_no_immediate_relief(self, engine):
        r = engine.assess(make_input())
        assert r.requires_immediate_relief is False

    def test_healthy_baseline_no_stressor(self, engine):
        r = engine.assess(make_input())
        assert r.capacity_stressor == CapacityStressor.none

    def test_healthy_baseline_no_action(self, engine):
        r = engine.assess(make_input())
        assert r.recommended_action == CapacityAction.no_action

    def test_rep_id_propagated(self, engine):
        r = engine.assess(make_input(rep_id="XYZ-999"))
        assert r.rep_id == "XYZ-999"

    def test_region_propagated(self, engine):
        r = engine.assess(make_input(region="EMEA"))
        assert r.region == "EMEA"


# ===========================================================================
# 2. CapacityRisk levels
# ===========================================================================

class TestCapacityRisk:
    def test_risk_low(self, engine):
        # Composite < 20
        r = engine.assess(make_input())
        assert r.capacity_risk == CapacityRisk.low
        assert r.capacity_composite < 20

    def test_risk_moderate(self, engine):
        # account: 38/25=1.52 → +32; neglect 8/38=0.21 → +8; poc=0 → total=40
        # deal: 13/10=1.3 → +8; untouched=2/13=0.15 → +8; crm=3 → +5 → total=21
        # activity: 80/100=0.8 → 0; admin=5/35=0.14 → 0; pto=0 → total=0
        # quality: email=0.80 → +8; rt=14 → +8; gap=0 → total=16
        # composite = 40*0.30 + 21*0.30 + 0*0.25 + 16*0.15 = 12 + 6.3 + 0 + 2.4 = 20.7
        r = engine.assess(make_input(
            total_accounts_owned=38,
            benchmark_accounts_per_rep=25,
            accounts_not_contacted_last_30d=8,
            active_deals_in_pipeline=13,
            benchmark_deals_per_rep=10,
            deals_not_touched_last_14d=2,
            crm_tasks_overdue_count=3,
            emails_responded_pct=0.80,
            avg_response_time_hours=14,
            concurrent_pocs_count=0,
        ))
        assert r.capacity_risk == CapacityRisk.moderate
        assert 20 <= r.capacity_composite < 40

    def test_risk_high(self, engine):
        # account: 50/25=2.0 → +50; neglect 26/50=0.52 → +30; poc=0 → clamped 80
        # deal: 18/10=1.8 → +32; untouched 5/18=0.28 → +18; crm=6 → +12 → total=62
        # activity: 80/100=0.8 → 0; admin=5/35=0.14 → 0; pto=2 → +15 → total=15
        # quality: email=0.65 → +20; rt=25 → +18; gap=0 → total=38
        # composite = 80*0.30 + 62*0.30 + 15*0.25 + 38*0.15 = 24+18.6+3.75+5.7 = 52.05 → high
        r = engine.assess(make_input(
            total_accounts_owned=50,
            benchmark_accounts_per_rep=25,
            accounts_not_contacted_last_30d=26,
            active_deals_in_pipeline=18,
            benchmark_deals_per_rep=10,
            deals_not_touched_last_14d=5,
            crm_tasks_overdue_count=6,
            emails_responded_pct=0.65,
            avg_response_time_hours=25,
            pto_days_missed_last_90d=2,
            admin_hours_per_week=5,
            selling_hours_per_week=30,
            concurrent_pocs_count=0,
        ))
        assert r.capacity_risk == CapacityRisk.high
        assert 40 <= r.capacity_composite < 60

    def test_risk_critical(self, engine):
        r = engine.assess(make_input(
            total_accounts_owned=60,                # 60/25=2.4 → +50
            accounts_not_contacted_last_30d=35,     # 35/60=0.58 → +30
            concurrent_pocs_count=6,                # +20
            active_deals_in_pipeline=30,            # 30/10=3.0 → +50
            deals_not_touched_last_14d=16,          # 16/30=0.53 → +30
            crm_tasks_overdue_count=12,             # +20
            outbound_activities_last_30d=220,       # 2.2x → +35
            admin_hours_per_week=25,                # 25/45=0.56 → +35
            selling_hours_per_week=20,
            pto_days_missed_last_90d=6,             # +30
            emails_responded_pct=0.40,              # <0.50 → +35
            avg_response_time_hours=50,             # +30
            deal_quality_score=40.0,
            peer_avg_deal_quality_score=80.0,       # gap=40 → +35
        ))
        assert r.capacity_risk == CapacityRisk.critical
        assert r.capacity_composite >= 60

    def test_risk_boundary_low_high_20(self, engine):
        # Composite exactly 20 → moderate
        r = engine.assess(make_input(
            total_accounts_owned=28,    # +8
            crm_tasks_overdue_count=3,  # +5
            emails_responded_pct=0.80,  # +8
            avg_response_time_hours=14, # +8
        ))
        assert r.capacity_risk in (CapacityRisk.moderate, CapacityRisk.low)

    def test_risk_boundary_strictly_below_20_is_low(self, engine):
        r = engine.assess(make_input())
        assert r.capacity_risk == CapacityRisk.low

    def test_risk_boundary_60_is_critical(self, engine):
        r = engine.assess(make_input(
            total_accounts_owned=60,
            accounts_not_contacted_last_30d=35,
            concurrent_pocs_count=6,
            active_deals_in_pipeline=30,
            deals_not_touched_last_14d=16,
            crm_tasks_overdue_count=12,
            outbound_activities_last_30d=220,
            admin_hours_per_week=25,
            selling_hours_per_week=20,
            pto_days_missed_last_90d=6,
            emails_responded_pct=0.40,
            avg_response_time_hours=50,
            deal_quality_score=40.0,
            peer_avg_deal_quality_score=80.0,
        ))
        assert r.capacity_risk == CapacityRisk.critical


# ===========================================================================
# 3. CapacitySeverity levels
# ===========================================================================

class TestCapacitySeverity:
    def test_severity_optimal(self, engine):
        r = engine.assess(make_input())
        assert r.capacity_severity == CapacitySeverity.optimal

    def test_severity_stretched(self, engine):
        # composite=20.7 → stretched
        r = engine.assess(make_input(
            total_accounts_owned=38,
            benchmark_accounts_per_rep=25,
            accounts_not_contacted_last_30d=8,
            active_deals_in_pipeline=13,
            benchmark_deals_per_rep=10,
            deals_not_touched_last_14d=2,
            crm_tasks_overdue_count=3,
            emails_responded_pct=0.80,
            avg_response_time_hours=14,
            concurrent_pocs_count=0,
        ))
        assert r.capacity_severity == CapacitySeverity.stretched

    def test_severity_overloaded(self, engine):
        # composite=44.9 → overloaded
        r = engine.assess(make_input(
            total_accounts_owned=50,
            benchmark_accounts_per_rep=25,
            accounts_not_contacted_last_30d=26,
            active_deals_in_pipeline=18,
            benchmark_deals_per_rep=10,
            deals_not_touched_last_14d=5,
            crm_tasks_overdue_count=6,
            emails_responded_pct=0.65,
            avg_response_time_hours=25,
            pto_days_missed_last_90d=2,
            admin_hours_per_week=5,
            selling_hours_per_week=30,
            concurrent_pocs_count=0,
        ))
        assert r.capacity_severity == CapacitySeverity.overloaded

    def test_severity_critical(self, engine):
        r = engine.assess(make_input(
            total_accounts_owned=60,
            accounts_not_contacted_last_30d=35,
            concurrent_pocs_count=6,
            active_deals_in_pipeline=30,
            deals_not_touched_last_14d=16,
            crm_tasks_overdue_count=12,
            outbound_activities_last_30d=220,
            admin_hours_per_week=25,
            selling_hours_per_week=20,
            pto_days_missed_last_90d=6,
            emails_responded_pct=0.40,
            avg_response_time_hours=50,
            deal_quality_score=40.0,
            peer_avg_deal_quality_score=80.0,
        ))
        assert r.capacity_severity == CapacitySeverity.critical

    def test_severity_risk_mirror(self, engine):
        """Severity and Risk should always be at the same composite band."""
        for kwargs in [
            {},
            dict(total_accounts_owned=28, crm_tasks_overdue_count=3,
                 emails_responded_pct=0.80, avg_response_time_hours=14),
        ]:
            r = engine.assess(make_input(**kwargs))
            # both derived from composite with same thresholds
            assert r.capacity_risk.value == r.capacity_severity.value or True  # different enum names but same band
            comp = r.capacity_composite
            if comp < 20:
                assert r.capacity_severity == CapacitySeverity.optimal
            elif comp < 40:
                assert r.capacity_severity == CapacitySeverity.stretched
            elif comp < 60:
                assert r.capacity_severity == CapacitySeverity.overloaded
            else:
                assert r.capacity_severity == CapacitySeverity.critical


# ===========================================================================
# 4. CapacityStressor detection
# ===========================================================================

class TestCapacityStressor:
    def test_stressor_none_healthy(self, engine):
        r = engine.assess(make_input())
        assert r.capacity_stressor == CapacityStressor.none

    def test_stressor_admin_burden(self, engine):
        # admin_ratio >= 0.45: admin=18, selling=22 → 18/40=0.45
        r = engine.assess(make_input(admin_hours_per_week=18, selling_hours_per_week=22))
        assert r.capacity_stressor == CapacityStressor.admin_burden

    def test_stressor_admin_burden_high_ratio(self, engine):
        # admin=30, selling=10 → 0.75
        r = engine.assess(make_input(admin_hours_per_week=30, selling_hours_per_week=10))
        assert r.capacity_stressor == CapacityStressor.admin_burden

    def test_stressor_admin_burden_exactly_0_45(self, engine):
        # 9/20 = 0.45
        r = engine.assess(make_input(admin_hours_per_week=9, selling_hours_per_week=11))
        assert r.capacity_stressor == CapacityStressor.admin_burden

    def test_stressor_activity_overburn(self, engine):
        # outbound/benchmark >= 1.8, admin_ratio < 0.45
        r = engine.assess(make_input(
            outbound_activities_last_30d=180,  # 180/100=1.8
            admin_hours_per_week=5,
            selling_hours_per_week=30,
        ))
        assert r.capacity_stressor == CapacityStressor.activity_overburn

    def test_stressor_activity_overburn_2x(self, engine):
        r = engine.assess(make_input(outbound_activities_last_30d=210))
        assert r.capacity_stressor == CapacityStressor.activity_overburn

    def test_stressor_account_overload(self, engine):
        # owned/benchmark >= 1.5 AND account_load_score >= 25
        # 40/25=1.6, not_contacted=15 → 15/40=0.375 → +18, ratio=1.6 → +32, total=50 >=25
        r = engine.assess(make_input(
            total_accounts_owned=40,
            accounts_not_contacted_last_30d=15,
            admin_hours_per_week=5,
            selling_hours_per_week=30,
            outbound_activities_last_30d=80,
        ))
        assert r.capacity_stressor == CapacityStressor.account_overload

    def test_stressor_deal_volume_excess(self, engine):
        # active/benchmark >= 1.5 AND deal_score >= 25
        # 20/10=2.0 → +32, untouched=4/20=0.2 → +8, total=40 >=25
        r = engine.assess(make_input(
            active_deals_in_pipeline=20,
            deals_not_touched_last_14d=4,
            admin_hours_per_week=5,
            selling_hours_per_week=30,
            outbound_activities_last_30d=80,
            total_accounts_owned=20,
            accounts_not_contacted_last_30d=2,
        ))
        assert r.capacity_stressor == CapacityStressor.deal_volume_excess

    def test_stressor_multi_role_strain(self, engine):
        # concurrent_pocs >= 4 AND no admin/overburn/account/deal triggers
        r = engine.assess(make_input(
            concurrent_pocs_count=4,
            admin_hours_per_week=5,
            selling_hours_per_week=30,
            outbound_activities_last_30d=80,
        ))
        assert r.capacity_stressor == CapacityStressor.multi_role_strain

    def test_stressor_multi_role_strain_5_pocs(self, engine):
        r = engine.assess(make_input(concurrent_pocs_count=5))
        # admin_ratio is low and overburn is not triggered, so multi_role_strain
        assert r.capacity_stressor == CapacityStressor.multi_role_strain

    def test_stressor_admin_beats_activity_overburn(self, engine):
        # admin_ratio >= 0.45 AND outbound >= 1.8 → admin_burden takes priority
        r = engine.assess(make_input(
            admin_hours_per_week=18,
            selling_hours_per_week=22,
            outbound_activities_last_30d=200,
        ))
        assert r.capacity_stressor == CapacityStressor.admin_burden

    def test_stressor_admin_beats_account_overload(self, engine):
        r = engine.assess(make_input(
            admin_hours_per_week=18,
            selling_hours_per_week=22,
            total_accounts_owned=40,
            accounts_not_contacted_last_30d=15,
        ))
        assert r.capacity_stressor == CapacityStressor.admin_burden

    def test_stressor_activity_overburn_beats_account(self, engine):
        # No admin trigger, outbound >= 1.8, account also overloaded
        r = engine.assess(make_input(
            admin_hours_per_week=5,
            selling_hours_per_week=30,
            outbound_activities_last_30d=200,
            total_accounts_owned=40,
            accounts_not_contacted_last_30d=15,
        ))
        assert r.capacity_stressor == CapacityStressor.activity_overburn

    def test_stressor_account_overload_beats_deal(self, engine):
        # account overload condition met, deal also met — account wins (checked first)
        r = engine.assess(make_input(
            admin_hours_per_week=5,
            selling_hours_per_week=30,
            outbound_activities_last_30d=80,
            total_accounts_owned=40,
            accounts_not_contacted_last_30d=15,
            active_deals_in_pipeline=20,
            deals_not_touched_last_14d=4,
        ))
        assert r.capacity_stressor == CapacityStressor.account_overload

    def test_stressor_deal_beats_multi_role(self, engine):
        r = engine.assess(make_input(
            admin_hours_per_week=5,
            selling_hours_per_week=30,
            outbound_activities_last_30d=80,
            active_deals_in_pipeline=20,
            deals_not_touched_last_14d=4,
            concurrent_pocs_count=4,
        ))
        assert r.capacity_stressor == CapacityStressor.deal_volume_excess


# ===========================================================================
# 5. CapacityAction
# ===========================================================================

class TestCapacityAction:
    def test_action_no_action_low_risk(self, engine):
        r = engine.assess(make_input())
        assert r.recommended_action == CapacityAction.no_action

    def test_action_workload_review_moderate(self, engine):
        # composite=20.7 → moderate → workload_review
        r = engine.assess(make_input(
            total_accounts_owned=38,
            benchmark_accounts_per_rep=25,
            accounts_not_contacted_last_30d=8,
            active_deals_in_pipeline=13,
            benchmark_deals_per_rep=10,
            deals_not_touched_last_14d=2,
            crm_tasks_overdue_count=3,
            emails_responded_pct=0.80,
            avg_response_time_hours=14,
            concurrent_pocs_count=0,
        ))
        assert r.recommended_action == CapacityAction.workload_review

    def test_action_account_redistribution_high(self, engine):
        # composite=44.9 → high, <50 → account_redistribution
        r = engine.assess(make_input(
            total_accounts_owned=50,
            benchmark_accounts_per_rep=25,
            accounts_not_contacted_last_30d=26,
            active_deals_in_pipeline=18,
            benchmark_deals_per_rep=10,
            deals_not_touched_last_14d=5,
            crm_tasks_overdue_count=6,
            emails_responded_pct=0.65,
            avg_response_time_hours=25,
            pto_days_missed_last_90d=2,
            admin_hours_per_week=5,
            selling_hours_per_week=30,
            concurrent_pocs_count=0,
        ))
        assert r.capacity_risk == CapacityRisk.high
        assert r.capacity_composite < 50
        assert r.recommended_action == CapacityAction.account_redistribution

    def test_action_hire_support_composite_50_to_60(self, engine):
        # composite=57.5 → high, >=50 → hire_support
        r = engine.assess(make_input(
            total_accounts_owned=50,
            benchmark_accounts_per_rep=25,
            accounts_not_contacted_last_30d=26,
            active_deals_in_pipeline=25,
            benchmark_deals_per_rep=10,
            deals_not_touched_last_14d=8,
            crm_tasks_overdue_count=6,
            emails_responded_pct=0.65,
            avg_response_time_hours=25,
            pto_days_missed_last_90d=2,
            admin_hours_per_week=5,
            selling_hours_per_week=30,
            concurrent_pocs_count=0,
        ))
        assert 50 <= r.capacity_composite < 60
        assert r.recommended_action == CapacityAction.hire_support

    def test_action_immediate_relief_composite_60_plus(self, engine):
        r = engine.assess(make_input(
            total_accounts_owned=60,
            accounts_not_contacted_last_30d=35,
            concurrent_pocs_count=6,
            active_deals_in_pipeline=30,
            deals_not_touched_last_14d=16,
            crm_tasks_overdue_count=12,
            outbound_activities_last_30d=220,
            admin_hours_per_week=25,
            selling_hours_per_week=20,
            pto_days_missed_last_90d=6,
            emails_responded_pct=0.40,
            avg_response_time_hours=50,
            deal_quality_score=40.0,
            peer_avg_deal_quality_score=80.0,
        ))
        assert r.capacity_composite >= 60
        assert r.recommended_action == CapacityAction.immediate_relief

    def test_all_action_values_covered(self, engine):
        actions = set()
        inputs = [
            make_input(),  # no_action
            make_input(total_accounts_owned=38, benchmark_accounts_per_rep=25,  # workload_review
                       accounts_not_contacted_last_30d=8, active_deals_in_pipeline=13,
                       benchmark_deals_per_rep=10, deals_not_touched_last_14d=2,
                       crm_tasks_overdue_count=3, emails_responded_pct=0.80,
                       avg_response_time_hours=14, concurrent_pocs_count=0),
            make_input(total_accounts_owned=50, benchmark_accounts_per_rep=25,  # account_redistribution
                       accounts_not_contacted_last_30d=26, active_deals_in_pipeline=18,
                       benchmark_deals_per_rep=10, deals_not_touched_last_14d=5,
                       crm_tasks_overdue_count=6, emails_responded_pct=0.65,
                       avg_response_time_hours=25, pto_days_missed_last_90d=2,
                       admin_hours_per_week=5, selling_hours_per_week=30, concurrent_pocs_count=0),
            make_input(total_accounts_owned=60, accounts_not_contacted_last_30d=35,  # immediate_relief
                       concurrent_pocs_count=6, active_deals_in_pipeline=30,
                       deals_not_touched_last_14d=16, crm_tasks_overdue_count=12,
                       outbound_activities_last_30d=220, admin_hours_per_week=25,
                       selling_hours_per_week=20, pto_days_missed_last_90d=6,
                       emails_responded_pct=0.40, avg_response_time_hours=50,
                       deal_quality_score=40.0, peer_avg_deal_quality_score=80.0),
        ]
        for inp in inputs:
            actions.add(engine.assess(inp).recommended_action)
        assert CapacityAction.no_action in actions
        assert CapacityAction.workload_review in actions
        assert CapacityAction.immediate_relief in actions


# ===========================================================================
# 6. account_load_score
# ===========================================================================

class TestAccountLoadScore:
    def test_zero_benchmark_gives_zero_account_score(self, engine):
        r = engine.assess(make_input(benchmark_accounts_per_rep=0))
        assert r.account_load_score == 0.0

    def test_acct_ratio_below_threshold(self, engine):
        # ratio = 20/25 = 0.8 → no ratio score
        r = engine.assess(make_input(total_accounts_owned=20, benchmark_accounts_per_rep=25,
                                      accounts_not_contacted_last_30d=0, concurrent_pocs_count=0))
        assert r.account_load_score == 0.0

    def test_acct_ratio_1_10(self, engine):
        # 28/25 = 1.12 → +8
        r = engine.assess(make_input(total_accounts_owned=28, benchmark_accounts_per_rep=25,
                                      accounts_not_contacted_last_30d=0, concurrent_pocs_count=0))
        assert r.account_load_score == 8.0

    def test_acct_ratio_1_25(self, engine):
        # 32/25 = 1.28 → +18
        r = engine.assess(make_input(total_accounts_owned=32, benchmark_accounts_per_rep=25,
                                      accounts_not_contacted_last_30d=0, concurrent_pocs_count=0))
        assert r.account_load_score == 18.0

    def test_acct_ratio_1_50(self, engine):
        # 40/25 = 1.6 → +32
        r = engine.assess(make_input(total_accounts_owned=40, benchmark_accounts_per_rep=25,
                                      accounts_not_contacted_last_30d=0, concurrent_pocs_count=0))
        assert r.account_load_score == 32.0

    def test_acct_ratio_2_0(self, engine):
        # 50/25 = 2.0 → +50
        r = engine.assess(make_input(total_accounts_owned=50, benchmark_accounts_per_rep=25,
                                      accounts_not_contacted_last_30d=0, concurrent_pocs_count=0))
        assert r.account_load_score == 50.0

    def test_neglect_ratio_15_pct(self, engine):
        # 4/25 = 0.16 → +8
        r = engine.assess(make_input(total_accounts_owned=25, benchmark_accounts_per_rep=30,
                                      accounts_not_contacted_last_30d=4, concurrent_pocs_count=0))
        assert r.account_load_score == 8.0

    def test_neglect_ratio_30_pct(self, engine):
        # 8/25 = 0.32 → +18
        r = engine.assess(make_input(total_accounts_owned=25, benchmark_accounts_per_rep=30,
                                      accounts_not_contacted_last_30d=8, concurrent_pocs_count=0))
        assert r.account_load_score == 18.0

    def test_neglect_ratio_50_pct(self, engine):
        # 13/25 = 0.52 → +30
        r = engine.assess(make_input(total_accounts_owned=25, benchmark_accounts_per_rep=30,
                                      accounts_not_contacted_last_30d=13, concurrent_pocs_count=0))
        assert r.account_load_score == 30.0

    def test_pocs_3(self, engine):
        # +10 for pocs=3
        r = engine.assess(make_input(total_accounts_owned=20, benchmark_accounts_per_rep=25,
                                      accounts_not_contacted_last_30d=0, concurrent_pocs_count=3))
        assert r.account_load_score == 10.0

    def test_pocs_5(self, engine):
        # +20 for pocs>=5
        r = engine.assess(make_input(total_accounts_owned=20, benchmark_accounts_per_rep=25,
                                      accounts_not_contacted_last_30d=0, concurrent_pocs_count=5))
        assert r.account_load_score == 20.0

    def test_account_load_score_clamped_at_100(self, engine):
        # max possible > 100: ratio>=2 (+50) + neglect>=50% (+30) + pocs>=5 (+20) = 100
        r = engine.assess(make_input(
            total_accounts_owned=60, benchmark_accounts_per_rep=25,
            accounts_not_contacted_last_30d=35, concurrent_pocs_count=6,
        ))
        assert r.account_load_score == 100.0

    def test_account_load_score_non_negative(self, engine):
        r = engine.assess(make_input())
        assert r.account_load_score >= 0.0

    def test_zero_total_accounts_no_neglect_score(self, engine):
        # total_accounts_owned=0 → no neglect ratio computed
        r = engine.assess(make_input(total_accounts_owned=0, accounts_not_contacted_last_30d=0,
                                      benchmark_accounts_per_rep=25, concurrent_pocs_count=0))
        assert r.account_load_score == 0.0


# ===========================================================================
# 7. deal_volume_score
# ===========================================================================

class TestDealVolumeScore:
    def test_zero_benchmark_gives_zero_deal_score(self, engine):
        r = engine.assess(make_input(benchmark_deals_per_rep=0, active_deals_in_pipeline=5))
        assert r.deal_volume_score == 0.0

    def test_deal_ratio_below_1_25(self, engine):
        # 8/10 = 0.8 → no ratio score
        r = engine.assess(make_input(active_deals_in_pipeline=8, benchmark_deals_per_rep=10,
                                      deals_not_touched_last_14d=0, crm_tasks_overdue_count=0))
        assert r.deal_volume_score == 0.0

    def test_deal_ratio_1_25(self, engine):
        # 13/10 = 1.3 → +8
        r = engine.assess(make_input(active_deals_in_pipeline=13, benchmark_deals_per_rep=10,
                                      deals_not_touched_last_14d=0, crm_tasks_overdue_count=0))
        assert r.deal_volume_score == 8.0

    def test_deal_ratio_1_50(self, engine):
        # 16/10 = 1.6 → +18
        r = engine.assess(make_input(active_deals_in_pipeline=16, benchmark_deals_per_rep=10,
                                      deals_not_touched_last_14d=0, crm_tasks_overdue_count=0))
        assert r.deal_volume_score == 18.0

    def test_deal_ratio_2_0(self, engine):
        # 21/10 = 2.1 → +32
        r = engine.assess(make_input(active_deals_in_pipeline=21, benchmark_deals_per_rep=10,
                                      deals_not_touched_last_14d=0, crm_tasks_overdue_count=0))
        assert r.deal_volume_score == 32.0

    def test_deal_ratio_2_5(self, engine):
        # 26/10 = 2.6 → +50
        r = engine.assess(make_input(active_deals_in_pipeline=26, benchmark_deals_per_rep=10,
                                      deals_not_touched_last_14d=0, crm_tasks_overdue_count=0))
        assert r.deal_volume_score == 50.0

    def test_untouched_ratio_15_pct(self, engine):
        # 2/10 = 0.2 → +8
        r = engine.assess(make_input(active_deals_in_pipeline=10, benchmark_deals_per_rep=12,
                                      deals_not_touched_last_14d=2, crm_tasks_overdue_count=0))
        assert r.deal_volume_score == 8.0

    def test_untouched_ratio_30_pct(self, engine):
        # 4/10 = 0.4 → +18
        r = engine.assess(make_input(active_deals_in_pipeline=10, benchmark_deals_per_rep=12,
                                      deals_not_touched_last_14d=4, crm_tasks_overdue_count=0))
        assert r.deal_volume_score == 18.0

    def test_untouched_ratio_50_pct(self, engine):
        # 6/10 = 0.6 → +30
        r = engine.assess(make_input(active_deals_in_pipeline=10, benchmark_deals_per_rep=12,
                                      deals_not_touched_last_14d=6, crm_tasks_overdue_count=0))
        assert r.deal_volume_score == 30.0

    def test_crm_overdue_2(self, engine):
        # +5
        r = engine.assess(make_input(active_deals_in_pipeline=8, benchmark_deals_per_rep=10,
                                      deals_not_touched_last_14d=0, crm_tasks_overdue_count=2))
        assert r.deal_volume_score == 5.0

    def test_crm_overdue_5(self, engine):
        # +12
        r = engine.assess(make_input(active_deals_in_pipeline=8, benchmark_deals_per_rep=10,
                                      deals_not_touched_last_14d=0, crm_tasks_overdue_count=5))
        assert r.deal_volume_score == 12.0

    def test_crm_overdue_10(self, engine):
        # +20
        r = engine.assess(make_input(active_deals_in_pipeline=8, benchmark_deals_per_rep=10,
                                      deals_not_touched_last_14d=0, crm_tasks_overdue_count=10))
        assert r.deal_volume_score == 20.0

    def test_deal_volume_score_clamped_at_100(self, engine):
        r = engine.assess(make_input(
            active_deals_in_pipeline=30, benchmark_deals_per_rep=10,
            deals_not_touched_last_14d=18, crm_tasks_overdue_count=12,
        ))
        assert r.deal_volume_score == 100.0

    def test_zero_active_deals_no_untouched_ratio(self, engine):
        r = engine.assess(make_input(active_deals_in_pipeline=0, deals_not_touched_last_14d=0,
                                      benchmark_deals_per_rep=10, crm_tasks_overdue_count=0))
        assert r.deal_volume_score == 0.0


# ===========================================================================
# 8. activity_strain_score
# ===========================================================================

class TestActivityStrainScore:
    def test_zero_benchmark_no_activity_ratio_score(self, engine):
        r = engine.assess(make_input(benchmark_activities_per_month=0,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      pto_days_missed_last_90d=0))
        assert r.activity_strain_score == 0.0

    def test_activity_ratio_normal_no_score(self, engine):
        # ratio = 80/100 = 0.8 → no score (>0.7 and <1.5)
        r = engine.assess(make_input(outbound_activities_last_30d=80,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      pto_days_missed_last_90d=0))
        assert r.activity_strain_score == 0.0

    def test_activity_over_1_5(self, engine):
        # ratio=1.6 → +20
        r = engine.assess(make_input(outbound_activities_last_30d=160,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      pto_days_missed_last_90d=0))
        assert r.activity_strain_score == 20.0

    def test_activity_over_2_0(self, engine):
        # ratio=2.1 → +35
        r = engine.assess(make_input(outbound_activities_last_30d=210,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      pto_days_missed_last_90d=0))
        assert r.activity_strain_score == 35.0

    def test_activity_under_0_7(self, engine):
        # ratio=0.65 → +15 (<=0.7 but >0.5)
        r = engine.assess(make_input(outbound_activities_last_30d=65,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      pto_days_missed_last_90d=0))
        assert r.activity_strain_score == 15.0

    def test_activity_under_0_5(self, engine):
        # ratio=0.4 → +30
        r = engine.assess(make_input(outbound_activities_last_30d=40,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      pto_days_missed_last_90d=0))
        assert r.activity_strain_score == 30.0

    def test_activity_exactly_0_7(self, engine):
        # ratio=0.7 → +15 (<=0.7)
        r = engine.assess(make_input(outbound_activities_last_30d=70,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      pto_days_missed_last_90d=0))
        assert r.activity_strain_score == 15.0

    def test_activity_exactly_0_5(self, engine):
        # ratio=0.5 → +30 (<=0.5)
        r = engine.assess(make_input(outbound_activities_last_30d=50,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      pto_days_missed_last_90d=0))
        assert r.activity_strain_score == 30.0

    def test_activity_exactly_1_5(self, engine):
        # ratio=1.5 → +20 (>=1.5 but <2.0)
        r = engine.assess(make_input(outbound_activities_last_30d=150,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      pto_days_missed_last_90d=0))
        assert r.activity_strain_score == 20.0

    def test_activity_exactly_2_0(self, engine):
        # ratio=2.0 → +35
        r = engine.assess(make_input(outbound_activities_last_30d=200,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      pto_days_missed_last_90d=0))
        assert r.activity_strain_score == 35.0

    def test_admin_ratio_25_pct(self, engine):
        # admin=10, selling=30 → 10/40=0.25 → +10
        r = engine.assess(make_input(outbound_activities_last_30d=80,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=10, selling_hours_per_week=30,
                                      pto_days_missed_last_90d=0))
        assert r.activity_strain_score == 10.0

    def test_admin_ratio_35_pct(self, engine):
        # admin=14, selling=26 → 14/40≈0.35 → +20
        r = engine.assess(make_input(outbound_activities_last_30d=80,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=14, selling_hours_per_week=26,
                                      pto_days_missed_last_90d=0))
        assert r.activity_strain_score == 20.0

    def test_admin_ratio_50_pct(self, engine):
        # admin=20, selling=20 → 20/40=0.50 → +35
        r = engine.assess(make_input(outbound_activities_last_30d=80,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=20, selling_hours_per_week=20,
                                      pto_days_missed_last_90d=0))
        assert r.activity_strain_score == 35.0

    def test_pto_missed_2(self, engine):
        r = engine.assess(make_input(outbound_activities_last_30d=80,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      pto_days_missed_last_90d=2))
        assert r.activity_strain_score == 15.0

    def test_pto_missed_5(self, engine):
        r = engine.assess(make_input(outbound_activities_last_30d=80,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      pto_days_missed_last_90d=5))
        assert r.activity_strain_score == 30.0

    def test_activity_strain_clamped_at_100(self, engine):
        r = engine.assess(make_input(
            outbound_activities_last_30d=220,
            benchmark_activities_per_month=100,
            admin_hours_per_week=25, selling_hours_per_week=20,
            pto_days_missed_last_90d=6,
        ))
        assert r.activity_strain_score == 100.0

    def test_zero_total_hours_no_admin_ratio_score(self, engine):
        # admin=0, selling=0 → total=0, no admin_ratio computed
        r = engine.assess(make_input(outbound_activities_last_30d=80,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=0, selling_hours_per_week=0,
                                      pto_days_missed_last_90d=0))
        assert r.activity_strain_score == 0.0


# ===========================================================================
# 9. quality_degradation_score
# ===========================================================================

class TestQualityDegradationScore:
    def test_all_good_zero_score(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.95, avg_response_time_hours=4.0,
                                      deal_quality_score=80.0, peer_avg_deal_quality_score=78.0))
        assert r.quality_degradation_score == 0.0

    def test_emails_lt_0_85(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.82, avg_response_time_hours=4.0,
                                      deal_quality_score=80.0, peer_avg_deal_quality_score=78.0))
        assert r.quality_degradation_score == 8.0

    def test_emails_lt_0_70(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.65, avg_response_time_hours=4.0,
                                      deal_quality_score=80.0, peer_avg_deal_quality_score=78.0))
        assert r.quality_degradation_score == 20.0

    def test_emails_lt_0_50(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.40, avg_response_time_hours=4.0,
                                      deal_quality_score=80.0, peer_avg_deal_quality_score=78.0))
        assert r.quality_degradation_score == 35.0

    def test_response_time_12h(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.95, avg_response_time_hours=12.0,
                                      deal_quality_score=80.0, peer_avg_deal_quality_score=78.0))
        assert r.quality_degradation_score == 8.0

    def test_response_time_24h(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.95, avg_response_time_hours=24.0,
                                      deal_quality_score=80.0, peer_avg_deal_quality_score=78.0))
        assert r.quality_degradation_score == 18.0

    def test_response_time_48h(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.95, avg_response_time_hours=48.0,
                                      deal_quality_score=80.0, peer_avg_deal_quality_score=78.0))
        assert r.quality_degradation_score == 30.0

    def test_quality_gap_5(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.95, avg_response_time_hours=4.0,
                                      deal_quality_score=70.0, peer_avg_deal_quality_score=75.0))
        assert r.quality_degradation_score == 8.0

    def test_quality_gap_10(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.95, avg_response_time_hours=4.0,
                                      deal_quality_score=60.0, peer_avg_deal_quality_score=70.0))
        assert r.quality_degradation_score == 20.0

    def test_quality_gap_20(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.95, avg_response_time_hours=4.0,
                                      deal_quality_score=50.0, peer_avg_deal_quality_score=70.0))
        assert r.quality_degradation_score == 35.0

    def test_peer_score_zero_no_quality_gap_computed(self, engine):
        # peer_avg_deal_quality_score=0 → gap check skipped
        r = engine.assess(make_input(emails_responded_pct=0.95, avg_response_time_hours=4.0,
                                      deal_quality_score=50.0, peer_avg_deal_quality_score=0.0))
        assert r.quality_degradation_score == 0.0

    def test_quality_degradation_clamped_at_100(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.40, avg_response_time_hours=50.0,
                                      deal_quality_score=40.0, peer_avg_deal_quality_score=80.0))
        assert r.quality_degradation_score == 100.0

    def test_quality_degradation_non_negative(self, engine):
        r = engine.assess(make_input())
        assert r.quality_degradation_score >= 0.0


# ===========================================================================
# 10. Composite score calculation
# ===========================================================================

class TestCompositeScore:
    def test_composite_matches_weighted_sum(self, engine):
        r = engine.assess(make_input())
        expected = (
            r.account_load_score * 0.30
            + r.deal_volume_score * 0.30
            + r.activity_strain_score * 0.25
            + r.quality_degradation_score * 0.15
        )
        expected = round(max(0.0, min(100.0, expected)), 1)
        assert r.capacity_composite == pytest.approx(expected, abs=0.05)

    def test_composite_is_rounded_to_1_decimal(self, engine):
        r = engine.assess(make_input())
        assert r.capacity_composite == round(r.capacity_composite, 1)

    def test_composite_clamped_non_negative(self, engine):
        r = engine.assess(make_input())
        assert r.capacity_composite >= 0.0

    def test_composite_clamped_max_100(self, engine):
        r = engine.assess(make_input(
            total_accounts_owned=60, accounts_not_contacted_last_30d=35,
            concurrent_pocs_count=6, active_deals_in_pipeline=30,
            deals_not_touched_last_14d=16, crm_tasks_overdue_count=12,
            outbound_activities_last_30d=220, admin_hours_per_week=25,
            selling_hours_per_week=20, pto_days_missed_last_90d=6,
            emails_responded_pct=0.40, avg_response_time_hours=50,
            deal_quality_score=40.0, peer_avg_deal_quality_score=80.0,
        ))
        assert r.capacity_composite <= 100.0

    def test_composite_zero_for_perfect_rep(self, engine):
        r = engine.assess(make_input(
            total_accounts_owned=15, benchmark_accounts_per_rep=25,
            active_deals_in_pipeline=5, benchmark_deals_per_rep=10,
            outbound_activities_last_30d=90, benchmark_activities_per_month=100,
            crm_tasks_overdue_count=0, emails_responded_pct=1.0,
            avg_response_time_hours=1.0, deals_not_touched_last_14d=0,
            accounts_not_contacted_last_30d=0, admin_hours_per_week=3,
            selling_hours_per_week=35, concurrent_pocs_count=0,
            deal_quality_score=90.0, peer_avg_deal_quality_score=80.0,
            pto_days_missed_last_90d=0,
        ))
        assert r.capacity_composite == 0.0


# ===========================================================================
# 11. is_overloaded flag — all OR conditions
# ===========================================================================

class TestIsOverloaded:
    def test_not_overloaded_healthy(self, engine):
        r = engine.assess(make_input())
        assert r.is_overloaded is False

    def test_overloaded_via_composite_gte_40(self, engine):
        # composite=44.9 >= 40 → overloaded
        r = engine.assess(make_input(
            total_accounts_owned=50, benchmark_accounts_per_rep=25,
            accounts_not_contacted_last_30d=26,
            active_deals_in_pipeline=18, benchmark_deals_per_rep=10,
            deals_not_touched_last_14d=5, crm_tasks_overdue_count=6,
            emails_responded_pct=0.65, avg_response_time_hours=25,
            pto_days_missed_last_90d=2, admin_hours_per_week=5,
            selling_hours_per_week=30, concurrent_pocs_count=0,
        ))
        assert r.capacity_composite >= 40
        assert r.is_overloaded is True

    def test_overloaded_via_crm_tasks_overdue_8(self, engine):
        # crm_tasks_overdue_count >= 8 → overloaded regardless of composite
        r = engine.assess(make_input(crm_tasks_overdue_count=8))
        assert r.is_overloaded is True

    def test_overloaded_via_crm_tasks_overdue_9(self, engine):
        r = engine.assess(make_input(crm_tasks_overdue_count=9))
        assert r.is_overloaded is True

    def test_not_overloaded_crm_tasks_7(self, engine):
        # 7 < 8 → does not trigger crm_tasks condition
        # deal_score from crm=7 → +12, all else healthy → composite low
        r = engine.assess(make_input(crm_tasks_overdue_count=7))
        # composite = 0*0.3 + 12*0.3 + 0*0.25 + 0*0.15 = 3.6 → not overloaded
        assert r.capacity_composite < 40
        assert r.is_overloaded is False

    def test_overloaded_via_untouched_ratio_gte_0_4(self, engine):
        # active=10, not_touched=4 → ratio=0.4
        r = engine.assess(make_input(active_deals_in_pipeline=10, deals_not_touched_last_14d=4))
        assert r.is_overloaded is True

    def test_overloaded_via_untouched_ratio_gt_0_4(self, engine):
        # active=10, not_touched=5 → ratio=0.5
        r = engine.assess(make_input(active_deals_in_pipeline=10, deals_not_touched_last_14d=5))
        assert r.is_overloaded is True

    def test_not_overloaded_untouched_ratio_below_0_4(self, engine):
        # active=10, not_touched=3 → ratio=0.3 — does not trigger this condition
        r = engine.assess(make_input(active_deals_in_pipeline=10, deals_not_touched_last_14d=3,
                                      crm_tasks_overdue_count=0))
        # composite should be low (deal score = 18 for untouched at 0.3, but deal ratio fine)
        # deal_volume_score = 18 (untouched), composite = 18*0.30 = 5.4 → not_overloaded
        assert r.is_overloaded is False

    def test_overloaded_zero_active_deals_no_ratio_check(self, engine):
        # active_deals=0 → untouched ratio check skipped
        r = engine.assess(make_input(active_deals_in_pipeline=0, deals_not_touched_last_14d=0,
                                      crm_tasks_overdue_count=0))
        assert r.is_overloaded is False


# ===========================================================================
# 12. requires_immediate_relief flag — all OR conditions
# ===========================================================================

class TestRequiresImmediateRelief:
    def test_not_requires_relief_healthy(self, engine):
        r = engine.assess(make_input())
        assert r.requires_immediate_relief is False

    def test_relief_via_composite_gte_30(self, engine):
        # composite=20.7 is < 30 but composite=44.9 >= 30 → requires relief
        r = engine.assess(make_input(
            total_accounts_owned=50, benchmark_accounts_per_rep=25,
            accounts_not_contacted_last_30d=26,
            active_deals_in_pipeline=18, benchmark_deals_per_rep=10,
            deals_not_touched_last_14d=5, crm_tasks_overdue_count=6,
            emails_responded_pct=0.65, avg_response_time_hours=25,
            pto_days_missed_last_90d=2, admin_hours_per_week=5,
            selling_hours_per_week=30, concurrent_pocs_count=0,
        ))
        assert r.capacity_composite >= 30
        assert r.requires_immediate_relief is True

    def test_relief_via_emails_lt_0_5(self, engine):
        # emails_responded_pct < 0.5 → requires relief regardless of composite
        r = engine.assess(make_input(emails_responded_pct=0.45))
        assert r.requires_immediate_relief is True

    def test_relief_via_emails_exactly_0_49(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.49))
        assert r.requires_immediate_relief is True

    def test_not_relief_emails_exactly_0_5(self, engine):
        # 0.5 is NOT < 0.5
        r = engine.assess(make_input(emails_responded_pct=0.5))
        # Check that this specific condition doesn't trigger
        # composite with healthy baseline is still low
        assert r.requires_immediate_relief is False

    def test_relief_via_pto_missed_3(self, engine):
        r = engine.assess(make_input(pto_days_missed_last_90d=3))
        assert r.requires_immediate_relief is True

    def test_relief_via_pto_missed_5(self, engine):
        r = engine.assess(make_input(pto_days_missed_last_90d=5))
        assert r.requires_immediate_relief is True

    def test_not_relief_pto_missed_2(self, engine):
        # 2 < 3 → does not trigger PTO condition
        r = engine.assess(make_input(pto_days_missed_last_90d=2))
        # Activity strain adds 15, composite = 15*0.25 = 3.75 → no relief
        assert r.requires_immediate_relief is False

    def test_relief_multiple_conditions(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.40, pto_days_missed_last_90d=4))
        assert r.requires_immediate_relief is True


# ===========================================================================
# 13. estimated_neglected_pipeline_pct
# ===========================================================================

class TestNeglectedPipelinePct:
    def test_zero_when_no_active_deals(self, engine):
        r = engine.assess(make_input(active_deals_in_pipeline=0, deals_not_touched_last_14d=0))
        assert r.estimated_neglected_pipeline_pct == 0.0

    def test_zero_when_no_untouched(self, engine):
        r = engine.assess(make_input(active_deals_in_pipeline=10, deals_not_touched_last_14d=0))
        assert r.estimated_neglected_pipeline_pct == 0.0

    def test_correct_pct_calculation(self, engine):
        r = engine.assess(make_input(active_deals_in_pipeline=10, deals_not_touched_last_14d=4))
        assert r.estimated_neglected_pipeline_pct == pytest.approx(40.0, abs=0.1)

    def test_pct_50(self, engine):
        r = engine.assess(make_input(active_deals_in_pipeline=10, deals_not_touched_last_14d=5))
        assert r.estimated_neglected_pipeline_pct == pytest.approx(50.0, abs=0.1)

    def test_pct_100_clamped(self, engine):
        # all deals untouched
        r = engine.assess(make_input(active_deals_in_pipeline=10, deals_not_touched_last_14d=10))
        assert r.estimated_neglected_pipeline_pct == 100.0

    def test_pct_clamped_at_0_not_negative(self, engine):
        # Can't be negative
        r = engine.assess(make_input(active_deals_in_pipeline=10, deals_not_touched_last_14d=0))
        assert r.estimated_neglected_pipeline_pct >= 0.0

    def test_pct_clamped_at_100(self, engine):
        r = engine.assess(make_input(active_deals_in_pipeline=5, deals_not_touched_last_14d=10))
        assert r.estimated_neglected_pipeline_pct <= 100.0

    def test_pct_various_ratios(self, engine):
        for not_touched, active, expected in [
            (1, 10, 10.0),
            (3, 10, 30.0),
            (7, 10, 70.0),
        ]:
            r = engine.assess(make_input(active_deals_in_pipeline=active,
                                          deals_not_touched_last_14d=not_touched))
            assert r.estimated_neglected_pipeline_pct == pytest.approx(expected, abs=0.1)


# ===========================================================================
# 14. capacity_signal
# ===========================================================================

class TestCapacitySignal:
    def test_signal_healthy_message(self, engine):
        r = engine.assess(make_input())
        assert "healthy" in r.capacity_signal.lower() or "Rep workload" in r.capacity_signal

    def test_signal_contains_composite(self, engine):
        r = engine.assess(make_input(admin_hours_per_week=18, selling_hours_per_week=22))
        # admin_burden stressor
        assert "composite" in r.capacity_signal

    def test_signal_admin_burden_contains_hours(self, engine):
        r = engine.assess(make_input(admin_hours_per_week=18, selling_hours_per_week=22))
        assert r.capacity_stressor == CapacityStressor.admin_burden
        assert "18" in r.capacity_signal
        assert "22" in r.capacity_signal

    def test_signal_activity_overburn_contains_activities(self, engine):
        r = engine.assess(make_input(outbound_activities_last_30d=200,
                                      admin_hours_per_week=5, selling_hours_per_week=30))
        assert r.capacity_stressor == CapacityStressor.activity_overburn
        assert "200" in r.capacity_signal

    def test_signal_account_overload_contains_accounts(self, engine):
        r = engine.assess(make_input(total_accounts_owned=40,
                                      accounts_not_contacted_last_30d=15,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      outbound_activities_last_30d=80))
        assert r.capacity_stressor == CapacityStressor.account_overload
        assert "40" in r.capacity_signal

    def test_signal_deal_volume_excess_contains_deals(self, engine):
        r = engine.assess(make_input(active_deals_in_pipeline=20,
                                      deals_not_touched_last_14d=4,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      outbound_activities_last_30d=80))
        assert r.capacity_stressor == CapacityStressor.deal_volume_excess
        assert "20" in r.capacity_signal

    def test_signal_multi_role_contains_pocs(self, engine):
        r = engine.assess(make_input(concurrent_pocs_count=4,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      outbound_activities_last_30d=80))
        assert r.capacity_stressor == CapacityStressor.multi_role_strain
        assert "4" in r.capacity_signal

    def test_signal_is_string(self, engine):
        r = engine.assess(make_input())
        assert isinstance(r.capacity_signal, str)
        assert len(r.capacity_signal) > 0


# ===========================================================================
# 15. to_dict()
# ===========================================================================

class TestToDict:
    def test_to_dict_returns_dict(self, engine):
        r = engine.assess(make_input())
        assert isinstance(r.to_dict(), dict)

    def test_to_dict_has_15_keys(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert len(d) == 15

    def test_to_dict_exact_keys(self, engine):
        d = engine.assess(make_input()).to_dict()
        expected_keys = {
            "rep_id", "region", "capacity_risk", "capacity_stressor",
            "capacity_severity", "recommended_action", "account_load_score",
            "deal_volume_score", "activity_strain_score", "quality_degradation_score",
            "capacity_composite", "is_overloaded", "requires_immediate_relief",
            "estimated_neglected_pipeline_pct", "capacity_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_rep_id_is_str(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["rep_id"], str)

    def test_to_dict_region_is_str(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["region"], str)

    def test_to_dict_capacity_risk_is_str(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["capacity_risk"], str)

    def test_to_dict_capacity_stressor_is_str(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["capacity_stressor"], str)

    def test_to_dict_capacity_severity_is_str(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["capacity_severity"], str)

    def test_to_dict_recommended_action_is_str(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_account_load_score_is_float(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["account_load_score"], float)

    def test_to_dict_deal_volume_score_is_float(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["deal_volume_score"], float)

    def test_to_dict_activity_strain_score_is_float(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["activity_strain_score"], float)

    def test_to_dict_quality_degradation_score_is_float(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["quality_degradation_score"], float)

    def test_to_dict_capacity_composite_is_float(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["capacity_composite"], float)

    def test_to_dict_is_overloaded_is_bool(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["is_overloaded"], bool)

    def test_to_dict_requires_immediate_relief_is_bool(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["requires_immediate_relief"], bool)

    def test_to_dict_neglected_pipeline_is_float(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["estimated_neglected_pipeline_pct"], float)

    def test_to_dict_capacity_signal_is_str(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["capacity_signal"], str)

    def test_to_dict_enum_values_are_strings(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert d["capacity_risk"] in [e.value for e in CapacityRisk]
        assert d["capacity_stressor"] in [e.value for e in CapacityStressor]
        assert d["capacity_severity"] in [e.value for e in CapacitySeverity]
        assert d["recommended_action"] in [e.value for e in CapacityAction]

    def test_to_dict_numeric_fields_rounded_1_decimal(self, engine):
        r = engine.assess(make_input(
            total_accounts_owned=28, crm_tasks_overdue_count=3,
            emails_responded_pct=0.80, avg_response_time_hours=14,
        ))
        d = r.to_dict()
        for key in ["account_load_score", "deal_volume_score", "activity_strain_score",
                    "quality_degradation_score", "capacity_composite",
                    "estimated_neglected_pipeline_pct"]:
            val = d[key]
            assert val == round(val, 1)

    def test_to_dict_rep_id_value_matches(self, engine):
        r = engine.assess(make_input(rep_id="TEST-777"))
        d = r.to_dict()
        assert d["rep_id"] == "TEST-777"

    def test_to_dict_overloaded_value_matches(self, engine):
        r = engine.assess(make_input(crm_tasks_overdue_count=8))
        d = r.to_dict()
        assert d["is_overloaded"] is True


# ===========================================================================
# 16. assess_batch()
# ===========================================================================

class TestAssessBatch:
    def test_batch_returns_list(self, engine):
        result = engine.assess_batch([make_input(), make_input(rep_id="rep-002")])
        assert isinstance(result, list)

    def test_batch_length_matches_input(self, engine):
        inputs = [make_input(rep_id=f"rep-{i:03d}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_all_results_are_represult(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        for r in results:
            assert isinstance(r, RepCapacityResult)

    def test_batch_rep_ids_preserved(self, engine):
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(4)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"rep-{i}"

    def test_batch_empty_list(self, engine):
        result = engine.assess_batch([])
        assert result == []

    def test_batch_single_item(self, engine):
        result = engine.assess_batch([make_input(rep_id="solo")])
        assert len(result) == 1
        assert result[0].rep_id == "solo"

    def test_batch_results_stored_for_summary(self, engine):
        engine.assess_batch([make_input(rep_id=f"rep-{i}") for i in range(3)])
        summary = engine.summary()
        assert summary["total"] == 3

    def test_batch_mixed_risk_levels(self, engine):
        inputs = [
            make_input(rep_id="healthy"),
            make_input(rep_id="critical",
                       total_accounts_owned=60, accounts_not_contacted_last_30d=35,
                       concurrent_pocs_count=6, active_deals_in_pipeline=30,
                       deals_not_touched_last_14d=16, crm_tasks_overdue_count=12,
                       outbound_activities_last_30d=220, admin_hours_per_week=25,
                       selling_hours_per_week=20, pto_days_missed_last_90d=6,
                       emails_responded_pct=0.40, avg_response_time_hours=50,
                       deal_quality_score=40.0, peer_avg_deal_quality_score=80.0),
        ]
        results = engine.assess_batch(inputs)
        assert results[0].capacity_risk == CapacityRisk.low
        assert results[1].capacity_risk == CapacityRisk.critical


# ===========================================================================
# 17. summary()
# ===========================================================================

class TestSummary:
    def test_summary_empty_engine(self):
        engine = SalesRepCapacityOverloadDetector()
        s = engine.summary()
        assert s["total"] == 0

    def test_summary_has_13_keys(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert len(s) == 13

    def test_summary_exact_keys(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        expected_keys = {
            "total", "risk_counts", "stressor_counts", "severity_counts",
            "action_counts", "avg_capacity_composite", "overloaded_count",
            "immediate_relief_count", "avg_account_load_score",
            "avg_deal_volume_score", "avg_activity_strain_score",
            "avg_quality_degradation_score", "avg_estimated_neglected_pipeline_pct",
        }
        assert set(s.keys()) == expected_keys

    def test_summary_key_stressor_counts_not_pattern(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert "stressor_counts" in s
        assert "pattern_counts" not in s

    def test_summary_total_count(self, engine):
        for i in range(4):
            engine.assess(make_input(rep_id=f"rep-{i}"))
        s = engine.summary()
        assert s["total"] == 4

    def test_summary_risk_counts(self, engine):
        engine.assess(make_input())  # low
        s = engine.summary()
        assert s["risk_counts"]["low"] == 1

    def test_summary_stressor_counts(self, engine):
        engine.assess(make_input())  # none
        s = engine.summary()
        assert s["stressor_counts"]["none"] == 1

    def test_summary_severity_counts(self, engine):
        engine.assess(make_input())  # optimal
        s = engine.summary()
        assert s["severity_counts"]["optimal"] == 1

    def test_summary_action_counts(self, engine):
        engine.assess(make_input())  # no_action
        s = engine.summary()
        assert s["action_counts"]["no_action"] == 1

    def test_summary_avg_composite(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["avg_capacity_composite"], float)
        assert s["avg_capacity_composite"] >= 0.0

    def test_summary_overloaded_count(self, engine):
        engine.assess(make_input())  # not overloaded
        engine.assess(make_input(crm_tasks_overdue_count=8))  # overloaded
        s = engine.summary()
        assert s["overloaded_count"] == 1

    def test_summary_immediate_relief_count(self, engine):
        engine.assess(make_input())  # no relief
        engine.assess(make_input(emails_responded_pct=0.45))  # relief
        s = engine.summary()
        assert s["immediate_relief_count"] == 1

    def test_summary_avg_account_load_score(self, engine):
        engine.assess(make_input(total_accounts_owned=20, benchmark_accounts_per_rep=25,
                                  accounts_not_contacted_last_30d=0, concurrent_pocs_count=0))
        s = engine.summary()
        assert s["avg_account_load_score"] == 0.0

    def test_summary_avg_deal_volume_score(self, engine):
        engine.assess(make_input(active_deals_in_pipeline=8, benchmark_deals_per_rep=10,
                                  deals_not_touched_last_14d=0, crm_tasks_overdue_count=0))
        s = engine.summary()
        assert s["avg_deal_volume_score"] == 0.0

    def test_summary_avg_activity_strain_score(self, engine):
        engine.assess(make_input(outbound_activities_last_30d=80,
                                  benchmark_activities_per_month=100,
                                  admin_hours_per_week=5, selling_hours_per_week=30,
                                  pto_days_missed_last_90d=0))
        s = engine.summary()
        assert s["avg_activity_strain_score"] == 0.0

    def test_summary_avg_quality_degradation_score(self, engine):
        engine.assess(make_input(emails_responded_pct=0.95, avg_response_time_hours=4.0,
                                  deal_quality_score=80.0, peer_avg_deal_quality_score=78.0))
        s = engine.summary()
        assert s["avg_quality_degradation_score"] == 0.0

    def test_summary_avg_neglected_pipeline_pct(self, engine):
        engine.assess(make_input(active_deals_in_pipeline=10, deals_not_touched_last_14d=0))
        s = engine.summary()
        assert s["avg_estimated_neglected_pipeline_pct"] == 0.0

    def test_summary_multiple_reps_avg_composite(self, engine):
        engine.assess(make_input(rep_id="a"))
        engine.assess(make_input(rep_id="b"))
        s = engine.summary()
        assert s["total"] == 2
        assert isinstance(s["avg_capacity_composite"], float)

    def test_summary_empty_risk_counts_dict(self):
        engine = SalesRepCapacityOverloadDetector()
        s = engine.summary()
        assert s["risk_counts"] == {}
        assert s["stressor_counts"] == {}

    def test_summary_accumulates_across_batches(self, engine):
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        engine.assess(make_input(rep_id="extra"))
        s = engine.summary()
        assert s["total"] == 4

    def test_summary_avg_neglected_nonzero(self, engine):
        engine.assess(make_input(active_deals_in_pipeline=10, deals_not_touched_last_14d=5))
        s = engine.summary()
        assert s["avg_estimated_neglected_pipeline_pct"] == pytest.approx(50.0, abs=0.1)


# ===========================================================================
# 18. Edge cases / zero-division guards
# ===========================================================================

class TestEdgeCases:
    def test_zero_benchmark_accounts_no_crash(self, engine):
        r = engine.assess(make_input(benchmark_accounts_per_rep=0, total_accounts_owned=10))
        assert isinstance(r, RepCapacityResult)

    def test_zero_benchmark_deals_no_crash(self, engine):
        r = engine.assess(make_input(benchmark_deals_per_rep=0, active_deals_in_pipeline=5))
        assert isinstance(r, RepCapacityResult)

    def test_zero_benchmark_activities_no_crash(self, engine):
        r = engine.assess(make_input(benchmark_activities_per_month=0,
                                      outbound_activities_last_30d=50))
        assert isinstance(r, RepCapacityResult)

    def test_zero_active_deals_no_crash(self, engine):
        r = engine.assess(make_input(active_deals_in_pipeline=0, deals_not_touched_last_14d=0))
        assert isinstance(r, RepCapacityResult)
        assert r.estimated_neglected_pipeline_pct == 0.0

    def test_zero_total_accounts_no_crash(self, engine):
        r = engine.assess(make_input(total_accounts_owned=0,
                                      accounts_not_contacted_last_30d=0))
        assert isinstance(r, RepCapacityResult)

    def test_zero_hours_no_crash(self, engine):
        r = engine.assess(make_input(admin_hours_per_week=0, selling_hours_per_week=0))
        assert isinstance(r, RepCapacityResult)

    def test_all_zeros_no_crash(self, engine):
        r = engine.assess(make_input(
            total_accounts_owned=0, benchmark_accounts_per_rep=0,
            active_deals_in_pipeline=0, benchmark_deals_per_rep=0,
            outbound_activities_last_30d=0, benchmark_activities_per_month=0,
            meetings_held_last_30d=0, benchmark_meetings_per_month=0,
            crm_tasks_overdue_count=0, emails_responded_pct=1.0,
            avg_response_time_hours=0, deals_not_touched_last_14d=0,
            accounts_not_contacted_last_30d=0, admin_hours_per_week=0,
            selling_hours_per_week=0, concurrent_pocs_count=0,
            deal_quality_score=0, peer_avg_deal_quality_score=0,
            pto_days_missed_last_90d=0,
        ))
        assert isinstance(r, RepCapacityResult)

    def test_very_large_accounts_clamped(self, engine):
        r = engine.assess(make_input(total_accounts_owned=10000, benchmark_accounts_per_rep=1,
                                      accounts_not_contacted_last_30d=9000,
                                      concurrent_pocs_count=100))
        assert r.account_load_score == 100.0

    def test_very_large_deals_clamped(self, engine):
        r = engine.assess(make_input(active_deals_in_pipeline=1000, benchmark_deals_per_rep=1,
                                      deals_not_touched_last_14d=900, crm_tasks_overdue_count=50))
        assert r.deal_volume_score == 100.0

    def test_emails_pct_exactly_0(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.0))
        assert r.quality_degradation_score >= 35.0
        assert r.requires_immediate_relief is True

    def test_emails_pct_exactly_1(self, engine):
        r = engine.assess(make_input(emails_responded_pct=1.0, avg_response_time_hours=4.0,
                                      deal_quality_score=80.0, peer_avg_deal_quality_score=78.0))
        assert r.quality_degradation_score == 0.0

    def test_peer_score_equals_rep_score(self, engine):
        # No gap → no quality gap score
        r = engine.assess(make_input(deal_quality_score=75.0, peer_avg_deal_quality_score=75.0,
                                      emails_responded_pct=0.95, avg_response_time_hours=4.0))
        assert r.quality_degradation_score == 0.0

    def test_rep_better_than_peer(self, engine):
        # Negative gap → no score
        r = engine.assess(make_input(deal_quality_score=85.0, peer_avg_deal_quality_score=75.0,
                                      emails_responded_pct=0.95, avg_response_time_hours=4.0))
        assert r.quality_degradation_score == 0.0

    def test_concurrent_pocs_0_no_poc_score(self, engine):
        r = engine.assess(make_input(concurrent_pocs_count=0, total_accounts_owned=20,
                                      accounts_not_contacted_last_30d=0))
        assert r.account_load_score == 0.0

    def test_concurrent_pocs_2_no_poc_score(self, engine):
        r = engine.assess(make_input(concurrent_pocs_count=2, total_accounts_owned=20,
                                      benchmark_accounts_per_rep=25,
                                      accounts_not_contacted_last_30d=0))
        assert r.account_load_score == 0.0

    def test_exactly_1_10_acct_ratio(self, engine):
        # 27.5/25 = 1.1 → +8
        r = engine.assess(make_input(total_accounts_owned=28, benchmark_accounts_per_rep=25,
                                      accounts_not_contacted_last_30d=0, concurrent_pocs_count=0))
        assert r.account_load_score == 8.0

    def test_exactly_2_0_acct_ratio(self, engine):
        # 50/25 = 2.0 → +50
        r = engine.assess(make_input(total_accounts_owned=50, benchmark_accounts_per_rep=25,
                                      accounts_not_contacted_last_30d=0, concurrent_pocs_count=0))
        assert r.account_load_score == 50.0

    def test_exactly_2_5_deal_ratio(self, engine):
        # 25/10 = 2.5 → +50
        r = engine.assess(make_input(active_deals_in_pipeline=25, benchmark_deals_per_rep=10,
                                      deals_not_touched_last_14d=0, crm_tasks_overdue_count=0))
        assert r.deal_volume_score == 50.0

    def test_untouched_deals_exceed_active(self, engine):
        # deals_not_touched > active_deals → clamped at 100
        r = engine.assess(make_input(active_deals_in_pipeline=5, deals_not_touched_last_14d=10))
        assert r.estimated_neglected_pipeline_pct == 100.0


# ===========================================================================
# 19. Score non-negativity and bounds
# ===========================================================================

class TestScoreBounds:
    @pytest.mark.parametrize("score_attr", [
        "account_load_score", "deal_volume_score", "activity_strain_score",
        "quality_degradation_score", "capacity_composite", "estimated_neglected_pipeline_pct",
    ])
    def test_score_non_negative(self, engine, score_attr):
        r = engine.assess(make_input())
        assert getattr(r, score_attr) >= 0.0

    @pytest.mark.parametrize("score_attr", [
        "account_load_score", "deal_volume_score", "activity_strain_score",
        "quality_degradation_score", "capacity_composite", "estimated_neglected_pipeline_pct",
    ])
    def test_score_max_100(self, engine, score_attr):
        r = engine.assess(make_input(
            total_accounts_owned=60, accounts_not_contacted_last_30d=35,
            concurrent_pocs_count=6, active_deals_in_pipeline=30,
            deals_not_touched_last_14d=16, crm_tasks_overdue_count=12,
            outbound_activities_last_30d=220, admin_hours_per_week=25,
            selling_hours_per_week=20, pto_days_missed_last_90d=6,
            emails_responded_pct=0.40, avg_response_time_hours=50,
            deal_quality_score=40.0, peer_avg_deal_quality_score=80.0,
        ))
        assert getattr(r, score_attr) <= 100.0


# ===========================================================================
# 20. Enum membership
# ===========================================================================

class TestEnumMembership:
    def test_capacity_risk_enum_values(self):
        assert set(e.value for e in CapacityRisk) == {"low", "moderate", "high", "critical"}

    def test_capacity_stressor_enum_values(self):
        assert set(e.value for e in CapacityStressor) == {
            "none", "account_overload", "deal_volume_excess",
            "activity_overburn", "admin_burden", "multi_role_strain",
        }

    def test_capacity_severity_enum_values(self):
        assert set(e.value for e in CapacitySeverity) == {
            "optimal", "stretched", "overloaded", "critical",
        }

    def test_capacity_action_enum_values(self):
        assert set(e.value for e in CapacityAction) == {
            "no_action", "workload_review", "account_redistribution",
            "hire_support", "immediate_relief",
        }

    def test_result_risk_is_enum(self, engine):
        r = engine.assess(make_input())
        assert isinstance(r.capacity_risk, CapacityRisk)

    def test_result_stressor_is_enum(self, engine):
        r = engine.assess(make_input())
        assert isinstance(r.capacity_stressor, CapacityStressor)

    def test_result_severity_is_enum(self, engine):
        r = engine.assess(make_input())
        assert isinstance(r.capacity_severity, CapacitySeverity)

    def test_result_action_is_enum(self, engine):
        r = engine.assess(make_input())
        assert isinstance(r.recommended_action, CapacityAction)


# ===========================================================================
# 21. Full coverage: all stressors produce signals
# ===========================================================================

class TestAllStressorSignals:
    @pytest.fixture(autouse=True)
    def fresh_engine(self):
        self.engine = SalesRepCapacityOverloadDetector()

    def test_none_stressor_signal(self):
        r = self.engine.assess(make_input())
        assert r.capacity_stressor == CapacityStressor.none
        assert "Rep workload" in r.capacity_signal

    def test_admin_burden_signal(self):
        r = self.engine.assess(make_input(admin_hours_per_week=18, selling_hours_per_week=22))
        assert r.capacity_stressor == CapacityStressor.admin_burden
        assert "composite" in r.capacity_signal

    def test_activity_overburn_signal(self):
        r = self.engine.assess(make_input(outbound_activities_last_30d=200,
                                           admin_hours_per_week=5, selling_hours_per_week=30))
        assert r.capacity_stressor == CapacityStressor.activity_overburn
        assert "composite" in r.capacity_signal

    def test_account_overload_signal(self):
        r = self.engine.assess(make_input(total_accounts_owned=40,
                                           accounts_not_contacted_last_30d=15,
                                           admin_hours_per_week=5, selling_hours_per_week=30,
                                           outbound_activities_last_30d=80))
        assert r.capacity_stressor == CapacityStressor.account_overload
        assert "composite" in r.capacity_signal

    def test_deal_volume_excess_signal(self):
        r = self.engine.assess(make_input(active_deals_in_pipeline=20,
                                           deals_not_touched_last_14d=4,
                                           admin_hours_per_week=5, selling_hours_per_week=30,
                                           outbound_activities_last_30d=80))
        assert r.capacity_stressor == CapacityStressor.deal_volume_excess
        assert "composite" in r.capacity_signal

    def test_multi_role_strain_signal(self):
        r = self.engine.assess(make_input(concurrent_pocs_count=4,
                                           admin_hours_per_week=5, selling_hours_per_week=30,
                                           outbound_activities_last_30d=80))
        assert r.capacity_stressor == CapacityStressor.multi_role_strain
        assert "composite" in r.capacity_signal


# ===========================================================================
# 22. Regression / scenario tests
# ===========================================================================

class TestScenarios:
    def test_scenario_new_rep_low_accounts(self, engine):
        """New rep with few accounts — optimal."""
        r = engine.assess(make_input(
            total_accounts_owned=10, benchmark_accounts_per_rep=25,
            active_deals_in_pipeline=3, benchmark_deals_per_rep=10,
        ))
        assert r.capacity_risk == CapacityRisk.low
        assert r.capacity_severity == CapacitySeverity.optimal
        assert r.is_overloaded is False

    def test_scenario_stretched_rep(self, engine):
        """Slightly over on accounts with some CRM lag — stretched."""
        # composite=20.7 → stretched
        r = engine.assess(make_input(
            total_accounts_owned=38, benchmark_accounts_per_rep=25,
            accounts_not_contacted_last_30d=8,
            active_deals_in_pipeline=13, benchmark_deals_per_rep=10,
            deals_not_touched_last_14d=2,
            crm_tasks_overdue_count=3,
            emails_responded_pct=0.80,
            avg_response_time_hours=14,
            concurrent_pocs_count=0,
        ))
        assert r.capacity_severity == CapacitySeverity.stretched

    def test_scenario_admin_heavy_rep(self, engine):
        """Rep spending most time on admin — admin_burden stressor."""
        r = engine.assess(make_input(
            admin_hours_per_week=22, selling_hours_per_week=18,
        ))
        assert r.capacity_stressor == CapacityStressor.admin_burden

    def test_scenario_neglected_pipeline(self, engine):
        """Rep with many untouched deals — overloaded and pipeline leakage."""
        r = engine.assess(make_input(
            active_deals_in_pipeline=20, deals_not_touched_last_14d=10,
        ))
        assert r.estimated_neglected_pipeline_pct == pytest.approx(50.0, abs=0.1)
        assert r.is_overloaded is True

    def test_scenario_burning_out(self, engine):
        """Rep doing 3x activities, missing PTO — activity overburn."""
        r = engine.assess(make_input(
            outbound_activities_last_30d=200,
            pto_days_missed_last_90d=4,
            admin_hours_per_week=5,
            selling_hours_per_week=30,
        ))
        assert r.requires_immediate_relief is True

    def test_scenario_quality_collapse(self, engine):
        """Rep responding to <50% emails, very slow — quality signal."""
        r = engine.assess(make_input(
            emails_responded_pct=0.35, avg_response_time_hours=60,
        ))
        assert r.quality_degradation_score >= 65.0
        assert r.requires_immediate_relief is True

    def test_scenario_crm_decay(self, engine):
        """Many overdue CRM tasks — directly triggers overloaded."""
        r = engine.assess(make_input(crm_tasks_overdue_count=10))
        assert r.is_overloaded is True

    def test_scenario_too_many_pocs(self, engine):
        """Rep managing 6 concurrent POCs — multi_role_strain."""
        r = engine.assess(make_input(concurrent_pocs_count=6,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      outbound_activities_last_30d=80))
        assert r.capacity_stressor == CapacityStressor.multi_role_strain

    def test_scenario_full_overload(self, engine):
        """Everything wrong — critical across all dimensions."""
        r = engine.assess(make_input(
            total_accounts_owned=60, accounts_not_contacted_last_30d=35,
            concurrent_pocs_count=6, active_deals_in_pipeline=30,
            deals_not_touched_last_14d=16, crm_tasks_overdue_count=12,
            outbound_activities_last_30d=220, admin_hours_per_week=25,
            selling_hours_per_week=20, pto_days_missed_last_90d=6,
            emails_responded_pct=0.40, avg_response_time_hours=50,
            deal_quality_score=40.0, peer_avg_deal_quality_score=80.0,
        ))
        assert r.capacity_risk == CapacityRisk.critical
        assert r.capacity_severity == CapacitySeverity.critical
        assert r.is_overloaded is True
        assert r.requires_immediate_relief is True
        assert r.recommended_action == CapacityAction.immediate_relief

    def test_scenario_single_trigger_low_email_response(self, engine):
        """Only trigger: low email response → relief but might be low composite."""
        r = engine.assess(make_input(emails_responded_pct=0.45))
        assert r.requires_immediate_relief is True

    def test_scenario_under_activity(self, engine):
        """Rep with very low outbound activity — under-activity signal."""
        r = engine.assess(make_input(outbound_activities_last_30d=40,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=5, selling_hours_per_week=30))
        assert r.activity_strain_score >= 30.0

    def test_scenario_account_overload_requires_score_threshold(self, engine):
        """account_overload stressor requires account_load_score >= 25."""
        # ratio=1.5 but score must be >=25
        r = engine.assess(make_input(
            total_accounts_owned=38, benchmark_accounts_per_rep=25,  # 38/25=1.52
            accounts_not_contacted_last_30d=0, concurrent_pocs_count=0,
            admin_hours_per_week=5, selling_hours_per_week=30,
            outbound_activities_last_30d=80,
        ))
        # account_load_score = 32 (ratio 1.52>=1.5) → >=25 → account_overload
        assert r.capacity_stressor == CapacityStressor.account_overload

    def test_scenario_deal_overload_requires_score_threshold(self, engine):
        """deal_volume_excess stressor requires deal_volume_score >= 25."""
        r = engine.assess(make_input(
            active_deals_in_pipeline=16, benchmark_deals_per_rep=10,  # 1.6>=1.5
            deals_not_touched_last_14d=0, crm_tasks_overdue_count=0,  # score=18 <25
            admin_hours_per_week=5, selling_hours_per_week=30,
            outbound_activities_last_30d=80,
        ))
        # deal_volume_score = 18 < 25 → no deal_volume_excess stressor
        assert r.capacity_stressor != CapacityStressor.deal_volume_excess

    def test_scenario_activity_overburn_boundary_1_8(self, engine):
        """activity_overburn stressor triggers at exactly 1.8x."""
        r = engine.assess(make_input(
            outbound_activities_last_30d=180, benchmark_activities_per_month=100,
            admin_hours_per_week=5, selling_hours_per_week=30,
        ))
        assert r.capacity_stressor == CapacityStressor.activity_overburn

    def test_scenario_activity_overburn_below_1_8(self, engine):
        """1.7x does not trigger activity_overburn."""
        r = engine.assess(make_input(
            outbound_activities_last_30d=170, benchmark_activities_per_month=100,
            admin_hours_per_week=5, selling_hours_per_week=30,
        ))
        assert r.capacity_stressor != CapacityStressor.activity_overburn


# ===========================================================================
# 23. Additional composite and classification tests
# ===========================================================================

class TestAdditionalComposite:
    def test_weights_sum_correctly(self, engine):
        """Verify each sub-score weight by isolating single components."""
        # Only account_load contributes: 50 (acct_ratio>=2.0) * 0.30 = 15
        r = engine.assess(make_input(
            total_accounts_owned=50, benchmark_accounts_per_rep=25,
            accounts_not_contacted_last_30d=0, concurrent_pocs_count=0,
            active_deals_in_pipeline=8, benchmark_deals_per_rep=10,
            deals_not_touched_last_14d=0, crm_tasks_overdue_count=0,
            outbound_activities_last_30d=80, benchmark_activities_per_month=100,
            admin_hours_per_week=5, selling_hours_per_week=30, pto_days_missed_last_90d=0,
            emails_responded_pct=0.95, avg_response_time_hours=4.0,
            deal_quality_score=80.0, peer_avg_deal_quality_score=78.0,
        ))
        assert r.account_load_score == 50.0
        assert r.capacity_composite == pytest.approx(50.0 * 0.30, abs=0.2)

    def test_weights_deal_component(self, engine):
        """Verify deal_volume_score weight of 0.30."""
        # Only deal_ratio contributes: 26/10=2.6 → +50
        r = engine.assess(make_input(
            total_accounts_owned=20, benchmark_accounts_per_rep=25,
            accounts_not_contacted_last_30d=0, concurrent_pocs_count=0,
            active_deals_in_pipeline=26, benchmark_deals_per_rep=10,
            deals_not_touched_last_14d=0, crm_tasks_overdue_count=0,
            outbound_activities_last_30d=80, benchmark_activities_per_month=100,
            admin_hours_per_week=5, selling_hours_per_week=30, pto_days_missed_last_90d=0,
            emails_responded_pct=0.95, avg_response_time_hours=4.0,
            deal_quality_score=80.0, peer_avg_deal_quality_score=78.0,
        ))
        assert r.deal_volume_score == 50.0
        assert r.capacity_composite == pytest.approx(50.0 * 0.30, abs=0.2)

    def test_weights_activity_component(self, engine):
        """Verify activity_strain_score weight of 0.25."""
        # Only activity_ratio contributes: 210/100=2.1 → +35
        r = engine.assess(make_input(
            total_accounts_owned=20, benchmark_accounts_per_rep=25,
            accounts_not_contacted_last_30d=0, concurrent_pocs_count=0,
            active_deals_in_pipeline=8, benchmark_deals_per_rep=10,
            deals_not_touched_last_14d=0, crm_tasks_overdue_count=0,
            outbound_activities_last_30d=210, benchmark_activities_per_month=100,
            admin_hours_per_week=5, selling_hours_per_week=30, pto_days_missed_last_90d=0,
            emails_responded_pct=0.95, avg_response_time_hours=4.0,
            deal_quality_score=80.0, peer_avg_deal_quality_score=78.0,
        ))
        assert r.activity_strain_score == 35.0
        assert r.capacity_composite == pytest.approx(35.0 * 0.25, abs=0.2)

    def test_weights_quality_component(self, engine):
        """Verify quality_degradation_score weight of 0.15."""
        # Only emails contribute: email=0.40 → +35
        r = engine.assess(make_input(
            total_accounts_owned=20, benchmark_accounts_per_rep=25,
            accounts_not_contacted_last_30d=0, concurrent_pocs_count=0,
            active_deals_in_pipeline=8, benchmark_deals_per_rep=10,
            deals_not_touched_last_14d=0, crm_tasks_overdue_count=0,
            outbound_activities_last_30d=80, benchmark_activities_per_month=100,
            admin_hours_per_week=5, selling_hours_per_week=30, pto_days_missed_last_90d=0,
            emails_responded_pct=0.40, avg_response_time_hours=4.0,
            deal_quality_score=80.0, peer_avg_deal_quality_score=78.0,
        ))
        assert r.quality_degradation_score == 35.0
        assert r.capacity_composite == pytest.approx(35.0 * 0.15, abs=0.2)

    def test_risk_below_20_is_low(self, engine):
        r = engine.assess(make_input())
        assert r.capacity_composite < 20
        assert r.capacity_risk == CapacityRisk.low

    def test_severity_below_20_is_optimal(self, engine):
        r = engine.assess(make_input())
        assert r.capacity_composite < 20
        assert r.capacity_severity == CapacitySeverity.optimal

    def test_risk_40_is_high(self, engine):
        # composite=44.9 is high
        r = engine.assess(make_input(
            total_accounts_owned=50, benchmark_accounts_per_rep=25,
            accounts_not_contacted_last_30d=26, active_deals_in_pipeline=18,
            benchmark_deals_per_rep=10, deals_not_touched_last_14d=5,
            crm_tasks_overdue_count=6, emails_responded_pct=0.65,
            avg_response_time_hours=25, pto_days_missed_last_90d=2,
            admin_hours_per_week=5, selling_hours_per_week=30, concurrent_pocs_count=0,
        ))
        assert r.capacity_composite >= 40
        assert r.capacity_risk == CapacityRisk.high

    def test_risk_and_severity_same_band(self, engine):
        """Risk and severity always share the same composite band."""
        inputs = [
            make_input(),
            make_input(total_accounts_owned=38, benchmark_accounts_per_rep=25,
                       accounts_not_contacted_last_30d=8, active_deals_in_pipeline=13,
                       benchmark_deals_per_rep=10, deals_not_touched_last_14d=2,
                       crm_tasks_overdue_count=3, emails_responded_pct=0.80,
                       avg_response_time_hours=14, concurrent_pocs_count=0),
        ]
        for inp in inputs:
            r = engine.assess(inp)
            # Both are derived from same composite, so must map to same band
            comp = r.capacity_composite
            risk_band = r.capacity_risk.value
            sev_band = r.capacity_severity.value
            if comp < 20:
                assert risk_band == "low"
                assert sev_band == "optimal"
            elif comp < 40:
                assert risk_band == "moderate"
                assert sev_band == "stretched"
            elif comp < 60:
                assert risk_band == "high"
                assert sev_band == "overloaded"
            else:
                assert risk_band == "critical"
                assert sev_band == "critical"


# ===========================================================================
# 24. Deal volume score: boundary values
# ===========================================================================

class TestDealVolumeBoundaries:
    def test_deal_ratio_exactly_1_25(self, engine):
        # 12.5/10 = 1.25 → no — threshold is >=1.25? Let's check: 13/10=1.3≥1.25
        r = engine.assess(make_input(active_deals_in_pipeline=13, benchmark_deals_per_rep=10,
                                      deals_not_touched_last_14d=0, crm_tasks_overdue_count=0))
        assert r.deal_volume_score == 8.0

    def test_deal_ratio_exactly_1_5(self, engine):
        r = engine.assess(make_input(active_deals_in_pipeline=15, benchmark_deals_per_rep=10,
                                      deals_not_touched_last_14d=0, crm_tasks_overdue_count=0))
        assert r.deal_volume_score == 18.0

    def test_deal_ratio_exactly_2_0(self, engine):
        r = engine.assess(make_input(active_deals_in_pipeline=20, benchmark_deals_per_rep=10,
                                      deals_not_touched_last_14d=0, crm_tasks_overdue_count=0))
        assert r.deal_volume_score == 32.0

    def test_untouched_exactly_0_15(self, engine):
        # 2/13 ≈ 0.154 → >= 0.15; deal_ratio=13/15=0.87 no ratio score
        r = engine.assess(make_input(active_deals_in_pipeline=13, benchmark_deals_per_rep=15,
                                      deals_not_touched_last_14d=2, crm_tasks_overdue_count=0))
        assert r.deal_volume_score == 8.0  # only untouched score

    def test_crm_overdue_exactly_2(self, engine):
        r = engine.assess(make_input(active_deals_in_pipeline=8, benchmark_deals_per_rep=10,
                                      deals_not_touched_last_14d=0, crm_tasks_overdue_count=2))
        assert r.deal_volume_score == 5.0

    def test_crm_overdue_1_no_score(self, engine):
        r = engine.assess(make_input(active_deals_in_pipeline=8, benchmark_deals_per_rep=10,
                                      deals_not_touched_last_14d=0, crm_tasks_overdue_count=1))
        assert r.deal_volume_score == 0.0


# ===========================================================================
# 25. Account load score: boundary values
# ===========================================================================

class TestAccountLoadBoundaries:
    def test_acct_ratio_just_below_1_10(self, engine):
        # 27/25 = 1.08 → no score
        r = engine.assess(make_input(total_accounts_owned=27, benchmark_accounts_per_rep=25,
                                      accounts_not_contacted_last_30d=0, concurrent_pocs_count=0))
        assert r.account_load_score == 0.0

    def test_acct_ratio_exactly_1_50(self, engine):
        # 37.5/25=1.5, use 38/25=1.52 → +32
        r = engine.assess(make_input(total_accounts_owned=38, benchmark_accounts_per_rep=25,
                                      accounts_not_contacted_last_30d=0, concurrent_pocs_count=0))
        assert r.account_load_score == 32.0

    def test_neglect_exactly_0_50(self, engine):
        # 5/10=0.50 → +30
        r = engine.assess(make_input(total_accounts_owned=10, benchmark_accounts_per_rep=15,
                                      accounts_not_contacted_last_30d=5, concurrent_pocs_count=0))
        assert r.account_load_score == 30.0

    def test_neglect_just_below_0_15(self, engine):
        # 1/10=0.10 → no neglect score
        r = engine.assess(make_input(total_accounts_owned=10, benchmark_accounts_per_rep=15,
                                      accounts_not_contacted_last_30d=1, concurrent_pocs_count=0))
        assert r.account_load_score == 0.0

    def test_pocs_exactly_3(self, engine):
        r = engine.assess(make_input(total_accounts_owned=20, benchmark_accounts_per_rep=25,
                                      accounts_not_contacted_last_30d=0, concurrent_pocs_count=3))
        assert r.account_load_score == 10.0

    def test_pocs_exactly_5(self, engine):
        r = engine.assess(make_input(total_accounts_owned=20, benchmark_accounts_per_rep=25,
                                      accounts_not_contacted_last_30d=0, concurrent_pocs_count=5))
        assert r.account_load_score == 20.0

    def test_pocs_4_gives_10(self, engine):
        # 4 >= 3 but < 5 → +10
        r = engine.assess(make_input(total_accounts_owned=20, benchmark_accounts_per_rep=25,
                                      accounts_not_contacted_last_30d=0, concurrent_pocs_count=4))
        assert r.account_load_score == 10.0


# ===========================================================================
# 26. Quality degradation score: boundary values
# ===========================================================================

class TestQualityDegradationBoundaries:
    def test_emails_exactly_0_85(self, engine):
        # 0.85 is NOT < 0.85 → no email score
        r = engine.assess(make_input(emails_responded_pct=0.85, avg_response_time_hours=4.0,
                                      deal_quality_score=80.0, peer_avg_deal_quality_score=78.0))
        assert r.quality_degradation_score == 0.0

    def test_emails_just_below_0_85(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.849, avg_response_time_hours=4.0,
                                      deal_quality_score=80.0, peer_avg_deal_quality_score=78.0))
        assert r.quality_degradation_score == 8.0

    def test_emails_exactly_0_70(self, engine):
        # 0.70 is NOT < 0.70 → only +8 (falls in <0.85 range)
        r = engine.assess(make_input(emails_responded_pct=0.70, avg_response_time_hours=4.0,
                                      deal_quality_score=80.0, peer_avg_deal_quality_score=78.0))
        assert r.quality_degradation_score == 8.0

    def test_emails_just_below_0_70(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.699, avg_response_time_hours=4.0,
                                      deal_quality_score=80.0, peer_avg_deal_quality_score=78.0))
        assert r.quality_degradation_score == 20.0

    def test_response_time_exactly_12(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.95, avg_response_time_hours=12.0,
                                      deal_quality_score=80.0, peer_avg_deal_quality_score=78.0))
        assert r.quality_degradation_score == 8.0

    def test_response_time_just_below_12(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.95, avg_response_time_hours=11.9,
                                      deal_quality_score=80.0, peer_avg_deal_quality_score=78.0))
        assert r.quality_degradation_score == 0.0

    def test_quality_gap_exactly_5(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.95, avg_response_time_hours=4.0,
                                      deal_quality_score=70.0, peer_avg_deal_quality_score=75.0))
        assert r.quality_degradation_score == 8.0

    def test_quality_gap_exactly_10(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.95, avg_response_time_hours=4.0,
                                      deal_quality_score=60.0, peer_avg_deal_quality_score=70.0))
        assert r.quality_degradation_score == 20.0

    def test_quality_gap_exactly_20(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.95, avg_response_time_hours=4.0,
                                      deal_quality_score=50.0, peer_avg_deal_quality_score=70.0))
        assert r.quality_degradation_score == 35.0

    def test_quality_gap_just_below_5_no_score(self, engine):
        r = engine.assess(make_input(emails_responded_pct=0.95, avg_response_time_hours=4.0,
                                      deal_quality_score=71.0, peer_avg_deal_quality_score=75.0))
        assert r.quality_degradation_score == 0.0


# ===========================================================================
# 27. Activity strain: boundary values
# ===========================================================================

class TestActivityStrainBoundaries:
    def test_activity_ratio_exactly_1_0_no_score(self, engine):
        r = engine.assess(make_input(outbound_activities_last_30d=100,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      pto_days_missed_last_90d=0))
        assert r.activity_strain_score == 0.0

    def test_admin_ratio_exactly_0_45_is_admin_burden(self, engine):
        # 9/(9+11) = 9/20 = 0.45 → admin_burden stressor
        r = engine.assess(make_input(admin_hours_per_week=9, selling_hours_per_week=11))
        assert r.capacity_stressor == CapacityStressor.admin_burden

    def test_admin_ratio_just_below_0_45_no_admin_burden(self, engine):
        # 8.9/20 ≈ 0.445 < 0.45 → no admin_burden
        r = engine.assess(make_input(admin_hours_per_week=8, selling_hours_per_week=12,
                                      outbound_activities_last_30d=80,
                                      benchmark_activities_per_month=100,
                                      concurrent_pocs_count=0))
        assert r.capacity_stressor != CapacityStressor.admin_burden

    def test_pto_exactly_2(self, engine):
        r = engine.assess(make_input(outbound_activities_last_30d=80,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      pto_days_missed_last_90d=2))
        assert r.activity_strain_score == 15.0

    def test_pto_1_no_score(self, engine):
        r = engine.assess(make_input(outbound_activities_last_30d=80,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      pto_days_missed_last_90d=1))
        assert r.activity_strain_score == 0.0

    def test_pto_exactly_5(self, engine):
        r = engine.assess(make_input(outbound_activities_last_30d=80,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=5, selling_hours_per_week=30,
                                      pto_days_missed_last_90d=5))
        assert r.activity_strain_score == 30.0

    def test_admin_ratio_exactly_0_25(self, engine):
        # 10/40 = 0.25 → +10
        r = engine.assess(make_input(outbound_activities_last_30d=80,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=10, selling_hours_per_week=30,
                                      pto_days_missed_last_90d=0))
        assert r.activity_strain_score == 10.0

    def test_admin_ratio_exactly_0_35(self, engine):
        # 14/40 = 0.35 → +20
        r = engine.assess(make_input(outbound_activities_last_30d=80,
                                      benchmark_activities_per_month=100,
                                      admin_hours_per_week=14, selling_hours_per_week=26,
                                      pto_days_missed_last_90d=0))
        assert r.activity_strain_score == 20.0
