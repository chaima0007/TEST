"use client";

import { useState } from "react";

// ─── Types ───────────────────────────────────────────────────────────────────

type SignalType = "recrutement" | "brevet" | "domaine" | "linkedin" | "investissement" | "partenariat";
type ConfidenceLevel = "low" | "medium" | "high";

interface Signal {
  id: string;
  competitorId: string;
  competitorName: string;
  competitorLogo: string;
  competitorColor: string;
  type: SignalType;
  description: string;
  interpretation: string;
  confidence: number;
  date: string;
  isNew?: boolean;
}

interface Prediction {
  id: string;
  competitorName: string;
  competitorColor: string;
  competitorLogo: string;
  prediction: string;
  probability: number;
  horizon: string;
}

// ─── Mock data ────────────────────────────────────────────────────────────────

const SIGNALS: Signal[] = [
  {
    id: "s1",
    competitorId: "1",
    competitorName: "Salesforce",
    competitorLogo: "SF",
    competitorColor: "#00A1E0",
    type: "recrutement",
    description: "Salesforce a publié 23 offres d'emploi pour des ingénieurs NLP et ML en 4 semaines — tous rattachés à l'équipe Einstein AI.",
    interpretation: "→ Forte probabilité d'un module IA de pricing ou de forecasting intégré dans les 8 mois.",
    confidence: 92,
    date: "2026-06-16",
    isNew: true,
  },
  {
    id: "s2",
    competitorId: "1",
    competitorName: "Salesforce",
    competitorLogo: "SF",
    competitorColor: "#00A1E0",
    type: "brevet",
    description: "Salesforce a déposé 3 brevets USPTO autour de la 'dynamic revenue optimization via generative AI' entre avril et juin 2026.",
    interpretation: "→ Signal d'un produit de Revenue Intelligence de nouvelle génération, concurrent direct de Clari et Gong.",
    confidence: 78,
    date: "2026-06-10",
    isNew: true,
  },
  {
    id: "s3",
    competitorId: "2",
    competitorName: "HubSpot",
    competitorLogo: "HS",
    competitorColor: "#FF7A59",
    type: "investissement",
    description: "HubSpot a levé 340 M$ en dette convertible auprès de Goldman Sachs, non annoncé publiquement — source : SEC filing du 05/06/2026.",
    interpretation: "→ Précède généralement une grande acquisition ou un round Série D. Horizon estimé : 2-3 mois.",
    confidence: 65,
    date: "2026-06-05",
    isNew: true,
  },
  {
    id: "s4",
    competitorId: "2",
    competitorName: "HubSpot",
    competitorLogo: "HS",
    competitorColor: "#FF7A59",
    type: "linkedin",
    description: "Le VP Engineering de HubSpot a quitté l'entreprise silencieusement après 7 ans. Trois directeurs techniques ont mis à jour leur profil LinkedIn vers 'Open to Work'.",
    interpretation: "→ Restructuring interne probable, possiblement lié à une réorganisation pré-IPO ou post-acquisition.",
    confidence: 54,
    date: "2026-06-02",
  },
  {
    id: "s5",
    competitorId: "3",
    competitorName: "Pipedrive",
    competitorLogo: "PD",
    competitorColor: "#2C3E50",
    type: "domaine",
    description: "Pipedrive a enregistré 6 nouveaux domaines : pipedrive-ai.com, pdai.io, pipedrive-intelligence.com et 3 variantes — tous le même jour.",
    interpretation: "→ Lancement prochain d'une offre IA standalone ou d'une suite 'Pipedrive AI' distincte du core product.",
    confidence: 71,
    date: "2026-05-28",
  },
  {
    id: "s6",
    competitorId: "3",
    competitorName: "Pipedrive",
    competitorLogo: "PD",
    competitorColor: "#2C3E50",
    type: "partenariat",
    description: "Pipedrive a passé une certification AWS ISV Accelerate et un accord Marketplace avec Microsoft Azure, détectés via les registres publics des deux clouds.",
    interpretation: "→ Préparation d'une distribution via les marketplaces cloud — stratégie d'acquisition channel B2B pour 2027.",
    confidence: 83,
    date: "2026-05-20",
  },
  {
    id: "s7",
    competitorId: "4",
    competitorName: "Zoho CRM",
    competitorLogo: "ZO",
    competitorColor: "#E42527",
    type: "recrutement",
    description: "Zoho recrute massivement en Europe : 14 postes ouverts à Dublin et Amsterdam (Sales, Success, Marketing) — pic inhabituel par rapport à la baseline.",
    interpretation: "→ Expansion géographique agressive en Europe de l'Ouest, potentiellement accompagnée d'une offre localisée.",
    confidence: 88,
    date: "2026-05-15",
  },
  {
    id: "s8",
    competitorId: "5",
    competitorName: "Monday.com",
    competitorLogo: "MN",
    competitorColor: "#F6517C",
    type: "brevet",
    description: "Monday.com a déposé 2 brevets autour de 'AI-driven workflow orchestration' et 'natural language pipeline creation' — USPTO, mai 2026.",
    interpretation: "→ Pivot vers un CRM conversationnel full-IA — menace directe sur les segments mid-market d'ici 12-18 mois.",
    confidence: 47,
    date: "2026-05-10",
  },
  {
    id: "s9",
    competitorId: "2",
    competitorName: "HubSpot",
    competitorLogo: "HS",
    competitorColor: "#FF7A59",
    type: "partenariat",
    description: "HubSpot a silencieusement intégré OpenAI GPT-5 dans ses APIs internes — détecté via les changelogs privés de sandbox partenaires.",
    interpretation: "→ Annonce publique imminente d'une suite IA générative native, probablement à INBOUND 2026 en septembre.",
    confidence: 91,
    date: "2026-05-07",
    isNew: false,
  },
  {
    id: "s10",
    competitorId: "1",
    competitorName: "Salesforce",
    competitorLogo: "SF",
    competitorColor: "#00A1E0",
    type: "linkedin",
    description: "L'ex-CPO de Stripe a rejoint Salesforce comme SVP Product — profile validé LinkedIn + annonce interne Slack leakée.",
    interpretation: "→ Renforcement du leadership produit dans le segment Fintech/payments — probable lancement d'une offre billing intégrée.",
    confidence: 76,
    date: "2026-04-30",
  },
];

