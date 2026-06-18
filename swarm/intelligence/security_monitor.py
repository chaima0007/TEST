"""
Security Monitor — detects and blocks suspicious patterns in API requests.

Threat categories:
  SQL injection, XSS, path traversal, brute force, rate abuse, anomalous payloads
  → ThreatSeverity: INFO/LOW/MEDIUM/HIGH/CRITICAL
  → SecurityEvent with recommended action: LOG/ALERT/BLOCK/BAN
"""

from __future__ import annotations

import re
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Deque, Tuple


class ThreatSeverity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RecommendedAction(str, Enum):
    LOG = "log"
    ALERT = "alert"
    BLOCK = "block"
    BAN = "ban"


@dataclass
class SecurityEvent:
    event_id: str
    timestamp: float
    ip_address: str
    endpoint: str
    threat_type: str
    severity: ThreatSeverity
    recommended_action: RecommendedAction
    matched_pattern: str
    raw_input: str
    details: str

    def to_dict(self) -> dict:
        return {
            **asdict(self),
            "severity": self.severity.value,
            "recommended_action": self.recommended_action.value,
        }


@dataclass
class IPRecord:
    ip: str
    request_times: Deque[float] = field(default_factory=lambda: deque(maxlen=200))
    failed_auth_count: int = 0
    is_banned: bool = False
    is_blocked: bool = False
    ban_reason: Optional[str] = None
    event_count: int = 0


# ─── Threat patterns ─────────────────────────────────────────────────────────

_SQL_PATTERNS = re.compile(
    r"(\bUNION\b|\bSELECT\b|\bINSERT\b|\bUPDATE\b|\bDELETE\b|\bDROP\b|\bEXEC\b"
    r"|\bEXECUTE\b|--|;--|/\*|\*/|xp_|0x[0-9a-fA-F]+|CHAR\(|NCHAR\()",
    re.IGNORECASE,
)

_XSS_PATTERNS = re.compile(
    r"(<script|javascript:|on\w+=|<iframe|<object|<embed|<form|<input"
    r"|data:text/html|vbscript:|expression\()",
    re.IGNORECASE,
)

_PATH_TRAVERSAL = re.compile(
    r"(\.\./|\.\.\%2F|%2E%2E%2F|%252E%252E|/etc/passwd|/proc/self|\\windows\\)",
    re.IGNORECASE,
)

_COMMAND_INJECTION = re.compile(
    r"(;\s*(ls|cat|curl|wget|rm|echo|bash|sh|python|php)\b|\|\s*(ls|cat|curl|wget)"
    r"|`[^`]+`|\$\([^)]+\))",
    re.IGNORECASE,
)

_TEMPLATE_INJECTION = re.compile(
    r"(\{\{.*\}\}|{%.*%}|\$\{.*\}|<\?php|\#{.*})",
    re.IGNORECASE,
)

_LARGE_PAYLOAD_THRESHOLD = 50_000  # bytes

_THREAT_MAP: List[Tuple[re.Pattern, str, ThreatSeverity, RecommendedAction]] = [
    (_SQL_PATTERNS,       "sql_injection",      ThreatSeverity.HIGH,     RecommendedAction.BLOCK),
    (_XSS_PATTERNS,       "xss_attempt",        ThreatSeverity.HIGH,     RecommendedAction.BLOCK),
    (_PATH_TRAVERSAL,     "path_traversal",     ThreatSeverity.CRITICAL, RecommendedAction.BAN),
    (_COMMAND_INJECTION,  "command_injection",  ThreatSeverity.CRITICAL, RecommendedAction.BAN),
    (_TEMPLATE_INJECTION, "template_injection", ThreatSeverity.HIGH,     RecommendedAction.BLOCK),
]

_BRUTE_FORCE_WINDOW_SECONDS = 60
_BRUTE_FORCE_THRESHOLD = 10  # failed auths in window
_RATE_LIMIT_WINDOW = 60      # seconds
_RATE_LIMIT_MAX = 120        # requests per window per IP


def _check_payload(payload: str) -> Optional[Tuple[str, ThreatSeverity, RecommendedAction, str]]:
    if len(payload.encode("utf-8", errors="replace")) > _LARGE_PAYLOAD_THRESHOLD:
        return ("oversized_payload", ThreatSeverity.MEDIUM, RecommendedAction.BLOCK, f"payload>{_LARGE_PAYLOAD_THRESHOLD}b")
    for pattern, threat_type, severity, action in _THREAT_MAP:
        m = pattern.search(payload)
        if m:
            return (threat_type, severity, action, m.group(0)[:100])
    return None


_event_counter = 0


def _next_event_id() -> str:
    global _event_counter
    _event_counter += 1
    return f"evt_{_event_counter:06d}"


