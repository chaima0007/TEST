"""
Division 2 — Rédaction & Outreach (10 agents)
Generates hyper-personalised cold emails with A/B tone testing.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List, Optional

from crewai import Crew, Process, Task

from config import DIVISION_2
from agents.base import SwarmAgent
from agents.tools import resolve_tools
from divisions.division_1_detection import ProspectFiche
from intelligence.ab_tester import ABTester

logger = logging.getLogger("Division2")


@dataclass
class OutreachRecord:
    company_id: str
    fiche: ProspectFiche
    email_draft: str
    tone: str
    copywriter_agent: str
    rgpd_validated: bool = False
    sent_at: Optional[str] = None
    open_rate_estimate: float = 0.0

    def to_dict(self) -> dict:
        d = self.__dict__.copy()
        d["fiche"] = self.fiche.to_dict()
        return d


# Maps tone variant to the copywriter agent ID
TONE_ASSIGNMENTS = {
    "factuel": "2.1",
    "amical": "2.2",
    "client_perdu": "2.3",
    "regional_nord": "2.4",
    "regional_sud": "2.5",
    "paris_idf": "2.6",
    "premium": "2.7",
    "artisans_tpe": "2.8",
    "relance": "2.9",
}

EMAIL_TEMPLATES = {
    "2.1": (
        "Objet : Votre site charge en {load_time}ms — PageSpeed {score}/100\n\n"
        "Bonjour,\n\n"
        "En analysant {website}, j'ai relevé : temps de chargement {load_time}ms, "
        "score PageSpeed mobile {score}/100. Ces indicateurs représentent une perte "
        "estimée de 35 % de vos visiteurs mobiles. Ces chiffres vous ont-ils déjà été signalés ?"
    ),
    "2.2": (
        "Objet : Un petit souci sur votre site mobile\n\n"
        "Bonjour,\n\n"
        "En visitant {website} depuis mon téléphone, j'ai remarqué que la page mettait "
        "beaucoup de temps à s'afficher. Je voulais simplement vous prévenir — "
        "est-ce que ce bug vous a déjà été remonté par vos clients ?"
    ),
    "2.3": (
        "Objet : J'ai essayé de vous contacter depuis mon mobile — impossible\n\n"
        "Bonjour,\n\n"
        "J'ai voulu faire une demande via {website} mais le formulaire ne répondait pas "
        "sur mon iPhone. Est-ce un problème connu ? Je souhaitais juste vous transmettre "
        "ma demande correctement."
    ),
}


def _draft_email(fiche: ProspectFiche, agent_id: str) -> str:
    template = EMAIL_TEMPLATES.get(agent_id, EMAIL_TEMPLATES["2.2"])
    return template.format(
        website=fiche.website,
        load_time=fiche.load_time_ms,
        score=fiche.pagespeed_score,
        name=fiche.name,
    )


class Division2Redaction:
    """
    Manager 2.0 distributes prospect fiches to 9 copywriters (2.1–2.9).
    Each copywriter applies a distinct psychological angle.
    Thompson Sampling (via ABTester) picks the winning tone per prospect.
    """

    def __init__(self):
        self.agents = [SwarmAgent(cfg, resolve_tools(cfg.tools)) for cfg in DIVISION_2]
        self.manager = next(a for a in self.agents if a.is_manager)
        self.writers = [a for a in self.agents if not a.is_manager]
        self.ab_tester = ABTester()
        logger.info(f"Division 2 initialised — {len(self.writers)} copywriters + ABTester ready")

    def build_crew(self, fiches: List[ProspectFiche]) -> Crew:
        tasks = []
        for i, fiche in enumerate(fiches[:9]):
            writer = self.writers[i % len(self.writers)]
            tasks.append(Task(
                description=(
                    f"Rédige un e-mail d'approche en 120 mots maximum pour {fiche.name} "
                    f"({fiche.sector}). Site : {fiche.website}. "
                    f"Problème détecté : PageSpeed {fiche.pagespeed_score}/100, "
                    f"chargement {fiche.load_time_ms}ms. "
                    f"Applique ton angle : {writer.config.role}. "
                    f"Interdiction de vendre quoi que ce soit — pose une question ouverte uniquement."
                ),
                expected_output="Email texte brut, objet + corps, 120 mots max",
                agent=writer.build(),
            ))

        validation_task = Task(
            description=(
                "Révise tous les emails rédigés par tes copywriters. "
                "Vérifie : ton non-agressif, < 120 mots, question ouverte présente, "
                "nom de l'entreprise correctement utilisé. "
                "Retourne la liste validée au format JSON."
            ),
            expected_output="JSON array des emails validés avec champ 'approved': true/false",
            agent=self.manager.build(),
            context=tasks,
        )

        return Crew(
            agents=[a.build() for a in self.agents],
            tasks=[*tasks, validation_task],
            process=Process.hierarchical,
            manager_agent=self.manager.build(),
            verbose=False,
        )

    def draft_all(self, fiches: List[ProspectFiche]) -> List[OutreachRecord]:
        """Draft personalised emails for each prospect fiche using Thompson Sampling."""
        records: List[OutreachRecord] = []
        for fiche in fiches:
            agent_id = self.ab_tester.select_agent(sector=fiche.sector)
            writer = next((w for w in self.writers if w.id == agent_id), self.writers[0])
            draft = _draft_email(fiche, writer.id)
            self.ab_tester.record_result(agent_id, sent=True)
            records.append(OutreachRecord(
                company_id=fiche.company_id,
                fiche=fiche,
                email_draft=draft,
                tone=writer.config.role,
                copywriter_agent=writer.id,
            ))
        logger.info(f"[Div2] {len(records)} emails drafted — ABTester winner: {self.ab_tester.get_winner()}")
        return records

    def record_reply(self, agent_id: str, opened: bool = False, replied: bool = False, paid: bool = False) -> None:
        """Feed reply outcome back to the A/B tester to update Thompson posteriors."""
        self.ab_tester.record_result(agent_id, sent=False, opened=opened, replied=replied, paid=paid)

    def get_ab_report(self) -> dict:
        """Return the current A/B test performance report."""
        return self.ab_tester.get_report()
