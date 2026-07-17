"""
Comprehensive tests for swarm/intelligence/email_subject_optimizer.py
"""

import pytest

from swarm.intelligence.email_subject_optimizer import (
    EmailSubjectOptimizer,
    SubjectLine,
    OptimizationTier,
    _length_score,
    _personalization_score,
    _urgency_score,
    _clarity_score,
    _question_score,
    _emoji_balance_score,
    _send_hour_multiplier,
    _count_emojis,
    _compute_predicted_open_rate,
    _classify_tier,
    OptimizedSubject,
)


# ---------------------------------------------------------------------------
# TestSubjectLine
# ---------------------------------------------------------------------------

class TestSubjectLine:
    def test_to_dict_keys(self):
        sl = SubjectLine(subject_id="s1", text="Hello world this is a test")
        d = sl.to_dict()
        assert set(d.keys()) == {"subject_id", "text", "template_id", "variant_key", "send_hour"}

    def test_to_dict_values(self):
        sl = SubjectLine(
            subject_id="s42",
            text="Bonjour {name}!",
            template_id="tmpl-01",
            variant_key="B",
            send_hour=11,
        )
        d = sl.to_dict()
        assert d["subject_id"] == "s42"
        assert d["text"] == "Bonjour {name}!"
        assert d["template_id"] == "tmpl-01"
        assert d["variant_key"] == "B"
        assert d["send_hour"] == 11

    def test_default_template_id_is_none(self):
        sl = SubjectLine(subject_id="s1", text="Some text for testing purposes")
        assert sl.template_id is None
        assert sl.to_dict()["template_id"] is None

    def test_default_variant_key(self):
        sl = SubjectLine(subject_id="s1", text="Some text for testing purposes")
        assert sl.variant_key == "A"

    def test_default_send_hour(self):
        sl = SubjectLine(subject_id="s1", text="Some text for testing purposes")
        assert sl.send_hour == 9

    def test_to_dict_returns_new_dict(self):
        sl = SubjectLine(subject_id="s1", text="Test text for checking dict")
        d1 = sl.to_dict()
        d2 = sl.to_dict()
        assert d1 == d2
        # mutating one should not affect the other (asdict returns new dict)
        d1["subject_id"] = "modified"
        assert d2["subject_id"] == "s1"


# ---------------------------------------------------------------------------
# TestLengthScore
# ---------------------------------------------------------------------------

class TestLengthScore:
    def test_too_short_returns_30_and_tip(self):
        # < 20 chars
        score, tips = _length_score("Hi there")  # 8 chars
        assert score == 30.0
        assert "too_short" in tips

    def test_exact_boundary_19_is_too_short(self):
        text = "a" * 19
        score, tips = _length_score(text)
        assert score == 30.0
        assert "too_short" in tips

    def test_perfect_range_20_chars(self):
        text = "a" * 20
        score, tips = _length_score(text)
        assert score == 100.0
        assert tips == []

    def test_perfect_range_40_chars(self):
        text = "a" * 40
        score, tips = _length_score(text)
        assert score == 100.0
        assert tips == []

    def test_good_range_41_to_60(self):
        text = "a" * 50
        score, tips = _length_score(text)
        assert score == 80.0
        assert tips == []

    def test_too_long_above_60(self):
        # 70 chars → 80 - (70-60)*2 = 80 - 20 = 60
        text = "a" * 70
        score, tips = _length_score(text)
        assert score == 60.0
        assert "too_long" in tips

    def test_too_long_scores_floor_at_zero(self):
        # 100 chars → 80 - (100-60)*2 = 80 - 80 = 0
        text = "a" * 100
        score, tips = _length_score(text)
        assert score == 0.0
        assert "too_long" in tips

    def test_too_long_does_not_go_below_zero(self):
        text = "a" * 200
        score, tips = _length_score(text)
        assert score == 0.0
        assert "too_long" in tips


# ---------------------------------------------------------------------------
# TestPersonalizationScore
# ---------------------------------------------------------------------------

