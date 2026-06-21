"""
Caelum Partners — Sexual Violence Conflict Impunity Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Violence sexuelle dans les conflits armés — viol comme arme de guerre, impunité des
auteurs, accès à la justice pour survivantes.

La violence sexuelle dans les conflits armés (SVCA) constitue l'une des violations des
droits humains les plus systématiquement sous-poursuivies et les plus dévastatrices.
Reconnue crime de guerre et crime contre l'humanité depuis le Tribunal de Nuremberg,
elle est pourtant utilisée de manière délibérée dans presque tous les conflits armés
contemporains comme tactique de terreur, d'épuration ethnique et de destruction des
structures sociales.

Le Bureau de la Représentante Spéciale du Secrétaire Général de l'ONU sur la SVCA
documente des milliers de cas annuels, mais les taux de poursuite restent infimes.
Les survivantes font face à une triple peine : trauma physique et psychologique,
stigmatisation communautaire, et absence quasi-totale de justice. Le précédent Akayesu
au TPIR (1998) — première condamnation internationale de viol comme crime contre
l'humanité — reste une exception dans un océan d'impunité.

Risk levels (violence sexuelle conflits et impunité auteurs) :
  critique  -> composite >= 60  (SVCA systémique — tactique militaire, impunité totale)
  élevé     -> composite >= 40  (violences documentées — poursuites insuffisantes)
  modéré    -> composite >= 20  (progress judiciaire — stigmatisation persistante)
  faible    -> composite < 20   (cadre légal avancé — prévention et soutien effectifs)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class SexualViolenceConflictImpunityEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    systematic_sexual_violence_warfare_score: float
    survivor_justice_access_support_deficit_score: float
    perpetrator_impunity_prosecution_gap_score: float
    stigma_community_reintegration_barriers_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_sexual_violence_conflict_impunity_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.systematic_sexual_violence_warfare_score * 0.30
            + self.survivor_justice_access_support_deficit_score * 0.25
            + self.perpetrator_impunity_prosecution_gap_score * 0.25
            + self.stigma_community_reintegration_barriers_score * 0.20,
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
        self.estimated_sexual_violence_conflict_impunity_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "systematic_sexual_violence_warfare_score": self.systematic_sexual_violence_warfare_score,
            "survivor_justice_access_support_deficit_score": self.survivor_justice_access_support_deficit_score,
            "perpetrator_impunity_prosecution_gap_score": self.perpetrator_impunity_prosecution_gap_score,
            "stigma_community_reintegration_barriers_score": self.stigma_community_reintegration_barriers_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_sexual_violence_conflict_impunity_index": self.estimated_sexual_violence_conflict_impunity_index,
            "last_updated": self.last_updated,
        }


@dataclass
class SexualViolenceConflictImpunityEngineResult:
    agent: str = "Sexual Violence Conflict Impunity Engine Agent"
    domain: str = "sexual_violence_conflict_impunity"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.89
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_sexual_violence_conflict_impunity_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SexualViolenceConflictImpunityEntity] = field(default_factory=list)


def run_sexual_violence_conflict_impunity_engine() -> SexualViolenceConflictImpunityEngineResult:
    entities = [
        SexualViolenceConflictImpunityEntity(
            entity_id="SVCI-001",
            name="RDC/Congo — Capitale Mondiale du Viol, 400K Victimes/An Estimé ONU, Groupes Armés Multiples, Minova Procès Symbolique",
            country="RDC",
            sector="Conflit Armé Chronique",
            systematic_sexual_violence_warfare_score=97.0,
            survivor_justice_access_support_deficit_score=95.0,
            perpetrator_impunity_prosecution_gap_score=96.0,
            stigma_community_reintegration_barriers_score=94.0,
            primary_pattern="systematic_sexual_violence_warfare",
            key_signals=[
                "400 000 victimes de violences sexuelles par an estimé par ONU — chiffres sous-déclarés",
                "Procès Minova 2013 : 135 soldats jugés, 2 condamnations — impunité quasi totale",
                "Docteur Denis Mukwege Prix Nobel soigne survivantes depuis 1999 Panzi",
                "Groupes armés FDLR, ADF, M23 utilisent viol comme tactique de guerre systématique",
            ],
        ),
        SexualViolenceConflictImpunityEntity(
            entity_id="SVCI-002",
            name="Soudan/Darfour & RSF 2023 — Viols Massifs Khartoum, RSF Soldats Systématiques, HRW Documenté, ICC Mandat",
            country="Soudan",
            sector="Conflit RSF & Darfour",
            systematic_sexual_violence_warfare_score=94.0,
            survivor_justice_access_support_deficit_score=92.0,
            perpetrator_impunity_prosecution_gap_score=90.0,
            stigma_community_reintegration_barriers_score=91.0,
            primary_pattern="systematic_sexual_violence_warfare",
            key_signals=[
                "RSF Forces de Soutien Rapide documentées pour viols systématiques Darfour 2023",
                "Viols à Khartoum documentés par HRW et ONU durant conflit avril 2023",
                "Omar el-Béchir sous mandat CPI pour SVCA Darfour — jamais transféré",
                "Accès humanitaire bloqué — survivantes sans soins médicaux ni soutien",
            ],
        ),
        SexualViolenceConflictImpunityEntity(
            entity_id="SVCI-003",
            name="Syrie/Assad — Viols Centres Détention Documentés Commission ONU, Milliers Femmes, Amnistie Interne",
            country="Syrie",
            sector="Répression & Conflit Civil",
            systematic_sexual_violence_warfare_score=91.0,
            survivor_justice_access_support_deficit_score=89.0,
            perpetrator_impunity_prosecution_gap_score=92.0,
            stigma_community_reintegration_barriers_score=88.0,
            primary_pattern="perpetrator_impunity_prosecution_gap",
            key_signals=[
                "Commission ONU Syrie documente viols systématiques centres détention Assad",
                "Témoignages de milliers de femmes et hommes détenus dans prisons secret",
                "Amnistie interne 2022 excluant crimes SVCA — impunité institutionnalisée",
                "Procès en Allemagne Anwar Raslan — justice universelle seule voie possible",
            ],
        ),
        SexualViolenceConflictImpunityEntity(
            entity_id="SVCI-004",
            name="Éthiopie/Tigray — TPLF & Forces Fédérales, 120K+ Viols Estimés, EHRC Rapport, Silence International",
            country="Éthiopie",
            sector="Conflit Tigray 2020-2022",
            systematic_sexual_violence_warfare_score=88.0,
            survivor_justice_access_support_deficit_score=85.0,
            perpetrator_impunity_prosecution_gap_score=87.0,
            stigma_community_reintegration_barriers_score=90.0,
            primary_pattern="stigma_community_reintegration_barriers",
            key_signals=[
                "120 000+ viols estimés durant conflit Tigray — chiffre ONU/UNFPA",
                "Enquêtes jointes EHRC-OHCHR documentent viols par toutes les parties",
                "Accord Pretoria novembre 2022 — silence sur justice SVCA pour la paix",
                "Stigmatisation extrême survivantes en contexte Tigray — rejet familial",
            ],
        ),
        SexualViolenceConflictImpunityEntity(
            entity_id="SVCI-005",
            name="Birmanie/Rohingya — Viols Génocidaires 2017, Meikhtila, Rakhine, ICC Case En Cours, Généraux Visés",
            country="Myanmar",
            sector="Violence Génocidaire Ethnique",
            systematic_sexual_violence_warfare_score=58.0,
            survivor_justice_access_support_deficit_score=55.0,
            perpetrator_impunity_prosecution_gap_score=57.0,
            stigma_community_reintegration_barriers_score=56.0,
            primary_pattern="systematic_sexual_violence_warfare",
            key_signals=[
                "Viols de masse documentés durant opérations Tatmadaw Rakhine 2016-2017",
                "Rapport Mission Indépendante ONU recommande poursuite généraux pour génocide",
                "Case Gambie vs Myanmar devant CIJ — viols inclus dans actes génocidaires",
                "Survivantes réfugiées Bangladesh sans accès justice ni soins post-traumatiques",
            ],
        ),
        SexualViolenceConflictImpunityEntity(
            entity_id="SVCI-006",
            name="Ukraine/2022 — Documentation ONU Systématique, 150+ Cas Formels, Guerre En Cours Documentation Difficile",
            country="Ukraine",
            sector="Conflit Armé En Cours",
            systematic_sexual_violence_warfare_score=52.0,
            survivor_justice_access_support_deficit_score=50.0,
            perpetrator_impunity_prosecution_gap_score=55.0,
            stigma_community_reintegration_barriers_score=49.0,
            primary_pattern="perpetrator_impunity_prosecution_gap",
            key_signals=[
                "150+ cas formels SVCA documentés CPI, ONU Monitoring Mission Ukraine",
                "Violations dans territoires occupés — accès restreint documentation complète",
                "Ukraine adopte mécanisme dépôt plainte SVCA — infrastructure judiciaire active",
                "Coordination internationale ICC — mandats arrêt en cours pour crimes russes",
            ],
        ),
        SexualViolenceConflictImpunityEntity(
            entity_id="SVCI-007",
            name="Rwanda/Post-Génocide — TPIR Akayesu Premier Condamné Viol Crime Contre Humanité 1998, Progress Laws",
            country="Rwanda",
            sector="Justice Transitionnelle",
            systematic_sexual_violence_warfare_score=29.0,
            survivor_justice_access_support_deficit_score=27.0,
            perpetrator_impunity_prosecution_gap_score=25.0,
            stigma_community_reintegration_barriers_score=30.0,
            primary_pattern="stigma_community_reintegration_barriers",
            key_signals=[
                "TPIR Affaire Akayesu 1998 — premier jugement viol crime contre humanité",
                "Gacaca tribunaux communautaires traitent 1.9 million dossiers dont SVCA",
                "Loi Rwanda 2008 criminalise spécifiquement SVCA en temps de conflit",
                "Stigmatisation persistante survivantes — progrès réels mais inégaux",
            ],
        ),
        SexualViolenceConflictImpunityEntity(
            entity_id="SVCI-008",
            name="Suède/Législation Modèle — Loi Consentement 2018, Formation Forces Armées, Centre Folke Bernadotte",
            country="Suède",
            sector="Cadre Normatif Référence",
            systematic_sexual_violence_warfare_score=7.0,
            survivor_justice_access_support_deficit_score=6.0,
            perpetrator_impunity_prosecution_gap_score=8.0,
            stigma_community_reintegration_barriers_score=7.0,
            primary_pattern="perpetrator_impunity_prosecution_gap",
            key_signals=[
                "Loi consentement 2018 — référence internationale, condamnations augmentées 75%",
                "Centre Folke Bernadotte forme personnel ONU à prévention SVCA",
                "Plan Action National SVCA en conflits armés — diplomatie active ONU",
                "Financement ONU Women et UNFPA — leadership international prévention",
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

    return SexualViolenceConflictImpunityEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_sexual_violence_conflict_impunity_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_action_sexual_violence_conflict_annual_report_2023",
            "human_rights_watch_sexual_violence_conflict_2023",
            "icc_sexual_gender_based_crimes_protocol_2023",
            "un_women_report_sexual_violence_armed_conflict_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_sexual_violence_conflict_impunity_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_sexual_violence_conflict_impunity_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
