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

// SVG Icons
function IconBuilding({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4zm3 1h6v4H7V5zm2 6H7v2h2v-2zm4 0h-2v2h2v-2z" clipRule="evenodd" />
    </svg>
  );
}

function IconBell({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
    </svg>
  );
}

function IconDocument({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
    </svg>
  );
}

function IconTrendingUp({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clipRule="evenodd" />
    </svg>
  );
}

function IconPlus({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
    </svg>
  );
}

function IconSpark({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" />
    </svg>
  );
}

function IconScale({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 14a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 5.477V17a1 1 0 11-2 0V5.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1z" clipRule="evenodd" />
    </svg>
  );
}

function IconArrowRight({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
    </svg>
  );
}

// Stat card config with SVG icon components and trend data
const statCardConfigs = [
  {
    key: "competitors",
    label: "Concurrents suivis",
    href: "/dashboard/competitors",
    Icon: IconBuilding,
    bgClass: "bg-blue-50",
    iconClass: "text-[#0078D4]",
    borderClass: "border-blue-100",
    accentClass: "bg-[#0078D4]",
    trend: { value: "+2 ce mois", direction: "up" },
  },
  {
    key: "alerts",
    label: "Alertes actives",
    href: "/dashboard/alerts",
    Icon: IconBell,
    bgClass: "bg-amber-50",
    iconClass: "text-amber-600",
    borderClass: "border-amber-100",
    accentClass: "bg-amber-500",
    trend: { value: "+3 cette semaine", direction: "up" },
  },
  {
    key: "reports",
    label: "Rapports générés",
    href: "/dashboard/reports",
    Icon: IconDocument,
    bgClass: "bg-[#107C10]/5",
    iconClass: "text-[#107C10]",
    borderClass: "border-green-100",
    accentClass: "bg-[#107C10]",
    trend: { value: "Stable", direction: "neutral" },
  },
  {
    key: "marketScore",
    label: "Score de marché",
    href: "/dashboard/compare",
    Icon: IconTrendingUp,
    bgClass: "bg-rose-50",
    iconClass: "text-rose-600",
    borderClass: "border-rose-100",
    accentClass: "bg-rose-500",
    trend: { value: "-1 ce mois", direction: "down" },
    suffix: "%",
  },
];

// Alert type dot colors and labels
const alertTypeMeta: Record<string, { dot: string; label: string; ring: string }> = {
  pricing: { dot: "bg-amber-400", label: "Pricing", ring: "ring-amber-200" },
  feature: { dot: "bg-indigo-500", label: "Feature", ring: "ring-indigo-200" },
  acquisition: { dot: "bg-rose-500", label: "Acquisition", ring: "ring-rose-200" },
  product: { dot: "bg-violet-500", label: "Produit", ring: "ring-violet-200" },
  partnership: { dot: "bg-sky-500", label: "Partenariat", ring: "ring-sky-200" },
  website: { dot: "bg-slate-400", label: "Site web", ring: "ring-slate-200" },
};

// Threat level config
const threatMeta: Record<string, { label: string; bar: string; text: string; bg: string; width: string }> = {
  high: { label: "Élevée", bar: "bg-[#D83B01]", text: "text-[#D83B01]", bg: "bg-red-50", width: "w-full" },
  medium: { label: "Moyenne", bar: "bg-amber-500", text: "text-amber-700", bg: "bg-amber-50", width: "w-2/3" },
  low: { label: "Faible", bar: "bg-[#107C10]", text: "text-[#107C10]", bg: "bg-green-50", width: "w-1/3" },
};

