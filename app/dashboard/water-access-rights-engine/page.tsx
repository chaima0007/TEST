"use client";
import { useEffect, useState } from "react";

// ── Types ──────────────────────────────────────────────────────────────────────

interface WAREntity {
  id: string;
  name: string;
  country: string;
  composite_score: number;
  severity: string;
  estimated_water_access_rights_index: number;
  key_violation: string;
}

interface WARData {
  source: string;
  wave: number;
  accent: string;
  avg_composite_score: number;
  entity_count: number;
  entities: WAREntity[];
}

// ── Constants ──────────────────────────────────────────────────────────────────

const ACCENT = "#0ea5e9";

const SEVERITY_STYLES: Record<string, { bg: string; color: string; label: string }> = {
  critique: { bg: "#fef2f2", color: "#b91c1c", label: "Critique" },
  "élevé":  { bg: "#f0f9ff", color: "#0369a1", label: "Élevé" },
  "modéré": { bg: "#eff6ff", color: "#1d4ed8", label: "Modéré" },
  faible:   { bg: "#f0fdf4", color: "#15803d", label: "Faible" },
};

// ── GaugeRing ──────────────────────────────────────────────────────────────────

// r=36, cx=44, cy=44, viewBox="0 0 88 88"
// circumference = 2 * π * 36 ≈ 226.19
// strokeDashoffset = circumference * (1 - score/100)

