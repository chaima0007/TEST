"use client";

import { useState } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

type Scenario = "pessimistic" | "realistic" | "optimistic";

interface ScenarioData {
  label: string;
  emoji: string;
  color: string;
  colorHex: string;
  bgTint: string;
  borderTint: string;
  btnActive: string;
  accentBg: string;
  arr18: number;        // K€
  clients18: number;
  marketShare18: number;
  valuation18: number;  // M€
  arrMonthly: number[]; // 18 values in K€
}

// ─── Data ─────────────────────────────────────────────────────────────────────

const SCENARIOS: Record<Scenario, ScenarioData> = {
  pessimistic: {
    label: "Pessimiste",
    emoji: "🔴",
    color: "text-red-600",
    colorHex: "#dc2626",
    bgTint: "bg-red-50/60",
    borderTint: "border-red-100",
    btnActive: "bg-red-600 text-white border-red-600 shadow-lg shadow-red-900/20",
    accentBg: "bg-red-500",
    arr18: 480,
    clients18: 32,
    marketShare18: 2.1,
    valuation18: 3.8,
    arrMonthly: [12, 20, 30, 42, 55, 72, 90, 110, 135, 162, 192, 228, 270, 318, 368, 410, 448, 480],
  },
  realistic: {
    label: "Réaliste",
    emoji: "🟡",
    color: "text-amber-600",
    colorHex: "#d97706",
    bgTint: "bg-amber-50/60",
    borderTint: "border-amber-100",
    btnActive: "bg-amber-500 text-white border-amber-500 shadow-lg shadow-amber-900/20",
    accentBg: "bg-amber-500",
    arr18: 1200,
    clients18: 78,
    marketShare18: 5.4,
    valuation18: 9.6,
    arrMonthly: [25, 48, 82, 122, 168, 220, 278, 345, 418, 500, 590, 690, 800, 910, 1010, 1090, 1150, 1200],
  },
  optimistic: {
    label: "Optimiste",
    emoji: "🟢",
    color: "text-emerald-600",
    colorHex: "#059669",
    bgTint: "bg-emerald-50/60",
    borderTint: "border-emerald-100",
    btnActive: "bg-emerald-600 text-white border-emerald-600 shadow-lg shadow-emerald-900/20",
    accentBg: "bg-emerald-600",
    arr18: 3400,
    clients18: 215,
    marketShare18: 14.8,
    valuation18: 27.2,
    arrMonthly: [45, 105, 195, 310, 460, 640, 860, 1120, 1420, 1760, 2130, 2520, 2880, 3100, 3220, 3310, 3370, 3400],
  },
};

const MILESTONES = [
  {
    month: "M1",
    title: "Premiers clients enterprise signés",
    icon: (
      <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
        <path fillRule="evenodd" d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v3.57A22.952 22.952 0 0110 13a22.95 22.95 0 01-8-1.43V8a2 2 0 012-2h2zm2-1a1 1 0 011-1h2a1 1 0 011 1v1H8V5zm1 5a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1z" clipRule="evenodd" />
        <path d="M2 13.692V16a2 2 0 002 2h12a2 2 0 002-2v-2.308A24.974 24.974 0 0110 15c-2.796 0-5.487-.46-8-1.308z" />
      </svg>
    ),
    desc: "Signature des 3 premiers comptes ETI via réseau fondateur et warm intros investisseurs.",
    metric: "3 logos référence",
  },
  {
    month: "M3",
    title: "50K€ ARR — Break-even marketing",
    icon: (
      <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
        <path fillRule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clipRule="evenodd" />
      </svg>
    ),
    desc: "Le CAC payé se rembourse en moins de 3 mois. Activation des premiers canaux outbound.",
    metric: "CAC payback < 3 mois",
  },
  {
    month: "M6",
    title: "Premier rapport ROI client publié",
    icon: (
      <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
        <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
      </svg>
    ),
    desc: "Case study complet avec ROI mesurable (réduction coûts / gain temps) — arme de vente #1.",
    metric: "+340% conversion démo",
  },
  {
    month: "M9",
    title: "Équipe commerciale 3 personnes",
    icon: (
      <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
        <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
      </svg>
    ),
    desc: "Recrutement d'un Head of Sales + 2 AE. Pipeline qualifié à 800K€. Machine de vente opérationnelle.",
    metric: "Pipeline 800K€",
  },
  {
    month: "M12",
    title: "Levée de fonds Série A amorcée",
    icon: (
      <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
        <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z" />
        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
      </svg>
    ),
    desc: "Premiers contacts avec fonds Tier-1 (Partech, Idinvest). NRR > 120%, ARR run-rate convaincant.",
    metric: "NRR > 120%",
  },
  {
    month: "M18",
    title: "Leader sur le segment ETI français",
    icon: (
      <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
        <path fillRule="evenodd" d="M10 2l2.928 5.929 6.072.882-4.392 4.282 1.036 6.043L10 16.222l-5.644 2.914 1.036-6.043L1 8.811l6.072-.882L10 2z" clipRule="evenodd" />
      </svg>
    ),
    desc: "Référence obligatoire pour tout acheteur ETI. Prix d'excellence sectoriel. Roadmap IPO envisagée.",
    metric: "Top 3 Gartner Peer Insights",
  },
];

