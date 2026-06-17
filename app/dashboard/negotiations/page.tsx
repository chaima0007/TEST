"use client";

import { useEffect, useState } from "react";
import type { SwarmJob, NegotiationMessage, SwarmMetrics } from "@/lib/swarm-data";
import { SIMULATION_DIALOGUE } from "@/lib/swarm-data";

// ── Types ────────────────────────────────────────────────────────────────────

interface SwarmData {
  metrics: SwarmMetrics;
  jobs: SwarmJob[];
  simulation: NegotiationMessage[];
  lastUpdated: string;
}

type Sentiment = "Positif" | "Curieux" | "Sceptique" | "Négatif";

const SENTIMENT_MAP: Record<string, Sentiment> = {
  "j001": "Positif",
  "j002": "Curieux",
  "j003": "Sceptique",
  "j004": "Positif",
  "j005": "Négatif",
  "j006": "Curieux",
  "j007": "Positif",
  "j008": "Sceptique",
};

const SENTIMENT_STYLE: Record<Sentiment, { bg: string; text: string; dot: string }> = {
  Positif:   { bg: "bg-emerald-50",  text: "text-emerald-700",  dot: "bg-emerald-400" },
  Curieux:   { bg: "bg-blue-50",     text: "text-blue-700",     dot: "bg-blue-400" },
  Sceptique: { bg: "bg-amber-50",    text: "text-amber-700",    dot: "bg-amber-400" },
  Négatif:   { bg: "bg-red-50",      text: "text-red-700",      dot: "bg-red-400" },
};

const STAGES = ["detection", "outreach", "negotiation", "production", "paid"] as const;
type Stage = (typeof STAGES)[number];

const STAGE_LABELS: Record<Stage, string> = {
  detection:   "Détection",
  outreach:    "Outreach",
  negotiation: "Négociation",
  production:  "Production",
  paid:        "Payé",
};

const STAGE_COLORS: Record<Stage, string> = {
  detection:   "#3B82F6",
  outreach:    "#8B5CF6",
  negotiation: "#F59E0B",
  production:  "#10B981",
  paid:        "#059669",
};

// ── Sub-components ────────────────────────────────────────────────────────────

function Skeleton({ className }: { className?: string }) {
  return <div className={`animate-pulse bg-slate-100 rounded ${className}`} />;
}

function StatCard({
  label,
  value,
  sub,
  color,
  icon,
}: {
  label: string;
  value: string | number;
  sub?: string;
  color: string;
  icon: React.ReactNode;
}) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-4 flex items-start gap-3">
      <div
        className="w-9 h-9 rounded-lg flex items-center justify-center text-white text-base flex-shrink-0"
        style={{ backgroundColor: color }}
      >
        {icon}
      </div>
      <div className="min-w-0">
        <p className="text-[11px] text-slate-500 font-medium uppercase tracking-wide">{label}</p>
        <p className="text-[22px] font-bold text-slate-900 tabular-nums leading-tight">{value}</p>
        {sub && <p className="text-[11px] text-slate-400 mt-0.5">{sub}</p>}
      </div>
    </div>
  );
}

function MiniTimeline({ currentStage }: { currentStage: Stage }) {
  const currentIdx = STAGES.indexOf(currentStage);
  return (
    <div className="flex items-center gap-0.5 mt-2">
      {STAGES.map((stage, idx) => {
        const isCompleted = idx < currentIdx;
        const isCurrent = idx === currentIdx;
        const color = STAGE_COLORS[stage];
        return (
          <div key={stage} className="flex items-center gap-0.5 flex-1 min-w-0">
            <div className="flex flex-col items-center flex-1 min-w-0">
              <div
                className="w-full h-1.5 rounded-full transition-all"
                style={{
                  backgroundColor: isCompleted || isCurrent ? color : "#E2E8F0",
                  opacity: isCurrent ? 1 : isCompleted ? 0.6 : 0.3,
                }}
              />
              <span
                className="text-[8px] mt-0.5 font-medium truncate w-full text-center"
                style={{
                  color: isCurrent ? color : isCompleted ? "#94A3B8" : "#CBD5E1",
                  fontWeight: isCurrent ? 700 : 400,
                }}
              >
                {STAGE_LABELS[stage]}
              </span>
            </div>
            {idx < STAGES.length - 1 && (
              <div className="w-1 h-1.5 flex-shrink-0" />
            )}
          </div>
        );
      })}
    </div>
  );
}