class TestPersonalizationScore:
    def test_no_token_returns_zero_and_tip(self):
        score, tips = _personalization_score("No personalization here at all")
        assert score == 0.0
        assert "no_personalization" in tips

    def test_one_token_returns_50(self):
        score, tips = _personalization_score("Hello {name}, check this out now")
        assert score == 50.0
        assert tips == []

    def test_two_tokens_returns_100(self):
        score, tips = _personalization_score("Hi {name} from {company}, see this")
        assert score == 100.0
        assert tips == []

    def test_three_tokens_capped_at_100(self):
        score, tips = _personalization_score("{a} {b} {c} many tokens here added")
        assert score == 100.0
        assert tips == []

    def test_empty_string_returns_zero(self):
        score, tips = _personalization_score("")
        assert score == 0.0
        assert "no_personalization" in tips


# ---------------------------------------------------------------------------
# TestUrgencyScore
# ---------------------------------------------------------------------------

class TestUrgencyScore:
    def test_no_urgency_returns_20_and_tip(self):
        score, tips = _urgency_score("Completely neutral subject line here")
        assert score == 20.0
        assert "no_urgency" in tips

    def test_one_urgency_word(self):
        # hits=1 → 40 + 1*30 = 70
        score, tips = _urgency_score("Ne ratez pas cette offre spéciale")
        assert score == 70.0
        assert tips == []

    def test_multiple_urgency_words(self):
        # "urgent" + "limite" + "maintenant" → hits=3 → 40 + 3*30 = 130 → capped at 100
        score, tips = _urgency_score("Urgent: limite maintenant")
        assert score == 100.0
        assert tips == []

    def test_urgency_is_case_insensitive(self):
        score, tips = _urgency_score("URGENT action required immediately")
        assert score > 20.0
        assert "no_urgency" not in tips


# ---------------------------------------------------------------------------
# TestClarityScore
# ---------------------------------------------------------------------------

class TestClarityScore:
    def test_clean_text_returns_100(self):
        score, tips = _clarity_score("Great subject with no spam words")
        assert score == 100.0
        assert tips == []

    def test_one_spam_word_penalty(self):
        # "fwd:" present → 100 - 40 = 60
        score, tips = _clarity_score("Fwd: check this message out now")
        assert score == 60.0
        assert "spam_risk" in tips

    def test_two_spam_words_penalty(self):
        # "fwd:" + "re:" → 100 - 80 = 20
        score, tips = _clarity_score("Fwd: Re: check this message out now")
        assert score == 20.0
        assert "spam_risk" in tips

    def test_three_spam_words_floors_at_zero(self):
        # "fwd:" + "re:" + "cliquez" → 100 - 120 = -20 → floored to 0
        score, tips = _clarity_score("Fwd: Re: cliquez ici maintenant pour voir")
        assert score == 0.0
        assert "spam_risk" in tips


# ---------------------------------------------------------------------------
# TestQuestionScore
# ---------------------------------------------------------------------------

class TestQuestionScore:
    def test_no_question_mark_returns_30(self):
        score, tips = _question_score("This is a statement subject line")
        assert score == 30.0
        assert "no_question" in tips

    def test_with_question_mark_returns_100(self):
        score, tips = _question_score("Are you ready to open this email?")
        assert score == 100.0
        assert tips == []


# ---------------------------------------------------------------------------
# TestEmojiScore
# ---------------------------------------------------------------------------

class TestEmojiScore:
    def test_no_emoji_returns_50_and_tip(self):
        score, tips = _emoji_balance_score("No emoji in this subject line here")
        assert score == 50.0
        assert "no_emoji" in tips

    def test_one_emoji_returns_100(self):
        score, tips = _emoji_balance_score("Great offer today 🎉")
        assert score == 100.0
        assert tips == []

    def test_two_emojis_returns_100(self):
        score, tips = _emoji_balance_score("Great offer today 🎉🚀")
        assert score == 100.0
        assert tips == []

    def test_three_emojis_has_penalty(self):
        # count=3 → 100 - (3-2)*20 = 80
        # Emojis must be separated by non-emoji chars so the regex counts each individually
        score, tips = _emoji_balance_score("Great offer 🎉 🚀 🔥")
        assert score == 80.0
        assert "too_many_emojis" in tips

    def test_four_emojis_returns_60(self):
        # count=4 → 100 - (4-2)*20 = 60
        # Emojis separated by letters so each is a distinct regex match
        score, tips = _emoji_balance_score("a 🎉 b 🚀 c 🔥 d 😀 e")
        assert score == 60.0
        assert "too_many_emojis" in tips


