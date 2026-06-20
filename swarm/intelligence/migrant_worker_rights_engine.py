"""Migrant Worker Rights Engine — Droits des travailleurs migrants & systèmes kafala/sponsorship."""

from dataclasses import dataclass
from typing import List


@dataclass
class MigrantWorkerRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    wage_theft_exploitation_score: float
    recruitment_fee_debt_score: float
    kafala_system_dependency_score: float
    labor_rights_access_failure_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.wage_theft_exploitation_score * 0.30
            + self.recruitment_fee_debt_score * 0.25
            + self.kafala_system_dependency_score * 0.25
            + self.labor_rights_access_failure_score * 0.20,
            2,
        )

    @property
    def risk_level(self) -> str:
        s = self.composite_score
        if s >= 60:
            return "critique"
        if s >= 40:
            return "élevé"
        if s >= 20:
            return "modéré"
        return "faible"

    @property
    def primary_pattern(self) -> str:
        scores = {
            "vol_salaires_exploitation": self.wage_theft_exploitation_score,
            "dette_frais_recrutement": self.recruitment_fee_debt_score,
            "dependance_systeme_kafala": self.kafala_system_dependency_score,
            "exclusion_droits_travail": self.labor_rights_access_failure_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        return [
            f"Exploitation des travailleurs migrants documentée — {self.name} avec score composite {self.composite_score}/100 révélant des violations des Conventions OIT C97/C143 sur les travailleurs migrants et du Protocole de Palerme",
            f"Système Kafala/Sponsorship ({self.kafala_system_dependency_score}/100) — le système de parrainage crée une dépendance totale de l'employeur empêchant les travailleurs migrants de changer d'emploi ou de quitter le pays",
            f"Activer le Rapporteur Spécial ONU sur les droits des migrants pour enquête sur le système Kafala et exiger la ratification par les États du Golfe des Conventions OIT C87/C98 sur la liberté syndicale",
        ]

    @property
    def estimated_migrant_worker_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "wage_theft_exploitation_score": self.wage_theft_exploitation_score,
            "recruitment_fee_debt_score": self.recruitment_fee_debt_score,
            "kafala_system_dependency_score": self.kafala_system_dependency_score,
            "labor_rights_access_failure_score": self.labor_rights_access_failure_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_migrant_worker_rights_index": self.estimated_migrant_worker_rights_index,
            "last_updated": "2026-06-20",
        }


