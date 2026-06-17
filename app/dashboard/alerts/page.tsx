"use client";

import { useState, useEffect } from "react";

interface Alert {
  id: string;
  type: string;
  message: string;
  isRead: boolean;
  competitorId: string | null;
  competitorName?: string;
  date: string;
}

const alertTypeIcons: Record<string, string> = {
  pricing: "💰",
  feature: "🚀",
  acquisition: "🤝",
  product: "📦",
  partnership: "🔗",
  website: "🌐",
};

const alertTypeLabels: Record<string, string> = {
  pricing: "Tarifs",
  feature: "Fonctionnalité",
  acquisition: "Acquisition",
  product: "Produit",
  partnership: "Partenariat",
  website: "Site web",
};

const alertTypeColors: Record<string, { badge: string; bar: string; dot: string }> = {
  pricing: { badge: "bg-amber-100 text-amber-700", bar: "bg-amber-400", dot: "bg-amber-400" },
  feature: { badge: "bg-indigo-100 text-indigo-700", bar: "bg-indigo-500", dot: "bg-indigo-500" },
  acquisition: { badge: "bg-rose-100 text-rose-700", bar: "bg-rose-500", dot: "bg-rose-500" },
  product: { badge: "bg-purple-100 text-purple-700", bar: "bg-purple-500", dot: "bg-purple-500" },
  partnership: { badge: "bg-emerald-100 text-emerald-700", bar: "bg-emerald-500", dot: "bg-emerald-500" },
  website: { badge: "bg-slate-100 text-slate-600", bar: "bg-slate-400", dot: "bg-slate-400" },
};

const DEFAULT_COLORS = { badge: "bg-slate-100 text-slate-600", bar: "bg-slate-400", dot: "bg-slate-400" };

const ALL_TYPES = ["pricing", "feature", "acquisition", "product", "partnership", "website"];

function AlertSkeleton() {
  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden animate-pulse flex">
      <div className="w-1 bg-slate-200 flex-shrink-0" />
      <div className="flex-1 p-4">
        <div className="flex items-start gap-3">
          <div className="w-9 h-9 rounded-full bg-slate-100 flex-shrink-0" />
          <div className="flex-1 min-w-0">
            <div className="flex gap-2 mb-2.5">
              <div className="h-5 w-20 bg-slate-100 rounded-full" />
              <div className="h-5 w-16 bg-slate-100 rounded-full" />
            </div>
            <div className="h-4 w-full bg-slate-100 rounded mb-1.5" />
            <div className="h-4 w-3/4 bg-slate-100 rounded mb-2" />
            <div className="h-3 w-36 bg-slate-100 rounded" />
          </div>
          <div className="h-7 w-24 bg-slate-100 rounded-lg flex-shrink-0" />
        </div>
      </div>
    </div>
  );
}

function formatDate(dateStr: string) {
  const date = new Date(dateStr);
  return date.toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" });
}