const ACCELERATORS = [
  {
    icon: (
      <svg viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5">
        <path d="M11 6a3 3 0 11-6 0 3 3 0 016 0zM14 8a2 2 0 100 4 2 2 0 000-4zM10.5 10.5a5 5 0 00-5 5v.5a.5.5 0 00.5.5h9a.5.5 0 00.5-.5v-.5a5 5 0 00-5-5z" />
      </svg>
    ),
    title: "Partenariat revendeur",
    subtitle: "Volume ×2.4",
    desc: "Un accord avec un intégrateur SI national (Capgemini, Sopra) multiplie le pipeline par 2.4 sans coût fixe additionnel. Activation dès M4.",
    badge: "×2.4 volume",
  },
  {
    icon: (
      <svg viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5">
        <path fillRule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z" clipRule="evenodd" />
      </svg>
    ),
    title: "Viral loop client → référence",
    subtitle: "CAC ÷3",
    desc: "Programme de parrainage structuré : chaque client satisfait génère 1.8 opportunité qualifiée. Le CAC s'effondre de 2800€ à moins de 1000€.",
    badge: "CAC ÷3",
  },
  {
    icon: (
      <svg viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5">
        <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" />
      </svg>
    ),
    title: "Feature différenciante exclusive",
    subtitle: "Churn ÷2",
    desc: "Une intégration native ERP (SAP / Sage) ou une fonctionnalité IA exclusive rend le remplacement 3× plus coûteux. Le churn mensuel passe de 2.1% à 0.8%.",
    badge: "Churn ÷2",
  },
];

// ─── SVG Growth Chart ─────────────────────────────────────────────────────────

const CHART_W = 700;
const CHART_H = 280;
const PAD_LEFT = 64;
const PAD_RIGHT = 20;
const PAD_TOP = 22;
const PAD_BOTTOM = 50;

function toPoint(idx: number, val: number, maxVal: number): { x: number; y: number } {
  return {
    x: PAD_LEFT + (idx / 17) * (CHART_W - PAD_LEFT - PAD_RIGHT),
    y: PAD_TOP + (1 - val / maxVal) * (CHART_H - PAD_TOP - PAD_BOTTOM),
  };
}

function smoothPath(data: number[], maxVal: number): string {
  const pts = data.map((v, i) => toPoint(i, v, maxVal));
  let d = `M ${pts[0].x} ${pts[0].y}`;
  for (let i = 1; i < pts.length; i++) {
    const prev = pts[i - 1];
    const curr = pts[i];
    const cpX = (prev.x + curr.x) / 2;
    d += ` C ${cpX} ${prev.y} ${cpX} ${curr.y} ${curr.x} ${curr.y}`;
  }
  return d;
}

