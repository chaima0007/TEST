"use client";

import Link from "next/link";
import { useState } from "react";
import { competitors, alerts, stats as globalStats } from "@/lib/data";

// ─── Helpers ────────────────────────────────────────────────────────────────

function formatRelative(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime();
  const d = Math.floor(diff / 86_400_000);
  if (d === 0) return "Aujourd'hui";
  if (d === 1) return "Hier";
  if (d < 7) return `il y a ${d}j`;
  if (d < 30) return `il y a ${Math.floor(d / 7)} sem.`;
  return `il y a ${Math.floor(d / 30)} mois`;
}

// ─── KPI: Arc Gauge (semicircle) ────────────────────────────────────────────

function ArcGauge({ value, max = 100 }: { value: number; max?: number }) {
  const pct = value / max;
  // SVG semicircle: cx=40, cy=40, r=30 → circumference = π * r = ~94.25
  const r = 30;
  const circ = Math.PI * r; // half circumference for semicircle
  const dash = pct * circ;
  return (
    <svg width="56" height="32" viewBox="0 0 80 44" fill="none">
      {/* Track */}
      <path
        d="M10 40 A30 30 0 0 1 70 40"
        stroke="#E2E8F0"
        strokeWidth="7"
        strokeLinecap="round"
        fill="none"
      />
      {/* Fill */}
      <path
        d="M10 40 A30 30 0 0 1 70 40"
        stroke="#4F46E5"
        strokeWidth="7"
        strokeLinecap="round"
        strokeDasharray={`${dash} ${circ}`}
        fill="none"
      />
      <text x="40" y="38" textAnchor="middle" fontSize="13" fontWeight="700" fill="#1E293B">
        {value}
      </text>
    </svg>
  );
}

// ─── KPI: Sparkline ─────────────────────────────────────────────────────────

function Sparkline({ data, color = "#4F46E5" }: { data: number[]; color?: string }) {
  const w = 56;
  const h = 20;
  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;
  const pts = data.map((v, i) => {
    const x = (i / (data.length - 1)) * w;
    const y = h - ((v - min) / range) * h;
    return `${x},${y}`;
  });
  return (
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} fill="none">
      <polyline points={pts.join(" ")} stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      {data.map((v, i) => {
        const x = (i / (data.length - 1)) * w;
        const y = h - ((v - min) / range) * h;
        return <circle key={i} cx={x} cy={y} r="2.5" fill={color} />;
      })}
    </svg>
  );
}

// ─── Donut Chart (pure SVG) ──────────────────────────────────────────────────

interface DonutSegment {
  label: string;
  pct: number;
  color: string;
}