function EmptyState({ filter, typeFilter }: { filter: string; typeFilter: string }) {
  const messages: Record<string, { title: string; sub: string }> = {
    unread: { title: "Aucune alerte non lue", sub: "Vous êtes à jour — toutes les alertes ont été consultées." },
    read: { title: "Aucune alerte lue", sub: "Les alertes que vous consultez apparaîtront ici." },
    all: { title: "Aucune alerte", sub: "Configurez vos concurrents pour commencer à recevoir des alertes." },
  };
  const msg = typeFilter !== "all"
    ? { title: `Aucune alerte de type "${alertTypeLabels[typeFilter] ?? typeFilter}"`, sub: "Essayez un autre filtre ou attendez de nouvelles détections." }
    : messages[filter] ?? messages.all;

  return (
    <div className="flex flex-col items-center justify-center py-20 px-4">
      <svg className="w-16 h-16 text-slate-200 mb-5" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="8" y="12" width="48" height="36" rx="6" fill="currentColor" />
        <rect x="16" y="20" width="32" height="3" rx="1.5" fill="white" opacity="0.5" />
        <rect x="16" y="27" width="24" height="3" rx="1.5" fill="white" opacity="0.5" />
        <rect x="16" y="34" width="18" height="3" rx="1.5" fill="white" opacity="0.5" />
        <circle cx="48" cy="48" r="10" fill="#E2E8F0" />
        <path d="M44 48h8M48 44v8" stroke="#94A3B8" strokeWidth="2" strokeLinecap="round" />
      </svg>
      <p className="text-base font-semibold text-slate-700 mb-1">{msg.title}</p>
      <p className="text-sm text-slate-400 text-center max-w-xs">{msg.sub}</p>
    </div>
  );
}

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<"all" | "unread" | "read">("all");
  const [typeFilter, setTypeFilter] = useState<string>("all");

  useEffect(() => {
    fetch("/api/alerts")
      .then((r) => r.json())
      .then((data: Alert[]) => {
        setAlerts(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const unreadCount = alerts.filter((a) => !a.isRead).length;
  const readCount = alerts.filter((a) => a.isRead).length;

  const markAllRead = async () => {
    await fetch("/api/alerts", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ markAllRead: true }),
    });
    setAlerts((prev) => prev.map((a) => ({ ...a, isRead: true })));
  };

  const markRead = async (id: string) => {
    await fetch("/api/alerts", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id }),
    });
    setAlerts((prev) => prev.map((a) => (a.id === id ? { ...a, isRead: true } : a)));
  };

  const byReadFilter = alerts.filter((a) =>
    filter === "unread" ? !a.isRead : filter === "read" ? a.isRead : true
  );
  const filtered = byReadFilter.filter((a) => typeFilter === "all" || a.type === typeFilter);

  const countFor = (f: "all" | "unread" | "read") =>
    f === "all" ? alerts.length : f === "unread" ? unreadCount : readCount;

  const typeCountFor = (t: string) =>
    t === "all" ? byReadFilter.length : byReadFilter.filter((a) => a.type === t).length;

  const readTabs: { key: "all" | "unread" | "read"; label: string }[] = [
    { key: "all", label: "Toutes" },
    { key: "unread", label: "Non lues" },
    { key: "read", label: "Lues" },
  ];

  return (
    <div className="space-y-0">
      {/* Header */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <div className="flex items-center gap-3">
            <h2 className="text-2xl font-bold text-slate-900">Alertes</h2>
            {!loading && unreadCount > 0 && (
              <span className="inline-flex items-center justify-center bg-red-500 text-white text-xs font-bold rounded-full min-w-[22px] h-[22px] px-1.5 leading-none">
                {unreadCount}
              </span>
            )}
          </div>
          <p className="text-slate-500 text-sm mt-1">
            {loading
              ? "Chargement des alertes…"
              : `${alerts.length} alerte${alerts.length !== 1 ? "s" : ""} au total`}
          </p>
        </div>
        {!loading && unreadCount > 0 && (
          <button
            onClick={markAllRead}
            className="flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-50 hover:border-slate-300 transition-all shadow-sm"
          >
            <svg className="w-4 h-4 text-slate-500" viewBox="0 0 16 16" fill="none">
              <path d="M2 8l4 4 8-8" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            Tout marquer lu
          </button>
        )}
      </div>

      {/* Read/unread tab bar — Teams style */}
      <div className="flex border-b border-slate-200 mb-4">
        {readTabs.map((t) => (
          <button
            key={t.key}
            onClick={() => { setFilter(t.key); setTypeFilter("all"); }}
            className={`relative flex items-center gap-1.5 px-4 py-2.5 text-sm font-medium transition-colors ${
              filter === t.key
                ? "text-indigo-600"
                : "text-slate-500 hover:text-slate-700"
            }`}
          >
            {t.label}
            {!loading && (
              <span className={`text-xs rounded-full px-1.5 py-0.5 font-medium min-w-[20px] text-center leading-none ${
                filter === t.key ? "bg-indigo-100 text-indigo-600" : "bg-slate-100 text-slate-500"
              }`}>
                {countFor(t.key)}
              </span>
            )}
            {filter === t.key && (
              <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-600 rounded-t-full" />
            )}
          </button>
        ))}
      </div>

      {/* Type filter pills */}
      <div className="flex flex-wrap gap-2 mb-5">
        <button
          onClick={() => setTypeFilter("all")}
          className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all border ${
            typeFilter === "all"
              ? "bg-slate-800 text-white border-slate-800"
              : "bg-white text-slate-600 border-slate-200 hover:border-slate-300 hover:bg-slate-50"
          }`}
        >
          Tous les types
          {!loading && (
            <span className="ml-1.5 opacity-60">{typeCountFor("all")}</span>
          )}
        </button>
        {ALL_TYPES.map((t) => {
          const count = typeCountFor(t);
          if (!loading && count === 0) return null;
          const colors = alertTypeColors[t] ?? DEFAULT_COLORS;
          return (
            <button
              key={t}
              onClick={() => setTypeFilter(t)}
              className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all border ${
                typeFilter === t
                  ? colors.badge + " border-transparent shadow-sm"
                  : "bg-white text-slate-600 border-slate-200 hover:border-slate-300 hover:bg-slate-50"
              }`}
            >
              {alertTypeIcons[t]} {alertTypeLabels[t]}
              {!loading && <span className="ml-1.5 opacity-60">{count}</span>}
            </button>
          );
        })}
      </div>

      {/* Alert list */}
      <div className="space-y-2.5">
        {loading ? (
          <>
            {[...Array(4)].map((_, i) => <AlertSkeleton key={i} />)}
          </>
        ) : filtered.length === 0 ? (
          <EmptyState filter={filter} typeFilter={typeFilter} />
        ) : (
          filtered.map((alert) => {
            const colors = alertTypeColors[alert.type] ?? DEFAULT_COLORS;
            return (
              <div
                key={alert.id}
                className={`bg-white rounded-xl border overflow-hidden flex transition-all group ${
                  !alert.isRead
                    ? "border-indigo-100 shadow-sm hover:shadow-md hover:border-indigo-200"
                    : "border-slate-200 hover:border-slate-300 hover:shadow-sm"
                }`}
              >
                {/* Colored left bar */}
                <div className={`w-1 flex-shrink-0 ${colors.bar}`} />

                <div className="flex-1 px-4 py-3.5 flex items-start gap-3 min-w-0">
                  {/* Icon circle */}
                  <div className={`w-9 h-9 rounded-full flex items-center justify-center text-base flex-shrink-0 ${!alert.isRead ? "bg-indigo-50" : "bg-slate-50"}`}>
                    {alertTypeIcons[alert.type] ?? "📌"}
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap mb-1">
                      <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${colors.badge}`}>
                        {alertTypeLabels[alert.type] ?? alert.type}
                      </span>
                      {!alert.isRead && (
                        <span className="relative flex h-2 w-2">
                          <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${colors.dot}`} />
                          <span className={`relative inline-flex rounded-full h-2 w-2 ${colors.dot}`} />
                        </span>
                      )}
                    </div>
                    <p className={`text-sm leading-relaxed ${!alert.isRead ? "font-semibold text-slate-900" : "font-normal text-slate-700"}`}>
                      {alert.message}
                    </p>
                    <p className="text-xs text-slate-400 mt-1.5">
                      {alert.competitorName && (
                        <span className="font-medium text-slate-500 hover:text-indigo-600 cursor-pointer transition-colors">{alert.competitorName}</span>
                      )}
                      {alert.competitorName && " · "}
                      {formatDate(alert.date)}
                    </p>
                  </div>

                  {/* Mark read button */}
                  {!alert.isRead && (
                    <button
                      onClick={() => markRead(alert.id)}
                      className="flex-shrink-0 opacity-0 group-hover:opacity-100 flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-500 hover:text-slate-800 border border-slate-200 hover:border-slate-300 rounded-lg bg-white hover:bg-slate-50 transition-all"
                    >
                      <svg className="w-3 h-3" viewBox="0 0 12 12" fill="none">
                        <path d="M1.5 6l3 3 6-6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                      Marquer lu
                    </button>
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