function ThreadCard({
  job,
  selected,
  onClick,
}: {
  job: SwarmJob;
  selected: boolean;
  onClick: () => void;
}) {
  const sentiment: Sentiment = SENTIMENT_MAP[job.id] ?? "Curieux";
  const sentStyle = SENTIMENT_STYLE[sentiment];
  const stageColor = STAGE_COLORS[job.stage] ?? "#6B7280";
  const stageLabel = STAGE_LABELS[job.stage] ?? job.stage;

  return (
    <button
      onClick={onClick}
      className={`w-full text-left rounded-xl border p-4 transition-all ${
        selected
          ? "border-blue-400 bg-blue-50 shadow-sm"
          : "border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50"
      }`}
    >
      {/* Header row */}
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <p className="text-[13px] font-semibold text-slate-900 truncate">{job.companyName}</p>
          <p className="text-[11px] text-slate-400 mt-0.5">
            {job.sector} · <span className="font-medium text-slate-600">Agent {job.assignedAgent}</span>
          </p>
        </div>
        <div className="flex flex-col items-end gap-1.5 flex-shrink-0">
          <span
            className="text-[10px] font-bold px-2 py-0.5 rounded-full"
            style={{ backgroundColor: `${stageColor}18`, color: stageColor }}
          >
            {stageLabel}
          </span>
          {job.amount && (
            <span className="text-[12px] font-bold text-emerald-600">{job.amount}€</span>
          )}
        </div>
      </div>

      {/* Sentiment badge */}
      <div className="flex items-center gap-1.5 mt-2.5">
        <span
          className={`inline-flex items-center gap-1 text-[10px] font-semibold px-2 py-0.5 rounded-full ${sentStyle.bg} ${sentStyle.text}`}
        >
          <span className={`w-1.5 h-1.5 rounded-full ${sentStyle.dot}`} />
          {sentiment}
        </span>
      </div>

      {/* Mini timeline */}
      <MiniTimeline currentStage={job.stage} />
    </button>
  );
}

