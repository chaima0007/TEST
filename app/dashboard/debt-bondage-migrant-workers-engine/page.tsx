"use client";
import { useEffect, useState } from "react";

const ACCENT = "#4c0519";
const CIRC = 226.19;

const FALLBACK = [
  { name: "Qatar kafala", score: 91.75, level: "critique" },
  { name: "UAE construction", score: 88.05, level: "critique" },
  { name: "Saudi domestic workers", score: 83.05, level: "critique" },
  { name: "Kuwait construction", score: 77.05, level: "critique" },
  { name: "Bahrain hospitality", score: 53.05, level: "élevé" },
  { name: "Oman agriculture", score: 51.05, level: "élevé" },
  { name: "Jordan garment industry", score: 27.05, level: "modéré" },
  { name: "ILO Fair Recruitment", score: 10.95, level: "faible" },
];

const LEVEL_COLORS: Record<string, string> = {
  critique: "#ef4444", élevé: "#f97316", modéré: "#eab308", faible: "#22c55e",
};

export default function DebtBondageMigrantWorkersPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/debt-bondage-migrant-workers-engine")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const entities = data?.entities ?? FALLBACK;
  const avg = data?.avg_composite ?? 60.25;

  if (loading) return <div style={{ padding: "2rem", color: "#94a3b8" }}>Chargement...</div>;

  return (
    <div style={{ padding: "2rem", background: "#0f172a", minHeight: "100vh", color: "#e2e8f0", fontFamily: "system-ui" }}>
      <h1 style={{ fontSize: "1.5rem", fontWeight: 700, color: ACCENT, marginBottom: "0.5rem" }}>
        Travail Migrant & Servitude Dettes
      </h1>
      <p style={{ color: "#64748b", marginBottom: "2rem", fontSize: "0.875rem" }}>
        CSDDD Art.8-13 — CaelumSwarm™ | DBM Engine
      </p>
      <div style={{ display: "flex", alignItems: "center", gap: "2rem", marginBottom: "2rem" }}>
        <svg viewBox="0 0 88 88" width={88} height={88}>
          <circle cx="44" cy="44" r="36" fill="none" stroke="#1e293b" strokeWidth="8" />
          <circle cx="44" cy="44" r="36" fill="none" stroke={ACCENT} strokeWidth="8"
            strokeDasharray={CIRC} strokeDashoffset={CIRC * (1 - avg / 100)}
            strokeLinecap="round" transform="rotate(-90 44 44)" />
          <text x="44" y="49" textAnchor="middle" fill="#e2e8f0" fontSize="14" fontWeight="bold">{avg.toFixed(1)}</text>
        </svg>
        <div>
          <div style={{ fontSize: "0.75rem", color: "#64748b" }}>Score moyen composite</div>
          <div style={{ fontSize: "1.25rem", fontWeight: 700, color: ACCENT }}>{avg.toFixed(2)}</div>
          <div style={{ fontSize: "0.75rem", color: "#64748b", marginTop: "0.25rem" }}>Distribution: 4c / 2é / 1m / 1f</div>
        </div>
      </div>
      <div style={{ display: "grid", gap: "0.75rem" }}>
        {entities.map((e: any) => (
          <div key={e.name} style={{ background: "#1e293b", borderRadius: "0.5rem", padding: "0.75rem 1rem", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <span style={{ fontSize: "0.875rem" }}>{e.name}</span>
            <div style={{ display: "flex", gap: "0.75rem", alignItems: "center" }}>
              <span style={{ fontSize: "0.75rem", color: LEVEL_COLORS[e.level] ?? "#94a3b8", textTransform: "uppercase", fontWeight: 600 }}>{e.level}</span>
              <span style={{ fontSize: "1rem", fontWeight: 700, color: LEVEL_COLORS[e.level] ?? "#e2e8f0" }}>{(e.composite_score ?? e.score).toFixed(2)}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
