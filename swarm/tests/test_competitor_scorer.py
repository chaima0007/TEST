import pytest
from intelligence.competitor_scorer import (
    CompetitorProfile,
    CompetitorScorer,
    ScoredCompetitor,
    ThreatLevel,
)


def make_profile(
    competitor_id="c1",
    name="TestCo",
    sector="tech",
    website="https://testco.com",
    price_index=50.0,
    seo_strength=50.0,
    tech_quality=50.0,
    review_score=3.0,
    market_share_pct=50.0,
) -> CompetitorProfile:
    return CompetitorProfile(
        competitor_id=competitor_id,
        name=name,
        sector=sector,
        website=website,
        price_index=price_index,
        seo_strength=seo_strength,
        tech_quality=tech_quality,
        review_score=review_score,
        market_share_pct=market_share_pct,
    )


@pytest.fixture
def scorer():
    return CompetitorScorer()


@pytest.fixture
def base_profile():
    return make_profile()


@pytest.fixture
def critical_profile():
    return make_profile(
        competitor_id="crit",
        name="CriticalCo",
        price_index=0.0,
        seo_strength=100.0,
        tech_quality=100.0,
        review_score=5.0,
        market_share_pct=100.0,
    )


@pytest.fixture
def low_profile():
    return make_profile(
        competitor_id="low",
        name="LowCo",
        price_index=100.0,
        seo_strength=0.0,
        tech_quality=0.0,
        review_score=0.0,
        market_share_pct=0.0,
    )


class TestCompetitorProfile:
    def test_competitor_id_stored(self, base_profile):
        assert base_profile.competitor_id == "c1"

    def test_name_stored(self, base_profile):
        assert base_profile.name == "TestCo"

    def test_sector_stored(self, base_profile):
        assert base_profile.sector == "tech"

    def test_website_stored(self, base_profile):
        assert base_profile.website == "https://testco.com"

    def test_price_index_stored(self, base_profile):
        assert base_profile.price_index == 50.0

    def test_seo_strength_stored(self, base_profile):
        assert base_profile.seo_strength == 50.0

    def test_tech_quality_stored(self, base_profile):
        assert base_profile.tech_quality == 50.0

    def test_review_score_stored(self, base_profile):
        assert base_profile.review_score == 3.0

    def test_market_share_pct_stored(self, base_profile):
        assert base_profile.market_share_pct == 50.0

    def test_to_dict_returns_dict(self, base_profile):
        d = base_profile.to_dict()
        assert isinstance(d, dict)

    def test_to_dict_has_all_keys(self, base_profile):
        d = base_profile.to_dict()
        expected_keys = {
            "competitor_id", "name", "sector", "website", "price_index",
            "seo_strength", "tech_quality", "review_score", "market_share_pct",
        }
        assert expected_keys == set(d.keys())

    def test_to_dict_values_correct(self, base_profile):
        d = base_profile.to_dict()
        assert d["competitor_id"] == "c1"
        assert d["price_index"] == 50.0


