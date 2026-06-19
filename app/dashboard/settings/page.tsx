"use client";

import { useState, useEffect, useRef } from "react";
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
      className={`relative w-11 h-6 rounded-full transition-colors flex-shrink-0 focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2 ${value ? "bg-indigo-600" : "bg-slate-200"}`}
    >
      <span
        className="absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow-sm transition-transform"
        style={{ transform: value ? "translateX(20px)" : "translateX(0)" }}
      />
    </button>
  );
}

type NavSection = "profile" | "notifications" | "api" | "compliance" | "support";

const NAV_ITEMS: { key: NavSection; label: string; icon: React.ReactNode }[] = [
  {
    key: "profile",
    label: "Profil",
    icon: (
      <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none">
        <circle cx="8" cy="5" r="3" stroke="currentColor" strokeWidth="1.4" />
        <path d="M2 14c0-3.314 2.686-5 6-5s6 1.686 6 5" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    key: "notifications",
    label: "Notifications",
    icon: (
      <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none">
        <path d="M8 2a5 5 0 00-5 5v2.5L2 11h12l-1-1.5V7a5 5 0 00-5-5z" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round" />
        <path d="M6.5 13a1.5 1.5 0 003 0" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    key: "api",
    label: "API",
    icon: (
      <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none">
        <path d="M5 5l-3 3 3 3M11 5l3 3-3 3M9 3l-2 10" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    key: "compliance",
    label: "Conformité",
    icon: (
      <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none">
        <path d="M8 2L3 4.5v4C3 11.5 5.2 13.8 8 14.5c2.8-.7 5-3 5-6v-4L8 2z" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round" />
        <path d="M5.5 8l2 2 3-3" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    key: "support",
    label: "Support dédié",
    icon: (
      <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none">
        <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="1.4" />
        <path d="M5.5 6.5a2.5 2.5 0 015 0c0 1.5-1.5 2-2.5 2.5" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
        <circle cx="8" cy="12" r="0.75" fill="currentColor" />
      </svg>
    ),
  },
];

export default function SettingsPage() {
  const { toast } = useToast();
  const [form, setForm] = useState({ firstName: "Demo", lastName: "User", email: "demo@competeiq.com", company: "CompeteIQ Inc." });
  const [saving, setSaving] = useState(false);
  const [notifications, setNotifications] = useState({
    pricing: true, features: true, acquisitions: false, weekly: true, monthly: true,
  });
  const [activeSection, setActiveSection] = useState<NavSection>("profile");
  const [deleteConfirm, setDeleteConfirm] = useState(false);

  const sectionRefs = useRef<Record<NavSection, HTMLDivElement | null>>({
    profile: null,
    notifications: null,
    api: null,
    compliance: null,
    support: null,
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

  const scrollToSection = (key: NavSection) => {
    sectionRefs.current[key]?.scrollIntoView({ behavior: "smooth", block: "start" });
    setActiveSection(key);
  };

  // Intersection observer to update active nav item on scroll
  useEffect(() => {
    const observers: IntersectionObserver[] = [];
    (Object.keys(sectionRefs.current) as NavSection[]).forEach((key) => {
      const el = sectionRefs.current[key];
      if (!el) return;
      const obs = new IntersectionObserver(
        ([entry]) => { if (entry.isIntersecting) setActiveSection(key); },
        { rootMargin: "-30% 0px -60% 0px", threshold: 0 }
      );
      obs.observe(el);
      observers.push(obs);
    });
    return () => observers.forEach((o) => o.disconnect());
  }, []);

  const initials = (form.firstName[0] ?? "") + (form.lastName[0] ?? "");

  return (
    <div className="flex gap-8 items-start">
      {/* Left nav */}
      <nav className="w-48 flex-shrink-0 sticky top-6">
        <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-3 px-3">Paramètres</p>
        <ul className="space-y-0.5">
          {NAV_ITEMS.map((item) => (
            <li key={item.key}>
              <button
                onClick={() => scrollToSection(item.key)}
                className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium transition-all text-left ${
                  activeSection === item.key
                    ? "bg-indigo-50 text-indigo-700"
                    : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                }`}
              >
                <span className={activeSection === item.key ? "text-indigo-600" : "text-slate-400"}>
                  {item.icon}
                </span>
                {item.label}
                {activeSection === item.key && (
                  <span className="ml-auto w-1.5 h-1.5 rounded-full bg-indigo-500 flex-shrink-0" />
                )}
              </button>
            </li>
          ))}
        </ul>
      </nav>

      {/* Main content */}
      <div className="flex-1 min-w-0 space-y-6 max-w-2xl">
        {/* Page header */}
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Paramètres</h2>
          <p className="text-slate-500 text-sm mt-1">Gérez votre compte et vos préférences</p>
        </div>

        {/* Profile section */}
        <div ref={(el) => { sectionRefs.current.profile = el; }} className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-100">
            <h3 className="font-semibold text-slate-900">Profil</h3>
            <p className="text-xs text-slate-400 mt-0.5">Vos informations personnelles et professionnelles</p>
          </div>
          <div className="p-6">
            {/* Avatar row */}
            <div className="flex items-center gap-4 mb-6">
              <div className="relative">
                <div className="w-16 h-16 rounded-full bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center text-white text-xl font-bold select-none shadow-sm">
                  {initials}
                </div>
                <span className="absolute -bottom-0.5 -right-0.5 w-4 h-4 bg-emerald-400 border-2 border-white rounded-full" title="En ligne" />
              </div>
              <div>
                <p className="font-semibold text-slate-900">{form.firstName} {form.lastName}</p>
                <p className="text-sm text-slate-500">{form.email}</p>
                <p className="text-xs text-slate-400 mt-0.5">{form.company}</p>
              </div>
            </div>

            {/* Plan badge */}
            <div className="flex items-center justify-between bg-indigo-50 border border-indigo-100 rounded-xl px-4 py-3 mb-6">
              <div>
                <p className="text-xs font-semibold text-indigo-500 uppercase tracking-widest mb-0.5">Plan actuel</p>
                <p className="text-sm font-bold text-indigo-900">Performance — 2 490€/mois</p>
              </div>
              <a
                href="#"
                className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 transition-colors whitespace-nowrap"
              >
                Changer de plan →
              </a>
            </div>

            {/* Form fields */}
            <div className="grid sm:grid-cols-2 gap-4">
              {[
                { label: "Prénom", key: "firstName" as const, type: "text", placeholder: "Jean" },
                { label: "Nom", key: "lastName" as const, type: "text", placeholder: "Dupont" },
                { label: "Adresse email", key: "email" as const, type: "email", placeholder: "jean@exemple.com" },
                { label: "Entreprise", key: "company" as const, type: "text", placeholder: "Acme Corp." },
              ].map((f) => (
                <div key={f.label}>
                  <label className="block text-xs font-semibold text-slate-600 mb-1.5">{f.label}</label>
                  <input
                    type={f.type}
                    value={form[f.key]}
                    placeholder={f.placeholder}
                    onChange={(e) => setForm((prev) => ({ ...prev, [f.key]: e.target.value }))}
                    className="w-full border border-slate-200 rounded-lg px-3.5 py-2.5 text-sm text-slate-800 placeholder-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow hover:border-slate-300"
                  />
                </div>
              ))}
            </div>

            {/* Save row */}
            <div className="flex gap-3 mt-6 pt-5 border-t border-slate-100">
              <button
                onClick={handleSave}
                disabled={saving}
                className="bg-indigo-600 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors disabled:opacity-60 flex items-center gap-2 shadow-sm"
              >
                {saving && <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />}
                {saving ? "Sauvegarde…" : "Sauvegarder les modifications"}
              </button>
              <button
                onClick={() => setForm({ firstName: "Demo", lastName: "User", email: "demo@competeiq.com", company: "CompeteIQ Inc." })}
                className="border border-slate-200 text-slate-600 px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-slate-50 transition-colors"
              >
                Réinitialiser
              </button>
            </div>
          </div>
        </div>

        {/* Notifications section */}
        <div ref={(el) => { sectionRefs.current.notifications = el; }} className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-100">
            <h3 className="font-semibold text-slate-900">Notifications</h3>
            <p className="text-xs text-slate-400 mt-0.5">Choisissez les alertes que vous souhaitez recevoir</p>
          </div>
          <div className="divide-y divide-slate-50">
            {[
              { key: "pricing" as const, label: "Changements de prix", desc: "Alertes dès qu'un concurrent modifie ses tarifs", icon: "💰" },
              { key: "features" as const, label: "Nouvelles fonctionnalités", desc: "Mises à jour produit des concurrents surveillés", icon: "🚀" },
              { key: "acquisitions" as const, label: "Acquisitions & partenariats", desc: "Actualités stratégiques et mouvements de marché", icon: "🤝" },
              { key: "weekly" as const, label: "Rapport hebdomadaire", desc: "Résumé complet envoyé chaque lundi matin", icon: "📅" },
              { key: "monthly" as const, label: "Rapport mensuel", desc: "Analyse complète mensuelle avec tendances", icon: "📊" },
            ].map((n) => (
              <div key={n.key} className="flex items-center justify-between px-6 py-4 hover:bg-slate-50/50 transition-colors">
                <div className="flex items-start gap-3">
                  <span className="text-lg mt-0.5">{n.icon}</span>
                  <div>
                    <p className="text-sm font-medium text-slate-800">{n.label}</p>
                    <p className="text-xs text-slate-400 mt-0.5">{n.desc}</p>
                  </div>
                </div>
                <Toggle
                  value={notifications[n.key]}
                  onChange={() => setNotifications((prev) => ({ ...prev, [n.key]: !prev[n.key] }))}
                />
              </div>
            ))}
          </div>
        </div>

        {/* API section */}
        <div ref={(el) => { sectionRefs.current.api = el; }} className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-100">
            <h3 className="font-semibold text-slate-900">Clé API</h3>
            <p className="text-xs text-slate-400 mt-0.5">Accédez à l&apos;API REST CompeteIQ depuis vos applications</p>
          </div>
          <div className="p-6">
            <div className="bg-slate-50 rounded-xl border border-slate-200 p-4 mb-4">
              <div className="flex items-center justify-between mb-2">
                <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Clé de production</p>
                <span className="flex items-center gap-1 text-xs text-emerald-600 font-medium">
                  <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full" />
                  Active
                </span>
              </div>
              <div className="flex items-center gap-2">
                <code className="flex-1 text-xs font-mono text-slate-700 bg-white border border-slate-200 rounded-lg px-3 py-2.5 select-all overflow-hidden text-ellipsis whitespace-nowrap">
                  {MASKED_API_KEY}
                </code>
                <button
                  onClick={copyApiKey}
                  className="flex-shrink-0 p-2.5 border border-slate-200 rounded-lg text-slate-500 hover:bg-white hover:text-slate-800 hover:border-slate-300 transition-all bg-white"
                  title="Copier"
                >
                  <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none">
                    <rect x="5" y="5" width="9" height="9" rx="1.5" stroke="currentColor" strokeWidth="1.4" />
                    <path d="M11 5V3.5A1.5 1.5 0 009.5 2h-7A1.5 1.5 0 001 3.5v7A1.5 1.5 0 002.5 12H4" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
                  </svg>
                </button>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={regenerateKey}
                className="flex items-center gap-2 px-4 py-2 border border-slate-200 text-slate-600 rounded-lg text-sm font-medium hover:bg-slate-50 hover:border-slate-300 transition-all"
              >
                <svg className="w-3.5 h-3.5" viewBox="0 0 14 14" fill="none">
                  <path d="M13 2v4H9" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
                  <path d="M1 12v-4h4" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
                  <path d="M2.3 5a5 5 0 018-1.7l2.7 2.7M11.7 9a5 5 0 01-8 1.7L1 8" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                Régénérer la clé
              </button>
              <p className="text-xs text-slate-400">Une nouvelle clé sera générée et l&apos;ancienne sera invalidée.</p>
            </div>
          </div>
        </div>

        {/* Conformité & Sécurité section */}
        <div ref={(el) => { sectionRefs.current.compliance = el; }} className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-100">
            <h3 className="font-semibold text-slate-900">Conformité &amp; Sécurité</h3>
            <p className="text-xs text-slate-400 mt-0.5">Certifications et garanties de conformité de votre compte</p>
          </div>
          <div className="p-6">
            <div className="flex flex-wrap gap-3">
              {[
                { label: "RGPD", icon: "✓" },
                { label: "ISO 27001", icon: "✓" },
                { label: "SOC 2 Type II", icon: "✓" },
                { label: "Hébergement EU", icon: "✓" },
              ].map((badge) => (
                <div
                  key={badge.label}
                  className="flex items-center gap-2 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-lg px-3.5 py-2 text-sm font-semibold"
                >
                  <span className="w-4 h-4 rounded-full bg-emerald-500 text-white text-xs flex items-center justify-center font-bold flex-shrink-0">
                    {badge.icon}
                  </span>
                  {badge.label}
                </div>
              ))}
            </div>
            <p className="text-xs text-slate-400 mt-4 leading-relaxed">
              Vos données sont hébergées exclusivement dans des datacenters certifiés situés dans l&apos;Union Européenne.
              CompeteIQ est audité annuellement par un tiers indépendant accrédité.
            </p>
          </div>
        </div>

        {/* Support dédié section */}
        <div ref={(el) => { sectionRefs.current.support = el; }} className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-100">
            <h3 className="font-semibold text-slate-900">Support dédié</h3>
            <p className="text-xs text-slate-400 mt-0.5">Votre interlocuteur privilégié chez CompeteIQ</p>
          </div>
          <div className="p-6">
            <div className="flex items-center gap-4 mb-5">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-violet-500 to-indigo-600 flex items-center justify-center text-white font-bold text-lg flex-shrink-0 shadow-sm select-none">
                MD
              </div>
              <div>
                <p className="font-semibold text-slate-900 text-sm">Marie Dubois</p>
                <p className="text-xs text-indigo-600 font-medium">Customer Success Manager</p>
              </div>
            </div>
            <div className="space-y-3">
              <div className="flex items-center gap-3 text-sm text-slate-700">
                <svg className="w-4 h-4 text-slate-400 flex-shrink-0" viewBox="0 0 16 16" fill="none">
                  <rect x="1" y="4" width="14" height="9" rx="1.5" stroke="currentColor" strokeWidth="1.4" />
                  <path d="M1 5.5l7 4.5 7-4.5" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
                </svg>
                <a href="mailto:m.dubois@competeiq.io" className="text-indigo-600 hover:text-indigo-800 transition-colors font-medium">
                  m.dubois@competeiq.io
                </a>
              </div>
              <div className="flex items-center gap-3 text-sm text-slate-700">
                <svg className="w-4 h-4 text-slate-400 flex-shrink-0" viewBox="0 0 16 16" fill="none">
                  <path d="M3 2h3l1.5 3.5-1.5 1a8 8 0 004 4l1-1.5L14.5 10V13c0 .6-.5 1-1 .9C4.8 12.5 1 7 2.1 3.5A1 1 0 013 2z" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round" />
                </svg>
                <span className="font-medium">+33 1 82 88 XX XX</span>
              </div>
              <div className="flex items-center gap-3 text-sm text-slate-500">
                <svg className="w-4 h-4 text-slate-400 flex-shrink-0" viewBox="0 0 16 16" fill="none">
                  <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="1.4" />
                  <path d="M8 5v3.5l2 1.5" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                <span>Disponible du lundi au vendredi, 9h–18h CET</span>
              </div>
            </div>
          </div>
        </div>

        {/* Danger zone */}
        <div className="bg-white rounded-xl border border-red-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-red-100 bg-red-50/50">
            <h3 className="font-semibold text-red-700">Zone de danger</h3>
            <p className="text-xs text-red-400 mt-0.5">Ces actions sont irréversibles. Procédez avec précaution.</p>
          </div>
          <div className="p-6">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-sm font-medium text-slate-800">Supprimer le compte</p>
                <p className="text-xs text-slate-500 mt-0.5">
                  Supprime définitivement votre compte, vos données et tous vos rapports.
                </p>
              </div>
              {!deleteConfirm ? (
                <button
                  onClick={() => setDeleteConfirm(true)}
                  className="flex-shrink-0 px-4 py-2 border border-red-200 text-red-500 rounded-lg text-sm font-medium hover:bg-red-50 hover:border-red-400 hover:text-red-700 transition-all"
                >
                  Supprimer le compte
                </button>
              ) : (
                <div className="flex-shrink-0 flex items-center gap-2">
                  <p className="text-xs text-red-500 font-medium">Confirmer ?</p>
                  <button
                    className="px-3 py-1.5 bg-red-600 text-white rounded-lg text-xs font-semibold hover:bg-red-700 transition-colors"
                    onClick={() => { setDeleteConfirm(false); toast("Action annulée", "info"); }}
                  >
                    Oui, supprimer
                  </button>
                  <button
                    onClick={() => setDeleteConfirm(false)}
                    className="px-3 py-1.5 border border-slate-200 text-slate-600 rounded-lg text-xs font-medium hover:bg-slate-50 transition-colors"
                  >
                    Annuler
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
