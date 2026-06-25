"""
Sentiment Router — analyses prospect reply text and routes to the most
appropriate negotiation agent.

Uses a keyword-based heuristic (fast, no external API calls) combined with
an optional Claude API call for accurate sentiment when ANTHROPIC_API_KEY is set.

Sentiment classes:
  Positif   → Agent 3.5  (fast close, upsell)
  Curieux   → Agent 3.5  (nurture, educate)
  Sceptique → Agent 3.1  (objection handling — preuves)
  Méfiant   → Agent 3.2  (objection handling — garanties)
  Négatif   → Agent 3.3  (empathie + urgence douce)
  Fantôme   → Agent 3.7  (relance J+4)
  Pressé    → Agent 3.5  (quick close)

Usage:
    from intelligence.sentiment_router import SentimentRouter
    router = SentimentRouter()
    result = router.analyze("Je suis intéressé mais j'ai des doutes")
    print(result.sentiment, result.agent_id, result.confidence)
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger("swarm.sentiment")


# ── Keyword dictionaries ───────────────────────────────────────────────────────

_POSITIVE_KEYWORDS = [
    "intéressé", "super", "parfait", "excellent", "d'accord", "ok", "oui",
    "bonne idée", "top", "impressionné", "bravo", "merci", "quand", "commencer",
    "allons-y", "enchanté", "disponible", "rendez-vous",
]

_CURIOUS_KEYWORDS = [
    "comment", "pourquoi", "expliquer", "plus d'info", "en savoir plus",
    "curieux", "comprendre", "détail", "fonctionn", "exemple", "montrer",
    "question", "demande", "pouvez-vous", "pourrais", "qu'est-ce",
]

_SKEPTICAL_KEYWORDS = [
    "prouve", "preuve", "résultat", "garanti", "vraiment", "sûr", "certains",
    "beaucoup promettent", "j'ai déjà essayé", "comme les autres", "pareil",
    "bof", "moyen", "pas convaincu", "difficile à croire",
]

_SUSPICIOUS_KEYWORDS = [
    "arnaque", "méfiant", "méfie", "spam", "indésirable", "stop", "jamais demandé",
    "données personnelles", "rgpd", "désabonner", "comment avez-vous", "d'où venez",
    "supprimer", "STOP",
]

_NEGATIVE_KEYWORDS = [
    "non", "pas intéressé", "pas besoin", "laissez-moi", "ne pas contacter",
    "trop cher", "aucun intérêt", "occupé", "plus tard peut-être",
    "cousin", "déjà quelqu'un", "interne",
]

_GHOST_SIGNALS = []  # no reply → caller must detect silence externally

_URGENT_KEYWORDS = [
    "urgent", "rapidement", "vite", "maintenant", "aujourd'hui", "dès que",
    "immédiatement", "sous 24h", "au plus vite",
]


@dataclass
class SentimentResult:
    sentiment: str
    agent_id: str
    confidence: float  # 0.0–1.0
    reasoning: str
    keywords_matched: list[str]


# ── Routing map ───────────────────────────────────────────────────────────────

_ROUTING: dict[str, str] = {
    "Positif": "3.5",
    "Curieux": "3.5",
    "Sceptique": "3.1",
    "Méfiant": "3.2",
    "Négatif": "3.3",
    "Fantôme": "3.7",
    "Pressé": "3.5",
}


# ── Router ────────────────────────────────────────────────────────────────────

class SentimentRouter:
    def __init__(self, use_llm: bool = True):
        self._use_llm = use_llm and bool(os.getenv("ANTHROPIC_API_KEY"))
        logger.info("SentimentRouter init — LLM mode: %s", self._use_llm)

    def analyze(self, text: str) -> SentimentResult:
        """Analyze prospect reply and return routing decision."""
        if not text or not text.strip():
            return SentimentResult(
                sentiment="Fantôme",
                agent_id="3.7",
                confidence=1.0,
                reasoning="Empty reply → ghost treatment",
                keywords_matched=[],
            )

        result = self._heuristic_analyze(text)

        if self._use_llm and result.confidence < 0.7:
            try:
                llm_result = self._llm_analyze(text)
                if llm_result:
                    logger.info("LLM upgraded sentiment: %s → %s", result.sentiment, llm_result.sentiment)
                    return llm_result
            except Exception as e:
                logger.warning("LLM sentiment failed, using heuristic: %s", e)

        return result

    def _heuristic_analyze(self, text: str) -> SentimentResult:
        t = text.lower()

        scores: dict[str, list[str]] = {
            "Positif": [],
            "Curieux": [],
            "Sceptique": [],
            "Méfiant": [],
            "Négatif": [],
            "Pressé": [],
        }

        for kw in _POSITIVE_KEYWORDS:
            if re.search(r'\b' + re.escape(kw), t):
                scores["Positif"].append(kw)
        for kw in _CURIOUS_KEYWORDS:
            if re.search(r'\b' + re.escape(kw), t):
                scores["Curieux"].append(kw)
        for kw in _SKEPTICAL_KEYWORDS:
            if re.search(r'\b' + re.escape(kw), t):
                scores["Sceptique"].append(kw)
        for kw in _SUSPICIOUS_KEYWORDS:
            if kw.lower() in t or kw in text:
                scores["Méfiant"].append(kw)
        for kw in _NEGATIVE_KEYWORDS:
            if re.search(r'\b' + re.escape(kw), t):
                scores["Négatif"].append(kw)
        for kw in _URGENT_KEYWORDS:
            if re.search(r'\b' + re.escape(kw), t):
                scores["Pressé"].append(kw)

        # Méfiant overrides everything if triggered
        if scores["Méfiant"]:
            return SentimentResult(
                sentiment="Méfiant",
                agent_id=_ROUTING["Méfiant"],
                confidence=0.95,
                reasoning=f"Suspicious keywords detected: {scores['Méfiant']}",
                keywords_matched=scores["Méfiant"],
            )

        # Négatif wins ties — a rejection is never ambiguous
        def _rank(k: str) -> tuple:
            return (len(scores[k]), 1 if k == "Négatif" else 0)

        best = max(scores, key=_rank)
        matched = scores[best]

        if not matched:
            return SentimentResult(
                sentiment="Curieux",
                agent_id=_ROUTING["Curieux"],
                confidence=0.4,
                reasoning="No clear signal — defaulting to Curieux",
                keywords_matched=[],
            )

        total_signals = sum(len(v) for v in scores.values())
        confidence = min(0.95, len(matched) / max(total_signals, 1) + 0.4)

        return SentimentResult(
            sentiment=best,
            agent_id=_ROUTING[best],
            confidence=confidence,
            reasoning=f"Heuristic match: {matched}",
            keywords_matched=matched,
        )

    def _llm_analyze(self, text: str) -> Optional[SentimentResult]:
        """Use Claude API for nuanced sentiment analysis."""
        import anthropic  # type: ignore

        client = anthropic.Anthropic()
        prompt = f"""Analyse le sentiment commercial de ce message d'un prospect PME français et classe-le dans une de ces catégories :
Positif, Curieux, Sceptique, Méfiant, Négatif, Pressé

Message : "{text}"

Réponds UNIQUEMENT avec ce JSON :
{{"sentiment": "...", "confidence": 0.0-1.0, "reasoning": "..."}}"""

        msg = client.messages.create(
            model=os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001"),
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}],
        )

        import json
        raw = msg.content[0].text.strip()
        data = json.loads(raw)
        sentiment = data.get("sentiment", "Curieux")
        return SentimentResult(
            sentiment=sentiment,
            agent_id=_ROUTING.get(sentiment, "3.5"),
            confidence=float(data.get("confidence", 0.8)),
            reasoning=data.get("reasoning", "LLM analysis"),
            keywords_matched=[],
        )

    def route(self, text: str) -> str:
        """Convenience: returns just the agent_id to route to."""
        return self.analyze(text).agent_id
