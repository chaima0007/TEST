"""
Caelum Partners — Sex Work Criminalization & Trafficking Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Criminalisation du travail sexuel, traite des êtres humains, droits des travailleuses du sexe,
modèles réglementaires comparatifs.

La crimininalisation du travail sexuel génère des conditions structurelles qui exposent les
travailleuses et travailleurs du sexe à la violence, à l'exploitation et à la traite. Selon
l'ONUDC, 79% des victimes de traite des êtres humains à des fins d'exploitation sexuelle sont
des femmes et des filles. Le débat réglementaire oppose trois approches principales : la
criminalisation totale, la décriminalisation (modèle néo-zélandais), et le modèle nordique
(criminalisation du client uniquement).

Amnesty International (2016) et l'OMS recommandent la décriminalisation complète du travail
sexuel comme mesure de santé publique et de protection des droits humains. À l'inverse,
l'exploitation sexuelle forcée et la traite constituent des violations graves des droits humains,
documentées dans des pays où la demande touristique, la pauvreté et l'impunité créent des
conditions favorables au crime organisé.

La distinction entre travail sexuel consenti et traite est centrale : les approches qui
criminalisent indistinctement marginalisent les personnes qui choisissent ce travail tout
en rendant les victimes de traite encore plus vulnérables.

Risk levels (criminalisation travail sexuel et traite) :
  critique  -> composite >= 60  (traite systémique — exploitation forcée, crime organisé, impunité)
  élevé     -> composite >= 40  (criminalisation — stigmatisation, violence, accès soins réduit)
  modéré    -> composite >= 20  (régulation partielle — zones grises, droits incomplets)
  faible    -> composite < 20   (modèle droits — décriminalisation, protection, accès santé)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class SexWorkCriminalizationTraffickingEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    trafficking_exploitation_score: float
    criminalization_harm_score: float
    impunity_law_enforcement_score: float
    victim_vulnerability_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_sex_work_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.trafficking_exploitation_score * 0.30
            + self.criminalization_harm_score * 0.25
            + self.impunity_law_enforcement_score * 0.25
            + self.victim_vulnerability_score * 0.20,
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
        self.estimated_sex_work_rights_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "trafficking_exploitation_score": self.trafficking_exploitation_score,
            "criminalization_harm_score": self.criminalization_harm_score,
            "impunity_law_enforcement_score": self.impunity_law_enforcement_score,
            "victim_vulnerability_score": self.victim_vulnerability_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_sex_work_rights_index": self.estimated_sex_work_rights_index,
            "last_updated": self.last_updated,
        }


@dataclass
class SexWorkCriminalizationTraffickingEngineResult:
    agent: str = "Sex Work Criminalization & Trafficking Engine Agent"
    domain: str = "sex_work_criminalization_trafficking"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_sex_work_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SexWorkCriminalizationTraffickingEntity] = field(default_factory=list)


def run_sex_work_criminalization_trafficking_engine() -> SexWorkCriminalizationTraffickingEngineResult:
    entities = [
        SexWorkCriminalizationTraffickingEntity(
            entity_id="SWT-001",
            name="République Dominicaine/Tourisme Sexuel Enfants — ONUDC 100 000 Victimes Mineures, Resorts Complicité, Impunité Systémique",
            country="République Dominicaine",
            sector="Tourisme Sexuel Exploitation Mineurs",
            trafficking_exploitation_score=92.0,
            criminalization_harm_score=88.0,
            impunity_law_enforcement_score=90.0,
            victim_vulnerability_score=86.0,
            primary_pattern="trafficking_exploitation",
            key_signals=[
                "ONUDC rapport 2021 : 100 000+ victimes mineures exploitation sexuelle tourisme — Boca Chica, Sosúa",
                "Chaînes hôtelières complicité passive : touristes sexuels protégés, mineurs recrutés à l'entrée",
                "Loi 137-03 anti-traite 2003 : non-appliquée, poursuites rares, corruption forces ordre",
                "ECPAT International : RD classée zone rouge tourisme sexuel enfants Caraïbes — 3e mondiale",
            ],
        ),
        SexWorkCriminalizationTraffickingEntity(
            entity_id="SWT-002",
            name="Nigeria/Benin City Traite EU — 40 000 Femmes Edo Trafiquées Europe/An, Madams, Juju Serment, Dette Bondage",
            country="Nigeria",
            sector="Traite Internationale Crime Organisé",
            trafficking_exploitation_score=90.0,
            criminalization_harm_score=82.0,
            impunity_law_enforcement_score=86.0,
            victim_vulnerability_score=88.0,
            primary_pattern="trafficking_exploitation",
            key_signals=[
                "Benin City hub traite : 40 000 femmes Edo State trafiquées vers Europe annuellement estimé EUROPOL",
                "Madams (formatrices) : recrutement villages, serment juju fetish, dette 30 000-50 000 EUR à rembourser",
                "Route Libye-Méditerranée : transit viols, vente marchés Libye, arrivée Italie-Espagne-France",
                "NAPTIP Nigeria : 12 000 victimes identifiées 2020, 500 condamnations — iceberg systémique",
            ],
        ),
        SexWorkCriminalizationTraffickingEntity(
            entity_id="SWT-003",
            name="Thaïlande/Pattaya Traite Déguisée — 250 000 Travailleuses Sexuelles, Industrie 6.4Mds USD, Proxénétisme Crime Organisé",
            country="Thaïlande",
            sector="Industrie Sexuelle Traite Masquée",
            trafficking_exploitation_score=78.0,
            criminalization_harm_score=72.0,
            impunity_law_enforcement_score=80.0,
            victim_vulnerability_score=74.0,
            primary_pattern="impunity_law_enforcement",
            key_signals=[
                "Industrie sexuelle Thaïlande : 6.4 milliards USD/an — 250 000 à 300 000 personnes estimées OIT",
                "Pattaya/Bangkok/Phuket : gogo bars, massage 'happy ending', karaoke — travail légal en apparence",
                "Traite Myanmar, Cambodge, Laos : 30% travailleurs sexuels étrangers — dette migration, contrôle passeport",
                "Prevention and Suppression of Prostitution Act 1996 : prostitution illégale mais tolérance officielle",
            ],
        ),
        SexWorkCriminalizationTraffickingEntity(
            entity_id="SWT-004",
            name="Inde/Sonagachi 100 000 Travailleurs Sexuels Stigmatisés — Durbar Mahila Samanwaya Résistance, SIDA, Criminalisation",
            country="Inde",
            sector="Travail Sexuel Stigmatisation Criminalisation Partielle",
            trafficking_exploitation_score=65.0,
            criminalization_harm_score=70.0,
            impunity_law_enforcement_score=68.0,
            victim_vulnerability_score=72.0,
            primary_pattern="criminalization_harm",
            key_signals=[
                "Sonagachi Kolkata : 100 000 travailleurs sexuels — plus grand quartier rouge Asie du Sud",
                "ITPA 1956 : sollicitation illégale — police extorsion systématique, violences documentées HRW",
                "Durbar Mahila Samanwaya Committee : syndicat 65 000 membres, programme VIH réduction risques",
                "Prévalence VIH Sonagachi réduite à 5% grâce programme pair-éducateurs — modèle OMS cité",
            ],
        ),
        SexWorkCriminalizationTraffickingEntity(
            entity_id="SWT-005",
            name="Corée du Sud/Criminalisation 2004 Stigmate — Special Law Anti-Prostitution, 140 000 Travailleuses Marginalisées, Violence",
            country="Corée du Sud",
            sector="Criminalisation Post-2004 Effets Pervers",
            trafficking_exploitation_score=38.0,
            criminalization_harm_score=58.0,
            impunity_law_enforcement_score=42.0,
            victim_vulnerability_score=45.0,
            primary_pattern="criminalization_harm",
            key_signals=[
                "Loi Spéciale Anti-Prostitution 2004 : criminalisation complète — prostitution et clients sanctionnés",
                "Post-2004 : 140 000 travailleuses déplacées vers internet, hôtels love, lieux non déclarés plus dangereux",
                "Korea Women's Development Institute 2016 : violence des clients augmentée 40% post-criminalisation",
                "Criminalisation des victimes traite aussi : arrestations travailleuses sexuelles migrants — ONG condamnent",
            ],
        ),
        SexWorkCriminalizationTraffickingEntity(
            entity_id="SWT-006",
            name="Pays-Bas/Légalisation Zones Contrôlées — Fenêtres Amsterdam, Traite Résiduelle, Projet 1012 Fermeture 40% Fenêtres",
            country="Pays-Bas",
            sector="Légalisation Zones Contrôlées Régulation",
            trafficking_exploitation_score=48.0,
            criminalization_harm_score=46.0,
            impunity_law_enforcement_score=52.0,
            victim_vulnerability_score=44.0,
            primary_pattern="trafficking_exploitation",
            key_signals=[
                "Légalisation proxénétisme 2000 : travail sexuel réglementé, licences, contrôles santé obligatoires",
                "Projet 1012 Amsterdam : fermeture 40% fenêtres 2007-2013 — gentrification, pas réduction traite",
                "Politie rapport 2018 : 50-90% travailleuses fenêtres issues pays est-européens en situation contrainte",
                "Traite résiduelle : demande légale crée écran pour exploitation — ONG signalent ambivalence modèle",
            ],
        ),
        SexWorkCriminalizationTraffickingEntity(
            entity_id="SWT-007",
            name="Suède/Modèle Nordic Client Criminalisé — Sex Purchase Act 1999, Réduction Demande 50%, Modèle Exporté EU",
            country="Suède",
            sector="Modèle Nordique Criminalisation Client",
            trafficking_exploitation_score=22.0,
            criminalization_harm_score=30.0,
            impunity_law_enforcement_score=24.0,
            victim_vulnerability_score=26.0,
            primary_pattern="criminalization_harm",
            key_signals=[
                "Sex Purchase Act 1999 : achat sexe illégal, vente légale — modèle exporté Norvège, Islande, France",
                "Évaluation 2010 : réduction prostitution de rue 50%, traite stabilisée — débat impact réel complexe",
                "Travailleuses sexuelles critiquent : clients méfiants, moins temps négocier sécurité, prix baissés",
                "ICRSE 2018 : travailleuses sexuelles excluent du débat — modèle imposé sans leur consultation",
            ],
        ),
        SexWorkCriminalizationTraffickingEntity(
            entity_id="SWT-008",
            name="Nouvelle-Zélande/Prostitution Reform Act 2003 Modèle — Décriminalisation, Droits Travailleurs, Santé, Accès Justice",
            country="Nouvelle-Zélande",
            sector="Décriminalisation Modèle Droits",
            trafficking_exploitation_score=5.0,
            criminalization_harm_score=4.0,
            impunity_law_enforcement_score=6.0,
            victim_vulnerability_score=5.0,
            primary_pattern="victim_vulnerability",
            key_signals=[
                "Prostitution Reform Act 2003 : décriminalisation complète — travail sexuel = travail comme autre",
                "Évaluation 2008 Comité Review : accès santé amélioré, violence réduite, liens police normalisés",
                "Travailleuses droit santé travail, accident travail, syndicat — NZPC défend droits 23 ans",
                "Amnesty International 2016 cite NZ comme modèle — OMS recommande décriminalisation globale",
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

    return SexWorkCriminalizationTraffickingEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_sex_work_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unodc_global_report_trafficking_persons_2022",
            "europol_trafficking_sexual_exploitation_nigeria_report_2021",
            "amnesty_international_sex_work_decriminalization_2016",
            "who_hiv_prevention_sex_workers_global_guidance_2012",
            "ecpat_international_child_sexual_exploitation_tourism_2022",
            "nz_prostitution_law_review_committee_report_2008",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_sex_work_criminalization_trafficking_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_sex_work_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}] — {e.name[:60]}")