# ---------------------------------------------------------------------------
# TestSendHourMultiplier
# ---------------------------------------------------------------------------

class TestSendHourMultiplier:
    def test_peak_morning_8_to_10(self):
        assert _send_hour_multiplier(8) == 1.15
        assert _send_hour_multiplier(9) == 1.15
        assert _send_hour_multiplier(10) == 1.15

    def test_good_midday_11_to_13(self):
        assert _send_hour_multiplier(11) == 1.05
        assert _send_hour_multiplier(12) == 1.05
        assert _send_hour_multiplier(13) == 1.05

    def test_neutral_afternoon_14_to_16(self):
        assert _send_hour_multiplier(14) == 1.0
        assert _send_hour_multiplier(15) == 1.0
        assert _send_hour_multiplier(16) == 1.0

    def test_reduced_early_and_evening(self):
        # 6-7 and 17-19
        assert _send_hour_multiplier(6) == 0.90
        assert _send_hour_multiplier(7) == 0.90
        assert _send_hour_multiplier(17) == 0.90
        assert _send_hour_multiplier(18) == 0.90
        assert _send_hour_multiplier(19) == 0.90

    def test_off_hours_returns_0_75(self):
        # 0-5 and 20-23
        assert _send_hour_multiplier(0) == 0.75
        assert _send_hour_multiplier(3) == 0.75
        assert _send_hour_multiplier(5) == 0.75
        assert _send_hour_multiplier(20) == 0.75
        assert _send_hour_multiplier(23) == 0.75


# ---------------------------------------------------------------------------
# TestOptimizedSubject
# ---------------------------------------------------------------------------

class TestOptimizedSubject:
    def _make_optimized(self, text="A decent subject line here", send_hour=9,
                        template_id=None):
        sl = SubjectLine(subject_id="os1", text=text, template_id=template_id,
                         send_hour=send_hour)
        opt = EmailSubjectOptimizer()
        return opt.optimize(sl)

    def test_to_dict_shape(self):
        result = self._make_optimized()
        d = result.to_dict()
        expected_keys = {
            "subject", "predicted_open_rate", "optimization_tier",
            "dimension_scores", "suggestions", "emoji_count",
            "word_count", "char_count", "has_personalization",
            "has_urgency", "has_question",
        }
        assert set(d.keys()) == expected_keys
        assert isinstance(d["subject"], dict)
        assert isinstance(d["dimension_scores"], dict)
        assert isinstance(d["suggestions"], list)
        assert isinstance(d["optimization_tier"], str)

    def test_open_rate_clamped_between_0_and_1(self):
        # Even with extreme inputs, rate should be in [0, 1]
        result = self._make_optimized(text="a" * 200)
        assert 0.0 <= result.predicted_open_rate <= 1.0

    def test_tier_classification_excellent(self):
        assert _classify_tier(0.40) == OptimizationTier.EXCELLENT
        assert _classify_tier(0.38) == OptimizationTier.EXCELLENT

    def test_tier_classification_good(self):
        assert _classify_tier(0.28) == OptimizationTier.GOOD
        assert _classify_tier(0.30) == OptimizationTier.GOOD
        assert _classify_tier(0.379) == OptimizationTier.GOOD

    def test_tier_classification_fair(self):
        assert _classify_tier(0.18) == OptimizationTier.FAIR
        assert _classify_tier(0.25) == OptimizationTier.FAIR
        assert _classify_tier(0.279) == OptimizationTier.FAIR

    def test_tier_classification_weak(self):
        assert _classify_tier(0.05) == OptimizationTier.WEAK
        assert _classify_tier(0.17) == OptimizationTier.WEAK
        assert _classify_tier(0.0) == OptimizationTier.WEAK

    def test_has_personalization_true(self):
        result = self._make_optimized(text="Bonjour {name}, découvrez notre offre!")
        assert result.has_personalization is True

    def test_has_personalization_false(self):
        result = self._make_optimized(text="Bonjour, découvrez notre offre du jour!")
        assert result.has_personalization is False

    def test_has_urgency_true(self):
        result = self._make_optimized(text="Offre exclusive limitée, agissez maintenant!")
        assert result.has_urgency is True

    def test_has_urgency_false(self):
        result = self._make_optimized(text="Notre newsletter mensuelle est disponible")
        assert result.has_urgency is False

    def test_has_question_true(self):
        result = self._make_optimized(text="Avez-vous vu notre dernière nouveauté?")
        assert result.has_question is True

    def test_has_question_false(self):
        result = self._make_optimized(text="Notre dernière nouveauté est disponible")
        assert result.has_question is False


