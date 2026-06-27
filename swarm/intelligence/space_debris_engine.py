"""
Module 370 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
Space Debris & Kessler Syndrome Intelligence Engine
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class SpaceDebrisInput:
    entity_id: str
    name: str
    country: str
    sector: str
    debris_density_score: float            # 0-1
    collision_probability_score: float     # 0-1
    deorbit_compliance_gap_score: float    # 0-1
    satellite_operator_risk_score: float   # 0-1


@dataclass
class SpaceDebrisResult:
    entity_id: str
    name: str
    country: str
    sector: str
    score1: float
    score2: float
    score3: float
    score4: float
    composite_score: float
    risk_level: str
    primary_pattern: str
    key_signals: str
    recommended_action: str
    estimated_kessler_index: float
    last_updated: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "score1": self.score1,
            "score2": self.score2,
            "score3": self.score3,
            "score4": self.score4,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "recommended_action": self.recommended_action,
            "estimated_kessler_index": self.estimated_kessler_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES_RAW = [
    # SDE-001 — critique — États-Unis (debris>=0.85, collision>=0.80 => kessler_onset)
    # composite = 0.90*30 + 0.88*25 + 0.82*25 + 0.76*20 = 27+22+20.5+15.2 = 84.7
    {"id": "SDE-001", "name": "SpaceX Starlink LEO Operations", "country": "États-Unis", "sector": "operateur_mega_constellation",
     "s1": 0.90, "s2": 0.88, "s3": 0.82, "s4": 0.76},
    # SDE-002 — critique — Russie (collision>=0.85, deorbit>=0.80 => collision_cascade)
    # composite = 0.82*30 + 0.88*25 + 0.85*25 + 0.76*20 = 24.6+22+21.25+15.2 = 83.05
    {"id": "SDE-002", "name": "Roscosmos Debris Management", "country": "Russie", "sector": "agence_spatiale",
     "s1": 0.82, "s2": 0.88, "s3": 0.85, "s4": 0.76},
    # SDE-003 — critique — Chine (deorbit>=0.85, operator>=0.80 => asat_debris_field)
    # composite = 0.78*30 + 0.80*25 + 0.88*25 + 0.85*20 = 23.4+20+22+17 = 82.4
    {"id": "SDE-003", "name": "CNSA Space Debris Command", "country": "Chine", "sector": "agence_spatiale",
     "s1": 0.78, "s2": 0.80, "s3": 0.88, "s4": 0.85},
    # SDE-004 — eleve — UE/ESA
    # composite = 0.58*30 + 0.55*25 + 0.60*25 + 0.50*20 = 17.4+13.75+15+10 = 56.15
    {"id": "SDE-004", "name": "ESA Space Safety Programme", "country": "Europe", "sector": "agence_spatiale",
     "s1": 0.58, "s2": 0.55, "s3": 0.60, "s4": 0.50},
    # SDE-005 — eleve — Japon
    # composite = 0.52*30 + 0.50*25 + 0.55*25 + 0.55*20 = 15.6+12.5+13.75+11 = 52.85
    {"id": "SDE-005", "name": "JAXA Space Debris Research", "country": "Japon", "sector": "agence_spatiale",
     "s1": 0.52, "s2": 0.50, "s3": 0.55, "s4": 0.55},
    # SDE-006 — modere — Inde
    # composite = 0.35*30 + 0.30*25 + 0.32*25 + 0.28*20 = 10.5+7.5+8+5.6 = 31.6
    {"id": "SDE-006", "name": "ISRO Space Situational Awareness", "country": "Inde", "sector": "agence_spatiale",
     "s1": 0.35, "s2": 0.30, "s3": 0.32, "s4": 0.28},
    # SDE-007 — faible — Canada
    # composite = 0.12*30 + 0.10*25 + 0.14*25 + 0.10*20 = 3.6+2.5+3.5+2 = 11.6
    {"id": "SDE-007", "name": "MDA Space Debris Monitoring", "country": "Canada", "sector": "industrie_spatiale",
     "s1": 0.12, "s2": 0.10, "s3": 0.14, "s4": 0.10},
    # SDE-008 — faible — Royaume-Uni
    # composite = 0.10*30 + 0.12*25 + 0.10*25 + 0.14*20 = 3+3+2.5+2.8 = 11.3
    {"id": "SDE-008", "name": "UK Space Agency Debris Division", "country": "Royaume-Uni", "sector": "agence_spatiale",
     "s1": 0.10, "s2": 0.12, "s3": 0.10, "s4": 0.14},
]


def _calc_scores(raw: dict):
    s1 = round(raw["s1"] * 100 * 100) / 100
    s2 = round(raw["s2"] * 100 * 100) / 100
    s3 = round(raw["s3"] * 100 * 100) / 100
    s4 = round(raw["s4"] * 100 * 100) / 100
    comp = round((s1 * 0.30 + s2 * 0.25 + s3 * 0.25 + s4 * 0.20) * 100) / 100
    return s1, s2, s3, s4, comp


def _risk_level(comp: float) -> str:
    if comp >= 60: return "critique"
    if comp >= 40: return "eleve"
    if comp >= 20: return "modere"
    return "faible"


def _primary_pattern(raw: dict) -> str:
    if raw["s1"] >= 0.85 and raw["s2"] >= 0.80: return "kessler_onset"
    if raw["s2"] >= 0.85 and raw["s3"] >= 0.80: return "collision_cascade"
    if raw["s3"] >= 0.85 and raw["s4"] >= 0.80: return "asat_debris_field"
    if raw["s2"] >= 0.70 and raw["s3"] >= 0.65: return "mega_constellation_saturation"
    if raw["s3"] >= 0.70 and raw["s4"] >= 0.65: return "governance_remediation_failure"
    return "none"


def _recommended_action(risk: str) -> str:
    if risk == "critique": return "intervention_urgente_debris_orbitaux_critiques"
    if risk == "eleve": return "retrait_debris_actifs_accelere"
    if risk == "modere": return "renforcement_gouvernance_orbitale"
    return "veille_debris_spatiaux_continue"


def _key_signals(risk: str, pattern: str, comp: float) -> str:
    labels = {
        "kessler_onset": "Déclenchement syndrome Kessler",
        "collision_cascade": "Cascade collisions orbitales",
        "asat_debris_field": "Champ de débris ASAT",
        "mega_constellation_saturation": "Saturation méga-constellation",
        "governance_remediation_failure": "Défaillance gouvernance et remédiation",
        "none": "Débris sous surveillance",
    }
    label = labels.get(pattern, pattern)
    if risk == "critique": return f"Crise débris orbitaux systémique — {label} — composite {comp:.1f}"
    if risk == "eleve": return f"Crise débris majeure — {label} — composite {comp:.1f}"
    if risk == "modere": return f"Saturation orbitale structurelle — {label} — composite {comp:.1f}"
    return f"Débris spatiaux surveillés — composite {comp:.1f}"


def analyze_space(raw: dict) -> dict:
    from datetime import datetime
    s1, s2, s3, s4, comp = _calc_scores(raw)
    risk = _risk_level(comp)
    pattern = _primary_pattern(raw)
    return {
        "entity_id": raw["id"],
        "name": raw["name"],
        "country": raw["country"],
        "sector": raw["sector"],
        "score1": s1,
        "score2": s2,
        "score3": s3,
        "score4": s4,
        "composite_score": comp,
        "risk_level": risk,
        "primary_pattern": pattern,
        "key_signals": _key_signals(risk, pattern, comp),
        "recommended_action": _recommended_action(risk),
        "estimated_kessler_index": round(comp / 100 * 10 * 100) / 100,
        "last_updated": datetime.utcnow().isoformat(),
    }


def summary(entities: list) -> dict:
    n = len(entities)
    risk_dist: Dict[str, int] = {}
    pattern_dist: Dict[str, int] = {}
    total_comp = 0.0
    total_idx = 0.0
    top_risk = []
    critical_alerts = []
    for e in entities:
        risk_dist[e["risk_level"]] = risk_dist.get(e["risk_level"], 0) + 1
        pattern_dist[e["primary_pattern"]] = pattern_dist.get(e["primary_pattern"], 0) + 1
        total_comp += e["composite_score"]
        total_idx += e["estimated_kessler_index"]
        if e["risk_level"] == "critique":
            top_risk.append({"entity_id": e["entity_id"], "name": e["name"], "composite_score": e["composite_score"]})
            critical_alerts.append(e["key_signals"])
    avg_comp = round(total_comp / n * 100) / 100 if n else 0.0
    avg_idx = round(total_idx / n * 100) / 100 if n else 0.0
    return {
        "total_entities": n,
        "avg_composite": avg_comp,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": top_risk,
        "critical_alerts": critical_alerts,
        "engine_version": "370.2.0",
        "domain": "space",
        "confidence_score": 0.90,
        "data_sources": ["SpaceX", "Roscosmos", "CNSA", "ESA", "JAXA", "ISRO", "MDA", "UKSA"],
        "avg_estimated_kessler_index": avg_idx,
    }


class SpaceDebrisEngine:
    """Module 370 — Space Debris & Kessler Syndrome Intelligence Engine"""

    def analyze(self, entities: List[Dict]) -> Dict[str, Any]:
        results = [analyze_space(e) for e in entities]
        return summary(results)

    def get_mock_data(self) -> Dict[str, Any]:
        entities = [analyze_space(raw) for raw in MOCK_ENTITIES_RAW]
        result = summary(entities)
        result["entities"] = entities
        return result
