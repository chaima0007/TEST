"use client";

import { notFound, useRouter } from "next/navigation";
import Link from "next/link";
import { use, useState } from "react";
import { competitors } from "@/lib/data";
import { useToast } from "@/components/Toast";

type ThreatLevel = "high" | "medium" | "low";
type TabId = "apercu" | "fonctionnalites" | "tarifs" | "actualites";

function formatDate(dateStr: string) {
  const d = new Date(dateStr);
  if (isNaN(d.getTime())) return dateStr;
  return d.toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" });
}

function formatShortDate(dateStr: string) {
  const d = new Date(dateStr);
  if (isNaN(d.getTime())) return dateStr;
  return d.toLocaleDateString("fr-FR", { day: "numeric", month: "short", year: "numeric" });
}

const newsTypeConfig: Record<string, { label: string; cls: string }> = {
  product:     { label: "Produit",      cls: "bg-indigo-50 text-indigo-700 border border-indigo-100" },
  pricing:     { label: "Tarifs",       cls: "bg-amber-50 text-amber-700 border border-amber-100" },
  acquisition: { label: "Acquisition",  cls: "bg-rose-50 text-rose-700 border border-rose-100" },
  partnership: { label: "Partenariat",  cls: "bg-emerald-50 text-emerald-700 border border-emerald-100" },
};

const threatConfig: Record<ThreatLevel, { label: string; badge: string; dot: string; ring: string }> = {
  high:   { label: "Menace Élevée",  badge: "bg-red-50 text-red-700 border border-red-200",     dot: "bg-red-500",     ring: "ring-red-200" },
  medium: { label: "Menace Moyenne", badge: "bg-amber-50 text-amber-700 border border-amber-200", dot: "bg-amber-500",   ring: "ring-amber-200" },
  low:    { label: "Menace Faible",  badge: "bg-emerald-50 text-emerald-700 border border-emerald-200", dot: "bg-emerald-500", ring: "ring-emerald-200" },
};

const qualityConfig: Record<string, string> = {
  Excellent: "bg-emerald-50 text-emerald-700 border border-emerald-100",
  Bien:      "bg-indigo-50 text-indigo-700 border border-indigo-100",
  Moyen:     "bg-amber-50 text-amber-700 border border-amber-100",
};

const tabs: { id: TabId; label: string }[] = [
  { id: "apercu",         label: "Aperçu" },
  { id: "fonctionnalites", label: "Fonctionnalités" },
  { id: "tarifs",         label: "Tarifs" },
  { id: "actualites",     label: "Actualités" },
];

