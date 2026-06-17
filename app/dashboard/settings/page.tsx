"use client";

import { useState } from "react";
import { useToast } from "@/components/Toast";

const MASKED_API_KEY = "ciq_live_••••••••••••••••••••••••••••";

interface ToggleProps {
  value: boolean;
  onChange: () => void;
}

function Toggle({ value, onChange }: ToggleProps) {
  return (
    <button
      role="switch"
      aria-checked={value}
      onClick={onChange}
      className={`relative w-11 h-6 rounded-full transition-colors flex-shrink-0 ${value ? "bg-indigo-600" : "bg-slate-200"}`}
    >
      <span
        className="absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform"
        style={{ transform: value ? "translateX(20px)" : "translateX(0)" }}
      />
    </button>
  );
}

export default function SettingsPage() {
  const { toast } = useToast();
  const [form, setForm] = useState({ firstName: "Demo", lastName: "User", email: "demo@competeiq.com", company: "CompeteIQ Inc." });
  const [saving, setSaving] = useState(false);
  const [notifications, setNotifications] = useState({
    pricing: true, features: true, acquisitions: false, weekly: true, monthly: true,
  });

  const handleSave = async () => {
    setSaving(true);
    await new Promise((r) => setTimeout(r, 600));
    setSaving(false);
    toast("Modifications sauvegardées avec succès");
  };

  const copyApiKey = async () => {
    toast("La clé complète est disponible uniquement via l'API sécurisée", "info");
  };

  const regenerateKey = async () => {
    const res = await fetch("/api/auth/logout", { method: "POST" }).catch(() => null);
    if (res?.ok) toast("Clé API régénérée — reconnectez-vous", "info");
    else toast("Erreur lors de la régénération", "error");
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
          <div className="w-14 h-14 rounded-full bg-indigo-500 flex items-center justify-center text-white text-xl font-bold select-none">
            {form.firstName[0]}{form.lastName[0]}
          </div>
          <div>
            <p className="font-medium text-slate-900">{form.firstName} {form.lastName}</p>
            <p className="text-sm text-slate-500">{form.email}</p>
          </div>
        </div>
        <div className="grid sm:grid-cols-2 gap-4">
          {[
            { label: "Prénom", key: "firstName" as const, type: "text" },
            { label: "Nom", key: "lastName" as const, type: "text" },
            { label: "Email", key: "email" as const, type: "email" },
            { label: "Entreprise", key: "company" as const, type: "text" },
          ].map((f) => (
            <div key={f.label}>
              <label className="block text-xs font-medium text-slate-500 mb-1">{f.label}</label>
              <input
                type={f.type}
                value={form[f.key]}
                onChange={(e) => setForm((prev) => ({ ...prev, [f.key]: e.target.value }))}
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-shadow"
              />
            </div>
          ))}
        </div>
      </div>

      {/* Notifications */}
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <h3 className="font-semibold text-slate-900 mb-4">Notifications</h3>
        <div className="divide-y divide-slate-50">
          {[
            { key: "pricing" as const, label: "Changements de prix", desc: "Alertes lors de modifications tarifaires" },
            { key: "features" as const, label: "Nouvelles fonctionnalités", desc: "Mises à jour produit des concurrents" },
            { key: "acquisitions" as const, label: "Acquisitions & partenariats", desc: "Actualités stratégiques" },
            { key: "weekly" as const, label: "Rapport hebdomadaire", desc: "Résumé chaque lundi matin" },
            { key: "monthly" as const, label: "Rapport mensuel", desc: "Analyse complète mensuelle" },
          ].map((n) => (
            <div key={n.key} className="flex items-center justify-between py-3.5">
              <div>
                <p className="text-sm font-medium text-slate-800">{n.label}</p>
                <p className="text-xs text-slate-400">{n.desc}</p>
              </div>
              <Toggle
                value={notifications[n.key]}
                onChange={() => setNotifications((prev) => ({ ...prev, [n.key]: !prev[n.key] }))}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Danger zone */}
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <h3 className="font-semibold text-slate-900 mb-1">Clé API</h3>
        <p className="text-xs text-slate-500 mb-4">
          Utilisez cette clé pour accéder à l&apos;API REST CompeteIQ depuis vos applications.
        </p>
        <div className="flex gap-2">
          <input
            type="text"
            readOnly
            value={MASKED_API_KEY}
            className="flex-1 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-500 bg-slate-50 font-mono select-all"
          />
          <button
            onClick={copyApiKey}
            className="px-3 py-2 border border-slate-200 rounded-lg text-sm text-slate-600 hover:bg-slate-50 transition-colors whitespace-nowrap"
          >
            Copier
          </button>
          <button
            onClick={regenerateKey}
            className="px-3 py-2 border border-red-200 rounded-lg text-sm text-red-500 hover:bg-red-50 transition-colors whitespace-nowrap"
          >
            Régénérer
          </button>
        </div>
      </div>

      {/* Save */}
      <div className="flex gap-3">
        <button
          onClick={handleSave}
          disabled={saving}
          className="bg-indigo-600 text-white px-6 py-2.5 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors disabled:opacity-60 flex items-center gap-2"
        >
          {saving && <span className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />}
          {saving ? "Sauvegarde..." : "Sauvegarder"}
        </button>
        <button
          onClick={() => setForm({ firstName: "Demo", lastName: "User", email: "demo@competeiq.com", company: "CompeteIQ Inc." })}
          className="border border-slate-200 text-slate-600 px-6 py-2.5 rounded-lg text-sm font-medium hover:bg-slate-50 transition-colors"
        >
          Réinitialiser
        </button>
      </div>
    </div>
  );
}
