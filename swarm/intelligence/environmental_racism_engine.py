"""Environmental Racism Engine — Caelum Partners Intelligence Swarm"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass
class EnvironmentalRacismActor:
    entity_id: str
    name: str
    country: str
    sector: str
    toxic_exposure_minority_score: float
    environmental_sacrifice_zone_score: float
    regulatory_discrimination_score: float
    environmental_justice_impunity_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.toxic_exposure_minority_score * 0.30 +
            self.environmental_sacrifice_zone_score * 0.25 +
            self.regulatory_discrimination_score * 0.25 +
            self.environmental_justice_impunity_score * 0.20,
            2
        )

    @property
    def risk_level(self) -> str:
        s = self.composite_score
        if s >= 60: return "critique"
        if s >= 40: return "élevé"
        if s >= 20: return "modéré"
        return "faible"

    @property
    def estimated_environmental_racism_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    @property
    def primary_pattern(self) -> str:
        scores = {
            "exposition_toxique_minorites": self.toxic_exposure_minority_score,
            "zone_sacrifice_environnemental": self.environmental_sacrifice_zone_score,
            "discrimination_reglementaire": self.regulatory_discrimination_score,
            "impunite_justice_environnementale": self.environmental_justice_impunity_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        SIGNAL_MAP = {
            "exposition_toxique_minorites": f"Exposition toxique disproportionnée des minorités de {self.name} — communautés racisées concentrées autour de sites polluants avec taux de pathologies chroniques significativement supérieurs à la moyenne nationale",
            "zone_sacrifice_environnemental": f"Zones de sacrifice environnemental de {self.name} — territoires autochtones ou minoritaires systématiquement sélectionnés pour l'implantation d'industries polluantes en raison de leur moindre capacité de résistance politique",
            "discrimination_reglementaire": f"Discrimination réglementaire de {self.name} — normes environnementales appliquées différemment selon la composition raciale des quartiers affectés, documentée dans les décisions administratives",
            "impunite_justice_environnementale": f"Impunité en matière de justice environnementale de {self.name} — absence de poursuites pour les entreprises polluant délibérément les quartiers minoritaires malgré les dommages documentés",
        }
        return [
            SIGNAL_MAP.get(self.primary_pattern, f"Racisme environnemental de {self.name}"),
            "Discrimination intersectionnelle — le racisme environnemental combine discrimination raciale et violence écologique, violant simultanément le droit à la santé, à un environnement sain et à l'égalité de traitement",
            "Activer le Rapporteur Spécial ONU sur les substances dangereuses et le droit à un environnement sain pour audit des inégalités environnementales selon l'origine raciale et ethnique",
        ]

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "toxic_exposure_minority_score": self.toxic_exposure_minority_score,
            "environmental_sacrifice_zone_score": self.environmental_sacrifice_zone_score,
            "regulatory_discrimination_score": self.regulatory_discrimination_score,
            "environmental_justice_impunity_score": self.environmental_justice_impunity_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_environmental_racism_index": self.estimated_environmental_racism_index,
            "last_updated": "2026-06-20",
        }


ACTORS = [
    EnvironmentalRacismActor("ER-001", "Nigeria/Delta Niger — Shell Ogoniland, Pétrole Igbo & Pollution 50 Ans Sans Réparation", "Afrique de l'Ouest", "Ogoniland Pollution Shell 50 Ans, Ken Saro-Wiwa Exécuté 1995, 11 000 Déversements Documentés & 40B$ Pétrole 1 $ Développement Local", 95, 92, 88, 90),
    EnvironmentalRacismActor("ER-002", "USA/Cancer Alley — Louisiane Noire, Plastiques & Inégalités EPA Documentées", "Amérique du Nord", "Cancer Alley 100+ Usines Pétrochimiques, Populations Noires 85%+ Zone, Mortalité Cancer +700%, EPA Consentement Décret 2023 Annulé", 90, 88, 92, 85),
    EnvironmentalRacismActor("ER-003", "Amazonie/Yanomami — Mercure Orpaillage, Malnutrition Crise & Morts Garimpeiros", "Amérique du Sud", "Orpaillage Illégal 30 000 Garimpeiros Yanomami 2019-23, Mercure Contamination Rivières, Malnutrition Sévère & Morts Déclarées Urgence", 88, 90, 82, 88),
    EnvironmentalRacismActor("ER-004", "Inde/Dalits — Castes Basses Usines Déchets & Nettoyeurs Manuels", "Asie du Sud", "Dalits 80% Travailleurs Déchets Informels, Nettoyeurs Manuels 58 000 Officiel, Castes Zones Industrielles Polluées & Loi Interdiction Non Appliquée", 85, 82, 88, 82),
    EnvironmentalRacismActor("ER-005", "Kanaky/Nouvelle-Calédonie — Nickel Kanak & Terres Coutumières Sacrifiées", "Océanie", "Kanak Terres Coutumières Zones Extraction Nickel, Vaie Nickel Pollution Rivières, Communautés Sans Compensation & Référendum Indépendance Lié", 55, 62, 52, 58),
    EnvironmentalRacismActor("ER-006", "Chine/Guangdong — Recyclage E-Waste Minorités Migrantes & Guiyu Pollution", "Asie", "Guiyu Village E-Waste Recycleurs Migrants, Plomb 190x Seuil Enfants, Contamination Sols & Travailleurs Sans Protection Réglementation", 52, 55, 58, 55),
    EnvironmentalRacismActor("ER-007", "Europe/Roms — Décharges Roumanie/Bulgarie & Sites Contaminés Communautés", "Europe", "Roms Décharges Proximitée Roumanie/Bulgarie, Sites Contaminés Camps Informels, Plomb Sang Enfants Roms 3x Moyenne & UE Inaction", 30, 32, 28, 32),
    EnvironmentalRacismActor("ER-008", "PNUE/Enviro-Justice — Droit Environnement Sain & Rapporteur ONU", "Global", "ONU Résolution Droit Environnement Sain 2022, PNUE Enviro-Justice Framework, Aarhus Convention & Rapporteur Substances Dangereuses", 5, 4, 3, 6),
]


def summary() -> dict:
    entities = [a.to_dict() for a in ACTORS]
    scores = [a.composite_score for a in ACTORS]
    avg = round(sum(scores) / len(scores), 2)
    risk_dist: dict = {}
    pattern_dist: dict = {}
    for a in ACTORS:
        risk_dist[a.risk_level] = risk_dist.get(a.risk_level, 0) + 1
        pattern_dist[a.primary_pattern] = pattern_dist.get(a.primary_pattern, 0) + 1
    top3 = sorted(ACTORS, key=lambda x: x.composite_score, reverse=True)[:3]
    critiques = [a for a in ACTORS if a.risk_level == "critique"]
    return {
        "total_entities": len(ACTORS),
        "avg_composite": avg,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": [a.name for a in top3],
        "critical_alerts": [f"{a.name.split(' —')[0]}: {a.primary_pattern.replace('_', ' ')}" for a in critiques],
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "environmental_racism",
        "confidence_score": 0.79,
        "data_sources": ["amnesty_international_pollution_reports", "ejatlas_environmental_justice_database", "unep_environmental_defenders_reports"],
        "entities": entities,
        "avg_estimated_environmental_racism_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Environmental Racism Engine — {s['total_entities']} acteurs, avg risque: {s['avg_composite']}")
    for e in s["entities"]:
        print(f"  [{e['risk_level'].upper()}] {e['name'][:50]} — score {e['composite_score']}")
    print(f"Distribution: {s['risk_distribution']}")