class TestScoring:
    def test_score_returns_scored_competitor(self, scorer, base_profile):
        result = scorer.score(base_profile)
        assert isinstance(result, ScoredCompetitor)

    def test_threat_score_is_float(self, scorer, base_profile):
        result = scorer.score(base_profile)
        assert isinstance(result.threat_score, float)

    def test_threat_score_between_0_and_100(self, scorer, base_profile):
        result = scorer.score(base_profile)
        assert 0.0 <= result.threat_score <= 100.0

    def test_threat_level_critical(self, scorer, critical_profile):
        result = scorer.score(critical_profile)
        assert result.threat_level == ThreatLevel.CRITICAL

    def test_threat_level_low(self, scorer, low_profile):
        result = scorer.score(low_profile)
        assert result.threat_level == ThreatLevel.LOW

    def test_threat_level_high(self, scorer):
        profile = make_profile(
            competitor_id="high",
            price_index=20.0,
            seo_strength=75.0,
            tech_quality=70.0,
            review_score=4.0,
            market_share_pct=60.0,
        )
        result = scorer.score(profile)
        assert result.threat_level == ThreatLevel.HIGH

    def test_threat_level_medium(self, scorer):
        profile = make_profile(
            competitor_id="med",
            price_index=60.0,
            seo_strength=40.0,
            tech_quality=40.0,
            review_score=2.5,
            market_share_pct=30.0,
        )
        result = scorer.score(profile)
        assert result.threat_level == ThreatLevel.MEDIUM

    def test_dimension_scores_populated(self, scorer, base_profile):
        result = scorer.score(base_profile)
        assert isinstance(result.dimension_scores, dict)
        assert len(result.dimension_scores) == 5

    def test_dimension_scores_has_price_threat(self, scorer, base_profile):
        result = scorer.score(base_profile)
        assert "price_threat" in result.dimension_scores

    def test_dimension_scores_has_seo(self, scorer, base_profile):
        result = scorer.score(base_profile)
        assert "seo" in result.dimension_scores

    def test_dimension_scores_has_tech(self, scorer, base_profile):
        result = scorer.score(base_profile)
        assert "tech" in result.dimension_scores

    def test_dimension_scores_has_review_normalized(self, scorer, base_profile):
        result = scorer.score(base_profile)
        assert "review_normalized" in result.dimension_scores

    def test_dimension_scores_has_market(self, scorer, base_profile):
        result = scorer.score(base_profile)
        assert "market" in result.dimension_scores

    def test_price_threat_inverse_of_price_index(self, scorer):
        profile = make_profile(price_index=30.0)
        result = scorer.score(profile)
        assert result.dimension_scores["price_threat"] == pytest.approx(70.0)

    def test_review_normalized_scale(self, scorer):
        profile = make_profile(review_score=4.0)
        result = scorer.score(profile)
        assert result.dimension_scores["review_normalized"] == pytest.approx(80.0)

    def test_strengths_is_list(self, scorer, base_profile):
        result = scorer.score(base_profile)
        assert isinstance(result.strengths, list)

    def test_vulnerabilities_is_list(self, scorer, base_profile):
        result = scorer.score(base_profile)
        assert isinstance(result.vulnerabilities, list)

    def test_recommendations_non_empty(self, scorer, base_profile):
        result = scorer.score(base_profile)
        assert len(result.recommendations) > 0

    def test_strength_price_generated(self, scorer):
        profile = make_profile(price_index=5.0)
        result = scorer.score(profile)
        assert any("Prix agressif" in s for s in result.strengths)

    def test_strength_seo_generated(self, scorer):
        profile = make_profile(seo_strength=90.0)
        result = scorer.score(profile)
        assert any("SEO fort" in s for s in result.strengths)

    def test_strength_tech_generated(self, scorer):
        profile = make_profile(tech_quality=85.0)
        result = scorer.score(profile)
        assert any("Stack technique" in s for s in result.strengths)

    def test_strength_review_generated(self, scorer):
        profile = make_profile(review_score=4.5)
        result = scorer.score(profile)
        assert any("Excellents avis" in s for s in result.strengths)

    def test_strength_market_generated(self, scorer):
        profile = make_profile(market_share_pct=85.0)
        result = scorer.score(profile)
        assert any("Part de marché élevée" in s for s in result.strengths)

    def test_vulnerability_high_price_generated(self, scorer):
        profile = make_profile(price_index=95.0)
        result = scorer.score(profile)
        assert any("Prix élevés" in v for v in result.vulnerabilities)

    def test_vulnerability_low_seo_generated(self, scorer):
        profile = make_profile(seo_strength=10.0)
        result = scorer.score(profile)
        assert any("Faible SEO" in v for v in result.vulnerabilities)

    def test_vulnerability_low_tech_generated(self, scorer):
        profile = make_profile(tech_quality=15.0)
        result = scorer.score(profile)
        assert any("médiocre" in v for v in result.vulnerabilities)

    def test_vulnerability_low_review_generated(self, scorer):
        profile = make_profile(review_score=1.0)
        result = scorer.score(profile)
        assert any("Avis clients faibles" in v for v in result.vulnerabilities)

    def test_vulnerability_low_market_generated(self, scorer):
        profile = make_profile(market_share_pct=5.0)
        result = scorer.score(profile)
        assert any("Part de marché faible" in v for v in result.vulnerabilities)

    def test_critical_recommendations(self, scorer, critical_profile):
        result = scorer.score(critical_profile)
        assert any("différenciation" in r for r in result.recommendations)

    def test_low_recommendations(self, scorer, low_profile):
        result = scorer.score(low_profile)
        assert any("trimestrielle" in r for r in result.recommendations)

    def test_to_dict_on_scored(self, scorer, base_profile):
        result = scorer.score(base_profile)
        d = result.to_dict()
        assert isinstance(d, dict)
        assert "threat_score" in d
        assert "threat_level" in d
        assert "dimension_scores" in d
        assert "strengths" in d
        assert "vulnerabilities" in d
        assert "recommendations" in d
        assert "profile" in d


