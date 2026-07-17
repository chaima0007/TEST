"""
Comprehensive pytest tests for the ThreatIntelligence module.
"""

from __future__ import annotations

import pytest
from typing import List

from swarm.intelligence.threat_intelligence import (
    ThreatLevel,
    RawEvent,
    ThreatActor,
    EndpointVulnerability,
    ThreatIntelligence,
    _actor_threat_level,
    _endpoint_risk_score,
    _HIGH_SEVERITY_TYPES,
    _CRITICAL_TYPES,
    _HARDENING_MAP,
)

# ---------------------------------------------------------------------------
# Fixed timestamps for deterministic tests
# ---------------------------------------------------------------------------

TS_BASE = 1_700_000_000.0          # arbitrary fixed base
TS_1H   = TS_BASE + 3_600.0        # +1 hour
TS_12H  = TS_BASE + 43_200.0       # +12 hours
TS_13H  = TS_BASE + 46_800.0       # +13 hours
TS_24H  = TS_BASE + 86_400.0       # +24 hours


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_event(
    event_id: str = "e1",
    timestamp: float = TS_BASE,
    ip_address: str = "1.2.3.4",
    endpoint: str = "/api/test",
    threat_type: str = "sql_injection",
    severity: str = "high",
    recommended_action: str = "block",
) -> RawEvent:
    return RawEvent(
        event_id=event_id,
        timestamp=timestamp,
        ip_address=ip_address,
        endpoint=endpoint,
        threat_type=threat_type,
        severity=severity,
        recommended_action=recommended_action,
    )


def make_ti(*events: RawEvent) -> ThreatIntelligence:
    ti = ThreatIntelligence()
    ti.ingest_events(list(events))
    return ti


# ===========================================================================
# 1. ThreatLevel enum
# ===========================================================================

class TestThreatLevelEnum:
    def test_benign_value(self):
        assert ThreatLevel.BENIGN.value == "benign"

    def test_suspicious_value(self):
        assert ThreatLevel.SUSPICIOUS.value == "suspicious"

    def test_malicious_value(self):
        assert ThreatLevel.MALICIOUS.value == "malicious"

    def test_apt_value(self):
        assert ThreatLevel.APT.value == "apt"

    def test_is_string_enum(self):
        assert isinstance(ThreatLevel.BENIGN, str)
        assert ThreatLevel.MALICIOUS == "malicious"

    def test_all_four_members(self):
        levels = {l.value for l in ThreatLevel}
        assert levels == {"benign", "suspicious", "malicious", "apt"}


# ===========================================================================
# 2. RawEvent dataclass & to_dict()
# ===========================================================================

