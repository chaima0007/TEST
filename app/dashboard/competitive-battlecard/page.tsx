"use client";

import { useEffect, useState } from "react";

interface Battlecard {
  competitor_id: string;
  competitor_name: string;
  market_position: string;
  threat_score: number;
  threat_level: string;
  win_probability: string;
  battlecard_action: string;
  executive_summary: string;
  our_advantages: string[];
  their_advantages: string[];
  counter_tactics: string[];
  talk_tracks: string[];
  objection_responses: string[];
  red_flags: string[];
}

interface Summary {
  total: number;
  threat_counts: Record<string, number>;
  action_counts: Record<string, number>;
  win_probability_counts: Record<string, number>;
  avg_threat_score: number;
  critical_count: number;
  escalation_count: number;
}

const THREAT_COLOR: Record<string, string> = {
  critical: "#ef4444",
  high: "#f59e0b",
  medium: "#38bdf8",
  low: "#10b981",
};

const THREAT_BADGE: Record<string, string> = {
  critical: "bg-red-900/60 text-red-300 border-red-700",
  high: "bg-amber-900/60 text-amber-300 border-amber-700",
  medium: "bg-sky-900/60 text-sky-300 border-sky-700",
  low: "bg-emerald-900/60 text-emerald-300 border-emerald-700",
};

const ACTION_BADGE: Record<string, string> = {
  escalate: "bg-red-900/60 text-red-300 border-red-700",
  differentiate: "bg-violet-900/60 text-violet-300 border-violet-700",
  counter: "bg-amber-900/60 text-amber-300 border-amber-700",
  monitor: "bg-slate-800 text-slate-400 border-slate-600",
};

const WIN_BADGE: Record<string, string> = {
  strong: "bg-emerald-900/60 text-emerald-300 border-emerald-700",
  moderate: "bg-sky-900/60 text-sky-300 border-sky-700",
  weak: "bg-amber-900/60 text-amber-300 border-amber-700",
  very_weak: "bg-red-900/60 text-red-300 border-red-700",
};

function ThreatRing({ score, threat }: { score: number; threat: string }) {
  const r = 40;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;
  const stroke = THREAT_COLOR[threat] || "#64748b";
  return (
    <svg width="96" height="96" viewBox="0 0 96 96">
      <circle cx="48" cy="48" r={r} fill="none" stroke="#1e293b" strokeWidth="10" />
      <circle
        cx="48"
        cy="48"
        r={r}
        fill="none"
        stroke={stroke}
        strokeWidth="10"
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform="rotate(-90 48 48)"
      />
      <text x="48" y="53" textAnchor="middle" fill="#f1f5f9" fontSize="18" fontWeight="bold">
        {Math.round(score)}
      </text>
    </svg>
  );
}

function ThreatBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  if (!total) return null;
  const segments = [
    { key: "critical", label: "Critique", color: "bg-red-500" },
    { key: "high", label: "Élevée", color: "bg-amber-500" },
    { key: "medium", label: "Moyenne", color: "bg-sky-500" },
    { key: "low", label: "Faible", color: "bg-emerald-500" },
  ];
  return (
    <div className="mb-6">
      <div className="flex rounded-full overflow-hidden h-3 mb-2">
        {segments.map(({ key, color }) => {
          const pct = ((counts[key] || 0) / total) * 100;
          return pct > 0 ? (
            <div key={key} className={`${color} h-3`} style={{ width: `${pct}%` }} title={`${key}: ${counts[key]}`} />
          ) : null;
        })}
      </div>
      <div className="flex gap-4 text-xs text-slate-400">
        {segments.map(({ key, label, color }) => (
          <span key={key} className="flex items-center gap-1">
            <span className={`inline-block w-2 h-2 rounded-full ${color}`} />
            {label} ({counts[key] || 0})
          </span>
        ))}
      </div>
    </div>
  );
}

function actionLabel(action: string) {
  const map: Record<string, string> = {
    escalate: "Escalader",
    differentiate: "Différencier",
    counter: "Contrer",
    monitor: "Surveiller",
  };
  return map[action] || action;
}

function winLabel(win: string) {
  const map: Record<string, string> = {
    strong: "Victoire probable",
    moderate: "Modérée",
    weak: "Difficile",
    very_weak: "Très difficile",
  };
  return map[win] || win;
}

function positionLabel(pos: string) {
  const map: Record<string, string> = {
    leader: "Leader",
    challenger: "Challenger",
    niche: "Niche",
    emerging: "Émergent",
  };
  return map[pos] || pos;
}

