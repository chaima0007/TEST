"use client";

import { useEffect, useState } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

type Confidence = "high" | "medium" | "low";

interface OptimalWindow {
  sector: string;
  day_of_week: number;
  day_name: string;
  hour_start: number;
  hour_end: number;
  score: number;
  confidence: Confidence;
  rationale: string;
  top_windows?: OptimalWindow[];
}

interface TimingData {
  sectors: OptimalWindow[];
  known_sectors: string[];
}

// ─── Constants ────────────────────────────────────────────────────────────────

const DAY_NAMES = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"];

const CONFIDENCE_META: Record<Confidence, { label: string; color: string; dot: string }> = {
  high:   { label: "Élevée",  color: "text-emerald-400", dot: "bg-emerald-400" },
  medium: { label: "Moyenne", color: "text-amber-400",   dot: "bg-amber-400"   },
  low:    { label: "Faible",  color: "text-slate-400",   dot: "bg-slate-400"   },
};

const SECTOR_LABELS: Record<string, string> = {
  artisan: "Artisan", restaurant: "Restaurant", médecin: "Médecin",
  comptable: "Comptable", avocat: "Avocat", PME: "PME", immobilier: "Immobilier",
  hôtel: "Hôtel", dentiste: "Dentiste", notaire: "Notaire",
};

// ─── Sub-components ───────────────────────────────────────────────────────────

