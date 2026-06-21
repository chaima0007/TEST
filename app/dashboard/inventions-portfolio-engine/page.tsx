"use client";
import { useEffect, useState } from "react";

const ACCENT = "#1a0a5a";

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

export default function InventionsPortfolioPage() {
  const [data, setData] = useState<Record<string, unknown> | null>(null);
  useEffect(() => {
    fetch("/api/inventions-portfolio-engine")
      .then((r) => r.json())
      .then((d) => setData(d.payload ?? d));
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400 text-sm">Chargement...</div>
    </div>
  );

  const entities = (data.entities as Array<Record<string, unknown>>) ?? [];
  const avgComposite = (data.avg_patentability_score as number) ?? 0;
  const genDist = (data.generation_distribution as Record<string, number>) ?? {};
  const totalInventions = (data.total_inventions as number) ?? 0;
  const confidence = (data.confidence_score as number) ?? 0;
  const inventor = (data.inventor as string) ?? "";

  const genColor = (gen: string) => {
    if (gen === "G1") return "#6366f1";
    if (gen === "G2") return "#8b5cf6";
    if (gen === "G3") return "#a855f7";
    return "#c084fc";
  };

  const statusBadge = (status: string) => {
    if (status === "filed") return { color: "#22c55e", label: "Déposé" };
    if (status === "granted") return { color: "#3b82f6", label: "Accordé" };
    return { color: "#eab308", label: "Draft" };
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-5xl mx-auto space-y-8">
        <div className="border-b border-slate-800 pb-6">
          <h1 className="text-2xl font-bold tracking-tight" style={{ color: ACCENT }}>
            Portefeuille de Brevets — Caelum Partners
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            Inventrice : {inventor} · EPO / USPTO · Intelligence Artificielle &amp; Droits Humains
          </p>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Score Moyen", value: avgComposite.toFixed(2), unit: "/10" },
            { label: "Confiance", value: (confidence * 100).toFixed(0), unit: "%" },
            { label: "Inventions", value: String(totalInventions), unit: "" },
            { label: "Générations", value: String(Object.keys(genDist).length), unit: "" },
          ].map(({ label, value, unit }) => (
            <div key={label} className="rounded-xl bg-slate-900 border border-slate-800 p-4 text-center">
              <div className="text-xs text-slate-500 uppercase tracking-widest mb-1">{label}</div>
              <div className="text-2xl font-bold" style={{ color: ACCENT }}>{value}<span className="text-sm text-slate-500 ml-1">{unit}</span></div>
            </div>
          ))}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="rounded-xl bg-slate-900 border border-slate-800 p-6 flex flex-col items-center">
            <div className="text-xs text-slate-500 uppercase tracking-widest mb-4">Score Brevetabilité Global</div>
            <div className="w-32 h-32"><GaugeRing value={avgComposite * 10} color={ACCENT} /></div>
            <div className="mt-3 text-3xl font-bold" style={{ color: ACCENT }}>{avgComposite.toFixed(2)}<span className="text-base text-slate-500 ml-1">/10</span></div>
          </div>
          <div className="rounded-xl bg-slate-900 border border-slate-800 p-6">
            <div className="text-xs text-slate-500 uppercase tracking-widest mb-4">Distribution par Génération</div>
            <div className="space-y-3">
              {Object.entries(genDist).map(([gen, count]) => (
                <div key={gen} className="flex items-center gap-3">
                  <div className="text-xs font-mono font-medium w-8" style={{ color: genColor(gen) }}>{gen}</div>
                  <div className="flex-1 bg-slate-800 rounded-full h-2">
                    <div className="h-2 rounded-full" style={{ width: `${(count / totalInventions) * 100}%`, backgroundColor: genColor(gen) }} />
                  </div>
                  <div className="text-xs text-slate-400 w-4">{count}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
        {entities.length > 0 && (
          <div className="rounded-xl bg-slate-900 border border-slate-800 overflow-hidden">
            <div className="px-6 py-4 border-b border-slate-800">
              <div className="text-xs text-slate-500 uppercase tracking-widest">Inventions du Portefeuille</div>
            </div>
            <div className="divide-y divide-slate-800">
              {entities.map((e) => {
                const gen = e.generation as string;
                const name = e.name as string;
                const id = e.entity_id as string;
                const ipc = e.ipc_class as string;
                const score = e.patentability_score as number;
                const status = e.filing_status as string;
                const badge = statusBadge(status);
                return (
                  <div key={id} className="px-6 py-4 flex items-start gap-4">
                    <div className="text-xs font-mono font-bold w-24 pt-0.5" style={{ color: genColor(gen) }}>{id}</div>
                    <div className="flex-1 min-w-0">
                      <div className="text-sm text-slate-200 font-medium truncate">{name}</div>
                      <div className="text-xs text-slate-500 mt-0.5 font-mono">{ipc}</div>
                    </div>
                    <div className="flex items-center gap-2 flex-shrink-0">
                      <div className="text-xs font-medium px-2 py-0.5 rounded-full border" style={{ color: badge.color, borderColor: badge.color + "40" }}>{badge.label}</div>
                      <div className="text-sm font-mono font-bold w-10 text-right" style={{ color: genColor(gen) }}>{score.toFixed(2)}</div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
        <div className="rounded-xl bg-slate-900 border border-slate-800 p-6">
          <div className="text-xs text-slate-500 uppercase tracking-widest mb-3">Prochaine Étape — Dépôt</div>
          <p className="text-sm text-slate-300">
            Les drafts EPO/USPTO sont disponibles dans <code className="text-purple-400 text-xs bg-slate-800 px-1 py-0.5 rounded">docs/inventions/patents/</code>.
            Consulter <code className="text-purple-400 text-xs bg-slate-800 px-1 py-0.5 rounded">docs/inventions/FILING-GUIDE.md</code> pour les étapes de dépôt, coûts et cabinets recommandés à Bruxelles.
          </p>
        </div>
      </div>
    </div>
  );
}
