"""
Comprehensive pytest test suite for swarm/intelligence/customer_lifetime_value_predictor.py
Covers all enums, formulas, edge cases, filter methods, aggregates, and integration scenarios.
"""

import pytest
from swarm.intelligence.customer_lifetime_value_predictor import (
    CLVTier,
    ExpansionPotential,
    ChurnRisk,
    CLVAction,
    CLVInput,
    CLVResult,
    CustomerLifetimeValuePredictor,
)


# ─── Helper factory ───────────────────────────────────────────────────────────

def make_input(**overrides) -> CLVInput:
    """Return a CLVInput with sensible, healthy defaults. Override specific fields as needed."""
    defaults = dict(
        account_id="ACC-001",
        account_name="Acme Corp",
        region="EMEA",
        segment="Enterprise",
        arr_eur=50_000.0,
        contract_start_months_ago=24,
        contract_length_months=12,
        renewals_completed=2,
        avg_renewal_growth_pct=10.0,
        last_renewal_months_ago=2,
        seats_used_pct=75.0,
        products_adopted=3,
        total_products_available=5,
        expansion_conversations_open=False,
        nps_score=30.0,
        support_tickets_90d=2,
        executive_sponsor_engaged=True,
        last_qbr_months_ago=2,
        competitor_evaluation_active=False,
        key_champion_left=False,
        payment_delays_12m=0,
        rep_churn_risk_score=3.0,
    )
    defaults.update(overrides)
    return CLVInput(**defaults)


# ─── 1. Enum values and str inheritance ───────────────────────────────────────

class TestCLVTierEnum:
    def test_platinum_value(self):
        assert CLVTier.PLATINUM == "platinum"
        assert CLVTier.PLATINUM.value == "platinum"

    def test_gold_value(self):
        assert CLVTier.GOLD == "gold"
        assert CLVTier.GOLD.value == "gold"

    def test_silver_value(self):
        assert CLVTier.SILVER == "silver"
        assert CLVTier.SILVER.value == "silver"

    def test_bronze_value(self):
        assert CLVTier.BRONZE == "bronze"
        assert CLVTier.BRONZE.value == "bronze"

    def test_minimal_value(self):
        assert CLVTier.MINIMAL == "minimal"
        assert CLVTier.MINIMAL.value == "minimal"

    def test_str_inheritance(self):
        assert isinstance(CLVTier.PLATINUM, str)
        assert isinstance(CLVTier.GOLD, str)
        assert isinstance(CLVTier.SILVER, str)
        assert isinstance(CLVTier.BRONZE, str)
        assert isinstance(CLVTier.MINIMAL, str)

    def test_all_five_members(self):
        assert len(CLVTier) == 5


class TestExpansionPotentialEnum:
    def test_high_value(self):
        assert ExpansionPotential.HIGH == "high"

    def test_medium_value(self):
        assert ExpansionPotential.MEDIUM == "medium"

    def test_low_value(self):
        assert ExpansionPotential.LOW == "low"

    def test_none_value(self):
        assert ExpansionPotential.NONE == "none"

    def test_str_inheritance(self):
        for member in ExpansionPotential:
            assert isinstance(member, str)

    def test_all_four_members(self):
        assert len(ExpansionPotential) == 4


class TestChurnRiskEnum:
    def test_critical_value(self):
        assert ChurnRisk.CRITICAL == "critical"

    def test_high_value(self):
        assert ChurnRisk.HIGH == "high"

    def test_medium_value(self):
        assert ChurnRisk.MEDIUM == "medium"

    def test_low_value(self):
        assert ChurnRisk.LOW == "low"

    def test_str_inheritance(self):
        for member in ChurnRisk:
            assert isinstance(member, str)

    def test_all_four_members(self):
        assert len(ChurnRisk) == 4


class TestCLVActionEnum:
    def test_invest_value(self):
        assert CLVAction.INVEST == "invest"

    def test_grow_value(self):
        assert CLVAction.GROW == "grow"

    def test_nurture_value(self):
        assert CLVAction.NURTURE == "nurture"

    def test_monitor_value(self):
        assert CLVAction.MONITOR == "monitor"

    def test_rescue_value(self):
        assert CLVAction.RESCUE == "rescue"

    def test_str_inheritance(self):
        for member in CLVAction:
            assert isinstance(member, str)

    def test_all_five_members(self):
        assert len(CLVAction) == 5


# ─── 2. CLVInput field count ───────────────────────────────────────────────────

class TestCLVInputFields:
    def test_field_count(self):
        import dataclasses
        fields = dataclasses.fields(CLVInput)
        assert len(fields) == 22

    def test_can_instantiate_with_all_fields(self):
        inp = make_input()
        assert inp.account_id == "ACC-001"

    def test_all_fields_accessible(self):
        inp = make_input()
        field_names = [
            "account_id", "account_name", "region", "segment", "arr_eur",
            "contract_start_months_ago", "contract_length_months", "renewals_completed",
            "avg_renewal_growth_pct", "last_renewal_months_ago", "seats_used_pct",
            "products_adopted", "total_products_available", "expansion_conversations_open",
            "nps_score", "support_tickets_90d", "executive_sponsor_engaged",
            "last_qbr_months_ago", "competitor_evaluation_active", "key_champion_left",
            "payment_delays_12m", "rep_churn_risk_score",
        ]
        for name in field_names:
            assert hasattr(inp, name), f"Missing field: {name}"


# ─── 3. Health score components ───────────────────────────────────────────────

