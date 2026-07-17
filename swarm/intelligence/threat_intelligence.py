"""
Threat Intelligence — actor profiling and endpoint vulnerability analysis.

Extends SecurityMonitor by grouping events into threat actors, scoring
endpoint risk, and generating hardening recommendations:
  ThreatLevel: BENIGN / SUSPICIOUS / MALICIOUS / APT
  Risk scoring: attack_count + diversity + targeting pattern
"""

from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple


class ThreatLevel(str, Enum):
    BENIGN = "benign"
    SUSPICIOUS = "suspicious"
    MALICIOUS = "malicious"
    APT = "apt"


_THREAT_LEVEL_SCORE = {
    ThreatLevel.BENIGN: 0,
    ThreatLevel.SUSPICIOUS: 25,
    ThreatLevel.MALICIOUS: 60,
    ThreatLevel.APT: 90,
}

_HIGH_SEVERITY_TYPES = frozenset([
    "sql_injection", "command_injection", "path_traversal",
    "banned_ip_request", "brute_force",
])

_CRITICAL_TYPES = frozenset([
    "command_injection", "path_traversal",
])

_HARDENING_MAP: Dict[str, str] = {
    "sql_injection": "Activer la validation stricte des paramètres SQL et utiliser des requêtes préparées",
    "xss_attempt": "Implémenter Content-Security-Policy et encoder toutes les sorties HTML",
    "path_traversal": "Valider et normaliser tous les chemins de fichiers, rejeter les séquences ../ ",
    "command_injection": "Éviter exec() avec des entrées utilisateur, utiliser des listes d'arguments",
    "template_injection": "Désactiver l'exécution de templates sur les entrées non-fiables",
    "brute_force": "Implémenter CAPTCHA et verrouillage de compte après N échecs",
    "rate_limit_exceeded": "Renforcer les règles de rate-limiting et implémenter un circuit breaker",
    "oversized_payload": "Réduire la limite de payload ou implémenter un contrôle de streaming",
    "banned_ip_request": "Activer la synchronisation de liste noire en temps réel avec threat feeds",
    "blocked_ip_request": "Vérifier les listes de blocage IP avant traitement de chaque requête",
}


@dataclass
class RawEvent:
    event_id: str
    timestamp: float
    ip_address: str
    endpoint: str
    threat_type: str
    severity: str          # info/low/medium/high/critical
    recommended_action: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ThreatActor:
    actor_id: str
    ip_addresses: List[str]
    first_seen: float
    last_seen: float
    attack_count: int
    threat_types: List[str]         # distinct threat types used
    targeted_endpoints: List[str]   # distinct endpoints targeted
    threat_level: ThreatLevel
    confidence: float               # 0.0-1.0
    persistence_hours: float        # hours between first and last seen

    def to_dict(self) -> dict:
        return {
            **asdict(self),
            "threat_level": self.threat_level.value,
        }


@dataclass
class EndpointVulnerability:
    endpoint: str
    attack_count: int
    unique_attackers: int
    threat_types: List[str]
    risk_score: float               # 0-100
    recommended_actions: List[str]

    def to_dict(self) -> dict:
        return asdict(self)


# ─── Scoring helpers ──────────────────────────────────────────────────────────

def _actor_threat_level(
    attack_count: int,
    threat_types: List[str],
    persistence_hours: float,
) -> Tuple[ThreatLevel, float]:
    critical_hits = sum(1 for t in threat_types if t in _CRITICAL_TYPES)
    high_hits = sum(1 for t in threat_types if t in _HIGH_SEVERITY_TYPES)
    type_diversity = len(set(threat_types))

    # APT: persistent (>12h), diverse (>2 types), at least one critical
    if persistence_hours > 12 and type_diversity >= 3 and critical_hits >= 1:
        confidence = min(1.0, 0.70 + (type_diversity - 3) * 0.05 + (attack_count - 5) * 0.01)
        return ThreatLevel.APT, round(min(1.0, confidence), 4)

    # MALICIOUS: critical type OR many attacks
    if critical_hits >= 1 or attack_count >= 5 or high_hits >= 2:
        confidence = min(1.0, 0.55 + critical_hits * 0.10 + high_hits * 0.05)
        return ThreatLevel.MALICIOUS, round(min(1.0, confidence), 4)

    # SUSPICIOUS: at least one high-severity type or multiple attacks
    if high_hits >= 1 or attack_count >= 2 or type_diversity >= 2:
        confidence = min(1.0, 0.40 + high_hits * 0.05)
        return ThreatLevel.SUSPICIOUS, round(min(1.0, confidence), 4)

    return ThreatLevel.BENIGN, round(max(0.1, 0.30 - attack_count * 0.05), 4)


def _endpoint_risk_score(
    attack_count: int,
    unique_attackers: int,
    threat_types: List[str],
) -> float:
    critical_weight = sum(3.0 for t in threat_types if t in _CRITICAL_TYPES)
    high_weight = sum(1.5 for t in threat_types if t in _HIGH_SEVERITY_TYPES)
    base = min(60.0, attack_count * 5.0) + critical_weight * 5 + high_weight * 2
    attacker_bonus = min(20.0, unique_attackers * 4.0)
    return round(min(100.0, base + attacker_bonus), 2)


