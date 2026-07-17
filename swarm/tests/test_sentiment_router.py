"""Tests for SentimentRouter (heuristic mode only — no API key required)."""

import pytest
from intelligence.sentiment_router import SentimentRouter, SentimentResult


@pytest.fixture()
def router():
    return SentimentRouter(use_llm=False)


class TestEmptyAndGhost:
    def test_empty_string_returns_fantome(self, router):
        r = router.analyze("")
        assert r.sentiment == "Fantôme"

    def test_whitespace_only_returns_fantome(self, router):
        r = router.analyze("   ")
        assert r.sentiment == "Fantôme"

    def test_fantome_routes_to_3_7(self, router):
        r = router.analyze("")
        assert r.agent_id == "3.7"

    def test_fantome_confidence_is_1(self, router):
        r = router.analyze("")
        assert r.confidence == 1.0


class TestPositiveSentiment:
    def test_interested_text(self, router):
        r = router.analyze("Je suis intéressé par votre offre")
        assert r.sentiment == "Positif"

    def test_ok_yes(self, router):
        r = router.analyze("Oui d'accord, allons-y")
        assert r.sentiment == "Positif"

    def test_positive_routes_to_3_5(self, router):
        r = router.analyze("Super idée, quand peut-on commencer ?")
        assert r.agent_id == "3.5"

    def test_positive_has_keywords(self, router):
        r = router.analyze("Super, parfait !")
        assert len(r.keywords_matched) > 0


class TestCuriousSentiment:
    def test_how_question(self, router):
        r = router.analyze("comment ça fonctionne exactement ?")
        assert r.sentiment == "Curieux"

    def test_more_info_request(self, router):
        r = router.analyze("J'aimerais en savoir plus sur votre solution")
        assert r.sentiment == "Curieux"

    def test_default_no_signal_is_curieux(self, router):
        r = router.analyze("Bonjour, j'ai bien reçu votre message.")
        assert r.sentiment == "Curieux"


class TestSkepticalSentiment:
    def test_proof_request(self, router):
        r = router.analyze("Vous avez des preuves de vos résultats ?")
        assert r.sentiment == "Sceptique"

    def test_not_convinced(self, router):
        r = router.analyze("pas convaincu que ça marche vraiment")
        assert r.sentiment == "Sceptique"

    def test_skeptical_routes_to_3_1(self, router):
        r = router.analyze("Difficile à croire sans garanties")
        assert r.agent_id == "3.1"


class TestSuspiciousSentiment:
    def test_spam_word_triggers_mefiant(self, router):
        r = router.analyze("C'est du spam, désabonnez-moi")
        assert r.sentiment == "Méfiant"

    def test_mefiant_overrides_positive(self, router):
        r = router.analyze("Super idée mais c'est une arnaque")
        assert r.sentiment == "Méfiant"

    def test_mefiant_routes_to_3_2(self, router):
        r = router.analyze("STOP envoyez-moi plus rien")
        assert r.agent_id == "3.2"

    def test_high_confidence_for_mefiant(self, router):
        r = router.analyze("arnaque")
        assert r.confidence >= 0.9


class TestNegativeSentiment:
    def test_not_interested(self, router):
        r = router.analyze("non, pas intéressé du tout")
        assert r.sentiment == "Négatif"

    def test_negative_routes_to_3_3(self, router):
        r = router.analyze("Pas besoin, aucun intérêt")
        assert r.agent_id == "3.3"


class TestUrgentSentiment:
    def test_urgent_keyword(self, router):
        r = router.analyze("C'est urgent, j'ai besoin d'une réponse aujourd'hui")
        assert r.sentiment == "Pressé"

    def test_presse_routes_to_3_5(self, router):
        r = router.analyze("Rappellez-moi immédiatement s'il vous plaît")
        assert r.agent_id == "3.5"


class TestResultShape:
    def test_result_is_sentiment_result(self, router):
        r = router.analyze("Bonjour")
        assert isinstance(r, SentimentResult)

    def test_confidence_between_0_and_1(self, router):
        texts = [
            "intéressé", "pas intéressé", "comment ça marche",
            "arnaque", "urgent", "", "pas convaincu",
        ]
        for t in texts:
            r = router.analyze(t)
            assert 0.0 <= r.confidence <= 1.0, f"confidence out of range for: {t!r}"

    def test_agent_id_is_valid(self, router):
        valid = {"3.1", "3.2", "3.3", "3.5", "3.7"}
        texts = [
            "intéressé", "pas intéressé", "comment ça marche",
            "arnaque", "urgent", "", "pas convaincu", "garanties",
        ]
        for t in texts:
            r = router.analyze(t)
            assert r.agent_id in valid, f"bad agent_id {r.agent_id!r} for: {t!r}"

    def test_keywords_matched_is_list(self, router):
        r = router.analyze("super intéressé")
        assert isinstance(r.keywords_matched, list)

    def test_route_returns_string(self, router):
        agent = router.route("Je suis intéressé")
        assert isinstance(agent, str)
        assert "." in agent
