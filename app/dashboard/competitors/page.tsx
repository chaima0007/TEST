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

const threatColors: Record<ThreatLevel, string> = {
  high: "bg-red-100 text-red-700 border-red-200",
  medium: "bg-amber-100 text-amber-700 border-amber-200",
  low: "bg-emerald-100 text-emerald-700 border-emerald-200",
};

const threatLabels: Record<ThreatLevel, string> = {
  high: "Menace Élevée",
  medium: "Menace Moyenne",
  low: "Menace Faible",
};

type FilterTab = "Tous" | "Menace Élevée" | "Menace Moyenne" | "Menace Faible";

const filterToThreat: Record<FilterTab, ThreatLevel | null> = {
  "Tous": null,
  "Menace Élevée": "high",
  "Menace Moyenne": "medium",
  "Menace Faible": "low",
};

export default function CompetitorsPage() {
  const [competitors, setCompetitors] = useState<Competitor[]>(
    initialCompetitors as Competitor[]
  );
  const [search, setSearch] = useState("");
  const [activeFilter, setActiveFilter] = useState<FilterTab>("Tous");
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

  const filtered = competitors.filter((c) => {
    const matchesSearch =
      search === "" ||
      c.name.toLowerCase().includes(search.toLowerCase()) ||
      c.industry.toLowerCase().includes(search.toLowerCase()) ||
      c.website.toLowerCase().includes(search.toLowerCase());

    const threatFilter = filterToThreat[activeFilter];
    const matchesFilter = threatFilter === null || c.threatLevel === threatFilter;

    return matchesSearch && matchesFilter;
  });

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

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Concurrents</h2>
          <p className="text-slate-500 text-sm mt-1">{competitors.length} concurrent{competitors.length > 1 ? "s" : ""} surveillé{competitors.length > 1 ? "s" : ""}</p>
        </div>
        <button
          onClick={() => { setShowForm(true); setFormError(""); }}
          className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors"
        >
          + Ajouter un concurrent
        </button>
      </div>

      {/* Add competitor modal */}
      {showForm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl w-full max-w-md">
            <div className="px-6 py-5 border-b border-slate-100 flex items-center justify-between">
              <h3 className="font-semibold text-slate-900">Ajouter un concurrent</h3>
              <button
                onClick={() => setShowForm(false)}
                className="text-slate-400 hover:text-slate-600 transition-colors text-lg leading-none"
                aria-label="Fermer"
              >
                ×
              </button>
            </div>
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              {formError && (
                <div className="p-3 bg-red-50 border border-red-100 rounded-lg text-xs text-red-600">
                  {formError}
                </div>
              )}
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Nom <span className="text-red-500">*</span></label>
                <input
                  type="text"
                  value={form.name}
                  onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                  placeholder="ex: Salesforce"
                  required
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Site web <span className="text-red-500">*</span></label>
                <input
                  type="text"
                  value={form.website}
                  onChange={(e) => setForm((f) => ({ ...f, website: e.target.value }))}
                  placeholder="ex: salesforce.com"
                  required
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Secteur</label>
                <input
                  type="text"
                  value={form.industry}
                  onChange={(e) => setForm((f) => ({ ...f, industry: e.target.value }))}
                  placeholder="ex: CRM, Marketing..."
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Description</label>
                <textarea
                  value={form.description}
                  onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
                  placeholder="Décrivez brièvement ce concurrent..."
                  rows={2}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Niveau de menace</label>
                <select
                  value={form.threatLevel}
                  onChange={(e) => setForm((f) => ({ ...f, threatLevel: e.target.value as ThreatLevel }))}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="low">Faible</option>
                  <option value="medium">Moyenne</option>
                  <option value="high">Élevée</option>
                </select>
              </div>
              <div className="flex gap-3 pt-2">
                <button
                  type="submit"
                  disabled={submitting}
                  className="flex-1 bg-indigo-600 text-white py-2.5 rounded-lg text-sm font-semibold hover:bg-indigo-700 transition-colors disabled:opacity-60 flex items-center justify-center gap-2"
                >
                  {submitting && (
                    <span className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                  )}
                  {submitting ? "Ajout..." : "Ajouter"}
                </button>
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="flex-1 border border-slate-200 text-slate-600 py-2.5 rounded-lg text-sm font-semibold hover:bg-slate-50 transition-colors"
                >
                  Annuler
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Search + Filter */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">🔍</span>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Rechercher un concurrent..."
            className="w-full pl-9 pr-3 py-2 border border-slate-200 rounded-lg text-sm text-slate-700 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <div className="flex gap-2">
          {(["Tous", "Menace Élevée", "Menace Moyenne", "Menace Faible"] as FilterTab[]).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveFilter(tab)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors whitespace-nowrap ${
                activeFilter === tab
                  ? "bg-indigo-600 text-white"
                  : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-50"
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {/* Grid */}
      {filtered.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-center">
          <div className="w-20 h-20 rounded-2xl bg-slate-100 flex items-center justify-center text-4xl mb-4">
            🏢
          </div>
          <h3 className="text-lg font-semibold text-slate-700 mb-2">
            {search || activeFilter !== "Tous" ? "Aucun concurrent trouvé" : "Aucun concurrent"}
          </h3>
          <p className="text-sm text-slate-400 max-w-xs">
            {search || activeFilter !== "Tous"
              ? "Essayez de modifier votre recherche ou vos filtres."
              : "Commencez par ajouter votre premier concurrent à surveiller."}
          </p>
          {(search || activeFilter !== "Tous") && (
            <button
              onClick={() => { setSearch(""); setActiveFilter("Tous"); }}
              className="mt-4 text-sm text-indigo-600 hover:underline"
            >
              Réinitialiser les filtres
            </button>
          )}
        </div>
      ) : (
        <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-5">
          {filtered.map((c) => (
            <Link
              key={c.id}
              href={`/dashboard/competitors/${c.id}`}
              className="bg-white rounded-xl border border-slate-200 p-5 hover:border-indigo-300 hover:shadow-md transition-all group"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div
                    className="w-10 h-10 rounded-xl flex items-center justify-center text-white font-bold text-sm"
                    style={{ backgroundColor: c.color }}
                  >
                    {c.logo}
                  </div>
                  <div>
                    <h3 className="font-semibold text-slate-900 group-hover:text-indigo-600 transition-colors">
                      {c.name}
                    </h3>
                    <p className="text-xs text-slate-400">{c.website}</p>
                  </div>
                </div>
                <span className={`text-xs font-medium px-2 py-0.5 rounded-full border ${threatColors[c.threatLevel]}`}>
                  {threatLabels[c.threatLevel]}
                </span>
              </div>

              <p className="text-sm text-slate-500 line-clamp-2 mb-4 leading-relaxed">{c.description}</p>

              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Secteur</p>
                  <p className="text-xs font-medium text-slate-700 mt-0.5">{c.industry}</p>
                </div>
                <div className="bg-slate-50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Part de marché</p>
                  <p className="text-xs font-medium text-slate-700 mt-0.5">{c.marketShare}%</p>
                </div>
                <div className="bg-slate-50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Employés</p>
                  <p className="text-xs font-medium text-slate-700 mt-0.5">{c.employees}</p>
                </div>
                <div className="bg-slate-50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Mis à jour</p>
                  <p className="text-xs font-medium text-slate-700 mt-0.5">{c.lastUpdated}</p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