function GaugeRing({ score, accent }: { score: number; accent: string }) {
  const r = 36;
  const cx = 44;
  const cy = 44;
  const circumference = 2 * Math.PI * r; // ≈ 226.19
  const pct = Math.min(Math.max(score / 10, 0), 1);
  const dash = pct * circumference;
  const gap = circumference - dash;

  return (
    <svg viewBox="0 0 88 88" width={88} height={88} style={{ display: "block" }}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#e5e7eb" strokeWidth={8} />
      <circle
        cx={cx}
        cy={cy}
        r={r}
        fill="none"
        stroke={accent}
        strokeWidth={8}
        strokeDasharray={`${dash} ${gap}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text
        x={cx}
        y={cy + 1}
        textAnchor="middle"
        dominantBaseline="middle"
        fontSize={14}
        fontWeight={700}
        fill="#111827"
      >
        {score.toFixed(1)}
      </text>
    </svg>
  );
}

// ── SeverityBadge ──────────────────────────────────────────────────────────────

function SeverityBadge({ severity }: { severity: string }) {
  const s = SEVERITY_STYLES[severity] ?? { bg: "#f3f4f6", color: "#374151", label: severity };
  return (
    <span
      style={{
        display: "inline-block",
        padding: "2px 10px",
        borderRadius: 9999,
        fontSize: 11,
        fontWeight: 600,
        backgroundColor: s.bg,
        color: s.color,
      }}
    >
      {s.label}
    </span>
  );
}

// ── EntityCard ─────────────────────────────────────────────────────────────────

function EntityCard({ entity }: { entity: WAREntity }) {
  const idx = entity.estimated_water_access_rights_index;
  return (
    <div
      style={{
        background: "#ffffff",
        border: "1px solid #e5e7eb",
        borderRadius: 12,
        padding: 20,
        display: "flex",
        flexDirection: "column",
        gap: 12,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        <GaugeRing score={idx} accent={ACCENT} />
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: "#111827", marginBottom: 4 }}>
            {entity.name}
          </div>
          <div style={{ fontSize: 11, color: "#6b7280", marginBottom: 6 }}>
            {entity.id} · {entity.country}
          </div>
          <SeverityBadge severity={entity.severity} />
        </div>
      </div>
      <div
        style={{
          fontSize: 12,
          color: "#374151",
          background: "#fafafa",
          borderRadius: 8,
          padding: "8px 12px",
          borderLeft: `3px solid ${ACCENT}`,
        }}
      >
        {entity.key_violation}
      </div>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, color: "#9ca3af" }}>
        <span>Score composite</span>
        <span style={{ fontWeight: 700, color: "#111827" }}>{entity.composite_score.toFixed(2)}</span>
      </div>
    </div>
  );
}

// ── SummaryBadges ──────────────────────────────────────────────────────────────

function SummaryBadges({ entities, avg }: { entities: WAREntity[]; avg: number }) {
  const counts: Record<string, number> = {};
  for (const e of entities) {
    counts[e.severity] = (counts[e.severity] ?? 0) + 1;
  }
  const items = [
    { key: "critique", label: "Critique" },
    { key: "élevé",   label: "Élevé" },
    { key: "modéré",  label: "Modéré" },
    { key: "faible",  label: "Faible" },
  ];
  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 10, alignItems: "center" }}>
      {items.map(({ key, label }) => {
        const s = SEVERITY_STYLES[key];
        const count = counts[key] ?? 0;
        return (
          <div
            key={key}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 6,
              padding: "6px 14px",
              borderRadius: 9999,
              background: s.bg,
              border: `1px solid ${s.color}30`,
            }}
          >
            <span style={{ fontSize: 18, fontWeight: 800, color: s.color }}>{count}</span>
            <span style={{ fontSize: 12, fontWeight: 500, color: s.color }}>{label}</span>
          </div>
        );
      })}
      <div
        style={{
          marginLeft: "auto",
          padding: "6px 16px",
          borderRadius: 9999,
          background: "#f3f4f6",
          fontSize: 13,
          fontWeight: 700,
          color: "#111827",
        }}
      >
        Moy. {avg.toFixed(2)}
      </div>
    </div>
  );
}

// ── Page ───────────────────────────────────────────────────────────────────────

export default function WaterAccessRightsPage() {
  const [data, setData] = useState<WARData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/water-access-rights-engine")
      .then((r) => r.json())
      .then((d) => { setData(d.payload ?? d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: 256 }}>
        <div
          style={{
            width: 36,
            height: 36,
            border: `3px solid ${ACCENT}`,
            borderTopColor: "transparent",
            borderRadius: "50%",
            animation: "spin 0.8s linear infinite",
          }}
        />
        <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
      </div>
    );
  }

  if (!data) {
    return (
      <div style={{ padding: 32, color: "#f87171", fontSize: 14 }}>
        Erreur de chargement des données.
      </div>
    );
  }

  return (
    <div style={{ padding: "2rem", background: "#0f172a", minHeight: "100vh", color: "#e2e8f0", fontFamily: "system-ui" }}>
      {/* Header */}
      <div
        style={{
          display: "flex",
          alignItems: "flex-start",
          justifyContent: "space-between",
          marginBottom: 24,
          flexWrap: "wrap",
          gap: 12,
        }}
      >
        <div>
          <h1 style={{ fontSize: "1.5rem", fontWeight: 700, color: ACCENT, marginBottom: "0.5rem", margin: 0, letterSpacing: "-0.02em" }}>
            Droits d&apos;Accès à l&apos;Eau
          </h1>
          <p style={{ color: "#64748b", marginBottom: "2rem", fontSize: "0.875rem", marginTop: 4 }}>
            CSDDD Art.8-13 — CaelumSwarm™ · Wave {data.wave} · {data.entity_count} entités analysées
          </p>
        </div>
        {data.source === "mock" && (
          <span
            style={{
              fontSize: 11,
              fontWeight: 600,
              padding: "4px 12px",
              borderRadius: 9999,
              background: "#f0f9ff",
              color: "#0369a1",
              border: "1px solid #bae6fd",
            }}
          >
            Données démo
          </span>
        )}
      </div>

      {/* Summary badges */}
      <div
        style={{
          background: "#1e293b",
          border: "1px solid #334155",
          borderRadius: 12,
          padding: "14px 20px",
          marginBottom: 24,
        }}
      >
        <SummaryBadges entities={data.entities} avg={data.avg_composite_score} />
      </div>

      {/* Accent bar */}
      <div
        style={{
          height: 4,
          borderRadius: 2,
          background: `linear-gradient(90deg, ${ACCENT}, #38bdf8)`,
          marginBottom: 24,
        }}
      />

      {/* Entity grid */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))",
          gap: 16,
        }}
      >
        {data.entities.map((entity) => (
          <EntityCard key={entity.id} entity={entity} />
        ))}
      </div>
    </div>
  );
}
