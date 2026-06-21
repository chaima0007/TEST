"use client";
import { useEffect, useState } from "react";

const ACCENT = "#0a1a3a";
const CYBER = "#3b82f6";

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

export default function CybersecurityDataProtectionPage() {
  const [data, setData] = useState<Record<string, unknown> | null>(null);
  useEffect(() => {
    fetch("/api/cybersecurity-data-protection-engine")
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
  const layers = (data.protection_layers as Record<string, string>) ?? {};
  const dataMap = (data.data_map as Record<string, string>) ?? {};
  const alerts = (data.critical_alerts as string[]) ?? [];

  const riskColor = (level: string) => {
    if (level === "critique") return "#ef4444";
    if (level === "élevé") return "#f97316";
    if (level === "modéré") return "#eab308";
    return "#22c55e";
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-5xl mx-auto space-y-8">
        <div className="border-b border-slate-800 pb-6">
          <h1 className="text-2xl font-bold tracking-tight" style={{ color: CYBER }}>
            Cybersécurité &amp; Protection des Données Caelum
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            NIST · OWASP · EU NIS2 · ISO 27001 — Zéro virus · Accès Chaima garanti
          </p>
        </div>

        {alerts.length > 0 && (
          <div className="space-y-2">
            {alerts.map((a, i) => (
              <div key={i} className="flex items-start gap-3 rounded-lg bg-red-950/30 border border-red-800/50 px-4 py-3">
                <div className="text-red-400 text-xs mt-0.5">🛡</div>
                <div className="text-xs text-red-300">{a}</div>
              </div>
            ))}
          </div>
        )}

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Menace Avg", value: avgComposite.toFixed(2), unit: "/100" },
            { label: "Indice Risque", value: avgIndex.toFixed(2), unit: "/10" },
            { label: "Confiance", value: (confidence * 100).toFixed(0), unit: "%" },
            { label: "Vecteurs", value: String(totalEntities), unit: "" },
          ].map(({ label, value, unit }) => (
            <div key={label} className="rounded-xl bg-slate-900 border border-slate-800 p-4 text-center">
              <div className="text-xs text-slate-500 uppercase tracking-widest mb-1">{label}</div>
              <div className="text-2xl font-bold" style={{ color: CYBER }}>{value}<span className="text-sm text-slate-500 ml-1">{unit}</span></div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="rounded-xl bg-slate-900 border border-slate-800 p-6 flex flex-col items-center">
            <div className="text-xs text-slate-500 uppercase tracking-widest mb-4">Niveau Menace Global</div>
            <div className="w-32 h-32"><GaugeRing value={avgComposite} color={CYBER} /></div>
            <div className="mt-3 text-3xl font-bold" style={{ color: CYBER }}>{avgComposite.toFixed(1)}</div>
          </div>
          <div className="rounded-xl bg-slate-900 border border-slate-800 p-6">
            <div className="text-xs text-slate-500 uppercase tracking-widest mb-4">Distribution Vecteurs</div>
            <div className="space-y-3">
              {Object.entries(riskDist).map(([level, count]) => (
                <div key={level} className="flex items-center gap-3">
                  <div className="text-xs font-medium w-16 capitalize" style={{ color: riskColor(level) }}>{level}</div>
                  <div className="flex-1 bg-slate-800 rounded-full h-2">
                    <div className="h-2 rounded-full" style={{ width: `${(count / totalEntities) * 100}%`, backgroundColor: riskColor(level) }} />
                  </div>
                  <div className="text-xs text-slate-400 w-4">{count}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {Object.keys(layers).length > 0 && (
          <div className="rounded-xl bg-slate-900 border border-slate-800 p-6">
            <div className="text-xs text-slate-500 uppercase tracking-widest mb-4">7 Couches de Protection Actives</div>
            <div className="space-y-2">
              {Object.entries(layers).map(([key, desc], i) => (
                <div key={key} className="flex items-start gap-3">
                  <div className="w-5 h-5 rounded flex items-center justify-center flex-shrink-0 text-xs font-bold" style={{ backgroundColor: CYBER + "20", color: CYBER }}>{i + 1}</div>
                  <div className="text-xs text-slate-300 pt-0.5">{desc}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {Object.keys(dataMap).length > 0 && (
          <div className="rounded-xl bg-slate-900 border border-slate-800 p-6">
            <div className="text-xs text-slate-500 uppercase tracking-widest mb-4">Carte des Données — Où Se Trouve Quoi</div>
            <div className="space-y-2">
              {Object.entries(dataMap).map(([key, path]) => (
                <div key={key} className="flex items-start gap-3">
                  <div className="text-xs text-slate-500 w-32 flex-shrink-0 capitalize">{key.replace(/_/g, " ")}</div>
                  <code className="text-xs text-blue-400 bg-slate-800 px-2 py-0.5 rounded break-all">{path}</code>
                </div>
              ))}
            </div>
          </div>
        )}

        {entities.length > 0 && (
          <div className="rounded-xl bg-slate-900 border border-slate-800 overflow-hidden">
            <div className="px-6 py-4 border-b border-slate-800">
              <div className="text-xs text-slate-500 uppercase tracking-widest">Vecteurs de Menace Analysés</div>
            </div>
            <div className="divide-y divide-slate-800">
              {entities.map((e) => {
                const score = e.composite_score as number;
                const level = e.risk_level as string;
                const name = e.name as string;
                return (
                  <div key={e.entity_id as string} className="px-6 py-3 flex items-center gap-4">
                    <div className="flex-1 text-sm text-slate-300 truncate">{name}</div>
                    <div className="text-xs font-medium capitalize px-2 py-0.5 rounded-full border" style={{ color: riskColor(level), borderColor: riskColor(level) + "40" }}>{level}</div>
                    <div className="text-sm font-mono font-bold w-12 text-right" style={{ color: riskColor(level) }}>{score.toFixed(1)}</div>
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
