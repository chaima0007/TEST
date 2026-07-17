"""
Tests for exporters/cv_exporter.py
"""

import json
import os
import pytest
import tempfile
from exporters.cv_exporter import CVExporter, CVProfile, CVEntry, CVSkillGroup


# ── Fixtures ──────────────────────────────────────────────────────────────────

def make_profile() -> CVProfile:
    return CVProfile(
        name="Jane Dupont",
        title="Architecte IA & Automatisation",
        summary="Experte en systèmes multi-agents et automatisation commerciale.",
        email="jane@example.com",
        linkedin="https://linkedin.com/in/janedupont",
        github="https://github.com/janedupont",
        location="Paris, France",
        languages=["Français (natif)", "Anglais (C1)", "Espagnol (B1)"],
        stack=["Python", "TypeScript", "React", "FastAPI", "CrewAI", "LangGraph"],
    )


def make_entries() -> list[CVEntry]:
    return [
        CVEntry(
            role="Architecte IA",
            company="CompeteIQ",
            period="2026 — Présent",
            summary="Développement du swarm de 50 agents autonomes.",
            bullets=[
                "Conçu une architecture Swarm Intelligence avec 60 agents.",
                "Pipeline automatisé : détection → outreach → négociation → paiement.",
            ],
            tags=["IA", "Swarm", "Python"],
            metrics="+28% leads, 5 clients, 4 920€/mois",
        ),
        CVEntry(
            role="Développeuse Full-Stack",
            company="Agence Web XYZ",
            period="2024 — 2026",
            summary="Développement d'applications web React/Node.js.",
            bullets=["Développé 12 applications SaaS.", "Réduit le temps de chargement de 60%."],
            tags=["React", "Node.js", "PostgreSQL"],
        ),
    ]


def make_skills() -> list[CVSkillGroup]:
    return [
        CVSkillGroup("IA & Automatisation", ["Claude API", "CrewAI", "LangGraph", "Prompt Engineering"]),
        CVSkillGroup("Backend", ["Python", "FastAPI", "asyncio", "Celery", "Redis"]),
    ]


def make_exporter() -> CVExporter:
    return CVExporter(make_profile(), make_entries(), make_skills())


# ── JSON export ───────────────────────────────────────────────────────────────

class TestExportJSON:
    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_json(tmp)
            assert os.path.exists(path)

    def test_file_extension_is_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_json(tmp)
            assert path.endswith(".json")

    def test_json_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_json(tmp)
            with open(path) as f:
                data = json.load(f)
            assert data  # non-empty

    def test_json_has_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_json(tmp)
            with open(path) as f:
                data = json.load(f)
            assert "profile" in data
            assert data["profile"]["name"] == "Jane Dupont"

    def test_json_has_experience(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_json(tmp)
            with open(path) as f:
                data = json.load(f)
            assert "experience" in data
            assert len(data["experience"]) == 2

    def test_json_has_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_json(tmp)
            with open(path) as f:
                data = json.load(f)
            assert "skills" in data
            assert len(data["skills"]) == 2

    def test_json_has_exported_at(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_json(tmp)
            with open(path) as f:
                data = json.load(f)
            assert "exported_at" in data

    def test_creates_output_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            nested = os.path.join(tmp, "sub", "dir")
            path = make_exporter().export_json(nested)
            assert os.path.exists(path)


# ── TXT export ────────────────────────────────────────────────────────────────

class TestExportTXT:
    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_txt(tmp)
            assert os.path.exists(path)

    def test_file_is_utf8_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_txt(tmp)
            with open(path, encoding="utf-8") as f:
                content = f.read()
            assert isinstance(content, str)
            assert len(content) > 100

    def test_contains_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_txt(tmp)
            content = open(path, encoding="utf-8").read()
            assert "JANE DUPONT" in content

    def test_contains_role(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_txt(tmp)
            content = open(path, encoding="utf-8").read()
            assert "Architecte IA" in content

    def test_contains_email(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_txt(tmp)
            content = open(path, encoding="utf-8").read()
            assert "jane@example.com" in content

    def test_contains_stack(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_txt(tmp)
            content = open(path, encoding="utf-8").read()
            assert "Python" in content

    def test_contains_bullets(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_txt(tmp)
            content = open(path, encoding="utf-8").read()
            assert "•" in content

    def test_contains_metrics(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_txt(tmp)
            content = open(path, encoding="utf-8").read()
            assert "4 920€" in content

    def test_contains_languages(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_txt(tmp)
            content = open(path, encoding="utf-8").read()
            assert "Français" in content


# ── HTML export ───────────────────────────────────────────────────────────────

class TestExportHTML:
    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_html(tmp)
            assert os.path.exists(path)

    def test_file_extension_is_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_html(tmp)
            assert path.endswith(".html")

    def test_is_valid_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_html(tmp)
            content = open(path, encoding="utf-8").read()
            assert "<!DOCTYPE html>" in content
            assert "<html" in content
            assert "</html>" in content

    def test_contains_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_html(tmp)
            content = open(path, encoding="utf-8").read()
            assert "Jane Dupont" in content

    def test_contains_linkedin_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_html(tmp)
            content = open(path, encoding="utf-8").read()
            assert "linkedin.com" in content

    def test_contains_skill_chips(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_html(tmp)
            content = open(path, encoding="utf-8").read()
            assert "skill-chip" in content

    def test_has_print_media_query(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = make_exporter().export_html(tmp)
            content = open(path, encoding="utf-8").read()
            assert "@media print" in content


# ── export_all ────────────────────────────────────────────────────────────────

class TestExportAll:
    def test_returns_three_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = make_exporter().export_all(tmp)
            assert set(result.keys()) == {"json", "txt", "html"}

    def test_all_files_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = make_exporter().export_all(tmp)
            for path in result.values():
                assert os.path.exists(path), f"Missing: {path}"


# ── Edge cases ────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_no_skills(self):
        exporter = CVExporter(make_profile(), make_entries(), skill_groups=[])
        with tempfile.TemporaryDirectory() as tmp:
            path = exporter.export_txt(tmp)
            assert os.path.exists(path)

    def test_no_languages(self):
        profile = make_profile()
        profile.languages = []
        exporter = CVExporter(profile, make_entries())
        with tempfile.TemporaryDirectory() as tmp:
            path = exporter.export_txt(tmp)
            content = open(path, encoding="utf-8").read()
            assert "LANGUES" not in content

    def test_empty_entries(self):
        exporter = CVExporter(make_profile(), [])
        with tempfile.TemporaryDirectory() as tmp:
            path = exporter.export_json(tmp)
            with open(path) as f:
                data = json.load(f)
            assert data["experience"] == []
