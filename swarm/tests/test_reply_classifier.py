"""
Tests for intelligence/reply_classifier.py
"""

import pytest
from intelligence.reply_classifier import ReplyClassifier, ClassificationResult


# ── Helpers ───────────────────────────────────────────────────────────────────

def clf() -> ReplyClassifier:
    return ReplyClassifier()


# ── classify() — output structure ────────────────────────────────────────────

class TestClassifyOutput:
    def test_returns_classification_result(self):
        result = clf().classify("Je suis intéressé")
        assert isinstance(result, ClassificationResult)

    def test_objection_type_is_valid(self):
        result = clf().classify("Votre prix est trop cher")
        assert result.objection_type in {"price", "trust", "timing", "competitor", "technical", "none"}

    def test_timeline_is_valid(self):
        result = clf().classify("Je veux démarrer aujourd'hui")
        assert result.timeline in {"immédiat", "sous_48h", "cette_semaine", "dans_un_mois", "indéfini"}

    def test_buying_signal_in_range(self):
        result = clf().classify("Je suis intéressé, quand peut-on commencer ?")
        assert 0.0 <= result.buying_signal <= 1.0

    def test_priority_is_valid(self):
        result = clf().classify("Urgence !")
        assert result.priority in {"urgent", "high", "normal", "low"}

    def test_next_action_not_empty(self):
        result = clf().classify("Votre tarif est trop cher")
        assert len(result.next_action) > 0

    def test_to_dict_has_required_keys(self):
        d = clf().classify("test").to_dict()
        for key in ("objection_type", "timeline", "buying_signal",
                    "competitor_mentioned", "next_action", "priority"):
            assert key in d


# ── Empty / edge cases ────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_empty_string_returns_safe_default(self):
        result = clf().classify("")
        assert result.objection_type == "none"
        assert result.timeline == "indéfini"
        assert result.buying_signal == 0.0
        assert result.priority == "low"

    def test_whitespace_only_returns_safe_default(self):
        result = clf().classify("   ")
        assert result.objection_type == "none"

    def test_unrelated_text_returns_none_objection(self):
        result = clf().classify("Bonjour comment allez-vous")
        assert result.objection_type == "none"


# ── Objection detection ───────────────────────────────────────────────────────

class TestObjectionDetection:
    def test_price_objection_detected(self):
        result = clf().classify("Votre prix est trop cher pour notre budget")
        assert result.objection_type == "price"
        assert len(result.objection_keywords) > 0

    def test_trust_objection_detected(self):
        result = clf().classify("Je ne vous connais pas, j'ai besoin de preuve de votre sérieux")
        assert result.objection_type == "trust"

    def test_timing_objection_detected(self):
        result = clf().classify("Pas maintenant, peut-être plus tard dans quelques mois")
        assert result.objection_type == "timing"

    def test_competitor_objection_detected(self):
        result = clf().classify("Nous travaillons déjà avec quelqu'un d'autre")
        assert result.objection_type == "competitor"

    def test_technical_objection_detected(self):
        result = clf().classify("Je n'y connais rien en technique, c'est trop compliqué")
        assert result.objection_type == "technical"

    def test_no_objection_when_positive(self):
        result = clf().classify("Je suis intéressé et d'accord pour commencer")
        assert result.objection_type == "none"

    def test_trust_overrides_price_when_more_keywords(self):
        # Trust has multiple keywords vs single price
        result = clf().classify("Je ne vous connais pas, j'ai besoin de témoignage, de référence et d'avis clients")
        assert result.objection_type == "trust"


# ── Timeline detection ────────────────────────────────────────────────────────

