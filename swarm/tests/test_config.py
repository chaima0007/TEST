"""
Unit tests for swarm/config.py — validates all 60 agent configurations.

Run: pytest swarm/tests/test_config.py -v
"""

import pytest
from config import ALL_AGENTS, DIVISION_METADATA, DIVISION_1, DIVISION_2, DIVISION_3, DIVISION_4, DIVISION_5, DIVISION_6


class TestAgentCount:
    def test_total_agent_count(self):
        assert len(ALL_AGENTS) >= 60, f"Expected at least 60 agents, got {len(ALL_AGENTS)}"

    def test_exactly_6_divisions_in_metadata(self):
        assert len(DIVISION_METADATA) == 6

    def test_each_division_has_10_agents(self):
        for div_list, name in [
            (DIVISION_1, "Division 1"),
            (DIVISION_2, "Division 2"),
            (DIVISION_3, "Division 3"),
            (DIVISION_4, "Division 4"),
            (DIVISION_5, "Division 5"),
            (DIVISION_6, "Division 6"),
        ]:
            assert len(div_list) == 10, f"{name} should have exactly 10 agents, got {len(div_list)}"


class TestAgentConfig:
    def test_all_agents_have_unique_ids(self):
        ids = [a.id for a in ALL_AGENTS]
        assert len(ids) == len(set(ids)), "Duplicate agent IDs found"

    def test_all_agents_have_non_empty_role(self):
        for agent in ALL_AGENTS:
            assert agent.role and agent.role.strip(), f"Agent {agent.id} has empty role"

    def test_all_agents_have_non_empty_goal(self):
        for agent in ALL_AGENTS:
            assert agent.goal and agent.goal.strip(), f"Agent {agent.id} has empty goal"

    def test_all_agents_have_non_empty_backstory(self):
        for agent in ALL_AGENTS:
            assert agent.backstory and agent.backstory.strip(), f"Agent {agent.id} has empty backstory"

    def test_each_division_has_exactly_one_manager(self):
        for div_num in range(1, 7):
            managers = [a for a in ALL_AGENTS if a.division == div_num and a.is_manager]
            assert len(managers) == 1, f"Division {div_num} should have exactly 1 manager"

    def test_manager_ids_end_in_zero(self):
        managers = [a for a in ALL_AGENTS if a.is_manager]
        for m in managers:
            assert m.id.endswith(".0"), f"Manager {m.id} should end in .0"

    def test_agent_division_matches_list(self):
        for i, agent in enumerate(DIVISION_6):
            assert agent.division == 6, f"Division 6 agent {agent.id} has wrong division {agent.division}"

    def test_all_agents_have_at_least_one_tool(self):
        for agent in ALL_AGENTS:
            assert isinstance(agent.tools, list) and len(agent.tools) >= 1, \
                f"Agent {agent.id} has no tools"


class TestDivisionMetadata:
    def test_all_divisions_have_required_keys(self):
        required = {"name", "color", "emoji", "description"}
        for div_id, meta in DIVISION_METADATA.items():
            missing = required - set(meta.keys())
            assert not missing, f"Division {div_id} metadata missing: {missing}"

    def test_division_colors_are_hex(self):
        for div_id, meta in DIVISION_METADATA.items():
            color = meta.get("color", "")
            assert color.startswith("#") and len(color) in (4, 7), \
                f"Division {div_id} has invalid color: {color}"