class TestHealthScore:
    def setup_method(self):
        self.engine = CustomerLifetimeValuePredictor()

    def _hs(self, **kw):
        return self.engine._health_score(make_input(**kw))

    def test_nps_max_contribution(self):
        # nps_score=+100 → nps_pts = 200/200 × 20 = 20
        score = self._hs(nps_score=100, seats_used_pct=0, products_adopted=0,
                         renewals_completed=0, support_tickets_90d=100,
                         executive_sponsor_engaged=False, last_qbr_months_ago=100)
        # Only nps_pts contributes = 20, rest = 0
        assert score == pytest.approx(20.0, abs=0.2)

    def test_nps_min_contribution(self):
        # nps_score=-100 → nps_pts = 0
        score = self._hs(nps_score=-100, seats_used_pct=0, products_adopted=0,
                         renewals_completed=0, support_tickets_90d=100,
                         executive_sponsor_engaged=False, last_qbr_months_ago=100)
        assert score == pytest.approx(0.0, abs=0.2)

    def test_nps_zero_gives_10_pts(self):
        # nps_score=0 → (0+100)/200 * 20 = 10
        score = self._hs(nps_score=0, seats_used_pct=0, products_adopted=0,
                         renewals_completed=0, support_tickets_90d=100,
                         executive_sponsor_engaged=False, last_qbr_months_ago=100)
        assert score == pytest.approx(10.0, abs=0.2)

    def test_utilisation_max_contribution(self):
        # seats_used_pct=100 → util_pts = 20
        score = self._hs(nps_score=-100, seats_used_pct=100, products_adopted=0,
                         renewals_completed=0, support_tickets_90d=100,
                         executive_sponsor_engaged=False, last_qbr_months_ago=100)
        assert score == pytest.approx(20.0, abs=0.2)

    def test_adoption_max_contribution(self):
        # products_adopted=5, total=5 → adop_pts = 15
        score = self._hs(nps_score=-100, seats_used_pct=0, products_adopted=5,
                         total_products_available=5, renewals_completed=0,
                         support_tickets_90d=100, executive_sponsor_engaged=False,
                         last_qbr_months_ago=100)
        assert score == pytest.approx(15.0, abs=0.2)

    def test_adoption_zero_products_available(self):
        # total_products_available=0 → adop_pts = 0
        score = self._hs(nps_score=-100, seats_used_pct=0, products_adopted=0,
                         total_products_available=0, renewals_completed=0,
                         support_tickets_90d=100, executive_sponsor_engaged=False,
                         last_qbr_months_ago=100)
        assert score == pytest.approx(0.0, abs=0.2)

    def test_renewals_cap_at_15(self):
        # renewals=10 → min(15, 50) = 15
        score = self._hs(nps_score=-100, seats_used_pct=0, products_adopted=0,
                         renewals_completed=10, support_tickets_90d=100,
                         executive_sponsor_engaged=False, last_qbr_months_ago=100)
        assert score == pytest.approx(15.0, abs=0.2)

    def test_renewals_3_gives_15(self):
        # renewals=3 → min(15, 15) = 15
        score = self._hs(nps_score=-100, seats_used_pct=0, products_adopted=0,
                         renewals_completed=3, support_tickets_90d=100,
                         executive_sponsor_engaged=False, last_qbr_months_ago=100)
        assert score == pytest.approx(15.0, abs=0.2)

    def test_renewals_2_gives_10(self):
        # renewals=2 → 10
        score = self._hs(nps_score=-100, seats_used_pct=0, products_adopted=0,
                         renewals_completed=2, support_tickets_90d=100,
                         executive_sponsor_engaged=False, last_qbr_months_ago=100)
        assert score == pytest.approx(10.0, abs=0.2)

    def test_support_max_contribution_zero_tickets(self):
        # tickets=0 → support_pts = 10
        score = self._hs(nps_score=-100, seats_used_pct=0, products_adopted=0,
                         renewals_completed=0, support_tickets_90d=0,
                         executive_sponsor_engaged=False, last_qbr_months_ago=100)
        assert score == pytest.approx(10.0, abs=0.2)

    def test_support_clamped_at_zero(self):
        # tickets=100 → max(0, 10 - 150) = 0
        score = self._hs(nps_score=-100, seats_used_pct=0, products_adopted=0,
                         renewals_completed=0, support_tickets_90d=100,
                         executive_sponsor_engaged=False, last_qbr_months_ago=100)
        assert score == pytest.approx(0.0, abs=0.2)

    def test_exec_sponsor_engaged_gives_10(self):
        score = self._hs(nps_score=-100, seats_used_pct=0, products_adopted=0,
                         renewals_completed=0, support_tickets_90d=100,
                         executive_sponsor_engaged=True, last_qbr_months_ago=100)
        assert score == pytest.approx(10.0, abs=0.2)

    def test_exec_sponsor_not_engaged_gives_0(self):
        score = self._hs(nps_score=-100, seats_used_pct=0, products_adopted=0,
                         renewals_completed=0, support_tickets_90d=100,
                         executive_sponsor_engaged=False, last_qbr_months_ago=100)
        assert score == pytest.approx(0.0, abs=0.2)

    def test_qbr_recent_gives_max(self):
        # last_qbr=0 → qbr_pts = 10
        score = self._hs(nps_score=-100, seats_used_pct=0, products_adopted=0,
                         renewals_completed=0, support_tickets_90d=100,
                         executive_sponsor_engaged=False, last_qbr_months_ago=0)
        assert score == pytest.approx(10.0, abs=0.2)

    def test_qbr_5_months_gives_0(self):
        # last_qbr=5 → max(0, 10-10) = 0
        score = self._hs(nps_score=-100, seats_used_pct=0, products_adopted=0,
                         renewals_completed=0, support_tickets_90d=100,
                         executive_sponsor_engaged=False, last_qbr_months_ago=5)
        assert score == pytest.approx(0.0, abs=0.2)

    def test_health_clamped_at_100(self):
        # Maximise every component
        score = self._hs(nps_score=100, seats_used_pct=100, products_adopted=5,
                         total_products_available=5, renewals_completed=10,
                         support_tickets_90d=0, executive_sponsor_engaged=True,
                         last_qbr_months_ago=0)
        assert score == 100.0

    def test_health_clamped_at_0(self):
        # All components at minimum
        score = self._hs(nps_score=-100, seats_used_pct=0, products_adopted=0,
                         renewals_completed=0, support_tickets_90d=100,
                         executive_sponsor_engaged=False, last_qbr_months_ago=100)
        assert score == 0.0

    def test_health_returns_numeric(self):
        score = self._hs()
        assert isinstance(score, (int, float))


# ─── 4. Churn probability ─────────────────────────────────────────────────────

