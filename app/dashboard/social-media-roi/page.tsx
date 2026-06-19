"use client";

import { useEffect, useState } from "react";

// ── Types ──────────────────────────────────────────────────────────────────────

interface SocialProfile {
  id: string;
  client_name: string;
  sector: string;
  platform: "LinkedIn" | "Instagram" | "Facebook" | "Google";
  followers_count: number;
  monthly_reach: number;
  engagement_rate: number;
  post_frequency_per_week: number;
  ad_spend_eur_monthly: number;
  leads_generated_monthly: number;
  cost_per_lead_eur: number;
  conversion_rate: number;
  roi_score: number;
  composite_score: number;
  risk_level: "critique" | "élevé" | "modéré" | "faible";
}

interface SummaryData {
  total_profiles: number;
  avg_engagement_rate: number;
  avg_roi_score: number;
  total_monthly_ad_spend: number;
  profiles_critique: number;
  profiles_eleve: number;
  profiles_modere: number;
  profiles_faible: number;
  top_risk_profile: string;
  top_risk_score: number;
  patterns_detected: string[];
  avg_composite: number;
  avg_estimated_social_index: number;
}

interface ApiResponse {
  data: {
    entities: SocialProfile[];
    summary: SummaryData;
  };
}

type RiskFilter = "Tous" | "Critique" | "Élevé" | "Modéré" | "Faible";
type ModalTab = "Scores" | "Signaux" | "Actions";

// ── Constants ──────────────────────────────────────────────────────────────────

const RISK_COLORS: Record<string, { bg: string; text: string; border: string; dot: string }> = {
  critique: {
    bg: "bg-red-900/30",
    text: "text-red-400",
    border: "border-red-700/50",
    dot: "bg-red-500",
  },
  élevé: {
    bg: "bg-orange-900/30",
    text: "text-orange-400",
    border: "border-orange-700/50",
    dot: "bg-orange-500",
  },
  modéré: {
    bg: "bg-yellow-900/30",
    text: "text-yellow-400",
    border: "border-yellow-700/50",
    dot: "bg-yellow-500",
  },
  faible: {
    bg: "bg-emerald-900/30",
    text: "text-emerald-400",
    border: "border-emerald-700/50",
    dot: "bg-emerald-500",
  },
};

const PLATFORM_COLORS: Record<string, { bg: string; text: string; abbr: string }> = {
  LinkedIn: { bg: "bg-blue-700", text: "text-white", abbr: "LI" },
  Instagram: { bg: "bg-pink-600", text: "text-white", abbr: "IG" },
  Facebook: { bg: "bg-indigo-600", text: "text-white", abbr: "FB" },
  Google: { bg: "bg-emerald-600", text: "text-white", abbr: "GO" },
};

const RISK_ACTIONS: Record<string, string[]> = {
  critique: [
    "Audit complet de la stratégie publicitaire sous 48h",
    "Révision immédiate des audiences cibles et des créatifs",
    "Réduction du budget publicitaire jusqu'à correction",
    "Mise en place d'un suivi hebdomadaire des KPIs",
  ],
  élevé: [
    "Analyse approfondie des contenus les moins performants",
    "Test A/B sur les visuels et les copies publicitaires",
    "Augmentation de la fréquence de publication à 5/semaine",
    "Optimisation du ciblage géographique et démographique",
  ],
  modéré: [
    "Renforcement du calendrier éditorial",
    "Exploration des formats Reels / Stories pour la portée organique",
    "Mise en place d'une stratégie d'influence locale",
    "Suivi mensuel des conversions et du coût par lead",
  ],
  faible: [
    "Maintien de la stratégie actuelle avec ajustements mineurs",
    "Scaling progressif du budget publicitaire (+20% trimestriel)",
    "Développement d'une stratégie de contenu viral",
    "Exploration de nouvelles plateformes pour diversifier",
  ],
};

// ── SVG Icons ──────────────────────────────────────────────────────────────────

function IconUsers({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
    </svg>
  );
}

function IconTrending({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clipRule="evenodd" />
    </svg>
  );
}

function IconStar({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
    </svg>
  );
}

function IconCash({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
    </svg>
  );
}

function IconWarning({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
    </svg>
  );
}

