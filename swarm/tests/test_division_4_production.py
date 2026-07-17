"""
Tests for divisions/division_4_production.py
"""

import asyncio
import pytest
from divisions.division_4_production import (
    Division4Production,
    ProductionJob,
    Deliverable,
    JobStatus,
    ISSUE_TO_AGENTS,
    DELIVERABLE_TEMPLATES,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


def make_job(
    company_id: str = "co_001",
    company_name: str = "Plomberie Martin SARL",
    sector: str = "Artisans & Bâtiment",
    issues: list | None = None,
) -> ProductionJob:
    div4 = Division4Production()
    return div4.create_job(
        company_id=company_id,
        company_name=company_name,
        sector=sector,
        issues=issues or ["Non-responsive mobile", "PageSpeed critique"],
    )


def div4() -> Division4Production:
    return Division4Production()


# ── assign_agents ─────────────────────────────────────────────────────────────

class TestAssignAgents:
    def test_mobile_issue_assigns_4_1_4_2(self):
        agents = div4().assign_agents(["Non-responsive mobile"])
        assert "4.1" in agents
        assert "4.2" in agents

    def test_pagespeed_issue_assigns_4_7_4_9(self):
        agents = div4().assign_agents(["PageSpeed critique"])
        assert "4.7" in agents
        assert "4.9" in agents

    def test_seo_issue_assigns_seo_agents(self):
        agents = div4().assign_agents(["SEO manquant"])
        assert "4.4" in agents
        assert "4.5" in agents
        assert "4.6" in agents

    def test_ssl_issue_assigns_4_8(self):
        agents = div4().assign_agents(["SSL absent"])
        assert "4.8" in agents

    def test_wordpress_issue_assigns_4_3(self):
        agents = div4().assign_agents(["WordPress non-responsive"])
        assert "4.3" in agents

    def test_cwv_issue_assigns_4_9_4_7(self):
        agents = div4().assign_agents(["Core Web Vitals"])
        assert "4.9" in agents
        assert "4.7" in agents

    def test_multiple_issues_deduplicates(self):
        agents = div4().assign_agents(["PageSpeed critique", "Core Web Vitals"])
        assert agents == sorted(set(agents))

    def test_empty_issues_fallback_to_defaults(self):
        agents = div4().assign_agents([])
        assert set(agents) == {"4.1", "4.4", "4.7"}

    def test_unknown_issue_fallback_to_defaults(self):
        agents = div4().assign_agents(["Problème inconnu XYZ"])
        assert set(agents) == {"4.1", "4.4", "4.7"}

    def test_case_insensitive_matching(self):
        agents_lower = div4().assign_agents(["pagespeed critique"])
        agents_upper = div4().assign_agents(["PAGESPEED CRITIQUE"])
        assert set(agents_lower) == set(agents_upper)

    def test_returns_sorted_list(self):
        agents = div4().assign_agents(["Non-responsive mobile", "SEO manquant", "SSL absent"])
        assert agents == sorted(agents)

    def test_partial_issue_string_matches(self):
        agents = div4().assign_agents(["Has Non-responsive mobile issues"])
        assert "4.1" in agents


# ── create_job ────────────────────────────────────────────────────────────────

class TestCreateJob:
    def test_returns_production_job(self):
        job = make_job()
        assert isinstance(job, ProductionJob)

    def test_job_id_contains_company_id(self):
        job = make_job(company_id="test_co")
        assert "test_co" in job.job_id

    def test_initial_status_is_pending(self):
        job = make_job()
        assert job.status == JobStatus.PENDING

    def test_initial_deliverables_empty(self):
        job = make_job()
        assert job.deliverables == []

    def test_initial_assigned_agents_empty(self):
        job = make_job()
        assert job.assigned_agents == []

    def test_company_name_preserved(self):
        job = make_job(company_name="Restaurant Le Gaulois")
        assert job.company_name == "Restaurant Le Gaulois"

    def test_sector_preserved(self):
        job = make_job(sector="Restauration & Hôtellerie")
        assert job.sector == "Restauration & Hôtellerie"

    def test_issues_preserved(self):
        issues = ["SSL absent", "SEO manquant"]
        job = make_job(issues=issues)
        assert job.issues == issues

    def test_started_at_is_none_initially(self):
        job = make_job()
        assert job.started_at is None

    def test_completed_at_is_none_initially(self):
        job = make_job()
        assert job.completed_at is None

    def test_output_package_url_none_initially(self):
        job = make_job()
        assert job.output_package_url is None


# ── execute_job ───────────────────────────────────────────────────────────────

class TestExecuteJob:
    def test_job_status_success_after_execution(self):
        job = make_job()
        result = run(div4().execute_job(job))
        assert result.status == JobStatus.SUCCESS

    def test_assigned_agents_populated(self):
        job = make_job(issues=["Non-responsive mobile"])
        result = run(div4().execute_job(job))
        assert len(result.assigned_agents) >= 1
        assert "4.1" in result.assigned_agents

    def test_deliverables_generated(self):
        job = make_job(issues=["Non-responsive mobile"])
        result = run(div4().execute_job(job))
        assert len(result.deliverables) > 0

    def test_all_deliverables_are_deliverable_type(self):
        job = make_job()
        result = run(div4().execute_job(job))
        assert all(isinstance(d, Deliverable) for d in result.deliverables)

    def test_started_at_set(self):
        job = make_job()
        result = run(div4().execute_job(job))
        assert result.started_at is not None

    def test_completed_at_set(self):
        job = make_job()
        result = run(div4().execute_job(job))
        assert result.completed_at is not None

    def test_output_package_url_set(self):
        job = make_job()
        result = run(div4().execute_job(job))
        assert result.output_package_url is not None
        assert job.job_id in result.output_package_url

    def test_deliverable_has_correct_agent_id(self):
        job = make_job(issues=["SSL absent"])
        result = run(div4().execute_job(job))
        agent_ids = {d.agent_id for d in result.deliverables}
        assert "4.8" in agent_ids

    def test_deliverable_has_download_url(self):
        job = make_job()
        result = run(div4().execute_job(job))
        for d in result.deliverables:
            assert d.download_url is not None
            assert job.job_id in d.download_url

    def test_deliverable_has_positive_size_kb(self):
        job = make_job()
        result = run(div4().execute_job(job))
        for d in result.deliverables:
            assert d.size_kb > 0

    def test_multiple_issues_produce_more_deliverables(self):
        few_issues = make_job(issues=["SSL absent"])
        many_issues = make_job(issues=["Non-responsive mobile", "SEO manquant", "PageSpeed critique"])
        result_few = run(div4().execute_job(few_issues))
        result_many = run(div4().execute_job(many_issues))
        assert len(result_many.deliverables) >= len(result_few.deliverables)

    def test_seo_job_produces_seo_files(self):
        job = make_job(issues=["SEO manquant"])
        result = run(div4().execute_job(job))
        filenames = {d.filename for d in result.deliverables}
        assert "seo_balises.txt" in filenames

    def test_ssl_job_produces_nginx_config(self):
        job = make_job(issues=["SSL absent"])
        result = run(div4().execute_job(job))
        filenames = {d.filename for d in result.deliverables}
        assert "ssl_headers.nginx" in filenames

    def test_pagespeed_job_produces_optimizer_script(self):
        job = make_job(issues=["PageSpeed critique"])
        result = run(div4().execute_job(job))
        filenames = {d.filename for d in result.deliverables}
        assert "image_optimizer.sh" in filenames

    def test_wordpress_job_produces_theme_zip(self):
        job = make_job(issues=["WordPress non-responsive"])
        result = run(div4().execute_job(job))
        filenames = {d.filename for d in result.deliverables}
        assert "child_theme_fix.zip" in filenames


# ── to_dict ───────────────────────────────────────────────────────────────────

class TestToDict:
    def test_to_dict_returns_dict(self):
        job = make_job()
        run(div4().execute_job(job))
        d = job.to_dict()
        assert isinstance(d, dict)

    def test_to_dict_status_is_string(self):
        job = make_job()
        run(div4().execute_job(job))
        d = job.to_dict()
        assert isinstance(d["status"], str)
        assert d["status"] == "success"

    def test_to_dict_deliverables_are_dicts(self):
        job = make_job()
        run(div4().execute_job(job))
        d = job.to_dict()
        assert isinstance(d["deliverables"], list)
        if d["deliverables"]:
            assert isinstance(d["deliverables"][0], dict)

    def test_to_dict_contains_required_keys(self):
        job = make_job()
        d = job.to_dict()
        for key in ("job_id", "company_id", "company_name", "sector", "issues", "status"):
            assert key in d


# ── ISSUE_TO_AGENTS / DELIVERABLE_TEMPLATES coverage ─────────────────────────

class TestConstants:
    def test_issue_to_agents_all_known_agent_ids(self):
        known = {f"4.{i}" for i in range(1, 10)}
        for agents in ISSUE_TO_AGENTS.values():
            for agent in agents:
                assert agent in known

    def test_deliverable_templates_cover_all_specialists(self):
        specialists = {f"4.{i}" for i in range(1, 10)}
        for specialist in specialists:
            assert specialist in DELIVERABLE_TEMPLATES, f"No template for {specialist}"

    def test_deliverable_templates_have_required_fields(self):
        for agent_id, templates in DELIVERABLE_TEMPLATES.items():
            for t in templates:
                assert "filename" in t
                assert "content_type" in t
                assert "description" in t
