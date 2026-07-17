"use client";

import { useEffect, useState } from "react";
import type { PortfolioProject, PortfolioSkill, PortfolioStat } from "@/lib/portfolio-data";

interface PortfolioData {
  stats: PortfolioStat[];
  projects: PortfolioProject[];
  skills: PortfolioSkill[];
}

// ── Icons ──────────────────────────────────────────────────────────────────

function IconBolt({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" />
    </svg>
  );
}

function IconTag({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M17.707 9.293l-7-7A1 1 0 0010 2H4a2 2 0 00-2 2v6a1 1 0 00.293.707l7 7a1 1 0 001.414 0l7-7a1 1 0 000-1.414zM6 7a1 1 0 110-2 1 1 0 010 2z" clipRule="evenodd" />
    </svg>
  );
}

function IconChevronDown({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
    </svg>
  );
}

// ── Stat Card ─────────────────────────────────────────────────────────────────

const COLOR_MAP: Record<string, string> = {
  indigo: "bg-indigo-50 text-indigo-700 border-indigo-100",
  green: "bg-green-50 text-green-700 border-green-100",
  blue: "bg-blue-50 text-blue-700 border-blue-100",
  pink: "bg-pink-50 text-pink-700 border-pink-100",
};

function StatCard({ stat }: { stat: PortfolioStat }) {
  const cls = COLOR_MAP[stat.color] ?? "bg-slate-50 text-slate-700 border-slate-100";
  return (
    <div className={`rounded-xl border p-5 ${cls}`}>
      <p className="text-2xl font-bold tracking-tight">{stat.value}</p>
      <p className="text-sm font-medium mt-0.5">{stat.label}</p>
      {stat.delta && (
        <p className="text-xs opacity-70 mt-1">{stat.delta}</p>
      )}
    </div>
  );
}

// ── Project Card ──────────────────────────────────────────────────────────────

function scoreColor(score: number) {
  if (score >= 90) return "text-green-600";
  if (score >= 70) return "text-amber-600";
  return "text-red-600";
}

function formatMs(ms: number) {
  if (ms === 0) return "N/A";
  return ms >= 1000 ? `${(ms / 1000).toFixed(1)}s` : `${ms}ms`;
}

