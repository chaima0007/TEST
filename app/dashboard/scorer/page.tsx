"use client";

import { useEffect, useState } from "react";

type ThreatLevel = "low" | "medium" | "high" | "critical";

interface CompetitorProfile {
  competitor_id: string;
  name: string;
  sector: string;
  website: string;
  price_index: number;
  seo_strength: number;
  tech_quality: number;
  review_score: number;
  market_share_pct: number;
}

interface DimensionScores {
  price_threat: number;
  seo: number;
  tech: number;
  review_normalized: number;
  market: number;
}

interface ScoredCompetitor {
  profile: CompetitorProfile;
  threat_score: number;
  threat_level: ThreatLevel;
  dimension_scores: DimensionScores;
  strengths: string[];
  vulnerabilities: string[];
  recommendations: string[];
}

interface Summary {
  total: number;
  avg_threat_score: number;
  threat_level_distribution: Record<ThreatLevel, number>;
  top_threat_name: string;
  top_threat_score: number;
}

interface SectorSummary {
  sector: string;
  count: number;
  avg_threat: number;
  critical_count: number;
}

const THREAT_STYLES: Record<ThreatLevel, { bg: string; text: string; border: string; label: string }> = {
  critical: { bg: "bg-red-900/40",    text: "text-red-300",    border: "border-red-700/60",    label: "CRITIQUE" },
  high:     { bg: "bg-orange-900/40", text: "text-orange-300", border: "border-orange-700/60", label: "ÉLEVÉ" },
  medium:   { bg: "bg-amber-900/40",  text: "text-amber-300",  border: "border-amber-700/60",  label: "MOYEN" },
  low:      { bg: "bg-slate-800",     text: "text-slate-400",  border: "border-slate-700",     label: "FAIBLE" },
};

const DIM_LABELS: Record<keyof DimensionScores, string> = {
  price_threat: "Prix menace",
  seo: "SEO",
  tech: "Technique",
  review_normalized: "Avis clients",
  market: "Part marché",
};

