"""
Tests for Division 2 — Rédaction & Outreach.
"""

import pytest
from unittest.mock import patch, MagicMock
from divisions.division_2_redaction import (
    Division2Redaction,
    OutreachRecord,
    EMAIL_TEMPLATES,
    TONE_ASSIGNMENTS,
    _draft_email,
)
from divisions.division_1_detection import ProspectFiche


# ── Fixtures ──────────────────────────────────────────────────────────────────

def make_fiche(
    company_id: str = "test_001",
    name: str = "Plomberie Martin",
    sector: str = "artisan plombier",
    website: str = "http://plomberie-martin.fr",
    pagespeed_score: int = 42,
    load_time_ms: int = 3800,
) -> ProspectFiche:
    return ProspectFiche(
        company_id=company_id,
        name=name,
        sector=sector,
        website=website,
        contact_email="contact@plomberie-martin.fr",
        pagespeed_score=pagespeed_score,
        load_time_ms=load_time_ms,
        issues=["Performance mobile critique", "Score PageSpeed < 50"],
    )


# ── Division2Redaction initialisation ─────────────────────────────────────────

class TestDivision2Initialisation:
    def test_has_ab_tester(self):
        d = Division2Redaction()
        assert d.ab_tester is not None

    def test_has_nine_writers(self):
        d = Division2Redaction()
        assert len(d.writers) == 9

    def test_has_one_manager(self):
        d = Division2Redaction()
        assert d.manager is not None
        assert d.manager.is_manager is True

    def test_manager_is_2_0(self):
        d = Division2Redaction()
        assert d.manager.id == "2.0"


# ── _draft_email ──────────────────────────────────────────────────────────────

class TestDraftEmail:
    def test_factuel_template_has_pagespeed(self):
        fiche = make_fiche()
        result = _draft_email(fiche, "2.1")
        assert "42" in result  # pagespeed_score
        assert "3800" in result  # load_time_ms

    def test_unknown_agent_falls_back_to_2_2(self):
        fiche = make_fiche()
        result_unknown = _draft_email(fiche, "9.9")
        result_2_2 = _draft_email(fiche, "2.2")
        assert result_unknown == result_2_2

    def test_all_templates_include_website(self):
        fiche = make_fiche()
        for agent_id in EMAIL_TEMPLATES:
            result = _draft_email(fiche, agent_id)
            assert fiche.website in result, f"Website missing from template {agent_id}"

    def test_result_is_non_empty_string(self):
        fiche = make_fiche()
        for agent_id in EMAIL_TEMPLATES:
            result = _draft_email(fiche, agent_id)
            assert isinstance(result, str) and len(result) > 20


# ── draft_all ─────────────────────────────────────────────────────────────────

class TestDraftAll:
    def test_returns_list_of_outreach_records(self):
        d = Division2Redaction()
        fiches = [make_fiche(company_id=f"c{i}") for i in range(5)]
        records = d.draft_all(fiches)
        assert isinstance(records, list)
        assert all(isinstance(r, OutreachRecord) for r in records)

    def test_one_record_per_fiche(self):
        d = Division2Redaction()
        fiches = [make_fiche(company_id=f"c{i}") for i in range(7)]
        records = d.draft_all(fiches)
        assert len(records) == 7

    def test_records_have_company_ids(self):
        d = Division2Redaction()
        fiches = [make_fiche(company_id=f"c{i}") for i in range(3)]
        records = d.draft_all(fiches)
        ids = [r.company_id for r in records]
        assert "c0" in ids and "c1" in ids and "c2" in ids

    def test_agent_id_is_valid_division_2(self):
        d = Division2Redaction()
        fiches = [make_fiche(company_id=f"c{i}") for i in range(9)]
        records = d.draft_all(fiches)
        for r in records:
            assert r.copywriter_agent.startswith("2."), f"Unexpected agent: {r.copywriter_agent}"

    def test_ab_tester_sent_count_increments(self):
        d = Division2Redaction()
        initial_total = sum(v.sent for v in d.ab_tester.variants.values())
        fiches = [make_fiche(company_id=f"c{i}") for i in range(5)]
        d.draft_all(fiches)
        final_total = sum(v.sent for v in d.ab_tester.variants.values())
        assert final_total == initial_total + 5

    def test_sector_artisan_biases_agent_2_8(self):
        d = Division2Redaction()
        fiches = [make_fiche(company_id="art_01", sector="artisan maçon")]
        records = d.draft_all(fiches)
        assert records[0].copywriter_agent == "2.8"

    def test_sector_paris_biases_agent_2_6(self):
        d = Division2Redaction()
        fiches = [make_fiche(company_id="paris_01", sector="Paris Île-de-France")]
        records = d.draft_all(fiches)
        assert records[0].copywriter_agent == "2.6"

    def test_email_draft_is_non_empty(self):
        d = Division2Redaction()
        fiches = [make_fiche()]
        records = d.draft_all(fiches)
        assert len(records[0].email_draft) > 20

    def test_to_dict_includes_fiche(self):
        d = Division2Redaction()
        fiches = [make_fiche()]
        record = d.draft_all(fiches)[0]
        d_out = record.to_dict()
        assert "fiche" in d_out
        assert isinstance(d_out["fiche"], dict)


# ── record_reply / get_ab_report ──────────────────────────────────────────────

class TestABIntegration:
    def test_record_reply_updates_posterior(self):
        d = Division2Redaction()
        alpha_before = d.ab_tester.variants["2.1"].alpha
        d.record_reply("2.1", replied=True)
        assert d.ab_tester.variants["2.1"].alpha > alpha_before

    def test_get_ab_report_returns_dict(self):
        d = Division2Redaction()
        report = d.get_ab_report()
        assert isinstance(report, dict)
        assert "variants" in report
        assert "total_sent" in report

    def test_get_ab_report_has_nine_variants(self):
        d = Division2Redaction()
        report = d.get_ab_report()
        assert len(report["variants"]) == 9