function ProjectCard({ project }: { project: PortfolioProject }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden hover:shadow-md transition-shadow">
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full text-left px-5 py-4 flex items-start gap-4"
      >
        {/* Score badge */}
        <div className="flex-shrink-0 w-14 h-14 rounded-xl bg-slate-50 border border-slate-100 flex flex-col items-center justify-center">
          <span className={`text-lg font-bold leading-none ${scoreColor(project.result_score)}`}>
            {project.result_score}
          </span>
          <span className="text-[9px] text-slate-400 mt-0.5">PageSpeed</span>
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className="text-sm font-semibold text-slate-900 truncate">{project.client_alias}</h3>
            <span className="text-xs bg-slate-100 text-slate-500 px-2 py-0.5 rounded-full">{project.sector}</span>
            <span className="text-xs text-slate-400">{project.city}</span>
          </div>
          <p className="text-xs text-slate-500 mt-1 line-clamp-2">{project.problem}</p>
          <div className="flex items-center gap-4 mt-2">
            <span className="text-xs text-slate-400">
              Avant: <span className="font-medium text-red-500">{formatMs(project.result_loadtime_before)}</span>
            </span>
            <span className="text-slate-300">→</span>
            <span className="text-xs text-slate-400">
              Après: <span className="font-medium text-green-600">{formatMs(project.result_loadtime_after)}</span>
            </span>
            <span className="ml-auto text-sm font-bold text-indigo-600">{project.revenue_eur}€</span>
          </div>
        </div>

        <IconChevronDown className={`w-4 h-4 text-slate-400 flex-shrink-0 mt-1 transition-transform ${open ? "rotate-180" : ""}`} />
      </button>

      {open && (
        <div className="px-5 pb-5 border-t border-slate-100 pt-4 space-y-4">
          {/* Solution */}
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1">Solution déployée</p>
            <p className="text-sm text-slate-700">{project.solution}</p>
          </div>

          {/* Deliverables */}
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">Livrables</p>
            <ul className="grid grid-cols-2 gap-1.5">
              {project.deliverables.map((d) => (
                <li key={d} className="text-xs text-slate-600 flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 flex-shrink-0" />
                  {d}
                </li>
              ))}
            </ul>
          </div>

          {/* Tags + agents */}
          <div className="flex flex-wrap gap-1.5">
            {project.tags.map((tag) => (
              <span key={tag} className="text-[11px] bg-indigo-50 text-indigo-600 px-2 py-0.5 rounded-full">
                {tag}
              </span>
            ))}
          </div>
          <div className="flex flex-wrap gap-1.5">
            {project.agent_ids.map((a) => (
              <span key={a} className="text-[11px] bg-slate-100 text-slate-500 px-2 py-0.5 rounded-full font-mono">
                Agent {a}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ── Skills Panel ──────────────────────────────────────────────────────────────

function SkillBar({ name, level }: { name: string; level: number }) {
  return (
    <div>
      <div className="flex justify-between items-center mb-1">
        <span className="text-xs text-slate-700 font-medium">{name}</span>
        <span className="text-xs text-slate-400 font-mono">{level}%</span>
      </div>
      <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-pink-500"
          style={{ width: `${level}%` }}
        />
      </div>
    </div>
  );
}

function SkillCategory({ cat }: { cat: PortfolioSkill }) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5">
      <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-4">{cat.category}</h3>
      <div className="space-y-3">
        {cat.skills.map((s) => (
          <SkillBar key={s.name} name={s.name} level={s.level} />
        ))}
      </div>
    </div>
  );
}

// ── Main Page ─────────────────────────────────────────────────────────────────

type Tab = "projects" | "skills";

export default function PortfolioPage() {
  const [data, setData] = useState<PortfolioData | null>(null);
  const [tab, setTab] = useState<Tab>("projects");
  const [filter, setFilter] = useState<string>("Tous");

  useEffect(() => {
    fetch("/api/portfolio")
      .then((r) => r.json())
      .then(setData);
  }, []);

  const sectors = data
    ? ["Tous", ...Array.from(new Set(data.projects.map((p) => p.sector)))]
    : ["Tous"];

  const filtered =
    data?.projects.filter((p) => filter === "Tous" || p.sector === filter) ?? [];

  const totalRevenue = data?.projects.reduce((s, p) => s + p.revenue_eur, 0) ?? 0;

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 px-6 py-10">
        <div className="max-w-5xl mx-auto">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-xl bg-white/20 backdrop-blur flex items-center justify-center">
              <IconBolt className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Portfolio Swarm IA</h1>
              <p className="text-sm text-white/70">Projets livrés par les 60 agents autonomes</p>
            </div>
          </div>

          {data && (
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6">
              {data.stats.map((s) => (
                <StatCard key={s.label} stat={s} />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Tabs */}
      <div className="max-w-5xl mx-auto px-6">
        <div className="flex gap-1 border-b border-slate-200 mt-6">
          {(["projects", "skills"] as Tab[]).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-4 py-2.5 text-sm font-medium border-b-2 -mb-px transition-colors ${
                tab === t
                  ? "border-indigo-600 text-indigo-600"
                  : "border-transparent text-slate-500 hover:text-slate-700"
              }`}
            >
              {t === "projects" ? `Projets (${data?.projects.length ?? 0})` : "Compétences"}
            </button>
          ))}
        </div>

        <div className="py-6">
          {tab === "projects" && (
            <>
              {/* Sector filter */}
              <div className="flex flex-wrap gap-2 mb-5">
                {sectors.map((s) => (
                  <button
                    key={s}
                    onClick={() => setFilter(s)}
                    className={`text-xs px-3 py-1.5 rounded-full border font-medium transition-colors ${
                      filter === s
                        ? "bg-indigo-600 text-white border-indigo-600"
                        : "bg-white text-slate-600 border-slate-200 hover:border-slate-300"
                    }`}
                  >
                    {s}
                  </button>
                ))}
                {filter !== "Tous" && (
                  <span className="text-xs text-slate-400 flex items-center gap-1 ml-2">
                    <IconTag className="w-3 h-3" />
                    {filtered.length} projet{filtered.length !== 1 ? "s" : ""} · {filtered.reduce((s, p) => s + p.revenue_eur, 0)}€
                  </span>
                )}
              </div>

              {/* Revenue summary */}
              {data && (
                <div className="bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-100 rounded-xl px-5 py-3 mb-5 flex items-center justify-between">
                  <span className="text-sm text-indigo-700 font-medium">CA total portefeuille</span>
                  <span className="text-lg font-bold text-indigo-700">{totalRevenue.toLocaleString("fr-FR")}€</span>
                </div>
              )}

              {!data && (
                <div className="text-center py-16 text-slate-400 text-sm">Chargement…</div>
              )}
              <div className="space-y-3">
                {filtered.map((p) => (
                  <ProjectCard key={p.project_id} project={p} />
                ))}
              </div>
            </>
          )}

          {tab === "skills" && data && (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {data.skills.map((cat) => (
                <SkillCategory key={cat.category} cat={cat} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
