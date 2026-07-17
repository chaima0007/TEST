"""
CV Exporter — generates professional CV documents from structured entries.

Supports three output formats:
  - JSON  : machine-readable for ATS/job portals
  - TXT   : human-readable plain text for email attachment
  - HTML  : styled document (can be printed/printed to PDF via browser)

Usage:
    from exporters.cv_exporter import CVExporter, CVEntry, CVProfile
    profile = CVProfile(name="Jane Doe", title="Développeuse Web", ...)
    exporter = CVExporter(profile, entries)
    path = exporter.export_txt(output_dir="./exports")
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional

# ── Data models ───────────────────────────────────────────────────────────────


@dataclass
class CVProfile:
    name: str
    title: str
    summary: str
    email: str = ""
    linkedin: str = ""
    github: str = ""
    location: str = ""
    languages: List[str] = field(default_factory=list)
    stack: List[str] = field(default_factory=list)


@dataclass
class CVEntry:
    role: str
    company: str
    period: str
    summary: str
    bullets: List[str] = field(default_factory=list)  # STAR-format achievements
    tags: List[str] = field(default_factory=list)
    metrics: Optional[str] = None  # e.g. "+28% leads, 5 clients, 4 920€"


@dataclass
class CVSkillGroup:
    category: str
    skills: List[str]


# ── Exporter ──────────────────────────────────────────────────────────────────


class CVExporter:
    """
    Builds professional CV output from a CVProfile + list of CVEntry objects.
    Each export method writes a file and returns its path.
    """

    def __init__(
        self,
        profile: CVProfile,
        entries: List[CVEntry],
        skill_groups: Optional[List[CVSkillGroup]] = None,
    ):
        self.profile = profile
        self.entries = entries
        self.skill_groups = skill_groups or []

    # ── JSON ──────────────────────────────────────────────────────────────────

    def export_json(self, output_dir: str = "./exports") -> str:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        date_tag = datetime.now().strftime("%Y%m%d")
        path = os.path.join(output_dir, f"cv_{date_tag}.json")
        data = {
            "exported_at": datetime.now().isoformat(),
            "profile": asdict(self.profile),
            "experience": [asdict(e) for e in self.entries],
            "skills": [asdict(g) for g in self.skill_groups],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return path

    # ── Plain text ────────────────────────────────────────────────────────────

    def _txt_separator(self, char: str = "─", width: int = 72) -> str:
        return char * width

    def export_txt(self, output_dir: str = "./exports") -> str:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        date_tag = datetime.now().strftime("%Y%m%d")
        path = os.path.join(output_dir, f"cv_{date_tag}.txt")

        p = self.profile
        lines: List[str] = []

        # Header
        lines += [
            self._txt_separator("═"),
            f"  {p.name.upper()}",
            f"  {p.title}",
            self._txt_separator("═"),
        ]
        if p.location:
            lines.append(f"  📍 {p.location}")
        if p.email:
            lines.append(f"  ✉  {p.email}")
        if p.linkedin:
            lines.append(f"  🔗 {p.linkedin}")
        if p.github:
            lines.append(f"  💻 {p.github}")
        lines += ["", p.summary, ""]

        # Stack
        if p.stack:
            lines += [
                self._txt_separator(),
                "STACK TECHNIQUE",
                self._txt_separator(),
                "  " + " · ".join(p.stack),
                "",
            ]

        # Experience
        lines += [
            self._txt_separator(),
            "EXPÉRIENCE PROFESSIONNELLE",
            self._txt_separator(),
        ]
        for e in self.entries:
            lines.append(f"\n  {e.role}  —  {e.company}")
            lines.append(f"  {e.period}")
            if e.metrics:
                lines.append(f"  📈 {e.metrics}")
            lines.append(f"\n  {e.summary}")
            for bullet in e.bullets:
                lines.append(f"    • {bullet}")
            if e.tags:
                lines.append(f"    Tags : {', '.join(e.tags)}")

        # Skills
        if self.skill_groups:
            lines += [
                "",
                self._txt_separator(),
                "COMPÉTENCES",
                self._txt_separator(),
            ]
            for g in self.skill_groups:
                lines.append(f"\n  {g.category}")
                lines.append("  " + " · ".join(g.skills))

        # Languages
        if p.languages:
            lines += [
                "",
                self._txt_separator(),
                "LANGUES",
                self._txt_separator(),
                "  " + " · ".join(p.languages),
            ]

        lines += ["", self._txt_separator("═"), ""]
        content = "\n".join(lines)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    # ── HTML ─────────────────────────────────────────────────────────────────

    _HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>{name} — CV</title>
<style>
  body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 800px; margin: 40px auto;
          color: #1a1a2e; line-height: 1.6; padding: 0 20px; }}
  h1 {{ color: #4f46e5; margin-bottom: 4px; }}
  h2 {{ color: #4f46e5; border-bottom: 2px solid #e0e0f0; padding-bottom: 4px; margin-top: 28px; }}
  .subtitle {{ color: #6b7280; font-size: 1.1em; margin-bottom: 8px; }}
  .meta {{ display: flex; gap: 20px; flex-wrap: wrap; color: #6b7280; font-size: 0.9em; margin-bottom: 12px; }}
  .summary {{ background: #f5f3ff; border-left: 4px solid #4f46e5; padding: 12px 16px;
              border-radius: 4px; margin-bottom: 8px; }}
  .entry {{ margin-bottom: 20px; border-bottom: 1px solid #e0e0f0; padding-bottom: 16px; }}
  .entry h3 {{ margin: 0 0 2px; color: #1a1a2e; }}
  .entry .period {{ color: #9ca3af; font-size: 0.88em; }}
  .metrics {{ display: inline-block; background: #ecfdf5; color: #065f46;
               font-size: 0.85em; padding: 2px 10px; border-radius: 12px; margin: 4px 0; }}
  ul {{ margin: 8px 0; padding-left: 20px; }}
  .tags {{ margin-top: 6px; }}
  .tag {{ display: inline-block; background: #ede9fe; color: #5b21b6; font-size: 0.78em;
           padding: 1px 8px; border-radius: 10px; margin-right: 4px; }}
  .stack {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 8px 0; }}
  .skill-chip {{ background: #f3f4f6; border: 1px solid #e5e7eb; border-radius: 6px;
                  padding: 3px 10px; font-size: 0.85em; }}
  @media print {{ body {{ margin: 0; }} h2 {{ page-break-after: avoid; }} .entry {{ page-break-inside: avoid; }} }}
</style>
</head>
<body>
<h1>{name}</h1>
<p class="subtitle">{title}</p>
<div class="meta">{meta_items}</div>
<div class="summary">{summary}</div>

{stack_section}

<h2>Expérience Professionnelle</h2>
{entries_html}

{skills_html}

{languages_html}

<p style="color:#9ca3af;font-size:0.78em;margin-top:32px">
  Généré le {date} — CompeteIQ Swarm Intelligence
</p>
</body>
</html>"""

    def export_html(self, output_dir: str = "./exports") -> str:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        date_tag = datetime.now().strftime("%Y%m%d")
        path = os.path.join(output_dir, f"cv_{date_tag}.html")

        p = self.profile
        meta_parts = []
        if p.location:
            meta_parts.append(f"📍 {p.location}")
        if p.email:
            meta_parts.append(f'<a href="mailto:{p.email}">{p.email}</a>')
        if p.linkedin:
            meta_parts.append(f'<a href="{p.linkedin}">LinkedIn</a>')
        if p.github:
            meta_parts.append(f'<a href="{p.github}">GitHub</a>')

        stack_section = ""
        if p.stack:
            chips = "".join(f'<span class="skill-chip">{s}</span>' for s in p.stack)
            stack_section = f"<h2>Stack Technique</h2><div class='stack'>{chips}</div>"

        entries_html = ""
        for e in self.entries:
            bullets_html = "".join(f"<li>{b}</li>" for b in e.bullets)
            metrics_html = f'<span class="metrics">📈 {e.metrics}</span>' if e.metrics else ""
            tags_html = (
                '<div class="tags">' + "".join(f'<span class="tag">{t}</span>' for t in e.tags) + "</div>"
                if e.tags else ""
            )
            entries_html += f"""
<div class="entry">
  <h3>{e.role} — {e.company}</h3>
  <p class="period">{e.period}</p>
  {metrics_html}
  <p>{e.summary}</p>
  <ul>{bullets_html}</ul>
  {tags_html}
</div>"""

        skills_html = ""
        if self.skill_groups:
            rows = "".join(
                f"<p><strong>{g.category}</strong> : {', '.join(g.skills)}</p>"
                for g in self.skill_groups
            )
            skills_html = f"<h2>Compétences</h2>{rows}"

        languages_html = ""
        if p.languages:
            languages_html = f"<h2>Langues</h2><p>{' · '.join(p.languages)}</p>"

        html = self._HTML_TEMPLATE.format(
            name=p.name,
            title=p.title,
            summary=p.summary,
            meta_items=" &nbsp;|&nbsp; ".join(meta_parts),
            stack_section=stack_section,
            entries_html=entries_html,
            skills_html=skills_html,
            languages_html=languages_html,
            date=datetime.now().strftime("%d/%m/%Y"),
        )

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return path

    # ── Convenience: all formats ───────────────────────────────────────────────

    def export_all(self, output_dir: str = "./exports") -> dict[str, str]:
        """Export in all three formats. Returns {format: path}."""
        return {
            "json": self.export_json(output_dir),
            "txt":  self.export_txt(output_dir),
            "html": self.export_html(output_dir),
        }
