"use client";

import { useState, useEffect, useRef } from "react";
import { competitors } from "@/lib/data";

// ─── Types ────────────────────────────────────────────────────────────────────

type Action =
  | "price_cut"
  | "new_feature"
  | "acquisition"
  | "fundraising"
  | "freemium"
  | "exit_segment";

type Timeline = "1m" | "3m" | "6m" | "12m";

interface SimulationResult {
  revenueImpact: number; // percentage, negative = loss
  marketShareImpact: number; // points
  churnAccounts: number; // out of 340
  responseDelay: "Immédiat" | "30 jours" | "90 jours";
  actions: { label: string; priority: "URGENT" | "IMPORTANT" | "À PLANIFIER" }[];
}

interface SavedScenario {
  title: string;
  description: string;
  revenueImpact: number;
  marketShareImpact: number;
  churnAccounts: number;
}

// ─── Constants ────────────────────────────────────────────────────────────────

const ACTIONS: { value: Action; label: string }[] = [
  { value: "price_cut", label: "Baissent leurs prix de X%" },
  { value: "new_feature", label: "Lancent une nouvelle feature" },
  { value: "acquisition", label: "Acquièrent un concurrent" },
  { value: "fundraising", label: "Lèvent des fonds (montant important)" },
  { value: "freemium", label: "Proposent une offre gratuite" },
  { value: "exit_segment", label: "Quittent un segment de marché" },
];

const TIMELINES: { value: Timeline; label: string }[] = [
  { value: "1m", label: "1 mois" },
  { value: "3m", label: "3 mois" },
  { value: "6m", label: "6 mois" },
  { value: "12m", label: "12 mois" },
];

const TIMELINE_MULTIPLIER: Record<Timeline, number> = {
  "1m": 1.3,
  "3m": 1.0,
  "6m": 0.75,
  "12m": 0.55,
};

const ACTION_BASE: Record<Action, { revenue: number; market: number; churn: number }> = {
  price_cut:     { revenue: -0.18, market: -1.8, churn: 32 },
  new_feature:   { revenue: -0.10, market: -1.2, churn: 18 },
  acquisition:   { revenue: -0.22, market: -2.4, churn: 42 },
  fundraising:   { revenue: -0.08, market: -0.9, churn: 14 },
  freemium:      { revenue: -0.28, market: -3.1, churn: 58 },
  exit_segment:  { revenue:  0.06, market:  1.1, churn: -8 },
};

const SAVED_SCENARIOS: SavedScenario[] = [
  {
    title: "Salesforce −20% pricing",
    description: "Salesforce annonce une réduction tarifaire de 20% sur toute sa gamme CRM Professional.",
    revenueImpact: -8,
    marketShareImpact: -1.4,
    churnAccounts: 27,
  },
  {
    title: "HubSpot acquisition Pipedrive",
    description: "HubSpot acquiert Pipedrive pour consolider sa position sur le segment PME/Mid-Market.",
    revenueImpact: -6,
    marketShareImpact: -2.1,
    churnAccounts: 38,
  },
  {
    title: "Nouveau entrant freemium",
    description: "Un nouvel acteur bien financé lance une offre gratuite illimitée ciblant votre cœur de marché.",
    revenueImpact: -11,
    marketShareImpact: -2.8,
    churnAccounts: 23,
  },
];

// ─── Deterministic calculation ────────────────────────────────────────────────