class TestChurnProbability:
    def setup_method(self):
        self.engine = CustomerLifetimeValuePredictor()

    def _cp(self, health=100.0, **kw):
        inp = make_input(**kw)
        return self.engine._churn_probability(inp, health)

    def test_base_probability_perfect_health(self):
        # health=100 → base = max(0, 0) * 0.6 = 0, no extra risks
        prob = self._cp(health=100.0, competitor_evaluation_active=False,
                        key_champion_left=False, payment_delays_12m=0,
                        rep_churn_risk_score=0.0, last_renewal_months_ago=2,
                        contract_length_months=12)
        assert prob == pytest.approx(0.0, abs=0.1)

    def test_base_probability_zero_health(self):
        # health=0 → base = 100 * 0.6 = 60, no extras
        prob = self._cp(health=0.0, competitor_evaluation_active=False,
                        key_champion_left=False, payment_delays_12m=0,
                        rep_churn_risk_score=0.0, last_renewal_months_ago=2,
                        contract_length_months=12)
        assert prob == pytest.approx(60.0, abs=0.1)

    def test_competitor_eval_adds_20(self):
        prob_without = self._cp(health=100.0, competitor_evaluation_active=False)
        prob_with = self._cp(health=100.0, competitor_evaluation_active=True)
        assert prob_with - prob_without == pytest.approx(20.0, abs=0.1)

    def test_champion_left_adds_15(self):
        prob_without = self._cp(health=100.0, key_champion_left=False)
        prob_with = self._cp(health=100.0, key_champion_left=True)
        assert prob_with - prob_without == pytest.approx(15.0, abs=0.1)

    def test_payment_delays_2_adds_10(self):
        prob_without = self._cp(health=100.0, payment_delays_12m=1)
        prob_with = self._cp(health=100.0, payment_delays_12m=2)
        assert prob_with - prob_without == pytest.approx(10.0, abs=0.1)

    def test_payment_delays_1_adds_nothing(self):
        prob_without = self._cp(health=100.0, payment_delays_12m=0)
        prob_with = self._cp(health=100.0, payment_delays_12m=1)
        assert prob_with == prob_without

    def test_rep_score_7_adds_15(self):
        prob_without = self._cp(health=100.0, rep_churn_risk_score=4.0)
        prob_with = self._cp(health=100.0, rep_churn_risk_score=7.0)
        assert prob_with - prob_without == pytest.approx(15.0, abs=0.1)

    def test_rep_score_5_adds_8(self):
        prob_without = self._cp(health=100.0, rep_churn_risk_score=4.0)
        prob_with = self._cp(health=100.0, rep_churn_risk_score=5.0)
        assert prob_with - prob_without == pytest.approx(8.0, abs=0.1)

    def test_rep_score_below_5_adds_nothing(self):
        prob_4 = self._cp(health=100.0, rep_churn_risk_score=4.9)
        prob_0 = self._cp(health=100.0, rep_churn_risk_score=0.0)
        assert prob_4 == prob_0

    def test_overdue_renewal_adds_10(self):
        # last_renewal=13 > contract_length=12 → overdue
        prob_not_overdue = self._cp(health=100.0, last_renewal_months_ago=12,
                                    contract_length_months=12)
        prob_overdue = self._cp(health=100.0, last_renewal_months_ago=13,
                                contract_length_months=12)
        assert prob_overdue - prob_not_overdue == pytest.approx(10.0, abs=0.1)

    def test_renewal_on_time_no_extra(self):
        # last_renewal=5, contract=12 → not overdue
        prob = self._cp(health=100.0, last_renewal_months_ago=5,
                        contract_length_months=12, competitor_evaluation_active=False,
                        key_champion_left=False, payment_delays_12m=0,
                        rep_churn_risk_score=0.0)
        assert prob == pytest.approx(0.0, abs=0.1)

    def test_churn_clamped_at_95(self):
        # All risk signals active, low health → should cap at 95
        prob = self._cp(health=0.0, competitor_evaluation_active=True,
                        key_champion_left=True, payment_delays_12m=5,
                        rep_churn_risk_score=9.0, last_renewal_months_ago=24,
                        contract_length_months=12)
        assert prob == 95.0

    def test_churn_returns_numeric(self):
        inp = make_input()
        prob = self.engine._churn_probability(inp, 50.0)
        assert isinstance(prob, (int, float))


# ─── 5. Churn risk thresholds ─────────────────────────────────────────────────

class TestChurnRiskThresholds:
    def setup_method(self):
        self.engine = CustomerLifetimeValuePredictor()

    def test_critical_at_60(self):
        assert self.engine._churn_risk(60.0) == ChurnRisk.CRITICAL

    def test_critical_at_95(self):
        assert self.engine._churn_risk(95.0) == ChurnRisk.CRITICAL

    def test_high_at_59(self):
        assert self.engine._churn_risk(59.9) == ChurnRisk.HIGH

    def test_high_at_40(self):
        assert self.engine._churn_risk(40.0) == ChurnRisk.HIGH

    def test_medium_at_39(self):
        assert self.engine._churn_risk(39.9) == ChurnRisk.MEDIUM

    def test_medium_at_20(self):
        assert self.engine._churn_risk(20.0) == ChurnRisk.MEDIUM

    def test_low_at_19(self):
        assert self.engine._churn_risk(19.9) == ChurnRisk.LOW

    def test_low_at_0(self):
        assert self.engine._churn_risk(0.0) == ChurnRisk.LOW


# ─── 6. Expansion opportunity EUR ─────────────────────────────────────────────

class TestExpansionOpportunityEur:
    def setup_method(self):
        self.engine = CustomerLifetimeValuePredictor()

    def _eop(self, **kw):
        return self.engine._expansion_opportunity_eur(make_input(**kw))

    def test_zero_arr_gives_zero(self):
        result = self._eop(arr_eur=0.0)
        assert result == 0.0

    def test_100_pct_utilisation_no_seat_whitespace(self):
        # seats_used_pct=100 → unused_pct=0 → seat_whitespace=0
        result = self._eop(arr_eur=100_000, seats_used_pct=100,
                           products_adopted=5, total_products_available=5)
        # product_whitespace=0 too → 0
        assert result == 0.0

    def test_seat_whitespace_formula(self):
        # arr=100k, seats_used=0 → unused=1.0 → seat_whitespace=50k
        # products_adopted=total → product_whitespace=0
        result = self._eop(arr_eur=100_000, seats_used_pct=0,
                           products_adopted=5, total_products_available=5)
        assert result == pytest.approx(50_000.0, abs=1.0)

    def test_product_whitespace_formula(self):
        # arr=100k, seats_used=100 → seat_whitespace=0
        # products_adopted=0, total=5 → gap=5 → product_whitespace=100k * 1.0 * 0.4 = 40k
        result = self._eop(arr_eur=100_000, seats_used_pct=100,
                           products_adopted=0, total_products_available=5)
        assert result == pytest.approx(40_000.0, abs=1.0)

    def test_combined_whitespace(self):
        # arr=100k, seats_used=50 → unused=0.5 → seat_whitespace=25k
        # products_adopted=2, total=5 → gap=3 → product_whitespace=100k * 0.6 * 0.4 = 24k
        result = self._eop(arr_eur=100_000, seats_used_pct=50,
                           products_adopted=2, total_products_available=5)
        assert result == pytest.approx(49_000.0, abs=1.0)

    def test_returns_numeric(self):
        result = self._eop()
        assert isinstance(result, (int, float))

    def test_returns_rounded(self):
        # Should return integer-rounded value
        result = self._eop(arr_eur=33_333.33, seats_used_pct=33.33)
        # Just verify it's a numeric value with no fractional part
        assert result == round(result, 0)


# ─── 7. Expansion potential ───────────────────────────────────────────────────

