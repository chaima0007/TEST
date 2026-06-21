"use client";

import { useEffect, useState } from "react";

const ACCENT = "#0a1a1a";

function riskColor(level: string) {
  if (level === "critique") return "#dc2626";
  if (level === "élevé") return "#ea580c";
  if (level === "modéré") return "#ca8a04";
  return "#16a34a";
}

function GaugeRing({ value, max = 10, color }: { value: number; max?: number; color: string }) {
  const r = 36;
  const cx = 44;
  const cy = 44;
  const circumference = 2 * Math.PI * r;
  const pct = Math.min(value / max, 1);
  const dash = pct * circumference;
  return (
    <svg viewBox="0 0 88 88" width={88} height={88}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#e5e7eb" strokeWidth={8} />
      <circle
        cx={cx}
        cy={cy}
        r={r}
        fill="none"
        stroke={color}
        strokeWidth={8}
        strokeDasharray={`${dash} ${circumference - dash}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy + 5} textAnchor="middle" fontSize={14} fontWeight={700} fill={color}>
        {value}
      </text>
    </svg>
  );
}

interface Entity {
  name: string;
  risk_level: string;
  composite_score: number;
  estimated_satellite_surveillance_privacy_rights_index: number;
}

interface Payload {
  agent: string;
  domain: string;
  total_entities: number;
  avg_composite: number;
  confidence_score: number;
  avg_estimated_satellite_surveillance_privacy_rights_index: number;
  risk_distribution: Record<string, number>;
  data_sources: string[];
  critical_alerts: string[];
  entities: Entity[];
}

export default function SatelliteSurveillancePrivacyRightsPage() {
  const [data, setData] = useState<Payload | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch("/api/satellite-surveillance-privacy-rights-engine")
      .then((r) => r.json())
      .then((d) => setData(d.payload ?? d))
      .catch(() => setError(true));
  }, []);

  if (error) return <div className="p-8 text-red-600">Erreur de chargement.</div>;
  if (!data) return <div className="p-8 text-gray-500">Chargement...</div>;

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-5xl mx-auto space-y-6">
        <div className="rounded-2xl p-6 text-white" style={{ backgroundColor: ACCENT }}>
          <h1 className="text-2xl font-bold">Surveillance Satellitaire &amp; Droits à la Vie Privée</h1>
          <p className="text-sm mt-1 opacity-80">NSO Group · Pegasus · EU AI Act · Privacy International</p>
          <div className="mt-4 flex gap-8 text-sm">
            <div>
              <div className="opacity-60">Entités</div>
              <div className="text-xl font-semibold">{data.total_entities}</div>
            </div>
            <div>
              <div className="opacity-60">Score moyen</div>
              <div className="text-xl font-semibold">{data.avg_composite}</div>
            </div>
            <div>
              <div className="opacity-60">Confiance</div>
              <div className="text-xl font-semibold">{(data.confidence_score * 100).toFixed(0)}%</div>
            </div>
            <div>
              <div className="opacity-60">Index Surveillance</div>
              <div className="text-xl font-semibold">{data.avg_estimated_satellite_surveillance_privacy_rights_index}</div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-4 gap-4">
          {Object.entries(data.risk_distribution).map(([level, count]) => (
            <div key={level} className="bg-white rounded-xl p-4 shadow-sm text-center">
              <div className="text-2xl font-bold" style={{ color: riskColor(level) }}>{count}</div>
              <div className="text-xs text-gray-500 capitalize mt-1">{level}</div>
            </div>
          ))}
        </div>

        {data.critical_alerts.length > 0 && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-4">
            <h2 className="font-semibold text-red-700 mb-2">Alertes critiques</h2>
            <ul className="space-y-1 text-sm text-red-600">
              {data.critical_alerts.map((a, i) => <li key={i}>{a}</li>)}
            </ul>
          </div>
        )}

        {data.entities.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.entities.map((e, i) => (
              <div key={i} className="bg-white rounded-xl p-4 shadow-sm flex items-center gap-4">
                <GaugeRing
                  value={e.estimated_satellite_surveillance_privacy_rights_index}
                  color={riskColor(e.risk_level)}
                />
                <div>
                  <div className="font-medium text-gray-900">{e.name}</div>
                  <div className="text-sm text-gray-500">Score : {e.composite_score}</div>
                  <div className="text-xs mt-1 font-semibold capitalize" style={{ color: riskColor(e.risk_level) }}>
                    {e.risk_level}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        <div className="bg-white rounded-xl p-4 shadow-sm">
          <h2 className="font-semibold text-gray-700 mb-2 text-sm">Sources de données</h2>
          <ul className="flex flex-wrap gap-2">
            {data.data_sources.map((s, i) => (
              <li key={i} className="text-xs bg-gray-100 rounded-full px-3 py-1 text-gray-600">{s}</li>
            ))}
          </ul>
        </div>
      </div>
    </main>
  );
}