function IconTarget({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm0-2a6 6 0 100-12 6 6 0 000 12zm0-2a4 4 0 100-8 4 4 0 000 8zm0-2a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
    </svg>
  );
}

function IconX({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
    </svg>
  );
}

// ── GaugeRing SVG ──────────────────────────────────────────────────────────────

function GaugeRing({
  value,
  max,
  label,
  color,
  unit = "",
}: {
  value: number;
  max: number;
  label: string;
  color: string;
  unit?: string;
}) {
  const radius = 36;
  const circumference = 2 * Math.PI * radius;
  const pct = Math.min(1, Math.max(0, value / max));
  const dash = pct * circumference;
  const gap = circumference - dash;

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative w-24 h-24">
        <svg viewBox="0 0 100 100" className="w-full h-full -rotate-90">
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke="#1e293b"
            strokeWidth="10"
          />
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke={color}
            strokeWidth="10"
            strokeLinecap="round"
            strokeDasharray={`${dash} ${gap}`}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-[15px] font-bold text-white leading-none">
            {typeof value === "number" ? value.toFixed(1) : value}
            {unit}
          </span>
        </div>
      </div>
      <p className="text-[11px] text-slate-400 text-center font-medium leading-tight max-w-[80px]">
        {label}
      </p>
    </div>
  );
}

// ── DistBar ────────────────────────────────────────────────────────────────────

function DistBar({
  label,
  count,
  total,
  color,
}: {
  label: string;
  count: number;
  total: number;
  color: string;
}) {
  const pct = total > 0 ? (count / total) * 100 : 0;
  return (
    <div className="flex items-center gap-3">
      <span className="text-[12px] text-slate-400 w-16 shrink-0">{label}</span>
      <div className="flex-1 h-4 bg-slate-800 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full ${color} transition-all duration-700`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="text-[12px] text-slate-300 font-semibold w-5 text-right shrink-0">
        {count}
      </span>
    </div>
  );
}

// ── KPI Card ───────────────────────────────────────────────────────────────────

function KpiCard({
  label,
  value,
  Icon,
  accent,
  sub,
}: {
  label: string;
  value: string | number;
  Icon: React.ComponentType<{ className?: string }>;
  accent: string;
  sub?: string;
}) {
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 flex flex-col gap-2">
      <div className="flex items-center justify-between">
        <p className="text-[11px] text-slate-400 font-semibold uppercase tracking-wide">
          {label}
        </p>
        <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${accent}`}>
          <Icon className="w-4 h-4 text-white" />
        </div>
      </div>
      <p className="text-2xl font-bold text-white tabular-nums leading-none">{value}</p>
      {sub && <p className="text-[11px] text-slate-500">{sub}</p>}
    </div>
  );
}

// ── Entity Card ────────────────────────────────────────────────────────────────

function EntityCard({
  profile,
  onClick,
}: {
  profile: SocialProfile;
  onClick: () => void;
}) {
  const risk = RISK_COLORS[profile.risk_level] ?? RISK_COLORS["modéré"];
  const platform = PLATFORM_COLORS[profile.platform] ?? { bg: "bg-slate-600", text: "text-white", abbr: "??" };

  return (
    <button
      onClick={onClick}
      className={`w-full text-left bg-slate-800 border ${risk.border} rounded-xl p-4 hover:bg-slate-750 hover:border-slate-500 transition-all duration-150 focus:outline-none focus:ring-2 focus:ring-slate-500`}
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-2 mb-3">
        <div className="flex items-center gap-2 min-w-0">
          <div
            className={`w-9 h-9 rounded-lg ${platform.bg} ${platform.text} flex items-center justify-center text-[11px] font-bold shrink-0`}
          >
            {platform.abbr}
          </div>
          <div className="min-w-0">
            <p className="text-[13px] font-semibold text-white truncate">
              {profile.client_name}
            </p>
            <p className="text-[11px] text-slate-400 capitalize">{profile.sector}</p>
          </div>
        </div>
        <span
          className={`text-[10px] font-semibold uppercase tracking-wide px-2 py-0.5 rounded-full shrink-0 ${risk.bg} ${risk.text}`}
        >
          {profile.risk_level}
        </span>
      </div>

      {/* Metrics row */}
      <div className="grid grid-cols-3 gap-2 mt-2">
        <div className="bg-slate-900/50 rounded-lg p-2 text-center">
          <p className="text-[14px] font-bold text-white tabular-nums">
            {profile.engagement_rate.toFixed(1)}
          </p>
          <p className="text-[9px] text-slate-500 mt-0.5">Engagement</p>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-2 text-center">
          <p className="text-[14px] font-bold text-white tabular-nums">
            {profile.roi_score.toFixed(0)}
          </p>
          <p className="text-[9px] text-slate-500 mt-0.5">ROI Score</p>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-2 text-center">
          <p className="text-[14px] font-bold text-white tabular-nums">
            {profile.leads_generated_monthly}
          </p>
          <p className="text-[9px] text-slate-500 mt-0.5">Leads/mois</p>
        </div>
      </div>

      {/* Composite bar */}
      <div className="mt-3">
        <div className="flex items-center justify-between mb-1">
          <span className="text-[10px] text-slate-500">Score composite</span>
          <span className="text-[10px] font-semibold text-slate-300">
            {profile.composite_score.toFixed(1)} / 100
          </span>
        </div>
        <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full ${risk.dot}`}
            style={{ width: `${profile.composite_score}%` }}
          />
        </div>
      </div>
    </button>
  );
}

