"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

interface StatsData {
  competitors: number;
  alerts: number;
  reports: number;
  marketScore: number;
  recentAlerts: { id: string; type: string; message: string; createdAt: string }[];
  recentCompetitors: { id: string; name: string; industry: string; threatLevel: string; logo: string; color: string }[];
}

const alertTypeIcons: Record<string, string> = {
  pricing: "💰", feature: "🚀", acquisition: "🤝",
  product: "📦", partnership: "🔗", website: "🌐",
};

const threatColors: Record<string, string> = {
  high: "bg-red-100 text-red-700",
  medium: "bg-amber-100 text-amber-700",
  low: "bg-emerald-100 text-emerald-700",
};

const threatLabels: Record<string, string> = {
  high: "Élevée", medium: "Moyenne", low: "Faible",
};

function StatSkeleton() {
  return <div className="bg-white rounded-xl border border-slate-200 p-5 animate-pulse h-28" />;
}

function formatRelativeTime(dateStr: string) {
  if (!dateStr) return "Récemment";
  const date = new Date(dateStr);
  if (isNaN(date.getTime())) return "Récemment";
  const diff = Date.now() - date.getTime();
  const days = Math.floor(diff / 86400000);
  if (days === 0) return "Aujourd'hui";
  if (days === 1) return "Hier";
  return `Il y a ${days} jours`;
}