function ScoreBar({ score }: { score: number }) {
  const color = score >= 70 ? "bg-emerald-500" : score >= 50 ? "bg-blue-500" : score >= 30 ? "bg-amber-500" : "bg-slate-600";
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-2 rounded-full ${color} transition-all`} style={{ width: `${score}%` }} />
      </div>
      <span className="text-xs font-bold tabular-nums w-8 text-right text-slate-300">{score}</span>
    </div>
  );
}

function DayHeatmap({ sector, schedule }: { sector: string; schedule: Record<string, Record<number, number>> }) {
  const hours = Array.from({ length: 14 }, (_, i) => i + 6);
  const days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"];

  const maxScore = Math.max(...days.flatMap((d) => hours.map((h) => schedule[d]?.[h] ?? 0)));

  return (
    <div className="overflow-x-auto">
      <div className="min-w-[500px]">
        {/* Hour headers */}
        <div className="flex gap-0.5 mb-1 ml-14">
          {hours.map((h) => (
            <div key={h} className="flex-1 text-center text-[9px] text-slate-600">{h}h</div>
          ))}
        </div>
        {/* Day rows */}
        {days.map((day, dayIdx) => (
          <div key={day} className="flex items-center gap-0.5 mb-0.5">
            <div className="w-14 text-xs text-slate-500 flex-shrink-0">
              {DAY_NAMES[dayIdx]}
            </div>
            {hours.map((h) => {
              const score = schedule[day]?.[h] ?? 0;
              const intensity = maxScore > 0 ? score / maxScore : 0;
              const bg = intensity >= 0.85 ? "bg-emerald-500" :
                intensity >= 0.65 ? "bg-emerald-600/80" :
                intensity >= 0.45 ? "bg-blue-600/70" :
                intensity >= 0.25 ? "bg-slate-700" :
                intensity > 0 ? "bg-slate-800" : "bg-slate-900";
              return (
                <div
                  key={h}
                  title={`${day} ${h}h: ${score}`}
                  className={`flex-1 h-6 rounded-sm ${bg} transition-colors cursor-default`}
                />
              );
            })}
          </div>
        ))}
        <div className="flex items-center gap-2 mt-2 ml-14">
          <span className="text-[9px] text-slate-600">Faible</span>
          <div className="flex gap-0.5">
            {["bg-slate-900", "bg-slate-800", "bg-slate-700", "bg-blue-600/70", "bg-emerald-600/80", "bg-emerald-500"].map((c, i) => (
              <div key={i} className={`w-4 h-2 rounded-sm ${c}`} />
            ))}
          </div>
          <span className="text-[9px] text-slate-600">Élevé</span>
        </div>
      </div>
    </div>
  );
}

// ─── Detail Modal ─────────────────────────────────────────────────────────────

function DetailModal({ window: w, onClose }: { window: OptimalWindow; onClose: () => void }) {
  const [schedule, setSchedule] = useState<Record<string, Record<number, number>> | null>(null);

  useEffect(() => {
    const h = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  useEffect(() => {
    fetch(`/api/timing?sector=${encodeURIComponent(w.sector)}`)
      .then((r) => r.json())
      .then((d) => setSchedule(d.schedule ?? null));
  }, [w.sector]);

  const cm = CONFIDENCE_META[w.confidence];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm" onClick={onClose}>
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl w-full max-w-2xl mx-4 p-6 space-y-5"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-white font-bold text-lg capitalize">
              {SECTOR_LABELS[w.sector] ?? w.sector}
            </h2>
            <p className="text-slate-400 text-sm mt-0.5">
              Meilleur créneau : <span className="text-white font-semibold">{w.day_name} {w.hour_start}h–{w.hour_end}h</span>
            </p>
          </div>
          <div className="text-right">
            <p className="text-3xl font-black text-indigo-400">{w.score}</p>
            <p className="text-xs text-slate-500">/100</p>
          </div>
        </div>

        <ScoreBar score={w.score} />

        {/* Confidence */}
        <div className="flex items-center gap-2">
          <span className={`w-2 h-2 rounded-full ${cm.dot}`} />
          <span className={`text-sm font-medium ${cm.color}`}>Confiance {cm.label}</span>
        </div>

        {/* Rationale */}
        <div className="bg-indigo-950/40 border border-indigo-900/50 rounded-lg p-3">
          <p className="text-xs text-indigo-400 font-semibold mb-1">Justification</p>
          <p className="text-slate-300 text-sm">{w.rationale}</p>
        </div>

        {/* Top 3 windows */}
        {w.top_windows && w.top_windows.length > 0 && (
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-2">Top créneaux</p>
            <div className="space-y-2">
              {w.top_windows.slice(0, 3).map((tw, i) => (
                <div key={i} className="flex items-center gap-3 bg-slate-800/60 rounded-lg p-3">
                  <span className="text-slate-500 text-xs w-4">#{i + 1}</span>
                  <span className="text-slate-300 text-sm font-medium flex-1">
                    {tw.day_name} {tw.hour_start}h–{tw.hour_end}h
                  </span>
                  <ScoreBar score={tw.score} />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Heatmap */}
        {schedule && (
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-3">Heatmap hebdomadaire</p>
            <DayHeatmap sector={w.sector} schedule={schedule} />
          </div>
        )}

        <button
          onClick={onClose}
          className="w-full py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-medium transition-colors"
        >
          Fermer
        </button>
      </div>
    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function TimingPage() {
  const [data, setData] = useState<TimingData | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<OptimalWindow | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/timing")
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="p-6 space-y-6 text-slate-100">
      <div>
        <h1 className="text-2xl font-bold text-white">Timing Optimal de Contact</h1>
        <p className="text-slate-400 text-sm mt-1">
          Meilleur jour et créneau horaire par secteur · Score 0–100 · Mardi et Jeudi, 9h-11h et 14h-16h dominent
        </p>
      </div>

      {loading ? (
        <div className="text-slate-500 text-center py-16">Chargement…</div>
      ) : data ? (
        <>
          {/* Sector cards grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {data.sectors.map((w) => {
              const cm = CONFIDENCE_META[w.confidence];
              return (
                <div
                  key={w.sector}
                  onClick={() => setSelected(w)}
                  className="bg-slate-900 border border-slate-800 rounded-xl p-5 cursor-pointer hover:border-slate-600 transition-all space-y-3"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-white font-semibold capitalize">
                        {SECTOR_LABELS[w.sector] ?? w.sector}
                      </p>
                      <p className="text-slate-500 text-xs mt-0.5">
                        {w.day_name} · {w.hour_start}h–{w.hour_end}h
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-black text-indigo-400">{w.score}</p>
                    </div>
                  </div>

                  <ScoreBar score={w.score} />

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-1.5">
                      <span className={`w-1.5 h-1.5 rounded-full ${cm.dot}`} />
                      <span className={`text-xs ${cm.color}`}>{cm.label}</span>
                    </div>
                    <span className="text-xs text-slate-600">Cliquer pour heatmap →</span>
                  </div>

                  <p className="text-xs text-slate-500 line-clamp-2">{w.rationale}</p>
                </div>
              );
            })}
          </div>

          {/* Summary table */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-800">
              <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">
                Récapitulatif par secteur
              </h3>
            </div>
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-800">
                  <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider">Secteur</th>
                  <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider">Jour optimal</th>
                  <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider">Horaire</th>
                  <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider">Score</th>
                  <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider hidden md:table-cell">Confiance</th>
                </tr>
              </thead>
              <tbody>
                {[...data.sectors].sort((a, b) => b.score - a.score).map((w) => {
                  const cm = CONFIDENCE_META[w.confidence];
                  return (
                    <tr
                      key={w.sector}
                      onClick={() => setSelected(w)}
                      className="border-b border-slate-800/50 hover:bg-slate-800/40 cursor-pointer transition-colors"
                    >
                      <td className="py-3 px-4 text-white font-medium capitalize">
                        {SECTOR_LABELS[w.sector] ?? w.sector}
                      </td>
                      <td className="py-3 px-4 text-slate-300 text-sm">{w.day_name}</td>
                      <td className="py-3 px-4 text-slate-300 text-sm font-mono">
                        {w.hour_start}h–{w.hour_end}h
                      </td>
                      <td className="py-3 px-4 w-40">
                        <ScoreBar score={w.score} />
                      </td>
                      <td className="py-3 px-4 hidden md:table-cell">
                        <div className="flex items-center gap-1.5">
                          <span className={`w-1.5 h-1.5 rounded-full ${cm.dot}`} />
                          <span className={`text-xs ${cm.color}`}>{cm.label}</span>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </>
      ) : (
        <p className="text-slate-500">Erreur de chargement.</p>
      )}

      {selected && <DetailModal window={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
