"""
Contact Personalizer — generates personalized outreach angle and message strategy.

Composite personalization score:
  profile_richness(30%) + engagement_signals(25%) + timing_fit(25%) + channel_fit(20%)
  → PersonalizationLevel: DEEP / STRONG / MODERATE / BASIC / GENERIC
  → OutreachChannel: EMAIL / LINKEDIN / PHONE / MULTI
"""

from __future__ import annotations

import math
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple


class PersonalizationLevel(str, Enum):
    DEEP = "deep"
    STRONG = "strong"
    MODERATE = "moderate"
    BASIC = "basic"
    GENERIC = "generic"


class OutreachChannel(str, Enum):
    EMAIL = "email"
    LINKEDIN = "linkedin"
    PHONE = "phone"
    MULTI = "multi"


class TriggerType(str, Enum):
    JOB_CHANGE = "job_change"
    FUNDING = "funding"
    PRODUCT_LAUNCH = "product_launch"
    HIRING = "hiring"
    CONTENT_PUBLISHED = "content_published"
    EVENT_ATTENDED = "event_attended"
    WEBSITE_VISIT = "website_visit"
    EMAIL_OPENED = "email_opened"
    AWARD = "award"
    EXPANSION = "expansion"


_ANGLE_TEMPLATES: Dict[str, str] = {
    "job_change_angle": "Féliciter pour la prise de poste et proposer un accompagnement adapté aux 90 premiers jours",
    "funding_angle": "Capitaliser sur la levée de fonds — aligner la proposition sur les objectifs de croissance accélérée",
    "hiring_angle": "Aborder le défi de scale commercial lié aux recrutements actifs",
    "content_angle": "Rebondir sur le contenu publié pour montrer un alignement de vision",
    "event_angle": "Faire référence à l'événement commun pour créer un point de contact chaud",
    "website_angle": "Timing parfait — le prospect a visité le site récemment",
    "email_opened_angle": "Relance ciblée — le prospect a ouvert un email précédent sans répondre",
    "expertise_angle": "Valider l'expertise sectorielle du prospect et positionner la solution en complémentarité",
    "pain_angle": "Adresser directement le pain point identifié avec une étude de cas similaire",
    "peer_angle": "Mentionner un client concurrent ou pair pour créer un effet social proof",
    "growth_angle": "Aligner la proposition sur les signaux de croissance détectés (expansion, award)",
}

_OPENING_HOOKS: Dict[str, str] = {
    "job_change": "Suite à votre récente prise de poste en tant que {title}…",
    "funding": "Félicitations pour la levée de {amount} — c'est une étape clé…",
    "hiring": "J'ai vu que {company} recrute activement — vous scalez la force commerciale…",
    "content": "Votre post sur {topic} a vraiment résonné — je partage cette vision…",
    "event": "On s'est croisés lors de {event} — j'aurais voulu échanger plus longtemps…",
    "website": "Je vois que vous avez exploré notre solution récemment…",
    "email_opened": "Je reviens vers vous suite à mon message précédent…",
    "default": "Je vous contacte car votre profil correspond exactement à nos clients qui…",
}

_CTA_BY_LEVEL: Dict[PersonalizationLevel, str] = {
    PersonalizationLevel.DEEP: "Proposer un appel de 20 min avec agenda personnalisé et étude de cas préparée",
    PersonalizationLevel.STRONG: "Proposer un appel découverte de 15 min avec une question d'ouverture ciblée",
    PersonalizationLevel.MODERATE: "Envoyer un contenu pertinent en pièce jointe et proposer un échange de 15 min",
    PersonalizationLevel.BASIC: "Proposer une démo ou un lien calendrier direct",
    PersonalizationLevel.GENERIC: "Envoyer un email template court avec lien vers ressource générique",
}


