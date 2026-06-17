"""
Objection Handler — maps prospect objection types to rebuttal strategies,
selects the best rebuttal based on outcome history, and tracks effectiveness.

Pairs with ReplyClassifier: once an objection type is detected, feed it
here to get the recommended rebuttal template and talking points.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


# ── Objection taxonomy ────────────────────────────────────────────────────────

class ObjectionType(str, Enum):
    PRICE       = "price"        # "C'est trop cher"
    TIMING      = "timing"       # "Pas maintenant, rappelez-moi"
    COMPETITOR  = "competitor"   # "On travaille déjà avec quelqu'un"
    TRUST       = "trust"        # "Je ne vous connais pas"
    RELEVANCE   = "relevance"    # "Ça ne s'applique pas à nous"
    AUTHORITY   = "authority"    # "Je ne suis pas décideur"
    SATISFIED   = "satisfied"    # "Notre site marche très bien"
    NO_BUDGET   = "no_budget"    # "On n'a pas de budget"
    TOO_BUSY    = "too_busy"     # "Je n'ai pas le temps"
    UNKNOWN     = "unknown"


class RebuttalOutcome(str, Enum):
    CONVERTED    = "converted"    # prospect signed
    POSITIVE     = "positive"     # prospect showed interest / asked for more
    NEUTRAL      = "neutral"      # no change
    NEGATIVE     = "negative"     # prospect pushed back harder
    UNSUBSCRIBED = "unsubscribed" # prospect opted out


# ── Rebuttal definition ───────────────────────────────────────────────────────

@dataclass
class Rebuttal:
    rebuttal_id:   str
    objection:     ObjectionType
    name:          str
    template_id:   str         # email template key to render
    talking_points: List[str]
    urgency_angle: bool = False  # does this rebuttal use urgency framing?
    social_proof:  bool = False  # does this rebuttal use social proof?

    def to_dict(self) -> dict:
        return {
            "rebuttal_id":    self.rebuttal_id,
            "objection":      self.objection.value,
            "name":           self.name,
            "template_id":    self.template_id,
            "talking_points": self.talking_points,
            "urgency_angle":  self.urgency_angle,
            "social_proof":   self.social_proof,
        }


# ── Outcome record ────────────────────────────────────────────────────────────

@dataclass
class OutcomeRecord:
    rebuttal_id:  str
    prospect_id:  str
    objection:    ObjectionType
    outcome:      RebuttalOutcome
    sector:       str = ""
    notes:        str = ""

    def to_dict(self) -> dict:
        return {
            "rebuttal_id": self.rebuttal_id,
            "prospect_id": self.prospect_id,
            "objection":   self.objection.value,
            "outcome":     self.outcome.value,
            "sector":      self.sector,
            "notes":       self.notes,
        }


# ── Built-in rebuttal catalogue ───────────────────────────────────────────────

_REBUTTALS: List[Rebuttal] = [
    # ── PRICE ────────────────────────────────────────────────────────────────
    Rebuttal(
        rebuttal_id="price_roi",
        objection=ObjectionType.PRICE,
        name="ROI concret",
        template_id="rebuttal_price_roi",
        talking_points=[
            "Un site lent perd en moyenne 7% de revenus par seconde de chargement supplémentaire.",
            "Nos clients récupèrent l'investissement en 2 à 4 mois grâce à l'augmentation du trafic organique.",
            "On vous propose un audit gratuit pour chiffrer l'impact précis sur votre activité.",
        ],
        urgency_angle=False,
        social_proof=True,
    ),
    Rebuttal(
        rebuttal_id="price_payment_plan",
        objection=ObjectionType.PRICE,
        name="Paiement échelonné",
        template_id="rebuttal_price_payment",
        talking_points=[
            "Nous proposons un paiement en 3 fois sans frais.",
            "Le premier versement démarre seulement après la livraison des premiers résultats.",
            "Calculez vous-même : pour le prix d'un repas d'affaires par semaine, votre site est optimisé.",
        ],
        urgency_angle=False,
        social_proof=False,
    ),
    Rebuttal(
        rebuttal_id="price_competitor_compare",
        objection=ObjectionType.PRICE,
        name="Comparaison marché",
        template_id="rebuttal_price_compare",
        talking_points=[
            "Une agence web classique facture 3 000 à 10 000 € pour le même travail.",
            "Notre approche automatisée nous permet de livrer en 5 jours au lieu de 3 mois.",
            "Vous pouvez comparer ligne par ligne nos livrables avec nos concurrents.",
        ],
        urgency_angle=True,
        social_proof=False,
    ),
    # ── TIMING ───────────────────────────────────────────────────────────────
    Rebuttal(
        rebuttal_id="timing_now_or_never",
        objection=ObjectionType.TIMING,
        name="Coût du délai",
        template_id="rebuttal_timing_cost",
        talking_points=[
            "Chaque mois de retard est un mois où vos concurrents captent les clients que Google vous refuse.",
            "Votre score PageSpeed de {pagespeed}/100 vous fait perdre des positions chaque semaine.",
            "Il faut 3 à 6 mois pour qu'une optimisation SEO porte ses fruits — chaque jour compte.",
        ],
        urgency_angle=True,
        social_proof=False,
    ),
    Rebuttal(
        rebuttal_id="timing_low_effort",
        objection=ObjectionType.TIMING,
        name="Effort minimal de votre côté",
        template_id="rebuttal_timing_effort",
        talking_points=[
            "Nous gérons tout de A à Z — vous n'avez besoin que de 30 minutes pour le brief initial.",
            "Pas de réunions interminables : livraison clé en main en 5 jours ouvrés.",
            "On peut démarrer cette semaine et vous montrer les premiers résultats avant la fin du mois.",
        ],
        urgency_angle=False,
        social_proof=False,
    ),
    # ── COMPETITOR ───────────────────────────────────────────────────────────
    Rebuttal(
        rebuttal_id="competitor_differentiation",
        objection=ObjectionType.COMPETITOR,
        name="Différenciation claire",
        template_id="rebuttal_competitor_diff",
        talking_points=[
            "Votre prestataire actuel vous a-t-il fourni un rapport PageSpeed avec un score avant/après ?",
            "Nous intervenons en complément ou en remplacement — un audit gratuit vous montrera ce qui manque.",
            "Beaucoup de nos clients avaient déjà une agence web. On leur apporte ce que l'agence ne fait pas.",
        ],
        urgency_angle=False,
        social_proof=True,
    ),
    # ── TRUST ────────────────────────────────────────────────────────────────
    Rebuttal(
        rebuttal_id="trust_social_proof",
        objection=ObjectionType.TRUST,
        name="Preuve sociale",
        template_id="rebuttal_trust_proof",
        talking_points=[
            "Voici 3 exemples de sites dans votre secteur que nous avons améliorés ce trimestre.",
            "Nous offrons une garantie satisfait ou remboursé sur les 30 premiers jours.",
            "Je vous mets en relation avec un client de votre secteur qui peut témoigner directement.",
        ],
        urgency_angle=False,
        social_proof=True,
    ),
    Rebuttal(
        rebuttal_id="trust_free_audit",
        objection=ObjectionType.TRUST,
        name="Audit gratuit sans engagement",
        template_id="rebuttal_trust_audit",
        talking_points=[
            "Aucun engagement : nous vous livrons un audit complet de votre site, gratuitement.",
            "Vous jugez sur pièces avant de décider — aucune carte bancaire requise.",
            "Si l'audit ne révèle rien d'utile, vous ne nous devez rien.",
        ],
        urgency_angle=False,
        social_proof=False,
    ),
    # ── RELEVANCE ────────────────────────────────────────────────────────────
    Rebuttal(
        rebuttal_id="relevance_sector_data",
        objection=ObjectionType.RELEVANCE,
        name="Données sectorielles",
        template_id="rebuttal_relevance_sector",
        talking_points=[
            "Dans le secteur {sector}, 73% des prospects cherchent en ligne avant d'appeler.",
            "Vos concurrents directs ont un score PageSpeed supérieur de {delta} points au vôtre.",
            "Les entreprises {sector} avec un site rapide génèrent 2,4× plus de leads organiques.",
        ],
        urgency_angle=False,
        social_proof=True,
    ),
    # ── AUTHORITY ────────────────────────────────────────────────────────────
    Rebuttal(
        rebuttal_id="authority_decision_kit",
        objection=ObjectionType.AUTHORITY,
        name="Kit de décision",
        template_id="rebuttal_authority_kit",
        talking_points=[
            "Pas de problème — je vous prépare un dossier synthétique à présenter à votre direction.",
            "Le document inclut : ROI projeté, comparatif concurrents, planning et conditions.",
            "Quel est le meilleur moment pour une démo de 20 minutes avec le décideur ?",
        ],
        urgency_angle=False,
        social_proof=False,
    ),
    # ── SATISFIED ────────────────────────────────────────────────────────────
    Rebuttal(
        rebuttal_id="satisfied_benchmark",
        objection=ObjectionType.SATISFIED,
        name="Benchmark objectif",
        template_id="rebuttal_satisfied_bench",
        talking_points=[
            "C'est super ! Pour confirmer, votre score Google PageSpeed est de {pagespeed}/100.",
            "Un score < 70 coûte en moyenne 15% de trafic organique — laissez-nous vérifier ensemble.",
            "On vous offre un benchmark gratuit face à vos 3 principaux concurrents.",
        ],
        urgency_angle=False,
        social_proof=False,
    ),
    # ── NO_BUDGET ────────────────────────────────────────────────────────────
    Rebuttal(
        rebuttal_id="no_budget_starter",
        objection=ObjectionType.NO_BUDGET,
        name="Offre d'entrée accessible",
        template_id="rebuttal_no_budget_starter",
        talking_points=[
            "Notre pack Starter à 99€ HT couvre les corrections PageSpeed et mobile les plus impactantes.",
            "Un investissement de 99€ pour récupérer 15% de trafic perdu — c'est rentable dès le 1er mois.",
            "On peut aussi vous proposer un audit seul à prix symbolique pour commencer.",
        ],
        urgency_angle=False,
        social_proof=False,
    ),
    # ── TOO_BUSY ─────────────────────────────────────────────────────────────
    Rebuttal(
        rebuttal_id="too_busy_autonomous",
        objection=ObjectionType.TOO_BUSY,
        name="Processus 100% autonome",
        template_id="rebuttal_too_busy",
        talking_points=[
            "Notre process est conçu pour les dirigeants occupés : 1 brief de 30 min, puis on prend tout en main.",
            "Vous recevrez un rapport d'avancement chaque vendredi — rien d'autre de votre côté.",
            "On peut planifier ce brief au créneau qui vous convient, même tôt le matin ou en pause déjeuner.",
        ],
        urgency_angle=False,
        social_proof=False,
    ),
    # ── UNKNOWN ──────────────────────────────────────────────────────────────
    Rebuttal(
        rebuttal_id="unknown_open_question",
        objection=ObjectionType.UNKNOWN,
        name="Question ouverte",
        template_id="rebuttal_unknown_question",
        talking_points=[
            "Je comprends votre hésitation. Qu'est-ce qui vous ferait changer d'avis ?",
            "Quelle serait la condition pour que vous considériez de travailler avec nous ?",
            "Y a-t-il une information supplémentaire que je peux vous apporter ?",
        ],
        urgency_angle=False,
        social_proof=False,
    ),
]

_REBUTTAL_INDEX: Dict[str, Rebuttal] = {r.rebuttal_id: r for r in _REBUTTALS}
_BY_OBJECTION: Dict[ObjectionType, List[Rebuttal]] = {}
for _r in _REBUTTALS:
    _BY_OBJECTION.setdefault(_r.objection, []).append(_r)


# ── Objection Handler ─────────────────────────────────────────────────────────

class ObjectionHandler:
    """
    Selects the best rebuttal for a given objection type.

    Selection strategy:
    - Default: pick the rebuttal with the highest positive outcome rate
      among past records for the same objection + sector combination.
    - If no history exists: pick the rebuttal with the highest global
      positive rate, falling back to random choice.

    Usage::
        handler = ObjectionHandler()
        rebuttal = handler.recommend("price", sector="restaurant")
        handler.record_outcome(rebuttal.rebuttal_id, "p001", "price", "positive", sector="restaurant")
    """

    def __init__(self) -> None:
        self._outcomes: List[OutcomeRecord] = []

    # ── Catalogue access ──────────────────────────────────────────────────────

    def get_rebuttal(self, rebuttal_id: str) -> Optional[Rebuttal]:
        return _REBUTTAL_INDEX.get(rebuttal_id)

    def rebuttals_for(self, objection: ObjectionType) -> List[Rebuttal]:
        return list(_BY_OBJECTION.get(objection, []))

    def all_rebuttals(self) -> List[Rebuttal]:
        return list(_REBUTTALS)

    # ── Recommendation engine ─────────────────────────────────────────────────

    def recommend(
        self,
        objection: str | ObjectionType,
        sector: str = "",
        exclude_ids: Optional[List[str]] = None,
    ) -> Optional[Rebuttal]:
        """Return the best rebuttal for the given objection type."""
        try:
            obj_type = ObjectionType(objection) if isinstance(objection, str) else objection
        except ValueError:
            obj_type = ObjectionType.UNKNOWN

        candidates = [
            r for r in _BY_OBJECTION.get(obj_type, [])
            if not (exclude_ids and r.rebuttal_id in exclude_ids)
        ]
        if not candidates:
            return None

        scored = self._score_rebuttals(candidates, sector=sector)
        if scored:
            return scored[0][0]
        return candidates[0]

    def recommend_sequence(
        self,
        objection: str | ObjectionType,
        sector: str = "",
    ) -> List[Rebuttal]:
        """Return all rebuttals for the objection, ranked by effectiveness."""
        try:
            obj_type = ObjectionType(objection) if isinstance(objection, str) else objection
        except ValueError:
            obj_type = ObjectionType.UNKNOWN

        candidates = list(_BY_OBJECTION.get(obj_type, []))
        scored = self._score_rebuttals(candidates, sector=sector)
        return [r for r, _ in scored] if scored else candidates

    def _score_rebuttals(
        self,
        candidates: List[Rebuttal],
        sector: str = "",
    ) -> List[Tuple[Rebuttal, float]]:
        """Score each candidate by positive outcome rate (sector-aware)."""
        if not self._outcomes:
            return [(r, 0.0) for r in candidates]

        def win_rate(rebuttal_id: str) -> float:
            sector_outcomes = [
                o for o in self._outcomes
                if o.rebuttal_id == rebuttal_id and (not sector or sector.lower() in o.sector.lower())
            ]
            global_outcomes = [o for o in self._outcomes if o.rebuttal_id == rebuttal_id]
            # Prefer sector-specific, fall back to global
            pool = sector_outcomes if len(sector_outcomes) >= 3 else global_outcomes
            if not pool:
                return 0.0
            wins = sum(
                1 for o in pool
                if o.outcome in (RebuttalOutcome.CONVERTED, RebuttalOutcome.POSITIVE)
            )
            return wins / len(pool)

        scored = [(r, win_rate(r.rebuttal_id)) for r in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    # ── Outcome tracking ──────────────────────────────────────────────────────

    def record_outcome(
        self,
        rebuttal_id: str,
        prospect_id: str,
        objection: str | ObjectionType,
        outcome: str | RebuttalOutcome,
        sector: str = "",
        notes: str = "",
    ) -> OutcomeRecord:
        try:
            obj_type = ObjectionType(objection) if isinstance(objection, str) else objection
        except ValueError:
            obj_type = ObjectionType.UNKNOWN
        try:
            out_type = RebuttalOutcome(outcome) if isinstance(outcome, str) else outcome
        except ValueError:
            out_type = RebuttalOutcome.NEUTRAL

        rec = OutcomeRecord(
            rebuttal_id=rebuttal_id,
            prospect_id=prospect_id,
            objection=obj_type,
            outcome=out_type,
            sector=sector,
            notes=notes,
        )
        self._outcomes.append(rec)
        return rec

    def outcomes_for(self, rebuttal_id: str) -> List[OutcomeRecord]:
        return [o for o in self._outcomes if o.rebuttal_id == rebuttal_id]

    # ── Analytics ─────────────────────────────────────────────────────────────

    def effectiveness_report(self) -> List[dict]:
        """Return win-rate per rebuttal, sorted descending."""
        report = []
        for rebuttal in _REBUTTALS:
            outcomes = self.outcomes_for(rebuttal.rebuttal_id)
            total = len(outcomes)
            if total == 0:
                report.append({
                    "rebuttal_id":  rebuttal.rebuttal_id,
                    "objection":    rebuttal.objection.value,
                    "name":         rebuttal.name,
                    "total":        0,
                    "wins":         0,
                    "win_rate_pct": 0.0,
                })
                continue
            wins = sum(
                1 for o in outcomes
                if o.outcome in (RebuttalOutcome.CONVERTED, RebuttalOutcome.POSITIVE)
            )
            report.append({
                "rebuttal_id":  rebuttal.rebuttal_id,
                "objection":    rebuttal.objection.value,
                "name":         rebuttal.name,
                "total":        total,
                "wins":         wins,
                "win_rate_pct": round(wins / total * 100, 1),
            })
        report.sort(key=lambda x: x["win_rate_pct"], reverse=True)
        return report

    def summary(self) -> dict:
        total   = len(self._outcomes)
        wins    = sum(1 for o in self._outcomes if o.outcome in (RebuttalOutcome.CONVERTED, RebuttalOutcome.POSITIVE))
        by_obj: Dict[str, int] = {}
        by_out: Dict[str, int] = {}
        for o in self._outcomes:
            by_obj[o.objection.value]  = by_obj.get(o.objection.value, 0) + 1
            by_out[o.outcome.value]    = by_out.get(o.outcome.value, 0) + 1

        return {
            "total_outcomes":   total,
            "wins":             wins,
            "win_rate_pct":     round(wins / total * 100, 1) if total else 0.0,
            "by_objection":     by_obj,
            "by_outcome":       by_out,
            "rebuttals_count":  len(_REBUTTALS),
        }

    # ── Reset ─────────────────────────────────────────────────────────────────

    def reset(self) -> None:
        self._outcomes.clear()