class TestCompetitorScorer:
    def test_score_and_retrieve(self, scorer, base_profile):
        scorer.score(base_profile)
        retrieved = scorer.get("c1")
        assert retrieved is not None
        assert retrieved.profile.competitor_id == "c1"

    def test_get_missing_returns_none(self, scorer):
        assert scorer.get("nonexistent") is None

    def test_all_scored_empty_initially(self, scorer):
        assert scorer.all_scored() == []

    def test_all_scored_returns_all(self, scorer):
        scorer.score(make_profile(competitor_id="a"))
        scorer.score(make_profile(competitor_id="b"))
        assert len(scorer.all_scored()) == 2

    def test_batch_scoring(self, scorer):
        profiles = [
            make_profile(competitor_id="x1"),
            make_profile(competitor_id="x2"),
            make_profile(competitor_id="x3"),
        ]
        results = scorer.score_batch(profiles)
        assert len(results) == 3
        assert all(isinstance(r, ScoredCompetitor) for r in results)

    def test_batch_scoring_stores_all(self, scorer):
        profiles = [make_profile(competitor_id=f"b{i}") for i in range(4)]
        scorer.score_batch(profiles)
        assert len(scorer.all_scored()) == 4

    def test_top_threats_sorted_desc(self, scorer, critical_profile, low_profile):
        scorer.score(critical_profile)
        scorer.score(low_profile)
        top = scorer.top_threats(n=2)
        assert top[0].threat_score >= top[1].threat_score

    def test_top_threats_respects_n(self, scorer):
        profiles = [make_profile(competitor_id=f"t{i}") for i in range(10)]
        scorer.score_batch(profiles)
        assert len(scorer.top_threats(n=3)) == 3

    def test_top_threats_default_n_5(self, scorer):
        profiles = [make_profile(competitor_id=f"d{i}") for i in range(8)]
        scorer.score_batch(profiles)
        assert len(scorer.top_threats()) == 5

    def test_by_threat_level_filter(self, scorer, critical_profile, low_profile):
        scorer.score(critical_profile)
        scorer.score(low_profile)
        criticals = scorer.by_threat_level(ThreatLevel.CRITICAL)
        assert all(s.threat_level == ThreatLevel.CRITICAL for s in criticals)

    def test_by_threat_level_empty_when_none(self, scorer, low_profile):
        scorer.score(low_profile)
        assert scorer.by_threat_level(ThreatLevel.CRITICAL) == []

    def test_sector_summary_keys(self, scorer):
        scorer.score(make_profile(sector="fintech"))
        summary = scorer.sector_summary("fintech")
        assert "sector" in summary
        assert "count" in summary
        assert "avg_threat" in summary
        assert "critical_count" in summary
        assert "high_count" in summary
        assert "top_threat_name" in summary

    def test_sector_summary_count(self, scorer):
        scorer.score(make_profile(competitor_id="s1", sector="fintech"))
        scorer.score(make_profile(competitor_id="s2", sector="fintech"))
        summary = scorer.sector_summary("fintech")
        assert summary["count"] == 2

    def test_sector_summary_empty_sector(self, scorer):
        summary = scorer.sector_summary("nonexistent")
        assert summary["count"] == 0
        assert summary["avg_threat"] == 0.0

    def test_market_snapshot_has_required_keys(self, scorer, base_profile):
        scorer.score(base_profile)
        snap = scorer.market_snapshot()
        assert "total_competitors" in snap
        assert "avg_threat_score" in snap
        assert "threat_level_distribution" in snap
        assert "top_threat" in snap

    def test_market_snapshot_total_competitors(self, scorer):
        scorer.score(make_profile(competitor_id="m1"))
        scorer.score(make_profile(competitor_id="m2"))
        snap = scorer.market_snapshot()
        assert snap["total_competitors"] == 2

    def test_market_snapshot_distribution_has_all_levels(self, scorer, base_profile):
        scorer.score(base_profile)
        snap = scorer.market_snapshot()
        dist = snap["threat_level_distribution"]
        assert "low" in dist
        assert "medium" in dist
        assert "high" in dist
        assert "critical" in dist

    def test_reset_clears_state(self, scorer, base_profile):
        scorer.score(base_profile)
        scorer.reset()
        assert scorer.all_scored() == []

    def test_reset_get_returns_none_after(self, scorer, base_profile):
        scorer.score(base_profile)
        scorer.reset()
        assert scorer.get("c1") is None