const PREDICTIONS: Prediction[] = [
  {
    id: "p1",
    competitorName: "Salesforce",
    competitorColor: "#00A1E0",
    competitorLogo: "SF",
    prediction: "Lancement d'un module IA de pricing et forecasting natif (Einstein Revenue Cloud v2)",
    probability: 78,
    horizon: "4–6 mois",
  },
  {
    id: "p2",
    competitorName: "HubSpot",
    competitorColor: "#FF7A59",
    competitorLogo: "HS",
    prediction: "Levée de fonds Série D ou acquisition majeure d'un outil de data enrichment",
    probability: 65,
    horizon: "2–3 mois",
  },
  {
    id: "p3",
    competitorName: "Pipedrive",
    competitorColor: "#2C3E50",
    competitorLogo: "PD",
    prediction: "Acquisition par un fonds PE ou par un acteur cloud (AWS, SAP) — consolidation du marché mid-market",
    probability: 43,
    horizon: "6–12 mois",
  },
];

// ─── Helpers ──────────────────────────────────────────────────────────────────

function formatRelativeTime(dateStr: string): string {
  const date = new Date(dateStr);
  const now = new Date("2026-06-18");
  const diffMs = now.getTime() - date.getTime();
  const days = Math.floor(diffMs / 86400000);
  if (days === 0) return "Aujourd'hui";
  if (days === 1) return "Hier";
  if (days < 7) return `Il y a ${days} jours`;
  if (days < 14) return "Il y a 1 semaine";
  if (days < 30) return `Il y a ${Math.floor(days / 7)} semaines`;
  return `Il y a ${Math.floor(days / 30)} mois`;
}

function getConfidenceLevel(score: number): ConfidenceLevel {
  if (score >= 75) return "high";
  if (score >= 50) return "medium";
  return "low";
}

function confidenceStyle(score: number): { bg: string; text: string; ring: string } {
  const level = getConfidenceLevel(score);
  if (level === "high") return { bg: "bg-emerald-50", text: "text-emerald-700", ring: "ring-emerald-200" };
  if (level === "medium") return { bg: "bg-amber-50", text: "text-amber-700", ring: "ring-amber-200" };
  return { bg: "bg-red-50", text: "text-red-700", ring: "ring-red-200" };
}

