"use client";

import { notFound, useRouter } from "next/navigation";
import Link from "next/link";
import { use, useState } from "react";
import { competitors } from "@/lib/data";
import { useToast } from "@/components/Toast";

type ThreatLevel = "high" | "medium" | "low";

const newsTypeColors: Record<string, string> = {
  product: "bg-indigo-100 text-indigo-700",
  pricing: "bg-amber-100 text-amber-700",
  acquisition: "bg-rose-100 text-rose-700",
  partnership: "bg-emerald-100 text-emerald-700",
};

const newsTypeLabels: Record<string, string> = {
  product: "Produit", pricing: "Tarifs", acquisition: "Acquisition", partnership: "Partenariat",
};

const threatLabels: Record<ThreatLevel, string> = { high: "Élevée", medium: "Moyenne", low: "Faible" };
const threatColors: Record<ThreatLevel, string> = {
  high: "bg-red-100 text-red-700", medium: "bg-amber-100 text-amber-700", low: "bg-emerald-100 text-emerald-700",
};

export default function CompetitorDetailPage(props: PageProps<"/dashboard/competitors/[id]">) {
  const { id } = use(props.params);
  const router = useRouter();
  const { toast } = useToast();
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

  const maxPrice = Math.max(...competitor.priceHistory);

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

  const threatLevel = competitor.threatLevel as ThreatLevel;

  return (
    <div className="space-y-6">
      {/* Header bar */}
      <div className="flex items-center justify-between flex-wrap gap-2">
        <Link href="/dashboard/competitors" className="text-sm text-slate-500 hover:text-slate-900 flex items-center gap-1 transition-colors">
          ← Retour aux concurrents
        </Link>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowEdit(true)}
            className="text-sm text-indigo-600 border border-indigo-200 hover:border-indigo-400 hover:bg-indigo-50 px-3 py-1.5 rounded-lg transition-colors"
          >
            Modifier
          </button>
          <button
            onClick={() => setShowConfirm(true)}
            className="text-sm text-red-500 hover:text-red-700 border border-red-200 hover:border-red-400 hover:bg-red-50 px-3 py-1.5 rounded-lg transition-colors"
          >
            Supprimer
          </button>
        </div>
      </div>

      {/* Edit modal */}
      {showEdit && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl w-full max-w-md">
            <div className="px-6 py-5 border-b border-slate-100 flex items-center justify-between">
              <h3 className="font-semibold text-slate-900">Modifier {competitor.name}</h3>
              <button onClick={() => setShowEdit(false)} className="text-slate-400 hover:text-slate-600 text-xl leading-none transition-colors">×</button>
            </div>
            <form onSubmit={handleEdit} className="p-6 space-y-4">
              {[
                { label: "Nom", key: "name" as const, type: "text", required: true },
                { label: "Site web", key: "website" as const, type: "text", required: true },
                { label: "Secteur", key: "industry" as const, type: "text", required: false },
              ].map((f) => (
                <div key={f.key}>
                  <label className="block text-xs font-medium text-slate-600 mb-1">
                    {f.label}{f.required && <span className="text-red-500 ml-0.5">*</span>}
                  </label>
                  <input
                    type={f.type}
                    value={editForm[f.key]}
                    onChange={(e) => setEditForm((prev) => ({ ...prev, [f.key]: e.target.value }))}
                    required={f.required}
                    className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              ))}
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Description</label>
                <textarea
                  value={editForm.description}
                  onChange={(e) => setEditForm((prev) => ({ ...prev, description: e.target.value }))}
                  rows={2}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Niveau de menace</label>
                <select
                  value={editForm.threatLevel}
                  onChange={(e) => setEditForm((prev) => ({ ...prev, threatLevel: e.target.value as ThreatLevel }))}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="low">Faible</option>
                  <option value="medium">Moyenne</option>
                  <option value="high">Élevée</option>
                </select>
              </div>
              <div className="flex gap-3 pt-1">
                <button type="submit" disabled={saving} className="flex-1 bg-indigo-600 text-white py-2.5 rounded-lg text-sm font-semibold hover:bg-indigo-700 disabled:opacity-60 flex items-center justify-center gap-2 transition-colors">
                  {saving && <span className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />}
                  {saving ? "Sauvegarde..." : "Sauvegarder"}
                </button>
                <button type="button" onClick={() => setShowEdit(false)} className="flex-1 border border-slate-200 text-slate-600 py-2.5 rounded-lg text-sm font-semibold hover:bg-slate-50 transition-colors">
                  Annuler
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete confirmation */}
      {showConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl w-full max-w-sm p-6 text-center">
            <div className="text-4xl mb-4">⚠️</div>
            <h3 className="font-semibold text-slate-900 mb-2">Supprimer {competitor.name} ?</h3>
            <p className="text-sm text-slate-500 mb-6">
              Cette action est irréversible. Toutes les données associées seront supprimées.
            </p>
            <div className="flex gap-3">
              <button onClick={handleDelete} disabled={deleting} className="flex-1 bg-red-600 text-white py-2.5 rounded-lg text-sm font-semibold hover:bg-red-700 disabled:opacity-60 flex items-center justify-center gap-2 transition-colors">
                {deleting && <span className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />}
                {deleting ? "Suppression..." : "Supprimer"}
              </button>
              <button onClick={() => setShowConfirm(false)} disabled={deleting} className="flex-1 border border-slate-200 text-slate-600 py-2.5 rounded-lg text-sm font-semibold hover:bg-slate-50 transition-colors">
                Annuler
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Header card */}
      <div className="bg-white rounded-xl border border-slate-200 p-6">
        <div className="flex items-start gap-4">
          <div
            className="w-16 h-16 rounded-2xl flex items-center justify-center text-white text-xl font-bold flex-shrink-0"
            style={{ backgroundColor: competitor.color }}
          >
            {competitor.logo}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-3 flex-wrap">
              <h2 className="text-2xl font-bold text-slate-900">{competitor.name}</h2>
              <span className={`text-xs font-medium px-2.5 py-1 rounded-full ${threatColors[threatLevel]}`}>
                Menace {threatLabels[threatLevel]}
              </span>
              <a href={`https://${competitor.website}`} className="text-sm text-indigo-600 hover:underline" target="_blank" rel="noopener noreferrer">
                {competitor.website} ↗
              </a>
            </div>
            <p className="text-slate-500 mt-1.5 text-sm leading-relaxed">{competitor.description}</p>
            <div className="flex flex-wrap gap-x-6 gap-y-1 mt-3">
              {[
                { label: "Fondé en", value: competitor.founded },
                { label: "Employés", value: competitor.employees },
                { label: "Revenue", value: competitor.revenue },
                { label: "Part de marché", value: `${competitor.marketShare}%` },
              ].map((d) => (
                <span key={d.label} className="text-xs text-slate-500">
                  <span className="font-medium text-slate-700">{d.label}</span> {d.value}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Features */}
        <div className="bg-white rounded-xl border border-slate-200 p-5">
          <h3 className="font-semibold text-slate-900 mb-4">Fonctionnalités</h3>
          <div className="divide-y divide-slate-50">
            {competitor.features.map((f) => (
              <div key={f.name} className="flex items-center justify-between py-2.5">
                <div className="flex items-center gap-2">
                  <span className={`text-base ${f.available ? "text-emerald-500" : "text-slate-300"}`}>
                    {f.available ? "✓" : "✗"}
                  </span>
                  <span className="text-sm text-slate-700">{f.name}</span>
                </div>
                {f.available && (
                  <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                    f.quality === "Excellent" ? "bg-emerald-100 text-emerald-700" :
                    f.quality === "Bien" ? "bg-indigo-100 text-indigo-700" :
                    "bg-slate-100 text-slate-600"
                  }`}>
                    {f.quality}
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Price history */}
        <div className="bg-white rounded-xl border border-slate-200 p-5">
          <h3 className="font-semibold text-slate-900 mb-4">Évolution du prix — 12 mois</h3>
          <div className="flex items-end gap-1.5 h-36 mb-2">
            {competitor.priceHistory.map((price, i) => {
              const minPrice = Math.min(...competitor.priceHistory);
              const range = maxPrice - minPrice || 1;
              const height = Math.max(10, Math.round(((price - minPrice) / range) * 80) + 20);
              const months = ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun", "Jul", "Aoû", "Sep", "Oct", "Nov", "Déc"];
              const isLast = i === competitor.priceHistory.length - 1;
              return (
                <div key={i} className="flex-1 flex flex-col items-center gap-1 group relative">
                  <div
                    className="w-full rounded-t transition-all"
                    style={{ height: `${height}%`, backgroundColor: competitor.color, opacity: isLast ? 1 : 0.35 + (i / 11) * 0.55 }}
                  />
                  <span className="text-[9px] text-slate-400 hidden sm:block">{months[i]}</span>
                  <div className="absolute -top-7 left-1/2 -translate-x-1/2 bg-slate-800 text-white text-[10px] px-1.5 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
                    {price}€
                  </div>
                </div>
              );
            })}
          </div>
          <div className="flex items-center justify-between text-xs text-slate-400 mt-1">
            <span>Min: {Math.min(...competitor.priceHistory)}€</span>
            <span>Actuel: <span className="font-semibold text-slate-700">{competitor.priceHistory[competitor.priceHistory.length - 1]}€/mois</span></span>
            <span>Max: {maxPrice}€</span>
          </div>
        </div>
      </div>

      {/* Pricing plans */}
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <h3 className="font-semibold text-slate-900 mb-4">Plans tarifaires</h3>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {competitor.pricing.map((plan, i) => (
            <div key={plan.name} className={`border rounded-xl p-4 ${i === 1 ? "border-indigo-300 ring-1 ring-indigo-200" : "border-slate-200"} hover:shadow-sm transition-shadow`}>
              {i === 1 && <div className="text-xs text-indigo-600 font-semibold mb-2">Populaire</div>}
              <h4 className="font-semibold text-slate-800 text-sm mb-1">{plan.name}</h4>
              <div className="flex items-baseline gap-0.5 mb-3">
                {plan.price === 0
                  ? <span className="text-xl font-bold text-emerald-600">Gratuit</span>
                  : <><span className="text-2xl font-bold text-slate-900">{plan.price}</span><span className="text-sm text-slate-400">{plan.currency}/{plan.interval}</span></>
                }
              </div>
              <ul className="space-y-1.5">
                {plan.features.map((f) => (
                  <li key={f} className="text-xs text-slate-500 flex items-center gap-1.5">
                    <span className="text-emerald-500">✓</span> {f}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      {/* News */}
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <h3 className="font-semibold text-slate-900 mb-4">Actualités récentes</h3>
        <div className="divide-y divide-slate-50">
          {competitor.news.map((n, i) => (
            <div key={i} className="flex items-start gap-3 py-3">
              <span className={`text-xs font-medium px-2 py-0.5 rounded-full flex-shrink-0 mt-0.5 ${newsTypeColors[n.type] || "bg-slate-100 text-slate-600"}`}>
                {newsTypeLabels[n.type] || n.type}
              </span>
              <p className="text-sm text-slate-700 flex-1 leading-relaxed">{n.title}</p>
              <span className="text-xs text-slate-400 flex-shrink-0 whitespace-nowrap">{n.date}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
