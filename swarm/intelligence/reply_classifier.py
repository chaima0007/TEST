"""
Reply Classifier — deeper analysis of prospect replies beyond basic sentiment.

Extracts:
  - Objection type (price / trust / timing / competitor / technical / none)
  - Timeline urgency (immédiat / sous_48h / cette_semaine / dans_un_mois / indéfini)
  - Competitor mention detection
  - Buying signal strength (0.0-1.0)
  - Next action recommendation

Used by Division 3 agents to personalise negotiation responses.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional


# ── Keyword tables ────────────────────────────────────────────────────────────

_PRICE_OBJECTIONS = [
    "trop cher", "budget", "prix", "coût", "coute", "tarif", "devis",
    "pas les moyens", "financièrement", "euro", "€",
]

_TRUST_OBJECTIONS = [
    "arnaque", "méfiant", "jamais entendu", "inconnu", "comment savoir",
    "référence", "avis", "témoignage", "preuve", "garanti", "certifié",
    "fiable", "sérieux", "confiance", "vérifié",
]

_TIMING_OBJECTIONS = [
    "pas maintenant", "plus tard", "dans quelques mois", "l'année prochaine",
    "après les vacances", "pas le bon moment", "trop occupé", "pas prioritaire",
    "on verra", "peut-être plus tard",
]

_COMPETITOR_SIGNALS = [
    "concurrent", "agence", "prestataire", "quelqu'un d'autre", "quelqu'un",
    "déjà un", "déjà une", "travaillons avec", "fidèle à", "satisfait de",
    "pas de changement", "freelance", "wix", "wordpress", "shopify",
]

_TECHNICAL_OBJECTIONS = [
    "trop compliqué", "pas informaticien", "je n'y connais rien", "technique",
    "comment ça marche", "difficile", "complexe", "besoin d'aide", "accompagnement",
    "formation", "pas le temps",
]

_BUYING_SIGNALS = [
    "intéressé", "quand", "comment commencer", "combien", "procédure",
    "contrat", "signature", "commencer", "démarrer", "aujourd'hui",
    "parfait", "go", "ok", "d'accord", "marché conclu", "rendez-vous",
    "appeler", "disponible", "envoyer", "proposez",
]

_IMMEDIATE_TIMELINE = [
    "aujourd'hui", "maintenant", "immédiatement", "urgent", "sous 24h",
    "dès que", "au plus vite", "rapidement",
]

_SHORT_TIMELINE = [
    "cette semaine", "sous 48h", "lundi", "mardi", "mercredi",
    "jeudi", "vendredi", "48 heures", "demain",
]

_MEDIUM_TIMELINE = [
    "cette semaine", "fin de semaine", "avant le", "la semaine prochaine",
    "début de mois", "dans les jours",
]

_LONG_TIMELINE = [
    "le mois prochain", "dans un mois", "dans quelques semaines",
    "prochain trimestre", "fin de mois",
]


# ── Output ─────────────────────────────────────────────────────────────────────

@dataclass
class ClassificationResult:
    objection_type: str            # "price" | "trust" | "timing" | "competitor" | "technical" | "none"
    timeline: str                  # "immédiat" | "sous_48h" | "cette_semaine" | "dans_un_mois" | "indéfini"
    buying_signal: float           # 0.0-1.0
    competitor_mentioned: bool
    objection_keywords: List[str] = field(default_factory=list)
    buying_keywords: List[str] = field(default_factory=list)
    next_action: str = ""
    priority: str = "normal"       # "urgent" | "high" | "normal" | "low"

    def to_dict(self) -> dict:
        return {
            "objection_type": self.objection_type,
            "timeline": self.timeline,
            "buying_signal": round(self.buying_signal, 3),
            "competitor_mentioned": self.competitor_mentioned,
            "objection_keywords": self.objection_keywords,
            "buying_keywords": self.buying_keywords,
            "next_action": self.next_action,
            "priority": self.priority,
        }


# ── Classifier ────────────────────────────────────────────────────────────────

class ReplyClassifier:
    """
    Keyword-based reply intent classifier.
    Runs offline — no external API calls.
    """

    _NEXT_ACTIONS = {
        # (objection_type, timeline): action
        ("price",      "immédiat"):     "Envoyer offre groupée avec réduction 15% — sous 1h",
        ("price",      "sous_48h"):     "Envoyer ROI calculator + étude de cas secteur",
        ("price",      "cette_semaine"):"Proposer appel de 15 min pour budget personnalisé",
        ("price",      "dans_un_mois"): "Nurturing : 3 emails ROI sur 10 jours",
        ("price",      "indéfini"):     "Relance J+7 avec témoignage client similaire",
        ("trust",      "immédiat"):     "Envoyer 3 études de cas + certifications",
        ("trust",      "sous_48h"):     "Proposer démo gratuite 30 min",
        ("trust",      "cette_semaine"):"Envoyer portfolio + appel référence client",
        ("trust",      "dans_un_mois"): "Séquence nurturing confiance (5 emails)",
        ("trust",      "indéfini"):     "Agent 3.2 : email garantie satisfait ou remboursé",
        ("timing",     "immédiat"):     "Demander date exacte et bloquer agenda",
        ("timing",     "sous_48h"):     "Envoyer rappel et proposition calendrier",
        ("timing",     "cette_semaine"):"Proposer appel découverte flexible",
        ("timing",     "dans_un_mois"): "Email de nurturing mensuel",
        ("timing",     "indéfini"):     "Relance automatique dans 30 jours",
        ("competitor", "immédiat"):     "Envoyer comparatif concurrentiel + avantages uniques",
        ("competitor", "sous_48h"):     "Agent 3.1 : présentation différenciation",
        ("competitor", "cette_semaine"):"Proposer audit gratuit vs solution actuelle",
        ("competitor", "dans_un_mois"): "Nurturing : résultats clients ayant switché",
        ("competitor", "indéfini"):     "Email de benchmark — positionnement marché",
        ("technical",  "immédiat"):     "Planifier onboarding accompagné dès aujourd'hui",
        ("technical",  "sous_48h"):     "Envoyer guide démarrage rapide + FAQ",
        ("technical",  "cette_semaine"):"Proposer démo personnalisée avec technicien",
        ("technical",  "dans_un_mois"): "Email formation + vidéo tutoriel",
        ("technical",  "indéfini"):     "Séquence éducative 3 emails",
        ("none",       "immédiat"):     "Appel de closing immédiat — prospect chaud",
        ("none",       "sous_48h"):     "Envoi contrat et lien de paiement",
        ("none",       "cette_semaine"):"Proposition de rendez-vous signature",
        ("none",       "dans_un_mois"): "Email récapitulatif offre + deadline",
        ("none",       "indéfini"):     "Relance J+4 — Agent 3.5",
    }

    def classify(self, text: str) -> ClassificationResult:
        if not text or not text.strip():
            return ClassificationResult(
                objection_type="none",
                timeline="indéfini",
                buying_signal=0.0,
                competitor_mentioned=False,
                next_action="Relance J+4 — Agent 3.7 (ghost)",
                priority="low",
            )

        t = text.lower()

        objection_type, objection_kws = self._detect_objection(t)
        timeline = self._detect_timeline(t)
        buying_signal, buying_kws = self._detect_buying_signal(t)
        competitor = self._detect_competitor(t)

        priority = self._compute_priority(buying_signal, timeline, objection_type)
        next_action = self._NEXT_ACTIONS.get(
            (objection_type, timeline),
            self._NEXT_ACTIONS.get(("none", "indéfini"), "Relance J+4"),
        )

        return ClassificationResult(
            objection_type=objection_type,
            timeline=timeline,
            buying_signal=buying_signal,
            competitor_mentioned=competitor,
            objection_keywords=objection_kws,
            buying_keywords=buying_kws,
            next_action=next_action,
            priority=priority,
        )

    def classify_batch(self, texts: List[str]) -> List[ClassificationResult]:
        return [self.classify(t) for t in texts]

    # ── Internal ──────────────────────────────────────────────────────────────

    def _detect_objection(self, text: str):
        checks = [
            ("trust",      _TRUST_OBJECTIONS),
            ("price",      _PRICE_OBJECTIONS),
            ("competitor", _COMPETITOR_SIGNALS),
            ("technical",  _TECHNICAL_OBJECTIONS),
            ("timing",     _TIMING_OBJECTIONS),
        ]
        best_type = "none"
        best_kws: List[str] = []
        for obj_type, kw_list in checks:
            matched = [kw for kw in kw_list if kw in text]
            if len(matched) > len(best_kws):
                best_type = obj_type
                best_kws = matched
        return best_type, best_kws

    def _detect_timeline(self, text: str) -> str:
        for kw in _IMMEDIATE_TIMELINE:
            if kw in text:
                return "immédiat"
        for kw in _SHORT_TIMELINE:
            if kw in text:
                return "sous_48h"
        for kw in _MEDIUM_TIMELINE:
            if kw in text:
                return "cette_semaine"
        for kw in _LONG_TIMELINE:
            if kw in text:
                return "dans_un_mois"
        return "indéfini"

    def _detect_buying_signal(self, text: str):
        matched = [kw for kw in _BUYING_SIGNALS if kw in text]
        score = min(1.0, len(matched) * 0.25)
        return score, matched

    def _detect_competitor(self, text: str) -> bool:
        return any(kw in text for kw in _COMPETITOR_SIGNALS)

    def _compute_priority(self, buying_signal: float, timeline: str, objection_type: str) -> str:
        if timeline == "immédiat" and buying_signal >= 0.5:
            return "urgent"
        if buying_signal >= 0.5 or timeline in ("immédiat", "sous_48h"):
            return "high"
        if objection_type == "trust" or timeline == "cette_semaine":
            return "normal"
        return "low"
