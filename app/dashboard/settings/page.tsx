"use client";

import { useState } from "react";

export default function SettingsPage() {
  const [saved, setSaved] = useState(false);
  const [notifications, setNotifications] = useState({
    pricing: true,
    features: true,
    acquisitions: false,
    weekly: true,
    monthly: true,
  });

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h2 className="text-2xl font-bold text-slate-900">Paramètres</h2>
        <p className="text-slate-500 text-sm mt-1">Gérez votre compte et vos préférences</p>
      </div>

      {/* Profile */}
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <h3 className="font-semibold text-slate-900 mb-4">Profil</h3>
        <div className="flex items-center gap-4 mb-6">
          <div className="w-14 h-14 rounded-full bg-indigo-500 flex items-center justify-center text-white text-xl font-bold">
            DU
          </div>
          <div>
            <p className="font-medium text-slate-900">Demo User</p>
            <p className="text-sm text-slate-500">demo@competeiq.com</p>
          </div>
        </div>
        <div className="grid sm:grid-cols-2 gap-4">
          {[
            { label: "Prénom", value: "Demo", type: "text" },
            { label: "Nom", value: "User", type: "text" },
            { label: "Email", value: "demo@competeiq.com", type: "email" },
            { label: "Entreprise", value: "CompeteIQ Inc.", type: "text" },
          ].map((f) => (
            <div key={f.label}>
              <label className="block text-xs font-medium text-slate-500 mb-1">{f.label}</label>
              <input
                type={f.type}
                defaultValue={f.value}
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          ))}
        </div>
      </div>

      {/* Notifications */}
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <h3 className="font-semibold text-slate-900 mb-4">Notifications</h3>
        <div className="space-y-3">
          {[
            { key: "pricing" as const, label: "Changements de prix", desc: "Alertes lors de modifications tarifaires" },
            { key: "features" as const, label: "Nouvelles fonctionnalités", desc: "Mises à jour produit des concurrents" },
            { key: "acquisitions" as const, label: "Acquisitions & partenariats", desc: "Actualités stratégiques" },
            { key: "weekly" as const, label: "Rapport hebdomadaire", desc: "Résumé chaque lundi matin" },
            { key: "monthly" as const, label: "Rapport mensuel", desc: "Analyse complète mensuelle" },
          ].map((n) => (
            <div key={n.key} className="flex items-center justify-between py-2.5 border-b border-slate-50 last:border-0">
              <div>
                <p className="text-sm font-medium text-slate-800">{n.label}</p>
                <p className="text-xs text-slate-400">{n.desc}</p>
              </div>
              <button
                onClick={() => setNotifications((prev) => ({ ...prev, [n.key]: !prev[n.key] }))}
                className={`relative w-10 h-5.5 rounded-full transition-colors ${notifications[n.key] ? "bg-indigo-600" : "bg-slate-200"}`}
                style={{ height: 22 }}
              >
                <span
                  className={`absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full shadow transition-transform ${notifications[n.key] ? "translate-x-4.5" : ""}`}
                  style={{ transform: notifications[n.key] ? "translateX(18px)" : "translateX(0)" }}
                ></span>
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* API Key */}
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <h3 className="font-semibold text-slate-900 mb-1">Clé API</h3>
        <p className="text-xs text-slate-500 mb-4">Utilisez cette clé pour accéder à l&apos;API CompeteIQ</p>
        <div className="flex gap-2">
          <input
            type="text"
            readOnly
            value="ciq_live_k9x2m5p8n3q7r1t4v6w0y2z5..."
            className="flex-1 border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-500 bg-slate-50 font-mono"
          />
          <button className="px-3 py-2 border border-slate-200 rounded-lg text-sm text-slate-600 hover:bg-slate-50 transition-colors">
            Copier
          </button>
          <button className="px-3 py-2 border border-slate-200 rounded-lg text-sm text-red-500 hover:bg-red-50 transition-colors">
            Régénérer
          </button>
        </div>
      </div>

      {/* Save */}
      <div className="flex gap-3">
        <button
          onClick={handleSave}
          className="bg-indigo-600 text-white px-6 py-2.5 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors"
        >
          {saved ? "✓ Sauvegardé !" : "Sauvegarder les modifications"}
        </button>
        <button className="border border-slate-200 text-slate-600 px-6 py-2.5 rounded-lg text-sm font-medium hover:bg-slate-50 transition-colors">
          Annuler
        </button>
      </div>
    </div>
  );
}
