"""
Caelum Partners — Extraordinary Rendition & Secret Detention Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Renditions extraordinaires, sites de détention secrets, torture post-9/11
(programme CIA, art. 5 DUDH, Convention contre la torture CAT).

Le programme de renditions extraordinaires de la CIA post-11 septembre 2001 constitue
l'une des violations les plus documentées du droit international des droits humains
au XXIe siècle. Plus de 136 individus ont été transférés illégalement entre pays,
détenus dans des sites noirs secrets (black sites) en Europe et en dehors, soumis
à des techniques d'interrogatoire constituant de la torture selon la Convention CAT
et l'article 5 de la Déclaration Universelle des Droits de l'Homme.

Le rapport du Sénat américain de 2014 (SSCI), les arrêts de la Cour Européenne des
Droits de l'Homme (Abu Zubaydah c. Pologne, 2014 ; Al Nashiri c. Roumanie, 2018),
et les rapports du Rapporteur spécial ONU ont documenté la complicité de 54 États
dans ce système d'impunité organisée. Les victimes font face à des obstacles
systématiques d'accès aux recours : secret d'État, immunité diplomatique, et
absence de poursuites contre les hauts responsables.

Risk levels (renditions extraordinaires et détention secrète — impunité systémique) :
  critique  -> composite >= 60  (programme systémique — torture documentée, zéro accountability)
  élevé     -> composite >= 40  (sites noirs actifs ou complicité majeure — réformes insuffisantes)
  modéré    -> composite >= 20  (complicité partielle — reconnaissances et compensations partielles)
  faible    -> composite < 20   (réformes judiciaires et institutionnelles — cadre accountability)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class ExtraordinaryRenditionSecretDetentionEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    rendition_program_scale_score: float
    torture_detention_severity_score: float
    judicial_impunity_accountability_score: float
    victim_remedy_access_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_rendition_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.rendition_program_scale_score * 0.30
            + self.torture_detention_severity_score * 0.25
            + self.judicial_impunity_accountability_score * 0.25
            + self.victim_remedy_access_score * 0.20,
            2,
        )
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_rendition_rights_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "rendition_program_scale_score": self.rendition_program_scale_score,
            "torture_detention_severity_score": self.torture_detention_severity_score,
            "judicial_impunity_accountability_score": self.judicial_impunity_accountability_score,
            "victim_remedy_access_score": self.victim_remedy_access_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_rendition_rights_index": self.estimated_rendition_rights_index,
            "last_updated": self.last_updated,
        }


@dataclass
class ExtraordinaryRenditionSecretDetentionEngineResult:
    agent: str = "Extraordinary Rendition & Secret Detention Engine Agent"
    domain: str = "extraordinary_rendition_secret_detention"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.88
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_rendition_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ExtraordinaryRenditionSecretDetentionEntity] = field(default_factory=list)


def run_extraordinary_rendition_secret_detention_engine() -> ExtraordinaryRenditionSecretDetentionEngineResult:
    entities = [
        ExtraordinaryRenditionSecretDetentionEntity(
            entity_id="ERD-001",
            name="USA/CIA Programme Post-9/11 — 136 Détenus, 54 Pays Complices, Rapport Senate 2014, Sites Noirs Globaux",
            country="USA",
            sector="Programme Renditions CIA",
            rendition_program_scale_score=90.0,
            torture_detention_severity_score=88.0,
            judicial_impunity_accountability_score=87.0,
            victim_remedy_access_score=72.0,
            primary_pattern="rendition_program_scale",
            key_signals=[
                "136 individus transférés illégalement documentés SSCI 2014",
                "54 États complices programme renditions CIA",
                "Techniques interrogatoire EIT : waterboarding, sleep deprivation, confinement",
                "Zéro poursuite pénale contre hauts responsables CIA/DoD",
            ],
        ),
        ExtraordinaryRenditionSecretDetentionEntity(
            entity_id="ERD-002",
            name="Égypte/Extraordinary Rendition Hub — Destination Principale CIA, Mohamed Al-Zery, Ibrahim Al-Zubaydi, Impunité SSNSI",
            country="Égypte",
            sector="Hub Renditions CIA-SSNSI",
            rendition_program_scale_score=87.0,
            torture_detention_severity_score=85.0,
            judicial_impunity_accountability_score=84.0,
            victim_remedy_access_score=68.0,
            primary_pattern="torture_detention_severity",
            key_signals=[
                "Destination principale transferts illégaux CIA — coordination SSNSI",
                "Mohamed Al-Zery : rendu de Suède vers Égypte, électrochocs, condamné CEDH",
                "Ibrahim Al-Zubaydi : disparition forcée, famille sans recours",
                "Présidence Hosni Moubarak complice documentée — impunité totale post-2011",
            ],
        ),
        ExtraordinaryRenditionSecretDetentionEntity(
            entity_id="ERD-003",
            name="Syrie/Assad Torture Centres — CIA Renditions vers Assad, Maher Arar, Détention al-Mazzeh, Pratiques Documentées",
            country="Syrie",
            sector="Centres Détention Assad-CIA",
            rendition_program_scale_score=85.0,
            torture_detention_severity_score=83.0,
            judicial_impunity_accountability_score=82.0,
            victim_remedy_access_score=65.0,
            primary_pattern="torture_detention_severity",
            key_signals=[
                "Maher Arar : rendu Canada→Syrie, 374 jours torture prison al-Far Falasin",
                "Prison al-Mazzeh : cellules 1m², techniques torture systématiques",
                "CIA utilise régime Assad malgré connaissance torture — 'proxy torture'",
                "Commission Arar Canada 2006 : condamné CIA/RCMP, compensation 10.5M CAD",
            ],
        ),
        ExtraordinaryRenditionSecretDetentionEntity(
            entity_id="ERD-004",
            name="Pakistan/ISI Collaboration — Capture HVTs Post-9/11, Disparitions Forcées Baloutchistan, Complice Renditions 500+",
            country="Pakistan",
            sector="Collaboration ISI-CIA Renditions",
            rendition_program_scale_score=78.0,
            torture_detention_severity_score=76.0,
            judicial_impunity_accountability_score=75.0,
            victim_remedy_access_score=58.0,
            primary_pattern="rendition_program_scale",
            key_signals=[
                "ISI co-capture de Khalid Sheikh Mohammed, Abu Zubaydah — transferts CIA",
                "Disparitions forcées Baloutchistan : 5000+ cas documentés HRW/Amnesty",
                "500+ individus transférés vers CIA avec compensation financière ISI",
                "Commission enforced disappearances Pakistan : zéro poursuites militaires",
            ],
        ),
        ExtraordinaryRenditionSecretDetentionEntity(
            entity_id="ERD-005",
            name="Pologne-Roumanie-Lituanie/Sites Noirs CIA Europe — Arrêts CEDH, Abu Zubaydah vs Pologne, Stare Kiejkuty",
            country="Pologne/Roumanie/Lituanie",
            sector="Sites Noirs CIA Europe",
            rendition_program_scale_score=58.0,
            torture_detention_severity_score=57.0,
            judicial_impunity_accountability_score=56.0,
            victim_remedy_access_score=47.0,
            primary_pattern="judicial_impunity_accountability",
            key_signals=[
                "CEDH Abu Zubaydah c. Pologne (2014) : violation art. 3 CEDH — torture consentie",
                "Stare Kiejkuty Pologne : site noir CIA opérationnel 2002-2003, confirmé CEDH",
                "Roumanie : arrêt Al Nashiri c. Roumanie (2018) — Villa Cincu CIA prison",
                "Lituanie : arrêts Mustafa Najar (2021) — réformes enquêtes insuffisantes",
            ],
        ),
        ExtraordinaryRenditionSecretDetentionEntity(
            entity_id="ERD-006",
            name="Maroc/DGED Coopération — Témara Prison Noire, Coalition CIA-MI6-DGED, Impunité Persistante des Responsables",
            country="Maroc",
            sector="Coopération DGED-CIA Détention",
            rendition_program_scale_score=50.0,
            torture_detention_severity_score=50.0,
            judicial_impunity_accountability_score=49.0,
            victim_remedy_access_score=42.0,
            primary_pattern="rendition_program_scale",
            key_signals=[
                "Prison Témara : site noir CIA-DGED, techniques torture documentées Amnesty",
                "Coalition CIA-MI6-DGED : triangulation interrogatoires détenus rendus",
                "Bisher Al-Rawi : rendu vers Gambie puis Guantanamo via coordination DGED",
                "Impunité persistante : aucun responsable DGED poursuivi post-2011",
            ],
        ),
        ExtraordinaryRenditionSecretDetentionEntity(
            entity_id="ERD-007",
            name="Royaume-Uni/Complicité Partielle — Rapport ISC 2018, Belhaj v UK, Dédommagements Partiels, Réformes Intelligence",
            country="Royaume-Uni",
            sector="Complicité MI6-HMG Renditions",
            rendition_program_scale_score=32.0,
            torture_detention_severity_score=31.0,
            judicial_impunity_accountability_score=30.0,
            victim_remedy_access_score=26.0,
            primary_pattern="victim_remedy_access",
            key_signals=[
                "Rapport ISC 2018 : MI6 complice 28 cas renditions — 'inadequate oversight'",
                "Belhaj v UK : Abdelhakim Belhaj et Fatima Boudchar rendus vers Libye/Kadhafi",
                "Règlement 2018 : excuses formelles HMG + compensation — admission partielle",
                "Réformes oversight intelligence post-ISC : Investigatory Powers Act 2016",
            ],
        ),
        ExtraordinaryRenditionSecretDetentionEntity(
            entity_id="ERD-008",
            name="Allemagne/Recours Khaled El-Masri — Condamnation CEDH CIA, Réformes BND-Parlementaires, Accountability Croissant",
            country="Allemagne",
            sector="Réformes Accountability Renditions",
            rendition_program_scale_score=11.0,
            torture_detention_severity_score=10.0,
            judicial_impunity_accountability_score=9.0,
            victim_remedy_access_score=9.0,
            primary_pattern="judicial_impunity_accountability",
            key_signals=[
                "CEDH El-Masri c. Macédoine (2012) : torture CIA Salt Pit confirmée, réparation",
                "Bundestag enquête NSA-BND : réformes oversight renseignement 2016",
                "El-Masri : citoyen allemand rendu CIA par erreur — compensation partielle obtenue",
                "BND Reform Act 2016 : supervision parlementaire renforcée services secrets",
            ],
        ),
    ]

    composites = [e.composite_score for e in entities]
    avg_composite = round(statistics.mean(composites), 2)

    risk_dist: dict = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1

    pattern_dist: dict = {}
    for e in entities:
        pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1

    sorted_entities = sorted(entities, key=lambda x: x.composite_score, reverse=True)
    top_risk = [e.name for e in sorted_entities[:3]]
    alerts = [
        f"{e.name.split('—')[0].strip()}: {e.primary_pattern}"
        for e in sorted_entities[:4]
    ]

    # Assertions OBLIGATOIRES — distribution 4 critique / 2 élevé / 1 modéré / 1 faible
    critique_count = risk_dist.get("critique", 0)
    eleve_count = risk_dist.get("élevé", 0)
    modere_count = risk_dist.get("modéré", 0)
    faible_count = risk_dist.get("faible", 0)
    assert critique_count == 4, f"Expected 4 critique, got {critique_count}: {risk_dist}"
    assert eleve_count == 2, f"Expected 2 élevé, got {eleve_count}: {risk_dist}"
    assert modere_count == 1, f"Expected 1 modéré, got {modere_count}: {risk_dist}"
    assert faible_count == 1, f"Expected 1 faible, got {faible_count}: {risk_dist}"

    return ExtraordinaryRenditionSecretDetentionEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_rendition_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ssci_senate_cia_torture_report_2014_declassified",
            "echr_abu_zubaydah_poland_2014_rendition_black_sites_ruling",
            "human_rights_watch_extraordinary_renditions_global_network_report",
            "amnesty_international_secret_detention_cia_black_sites_analysis",
            "un_special_rapporteur_torture_extraordinary_rendition_2010",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_extraordinary_rendition_secret_detention_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_rendition_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}] — {e.name[:60]}")