export default function CompetitorDetailPage(props: PageProps<"/dashboard/competitors/[id]">) {
  const { id } = use(props.params);
  const router = useRouter();
  const { toast } = useToast();

  const [activeTab, setActiveTab] = useState<TabId>("apercu");
  const [deleting, setDeleting] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [showEdit, setShowEdit] = useState(false);
  const [saving, setSaving] = useState(false);

  const competitor = competitors.find((c) => c.id === id);
  if (!competitor) notFound();

  const [editForm, setEditForm] = useState({
    name: competitor.name,
    website: competitor.website,
    industry: competitor.industry,
    description: competitor.description,
    threatLevel: competitor.threatLevel as ThreatLevel,
  });

  const threatLevel = competitor.threatLevel as ThreatLevel;
  const threat = threatConfig[threatLevel];
  const priceHistory = competitor.priceHistory;
  const maxPrice = priceHistory.length ? Math.max(...priceHistory) : 0;
  const minPrice = priceHistory.length ? Math.min(...priceHistory) : 0;

  const handleDelete = async () => {
    setDeleting(true);
    try {
      const res = await fetch(`/api/competitors/${id}`, { method: "DELETE" });
      if (res.ok) {
        toast("Concurrent supprimé");
        router.push("/dashboard/competitors");
        router.refresh();
      } else {
        throw new Error();
      }
    } catch {
      toast("Erreur lors de la suppression", "error");
      setDeleting(false);
      setShowConfirm(false);
    }
  };

  const handleEdit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      const res = await fetch(`/api/competitors/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(editForm),
      });
      if (res.ok) {
        toast("Concurrent mis à jour");
        setShowEdit(false);
        router.refresh();
      } else {
        throw new Error();
      }
    } catch {
      toast("Erreur lors de la mise à jour", "error");
    } finally {
      setSaving(false);
    }
  };

  const months = ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun", "Jul", "Aoû", "Sep", "Oct", "Nov", "Déc"];

  return (
    <div className="space-y-6">

      {/* Edit modal */}
      {showEdit && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4"
          onClick={(e) => { if (e.target === e.currentTarget) setShowEdit(false); }}
        >
          <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl w-full max-w-md">
            <div className="px-6 py-5 border-b border-slate-100 flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-slate-900">Modifier {competitor.name}</h3>
                <p className="text-xs text-slate-400 mt-0.5">Modifiez les informations du concurrent</p>
              </div>
              <button
                onClick={() => setShowEdit(false)}
                className="w-8 h-8 flex items-center justify-center rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
              >
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                  <line x1="1" y1="1" x2="13" y2="13" />
                  <line x1="13" y1="1" x2="1" y2="13" />
                </svg>
              </button>
            </div>
            <form onSubmit={handleEdit} className="p-6 space-y-4">
              {[
                { label: "Nom", key: "name" as const, type: "text", required: true },
                { label: "Site web", key: "website" as const, type: "text", required: true },
                { label: "Secteur", key: "industry" as const, type: "text", required: false },
              ].map((f) => (
                <div key={f.key}>
                  <label className="block text-xs font-medium text-slate-600 mb-1.5">
                    {f.label}{f.required && <span className="text-red-500 ml-0.5">*</span>}
                  </label>
                  <input
                    type={f.type}
                    value={editForm[f.key]}
                    onChange={(e) => setEditForm((prev) => ({ ...prev, [f.key]: e.target.value }))}
                    required={f.required}
                    className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow"
                  />
                </div>
              ))}
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1.5">Description</label>
                <textarea
                  value={editForm.description}
                  onChange={(e) => setEditForm((prev) => ({ ...prev, description: e.target.value }))}
                  rows={2}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none transition-shadow"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1.5">Niveau de menace</label>
                <select
                  value={editForm.threatLevel}
                  onChange={(e) => setEditForm((prev) => ({ ...prev, threatLevel: e.target.value as ThreatLevel }))}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white transition-shadow"
                >
                  <option value="low">Faible</option>
                  <option value="medium">Moyenne</option>
                  <option value="high">Élevée</option>
                </select>
              </div>
              <div className="flex gap-3 pt-1">
                <button
                  type="submit"
                  disabled={saving}
                  className="flex-1 bg-indigo-600 text-white py-2.5 rounded-lg text-sm font-semibold hover:bg-indigo-700 disabled:opacity-60 flex items-center justify-center gap-2 transition-colors"
                >
                  {saving && <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />}
                  {saving ? "Sauvegarde..." : "Sauvegarder"}
                </button>
                <button
                  type="button"
                  onClick={() => setShowEdit(false)}
                  className="px-4 border border-slate-200 text-slate-600 py-2.5 rounded-lg text-sm font-semibold hover:bg-slate-50 transition-colors"
                >
                  Annuler
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete confirmation modal */}
      {showConfirm && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4"
          onClick={(e) => { if (e.target === e.currentTarget && !deleting) setShowConfirm(false); }}
        >
          <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl w-full max-w-sm p-6 text-center">
            <div className="w-12 h-12 rounded-full bg-red-50 border border-red-100 flex items-center justify-center mx-auto mb-4">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="#dc2626" strokeWidth="2" strokeLinecap="round">
                <path d="M10 6v4M10 14h.01M19 10a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="font-semibold text-slate-900 mb-1.5">Supprimer {competitor.name} ?</h3>
            <p className="text-sm text-slate-500 mb-6 leading-relaxed">
              Cette action est irréversible. Toutes les données associées à ce concurrent seront supprimées définitivement.
            </p>
            <div className="flex gap-3">
              <button
                onClick={handleDelete}
                disabled={deleting}
                className="flex-1 bg-red-600 text-white py-2.5 rounded-lg text-sm font-semibold hover:bg-red-700 disabled:opacity-60 flex items-center justify-center gap-2 transition-colors"
              >
                {deleting && <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />}
                {deleting ? "Suppression..." : "Supprimer définitivement"}
              </button>
              <button
                onClick={() => setShowConfirm(false)}
                disabled={deleting}
                className="px-4 border border-slate-200 text-slate-600 py-2.5 rounded-lg text-sm font-semibold hover:bg-slate-50 disabled:opacity-60 transition-colors"
              >
                Annuler
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Top nav */}
      <div className="flex items-center justify-between flex-wrap gap-2">
        <Link
          href="/dashboard/competitors"
          className="inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-900 transition-colors"
        >
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M9 1L3 7l6 6" />
          </svg>
          Retour aux concurrents
        </Link>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowEdit(true)}
            className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-600 border border-indigo-200 hover:border-indigo-400 hover:bg-indigo-50 px-3 py-1.5 rounded-lg transition-colors"
          >
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
              <path d="M8.5 1.5l2 2-7 7H1.5v-2l7-7z" />
            </svg>
            Modifier
          </button>
          <button
            onClick={() => setShowConfirm(true)}
            className="inline-flex items-center gap-1.5 text-sm font-medium text-red-500 border border-red-200 hover:border-red-400 hover:bg-red-50 px-3 py-1.5 rounded-lg transition-colors"
          >
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
              <path d="M1.5 3h9M4 3V2h4v1M5 5.5v4M7 5.5v4M2.5 3l.75 7.5h5.5L9.5 3" />
            </svg>
            Supprimer
          </button>
        </div>
      </div>

      {/* Profile header card */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
        <div className="flex items-start gap-5 flex-wrap sm:flex-nowrap">
          {/* Logo */}
          <div
            className="w-16 h-16 rounded-2xl flex items-center justify-center text-white text-xl font-bold flex-shrink-0 shadow-md"
            style={{ backgroundColor: competitor.color }}
          >
            {competitor.logo}
          </div>

          {/* Info */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-3 flex-wrap">
              <h2 className="text-2xl font-bold text-slate-900 tracking-tight">{competitor.name}</h2>
              <span className={`inline-flex items-center gap-1.5 text-xs font-medium px-2.5 py-1 rounded-full ${threat.badge}`}>
                <span className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${threat.dot} ${threatLevel === "high" ? "animate-pulse" : ""}`} />
                {threat.label}
              </span>
            </div>
            <div className="flex items-center gap-1.5 mt-1.5">
              <a
                href={/^https?:\/\//.test(competitor.website) ? competitor.website : `https://${competitor.website}`}
                className="text-sm text-indigo-600 hover:text-indigo-800 hover:underline inline-flex items-center gap-1 transition-colors"
                target="_blank"
                rel="noopener noreferrer"
              >
                {competitor.website}
                <svg width="11" height="11" viewBox="0 0 11 11" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M2 9L9 2M5 2h4v4" />
                </svg>
              </a>
            </div>
            <p className="text-slate-500 mt-2 text-sm leading-relaxed max-w-2xl">{competitor.description}</p>
            <div className="flex flex-wrap gap-x-6 gap-y-1.5 mt-3">
              {[
                { label: "Fondé en", value: competitor.founded },
                { label: "Employés", value: competitor.employees },
                { label: "Revenue", value: competitor.revenue },
                { label: "Part de marché", value: `${competitor.marketShare}%` },
              ].map((d) => (
                <div key={d.label} className="text-xs text-slate-500">
                  <span className="text-slate-400">{d.label} </span>
                  <span className="font-semibold text-slate-700">{d.value}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Last updated — top right */}
          <div className="text-right flex-shrink-0 hidden sm:block">
            <p className="text-[10px] text-slate-400 uppercase tracking-wide">Dernière MAJ</p>
            <p className="text-xs font-medium text-slate-600 mt-0.5">{formatDate(competitor.lastUpdated)}</p>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-slate-200">
        <nav className="flex gap-0 -mb-px overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-5 py-3 text-sm font-medium border-b-2 transition-colors whitespace-nowrap ${
                activeTab === tab.id
                  ? "border-indigo-600 text-indigo-600"
                  : "border-transparent text-slate-500 hover:text-slate-800 hover:border-slate-300"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab: Apercu */}
      {activeTab === "apercu" && (
        <div className="space-y-6">
          {/* Key stats */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              { label: "Part de marché", value: `${competitor.marketShare}%`, sub: "du marché total", color: "text-indigo-600" },
              { label: "Employés", value: competitor.employees, sub: "effectif mondial", color: "text-slate-700" },
              { label: "Revenue annuel", value: competitor.revenue, sub: "chiffre d'affaires", color: "text-emerald-600" },
              { label: "Fondé en", value: String(competitor.founded), sub: `${2026 - competitor.founded} ans d'existence`, color: "text-slate-700" },
            ].map((stat) => (
              <div key={stat.label} className="bg-white rounded-xl border border-slate-200 p-4 hover:shadow-sm transition-shadow">
                <p className="text-xs text-slate-400 mb-1">{stat.label}</p>
                <p className={`text-2xl font-bold ${stat.color}`}>{stat.value}</p>
                <p className="text-xs text-slate-400 mt-0.5">{stat.sub}</p>
              </div>
            ))}
          </div>

          {/* Description card */}
          <div className="bg-white rounded-xl border border-slate-200 p-5">
            <h3 className="font-semibold text-slate-900 mb-3">À propos</h3>
            <p className="text-sm text-slate-600 leading-relaxed">{competitor.description}</p>
          </div>

          {/* Price chart */}
          <div className="bg-white rounded-xl border border-slate-200 p-5">
            <div className="flex items-center justify-between mb-5">
              <div>
                <h3 className="font-semibold text-slate-900">Évolution du prix</h3>
                <p className="text-xs text-slate-400 mt-0.5">12 derniers mois</p>
              </div>
              <div className="text-right">
                <p className="text-xs text-slate-400">Prix actuel</p>
                <p className="text-lg font-bold text-slate-900 mt-0.5">
                  {priceHistory[priceHistory.length - 1]}€
                  <span className="text-xs font-normal text-slate-400">/mois</span>
                </p>
              </div>
            </div>

            {/* Chart */}
            <div className="relative">
              <div className="flex items-end gap-1 h-36">
                {priceHistory.map((price, i) => {
                  const range = maxPrice - minPrice || 1;
                  const heightPct = Math.max(8, Math.round(((price - minPrice) / range) * 72) + 20);
                  const isLast = i === priceHistory.length - 1;
                  const prevPrice = i > 0 ? priceHistory[i - 1] : price;
                  const isUp = price > prevPrice;
                  const isDown = price < prevPrice;
                  return (
                    <div key={i} className="flex-1 flex flex-col items-center gap-1 group relative">
                      <div
                        className="w-full rounded-t transition-all duration-300"
                        style={{
                          height: `${heightPct}%`,
                          backgroundColor: competitor.color,
                          opacity: isLast ? 1 : 0.25 + (i / (priceHistory.length - 1)) * 0.65,
                        }}
                      />
                      <span className="text-[9px] text-slate-400 hidden sm:block">{months[i]}</span>
                      {/* Tooltip */}
                      <div className="absolute -top-10 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-10">
                        <div className="bg-slate-800 text-white text-[10px] font-medium px-2 py-1 rounded-lg shadow-lg whitespace-nowrap flex items-center gap-1">
                          {isUp && <span className="text-red-400">+</span>}
                          {isDown && <span className="text-emerald-400">-</span>}
                          {price}€
                        </div>
                        <div className="w-2 h-2 bg-slate-800 rotate-45 mx-auto -mt-1" />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="flex items-center justify-between mt-3 pt-3 border-t border-slate-50 text-xs text-slate-400">
              <span>Min : <span className="font-semibold text-slate-600">{minPrice}€</span></span>
              <div className="flex items-center gap-1">
                <span className="text-slate-300">Variation 12 mois :</span>
                {(() => {
                  const change = priceHistory[priceHistory.length - 1] - priceHistory[0];
                  const pct = priceHistory[0] ? Math.round((change / priceHistory[0]) * 100) : 0;
                  return (
                    <span className={`font-semibold ${change > 0 ? "text-red-600" : change < 0 ? "text-emerald-600" : "text-slate-600"}`}>
                      {change > 0 ? "+" : ""}{pct}%
                    </span>
                  );
                })()}
              </div>
              <span>Max : <span className="font-semibold text-slate-600">{maxPrice}€</span></span>
            </div>
          </div>
        </div>
      )}

      {/* Tab: Fonctionnalites */}
      {activeTab === "fonctionnalites" && (
        <div className="bg-white rounded-xl border border-slate-200 p-5">
          <div className="flex items-center justify-between mb-5">
            <div>
              <h3 className="font-semibold text-slate-900">Fonctionnalités</h3>
              <p className="text-xs text-slate-400 mt-0.5">
                {competitor.features.filter((f) => f.available).length} disponibles sur {competitor.features.length}
              </p>
            </div>
            <div className="flex items-center gap-3 flex-wrap">
              {[
                { label: "Excellent", cls: "bg-emerald-50 text-emerald-700 border border-emerald-100" },
                { label: "Bien",      cls: "bg-indigo-50 text-indigo-700 border border-indigo-100" },
                { label: "Moyen",     cls: "bg-amber-50 text-amber-700 border border-amber-100" },
              ].map((q) => (
                <span key={q.label} className={`text-[10px] font-medium px-2 py-0.5 rounded-full ${q.cls}`}>
                  {q.label}
                </span>
              ))}
            </div>
          </div>
          <div className="grid sm:grid-cols-2 gap-2">
            {competitor.features.map((f) => (
              <div
                key={f.name}
                className={`flex items-center justify-between px-4 py-3 rounded-xl border transition-colors ${
                  f.available
                    ? "bg-white border-slate-200 hover:border-slate-300"
                    : "bg-slate-50/50 border-slate-100"
                }`}
              >
                <div className="flex items-center gap-2.5 min-w-0">
                  <span className={`w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0 text-[11px] font-bold ${
                    f.available ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-400"
                  }`}>
                    {f.available ? "✓" : "✕"}
                  </span>
                  <span className={`text-sm truncate ${f.available ? "text-slate-800" : "text-slate-400 line-through"}`}>
                    {f.name}
                  </span>
                </div>
                {f.available && f.quality && f.quality !== "-" ? (
                  <span className={`text-xs font-medium px-2 py-0.5 rounded-full flex-shrink-0 ml-2 ${qualityConfig[f.quality] || "bg-slate-100 text-slate-600"}`}>
                    {f.quality}
                  </span>
                ) : !f.available ? (
                  <span className="text-xs text-slate-300 flex-shrink-0 ml-2">Indisponible</span>
                ) : null}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab: Tarifs */}
      {activeTab === "tarifs" && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-semibold text-slate-900">Plans tarifaires</h3>
              <p className="text-xs text-slate-400 mt-0.5">{competitor.pricing.length} plans disponibles</p>
            </div>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {competitor.pricing.map((plan, i) => {
              const isPopular = i === 1;
              return (
                <div
                  key={plan.name}
                  className={`bg-white rounded-xl border p-5 flex flex-col hover:shadow-md transition-all ${
                    isPopular
                      ? "border-indigo-300 ring-2 ring-indigo-100 shadow-sm"
                      : "border-slate-200"
                  }`}
                >
                  {isPopular && (
                    <div className="inline-flex items-center gap-1 text-[10px] font-semibold text-indigo-600 bg-indigo-50 border border-indigo-100 px-2 py-0.5 rounded-full self-start mb-3">
                      <svg width="10" height="10" viewBox="0 0 10 10" fill="currentColor"><path d="M5 1l1.2 2.5L9 4l-2 1.9.5 2.7L5 7.3 2.5 8.6 3 5.9 1 4l2.8-.5L5 1z"/></svg>
                      Populaire
                    </div>
                  )}
                  <h4 className="font-semibold text-slate-800 mb-1">{plan.name}</h4>
                  <div className="flex items-baseline gap-1 mb-4">
                    {plan.price === 0 ? (
                      <span className="text-2xl font-bold text-emerald-600">Gratuit</span>
                    ) : (
                      <>
                        <span className="text-3xl font-bold text-slate-900">{plan.price}</span>
                        <span className="text-sm text-slate-400">{plan.currency}/{plan.interval}</span>
                      </>
                    )}
                  </div>
                  <ul className="space-y-2 flex-1">
                    {plan.features.map((feat) => (
                      <li key={feat} className="flex items-start gap-2 text-xs text-slate-600">
                        <span className="w-4 h-4 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center flex-shrink-0 mt-0.5 font-bold text-[10px]">✓</span>
                        {feat}
                      </li>
                    ))}
                  </ul>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Tab: Actualites */}
      {activeTab === "actualites" && (
        <div className="bg-white rounded-xl border border-slate-200 p-5">
          <div className="flex items-center justify-between mb-5">
            <div>
              <h3 className="font-semibold text-slate-900">Actualités récentes</h3>
              <p className="text-xs text-slate-400 mt-0.5">{competitor.news.length} événement{competitor.news.length > 1 ? "s" : ""} enregistré{competitor.news.length > 1 ? "s" : ""}</p>
            </div>
          </div>
          <div className="relative">
            {/* Timeline line */}
            <div className="absolute left-[7px] top-2 bottom-2 w-px bg-slate-100" />
            <div className="space-y-0">
              {competitor.news.map((n, i) => {
                const cfg = newsTypeConfig[n.type] || { label: n.type, cls: "bg-slate-100 text-slate-600 border border-slate-200" };
                return (
                  <div key={i} className="flex items-start gap-4 relative pl-6 py-4 group">
                    {/* Timeline dot */}
                    <div
                      className="absolute left-0 top-5 w-3.5 h-3.5 rounded-full border-2 border-white ring-2 flex-shrink-0 shadow-sm"
                      style={{
                        backgroundColor: competitor.color,
                        ringColor: competitor.color + "40",
                      }}
                    />

                    <div className="flex-1 min-w-0 bg-slate-50/0 group-hover:bg-slate-50 rounded-lg px-0 transition-colors">
                      <div className="flex items-start justify-between gap-3 flex-wrap">
                        <div className="flex items-start gap-2.5 flex-wrap">
                          <span className={`inline-block text-[10px] font-semibold px-2 py-0.5 rounded-full flex-shrink-0 ${cfg.cls}`}>
                            {cfg.label}
                          </span>
                          <p className="text-sm text-slate-800 leading-relaxed">{n.title}</p>
                        </div>
                        <span className="text-xs text-slate-400 whitespace-nowrap flex-shrink-0">{formatShortDate(n.date)}</span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
          {competitor.news.length === 0 && (
            <div className="text-center py-10">
              <p className="text-sm text-slate-400">Aucune actualité enregistrée pour ce concurrent.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