# ---------------------------------------------------------------------------
# TestEmailSubjectOptimizer
# ---------------------------------------------------------------------------

class TestEmailSubjectOptimizer:
    def setup_method(self):
        self.optimizer = EmailSubjectOptimizer()

    # --- optimize / get (CRUD) ---

    def test_optimize_returns_optimized_subject(self):
        sl = SubjectLine(subject_id="t1", text="Découvrez notre offre exclusive!")
        result = self.optimizer.optimize(sl)
        assert isinstance(result, OptimizedSubject)
        assert result.subject.subject_id == "t1"

    def test_get_returns_stored_result(self):
        sl = SubjectLine(subject_id="t2", text="Ne manquez pas cette occasion unique!")
        self.optimizer.optimize(sl)
        stored = self.optimizer.get("t2")
        assert stored is not None
        assert stored.subject.subject_id == "t2"

    def test_get_returns_none_for_unknown_id(self):
        result = self.optimizer.get("nonexistent")
        assert result is None

    def test_optimize_overwrites_existing_entry(self):
        sl1 = SubjectLine(subject_id="dup", text="First version of this subject line")
        sl2 = SubjectLine(subject_id="dup", text="Deuxième version avec urgence maintenant!")
        self.optimizer.optimize(sl1)
        self.optimizer.optimize(sl2)
        stored = self.optimizer.get("dup")
        assert stored.subject.text == "Deuxième version avec urgence maintenant!"

    # --- optimize_batch ---

    def test_optimize_batch_returns_all(self):
        subjects = [
            SubjectLine(subject_id=f"b{i}", text=f"Subject number {i} test here!")
            for i in range(5)
        ]
        results = self.optimizer.optimize_batch(subjects)
        assert len(results) == 5

    def test_optimize_batch_stores_all(self):
        subjects = [
            SubjectLine(subject_id=f"c{i}", text=f"Subject number {i} test here!")
            for i in range(3)
        ]
        self.optimizer.optimize_batch(subjects)
        for i in range(3):
            assert self.optimizer.get(f"c{i}") is not None

    # --- all_subjects sorted by rate desc ---

    def test_all_subjects_sorted_descending(self):
        # Create subjects with varying quality
        subjects = [
            SubjectLine(subject_id="low", text="Hi"),  # very short, low score
            SubjectLine(
                subject_id="high",
                text="{name}, offre exclusive aujourd'hui? 🎉",
                send_hour=9,
            ),
            SubjectLine(subject_id="mid", text="Voici notre newsletter du mois"),
        ]
        self.optimizer.optimize_batch(subjects)
        all_s = self.optimizer.all_subjects()
        rates = [o.predicted_open_rate for o in all_s]
        assert rates == sorted(rates, reverse=True)

    def test_all_subjects_empty_when_no_optimizations(self):
        assert self.optimizer.all_subjects() == []

    # --- best_for_template ---

    def test_best_for_template_returns_highest_rate(self):
        self.optimizer.optimize(SubjectLine(
            subject_id="tmA1", text="Hi", template_id="tmpl-A"
        ))
        self.optimizer.optimize(SubjectLine(
            subject_id="tmA2",
            text="{name}, offre exclusive aujourd'hui? 🎉",
            template_id="tmpl-A",
            send_hour=9,
        ))
        best = self.optimizer.best_for_template("tmpl-A")
        assert best is not None
        assert best.subject.subject_id == "tmA2"

    def test_best_for_template_returns_none_when_no_match(self):
        result = self.optimizer.best_for_template("nonexistent-template")
        assert result is None

    def test_best_for_template_ignores_other_templates(self):
        self.optimizer.optimize(SubjectLine(
            subject_id="tB1", text="Offre exclusive pour vous maintenant!",
            template_id="tmpl-B"
        ))
        self.optimizer.optimize(SubjectLine(
            subject_id="tC1", text="{name}, check this offer today for you!",
            template_id="tmpl-C"
        ))
        best_b = self.optimizer.best_for_template("tmpl-B")
        assert best_b.subject.template_id == "tmpl-B"

    # --- by_tier ---

    def test_by_tier_returns_matching_tier(self):
        # Optimize a subject and find its tier, then verify by_tier returns it
        sl = SubjectLine(subject_id="tier1", text="Voici une simple newsletter")
        result = self.optimizer.optimize(sl)
        tier = result.optimization_tier
        by_t = self.optimizer.by_tier(tier)
        ids = [o.subject.subject_id for o in by_t]
        assert "tier1" in ids

    def test_by_tier_returns_empty_for_absent_tier(self):
        # Add a known weak subject; EXCELLENT tier should be empty
        self.optimizer.optimize(SubjectLine(subject_id="weak1", text="Hi"))
        excellent = self.optimizer.by_tier(OptimizationTier.EXCELLENT)
        # It's possible but unlikely; check ids don't include weak1
        ids = [o.subject.subject_id for o in excellent]
        assert "weak1" not in ids

    # --- compare ---

    def test_compare_returns_sorted_by_rate_desc(self):
        self.optimizer.optimize(SubjectLine(subject_id="cp1", text="Hello"))
        self.optimizer.optimize(SubjectLine(
            subject_id="cp2",
            text="{name}, offre exclusive aujourd'hui? 🎉",
            send_hour=9,
        ))
        compared = self.optimizer.compare(["cp1", "cp2"])
        assert len(compared) == 2
        assert compared[0].predicted_open_rate >= compared[1].predicted_open_rate

    def test_compare_ignores_unknown_ids(self):
        self.optimizer.optimize(SubjectLine(subject_id="cq1", text="Test subject line"))
        compared = self.optimizer.compare(["cq1", "does-not-exist"])
        assert len(compared) == 1
        assert compared[0].subject.subject_id == "cq1"

    def test_compare_empty_list_returns_empty(self):
        result = self.optimizer.compare([])
        assert result == []

    # --- summary ---

    def test_summary_all_keys_present(self):
        self.optimizer.optimize(SubjectLine(
            subject_id="sum1", text="Découvrez notre offre mensuelle!"
        ))
        s = self.optimizer.summary()
        assert set(s.keys()) == {
            "total", "tier_counts", "avg_open_rate", "best_open_rate",
            "pct_with_personalization"
        }

    def test_summary_empty_store(self):
        s = self.optimizer.summary()
        assert s["total"] == 0
        assert s["avg_open_rate"] == 0.0
        assert s["best_open_rate"] == 0.0
        assert s["pct_with_personalization"] == 0.0
        assert set(s["tier_counts"].keys()) == {"weak", "fair", "good", "excellent"}

    def test_summary_total_count(self):
        for i in range(4):
            self.optimizer.optimize(SubjectLine(
                subject_id=f"sum{i}", text=f"Subject line number {i} test check"
            ))
        s = self.optimizer.summary()
        assert s["total"] == 4

    def test_summary_tier_counts_sum_to_total(self):
        for i in range(5):
            self.optimizer.optimize(SubjectLine(
                subject_id=f"sc{i}", text=f"Subject number {i} for tier test check"
            ))
        s = self.optimizer.summary()
        assert sum(s["tier_counts"].values()) == s["total"]

    def test_summary_pct_personalization(self):
        self.optimizer.optimize(SubjectLine(
            subject_id="p1", text="Bonjour {name}, voici votre offre exclusive!"
        ))
        self.optimizer.optimize(SubjectLine(
            subject_id="p2", text="Voici une offre sans personnalisation du tout"
        ))
        s = self.optimizer.summary()
        assert s["pct_with_personalization"] == 0.5

    def test_summary_best_open_rate_is_max(self):
        sl1 = SubjectLine(subject_id="br1", text="Hi")
        sl2 = SubjectLine(
            subject_id="br2",
            text="{name}, offre exclusive aujourd'hui? 🎉",
            send_hour=9,
        )
        r1 = self.optimizer.optimize(sl1)
        r2 = self.optimizer.optimize(sl2)
        s = self.optimizer.summary()
        expected_best = round(max(r1.predicted_open_rate, r2.predicted_open_rate), 4)
        assert s["best_open_rate"] == expected_best

    # --- reset ---

    def test_reset_clears_store(self):
        self.optimizer.optimize(SubjectLine(subject_id="r1", text="Reset test subject line"))
        self.optimizer.reset()
        assert self.optimizer.all_subjects() == []
        assert self.optimizer.get("r1") is None

    def test_reset_summary_returns_zeros(self):
        self.optimizer.optimize(SubjectLine(
            subject_id="r2", text="Reset summary test subject line"
        ))
        self.optimizer.reset()
        s = self.optimizer.summary()
        assert s["total"] == 0

    def test_can_optimize_after_reset(self):
        self.optimizer.optimize(SubjectLine(subject_id="r3", text="Pre-reset subject line"))
        self.optimizer.reset()
        sl = SubjectLine(subject_id="r4", text="Post-reset subject works fine!")
        result = self.optimizer.optimize(sl)
        assert result.subject.subject_id == "r4"
        assert self.optimizer.get("r4") is not None