function BattlecardCard({ card, onClick }: { card: Battlecard; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className="bg-slate-800/60 border border-slate-700 rounded-xl p-5 cursor-pointer hover:border-slate-500 hover:bg-slate-800 transition-all"
    >
      <div className="flex items-start gap-4 mb-4">
        <ThreatRing score={card.threat_score} threat={card.threat_level} />
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-slate-100 text-base truncate">{card.competitor_name}</h3>
          <p className="text-slate-400 text-sm">{positionLabel(card.market_position)}</p>
          <div className="flex flex-wrap gap-1 mt-2">
            <span className={`text-xs px-2 py-0.5 rounded-full border font-medium capitalize ${THREAT_BADGE[card.threat_level]}`}>
              {card.threat_level}
            </span>
            <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${ACTION_BADGE[card.battlecard_action]}`}>
              {actionLabel(card.battlecard_action)}
            </span>
          </div>
        </div>
      </div>

      <div className={`text-xs px-2 py-1 rounded-full border text-center mb-3 ${WIN_BADGE[card.win_probability]}`}>
        {winLabel(card.win_probability)}
      </div>

      <div className="grid grid-cols-2 gap-2 mb-3 text-sm">
        <div className="text-slate-400">
          <span className="text-xs text-slate-500">Nos avantages</span>
          <div className="text-slate-300 font-medium">{card.our_advantages.length}</div>
        </div>
        <div className="text-slate-400">
          <span className="text-xs text-slate-500">Signaux d'alerte</span>
          <div className={`font-medium ${card.red_flags.length > 0 ? "text-red-400" : "text-emerald-400"}`}>
            {card.red_flags.length}
          </div>
        </div>
      </div>

      <p className="text-slate-500 text-xs line-clamp-2">{card.executive_summary}</p>

      <div className="mt-3">
        <div className="flex justify-between text-xs text-slate-500 mb-1">
          <span>Score menace</span>
          <span>{Math.round(card.threat_score)}/100</span>
        </div>
        <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
          <div
            className="h-1.5 rounded-full"
            style={{
              width: `${card.threat_score}%`,
              backgroundColor: THREAT_COLOR[card.threat_level] || "#64748b",
            }}
          />
        </div>
      </div>
    </div>
  );
}

function BattlecardModal({ card, onClose }: { card: Battlecard; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "tactics" | "tracks" | "objections">("overview");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-6 border-b border-slate-800 flex items-start gap-4">
          <ThreatRing score={card.threat_score} threat={card.threat_level} />
          <div className="flex-1">
            <h2 className="text-xl font-bold text-slate-100">{card.competitor_name}</h2>
            <p className="text-slate-400 text-sm">{positionLabel(card.market_position)}</p>
            <div className="flex flex-wrap gap-2 mt-2">
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium capitalize ${THREAT_BADGE[card.threat_level]}`}>
                Menace {card.threat_level}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${ACTION_BADGE[card.battlecard_action]}`}>
                {actionLabel(card.battlecard_action)}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full border ${WIN_BADGE[card.win_probability]}`}>
                {winLabel(card.win_probability)}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-2xl leading-none">&times;</button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["overview", "tactics", "tracks", "objections"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2 text-xs font-medium capitalize transition-colors ${
                tab === t
                  ? "text-indigo-400 border-b-2 border-indigo-500"
                  : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "overview" ? "Aperçu" : t === "tactics" ? "Tactiques" : t === "tracks" ? "Talk Tracks" : "Objections"}
            </button>
          ))}
        </div>

        <div className="p-6 space-y-5">
          {tab === "overview" && (
            <>
              <p className="text-sm text-slate-300 bg-slate-800 rounded-xl p-4 leading-relaxed">
                {card.executive_summary}
              </p>

              {card.our_advantages.length > 0 && (
                <div>
                  <h3 className="text-sm font-semibold text-emerald-400 mb-2 flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block" />
                    Nos avantages
                  </h3>
                  <ul className="space-y-1.5">
                    {card.our_advantages.map((a, i) => (
                      <li key={i} className="text-sm text-slate-300 bg-emerald-900/20 border border-emerald-800/40 rounded-lg px-3 py-2">
                        {a}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {card.their_advantages.length > 0 && (
                <div>
                  <h3 className="text-sm font-semibold text-red-400 mb-2 flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-red-400 inline-block" />
                    Leurs avantages
                  </h3>
                  <ul className="space-y-1.5">
                    {card.their_advantages.map((a, i) => (
                      <li key={i} className="text-sm text-slate-300 bg-red-900/20 border border-red-800/40 rounded-lg px-3 py-2">
                        {a}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {card.red_flags.length > 0 && (
                <div>
                  <h3 className="text-sm font-semibold text-orange-400 mb-2 flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-orange-400 inline-block" />
                    Signaux d'alerte
                  </h3>
                  <ul className="space-y-1.5">
                    {card.red_flags.map((f, i) => (
                      <li key={i} className="text-sm text-slate-300 bg-orange-900/20 border border-orange-800/40 rounded-lg px-3 py-2">
                        {f}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </>
          )}

          {tab === "tactics" && (
            <div>
              <h3 className="text-sm font-semibold text-amber-400 mb-3 flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-400 inline-block" />
                Tactiques de contre
              </h3>
              <ol className="space-y-2">
                {card.counter_tactics.map((t, i) => (
                  <li key={i} className="text-sm text-slate-300 bg-amber-900/20 border border-amber-800/40 rounded-lg px-3 py-2 flex gap-2">
                    <span className="text-amber-400 font-bold shrink-0">{i + 1}.</span>
                    {t}
                  </li>
                ))}
              </ol>
            </div>
          )}

          {tab === "tracks" && (
            <div>
              <h3 className="text-sm font-semibold text-indigo-400 mb-3 flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 inline-block" />
                Talk Tracks
              </h3>
              <ul className="space-y-3">
                {card.talk_tracks.map((t, i) => (
                  <li key={i} className="text-sm text-slate-300 bg-indigo-900/20 border border-indigo-800/40 rounded-xl px-4 py-3 italic">
                    {t}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {tab === "objections" && (
            <div>
              <h3 className="text-sm font-semibold text-violet-400 mb-3 flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-violet-400 inline-block" />
                Réponses aux objections
              </h3>
              <ul className="space-y-2">
                {card.objection_responses.map((r, i) => (
                  <li key={i} className="text-sm text-slate-300 bg-violet-900/20 border border-violet-800/40 rounded-lg px-3 py-2">
                    {r}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

const THREATS = ["all", "critical", "high", "medium", "low"];
const ACTIONS = ["all", "escalate", "differentiate", "counter", "monitor"];

export default function CompetitiveBattlecardPage() {
  const [data, setData] = useState<{ battlecards: Battlecard[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedCard, setSelectedCard] = useState<Battlecard | null>(null);
  const [threatFilter, setThreatFilter] = useState("all");
  const [actionFilter, setActionFilter] = useState("all");

  useEffect(() => {
    async function load() {
      const params = new URLSearchParams();
      if (threatFilter !== "all") params.set("threat", threatFilter);
      if (actionFilter !== "all") params.set("action", actionFilter);
      const res = await fetch(`/api/competitive-battlecard?${params}`);
      const json = await res.json();
      setData(json);
      setLoading(false);
    }
    load();
  }, [threatFilter, actionFilter]);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-400 animate-pulse">Chargement battlecards...</div>
      </div>
    );
  }

  const s = data!.summary;

  const kpis = [
    { label: "Score Menace Moy.", value: s.avg_threat_score.toFixed(1), sub: "/ 100" },
    { label: "Menaces Critiques", value: s.critical_count, sub: "escalade requise" },
    { label: "Escalades", value: s.escalation_count, sub: "deals à risque" },
    { label: "Concurrents", value: s.total, sub: "analysés" },
    { label: "À Différencier", value: s.action_counts["differentiate"] || 0, sub: "menace high" },
    { label: "À Surveiller", value: s.action_counts["monitor"] || 0, sub: "menace faible" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-100">Battlecards Concurrents</h1>
          <p className="text-slate-400 mt-1">Intelligence concurrentielle IA — tactiques, talk tracks et réponses aux objections en temps réel</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
          {kpis.map(({ label, value, sub }) => (
            <div key={label} className="bg-slate-800/60 border border-slate-700 rounded-xl p-4">
              <div className="text-2xl font-bold text-slate-100">{value}</div>
              <div className="text-xs text-slate-400 mt-0.5">{label}</div>
              <div className="text-xs text-slate-600 mt-0.5">{sub}</div>
            </div>
          ))}
        </div>

        <ThreatBar counts={s.threat_counts} total={s.total} />

        <div className="flex flex-wrap gap-2 mb-3">
          {THREATS.map((v) => (
            <button
              key={v}
              onClick={() => setThreatFilter(v)}
              className={`text-xs px-3 py-1.5 rounded-full border transition-colors capitalize ${
                threatFilter === v
                  ? "bg-indigo-600 border-indigo-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500"
              }`}
            >
              {v === "all" ? "Toutes menaces" : v}
              {v !== "all" && s.threat_counts[v] ? ` (${s.threat_counts[v]})` : ""}
            </button>
          ))}
        </div>

        <div className="flex flex-wrap gap-2 mb-8">
          {ACTIONS.map((v) => (
            <button
              key={v}
              onClick={() => setActionFilter(v)}
              className={`text-xs px-3 py-1.5 rounded-full border transition-colors ${
                actionFilter === v
                  ? "bg-red-600 border-red-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500"
              }`}
            >
              {v === "all" ? "Toutes actions" : actionLabel(v)}
              {v !== "all" && s.action_counts[v] ? ` (${s.action_counts[v]})` : ""}
            </button>
          ))}
        </div>

        {data!.battlecards.length === 0 ? (
          <div className="text-center text-slate-500 py-20">Aucun concurrent pour ces filtres</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
            {data!.battlecards.map((card) => (
              <BattlecardCard key={card.competitor_id} card={card} onClick={() => setSelectedCard(card)} />
            ))}
          </div>
        )}
      </div>

      {selectedCard && <BattlecardModal card={selectedCard} onClose={() => setSelectedCard(null)} />}
    </div>
  );
}
