"use client";

import { useState } from "react";
import { alerts as initialAlerts } from "@/lib/data";

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

export default function AlertsPage() {
  const [alerts, setAlerts] = useState(initialAlerts);
  const [filter, setFilter] = useState<"all" | "unread" | "read">("all");

  const unreadCount = alerts.filter((a) => !a.isRead).length;

  const markAllRead = () => setAlerts((prev) => prev.map((a) => ({ ...a, isRead: true })));
  const markRead = (id: string) => setAlerts((prev) => prev.map((a) => a.id === id ? { ...a, isRead: true } : a));

  const filtered = alerts.filter((a) =>
    filter === "unread" ? !a.isRead : filter === "read" ? a.isRead : true
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Alertes</h2>
          <p className="text-slate-500 text-sm mt-1">
            {unreadCount} alerte{unreadCount !== 1 ? "s" : ""} non lue{unreadCount !== 1 ? "s" : ""}
          </p>
        </div>
        {unreadCount > 0 && (
          <button
            onClick={markAllRead}
            className="text-sm text-indigo-600 hover:underline font-medium"
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
        {filtered.map((alert) => (
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
                  <span className="text-xs text-slate-400">{alert.competitorName}</span>
                  {!alert.isRead && (
                    <span className="w-2 h-2 rounded-full bg-indigo-500 inline-block"></span>
                  )}
                </div>
                <p className="text-sm text-slate-800 leading-relaxed">{alert.message}</p>
                <p className="text-xs text-slate-400 mt-1">{alert.date}</p>
              </div>
              {!alert.isRead && (
                <button
                  onClick={() => markRead(alert.id)}
                  className="text-xs text-slate-400 hover:text-slate-600 flex-shrink-0"
                >
                  Marquer lu
                </button>
              )}
            </div>
          </div>
        ))}
        {filtered.length === 0 && (
          <div className="text-center py-16 text-slate-400">
            <span className="text-4xl block mb-3">🔕</span>
            <p className="text-sm">Aucune alerte à afficher</p>
          </div>
        )}
      </div>
    </div>
  );
}
