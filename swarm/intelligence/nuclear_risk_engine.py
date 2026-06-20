"""
Module 326 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
Nuclear Risk & Proliferation Intelligence Engine
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class NuclearRiskInput:
    entity_id: str
    name: str
    country: str
    sector: str
    facility_safety_score: float           # 0-1
    waste_management_score: float          # 0-1
    proliferation_risk_score: float        # 0-1
    emergency_response_gap_score: float    # 0-1


@dataclass
class NuclearRiskResult:
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
    estimated_nuclear_index: float
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
            "estimated_nuclear_index": self.estimated_nuclear_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES_RAW = [
    # NUC-001 — critique — France (facility>=0.85, waste>=0.80 => aging_reactor_crisis)
    # composite = 0.88*30 + 0.85*25 + 0.78*25 + 0.72*20 = 26.4+21.25+19.5+14.4 = 81.55
    {"id": "NUC-001", "name": "EDF Parc Nucléaire France", "country": "France", "sector": "energie_nucleaire",
     "s1": 0.88, "s2": 0.85, "s3": 0.78, "s4": 0.72},
    # NUC-002 — critique — États-Unis (waste>=0.85, proliferation>=0.80 => waste_storage_failure)
    # composite = 0.80*30 + 0.88*25 + 0.85*25 + 0.76*20 = 24+22+21.25+15.2 = 82.45
    {"id": "NUC-002", "name": "US NRC Nuclear Safety Division", "country": "États-Unis", "sector": "agence_surete",
     "s1": 0.80, "s2": 0.88, "s3": 0.85, "s4": 0.76},
    # NUC-003 — critique — Russie (proliferation>=0.85, emergency>=0.80 => proliferation_leak)
    # composite = 0.75*30 + 0.72*25 + 0.88*25 + 0.85*20 = 22.5+18+22+17 = 79.5
    {"id": "NUC-003", "name": "Rosatom Nuclear Corporation", "country": "Russie", "sector": "industrie_nucleaire",
     "s1": 0.75, "s2": 0.72, "s3": 0.88, "s4": 0.85},
    # NUC-004 — eleve — Chine
    # composite = 0.60*30 + 0.58*25 + 0.55*25 + 0.48*20 = 18+14.5+13.75+9.6 = 55.85
    {"id": "NUC-004", "name": "China National Nuclear Corporation", "country": "Chine", "sector": "industrie_nucleaire",
     "s1": 0.60, "s2": 0.58, "s3": 0.55, "s4": 0.48},
    # NUC-005 — eleve — Corée du Sud
    # composite = 0.55*30 + 0.52*25 + 0.50*25 + 0.55*20 = 16.5+13+12.5+11 = 53.0
    {"id": "NUC-005", "name": "KEPCO Nuclear Korea", "country": "Corée du Sud", "sector": "energie_nucleaire",
     "s1": 0.55, "s2": 0.52, "s3": 0.50, "s4": 0.55},
    # NUC-006 — modere — Japon
    # composite = 0.38*30 + 0.35*25 + 0.32*25 + 0.28*20 = 11.4+8.75+8+5.6 = 33.75
    {"id": "NUC-006", "name": "TEPCO Nuclear Management", "country": "Japon", "sector": "energie_nucleaire",
     "s1": 0.38, "s2": 0.35, "s3": 0.32, "s4": 0.28},
    # NUC-007 — faible — Inde
    # composite = 0.14*30 + 0.12*25 + 0.10*25 + 0.14*20 = 4.2+3+2.5+2.8 = 12.5
    {"id": "NUC-007", "name": "Nuclear Power Corporation of India", "country": "Inde", "sector": "energie_nucleaire",
     "s1": 0.14, "s2": 0.12, "s3": 0.10, "s4": 0.14},
    # NUC-008 — faible — Ukraine
    # composite = 0.10*30 + 0.14*25 + 0.12*25 + 0.10*20 = 3+3.5+3+2 = 11.5
    {"id": "NUC-008", "name": "Energoatom Ukraine", "country": "Ukraine", "sector": "energie_nucleaire",
     "s1": 0.10, "s2": 0.14, "s3": 0.12, "s4": 0.10},
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
    if raw["s1"] >= 0.85 and raw["s2"] >= 0.80: return "aging_reactor_crisis"
    if raw["s2"] >= 0.85 and raw["s3"] >= 0.80: return "waste_storage_failure"
    if raw["s3"] >= 0.85 and raw["s4"] >= 0.80: return "proliferation_leak"
    if raw["s2"] >= 0.70 and raw["s3"] >= 0.65: return "dual_use_technology_breach"
    if raw["s3"] >= 0.70 and raw["s4"] >= 0.65: return "emergency_response_collapse"
    return "none"


def _recommended_action(risk: str) -> str:
    if risk == "critique": return "intervention_urgente_surete_nucleaire_critique"
    if risk == "eleve": return "renforcement_controle_nucleaire_accelere"
    if risk == "modere": return "surveillance_renforcee_installations_nucleaires"
    return "veille_nucleaire_continue"


def _key_signals(risk: str, pattern: str, comp: float) -> str:
    labels = {
        "aging_reactor_crisis": "Crise réacteurs vieillissants",
        "waste_storage_failure": "Défaillance stockage déchets nucléaires",
        "proliferation_leak": "Fuite prolifération matières fissiles",
        "dual_use_technology_breach": "Brèche technologie double usage",
        "emergency_response_collapse": "Effondrement réponse urgence nucléaire",
        "none": "Risque nucléaire sous contrôle",
    }
    label = labels.get(pattern, pattern)
    if risk == "critique": return f"Crise nucléaire systémique — {label} — composite {comp:.1f}"
    if risk == "eleve": return f"Risque nucléaire élevé — {label} — composite {comp:.1f}"
    if risk == "modere": return f"Tension nucléaire structurelle — {label} — composite {comp:.1f}"
    return f"Domaine nucléaire surveillé — composite {comp:.1f}"


def analyze_nuclear(raw: dict) -> dict:
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
        "estimated_nuclear_index": round(comp / 100 * 10 * 100) / 100,
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
        total_idx += e["estimated_nuclear_index"]
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
        "engine_version": "326.2.0",
        "domain": "nuclear",
        "confidence_score": 0.93,
        "data_sources": ["EDF", "US-NRC", "Rosatom", "CNNC", "KEPCO", "TEPCO", "NPCIL", "Energoatom"],
        "avg_estimated_nuclear_index": avg_idx,
    }


class NuclearRiskEngine:
    """Module 326 — Nuclear Risk & Proliferation Intelligence Engine"""

    def analyze(self, entities: List[Dict]) -> Dict[str, Any]:
        results = [analyze_nuclear(e) for e in entities]
        return summary(results)

    def get_mock_data(self) -> Dict[str, Any]:
        entities = [analyze_nuclear(raw) for raw in MOCK_ENTITIES_RAW]
        result = summary(entities)
        result["entities"] = entities
        return result