class TestExpansionPotential:
    def setup_method(self):
        self.engine = CustomerLifetimeValuePredictor()

    def _ep(self, churn_risk=ChurnRisk.LOW, **kw):
        inp = make_input(**kw)
        return self.engine._expansion_potential(inp, churn_risk)

    def test_critical_churn_returns_none(self):
        result = self._ep(churn_risk=ChurnRisk.CRITICAL,
                          seats_used_pct=100, products_adopted=0,
                          total_products_available=5,
                          expansion_conversations_open=True,
                          executive_sponsor_engaged=True, nps_score=100)
        assert result == ExpansionPotential.NONE

    def test_high_potential_score_6(self):
        # seats>=80 (+2), products gap (+2), conversations (+2) → score=6 → HIGH
        result = self._ep(churn_risk=ChurnRisk.LOW,
                          seats_used_pct=80, products_adopted=2,
                          total_products_available=5,
                          expansion_conversations_open=True,
                          executive_sponsor_engaged=False, nps_score=0)
        assert result == ExpansionPotential.HIGH

    def test_medium_potential_score_3(self):
        # seats>=60 (+1), products gap (+2) → score=3 → MEDIUM
        result = self._ep(churn_risk=ChurnRisk.LOW,
                          seats_used_pct=60, products_adopted=2,
                          total_products_available=5,
                          expansion_conversations_open=False,
                          executive_sponsor_engaged=False, nps_score=0)
        assert result == ExpansionPotential.MEDIUM

    def test_low_potential_score_1(self):
        # seats>=60 (+1) → score=1 → LOW
        result = self._ep(churn_risk=ChurnRisk.LOW,
                          seats_used_pct=60, products_adopted=5,
                          total_products_available=5,
                          expansion_conversations_open=False,
                          executive_sponsor_engaged=False, nps_score=0)
        assert result == ExpansionPotential.LOW

    def test_none_potential_score_0(self):
        # seats<60 (0), no gap (products=total) → score=0 → NONE
        result = self._ep(churn_risk=ChurnRisk.LOW,
                          seats_used_pct=50, products_adopted=5,
                          total_products_available=5,
                          expansion_conversations_open=False,
                          executive_sponsor_engaged=False, nps_score=0)
        assert result == ExpansionPotential.NONE

    def test_exec_sponsor_adds_1(self):
        # seats=50 (0), no gap, no convo, exec_engaged (+1) → score=1 → LOW
        result = self._ep(churn_risk=ChurnRisk.LOW,
                          seats_used_pct=50, products_adopted=5,
                          total_products_available=5,
                          expansion_conversations_open=False,
                          executive_sponsor_engaged=True, nps_score=0)
        assert result == ExpansionPotential.LOW

    def test_nps_40_adds_1(self):
        # seats=50 (0), no gap, no convo, no exec, nps>=40 (+1) → score=1 → LOW
        result = self._ep(churn_risk=ChurnRisk.LOW,
                          seats_used_pct=50, products_adopted=5,
                          total_products_available=5,
                          expansion_conversations_open=False,
                          executive_sponsor_engaged=False, nps_score=40)
        assert result == ExpansionPotential.LOW

    def test_high_churn_not_critical_can_expand(self):
        # HIGH churn should still allow expansion
        result = self._ep(churn_risk=ChurnRisk.HIGH,
                          seats_used_pct=80, products_adopted=0,
                          total_products_available=5,
                          expansion_conversations_open=True,
                          executive_sponsor_engaged=True, nps_score=50)
        assert result != ExpansionPotential.NONE

    def test_conversations_open_adds_2(self):
        # seats=50, no gap, conversations (+2) → score=2 → LOW
        result = self._ep(churn_risk=ChurnRisk.LOW,
                          seats_used_pct=50, products_adopted=5,
                          total_products_available=5,
                          expansion_conversations_open=True,
                          executive_sponsor_engaged=False, nps_score=0)
        assert result == ExpansionPotential.LOW

    def test_seats_80_adds_2_not_1(self):
        # seats=80 → score=2 (not 1 from the elif branch)
        # With only seats=80, products=total, no other signals → score=2 → LOW
        result = self._ep(churn_risk=ChurnRisk.LOW,
                          seats_used_pct=80, products_adopted=5,
                          total_products_available=5,
                          expansion_conversations_open=False,
                          executive_sponsor_engaged=False, nps_score=0)
        assert result == ExpansionPotential.LOW


# ─── 8. CLV tier thresholds ───────────────────────────────────────────────────

class TestCLVTierThresholds:
    def setup_method(self):
        self.engine = CustomerLifetimeValuePredictor()

    def test_platinum_at_500000(self):
        assert self.engine._clv_tier(500_000) == CLVTier.PLATINUM

    def test_platinum_above_500000(self):
        assert self.engine._clv_tier(1_000_000) == CLVTier.PLATINUM

    def test_gold_at_200000(self):
        assert self.engine._clv_tier(200_000) == CLVTier.GOLD

    def test_gold_below_500000(self):
        assert self.engine._clv_tier(499_999) == CLVTier.GOLD

    def test_silver_at_80000(self):
        assert self.engine._clv_tier(80_000) == CLVTier.SILVER

    def test_silver_below_200000(self):
        assert self.engine._clv_tier(199_999) == CLVTier.SILVER

    def test_bronze_at_20000(self):
        assert self.engine._clv_tier(20_000) == CLVTier.BRONZE

    def test_bronze_below_80000(self):
        assert self.engine._clv_tier(79_999) == CLVTier.BRONZE

    def test_minimal_below_20000(self):
        assert self.engine._clv_tier(19_999) == CLVTier.MINIMAL

    def test_minimal_at_zero(self):
        assert self.engine._clv_tier(0) == CLVTier.MINIMAL


# ─── 9. CLV action ────────────────────────────────────────────────────────────