class MigrantWorkerRightsEngine:
    ENGINE_VERSION = "1.0.0"
    CONFIDENCE_SCORE = 0.82
    DATA_SOURCES = [
        "ilo_global_estimates_international_migrant_workers",
        "migrant_forum_asia_recruitment_fees_database",
        "business_human_rights_resource_centre_migrant_reports",
    ]

    def __init__(self):
        self.entities: List[MigrantWorkerRightsEntity] = [
            MigrantWorkerRightsEntity(
                "MW-001", "Qatar/FIFA — Kafala Système, 6 500+ Morts Travailleurs Migrants & Stades Coupe 2022",
                "MENA",
                "Qatar 6 500+ Morts Travailleurs Migrants Stades FIFA 2010-22 Estimation Guardian, Kafala Système Captivité, Passeports Confisqués & Réformes 2021 Insuffisantes ILO",
                92, 88, 95, 88,
            ),
            MigrantWorkerRightsEntity(
                "MW-002", "Golfe Arabe/Kafala — EAU/KSA/Koweït 25M Travailleurs Captifs Système Parrainage",
                "MENA",
                "25M Travailleurs Migrants Golfe Système Kafala EAU/KSA/Koweït/Bahreïn, Changement Emploi Interdit, Travailleuses Domestiques Exclues Code Travail & Réformes Cosmétiques",
                88, 85, 92, 85,
            ),
            MigrantWorkerRightsEntity(
                "MW-003", "Malaisie/Top Glove — Travailleurs Migrants Captifs, Palm Oil & Gants Pandémie COVID",
                "Asie du Sud-Est",
                "Top Glove Malaisie Gants Latex 10 000 Travailleurs Migrants Logements Surpeuplés, Frais Recrutement 3 000$, Palm Oil Travailleurs Népalais/Bangladeshis & Sanctions USA 2020",
                85, 90, 85, 82,
            ),
            MigrantWorkerRightsEntity(
                "MW-004", "USA/H-2A H-2B — Visa Sponsorship Captivité, Abus Agricoles & Frais Recrutement",
                "Amérique du Nord",
                "USA H-2A H-2B Visa Workers 300 000/An, Captivité Sponsor Changement Emploi Difficile, Abus Agricoles Saisonniers EWA & Frais Recrutement Mexique/Guatemala",
                82, 85, 80, 85,
            ),
            MigrantWorkerRightsEntity(
                "MW-005", "Thaïlande/Pêche Maritime — Esclavage Bateaux Haute Mer, ILO C188 & GFW Rapport",
                "Asie du Sud-Est",
                "Thaïlande Pêche Maritime Travailleurs Migrants Myanmar/Cambodge Esclavage Bateaux, Pêche Haute Mer Hors Portée Inspection, AP Enquête 2015 & ILO C188 Non-Ratifié",
                55, 52, 58, 50,
            ),
            MigrantWorkerRightsEntity(
                "MW-006", "Italie/Caporalato — Travailleurs Africains Agriculture, Travail Forcé & Loi 2016",
                "Europe de l'Ouest",
                "Italie Caporalato Système Intermédiaires Exploitation Travailleurs Migrants Africains Agriculture, Muerte Agriculteurs Sans Eau/Soleil, Loi 199/2016 Anti-Caporalato & Application Lacunaire",
                52, 48, 55, 55,
            ),
            MigrantWorkerRightsEntity(
                "MW-007", "Allemagne/Travailleurs Saisonniers — COVID Tönnies Abattoir, Logements & Saisonnier",
                "Europe de l'Ouest",
                "Allemagne Tönnies Abattoir COVID 1 500 Infectés Travailleurs Roumains 2020, Logements Surpeuplés, Travailleurs Saisonniers UE Contrats & AEntG Arbeitnehmer-Entsendegesetz Lacunes",
                30, 28, 32, 28,
            ),
            MigrantWorkerRightsEntity(
                "MW-008", "OIT/ITUC — Convention 189 Domestiques, C97 Migrants Travailleurs & MOU Bilatéraux",
                "Global",
                "OIT Convention 189 Travailleurs Domestiques 2011, C97 Travailleurs Migrants, ITUC Rapports Syndicalisation Migrants & MOU Bilatéraux Philippines/Sri Lanka Golfe",
                5, 4, 3, 6,
            ),
        ]

    def summary(self) -> dict:
        data = [e.to_dict() for e in self.entities]
        avg = round(sum(e.composite_score for e in self.entities) / len(self.entities), 2)
        risk_dist: dict = {}
        pattern_dist: dict = {}
        for e in self.entities:
            risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
            pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1
        critical = [e for e in self.entities if e.risk_level == "critique"]
        return {
            "total_entities": len(self.entities),
            "avg_composite": avg,
            "risk_distribution": risk_dist,
            "pattern_distribution": pattern_dist,
            "top_risk_entities": [e.name for e in sorted(critical, key=lambda x: -x.composite_score)[:3]],
            "critical_alerts": [f"{e.name}: {e.primary_pattern}" for e in critical],
            "last_analysis": "2026-06-20",
            "engine_version": self.ENGINE_VERSION,
            "domain": "migrant_worker_rights",
            "confidence_score": self.CONFIDENCE_SCORE,
            "data_sources": self.DATA_SOURCES,
            "entities": data,
            "avg_estimated_migrant_worker_rights_index": round(avg / 100 * 10, 2),
        }


if __name__ == "__main__":
    import json
    engine = MigrantWorkerRightsEngine()
    result = engine.summary()
    print(json.dumps({
        "total": result["total_entities"],
        "avg": result["avg_composite"],
        "distribution": result["risk_distribution"],
        "top3": result["top_risk_entities"],
    }, indent=2, ensure_ascii=False))
    for e in engine.entities:
        print(f"  {e.entity_id}: {e.composite_score:.2f} → {e.risk_level}")
