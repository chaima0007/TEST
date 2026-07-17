"""
Tests for intelligence/performance_monitor.py
"""

import time
import pytest
from intelligence.performance_monitor import (
    PerformanceMonitor, AgentStats, DivisionStats, AgentHealth, Alert
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def mon() -> PerformanceMonitor:
    m = PerformanceMonitor()
    m.initialize_agents()
    return m


def mini_mon(agent_ids=None) -> PerformanceMonitor:
    m = PerformanceMonitor()
    m.initialize_agents(agent_ids or ["1.0", "1.1", "1.2", "2.1", "2.2"])
    return m


# ── initialize_agents ─────────────────────────────────────────────────────────

class TestInitializeAgents:
    def test_auto_creates_60_agents(self):
        m = PerformanceMonitor()
        m.initialize_agents()
        assert len(m._agents) == 60

    def test_custom_agent_list(self):
        m = PerformanceMonitor()
        m.initialize_agents(["1.1", "2.3", "3.5"])
        assert len(m._agents) == 3

    def test_division_assigned_from_id(self):
        m = PerformanceMonitor()
        m.initialize_agents(["3.7"])
        assert m._agents["3.7"].division == 3

    def test_initial_tasks_zero(self):
        m = mon()
        for stats in m._agents.values():
            assert stats.tasks_completed == 0
            assert stats.tasks_failed == 0


# ── record_task ───────────────────────────────────────────────────────────────

class TestRecordTask:
    def test_success_increments_completed(self):
        m = mini_mon()
        m.record_task("1.1", success=True, response_time_ms=120)
        assert m._agents["1.1"].tasks_completed == 1

    def test_failure_increments_failed(self):
        m = mini_mon()
        m.record_task("1.1", success=False, error_msg="timeout")
        assert m._agents["1.1"].tasks_failed == 1

    def test_response_time_accumulated(self):
        m = mini_mon()
        m.record_task("1.1", success=True, response_time_ms=100)
        m.record_task("1.1", success=True, response_time_ms=200)
        assert m._agents["1.1"].total_response_time_ms == 300

    def test_error_msg_stored(self):
        m = mini_mon()
        m.record_task("1.1", success=False, error_msg="API timeout")
        assert m._agents["1.1"].last_error == "API timeout"

    def test_heartbeat_updated_on_record(self):
        m = mini_mon()
        before = time.time()
        m.record_task("1.1", success=True)
        assert m._agents["1.1"].last_heartbeat >= before

    def test_unknown_agent_auto_registered(self):
        m = mini_mon()
        m.record_task("9.9", success=True)
        assert "9.9" in m._agents


# ── AgentStats properties ─────────────────────────────────────────────────────

class TestAgentStatsProperties:
    def test_error_rate_zero_when_no_tasks(self):
        stats = AgentStats("1.1", 1)
        assert stats.error_rate == 0.0

    def test_error_rate_calculation(self):
        stats = AgentStats("1.1", 1, tasks_completed=8, tasks_failed=2)
        assert stats.error_rate == pytest.approx(0.2, abs=0.001)

    def test_avg_response_time_zero_when_no_completed(self):
        stats = AgentStats("1.1", 1)
        assert stats.avg_response_time_ms == 0.0

    def test_avg_response_time_calculation(self):
        stats = AgentStats("1.1", 1, tasks_completed=2, total_response_time_ms=400)
        assert stats.avg_response_time_ms == 200.0

    def test_health_healthy_when_fresh_and_no_errors(self):
        stats = AgentStats("1.1", 1, tasks_completed=10)
        assert stats.health == AgentHealth.HEALTHY

    def test_health_degraded_when_error_rate_10_to_25(self):
        stats = AgentStats("1.1", 1, tasks_completed=9, tasks_failed=1)
        assert stats.health == AgentHealth.DEGRADED

    def test_health_critical_when_error_rate_above_25(self):
        stats = AgentStats("1.1", 1, tasks_completed=7, tasks_failed=3)
        assert stats.health == AgentHealth.CRITICAL

    def test_health_offline_when_heartbeat_old(self):
        stats = AgentStats("1.1", 1, last_heartbeat=time.time() - 400)
        assert stats.health == AgentHealth.OFFLINE

    def test_to_dict_has_all_keys(self):
        stats = AgentStats("1.1", 1, tasks_completed=5)
        d = stats.to_dict()
        for key in ("agent_id", "division", "tasks_completed", "tasks_failed",
                    "error_rate", "avg_response_time_ms", "health"):
            assert key in d


# ── DivisionStats ─────────────────────────────────────────────────────────────

class TestDivisionStats:
    def _make_div(self, completed=10, failed=0):
        agents = [
            AgentStats("1.1", 1, tasks_completed=completed // 2, tasks_failed=failed // 2),
            AgentStats("1.2", 1, tasks_completed=completed - completed // 2, tasks_failed=failed - failed // 2),
        ]
        return DivisionStats(division=1, name="Test", agents=agents)

    def test_healthy_count(self):
        div = self._make_div(completed=10, failed=0)
        assert div.healthy_count == 2

    def test_total_tasks(self):
        div = self._make_div(completed=10)
        assert div.total_tasks == 10

    def test_total_errors(self):
        div = self._make_div(completed=8, failed=2)
        assert div.total_errors == 2

    def test_division_error_rate(self):
        div = self._make_div(completed=8, failed=2)
        assert div.division_error_rate == pytest.approx(0.2, abs=0.001)

    def test_division_health_healthy(self):
        div = self._make_div(completed=10)
        assert div.health == AgentHealth.HEALTHY

    def test_division_health_critical_if_one_critical(self):
        agents = [
            AgentStats("1.1", 1, tasks_completed=3, tasks_failed=7),  # critical
            AgentStats("1.2", 1, tasks_completed=10),
        ]
        div = DivisionStats(1, "T", agents)
        assert div.health == AgentHealth.CRITICAL

    def test_to_dict_has_agents_list(self):
        div = self._make_div()
        d = div.to_dict()
        assert "agents" in d
        assert isinstance(d["agents"], list)


# ── get_division / get_all_divisions ─────────────────────────────────────────

class TestGetDivision:
    def test_get_division_returns_division_stats(self):
        m = mini_mon()
        div = m.get_division(1)
        assert isinstance(div, DivisionStats)

    def test_get_division_name_correct(self):
        m = mini_mon()
        div = m.get_division(1)
        assert "Détection" in div.name

    def test_get_all_divisions_returns_6(self):
        m = mon()
        divisions = m.get_all_divisions()
        assert len(divisions) == 6

    def test_get_all_divisions_sorted(self):
        m = mon()
        divisions = m.get_all_divisions()
        ids = [d.division for d in divisions]
        assert ids == sorted(ids)


# ── critical / offline / healthy count ───────────────────────────────────────

class TestHealthQueries:
    def test_critical_agents_empty_when_all_healthy(self):
        m = mini_mon()
        assert m.critical_agents() == []

    def test_critical_agents_detected(self):
        m = mini_mon()
        for _ in range(4):
            m.record_task("1.1", success=False)
        m.record_task("1.1", success=True)
        assert any(a.agent_id == "1.1" for a in m.critical_agents())

    def test_healthy_agent_count_all_when_initialized(self):
        m = mini_mon()
        assert m.healthy_agent_count() == 5


# ── alerts ────────────────────────────────────────────────────────────────────

class TestAlerts:
    def test_no_alerts_initially(self):
        assert mini_mon().get_alerts() == []

    def test_critical_task_generates_alert(self):
        m = mini_mon()
        for _ in range(4):
            m.record_task("1.1", success=False)
        m.record_task("1.1", success=True)
        alerts = m.get_alerts()
        assert len(alerts) > 0

    def test_alerts_filtered_by_level(self):
        m = mini_mon()
        for _ in range(4):
            m.record_task("1.1", success=False)
        m.record_task("1.1", success=True)
        criticals = m.get_alerts(level="critical")
        warnings = m.get_alerts(level="warning")
        assert all(a.level == "critical" for a in criticals)
        assert all(a.level == "warning" for a in warnings)

    def test_alert_to_dict_has_required_keys(self):
        alert = Alert("1.1", 1, "critical", "test message")
        d = alert.to_dict()
        for key in ("agent_id", "division", "level", "message", "timestamp"):
            assert key in d


# ── global_summary ────────────────────────────────────────────────────────────

class TestGlobalSummary:
    def test_summary_has_all_keys(self):
        s = mini_mon().global_summary()
        for key in ("total_agents", "healthy_agents", "degraded_agents",
                    "critical_agents", "offline_agents", "total_tasks_completed",
                    "total_tasks_failed", "global_error_rate", "open_alerts"):
            assert key in s

    def test_total_agents_correct(self):
        m = mini_mon()
        assert m.global_summary()["total_agents"] == 5

    def test_global_error_rate_zero_when_no_tasks(self):
        m = mini_mon()
        assert m.global_summary()["global_error_rate"] == 0.0


# ── reset ─────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_agents(self):
        m = mon()
        m.reset()
        assert len(m._agents) == 0

    def test_reset_clears_alerts(self):
        m = mini_mon()
        for _ in range(5):
            m.record_task("1.1", success=False)
        m.reset()
        assert m.get_alerts() == []

    def test_reset_allows_reinit(self):
        m = mon()
        m.reset()
        m.initialize_agents(["1.1"])
        assert "1.1" in m._agents


# ── heartbeat / set_queued ────────────────────────────────────────────────────

class TestHeartbeatAndQueue:
    def test_heartbeat_updates_timestamp(self):
        m = mini_mon()
        before = time.time()
        m.heartbeat("1.1")
        assert m._agents["1.1"].last_heartbeat >= before

    def test_heartbeat_unknown_agent_noop(self):
        m = mini_mon()
        m.heartbeat("9.9")  # should not raise

    def test_set_queued(self):
        m = mini_mon()
        m.set_queued("1.1", 7)
        assert m._agents["1.1"].tasks_queued == 7