# ---------------------------------------------------------------------------
# TestComputePredictedOpenRate
# ---------------------------------------------------------------------------

class TestComputePredictedOpenRate:
    def test_formula_with_perfect_scores(self):
        scores = {
            "length": 100.0,
            "personalization": 100.0,
            "urgency": 100.0,
            "clarity": 100.0,
            "question": 100.0,
            "emoji_balance": 100.0,
        }
        # composite = 100, rate = (0.15 + 1.0*0.35) * 1.15 = 0.50 * 1.15 = 0.575
        rate = _compute_predicted_open_rate(scores, send_hour=9)
        assert rate == pytest.approx(0.50 * 1.15, abs=1e-3)

    def test_formula_with_zero_scores(self):
        scores = {
            "length": 0.0,
            "personalization": 0.0,
            "urgency": 0.0,
            "clarity": 0.0,
            "question": 0.0,
            "emoji_balance": 0.0,
        }
        # composite = 0, rate = 0.15 * 0.75 (off-hours)
        rate = _compute_predicted_open_rate(scores, send_hour=3)
        assert rate == pytest.approx(0.15 * 0.75, abs=1e-3)

    def test_rate_is_clamped_to_1(self):
        scores = {k: 100.0 for k in
                  ["length", "personalization", "urgency", "clarity", "question", "emoji_balance"]}
        rate = _compute_predicted_open_rate(scores, send_hour=9)
        assert rate <= 1.0

    def test_rate_is_clamped_to_0(self):
        scores = {k: 0.0 for k in
                  ["length", "personalization", "urgency", "clarity", "question", "emoji_balance"]}
        rate = _compute_predicted_open_rate(scores, send_hour=3)
        assert rate >= 0.0

    def test_send_hour_affects_rate(self):
        scores = {k: 50.0 for k in
                  ["length", "personalization", "urgency", "clarity", "question", "emoji_balance"]}
        rate_peak = _compute_predicted_open_rate(scores, send_hour=9)    # 1.15
        rate_off = _compute_predicted_open_rate(scores, send_hour=3)     # 0.75
        assert rate_peak > rate_off


# ---------------------------------------------------------------------------
# TestCountEmojis
# ---------------------------------------------------------------------------

class TestCountEmojis:
    def test_no_emoji_returns_0(self):
        assert _count_emojis("Hello world, no emojis here!") == 0

    def test_one_emoji(self):
        assert _count_emojis("Great offer 🎉") == 1

    def test_two_emojis(self):
        assert _count_emojis("🚀 Launch 🎉 now") == 2

    def test_four_emojis(self):
        # Emojis must be separated by non-emoji chars so each is a distinct regex match
        assert _count_emojis("a🎉b🚀c🔥d😀") == 4

    def test_text_only_no_emoji(self):
        assert _count_emojis("No special characters here at all") == 0
