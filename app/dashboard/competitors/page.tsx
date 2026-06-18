"use client";

import Link from "next/link";
import { useState } from "react";
import { competitors as initialCompetitors } from "@/lib/data";

type ThreatLevel = "high" | "medium" | "low";

interface Competitor {
  id: string;
  name: string;
  website: string;
  industry: string;
  description: string;
  threatLevel: ThreatLevel;
  logo: string;
  color: string;
  marketShare: number;
  employees: string;
  lastUpdated: string;
}

type FilterTab = "Tous" | "Élevée" | "Moyenne" | "Faible";
type ViewMode = "grid" | "list";
type SortKey = "threatLevel" | "marketShare" | "name" | "lastUpdated";

const filterToThreat: Record<FilterTab, ThreatLevel | null> = {
  "Tous": null,
  "Élevée": "high",
  "Moyenne": "medium",
  "Faible": "low",
};

const threatConfig: Record<ThreatLevel, { label: string; badge: string; dot: string; rank: number }> = {
  high: {
    label: "Élevée",
    badge: "bg-red-50 text-red-700 border border-red-200",
    dot: "bg-red-500",
    rank: 0,
  },
  medium: {
    label: "Moyenne",
    badge: "bg-amber-50 text-amber-700 border border-amber-200",
    dot: "bg-amber-500",
    rank: 1,
  },
  low: {
    label: "Faible",
    badge: "bg-emerald-50 text-emerald-700 border border-emerald-200",
    dot: "bg-emerald-500",
    rank: 2,
  },
};

