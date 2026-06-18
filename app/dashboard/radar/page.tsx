"use client";

import { useState } from "react";

// ─── Types ─────────────────────────────────────────────────────────────────

type RiskLevel = "critique" | "attention" | "surveillance";
type ActionType = "call" | "email" | "doc";

interface ClientAccount {
  id: string;
  company: string;
  sector: string;
  arr: number; // en euros
  riskScore: number; // 0-100
  competitor: string;
  competitorColor: string;
  riskReason: string;
  lastContact: string; // ISO date
  actionLabel: string;
  actionType: ActionType;
  status: RiskLevel;
  relationYears: number; // pour bubble chart
}

interface SavedClient {
  id: string;
  company: string;
  sector: string;
  arrSaved: number;
  action: string;
  competitor: string;
  date: string;
}

// ─── Mock Data ──────────────────────────────────────────────────────────────

const mockAccounts: ClientAccount[] = [
  {
    id: "1",
    company: "Groupe Moreau SA",
    sector: "Distribution",
    arr: 178000,
    riskScore: 87,
    competitor: "Salesforce",
    competitorColor: "#00A1E0",
    riskReason: "Salesforce a annoncé une baisse tarifaire de 22% sur le segment Enterprise ce trimestre.",
    lastContact: "2026-04-28",
    actionLabel: "Appel commercial urgent",
    actionType: "call",
    status: "critique",
    relationYears: 4,
  },
  {
    id: "2",
    company: "ETI Beaumont Industries",
    sector: "Industrie",
    arr: 142000,
    riskScore: 81,
    competitor: "HubSpot",
    competitorColor: "#FF7A59",
    riskReason: "HubSpot vient de lancer l'intégration Salesforce native qu'ils réclamaient depuis 18 mois.",
    lastContact: "2026-05-02",
    actionLabel: "Démonstration feature roadmap",
    actionType: "doc",
    status: "critique",
    relationYears: 6,
  },
  {
    id: "3",
    company: "Maison Leclerc & Associés",
    sector: "Services B2B",
    arr: 95000,
    riskScore: 78,
    competitor: "Pipedrive",
    competitorColor: "#28C16A",
    riskReason: "Leur directeur commercial vient de se connecter au site de Pipedrive 3 fois cette semaine.",
    lastContact: "2026-05-10",
    actionLabel: "Offrir remise de rétention",
    actionType: "email",
    status: "critique",
    relationYears: 2,
  },
  {
    id: "4",
    company: "Vernet Conseil SAS",
    sector: "Conseil",
    arr: 68000,
    riskScore: 71,
    competitor: "Monday.com",
    competitorColor: "#F62B54",
    riskReason: "Monday.com a publié un comparatif direct les ciblant et a contacté leur DSI.",
    lastContact: "2026-05-18",
    actionLabel: "Envoyer comparatif",
    actionType: "doc",
    status: "critique",
    relationYears: 3,
  },
  {
    id: "5",
    company: "Duplessis Médical",
    sector: "Santé",
    arr: 112000,
    riskScore: 64,
    competitor: "Zoho",
    competitorColor: "#E42527",
    riskReason: "Zoho propose un module conformité RGPD/santé avec certification HDS — fonctionnalité absente chez nous.",
    lastContact: "2026-05-22",
    actionLabel: "Planifier réunion technique",
    actionType: "call",
    status: "attention",
    relationYears: 5,
  },
  {
    id: "6",
    company: "Fontaine & Frères Bâtiment",
    sector: "BTP",
    arr: 54000,
    riskScore: 58,
    competitor: "HubSpot",
    competitorColor: "#FF7A59",
    riskReason: "HubSpot offre 3 mois gratuits aux PME du BTP dans leur campagne d'acquisition Q2.",
    lastContact: "2026-05-26",
    actionLabel: "Envoyer comparatif",
    actionType: "doc",
    status: "attention",
    relationYears: 2,
  },
  {
    id: "7",
    company: "Sarl Tissot Logistique",
    sector: "Logistique",
    arr: 38000,
    riskScore: 52,
    competitor: "Pipedrive",
    competitorColor: "#28C16A",
    riskReason: "Contrat annuel à renouveler dans 45 jours — aucun contact depuis 3 mois.",
    lastContact: "2026-03-12",
    actionLabel: "Relance renouvellement",
    actionType: "email",
    status: "attention",
    relationYears: 1,
  },
  {
    id: "8",
    company: "Groupe Pellerin Agroalimentaire",
    sector: "Agroalimentaire",
    arr: 87000,
    riskScore: 38,
    competitor: "Salesforce",
    competitorColor: "#00A1E0",
    riskReason: "Leur concurrent direct vient d'adopter Salesforce — risque d'alignement sectoriel.",
    lastContact: "2026-06-01",
    actionLabel: "Check-in de satisfaction",
    actionType: "call",
    status: "surveillance",
    relationYears: 7,
  },
  {
    id: "9",
    company: "Blanchot Ingénierie",
    sector: "Ingénierie",
    arr: 29000,
    riskScore: 31,
    competitor: "Zoho",
    competitorColor: "#E42527",
    riskReason: "Zoho a réduit ses prix de 15% sur le plan Pro — cohérent avec leur budget.",
    lastContact: "2026-06-05",
    actionLabel: "Partager nouveautés produit",
    actionType: "email",
    status: "surveillance",
    relationYears: 3,
  },
  {
    id: "10",
    company: "Ateliers Renard & Co",
    sector: "Retail",
    arr: 21000,
    riskScore: 22,
    competitor: "Monday.com",
    competitorColor: "#F62B54",
    riskReason: "Monday.com sponsorise leur salon professionnel annuel de septembre.",
    lastContact: "2026-06-10",
    actionLabel: "Préparer success story",
    actionType: "doc",
    status: "surveillance",
    relationYears: 1,
  },
];