class TestEdgeCases:
    def test_all_zero_dimensions_low_threat(self, scorer):
        profile = make_profile(
            competitor_id="zero",
            price_index=100.0,
            seo_strength=0.0,
            tech_quality=0.0,
            review_score=0.0,
            market_share_pct=0.0,
        )
        result = scorer.score(profile)
        assert result.threat_level == ThreatLevel.LOW

    def test_all_max_dimensions_critical_threat(self, scorer, critical_profile):
        result = scorer.score(critical_profile)
        assert result.threat_level == ThreatLevel.CRITICAL
        assert result.threat_score == pytest.approx(100.0)

    def test_all_max_threat_score_100(self, scorer, critical_profile):
        result = scorer.score(critical_profile)
        assert result.threat_score <= 100.0

    def test_single_competitor_top_threats(self, scorer, base_profile):
        scorer.score(base_profile)
        top = scorer.top_threats(n=5)
        assert len(top) == 1

    def test_single_competitor_sector_summary(self, scorer):
        scorer.score(make_profile(competitor_id="solo", sector="retail"))
        summary = scorer.sector_summary("retail")
        assert summary["count"] == 1
        assert summary["top_threat_name"] == "TestCo"

    def test_threat_score_exact_boundary_75_is_critical(self, scorer):
        profile = make_profile(
            competitor_id="boundary75",
            price_index=0.0,
            seo_strength=100.0,
            tech_quality=100.0,
            review_score=5.0,
            market_share_pct=100.0,
        )
        result = scorer.score(profile)
        assert result.threat_score >= 75.0
        assert result.threat_level == ThreatLevel.CRITICAL

    def test_no_strengths_for_mediocre_competitor(self, scorer):
        profile = make_profile(
            competitor_id="med2",
            price_index=50.0,
            seo_strength=50.0,
            tech_quality=50.0,
            review_score=2.5,
            market_share_pct=50.0,
        )
        result = scorer.score(profile)
        assert result.strengths == []

    def test_no_vulnerabilities_for_strong_competitor(self, scorer, critical_profile):
        result = scorer.score(critical_profile)
        assert result.vulnerabilities == []

    def test_rescoring_same_id_updates_store(self, scorer):
        profile1 = make_profile(competitor_id="dup", seo_strength=10.0)
        profile2 = make_profile(competitor_id="dup", seo_strength=90.0)
        scorer.score(profile1)
        scorer.score(profile2)
        retrieved = scorer.get("dup")
        assert retrieved.profile.seo_strength == 90.0

    def test_market_snapshot_empty_store(self, scorer):
        snap = scorer.market_snapshot()
        assert snap["total_competitors"] == 0
        assert snap["top_threat"] is None