class SecurityMonitor:
    def __init__(self) -> None:
        self._events: List[SecurityEvent] = []
        self._ip_records: Dict[str, IPRecord] = defaultdict(lambda: IPRecord(ip=""))
        self._blocked_ips: set = set()
        self._banned_ips: set = set()

    def _get_record(self, ip: str) -> IPRecord:
        if ip not in self._ip_records:
            self._ip_records[ip] = IPRecord(ip=ip)
        return self._ip_records[ip]

    def scan_request(
        self,
        ip: str,
        endpoint: str,
        payload: str,
        timestamp: Optional[float] = None,
    ) -> Optional[SecurityEvent]:
        ts = timestamp if timestamp is not None else time.time()
        record = self._get_record(ip)

        if record.is_banned:
            evt = SecurityEvent(
                event_id=_next_event_id(),
                timestamp=ts,
                ip_address=ip,
                endpoint=endpoint,
                threat_type="banned_ip_request",
                severity=ThreatSeverity.CRITICAL,
                recommended_action=RecommendedAction.BAN,
                matched_pattern="ip_ban_list",
                raw_input=payload[:200],
                details=f"Banned IP attempted access: {record.ban_reason}",
            )
            self._events.append(evt)
            record.event_count += 1
            return evt

        if record.is_blocked:
            evt = SecurityEvent(
                event_id=_next_event_id(),
                timestamp=ts,
                ip_address=ip,
                endpoint=endpoint,
                threat_type="blocked_ip_request",
                severity=ThreatSeverity.HIGH,
                recommended_action=RecommendedAction.BLOCK,
                matched_pattern="ip_block_list",
                raw_input=payload[:200],
                details="Blocked IP attempted access",
            )
            self._events.append(evt)
            record.event_count += 1
            return evt

        result = _check_payload(payload)
        if result:
            threat_type, severity, action, matched = result

            if action == RecommendedAction.BAN:
                self.ban_ip(ip, reason=f"auto-ban: {threat_type}")
            elif action == RecommendedAction.BLOCK:
                self.block_ip(ip)

            evt = SecurityEvent(
                event_id=_next_event_id(),
                timestamp=ts,
                ip_address=ip,
                endpoint=endpoint,
                threat_type=threat_type,
                severity=severity,
                recommended_action=action,
                matched_pattern=matched,
                raw_input=payload[:200],
                details=f"Malicious pattern detected in request to {endpoint}",
            )
            self._events.append(evt)
            record.event_count += 1
            return evt

        return None

    def record_request(self, ip: str, timestamp: Optional[float] = None) -> bool:
        ts = timestamp if timestamp is not None else time.time()
        record = self._get_record(ip)
        record.request_times.append(ts)

        cutoff = ts - _RATE_LIMIT_WINDOW
        recent = sum(1 for t in record.request_times if t >= cutoff)
        if recent > _RATE_LIMIT_MAX:
            self.block_ip(ip)
            evt = SecurityEvent(
                event_id=_next_event_id(),
                timestamp=ts,
                ip_address=ip,
                endpoint="*",
                threat_type="rate_limit_exceeded",
                severity=ThreatSeverity.MEDIUM,
                recommended_action=RecommendedAction.BLOCK,
                matched_pattern=f">{_RATE_LIMIT_MAX} req/{_RATE_LIMIT_WINDOW}s",
                raw_input="",
                details=f"{recent} requests in {_RATE_LIMIT_WINDOW}s window",
            )
            self._events.append(evt)
            record.event_count += 1
            return False
        return True

    def record_failed_auth(self, ip: str, timestamp: Optional[float] = None) -> Optional[SecurityEvent]:
        ts = timestamp if timestamp is not None else time.time()
        record = self._get_record(ip)
        record.failed_auth_count += 1

        if record.failed_auth_count >= _BRUTE_FORCE_THRESHOLD:
            self.ban_ip(ip, reason="brute_force_auth")
            evt = SecurityEvent(
                event_id=_next_event_id(),
                timestamp=ts,
                ip_address=ip,
                endpoint="/api/auth/login",
                threat_type="brute_force",
                severity=ThreatSeverity.CRITICAL,
                recommended_action=RecommendedAction.BAN,
                matched_pattern=f">={_BRUTE_FORCE_THRESHOLD} failed auths",
                raw_input="",
                details=f"{record.failed_auth_count} failed authentication attempts",
            )
            self._events.append(evt)
            record.event_count += 1
            return evt
        return None

    def block_ip(self, ip: str) -> None:
        record = self._get_record(ip)
        record.is_blocked = True
        self._blocked_ips.add(ip)

    def ban_ip(self, ip: str, reason: str = "manual") -> None:
        record = self._get_record(ip)
        record.is_banned = True
        record.ban_reason = reason
        self._banned_ips.add(ip)
        self._blocked_ips.add(ip)

    def unblock_ip(self, ip: str) -> None:
        record = self._get_record(ip)
        record.is_blocked = False
        self._blocked_ips.discard(ip)

    def is_blocked(self, ip: str) -> bool:
        return ip in self._blocked_ips

    def is_banned(self, ip: str) -> bool:
        return ip in self._banned_ips

    def recent_events(self, n: int = 50) -> List[SecurityEvent]:
        return list(reversed(self._events[-n:]))

    def events_by_severity(self, severity: ThreatSeverity) -> List[SecurityEvent]:
        return [e for e in self._events if e.severity == severity]

    def events_by_ip(self, ip: str) -> List[SecurityEvent]:
        return [e for e in self._events if e.ip_address == ip]

    def threat_summary(self) -> dict:
        total = len(self._events)
        severity_counts: Dict[str, int] = {s.value: 0 for s in ThreatSeverity}
        type_counts: Dict[str, int] = {}
        for e in self._events:
            severity_counts[e.severity.value] += 1
            type_counts[e.threat_type] = type_counts.get(e.threat_type, 0) + 1
        top_threat_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        return {
            "total_events": total,
            "severity_counts": severity_counts,
            "blocked_ips": len(self._blocked_ips),
            "banned_ips": len(self._banned_ips),
            "top_threat_types": [{"type": t, "count": c} for t, c in top_threat_types],
        }

    def reset(self) -> None:
        self._events.clear()
        self._ip_records.clear()
        self._blocked_ips.clear()
        self._banned_ips.clear()