const savedClients: SavedClient[] = [
  {
    id: "s1",
    company: "Marchetti Distribution",
    sector: "Distribution",
    arrSaved: 120000,
    action: "Réunion exécutive + roadmap exclusive partagée 48h avant annonce publique",
    competitor: "Salesforce",
    date: "2026-03-14",
  },
  {
    id: "s2",
    company: "Faure Technologies SAS",
    sector: "Tech",
    arrSaved: 85000,
    action: "Remise de fidélité 18% accordée + migration vers plan Enterprise offerte",
    competitor: "HubSpot",
    date: "2026-01-27",
  },
  {
    id: "s3",
    company: "Groupe Castillon Santé",
    sector: "Santé",
    arrSaved: 135000,
    action: "Développement accéléré du module HDS réclamé — livraison en 6 semaines",
    competitor: "Zoho",
    date: "2025-11-09",
  },
];

// ─── KPIs ────────────────────────────────────────────────────────────────────

const highRiskCount = mockAccounts.filter((a) => a.status === "critique").length;
const projectedChurn = mockAccounts
  .filter((a) => a.riskScore >= 70)
  .reduce((sum, a) => sum + a.arr, 0);
const avgActionWindow = 18;

// ─── Helpers ─────────────────────────────────────────────────────────────────

function formatArr(n: number): string {
  if (n >= 1000) return `${(n / 1000).toFixed(0)} K€`;
  return `${n} €`;
}

function formatDate(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleDateString("fr-FR", { day: "2-digit", month: "short", year: "numeric" });
}

function daysSince(iso: string): number {
  return Math.floor((Date.now() - new Date(iso).getTime()) / 86400000);
}

const statusMeta: Record<RiskLevel, { label: string; bg: string; text: string; dot: string; border: string }> = {
  critique: { label: "Critique", bg: "bg-red-50", text: "text-red-700", dot: "bg-red-500", border: "border-red-200" },
  attention: { label: "Attention", bg: "bg-orange-50", text: "text-orange-700", dot: "bg-orange-400", border: "border-orange-200" },
  surveillance: { label: "Surveillance", bg: "bg-yellow-50", text: "text-yellow-700", dot: "bg-yellow-400", border: "border-yellow-200" },
};

function riskBarColor(score: number): string {
  if (score >= 70) return "bg-red-500";
  if (score >= 40) return "bg-orange-400";
  return "bg-yellow-400";
}

function riskTextColor(score: number): string {
  if (score >= 70) return "text-red-600";
  if (score >= 40) return "text-orange-600";
  return "text-yellow-600";
}

// ─── SVG Icons ───────────────────────────────────────────────────────────────

function IconPhone({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
    </svg>
  );
}

function IconMail({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
      <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
    </svg>
  );
}

function IconDocument({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
    </svg>
  );
}

function IconShield({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
    </svg>
  );
}