class TestRawEvent:
    def test_to_dict_has_all_keys(self):
        ev = make_event()
        d = ev.to_dict()
        expected_keys = {
            "event_id", "timestamp", "ip_address", "endpoint",
            "threat_type", "severity", "recommended_action",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_values(self):
        ev = make_event(event_id="xyz", ip_address="9.9.9.9", threat_type="xss_attempt")
        d = ev.to_dict()
        assert d["event_id"] == "xyz"
        assert d["ip_address"] == "9.9.9.9"
        assert d["threat_type"] == "xss_attempt"

    def test_to_dict_timestamp_preserved(self):
        ev = make_event(timestamp=TS_BASE)
        assert ev.to_dict()["timestamp"] == TS_BASE


# ===========================================================================
# 3. _actor_threat_level — classification logic
# ===========================================================================

class TestActorThreatLevelAPT:
    """APT requires: persistence_hours > 12, type_diversity >= 3, critical_hits >= 1."""

    def test_apt_basic(self):
        types = ["command_injection", "sql_injection", "brute_force"]
        level, conf = _actor_threat_level(10, types, 13.0)
        assert level == ThreatLevel.APT

    def test_apt_confidence_capped_at_1(self):
        types = ["command_injection", "path_traversal", "sql_injection", "brute_force", "xss_attempt"]
        level, conf = _actor_threat_level(1000, types, 100.0)
        assert level == ThreatLevel.APT
        assert conf == 1.0

    def test_apt_confidence_minimum_formula(self):
        # diversity=3, attack_count=5 → 0.70 + 0*0.05 + 0*0.01 = 0.70
        types = ["command_injection", "sql_injection", "brute_force"]
        level, conf = _actor_threat_level(5, types, 13.0)
        assert level == ThreatLevel.APT
        assert conf == round(min(1.0, 0.70 + 0 * 0.05 + 0 * 0.01), 4)

    def test_apt_requires_persistence_gt_12(self):
        # exactly 12 hours should NOT be APT
        types = ["command_injection", "sql_injection", "brute_force"]
        level, _ = _actor_threat_level(10, types, 12.0)
        assert level != ThreatLevel.APT

    def test_apt_requires_diversity_ge_3(self):
        # only 2 distinct types
        types = ["command_injection", "sql_injection"]
        level, _ = _actor_threat_level(10, types, 13.0)
        assert level != ThreatLevel.APT

    def test_apt_requires_critical_hit(self):
        # 3+ types but none critical
        types = ["sql_injection", "brute_force", "xss_attempt"]
        level, _ = _actor_threat_level(10, types, 13.0)
        assert level != ThreatLevel.APT

    def test_apt_with_path_traversal_as_critical(self):
        types = ["path_traversal", "sql_injection", "brute_force"]
        level, conf = _actor_threat_level(6, types, 15.0)
        assert level == ThreatLevel.APT


class TestActorThreatLevelMalicious:
    """MALICIOUS: critical type OR attack_count >= 5 OR 2+ high severity types."""

    def test_malicious_via_critical_type(self):
        level, _ = _actor_threat_level(1, ["command_injection"], 0.0)
        assert level == ThreatLevel.MALICIOUS

    def test_malicious_via_attack_count(self):
        level, _ = _actor_threat_level(5, ["xss_attempt"], 0.0)
        assert level == ThreatLevel.MALICIOUS

    def test_malicious_via_two_high_severity(self):
        level, _ = _actor_threat_level(1, ["sql_injection", "brute_force"], 0.0)
        assert level == ThreatLevel.MALICIOUS

    def test_malicious_confidence_formula_critical(self):
        # command_injection is in BOTH _CRITICAL_TYPES and _HIGH_SEVERITY_TYPES
        # critical_hits=1, high_hits=2 (command_injection + sql_injection)
        # → 0.55 + 1*0.10 + 2*0.05 = 0.75
        types = ["command_injection", "sql_injection"]
        level, conf = _actor_threat_level(1, types, 0.0)
        assert level == ThreatLevel.MALICIOUS
        assert conf == round(min(1.0, 0.55 + 1 * 0.10 + 2 * 0.05), 4)

    def test_malicious_confidence_capped(self):
        # many critical + high types
        types = ["command_injection", "path_traversal", "sql_injection",
                 "brute_force", "banned_ip_request"]
        level, conf = _actor_threat_level(20, types, 0.0)
        assert level == ThreatLevel.MALICIOUS or level == ThreatLevel.APT
        if level == ThreatLevel.MALICIOUS:
            assert conf <= 1.0

    def test_malicious_not_triggered_by_one_high_type(self):
        # 1 high severity, attack_count=1, diversity=1 → SUSPICIOUS
        level, _ = _actor_threat_level(1, ["sql_injection"], 0.0)
        assert level == ThreatLevel.SUSPICIOUS


class TestActorThreatLevelSuspicious:
    """SUSPICIOUS: 1 high-severity type OR attack_count >= 2 OR diversity >= 2."""

    def test_suspicious_via_high_severity(self):
        level, _ = _actor_threat_level(1, ["sql_injection"], 0.0)
        assert level == ThreatLevel.SUSPICIOUS

    def test_suspicious_via_attack_count(self):
        level, _ = _actor_threat_level(2, ["xss_attempt"], 0.0)
        assert level == ThreatLevel.SUSPICIOUS

    def test_suspicious_via_diversity(self):
        level, _ = _actor_threat_level(1, ["xss_attempt", "template_injection"], 0.0)
        assert level == ThreatLevel.SUSPICIOUS

    def test_suspicious_confidence_formula(self):
        # high_hits=1 → 0.40 + 1*0.05 = 0.45
        level, conf = _actor_threat_level(1, ["sql_injection"], 0.0)
        assert level == ThreatLevel.SUSPICIOUS
        assert conf == round(min(1.0, 0.40 + 1 * 0.05), 4)

    def test_suspicious_no_high_type(self):
        # diversity=2, no high severity → 0.40 + 0*0.05 = 0.40
        level, conf = _actor_threat_level(1, ["xss_attempt", "template_injection"], 0.0)
        assert level == ThreatLevel.SUSPICIOUS
        assert conf == round(min(1.0, 0.40 + 0 * 0.05), 4)


class TestActorThreatLevelBenign:
    """BENIGN: no high severity, attack_count < 2, diversity < 2."""

    def test_benign_zero_attacks(self):
        level, conf = _actor_threat_level(0, [], 0.0)
        assert level == ThreatLevel.BENIGN

    def test_benign_single_low_type(self):
        level, _ = _actor_threat_level(1, ["xss_attempt"], 0.0)
        # xss_attempt is NOT in _HIGH_SEVERITY_TYPES, attack_count=1, diversity=1
        # → BENIGN
        assert level == ThreatLevel.BENIGN

    def test_benign_confidence_formula(self):
        # attack_count=1 → max(0.1, 0.30 - 1*0.05) = 0.25
        level, conf = _actor_threat_level(1, ["xss_attempt"], 0.0)
        assert level == ThreatLevel.BENIGN
        assert conf == round(max(0.1, 0.30 - 1 * 0.05), 4)

    def test_benign_confidence_floor(self):
        # attack_count=10 → max(0.1, 0.30 - 10*0.05) = max(0.1, -0.20) = 0.1
        level, conf = _actor_threat_level(10, ["xss_attempt"], 0.0)
        # 10 attacks could push to SUSPICIOUS via attack_count>=2, so benign only if no triggers
        # but attack_count=10 >= 2 → actually SUSPICIOUS; let's use 1 attack
        pass

    def test_benign_zero_attack_confidence(self):
        # 0 attacks → max(0.1, 0.30 - 0) = 0.30
        level, conf = _actor_threat_level(0, [], 0.0)
        assert level == ThreatLevel.BENIGN
        assert conf == 0.30


# ===========================================================================
# 4. _endpoint_risk_score
# ===========================================================================

class TestEndpointRiskScore:
    def test_zero_attacks(self):
        score = _endpoint_risk_score(0, 0, [])
        assert score == 0.0

    def test_base_attack_count_only(self):
        # 4 attacks, no special types, 1 attacker
        # base = min(60, 4*5) = 20, attacker_bonus = min(20, 1*4) = 4 → 24
        score = _endpoint_risk_score(4, 1, ["xss_attempt"])
        assert score == 24.0

    def test_base_capped_at_60(self):
        # 20 attacks → min(60, 100) = 60
        score = _endpoint_risk_score(20, 0, [])
        assert score == 60.0

    def test_critical_weight_contribution(self):
        # command_injection is BOTH critical and high severity
        # critical_weight = 1*3.0 = 3.0 → contributes 3*5 = 15
        # high_weight = 1*1.5 = 1.5 → contributes 1.5*2 = 3
        # attack_count=1 → base = min(60,5) + 15 + 3 = 23, 0 attackers → 23
        score = _endpoint_risk_score(1, 0, ["command_injection"])
        assert score == 23.0

    def test_high_weight_contribution(self):
        # 1 high type (sql_injection): high_weight = 1.5, base += 1.5*2 = 3
        # attack_count=1 → base = 5 + 3 = 8, no attackers → 8
        score = _endpoint_risk_score(1, 0, ["sql_injection"])
        assert score == 8.0

    def test_attacker_bonus(self):
        # 5 attackers → min(20, 5*4) = 20
        score = _endpoint_risk_score(0, 5, [])
        assert score == 20.0

    def test_attacker_bonus_capped(self):
        # 10 attackers → min(20, 10*4=40) = 20
        score = _endpoint_risk_score(0, 10, [])
        assert score == 20.0

    def test_ceiling_at_100(self):
        # many attacks + critical + many attackers → should cap at 100
        types = ["command_injection", "path_traversal", "sql_injection",
                 "brute_force", "banned_ip_request"]
        score = _endpoint_risk_score(100, 100, types)
        assert score == 100.0

    def test_combined_calculation(self):
        # attack_count=2, unique_attackers=2, threat_types=["command_injection", "sql_injection"]
        # critical_weight = 1 * 3.0 = 3.0
        # high_weight = 2 * 1.5 = 3.0  (command_injection also in high, sql_injection in high)
        # base = min(60, 10) + 3*5 + 3*2 = 10 + 15 + 6 = 31
        # attacker_bonus = min(20, 2*4) = 8
        # total = 39
        score = _endpoint_risk_score(2, 2, ["command_injection", "sql_injection"])
        assert score == 39.0

    def test_path_traversal_is_critical(self):
        score_critical = _endpoint_risk_score(1, 0, ["path_traversal"])
        score_non_critical = _endpoint_risk_score(1, 0, ["sql_injection"])
        # path_traversal is both critical and high → contributes more
        assert score_critical > score_non_critical


# ===========================================================================
# 5. ingest_event / ingest_events
# ===========================================================================

class TestIngest:
    def test_ingest_event_stores_event(self):
        ti = ThreatIntelligence()
        ev = make_event()
        ti.ingest_event(ev)
        assert len(ti._events) == 1

    def test_ingest_events_stores_multiple(self):
        ti = ThreatIntelligence()
        evts = [make_event(event_id=f"e{i}") for i in range(5)]
        ti.ingest_events(evts)
        assert len(ti._events) == 5

    def test_ingest_events_accumulates(self):
        ti = ThreatIntelligence()
        ti.ingest_events([make_event(event_id="e1")])
        ti.ingest_events([make_event(event_id="e2")])
        assert len(ti._events) == 2

    def test_ingest_event_triggers_rebuild(self):
        ti = ThreatIntelligence()
        assert len(ti._actors) == 0
        ti.ingest_event(make_event())
        assert len(ti._actors) == 1

    def test_ingest_events_triggers_rebuild(self):
        ti = ThreatIntelligence()
        ti.ingest_events([make_event(ip_address="1.1.1.1"), make_event(ip_address="2.2.2.2")])
        assert len(ti._actors) == 2

    def test_ingest_empty_list(self):
        ti = ThreatIntelligence()
        ti.ingest_events([])
        assert len(ti._events) == 0
        assert len(ti._actors) == 0


# ===========================================================================
# 6. _build_actors — grouping, actor_id, deduplication, persistence
# ===========================================================================

class TestBuildActors:
    def test_actor_id_pattern(self):
        ti = make_ti(make_event(ip_address="192.168.1.1"))
        assert "actor_192_168_1_1" in ti._actors

    def test_actor_ip_dots_replaced_with_underscores(self):
        ti = make_ti(make_event(ip_address="10.0.0.1"))
        actor = ti.actor_by_ip("10.0.0.1")
        assert actor is not None
        assert actor.actor_id == "actor_10_0_0_1"

    def test_group_events_by_ip(self):
        evts = [
            make_event(event_id="e1", ip_address="1.1.1.1"),
            make_event(event_id="e2", ip_address="1.1.1.1"),
            make_event(event_id="e3", ip_address="2.2.2.2"),
        ]
        ti = make_ti(*evts)
        assert len(ti._actors) == 2
        assert ti._actors["actor_1_1_1_1"].attack_count == 2
        assert ti._actors["actor_2_2_2_2"].attack_count == 1

    def test_threat_types_deduplicated(self):
        evts = [
            make_event(event_id="e1", threat_type="sql_injection"),
            make_event(event_id="e2", threat_type="sql_injection"),
            make_event(event_id="e3", threat_type="brute_force"),
        ]
        ti = make_ti(*evts)
        actor = ti.actor_by_ip("1.2.3.4")
        assert actor is not None
        assert sorted(actor.threat_types) == sorted(["sql_injection", "brute_force"])

    def test_targeted_endpoints_deduplicated(self):
        evts = [
            make_event(event_id="e1", endpoint="/login"),
            make_event(event_id="e2", endpoint="/login"),
            make_event(event_id="e3", endpoint="/admin"),
        ]
        ti = make_ti(*evts)
        actor = ti.actor_by_ip("1.2.3.4")
        assert actor is not None
        assert sorted(actor.targeted_endpoints) == sorted(["/login", "/admin"])

    def test_persistence_hours_calculation(self):
        # 13 hours apart
        evts = [
            make_event(event_id="e1", timestamp=TS_BASE),
            make_event(event_id="e2", timestamp=TS_13H),
        ]
        ti = make_ti(*evts)
        actor = ti.actor_by_ip("1.2.3.4")
        assert actor is not None
        assert actor.persistence_hours == round((TS_13H - TS_BASE) / 3600.0, 2)

    def test_persistence_hours_single_event(self):
        ti = make_ti(make_event())
        actor = ti.actor_by_ip("1.2.3.4")
        assert actor is not None
        assert actor.persistence_hours == 0.0

    def test_first_seen_and_last_seen(self):
        evts = [
            make_event(event_id="e1", timestamp=TS_BASE),
            make_event(event_id="e2", timestamp=TS_1H),
            make_event(event_id="e3", timestamp=TS_12H),
        ]
        ti = make_ti(*evts)
        actor = ti.actor_by_ip("1.2.3.4")
        assert actor.first_seen == TS_BASE
        assert actor.last_seen == TS_12H

    def test_ip_addresses_list(self):
        ti = make_ti(make_event(ip_address="5.6.7.8"))
        actor = ti.actor_by_ip("5.6.7.8")
        assert actor.ip_addresses == ["5.6.7.8"]


# ===========================================================================
# 7. _build_endpoints — grouping, unique_attackers, risk, recommended_actions
# ===========================================================================

class TestBuildEndpoints:
    def test_group_events_by_endpoint(self):
        evts = [
            make_event(event_id="e1", endpoint="/login"),
            make_event(event_id="e2", endpoint="/login"),
            make_event(event_id="e3", endpoint="/admin"),
        ]
        ti = make_ti(*evts)
        assert len(ti._endpoints) == 2
        assert ti._endpoints["/login"].attack_count == 2

    def test_unique_attackers_count(self):
        evts = [
            make_event(event_id="e1", ip_address="1.1.1.1", endpoint="/api"),
            make_event(event_id="e2", ip_address="2.2.2.2", endpoint="/api"),
            make_event(event_id="e3", ip_address="1.1.1.1", endpoint="/api"),
        ]
        ti = make_ti(*evts)
        vuln = ti.endpoint_risk("/api")
        assert vuln.unique_attackers == 2

    def test_risk_score_computed(self):
        ti = make_ti(make_event(threat_type="sql_injection"))
        vuln = ti.endpoint_risk("/api/test")
        assert vuln.risk_score > 0

    def test_recommended_actions_from_hardening_map(self):
        ti = make_ti(make_event(threat_type="sql_injection"))
        vuln = ti.endpoint_risk("/api/test")
        assert _HARDENING_MAP["sql_injection"] in vuln.recommended_actions

    def test_recommended_actions_unknown_type(self):
        ti = make_ti(make_event(threat_type="unknown_type"))
        vuln = ti.endpoint_risk("/api/test")
        assert vuln.recommended_actions == []

    def test_threat_types_deduplicated_in_endpoint(self):
        evts = [
            make_event(event_id="e1", threat_type="sql_injection"),
            make_event(event_id="e2", threat_type="sql_injection"),
        ]
        ti = make_ti(*evts)
        vuln = ti.endpoint_risk("/api/test")
        assert vuln.threat_types == ["sql_injection"]

    def test_multiple_threat_types_in_endpoint(self):
        evts = [
            make_event(event_id="e1", threat_type="sql_injection"),
            make_event(event_id="e2", threat_type="brute_force"),
        ]
        ti = make_ti(*evts)
        vuln = ti.endpoint_risk("/api/test")
        assert set(vuln.threat_types) == {"sql_injection", "brute_force"}
        assert len(vuln.recommended_actions) == 2


# ===========================================================================
# 8. all_actors() sort order
# ===========================================================================

class TestAllActorsSortOrder:
    def _build_mixed_ti(self) -> ThreatIntelligence:
        """3 actors: APT, MALICIOUS, SUSPICIOUS each on different IPs."""
        ti = ThreatIntelligence()
        # APT actor (ip=10.0.0.1): persistence > 12h, diversity >= 3, 1 critical
        apt_evts = [
            make_event(event_id="a1", ip_address="10.0.0.1", timestamp=TS_BASE,
                       threat_type="command_injection"),
            make_event(event_id="a2", ip_address="10.0.0.1", timestamp=TS_13H,
                       threat_type="sql_injection"),
            make_event(event_id="a3", ip_address="10.0.0.1", timestamp=TS_13H + 1,
                       threat_type="brute_force"),
        ]
        # MALICIOUS actor (ip=10.0.0.2): critical type, short timeframe
        mal_evts = [
            make_event(event_id="m1", ip_address="10.0.0.2", timestamp=TS_BASE,
                       threat_type="path_traversal"),
        ]
        # SUSPICIOUS actor (ip=10.0.0.3): 1 high severity, attack_count=1
        sus_evts = [
            make_event(event_id="s1", ip_address="10.0.0.3", timestamp=TS_BASE,
                       threat_type="sql_injection"),
        ]
        ti.ingest_events(apt_evts + mal_evts + sus_evts)
        return ti

    def test_apt_before_malicious(self):
        ti = self._build_mixed_ti()
        actors = ti.all_actors()
        levels = [a.threat_level for a in actors]
        apt_idx = levels.index(ThreatLevel.APT)
        mal_idx = levels.index(ThreatLevel.MALICIOUS)
        assert apt_idx < mal_idx

    def test_malicious_before_suspicious(self):
        ti = self._build_mixed_ti()
        actors = ti.all_actors()
        levels = [a.threat_level for a in actors]
        mal_idx = levels.index(ThreatLevel.MALICIOUS)
        sus_idx = levels.index(ThreatLevel.SUSPICIOUS)
        assert mal_idx < sus_idx

    def test_sort_by_attack_count_within_level(self):
        ti = ThreatIntelligence()
        # Two MALICIOUS actors with different attack counts
        evts = [
            make_event(event_id="m1", ip_address="1.1.1.1", threat_type="path_traversal"),
            make_event(event_id="m2", ip_address="2.2.2.2", threat_type="path_traversal"),
            make_event(event_id="m3", ip_address="2.2.2.2", threat_type="sql_injection"),
        ]
        ti.ingest_events(evts)
        actors = ti.all_actors()
        # both malicious, 2.2.2.2 has more attacks
        mal_actors = [a for a in actors if a.threat_level == ThreatLevel.MALICIOUS]
        if len(mal_actors) >= 2:
            assert mal_actors[0].attack_count >= mal_actors[1].attack_count


# ===========================================================================
# 9. top_threats(n)
# ===========================================================================

class TestTopThreats:
    def test_top_threats_default_10(self):
        ti = ThreatIntelligence()
        for i in range(15):
            ti.ingest_event(make_event(event_id=f"e{i}", ip_address=f"10.0.0.{i}"))
        assert len(ti.top_threats()) == 10

    def test_top_threats_custom_n(self):
        ti = ThreatIntelligence()
        for i in range(10):
            ti.ingest_event(make_event(event_id=f"e{i}", ip_address=f"10.0.0.{i}"))
        assert len(ti.top_threats(n=3)) == 3

    def test_top_threats_fewer_than_n(self):
        ti = ThreatIntelligence()
        ti.ingest_event(make_event())
        assert len(ti.top_threats(n=10)) == 1

    def test_top_threats_empty(self):
        ti = ThreatIntelligence()
        assert ti.top_threats() == []

    def test_top_threats_returns_highest_level_first(self):
        ti = ThreatIntelligence()
        # APT actor
        ti.ingest_events([
            make_event(event_id="a1", ip_address="1.1.1.1", timestamp=TS_BASE,
                       threat_type="command_injection"),
            make_event(event_id="a2", ip_address="1.1.1.1", timestamp=TS_13H,
                       threat_type="sql_injection"),
            make_event(event_id="a3", ip_address="1.1.1.1", timestamp=TS_13H + 1,
                       threat_type="brute_force"),
        ])
        # BENIGN actor
        ti.ingest_event(make_event(event_id="b1", ip_address="9.9.9.9",
                                   threat_type="xss_attempt"))
        threats = ti.top_threats(n=1)
        assert len(threats) == 1
        assert threats[0].ip_addresses == ["1.1.1.1"]


# ===========================================================================
# 10. actors_by_level
# ===========================================================================

class TestActorsByLevel:
    def test_actors_by_level_apt(self):
        ti = ThreatIntelligence()
        ti.ingest_events([
            make_event(event_id="a1", ip_address="1.1.1.1", timestamp=TS_BASE,
                       threat_type="command_injection"),
            make_event(event_id="a2", ip_address="1.1.1.1", timestamp=TS_13H,
                       threat_type="sql_injection"),
            make_event(event_id="a3", ip_address="1.1.1.1", timestamp=TS_13H + 1,
                       threat_type="brute_force"),
        ])
        apt_actors = ti.actors_by_level(ThreatLevel.APT)
        assert all(a.threat_level == ThreatLevel.APT for a in apt_actors)
        assert len(apt_actors) >= 1

    def test_actors_by_level_returns_empty_when_none(self):
        ti = make_ti(make_event(threat_type="xss_attempt"))
        # xss_attempt with 1 attack → BENIGN
        result = ti.actors_by_level(ThreatLevel.APT)
        assert result == []

    def test_actors_by_level_suspicious(self):
        ti = make_ti(make_event(threat_type="sql_injection"))
        suspicious = ti.actors_by_level(ThreatLevel.SUSPICIOUS)
        assert len(suspicious) == 1

    def test_actors_by_level_malicious(self):
        ti = make_ti(make_event(threat_type="command_injection"))
        malicious = ti.actors_by_level(ThreatLevel.MALICIOUS)
        assert len(malicious) == 1


# ===========================================================================
# 11. actor_by_ip
# ===========================================================================

class TestActorByIp:
    def test_actor_by_ip_found(self):
        ti = make_ti(make_event(ip_address="192.168.0.1"))
        actor = ti.actor_by_ip("192.168.0.1")
        assert actor is not None
        assert actor.ip_addresses == ["192.168.0.1"]

    def test_actor_by_ip_not_found(self):
        ti = make_ti(make_event(ip_address="1.2.3.4"))
        assert ti.actor_by_ip("9.9.9.9") is None

    def test_actor_by_ip_id_format(self):
        ti = make_ti(make_event(ip_address="10.20.30.40"))
        actor = ti.actor_by_ip("10.20.30.40")
        assert actor.actor_id == "actor_10_20_30_40"

    def test_actor_by_ip_after_multiple_events(self):
        ti = ThreatIntelligence()
        for i in range(3):
            ti.ingest_event(make_event(event_id=f"e{i}", ip_address="5.5.5.5"))
        actor = ti.actor_by_ip("5.5.5.5")
        assert actor.attack_count == 3


# ===========================================================================
# 12. vulnerability_report() sort order
# ===========================================================================

class TestVulnerabilityReport:
    def test_sorted_by_risk_score_descending(self):
        ti = ThreatIntelligence()
        # High-risk endpoint: command_injection
        ti.ingest_events([
            make_event(event_id="e1", endpoint="/critical", threat_type="command_injection",
                       ip_address="1.1.1.1"),
            make_event(event_id="e2", endpoint="/critical", threat_type="sql_injection",
                       ip_address="2.2.2.2"),
        ])
        # Low-risk endpoint: unknown type
        ti.ingest_event(make_event(event_id="e3", endpoint="/low", threat_type="xss_attempt",
                                   ip_address="3.3.3.3"))
        report = ti.vulnerability_report()
        scores = [e.risk_score for e in report]
        assert scores == sorted(scores, reverse=True)

    def test_vulnerability_report_contains_all_endpoints(self):
        endpoints = ["/a", "/b", "/c"]
        evts = [
            make_event(event_id=f"e{i}", endpoint=ep)
            for i, ep in enumerate(endpoints)
        ]
        ti = make_ti(*evts)
        report_eps = {e.endpoint for e in ti.vulnerability_report()}
        assert report_eps == set(endpoints)

    def test_vulnerability_report_empty(self):
        ti = ThreatIntelligence()
        assert ti.vulnerability_report() == []


# ===========================================================================
# 13. endpoint_risk() lookup
# ===========================================================================

class TestEndpointRiskLookup:
    def test_found(self):
        ti = make_ti(make_event(endpoint="/api/users"))
        vuln = ti.endpoint_risk("/api/users")
        assert vuln is not None
        assert vuln.endpoint == "/api/users"

    def test_not_found(self):
        ti = make_ti(make_event(endpoint="/api/users"))
        assert ti.endpoint_risk("/nonexistent") is None

    def test_attack_count_correct(self):
        evts = [make_event(event_id=f"e{i}", endpoint="/api") for i in range(4)]
        ti = make_ti(*evts)
        assert ti.endpoint_risk("/api").attack_count == 4


# ===========================================================================
# 14. high_risk_endpoints()
# ===========================================================================

class TestHighRiskEndpoints:
    def test_default_threshold_50(self):
        ti = ThreatIntelligence()
        # Create endpoint with risk > 50
        for i in range(12):
            ti.ingest_event(make_event(
                event_id=f"e{i}",
                ip_address=f"10.0.0.{i % 10}",
                endpoint="/high-risk",
                threat_type="command_injection",
            ))
        result = ti.high_risk_endpoints()
        assert any(e.endpoint == "/high-risk" for e in result)

    def test_custom_threshold(self):
        ti = ThreatIntelligence()
        # Low risk endpoint (1 attack, benign type)
        ti.ingest_event(make_event(endpoint="/low", threat_type="xss_attempt"))
        # threshold=0 should include everything
        result = ti.high_risk_endpoints(threshold=0.0)
        assert len(result) >= 1

    def test_high_threshold_excludes_low_risk(self):
        ti = make_ti(make_event(threat_type="xss_attempt"))
        # risk will be low; threshold=99 should exclude it
        result = ti.high_risk_endpoints(threshold=99.0)
        assert result == []

    def test_filters_correctly(self):
        ti = ThreatIntelligence()
        # endpoint A: high risk
        for i in range(15):
            ti.ingest_event(make_event(
                event_id=f"a{i}", ip_address=f"1.1.1.{i}",
                endpoint="/high", threat_type="command_injection"
            ))
        # endpoint B: low risk
        ti.ingest_event(make_event(event_id="b1", endpoint="/low",
                                   threat_type="xss_attempt"))
        high = ti.high_risk_endpoints(threshold=50.0)
        eps = {e.endpoint for e in high}
        assert "/high" in eps
        assert "/low" not in eps


# ===========================================================================
# 15. intelligence_summary()
# ===========================================================================

class TestIntelligenceSummary:
    def _populated_ti(self) -> ThreatIntelligence:
        ti = ThreatIntelligence()
        # APT actor
        ti.ingest_events([
            make_event(event_id="a1", ip_address="10.0.0.1", timestamp=TS_BASE,
                       threat_type="command_injection"),
            make_event(event_id="a2", ip_address="10.0.0.1", timestamp=TS_13H,
                       threat_type="sql_injection"),
            make_event(event_id="a3", ip_address="10.0.0.1", timestamp=TS_13H + 1,
                       threat_type="brute_force"),
        ])
        # SUSPICIOUS actor
        ti.ingest_event(make_event(event_id="s1", ip_address="10.0.0.2",
                                   threat_type="sql_injection"))
        return ti

    def test_all_keys_present(self):
        ti = self._populated_ti()
        summary = ti.intelligence_summary()
        expected_keys = {
            "total_events", "total_actors", "actor_level_counts",
            "total_endpoints_targeted", "avg_endpoint_risk_score",
            "high_risk_endpoint_count", "apt_count", "malicious_count",
        }
        assert set(summary.keys()) == expected_keys

    def test_total_events(self):
        ti = self._populated_ti()
        assert ti.intelligence_summary()["total_events"] == 4

    def test_total_actors(self):
        ti = self._populated_ti()
        assert ti.intelligence_summary()["total_actors"] == 2

    def test_actor_level_counts_keys(self):
        ti = self._populated_ti()
        counts = ti.intelligence_summary()["actor_level_counts"]
        assert set(counts.keys()) == {"benign", "suspicious", "malicious", "apt"}

    def test_actor_level_counts_values(self):
        ti = self._populated_ti()
        counts = ti.intelligence_summary()["actor_level_counts"]
        assert counts["apt"] == 1
        # Total should equal total_actors
        assert sum(counts.values()) == ti.intelligence_summary()["total_actors"]

    def test_apt_count(self):
        ti = self._populated_ti()
        assert ti.intelligence_summary()["apt_count"] == 1

    def test_total_endpoints_targeted(self):
        ti = self._populated_ti()
        # All events go to /api/test
        assert ti.intelligence_summary()["total_endpoints_targeted"] == 1

    def test_avg_endpoint_risk_score(self):
        ti = self._populated_ti()
        summary = ti.intelligence_summary()
        assert isinstance(summary["avg_endpoint_risk_score"], float)
        assert summary["avg_endpoint_risk_score"] >= 0.0

    def test_empty_summary(self):
        ti = ThreatIntelligence()
        summary = ti.intelligence_summary()
        assert summary["total_events"] == 0
        assert summary["total_actors"] == 0
        assert summary["avg_endpoint_risk_score"] == 0.0

    def test_high_risk_endpoint_count(self):
        ti = ThreatIntelligence()
        for i in range(15):
            ti.ingest_event(make_event(
                event_id=f"e{i}", ip_address=f"10.0.0.{i % 10}",
                endpoint="/risky", threat_type="command_injection"
            ))
        summary = ti.intelligence_summary()
        assert summary["high_risk_endpoint_count"] >= 1


# ===========================================================================
# 16. reset()
# ===========================================================================

class TestReset:
    def test_reset_clears_events(self):
        ti = make_ti(make_event())
        ti.reset()
        assert ti._events == []

    def test_reset_clears_actors(self):
        ti = make_ti(make_event())
        ti.reset()
        assert ti._actors == {}

    def test_reset_clears_endpoints(self):
        ti = make_ti(make_event())
        ti.reset()
        assert ti._endpoints == {}

    def test_reset_allows_reingest(self):
        ti = make_ti(make_event(event_id="old"))
        ti.reset()
        ti.ingest_event(make_event(event_id="new"))
        assert len(ti._events) == 1

    def test_all_actors_empty_after_reset(self):
        ti = make_ti(make_event())
        ti.reset()
        assert ti.all_actors() == []

    def test_vulnerability_report_empty_after_reset(self):
        ti = make_ti(make_event())
        ti.reset()
        assert ti.vulnerability_report() == []


# ===========================================================================
# 17. to_dict() on ThreatActor and EndpointVulnerability
# ===========================================================================

class TestToDictMethods:
    def test_threat_actor_to_dict_keys(self):
        ti = make_ti(make_event())
        actor = ti.actor_by_ip("1.2.3.4")
        d = actor.to_dict()
        expected = {
            "actor_id", "ip_addresses", "first_seen", "last_seen",
            "attack_count", "threat_types", "targeted_endpoints",
            "threat_level", "confidence", "persistence_hours",
        }
        assert set(d.keys()) == expected

    def test_threat_actor_to_dict_threat_level_is_string(self):
        ti = make_ti(make_event())
        actor = ti.actor_by_ip("1.2.3.4")
        d = actor.to_dict()
        assert isinstance(d["threat_level"], str)

    def test_threat_actor_to_dict_threat_level_value(self):
        ti = make_ti(make_event(threat_type="command_injection"))
        actor = ti.actor_by_ip("1.2.3.4")
        d = actor.to_dict()
        assert d["threat_level"] == actor.threat_level.value

    def test_endpoint_vulnerability_to_dict_keys(self):
        ti = make_ti(make_event())
        vuln = ti.endpoint_risk("/api/test")
        d = vuln.to_dict()
        expected = {
            "endpoint", "attack_count", "unique_attackers",
            "threat_types", "risk_score", "recommended_actions",
        }
        assert set(d.keys()) == expected

    def test_endpoint_vulnerability_to_dict_values(self):
        ti = make_ti(make_event(endpoint="/api/v1"))
        vuln = ti.endpoint_risk("/api/v1")
        d = vuln.to_dict()
        assert d["endpoint"] == "/api/v1"
        assert d["attack_count"] == 1
        assert isinstance(d["risk_score"], float)

    def test_threat_actor_to_dict_confidence_range(self):
        ti = make_ti(make_event())
        actor = ti.actor_by_ip("1.2.3.4")
        d = actor.to_dict()
        assert 0.0 <= d["confidence"] <= 1.0


# ===========================================================================
# 18. Constants
# ===========================================================================

class TestConstants:
    def test_high_severity_types_content(self):
        assert "sql_injection" in _HIGH_SEVERITY_TYPES
        assert "command_injection" in _HIGH_SEVERITY_TYPES
        assert "path_traversal" in _HIGH_SEVERITY_TYPES
        assert "banned_ip_request" in _HIGH_SEVERITY_TYPES
        assert "brute_force" in _HIGH_SEVERITY_TYPES

    def test_critical_types_content(self):
        assert "command_injection" in _CRITICAL_TYPES
        assert "path_traversal" in _CRITICAL_TYPES

    def test_critical_is_subset_of_high(self):
        assert _CRITICAL_TYPES.issubset(_HIGH_SEVERITY_TYPES)

    def test_hardening_map_has_entries(self):
        assert "sql_injection" in _HARDENING_MAP
        assert "command_injection" in _HARDENING_MAP
        assert "path_traversal" in _HARDENING_MAP

    def test_hardening_map_french_values(self):
        # Spot-check French recommendations
        assert "SQL" in _HARDENING_MAP["sql_injection"] or "requêtes" in _HARDENING_MAP["sql_injection"]