@dataclass
class ContactProfile:
    contact_id: str
    full_name: str
    title: str
    company: str
    industry: str
    company_size: str          # "1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"
    linkedin_connections: int
    # Engagement signals
    website_visits_30d: int
    emails_opened_30d: int
    content_downloads: int
    event_attendances: int
    # Profile richness
    has_direct_phone: bool
    has_linkedin: bool
    has_personal_email: bool
    crm_notes_count: int       # number of notes in CRM
    previous_interactions: int # calls + meetings historically
    # Trigger signals
    triggers: List[str]        # list of TriggerType values
    trigger_recency_days: int  # days since most recent trigger (0 = today)
    # Fit signals
    is_decision_maker: bool
    budget_authority: bool
    pain_score: float          # 0-100 — inferred pain from interactions
    icp_score: float           # 0-100 — ICP match
    # Preferred channel (if known)
    preferred_channel: Optional[str]   # "email" | "linkedin" | "phone" | None
    timezone_offset: int       # hours from UTC, for timing

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PersonalizationPlan:
    contact: ContactProfile
    personalization_level: PersonalizationLevel
    recommended_channel: OutreachChannel
    personalization_score: float        # 0-100
    profile_richness_score: float
    engagement_score: float
    timing_score: float
    channel_fit_score: float
    primary_angle: str
    secondary_angles: List[str]
    opening_hook: str
    call_to_action: str
    best_send_time: str                 # e.g., "Mardi 09h00"
    personalization_tokens: List[str]   # specific facts to weave into message
    do_not_contact: bool
    outreach_urgency: float             # 0-100, higher = contact now

    def to_dict(self) -> dict:
        return {
            "contact": self.contact.to_dict(),
            "personalization_level": self.personalization_level.value,
            "recommended_channel": self.recommended_channel.value,
            "personalization_score": self.personalization_score,
            "profile_richness_score": self.profile_richness_score,
            "engagement_score": self.engagement_score,
            "timing_score": self.timing_score,
            "channel_fit_score": self.channel_fit_score,
            "primary_angle": self.primary_angle,
            "secondary_angles": self.secondary_angles,
            "opening_hook": self.opening_hook,
            "call_to_action": self.call_to_action,
            "best_send_time": self.best_send_time,
            "personalization_tokens": self.personalization_tokens,
            "do_not_contact": self.do_not_contact,
            "outreach_urgency": self.outreach_urgency,
        }


# ─── Dimension scorers ────────────────────────────────────────────────────────

def _profile_richness(c: ContactProfile) -> float:
    score = 0.0
    # Contact data completeness
    score += 20.0 if c.has_direct_phone else 0.0
    score += 15.0 if c.has_linkedin else 0.0
    score += 10.0 if c.has_personal_email else 0.0
    # CRM depth
    score += min(20.0, c.crm_notes_count * 4.0)
    # Interaction history
    score += min(20.0, c.previous_interactions * 5.0)
    # ICP & pain match
    score += c.icp_score * 0.10 + c.pain_score * 0.05
    return round(min(100.0, score), 2)


def _engagement_signals(c: ContactProfile) -> float:
    website_score = min(40.0, c.website_visits_30d * 10.0)
    email_score = min(25.0, c.emails_opened_30d * 8.0)
    content_score = min(20.0, c.content_downloads * 10.0)
    event_score = min(15.0, c.event_attendances * 7.5)
    score = website_score + email_score + content_score + event_score
    return round(min(100.0, score), 2)


def _timing_fit(c: ContactProfile) -> float:
    # Trigger recency (0 days = 100, 7 days = 80, 30 days = 50, 60+ = 20)
    recency = c.trigger_recency_days
    if not c.triggers:
        trigger_score = 20.0
    elif recency == 0:
        trigger_score = 100.0
    elif recency <= 7:
        trigger_score = 80.0 + (7 - recency) * (20.0 / 7.0)
    elif recency <= 30:
        trigger_score = 50.0 + (30 - recency) * (30.0 / 23.0)
    elif recency <= 60:
        trigger_score = 20.0 + (60 - recency) * (30.0 / 30.0)
    else:
        trigger_score = 10.0

    # Engagement recency bonus
    engagement_bonus = 0.0
    if c.website_visits_30d > 0:
        engagement_bonus += 15.0
    if c.emails_opened_30d > 0:
        engagement_bonus += 10.0

    score = trigger_score * 0.70 + min(25.0, engagement_bonus) * 1.20
    return round(min(100.0, score), 2)


def _channel_fit(c: ContactProfile) -> float:
    scores: Dict[OutreachChannel, float] = {
        OutreachChannel.EMAIL: 50.0,
        OutreachChannel.LINKEDIN: 50.0,
        OutreachChannel.PHONE: 50.0,
        OutreachChannel.MULTI: 60.0,
    }

    if c.has_linkedin:
        scores[OutreachChannel.LINKEDIN] += 20.0
    if c.has_direct_phone:
        scores[OutreachChannel.PHONE] += 25.0
    if c.has_personal_email:
        scores[OutreachChannel.EMAIL] += 15.0
    if c.linkedin_connections >= 500:
        scores[OutreachChannel.LINKEDIN] += 10.0
    if c.emails_opened_30d > 0:
        scores[OutreachChannel.EMAIL] += 10.0
    if c.previous_interactions >= 2:
        scores[OutreachChannel.PHONE] += 15.0

    if c.preferred_channel:
        ch_map = {
            "email": OutreachChannel.EMAIL,
            "linkedin": OutreachChannel.LINKEDIN,
            "phone": OutreachChannel.PHONE,
        }
        pref = ch_map.get(c.preferred_channel)
        if pref:
            scores[pref] += 20.0

    best_channel = max(scores, key=lambda k: scores[k])
    return round(min(100.0, scores[best_channel]), 2), best_channel  # type: ignore[return-value]