function ThreatBadge({ level }: { level: ThreatLevel }) {
  const s = THREAT_STYLES[level];
  return (
    <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${s.bg} ${s.text} border ${s.border}`}>
      {s.label}
    </span>
  );
}

function DimBar({ label, value }: { label: string; value: number }) {
  const color =
    value >= 75 ? "bg-red-500" :
    value >= 55 ? "bg-orange-400" :
    value >= 35 ? "bg-amber-400" : "bg-slate-500";
  return (
    <div>
      <div className="flex justify-between text-[10px] text-slate-400 mb-0.5">
        <span>{label}</span>
        <span className="font-mono">{Math.round(value)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full ${color} rounded-full transition-all`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

function KpiCard({ label, value, sub, accent }: { label: string; value: string | number; sub?: string; accent?: string }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
      <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-1">{label}</p>
      <p className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</p>
      {sub && <p className="text-xs text-slate-500 mt-0.5">{sub}</p>}
    </div>
  );
}

function DetailModal({ comp, onClose }: { comp: ScoredCompetitor; onClose: () => void }) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const s = THREAT_STYLES[comp.threat_level];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60" onClick={onClose}>
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="px-6 py-4 border-b border-slate-800 flex items-start justify-between gap-3">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <h2 className="text-lg font-bold text-white">{comp.profile.name}</h2>
              <ThreatBadge level={comp.threat_level} />
            </div>
            <p className="text-xs text-slate-500">{comp.profile.sector} · {comp.profile.website}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none flex-shrink-0">×</button>
        </div>

        <div className="p-6 space-y-5">
          {/* Threat score */}
          <div className={`rounded-xl p-4 border ${s.bg} ${s.border} text-center`}>
            <p className="text-xs text-slate-400 mb-1">Score de menace</p>
            <p className={`text-4xl font-bold ${s.text}`}>{comp.threat_score}</p>
            <p className="text-xs text-slate-500 mt-1">/100</p>
          </div>

          {/* Dimensions */}
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-3">Dimensions</p>
            <div className="space-y-2">
              {(Object.entries(comp.dimension_scores) as [keyof DimensionScores, number][]).map(([k, v]) => (
                <DimBar key={k} label={DIM_LABELS[k]} value={v} />
              ))}
            </div>
          </div>

          {/* Strengths */}
          {comp.strengths.length > 0 && (
            <div>
              <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-2">Points forts</p>
              <ul className="space-y-1.5">
                {comp.strengths.map((s, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-emerald-400 flex-shrink-0 mt-0.5">✓</span>
                    {s}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Vulnerabilities */}
          {comp.vulnerabilities.length > 0 && (
            <div>
              <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-2">Vulnérabilités</p>
              <ul className="space-y-1.5">
                {comp.vulnerabilities.map((v, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-amber-400 flex-shrink-0 mt-0.5">⚠</span>
                    {v}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Recommendations */}
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-2">Recommandations</p>
            <ul className="space-y-1.5">
              {comp.recommendations.map((r, i) => (
                <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                  <span className="text-indigo-400 flex-shrink-0 mt-0.5">→</span>
                  {r}
                </li>
              ))}
            </ul>
          </div>

          {/* Raw inputs */}
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-2">Données brutes</p>
            <div className="grid grid-cols-2 gap-2 text-xs">
              {[
                ["Index prix", comp.profile.price_index],
                ["Force SEO", comp.profile.seo_strength],
                ["Qualité tech", comp.profile.tech_quality],
                ["Note avis", `${comp.profile.review_score.toFixed(1)}/5`],
                ["Part marché", `${comp.profile.market_share_pct}%`],
              ].map(([k, v]) => (
                <div key={String(k)} className="bg-slate-800 rounded-lg px-3 py-2">
                  <p className="text-slate-500">{k}</p>
                  <p className="text-white font-mono font-medium">{v}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function ScorerPage() {
  const [data, setData] = useState<{
    competitors: ScoredCompetitor[];
    summary: Summary;
    sector_summary: SectorSummary[];
  } | null>(null);
  const [loading, setLoading] = useState(true);
  const [levelFilter, setLevelFilter] = useState<ThreatLevel | "all">("all");
  const [sectorFilter, setSectorFilter] = useState("all");
  const [selected, setSelected] = useState<ScoredCompetitor | null>(null);

  useEffect(() => {
    fetch("/api/scorer")
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="p-6 text-slate-500 text-center py-16">Chargement…</div>;
  }

  if (!data) return null;

  const { competitors, summary, sector_summary } = data;

  const allSectors = Array.from(new Set(competitors.map((c) => c.profile.sector)));
  const filtered = competitors.filter((c) => {
    if (levelFilter !== "all" && c.threat_level !== levelFilter) return false;
    if (sectorFilter !== "all" && c.profile.sector !== sectorFilter) return false;
    return true;
  });

  const levelTabs: { key: ThreatLevel | "all"; label: string; count: number }[] = [
    { key: "all",      label: "Tous",     count: summary.total },
    { key: "critical", label: "Critique", count: summary.threat_level_distribution.critical },
    { key: "high",     label: "Élevé",    count: summary.threat_level_distribution.high },
    { key: "medium",   label: "Moyen",    count: summary.threat_level_distribution.medium },
    { key: "low",      label: "Faible",   count: summary.threat_level_distribution.low },
  ];

  return (
    <div className="p-6 space-y-6 text-slate-100">
      {selected && <DetailModal comp={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-white">Scoring Concurrents</h1>
        <p className="text-slate-400 text-sm mt-1">
          Analyse de menace sur 5 dimensions — prix, SEO, technique, avis, part de marché
        </p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard label="Concurrents analysés" value={summary.total} />
        <KpiCard
          label="Score moyen de menace"
          value={summary.avg_threat_score}
          sub="/100"
          accent={summary.avg_threat_score >= 75 ? "text-red-400" : summary.avg_threat_score >= 55 ? "text-orange-400" : "text-amber-400"}
        />
        <KpiCard
          label="Menaces critiques"
          value={summary.threat_level_distribution.critical}
          accent={summary.threat_level_distribution.critical > 0 ? "text-red-400" : "text-white"}
        />
        <KpiCard
          label="Menace principale"
          value={summary.top_threat_name ?? "—"}
          sub={`Score ${summary.top_threat_score}`}
          accent="text-red-300"
        />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-4 gap-6">
        {/* Main panel */}
        <div className="xl:col-span-3 space-y-4">
          {/* Filters */}
          <div className="flex flex-wrap gap-2 items-center">
            <div className="flex gap-1.5 flex-wrap">
              {levelTabs.map((t) => (
                <button
                  key={t.key}
                  onClick={() => setLevelFilter(t.key)}
                  className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${
                    levelFilter === t.key
                      ? "bg-indigo-600 text-white"
                      : "bg-slate-800 text-slate-400 hover:text-white"
                  }`}
                >
                  {t.label} <span className="opacity-60">({t.count})</span>
                </button>
              ))}
            </div>
            <select
              value={sectorFilter}
              onChange={(e) => setSectorFilter(e.target.value)}
              className="ml-auto text-xs bg-slate-800 border border-slate-700 text-slate-300 rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500"
            >
              <option value="all">Tous les secteurs</option>
              {allSectors.map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>

          {/* Competitor cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {filtered.map((comp) => {
              const s = THREAT_STYLES[comp.threat_level];
              return (
                <button
                  key={comp.profile.competitor_id}
                  onClick={() => setSelected(comp)}
                  className={`w-full text-left bg-slate-900 border rounded-xl p-4 hover:border-slate-600 transition-colors ${
                    comp.threat_level === "critical"
                      ? "border-red-800/50"
                      : comp.threat_level === "high"
                      ? "border-orange-800/40"
                      : "border-slate-800"
                  }`}
                >
                  <div className="flex items-start justify-between gap-2 mb-3">
                    <div>
                      <p className="text-sm font-semibold text-white">{comp.profile.name}</p>
                      <p className="text-xs text-slate-500 mt-0.5">{comp.profile.sector} · {comp.profile.website}</p>
                    </div>
                    <div className="flex flex-col items-end gap-1 flex-shrink-0">
                      <ThreatBadge level={comp.threat_level} />
                      <span className={`text-xl font-bold ${s.text}`}>{comp.threat_score}</span>
                    </div>
                  </div>

                  <div className="space-y-1.5">
                    {(Object.entries(comp.dimension_scores) as [keyof DimensionScores, number][]).map(([k, v]) => (
                      <DimBar key={k} label={DIM_LABELS[k]} value={v} />
                    ))}
                  </div>
                </button>
              );
            })}
            {filtered.length === 0 && (
              <div className="md:col-span-2 text-center py-12 text-slate-500">Aucun concurrent pour ce filtre</div>
            )}
          </div>
        </div>

        {/* Sector sidebar */}
        <div className="space-y-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-3">Par secteur</p>
            <div className="space-y-2">
              {sector_summary.map((s) => (
                <button
                  key={s.sector}
                  onClick={() => setSectorFilter(sectorFilter === s.sector ? "all" : s.sector)}
                  className={`w-full text-left rounded-lg p-2.5 transition-colors ${
                    sectorFilter === s.sector ? "bg-indigo-900/40 border border-indigo-700/40" : "hover:bg-slate-800 border border-transparent"
                  }`}
                >
                  <div className="flex justify-between items-center mb-1">
                    <p className="text-xs font-medium text-slate-300">{s.sector}</p>
                    <span className="text-xs text-slate-500">{s.count}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <div className="flex-1 mr-2">
                      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full ${s.avg_threat >= 75 ? "bg-red-500" : s.avg_threat >= 55 ? "bg-orange-400" : s.avg_threat >= 35 ? "bg-amber-400" : "bg-slate-500"}`}
                          style={{ width: `${s.avg_threat}%` }}
                        />
                      </div>
                    </div>
                    <span className="text-[10px] font-mono text-slate-400">{s.avg_threat}</span>
                  </div>
                  {s.critical_count > 0 && (
                    <p className="text-[10px] text-red-400 mt-1">{s.critical_count} critique{s.critical_count > 1 ? "s" : ""}</p>
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* Distribution */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-3">Distribution</p>
            <div className="space-y-2">
              {(["critical", "high", "medium", "low"] as ThreatLevel[]).map((lv) => {
                const count = summary.threat_level_distribution[lv];
                const pct = summary.total > 0 ? (count / summary.total) * 100 : 0;
                const style = THREAT_STYLES[lv];
                return (
                  <div key={lv}>
                    <div className="flex justify-between text-[10px] mb-0.5">
                      <span className={style.text}>{style.label}</span>
                      <span className="text-slate-500">{count}</span>
                    </div>
                    <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full ${
                          lv === "critical" ? "bg-red-500" : lv === "high" ? "bg-orange-400" : lv === "medium" ? "bg-amber-400" : "bg-slate-500"
                        }`}
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
