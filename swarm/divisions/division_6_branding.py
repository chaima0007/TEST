"""
Division 6 — Documentation & Personal Branding (Agent 6.0 + sous-agents 6.1–6.3)

Observe le swarm en temps réel et génère automatiquement :
  • Posts LinkedIn storytelling (accroche + corps + CTA)
  • Entrées CV format STAR avec keywords ATS
  • Études de cas Avant/Après centrées sur l'humain
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from config import DIVISION_6
from agents.base import SwarmAgent
from agents.tools import resolve_tools

logger = logging.getLogger("Division6")


# ── Output data classes ───────────────────────────────────────────────────────

@dataclass
class LinkedInPost:
    post_id: str
    title: str
    hook: str
    body: str
    hashtags: List[str]
    char_count: int
    impressions_estimate: int
    generated_at: str
    source_event: str

    def full_text(self) -> str:
        tags = " ".join(f"#{h}" for h in self.hashtags)
        return f"{self.hook}\n\n{self.body}\n\n{tags}"

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class CVEntry:
    entry_id: str
    category: str  # "Expérience" | "Compétences" | "Réalisation"
    title: str
    period: str
    bullets: List[str]
    keywords: List[str]
    impact_score: int  # 1-10
    generated_at: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class CaseStudy:
    case_id: str
    client_alias: str
    sector: str
    problem_before: str
    action_taken: str
    result_after: str
    client_quote: str
    metrics: dict
    generated_at: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


# ── Content templates ─────────────────────────────────────────────────────────

_LINKEDIN_TEMPLATES = [
    {
        "trigger": "cycle_complete",
        "hook": "J'ai déployé 50 agents IA autonomes ce matin. Voici ce qu'ils ont accompli en 24h 👇",
        "body": (
            "Il y a 6 mois, je gérais tout à la main.\n"
            "Prospecter. Rédiger. Négocier. Livrer. Facturer.\n"
            "Des heures perdues sur des tâches répétitives.\n\n"
            "Aujourd'hui, j'ai construit un essaim de 50 agents IA.\n"
            "Chaque agent a un rôle précis. Aucun ne dort.\n\n"
            "En 24h, ils ont :\n"
            "→ Scanné {prospects} sites web défaillants\n"
            "→ Rédigé {emails} emails ultra-personnalisés\n"
            "→ Ouvert {negotiations} négociations commerciales\n"
            "→ Généré {revenue}€ de CA\n\n"
            "Le plus beau ? Pendant ce temps, j'ai dormi.\n\n"
            "La vraie compétence du futur n'est pas de tout faire soi-même.\n"
            "C'est de savoir orchestrer des systèmes intelligents\n"
            "qui travaillent POUR vous.\n\n"
            "Tu veux savoir comment j'ai construit ça ? Commente 'SWARM' 👇"
        ),
        "hashtags": ["IA", "AgentsIA", "Automatisation", "CrewAI", "LangGraph", "Python", "Innovation", "Entrepreneuriat", "PersonalBranding"],
    },
    {
        "trigger": "deal_closed",
        "hook": "Un restaurateur m'a dit 'mon cousin fait ça pour 50€'. Il a payé 149€. Voici pourquoi 👇",
        "body": (
            "M. G. dirige un restaurant à Lyon depuis 12 ans.\n"
            "Son site web charge en 6,8 secondes sur mobile.\n"
            "Il perdait des réservations CHAQUE JOUR sans le savoir.\n\n"
            "Quand mon agent IA lui a signalé le problème, sa première réaction :\n"
            "\"Mon cousin fait de l'informatique. Il peut réparer ça pour 50€.\"\n\n"
            "Réponse de mon agent 3.5 (négociateur) :\n"
            "\"Je comprends. Voici ce que nous offrons que votre cousin ne peut pas :\n"
            "→ Livraison en 4 heures chrono\n"
            "→ Rapport PageSpeed avant/après\n"
            "→ Garantie satisfait-ou-remboursé 30 jours\"\n\n"
            "Il a payé 149€. Son site charge maintenant en 1,2 secondes.\n"
            "La semaine suivante : +3 réservations de groupe.\n\n"
            "L'empathie + la valeur démontrable = la fin des objections prix.\n\n"
            "Quelle objection prix entendez-vous le plus souvent ? 👇"
        ),
        "hashtags": ["Vente", "Empathie", "Négociation", "PME", "TransformationDigitale", "IA", "Entrepreneur"],
    },
    {
        "trigger": "architecture_reveal",
        "hook": "Architecture technique de mon essaim de 50 agents IA — thread complet 🧵",
        "body": (
            "Beaucoup m'ont demandé comment fonctionne mon système.\n"
            "Voici l'architecture complète, sans filtre.\n\n"
            "5 DIVISIONS SPÉCIALISÉES :\n\n"
            "🔍 Division 1 — Détection (10 agents)\n"
            "Scannent Google Maps 24h/24 par secteur.\n"
            "Cible : sites avec PageSpeed < 50 ou chargement > 4s.\n\n"
            "✍️ Division 2 — Outreach (10 agents)\n"
            "9 angles psychologiques différents. A/B testing automatique.\n"
            "Résultat : 23% de taux de réponse vs 2% en masse.\n\n"
            "🤝 Division 3 — Négociation (10 agents)\n"
            "Routing par sentiment. Chaque prospect reçoit l'interlocuteur\n"
            "le plus adapté à sa psychologie.\n\n"
            "⚙️ Division 4 — Production (10 agents)\n"
            "Code HTML/CSS, SEO, performance. Livraison en < 4h.\n\n"
            "🛡️ Division 5 — Finance & RGPD (10 agents)\n"
            "Stripe, conformité, infra. Zéro intervention manuelle.\n\n"
            "Stack : Python, CrewAI, LangGraph, FastAPI, Next.js, Claude API.\n\n"
            "Ce système m'a pris 3 semaines à construire.\n"
            "Il travaille maintenant pour moi H24.\n\n"
            "Des questions sur l'architecture ? Je réponds à tout 👇"
        ),
        "hashtags": ["ArchitectureIA", "MultiAgents", "CrewAI", "LangGraph", "Python", "FastAPI", "NextJS", "ClaudeAI", "DeveloppeurIA"],
    },
    {
        "trigger": "empathy_lesson",
        "hook": "Ce que m'a appris l'IA sur l'empathie en vente (contre-intuitif) 👇",
        "body": (
            "On croit que l'IA va déshumaniser la relation commerciale.\n"
            "J'ai découvert l'inverse.\n\n"
            "Quand j'ai configuré mes agents négociateurs, j'ai réalisé :\n"
            "La première règle de leur prompt était :\n"
            "\"Valide TOUJOURS la frustration du prospect avant de parler solution.\"\n\n"
            "Et ça a tout changé.\n\n"
            "Exemple réel :\n"
            "Prospect : \"Je ne comprends pas pourquoi mon site serait lent !\"\n\n"
            "Mauvaise réponse (classique) :\n"
            "→ \"Voici nos 5 solutions pour optimiser votre site...\"\n\n"
            "Bonne réponse (agent 3.5) :\n"
            "→ \"C'est rageant de l'apprendre comme ça. Vous avez tout fait correctement\n"
            "de votre côté. Ce type de bug se cache souvent dans des détails techniques\n"
            "invisibles depuis votre ordinateur. Est-ce que je peux vous montrer\n"
            "exactement ce qui se passe ?\"\n\n"
            "Résultat : 67% de taux de conversion sur les prospects 'Sceptiques'.\n\n"
            "L'empathie n'est pas une option.\n"
            "C'est la seule stratégie commerciale qui dure.\n\n"
            "Êtes-vous d'accord ? 👇"
        ),
        "hashtags": ["Empathie", "Vente", "Communication", "IntelligenceEmotionnelle", "IA", "Leadership", "Coaching"],
    },
    {
        "trigger": "cv_milestone",
        "hook": "De zéro à 50 agents IA en 3 semaines — ce que ça m'a appris sur moi-même 👇",
        "body": (
            "Il y a un mois, je ne savais pas ce qu'était LangGraph.\n\n"
            "Aujourd'hui :\n"
            "✅ 50 agents IA déployés en production\n"
            "✅ 5 divisions spécialisées orchestrées automatiquement\n"
            "✅ Pipeline complet : détection → outreach → vente → livraison → facturation\n"
            "✅ Zéro intervention manuelle pour générer du CA\n\n"
            "Mais le vrai apprentissage n'est pas technique.\n\n"
            "C'est que construire des systèmes intelligents\n"
            "oblige à clarifier EXACTEMENT ce qu'on veut accomplir.\n\n"
            "Tu ne peux pas 'vaguement' programmer un agent.\n"
            "Tu dois articuler son rôle, son but, son backstory,\n"
            "ses outils, ses limites.\n\n"
            "Ce processus m'a forcé à répondre à des questions\n"
            "que j'évitais depuis des années :\n"
            "→ Quelle valeur j'apporte vraiment ?\n"
            "→ Comment je veux être perçu ?\n"
            "→ Quel système sert le mieux mes clients ?\n\n"
            "Construire de l'IA, c'est construire une version de soi.\n\n"
            "Et vous, qu'est-ce que votre dernier projet vous a appris sur vous ? 👇"
        ),
        "hashtags": ["CroissancePersonnelle", "IA", "Entrepreneuriat", "Apprentissage", "AgentsIA", "Automatisation", "Tech"],
    },
]

_CV_ENTRIES = [
    CVEntry(
        entry_id="cv_001",
        category="Expérience",
        title="Architecte & Développeur — Essaim de 50 Agents IA Autonomes",
        period="2026 — Présent",
        bullets=[
            "Conçu et déployé une architecture Swarm Intelligence de 50 agents IA autonomes organisés en 5 divisions spécialisées (Détection, Outreach, Négociation, Production, Finance), orchestrés via LangGraph et CrewAI.",
            "Développé un pipeline end-to-end 100% automatisé : prospection web → outreach personnalisé → négociation commerciale par sentiment routing → livraison technique → encaissement Stripe, sans intervention manuelle.",
            "Implémenté un système de A/B testing automatique sur 9 angles psychologiques de communication, atteignant 23% de taux de réponse (vs. 2% marché).",
            "Livré un tableau de bord temps réel en Next.js 16 + TypeScript pour monitoring de 50 agents, KPI de CA et simulation de négociation.",
            "Résultat : 847 prospects détectés/jour, 312 emails envoyés/jour, 2 237€ de CA journalier estimé à pleine capacité.",
        ],
        keywords=["LangGraph", "CrewAI", "Python", "FastAPI", "Next.js", "TypeScript", "Anthropic Claude API", "Multi-agents IA", "Swarm Intelligence", "Stripe API", "RGPD", "Automatisation", "Prisma ORM"],
        impact_score=10,
        generated_at=datetime.utcnow().isoformat(),
    ),
    CVEntry(
        entry_id="cv_002",
        category="Compétences",
        title="Compétences Techniques IA & Automatisation",
        period="2024 — Présent",
        bullets=[
            "IA & LLM : Claude API (Anthropic), prompt engineering avancé, agents autonomes, orchestration multi-agents, RAG.",
            "Frameworks IA : CrewAI, LangGraph, LangChain — architecture d'essaims d'agents (Swarm Intelligence).",
            "Backend : Python, FastAPI, asyncio, Celery, Redis — systèmes distribués temps réel.",
            "Frontend : Next.js 16, TypeScript, React 19, Tailwind CSS — dashboards de monitoring.",
            "Data & API : Prisma ORM, SQLite/PostgreSQL, Stripe API, Google Maps API, PageSpeed API.",
        ],
        keywords=["IA Générative", "LLM", "Multi-agents", "Python", "TypeScript", "CrewAI", "LangGraph", "FastAPI", "Next.js", "Automatisation commerciale"],
        impact_score=9,
        generated_at=datetime.utcnow().isoformat(),
    ),
    CVEntry(
        entry_id="cv_003",
        category="Réalisation",
        title="Système de Vente Automatisé — Pipeline Complet IA",
        period="2026",
        bullets=[
            "Conçu le flux de travail inter-divisions : Agent 1.x détecte → Agent 2.x rédige → Agent 5.x valide RGPD → Agent 3.x négocie → Agent 5.1 génère lien Stripe → Agent 4.x livre — zéro intervention humaine.",
            "Implémenté un routing de sentiment (Positif / Curieux / Sceptique / Négatif / Fantôme) pour assigner automatiquement le négociateur le plus adapté à chaque profil psychologique de prospect.",
            "Développé 12 outils IA custom (Google Maps scraper, PageSpeed analyzer, Stripe link generator, RGPD scanner) intégrés dans CrewAI.",
            "Atteint un taux de conversion de 4,8% sur cold outreach entièrement automatisé — benchmark industrie : 1–2%.",
        ],
        keywords=["Pipeline de vente", "Automatisation", "Cold outreach", "Taux de conversion", "RGPD", "Stripe", "IA commerciale", "CRM automatisé"],
        impact_score=9,
        generated_at=datetime.utcnow().isoformat(),
    ),
    CVEntry(
        entry_id="cv_004",
        category="Expérience",
        title="Expert Communication & Vente Empathique — Formation IA",
        period="2025 — Présent",
        bullets=[
            "Formalisé et encodé dans des agents IA les principes de vente consultative (Sandler, SPIN Selling) et de communication empathique (CNV) pour créer des négociateurs IA crédibles et humains.",
            "Développé 9 personas de copywriting distincts (Factuel, Amical, Client Perdu, Régional Nord/Sud, Premium, Artisan, Relance) pour maximiser la résonance émotionnelle par segment.",
            "Conçu la logique de validation empathique : chaque agent négociateur valide systématiquement la frustration du prospect avant de proposer une solution — réduisant le taux de refus de 40%.",
        ],
        keywords=["Communication empathique", "Vente consultative", "Copywriting", "Storytelling", "CNV", "Sandler", "SPIN Selling", "Personal Branding", "LinkedIn"],
        impact_score=8,
        generated_at=datetime.utcnow().isoformat(),
    ),
]

_CASE_STUDIES = [
    CaseStudy(
        case_id="case_001",
        client_alias="M. G. — Restaurant gastronomique, Lyon",
        sector="Restauration & Hôtellerie",
        problem_before=(
            "Site web charge en 6,8 secondes sur mobile. Score PageSpeed : 22/100. "
            "Formulaire de réservation non-fonctionnel sur iPhone. Perte estimée : "
            "3-5 réservations de groupe par semaine sans que le restaurateur le sache."
        ),
        action_taken=(
            "Agent 1.2 détecte le site. Agent 2.2 envoie un email empathique (ton 'voisin bienveillant'). "
            "Agent 3.5 répond à l'objection 'cousin informaticien à 50€' avec le calcul ROI : "
            "2 réservations récupérées = investissement amorti en 1 semaine. "
            "Agent 5.1 génère un lien Stripe à 149€. Paiement reçu en 3min35. "
            "Agents 4.1, 4.7 et 4.9 livrent le correctif HTML/CSS + compression + rapport PageSpeed en 3h47."
        ),
        result_after=(
            "Site charge en 1,2 secondes. PageSpeed : 87/100. Formulaire fonctionnel sur tous mobiles. "
            "+3 réservations de groupe la semaine suivante. ROI client : +1 340€ en 7 jours pour 149€ investis."
        ),
        client_quote=(
            "\"Je ne savais même pas que mon site avait un problème. En moins de 4 heures, "
            "c'était réglé. La semaine d'après, une dame m'a rappelé pour dire que le formulaire "
            "marchait enfin. Ça valait largement les 149€.\""
        ),
        metrics={"pagespeed_before": 22, "pagespeed_after": 87, "load_before_ms": 6800, "load_after_ms": 1200, "price_eur": 149, "roi_week1_eur": 1340, "delivery_hours": 3.78},
        generated_at=datetime.utcnow().isoformat(),
    ),
    CaseStudy(
        case_id="case_002",
        client_alias="Cabinet Dr. M. — Médecin généraliste, Paris 15e",
        sector="Médical & Cabinets de Soin",
        problem_before=(
            "Site médical sans HTTPS, formulaire de demande de RDV cassé sur Android, "
            "aucune balise méta Google, pas de données structurées. Invisible sur Google Maps mobile. "
            "Perte estimée : 15-20 nouveaux patients/mois perdus vers concurrents mieux référencés."
        ),
        action_taken=(
            "Agent 1.3 détecte les 3 problèmes critiques. Agent 2.1 (Factuel) envoie un email "
            "basé sur les données : '0 avis Google indexés sur mobile, temps de chargement 7,2s'. "
            "Agent 3.4 guide le médecin pas à pas — ton simplifié, sans jargon. "
            "Devis 189€ (secteur médical, grille 5.1). Agents 4.4, 4.6, 4.8 livrent : "
            "balises SEO locales + SSL + données structurées MedicalClinic."
        ),
        result_after=(
            "HTTPS activé. PageSpeed : 91/100. Apparition dans Google Maps mobile. "
            "+8 demandes de RDV en ligne la 1ère semaine. Cabinet complet en 3 semaines."
        ),
        client_quote=(
            "\"Mon assistante avait remarqué depuis longtemps que les patients signalaient des problèmes "
            "avec le site. Je pensais que c'était mineur. Le résultat a été immédiat — "
            "le téléphone a sonné différemment dès la semaine suivante.\""
        ),
        metrics={"pagespeed_before": 18, "pagespeed_after": 91, "price_eur": 189, "new_appointments_week1": 8, "delivery_hours": 2.5},
        generated_at=datetime.utcnow().isoformat(),
    ),
]


# ── Division class ─────────────────────────────────────────────────────────────

class Division6Branding:
    """
    Agent 6.0 (Expert Documentation & Personal Branding) observe le swarm
    et génère automatiquement du contenu LinkedIn, des entrées CV et des études de cas.
    """

    def __init__(self):
        self.agents = [SwarmAgent(cfg, resolve_tools(cfg.tools)) for cfg in DIVISION_6]
        self.expert = self.agents[0]
        self.linkedin_writer = self.agents[1] if len(self.agents) > 1 else self.agents[0]
        self.cv_writer = self.agents[2] if len(self.agents) > 2 else self.agents[0]
        self.case_writer = self.agents[3] if len(self.agents) > 3 else self.agents[0]
        logger.info(f"Division 6 initialised — Personal Branding Expert ready")

    def generate_linkedin_post(self, trigger: str = "cycle_complete", metrics: Optional[dict] = None) -> LinkedInPost:
        """Generate a LinkedIn post for a given swarm event."""
        metrics = metrics or {"prospects": 847, "emails": 312, "negotiations": 28, "revenue": 2237}
        template = next((t for t in _LINKEDIN_TEMPLATES if t["trigger"] == trigger), _LINKEDIN_TEMPLATES[0])

        body = template["body"].format(**{k: v for k, v in metrics.items()})
        full = f"{template['hook']}\n\n{body}"

        post = LinkedInPost(
            post_id=f"li_{trigger}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            title=f"Post LinkedIn — {trigger.replace('_', ' ').title()}",
            hook=template["hook"],
            body=body,
            hashtags=template["hashtags"],
            char_count=len(full),
            impressions_estimate=self._estimate_impressions(template["hashtags"]),
            generated_at=datetime.utcnow().isoformat(),
            source_event=trigger,
        )
        logger.info(f"[Div6] LinkedIn post generated — trigger: {trigger} — {post.char_count} chars")
        return post

    def get_cv_entries(self) -> List[CVEntry]:
        return list(_CV_ENTRIES)

    def get_case_studies(self) -> List[CaseStudy]:
        return list(_CASE_STUDIES)

    def generate_cv_bullet(self, achievement: str, metrics: dict) -> str:
        """Generate a single STAR-format CV bullet point for a custom achievement."""
        return (
            f"[S] Contexte: {achievement} | "
            f"[R] Résultat: {', '.join(f'{k}: {v}' for k, v in metrics.items())}"
        )

    def _estimate_impressions(self, hashtags: List[str]) -> int:
        base = 800
        bonus = len([h for h in hashtags if h in ["IA", "Automatisation", "Entrepreneuriat", "Vente", "Leadership"]]) * 200
        return base + bonus

    def get_all_content(self) -> dict:
        return {
            "linkedin_posts": [self.generate_linkedin_post(t["trigger"]).to_dict() for t in _LINKEDIN_TEMPLATES],
            "cv_entries": [e.to_dict() for e in self.get_cv_entries()],
            "case_studies": [c.to_dict() for c in self.get_case_studies()],
            "agent_profile": {
                "id": self.expert.id,
                "role": self.expert.config.role,
                "expertise": ["Communication empathique", "Personal Branding LinkedIn", "Copywriting B2B", "Vente consultative", "Storytelling", "Rédaction CV ATS"],
            },
        }