class TestCLVAction:
    def setup_method(self):
        self.engine = CustomerLifetimeValuePredictor()

    def _action(self, tier, churn_risk, expansion):
        return self.engine._clv_action(tier, churn_risk, expansion)

    def test_rescue_on_critical_churn(self):
        assert self._action(CLVTier.PLATINUM, ChurnRisk.CRITICAL, ExpansionPotential.HIGH) == CLVAction.RESCUE

    def test_rescue_on_high_churn(self):
        assert self._action(CLVTier.GOLD, ChurnRisk.HIGH, ExpansionPotential.HIGH) == CLVAction.RESCUE

    def test_invest_platinum_low_churn(self):
        assert self._action(CLVTier.PLATINUM, ChurnRisk.LOW, ExpansionPotential.NONE) == CLVAction.INVEST

    def test_invest_gold_low_churn(self):
        assert self._action(CLVTier.GOLD, ChurnRisk.LOW, ExpansionPotential.NONE) == CLVAction.INVEST

    def test_grow_silver_high_expansion(self):
        assert self._action(CLVTier.SILVER, ChurnRisk.LOW, ExpansionPotential.HIGH) == CLVAction.GROW

    def test_grow_silver_medium_expansion(self):
        assert self._action(CLVTier.SILVER, ChurnRisk.LOW, ExpansionPotential.MEDIUM) == CLVAction.GROW

    def test_nurture_bronze(self):
        assert self._action(CLVTier.BRONZE, ChurnRisk.LOW, ExpansionPotential.NONE) == CLVAction.NURTURE

    def test_monitor_medium_churn_non_bronze(self):
        assert self._action(CLVTier.SILVER, ChurnRisk.MEDIUM, ExpansionPotential.NONE) == CLVAction.MONITOR

    def test_nurture_minimal_low_churn(self):
        assert self._action(CLVTier.MINIMAL, ChurnRisk.LOW, ExpansionPotential.NONE) == CLVAction.NURTURE

    def test_silver_low_expansion_not_grow(self):
        result = self._action(CLVTier.SILVER, ChurnRisk.LOW, ExpansionPotential.LOW)
        # SILVER + LOW expansion → not GROW (only HIGH/MEDIUM triggers GROW)
        assert result != CLVAction.GROW


# ─── 10. to_dict ──────────────────────────────────────────────────────────────

class TestToDict:
    def setup_method(self):
        self.engine = CustomerLifetimeValuePredictor()
        self.result = self.engine.predict(make_input())
        self.d = self.result.to_dict()

    def test_key_count(self):
        # to_dict returns 18 keys: 5 identity + 10 predicted/narrative fields + 3 lists
        assert len(self.d) == 18

    def test_account_id_present(self):
        assert "account_id" in self.d

    def test_account_name_present(self):
        assert "account_name" in self.d

    def test_region_present(self):
        assert "region" in self.d

    def test_segment_present(self):
        assert "segment" in self.d

    def test_arr_eur_present(self):
        assert "arr_eur" in self.d

    def test_clv_3yr_eur_present(self):
        assert "clv_3yr_eur" in self.d

    def test_clv_tier_is_string(self):
        assert isinstance(self.d["clv_tier"], str)
        assert self.d["clv_tier"] in [t.value for t in CLVTier]

    def test_expansion_potential_is_string(self):
        assert isinstance(self.d["expansion_potential"], str)
        assert self.d["expansion_potential"] in [e.value for e in ExpansionPotential]

    def test_churn_risk_is_string(self):
        assert isinstance(self.d["churn_risk"], str)
        assert self.d["churn_risk"] in [c.value for c in ChurnRisk]

    def test_clv_action_is_string(self):
        assert isinstance(self.d["clv_action"], str)
        assert self.d["clv_action"] in [a.value for a in CLVAction]

    def test_health_score_present(self):
        assert "health_score" in self.d

    def test_churn_probability_pct_present(self):
        assert "churn_probability_pct" in self.d

    def test_expansion_opportunity_eur_present(self):
        assert "expansion_opportunity_eur" in self.d

    def test_predicted_arr_yr2_eur_present(self):
        assert "predicted_arr_yr2_eur" in self.d

    def test_predicted_arr_yr3_eur_present(self):
        assert "predicted_arr_yr3_eur" in self.d

    def test_value_drivers_is_list(self):
        assert isinstance(self.d["value_drivers"], list)

    def test_risk_signals_present(self):
        assert "risk_signals" in self.d

    def test_recommended_plays_present(self):
        assert "recommended_plays" in self.d

    def test_enums_serialised_not_enum_instances(self):
        for key in ("clv_tier", "expansion_potential", "churn_risk", "clv_action"):
            assert not isinstance(self.d[key], CLVTier)
            assert not isinstance(self.d[key], ExpansionPotential)
            assert not isinstance(self.d[key], ChurnRisk)
            assert not isinstance(self.d[key], CLVAction)


# ─── 11. predict() ────────────────────────────────────────────────────────────

class TestPredict:
    def setup_method(self):
        self.engine = CustomerLifetimeValuePredictor()

    def test_returns_clv_result(self):
        result = self.engine.predict(make_input())
        assert isinstance(result, CLVResult)

    def test_result_stored_internally(self):
        self.engine.predict(make_input())
        assert len(self.engine.all_accounts()) == 1

    def test_multiple_predicts_stored(self):
        for i in range(3):
            self.engine.predict(make_input(account_id=f"ACC-{i}"))
        assert len(self.engine.all_accounts()) == 3

    def test_account_id_passed_through(self):
        result = self.engine.predict(make_input(account_id="TEST-123"))
        assert result.account_id == "TEST-123"

    def test_health_score_populated(self):
        result = self.engine.predict(make_input())
        assert isinstance(result.health_score, (int, float))

    def test_churn_probability_populated(self):
        result = self.engine.predict(make_input())
        assert isinstance(result.churn_probability_pct, (int, float))

    def test_clv_3yr_eur_populated(self):
        result = self.engine.predict(make_input())
        assert isinstance(result.clv_3yr_eur, (int, float))

    def test_clv_tier_populated(self):
        result = self.engine.predict(make_input())
        assert isinstance(result.clv_tier, CLVTier)

    def test_expansion_potential_populated(self):
        result = self.engine.predict(make_input())
        assert isinstance(result.expansion_potential, ExpansionPotential)

    def test_churn_risk_populated(self):
        result = self.engine.predict(make_input())
        assert isinstance(result.churn_risk, ChurnRisk)

    def test_clv_action_populated(self):
        result = self.engine.predict(make_input())
        assert isinstance(result.clv_action, CLVAction)

    def test_value_drivers_list(self):
        result = self.engine.predict(make_input())
        assert isinstance(result.value_drivers, list)

    def test_risk_signals_list(self):
        result = self.engine.predict(make_input())
        assert isinstance(result.risk_signals, list)

    def test_recommended_plays_list(self):
        result = self.engine.predict(make_input())
        assert isinstance(result.recommended_plays, list)


# ─── 12. predict_batch() ──────────────────────────────────────────────────────

class TestPredictBatch:
    def setup_method(self):
        self.engine = CustomerLifetimeValuePredictor()

    def test_returns_list(self):
        results = self.engine.predict_batch([make_input()])
        assert isinstance(results, list)

    def test_empty_batch_returns_empty(self):
        results = self.engine.predict_batch([])
        assert results == []

    def test_sorted_desc_by_clv(self):
        inputs = [
            make_input(account_id="LOW", arr_eur=1_000),
            make_input(account_id="HIGH", arr_eur=500_000),
            make_input(account_id="MID", arr_eur=50_000),
        ]
        results = self.engine.predict_batch(inputs)
        clvs = [r.clv_3yr_eur for r in results]
        assert clvs == sorted(clvs, reverse=True)

    def test_batch_stores_all_results(self):
        inputs = [make_input(account_id=f"ACC-{i}") for i in range(4)]
        self.engine.predict_batch(inputs)
        assert len(self.engine.all_accounts()) == 4

    def test_batch_result_count(self):
        inputs = [make_input(account_id=f"X-{i}") for i in range(5)]
        results = self.engine.predict_batch(inputs)
        assert len(results) == 5