function calculateImpact(
  competitorId: string,
  action: Action,
  intensity: number,
  timeline: Timeline
): SimulationResult {
  const competitor = competitors.find((c) => c.id === competitorId)!;
  const base = ACTION_BASE[action];
  const timeM = TIMELINE_MULTIPLIER[timeline];

  // Threat multiplier: high=1.3, medium=1.0, low=0.7
  const threatMap: Record<string, number> = { high: 1.3, medium: 1.0, low: 0.7 };
  const threatM = threatMap[competitor.threatLevel] ?? 1.0;

  // Intensity normalized 1-10 → 0.4-1.6
  const intensityM = 0.4 + (intensity - 1) * (1.2 / 9);

  const rawRevenue = base.revenue * timeM * threatM * intensityM;
  const rawMarket = base.market * timeM * threatM * intensityM;
  const rawChurn = base.churn * timeM * threatM * intensityM;

  // Round and clamp
  const revenueImpact = Math.max(-40, Math.min(15, Math.round(rawRevenue * 100) / 10 * 10) / 10);
  const marketShareImpact = Math.round(rawMarket * 10) / 10;
  const churnAccounts = Math.max(0, Math.min(340, Math.round(rawChurn)));

  // Response delay based on timeline
  let responseDelay: SimulationResult["responseDelay"];
  if (timeline === "1m") responseDelay = "Immédiat";
  else if (timeline === "3m") responseDelay = "30 jours";
  else responseDelay = "90 jours";

  // Action plan generation (deterministic, based on action type + intensity)
  const actionPlans: Record<Action, SimulationResult["actions"]> = {
    price_cut: [
      { label: `Auditer l'écart de valeur perçue avec ${competitor.name} et renforcer le ROI deck`, priority: "URGENT" },
      { label: "Lancer une campagne de rétention ciblant les comptes à risque identifiés", priority: "URGENT" },
      { label: "Mettre à jour la grille tarifaire avec options de bundle défensif", priority: "IMPORTANT" },
      { label: "Préparer un playbook de contre-arguments pour l'équipe commerciale", priority: "IMPORTANT" },
      { label: "Surveiller les signaux d'intérêt des prospects pour la prochaine période", priority: "À PLANIFIER" },
    ],
    new_feature: [
      { label: `Analyser la nouvelle feature ${competitor.name} et identifier les gaps produit`, priority: "URGENT" },
      { label: "Accélérer la roadmap sur les features similaires ou complémentaires", priority: "IMPORTANT" },
      { label: "Communiquer proactivement sur votre différenciation unique auprès des clients", priority: "IMPORTANT" },
      { label: "Planifier une session war room produit avec l'équipe R&D", priority: "À PLANIFIER" },
    ],
    acquisition: [
      { label: `Cartographier les clients communs exposés à la consolidation ${competitor.name}`, priority: "URGENT" },
      { label: "Accélérer les conversations en cours avec les comptes stratégiques", priority: "URGENT" },
      { label: "Préparer un narratif de positionnement post-acquisition pour le marché", priority: "IMPORTANT" },
      { label: "Identifier et approcher les clients insatisfaits de la cible acquise", priority: "IMPORTANT" },
      { label: "Surveiller l'intégration produit et les frictions potentielles chez l'acquéreur", priority: "À PLANIFIER" },
    ],
    fundraising: [
      { label: "Évaluer l'allocation probable des fonds (R&D, sales, M&A) et anticiper les mouvements", priority: "URGENT" },
      { label: "Renforcer les relations avec vos investisseurs actuels et prospects", priority: "IMPORTANT" },
      { label: "Accélérer les initiatives de croissance pour maintenir l'écart de momentum", priority: "IMPORTANT" },
      { label: "Mettre en place une veille mensuelle renforcée sur les actions de ce concurrent", priority: "À PLANIFIER" },
    ],
    freemium: [
      { label: "Évaluer l'impact immédiat sur votre funnel d'acquisition et ajuster les CPA cibles", priority: "URGENT" },
      { label: "Lancer une contre-offensive sur la valeur entreprise et le coût total de possession", priority: "URGENT" },
      { label: `Créer du contenu comparatif mettant en valeur les limites du freemium ${competitor.name}`, priority: "IMPORTANT" },
      { label: "Proposer une offre d'essai étendue aux prospects hésitants", priority: "IMPORTANT" },
      { label: "Analyser le taux de conversion freemium → payant historique de ce concurrent", priority: "À PLANIFIER" },
    ],
    exit_segment: [
      { label: `Identifier et contacter en priorité les clients ${competitor.name} dans ce segment`, priority: "URGENT" },
      { label: "Préparer un package de migration attractif avec onboarding accéléré", priority: "URGENT" },
      { label: "Renforcer la présence marketing dans ce segment pour capturer la demande orpheline", priority: "IMPORTANT" },
      { label: "Documenter les cas clients récupérés comme preuves sociales", priority: "À PLANIFIER" },
    ],
  };

  // Adjust action count based on intensity
  const maxActions = intensity >= 8 ? 5 : intensity >= 5 ? 4 : 3;
  const actions = actionPlans[action].slice(0, maxActions);

  return { revenueImpact, marketShareImpact, churnAccounts, responseDelay, actions };
}

// ─── Sub-components ───────────────────────────────────────────────────────────

