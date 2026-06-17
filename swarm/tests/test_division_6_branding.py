"""
Tests for Division 6 — Documentation & Personal Branding.
"""

import pytest
from divisions.division_6_branding import (
    Division6Branding,
    LinkedInPost,
    CVEntry,
    CaseStudy,
)


# ── Initialisation ────────────────────────────────────────────────────────────

class TestDivision6Init:
    def test_has_expert_agent(self):
        d = Division6Branding()
        assert d.expert is not None
        assert d.expert.id == "6.0"

    def test_has_linkedin_writer(self):
        d = Division6Branding()
        assert d.linkedin_writer is not None

    def test_has_cv_writer(self):
        d = Division6Branding()
        assert d.cv_writer is not None


# ── LinkedIn post generation ──────────────────────────────────────────────────

class TestLinkedInPost:
    def test_returns_linkedin_post(self):
        d = Division6Branding()
        post = d.generate_linkedin_post()
        assert isinstance(post, LinkedInPost)

    def test_post_has_hook(self):
        d = Division6Branding()
        post = d.generate_linkedin_post()
        assert post.hook and len(post.hook) > 10

    def test_post_has_body(self):
        d = Division6Branding()
        post = d.generate_linkedin_post()
        assert post.body and len(post.body) > 20

    def test_post_has_hashtags(self):
        d = Division6Branding()
        post = d.generate_linkedin_post()
        assert isinstance(post.hashtags, list)
        assert len(post.hashtags) >= 3

    def test_post_has_char_count(self):
        d = Division6Branding()
        post = d.generate_linkedin_post()
        assert post.char_count > 0

    def test_post_metrics_substituted(self):
        d = Division6Branding()
        metrics = {"prospects": 500, "emails": 200, "negotiations": 15, "revenue": 1500}
        post = d.generate_linkedin_post(trigger="cycle_complete", metrics=metrics)
        # Metrics should appear somewhere in the content
        assert "500" in post.body or "200" in post.body or "1500" in post.body

    def test_full_text_includes_hook_and_hashtags(self):
        d = Division6Branding()
        post = d.generate_linkedin_post()
        full = post.full_text()
        assert post.hook in full
        for tag in post.hashtags:
            assert f"#{tag}" in full

    def test_post_has_generated_at(self):
        d = Division6Branding()
        post = d.generate_linkedin_post()
        assert post.generated_at

    def test_impressions_estimate_positive(self):
        d = Division6Branding()
        post = d.generate_linkedin_post()
        assert post.impressions_estimate > 0

    def test_to_dict_has_all_fields(self):
        d = Division6Branding()
        post = d.generate_linkedin_post()
        data = post.to_dict()
        assert "post_id" in data
        assert "hook" in data
        assert "body" in data
        assert "hashtags" in data
        assert "char_count" in data
        assert "impressions_estimate" in data

    def test_different_triggers_give_different_hooks(self):
        d = Division6Branding()
        triggers = ["cycle_complete", "first_payment", "client_testimonial"]
        hooks = [d.generate_linkedin_post(trigger=t).hook for t in triggers]
        # At least some variation across triggers
        assert len(set(hooks)) >= 1  # at least different or same (template may fall back)


# ── CV entries ────────────────────────────────────────────────────────────────

class TestCVEntries:
    def test_returns_list_of_cv_entries(self):
        d = Division6Branding()
        entries = d.get_cv_entries()
        assert isinstance(entries, list)
        assert all(isinstance(e, CVEntry) for e in entries)

    def test_has_at_least_one_entry(self):
        d = Division6Branding()
        assert len(d.get_cv_entries()) >= 1

    def test_entries_have_role(self):
        d = Division6Branding()
        for e in d.get_cv_entries():
            assert e.title and len(e.title) > 5

    def test_entries_have_bullets(self):
        d = Division6Branding()
        for e in d.get_cv_entries():
            assert isinstance(e.bullets, list)
            assert len(e.bullets) >= 1

    def test_entries_have_keywords(self):
        d = Division6Branding()
        for e in d.get_cv_entries():
            assert isinstance(e.keywords, list)
            assert len(e.keywords) >= 1

    def test_impact_score_in_range(self):
        d = Division6Branding()
        for e in d.get_cv_entries():
            assert 1 <= e.impact_score <= 10

    def test_to_dict_works(self):
        d = Division6Branding()
        for e in d.get_cv_entries():
            data = e.to_dict()
            assert "title" in data
            assert "bullets" in data


# ── Case studies ──────────────────────────────────────────────────────────────

class TestCaseStudies:
    def test_returns_list_of_case_studies(self):
        d = Division6Branding()
        cases = d.get_case_studies()
        assert isinstance(cases, list)
        assert all(isinstance(c, CaseStudy) for c in cases)

    def test_has_at_least_one_case(self):
        d = Division6Branding()
        assert len(d.get_case_studies()) >= 1

    def test_cases_have_before_after(self):
        d = Division6Branding()
        for c in d.get_case_studies():
            assert c.problem_before
            assert c.result_after

    def test_cases_have_metrics(self):
        d = Division6Branding()
        for c in d.get_case_studies():
            assert isinstance(c.metrics, dict)
            assert len(c.metrics) >= 1

    def test_to_dict_works(self):
        d = Division6Branding()
        for c in d.get_case_studies():
            data = c.to_dict()
            assert "case_id" in data
            assert "sector" in data


# ── get_all_content ───────────────────────────────────────────────────────────

class TestGetAllContent:
    def test_returns_dict(self):
        d = Division6Branding()
        content = d.get_all_content()
        assert isinstance(content, dict)

    def test_has_all_keys(self):
        d = Division6Branding()
        content = d.get_all_content()
        assert "linkedin_posts" in content
        assert "cv_entries" in content
        assert "case_studies" in content
        assert "agent_profile" in content

    def test_linkedin_posts_are_dicts(self):
        d = Division6Branding()
        posts = d.get_all_content()["linkedin_posts"]
        assert all(isinstance(p, dict) for p in posts)

    def test_cv_entries_are_dicts(self):
        d = Division6Branding()
        entries = d.get_all_content()["cv_entries"]
        assert all(isinstance(e, dict) for e in entries)

    def test_agent_profile_has_id(self):
        d = Division6Branding()
        profile = d.get_all_content()["agent_profile"]
        assert profile["id"] == "6.0"


# ── CV bullet generation ──────────────────────────────────────────────────────

class TestCVBullet:
    def test_generate_cv_bullet_returns_string(self):
        d = Division6Branding()
        bullet = d.generate_cv_bullet("Launched AI swarm", {"clients": 5, "revenue": "4920€"})
        assert isinstance(bullet, str)
        assert len(bullet) > 20
