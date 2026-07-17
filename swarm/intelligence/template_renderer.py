"""
Template Renderer — stores email/SMS templates, renders them with variable
substitution, manages A/B subject variants, and tracks render/delivery stats.

Templates reference a template_id (used by OutreachSequencer steps and
ObjectionHandler rebuttal template_id fields).  Variables are injected via
a simple {variable_name} syntax.

Render pipeline:
  1. Look up template by template_id + optional variant key
  2. Substitute variables (raises on missing required variable)
  3. Return RenderedMessage (subject, body_text, body_html, metadata)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


# ── Data models ───────────────────────────────────────────────────────────────

@dataclass
class SubjectVariant:
    variant_key: str     # "A", "B", "C"
    subject:     str

    def to_dict(self) -> dict:
        return {"variant_key": self.variant_key, "subject": self.subject}


@dataclass
class Template:
    template_id:      str
    name:             str
    channel:          str              # "email" | "sms" | "linkedin"
    body_text:        str              # plain-text body (required)
    body_html:        str              # HTML body (may equal body_text for SMS)
    subject_variants: List[SubjectVariant] = field(default_factory=list)
    tags:             List[str]        = field(default_factory=list)
    description:      str             = ""

    # ── Introspection ─────────────────────────────────────────────────────────

    @property
    def required_variables(self) -> Set[str]:
        """Return the set of {variable} placeholders found in all text fields."""
        combined = self.body_text + self.body_html + "".join(v.subject for v in self.subject_variants)
        return set(re.findall(r"\{(\w+)\}", combined))

    def get_subject(self, variant_key: str = "A") -> str:
        for v in self.subject_variants:
            if v.variant_key == variant_key:
                return v.subject
        return self.subject_variants[0].subject if self.subject_variants else ""

    def to_dict(self) -> dict:
        return {
            "template_id":      self.template_id,
            "name":             self.name,
            "channel":          self.channel,
            "description":      self.description,
            "tags":             self.tags,
            "subject_variants": [v.to_dict() for v in self.subject_variants],
            "required_variables": sorted(self.required_variables),
        }


@dataclass
class RenderedMessage:
    template_id:  str
    variant_key:  str
    subject:      str
    body_text:    str
    body_html:    str
    channel:      str
    variables:    Dict[str, str] = field(default_factory=dict)
    missing_vars: List[str]      = field(default_factory=list)

    @property
    def is_complete(self) -> bool:
        return len(self.missing_vars) == 0

    def to_dict(self) -> dict:
        return {
            "template_id":  self.template_id,
            "variant_key":  self.variant_key,
            "subject":      self.subject,
            "body_text":    self.body_text,
            "body_html":    self.body_html,
            "channel":      self.channel,
            "is_complete":  self.is_complete,
            "missing_vars": self.missing_vars,
        }


# ── Render statistics ─────────────────────────────────────────────────────────

@dataclass
class TemplateStats:
    template_id:    str
    renders:        int = 0
    sends:          int = 0
    opens:          int = 0
    clicks:         int = 0
    replies:        int = 0

    @property
    def open_rate(self) -> float:
        return self.opens / self.sends if self.sends else 0.0

    @property
    def click_rate(self) -> float:
        return self.clicks / self.sends if self.sends else 0.0

    @property
    def reply_rate(self) -> float:
        return self.replies / self.sends if self.sends else 0.0

    def to_dict(self) -> dict:
        return {
            "template_id":   self.template_id,
            "renders":       self.renders,
            "sends":         self.sends,
            "opens":         self.opens,
            "clicks":        self.clicks,
            "replies":       self.replies,
            "open_rate_pct":  round(self.open_rate  * 100, 1),
            "click_rate_pct": round(self.click_rate * 100, 1),
            "reply_rate_pct": round(self.reply_rate * 100, 1),
        }


# ── Built-in template catalogue ───────────────────────────────────────────────

_BUILTIN_TEMPLATES: List[Template] = [
    # ── Cold outreach ─────────────────────────────────────────────────────────
    Template(
        template_id="intro_value",
        name="Introduction valeur",
        channel="email",
        description="Premier contact — présentation de la valeur",
        tags=["cold", "intro"],
        subject_variants=[
            SubjectVariant("A", "Votre site {company_name} perd du trafic chaque jour"),
            SubjectVariant("B", "J'ai analysé le site de {company_name}"),
            SubjectVariant("C", "Score PageSpeed : {pagespeed}/100 — on peut faire mieux"),
        ],
        body_text=(
            "Bonjour {contact_name},\n\n"
            "En analysant les sites dans le secteur {sector}, j'ai remarqué que {company_name} "
            "obtient un score PageSpeed de {pagespeed}/100 — ce qui représente une perte "
            "estimée de {revenue_loss}€/mois en trafic organique non capté.\n\n"
            "En 5 jours ouvrés, nous pouvons corriger les points critiques et améliorer "
            "votre positionnement Google.\n\n"
            "Avez-vous 15 minutes cette semaine pour en discuter ?\n\n"
            "Cordialement,\n{agent_name}"
        ),
        body_html=(
            "<p>Bonjour <strong>{contact_name}</strong>,</p>"
            "<p>En analysant les sites dans le secteur <em>{sector}</em>, j'ai remarqué que "
            "<strong>{company_name}</strong> obtient un score PageSpeed de "
            "<strong>{pagespeed}/100</strong> — ce qui représente une perte estimée de "
            "<strong>{revenue_loss}€/mois</strong> en trafic organique non capté.</p>"
            "<p>En 5 jours ouvrés, nous pouvons corriger les points critiques et améliorer "
            "votre positionnement Google.</p>"
            "<p>Avez-vous 15 minutes cette semaine pour en discuter ?</p>"
            "<p>Cordialement,<br><strong>{agent_name}</strong></p>"
        ),
    ),
    Template(
        template_id="follow_up_1",
        name="Relance 1",
        channel="email",
        description="Première relance après intro sans réponse",
        tags=["cold", "followup"],
        subject_variants=[
            SubjectVariant("A", "Re: {company_name} — avez-vous vu mon message ?"),
            SubjectVariant("B", "Une question rapide sur votre site"),
            SubjectVariant("C", "Votre concurrent a déjà agi — et vous ?"),
        ],
        body_text=(
            "Bonjour {contact_name},\n\n"
            "Je me permets de revenir vers vous concernant {company_name}.\n\n"
            "Un concurrent dans votre secteur vient d'améliorer son score de 18 points "
            "et capte désormais les recherches que vous manquez.\n\n"
            "Voulez-vous que je vous envoie l'analyse comparative gratuitement ?\n\n"
            "Bonne journée,\n{agent_name}"
        ),
        body_html=(
            "<p>Bonjour <strong>{contact_name}</strong>,</p>"
            "<p>Je me permets de revenir vers vous concernant <strong>{company_name}</strong>.</p>"
            "<p>Un concurrent dans votre secteur vient d'améliorer son score de 18 points "
            "et capte désormais les recherches que vous manquez.</p>"
            "<p>Voulez-vous que je vous envoie l'analyse comparative gratuitement ?</p>"
            "<p>Bonne journée,<br><strong>{agent_name}</strong></p>"
        ),
    ),
    Template(
        template_id="social_proof",
        name="Preuve sociale",
        channel="email",
        description="Troisième touch — cas client similaire",
        tags=["cold", "social_proof"],
        subject_variants=[
            SubjectVariant("A", "Comment {case_company} a gagné +{case_traffic}% de trafic en 30 jours"),
        ],
        body_text=(
            "Bonjour {contact_name},\n\n"
            "{case_company}, actif dans le secteur {sector} comme vous, "
            "a vu son trafic organique augmenter de {case_traffic}% en 30 jours "
            "après optimisation PageSpeed et mobile.\n\n"
            "Résultat : +{case_leads} leads supplémentaires par mois.\n\n"
            "Je serais ravi de vous préparer une projection similaire pour {company_name}.\n\n"
            "Cordialement,\n{agent_name}"
        ),
        body_html=(
            "<p>Bonjour <strong>{contact_name}</strong>,</p>"
            "<p><strong>{case_company}</strong>, actif dans le secteur <em>{sector}</em> comme vous, "
            "a vu son trafic organique augmenter de <strong>{case_traffic}%</strong> en 30 jours "
            "après optimisation PageSpeed et mobile.</p>"
            "<p>Résultat : <strong>+{case_leads} leads supplémentaires</strong> par mois.</p>"
            "<p>Je serais ravi de vous préparer une projection similaire pour <strong>{company_name}</strong>.</p>"
            "<p>Cordialement,<br><strong>{agent_name}</strong></p>"
        ),
    ),
    Template(
        template_id="urgency_close",
        name="Clôture urgence",
        channel="email",
        description="Avant-dernière relance avec angle urgence",
        tags=["cold", "urgency"],
        subject_variants=[
            SubjectVariant("A", "Dernière chance : offre limitée pour {company_name}"),
            SubjectVariant("C", "Je ferme votre dossier vendredi — un mot avant ?"),
        ],
        body_text=(
            "Bonjour {contact_name},\n\n"
            "Je m'apprête à clore le dossier {company_name} cette semaine.\n\n"
            "Avant cela, je voulais vous signaler que l'offre tarifaire que je vous avais "
            "préparée expire vendredi. Après cette date, les délais de livraison seront "
            "allongés à 3 semaines.\n\n"
            "Un simple 'oui' ou 'non' me suffit.\n\n"
            "{agent_name}"
        ),
        body_html=(
            "<p>Bonjour <strong>{contact_name}</strong>,</p>"
            "<p>Je m'apprête à clore le dossier <strong>{company_name}</strong> cette semaine.</p>"
            "<p>Avant cela, je voulais vous signaler que l'offre tarifaire que je vous avais "
            "préparée expire <strong>vendredi</strong>. Après cette date, les délais de livraison "
            "seront allongés à 3 semaines.</p>"
            "<p>Un simple 'oui' ou 'non' me suffit.</p>"
            "<p><strong>{agent_name}</strong></p>"
        ),
    ),
    Template(
        template_id="breakup",
        name="Breakup email",
        channel="email",
        description="Dernier message — fermeture du dossier",
        tags=["cold", "breakup"],
        subject_variants=[
            SubjectVariant("A", "Je ferme votre dossier"),
        ],
        body_text=(
            "Bonjour {contact_name},\n\n"
            "N'ayant pas eu de retour de votre part, je ferme votre dossier.\n\n"
            "Si votre situation évolue et que vous souhaitez optimiser votre présence en ligne, "
            "n'hésitez pas à me contacter.\n\n"
            "Bonne continuation,\n{agent_name}"
        ),
        body_html=(
            "<p>Bonjour <strong>{contact_name}</strong>,</p>"
            "<p>N'ayant pas eu de retour de votre part, je ferme votre dossier.</p>"
            "<p>Si votre situation évolue et que vous souhaitez optimiser votre présence en ligne, "
            "n'hésitez pas à me contacter.</p>"
            "<p>Bonne continuation,<br><strong>{agent_name}</strong></p>"
        ),
    ),
    # ── Warm / reactivation ───────────────────────────────────────────────────
    Template(
        template_id="warm_check_in",
        name="Check-in prospect chaud",
        channel="email",
        description="Réactivation d'un prospect ayant déjà interagi",
        tags=["warm", "reactivation"],
        subject_variants=[
            SubjectVariant("A", "Vous aviez ouvert mon email sur {company_name} — une question"),
        ],
        body_text=(
            "Bonjour {contact_name},\n\n"
            "Vous aviez regardé notre analyse de {company_name} il y a quelques semaines.\n\n"
            "Depuis, avez-vous eu l'occasion de regarder votre score PageSpeed ?\n\n"
            "Je serais heureux de vous montrer ce qui a changé dans votre secteur "
            "depuis notre dernier contact.\n\n"
            "{agent_name}"
        ),
        body_html=(
            "<p>Bonjour <strong>{contact_name}</strong>,</p>"
            "<p>Vous aviez regardé notre analyse de <strong>{company_name}</strong> il y a quelques semaines.</p>"
            "<p>Depuis, avez-vous eu l'occasion de regarder votre score PageSpeed ?</p>"
            "<p>Je serais heureux de vous montrer ce qui a changé dans votre secteur "
            "depuis notre dernier contact.</p>"
            "<p><strong>{agent_name}</strong></p>"
        ),
    ),
    Template(
        template_id="case_study",
        name="Cas client",
        channel="email",
        description="Étude de cas sectorielle pour prospects chauds",
        tags=["warm", "social_proof"],
        subject_variants=[
            SubjectVariant("B", "Étude de cas : {case_company} dans votre secteur"),
        ],
        body_text=(
            "Bonjour {contact_name},\n\n"
            "Voici l'étude de cas que je vous avais promise :\n\n"
            "{case_company} ({sector}) — résultats à 30 jours :\n"
            "• PageSpeed : +{case_pagespeed_gain} points\n"
            "• Trafic organique : +{case_traffic}%\n"
            "• Leads entrants : +{case_leads}/mois\n\n"
            "Est-ce que ces résultats vous semblent pertinents pour {company_name} ?\n\n"
            "{agent_name}"
        ),
        body_html=(
            "<p>Bonjour <strong>{contact_name}</strong>,</p>"
            "<p>Voici l'étude de cas que je vous avais promise :</p>"
            "<p><strong>{case_company}</strong> ({sector}) — résultats à 30 jours :</p>"
            "<ul>"
            "<li>PageSpeed : <strong>+{case_pagespeed_gain} points</strong></li>"
            "<li>Trafic organique : <strong>+{case_traffic}%</strong></li>"
            "<li>Leads entrants : <strong>+{case_leads}/mois</strong></li>"
            "</ul>"
            "<p>Est-ce que ces résultats vous semblent pertinents pour <strong>{company_name}</strong> ?</p>"
            "<p><strong>{agent_name}</strong></p>"
        ),
    ),
    Template(
        template_id="demo_offer",
        name="Offre de démo",
        channel="email",
        description="Proposition de démo personnalisée",
        tags=["warm", "demo"],
        subject_variants=[
            SubjectVariant("A", "Démo personnalisée pour {company_name} — 20 minutes"),
        ],
        body_text=(
            "Bonjour {contact_name},\n\n"
            "Je vous propose une démo personnalisée de 20 minutes pour {company_name}.\n\n"
            "Au programme :\n"
            "• Audit live de votre site\n"
            "• Comparaison avec 3 concurrents\n"
            "• Plan d'action chiffré\n\n"
            "Quel créneau vous conviendrait cette semaine ou la suivante ?\n\n"
            "{agent_name}"
        ),
        body_html=(
            "<p>Bonjour <strong>{contact_name}</strong>,</p>"
            "<p>Je vous propose une démo personnalisée de 20 minutes pour <strong>{company_name}</strong>.</p>"
            "<p>Au programme :</p>"
            "<ul><li>Audit live de votre site</li>"
            "<li>Comparaison avec 3 concurrents</li>"
            "<li>Plan d'action chiffré</li></ul>"
            "<p>Quel créneau vous conviendrait cette semaine ou la suivante ?</p>"
            "<p><strong>{agent_name}</strong></p>"
        ),
    ),
    # ── Post-quote ────────────────────────────────────────────────────────────
    Template(
        template_id="quote_reminder",
        name="Rappel devis",
        channel="email",
        description="Relance après envoi du devis",
        tags=["post_quote"],
        subject_variants=[
            SubjectVariant("A", "Votre devis {company_name} — avez-vous des questions ?"),
        ],
        body_text=(
            "Bonjour {contact_name},\n\n"
            "Je reviens vers vous au sujet du devis envoyé pour {company_name} "
            "({quote_total}€ TTC).\n\n"
            "Avez-vous eu le temps d'en prendre connaissance ? "
            "Je suis disponible pour répondre à toute question.\n\n"
            "{agent_name}"
        ),
        body_html=(
            "<p>Bonjour <strong>{contact_name}</strong>,</p>"
            "<p>Je reviens vers vous au sujet du devis envoyé pour <strong>{company_name}</strong> "
            "(<strong>{quote_total}€ TTC</strong>).</p>"
            "<p>Avez-vous eu le temps d'en prendre connaissance ? "
            "Je suis disponible pour répondre à toute question.</p>"
            "<p><strong>{agent_name}</strong></p>"
        ),
    ),
    Template(
        template_id="objection_faq",
        name="FAQ objections",
        channel="email",
        description="Réponse aux objections courantes post-devis",
        tags=["post_quote", "objection"],
        subject_variants=[
            SubjectVariant("A", "Questions fréquentes sur notre intervention chez {company_name}"),
        ],
        body_text=(
            "Bonjour {contact_name},\n\n"
            "Voici les 3 questions les plus fréquentes à ce stade :\n\n"
            "1. Combien de temps ça prend ? → 5 jours ouvrés, sans intervention de votre côté.\n"
            "2. Y a-t-il une garantie ? → Oui, satisfait ou remboursé 30 jours.\n"
            "3. Que se passe-t-il si on n'est pas content ? → On corrige jusqu'à satisfaction.\n\n"
            "Une autre question ?\n\n"
            "{agent_name}"
        ),
        body_html=(
            "<p>Bonjour <strong>{contact_name}</strong>,</p>"
            "<p>Voici les 3 questions les plus fréquentes à ce stade :</p>"
            "<ol>"
            "<li><strong>Combien de temps ça prend ?</strong> → 5 jours ouvrés, sans intervention de votre côté.</li>"
            "<li><strong>Y a-t-il une garantie ?</strong> → Oui, satisfait ou remboursé 30 jours.</li>"
            "<li><strong>Que se passe-t-il si on n'est pas content ?</strong> → On corrige jusqu'à satisfaction.</li>"
            "</ol>"
            "<p>Une autre question ?</p>"
            "<p><strong>{agent_name}</strong></p>"
        ),
    ),
    Template(
        template_id="final_offer",
        name="Offre finale",
        channel="email",
        description="Dernière opportunité avant fermeture du devis",
        tags=["post_quote", "urgency"],
        subject_variants=[
            SubjectVariant("B", "Votre devis {company_name} expire dans 48h"),
        ],
        body_text=(
            "Bonjour {contact_name},\n\n"
            "Votre devis pour {company_name} ({quote_total}€ TTC) expire dans 48 heures.\n\n"
            "Passé ce délai, je ne pourrai plus garantir le planning ni le tarif actuel.\n\n"
            "Si vous souhaitez aller de l'avant, répondez simplement 'OK' à cet email.\n\n"
            "{agent_name}"
        ),
        body_html=(
            "<p>Bonjour <strong>{contact_name}</strong>,</p>"
            "<p>Votre devis pour <strong>{company_name}</strong> (<strong>{quote_total}€ TTC</strong>) "
            "expire dans <strong>48 heures</strong>.</p>"
            "<p>Passé ce délai, je ne pourrai plus garantir le planning ni le tarif actuel.</p>"
            "<p>Si vous souhaitez aller de l'avant, répondez simplement <strong>'OK'</strong> à cet email.</p>"
            "<p><strong>{agent_name}</strong></p>"
        ),
    ),
]


# ── Template Renderer ─────────────────────────────────────────────────────────

class TemplateRenderer:
    """
    Renders email/SMS templates with variable substitution.

    Usage::
        renderer = TemplateRenderer()
        msg = renderer.render("intro_value", variables={
            "contact_name": "M. Dupont",
            "company_name": "Plomberie Martin",
            "sector": "artisan",
            "pagespeed": "28",
            "revenue_loss": "320",
            "agent_name": "Sophie",
        }, variant_key="A")
        print(msg.subject, msg.body_text)
    """

    def __init__(self) -> None:
        self._templates: Dict[str, Template] = {t.template_id: t for t in _BUILTIN_TEMPLATES}
        self._stats: Dict[str, TemplateStats] = {}

    # ── Template registry ─────────────────────────────────────────────────────

    def register(self, template: Template) -> None:
        self._templates[template.template_id] = template

    def get(self, template_id: str) -> Optional[Template]:
        return self._templates.get(template_id)

    def list_templates(self, tag: Optional[str] = None) -> List[Template]:
        templates = list(self._templates.values())
        if tag:
            templates = [t for t in templates if tag in t.tags]
        return templates

    # ── Rendering ─────────────────────────────────────────────────────────────

    def render(
        self,
        template_id: str,
        variables: Optional[Dict[str, str]] = None,
        variant_key: str = "A",
        strict: bool = False,
    ) -> RenderedMessage:
        """
        Render a template with variable substitution.

        If strict=True, raise ValueError on missing required variables.
        Otherwise, leave {variable} placeholders in place and list them
        in RenderedMessage.missing_vars.
        """
        tmpl = self._templates.get(template_id)
        if not tmpl:
            raise KeyError(f"Unknown template: {template_id!r}")

        vars_: Dict[str, str] = variables or {}
        subject  = self._substitute(tmpl.get_subject(variant_key), vars_)
        body_txt = self._substitute(tmpl.body_text, vars_)
        body_html= self._substitute(tmpl.body_html, vars_)

        missing = sorted(
            {v for v in tmpl.required_variables if v not in vars_}
        )
        if strict and missing:
            raise ValueError(f"Missing variables for {template_id!r}: {missing}")

        self._get_stats(template_id).renders += 1

        return RenderedMessage(
            template_id=template_id,
            variant_key=variant_key,
            subject=subject,
            body_text=body_txt,
            body_html=body_html,
            channel=tmpl.channel,
            variables=dict(vars_),
            missing_vars=missing,
        )

    @staticmethod
    def _substitute(text: str, variables: Dict[str, str]) -> str:
        def replacer(match: re.Match) -> str:
            key = match.group(1)
            return variables.get(key, match.group(0))
        return re.sub(r"\{(\w+)\}", replacer, text)

    # ── Stats tracking ────────────────────────────────────────────────────────

    def _get_stats(self, template_id: str) -> TemplateStats:
        if template_id not in self._stats:
            self._stats[template_id] = TemplateStats(template_id=template_id)
        return self._stats[template_id]

    def record_send(self, template_id: str) -> None:
        self._get_stats(template_id).sends += 1

    def record_open(self, template_id: str) -> None:
        self._get_stats(template_id).opens += 1

    def record_click(self, template_id: str) -> None:
        self._get_stats(template_id).clicks += 1

    def record_reply(self, template_id: str) -> None:
        self._get_stats(template_id).replies += 1

    def get_stats(self, template_id: str) -> TemplateStats:
        return self._get_stats(template_id)

    def all_stats(self) -> List[TemplateStats]:
        return list(self._stats.values())

    def top_by_open_rate(self, n: int = 5) -> List[TemplateStats]:
        with_sends = [s for s in self._stats.values() if s.sends > 0]
        return sorted(with_sends, key=lambda s: s.open_rate, reverse=True)[:n]

    # ── Summary ───────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        total_renders = sum(s.renders for s in self._stats.values())
        total_sends   = sum(s.sends   for s in self._stats.values())
        total_opens   = sum(s.opens   for s in self._stats.values())
        total_clicks  = sum(s.clicks  for s in self._stats.values())
        return {
            "templates_count": len(self._templates),
            "total_renders":   total_renders,
            "total_sends":     total_sends,
            "total_opens":     total_opens,
            "total_clicks":    total_clicks,
            "open_rate_pct":   round(total_opens  / total_sends * 100, 1) if total_sends else 0.0,
            "click_rate_pct":  round(total_clicks / total_sends * 100, 1) if total_sends else 0.0,
        }

    # ── Reset ─────────────────────────────────────────────────────────────────

    def reset_stats(self) -> None:
        self._stats.clear()

    def reset(self) -> None:
        self._templates = {t.template_id: t for t in _BUILTIN_TEMPLATES}
        self._stats.clear()
