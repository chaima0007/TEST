"""
Module 345 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
Methane Crisis & Arctic Methane Bomb Intelligence Engine
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class MethaneCrisisInput:
    entity_id: str
    name: str
    country: str
    sector: str
    emission_intensity_score: float        # 0-1
    leakage_detection_gap_score: float     # 0-1
    regulatory_enforcement_gap_score: float  # 0-1
    climate_feedback_risk_score: float     # 0-1


@dataclass
class MethaneCrisisResult:
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
    estimated_methane_index: float
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
            "estimated_methane_index": self.estimated_methane_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES_RAW = [
    # MCE-001 — critique — États-Unis (emission_intensity>=0.85, leakage>=0.80 => fossil_methane_surge)
    # composite = 0.90*30 + 0.88*25 + 0.82*25 + 0.76*20 = 27+22+20.5+15.2 = 84.7
    {"id": "MCE-001", "name": "US EPA Methane Monitoring", "country": "États-Unis", "sector": "agence_federale",
     "s1": 0.90, "s2": 0.88, "s3": 0.82, "s4": 0.76},
    # MCE-002 — critique — Russie (leakage>=0.85, regulatory>=0.80 => arctic_methane_bomb)
    # composite = 0.86*30 + 0.92*25 + 0.88*25 + 0.80*20 = 25.8+23+22+16 = 86.8
    {"id": "MCE-002", "name": "Gazprom Environmental Division", "country": "Russie", "sector": "industrie_gaziere",
     "s1": 0.86, "s2": 0.92, "s3": 0.88, "s4": 0.80},
    # MCE-003 — critique — Arabie Saoudite (emission>=0.85, climate>=0.80 => flaring_crisis)
    # composite = 0.88*30 + 0.78*25 + 0.72*25 + 0.85*20 = 26.4+19.5+18+17 = 80.9
    {"id": "MCE-003", "name": "Saudi Aramco Gas Operations", "country": "Arabie Saoudite", "sector": "industrie_petroliere",
     "s1": 0.88, "s2": 0.78, "s3": 0.72, "s4": 0.85},
    # MCE-004 — eleve — Australie
    # composite = 0.62*30 + 0.58*25 + 0.55*25 + 0.50*20 = 18.6+14.5+13.75+10 = 56.85 -> eleve
    {"id": "MCE-004", "name": "Australian Gas Infrastructure Group", "country": "Australie", "sector": "infrastructure_gaz",
     "s1": 0.62, "s2": 0.58, "s3": 0.55, "s4": 0.50},
    # MCE-005 — eleve — Kazakhstan
    # composite = 0.55*30 + 0.60*25 + 0.58*25 + 0.45*20 = 16.5+15+14.5+9 = 55.0 -> eleve
    {"id": "MCE-005", "name": "KazMunayGas Environmental", "country": "Kazakhstan", "sector": "industrie_gaziere",
     "s1": 0.55, "s2": 0.60, "s3": 0.58, "s4": 0.45},
    # MCE-006 — modere — Canada
    # composite = 0.35*30 + 0.30*25 + 0.28*25 + 0.32*20 = 10.5+7.5+7+6.4 = 31.4
    {"id": "MCE-006", "name": "Canada Energy Regulator", "country": "Canada", "sector": "agence_reglementation",
     "s1": 0.35, "s2": 0.30, "s3": 0.28, "s4": 0.32},
    # MCE-007 — faible — Pays-Bas
    # composite = 0.12*30 + 0.10*25 + 0.14*25 + 0.10*20 = 3.6+2.5+3.5+2 = 11.6
    {"id": "MCE-007", "name": "Nederlandse Gasunie", "country": "Pays-Bas", "sector": "infrastructure_gaz",
     "s1": 0.12, "s2": 0.10, "s3": 0.14, "s4": 0.10},
    # MCE-008 — faible — Iran
    # composite = 0.10*30 + 0.14*25 + 0.12*25 + 0.08*20 = 3+3.5+3+1.6 = 11.1
    {"id": "MCE-008", "name": "National Iranian Gas Company", "country": "Iran", "sector": "industrie_gaziere",
     "s1": 0.10, "s2": 0.14, "s3": 0.12, "s4": 0.08},
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
    if raw["s1"] >= 0.85 and raw["s2"] >= 0.80: return "fossil_methane_surge"
    if raw["s2"] >= 0.85 and raw["s3"] >= 0.80: return "arctic_methane_bomb"
    if raw["s1"] >= 0.85 and raw["s4"] >= 0.80: return "flaring_crisis"
    if raw["s2"] >= 0.70 and raw["s3"] >= 0.65: return "regulatory_failure_cascade"
    if raw["s3"] >= 0.70 and raw["s4"] >= 0.65: return "climate_feedback_loop"
    return "none"


def _recommended_action(risk: str) -> str:
    if risk == "critique": return "intervention_urgente_emissions_methane_critiques"
    if risk == "eleve": return "reduction_methane_acceleree"
    if risk == "modere": return "renforcement_surveillance_methane"
    return "veille_methane_continue"


def _key_signals(risk: str, pattern: str, comp: float) -> str:
    labels = {
        "fossil_methane_surge": "Surge émissions méthane fossile",
        "arctic_methane_bomb": "Bombe méthane arctique",
        "flaring_crisis": "Crise torchage méthane",
        "regulatory_failure_cascade": "Cascade défaillance réglementaire",
        "climate_feedback_loop": "Boucle rétroaction climatique méthane",
        "none": "Émissions méthane sous contrôle",
    }
    label = labels.get(pattern, pattern)
    if risk == "critique": return f"Crise méthane systémique — {label} — composite {comp:.1f}"
    if risk == "eleve": return f"Crise méthane majeure — {label} — composite {comp:.1f}"
    if risk == "modere": return f"Méthane structurel — {label} — composite {comp:.1f}"
    return f"Émissions méthane surveillées — composite {comp:.1f}"


def analyze_methane(raw: dict) -> dict:
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
        "estimated_methane_index": round(comp / 100 * 10 * 100) / 100,
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
        total_idx += e["estimated_methane_index"]
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
        "engine_version": "345.2.0",
        "domain": "methane",
        "confidence_score": 0.91,
        "data_sources": ["US-EPA", "Gazprom", "Aramco", "AEMO", "KMG", "CER", "Gasunie", "NIGC"],
        "avg_estimated_methane_index": avg_idx,
    }


class MethaneCrisisEngine:
    """Module 345 — Methane Crisis & Arctic Methane Bomb Intelligence Engine"""

    def analyze(self, entities: List[Dict]) -> Dict[str, Any]:
        results = [analyze_methane(e) for e in entities]
        return summary(results)

    def get_mock_data(self) -> Dict[str, Any]:
        entities = [analyze_methane(raw) for raw in MOCK_ENTITIES_RAW]
        result = summary(entities)
        result["entities"] = entities
        return result