const TYPE_META: Record<SignalType, { label: string; iconBg: string; iconColor: string; icon: React.ReactNode }> = {
  recrutement: {
    label: "Recrutement",
    iconBg: "bg-blue-100",
    iconColor: "text-blue-600",
    icon: (
      <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
        <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
      </svg>
    ),
  },
  brevet: {
    label: "Brevet",
    iconBg: "bg-violet-100",
    iconColor: "text-violet-600",
    icon: (
      <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
        <path fillRule="evenodd" d="M10 2a1 1 0 00-1 1v1a1 1 0 002 0V3a1 1 0 00-1-1zM4 4h3a3 3 0 006 0h3a2 2 0 012 2v9a2 2 0 01-2 2H4a2 2 0 01-2-2V6a2 2 0 012-2zm2.5 7a1.5 1.5 0 100-3 1.5 1.5 0 000 3zm2.45 4a2.5 2.5 0 10-4.9 0h4.9zM12 9a1 1 0 100 2h3a1 1 0 100-2h-3zm-1 4a1 1 0 011-1h2a1 1 0 110 2h-2a1 1 0 01-1-1z" clipRule="evenodd" />
      </svg>
    ),
  },
  domaine: {
    label: "Domaine",
    iconBg: "bg-cyan-100",
    iconColor: "text-cyan-600",
    icon: (
      <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
        <path fillRule="evenodd" d="M4.083 9h1.946c.089-1.546.383-2.97.837-4.118A6.004 6.004 0 004.083 9zM10 2a8 8 0 100 16A8 8 0 0010 2zm0 2c-.076 0-.232.032-.465.262-.238.234-.497.623-.737 1.182-.389.907-.673 2.142-.766 3.556h3.936c-.093-1.414-.377-2.649-.766-3.556-.24-.56-.5-.948-.737-1.182C10.232 4.032 10.076 4 10 4zm3.971 5c-.089-1.546-.383-2.97-.837-4.118A6.004 6.004 0 0115.917 9h-1.946zm-2.003 2H8.032c.093 1.414.377 2.649.766 3.556.24.56.5.948.737 1.182.233.23.389.262.465.262.076 0 .232-.032.465-.262.238-.234.498-.623.737-1.182.389-.907.673-2.142.766-3.556zm1.166 4.118c.454-1.147.748-2.572.837-4.118h1.946a6.004 6.004 0 01-2.783 4.118zm-6.268 0C6.412 13.97 6.118 12.546 6.03 11H4.083a6.004 6.004 0 002.783 4.118z" clipRule="evenodd" />
      </svg>
    ),
  },
  linkedin: {
    label: "LinkedIn",
    iconBg: "bg-sky-100",
    iconColor: "text-sky-700",
    icon: (
      <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
        <path fillRule="evenodd" d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v3.57A22.952 22.952 0 0110 13a22.95 22.95 0 01-8-1.43V8a2 2 0 012-2h2zm2-1a1 1 0 011-1h2a1 1 0 011 1v1H8V5zm1 5a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1z" clipRule="evenodd" />
        <path d="M2 13.692V16a2 2 0 002 2h12a2 2 0 002-2v-2.308A24.974 24.974 0 0110 15c-2.796 0-5.487-.46-8-1.308z" />
      </svg>
    ),
  },
  investissement: {
    label: "Investissement",
    iconBg: "bg-emerald-100",
    iconColor: "text-emerald-600",
    icon: (
      <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
        <path fillRule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clipRule="evenodd" />
      </svg>
    ),
  },
  partenariat: {
    label: "Partenariat",
    iconBg: "bg-orange-100",
    iconColor: "text-orange-600",
    icon: (
      <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
        <path d="M11 6a3 3 0 11-6 0 3 3 0 016 0zM14 8a2 2 0 100 4 2 2 0 000-4zM10.5 10.5a5 5 0 00-5 5v.5a.5.5 0 00.5.5h9a.5.5 0 00.5-.5v-.5a5 5 0 00-5-5z" />
      </svg>
    ),
  },
};