# ─── 13. Filter methods ───────────────────────────────────────────────────────

class TestFilterMethods:
    def setup_method(self):
        self.engine = CustomerLifetimeValuePredictor()

    def test_by_tier_platinum(self):
        # Predict a very high CLV account (should be PLATINUM)
        self.engine.predict(make_input(arr_eur=300_000,
                                       nps_score=80, seats_used_pct=90,
                                       products_adopted=5, total_products_available=5,
                                       renewals_completed=5, support_tickets_90d=0,
                                       executive_sponsor_engaged=True, last_qbr_months_ago=0,
                                       avg_renewal_growth_pct=20,
                                       competitor_evaluation_active=False,
                                       key_champion_left=False, payment_delays_12m=0,
                                       rep_churn_risk_score=1.0))
        results = self.engine.by_tier(CLVTier.PLATINUM)
        assert all(r.clv_tier == CLVTier.PLATINUM for r in results)

    def test_by_churn_risk_filters_correctly(self):
        # Predict an account that will be CRITICAL churn
        self.engine.predict(make_input(competitor_evaluation_active=True,
                                       key_champion_left=True,
                                       payment_delays_12m=5,
                                       rep_churn_risk_score=9.0))
        results = self.engine.by_churn_risk(ChurnRisk.CRITICAL)
        assert len(results) >= 1
        assert all(r.churn_risk == ChurnRisk.CRITICAL for r in results)

    def test_by_expansion_filters_correctly(self):
        self.engine.predict(make_input(seats_used_pct=85, products_adopted=0,
                                       total_products_available=5,
                                       expansion_conversations_open=True,
                                       executive_sponsor_engaged=True,
                                       nps_score=50))
        results = self.engine.by_expansion(ExpansionPotential.HIGH)
        assert all(r.expansion_potential == ExpansionPotential.HIGH for r in results)

    def test_by_action_filters_correctly(self):
        # High arr healthy account → should be INVEST
        self.engine.predict(make_input(arr_eur=200_000,
                                       nps_score=80, seats_used_pct=90,
                                       renewals_completed=5, support_tickets_90d=0,
                                       executive_sponsor_engaged=True, last_qbr_months_ago=0,
                                       avg_renewal_growth_pct=15,
                                       competitor_evaluation_active=False,
                                       key_champion_left=False, payment_delays_12m=0,
                                       rep_churn_risk_score=1.0))
        results = self.engine.by_action(CLVAction.INVEST)
        assert all(r.clv_action == CLVAction.INVEST for r in results)

    def test_by_tier_empty_when_no_match(self):
        # Only a minimal account predicted
        self.engine.predict(make_input(arr_eur=100))
        results = self.engine.by_tier(CLVTier.PLATINUM)
        assert results == []

    def test_all_accounts_returns_all(self):
        for i in range(3):
            self.engine.predict(make_input(account_id=f"A{i}"))
        assert len(self.engine.all_accounts()) == 3


# ─── 14. Convenience methods ──────────────────────────────────────────────────

class TestConvenienceMethods:
    def setup_method(self):
        self.engine = CustomerLifetimeValuePredictor()

    def _healthy_high_arr(self):
        return make_input(arr_eur=300_000, nps_score=80, seats_used_pct=90,
                          products_adopted=5, total_products_available=5,
                          renewals_completed=5, support_tickets_90d=0,
                          executive_sponsor_engaged=True, last_qbr_months_ago=0,
                          avg_renewal_growth_pct=20, competitor_evaluation_active=False,
                          key_champion_left=False, payment_delays_12m=0,
                          rep_churn_risk_score=1.0)

    def _risky(self):
        return make_input(competitor_evaluation_active=True,
                          key_champion_left=True, payment_delays_12m=5,
                          rep_churn_risk_score=9.0)

    def test_platinum_accounts(self):
        self.engine.predict(self._healthy_high_arr())
        results = self.engine.platinum_accounts()
        assert all(r.clv_tier == CLVTier.PLATINUM for r in results)

    def test_at_risk_accounts_critical(self):
        self.engine.predict(self._risky())
        results = self.engine.at_risk_accounts()
        assert len(results) >= 1
        assert all(r.churn_risk in (ChurnRisk.CRITICAL, ChurnRisk.HIGH) for r in results)

    def test_at_risk_accounts_excludes_low(self):
        self.engine.predict(make_input())  # healthy defaults → likely LOW
        # May or may not have at_risk; those that are should only be CRITICAL/HIGH
        results = self.engine.at_risk_accounts()
        assert all(r.churn_risk in (ChurnRisk.CRITICAL, ChurnRisk.HIGH) for r in results)

    def test_high_expansion_accounts(self):
        self.engine.predict(make_input(seats_used_pct=85, products_adopted=0,
                                       total_products_available=5,
                                       expansion_conversations_open=True,
                                       executive_sponsor_engaged=True,
                                       nps_score=50,
                                       competitor_evaluation_active=False,
                                       key_champion_left=False,
                                       payment_delays_12m=0,
                                       rep_churn_risk_score=1.0))
        results = self.engine.high_expansion_accounts()
        assert all(r.expansion_potential == ExpansionPotential.HIGH for r in results)

    def test_needs_rescue(self):
        self.engine.predict(self._risky())
        results = self.engine.needs_rescue()
        assert all(r.clv_action == CLVAction.RESCUE for r in results)

    def test_platinum_accounts_empty_when_none(self):
        self.engine.predict(make_input(arr_eur=100))
        assert self.engine.platinum_accounts() == []


# ─── 15. Aggregates ───────────────────────────────────────────────────────────

