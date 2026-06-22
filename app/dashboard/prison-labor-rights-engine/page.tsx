"use client";

import { useEffect, useState } from "react";

// ── Types ──────────────────────────────────────────────────────────────────────

interface PLREntity {
  id: string;
  name: string;
  country: string;
  composite_score: number;
  severity: string;
  estimated_prison_labor_rights_index: number;
  key_violation: string;
}

interface PLRData {
  source: string;
  wave: number;
  accent: string;
  avg_composite_score: number;
  entity_count: number;
  entities: PLREntity[];
}

// ── Constants ──────────────────────────────────────────────────────────────────

const ACCENT = "#4c1d95";

const SEVERITY_STYLES: Record<string, { bg: string; color: string; label: string }> = {
  critique: { bg: "#fef2f2", color: "#b91c1c", label: "Critique" },
  "élevé":  { bg: "#f5f3ff", color: "#6d28d9", label: "Élevé" },
  "modéré": { bg: "#eff6ff", color: "#1d4ed8", label: "Modéré" },
  faible:   { bg: "#f0fdf4", color: "#15803d", label: "Faible" },
};

// ── GaugeRing ──────────────────────────────────────────────────────────────────

function GaugeRing({ score, accent }: { score: number; accent: string }) {
  const r = 36;
  const cx = 44;
  const cy = 44;
  const circumference = 2 * Math.PI * r;
  const pct = Math.min(Math.max(score / 10, 0), 1);
  const dash = pct * circumference;
  const gap = circumference - dash;

  return (
    <svg viewBox="0 0 88 88" width={88} height={88} style={{ display: "block" }}>
      <circle
        cx={cx}
        cy={cy}
        r={r}
        fill="none"
        stroke="#e5e7eb"
        strokeWidth={8}
      />
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

function EntityCard({ entity }: { entity: PLREntity }) {
  const idx = entity.estimated_prison_labor_rights_index;
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

function SummaryBadges({ entities, avg }: { entities: PLREntity[]; avg: number }) {
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

export default function PrisonLaborRightsPage() {
  const [data, setData] = useState<PLRData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/prison-labor-rights-engine")
      .then((r) => r.json())
      .then((d) => setData(d.payload ?? d))
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          height: 256,
        }}
      >
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
      <div style={{ padding: 32, color: "#6b7280", fontSize: 14 }}>
        Erreur de chargement des données.
      </div>
    );
  }

  return (
    <div style={{ padding: "24px 24px 48px", maxWidth: 1200, margin: "0 auto" }}>
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
          <h1
            style={{
              fontSize: 22,
              fontWeight: 700,
              color: "#111827",
              margin: 0,
              letterSpacing: "-0.02em",
            }}
          >
            Travail Pénitentiaire &amp; Droits
          </h1>
          <p style={{ fontSize: 13, color: "#6b7280", marginTop: 4, marginBottom: 0 }}>
            CaelumSwarm™ · Wave {data.wave} · {data.entity_count} entités analysées
          </p>
        </div>
        {data.source === "mock" && (
          <span
            style={{
              fontSize: 11,
              fontWeight: 600,
              padding: "4px 12px",
              borderRadius: 9999,
              background: "#f5f3ff",
              color: "#5b21b6",
              border: "1px solid #c4b5fd",
            }}
          >
            Données démo
          </span>
        )}
      </div>

      {/* Summary badges */}
      <div
        style={{
          background: "#ffffff",
          border: "1px solid #e5e7eb",
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
          background: `linear-gradient(90deg, ${ACCENT}, #7c3aed)`,
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