function PriorityBadge({ priority }: { priority: "URGENT" | "IMPORTANT" | "À PLANIFIER" }) {
  if (priority === "URGENT")
    return (
      <span className="flex-shrink-0 text-[10px] font-bold px-2 py-0.5 rounded-full bg-red-100 text-red-700 border border-red-200 tracking-wide">
        URGENT
      </span>
    );
  if (priority === "IMPORTANT")
    return (
      <span className="flex-shrink-0 text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-100 text-amber-700 border border-amber-200 tracking-wide">
        IMPORTANT
      </span>
    );
  return (
    <span className="flex-shrink-0 text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-500 border border-slate-200 tracking-wide">
      À PLANIFIER
    </span>
  );
}

interface AnimatedBarProps {
  value: number; // 0-100
  color: string; // tailwind bg class
  delay?: number;
  animate: boolean;
}

function AnimatedBar({ value, color, delay = 0, animate }: AnimatedBarProps) {
  const [width, setWidth] = useState(0);

  useEffect(() => {
    if (!animate) { setWidth(0); return; }
    const t = setTimeout(() => setWidth(value), delay);
    return () => clearTimeout(t);
  }, [animate, value, delay]);

  return (
    <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
      <div
        className={`h-full rounded-full ${color} transition-all duration-700 ease-out`}
        style={{ width: `${width}%` }}
      />
    </div>
  );
}

function MetricCard({
  label,
  value,
  sub,
  barValue,
  barColor,
  animate,
  delay,
}: {
  label: string;
  value: string;
  sub?: string;
  barValue: number;
  barColor: string;
  animate: boolean;
  delay?: number;
}) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-4 space-y-3">
      <div className="text-xs font-medium text-slate-500 uppercase tracking-wide">{label}</div>
      <div className="flex items-end justify-between gap-2">
        <span className="text-2xl font-bold text-slate-900 leading-none">{value}</span>
        {sub && <span className="text-xs text-slate-400 mb-0.5">{sub}</span>}
      </div>
      <AnimatedBar value={barValue} color={barColor} animate={animate} delay={delay} />
    </div>
  );
}

function IconTarget({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm0-2a6 6 0 100-12 6 6 0 000 12zm0-2a4 4 0 100-8 4 4 0 000 8zm0-2a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
    </svg>
  );
}

function IconZap({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" />
    </svg>
  );
}

function IconClock({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
    </svg>
  );
}

function IconCheckCircle({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
    </svg>
  );
}