function IconAlert({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
    </svg>
  );
}

function IconEuro({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
    </svg>
  );
}

function IconClock({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
    </svg>
  );
}

function IconCheck({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
    </svg>
  );
}

function IconUsers({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
    </svg>
  );
}

function IconReport({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6zm2 10a1 1 0 10-2 0v3a1 1 0 102 0v-3zm2-3a1 1 0 011 1v5a1 1 0 11-2 0v-5a1 1 0 011-1zm4-1a1 1 0 10-2 0v7a1 1 0 102 0V8z" clipRule="evenodd" />
    </svg>
  );
}

// ─── Sub-components ──────────────────────────────────────────────────────────

function ActionIcon({ type, className }: { type: ActionType; className?: string }) {
  if (type === "call") return <IconPhone className={className} />;
  if (type === "email") return <IconMail className={className} />;
  return <IconDocument className={className} />;
}

function ActionButtonColor(type: ActionType): string {
  if (type === "call") return "bg-red-600 hover:bg-red-700 text-white";
  if (type === "email") return "bg-blue-600 hover:bg-blue-700 text-white";
  return "bg-slate-700 hover:bg-slate-800 text-white";
}

// ─── Bubble Chart (SVG pur) ───────────────────────────────────────────────────

function BubbleChart({ accounts }: { accounts: ClientAccount[] }) {
  const W = 560;
  const H = 300;
  const padL = 50;
  const padB = 36;
  const padR = 20;
  const padT = 16;

  const chartW = W - padL - padR;
  const chartH = H - padB - padT;

  const maxArr = Math.max(...accounts.map((a) => a.arr));
  const maxRelation = Math.max(...accounts.map((a) => a.relationYears));

  // Scale X = ARR, Y = riskScore (inverted: high risk = top)
  const sx = (arr: number) => padL + (arr / maxArr) * chartW;
  const sy = (score: number) => padT + chartH - (score / 100) * chartH;
  const sr = (years: number) => 7 + (years / maxRelation) * 18;

  const bubbleColor = (score: number) => {
    if (score >= 70) return "#ef4444";
    if (score >= 40) return "#f97316";
    return "#eab308";
  };

  const xTicks = [0, 50000, 100000, 150000];
  const yTicks = [0, 25, 50, 75, 100];

  return (
    <div className="overflow-x-auto">
      <svg
        viewBox={`0 0 ${W} ${H}`}
        width="100%"
        style={{ minWidth: 300, maxHeight: 320 }}
        aria-label="Bubble chart: ARR vs score de risque"
      >
        {/* Grid lines Y */}
        {yTicks.map((t) => (
          <g key={t}>
            <line
              x1={padL}
              y1={sy(t)}
              x2={W - padR}
              y2={sy(t)}
              stroke="#e2e8f0"
              strokeWidth={1}
              strokeDasharray={t === 0 ? "0" : "4 3"}
            />
            <text x={padL - 6} y={sy(t) + 4} textAnchor="end" fontSize={10} fill="#94a3b8">
              {t}
            </text>
          </g>
        ))}

        {/* X axis ticks */}
        {xTicks.map((t) => (
          <g key={t}>
            <line x1={sx(t)} y1={padT} x2={sx(t)} y2={H - padB} stroke="#e2e8f0" strokeWidth={1} strokeDasharray="4 3" />
            <text x={sx(t)} y={H - padB + 14} textAnchor="middle" fontSize={10} fill="#94a3b8">
              {t === 0 ? "0" : `${t / 1000}K`}
            </text>
          </g>
        ))}

        {/* Axis labels */}
        <text x={padL + chartW / 2} y={H - 2} textAnchor="middle" fontSize={11} fill="#64748b" fontWeight="500">
          ARR (€)
        </text>
        <text
          x={12}
          y={padT + chartH / 2}
          textAnchor="middle"
          fontSize={11}
          fill="#64748b"
          fontWeight="500"
          transform={`rotate(-90, 12, ${padT + chartH / 2})`}
        >
          Risque
        </text>

        {/* Bubbles */}
        {accounts.map((a) => {
          const cx = sx(a.arr);
          const cy = sy(a.riskScore);
          const r = sr(a.relationYears);
          const color = bubbleColor(a.riskScore);
          return (
            <g key={a.id}>
              <circle cx={cx} cy={cy} r={r} fill={color} fillOpacity={0.25} stroke={color} strokeWidth={1.5} />
              <title>{`${a.company} — ARR: ${formatArr(a.arr)} — Risque: ${a.riskScore}/100`}</title>
              <text x={cx} y={cy + 3} textAnchor="middle" fontSize={8} fill={color} fontWeight="700">
                {a.company.split(" ")[0].slice(0, 6)}
              </text>
            </g>
          );
        })}

        {/* Danger zone shading */}
        <rect
          x={padL}
          y={padT}
          width={chartW}
          height={(30 / 100) * chartH}
          fill="#ef4444"
          fillOpacity={0.04}
        />
        <text x={W - padR - 4} y={padT + (30 / 100) * chartH - 4} textAnchor="end" fontSize={9} fill="#ef4444" fillOpacity={0.7}>
          Zone critique
        </text>
      </svg>

      {/* Legend */}
      <div className="flex items-center gap-4 mt-2 pl-12 text-[11px] text-slate-500">
        <span className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-red-400 inline-block opacity-70" /> Critique (&gt;70)
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-orange-400 inline-block opacity-70" /> Attention (40-70)
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-yellow-400 inline-block opacity-70" /> Surveillance (&lt;40)
        </span>
        <span className="flex items-center gap-1.5 ml-2 text-slate-400 italic">Taille = durée relation</span>
      </div>
    </div>
  );
}

