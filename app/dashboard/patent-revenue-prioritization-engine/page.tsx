"use client";
import { useEffect, useState } from "react";

const GOLD = "#c9a84c";

function GaugeRing({ value, color }: { value: number; color: string }) {
  const r = 36, cx = 44, cy = 44;
  const circ = 2 * Math.PI * r;
  const offset = circ - (value / 100) * circ;
  return (
    <svg viewBox="0 0 88 88" className="w-full h-full">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={8}
        strokeDasharray={circ} strokeDashoffset={offset}
        strokeLinecap="round" transform="rotate(-90 44 44)" />
    </svg>
  );
}

export default function PatentRevenuePrioritizationPage() {
  const [data, setData] = useState<Record<string, unknown> | null>(null);
  useEffect(() => {
    fetch("/api/patent-revenue-prioritization-engine")
      .then((r) => r.json())
      .then((d) => setData(d.payload ?? d));
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400 text-sm">Chargement...</div>
    </div>
  );

  const entities = (data.entities as Array<Record<string, unknown>>) ?? [];
  const avgComposite = (data.avg_composite as number) ?? 0;
  const riskDist = (data.risk_distribution as Record<string, number>) ?? {};
  const totalEntities = (data.total_entities as number) ?? 0;
  const confidence = (data.confidence_score as number) ?? 0;
  const avgIndex = (Object.entries(data).find(([k]) => k.startsWith("avg_estimated_"))?.[1] as number) ?? 0;
  const revenueForecast = (data.revenue_forecast as Record<string, Record<string, string>>) ?? {};

  const priorityColor = (level: string) => {
    if (level === "critique") return "#c9a84c";
    if (level === "élevé") return "#f97316";
    if (level === "modéré") return "#eab308";
    return "#64748b";
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-5xl mx-auto space-y-8">
        <div className="border-b border-slate-800 pb-6">
          <h1 className="text-2xl font-bold tracking-tight" style={{ color: GOLD }}>
            Priorisation Brevets — Potentiel Revenus Caelum
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            EPO · USPTO · Forêt Brevets 2025-2049 · Licences obligatoires — Inventrice : Chaima Mhadbi
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Score Priorité", value: avgComposite.toFixed(2), unit: "/100" },
            { label: "Indice Moyen", value: avgIndex.toFixed(2), unit: "/10" },
            { label: "Confiance", value: (confidence * 100).toFixed(0), unit: "%" },
            { label: "Inventions", value: String(totalEntities), unit: "" },
          ].map(({ label, value, unit }) => (
            <div key={label} className="rounded-xl bg-slate-900 border border-slate-800 p-4 text-center">
              <div className="text-xs text-slate-500 uppercase tracking-widest mb-1">{label}</div>
              <div className="text-2xl font-bold" style={{ color: GOLD }}>{value}<span className="text-sm text-slate-500 ml-1">{unit}</span></div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="rounded-xl bg-slate-900 border border-slate-800 p-6 flex flex-col items-center">
            <div className="text-xs text-slate-500 uppercase tracking-widest mb-4">Score Priorité Global</div>
            <div className="w-32 h-32"><GaugeRing value={avgComposite} color={GOLD} /></div>
            <div className="mt-3 text-3xl font-bold" style={{ color: GOLD }}>{avgComposite.toFixed(1)}</div>
          </div>
          <div className="rounded-xl bg-slate-900 border border-slate-800 p-6">
            <div className="text-xs text-slate-500 uppercase tracking-widest mb-4">Distribution Priorité</div>
            <div className="space-y-3">
              {Object.entries(riskDist).map(([level, count]) => (
                <div key={level} className="flex items-center gap-3">
                  <div className="text-xs font-medium w-16 capitalize" style={{ color: priorityColor(level) }}>{level}</div>
                  <div className="flex-1 bg-slate-800 rounded-full h-2">
                    <div className="h-2 rounded-full" style={{ width: `${(count / totalEntities) * 100}%`, backgroundColor: priorityColor(level) }} />
                  </div>
                  <div className="text-xs text-slate-400 w-4">{count}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {Object.keys(revenueForecast).length > 0 && (
          <div className="rounded-xl bg-slate-900 border border-yellow-900/30 p-6">
            <div className="text-xs text-yellow-500 uppercase tracking-widest mb-4">Prévisions Revenus — Top 3 Brevets Prioritaires</div>
            <div className="space-y-4">
              {Object.entries(revenueForecast).map(([id, forecast]) => (
                <div key={id} className="rounded-lg bg-slate-800/50 border border-slate-700 p-4">
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-sm font-mono font-bold" style={{ color: GOLD }}>{id}</div>
                    <div className="text-lg font-bold text-green-400">{forecast.annual_potential}</div>
                  </div>
                  <div className="text-xs text-slate-400">{forecast.market}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {entities.length > 0 && (
          <div className="rounded-xl bg-slate-900 border border-slate-800 overflow-hidden">
            <div className="px-6 py-4 border-b border-slate-800">
              <div className="text-xs text-slate-500 uppercase tracking-widest">Inventions — Classement par Priorité</div>
            </div>
            <div className="divide-y divide-slate-800">
              {entities.map((e) => {
                const score = e.composite_score as number;
                const level = e.risk_level as string;
                const name = e.name as string;
                return (
                  <div key={e.entity_id as string} className="px-6 py-3 flex items-center gap-4">
                    <div className="text-xs font-mono text-slate-500 w-24 flex-shrink-0">{e.entity_id as string}</div>
                    <div className="flex-1 text-sm text-slate-300 truncate">{name}</div>
                    <div className="text-xs font-medium capitalize px-2 py-0.5 rounded-full border" style={{ color: priorityColor(level), borderColor: priorityColor(level) + "40" }}>{level}</div>
                    <div className="text-sm font-mono font-bold w-12 text-right" style={{ color: priorityColor(level) }}>{score.toFixed(1)}</div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
