"""
Comprehensive pytest tests for the SecurityMonitor module.
"""

from __future__ import annotations

import time
import pytest

from swarm.intelligence.security_monitor import (
    SecurityMonitor,
    SecurityEvent,
    ThreatSeverity,
    RecommendedAction,
    IPRecord,
    _SQL_PATTERNS,
    _XSS_PATTERNS,
    _PATH_TRAVERSAL,
    _COMMAND_INJECTION,
    _TEMPLATE_INJECTION,
    _LARGE_PAYLOAD_THRESHOLD,
    _BRUTE_FORCE_THRESHOLD,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

TS = 1_700_000_000.0  # fixed timestamp for deterministic tests


def fresh() -> SecurityMonitor:
    """Return a new, empty SecurityMonitor."""
    return SecurityMonitor()


# ===========================================================================
# TestThreatSeverity
# ===========================================================================


class TestThreatSeverity:
    def test_info_value(self):
        assert ThreatSeverity.INFO.value == "info"

    def test_low_value(self):
        assert ThreatSeverity.LOW.value == "low"

    def test_high_value(self):
        assert ThreatSeverity.HIGH.value == "high"

    def test_critical_value(self):
        assert ThreatSeverity.CRITICAL.value == "critical"

    def test_medium_value(self):
        assert ThreatSeverity.MEDIUM.value == "medium"


# ===========================================================================
# TestRecommendedAction
# ===========================================================================


class TestRecommendedAction:
    def test_log_value(self):
        assert RecommendedAction.LOG.value == "log"

    def test_alert_value(self):
        assert RecommendedAction.ALERT.value == "alert"

    def test_block_value(self):
        assert RecommendedAction.BLOCK.value == "block"

    def test_ban_value(self):
        assert RecommendedAction.BAN.value == "ban"


# ===========================================================================
# TestSecurityEvent
# ===========================================================================


class TestSecurityEvent:
    def _make_event(self) -> SecurityEvent:
        return SecurityEvent(
            event_id="evt_000001",
            timestamp=TS,
            ip_address="1.2.3.4",
            endpoint="/api/test",
            threat_type="sql_injection",
            severity=ThreatSeverity.HIGH,
            recommended_action=RecommendedAction.BLOCK,
            matched_pattern="UNION SELECT",
            raw_input="id=1 UNION SELECT * FROM users",
            details="test detail",
        )

    def test_to_dict_contains_expected_keys(self):
        d = self._make_event().to_dict()
        expected_keys = {
            "event_id", "timestamp", "ip_address", "endpoint",
            "threat_type", "severity", "recommended_action",
            "matched_pattern", "raw_input", "details",
        }
        assert expected_keys == set(d.keys())

    def test_to_dict_severity_is_string(self):
        d = self._make_event().to_dict()
        assert isinstance(d["severity"], str)

    def test_to_dict_severity_value(self):
        d = self._make_event().to_dict()
        assert d["severity"] == "high"

    def test_to_dict_action_is_string(self):
        d = self._make_event().to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_action_value(self):
        d = self._make_event().to_dict()
        assert d["recommended_action"] == "block"


# ===========================================================================
# TestSQLInjectionDetection
# ===========================================================================


class TestSQLInjectionDetection:
    def test_union_select(self):
        m = fresh()
        evt = m.scan_request("10.0.0.1", "/search", "id=1 UNION SELECT * FROM users", TS)
        assert evt is not None
        assert evt.threat_type == "sql_injection"
        assert evt.severity == ThreatSeverity.HIGH
        assert evt.recommended_action == RecommendedAction.BLOCK

    def test_drop_table(self):
        m = fresh()
        evt = m.scan_request("10.0.0.2", "/q", "DROP TABLE users", TS)
        assert evt is not None
        assert evt.threat_type == "sql_injection"

    def test_comment_injection(self):
        m = fresh()
        evt = m.scan_request("10.0.0.3", "/login", "' ; -- ", TS)
        assert evt is not None
        assert evt.threat_type == "sql_injection"

    def test_xp_cmdshell(self):
        m = fresh()
        evt = m.scan_request("10.0.0.4", "/api", "xp_cmdshell('dir')", TS)
        assert evt is not None
        assert evt.threat_type == "sql_injection"

    def test_exec_keyword(self):
        m = fresh()
        evt = m.scan_request("10.0.0.5", "/proc", "EXEC('malicious')", TS)
        assert evt is not None
        assert evt.threat_type == "sql_injection"


# ===========================================================================
# TestXSSDetection
# ===========================================================================


class TestXSSDetection:
    def test_script_tag(self):
        m = fresh()
        evt = m.scan_request("10.1.0.1", "/comment", "<script>alert(1)</script>", TS)
        assert evt is not None
        assert evt.threat_type == "xss_attempt"
        assert evt.severity == ThreatSeverity.HIGH

    def test_javascript_protocol(self):
        m = fresh()
        evt = m.scan_request("10.1.0.2", "/link", "javascript:void(0)", TS)
        assert evt is not None
        assert evt.threat_type == "xss_attempt"

    def test_onerror_handler(self):
        m = fresh()
        evt = m.scan_request("10.1.0.3", "/img", '<img src=x onerror=alert(1)>', TS)
        assert evt is not None
        assert evt.threat_type == "xss_attempt"

    def test_iframe_tag(self):
        m = fresh()
        evt = m.scan_request("10.1.0.4", "/page", "<iframe src='evil.com'>", TS)
        assert evt is not None
        assert evt.threat_type == "xss_attempt"


# ===========================================================================
# TestPathTraversalDetection
# ===========================================================================


class TestPathTraversalDetection:
    def test_dotdot_slash(self):
        m = fresh()
        evt = m.scan_request("10.2.0.1", "/file", "../../../etc/shadow", TS)
        assert evt is not None
        assert evt.threat_type == "path_traversal"
        assert evt.severity == ThreatSeverity.CRITICAL
        assert evt.recommended_action == RecommendedAction.BAN

    def test_etc_passwd(self):
        m = fresh()
        evt = m.scan_request("10.2.0.2", "/read", "/etc/passwd", TS)
        assert evt is not None
        assert evt.threat_type == "path_traversal"

    def test_encoded_traversal(self):
        m = fresh()
        evt = m.scan_request("10.2.0.3", "/download", "%2E%2E%2Fsecret", TS)
        assert evt is not None
        assert evt.threat_type == "path_traversal"


# ===========================================================================
# TestCommandInjection
# ===========================================================================


class TestCommandInjection:
    def test_semicolon_ls(self):
        m = fresh()
        evt = m.scan_request("10.3.0.1", "/run", "foo; ls -la", TS)
        assert evt is not None
        assert evt.threat_type == "command_injection"
        assert evt.severity == ThreatSeverity.CRITICAL

    def test_pipe_cat(self):
        m = fresh()
        evt = m.scan_request("10.3.0.2", "/exec", "bar | cat /etc/hosts", TS)
        assert evt is not None
        assert evt.threat_type == "command_injection"

    def test_backtick_cmd(self):
        m = fresh()
        evt = m.scan_request("10.3.0.3", "/shell", "`id`", TS)
        assert evt is not None
        assert evt.threat_type == "command_injection"


# ===========================================================================
# TestTemplateInjection
# ===========================================================================


class TestTemplateInjection:
    def test_double_curly(self):
        m = fresh()
        evt = m.scan_request("10.4.0.1", "/render", "{{7*7}}", TS)
        assert evt is not None
        assert evt.threat_type == "template_injection"
        assert evt.severity == ThreatSeverity.HIGH
        assert evt.recommended_action == RecommendedAction.BLOCK

    def test_dollar_curly(self):
        m = fresh()
        evt = m.scan_request("10.4.0.2", "/tmpl", "${7*7}", TS)
        assert evt is not None
        assert evt.threat_type == "template_injection"


# ===========================================================================
# TestOversizedPayload
# ===========================================================================


class TestOversizedPayload:
    def test_oversized_returns_event(self):
        m = fresh()
        big = "A" * (_LARGE_PAYLOAD_THRESHOLD + 1)
        evt = m.scan_request("10.5.0.1", "/upload", big, TS)
        assert evt is not None
        assert evt.threat_type == "oversized_payload"
        assert evt.severity == ThreatSeverity.MEDIUM
        assert evt.recommended_action == RecommendedAction.BLOCK

    def test_borderline_payload_is_blocked(self):
        m = fresh()
        # exactly threshold + 1 byte should trigger
        big = "B" * (_LARGE_PAYLOAD_THRESHOLD + 1)
        evt = m.scan_request("10.5.0.2", "/data", big, TS)
        assert evt is not None
        assert m.is_blocked("10.5.0.2")

    def test_payload_at_threshold_is_clean(self):
        m = fresh()
        # exactly at threshold: NOT oversized (strictly greater triggers)
        exact = "C" * _LARGE_PAYLOAD_THRESHOLD
        evt = m.scan_request("10.5.0.3", "/data", exact, TS)
        # may or may not be None depending on content — since "CCC..." has no threat patterns,
        # it should be None
        assert evt is None


# ===========================================================================
# TestCleanInput
# ===========================================================================


class TestCleanInput:
    def test_normal_text(self):
        m = fresh()
        assert m.scan_request("1.1.1.1", "/api", "hello world", TS) is None

    def test_valid_json(self):
        m = fresh()
        assert m.scan_request("1.1.1.2", "/api", '{"name": "Alice", "age": 30}', TS) is None

    def test_spaces_only(self):
        m = fresh()
        assert m.scan_request("1.1.1.3", "/api", "     ", TS) is None

    def test_numbers(self):
        m = fresh()
        assert m.scan_request("1.1.1.4", "/api", "42 3.14 0", TS) is None


# ===========================================================================
# TestIPManagement
# ===========================================================================


class TestIPManagement:
    def test_block_ip_sets_blocked(self):
        m = fresh()
        m.block_ip("2.2.2.2")
        assert m.is_blocked("2.2.2.2")

    def test_block_ip_does_not_ban(self):
        m = fresh()
        m.block_ip("2.2.2.3")
        assert not m.is_banned("2.2.2.3")

    def test_ban_ip_sets_banned(self):
        m = fresh()
        m.ban_ip("3.3.3.3")
        assert m.is_banned("3.3.3.3")

    def test_ban_ip_also_sets_blocked(self):
        m = fresh()
        m.ban_ip("3.3.3.4")
        assert m.is_blocked("3.3.3.4")

    def test_unblock_ip_clears_blocked(self):
        m = fresh()
        m.block_ip("4.4.4.4")
        m.unblock_ip("4.4.4.4")
        assert not m.is_blocked("4.4.4.4")

    def test_unknown_ip_not_blocked_or_banned(self):
        m = fresh()
        assert not m.is_blocked("9.9.9.9")
        assert not m.is_banned("9.9.9.9")


# ===========================================================================
# TestAutoBanOnCritical
# ===========================================================================


class TestAutoBanOnCritical:
    def test_path_traversal_auto_bans_ip(self):
        m = fresh()
        ip = "5.5.5.1"
        evt = m.scan_request(ip, "/file", "../../../etc/shadow", TS)
        assert evt is not None
        assert m.is_banned(ip)

    def test_path_traversal_also_blocks_ip(self):
        m = fresh()
        ip = "5.5.5.2"
        m.scan_request(ip, "/file", "../../../etc/passwd", TS)
        assert m.is_blocked(ip)


# ===========================================================================
# TestAutoBlockOnHigh
# ===========================================================================


class TestAutoBlockOnHigh:
    def test_sql_injection_auto_blocks_ip(self):
        m = fresh()
        ip = "6.6.6.1"
        evt = m.scan_request(ip, "/search", "UNION SELECT 1,2,3", TS)
        assert evt is not None
        assert m.is_blocked(ip)

    def test_sql_injection_does_not_auto_ban(self):
        m = fresh()
        ip = "6.6.6.2"
        m.scan_request(ip, "/search", "UNION SELECT password FROM users", TS)
        assert not m.is_banned(ip)


# ===========================================================================
# TestBannedIPSubsequentRequest
# ===========================================================================


class TestBannedIPSubsequentRequest:
    def test_banned_ip_returns_event(self):
        m = fresh()
        ip = "7.7.7.1"
        m.ban_ip(ip, reason="manual")
        evt = m.scan_request(ip, "/api", "hello", TS)
        assert evt is not None

    def test_banned_ip_event_is_critical(self):
        m = fresh()
        ip = "7.7.7.2"
        m.ban_ip(ip, reason="manual")
        evt = m.scan_request(ip, "/api", "hello", TS)
        assert evt.severity == ThreatSeverity.CRITICAL

    def test_banned_ip_event_threat_type(self):
        m = fresh()
        ip = "7.7.7.3"
        m.ban_ip(ip, reason="manual")
        evt = m.scan_request(ip, "/api", "hello", TS)
        assert evt.threat_type == "banned_ip_request"
        assert evt.recommended_action == RecommendedAction.BAN


# ===========================================================================
# TestBruteForce
# ===========================================================================


class TestBruteForce:
    def test_single_failed_auth_returns_none(self):
        m = fresh()
        result = m.record_failed_auth("8.8.8.1", TS)
        assert result is None

    def test_below_threshold_returns_none(self):
        m = fresh()
        ip = "8.8.8.2"
        for _ in range(_BRUTE_FORCE_THRESHOLD - 1):
            result = m.record_failed_auth(ip, TS)
        assert result is None

    def test_threshold_hit_returns_event(self):
        m = fresh()
        ip = "8.8.8.3"
        event = None
        for _ in range(_BRUTE_FORCE_THRESHOLD):
            event = m.record_failed_auth(ip, TS)
        assert event is not None
        assert event.threat_type == "brute_force"
        assert event.severity == ThreatSeverity.CRITICAL

    def test_threshold_hit_bans_ip(self):
        m = fresh()
        ip = "8.8.8.4"
        for _ in range(_BRUTE_FORCE_THRESHOLD):
            m.record_failed_auth(ip, TS)
        assert m.is_banned(ip)


# ===========================================================================
# TestRateLimit
# ===========================================================================


class TestRateLimit:
    def test_requests_within_limit_return_true(self):
        m = fresh()
        ip = "9.0.0.1"
        for i in range(10):
            assert m.record_request(ip, TS + i) is True

    def test_exceeding_limit_returns_false(self):
        from swarm.intelligence.security_monitor import _RATE_LIMIT_MAX, _RATE_LIMIT_WINDOW
        m = fresh()
        ip = "9.0.0.2"
        # Fill up to max; all within the same window
        for i in range(_RATE_LIMIT_MAX):
            m.record_request(ip, TS + i * 0.1)
        # One more should exceed
        result = m.record_request(ip, TS + _RATE_LIMIT_MAX * 0.1)
        assert result is False

    def test_exceeding_limit_blocks_ip(self):
        from swarm.intelligence.security_monitor import _RATE_LIMIT_MAX
        m = fresh()
        ip = "9.0.0.3"
        for i in range(_RATE_LIMIT_MAX):
            m.record_request(ip, TS + i * 0.1)
        m.record_request(ip, TS + _RATE_LIMIT_MAX * 0.1)
        assert m.is_blocked(ip)


# ===========================================================================
# TestRecentEvents
# ===========================================================================


class TestRecentEvents:
    def test_newest_first_ordering(self):
        m = fresh()
        m.scan_request("10.0.1.1", "/a", "UNION SELECT 1", TS)
        m.scan_request("10.0.1.2", "/b", "UNION SELECT 2", TS + 1)
        m.scan_request("10.0.1.3", "/c", "UNION SELECT 3", TS + 2)
        events = m.recent_events(3)
        # Newest (TS+2) should be first
        assert events[0].timestamp == TS + 2
        assert events[-1].timestamp == TS

    def test_n_parameter_limits_count(self):
        m = fresh()
        for i in range(5):
            m.scan_request(f"10.0.2.{i+1}", "/x", "UNION SELECT 1", TS + i)
        events = m.recent_events(3)
        assert len(events) == 3

    def test_recent_events_default_up_to_50(self):
        m = fresh()
        # Generate 60 unique IPs each with a threat
        for i in range(60):
            m.scan_request(f"11.{i}.0.1", "/x", "UNION SELECT 1", TS + i)
        events = m.recent_events()  # default n=50
        assert len(events) == 50


# ===========================================================================
# TestEventFilters
# ===========================================================================


class TestEventFilters:
    def test_events_by_severity_returns_matching(self):
        m = fresh()
        m.scan_request("12.0.0.1", "/a", "UNION SELECT 1", TS)          # HIGH
        m.scan_request("12.0.0.2", "/b", "../../../etc/passwd", TS + 1)  # CRITICAL
        high_events = m.events_by_severity(ThreatSeverity.HIGH)
        assert all(e.severity == ThreatSeverity.HIGH for e in high_events)

    def test_events_by_severity_excludes_others(self):
        m = fresh()
        m.scan_request("12.0.1.1", "/a", "UNION SELECT 1", TS)
        critical_events = m.events_by_severity(ThreatSeverity.CRITICAL)
        # SQL injection is HIGH, not CRITICAL
        assert all(e.severity == ThreatSeverity.CRITICAL for e in critical_events)

    def test_events_by_ip_returns_matching(self):
        m = fresh()
        target_ip = "12.1.0.1"
        m.scan_request(target_ip, "/a", "UNION SELECT 1", TS)
        m.scan_request("12.1.0.2", "/b", "UNION SELECT 2", TS + 1)
        ip_events = m.events_by_ip(target_ip)
        assert len(ip_events) >= 1
        assert all(e.ip_address == target_ip for e in ip_events)

    def test_events_by_ip_excludes_other_ips(self):
        m = fresh()
        m.scan_request("12.2.0.1", "/a", "UNION SELECT 1", TS)
        m.scan_request("12.2.0.2", "/b", "UNION SELECT 2", TS + 1)
        ip_events = m.events_by_ip("12.2.0.1")
        assert all(e.ip_address == "12.2.0.1" for e in ip_events)


# ===========================================================================
# TestThreatSummary
# ===========================================================================


class TestThreatSummary:
    def _populated_monitor(self) -> SecurityMonitor:
        m = fresh()
        m.scan_request("13.0.0.1", "/a", "UNION SELECT 1", TS)          # HIGH sql
        m.scan_request("13.0.0.2", "/b", "<script>alert(1)</script>", TS + 1)  # HIGH xss
        m.scan_request("13.0.0.3", "/c", "../../../etc/passwd", TS + 2)  # CRITICAL path
        return m

    def test_all_keys_present(self):
        m = self._populated_monitor()
        summary = m.threat_summary()
        assert set(summary.keys()) == {
            "total_events", "severity_counts", "blocked_ips",
            "banned_ips", "top_threat_types",
        }

    def test_total_events_count(self):
        m = self._populated_monitor()
        summary = m.threat_summary()
        assert summary["total_events"] == 3

    def test_severity_counts_has_all_five_keys(self):
        m = self._populated_monitor()
        summary = m.threat_summary()
        assert set(summary["severity_counts"].keys()) == {"info", "low", "medium", "high", "critical"}

    def test_severity_counts_values(self):
        m = self._populated_monitor()
        summary = m.threat_summary()
        counts = summary["severity_counts"]
        assert counts["high"] == 2
        assert counts["critical"] == 1
        assert counts["info"] == 0

    def test_top_threat_types_format(self):
        m = self._populated_monitor()
        summary = m.threat_summary()
        top = summary["top_threat_types"]
        assert isinstance(top, list)
        for entry in top:
            assert "type" in entry
            assert "count" in entry
            assert isinstance(entry["count"], int)


# ===========================================================================
# TestReset
# ===========================================================================


class TestReset:
    def test_reset_clears_events(self):
        m = fresh()
        m.scan_request("14.0.0.1", "/a", "UNION SELECT 1", TS)
        m.reset()
        assert m.recent_events() == []

    def test_reset_clears_blocked_and_banned_ips(self):
        m = fresh()
        m.block_ip("14.1.0.1")
        m.ban_ip("14.1.0.2")
        m.reset()
        assert not m.is_blocked("14.1.0.1")
        assert not m.is_banned("14.1.0.2")
        summary = m.threat_summary()
        assert summary["blocked_ips"] == 0
        assert summary["banned_ips"] == 0