// ─── Main Component ──────────────────────────────────────────────────────────

export default function RadarPage() {
  const [filter, setFilter] = useState<RiskLevel | "all">("all");
  const [sortBy, setSortBy] = useState<"risk" | "arr">("risk");
  const [toastMsg, setToastMsg] = useState<string | null>(null);
  const [showChart, setShowChart] = useState(true);

  const filtered = mockAccounts
    .filter((a) => filter === "all" || a.status === filter)
    .sort((a, b) => (sortBy === "risk" ? b.riskScore - a.riskScore : b.arr - a.arr));

  function handleAction(account: ClientAccount) {
    setToastMsg(`Action lancée pour ${account.company}`);
    setTimeout(() => setToastMsg(null), 3000);
  }

  function handleQuickAction(label: string) {
    setToastMsg(label);
    setTimeout(() => setToastMsg(null), 3000);
  }

  return (
    <div className="space-y-6 pb-10 relative">

      {/* Toast notification */}
      {toastMsg && (
        <div className="fixed top-5 right-5 z-50 bg-slate-900 text-white text-[13px] font-medium px-4 py-2.5 rounded-lg shadow-xl flex items-center gap-2 animate-fade-in">
          <IconCheck className="w-4 h-4 text-green-400" />
          {toastMsg}
        </div>
      )}

      {/* ─── HEADER ──────────────────────────────────────────────────── */}
      <div
        className="rounded-xl overflow-hidden"
        style={{ background: "linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #0f172a 100%)" }}
      >
        <div className="px-6 pt-6 pb-5">
          <div className="flex items-start justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-1.5">
                <div className="w-7 h-7 rounded-lg bg-red-500/20 flex items-center justify-center">
                  <IconAlert className="w-4 h-4 text-red-400" />
                </div>
                <span className="text-[11px] font-semibold text-red-400 uppercase tracking-widest">Intelligence Client</span>
              </div>
              <h1 className="text-[26px] font-bold text-white tracking-tight leading-tight">
                Radar — Clients à Risque Concurrentiel
              </h1>
              <p className="text-[13px] text-slate-400 mt-1.5 max-w-xl">
                Identifiez vos comptes vulnérables avant qu&apos;ils ne partent. 80% du churn B2B est prévisible 60 jours à l&apos;avance.
              </p>
            </div>
            <div className="hidden md:flex items-center gap-1.5 mt-1">
              <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
              <span className="text-[11px] text-slate-400 font-medium">Mis à jour aujourd&apos;hui</span>
            </div>
          </div>

          {/* KPI Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-5">
            {/* KPI 1 */}
            <div className="bg-white/5 border border-white/10 rounded-lg px-4 py-3.5 flex items-center gap-3 hover:bg-white/8 transition-colors">
              <div className="w-9 h-9 rounded-lg bg-red-500/20 flex items-center justify-center flex-shrink-0">
                <IconAlert className="w-5 h-5 text-red-400" />
              </div>
              <div>
                <p className="text-[26px] font-bold text-red-300 leading-none tabular-nums">{highRiskCount}</p>
                <p className="text-[11px] text-slate-400 mt-0.5">Comptes à risque élevé</p>
              </div>
            </div>

            {/* KPI 2 */}
            <div className="bg-white/5 border border-white/10 rounded-lg px-4 py-3.5 flex items-center gap-3 hover:bg-white/8 transition-colors">
              <div className="w-9 h-9 rounded-lg bg-orange-500/20 flex items-center justify-center flex-shrink-0">
                <IconEuro className="w-5 h-5 text-orange-400" />
              </div>
              <div>
                <p className="text-[26px] font-bold text-orange-300 leading-none tabular-nums">
                  {(projectedChurn / 1000).toFixed(0)} K€
                </p>
                <p className="text-[11px] text-slate-400 mt-0.5">Churn projeté si inaction</p>
              </div>
            </div>

            {/* KPI 3 */}
            <div className="bg-white/5 border border-white/10 rounded-lg px-4 py-3.5 flex items-center gap-3 hover:bg-white/8 transition-colors">
              <div className="w-9 h-9 rounded-lg bg-yellow-500/20 flex items-center justify-center flex-shrink-0">
                <IconClock className="w-5 h-5 text-yellow-400" />
              </div>
              <div>
                <p className="text-[26px] font-bold text-yellow-300 leading-none tabular-nums">{avgActionWindow} jours</p>
                <p className="text-[11px] text-slate-400 mt-0.5">Fenêtre d&apos;action restante (moy.)</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ─── BUBBLE CHART ────────────────────────────────────────────── */}
      <div className="bg-white rounded-xl border border-slate-200">
        <div className="px-5 py-3.5 border-b border-slate-100 flex items-center justify-between">
          <div>
            <h2 className="text-[13px] font-semibold text-slate-900">Carte de risque — ARR vs Score</h2>
            <p className="text-[11px] text-slate-400 mt-0.5">Taille des bulles = durée de la relation</p>
          </div>
          <button
            onClick={() => setShowChart((v) => !v)}
            className="text-[11px] text-slate-400 hover:text-slate-600 transition-colors font-medium border border-slate-200 px-3 py-1 rounded-md"
          >
            {showChart ? "Masquer" : "Afficher"}
          </button>
        </div>
        {showChart && (
          <div className="px-5 py-4">
            <BubbleChart accounts={mockAccounts} />
          </div>
        )}
      </div>

      {/* ─── FILTERS + TABLE ─────────────────────────────────────────── */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
        {/* Table toolbar */}
        <div className="px-5 py-3.5 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center gap-3 justify-between">
          <div>
            <h2 className="text-[14px] font-semibold text-slate-900">Comptes à risque</h2>
            <p className="text-[11px] text-slate-400 mt-0.5">
              {filtered.length} compte{filtered.length > 1 ? "s" : ""} — triés par {sortBy === "risk" ? "score de risque" : "ARR"}
            </p>
          </div>
          <div className="flex items-center gap-2 flex-wrap">
            {/* Filter pills */}
            {(["all", "critique", "attention", "surveillance"] as const).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`text-[11px] font-semibold px-3 py-1 rounded-full border transition-all ${
                  filter === f
                    ? f === "critique"
                      ? "bg-red-500 text-white border-red-500"
                      : f === "attention"
                      ? "bg-orange-500 text-white border-orange-500"
                      : f === "surveillance"
                      ? "bg-yellow-500 text-white border-yellow-500"
                      : "bg-slate-900 text-white border-slate-900"
                    : "bg-white text-slate-600 border-slate-200 hover:border-slate-300"
                }`}
              >
                {f === "all"
                  ? "Tous"
                  : f === "critique"
                  ? "Critique"
                  : f === "attention"
                  ? "Attention"
                  : "Surveillance"}
              </button>
            ))}

            {/* Sort */}
            <div className="flex items-center gap-1 border border-slate-200 rounded-md overflow-hidden ml-1">
              <button
                onClick={() => setSortBy("risk")}
                className={`text-[11px] font-medium px-2.5 py-1 transition-colors ${sortBy === "risk" ? "bg-slate-900 text-white" : "text-slate-500 hover:bg-slate-50"}`}
              >
                Par risque
              </button>
              <button
                onClick={() => setSortBy("arr")}
                className={`text-[11px] font-medium px-2.5 py-1 transition-colors ${sortBy === "arr" ? "bg-slate-900 text-white" : "text-slate-500 hover:bg-slate-50"}`}
              >
                Par ARR
              </button>
            </div>
          </div>
        </div>

        {/* Column headers */}
        <div className="hidden lg:grid grid-cols-[minmax(180px,2fr)_90px_160px_140px_minmax(180px,3fr)_100px_180px_110px] gap-3 px-5 py-2.5 bg-slate-50 border-b border-slate-100 text-[11px] font-semibold text-slate-400 uppercase tracking-wide">
          <span>Compte</span>
          <span className="text-right">ARR</span>
          <span>Score de risque</span>
          <span>Concurrent</span>
          <span>Raison</span>
          <span>Dernier contact</span>
          <span>Action recommandée</span>
          <span className="text-center">Statut</span>
        </div>

        {/* Rows */}
        <div className="divide-y divide-slate-100">
          {filtered.map((account) => {
            const sm = statusMeta[account.status];
            const days = daysSince(account.lastContact);
            const isStale = days > 30;
            return (
              <div
                key={account.id}
                className="group px-5 py-4 hover:bg-slate-50/70 transition-colors grid grid-cols-1 lg:grid-cols-[minmax(180px,2fr)_90px_160px_140px_minmax(180px,3fr)_100px_180px_110px] gap-3 lg:gap-3 items-center"
              >
                {/* Company */}
                <div className="flex items-center gap-2.5 min-w-0">
                  <div
                    className="w-8 h-8 rounded-lg flex-shrink-0 flex items-center justify-center text-white text-[11px] font-bold shadow-sm"
                    style={{ background: `linear-gradient(135deg, #1e293b, #334155)` }}
                  >
                    {account.company.split(" ")[0].slice(0, 2).toUpperCase()}
                  </div>
                  <div className="min-w-0">
                    <p className="text-[13px] font-semibold text-slate-900 truncate">{account.company}</p>
                    <p className="text-[11px] text-slate-400 truncate">{account.sector}</p>
                  </div>
                </div>

                {/* ARR */}
                <div className="lg:text-right">
                  <span className="text-[13px] font-semibold text-slate-800 tabular-nums">{formatArr(account.arr)}</span>
                  <span className="lg:hidden text-[11px] text-slate-400 ml-1">ARR</span>
                </div>

                {/* Risk score */}
                <div className="space-y-1">
                  <div className="flex items-center justify-between">
                    <span className={`text-[13px] font-bold tabular-nums ${riskTextColor(account.riskScore)}`}>
                      {account.riskScore}/100
                    </span>
                  </div>
                  <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all duration-500 ${riskBarColor(account.riskScore)}`}
                      style={{ width: `${account.riskScore}%` }}
                    />
                  </div>
                </div>

                {/* Competitor */}
                <div>
                  <span
                    className="inline-flex items-center gap-1.5 text-[11px] font-semibold px-2.5 py-1 rounded-full border"
                    style={{
                      backgroundColor: account.competitorColor + "18",
                      color: account.competitorColor,
                      borderColor: account.competitorColor + "40",
                    }}
                  >
                    <span
                      className="w-1.5 h-1.5 rounded-full flex-shrink-0"
                      style={{ backgroundColor: account.competitorColor }}
                    />
                    {account.competitor}
                  </span>
                </div>

                {/* Risk reason */}
                <p className="text-[12px] text-slate-600 leading-snug line-clamp-2">{account.riskReason}</p>

                {/* Last contact */}
                <div>
                  <p className="text-[12px] text-slate-600">{formatDate(account.lastContact)}</p>
                  <p className={`text-[10px] font-medium mt-0.5 ${isStale ? "text-red-500" : "text-slate-400"}`}>
                    {isStale ? `⚠ Il y a ${days}j` : `Il y a ${days}j`}
                  </p>
                </div>

                {/* Action button */}
                <button
                  onClick={() => handleAction(account)}
                  className={`inline-flex items-center justify-center gap-1.5 text-[11px] font-semibold px-3 py-1.5 rounded-lg transition-colors duration-100 shadow-sm ${ActionButtonColor(account.actionType)}`}
                >
                  <ActionIcon type={account.actionType} className="w-3.5 h-3.5 flex-shrink-0" />
                  <span className="truncate">{account.actionLabel}</span>
                </button>

                {/* Status badge */}
                <div className="flex lg:justify-center">
                  <span className={`inline-flex items-center gap-1.5 text-[11px] font-semibold px-2.5 py-1 rounded-full border ${sm.bg} ${sm.text} ${sm.border}`}>
                    <span className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${sm.dot}`} />
                    {sm.label}
                  </span>
                </div>
              </div>
            );
          })}
        </div>

        {filtered.length === 0 && (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <div className="w-12 h-12 rounded-full bg-green-50 flex items-center justify-center mb-3">
              <IconShield className="w-6 h-6 text-green-500" />
            </div>
            <p className="text-[14px] font-semibold text-slate-700">Aucun compte dans cette catégorie</p>
            <p className="text-[12px] text-slate-400 mt-1">Essayez un autre filtre</p>
          </div>
        )}
      </div>

      {/* ─── QUICK ACTIONS ───────────────────────────────────────────── */}
      <div className="bg-white rounded-xl border border-slate-200 px-5 py-4">
        <h2 className="text-[13px] font-semibold text-slate-900 mb-3">Actions rapides</h2>
        <div className="flex flex-wrap gap-3">
          <button
            onClick={() => handleQuickAction("Rapport de rétention en cours de génération…")}
            className="inline-flex items-center gap-2 bg-[#0078D4] hover:bg-[#006cbf] text-white text-[13px] font-semibold px-4 py-2 rounded-lg transition-colors shadow-sm"
          >
            <IconReport className="w-4 h-4" />
            Générer rapport de rétention complet
          </button>
          <button
            onClick={() => handleQuickAction("Notification envoyée à l'équipe commerciale")}
            className="inline-flex items-center gap-2 bg-slate-800 hover:bg-slate-900 text-white text-[13px] font-semibold px-4 py-2 rounded-lg transition-colors shadow-sm"
          >
            <IconUsers className="w-4 h-4" />
            Notifier l&apos;équipe commerciale
          </button>
          <button
            onClick={() => handleQuickAction("Plan d'action créé et partagé dans Notion")}
            className="inline-flex items-center gap-2 bg-white border border-slate-200 hover:border-slate-300 text-slate-700 hover:text-slate-900 text-[13px] font-semibold px-4 py-2 rounded-lg transition-colors"
          >
            <IconDocument className="w-4 h-4" />
            Créer plan d&apos;action
          </button>
        </div>
      </div>

      {/* ─── HISTORIQUE SAUVÉ ─────────────────────────────────────────── */}
      <div>
        <div className="flex items-center gap-2 mb-4">
          <div className="w-6 h-6 rounded-md bg-green-100 flex items-center justify-center">
            <IconShield className="w-4 h-4 text-green-600" />
          </div>
          <h2 className="text-[14px] font-semibold text-slate-900">Historique sauvé — Clients retenus grâce à une action rapide</h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {savedClients.map((sc) => (
            <div
              key={sc.id}
              className="bg-white border border-green-100 rounded-xl p-4 hover:shadow-[0_2px_12px_rgba(0,0,0,0.07)] transition-shadow relative overflow-hidden"
            >
              {/* Green accent strip */}
              <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-green-400 to-emerald-500" />

              <div className="flex items-start justify-between gap-2 mt-1 mb-3">
                <div>
                  <p className="text-[13px] font-bold text-slate-900">{sc.company}</p>
                  <p className="text-[11px] text-slate-400">{sc.sector}</p>
                </div>
                <span className="text-[10px] font-semibold bg-green-50 text-green-700 border border-green-200 px-2 py-0.5 rounded-full flex-shrink-0">
                  Retenu
                </span>
              </div>

              <p className="text-[12px] text-slate-600 leading-snug mb-3">{sc.action}</p>

              <div className="flex items-center justify-between pt-2.5 border-t border-slate-100">
                <span className="text-[11px] text-slate-400">
                  Concurrent : <span className="font-medium text-slate-600">{sc.competitor}</span>
                </span>
                <div className="flex items-center gap-1">
                  <IconCheck className="w-3.5 h-3.5 text-green-500" />
                  <span className="text-[12px] font-bold text-green-600">+{formatArr(sc.arrSaved)} ARR préservé</span>
                </div>
              </div>

              <p className="text-[10px] text-slate-400 mt-1.5">{formatDate(sc.date)}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