# ─── Main class ───────────────────────────────────────────────────────────────

class ThreatIntelligence:
    def __init__(self) -> None:
        self._events: List[RawEvent] = []
        self._actors: Dict[str, ThreatActor] = {}
        self._endpoints: Dict[str, EndpointVulnerability] = {}

    def ingest_events(self, events: List[RawEvent]) -> None:
        self._events.extend(events)
        self._rebuild()

    def ingest_event(self, event: RawEvent) -> None:
        self._events.append(event)
        self._rebuild()

    def _rebuild(self) -> None:
        self._build_actors()
        self._build_endpoints()

    def _build_actors(self) -> None:
        ip_events: Dict[str, List[RawEvent]] = defaultdict(list)
        for e in self._events:
            ip_events[e.ip_address].append(e)

        self._actors.clear()
        for ip, evts in ip_events.items():
            first_seen = min(e.timestamp for e in evts)
            last_seen = max(e.timestamp for e in evts)
            persistence_hours = (last_seen - first_seen) / 3600.0
            threat_types = [e.threat_type for e in evts]
            endpoints = list(dict.fromkeys(e.endpoint for e in evts))

            level, confidence = _actor_threat_level(
                attack_count=len(evts),
                threat_types=threat_types,
                persistence_hours=persistence_hours,
            )

            actor_id = f"actor_{ip.replace('.', '_')}"
            self._actors[actor_id] = ThreatActor(
                actor_id=actor_id,
                ip_addresses=[ip],
                first_seen=first_seen,
                last_seen=last_seen,
                attack_count=len(evts),
                threat_types=list(dict.fromkeys(threat_types)),
                targeted_endpoints=endpoints,
                threat_level=level,
                confidence=confidence,
                persistence_hours=round(persistence_hours, 2),
            )

    def _build_endpoints(self) -> None:
        ep_events: Dict[str, List[RawEvent]] = defaultdict(list)
        for e in self._events:
            ep_events[e.endpoint].append(e)

        self._endpoints.clear()
        for ep, evts in ep_events.items():
            threat_types = list(dict.fromkeys(e.threat_type for e in evts))
            unique_ips: Set[str] = {e.ip_address for e in evts}
            risk = _endpoint_risk_score(
                attack_count=len(evts),
                unique_attackers=len(unique_ips),
                threat_types=[e.threat_type for e in evts],
            )
            recommendations = [
                _HARDENING_MAP[t]
                for t in threat_types
                if t in _HARDENING_MAP
            ]
            self._endpoints[ep] = EndpointVulnerability(
                endpoint=ep,
                attack_count=len(evts),
                unique_attackers=len(unique_ips),
                threat_types=threat_types,
                risk_score=risk,
                recommended_actions=recommendations,
            )

    # ── Queries ───────────────────────────────────────────────────────────────

    def all_actors(self) -> List[ThreatActor]:
        return sorted(
            self._actors.values(),
            key=lambda a: (_THREAT_LEVEL_SCORE.get(a.threat_level, 0), a.attack_count),
            reverse=True,
        )

    def top_threats(self, n: int = 10) -> List[ThreatActor]:
        return self.all_actors()[:n]

    def actors_by_level(self, level: ThreatLevel) -> List[ThreatActor]:
        return [a for a in self._actors.values() if a.threat_level == level]

    def actor_by_ip(self, ip: str) -> Optional[ThreatActor]:
        actor_id = f"actor_{ip.replace('.', '_')}"
        return self._actors.get(actor_id)

    def vulnerability_report(self) -> List[EndpointVulnerability]:
        return sorted(self._endpoints.values(), key=lambda e: e.risk_score, reverse=True)

    def endpoint_risk(self, endpoint: str) -> Optional[EndpointVulnerability]:
        return self._endpoints.get(endpoint)

    def high_risk_endpoints(self, threshold: float = 50.0) -> List[EndpointVulnerability]:
        return [e for e in self._endpoints.values() if e.risk_score >= threshold]

    def intelligence_summary(self) -> dict:
        actors = list(self._actors.values())
        endpoints = list(self._endpoints.values())
        level_counts = {lvl.value: 0 for lvl in ThreatLevel}
        for a in actors:
            level_counts[a.threat_level.value] += 1
        avg_risk = (sum(e.risk_score for e in endpoints) / len(endpoints)) if endpoints else 0.0
        return {
            "total_events": len(self._events),
            "total_actors": len(actors),
            "actor_level_counts": level_counts,
            "total_endpoints_targeted": len(endpoints),
            "avg_endpoint_risk_score": round(avg_risk, 2),
            "high_risk_endpoint_count": len(self.high_risk_endpoints()),
            "apt_count": level_counts.get("apt", 0),
            "malicious_count": level_counts.get("malicious", 0),
        }

    def reset(self) -> None:
        self._events.clear()
        self._actors.clear()
        self._endpoints.clear()
