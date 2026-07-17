"""
Module 389 — Intellectual Property War & Patent Warfare Intelligence Engine
Caelum Partners Swarm Intelligence — Propriété exclusive de Chaima Mhadbi
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class IPWarfareInput:
    entity_id: str
    ip_domain: str
    region: str
    patent_trolling_scale: float
    state_IP_theft_intensity: float
    standard_essential_patent_abuse: float
    pharmaceutical_evergreening: float
    AI_patent_monopolization: float
    trade_secret_theft: float
    copyright_maximalism_harm: float
    WIPO_governance_capture: float
    developing_nation_IP_exclusion: float
    technology_transfer_blockade: float
    innovation_suppression_via_patents: float
    open_source_patent_attack: float
    geopolitical_IP_weaponization: float
    patent_litigation_cost_barrier: float
    generic_medicine_access_block: float
    technology_dependency_IP: float
    digital_content_monopoly: float


def _theft_score(e: IPWarfareInput) -> float:
    raw = (
        e.state_IP_theft_intensity
        + e.trade_secret_theft
        + e.patent_trolling_scale
        + e.open_source_patent_attack
    ) / 4 * 100
    return round(raw * 100) / 100


def _monopoly_score(e: IPWarfareInput) -> float:
    raw = (
        e.AI_patent_monopolization
        + e.standard_essential_patent_abuse
        + e.pharmaceutical_evergreening
        + e.copyright_maximalism_harm
        + e.digital_content_monopoly
        + e.innovation_suppression_via_patents
    ) / 6 * 100
    return round(raw * 100) / 100


def _access_score(e: IPWarfareInput) -> float:
    raw = (
        e.developing_nation_IP_exclusion
        + e.generic_medicine_access_block
        + e.patent_litigation_cost_barrier
        + e.technology_dependency_IP
        + e.technology_transfer_blockade
    ) / 5 * 100
    return round(raw * 100) / 100


def _geopolitical_score(e: IPWarfareInput) -> float:
    raw = (
        e.geopolitical_IP_weaponization
        + e.WIPO_governance_capture
    ) / 2 * 100
    return round(raw * 100) / 100


def _composite(theft: float, monopoly: float, access: float, geopolitical: float) -> float:
    return round((theft * 0.30 + monopoly * 0.25 + access * 0.25 + geopolitical * 0.20) * 100) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _patterns_detected(e: IPWarfareInput) -> List[str]:
    patterns = []
    if e.state_IP_theft_intensity > 0.85 and e.trade_secret_theft > 0.80:
        patterns.append("state_IP_espionage_campaign")
    if e.AI_patent_monopolization > 0.85 and e.innovation_suppression_via_patents > 0.80:
        patterns.append("patent_monopoly_capture")
    if e.pharmaceutical_evergreening > 0.85 and e.generic_medicine_access_block > 0.80:
        patterns.append("pharmaceutical_access_blockade")
    if e.geopolitical_IP_weaponization > 0.80 and e.technology_transfer_blockade > 0.75:
        patterns.append("geopolitical_IP_warfare")
    if e.developing_nation_IP_exclusion > 0.80 and e.WIPO_governance_capture > 0.75:
        patterns.append("global_south_IP_exclusion")
    return patterns


def _severity(risk: str) -> str:
    if risk == "critical":
        return "Critique"
    if risk == "high":
        return "Élevé"
    if risk == "moderate":
        return "Modéré"
    return "Faible"


def _action_required(risk: str) -> str:
    if risk == "critical":
        return "Intervention immédiate requise"
    if risk == "high":
        return "Surveillance renforcée recommandée"
    if risk == "moderate":
        return "Monitoring continu conseillé"
    return "Surveillance standard"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "ALERTE ROUGE — Guerre IP active"
    if risk == "high":
        return "ALERTE ORANGE — Risque IP majeur"
    if risk == "moderate":
        return "VIGILANCE — Tensions IP modérées"
    return "NORMAL — Situation IP stable"


def _analyze(e: IPWarfareInput) -> Dict[str, Any]:
    theft = _theft_score(e)
    monopoly = _monopoly_score(e)
    access = _access_score(e)
    geopolitical = _geopolitical_score(e)
    composite = _composite(theft, monopoly, access, geopolitical)
    risk = _risk_level(composite)
    patterns = _patterns_detected(e)
    severity = _severity(risk)
    action = _action_required(risk)
    sig = _signal(risk)
    estimated_ip_warfare_index = round(composite / 100 * 10, 2)

    return {
        "entity_id": e.entity_id,
        "ip_domain": e.ip_domain,
        "region": e.region,
        "theft_score": theft,
        "monopoly_score": monopoly,
        "access_score": access,
        "geopolitical_score": geopolitical,
        "composite_score": composite,
        "risk_level": risk,
        "patterns_detected": patterns,
        "severity": severity,
        "action_required": action,
        "signal": sig,
        "estimated_ip_warfare_index": estimated_ip_warfare_index,
        "metadata": {
            "state_IP_theft_intensity": e.state_IP_theft_intensity,
            "geopolitical_IP_weaponization": e.geopolitical_IP_weaponization,
            "pharmaceutical_evergreening": e.pharmaceutical_evergreening,
        },
    }


class IPWarfareEngine:
    def run(self, inputs: List[IPWarfareInput]) -> Dict[str, Any]:
        entities = [_analyze(e) for e in inputs]

        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0
        total_composite = 0.0
        total_theft = 0.0
        total_monopoly = 0.0
        total_access = 0.0

        risk_distribution: Dict[str, int] = {}
        pattern_distribution: Dict[str, int] = {}

        for ent in entities:
            risk = ent["risk_level"]
            risk_distribution[risk] = risk_distribution.get(risk, 0) + 1
            for pat in ent["patterns_detected"]:
                pattern_distribution[pat] = pattern_distribution.get(pat, 0) + 1
            total_composite += ent["composite_score"]
            total_theft += ent["theft_score"]
            total_monopoly += ent["monopoly_score"]
            total_access += ent["access_score"]

            if risk == "critical":
                critical_count += 1
            elif risk == "high":
                high_count += 1
            elif risk == "moderate":
                moderate_count += 1
            else:
                low_count += 1

        n = len(entities)
        avg_composite = round(total_composite / n * 10) / 10 if n else 0.0
        theft_avg = round(total_theft / n * 10) / 10 if n else 0.0
        monopoly_avg = round(total_monopoly / n * 10) / 10 if n else 0.0
        access_avg = round(total_access / n * 10) / 10 if n else 0.0

        summary = {
            "module_id": 389,
            "module_name": "Intellectual Property War & Patent Warfare Intelligence Engine",
            "total": n,
            "critical": critical_count,
            "high": high_count,
            "moderate": moderate_count,
            "low": low_count,
            "avg_composite": avg_composite,
            "distributions": {
                "risk": risk_distribution,
                "pattern": pattern_distribution,
            },
            "avg_estimated_ip_warfare_index": round(avg_composite / 100 * 10, 2),
            "theft_avg": theft_avg,
            "monopoly_avg": monopoly_avg,
            "access_avg": access_avg,
        }

        return {"entities": entities, "summary": summary}