def _personalization_level(score: float) -> PersonalizationLevel:
    if score >= 80:
        return PersonalizationLevel.DEEP
    if score >= 65:
        return PersonalizationLevel.STRONG
    if score >= 45:
        return PersonalizationLevel.MODERATE
    if score >= 25:
        return PersonalizationLevel.BASIC
    return PersonalizationLevel.GENERIC


def _select_angles(c: ContactProfile) -> Tuple[str, List[str]]:
    primary = "default"
    secondary: List[str] = []

    trigger_priority = [
        (TriggerType.JOB_CHANGE.value, "job_change_angle"),
        (TriggerType.FUNDING.value, "funding_angle"),
        (TriggerType.HIRING.value, "hiring_angle"),
        (TriggerType.CONTENT_PUBLISHED.value, "content_angle"),
        (TriggerType.EVENT_ATTENDED.value, "event_angle"),
        (TriggerType.WEBSITE_VISIT.value, "website_angle"),
        (TriggerType.EMAIL_OPENED.value, "email_opened_angle"),
        (TriggerType.AWARD.value, "growth_angle"),
        (TriggerType.EXPANSION.value, "growth_angle"),
    ]

    for trigger, angle in trigger_priority:
        if trigger in c.triggers:
            primary = angle
            break

    if primary == "default":
        if c.pain_score >= 70:
            primary = "pain_angle"
        elif c.icp_score >= 80:
            primary = "expertise_angle"

    # Secondary angles
    if c.pain_score >= 60 and primary != "pain_angle":
        secondary.append("pain_angle")
    if c.icp_score >= 75 and primary != "peer_angle":
        secondary.append("peer_angle")
    if TriggerType.JOB_CHANGE.value in c.triggers and primary != "job_change_angle":
        secondary.append("job_change_angle")

    seen: set = set()
    secondary = [a for a in secondary if not (a in seen or seen.add(a)) and a != primary]  # type: ignore[func-returns-value]

    primary_msg = _ANGLE_TEMPLATES.get(primary, _ANGLE_TEMPLATES["pain_angle"])
    secondary_msgs = [_ANGLE_TEMPLATES[a] for a in secondary[:2] if a in _ANGLE_TEMPLATES]
    return primary_msg, secondary_msgs


def _opening_hook(c: ContactProfile) -> str:
    if TriggerType.JOB_CHANGE.value in c.triggers:
        return _OPENING_HOOKS["job_change"].format(title=c.title)
    if TriggerType.FUNDING.value in c.triggers:
        return _OPENING_HOOKS["funding"].format(amount="votre dernière levée")
    if TriggerType.HIRING.value in c.triggers:
        return _OPENING_HOOKS["hiring"].format(company=c.company)
    if TriggerType.CONTENT_PUBLISHED.value in c.triggers:
        return _OPENING_HOOKS["content"].format(topic="votre dernier article")
    if TriggerType.EVENT_ATTENDED.value in c.triggers:
        return _OPENING_HOOKS["event"].format(event="l'événement récent")
    if c.website_visits_30d > 0:
        return _OPENING_HOOKS["website"]
    if c.emails_opened_30d > 0:
        return _OPENING_HOOKS["email_opened"]
    return _OPENING_HOOKS["default"]


def _best_send_time(c: ContactProfile) -> str:
    tz = c.timezone_offset
    # Best times: Tue/Thu 09h or 14h local time
    if -6 <= tz <= -3:
        return "Mardi 15h00 (heure Paris)"
    if tz >= 8:
        return "Mardi 08h00 (heure Paris)"
    return "Mardi 09h00 ou Jeudi 14h00"


def _personalization_tokens(c: ContactProfile) -> List[str]:
    tokens: List[str] = []
    tokens.append(f"Prénom: {c.full_name.split()[0]}")
    tokens.append(f"Titre: {c.title}")
    tokens.append(f"Entreprise: {c.company}")
    tokens.append(f"Secteur: {c.industry}")
    if c.triggers:
        tokens.append(f"Déclencheur: {c.triggers[0].replace('_', ' ')}")
    if c.pain_score >= 60:
        tokens.append(f"Pain score: {int(c.pain_score)}/100")
    if c.crm_notes_count > 0:
        tokens.append(f"Contexte CRM: {c.crm_notes_count} note(s)")
    if c.previous_interactions > 0:
        tokens.append(f"Historique: {c.previous_interactions} interaction(s)")
    return tokens