export default function DashboardPage() {
  const [stats, setStats] = useState<StatsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/stats")
      .then((r) => r.json())
      .then((d: StatsData) => { setStats(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const statCards = stats ? [
    { label: "Concurrents suivis", value: stats.competitors, icon: "🏢", color: "bg-indigo-50 text-indigo-600", href: "/dashboard/competitors" },
    { label: "Alertes actives", value: stats.alerts, icon: "🔔", color: "bg-amber-50 text-amber-600", href: "/dashboard/alerts" },
    { label: "Rapports générés", value: stats.reports, icon: "📊", color: "bg-emerald-50 text-emerald-600", href: "/dashboard/reports" },
    { label: "Score de marché", value: `${stats.marketScore}%`, icon: "📈", color: "bg-rose-50 text-rose-600", href: "/dashboard/compare" },
  ] : [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Tableau de bord</h2>
          <p className="text-slate-500 text-sm mt-1">Vue d&apos;ensemble de votre veille concurrentielle</p>
        </div>
        <span className="text-xs text-slate-400 hidden sm:block">
          Mis à jour à {new Date().toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" })}
        </span>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {loading
          ? [...Array(4)].map((_, i) => <StatSkeleton key={i} />)
          : statCards.map((s) => (
            <Link
              key={s.label}
              href={s.href}
              className="bg-white rounded-xl border border-slate-200 p-5 hover:border-indigo-300 hover:shadow-md transition-all group"
            >
              <div className={`w-10 h-10 rounded-lg ${s.color} flex items-center justify-center text-lg mb-3 group-hover:scale-110 transition-transform`}>
                {s.icon}
              </div>
              <p className="text-2xl font-bold text-slate-900">{s.value}</p>
              <p className="text-xs text-slate-500 mt-0.5">{s.label}</p>
            </Link>
          ))
        }
      </div>

      {/* Quick actions */}
      <div className="bg-gradient-to-r from-indigo-600 to-indigo-700 rounded-xl p-5 text-white">
        <h3 className="font-semibold mb-3 text-indigo-100 text-sm uppercase tracking-wide">Actions rapides</h3>
        <div className="flex flex-wrap gap-3">
          {[
            { href: "/dashboard/competitors", label: "+ Ajouter un concurrent", primary: true },
            { href: "/dashboard/reports", label: "✦ Générer un rapport", primary: false },
            { href: "/dashboard/compare", label: "⚡ Comparer", primary: false },
          ].map((a) => (
            <Link
              key={a.label}
              href={a.href}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                a.primary
                  ? "bg-white text-indigo-700 hover:bg-indigo-50"
                  : "bg-white/10 text-white hover:bg-white/20 border border-white/20"
              }`}
            >
              {a.label}
            </Link>
          ))}
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Competitors */}
        <div className="bg-white rounded-xl border border-slate-200">
          <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
            <h3 className="font-semibold text-slate-900">Concurrents</h3>
            <Link href="/dashboard/competitors" className="text-xs text-indigo-600 hover:underline font-medium">
              Voir tout →
            </Link>
          </div>
          <div className="divide-y divide-slate-100">
            {loading
              ? [...Array(3)].map((_, i) => (
                <div key={i} className="flex items-center gap-3 px-5 py-3.5 animate-pulse">
                  <div className="w-8 h-8 rounded-lg bg-slate-100 flex-shrink-0" />
                  <div className="flex-1"><div className="h-3 w-24 bg-slate-100 rounded mb-1" /><div className="h-2.5 w-16 bg-slate-100 rounded" /></div>
                </div>
              ))
              : stats?.recentCompetitors.map((c) => (
                <Link
                  key={c.id}
                  href={`/dashboard/competitors/${c.id}`}
                  className="flex items-center gap-3 px-5 py-3.5 hover:bg-slate-50 transition-colors"
                >
                  <div
                    className="w-8 h-8 rounded-lg flex items-center justify-center text-white text-xs font-bold flex-shrink-0"
                    style={{ backgroundColor: c.color }}
                  >
                    {c.logo}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-slate-900">{c.name}</p>
                    <p className="text-xs text-slate-400">{c.industry}</p>
                  </div>
                  <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${threatColors[c.threatLevel]}`}>
                    {threatLabels[c.threatLevel]}
                  </span>
                </Link>
              ))
            }
          </div>
        </div>

        {/* Recent alerts */}
        <div className="bg-white rounded-xl border border-slate-200">
          <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
            <h3 className="font-semibold text-slate-900">Alertes non lues</h3>
            <Link href="/dashboard/alerts" className="text-xs text-indigo-600 hover:underline font-medium">
              Voir tout →
            </Link>
          </div>
          <div className="divide-y divide-slate-100">
            {loading
              ? [...Array(3)].map((_, i) => (
                <div key={i} className="px-5 py-4 animate-pulse">
                  <div className="flex gap-3"><div className="w-6 h-6 rounded bg-slate-100" /><div className="flex-1"><div className="h-3 w-full bg-slate-100 rounded mb-1.5" /><div className="h-2.5 w-24 bg-slate-100 rounded" /></div></div>
                </div>
              ))
              : stats?.recentAlerts.length === 0
              ? <p className="px-5 py-8 text-center text-slate-400 text-sm">Aucune alerte non lue 🎉</p>
              : stats?.recentAlerts.map((a) => (
                <div key={a.id} className="px-5 py-4">
                  <div className="flex items-start gap-3">
                    <span className="text-lg flex-shrink-0">{alertTypeIcons[a.type] || "📌"}</span>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-slate-800 leading-snug">{a.message}</p>
                      <p className="text-xs text-slate-400 mt-1">{formatRelativeTime(a.createdAt)}</p>
                    </div>
                    <span className="w-2 h-2 rounded-full bg-indigo-500 flex-shrink-0 mt-1.5" />
                  </div>
                </div>
              ))
            }
          </div>
        </div>
      </div>

      {/* Market share */}
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold text-slate-900">Parts de marché estimées (secteur CRM)</h3>
          <Link href="/dashboard/compare" className="text-xs text-indigo-600 hover:underline font-medium">
            Analyse complète →
          </Link>
        </div>
        {loading
          ? <div className="space-y-3">{[...Array(5)].map((_, i) => <div key={i} className="h-5 bg-slate-100 rounded animate-pulse" />)}</div>
          : <div className="space-y-3">
              {(stats?.recentCompetitors ?? []).map((c) => {
                const marketShares: Record<string, number> = { SF: 23.8, HS: 8.4, PD: 3.1, ZO: 4.2, MN: 2.9 };
                const share = marketShares[c.logo] ?? 2;
                return (
                  <div key={c.id} className="flex items-center gap-3">
                    <Link href={`/dashboard/competitors/${c.id}`} className="text-sm text-slate-600 w-28 truncate hover:text-indigo-600 transition-colors">
                      {c.name}
                    </Link>
                    <div className="flex-1 bg-slate-100 rounded-full h-2.5 overflow-hidden">
                      <div className="h-2.5 rounded-full transition-all" style={{ width: `${(share / 30) * 100}%`, backgroundColor: c.color }} />
                    </div>
                    <span className="text-sm font-medium text-slate-700 w-12 text-right">{share}%</span>
                  </div>
                );
              })}
            </div>
        }
      </div>
    </div>
  );
}
