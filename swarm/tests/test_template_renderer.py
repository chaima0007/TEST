"""
Tests for intelligence/template_renderer.py
"""

import pytest
from intelligence.template_renderer import (
    TemplateRenderer, Template, SubjectVariant, RenderedMessage, TemplateStats,
    _BUILTIN_TEMPLATES,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def renderer() -> TemplateRenderer:
    return TemplateRenderer()


BASE_VARS = {
    "contact_name": "M. Dupont",
    "company_name": "Plomberie Martin",
    "sector": "artisan",
    "pagespeed": "28",
    "revenue_loss": "320",
    "agent_name": "Sophie",
}


# ── Built-in template catalogue ───────────────────────────────────────────────

class TestBuiltinCatalogue:
    def test_at_least_11_builtin_templates(self):
        assert len(_BUILTIN_TEMPLATES) >= 11

    def test_intro_value_exists(self):
        assert any(t.template_id == "intro_value" for t in _BUILTIN_TEMPLATES)

    def test_breakup_exists(self):
        assert any(t.template_id == "breakup" for t in _BUILTIN_TEMPLATES)

    def test_all_templates_have_subject_variants(self):
        for t in _BUILTIN_TEMPLATES:
            assert len(t.subject_variants) >= 1, f"{t.template_id} has no subject variants"

    def test_all_templates_have_body(self):
        for t in _BUILTIN_TEMPLATES:
            assert len(t.body_text) > 10, f"{t.template_id} body_text too short"

    def test_all_templates_have_html(self):
        for t in _BUILTIN_TEMPLATES:
            assert len(t.body_html) > 10, f"{t.template_id} body_html too short"

    def test_all_templates_have_tags(self):
        for t in _BUILTIN_TEMPLATES:
            assert len(t.tags) >= 1, f"{t.template_id} has no tags"

    def test_template_required_variables(self):
        intro = next(t for t in _BUILTIN_TEMPLATES if t.template_id == "intro_value")
        assert "company_name" in intro.required_variables
        assert "contact_name" in intro.required_variables

    def test_template_to_dict_has_keys(self):
        t = _BUILTIN_TEMPLATES[0]
        d = t.to_dict()
        for key in ("template_id", "name", "channel", "tags",
                    "subject_variants", "required_variables"):
            assert key in d

    def test_subject_variant_to_dict(self):
        sv = SubjectVariant("A", "Test subject")
        d = sv.to_dict()
        assert d["variant_key"] == "A"
        assert d["subject"] == "Test subject"

    def test_get_subject_default_variant(self):
        intro = next(t for t in _BUILTIN_TEMPLATES if t.template_id == "intro_value")
        subject = intro.get_subject("A")
        assert len(subject) > 0

    def test_get_subject_missing_variant_falls_back(self):
        intro = next(t for t in _BUILTIN_TEMPLATES if t.template_id == "intro_value")
        subject = intro.get_subject("Z")  # non-existent
        assert len(subject) > 0  # falls back to first variant


# ── Registry ──────────────────────────────────────────────────────────────────

class TestRegistry:
    def test_get_existing_template(self):
        r = renderer()
        tmpl = r.get("intro_value")
        assert tmpl is not None
        assert tmpl.template_id == "intro_value"

    def test_get_unknown_template_none(self):
        assert renderer().get("nonexistent") is None

    def test_list_templates_returns_all(self):
        r = renderer()
        templates = r.list_templates()
        assert len(templates) >= len(_BUILTIN_TEMPLATES)

    def test_list_templates_by_tag(self):
        r = renderer()
        cold = r.list_templates(tag="cold")
        assert len(cold) >= 1
        assert all("cold" in t.tags for t in cold)

    def test_register_custom_template(self):
        r = renderer()
        custom = Template(
            template_id="my_custom",
            name="Custom",
            channel="email",
            body_text="Hello {name}",
            body_html="<p>Hello {name}</p>",
            subject_variants=[SubjectVariant("A", "Hi {name}")],
            tags=["custom"],
        )
        r.register(custom)
        assert r.get("my_custom") is custom

    def test_register_overrides_existing(self):
        r = renderer()
        custom = Template(
            template_id="intro_value",
            name="Override",
            channel="email",
            body_text="Overridden",
            body_html="<p>Overridden</p>",
            subject_variants=[SubjectVariant("A", "Overridden")],
            tags=["cold"],
        )
        r.register(custom)
        assert r.get("intro_value").name == "Override"


# ── Rendering ─────────────────────────────────────────────────────────────────

class TestRendering:
    def test_render_returns_rendered_message(self):
        r = renderer()
        msg = r.render("intro_value", variables=BASE_VARS)
        assert isinstance(msg, RenderedMessage)

    def test_render_substitutes_variables(self):
        r = renderer()
        msg = r.render("intro_value", variables=BASE_VARS)
        assert "Plomberie Martin" in msg.body_text
        assert "M. Dupont" in msg.body_text
        assert "Sophie" in msg.body_text

    def test_render_subject_variant_a(self):
        r = renderer()
        msg = r.render("intro_value", variables=BASE_VARS, variant_key="A")
        assert "Plomberie Martin" in msg.subject

    def test_render_subject_variant_b(self):
        r = renderer()
        msg = r.render("intro_value", variables=BASE_VARS, variant_key="B")
        assert "Plomberie Martin" in msg.subject

    def test_render_html_substituted(self):
        r = renderer()
        msg = r.render("intro_value", variables=BASE_VARS)
        assert "Plomberie Martin" in msg.body_html

    def test_render_channel_set(self):
        r = renderer()
        msg = r.render("intro_value", variables=BASE_VARS)
        assert msg.channel == "email"

    def test_render_unknown_template_raises(self):
        with pytest.raises(KeyError):
            renderer().render("nonexistent")

    def test_render_missing_vars_listed(self):
        r = renderer()
        msg = r.render("intro_value", variables={})  # no variables at all
        assert "company_name" in msg.missing_vars
        assert not msg.is_complete

    def test_render_all_vars_present_is_complete(self):
        r = renderer()
        msg = r.render("intro_value", variables=BASE_VARS)
        assert msg.is_complete

    def test_render_strict_missing_raises(self):
        r = renderer()
        with pytest.raises(ValueError):
            r.render("intro_value", variables={}, strict=True)

    def test_render_strict_complete_does_not_raise(self):
        r = renderer()
        msg = r.render("intro_value", variables=BASE_VARS, strict=True)
        assert msg.is_complete

    def test_render_leaves_unknown_placeholder_in_place(self):
        r = renderer()
        msg = r.render("intro_value", variables={"contact_name": "Bob"})
        assert "{company_name}" in msg.body_text

    def test_render_increments_stats(self):
        r = renderer()
        r.render("intro_value", variables=BASE_VARS)
        r.render("intro_value", variables=BASE_VARS)
        assert r.get_stats("intro_value").renders == 2

    def test_rendered_message_to_dict(self):
        r = renderer()
        msg = r.render("intro_value", variables=BASE_VARS)
        d = msg.to_dict()
        for key in ("template_id", "variant_key", "subject", "body_text",
                    "body_html", "channel", "is_complete", "missing_vars"):
            assert key in d

    def test_breakup_render(self):
        r = renderer()
        msg = r.render("breakup", variables={
            "contact_name": "M. Martin",
            "agent_name": "Sophie",
        })
        assert msg.is_complete

    def test_post_quote_render(self):
        r = renderer()
        msg = r.render("quote_reminder", variables={
            "contact_name": "M. Dupont",
            "company_name": "Garage Dupont",
            "quote_total": "1199",
            "agent_name": "Sophie",
        })
        assert msg.is_complete
        assert "1199" in msg.body_text


# ── Stats ─────────────────────────────────────────────────────────────────────

class TestStats:
    def test_record_send(self):
        r = renderer()
        r.record_send("intro_value")
        assert r.get_stats("intro_value").sends == 1

    def test_record_open(self):
        r = renderer()
        r.record_send("intro_value")
        r.record_open("intro_value")
        assert r.get_stats("intro_value").opens == 1

    def test_record_click(self):
        r = renderer()
        r.record_send("intro_value")
        r.record_click("intro_value")
        assert r.get_stats("intro_value").clicks == 1

    def test_record_reply(self):
        r = renderer()
        r.record_send("intro_value")
        r.record_reply("intro_value")
        assert r.get_stats("intro_value").replies == 1

    def test_open_rate_calculation(self):
        r = renderer()
        r.record_send("intro_value")
        r.record_send("intro_value")
        r.record_open("intro_value")
        stats = r.get_stats("intro_value")
        assert stats.open_rate == pytest.approx(0.5)

    def test_click_rate_zero_sends(self):
        r = renderer()
        stats = r.get_stats("intro_value")
        assert stats.click_rate == 0.0

    def test_stats_to_dict_has_keys(self):
        r = renderer()
        r.record_send("intro_value")
        r.record_open("intro_value")
        d = r.get_stats("intro_value").to_dict()
        for key in ("template_id", "renders", "sends", "opens",
                    "clicks", "replies", "open_rate_pct", "click_rate_pct"):
            assert key in d

    def test_top_by_open_rate(self):
        r = renderer()
        r.render("intro_value", variables=BASE_VARS)
        r.record_send("intro_value")
        r.record_open("intro_value")
        r.record_send("breakup")
        top = r.top_by_open_rate(n=2)
        assert top[0].template_id == "intro_value"

    def test_all_stats_empty_initially(self):
        assert renderer().all_stats() == []

    def test_all_stats_after_render(self):
        r = renderer()
        r.render("intro_value", variables=BASE_VARS)
        r.render("breakup", variables={"contact_name": "x", "agent_name": "y"})
        assert len(r.all_stats()) == 2


# ── Summary ───────────────────────────────────────────────────────────────────

class TestSummary:
    def test_empty_summary(self):
        s = renderer().summary()
        assert s["total_renders"] == 0
        assert s["open_rate_pct"] == 0.0

    def test_summary_counts(self):
        r = renderer()
        r.render("intro_value", variables=BASE_VARS)
        r.render("intro_value", variables=BASE_VARS)
        r.record_send("intro_value")
        r.record_open("intro_value")
        s = r.summary()
        assert s["total_renders"] == 2
        assert s["total_sends"] == 1
        assert s["total_opens"] == 1

    def test_summary_has_keys(self):
        s = renderer().summary()
        for key in ("templates_count", "total_renders", "total_sends",
                    "total_opens", "total_clicks", "open_rate_pct", "click_rate_pct"):
            assert key in s

    def test_templates_count_in_summary(self):
        assert renderer().summary()["templates_count"] == len(_BUILTIN_TEMPLATES)


# ── Reset ─────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_stats_clears_counters(self):
        r = renderer()
        r.render("intro_value", variables=BASE_VARS)
        r.reset_stats()
        assert r.all_stats() == []

    def test_reset_stats_preserves_templates(self):
        r = renderer()
        r.reset_stats()
        assert r.get("intro_value") is not None

    def test_full_reset_restores_defaults(self):
        r = renderer()
        r.register(Template(
            template_id="custom", name="C", channel="email",
            body_text="x", body_html="x",
            subject_variants=[SubjectVariant("A", "x")], tags=["x"],
        ))
        r.reset()
        assert r.get("custom") is None
        assert r.get("intro_value") is not None

    def test_full_reset_clears_stats(self):
        r = renderer()
        r.render("intro_value", variables=BASE_VARS)
        r.reset()
        assert r.all_stats() == []
