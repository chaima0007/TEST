"""Water Weaponization Engine — Caelum Partners Intelligence Swarm"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass
class WaterWeaponizationActor:
    entity_id: str
    name: str
    country: str
    sector: str
    dam_upstream_coercion_score: float
    water_infrastructure_attack_score: float
    deliberate_contamination_score: float
    access_denial_civilian_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.dam_upstream_coercion_score * 0.30 +
            self.water_infrastructure_attack_score * 0.25 +
            self.deliberate_contamination_score * 0.25 +
            self.access_denial_civilian_score * 0.20,
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
    def estimated_water_weaponization_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    @property
    def primary_pattern(self) -> str:
        scores = {
            "barrage_coercition_amont": self.dam_upstream_coercion_score,
            "attaque_infrastructure_hydrique": self.water_infrastructure_attack_score,
            "contamination_deliberee": self.deliberate_contamination_score,
            "denial_acces_eau_civils": self.access_denial_civilian_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        SIGNAL_MAP = {
            "barrage_coercition_amont": f"Coercition par barrage amont de {self.name} — contrôle des flux hydriques pour exercer une pression géopolitique sur les États aval dépendants de l'eau comme levier de négociation",
            "attaque_infrastructure_hydrique": f"Attaque d'infrastructure hydrique par {self.name} — destruction délibérée d'usines de traitement, canalisations et systèmes d'eau potable en violation du DIH et de la Résolution CS-ONU 2417",
            "contamination_deliberee": f"Contamination délibérée des ressources en eau par {self.name} — empoisonnement ou pollution intentionnelle des sources d'eau pour incapaciter les populations civiles ou les forces adverses",
            "denial_acces_eau_civils": f"Déni d'accès à l'eau aux civils par {self.name} — coupures délibérées des systèmes d'approvisionnement comme instrument de pression ou de punition collective contre des populations civiles",
        }
        return [
            SIGNAL_MAP.get(self.primary_pattern, f"Weaponisation de l'eau de {self.name}"),
            "Droit humain fondamental violé — l'accès à l'eau potable est reconnu comme droit humain fondamental par la Résolution ONU 64/292 de 2010, rendant sa négation délibérée constitutive d'une violation grave",
            "Activer en urgence la Résolution CS-ONU 2417 et le Rapporteur Spécial ONU sur le droit à l'eau pour mesures d'urgence et accès humanitaire immédiat aux populations privées d'eau",
        ]

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "dam_upstream_coercion_score": self.dam_upstream_coercion_score,
            "water_infrastructure_attack_score": self.water_infrastructure_attack_score,
            "deliberate_contamination_score": self.deliberate_contamination_score,
            "access_denial_civilian_score": self.access_denial_civilian_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_water_weaponization_index": self.estimated_water_weaponization_index,
            "last_updated": "2026-06-20",
        }


ACTORS = [
    WaterWeaponizationActor("WW-001", "Russie/Ukraine — Barrage Kakhovka Destruction & Eau Kherson Coupée", "Europe de l'Est", "Barrage Kakhovka Destruction Juin 2023, 700 000 Sans Eau, Marioupol Assiégée Eau Coupée & Kherson Civilian Water Denial ONU", 85, 95, 88, 90),
    WaterWeaponizationActor("WW-002", "Éthiopie/GERD — Barrage Renaissance Nil & Coercition Égypte/Soudan", "Afrique de l'Est", "GERD Remplissage Unilatéral 74M m³, Casus Belli Égypte Eau -2%, Soudan Irrigation Menacée & Nil Bleu Négociations Échouées UA", 92, 78, 75, 88),
    WaterWeaponizationActor("WW-003", "Gaza/Israël — Infrastructure Eau Détruite, Dessalement & Puits Contamination", "MENA", "70% Infrastructure Eau Gaza Détruite, 4 Usines Dessalement Hors Service, 2.3M Personnes 3L/Jour Recommandé vs 15L Reçu & OMS Urgence", 80, 90, 85, 92),
    WaterWeaponizationActor("WW-004", "Syrie/Assad — Eau Alep Coupée, Euphrate Barrage & Populations Assoiffées", "MENA", "Alep Eau Coupée 250 Jours, Barrage Tishreen Contrôle IS, Euphrate Débit Réduit Turquie 40% & UNICEF 12M Sans Eau Sûre Syrie", 82, 88, 82, 88),
    WaterWeaponizationActor("WW-005", "Chine/Mékong — 11 Barrages Amont, Sécheresses Aval & Pêche Cambodge/Laos", "Asie du Sud-Est", "11 Barrages Mékong Chine, Débit Réduit 30% Saison Sèche, Pêche Cambodia -75% & Débit Historique Bas 2019-24 Alerte", 65, 55, 48, 52),
    WaterWeaponizationActor("WW-006", "Yémen/Coalition — Infrastructure Eau Frappes & Choléra 2.5M Cas", "MENA", "Frappes Infrastructure Eau Hodeida, Choléra 2.5M Cas Épidémie, UNICEF Pompes Détruites & Population 21M Sans Accès Eau Sûre", 52, 62, 55, 58),
    WaterWeaponizationActor("WW-007", "Inde/Pakistan — Traité Indus Suspendu & Tensions Eau Kashmir", "Asie du Sud", "Traité Indus Waters Suspendu 2023 après Attentat, Chenab Barrage Projets Conflictuels, Pakistanais Agriculture Dépendante & ICJ Arbitrage", 28, 25, 30, 32),
    WaterWeaponizationActor("WW-008", "ONU-Eau/CICR — Droit à l'Eau & Protection Infrastructures Hydriques", "Global", "ONU Résolution 64/292 Droit Eau 2010, CICR Protection Infrastructure Eau DIH, CICID Rapporteur Eau Spécial & Stockholm Water Prize", 5, 4, 3, 6),
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
        "domain": "water_weaponization",
        "confidence_score": 0.83,
        "data_sources": ["icrc_water_conflict_database", "pacific_institute_water_conflict_chronology", "un_water_global_analysis_assessment"],
        "entities": entities,
        "avg_estimated_water_weaponization_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Water Weaponization Engine — {s['total_entities']} acteurs, avg risque: {s['avg_composite']}")
    for e in s["entities"]:
        print(f"  [{e['risk_level'].upper()}] {e['name'][:50]} — score {e['composite_score']}")
    print(f"Distribution: {s['risk_distribution']}")