function ChatBubble({ msg }: { msg: NegotiationMessage }) {
  const isProspect = msg.role === "prospect";
  const isSystem = msg.role === "system";

  if (isSystem) {
    return (
      <div className="flex items-center gap-2 py-1">
        <div className="flex-1 h-px bg-slate-100" />
        <p className="text-[10px] text-slate-400 font-medium px-2 py-0.5 bg-slate-50 rounded-full border border-slate-100 text-center max-w-xs">
          {msg.content}
        </p>
        <div className="flex-1 h-px bg-slate-100" />
      </div>
    );
  }

  return (
    <div className={`flex gap-2 ${isProspect ? "flex-row-reverse" : "flex-row"}`}>
      {/* Avatar */}
      <div
        className="w-7 h-7 rounded-full flex items-center justify-center text-white text-[10px] font-bold flex-shrink-0 mt-0.5"
        style={{ backgroundColor: msg.color }}
      >
        {isProspect ? "P" : msg.agentId.replace(".", "")}
      </div>

      {/* Bubble */}
      <div className={`max-w-[75%] ${isProspect ? "items-end" : "items-start"} flex flex-col gap-0.5`}>
        <div className="flex items-center gap-1.5">
          <span
            className="text-[10px] font-semibold"
            style={{ color: msg.color }}
          >
            {msg.agentName}
          </span>
          <span className="text-[9px] text-slate-400 font-mono">{msg.timestamp}</span>
        </div>
        <div
          className={`rounded-2xl px-3 py-2 text-[12px] leading-relaxed ${
            isProspect
              ? "bg-amber-50 border border-amber-100 text-amber-900 rounded-tr-sm"
              : "bg-slate-900 text-slate-100 rounded-tl-sm"
          }`}
        >
          {msg.content}
        </div>
      </div>
    </div>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────────

export default function NegotiationsPage() {
  const [data, setData] = useState<SwarmData | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedJobId, setSelectedJobId] = useState<string | null>("j002");
  const [showAll, setShowAll] = useState(false);
  const [simVisible, setSimVisible] = useState(SIMULATION_DIALOGUE.length);

  useEffect(() => {
    fetch("/api/swarm")
      .then((r) => r.json())
      .then((d: SwarmData) => {
        setData(d);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const jobs = data?.jobs ?? [];

  // Filter negotiation-stage jobs, plus all for context
  const negotiationJobs = jobs.filter(
    (j) => j.stage === "negotiation" || j.stage === "outreach" || j.stage === "paid"
  );
  const displayedJobs = showAll ? negotiationJobs : negotiationJobs.slice(0, 5);

  const selectedJob = negotiationJobs.find((j) => j.id === selectedJobId) ?? negotiationJobs[0] ?? null;

  // Stats
  const totalThreads = negotiationJobs.length;
  const activeNeg = jobs.filter((j) => j.stage === "negotiation").length;
  const wonDeals = jobs.filter((j) => j.stage === "paid").length;
  const totalRevenue = jobs
    .filter((j) => j.stage === "paid" && j.amount)
    .reduce((s, j) => s + (j.amount ?? 0), 0);

  return (
    <div className="space-y-5 pb-10">
      {/* Page header */}
      <div className="flex items-start justify-between pt-1">
        <div>
          <h1 className="text-[22px] font-semibold text-slate-900 tracking-tight">
            Négociations
          </h1>
          <p className="text-[13px] text-slate-500 mt-0.5">
            Threads actifs · Sentiment IA · Suivi pipeline
          </p>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          <span className="flex items-center gap-1.5 text-[11px] text-slate-400 font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse inline-block" />
            {data?.metrics.activeNegotiations ?? "—"} négociations actives
          </span>
        </div>
      </div>

      {/* Stats strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {loading ? (
          Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-20" />)
        ) : (
          <>
            <StatCard
              label="Threads totaux"
              value={totalThreads}
              sub="outreach + négo + payé"
              color="#8B5CF6"
              icon="💬"
            />
            <StatCard
              label="En négociation"
              value={activeNeg}
              sub="réponse en attente"
              color="#F59E0B"
              icon="🤝"
            />
            <StatCard
              label="Deals gagnés"
              value={wonDeals}
              sub="ce cycle"
              color="#059669"
              icon="✅"
            />
            <StatCard
              label="CA négociations"
              value={`${totalRevenue}€`}
              sub="revenus encaissés"
              color="#EF4444"
              icon="💰"
            />
          </>
        )}
      </div>

      {/* Main two-column layout */}
      <div className="grid lg:grid-cols-[340px_1fr] gap-4">
        {/* Left: thread list */}
        <div className="space-y-2">
          <div className="flex items-center justify-between mb-1">
            <h2 className="text-[13px] font-semibold text-slate-700">Threads actifs</h2>
            <span className="text-[11px] text-slate-400">{negotiationJobs.length} threads</span>
          </div>

          {loading ? (
            Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-28" />)
          ) : negotiationJobs.length === 0 ? (
            <div className="text-center py-12 text-slate-400 text-[13px]">
              Aucune négociation en cours
            </div>
          ) : (
            <>
              {displayedJobs.map((job) => (
                <ThreadCard
                  key={job.id}
                  job={job}
                  selected={selectedJobId === job.id}
                  onClick={() => setSelectedJobId(job.id)}
                />
              ))}
              {negotiationJobs.length > 5 && (
                <button
                  onClick={() => setShowAll((v) => !v)}
                  className="w-full text-[12px] text-blue-600 font-medium py-2 hover:bg-blue-50 rounded-lg transition-colors border border-blue-100"
                >
                  {showAll
                    ? "Réduire"
                    : `Voir ${negotiationJobs.length - 5} autres threads`}
                </button>
              )}
            </>
          )}
        </div>

        {/* Right: detail + simulation */}
        <div className="space-y-4">
          {/* Selected thread detail */}
          {selectedJob && (
            <div className="bg-white rounded-xl border border-slate-200 p-5">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h3 className="text-[15px] font-semibold text-slate-900">
                    {selectedJob.companyName}
                  </h3>
                  <p className="text-[12px] text-slate-400 mt-0.5">
                    {selectedJob.sector} · Agent {selectedJob.assignedAgent} ·{" "}
                    <span className="font-mono text-[10px]">{selectedJob.id.toUpperCase()}</span>
                  </p>
                </div>
                <div className="text-right flex-shrink-0">
                  <span
                    className="text-[11px] font-bold px-2.5 py-1 rounded-full"
                    style={{
                      backgroundColor: `${STAGE_COLORS[selectedJob.stage]}15`,
                      color: STAGE_COLORS[selectedJob.stage],
                    }}
                  >
                    {STAGE_LABELS[selectedJob.stage]}
                  </span>
                  {selectedJob.amount && (
                    <p className="text-[16px] font-bold text-emerald-600 mt-1">
                      {selectedJob.amount}€
                    </p>
                  )}
                </div>
              </div>

              {/* Full pipeline timeline */}
              <div className="mt-5">
                <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wide mb-3">
                  Pipeline
                </p>
                <div className="flex items-start gap-0">
                  {STAGES.map((stage, idx) => {
                    const currentIdx = STAGES.indexOf(selectedJob.stage);
                    const isCompleted = idx < currentIdx;
                    const isCurrent = idx === currentIdx;
                    const color = STAGE_COLORS[stage];
                    return (
                      <div key={stage} className="flex-1 flex flex-col items-center relative">
                        {/* Connector line left */}
                        {idx > 0 && (
                          <div
                            className="absolute left-0 top-[14px] w-1/2 h-0.5 -translate-y-1/2"
                            style={{
                              backgroundColor: idx <= currentIdx ? STAGE_COLORS[STAGES[idx - 1]] : "#E2E8F0",
                            }}
                          />
                        )}
                        {/* Connector line right */}
                        {idx < STAGES.length - 1 && (
                          <div
                            className="absolute right-0 top-[14px] w-1/2 h-0.5 -translate-y-1/2"
                            style={{
                              backgroundColor: idx < currentIdx ? color : "#E2E8F0",
                            }}
                          />
                        )}
                        {/* Circle */}
                        <div
                          className="w-7 h-7 rounded-full flex items-center justify-center z-10 border-2 transition-all"
                          style={{
                            borderColor: isCompleted || isCurrent ? color : "#E2E8F0",
                            backgroundColor: isCurrent ? color : isCompleted ? `${color}30` : "white",
                          }}
                        >
                          {isCompleted ? (
                            <svg className="w-3.5 h-3.5" viewBox="0 0 16 16" fill="white">
                              <path d="M13.78 4.22a.75.75 0 010 1.06l-7.25 7.25a.75.75 0 01-1.06 0L2.22 9.28a.75.75 0 011.06-1.06L6 10.94l6.72-6.72a.75.75 0 011.06 0z" />
                            </svg>
                          ) : isCurrent ? (
                            <div className="w-2 h-2 rounded-full bg-white" />
                          ) : (
                            <div
                              className="w-2 h-2 rounded-full"
                              style={{ backgroundColor: "#CBD5E1" }}
                            />
                          )}
                        </div>
                        <p
                          className="text-[10px] mt-1.5 text-center font-medium"
                          style={{ color: isCurrent ? color : isCompleted ? "#64748B" : "#CBD5E1" }}
                        >
                          {STAGE_LABELS[stage]}
                        </p>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Sentiment */}
              <div className="mt-4 pt-4 border-t border-slate-100 flex items-center gap-3">
                <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wide">
                  Sentiment détecté
                </p>
                {(() => {
                  const sentiment: Sentiment = SENTIMENT_MAP[selectedJob.id] ?? "Curieux";
                  const s = SENTIMENT_STYLE[sentiment];
                  return (
                    <span
                      className={`inline-flex items-center gap-1.5 text-[11px] font-semibold px-2.5 py-1 rounded-full ${s.bg} ${s.text}`}
                    >
                      <span className={`w-2 h-2 rounded-full ${s.dot}`} />
                      {sentiment}
                    </span>
                  );
                })()}
              </div>
            </div>
          )}

          {/* Simulation panel */}
          <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-100">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-[14px] font-semibold text-slate-900">
                    Simulation — Négociation en direct
                  </h3>
                  <p className="text-[11px] text-slate-400 mt-0.5">
                    Agent 3.5 (Vente) × Agent 5.1 (Finance) × M. Girard, Restaurateur Lyon
                  </p>
                </div>
                <span className="flex items-center gap-1.5 text-[10px] font-semibold text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full border border-emerald-100">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  LIVE
                </span>
              </div>
            </div>

            <div className="p-5 space-y-3 max-h-[480px] overflow-y-auto">
              {SIMULATION_DIALOGUE.slice(0, simVisible).map((msg, idx) => (
                <ChatBubble key={idx} msg={msg} />
              ))}

              {simVisible >= SIMULATION_DIALOGUE.length && (
                <div className="flex items-center gap-2 pt-2 border-t border-slate-100 mt-2">
                  <div className="w-5 h-5 rounded-full bg-emerald-100 flex items-center justify-center flex-shrink-0">
                    <svg className="w-3 h-3 text-emerald-600" viewBox="0 0 16 16" fill="currentColor">
                      <path d="M13.78 4.22a.75.75 0 010 1.06l-7.25 7.25a.75.75 0 01-1.06 0L2.22 9.28a.75.75 0 011.06-1.06L6 10.94l6.72-6.72a.75.75 0 011.06 0z" />
                    </svg>
                  </div>
                  <span className="text-[12px] font-semibold text-emerald-700">
                    Deal conclu — 149€ encaissés · Durée cycle : 3min 35sec
                  </span>
                </div>
              )}
            </div>

            {simVisible < SIMULATION_DIALOGUE.length && (
              <div className="px-5 pb-4">
                <button
                  onClick={() => setSimVisible((v) => Math.min(v + 3, SIMULATION_DIALOGUE.length))}
                  className="w-full text-[12px] text-blue-600 font-medium py-2 hover:bg-blue-50 rounded-lg transition-colors border border-blue-100"
                >
                  Afficher la suite ({SIMULATION_DIALOGUE.length - simVisible} messages)
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
