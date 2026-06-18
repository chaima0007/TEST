"""
Email Subject Optimizer — predicts open rate for email subject lines based on
structural and linguistic signals:
  length_score(20%) + personalization(25%) + urgency(20%) + clarity(15%)
  + question(10%) + emoji_balance(10%)
  → predicted_open_rate 0.0-1.0, OptimizationTier: WEAK/FAIR/GOOD/EXCELLENT
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple


class OptimizationTier(str, Enum):
    WEAK = "weak"
    FAIR = "fair"
    GOOD = "good"
    EXCELLENT = "excellent"


_URGENCY_WORDS = frozenset([
    "urgent", "dernière chance", "expire", "limite", "maintenant", "aujourd'hui",
    "offre", "exclusif", "seulement", "immédiat", "critique", "alerte",
])

_CLARITY_PENALTIES = frozenset([
    "fwd:", "re:", "important!!!", "attention!!!", "cliquez",
])

_PERSONAL_TOKENS = re.compile(r"\{(\w+)\}")

_EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002700-\U000027BF"
    "\U0001F900-\U0001F9FF"
    "\U00002B00-\U00002BFF"
    "\U00002600-\U000026FF"
    "]",
    flags=re.UNICODE,
)

_TIER_THRESHOLDS = {
    OptimizationTier.EXCELLENT: 0.38,
    OptimizationTier.GOOD: 0.28,
    OptimizationTier.FAIR: 0.18,
}

_BASELINE_OPEN_RATE = 0.15

_SUGGESTIONS: Dict[str, str] = {
    "too_long": "Raccourcir le sujet à moins de 60 caractères",
    "too_short": "Allonger le sujet — au moins 20 caractères pour donner du contexte",
    "no_personalization": "Ajouter {contact_name} ou {company_name} pour personnaliser",
    "no_urgency": "Inclure un mot d'urgence (offre, limite, aujourd'hui…)",
    "no_question": "Formuler comme une question pour susciter la curiosité",
    "spam_risk": "Retirer les mots spam (fwd, re:, !!!)",
    "too_many_emojis": "Limiter à 1-2 emojis maximum",
    "no_emoji": "Un emoji en début ou fin peut augmenter le taux d'ouverture de 15%",
}


@dataclass
class SubjectLine:
    subject_id: str
    text: str
    template_id: Optional[str] = None
    variant_key: str = "A"
    send_hour: int = 9

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class OptimizedSubject:
    subject: SubjectLine
    predicted_open_rate: float
    optimization_tier: OptimizationTier
    dimension_scores: Dict[str, float]
    suggestions: List[str]
    emoji_count: int
    word_count: int
    char_count: int
    has_personalization: bool
    has_urgency: bool
    has_question: bool

    def to_dict(self) -> dict:
        return {
            "subject": self.subject.to_dict(),
            "predicted_open_rate": self.predicted_open_rate,
            "optimization_tier": self.optimization_tier.value,
            "dimension_scores": self.dimension_scores,
            "suggestions": self.suggestions,
            "emoji_count": self.emoji_count,
            "word_count": self.word_count,
            "char_count": self.char_count,
            "has_personalization": self.has_personalization,
            "has_urgency": self.has_urgency,
            "has_question": self.has_question,
        }


def _count_emojis(text: str) -> int:
    return sum(len(m) for m in _EMOJI_PATTERN.findall(text))


def _length_score(text: str) -> Tuple[float, List[str]]:
    length = len(text)
    tips: List[str] = []
    if length < 20:
        tips.append("too_short")
        return 30.0, tips
    if length <= 40:
        return 100.0, tips
    if length <= 60:
        return 80.0, tips
    tips.append("too_long")
    return max(0.0, 80.0 - (length - 60) * 2.0), tips


def _personalization_score(text: str) -> Tuple[float, List[str]]:
    tokens = _PERSONAL_TOKENS.findall(text)
    tips: List[str] = []
    if not tokens:
        tips.append("no_personalization")
        return 0.0, tips
    return min(100.0, len(tokens) * 50.0), tips


def _urgency_score(text: str) -> Tuple[float, List[str]]:
    lower = text.lower()
    hits = sum(1 for w in _URGENCY_WORDS if w in lower)
    tips: List[str] = []
    if hits == 0:
        tips.append("no_urgency")
        return 20.0, tips
    return min(100.0, 40.0 + hits * 30.0), tips


def _clarity_score(text: str) -> Tuple[float, List[str]]:
    lower = text.lower()
    penalties = sum(1 for p in _CLARITY_PENALTIES if p in lower)
    tips: List[str] = []
    if penalties > 0:
        tips.append("spam_risk")
    return max(0.0, 100.0 - penalties * 40.0), tips


def _question_score(text: str) -> Tuple[float, List[str]]:
    has_q = "?" in text
    tips: List[str] = []
    if not has_q:
        tips.append("no_question")
        return 30.0, tips
    return 100.0, tips


def _emoji_balance_score(text: str) -> Tuple[float, List[str]]:
    count = _count_emojis(text)
    tips: List[str] = []
    if count == 0:
        tips.append("no_emoji")
        return 50.0, tips
    if count <= 2:
        return 100.0, tips
    tips.append("too_many_emojis")
    return max(0.0, 100.0 - (count - 2) * 20.0), tips


def _send_hour_multiplier(hour: int) -> float:
    if 8 <= hour <= 10:
        return 1.15
    if 11 <= hour <= 13:
        return 1.05
    if 14 <= hour <= 16:
        return 1.0
    if 6 <= hour <= 7 or 17 <= hour <= 19:
        return 0.90
    return 0.75


_WEIGHTS = {
    "length": 0.20,
    "personalization": 0.25,
    "urgency": 0.20,
    "clarity": 0.15,
    "question": 0.10,
    "emoji_balance": 0.10,
}


def _compute_predicted_open_rate(
    dimension_scores: Dict[str, float], send_hour: int
) -> float:
    composite = sum(dimension_scores[k] * w for k, w in _WEIGHTS.items())
    rate = _BASELINE_OPEN_RATE + (composite / 100.0) * 0.35
    rate *= _send_hour_multiplier(send_hour)
    return round(max(0.0, min(1.0, rate)), 4)


def _classify_tier(rate: float) -> OptimizationTier:
    if rate >= _TIER_THRESHOLDS[OptimizationTier.EXCELLENT]:
        return OptimizationTier.EXCELLENT
    if rate >= _TIER_THRESHOLDS[OptimizationTier.GOOD]:
        return OptimizationTier.GOOD
    if rate >= _TIER_THRESHOLDS[OptimizationTier.FAIR]:
        return OptimizationTier.FAIR
    return OptimizationTier.WEAK


def _optimize(subject: SubjectLine) -> OptimizedSubject:
    text = subject.text

    len_score, len_tips = _length_score(text)
    pers_score, pers_tips = _personalization_score(text)
    urg_score, urg_tips = _urgency_score(text)
    clar_score, clar_tips = _clarity_score(text)
    q_score, q_tips = _question_score(text)
    emoji_score, emoji_tips = _emoji_balance_score(text)

    dimension_scores = {
        "length": len_score,
        "personalization": pers_score,
        "urgency": urg_score,
        "clarity": clar_score,
        "question": q_score,
        "emoji_balance": emoji_score,
    }

    all_tip_keys = len_tips + pers_tips + urg_tips + clar_tips + q_tips + emoji_tips
    suggestions = [_SUGGESTIONS[k] for k in all_tip_keys if k in _SUGGESTIONS]

    rate = _compute_predicted_open_rate(dimension_scores, subject.send_hour)
    tier = _classify_tier(rate)

    words = text.split()

    return OptimizedSubject(
        subject=subject,
        predicted_open_rate=rate,
        optimization_tier=tier,
        dimension_scores=dimension_scores,
        suggestions=suggestions,
        emoji_count=_count_emojis(text),
        word_count=len(words),
        char_count=len(text),
        has_personalization=bool(_PERSONAL_TOKENS.search(text)),
        has_urgency=any(w in text.lower() for w in _URGENCY_WORDS),
        has_question="?" in text,
    )


class EmailSubjectOptimizer:
    def __init__(self) -> None:
        self._store: Dict[str, OptimizedSubject] = {}

    def optimize(self, subject: SubjectLine) -> OptimizedSubject:
        result = _optimize(subject)
        self._store[subject.subject_id] = result
        return result

    def optimize_batch(self, subjects: List[SubjectLine]) -> List[OptimizedSubject]:
        return [self.optimize(s) for s in subjects]

    def get(self, subject_id: str) -> Optional[OptimizedSubject]:
        return self._store.get(subject_id)

    def all_subjects(self) -> List[OptimizedSubject]:
        return sorted(
            self._store.values(),
            key=lambda o: o.predicted_open_rate,
            reverse=True,
        )

    def best_for_template(self, template_id: str) -> Optional[OptimizedSubject]:
        candidates = [
            o for o in self._store.values()
            if o.subject.template_id == template_id
        ]
        return max(candidates, key=lambda o: o.predicted_open_rate) if candidates else None

    def by_tier(self, tier: OptimizationTier) -> List[OptimizedSubject]:
        return [o for o in self._store.values() if o.optimization_tier == tier]

    def compare(self, subject_ids: List[str]) -> List[OptimizedSubject]:
        results = [self._store[sid] for sid in subject_ids if sid in self._store]
        return sorted(results, key=lambda o: o.predicted_open_rate, reverse=True)

    def summary(self) -> dict:
        items = list(self._store.values())
        count = len(items)
        if count == 0:
            return {
                "total": 0,
                "tier_counts": {t.value: 0 for t in OptimizationTier},
                "avg_open_rate": 0.0,
                "best_open_rate": 0.0,
                "pct_with_personalization": 0.0,
            }
        tier_counts = {t.value: 0 for t in OptimizationTier}
        for o in items:
            tier_counts[o.optimization_tier.value] += 1
        avg_rate = sum(o.predicted_open_rate for o in items) / count
        best_rate = max(o.predicted_open_rate for o in items)
        pct_personal = sum(1 for o in items if o.has_personalization) / count
        return {
            "total": count,
            "tier_counts": tier_counts,
            "avg_open_rate": round(avg_rate, 4),
            "best_open_rate": round(best_rate, 4),
            "pct_with_personalization": round(pct_personal, 4),
        }

    def reset(self) -> None:
        self._store.clear()