def _outreach_urgency(c: ContactProfile, timing: float, engagement: float) -> float:
    base = (timing * 0.50 + engagement * 0.30 + c.icp_score * 0.20)
    if c.is_decision_maker:
        base = min(100.0, base + 10.0)
    if c.budget_authority:
        base = min(100.0, base + 5.0)
    return round(base, 2)


def _personalize_contact(c: ContactProfile) -> PersonalizationPlan:
    richness = _profile_richness(c)
    engagement = _engagement_signals(c)
    timing = _timing_fit(c)
    channel_result = _channel_fit(c)
    channel_score, best_channel = channel_result  # type: ignore[misc]

    score = round(
        richness * 0.30
        + engagement * 0.25
        + timing * 0.25
        + channel_score * 0.20,
        2,
    )

    level = _personalization_level(score)
    primary_angle, secondary_angles = _select_angles(c)
    hook = _opening_hook(c)
    cta = _CTA_BY_LEVEL[level]
    send_time = _best_send_time(c)
    tokens = _personalization_tokens(c)
    urgency = _outreach_urgency(c, timing, engagement)

    return PersonalizationPlan(
        contact=c,
        personalization_level=level,
        recommended_channel=best_channel,
        personalization_score=score,
        profile_richness_score=richness,
        engagement_score=engagement,
        timing_score=timing,
        channel_fit_score=channel_score,
        primary_angle=primary_angle,
        secondary_angles=secondary_angles,
        opening_hook=hook,
        call_to_action=cta,
        best_send_time=send_time,
        personalization_tokens=tokens,
        do_not_contact=False,
        outreach_urgency=urgency,
    )


class ContactPersonalizer:
    def __init__(self) -> None:
        self._store: Dict[str, PersonalizationPlan] = {}
        self._dnc: set = set()   # do-not-contact list

    def add_to_dnc(self, contact_id: str) -> None:
        self._dnc.add(contact_id)

    def personalize(self, contact: ContactProfile) -> PersonalizationPlan:
        plan = _personalize_contact(contact)
        if contact.contact_id in self._dnc:
            plan.do_not_contact = True
        self._store[contact.contact_id] = plan
        return plan

    def personalize_batch(self, contacts: List[ContactProfile]) -> List[PersonalizationPlan]:
        return [self.personalize(c) for c in contacts]

    def get(self, contact_id: str) -> Optional[PersonalizationPlan]:
        return self._store.get(contact_id)

    def all_plans(self) -> List[PersonalizationPlan]:
        return sorted(self._store.values(), key=lambda p: p.outreach_urgency, reverse=True)

    def by_level(self, level: PersonalizationLevel) -> List[PersonalizationPlan]:
        return [p for p in self._store.values() if p.personalization_level == level]

    def by_channel(self, channel: OutreachChannel) -> List[PersonalizationPlan]:
        return [p for p in self._store.values() if p.recommended_channel == channel]

    def hot_contacts(self, threshold: float = 70.0) -> List[PersonalizationPlan]:
        return sorted(
            [p for p in self._store.values() if p.outreach_urgency >= threshold and not p.do_not_contact],
            key=lambda p: p.outreach_urgency,
            reverse=True,
        )

    def top_priority(self, n: int = 10) -> List[PersonalizationPlan]:
        return self.all_plans()[:n]

    def deep_personalization_contacts(self) -> List[PersonalizationPlan]:
        return self.by_level(PersonalizationLevel.DEEP)

    def summary(self) -> dict:
        items = list(self._store.values())
        count = len(items)
        if count == 0:
            return {
                "total": 0,
                "level_counts": {l.value: 0 for l in PersonalizationLevel},
                "channel_counts": {c.value: 0 for c in OutreachChannel},
                "avg_personalization_score": 0.0,
                "avg_urgency": 0.0,
                "hot_count": 0,
                "dnc_count": 0,
            }
        level_counts = {l.value: 0 for l in PersonalizationLevel}
        channel_counts = {c.value: 0 for c in OutreachChannel}
        for p in items:
            level_counts[p.personalization_level.value] += 1
            channel_counts[p.recommended_channel.value] += 1
        avg_score = sum(p.personalization_score for p in items) / count
        avg_urgency = sum(p.outreach_urgency for p in items) / count
        hot = sum(1 for p in items if p.outreach_urgency >= 70.0 and not p.do_not_contact)
        dnc = sum(1 for p in items if p.do_not_contact)
        return {
            "total": count,
            "level_counts": level_counts,
            "channel_counts": channel_counts,
            "avg_personalization_score": round(avg_score, 2),
            "avg_urgency": round(avg_urgency, 2),
            "hot_count": hot,
            "dnc_count": dnc,
        }

    def reset(self) -> None:
        self._store.clear()
        self._dnc.clear()