const ALL_COMPETITORS = [
  { id: "1", name: "Salesforce", logo: "SF", color: "#00A1E0" },
  { id: "2", name: "HubSpot", logo: "HS", color: "#FF7A59" },
  { id: "3", name: "Pipedrive", logo: "PD", color: "#2C3E50" },
  { id: "4", name: "Zoho CRM", logo: "ZO", color: "#E42527" },
  { id: "5", name: "Monday.com", logo: "MN", color: "#F6517C" },
];

const ALL_TYPES: SignalType[] = ["recrutement", "brevet", "domaine", "linkedin", "investissement", "partenariat"];
const CONFIDENCE_FILTERS = [
  { label: "> 50%", min: 50 },
  { label: "> 70%", min: 70 },
  { label: "> 90%", min: 90 },
];

// ─── Sub-components ───────────────────────────────────────────────────────────

function ThreatGauge({ score }: { score: number }) {
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  // We only use 75% of the circle (270°) for the gauge arc
  const arcLength = circumference * 0.75;
  const filled = arcLength * (score / 100);
  const empty = arcLength - filled;
  // Rotate so the arc starts at 135° (bottom-left)
  const rotation = 135;

  // Color gradient: low = emerald, mid = amber, high = red
  let color = "#10b981";
  if (score >= 60) color = "#f59e0b";
  if (score >= 75) color = "#ef4444";

  return (
    <div className="relative w-36 h-36 flex items-center justify-center">
      <svg width="144" height="144" viewBox="0 0 144 144" className="absolute inset-0">
        {/* Track */}
        <circle
          cx="72" cy="72" r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.1)"
          strokeWidth="10"
          strokeDasharray={`${arcLength} ${circumference}`}
          strokeDashoffset="0"
          strokeLinecap="round"
          transform={`rotate(${rotation} 72 72)`}
        />
        {/* Fill */}
        <circle
          cx="72" cy="72" r={radius}
          fill="none"
          stroke={color}
          strokeWidth="10"
          strokeDasharray={`${filled} ${empty + circumference * 0.25}`}
          strokeDashoffset="0"
          strokeLinecap="round"
          transform={`rotate(${rotation} 72 72)`}
          style={{ filter: `drop-shadow(0 0 6px ${color}88)` }}
        />
      </svg>
      <div className="relative text-center z-10">
        <span className="block text-3xl font-bold text-white leading-none">{score}</span>
        <span className="block text-[11px] text-slate-400 font-medium mt-0.5">/ 100</span>
      </div>
    </div>
  );
}

function SignalCard({ signal }: { signal: Signal }) {
  const meta = TYPE_META[signal.type];
  const cs = confidenceStyle(signal.confidence);

  return (
    <div
      className={`bg-white rounded-xl border border-slate-200 p-5 hover:shadow-md transition-all duration-200 relative overflow-hidden${signal.isNew ? " ring-1 ring-blue-200" : ""}`}
    >
      {/* New pulse indicator */}
      {signal.isNew && (
        <span className="absolute top-4 right-4 flex h-2.5 w-2.5">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75" />
          <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-blue-500" />
        </span>
      )}

      <div className="flex items-start gap-4">
        {/* Source icon */}
        <div className={`w-10 h-10 rounded-lg ${meta.iconBg} ${meta.iconColor} flex items-center justify-center flex-shrink-0 mt-0.5`}>
          {meta.icon}
        </div>

        <div className="flex-1 min-w-0">
          {/* Header row */}
          <div className="flex flex-wrap items-center gap-2 mb-2">
            {/* Competitor badge */}
            <span
              className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-white text-[11px] font-bold"
              style={{ backgroundColor: signal.competitorColor }}
            >
              <span className="w-4 h-4 rounded-full bg-white/20 flex items-center justify-center text-[9px] font-black">
                {signal.competitorLogo[0]}
              </span>
              {signal.competitorName}
            </span>

            {/* Type tag */}
            <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold ${meta.iconBg} ${meta.iconColor}`}>
              {meta.label}
            </span>

            {/* Confidence badge */}
            <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-bold ring-1 ${cs.bg} ${cs.text} ${cs.ring}`}>
              {signal.confidence}% confiance
            </span>

            {/* Date */}
            <span className="text-[11px] text-slate-400 ml-auto">{formatRelativeTime(signal.date)}</span>
          </div>

          {/* Description */}
          <p className="text-[13.5px] text-slate-800 leading-relaxed mb-2">{signal.description}</p>

          {/* Interpretation */}
          <p className="text-[12.5px] text-slate-500 italic leading-snug border-l-2 border-slate-200 pl-3">
            {signal.interpretation}
          </p>
        </div>
      </div>
    </div>
  );
}