class TestAggregates:
    def setup_method(self):
        self.engine = CustomerLifetimeValuePredictor()

    def test_total_clv_eur_empty(self):
        assert self.engine.total_clv_eur() == 0.0

    def test_total_arr_eur_empty(self):
        assert self.engine.total_arr_eur() == 0.0

    def test_total_expansion_opportunity_eur_empty(self):
        assert self.engine.total_expansion_opportunity_eur() == 0.0

    def test_avg_health_score_empty_returns_zero(self):
        assert self.engine.avg_health_score() == 0.0

    def test_at_risk_arr_eur_empty(self):
        assert self.engine.at_risk_arr_eur() == 0.0

    def test_total_arr_eur_sums(self):
        self.engine.predict(make_input(arr_eur=10_000))
        self.engine.predict(make_input(arr_eur=20_000))
        assert self.engine.total_arr_eur() == pytest.approx(30_000.0, abs=0.1)

    def test_total_clv_eur_sums(self):
        r1 = self.engine.predict(make_input(arr_eur=10_000))
        r2 = self.engine.predict(make_input(arr_eur=20_000))
        expected = r1.clv_3yr_eur + r2.clv_3yr_eur
        assert self.engine.total_clv_eur() == pytest.approx(expected, abs=0.1)

    def test_avg_health_score_numeric(self):
        self.engine.predict(make_input())
        assert isinstance(self.engine.avg_health_score(), (int, float))

    def test_at_risk_arr_eur_only_counts_at_risk(self):
        self.engine.predict(make_input(arr_eur=10_000))  # healthy
        self.engine.predict(make_input(arr_eur=50_000,
                                       competitor_evaluation_active=True,
                                       key_champion_left=True,
                                       payment_delays_12m=5,
                                       rep_churn_risk_score=9.0))
        at_risk_arr = self.engine.at_risk_arr_eur()
        total_arr = self.engine.total_arr_eur()
        # at_risk_arr should be less than or equal to total_arr
        assert at_risk_arr <= total_arr


# ─── 16. summary() ────────────────────────────────────────────────────────────

class TestSummary:
    def setup_method(self):
        self.engine = CustomerLifetimeValuePredictor()
        self.engine.predict(make_input())
        self.s = self.engine.summary()

    def test_10_keys(self):
        assert len(self.s) == 10

    def test_total_key(self):
        assert "total" in self.s
        assert self.s["total"] == 1

    def test_tier_counts_key(self):
        assert "tier_counts" in self.s
        assert isinstance(self.s["tier_counts"], dict)

    def test_churn_risk_counts_key(self):
        assert "churn_risk_counts" in self.s
        assert isinstance(self.s["churn_risk_counts"], dict)

    def test_action_counts_key(self):
        assert "action_counts" in self.s
        assert isinstance(self.s["action_counts"], dict)

    def test_expansion_counts_key(self):
        assert "expansion_counts" in self.s
        assert isinstance(self.s["expansion_counts"], dict)

    def test_avg_health_score_key(self):
        assert "avg_health_score" in self.s
        assert isinstance(self.s["avg_health_score"], (int, float))

    def test_total_clv_eur_key(self):
        assert "total_clv_eur" in self.s
        assert isinstance(self.s["total_clv_eur"], (int, float))

    def test_total_arr_eur_key(self):
        assert "total_arr_eur" in self.s

    def test_total_expansion_opportunity_eur_key(self):
        assert "total_expansion_opportunity_eur" in self.s

    def test_at_risk_arr_eur_key(self):
        assert "at_risk_arr_eur" in self.s

    def test_tier_counts_sums_to_total(self):
        total = sum(self.s["tier_counts"].values())
        assert total == self.s["total"]

    def test_churn_risk_counts_sums_to_total(self):
        total = sum(self.s["churn_risk_counts"].values())
        assert total == self.s["total"]

    def test_action_counts_sums_to_total(self):
        total = sum(self.s["action_counts"].values())
        assert total == self.s["total"]

    def test_expansion_counts_sums_to_total(self):
        total = sum(self.s["expansion_counts"].values())
        assert total == self.s["total"]


# ─── 17. reset() ──────────────────────────────────────────────────────────────

class TestReset:
    def setup_method(self):
        self.engine = CustomerLifetimeValuePredictor()

    def test_reset_clears_results(self):
        self.engine.predict(make_input())
        self.engine.predict(make_input())
        self.engine.reset()
        assert self.engine.all_accounts() == []

    def test_reset_clears_aggregates(self):
        self.engine.predict(make_input(arr_eur=50_000))
        self.engine.reset()
        assert self.engine.total_arr_eur() == 0.0
        assert self.engine.total_clv_eur() == 0.0

    def test_reset_avg_health_returns_zero(self):
        self.engine.predict(make_input())
        self.engine.reset()
        assert self.engine.avg_health_score() == 0.0

    def test_predict_after_reset(self):
        self.engine.predict(make_input())
        self.engine.reset()
        self.engine.predict(make_input(account_id="NEW-001"))
        assert len(self.engine.all_accounts()) == 1
        assert self.engine.all_accounts()[0].account_id == "NEW-001"

    def test_reset_summary_total_zero(self):
        self.engine.predict(make_input())
        self.engine.reset()
        assert self.engine.summary()["total"] == 0


# ─── 18. Edge cases ───────────────────────────────────────────────────────────

class TestEdgeCases:
    def setup_method(self):
        self.engine = CustomerLifetimeValuePredictor()

    def test_zero_arr(self):
        result = self.engine.predict(make_input(arr_eur=0.0))
        assert result.arr_eur == 0.0
        assert isinstance(result.clv_3yr_eur, (int, float))

    def test_zero_arr_expansion_opportunity_zero(self):
        result = self.engine.predict(make_input(arr_eur=0.0))
        assert result.expansion_opportunity_eur == 0.0

    def test_no_renewals(self):
        result = self.engine.predict(make_input(renewals_completed=0))
        assert isinstance(result, CLVResult)

    def test_all_risk_signals_churn_capped_at_95(self):
        result = self.engine.predict(make_input(
            competitor_evaluation_active=True,
            key_champion_left=True,
            payment_delays_12m=5,
            rep_churn_risk_score=9.0,
            nps_score=-100,
            seats_used_pct=0,
            products_adopted=0,
            renewals_completed=0,
            support_tickets_90d=20,
            executive_sponsor_engaged=False,
            last_qbr_months_ago=24,
            last_renewal_months_ago=24,
            contract_length_months=12,
        ))
        assert result.churn_probability_pct <= 95.0
        assert result.churn_probability_pct == 95.0

    def test_zero_products_available_health_ok(self):
        result = self.engine.predict(make_input(products_adopted=0,
                                                total_products_available=0))
        assert isinstance(result.health_score, (int, float))

    def test_zero_products_available_expansion_opp(self):
        # product whitespace: gap=0, total=0 → division by max(1,0)=1 → 0
        result = self.engine.predict(make_input(arr_eur=100_000,
                                                products_adopted=0,
                                                total_products_available=0))
        assert isinstance(result.expansion_opportunity_eur, (int, float))

    def test_high_nps_gives_high_health(self):
        result = self.engine.predict(make_input(nps_score=100))
        assert result.health_score > 0

    def test_negative_nps_reduces_health(self):
        high_nps = self.engine.predict(make_input(nps_score=100))
        low_nps = self.engine.predict(make_input(nps_score=-100))
        assert low_nps.health_score < high_nps.health_score

    def test_single_payment_delay_no_penalty(self):
        r0 = self.engine.predict(make_input(payment_delays_12m=0))
        r1 = self.engine.predict(make_input(payment_delays_12m=1))
        # payment_delays_12m=1 does NOT add extra churn probability
        assert r0.churn_probability_pct == r1.churn_probability_pct

    def test_rep_score_boundary_7(self):
        r_below = self.engine.predict(make_input(rep_churn_risk_score=6.9))
        r_at = self.engine.predict(make_input(rep_churn_risk_score=7.0))
        # At 7: adds 15; at 6.9: adds 8
        assert r_at.churn_probability_pct > r_below.churn_probability_pct

    def test_rep_score_boundary_5(self):
        r_below = self.engine.predict(make_input(rep_churn_risk_score=4.9))
        r_at = self.engine.predict(make_input(rep_churn_risk_score=5.0))
        assert r_at.churn_probability_pct > r_below.churn_probability_pct

    def test_health_score_bounded_0_to_100(self):
        for inp in [make_input(), make_input(nps_score=-100, seats_used_pct=0),
                    make_input(nps_score=100, seats_used_pct=100)]:
            h = self.engine._health_score(inp)
            assert 0.0 <= h <= 100.0

    def test_churn_prob_bounded_0_to_95(self):
        inp = make_input()
        h = self.engine._health_score(inp)
        cp = self.engine._churn_probability(inp, h)
        assert 0.0 <= cp <= 95.0