function ThreatBadge({ level }: { level: ThreatLevel }) {
  const cfg = threatConfig[level];
  return (
    <span className={`inline-flex items-center gap-1.5 text-xs font-medium px-2 py-0.5 rounded-full ${cfg.badge}`}>
      <span
        className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${cfg.dot} ${level === "high" ? "animate-pulse" : ""}`}
      />
      {cfg.label}
    </span>
  );
}

function MarketShareBar({ value }: { value: number }) {
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 bg-slate-100 rounded-full overflow-hidden">
        <div
          className="h-full bg-indigo-500 rounded-full transition-all"
          style={{ width: `${Math.min(value * 3, 100)}%` }}
        />
      </div>
      <span className="text-xs font-semibold text-slate-700 tabular-nums w-8 text-right">{value}%</span>
    </div>
  );
}

function GridIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
      <rect x="1" y="1" width="6" height="6" rx="1" />
      <rect x="9" y="1" width="6" height="6" rx="1" />
      <rect x="1" y="9" width="6" height="6" rx="1" />
      <rect x="9" y="9" width="6" height="6" rx="1" />
    </svg>
  );
}

function ListIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
      <rect x="1" y="2" width="14" height="2" rx="1" />
      <rect x="1" y="7" width="14" height="2" rx="1" />
      <rect x="1" y="12" width="14" height="2" rx="1" />
    </svg>
  );
}

function SearchIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="9" cy="9" r="6" />
      <line x1="14.5" y1="14.5" x2="18" y2="18" />
    </svg>
  );
}

function EmptyIllustration() {
  return (
    <svg width="64" height="64" viewBox="0 0 64 64" fill="none" className="mb-4">
      <rect x="8" y="12" width="48" height="40" rx="6" className="fill-slate-100" />
      <rect x="16" y="22" width="32" height="4" rx="2" className="fill-slate-200" />
      <rect x="16" y="30" width="24" height="4" rx="2" className="fill-slate-200" />
      <rect x="16" y="38" width="20" height="4" rx="2" className="fill-slate-200" />
      <circle cx="48" cy="48" r="10" className="fill-indigo-50 stroke-indigo-200" strokeWidth="2" />
      <line x1="44" y1="48" x2="52" y2="48" stroke="#6366f1" strokeWidth="2" strokeLinecap="round" />
      <line x1="48" y1="44" x2="48" y2="52" stroke="#6366f1" strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
}

function exportCSV(competitors: Competitor[]) {
  const csv = [
    "Nom,Industrie,Menace,Part de marché,Dernière MàJ",
    ...competitors.map(
      (c) => `${c.name},${c.industry},${c.threatLevel},${c.marketShare}%,${c.lastUpdated}`
    ),
  ].join("\n");
  const blob = new Blob([csv], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "concurrents.csv";
  a.click();
  URL.revokeObjectURL(url);
}

function sortCompetitors(list: Competitor[], sortKey: SortKey): Competitor[] {
  return [...list].sort((a, b) => {
    switch (sortKey) {
      case "threatLevel":
        return threatConfig[a.threatLevel].rank - threatConfig[b.threatLevel].rank;
      case "marketShare":
        return b.marketShare - a.marketShare;
      case "name":
        return a.name.localeCompare(b.name, "fr");
      case "lastUpdated":
        return new Date(b.lastUpdated).getTime() - new Date(a.lastUpdated).getTime();
      default:
        return 0;
    }
  });
}

export default function CompetitorsPage() {
  const [competitors, setCompetitors] = useState<Competitor[]>(
    initialCompetitors as Competitor[]
  );
  const [search, setSearch] = useState("");
  const [activeFilter, setActiveFilter] = useState<FilterTab>("Tous");
  const [industryFilter, setIndustryFilter] = useState<string>("Tous");
  const [sortKey, setSortKey] = useState<SortKey>("threatLevel");
  const [viewMode, setViewMode] = useState<ViewMode>("grid");
  const [showForm, setShowForm] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState("");
  const [form, setForm] = useState({
    name: "",
    website: "",
    industry: "",
    description: "",
    threatLevel: "medium" as ThreatLevel,
  });

  // Unique industries
  const allIndustries = ["Tous", ...Array.from(new Set(competitors.map((c) => c.industry)))];

  const filtered = sortCompetitors(
    competitors.filter((c) => {
      const q = search.toLowerCase();
      const matchesSearch =
        q === "" ||
        c.name.toLowerCase().includes(q) ||
        c.industry.toLowerCase().includes(q) ||
        c.website.toLowerCase().includes(q);
      const threatFilter = filterToThreat[activeFilter];
      const matchesFilter = threatFilter === null || c.threatLevel === threatFilter;
      const matchesIndustry = industryFilter === "Tous" || c.industry === industryFilter;
      return matchesSearch && matchesFilter && matchesIndustry;
    }),
    sortKey
  );

  const highThreatCount = filtered.filter((c) => c.threatLevel === "high").length;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setFormError("");
    try {
      const res = await fetch("/api/competitors", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (!res.ok) {
        const data = await res.json() as { error?: string };
        throw new Error(data.error || "Erreur lors de l'ajout");
      }
      const newCompetitor = await res.json() as Competitor;
      setCompetitors((prev) => [newCompetitor, ...prev]);
      setShowForm(false);
      setForm({ name: "", website: "", industry: "", description: "", threatLevel: "medium" });
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Erreur inconnue");
    } finally {
      setSubmitting(false);
    }
  };

  const filterTabs: FilterTab[] = ["Tous", "Élevée", "Moyenne", "Faible"];
  const filterCounts: Record<FilterTab, number> = {
    "Tous": competitors.length,
    "Élevée": competitors.filter((c) => c.threatLevel === "high").length,
    "Moyenne": competitors.filter((c) => c.threatLevel === "medium").length,
    "Faible": competitors.filter((c) => c.threatLevel === "low").length,
  };

  const sortOptions: { value: SortKey; label: string }[] = [
    { value: "threatLevel", label: "Niveau de menace" },
    { value: "marketShare", label: "Part de marché" },
    { value: "name", label: "Nom (A-Z)" },
    { value: "lastUpdated", label: "Dernière mise à jour" },
  ];

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Concurrents</h2>
          <p className="text-slate-500 text-sm mt-0.5">
            <span className="font-semibold text-slate-700">{competitors.length}</span> concurrent{competitors.length > 1 ? "s" : ""} surveillé{competitors.length > 1 ? "s" : ""}
          </p>
        </div>
        <div className="flex items-center gap-2">
          {/* Export CSV */}
          <button
            onClick={() => exportCSV(filtered)}
            className="inline-flex items-center gap-1.5 bg-white border border-slate-200 text-slate-600 px-3 py-2 rounded-lg text-sm font-medium hover:bg-slate-50 hover:border-slate-300 transition-colors shadow-sm"
          >
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
              <path d="M7 1v8M4 7l3 3 3-3" />
              <path d="M2 11h10" />
            </svg>
            Exporter CSV
          </button>
          <button
            onClick={() => { setShowForm(true); setFormError(""); }}
            className="inline-flex items-center gap-1.5 bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-indigo-700 active:bg-indigo-800 transition-colors shadow-sm"
          >
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
              <line x1="7" y1="1" x2="7" y2="13" />
              <line x1="1" y1="7" x2="13" y2="7" />
            </svg>
            Ajouter
          </button>
        </div>
      </div>

      {/* Add competitor modal */}
      {showForm && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4"
          onClick={(e) => { if (e.target === e.currentTarget) setShowForm(false); }}
        >
          <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl w-full max-w-md animate-in fade-in zoom-in-95 duration-200">
            <div className="px-6 py-5 border-b border-slate-100 flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-slate-900">Nouveau concurrent</h3>
                <p className="text-xs text-slate-400 mt-0.5">Ajoutez un concurrent à surveiller</p>
              </div>
              <button
                onClick={() => setShowForm(false)}
                className="w-8 h-8 flex items-center justify-center rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
                aria-label="Fermer"
              >
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                  <line x1="1" y1="1" x2="13" y2="13" />
                  <line x1="13" y1="1" x2="1" y2="13" />
                </svg>
              </button>
            </div>
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              {formError && (
                <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-100 rounded-lg text-xs text-red-600">
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" className="flex-shrink-0">
                    <circle cx="7" cy="7" r="6" />
                    <line x1="7" y1="4" x2="7" y2="7" />
                    <circle cx="7" cy="10" r="0.5" fill="currentColor" />
                  </svg>
                  {formError}
                </div>
              )}
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1.5">
                  Nom <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={form.name}
                  onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                  placeholder="ex: Salesforce"
                  required
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm text-slate-800 placeholder:text-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1.5">
                  Site web <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={form.website}
                  onChange={(e) => setForm((f) => ({ ...f, website: e.target.value }))}
                  placeholder="ex: salesforce.com"
                  required
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm text-slate-800 placeholder:text-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1.5">Secteur</label>
                <input
                  type="text"
                  value={form.industry}
                  onChange={(e) => setForm((f) => ({ ...f, industry: e.target.value }))}
                  placeholder="ex: CRM, Marketing..."
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm text-slate-800 placeholder:text-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1.5">Description</label>
                <textarea
                  value={form.description}
                  onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
                  placeholder="Décrivez brièvement ce concurrent..."
                  rows={2}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm text-slate-800 placeholder:text-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none transition-shadow"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1.5">Niveau de menace</label>
                <select
                  value={form.threatLevel}
                  onChange={(e) => setForm((f) => ({ ...f, threatLevel: e.target.value as ThreatLevel }))}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow bg-white"
                >
                  <option value="low">Faible</option>
                  <option value="medium">Moyenne</option>
                  <option value="high">Élevée</option>
                </select>
              </div>
              <div className="flex gap-3 pt-1">
                <button
                  type="submit"
                  disabled={submitting}
                  className="flex-1 bg-indigo-600 text-white py-2.5 rounded-lg text-sm font-semibold hover:bg-indigo-700 transition-colors disabled:opacity-60 flex items-center justify-center gap-2"
                >
                  {submitting && (
                    <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  )}
                  {submitting ? "Ajout en cours..." : "Ajouter le concurrent"}
                </button>
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="px-4 border border-slate-200 text-slate-600 py-2.5 rounded-lg text-sm font-semibold hover:bg-slate-50 transition-colors"
                >
                  Annuler
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Sort + Search + Filters + View toggle */}
      <div className="flex flex-col gap-3">
        {/* Top row: sort, search, view toggle */}
        <div className="flex flex-col sm:flex-row gap-3 items-start sm:items-center">
          {/* Sort dropdown */}
          <div className="flex items-center gap-2 flex-shrink-0">
            <label className="text-xs font-medium text-slate-500 whitespace-nowrap">Trier par :</label>
            <select
              value={sortKey}
              onChange={(e) => setSortKey(e.target.value as SortKey)}
              className="border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-700 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow"
            >
              {sortOptions.map((o) => (
                <option key={o.value} value={o.value}>{o.label}</option>
              ))}
            </select>
          </div>

          {/* Search */}
          <div className="relative w-full sm:w-72">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">
              <SearchIcon />
            </span>
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Rechercher un concurrent..."
              className="w-full pl-9 pr-3 py-2 border border-slate-200 rounded-lg text-sm text-slate-700 bg-white placeholder:text-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow"
            />
            {search && (
              <button
                onClick={() => setSearch("")}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
              >
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                  <line x1="1" y1="1" x2="11" y2="11" />
                  <line x1="11" y1="1" x2="1" y2="11" />
                </svg>
              </button>
            )}
          </div>

          {/* View toggle */}
          <div className="flex items-center gap-0.5 border border-slate-200 rounded-lg p-0.5 bg-white ml-auto flex-shrink-0">
            <button
              onClick={() => setViewMode("grid")}
              className={`p-1.5 rounded-md transition-colors ${
                viewMode === "grid"
                  ? "bg-slate-100 text-slate-900"
                  : "text-slate-400 hover:text-slate-600"
              }`}
              title="Vue grille"
            >
              <GridIcon />
            </button>
            <button
              onClick={() => setViewMode("list")}
              className={`p-1.5 rounded-md transition-colors ${
                viewMode === "list"
                  ? "bg-slate-100 text-slate-900"
                  : "text-slate-400 hover:text-slate-600"
              }`}
              title="Vue liste"
            >
              <ListIcon />
            </button>
          </div>
        </div>

        {/* Threat filter pills */}
        <div className="flex items-center gap-1.5 flex-wrap">
          {filterTabs.map((tab) => {
            const isActive = activeFilter === tab;
            const dotColor =
              tab === "Élevée" ? "bg-red-500" :
              tab === "Moyenne" ? "bg-amber-500" :
              tab === "Faible" ? "bg-emerald-500" : null;
            return (
              <button
                key={tab}
                onClick={() => setActiveFilter(tab)}
                className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-all border ${
                  isActive
                    ? "bg-indigo-600 text-white border-indigo-600 shadow-sm"
                    : "bg-white text-slate-600 border-slate-200 hover:border-slate-300 hover:bg-slate-50"
                }`}
              >
                {dotColor && (
                  <span className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${isActive ? "bg-white/70" : dotColor}`} />
                )}
                {tab}
                <span className={`text-[10px] font-semibold px-1 py-0.5 rounded-full min-w-[16px] text-center ${
                  isActive ? "bg-white/20 text-white" : "bg-slate-100 text-slate-500"
                }`}>
                  {filterCounts[tab]}
                </span>
              </button>
            );
          })}
        </div>

        {/* Industry filter pills */}
        <div className="flex items-center gap-1.5 flex-wrap">
          <span className="text-xs font-medium text-slate-400 mr-1">Secteur :</span>
          {allIndustries.map((industry) => {
            const isActive = industryFilter === industry;
            return (
              <button
                key={industry}
                onClick={() => setIndustryFilter(industry)}
                className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium transition-all border ${
                  isActive
                    ? "bg-indigo-600 text-white border-indigo-600 shadow-sm"
                    : "bg-white text-slate-600 border-slate-200 hover:border-slate-300 hover:bg-slate-50"
                }`}
              >
                {industry}
              </button>
            );
          })}
        </div>
      </div>

      {/* Result count */}
      <p className="text-xs text-slate-500">
        <span className="font-semibold text-slate-700">{filtered.length}</span> concurrent{filtered.length > 1 ? "s" : ""}
        {highThreatCount > 0 && (
          <>
            <span className="mx-1.5 text-slate-300">•</span>
            <span className="font-semibold text-red-600">{highThreatCount}</span>
            <span className="text-slate-500"> menace{highThreatCount > 1 ? "s" : ""} élevée{highThreatCount > 1 ? "s" : ""}</span>
          </>
        )}
        {search && (
          <> pour &ldquo;<span className="font-medium text-slate-800">{search}</span>&rdquo;</>
        )}
      </p>

      {/* Empty state */}
      {filtered.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-24 text-center">
          <EmptyIllustration />
          <h3 className="text-base font-semibold text-slate-800 mb-1.5">
            {search || activeFilter !== "Tous" || industryFilter !== "Tous" ? "Aucun résultat trouvé" : "Aucun concurrent"}
          </h3>
          <p className="text-sm text-slate-400 max-w-xs leading-relaxed">
            {search || activeFilter !== "Tous" || industryFilter !== "Tous"
              ? "Essayez de modifier votre recherche ou de réinitialiser les filtres."
              : "Commencez par ajouter votre premier concurrent à surveiller."}
          </p>
          <div className="flex gap-2 mt-5">
            {(search || activeFilter !== "Tous" || industryFilter !== "Tous") && (
              <button
                onClick={() => { setSearch(""); setActiveFilter("Tous"); setIndustryFilter("Tous"); }}
                className="text-sm text-slate-600 border border-slate-200 px-4 py-2 rounded-lg hover:bg-slate-50 transition-colors"
              >
                Réinitialiser les filtres
              </button>
            )}
            <button
              onClick={() => { setShowForm(true); setFormError(""); }}
              className="text-sm bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
            >
              + Ajouter un concurrent
            </button>
          </div>
        </div>
      ) : viewMode === "grid" ? (
        /* Grid view */
        <div className="grid md:grid-cols-2 gap-5">
          {filtered.map((c) => (
            <div key={c.id} className="bg-white rounded-xl border border-slate-200 p-5 hover:border-slate-300 hover:shadow-md transition-all group flex flex-col">
              {/* Card header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div
                    className="w-11 h-11 rounded-xl flex items-center justify-center text-white font-bold text-sm flex-shrink-0 shadow-sm"
                    style={{ backgroundColor: c.color }}
                  >
                    {c.logo}
                  </div>
                  <div className="min-w-0">
                    <h3 className="font-semibold text-slate-900 group-hover:text-indigo-600 transition-colors leading-tight">
                      {c.name}
                    </h3>
                    <p className="text-xs text-slate-400 mt-0.5 truncate">{c.website}</p>
                  </div>
                </div>
                <ThreatBadge level={c.threatLevel} />
              </div>

              <p className="text-sm text-slate-500 line-clamp-2 mb-4 leading-relaxed flex-1">{c.description}</p>

              {/* Stats */}
              <div className="space-y-3 mb-4">
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs text-slate-400">Parts de marché</span>
                  </div>
                  <MarketShareBar value={c.marketShare} />
                </div>
                <div className="grid grid-cols-3 gap-2">
                  <div className="bg-slate-50 rounded-lg p-2.5">
                    <p className="text-[10px] text-slate-400 uppercase tracking-wide">Secteur</p>
                    <p className="text-xs font-medium text-slate-700 mt-0.5 leading-tight">{c.industry}</p>
                  </div>
                  <div className="bg-slate-50 rounded-lg p-2.5">
                    <p className="text-[10px] text-slate-400 uppercase tracking-wide">Employés</p>
                    <p className="text-xs font-medium text-slate-700 mt-0.5">{c.employees}</p>
                  </div>
                  <div className="bg-slate-50 rounded-lg p-2.5">
                    <p className="text-[10px] text-slate-400 uppercase tracking-wide">Mise à jour</p>
                    <p className="text-xs font-medium text-slate-700 mt-0.5">
                      {new Date(c.lastUpdated).toLocaleDateString("fr-FR", { day: "numeric", month: "short" })}
                    </p>
                  </div>
                </div>
              </div>

              {/* Footer */}
              <Link
                href={`/dashboard/competitors/${c.id}`}
                className="mt-auto w-full flex items-center justify-center gap-1.5 border border-slate-200 text-slate-600 text-sm font-medium py-2 rounded-lg hover:bg-indigo-50 hover:border-indigo-300 hover:text-indigo-700 transition-colors group-hover:border-indigo-200"
              >
                Voir le profil
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M2 6h8M6 2l4 4-4 4" />
                </svg>
              </Link>
            </div>
          ))}
        </div>
      ) : (
        /* List view */
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-100 bg-slate-50/70">
                <th className="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">Concurrent</th>
                <th className="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide hidden sm:table-cell">Secteur</th>
                <th className="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">Menace</th>
                <th className="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide hidden md:table-cell">Parts de marché</th>
                <th className="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide hidden lg:table-cell">Mise à jour</th>
                <th className="text-right px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-50">
              {filtered.map((c) => (
                <tr key={c.id} className="hover:bg-slate-50/50 transition-colors group">
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-3">
                      <div
                        className="w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold text-xs flex-shrink-0"
                        style={{ backgroundColor: c.color }}
                      >
                        {c.logo}
                      </div>
                      <div className="min-w-0">
                        <p className="font-semibold text-slate-900 group-hover:text-indigo-600 transition-colors truncate">{c.name}</p>
                        <p className="text-xs text-slate-400 truncate">{c.website}</p>
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-3 hidden sm:table-cell">
                    <span className="text-xs text-slate-600 bg-slate-100 px-2 py-0.5 rounded-md">{c.industry}</span>
                  </td>
                  <td className="px-4 py-3">
                    <ThreatBadge level={c.threatLevel} />
                  </td>
                  <td className="px-4 py-3 hidden md:table-cell w-36">
                    <MarketShareBar value={c.marketShare} />
                  </td>
                  <td className="px-4 py-3 hidden lg:table-cell text-xs text-slate-500">
                    {new Date(c.lastUpdated).toLocaleDateString("fr-FR", { day: "numeric", month: "short", year: "numeric" })}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <Link
                      href={`/dashboard/competitors/${c.id}`}
                      className="inline-flex items-center gap-1 text-xs font-medium text-indigo-600 hover:text-indigo-800 transition-colors"
                    >
                      Analyser
                      <svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M1.5 5h7M5 1.5l3.5 3.5L5 8.5" />
                      </svg>
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
