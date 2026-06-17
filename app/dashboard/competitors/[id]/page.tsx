"use client";

import { notFound, useRouter } from "next/navigation";
import Link from "next/link";
import { use, useState } from "react";
import { competitors } from "@/lib/data";

const newsTypeColors: Record<string, string> = {
  product: "bg-indigo-100 text-indigo-700",
  pricing: "bg-amber-100 text-amber-700",
  acquisition: "bg-rose-100 text-rose-700",
  partnership: "bg-emerald-100 text-emerald-700",
};

const newsTypeLabels: Record<string, string> = {
  product: "Produit",
  pricing: "Tarifs",
  acquisition: "Acquisition",
  partnership: "Partenariat",
};

export default function CompetitorDetailPage(props: PageProps<"/dashboard/competitors/[id]">) {
  const { id } = use(props.params);
  const router = useRouter();
  const [deleting, setDeleting] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const competitor = competitors.find((c) => c.id === id);
  if (!competitor) notFound();

  const maxPrice = Math.max(...competitor.priceHistory);

  const handleDelete = async () => {
    setDeleting(true);
    try {
      const res = await fetch(`/api/competitors/${id}`, { method: "DELETE" });
      if (res.ok) {
        router.push("/dashboard/competitors");
        router.refresh();
      }
    } catch {
      setDeleting(false);
      setShowConfirm(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Back */}
      <div className="flex items-center justify-between">
        <Link href="/dashboard/competitors" className="text-sm text-slate-500 hover:text-slate-900 flex items-center gap-1 transition-colors">
          ← Retour aux concurrents
        </Link>
        <button
          onClick={() => setShowConfirm(true)}
          className="text-sm text-red-500 hover:text-red-700 border border-red-200 hover:border-red-400 px-3 py-1.5 rounded-lg transition-colors"
        >
          Supprimer
        </button>
      </div>

      {/* Delete confirmation modal */}
      {showConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl w-full max-w-sm p-6 text-center">
            <div className="text-4xl mb-4">⚠️</div>
            <h3 className="font-semibold text-slate-900 mb-2">Supprimer {competitor.name} ?</h3>
            <p className="text-sm text-slate-500 mb-6">
              Cette action est irréversible. Toutes les données associées seront supprimées.
            </p>
            <div className="flex gap-3">
              <button
                onClick={handleDelete}
                disabled={deleting}
                className="flex-1 bg-red-600 text-white py-2.5 rounded-lg text-sm font-semibold hover:bg-red-700 transition-colors disabled:opacity-60 flex items-center justify-center gap-2"
              >
                {deleting && (
                  <span className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                )}
                {deleting ? "Suppression..." : "Supprimer"}
              </button>
              <button
                onClick={() => setShowConfirm(false)}
                disabled={deleting}
                className="flex-1 border border-slate-200 text-slate-600 py-2.5 rounded-lg text-sm font-semibold hover:bg-slate-50 transition-colors"
              >
                Annuler
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-6">
        <div className="flex items-start gap-4">
          <div
            className="w-16 h-16 rounded-2xl flex items-center justify-center text-white text-xl font-bold flex-shrink-0"
            style={{ backgroundColor: competitor.color }}
          >
            {competitor.logo}
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-3 flex-wrap">
              <h2 className="text-2xl font-bold text-slate-900">{competitor.name}</h2>
              <a
                href={`https://${competitor.website}`}
                className="text-sm text-indigo-600 hover:underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                {competitor.website} ↗
              </a>
            </div>
            <p className="text-slate-500 mt-1 text-sm">{competitor.description}</p>
            <div className="flex flex-wrap gap-4 mt-4">
              <span className="text-xs text-slate-500"><span className="font-medium text-slate-700">Fondé en</span> {competitor.founded}</span>
              <span className="text-xs text-slate-500"><span className="font-medium text-slate-700">Employés</span> {competitor.employees}</span>
              <span className="text-xs text-slate-500"><span className="font-medium text-slate-700">Revenue</span> {competitor.revenue}</span>
              <span className="text-xs text-slate-500"><span className="font-medium text-slate-700">Part de marché</span> {competitor.marketShare}%</span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Features */}
        <div className="bg-white rounded-xl border border-slate-200 p-5">
          <h3 className="font-semibold text-slate-900 mb-4">Fonctionnalités</h3>
          <div className="space-y-3">
            {competitor.features.map((f) => (
              <div key={f.name} className="flex items-center justify-between py-2 border-b border-slate-50 last:border-0">
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

        {/* Price history chart */}
        <div className="bg-white rounded-xl border border-slate-200 p-5">
          <h3 className="font-semibold text-slate-900 mb-4">Évolution du prix (plan de base, 12 mois)</h3>
          <div className="flex items-end gap-1.5 h-40">
            {competitor.priceHistory.map((price, i) => {
              const height = Math.round((price / maxPrice) * 100);
              const months = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"];
              return (
                <div key={i} className="flex-1 flex flex-col items-center gap-1">
                  <span className="text-[9px] text-slate-400">{price}€</span>
                  <div
                    className="w-full rounded-t-sm transition-all"
                    style={{ height: `${height}%`, backgroundColor: competitor.color, opacity: i === 11 ? 1 : 0.5 + (i / 11) * 0.5 }}
                  ></div>
                  <span className="text-[9px] text-slate-400">{months[i]}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Pricing plans */}
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <h3 className="font-semibold text-slate-900 mb-4">Plans tarifaires actuels</h3>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {competitor.pricing.map((plan) => (
            <div key={plan.name} className="border border-slate-200 rounded-xl p-4 hover:border-indigo-300 transition-colors">
              <h4 className="font-semibold text-slate-800 text-sm mb-1">{plan.name}</h4>
              <div className="flex items-baseline gap-0.5 mb-3">
                <span className="text-2xl font-bold text-slate-900">{plan.price}</span>
                <span className="text-sm text-slate-400">{plan.currency}/{plan.interval}</span>
              </div>
              <ul className="space-y-1.5">
                {plan.features.map((f) => (
                  <li key={f} className="text-xs text-slate-500 flex items-center gap-1.5">
                    <span className="text-emerald-500 text-xs">✓</span> {f}
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
        <div className="space-y-3">
          {competitor.news.map((n, i) => (
            <div key={i} className="flex items-start gap-3 py-3 border-b border-slate-50 last:border-0">
              <span className={`text-xs font-medium px-2 py-0.5 rounded-full flex-shrink-0 ${newsTypeColors[n.type] || "bg-slate-100 text-slate-600"}`}>
                {newsTypeLabels[n.type] || n.type}
              </span>
              <p className="text-sm text-slate-700 flex-1">{n.title}</p>
              <span className="text-xs text-slate-400 flex-shrink-0">{n.date}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
