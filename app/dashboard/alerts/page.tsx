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

const alertTypeColors: Record<string, string> = {
  pricing: "bg-amber-100 text-amber-700",
  feature: "bg-indigo-100 text-indigo-700",
  acquisition: "bg-rose-100 text-rose-700",
  product: "bg-purple-100 text-purple-700",
  partnership: "bg-emerald-100 text-emerald-700",
  website: "bg-slate-100 text-slate-700",
};

function AlertSkeleton() {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-4 animate-pulse">
      <div className="flex items-start gap-3">
        <div className="w-8 h-8 rounded-full bg-slate-100 flex-shrink-0"></div>
        <div className="flex-1">
          <div className="flex gap-2 mb-2">
            <div className="h-5 w-20 bg-slate-100 rounded-full"></div>
            <div className="h-5 w-16 bg-slate-100 rounded-full"></div>
          </div>
          <div className="h-4 w-full bg-slate-100 rounded mb-1.5"></div>
          <div className="h-3 w-32 bg-slate-100 rounded"></div>
        </div>
      </div>
    </div>
  );
}

function formatDate(dateStr: string) {
  const date = new Date(dateStr);
  return date.toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" });
}

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<"all" | "unread" | "read">("all");

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

  const filtered = alerts.filter((a) =>
    filter === "unread" ? !a.isRead : filter === "read" ? a.isRead : true
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Alertes</h2>
          <p className="text-slate-500 text-sm mt-1">
            {loading
              ? "Chargement..."
              : `${unreadCount} alerte${unreadCount !== 1 ? "s" : ""} non lue${unreadCount !== 1 ? "s" : ""}`}
          </p>
        </div>
        {!loading && unreadCount > 0 && (
          <button
            onClick={markAllRead}
            className="text-sm text-indigo-600 hover:underline font-medium transition-colors"
          >
            Tout marquer comme lu
          </button>
        )}
      </div>

      {/* Filters */}
      <div className="flex gap-2">
        {(["all", "unread", "read"] as const).map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              filter === f ? "bg-indigo-600 text-white" : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-50"
            }`}
          >
            {f === "all" ? "Toutes" : f === "unread" ? "Non lues" : "Lues"}
          </button>
        ))}
      </div>

      {/* Alert list */}
      <div className="space-y-3">
        {loading ? (
          <>
            {[...Array(5)].map((_, i) => (
              <AlertSkeleton key={i} />
            ))}
          </>
        ) : filtered.length === 0 ? (
          <div className="text-center py-16 text-slate-400">
            <span className="text-4xl block mb-3">🔕</span>
            <p className="text-sm">Aucune alerte à afficher</p>
          </div>
        ) : (
          filtered.map((alert) => (
            <div
              key={alert.id}
              className={`bg-white rounded-xl border p-4 transition-all ${
                !alert.isRead ? "border-indigo-200 shadow-sm" : "border-slate-200"
              }`}
            >
              <div className="flex items-start gap-3">
                <span className="text-2xl flex-shrink-0">{alertTypeIcons[alert.type] || "📌"}</span>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap mb-1">
                    <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${alertTypeColors[alert.type] || "bg-slate-100 text-slate-600"}`}>
                      {alertTypeLabels[alert.type] || alert.type}
                    </span>
                    {!alert.isRead && (
                      <span className="w-2 h-2 rounded-full bg-indigo-500 inline-block"></span>
                    )}
                  </div>
                  <p className="text-sm text-slate-800 leading-relaxed">{alert.message}</p>
                  <p className="text-xs text-slate-400 mt-1">{alert.competitorName && <span className="font-medium">{alert.competitorName} · </span>}{formatDate(alert.date)}</p>
                </div>
                {!alert.isRead && (
                  <button
                    onClick={() => markRead(alert.id)}
                    className="text-xs text-slate-400 hover:text-slate-600 flex-shrink-0 transition-colors"
                  >
                    Marquer lu
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
