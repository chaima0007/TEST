"""
Comprehensive tests for swarm.intelligence.customer_retention
"""

import pytest

from swarm.intelligence.customer_retention import (
    CustomerRetention,
    CustomerSignals,
    ChurnRisk,
    RetentionProfile,
    _login_recency_risk,
    _ticket_risk,
    _contract_risk,
    _engagement_trend_risk,
    _nps_risk,
    _compute_breakdown,
    _compute_churn_score,
    _classify_churn,
    _compute_risk_factors,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def healthy():
    return CustomerSignals(
        customer_id="healthy-001",
        name="Alice Dupont",
        company="GoodCorp",
        sector="SaaS",
        days_since_last_login=1,
        open_support_tickets=0,
        contract_months_remaining=24,
        engagement_trend=0.8,
        nps_score=60,
        avg_monthly_revenue_eur=500.0,
        months_as_customer=18,
    )


@pytest.fixture
def churning():
    return CustomerSignals(
        customer_id="churning-001",
        name="Bob Martin",
        company="BadCorp",
        sector="Retail",
        days_since_last_login=35,
        open_support_tickets=4,
        contract_months_remaining=1,
        engagement_trend=-0.7,
        nps_score=-40,
        avg_monthly_revenue_eur=300.0,
        months_as_customer=3,
    )


@pytest.fixture
def retention():
    """Fresh CustomerRetention instance for each test."""
    return CustomerRetention()


# ---------------------------------------------------------------------------
# TestCustomerSignals
# ---------------------------------------------------------------------------

class TestCustomerSignals:
    def test_to_dict_has_all_keys(self, healthy):
        d = healthy.to_dict()
        expected_keys = {
            "customer_id", "name", "company", "sector",
            "days_since_last_login", "open_support_tickets",
            "contract_months_remaining", "engagement_trend",
            "nps_score", "avg_monthly_revenue_eur", "months_as_customer",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_scalar_values(self, healthy):
        d = healthy.to_dict()
        assert d["customer_id"] == "healthy-001"
        assert d["name"] == "Alice Dupont"
        assert d["company"] == "GoodCorp"
        assert d["sector"] == "SaaS"

    def test_to_dict_numeric_values(self, healthy):
        d = healthy.to_dict()
        assert d["days_since_last_login"] == 1
        assert d["open_support_tickets"] == 0
        assert d["contract_months_remaining"] == 24

    def test_to_dict_float_values(self, healthy):
        d = healthy.to_dict()
        assert d["engagement_trend"] == pytest.approx(0.8)
        assert d["avg_monthly_revenue_eur"] == pytest.approx(500.0)

    def test_to_dict_churning_values(self, churning):
        d = churning.to_dict()
        assert d["customer_id"] == "churning-001"
        assert d["days_since_last_login"] == 35
        assert d["open_support_tickets"] == 4
        assert d["nps_score"] == -40
        assert d["engagement_trend"] == pytest.approx(-0.7)


# ---------------------------------------------------------------------------
# TestScoringHelpers
# ---------------------------------------------------------------------------

class TestScoringHelpers:
    # --- _login_recency_risk ---

    def test_login_recency_zero_days(self):
        assert _login_recency_risk(0) == pytest.approx(0.0)

    def test_login_recency_at_3(self):
        assert _login_recency_risk(3) == pytest.approx(0.0)

    def test_login_recency_at_4(self):
        # (4-3)*5 = 5
        assert _login_recency_risk(4) == pytest.approx(5.0)

    def test_login_recency_at_14(self):
        # (14-3)*5 = 55
        assert _login_recency_risk(14) == pytest.approx(55.0)

    def test_login_recency_at_15(self):
        # 55 + (15-14)*2.5 = 57.5
        assert _login_recency_risk(15) == pytest.approx(57.5)

    def test_login_recency_capped_at_100(self):
        # Very large value must be capped at 100
        assert _login_recency_risk(1000) == pytest.approx(100.0)

    def test_login_recency_proportional_in_middle_range(self):
        # Between 3 and 14, each day adds 5
        assert _login_recency_risk(8) == pytest.approx((8 - 3) * 5.0)

    # --- _ticket_risk ---

    def test_ticket_risk_zero(self):
        assert _ticket_risk(0) == pytest.approx(0.0)

    def test_ticket_risk_one(self):
        assert _ticket_risk(1) == pytest.approx(25.0)

    def test_ticket_risk_four(self):
        assert _ticket_risk(4) == pytest.approx(100.0)

    def test_ticket_risk_capped(self):
        assert _ticket_risk(10) == pytest.approx(100.0)

    def test_ticket_risk_proportional(self):
        assert _ticket_risk(2) == pytest.approx(50.0)
        assert _ticket_risk(3) == pytest.approx(75.0)

    # --- _contract_risk ---

    def test_contract_risk_12_months(self):
        assert _contract_risk(12) == pytest.approx(0.0)

    def test_contract_risk_above_12(self):
        assert _contract_risk(24) == pytest.approx(0.0)

    def test_contract_risk_6_months(self):
        assert _contract_risk(6) == pytest.approx(20.0)

    def test_contract_risk_11_months(self):
        assert _contract_risk(11) == pytest.approx(20.0)

    def test_contract_risk_3_months(self):
        assert _contract_risk(3) == pytest.approx(50.0)

    def test_contract_risk_5_months(self):
        assert _contract_risk(5) == pytest.approx(50.0)

    def test_contract_risk_1_month(self):
        assert _contract_risk(1) == pytest.approx(75.0)

    def test_contract_risk_2_months(self):
        assert _contract_risk(2) == pytest.approx(75.0)

    def test_contract_risk_0_months(self):
        assert _contract_risk(0) == pytest.approx(100.0)

    # --- _engagement_trend_risk ---

    def test_engagement_trend_plus_one(self):
        # (1 - 1.0) * 50 = 0
        assert _engagement_trend_risk(1.0) == pytest.approx(0.0)

    def test_engagement_trend_zero(self):
        # (1 - 0.0) * 50 = 50
        assert _engagement_trend_risk(0.0) == pytest.approx(50.0)

    def test_engagement_trend_minus_one(self):
        # (1 - (-1.0)) * 50 = 100
        assert _engagement_trend_risk(-1.0) == pytest.approx(100.0)

    def test_engagement_trend_clamped_above(self):
        # values > 1 are clamped to 1.0 → risk = 0
        assert _engagement_trend_risk(2.0) == pytest.approx(0.0)

    def test_engagement_trend_clamped_below(self):
        # values < -1 are clamped to -1.0 → risk = 100
        assert _engagement_trend_risk(-5.0) == pytest.approx(100.0)

    def test_engagement_trend_half(self):
        # (1 - 0.5) * 50 = 25
        assert _engagement_trend_risk(0.5) == pytest.approx(25.0)

    # --- _nps_risk ---

    def test_nps_risk_100(self):
        # (100 - 100) / 2 = 0
        assert _nps_risk(100) == pytest.approx(0.0)

    def test_nps_risk_0(self):
        # (100 - 0) / 2 = 50
        assert _nps_risk(0) == pytest.approx(50.0)

    def test_nps_risk_minus_100(self):
        # (100 - (-100)) / 2 = 100
        assert _nps_risk(-100) == pytest.approx(100.0)

    def test_nps_risk_50(self):
        # (100 - 50) / 2 = 25
        assert _nps_risk(50) == pytest.approx(25.0)

    def test_nps_risk_clamped(self):
        # Values outside range are clamped
        assert _nps_risk(200) == pytest.approx(0.0)
        assert _nps_risk(-200) == pytest.approx(100.0)


# ---------------------------------------------------------------------------
# TestChurnClassification
# ---------------------------------------------------------------------------

class TestChurnClassification:
    def test_low_at_zero(self):
        assert _classify_churn(0.0) == ChurnRisk.LOW

    def test_low_just_below_medium(self):
        assert _classify_churn(34.9) == ChurnRisk.LOW

    def test_medium_at_threshold(self):
        assert _classify_churn(35.0) == ChurnRisk.MEDIUM

    def test_medium_just_below_high(self):
        assert _classify_churn(54.9) == ChurnRisk.MEDIUM

    def test_high_at_threshold(self):
        assert _classify_churn(55.0) == ChurnRisk.HIGH

    def test_high_just_below_critical(self):
        assert _classify_churn(74.9) == ChurnRisk.HIGH

    def test_critical_at_threshold(self):
        assert _classify_churn(75.0) == ChurnRisk.CRITICAL

    def test_critical_at_100(self):
        assert _classify_churn(100.0) == ChurnRisk.CRITICAL

    def test_churn_risk_enum_values(self):
        assert ChurnRisk.LOW.value == "low"
        assert ChurnRisk.MEDIUM.value == "medium"
        assert ChurnRisk.HIGH.value == "high"
        assert ChurnRisk.CRITICAL.value == "critical"


# ---------------------------------------------------------------------------
# TestRetentionProfile
# ---------------------------------------------------------------------------

class TestRetentionProfile:
    def test_to_dict_has_all_keys(self, healthy):
        cr = CustomerRetention()
        profile = cr.analyze(healthy)
        d = profile.to_dict()
        expected_keys = {
            "signals", "churn_score", "churn_risk", "ltv_eur",
            "predicted_months_remaining", "risk_factors",
            "retention_actions", "score_breakdown",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_churn_risk_is_string(self, healthy):
        cr = CustomerRetention()
        profile = cr.analyze(healthy)
        d = profile.to_dict()
        assert isinstance(d["churn_risk"], str)
        assert d["churn_risk"] in ("low", "medium", "high", "critical")

    def test_to_dict_signals_is_dict(self, healthy):
        cr = CustomerRetention()
        profile = cr.analyze(healthy)
        d = profile.to_dict()
        assert isinstance(d["signals"], dict)
        assert d["signals"]["customer_id"] == "healthy-001"

    def test_to_dict_score_breakdown_has_5_keys(self, healthy):
        cr = CustomerRetention()
        profile = cr.analyze(healthy)
        d = profile.to_dict()
        breakdown = d["score_breakdown"]
        assert set(breakdown.keys()) == {
            "login_recency", "support_tickets", "contract_health",
            "engagement_trend", "nps_score",
        }

    def test_to_dict_risk_factors_and_actions_are_lists(self, churning):
        cr = CustomerRetention()
        profile = cr.analyze(churning)
        d = profile.to_dict()
        assert isinstance(d["risk_factors"], list)
        assert isinstance(d["retention_actions"], list)

    def test_healthy_profile_low_churn(self, healthy):
        cr = CustomerRetention()
        profile = cr.analyze(healthy)
        assert profile.churn_risk == ChurnRisk.LOW
        assert profile.churn_score < 35.0

    def test_churning_profile_high_churn(self, churning):
        cr = CustomerRetention()
        profile = cr.analyze(churning)
        assert profile.churn_risk in (ChurnRisk.HIGH, ChurnRisk.CRITICAL)
        assert profile.churn_score >= 55.0

    def test_churn_score_bounds(self, healthy, churning):
        cr = CustomerRetention()
        for sig in (healthy, churning):
            p = cr.analyze(sig)
            assert 0.0 <= p.churn_score <= 100.0

    def test_ltv_non_negative(self, healthy, churning):
        cr = CustomerRetention()
        for sig in (healthy, churning):
            p = cr.analyze(sig)
            assert p.ltv_eur >= 0.0


# ---------------------------------------------------------------------------
# TestComputeBreakdown
# ---------------------------------------------------------------------------

class TestComputeBreakdown:
    def test_breakdown_keys(self, healthy):
        bd = _compute_breakdown(healthy)
        assert set(bd.keys()) == {
            "login_recency", "support_tickets", "contract_health",
            "engagement_trend", "nps_score",
        }

    def test_breakdown_healthy_values_low(self, healthy):
        bd = _compute_breakdown(healthy)
        # healthy customer should have low risk in each component
        assert bd["login_recency"] == pytest.approx(0.0)
        assert bd["support_tickets"] == pytest.approx(0.0)
        assert bd["contract_health"] == pytest.approx(0.0)

    def test_breakdown_churning_values_high(self, churning):
        bd = _compute_breakdown(churning)
        # churning customer should have high risk
        assert bd["support_tickets"] == pytest.approx(100.0)  # 4*25=100
        assert bd["contract_health"] == pytest.approx(75.0)   # 1 month remaining

    def test_compute_churn_score_healthy(self, healthy):
        bd = _compute_breakdown(healthy)
        score = _compute_churn_score(bd)
        assert score < 35.0

    def test_compute_churn_score_churning(self, churning):
        bd = _compute_breakdown(churning)
        score = _compute_churn_score(bd)
        assert score >= 55.0

    def test_compute_churn_score_weights(self):
        # All components at 100 → score = 100
        bd = {
            "login_recency": 100.0,
            "support_tickets": 100.0,
            "contract_health": 100.0,
            "engagement_trend": 100.0,
            "nps_score": 100.0,
        }
        assert _compute_churn_score(bd) == pytest.approx(100.0)

    def test_compute_churn_score_all_zero(self):
        bd = {
            "login_recency": 0.0,
            "support_tickets": 0.0,
            "contract_health": 0.0,
            "engagement_trend": 0.0,
            "nps_score": 0.0,
        }
        assert _compute_churn_score(bd) == pytest.approx(0.0)

    def test_compute_churn_score_only_login(self):
        # Only login_recency=100, weight=0.25 → score=25
        bd = {
            "login_recency": 100.0,
            "support_tickets": 0.0,
            "contract_health": 0.0,
            "engagement_trend": 0.0,
            "nps_score": 0.0,
        }
        assert _compute_churn_score(bd) == pytest.approx(25.0)


# ---------------------------------------------------------------------------
# TestRiskFactors
# ---------------------------------------------------------------------------

class TestRiskFactors:
    def _make_signals(self, **overrides):
        base = dict(
            customer_id="test-rf",
            name="Test User",
            company="TestCo",
            sector="Tech",
            days_since_last_login=1,
            open_support_tickets=0,
            contract_months_remaining=24,
            engagement_trend=0.5,
            nps_score=50,
            avg_monthly_revenue_eur=500.0,
            months_as_customer=12,
        )
        base.update(overrides)
        return CustomerSignals(**base)

    def test_no_flags_for_healthy_customer(self, healthy):
        bd = _compute_breakdown(healthy)
        factors = _compute_risk_factors(healthy, bd)
        assert factors == []

    def test_login_recency_flag_triggered(self):
        # Need login_recency > 50: days=15 → 55+(15-14)*2.5=57.5 > 50 ✓
        sig = self._make_signals(days_since_last_login=15)
        bd = _compute_breakdown(sig)
        factors = _compute_risk_factors(sig, bd)
        assert any("15 jours" in f for f in factors)

    def test_login_recency_flag_not_triggered_below_threshold(self):
        # days=13 → (13-3)*5=50, NOT > 50, so no flag
        sig = self._make_signals(days_since_last_login=13)
        bd = _compute_breakdown(sig)
        factors = _compute_risk_factors(sig, bd)
        assert not any("jours" in f for f in factors)

    def test_ticket_flag_triggered(self):
        sig = self._make_signals(open_support_tickets=3)
        bd = _compute_breakdown(sig)
        factors = _compute_risk_factors(sig, bd)
        assert any("3 tickets" in f for f in factors)

    def test_ticket_flag_not_triggered_below_threshold(self):
        sig = self._make_signals(open_support_tickets=2)
        bd = _compute_breakdown(sig)
        factors = _compute_risk_factors(sig, bd)
        assert not any("tickets" in f for f in factors)

    def test_contract_expiry_flag_triggered(self):
        sig = self._make_signals(contract_months_remaining=3)
        bd = _compute_breakdown(sig)
        factors = _compute_risk_factors(sig, bd)
        assert any("Contrat expire" in f for f in factors)

    def test_contract_expiry_flag_not_triggered_above_threshold(self):
        sig = self._make_signals(contract_months_remaining=4)
        bd = _compute_breakdown(sig)
        factors = _compute_risk_factors(sig, bd)
        assert not any("Contrat expire" in f for f in factors)

    def test_engagement_decline_flag_triggered(self):
        sig = self._make_signals(engagement_trend=-0.31)
        bd = _compute_breakdown(sig)
        factors = _compute_risk_factors(sig, bd)
        assert any("déclin" in f for f in factors)

    def test_engagement_decline_flag_not_triggered_at_minus_0_3(self):
        sig = self._make_signals(engagement_trend=-0.3)
        bd = _compute_breakdown(sig)
        factors = _compute_risk_factors(sig, bd)
        assert not any("déclin" in f for f in factors)

    def test_nps_flag_triggered(self):
        sig = self._make_signals(nps_score=-1)
        bd = _compute_breakdown(sig)
        factors = _compute_risk_factors(sig, bd)
        assert any("NPS négatif" in f for f in factors)

    def test_nps_flag_not_triggered_at_zero(self):
        sig = self._make_signals(nps_score=0)
        bd = _compute_breakdown(sig)
        factors = _compute_risk_factors(sig, bd)
        assert not any("NPS" in f for f in factors)

    def test_churning_has_multiple_flags(self, churning):
        bd = _compute_breakdown(churning)
        factors = _compute_risk_factors(churning, bd)
        # churning fixture has: days=35(high recency), tickets=4, contract=1, trend=-0.7, nps=-40
        assert len(factors) >= 4

    def test_all_five_flags_can_trigger(self):
        sig = self._make_signals(
            days_since_last_login=20,   # login_recency > 50
            open_support_tickets=3,      # tickets >= 3
            contract_months_remaining=2, # <= 3
            engagement_trend=-0.5,       # < -0.3
            nps_score=-10,               # < 0
        )
        bd = _compute_breakdown(sig)
        factors = _compute_risk_factors(sig, bd)
        assert len(factors) == 5


# ---------------------------------------------------------------------------
# TestCustomerRetention
# ---------------------------------------------------------------------------

class TestCustomerRetention:
    def test_analyze_returns_retention_profile(self, retention, healthy):
        profile = retention.analyze(healthy)
        assert isinstance(profile, RetentionProfile)

    def test_analyze_stores_result(self, retention, healthy):
        retention.analyze(healthy)
        assert retention.get("healthy-001") is not None

    def test_get_returns_none_for_unknown_id(self, retention):
        assert retention.get("nonexistent") is None

    def test_get_returns_correct_profile(self, retention, healthy):
        profile = retention.analyze(healthy)
        retrieved = retention.get("healthy-001")
        assert retrieved is profile

    def test_analyze_batch(self, retention, healthy, churning):
        results = retention.analyze_batch([healthy, churning])
        assert len(results) == 2
        assert all(isinstance(r, RetentionProfile) for r in results)

    def test_analyze_batch_stores_all(self, retention, healthy, churning):
        retention.analyze_batch([healthy, churning])
        assert retention.get("healthy-001") is not None
        assert retention.get("churning-001") is not None

    def test_all_customers_sorted_by_churn_score_desc(self, retention, healthy, churning):
        retention.analyze_batch([healthy, churning])
        customers = retention.all_customers()
        assert len(customers) == 2
        scores = [c.churn_score for c in customers]
        assert scores == sorted(scores, reverse=True)

    def test_all_customers_empty(self, retention):
        assert retention.all_customers() == []

    def test_at_risk_returns_high_and_critical(self, retention, healthy, churning):
        retention.analyze_batch([healthy, churning])
        at_risk = retention.at_risk()
        for p in at_risk:
            assert p.churn_risk in (ChurnRisk.HIGH, ChurnRisk.CRITICAL)

    def test_at_risk_excludes_low_medium(self, retention, healthy):
        retention.analyze(healthy)
        at_risk = retention.at_risk()
        # healthy customer should be LOW, so not in at_risk
        assert len(at_risk) == 0

    def test_at_risk_includes_churning(self, retention, churning):
        retention.analyze(churning)
        at_risk = retention.at_risk()
        assert len(at_risk) >= 1

    def test_by_risk_filter(self, retention, healthy, churning):
        retention.analyze_batch([healthy, churning])
        low_customers = retention.by_risk(ChurnRisk.LOW)
        for p in low_customers:
            assert p.churn_risk == ChurnRisk.LOW

    def test_by_risk_empty_for_missing_category(self, retention, healthy):
        retention.analyze(healthy)
        # healthy should be LOW, so CRITICAL bucket is empty
        assert retention.by_risk(ChurnRisk.CRITICAL) == []

    def test_top_ltv_default_n(self, retention):
        signals_list = [
            CustomerSignals(
                customer_id=f"c{i}",
                name=f"Customer {i}",
                company=f"Corp{i}",
                sector="Tech",
                days_since_last_login=1,
                open_support_tickets=0,
                contract_months_remaining=24,
                engagement_trend=0.8,
                nps_score=60,
                avg_monthly_revenue_eur=float(i * 100),
                months_as_customer=12,
            )
            for i in range(1, 8)
        ]
        retention.analyze_batch(signals_list)
        top = retention.top_ltv()
        assert len(top) == 5

    def test_top_ltv_sorted_by_ltv_desc(self, retention, healthy, churning):
        retention.analyze_batch([healthy, churning])
        top = retention.top_ltv(n=2)
        ltvs = [p.ltv_eur for p in top]
        assert ltvs == sorted(ltvs, reverse=True)

    def test_top_ltv_custom_n(self, retention, healthy, churning):
        retention.analyze_batch([healthy, churning])
        top = retention.top_ltv(n=1)
        assert len(top) == 1

    def test_expiring_soon_default_threshold(self, retention, healthy, churning):
        retention.analyze_batch([healthy, churning])
        expiring = retention.expiring_soon()
        # churning has contract_months_remaining=1 (≤3), healthy has 24 (>3)
        ids = [p.signals.customer_id for p in expiring]
        assert "churning-001" in ids
        assert "healthy-001" not in ids

    def test_expiring_soon_custom_threshold(self, retention, healthy, churning):
        retention.analyze_batch([healthy, churning])
        # With a very large threshold, both should appear
        expiring = retention.expiring_soon(months=100)
        assert len(expiring) == 2

    def test_expiring_soon_at_boundary(self, retention):
        sig = CustomerSignals(
            customer_id="boundary-001",
            name="Boundary",
            company="BoundaryCo",
            sector="Tech",
            days_since_last_login=1,
            open_support_tickets=0,
            contract_months_remaining=3,
            engagement_trend=0.0,
            nps_score=0,
            avg_monthly_revenue_eur=100.0,
            months_as_customer=6,
        )
        retention.analyze(sig)
        expiring = retention.expiring_soon(months=3)
        assert len(expiring) == 1

    def test_portfolio_summary_empty(self, retention):
        summary = retention.portfolio_summary()
        assert summary["total"] == 0
        assert summary["avg_churn_score"] == 0.0
        assert summary["total_ltv_eur"] == 0.0
        assert summary["total_monthly_revenue_eur"] == 0.0
        assert summary["at_risk_revenue_eur"] == 0.0

    def test_portfolio_summary_keys(self, retention, healthy, churning):
        retention.analyze_batch([healthy, churning])
        summary = retention.portfolio_summary()
        expected_keys = {
            "total", "risk_counts", "avg_churn_score",
            "total_ltv_eur", "total_monthly_revenue_eur", "at_risk_revenue_eur",
        }
        assert set(summary.keys()) == expected_keys

    def test_portfolio_summary_total(self, retention, healthy, churning):
        retention.analyze_batch([healthy, churning])
        summary = retention.portfolio_summary()
        assert summary["total"] == 2

    def test_portfolio_summary_risk_counts_keys(self, retention, healthy):
        retention.analyze(healthy)
        summary = retention.portfolio_summary()
        assert set(summary["risk_counts"].keys()) == {"low", "medium", "high", "critical"}

    def test_portfolio_summary_risk_counts_sum(self, retention, healthy, churning):
        retention.analyze_batch([healthy, churning])
        summary = retention.portfolio_summary()
        total_in_counts = sum(summary["risk_counts"].values())
        assert total_in_counts == 2

    def test_portfolio_summary_avg_churn_score(self, retention, healthy, churning):
        profiles = retention.analyze_batch([healthy, churning])
        expected_avg = round(sum(p.churn_score for p in profiles) / 2, 4)
        summary = retention.portfolio_summary()
        assert summary["avg_churn_score"] == pytest.approx(expected_avg)

    def test_portfolio_summary_total_revenue(self, retention, healthy, churning):
        retention.analyze_batch([healthy, churning])
        summary = retention.portfolio_summary()
        # healthy=500 + churning=300
        assert summary["total_monthly_revenue_eur"] == pytest.approx(800.0)

    def test_portfolio_summary_at_risk_revenue(self, retention, churning):
        retention.analyze(churning)
        summary = retention.portfolio_summary()
        # churning is HIGH or CRITICAL → its revenue counts
        at_risk_profile = retention.at_risk()
        if at_risk_profile:
            assert summary["at_risk_revenue_eur"] == pytest.approx(300.0)

    def test_portfolio_summary_total_ltv(self, retention, healthy, churning):
        profiles = retention.analyze_batch([healthy, churning])
        expected_ltv = round(sum(p.ltv_eur for p in profiles), 2)
        summary = retention.portfolio_summary()
        assert summary["total_ltv_eur"] == pytest.approx(expected_ltv)

    def test_reset_clears_store(self, retention, healthy, churning):
        retention.analyze_batch([healthy, churning])
        retention.reset()
        assert retention.all_customers() == []
        assert retention.get("healthy-001") is None
        assert retention.get("churning-001") is None

    def test_reset_then_reanalyze(self, retention, healthy):
        retention.analyze(healthy)
        retention.reset()
        retention.analyze(healthy)
        assert retention.get("healthy-001") is not None

    def test_analyze_overwrites_existing(self, retention, healthy):
        p1 = retention.analyze(healthy)
        # Re-analyze the same customer — should overwrite
        p2 = retention.analyze(healthy)
        assert retention.get("healthy-001") is p2

    def test_retention_actions_not_empty(self, retention, healthy, churning):
        for sig in (healthy, churning):
            p = retention.analyze(sig)
            assert len(p.retention_actions) > 0

    def test_healthy_has_low_churn_actions(self, retention, healthy):
        p = retention.analyze(healthy)
        if p.churn_risk == ChurnRisk.LOW:
            assert any("upsell" in a.lower() or "ambassadeur" in a.lower() for a in p.retention_actions)