function DonutChart({ segments, center }: { segments: DonutSegment[]; center: string }) {
  const r = 54;
  const cx = 70;
  const cy = 70;
  const circ = 2 * Math.PI * r;
  let cumPct = 0;

  return (
    <div className="flex flex-col items-center gap-4">
      <svg width="140" height="140" viewBox="0 0 140 140">
        {/* Background ring */}
        <circle cx={cx} cy={cy} r={r} fill="none" stroke="#F1F5F9" strokeWidth="18" />
        {segments.map((seg, i) => {
          const offset = circ * (1 - cumPct);
          const dash = circ * seg.pct;
          const gap = circ - dash;
          const el = (
            <circle
              key={i}
              cx={cx}
              cy={cy}
              r={r}
              fill="none"
              stroke={seg.color}
              strokeWidth="18"
              strokeDasharray={`${dash} ${gap}`}
              strokeDashoffset={offset}
              strokeLinecap="butt"
              style={{ transform: "rotate(-90deg)", transformOrigin: `${cx}px ${cy}px` }}
            />
          );
          cumPct += seg.pct;
          return el;
        })}
        {/* Center label */}
        <text x={cx} y={cy - 6} textAnchor="middle" fontSize="26" fontWeight="800" fill="#1E293B">
          {center}
        </text>
        <text x={cx} y={cy + 14} textAnchor="middle" fontSize="12" fill="#94A3B8">
          /100
        </text>
      </svg>

      {/* Legend */}
      <div className="flex flex-col gap-1.5 w-full">
        {segments.map((seg) => (
          <div key={seg.label} className="flex items-center justify-between text-[12px]">
            <span className="flex items-center gap-1.5 text-slate-600">
              <span className="w-2.5 h-2.5 rounded-full inline-block flex-shrink-0" style={{ backgroundColor: seg.color }} />
              {seg.label}
            </span>
            <span className="font-semibold text-slate-800">{Math.round(seg.pct * 100)}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Threat level config ─────────────────────────────────────────────────────

const threatConfig: Record<string, { label: string; bg: string; text: string; border: string; bar: string }> = {
  high:   { label: "Élevée",  bg: "bg-red-50",    text: "text-red-700",    border: "border-red-200",   bar: "bg-red-500"   },
  medium: { label: "Moyenne", bg: "bg-amber-50",  text: "text-amber-700",  border: "border-amber-200", bar: "bg-amber-500" },
  low:    { label: "Faible",  bg: "bg-green-50",  text: "text-green-700",  border: "border-green-200", bar: "bg-green-500" },
};

// ─── Alert type icons ────────────────────────────────────────────────────────

const alertIcon: Record<string, string> = {
  pricing: "💰",
  feature: "⚡",
  acquisition: "🏢",
  partnership: "🤝",
  product: "🚀",
};

const alertDot: Record<string, string> = {
  pricing: "bg-amber-400",
  feature: "bg-indigo-500",
  acquisition: "bg-rose-500",
  partnership: "bg-sky-500",
  product: "bg-violet-500",
};

// ─── Sorted competitors (high → medium → low) ────────────────────────────────

const threatOrder: Record<string, number> = { high: 0, medium: 1, low: 2 };
const sortedCompetitors = [...competitors].sort(
  (a, b) => threatOrder[a.threatLevel] - threatOrder[b.threatLevel]
);

// ─── Main Component ──────────────────────────────────────────────────────────

export default function DashboardPage() {
  const [bannerDismissed, setBannerDismissed] = useState(false);

  const sparklineData = [2, 3, 3, 4, 4, 5, 5];

  const donutSegments: DonutSegment[] = [
    { label: "Veille",   pct: 0.35, color: "#4F46E5" },
    { label: "Analyse",  pct: 0.25, color: "#7C3AED" },
    { label: "Réponse",  pct: 0.14, color: "#059669" },
  ];

  return (
    <div className="space-y-5 pb-10 bg-slate-50 min-h-screen">

      {/* ─── Page header ─── */}
      <div className="flex items-center justify-between pt-1 pb-1">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Tableau de bord</h1>
          <p className="text-sm text-slate-500 mt-0.5">
            Vue exécutive — Veille concurrentielle en temps réel
          </p>
        </div>
        <span className="hidden sm:flex items-center gap-1.5 text-xs text-slate-400 font-medium bg-white border border-slate-200 rounded-lg px-3 py-1.5 shadow-sm">
          <span className="w-2 h-2 rounded-full bg-green-400 inline-block animate-pulse" />
          Mis à jour à {new Date().toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" })}
        </span>
      </div>

      {/* ─── KPI BANNER ─── */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 overflow-x-auto">

        {/* Score Marché */}
        <div className="bg-white rounded-xl shadow-sm border-l-4 border-indigo-600 p-4 hover:shadow-lg transition-shadow duration-200 flex flex-col gap-2">
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Score Marché</p>
          <ArcGauge value={globalStats.marketScore} />
          <p className="text-xs text-slate-400">sur 100 points</p>
        </div>

        {/* Concurrents surveillés */}
        <div className="bg-white rounded-xl shadow-sm border-l-4 border-blue-500 p-4 hover:shadow-lg transition-shadow duration-200 flex flex-col gap-2">
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Concurrents surveillés</p>
          <p className="text-3xl font-bold text-slate-900">{globalStats.competitorsTracked}</p>
          <Sparkline data={sparklineData} color="#3B82F6" />
        </div>

        {/* Alertes actives */}
        <div className="bg-white rounded-xl shadow-sm border-l-4 border-red-500 p-4 hover:shadow-lg transition-shadow duration-200 flex flex-col gap-2">
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Alertes actives</p>
          <div className="flex items-center gap-2">
            <p className="text-3xl font-bold text-slate-900">{globalStats.activeAlerts}</p>
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500" />
            </span>
          </div>
          <p className="text-xs text-slate-400">non traitées</p>
        </div>

        {/* Rapports générés */}
        <div className="bg-white rounded-xl shadow-sm border-l-4 border-emerald-500 p-4 hover:shadow-lg transition-shadow duration-200 flex flex-col gap-2">
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Rapports générés</p>
          <p className="text-3xl font-bold text-slate-900">{globalStats.reportsGenerated}</p>
          <span className="inline-flex items-center gap-1 text-xs font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full w-fit">
            ↑ +1 ce mois
          </span>
        </div>

        {/* Uptime */}
        <div className="bg-white rounded-xl shadow-sm border-l-4 border-green-400 p-4 hover:shadow-lg transition-shadow duration-200 flex flex-col gap-2">
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Uptime</p>
          <div className="flex items-center gap-2">
            <p className="text-3xl font-bold text-slate-900">{globalStats.slaUptime}%</p>
            <span className="w-2.5 h-2.5 rounded-full bg-green-400 flex-shrink-0" />
          </div>
          <p className="text-xs text-slate-400">SLA garanti</p>
        </div>
      </div>

      {/* ─── MENACE DU MOMENT ─── */}
      {!bannerDismissed && (
        <div className="rounded-xl overflow-hidden" style={{ background: "linear-gradient(135deg, #D97706 0%, #B45309 60%, #92400E 100%)" }}>
          <div className="px-5 py-4 flex items-start sm:items-center justify-between gap-4">
            <div className="flex-1">
              <p className="text-white font-semibold text-sm sm:text-base leading-snug">
                ⚠ Menace prioritaire détectée — Salesforce a augmenté ses prix de 12% ET acquis DataRobot.
                Impact estimé : 3 comptes à risque.
              </p>
            </div>
            <div className="flex items-center gap-3 flex-shrink-0">
              <Link
                href="/dashboard/resolveur"
                className="inline-flex items-center gap-1 bg-white text-amber-800 text-xs font-bold px-3 py-1.5 rounded-lg hover:bg-amber-50 transition-colors whitespace-nowrap"
              >
                Voir le plan de réponse →
              </Link>
              <button
                onClick={() => setBannerDismissed(true)}
                className="text-white/70 hover:text-white transition-colors text-lg leading-none font-light"
                aria-label="Fermer"
              >
                ✕
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ─── MAIN GRID ─── */}
      <div className="grid lg:grid-cols-3 gap-5">

        {/* ─── LEFT COLUMN (2/3) ─── */}
        <div className="lg:col-span-2 flex flex-col gap-5">

          {/* RADAR DE MENACES */}
          <div className="bg-white rounded-xl shadow-sm overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
              <div>
                <h2 className="text-sm font-bold text-slate-900">Radar de menaces</h2>
                <p className="text-xs text-slate-400 mt-0.5">5 concurrents — triés par niveau de menace</p>
              </div>
              <Link href="/dashboard/competitors" className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 transition-colors">
                Voir tout →
              </Link>
            </div>

            {/* Table header */}
            <div className="grid grid-cols-[2fr_1fr_1fr_1fr_auto] gap-3 px-5 py-2 bg-slate-50 border-b border-slate-100 text-xs font-semibold text-slate-400 uppercase tracking-wider">
              <span>Concurrent</span>
              <span className="hidden sm:block">Secteur</span>
              <span>Menace</span>
              <span className="hidden md:block">Part marché</span>
              <span />
            </div>

            <div className="divide-y divide-slate-100">
              {sortedCompetitors.map((c) => {
                const tc = threatConfig[c.threatLevel] ?? threatConfig.low;
                const lastNews = c.news?.[0];
                const marketBarPct = Math.min((c.marketShare / 30) * 100, 100);
                return (
                  <div
                    key={c.id}
                    className="grid grid-cols-[2fr_1fr_1fr_1fr_auto] gap-3 items-center px-5 py-3.5 hover:bg-slate-50 transition-colors group"
                  >
                    {/* Logo + Name + Last event */}
                    <div className="flex items-center gap-3 min-w-0">
                      <div
                        className="w-9 h-9 rounded-xl flex items-center justify-center text-white text-xs font-bold flex-shrink-0 shadow-sm"
                        style={{ backgroundColor: c.color }}
                      >
                        {c.logo}
                      </div>
                      <div className="min-w-0">
                        <p className="text-sm font-semibold text-slate-900 truncate">{c.name}</p>
                        {lastNews && (
                          <p className="text-xs text-slate-400 truncate">
                            {lastNews.title} · {lastNews.date}
                          </p>
                        )}
                      </div>
                    </div>

                    {/* Industry */}
                    <span className="hidden sm:block text-xs text-slate-500 truncate">{c.industry}</span>

                    {/* Threat badge */}
                    <span
                      className={`inline-flex items-center justify-center text-xs font-bold px-2 py-0.5 rounded-full border w-fit ${tc.bg} ${tc.text} ${tc.border}`}
                    >
                      {tc.label}
                    </span>

                    {/* Market share bar */}
                    <div className="hidden md:flex items-center gap-2">
                      <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full ${tc.bar}`}
                          style={{ width: `${marketBarPct}%` }}
                        />
                      </div>
                      <span className="text-xs text-slate-500 w-10 text-right tabular-nums">{c.marketShare}%</span>
                    </div>

                    {/* Analyse link */}
                    <Link
                      href={`/dashboard/competitors/${c.id}`}
                      className="text-xs font-semibold text-indigo-600 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap"
                    >
                      Analyser →
                    </Link>
                  </div>
                );
              })}
            </div>
          </div>

          {/* FIL D'ACTIVITE */}
          <div className="bg-white rounded-xl shadow-sm overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
              <div>
                <h2 className="text-sm font-bold text-slate-900">Fil d&apos;activité</h2>
                <p className="text-xs text-slate-400 mt-0.5">Événements récents détectés par les agents</p>
              </div>
              <Link href="/dashboard/alerts" className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 transition-colors">
                Voir tout →
              </Link>
            </div>

            <div className="px-5 py-4">
              <div className="relative">
                {/* Vertical timeline line */}
                <div className="absolute left-3.5 top-0 bottom-0 w-px bg-slate-100" />

                <div className="space-y-0">
                  {alerts.slice(0, 7).map((alert, idx) => {
                    const icon = alertIcon[alert.type] ?? "📌";
                    const dot = alertDot[alert.type] ?? "bg-slate-400";
                    const isUnread = !alert.isRead;
                    const isLast = idx === Math.min(alerts.length, 7) - 1;
                    return (
                      <div
                        key={alert.id}
                        className={`relative flex gap-4 ${!isLast ? "pb-5" : "pb-1"} ${isUnread ? "pl-0" : ""}`}
                      >
                        {/* Unread left accent */}
                        {isUnread && (
                          <div className="absolute left-0 top-0 bottom-0 w-0.5 bg-indigo-500 rounded-full" style={{ left: "-20px" }} />
                        )}

                        {/* Dot */}
                        <div className="relative z-10 flex-shrink-0 mt-0.5">
                          <div className={`w-7 h-7 rounded-full ${dot} flex items-center justify-center text-sm shadow-sm`}>
                            {icon}
                          </div>
                        </div>

                        {/* Content */}
                        <div className={`flex-1 rounded-lg p-3 ${isUnread ? "bg-indigo-50 border border-indigo-100" : "bg-slate-50"}`}>
                          <div className="flex items-start justify-between gap-2">
                            <p className="text-sm text-slate-800 font-medium leading-snug">{alert.message}</p>
                            {isUnread && (
                              <span className="flex-shrink-0 w-2 h-2 rounded-full bg-indigo-500 mt-1.5" />
                            )}
                          </div>
                          <div className="flex items-center gap-2 mt-1.5">
                            <span
                              className="inline-flex items-center text-xs font-semibold px-2 py-0.5 rounded-full text-white"
                              style={{ backgroundColor: competitors.find(c => c.id === alert.competitorId || c.name === alert.competitorName)?.color ?? "#94A3B8" }}
                            >
                              {alert.competitorName}
                            </span>
                            <span className="text-xs text-slate-400">{formatRelative(alert.date)}</span>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* ─── RIGHT COLUMN (1/3) ─── */}
        <div className="flex flex-col gap-5">

          {/* SCORE DE POSITION */}
          <div className="bg-white rounded-xl shadow-sm p-5">
            <h2 className="text-sm font-bold text-slate-900 mb-1">Score de position</h2>
            <p className="text-xs text-slate-400 mb-4">Indice CompeteIQ global</p>
            <DonutChart segments={donutSegments} center="74" />
          </div>

          {/* ACTIONS RECOMMANDEES */}
          <div className="bg-white rounded-xl shadow-sm overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-100">
              <h2 className="text-sm font-bold text-slate-900">Actions recommandées</h2>
              <p className="text-xs text-slate-400 mt-0.5">Priorisées par l&apos;IA</p>
            </div>
            <div className="divide-y divide-slate-100">
              {[
                {
                  priority: 1,
                  color: "bg-red-500",
                  text: "Répondre à la hausse Salesforce",
                  href: "/dashboard/resolveur",
                },
                {
                  priority: 2,
                  color: "bg-amber-500",
                  text: "Analyser Einstein Copilot v3",
                  href: "/dashboard/battlecards",
                },
                {
                  priority: 3,
                  color: "bg-indigo-600",
                  text: "Mettre à jour votre positionnement",
                  href: "/dashboard/plan",
                },
              ].map((action) => (
                <Link
                  key={action.priority}
                  href={action.href}
                  className="flex items-center gap-3 px-5 py-3.5 hover:bg-slate-50 transition-colors group"
                >
                  <span
                    className={`w-6 h-6 rounded-full ${action.color} text-white text-xs font-bold flex items-center justify-center flex-shrink-0`}
                  >
                    {action.priority}
                  </span>
                  <span className="flex-1 text-sm text-slate-700 font-medium group-hover:text-indigo-700 transition-colors leading-snug">
                    {action.text}
                  </span>
                  <span className="text-slate-300 group-hover:text-indigo-500 transition-colors text-base">→</span>
                </Link>
              ))}
            </div>
          </div>

          {/* AGENTS ACTIFS */}
          <div className="bg-white rounded-xl shadow-sm overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-100">
              <h2 className="text-sm font-bold text-slate-900">Agents actifs</h2>
              <p className="text-xs text-slate-400 mt-0.5">Surveillance automatique 24/7</p>
            </div>
            <div className="divide-y divide-slate-100">
              {[
                { name: "SENTINEL", role: "Veille prix",      status: "active"  },
                { name: "ORACLE",   role: "Analyse tendances", status: "active"  },
                { name: "HERMES",   role: "Suivi actualités",  status: "active"  },
                { name: "NEXUS",    role: "Cartographie réseau", status: "idle"  },
                { name: "FORGE",    role: "Génération rapports", status: "idle"  },
              ].map((agent) => (
                <div key={agent.name} className="flex items-center justify-between px-5 py-2.5">
                  <div className="flex items-center gap-2.5">
                    <span className="relative flex h-2 w-2 flex-shrink-0">
                      {agent.status === "active" ? (
                        <>
                          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75" />
                          <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500" />
                        </>
                      ) : (
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-amber-400" />
                      )}
                    </span>
                    <div>
                      <span className="text-xs font-bold text-slate-700 tracking-wide">{agent.name}</span>
                      <p className="text-xs text-slate-400">{agent.role}</p>
                    </div>
                  </div>
                  <span
                    className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
                      agent.status === "active"
                        ? "bg-green-50 text-green-700"
                        : "bg-amber-50 text-amber-700"
                    }`}
                  >
                    {agent.status === "active" ? "Actif" : "En veille"}
                  </span>
                </div>
              ))}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