function IconSave({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path d="M7.707 10.293a1 1 0 10-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 11.586V6h5a2 2 0 012 2v7a2 2 0 01-2 2H4a2 2 0 01-2-2V8a2 2 0 012-2h5v5.586l-1.293-1.293z" />
    </svg>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function SimulatePage() {
  const [competitorId, setCompetitorId] = useState(competitors[0].id);
  const [action, setAction] = useState<Action>("price_cut");
  const [intensity, setIntensity] = useState(5);
  const [timeline, setTimeline] = useState<Timeline>("3m");
  const [simulating, setSimulating] = useState(false);
  const [result, setResult] = useState<SimulationResult | null>(null);
  const [animateBars, setAnimateBars] = useState(false);
  const resultsRef = useRef<HTMLDivElement>(null);

  function handleSimulate() {
    setSimulating(true);
    setAnimateBars(false);
    setResult(null);

    // Simulate "thinking" delay for UX
    setTimeout(() => {
      const r = calculateImpact(competitorId, action, intensity, timeline);
      setResult(r);
      setSimulating(false);
      setTimeout(() => {
        setAnimateBars(true);
        resultsRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 80);
    }, 900);
  }

  const selectedCompetitor = competitors.find((c) => c.id === competitorId)!;

  // Derive bar values (0-100 scale)
  function revenueBarValue(pct: number) {
    // pct is negative for loss, map -40..+15 to 0-100 bar
    if (pct >= 0) return Math.min(100, Math.round((pct / 15) * 30 + 70));
    return Math.max(0, Math.round(100 + (pct / 40) * 100));
  }
  function revenueBarColor(pct: number) {
    if (pct >= 0) return "bg-emerald-500";
    if (pct > -10) return "bg-amber-400";
    return "bg-red-500";
  }
  function marketBarColor(pts: number) {
    if (pts >= 0) return "bg-emerald-500";
    if (pts > -1.5) return "bg-amber-400";
    return "bg-red-500";
  }
  function churnBarColor(accounts: number) {
    if (accounts <= 10) return "bg-emerald-500";
    if (accounts <= 30) return "bg-amber-400";
    return "bg-red-500";
  }
  function responseColor(delay: string) {
    if (delay === "Immédiat") return "text-red-600 bg-red-50 border-red-200";
    if (delay === "30 jours") return "text-amber-600 bg-amber-50 border-amber-200";
    return "text-emerald-700 bg-emerald-50 border-emerald-200";
  }

  return (
    <div className="space-y-8 pb-12">
      {/* ── Header ── */}
      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
            Simulateur de Scénarios Concurrentiels
          </h1>
          <span className="inline-flex items-center gap-1.5 text-xs font-bold px-2.5 py-1 rounded-full bg-indigo-600 text-white shadow-sm">
            <IconZap className="w-3 h-3" />
            War Room Mode
          </span>
        </div>
        <p className="text-slate-500 text-sm max-w-2xl">
          Anticipez les mouvements de vos concurrents et préparez votre réponse avant qu&apos;ils n&apos;agissent.
          Chaque simulation produit un plan d&apos;action calibré sur l&apos;intensité et le délai de la menace.
        </p>
      </div>

      {/* ── Two-column layout ── */}
      <div className="grid lg:grid-cols-2 gap-6 items-start">

        {/* ── Left: Configuration panel ── */}
        <div className="bg-slate-900 rounded-2xl border border-slate-700 overflow-hidden shadow-xl">
          {/* Panel header */}
          <div className="px-6 py-4 border-b border-slate-700 flex items-center gap-3">
            <div className="w-2 h-2 rounded-full bg-red-500 shadow-sm shadow-red-500/50" />
            <div className="w-2 h-2 rounded-full bg-amber-400 shadow-sm shadow-amber-400/50" />
            <div className="w-2 h-2 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400/50" />
            <span className="ml-2 text-slate-300 text-xs font-mono tracking-widest uppercase">
              Configuration du scénario
            </span>
          </div>

          <div className="p-6 space-y-6">
            {/* Competitor select */}
            <div className="space-y-2">
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                01 — Quel concurrent ?
              </label>
              <div className="relative">
                <select
                  value={competitorId}
                  onChange={(e) => setCompetitorId(e.target.value)}
                  className="w-full appearance-none bg-slate-800 border border-slate-600 rounded-lg px-4 py-3 text-slate-100 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent cursor-pointer"
                >
                  {competitors.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name} — {c.industry}
                    </option>
                  ))}
                </select>
                <div className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-slate-400">
                  <svg className="w-4 h-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </div>
              </div>
              {/* Threat level pill */}
              <div className="flex items-center gap-2">
                <span className="text-slate-500 text-xs">Niveau de menace :</span>
                <span
                  className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
                    selectedCompetitor.threatLevel === "high"
                      ? "bg-red-900/50 text-red-400 border border-red-700"
                      : selectedCompetitor.threatLevel === "medium"
                      ? "bg-amber-900/50 text-amber-400 border border-amber-700"
                      : "bg-slate-700 text-slate-400 border border-slate-600"
                  }`}
                >
                  {selectedCompetitor.threatLevel === "high"
                    ? "Élevé"
                    : selectedCompetitor.threatLevel === "medium"
                    ? "Moyen"
                    : "Faible"}
                </span>
                <span className="text-slate-600 text-xs">·</span>
                <span className="text-slate-500 text-xs">{selectedCompetitor.marketShare}% de part de marché</span>
              </div>
            </div>

            {/* Action select */}
            <div className="space-y-2">
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                02 — Que font-ils ?
              </label>
              <div className="relative">
                <select
                  value={action}
                  onChange={(e) => setAction(e.target.value as Action)}
                  className="w-full appearance-none bg-slate-800 border border-slate-600 rounded-lg px-4 py-3 text-slate-100 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent cursor-pointer"
                >
                  {ACTIONS.map((a) => (
                    <option key={a.value} value={a.value}>
                      {a.label}
                    </option>
                  ))}
                </select>
                <div className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-slate-400">
                  <svg className="w-4 h-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </div>
              </div>
            </div>

            {/* Intensity slider */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  03 — Intensité
                </label>
                <div className="flex items-center gap-1.5">
                  <span
                    className={`text-lg font-bold tabular-nums ${
                      intensity >= 8
                        ? "text-red-400"
                        : intensity >= 5
                        ? "text-amber-400"
                        : "text-emerald-400"
                    }`}
                  >
                    {intensity}
                  </span>
                  <span className="text-slate-500 text-xs">/ 10</span>
                </div>
              </div>
              <div className="relative">
                <input
                  type="range"
                  min={1}
                  max={10}
                  value={intensity}
                  onChange={(e) => setIntensity(Number(e.target.value))}
                  className="w-full h-2 rounded-full appearance-none cursor-pointer accent-indigo-500"
                  style={{
                    background: `linear-gradient(to right, ${
                      intensity >= 8 ? "#ef4444" : intensity >= 5 ? "#f59e0b" : "#10b981"
                    } 0%, ${
                      intensity >= 8 ? "#ef4444" : intensity >= 5 ? "#f59e0b" : "#10b981"
                    } ${((intensity - 1) / 9) * 100}%, #334155 ${((intensity - 1) / 9) * 100}%, #334155 100%)`,
                  }}
                />
                <div className="flex justify-between mt-1.5">
                  <span className="text-[10px] text-slate-600">Faible</span>
                  <span className="text-[10px] text-slate-600">Modéré</span>
                  <span className="text-[10px] text-slate-600">Extrême</span>
                </div>
              </div>
            </div>

            {/* Timeline */}
            <div className="space-y-2">
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                04 — Dans quel délai ?
              </label>
              <div className="grid grid-cols-4 gap-2">
                {TIMELINES.map((t) => (
                  <button
                    key={t.value}
                    onClick={() => setTimeline(t.value)}
                    className={`py-2.5 rounded-lg text-xs font-semibold border transition-all duration-150 cursor-pointer ${
                      timeline === t.value
                        ? "bg-indigo-600 border-indigo-500 text-white shadow-lg shadow-indigo-900/40"
                        : "bg-slate-800 border-slate-600 text-slate-400 hover:border-slate-500 hover:text-slate-300"
                    }`}
                  >
                    {t.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Simulate button */}
            <button
              onClick={handleSimulate}
              disabled={simulating}
              className="w-full py-3.5 rounded-xl font-bold text-sm text-white relative overflow-hidden transition-all duration-200 cursor-pointer disabled:cursor-not-allowed disabled:opacity-70 active:scale-[0.99]"
              style={{
                background: simulating
                  ? "linear-gradient(135deg, #4338ca, #6d28d9)"
                  : "linear-gradient(135deg, #4f46e5, #7c3aed)",
                boxShadow: simulating ? "none" : "0 4px 24px rgba(99,102,241,0.4)",
              }}
            >
              <span className="flex items-center justify-center gap-2">
                {simulating ? (
                  <>
                    <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                    Simulation en cours…
                  </>
                ) : (
                  <>
                    <IconTarget className="w-4 h-4" />
                    Simuler l&apos;impact
                  </>
                )}
              </span>
            </button>
          </div>
        </div>

        {/* ── Right: Results panel ── */}
        <div ref={resultsRef} className="space-y-5">
          {!result && !simulating && (
            <div className="bg-white rounded-2xl border border-slate-200 border-dashed p-12 flex flex-col items-center justify-center text-center gap-4">
              <div className="w-14 h-14 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-center">
                <IconTarget className="w-7 h-7 text-slate-300" />
              </div>
              <div>
                <p className="text-slate-500 text-sm font-medium">Aucune simulation lancée</p>
                <p className="text-slate-400 text-xs mt-1">
                  Configurez un scénario à gauche et cliquez sur &quot;Simuler l&apos;impact&quot;
                </p>
              </div>
            </div>
          )}

          {simulating && (
            <div className="space-y-4 animate-pulse">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="bg-white rounded-xl border border-slate-200 p-4 h-24" />
              ))}
            </div>
          )}

          {result && !simulating && (
            <>
              {/* Scenario banner */}
              <div className="bg-indigo-50 border border-indigo-200 rounded-xl px-4 py-3 flex items-center gap-3">
                <IconZap className="w-4 h-4 text-indigo-500 flex-shrink-0" />
                <div className="min-w-0">
                  <span className="text-indigo-700 font-semibold text-sm">
                    {selectedCompetitor.name}
                  </span>
                  <span className="text-indigo-500 text-sm mx-1.5">—</span>
                  <span className="text-indigo-600 text-sm">
                    {ACTIONS.find((a) => a.value === action)?.label}
                  </span>
                  <span className="text-indigo-400 text-xs ml-2">
                    · Intensité {intensity}/10 · {TIMELINES.find((t) => t.value === timeline)?.label}
                  </span>
                </div>
              </div>

              {/* 4 Metric cards */}
              <div className="grid grid-cols-2 gap-4">
                <MetricCard
                  label="Impact chiffre d'affaires"
                  value={`${result.revenueImpact > 0 ? "+" : ""}${result.revenueImpact}%`}
                  barValue={revenueBarValue(result.revenueImpact)}
                  barColor={revenueBarColor(result.revenueImpact)}
                  animate={animateBars}
                  delay={0}
                />
                <MetricCard
                  label="Impact parts de marché"
                  value={`${result.marketShareImpact > 0 ? "+" : ""}${result.marketShareImpact} pts`}
                  barValue={Math.max(0, Math.min(100, Math.round(50 + result.marketShareImpact * 10)))}
                  barColor={marketBarColor(result.marketShareImpact)}
                  animate={animateBars}
                  delay={120}
                />
                <MetricCard
                  label="Clients à risque de churn"
                  value={`${Math.max(0, result.churnAccounts)}`}
                  sub="sur 340 comptes"
                  barValue={Math.max(0, Math.min(100, Math.round((result.churnAccounts / 340) * 100)))}
                  barColor={churnBarColor(result.churnAccounts)}
                  animate={animateBars}
                  delay={240}
                />
                <div className="bg-white rounded-xl border border-slate-200 p-4 space-y-3">
                  <div className="text-xs font-medium text-slate-500 uppercase tracking-wide">
                    Délai de réponse recommandé
                  </div>
                  <div className="pt-1">
                    <span
                      className={`inline-flex items-center gap-1.5 text-sm font-bold px-3 py-1.5 rounded-lg border ${responseColor(result.responseDelay)}`}
                    >
                      <IconClock className="w-3.5 h-3.5" />
                      {result.responseDelay}
                    </span>
                  </div>
                  <div className="h-2 w-full bg-slate-100 rounded-full" />
                </div>
              </div>

              {/* Action plan */}
              <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
                <div className="px-5 py-3.5 border-b border-slate-100 flex items-center gap-2">
                  <IconCheckCircle className="w-4 h-4 text-indigo-500" />
                  <span className="text-sm font-semibold text-slate-800">Plan de réponse recommandé</span>
                </div>
                <div className="divide-y divide-slate-100">
                  {result.actions.map((item, i) => (
                    <div key={i} className="flex items-start gap-3 px-5 py-3.5">
                      <div className="flex-shrink-0 w-5 h-5 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center mt-0.5">
                        <span className="text-[10px] font-bold text-slate-500">{i + 1}</span>
                      </div>
                      <p className="flex-1 text-sm text-slate-700 leading-relaxed">{item.label}</p>
                      <PriorityBadge priority={item.priority} />
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      </div>

      {/* ── Saved scenarios ── */}
      <div className="space-y-4">
        <div className="flex items-center gap-3">
          <IconSave className="w-4 h-4 text-slate-400" />
          <h2 className="text-base font-semibold text-slate-800">Scénarios pré-calculés</h2>
          <span className="text-xs text-slate-400 font-medium">Analyses de référence — lecture seule</span>
        </div>
        <div className="grid md:grid-cols-3 gap-4">
          {SAVED_SCENARIOS.map((s, i) => (
            <div
              key={i}
              className="bg-white rounded-xl border border-slate-200 p-5 space-y-4 hover:border-indigo-200 hover:shadow-sm transition-all duration-150"
            >
              {/* Title */}
              <div>
                <div className="flex items-center gap-2 mb-1.5">
                  <div className="w-2 h-2 rounded-full bg-indigo-500" />
                  <span className="text-sm font-semibold text-slate-800">{s.title}</span>
                </div>
                <p className="text-xs text-slate-500 leading-relaxed">{s.description}</p>
              </div>

              {/* Metrics row */}
              <div className="grid grid-cols-3 gap-2">
                <div className="text-center">
                  <div className="text-lg font-bold text-red-600">{s.revenueImpact}%</div>
                  <div className="text-[10px] text-slate-400 font-medium uppercase tracking-wide mt-0.5">CA</div>
                </div>
                <div className="text-center border-x border-slate-100">
                  <div className="text-lg font-bold text-amber-600">{s.marketShareImpact} pts</div>
                  <div className="text-[10px] text-slate-400 font-medium uppercase tracking-wide mt-0.5">Marché</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-red-600">−{s.churnAccounts}</div>
                  <div className="text-[10px] text-slate-400 font-medium uppercase tracking-wide mt-0.5">Comptes</div>
                </div>
              </div>

              {/* Impact bar */}
              <div className="space-y-1">
                <div className="text-[10px] text-slate-400 font-medium uppercase tracking-wide">Impact CA</div>
                <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-red-400 rounded-full"
                    style={{ width: `${Math.min(100, Math.abs(s.revenueImpact) * 4)}%` }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