function fillPath(data: number[], maxVal: number): string {
  const pts = data.map((v, i) => toPoint(i, v, maxVal));
  const bottomY = PAD_TOP + (CHART_H - PAD_TOP - PAD_BOTTOM);
  let d = `M ${pts[0].x} ${bottomY} L ${pts[0].x} ${pts[0].y}`;
  for (let i = 1; i < pts.length; i++) {
    const prev = pts[i - 1];
    const curr = pts[i];
    const cpX = (prev.x + curr.x) / 2;
    d += ` C ${cpX} ${prev.y} ${cpX} ${curr.y} ${curr.x} ${curr.y}`;
  }
  d += ` L ${pts[pts.length - 1].x} ${bottomY} Z`;
  return d;
}

function formatK(val: number): string {
  return val >= 1000 ? `${(val / 1000).toFixed(1)}M€` : `${val}K€`;
}

function GrowthChart({ activeScenario }: { activeScenario: Scenario }) {
  const allMax = Math.max(...SCENARIOS.optimistic.arrMonthly) * 1.1;
  const allScenarios: Scenario[] = ["pessimistic", "realistic", "optimistic"];

  const yTicks = 5;
  const yLabels = Array.from({ length: yTicks + 1 }, (_, i) => {
    const val = (allMax * i) / yTicks;
    const y = PAD_TOP + (1 - i / yTicks) * (CHART_H - PAD_TOP - PAD_BOTTOM);
    return { label: formatK(val), y };
  });

  const annotationIdxs = [5, 11, 17];

  return (
    <div className="w-full overflow-x-auto">
      <svg
        viewBox={`0 0 ${CHART_W} ${CHART_H}`}
        className="w-full"
        style={{ minWidth: 320 }}
        aria-label="Courbes ARR 18 mois"
      >
        <defs>
          {allScenarios.map((s) => (
            <linearGradient key={`grad-${s}`} id={`grad-${s}`} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={SCENARIOS[s].colorHex} stopOpacity="0.20" />
              <stop offset="100%" stopColor={SCENARIOS[s].colorHex} stopOpacity="0.01" />
            </linearGradient>
          ))}
        </defs>

        {/* Horizontal grid lines */}
        {yLabels.map(({ y }, i) => (
          <line
            key={i}
            x1={PAD_LEFT} y1={y}
            x2={CHART_W - PAD_RIGHT} y2={y}
            stroke="#e2e8f0"
            strokeWidth="1"
            strokeDasharray={i === 0 ? "0" : "4 4"}
          />
        ))}

        {/* Vertical grid at M6, M12, M18 */}
        {annotationIdxs.map((idx) => {
          const x = PAD_LEFT + (idx / 17) * (CHART_W - PAD_LEFT - PAD_RIGHT);
          return (
            <line
              key={idx}
              x1={x} y1={PAD_TOP}
              x2={x} y2={CHART_H - PAD_BOTTOM}
              stroke="#e2e8f0"
              strokeWidth="1"
              strokeDasharray="4 4"
            />
          );
        })}

        {/* Y-axis labels */}
        {yLabels.map(({ label, y }, i) => (
          <text
            key={i}
            x={PAD_LEFT - 8} y={y}
            textAnchor="end"
            dominantBaseline="middle"
            fontSize="10.5"
            fill="#94a3b8"
            fontFamily="ui-sans-serif, system-ui, sans-serif"
          >
            {label}
          </text>
        ))}

        {/* X-axis labels */}
        {[1, 3, 6, 9, 12, 15, 18].map((m) => {
          const x = PAD_LEFT + ((m - 1) / 17) * (CHART_W - PAD_LEFT - PAD_RIGHT);
          return (
            <text
              key={m}
              x={x} y={CHART_H - PAD_BOTTOM + 16}
              textAnchor="middle"
              fontSize="10.5"
              fill="#94a3b8"
              fontFamily="ui-sans-serif, system-ui, sans-serif"
            >
              M{m}
            </text>
          );
        })}

        {/* Inactive curves */}
        {allScenarios
          .filter((s) => s !== activeScenario)
          .map((s) => (
            <path
              key={s}
              d={smoothPath(SCENARIOS[s].arrMonthly, allMax)}
              fill="none"
              stroke={SCENARIOS[s].colorHex}
              strokeWidth="1.5"
              strokeOpacity="0.20"
            />
          ))}

        {/* Active fill */}
        <path
          d={fillPath(SCENARIOS[activeScenario].arrMonthly, allMax)}
          fill={`url(#grad-${activeScenario})`}
        />

        {/* Active line */}
        <path
          d={smoothPath(SCENARIOS[activeScenario].arrMonthly, allMax)}
          fill="none"
          stroke={SCENARIOS[activeScenario].colorHex}
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* Annotation dots + labels */}
        {annotationIdxs.map((idx) => {
          const { x, y } = toPoint(idx, SCENARIOS[activeScenario].arrMonthly[idx], allMax);
          const label = formatK(SCENARIOS[activeScenario].arrMonthly[idx]);
          const above = y > PAD_TOP + 28;
          return (
            <g key={idx}>
              <circle cx={x} cy={y} r={7} fill="white" stroke={SCENARIOS[activeScenario].colorHex} strokeWidth="2" />
              <circle cx={x} cy={y} r={3.5} fill={SCENARIOS[activeScenario].colorHex} />
              <text
                x={x} y={above ? y - 14 : y + 20}
                textAnchor="middle"
                fontSize="10.5"
                fontWeight="700"
                fill={SCENARIOS[activeScenario].colorHex}
                fontFamily="ui-sans-serif, system-ui, sans-serif"
              >
                {label}
              </text>
            </g>
          );
        })}

        {/* Legend */}
        {allScenarios.map((s, i) => {
          const lx = PAD_LEFT + i * 170;
          const ly = CHART_H - 6;
          const isActive = s === activeScenario;
          return (
            <g key={s}>
              <line
                x1={lx} y1={ly}
                x2={lx + 18} y2={ly}
                stroke={SCENARIOS[s].colorHex}
                strokeWidth={isActive ? 2.5 : 1.5}
                strokeOpacity={isActive ? 1 : 0.30}
              />
              <text
                x={lx + 24} y={ly + 1}
                fontSize="10.5"
                dominantBaseline="middle"
                fill={isActive ? SCENARIOS[s].colorHex : "#94a3b8"}
                fontWeight={isActive ? "700" : "400"}
                fontFamily="ui-sans-serif, system-ui, sans-serif"
              >
                {SCENARIOS[s].label}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

// ─── KPI Card ─────────────────────────────────────────────────────────────────

function KpiCard({
  label,
  value,
  sub,
  icon,
  scenario,
}: {
  label: string;
  value: string;
  sub?: string;
  icon: React.ReactNode;
  scenario: Scenario;
}) {
  const s = SCENARIOS[scenario];
  return (
    <div className={`rounded-2xl border p-5 flex flex-col gap-3 transition-all duration-300 ${s.bgTint} ${s.borderTint}`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider leading-none">{label}</span>
        <span className={`w-8 h-8 rounded-xl flex items-center justify-center ${s.accentBg} text-white`}>{icon}</span>
      </div>
      <div>
        <span className={`text-3xl font-bold tabular-nums ${s.color}`}>{value}</span>
        {sub && <span className="text-xs text-slate-400 ml-2">{sub}</span>}
      </div>
    </div>
  );
}

// ─── Hypotheses Accordion ─────────────────────────────────────────────────────

function HypothesisRow({ label, pessi, real, opti }: { label: string; pessi: string; real: string; opti: string }) {
  return (
    <div className="grid grid-cols-4 gap-3 py-3 border-b border-slate-100 last:border-0 items-center">
      <span className="text-sm text-slate-600 font-medium">{label}</span>
      <span className="text-sm text-red-600 font-semibold text-center bg-red-50 rounded-lg px-2 py-1">{pessi}</span>
      <span className="text-sm text-amber-600 font-semibold text-center bg-amber-50 rounded-lg px-2 py-1">{real}</span>
      <span className="text-sm text-emerald-600 font-semibold text-center bg-emerald-50 rounded-lg px-2 py-1">{opti}</span>
    </div>
  );
}

function HypothesesAccordion() {
  const [open, setOpen] = useState(false);
  return (
    <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden">
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full flex items-center justify-between px-6 py-4 hover:bg-slate-50 transition-colors duration-150 cursor-pointer"
        aria-expanded={open}
      >
        <div className="flex items-center gap-3">
          <div className="w-7 h-7 rounded-lg bg-slate-100 flex items-center justify-center">
            <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-slate-500">
              <path fillRule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clipRule="evenodd" />
            </svg>
          </div>
          <span className="text-sm font-semibold text-slate-800">Hypothèses du modèle</span>
          <span className="text-xs text-slate-400 hidden sm:inline">— Transparence totale sur les inputs</span>
        </div>
        <svg
          viewBox="0 0 20 20"
          fill="currentColor"
          className={`w-4 h-4 text-slate-400 transition-transform duration-200 flex-shrink-0 ${open ? "rotate-180" : ""}`}
        >
          <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </button>

      {open && (
        <div className="px-6 pb-6">
          <div className="grid grid-cols-4 gap-3 pb-2 mb-1 border-b-2 border-slate-100">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Hypothèse</span>
            <span className="text-xs font-bold text-red-400 uppercase tracking-wider text-center">Pessimiste</span>
            <span className="text-xs font-bold text-amber-500 uppercase tracking-wider text-center">Réaliste</span>
            <span className="text-xs font-bold text-emerald-600 uppercase tracking-wider text-center">Optimiste</span>
          </div>
          <HypothesisRow label="Conv. démo → client" pessi="18%" real="28%" opti="42%" />
          <HypothesisRow label="Churn mensuel" pessi="3.5%" real="2.1%" opti="0.8%" />
          <HypothesisRow label="ACV moyen" pessi="15K€" real="18K€" opti="24K€" />
          <HypothesisRow label="Cycle de vente" pessi="90 jours" real="60 jours" opti="45 jours" />
          <HypothesisRow label="Coût acquisition client" pessi="4 200€" real="2 800€" opti="1 600€" />
        </div>
      )}
    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function SuccessPage() {
  const [scenario, setScenario] = useState<Scenario>("realistic");
  const s = SCENARIOS[scenario];
  const scenarioKeys: Scenario[] = ["pessimistic", "realistic", "optimistic"];

  return (
    <div className="space-y-8 pb-14">

      {/* ── HEADER ─────────────────────────────────────────────────────────── */}
      <div
        className="rounded-2xl overflow-hidden"
        style={{ background: "linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #0f172a 100%)" }}
      >
        <div className="px-6 py-8 md:px-8">
          <div className="flex flex-col md:flex-row md:items-center gap-6">
            {/* Title block */}
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-7 h-7 rounded-lg bg-white/10 flex items-center justify-center">
                  <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-white/70">
                    <path fillRule="evenodd" d="M10 2l2.928 5.929 6.072.882-4.392 4.282 1.036 6.043L10 16.222l-5.644 2.914 1.036-6.043L1 8.811l6.072-.882L10 2z" clipRule="evenodd" />
                  </svg>
                </div>
                <span className="text-[11px] font-bold text-white/40 uppercase tracking-widest">Projection stratégique · 18 mois</span>
              </div>
              <h1 className="text-2xl md:text-3xl font-bold text-white tracking-tight mb-2">
                Simulation de Succès
              </h1>
              <p className="text-[14px] text-slate-400 leading-relaxed max-w-xl">
                Visualisez votre trajectoire vers le{" "}
                <span className="text-white font-semibold">leadership de marché</span>.
                Trois scénarios calibrés sur des hypothèses SaaS réalistes — du conservateur à l&apos;exceptionnel.
              </p>
            </div>

            {/* Scenario toggle buttons */}
            <div className="flex flex-wrap gap-2 md:flex-col md:gap-2 md:min-w-[160px]">
              {scenarioKeys.map((key) => {
                const sc = SCENARIOS[key];
                const isActive = scenario === key;
                return (
                  <button
                    key={key}
                    onClick={() => setScenario(key)}
                    className={`flex items-center gap-2.5 px-4 py-2.5 rounded-xl text-sm font-semibold border transition-all duration-200 cursor-pointer ${
                      isActive
                        ? sc.btnActive
                        : "bg-white/5 border-white/10 text-white/55 hover:bg-white/10 hover:text-white/80"
                    }`}
                  >
                    <span>{sc.emoji}</span>
                    <span>{sc.label}</span>
                    {isActive && <span className="ml-auto flex h-1.5 w-1.5 rounded-full bg-white/70 flex-shrink-0" />}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* ── SECTION 1 : KPI CARDS ─────────────────────────────────────────────── */}
      <div>
        <div className="flex items-center gap-3 mb-4">
          <span className={`text-xs font-bold uppercase tracking-widest ${s.color}`}>Projections à 18 mois</span>
          <div className="flex-1 h-px bg-slate-200" />
          <span className="text-xs text-slate-400 font-medium">Scénario {s.label}</span>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <KpiCard
            scenario={scenario}
            label="ARR cible"
            value={s.arr18 >= 1000 ? `${(s.arr18 / 1000).toFixed(1)}M€` : `${s.arr18}K€`}
            sub="ARR annuel récurrent"
            icon={
              <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
                <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z" />
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
              </svg>
            }
          />
          <KpiCard
            scenario={scenario}
            label="Clients actifs"
            value={s.clients18.toString()}
            sub="comptes payants"
            icon={
              <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
                <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
              </svg>
            }
          />
          <KpiCard
            scenario={scenario}
            label="Parts de marché"
            value={`${s.marketShare18}%`}
            sub="segment ETI France"
            icon={
              <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm0-2a6 6 0 100-12 6 6 0 000 12zm0-2a4 4 0 100-8 4 4 0 000 8zm0-2a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
              </svg>
            }
          />
          <KpiCard
            scenario={scenario}
            label="Valeur entreprise"
            value={`${s.valuation18}M€`}
            sub="multiple 8× ARR"
            icon={
              <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
                <path fillRule="evenodd" d="M10 2l2.928 5.929 6.072.882-4.392 4.282 1.036 6.043L10 16.222l-5.644 2.914 1.036-6.043L1 8.811l6.072-.882L10 2z" clipRule="evenodd" />
              </svg>
            }
          />
        </div>
      </div>

      {/* ── SECTION 2 : ARR GROWTH CHART ──────────────────────────────────────── */}
      <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between flex-wrap gap-2">
          <div className="flex items-center gap-3">
            <div className="w-7 h-7 rounded-lg bg-slate-100 flex items-center justify-center">
              <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-slate-500">
                <path fillRule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clipRule="evenodd" />
              </svg>
            </div>
            <h2 className="text-sm font-semibold text-slate-800">Courbe de croissance ARR</h2>
          </div>
          <span className="text-xs text-slate-400 font-medium">3 scénarios superposés · M1 → M18</span>
        </div>
        <div className="p-4 md:p-6">
          <GrowthChart activeScenario={scenario} />
        </div>
      </div>

      {/* ── SECTION 3 : MILESTONES TIMELINE ──────────────────────────────────── */}
      <div>
        <div className="flex items-center gap-3 mb-6">
          <span className={`text-xs font-bold uppercase tracking-widest ${s.color}`}>Jalons de succès</span>
          <div className="flex-1 h-px bg-slate-200" />
          <span className="text-xs text-slate-400 font-medium">6 étapes clés</span>
        </div>

        <div className="relative">
          {/* Central line — desktop only */}
          <div className="hidden md:block absolute left-1/2 top-0 bottom-0 w-px bg-slate-200 -translate-x-1/2 pointer-events-none" />

          <div className="space-y-4 md:space-y-0">
            {MILESTONES.map((m, i) => {
              const isLeft = i % 2 === 0;
              return (
                <div
                  key={m.month}
                  className={`relative md:flex md:items-start ${isLeft ? "md:flex-row" : "md:flex-row-reverse"} md:mb-6`}
                >
                  {/* Card */}
                  <div className={`md:w-[calc(50%-2.5rem)] ${isLeft ? "md:pr-6" : "md:pl-6"}`}>
                    <div className={`bg-white rounded-xl border p-4 md:p-5 hover:shadow-md transition-all duration-200 ${s.borderTint}`}>
                      <div className="flex items-start gap-3">
                        <div className={`w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 ${s.accentBg} text-white`}>
                          {m.icon}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1 flex-wrap">
                            <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${s.bgTint} ${s.color} border ${s.borderTint}`}>
                              {m.month}
                            </span>
                          </div>
                          <h3 className="text-sm font-semibold text-slate-800 leading-snug mb-1">{m.title}</h3>
                          <p className="text-xs text-slate-500 leading-relaxed mb-2">{m.desc}</p>
                          <span className={`inline-flex text-[11px] font-bold px-2 py-0.5 rounded-full ${s.bgTint} ${s.color}`}>
                            {m.metric}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Center connector dot */}
                  <div className="hidden md:flex w-20 flex-shrink-0 items-start justify-center pt-5">
                    <div className={`w-4 h-4 rounded-full border-2 border-white shadow-md ${s.accentBg}`} />
                  </div>

                  {/* Empty half */}
                  <div className="hidden md:block md:w-[calc(50%-2.5rem)]" />
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* ── SECTION 4 : HYPOTHESES ACCORDION ─────────────────────────────────── */}
      <HypothesesAccordion />

      {/* ── SECTION 5 : ACCELERATORS (optimistic only) ────────────────────────── */}
      {scenario === "optimistic" && (
        <div>
          <div className="flex items-center gap-3 mb-4">
            <span className="text-xs font-bold uppercase tracking-widest text-emerald-600">
              Accélérateurs de succès
            </span>
            <div className="flex-1 h-px bg-slate-200" />
            <span className="text-xs text-slate-400 font-medium">Réaliste → Exceptionnel</span>
          </div>

          <div className="grid md:grid-cols-3 gap-4 mb-4">
            {ACCELERATORS.map((acc, i) => (
              <div
                key={i}
                className="bg-white rounded-2xl border border-emerald-100 p-5 hover:shadow-md hover:border-emerald-200 transition-all duration-200 relative overflow-hidden"
              >
                <div className="absolute -top-8 -right-8 w-28 h-28 rounded-full bg-emerald-400/10 blur-2xl pointer-events-none" />
                <div className="relative">
                  <div className="flex items-start justify-between mb-3">
                    <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center flex-shrink-0">
                      {acc.icon}
                    </div>
                    <span className="text-[11px] font-bold px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-700">
                      {acc.badge}
                    </span>
                  </div>
                  <h3 className="text-sm font-bold text-slate-800 mb-0.5">{acc.title}</h3>
                  <p className="text-xs font-semibold text-emerald-600 mb-2">{acc.subtitle}</p>
                  <p className="text-xs text-slate-500 leading-relaxed">{acc.desc}</p>
                </div>
              </div>
            ))}
          </div>

          <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-5 py-4 flex items-start gap-3">
            <div className="w-6 h-6 rounded-lg bg-emerald-600 flex items-center justify-center flex-shrink-0 mt-0.5">
              <svg viewBox="0 0 20 20" fill="currentColor" className="w-3.5 h-3.5 text-white">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
            </div>
            <div>
              <p className="text-[13px] font-semibold text-emerald-800 mb-0.5">Effet compound des accélérateurs</p>
              <p className="text-xs text-emerald-700 leading-relaxed">
                Les 3 accélérateurs activés simultanément créent un levier non-linéaire. Le partenariat revendeur alimente la viral loop, et la feature exclusive réduit le churn des clients issus du canal partenaire — multipliant l&apos;effet net par 3.8× vs. scénario réaliste.
              </p>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