// ── Detail Modal ───────────────────────────────────────────────────────────────

function DetailModal({
  profile,
  onClose,
}: {
  profile: SocialProfile;
  onClose: () => void;
}) {
  const [activeTab, setActiveTab] = useState<ModalTab>("Scores");
  const risk = RISK_COLORS[profile.risk_level] ?? RISK_COLORS["modéré"];
  const platform = PLATFORM_COLORS[profile.platform] ?? { bg: "bg-slate-600", text: "text-white", abbr: "??" };
  const actions = RISK_ACTIONS[profile.risk_level] ?? [];
  const tabs: ModalTab[] = ["Scores", "Signaux", "Actions"];

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/70 backdrop-blur-sm" />

      {/* Panel */}
      <div className="relative bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div
              className={`w-11 h-11 rounded-xl ${platform.bg} ${platform.text} flex items-center justify-center text-[13px] font-bold shrink-0`}
            >
              {platform.abbr}
            </div>
            <div>
              <h2 className="text-[15px] font-bold text-white">{profile.client_name}</h2>
              <div className="flex items-center gap-2 mt-0.5">
                <span className="text-[12px] text-slate-400 capitalize">{profile.sector}</span>
                <span className="text-slate-600">·</span>
                <span className="text-[12px] text-slate-400">{profile.platform}</span>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span
              className={`text-[11px] font-semibold uppercase tracking-wide px-2.5 py-1 rounded-full ${risk.bg} ${risk.text}`}
            >
              {profile.risk_level}
            </span>
            <button
              onClick={onClose}
              className="w-8 h-8 flex items-center justify-center rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            >
              <IconX className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {tabs.map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`flex-1 py-3 text-[13px] font-medium transition-colors ${
                activeTab === tab
                  ? "text-white border-b-2 border-blue-500 bg-slate-800/50"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-5 max-h-[55vh] overflow-y-auto">
          {/* SCORES TAB */}
          {activeTab === "Scores" && (
            <div className="space-y-3">
              {[
                { label: "ROI Score", value: profile.roi_score, max: 100, suffix: "/100" },
                { label: "Score composite", value: profile.composite_score, max: 100, suffix: "/100" },
                { label: "Taux d'engagement", value: profile.engagement_rate, max: 10, suffix: "/10" },
                { label: "Taux de conversion", value: profile.conversion_rate, max: 100, suffix: "%" },
                { label: "Coût par lead", value: profile.cost_per_lead_eur, max: 500, suffix: " €", invert: true },
              ].map(({ label, value, max, suffix }) => {
                const pct = Math.min(100, (value / max) * 100);
                return (
                  <div key={label}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-[12px] text-slate-400">{label}</span>
                      <span className="text-[12px] font-semibold text-white tabular-nums">
                        {typeof value === "number" ? value.toFixed(2) : value}
                        {suffix}
                      </span>
                    </div>
                    <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full ${risk.dot} opacity-80`}
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* SIGNAUX TAB */}
          {activeTab === "Signaux" && (
            <div className="space-y-3">
              {[
                { label: "Abonnés", value: profile.followers_count.toLocaleString("fr-FR"), icon: "👥" },
                { label: "Portée mensuelle", value: profile.monthly_reach.toLocaleString("fr-FR"), icon: "📡" },
                { label: "Fréquence de publication", value: `${profile.post_frequency_per_week}x / semaine`, icon: "📅" },
                { label: "Budget publicitaire", value: `${profile.ad_spend_eur_monthly.toLocaleString("fr-FR")} €/mois`, icon: "💶" },
                { label: "Leads générés", value: `${profile.leads_generated_monthly} / mois`, icon: "🎯" },
                { label: "Coût par lead", value: `${profile.cost_per_lead_eur.toFixed(2)} €`, icon: "💰" },
                { label: "Taux de conversion", value: `${profile.conversion_rate.toFixed(1)} %`, icon: "📈" },
              ].map(({ label, value, icon }) => (
                <div
                  key={label}
                  className="flex items-center justify-between bg-slate-800 rounded-lg px-3 py-2.5"
                >
                  <div className="flex items-center gap-2">
                    <span className="text-base leading-none">{icon}</span>
                    <span className="text-[12px] text-slate-400">{label}</span>
                  </div>
                  <span className="text-[13px] font-semibold text-white">{value}</span>
                </div>
              ))}
            </div>
          )}

          {/* ACTIONS TAB */}
          {activeTab === "Actions" && (
            <div className="space-y-3">
              <p className="text-[12px] text-slate-400 mb-3">
                Recommandations prioritaires pour niveau de risque{" "}
                <span className={`font-semibold ${risk.text}`}>{profile.risk_level}</span> :
              </p>
              {actions.map((action, i) => (
                <div
                  key={i}
                  className={`flex gap-3 bg-slate-800 rounded-lg p-3 border ${risk.border}`}
                >
                  <span
                    className={`w-5 h-5 rounded-full ${risk.bg} ${risk.text} flex items-center justify-center text-[10px] font-bold shrink-0 mt-0.5`}
                  >
                    {i + 1}
                  </span>
                  <p className="text-[12px] text-slate-300 leading-relaxed">{action}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Skeleton ───────────────────────────────────────────────────────────────────

function CardSkeleton() {
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 animate-pulse">
      <div className="flex items-start justify-between gap-2 mb-3">
        <div className="flex items-center gap-2">
          <div className="w-9 h-9 rounded-lg bg-slate-700" />
          <div>
            <div className="h-3 w-32 bg-slate-700 rounded mb-1.5" />
            <div className="h-2.5 w-20 bg-slate-700 rounded" />
          </div>
        </div>
        <div className="h-5 w-16 bg-slate-700 rounded-full" />
      </div>
      <div className="grid grid-cols-3 gap-2">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="bg-slate-900/50 rounded-lg p-2">
            <div className="h-4 w-8 bg-slate-700 rounded mx-auto mb-1" />
            <div className="h-2 w-12 bg-slate-700 rounded mx-auto" />
          </div>
        ))}
      </div>
    </div>
  );
}

// ── Main Page ──────────────────────────────────────────────────────────────────

export default function SocialMediaROIPage() {
  const [entities, setEntities] = useState<SocialProfile[]>([]);
  const [summary, setSummary] = useState<SummaryData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<RiskFilter>("Tous");
  const [selectedProfile, setSelectedProfile] = useState<SocialProfile | null>(null);

  useEffect(() => {
    fetch("/api/social-media-roi")
      .then((r) => r.json())
      .then((res: ApiResponse) => {
        if (res?.data?.entities) setEntities(res.data.entities);
        if (res?.data?.summary) setSummary(res.data.summary);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const filterMap: Record<RiskFilter, string> = {
    Tous: "",
    Critique: "critique",
    Élevé: "élevé",
    Modéré: "modéré",
    Faible: "faible",
  };

  const filtered =
    filter === "Tous"
      ? entities
      : entities.filter((e) => e.risk_level === filterMap[filter]);

  const totalLeads = entities.reduce((s, e) => s + e.leads_generated_monthly, 0);

  const filterPills: RiskFilter[] = ["Tous", "Critique", "Élevé", "Modéré", "Faible"];

  const pillStyles: Record<RiskFilter, { active: string; inactive: string }> = {
    Tous: {
      active: "bg-blue-600 text-white border-blue-600",
      inactive: "text-slate-400 border-slate-700 hover:border-slate-500",
    },
    Critique: {
      active: "bg-red-700 text-white border-red-700",
      inactive: "text-red-400 border-slate-700 hover:border-red-700/50",
    },
    Élevé: {
      active: "bg-orange-700 text-white border-orange-700",
      inactive: "text-orange-400 border-slate-700 hover:border-orange-700/50",
    },
    Modéré: {
      active: "bg-yellow-700 text-white border-yellow-700",
      inactive: "text-yellow-400 border-slate-700 hover:border-yellow-700/50",
    },
    Faible: {
      active: "bg-emerald-700 text-white border-emerald-700",
      inactive: "text-emerald-400 border-slate-700 hover:border-emerald-700/50",
    },
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white pb-12">
      {/* ── Page header ──────────────────────────────────────────────────────── */}
      <div className="px-6 pt-6 pb-4">
        <div className="flex items-start justify-between flex-wrap gap-4">
          <div>
            <h1 className="text-[22px] font-bold text-white tracking-tight">
              ROI Réseaux Sociaux &amp; Publicités
            </h1>
            <p className="text-[13px] text-slate-400 mt-1">
              Analyse intelligente des performances social media — Caelum Partners
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-[12px] text-slate-400">
              Mis à jour à{" "}
              {new Date().toLocaleTimeString("fr-FR", {
                hour: "2-digit",
                minute: "2-digit",
              })}
            </span>
          </div>
        </div>
      </div>

      <div className="px-6 space-y-6">
        {/* ── KPI Cards (6) ─────────────────────────────────────────────────── */}
        <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-3">
          {loading ? (
            [...Array(6)].map((_, i) => (
              <div
                key={i}
                className="bg-slate-800 border border-slate-700 rounded-xl p-4 animate-pulse h-24"
              />
            ))
          ) : (
            <>
              <KpiCard
                label="Profils Analysés"
                value={summary?.total_profiles ?? 0}
                Icon={IconUsers}
                accent="bg-blue-600"
                sub="clients actifs"
              />
              <KpiCard
                label="Taux d'Engagement Moy."
                value={summary ? `${summary.avg_engagement_rate.toFixed(1)}/10` : "—"}
                Icon={IconTrending}
                accent="bg-violet-600"
                sub="moyenne des profils"
              />
              <KpiCard
                label="ROI Score Moy."
                value={summary ? `${summary.avg_roi_score.toFixed(1)}/100` : "—"}
                Icon={IconStar}
                accent="bg-amber-600"
                sub="indice composite"
              />
              <KpiCard
                label="Budget Pub Total"
                value={
                  summary
                    ? `${summary.total_monthly_ad_spend.toLocaleString("fr-FR")} €`
                    : "—"
                }
                Icon={IconCash}
                accent="bg-emerald-600"
                sub="mensuel cumulé"
              />
              <KpiCard
                label="Profils Critiques"
                value={summary?.profiles_critique ?? 0}
                Icon={IconWarning}
                accent="bg-red-700"
                sub="attention urgente"
              />
              <KpiCard
                label="Leads Générés Total"
                value={loading ? "—" : totalLeads}
                Icon={IconTarget}
                accent="bg-cyan-600"
                sub="leads / mois"
              />
            </>
          )}
        </div>

        {/* ── Gauge Rings + Distribution bars ───────────────────────────────── */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {/* Gauge Rings */}
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
            <h2 className="text-[13px] font-semibold text-slate-300 mb-5">
              Indicateurs Clés — Vue Radar
            </h2>
            <div className="grid grid-cols-4 gap-4 justify-items-center">
              <GaugeRing
                value={summary?.avg_roi_score ?? 0}
                max={100}
                label="ROI Score"
                color="#f59e0b"
              />
              <GaugeRing
                value={summary?.avg_engagement_rate ?? 0}
                max={10}
                label="Taux d'Engagement"
                color="#8b5cf6"
              />
              <GaugeRing
                value={
                  entities.length > 0
                    ? entities.reduce((s, e) => s + e.conversion_rate, 0) / entities.length
                    : 0
                }
                max={100}
                label="Taux de Conversion"
                color="#06b6d4"
                unit="%"
              />
              <GaugeRing
                value={summary?.avg_composite ?? 0}
                max={100}
                label="Performance Globale"
                color="#10b981"
              />
            </div>
          </div>

          {/* Distribution bars */}
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
            <h2 className="text-[13px] font-semibold text-slate-300 mb-5">
              Distribution par Niveau de Risque
            </h2>
            <div className="space-y-3">
              <DistBar
                label="Critique"
                count={summary?.profiles_critique ?? 0}
                total={summary?.total_profiles ?? 1}
                color="bg-red-500"
              />
              <DistBar
                label="Élevé"
                count={summary?.profiles_eleve ?? 0}
                total={summary?.total_profiles ?? 1}
                color="bg-orange-500"
              />
              <DistBar
                label="Modéré"
                count={summary?.profiles_modere ?? 0}
                total={summary?.total_profiles ?? 1}
                color="bg-yellow-500"
              />
              <DistBar
                label="Faible"
                count={summary?.profiles_faible ?? 0}
                total={summary?.total_profiles ?? 1}
                color="bg-emerald-500"
              />
            </div>

            {/* Patterns banner */}
            {summary && summary.patterns_detected.length > 0 && (
              <div className="mt-5 pt-4 border-t border-slate-700">
                <p className="text-[11px] text-slate-500 uppercase tracking-wide font-semibold mb-2">
                  Patterns détectés
                </p>
                <div className="flex flex-wrap gap-1.5">
                  {summary.patterns_detected.map((pat) => (
                    <span
                      key={pat}
                      className="text-[10px] bg-slate-700 text-slate-300 px-2 py-0.5 rounded-full"
                    >
                      {pat}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* ── Filter Pills ───────────────────────────────────────────────────── */}
        <div className="flex items-center gap-2 flex-wrap">
          {filterPills.map((pill) => {
            const styles = pillStyles[pill];
            const isActive = filter === pill;
            return (
              <button
                key={pill}
                onClick={() => setFilter(pill)}
                className={`px-3.5 py-1.5 rounded-full text-[12px] font-semibold border transition-all duration-150 ${
                  isActive ? styles.active : styles.inactive
                }`}
              >
                {pill}
                {pill !== "Tous" && summary && (
                  <span className="ml-1.5 opacity-70">
                    {pill === "Critique"
                      ? summary.profiles_critique
                      : pill === "Élevé"
                      ? summary.profiles_eleve
                      : pill === "Modéré"
                      ? summary.profiles_modere
                      : summary.profiles_faible}
                  </span>
                )}
              </button>
            );
          })}
          <span className="text-[12px] text-slate-500 ml-auto">
            {filtered.length} profil{filtered.length !== 1 ? "s" : ""} affiché{filtered.length !== 1 ? "s" : ""}
          </span>
        </div>

        {/* ── Entity Cards Grid ──────────────────────────────────────────────── */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-4">
          {loading
            ? [...Array(6)].map((_, i) => <CardSkeleton key={i} />)
            : filtered.map((profile) => (
                <EntityCard
                  key={profile.id}
                  profile={profile}
                  onClick={() => setSelectedProfile(profile)}
                />
              ))}
          {!loading && filtered.length === 0 && (
            <div className="col-span-full flex flex-col items-center justify-center py-16 text-center">
              <div className="w-14 h-14 bg-slate-800 rounded-2xl flex items-center justify-center mb-3">
                <IconTarget className="w-7 h-7 text-slate-600" />
              </div>
              <p className="text-[14px] text-slate-400 font-medium">
                Aucun profil pour ce filtre
              </p>
              <p className="text-[12px] text-slate-600 mt-1">
                Essayez un autre niveau de risque
              </p>
            </div>
          )}
        </div>
      </div>

      {/* ── Detail Modal ───────────────────────────────────────────────────────── */}
      {selectedProfile && (
        <DetailModal
          profile={selectedProfile}
          onClose={() => setSelectedProfile(null)}
        />
      )}
    </div>
  );
}