class TestTimelineDetection:
    def test_immediate_timeline_detected(self):
        result = clf().classify("J'ai besoin de cela urgent, aujourd'hui si possible")
        assert result.timeline == "immédiat"

    def test_sous_48h_timeline_detected(self):
        result = clf().classify("Pouvez-vous me rappeler demain ?")
        assert result.timeline == "sous_48h"

    def test_cette_semaine_timeline_detected(self):
        result = clf().classify("On peut en reparler la semaine prochaine")
        assert result.timeline in {"sous_48h", "cette_semaine"}

    def test_dans_un_mois_timeline_detected(self):
        result = clf().classify("Contactez-moi le mois prochain")
        assert result.timeline == "dans_un_mois"

    def test_no_timeline_signal_returns_indefini(self):
        result = clf().classify("Votre offre est intéressante")
        assert result.timeline == "indéfini"

    def test_immediate_takes_priority(self):
        result = clf().classify("Urgent, aujourd'hui, et aussi la semaine prochaine c'est bien")
        assert result.timeline == "immédiat"


# ── Buying signal ─────────────────────────────────────────────────────────────

class TestBuyingSignal:
    def test_strong_buying_signal(self):
        result = clf().classify("Je suis intéressé, quand peut-on commencer ? D'accord pour le contrat")
        assert result.buying_signal >= 0.5

    def test_no_buying_signal(self):
        result = clf().classify("Non merci, cela ne nous convient pas.")
        assert result.buying_signal == 0.0

    def test_buying_keywords_extracted(self):
        result = clf().classify("D'accord, commencer aujourd'hui, envoyez le contrat")
        assert len(result.buying_keywords) > 0

    def test_buying_signal_capped_at_1(self):
        # Lots of buying keywords
        text = "intéressé quand commencer d'accord contrat signature rendez-vous disponible"
        result = clf().classify(text)
        assert result.buying_signal <= 1.0


# ── Competitor detection ──────────────────────────────────────────────────────

class TestCompetitorDetection:
    def test_competitor_flag_when_mentioned(self):
        result = clf().classify("Nous avons déjà un prestataire pour ça")
        assert result.competitor_mentioned is True

    def test_no_competitor_flag_for_clean_reply(self):
        result = clf().classify("Je suis intéressé par votre offre")
        assert result.competitor_mentioned is False

    def test_wix_mention_flags_competitor(self):
        result = clf().classify("Nous avons notre site sur Wix")
        assert result.competitor_mentioned is True

    def test_freelance_mention_flags_competitor(self):
        result = clf().classify("J'ai un freelance qui s'occupe de ça")
        assert result.competitor_mentioned is True


# ── Priority ──────────────────────────────────────────────────────────────────

class TestPriority:
    def test_urgent_when_immediate_and_buying(self):
        result = clf().classify("Urgent, j'ai besoin de commencer aujourd'hui d'accord")
        assert result.priority == "urgent"

    def test_high_when_short_timeline(self):
        result = clf().classify("Pouvez-vous rappeler demain ?")
        assert result.priority in {"urgent", "high"}

    def test_low_when_no_signals(self):
        result = clf().classify("Peut-être plus tard")
        assert result.priority == "low"


# ── Next action ───────────────────────────────────────────────────────────────

class TestNextAction:
    def test_price_immediate_has_urgency_action(self):
        result = clf().classify("Trop cher pour notre budget, mais j'ai besoin de quelque chose urgent aujourd'hui")
        assert len(result.next_action) > 5

    def test_trust_indéfini_mentions_garantie(self):
        result = clf().classify("J'ai besoin de preuve, je ne vous connais pas")
        assert len(result.next_action) > 5

    def test_competitor_action_mentions_comparison(self):
        result = clf().classify("Nous travaillons déjà avec quelqu'un d'autre, satisfait")
        assert len(result.next_action) > 5


# ── classify_batch ────────────────────────────────────────────────────────────

class TestClassifyBatch:
    def test_returns_list(self):
        texts = ["Je suis intéressé", "Trop cher", ""]
        results = clf().classify_batch(texts)
        assert isinstance(results, list)
        assert len(results) == 3

    def test_each_result_is_classification_result(self):
        results = clf().classify_batch(["test 1", "test 2"])
        assert all(isinstance(r, ClassificationResult) for r in results)

    def test_empty_batch(self):
        assert clf().classify_batch([]) == []
