"""
Unit tests for Division 1 Detection.

Run: pytest swarm/tests/test_division_1_detection.py -v
"""

import asyncio
import pytest
from divisions.division_1_detection import Division1Detection, ProspectFiche


@pytest.fixture
def div1():
    return Division1Detection()


class TestProspectFiche:
    def test_fiche_has_required_fields(self):
        fiche = ProspectFiche(
            company_id="test_001",
            name="Test SARL",
            sector="Artisans",
            website="test.fr",
            pagespeed_score=25,
            mobile_responsive=False,
            load_time_ms=6500,
            contact_email="contact@test.fr",
            agent_source="1.1",
            detected_issues=["Pas de mobile", "Lenteur"],
        )
        assert fiche.company_id == "test_001"
        assert fiche.pagespeed_score == 25
        assert len(fiche.detected_issues) == 2

    def test_fiche_with_minimal_data(self):
        fiche = ProspectFiche(
            company_id="test_002",
            name="Minimal",
            sector="Médical",
            website="minimal.fr",
            pagespeed_score=0,
            mobile_responsive=False,
            load_time_ms=0,
            contact_email=None,
            agent_source="1.3",
            detected_issues=[],
        )
        assert fiche.contact_email is None
        assert fiche.detected_issues == []


class TestDivision1Run:
    def test_run_returns_list(self, div1):
        fiches = asyncio.get_event_loop().run_until_complete(div1.run())
        assert isinstance(fiches, list)

    def test_run_returns_prospect_fiches(self, div1):
        fiches = asyncio.get_event_loop().run_until_complete(div1.run())
        for f in fiches:
            assert isinstance(f, ProspectFiche)

    def test_fiches_sorted_by_pagespeed_ascending(self, div1):
        fiches = asyncio.get_event_loop().run_until_complete(div1.run())
        if len(fiches) >= 2:
            scores = [f.pagespeed_score for f in fiches]
            assert scores == sorted(scores), "Fiches should be sorted by PageSpeed score ascending"

    def test_no_duplicate_websites(self, div1):
        fiches = asyncio.get_event_loop().run_until_complete(div1.run())
        websites = [f.website for f in fiches]
        assert len(websites) == len(set(websites)), "Duplicate websites found"

    def test_run_covers_multiple_sectors(self, div1):
        fiches = asyncio.get_event_loop().run_until_complete(div1.run())
        sectors = {f.sector for f in fiches}
        assert len(sectors) >= 2, "Should detect prospects across multiple sectors"
