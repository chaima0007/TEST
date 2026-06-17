"""
Tests for the intelligence modules: SentimentRouter and ABTester.
"""

import pytest
from intelligence.sentiment_router import SentimentRouter, SentimentResult
from intelligence.ab_tester import ABTester, AgentVariant, DEFAULT_VARIANTS


# ── SentimentRouter ───────────────────────────────────────────────────────────

class TestSentimentRouter:
    def setup_method(self):
        self.router = SentimentRouter(use_llm=False)

    def test_empty_text_returns_fantome(self):
        r = self.router.analyze("")
        assert r.sentiment == "Fantôme"
        assert r.agent_id == "3.7"
        assert r.confidence == 1.0

    def test_whitespace_returns_fantome(self):
        r = self.router.analyze("   \n  ")
        assert r.sentiment == "Fantôme"

    def test_positive_keywords_detected(self):
        r = self.router.analyze("Oui je suis intéressé, quand pouvons-nous commencer ?")
        assert r.sentiment == "Positif"
        assert r.agent_id == "3.5"
        assert r.confidence > 0.4
        assert len(r.keywords_matched) > 0

    def test_curious_keywords_detected(self):
        r = self.router.analyze("Pouvez-vous m'expliquer comment ça fonctionne ?")
        assert r.sentiment == "Curieux"
        assert r.agent_id == "3.5"

    def test_skeptical_keywords_detected(self):
        r = self.router.analyze("Vous avez des preuves ? Je ne suis pas convaincu.")
        assert r.sentiment == "Sceptique"
        assert r.agent_id == "3.1"

    def test_suspicious_keywords_override(self):
        r = self.router.analyze("C'est une arnaque ! Je n'ai jamais demandé ce spam.")
        assert r.sentiment == "Méfiant"
        assert r.agent_id == "3.2"
        assert r.confidence == 0.95

    def test_negative_keywords_detected(self):
        r = self.router.analyze("Non merci, pas intéressé.")
        assert r.sentiment == "Négatif"
        assert r.agent_id == "3.3"

    def test_urgent_keywords_detected(self):
        r = self.router.analyze("Urgent ! J'ai besoin d'une intervention aujourd'hui même.")
        assert r.sentiment == "Pressé"
        assert r.agent_id == "3.5"

    def test_no_keywords_defaults_to_curieux(self):
        r = self.router.analyze("Bonjour.")
        assert r.sentiment == "Curieux"
        assert r.confidence == 0.4

    def test_route_returns_string(self):
        agent_id = self.router.route("Je suis intéressé.")
        assert isinstance(agent_id, str)
        assert "." in agent_id

    def test_suspicious_overrides_positive(self):
        r = self.router.analyze("Super arnaque ! Très intéressé non.")
        assert r.sentiment == "Méfiant"

    def test_result_is_dataclass(self):
        r = self.router.analyze("Test message")
        assert isinstance(r, SentimentResult)
        assert hasattr(r, "sentiment")
        assert hasattr(r, "agent_id")
        assert hasattr(r, "confidence")
        assert hasattr(r, "reasoning")
        assert hasattr(r, "keywords_matched")

    def test_confidence_between_zero_and_one(self):
        for text in ["intéressé", "arnaque", "non merci", "urgent", "preuve"]:
            r = self.router.analyze(text)
            assert 0.0 <= r.confidence <= 1.0, f"Confidence out of range for '{text}': {r.confidence}"


# ── ABTester ──────────────────────────────────────────────────────────────────

class TestABTester:
    def setup_method(self):
        self.tester = ABTester()

    def test_has_nine_variants(self):
        assert len(self.tester.variants) == 9

    def test_default_variant_ids(self):
        expected_ids = {"2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9"}
        assert set(self.tester.variants.keys()) == expected_ids

    def test_select_agent_returns_valid_id(self):
        agent_id = self.tester.select_agent()
        assert agent_id in self.tester.variants

    def test_exploration_phase_covers_all_variants(self):
        selected = set()
        for _ in range(100):
            selected.add(self.tester.select_agent())
        assert len(selected) > 1

    def test_sector_paris_biases_agent_2_6(self):
        # With fresh tester (0 sends), Paris sector should return 2.6
        selected = self.tester.select_agent(sector="Paris et Île-de-France")
        assert selected == "2.6"

    def test_sector_nord_biases_agent_2_4(self):
        selected = self.tester.select_agent(sector="Lille Nord")
        assert selected == "2.4"

    def test_sector_sud_biases_agent_2_5(self):
        selected = self.tester.select_agent(sector="Marseille Sud")
        assert selected == "2.5"

    def test_sector_artisan_biases_agent_2_8(self):
        selected = self.tester.select_agent(sector="artisan plombier")
        assert selected == "2.8"

    def test_record_result_increments_sent(self):
        self.tester.record_result("2.1", sent=True)
        assert self.tester.variants["2.1"].sent == 1

    def test_record_result_reply_updates_alpha(self):
        v = self.tester.variants["2.1"]
        alpha_before = v.alpha
        self.tester.record_result("2.1", replied=True)
        assert v.alpha > alpha_before

    def test_record_result_no_reply_updates_beta(self):
        v = self.tester.variants["2.1"]
        beta_before = v.beta
        self.tester.record_result("2.1", replied=False)
        assert v.beta > beta_before

    def test_record_result_paid_strong_alpha_boost(self):
        v = self.tester.variants["2.1"]
        alpha_before = v.alpha
        self.tester.record_result("2.1", paid=True)
        assert v.alpha >= alpha_before + 2

    def test_get_winner_none_before_ten_sends(self):
        assert self.tester.get_winner() is None

    def test_get_winner_after_enough_sends(self):
        for _ in range(11):
            self.tester.record_result("2.1", sent=True, replied=True)
        winner = self.tester.get_winner()
        assert winner is not None
        assert winner.agent_id == "2.1"

    def test_get_report_structure(self):
        report = self.tester.get_report()
        assert "started_at" in report
        assert "total_sent" in report
        assert "total_replied" in report
        assert "winner" in report
        assert "variants" in report
        assert isinstance(report["variants"], list)
        assert len(report["variants"]) == 9

    def test_get_report_variants_sorted_by_reply_rate(self):
        # Give agent 2.3 high reply rate
        for _ in range(12):
            self.tester.record_result("2.3", sent=True, replied=True)
        report = self.tester.get_report()
        assert report["variants"][0]["agent_id"] == "2.3"

    def test_unknown_agent_id_does_not_crash(self):
        self.tester.record_result("9.9", sent=True)  # should log warning, not crash

    def test_reset_clears_all_stats(self):
        self.tester.record_result("2.1", sent=True, replied=True)
        self.tester.reset()
        for v in self.tester.variants.values():
            assert v.sent == 0
            assert v.replied == 0
            assert v.alpha == 1.0
            assert v.beta == 1.0

    def test_sample_returns_float_in_zero_one(self):
        v = self.tester.variants["2.1"]
        for _ in range(50):
            s = v.sample()
            assert 0.0 <= s <= 1.0

    def test_to_dict_has_rates(self):
        d = self.tester.variants["2.1"].to_dict()
        assert "open_rate" in d
        assert "reply_rate" in d
        assert "conversion_rate" in d

    def test_custom_variants(self):
        variants = [AgentVariant("X.1", "Tone A"), AgentVariant("X.2", "Tone B")]
        tester = ABTester(variants=variants)
        assert len(tester.variants) == 2
        assert tester.select_agent() in {"X.1", "X.2"}