function PredictionCard({ pred }: { pred: Prediction }) {
  const cs = confidenceStyle(pred.probability);
  const barWidth = `${pred.probability}%`;

  return (
    <div className="relative bg-white/5 border border-white/10 rounded-xl p-5 hover:bg-white/8 transition-colors duration-200 overflow-hidden">
      {/* Subtle glow */}
      <div
        className="absolute -top-6 -right-6 w-24 h-24 rounded-full opacity-10 blur-xl"
        style={{ backgroundColor: pred.competitorColor }}
      />
      <div className="relative">
        {/* Competitor */}
        <div className="flex items-center justify-between mb-3">
          <span
            className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-white text-[11px] font-bold"
            style={{ backgroundColor: pred.competitorColor }}
          >
            {pred.competitorLogo} — {pred.competitorName}
          </span>
          <span className="text-[11px] text-slate-400 font-medium">{pred.horizon}</span>
        </div>

        {/* Prediction text */}
        <p className="text-[13px] text-white/90 leading-snug mb-4 font-medium">{pred.prediction}</p>

        {/* Probability bar */}
        <div>
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-[11px] text-slate-400 font-medium">Probabilité</span>
            <span className={`text-[13px] font-bold ${cs.text.replace("text-", "text-")} tabular-nums`} style={{ color: pred.probability >= 75 ? "#10b981" : pred.probability >= 50 ? "#f59e0b" : "#ef4444" }}>
              {pred.probability}%
            </span>
          </div>
          <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full transition-all duration-700"
              style={{
                width: barWidth,
                background: pred.probability >= 75 ? "#10b981" : pred.probability >= 50 ? "#f59e0b" : "#ef4444",
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── Main page ────────────────────────────────────────────────────────────────

export default function SignalsPage() {
  const [selectedCompetitors, setSelectedCompetitors] = useState<string[]>([]);
  const [selectedTypes, setSelectedTypes] = useState<SignalType[]>([]);
  const [minConfidence, setMinConfidence] = useState<number>(0);

  const toggleCompetitor = (id: string) =>
    setSelectedCompetitors((prev) => (prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]));

  const toggleType = (t: SignalType) =>
    setSelectedTypes((prev) => (prev.includes(t) ? prev.filter((x) => x !== t) : [...prev, t]));

  const filtered = SIGNALS.filter((s) => {
    if (selectedCompetitors.length > 0 && !selectedCompetitors.includes(s.competitorId)) return false;
    if (selectedTypes.length > 0 && !selectedTypes.includes(s.type)) return false;
    if (s.confidence < minConfidence) return false;
    return true;
  });

  const newCount = SIGNALS.filter((s) => s.isNew).length;

  return (
    <div className="space-y-6 pb-10">
      {/* ─── DARK HEADER ─────────────────────────────────────────────────────── */}
      <div
        className="rounded-2xl overflow-hidden"
        style={{ background: "linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%)" }}
      >
        <div className="px-6 py-8">
          <div className="flex flex-col lg:flex-row lg:items-center gap-8">
            {/* Left: Title + stats */}
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-8 h-8 rounded-lg bg-blue-500/20 flex items-center justify-center">
                  <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-blue-400">
                    <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" />
                  </svg>
                </div>
                <span className="text-[11px] font-bold text-blue-400 uppercase tracking-widest">Radar Prédictif</span>
                {newCount > 0 && (
                  <span className="inline-flex items-center gap-1 bg-blue-500/20 border border-blue-500/30 text-blue-300 text-[11px] font-bold px-2 py-0.5 rounded-full">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse" />
                    {newCount} nouveaux
                  </span>
                )}
              </div>
              <h1 className="text-2xl font-bold text-white mb-2 tracking-tight">Signaux Faibles</h1>
              <p className="text-[14px] text-slate-400 leading-relaxed max-w-xl">
                Détectez les mouvements concurrentiels <span className="text-slate-200 font-semibold">3 à 6 mois avant l&apos;annonce publique</span>. Chaque signal est scoré par confidence et corrélé à des événements historiques similaires.
              </p>

              {/* Signal stats row */}
              <div className="flex flex-wrap gap-6 mt-6">
                {[
                  { label: "Signaux actifs", value: SIGNALS.length, color: "text-blue-400" },
                  { label: "Haute confiance (>75%)", value: SIGNALS.filter((s) => s.confidence >= 75).length, color: "text-emerald-400" },
                  { label: "Concurrents surveillés", value: 5, color: "text-violet-400" },
                  { label: "Prédictions actives", value: PREDICTIONS.length, color: "text-amber-400" },
                ].map((stat) => (
                  <div key={stat.label}>
                    <p className={`text-2xl font-bold tabular-nums ${stat.color}`}>{stat.value}</p>
                    <p className="text-[11px] text-slate-500 font-medium mt-0.5">{stat.label}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Right: Threat gauge */}
            <div className="flex flex-col items-center gap-3 lg:pr-4">
              <ThreatGauge score={67} />
              <div className="text-center">
                <p className="text-[13px] font-bold text-white/90">Score de menace global</p>
                <p className="text-[11px] text-slate-500 mt-0.5">Niveau : <span className="text-amber-400 font-semibold">Modéré–Élevé</span></p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ─── LAYOUT: FEED + PREDICTIONS ─────────────────────────────────────── */}
      <div className="grid xl:grid-cols-[1fr_340px] gap-6 items-start">

        {/* LEFT: Filters + Signal feed */}
        <div className="space-y-4">
          {/* Filter bar */}
          <div className="bg-white rounded-xl border border-slate-200 p-4 space-y-4">
            <p className="text-[11px] font-bold text-slate-400 uppercase tracking-widest">Filtres</p>

            {/* Competitor pills */}
            <div>
              <p className="text-[12px] text-slate-500 font-medium mb-2">Par concurrent</p>
              <div className="flex flex-wrap gap-2">
                {ALL_COMPETITORS.map((c) => {
                  const active = selectedCompetitors.includes(c.id);
                  return (
                    <button
                      key={c.id}
                      onClick={() => toggleCompetitor(c.id)}
                      className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[12px] font-semibold border transition-all duration-150"
                      style={
                        active
                          ? { backgroundColor: c.color, borderColor: c.color, color: "#fff" }
                          : { backgroundColor: "transparent", borderColor: "#e2e8f0", color: "#64748b" }
                      }
                    >
                      <span
                        className="w-3.5 h-3.5 rounded-full flex items-center justify-center text-[8px] font-black"
                        style={{ backgroundColor: active ? "rgba(255,255,255,0.25)" : c.color, color: active ? "#fff" : "#fff" }}
                      >
                        {c.logo[0]}
                      </span>
                      {c.name}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Type pills */}
            <div>
              <p className="text-[12px] text-slate-500 font-medium mb-2">Par type de signal</p>
              <div className="flex flex-wrap gap-2">
                {ALL_TYPES.map((t) => {
                  const meta = TYPE_META[t];
                  const active = selectedTypes.includes(t);
                  return (
                    <button
                      key={t}
                      onClick={() => toggleType(t)}
                      className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[12px] font-semibold border transition-all duration-150 ${
                        active
                          ? `${meta.iconBg} ${meta.iconColor} border-transparent`
                          : "bg-transparent border-slate-200 text-slate-500 hover:border-slate-300"
                      }`}
                    >
                      <span className={`w-3.5 h-3.5 ${meta.iconColor}`}>{meta.icon}</span>
                      {meta.label}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Confidence filter */}
            <div>
              <p className="text-[12px] text-slate-500 font-medium mb-2">Niveau de confiance minimum</p>
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => setMinConfidence(0)}
                  className={`px-3 py-1 rounded-full text-[12px] font-semibold border transition-all duration-150 ${
                    minConfidence === 0
                      ? "bg-slate-800 text-white border-slate-800"
                      : "bg-transparent border-slate-200 text-slate-500 hover:border-slate-300"
                  }`}
                >
                  Tous
                </button>
                {CONFIDENCE_FILTERS.map((cf) => (
                  <button
                    key={cf.min}
                    onClick={() => setMinConfidence(cf.min)}
                    className={`px-3 py-1 rounded-full text-[12px] font-semibold border transition-all duration-150 ${
                      minConfidence === cf.min
                        ? cf.min >= 90
                          ? "bg-emerald-600 text-white border-emerald-600"
                          : cf.min >= 70
                          ? "bg-emerald-500 text-white border-emerald-500"
                          : "bg-amber-500 text-white border-amber-500"
                        : "bg-transparent border-slate-200 text-slate-500 hover:border-slate-300"
                    }`}
                  >
                    {cf.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Signal count */}
          <div className="flex items-center justify-between px-1">
            <p className="text-[13px] font-semibold text-slate-700">
              {filtered.length} signal{filtered.length !== 1 ? "s" : ""} affiché{filtered.length !== 1 ? "s" : ""}
            </p>
            {(selectedCompetitors.length > 0 || selectedTypes.length > 0 || minConfidence > 0) && (
              <button
                onClick={() => { setSelectedCompetitors([]); setSelectedTypes([]); setMinConfidence(0); }}
                className="text-[12px] text-blue-600 hover:text-blue-800 font-medium transition-colors"
              >
                Réinitialiser les filtres
              </button>
            )}
          </div>

          {/* Signal feed */}
          <div className="space-y-3">
            {filtered.length === 0 ? (
              <div className="bg-white rounded-xl border border-slate-200 p-10 text-center">
                <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mx-auto mb-3">
                  <svg viewBox="0 0 20 20" fill="currentColor" className="w-6 h-6 text-slate-400">
                    <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
                  </svg>
                </div>
                <p className="text-[14px] text-slate-500 font-medium">Aucun signal ne correspond à ces filtres</p>
                <p className="text-[12px] text-slate-400 mt-1">Ajustez les critères pour afficher des résultats.</p>
              </div>
            ) : (
              filtered.map((signal) => <SignalCard key={signal.id} signal={signal} />)
            )}
          </div>
        </div>

        {/* RIGHT: Predictions panel */}
        <div
          className="rounded-2xl overflow-hidden sticky top-6"
          style={{ background: "linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%)" }}
        >
          <div className="px-5 py-5 border-b border-white/10">
            <div className="flex items-center gap-2 mb-1">
              <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-amber-400">
                <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                <path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd" />
              </svg>
              <h2 className="text-[13px] font-bold text-white">Prédictions stratégiques</h2>
            </div>
            <p className="text-[11px] text-slate-400">
              Top 3 événements prédits à partir des signaux agrégés
            </p>
          </div>

          <div className="p-5 space-y-4">
            {PREDICTIONS.map((pred) => (
              <PredictionCard key={pred.id} pred={pred} />
            ))}
          </div>

          {/* Legend */}
          <div className="px-5 pb-5">
            <div className="border-t border-white/10 pt-4 space-y-2">
              <p className="text-[11px] text-slate-500 font-semibold uppercase tracking-widest mb-3">Légende confiance</p>
              {[
                { range: "> 75%", label: "Haute — Signal fort", color: "bg-emerald-500" },
                { range: "50–75%", label: "Modérée — À surveiller", color: "bg-amber-500" },
                { range: "< 50%", label: "Faible — Signal émergent", color: "bg-red-500" },
              ].map((item) => (
                <div key={item.range} className="flex items-center gap-2.5">
                  <div className={`w-2.5 h-2.5 rounded-full ${item.color} flex-shrink-0`} />
                  <span className="text-[11px] text-slate-300 font-semibold w-12">{item.range}</span>
                  <span className="text-[11px] text-slate-500">{item.label}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Disclaimer */}
          <div className="px-5 pb-5">
            <p className="text-[10px] text-slate-600 leading-relaxed">
              Les prédictions sont générées par modèles bayésiens sur signaux agrégés. Elles ne constituent pas des certitudes. Horizon de révision : 30 jours.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