function StatSkeleton() {
  return (
    <div className="bg-white rounded-lg border border-slate-200 p-5 animate-pulse">
      <div className="flex items-start justify-between mb-4">
        <div className="w-10 h-10 rounded-lg bg-slate-100" />
        <div className="w-16 h-4 rounded bg-slate-100" />
      </div>
      <div className="h-8 w-16 bg-slate-100 rounded mb-1" />
      <div className="h-3 w-24 bg-slate-100 rounded" />
    </div>
  );
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

  const statValues: Record<string, number | string> = stats
    ? {
        competitors: stats.competitors,
        alerts: stats.alerts,
        reports: stats.reports,
        marketScore: stats.marketScore,
      }
    : {};

  return (
    <div className="space-y-6 pb-8">
      {/* Page header */}
      <div className="flex items-center justify-between pt-1">
        <div>
          <h1 className="text-[22px] font-semibold text-slate-900 tracking-tight">Tableau de bord</h1>
          <p className="text-[13px] text-slate-500 mt-0.5">Vue d&apos;ensemble de votre veille concurrentielle</p>
        </div>
        <div className="flex items-center gap-3">
          <span className="hidden sm:flex items-center gap-1.5 text-[11px] text-slate-400 font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-green-400 inline-block" />
            Mis à jour à {new Date().toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" })}
          </span>
        </div>
      </div>

      {/* ─── STAT CARDS ─── */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {loading
          ? [...Array(4)].map((_, i) => <StatSkeleton key={i} />)
          : statCardConfigs.map((cfg) => {
              const raw = statValues[cfg.key];
              const displayVal = cfg.suffix ? `${raw}${cfg.suffix}` : raw;
              const isUp = cfg.trend.direction === "up";
              const isDown = cfg.trend.direction === "down";
              return (
                <Link
                  key={cfg.key}
                  href={cfg.href}
                  className={`group relative bg-white rounded-lg border ${cfg.borderClass} p-5 hover:shadow-[0_2px_12px_rgba(0,0,0,0.08)] hover:border-slate-300 transition-all duration-150 overflow-hidden`}
                >
                  {/* Subtle color bleed top-right */}
                  <div className={`absolute -top-4 -right-4 w-16 h-16 rounded-full ${cfg.bgClass} opacity-60`} />
                  <div className="relative">
                    <div className="flex items-start justify-between mb-3">
                      <div className={`w-10 h-10 rounded-lg ${cfg.bgClass} flex items-center justify-center group-hover:scale-105 transition-transform duration-150`}>
                        <cfg.Icon className={`w-5 h-5 ${cfg.iconClass}`} />
                      </div>
                      {/* Trend badge */}
                      <span
                        className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${
                          isUp
                            ? "bg-green-50 text-[#107C10]"
                            : isDown
                            ? "bg-red-50 text-[#D83B01]"
                            : "bg-slate-50 text-slate-500"
                        }`}
                      >
                        {isUp ? "↑ " : isDown ? "↓ " : ""}{cfg.trend.value}
                      </span>
                    </div>
                    <p className="text-3xl font-bold text-slate-900 tabular-nums leading-none mb-1.5">{displayVal}</p>
                    <p className="text-[12px] text-slate-500 font-medium">{cfg.label}</p>
                    {/* Bottom accent bar */}
                    <div className={`absolute bottom-0 left-0 right-0 h-0.5 ${cfg.accentClass} opacity-0 group-hover:opacity-100 transition-opacity duration-150`} />
                  </div>
                </Link>
              );
            })}
      </div>

      {/* ─── QUICK ACTIONS BAND ─── */}
      <div className="rounded-lg overflow-hidden" style={{ background: "linear-gradient(135deg, #0078D4 0%, #005a9e 60%, #003d6b 100%)" }}>
        <div className="px-5 py-4 flex flex-col sm:flex-row sm:items-center gap-4">
          <div className="flex-1">
            <p className="text-[11px] font-semibold text-blue-200 uppercase tracking-widest mb-0.5">Actions rapides</p>
            <p className="text-white text-[13px] opacity-80">Gérez votre veille en un clic</p>
          </div>
          <div className="flex flex-wrap gap-2.5">
            <Link
              href="/dashboard/competitors"
              className="inline-flex items-center gap-2 bg-white text-[#0078D4] text-[13px] font-semibold px-4 py-2 rounded-md hover:bg-blue-50 transition-colors duration-100 shadow-sm"
            >
              <IconPlus className="w-4 h-4" />
              Ajouter un concurrent
            </Link>
            <Link
              href="/dashboard/reports"
              className="inline-flex items-center gap-2 bg-white/10 border border-white/20 text-white text-[13px] font-medium px-4 py-2 rounded-md hover:bg-white/20 transition-colors duration-100"
            >
              <IconSpark className="w-4 h-4" />
              Générer un rapport
            </Link>
            <Link
              href="/dashboard/compare"
              className="inline-flex items-center gap-2 bg-white/10 border border-white/20 text-white text-[13px] font-medium px-4 py-2 rounded-md hover:bg-white/20 transition-colors duration-100"
            >
              <IconScale className="w-4 h-4" />
              Comparer
            </Link>
          </div>
        </div>
      </div>

      {/* ─── MAIN GRID : COMPETITORS + ACTIVITY ─── */}
      <div className="grid lg:grid-cols-2 gap-5">

        {/* COMPETITORS — Microsoft-style compact table */}
        <div className="bg-white rounded-lg border border-slate-200 overflow-hidden">
          <div className="px-5 py-3.5 border-b border-slate-100 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <IconBuilding className="w-4 h-4 text-[#0078D4]" />
              <h2 className="text-[13px] font-semibold text-slate-900">Concurrents</h2>
            </div>
            <Link href="/dashboard/competitors" className="inline-flex items-center gap-1 text-[12px] text-[#0078D4] font-medium hover:text-blue-700 transition-colors">
              Voir tout <IconArrowRight className="w-3 h-3" />
            </Link>
          </div>

          {/* Table header */}
          <div className="grid grid-cols-[1fr_auto_auto_auto] gap-x-3 px-5 py-2 bg-slate-50 border-b border-slate-100">
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wide">Nom</span>
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wide text-center">Secteur</span>
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wide text-center w-28">Menace</span>
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wide text-right">Action</span>
          </div>

          <div className="divide-y divide-slate-100">
            {loading
              ? [...Array(3)].map((_, i) => (
                  <div key={i} className="grid grid-cols-[1fr_auto_auto_auto] gap-x-3 items-center px-5 py-3.5 animate-pulse">
                    <div className="flex items-center gap-2.5">
                      <div className="w-7 h-7 rounded-md bg-slate-100 flex-shrink-0" />
                      <div><div className="h-3 w-20 bg-slate-100 rounded mb-1" /><div className="h-2.5 w-14 bg-slate-100 rounded" /></div>
                    </div>
                    <div className="h-3 w-16 bg-slate-100 rounded" />
                    <div className="h-3 w-28 bg-slate-100 rounded" />
                    <div className="h-3 w-8 bg-slate-100 rounded" />
                  </div>
                ))
              : stats?.recentCompetitors.map((c) => {
                  const t = threatMeta[c.threatLevel] ?? threatMeta.low;
                  return (
                    <div key={c.id} className="grid grid-cols-[1fr_auto_auto_auto] gap-x-3 items-center px-5 py-3 hover:bg-slate-50/70 transition-colors group">
                      {/* Name col */}
                      <div className="flex items-center gap-2.5 min-w-0">
                        <div
                          className="w-7 h-7 rounded-md flex items-center justify-center text-white text-[10px] font-bold flex-shrink-0 shadow-sm"
                          style={{ backgroundColor: c.color }}
                        >
                          {c.logo}
                        </div>
                        <div className="min-w-0">
                          <p className="text-[13px] font-medium text-slate-900 truncate">{c.name}</p>
                        </div>
                      </div>
                      {/* Sector col */}
                      <span className="text-[11px] text-slate-400 whitespace-nowrap text-center hidden sm:block">{c.industry}</span>
                      {/* Threat col with progress bar */}
                      <div className="w-28 flex items-center gap-2">
                        <div className="flex-1 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                          <div className={`h-full rounded-full ${t.bar} ${t.width}`} />
                        </div>
                        <span className={`text-[11px] font-semibold ${t.text} w-12 text-right`}>{t.label}</span>
                      </div>
                      {/* Action col */}
                      <Link
                        href={`/dashboard/competitors/${c.id}`}
                        className="text-[11px] text-[#0078D4] font-medium opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap"
                      >
                        Voir →
                      </Link>
                    </div>
                  );
                })}
          </div>
        </div>

        {/* RECENT ACTIVITY — Vertical timeline */}
        <div className="bg-white rounded-lg border border-slate-200 overflow-hidden">
          <div className="px-5 py-3.5 border-b border-slate-100 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <IconBell className="w-4 h-4 text-[#0078D4]" />
              <h2 className="text-[13px] font-semibold text-slate-900">Activité récente</h2>
            </div>
            <Link href="/dashboard/alerts" className="inline-flex items-center gap-1 text-[12px] text-[#0078D4] font-medium hover:text-blue-700 transition-colors">
              Voir tout <IconArrowRight className="w-3 h-3" />
            </Link>
          </div>

          <div className="px-5 py-4">
            {loading ? (
              <div className="space-y-5">
                {[...Array(4)].map((_, i) => (
                  <div key={i} className="flex gap-3 animate-pulse">
                    <div className="flex flex-col items-center">
                      <div className="w-3 h-3 rounded-full bg-slate-200 mt-0.5 flex-shrink-0" />
                      {i < 3 && <div className="w-px flex-1 bg-slate-100 mt-1 mb-0" style={{ minHeight: 32 }} />}
                    </div>
                    <div className="pb-4 flex-1">
                      <div className="h-3 w-full bg-slate-100 rounded mb-1.5" />
                      <div className="h-2.5 w-20 bg-slate-100 rounded" />
                    </div>
                  </div>
                ))}
              </div>
            ) : stats?.recentAlerts?.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-8 text-center">
                <div className="w-10 h-10 rounded-full bg-green-50 flex items-center justify-center mb-2">
                  <IconBell className="w-5 h-5 text-[#107C10]" />
                </div>
                <p className="text-[13px] text-slate-500">Aucune alerte non lue</p>
              </div>
            ) : (
              <div className="space-y-0">
                {stats?.recentAlerts.map((a, idx) => {
                  const meta = alertTypeMeta[a.type] ?? alertTypeMeta.product;
                  const isLast = idx === (stats?.recentAlerts.length ?? 0) - 1;
                  return (
                    <div key={a.id} className="flex gap-3.5">
                      {/* Timeline spine */}
                      <div className="flex flex-col items-center flex-shrink-0 w-4">
                        <div className={`w-3 h-3 rounded-full mt-1 flex-shrink-0 ring-2 ${meta.ring} ${meta.dot}`} />
                        {!isLast && <div className="w-px flex-1 bg-slate-100 mt-1" style={{ minHeight: 28 }} />}
                      </div>
                      {/* Content */}
                      <div className={`flex-1 ${!isLast ? "pb-4" : "pb-1"}`}>
                        <div className="flex items-start justify-between gap-2">
                          <p className="text-[13px] text-slate-800 leading-snug">{a.message}</p>
                          <span className="w-2 h-2 rounded-full bg-[#0078D4] flex-shrink-0 mt-1.5" />
                        </div>
                        <div className="flex items-center gap-2 mt-1">
                          <span className="inline-flex items-center gap-1 text-[10px] font-semibold px-1.5 py-0.5 rounded bg-slate-100 text-slate-600">
                            <span className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${meta.dot}`} />
                            {meta.label}
                          </span>
                          <span className="text-[11px] text-slate-400">{formatRelativeTime(a.createdAt)}</span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* ─── PARTS DE MARCHÉ ─── */}
      <div className="bg-white rounded-lg border border-slate-200 p-5">
        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center gap-2">
            <IconTrendingUp className="w-4 h-4 text-[#0078D4]" />
            <h2 className="text-[13px] font-semibold text-slate-900">Parts de marché estimées — Secteur CRM</h2>
          </div>
          <Link href="/dashboard/compare" className="inline-flex items-center gap-1 text-[12px] text-[#0078D4] font-medium hover:text-blue-700 transition-colors">
            Analyse complète <IconArrowRight className="w-3 h-3" />
          </Link>
        </div>

        {loading ? (
          <div className="space-y-4">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="flex items-center gap-3 animate-pulse">
                <div className="h-3 w-24 bg-slate-100 rounded" />
                <div className="flex-1 h-5 bg-slate-100 rounded-full" />
                <div className="h-3 w-10 bg-slate-100 rounded" />
              </div>
            ))}
          </div>
        ) : (
          <div className="space-y-3.5">
            {(stats?.recentCompetitors ?? []).map((c) => {
              const marketShares: Record<string, number> = { SF: 23.8, HS: 8.4, PD: 3.1, ZO: 4.2, MN: 2.9 };
              const share = marketShares[c.logo] ?? 2;
              const barPct = (share / 30) * 100;
              return (
                <div key={c.id} className="flex items-center gap-3 group">
                  {/* Label */}
                  <Link
                    href={`/dashboard/competitors/${c.id}`}
                    className="text-[13px] text-slate-700 w-28 truncate font-medium hover:text-[#0078D4] transition-colors shrink-0"
                  >
                    {c.name}
                  </Link>
                  {/* Bar track */}
                  <div className="flex-1 h-6 bg-slate-100 rounded-md overflow-hidden relative">
                    {/* Gradient fill */}
                    <div
                      className="h-full rounded-md transition-all duration-500 ease-out relative overflow-hidden"
                      style={{
                        width: `${barPct}%`,
                        background: `linear-gradient(90deg, ${c.color}cc 0%, ${c.color} 100%)`,
                      }}
                    >
                      {/* Shimmer stripe */}
                      <div className="absolute inset-0 bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity duration-150" />
                    </div>
                    {/* Inline % label if bar wide enough */}
                    {barPct > 20 && (
                      <span className="absolute left-3 top-1/2 -translate-y-1/2 text-[11px] font-semibold text-white drop-shadow-sm">
                        {share}%
                      </span>
                    )}
                  </div>
                  {/* External value */}
                  <span className="text-[13px] font-semibold text-slate-700 w-10 text-right tabular-nums shrink-0">{share}%</span>
                </div>
              );
            })}
            {/* Legend note */}
            <p className="text-[11px] text-slate-400 mt-2 pt-3 border-t border-slate-100">
              Données estimées — Source : analyses sectorielles Q2 2026
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