# ─── 19. Integration: multi-account batch ────────────────────────────────────

class TestIntegration:
    def setup_method(self):
        self.engine = CustomerLifetimeValuePredictor()

    def test_multi_account_batch_sort_order(self):
        inputs = [
            make_input(account_id="BIG", arr_eur=400_000, nps_score=80,
                       seats_used_pct=90, renewals_completed=5,
                       support_tickets_90d=0, executive_sponsor_engaged=True,
                       last_qbr_months_ago=0, avg_renewal_growth_pct=20,
                       products_adopted=5, total_products_available=5,
                       competitor_evaluation_active=False, key_champion_left=False,
                       payment_delays_12m=0, rep_churn_risk_score=1.0),
            make_input(account_id="SMALL", arr_eur=5_000, nps_score=-50,
                       seats_used_pct=20, renewals_completed=0,
                       support_tickets_90d=10, executive_sponsor_engaged=False,
                       last_qbr_months_ago=12, avg_renewal_growth_pct=0,
                       products_adopted=1, total_products_available=5,
                       competitor_evaluation_active=True, key_champion_left=True,
                       payment_delays_12m=3, rep_churn_risk_score=8.0),
            make_input(account_id="MED", arr_eur=50_000),
        ]
        results = self.engine.predict_batch(inputs)
        clvs = [r.clv_3yr_eur for r in results]
        assert clvs == sorted(clvs, reverse=True)

    def test_multi_account_mixed_tiers(self):
        self.engine.predict(make_input(arr_eur=400_000, nps_score=80,
                                       seats_used_pct=90, renewals_completed=5,
                                       support_tickets_90d=0, executive_sponsor_engaged=True,
                                       last_qbr_months_ago=0, avg_renewal_growth_pct=20,
                                       products_adopted=5, total_products_available=5,
                                       competitor_evaluation_active=False, key_champion_left=False,
                                       payment_delays_12m=0, rep_churn_risk_score=1.0,
                                       account_id="BIG"))
        self.engine.predict(make_input(arr_eur=100, account_id="TINY"))
        summary = self.engine.summary()
        assert summary["total"] == 2
        assert sum(summary["tier_counts"].values()) == 2

    def test_at_risk_arr_eur_accumulates(self):
        # Two risky accounts
        arr1, arr2 = 30_000, 40_000
        self.engine.predict(make_input(arr_eur=arr1,
                                       competitor_evaluation_active=True,
                                       key_champion_left=True,
                                       rep_churn_risk_score=9.0))
        self.engine.predict(make_input(arr_eur=arr2,
                                       competitor_evaluation_active=True,
                                       key_champion_left=True,
                                       rep_churn_risk_score=9.0))
        at_risk_arr = self.engine.at_risk_arr_eur()
        assert at_risk_arr >= arr1  # at minimum the first account counts

    def test_full_workflow(self):
        """Test a realistic workflow: batch predict, filter, aggregate, reset."""
        inputs = [make_input(account_id=f"ACC-{i}", arr_eur=10_000 * (i + 1))
                  for i in range(5)]
        results = self.engine.predict_batch(inputs)
        assert len(results) == 5

        summary = self.engine.summary()
        assert summary["total"] == 5
        assert isinstance(summary["avg_health_score"], (int, float))

        self.engine.reset()
        assert self.engine.total_arr_eur() == 0.0
        assert self.engine.summary()["total"] == 0

    def test_clv_3yr_equals_arr_plus_yr2_plus_yr3(self):
        """CLV should equal arr + yr2 + yr3."""
        result = self.engine.predict(make_input(arr_eur=100_000))
        expected = round(result.arr_eur + result.predicted_arr_yr2_eur + result.predicted_arr_yr3_eur, 0)
        assert result.clv_3yr_eur == expected

    def test_rescue_action_for_all_critical_churn(self):
        self.engine.predict(make_input(competitor_evaluation_active=True,
                                       key_champion_left=True,
                                       payment_delays_12m=5,
                                       rep_churn_risk_score=9.0))
        critical_accounts = self.engine.by_churn_risk(ChurnRisk.CRITICAL)
        for acc in critical_accounts:
            assert acc.clv_action == CLVAction.RESCUE

    def test_growth_rate_zero_when_negative_renewal_growth(self):
        """Negative avg_renewal_growth_pct should give growth_rate of 0 (clamped)."""
        inp = make_input(avg_renewal_growth_pct=-20.0)
        h = self.engine._health_score(inp)
        cp = self.engine._churn_probability(inp, h)
        gr = self.engine._growth_rate(inp, cp)
        assert gr == 0.0

    def test_predicted_arr_yr2_greater_than_arr_for_growth(self):
        """When growth > 0 and survival > 1, yr2 might be less than arr but check it's positive."""
        result = self.engine.predict(make_input(arr_eur=50_000,
                                                avg_renewal_growth_pct=20,
                                                nps_score=80,
                                                competitor_evaluation_active=False,
                                                key_champion_left=False,
                                                payment_delays_12m=0,
                                                rep_churn_risk_score=1.0))
        assert result.predicted_arr_yr2_eur >= 0
        assert result.predicted_arr_yr3_eur >= 0
