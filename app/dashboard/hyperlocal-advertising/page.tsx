"use client";
import { useEffect, useState } from "react";

const COLOR = "#ea580c";
const DOMAIN = "hyperlocal-advertising";
const INDEX_KEY = "estimated_hyperlocal_index";
const TITLE = "Mobile Advertising";

type Entity = {
  name: string;
  composite_score: number;
  risk_level: string;
  [key: string]: number | string;
};
type DashData = { entities: Entity[]; avg_composite: number; distribution: Record<string, number> };

function GaugeRing({ value, color }: { value: number; color: string }) {
  const r = 36, cx = 44, cy = 44, sw = 8;
  const circ = 2 * Math.PI * r;
  const offset = circ - (value / 100) * circ;
  return (
    <svg width={88} height={88} viewBox="0 0 88 88">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#e5e7eb" strokeWidth={sw} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={sw}
        strokeDasharray={circ} strokeDashoffset={offset}
        strokeLinecap="round" transform="rotate(-90 44 44)" />
      <text x={cx} y={cy} textAnchor="middle" dominantBaseline="central"
        fontSize={16} fontWeight="bold" fill={color}>{value}</text>
    </svg>
  );
}

function deriveCerts(score: number) {
  return [
    { id: "ISO-26000", label: "ISO 26000", status: score >= 75 ? "certified" : score >= 50 ? "in-progress" : "not-certified" },
    { id: "SA8000", label: "SA8000", status: score >= 80 ? "certified" : score >= 55 ? "in-progress" : "not-certified" },
    { id: "FAIR-TRADE", label: "Fair Trade", status: score >= 70 ? "certified" : score >= 45 ? "in-progress" : "not-certified" },
    { id: "CSDDD", label: "CSDDD 2024/1760", status: score >= 65 ? "certified" : score >= 40 ? "in-progress" : "not-certified" },
    { id: "ILO-C182", label: "OIT C182", status: score >= 60 ? "certified" : score >= 35 ? "in-progress" : "not-certified" },
  ];
}

const SIGNALS = [
  "Mobile consent management",
  "IDFA/GAID compliance",
  "In-app ad disclosure",
  "Mobile data privacy",
  "Push notification consent",
];

const ACTIONS = [
  "Enforce mobile consent",
  "Audit IDFA/GAID usage",
  "Improve in-app disclosure",
  "Protect mobile data",
  "Regulate push notifications",
];

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signals" | "certs" | "actions">("scores");
  const score = entity.composite_score;
  const certs = deriveCerts(score);
  const tabs: { id: "scores" | "signals" | "certs" | "actions"; label: string }[] = [
    { id: "scores", label: "Scores" },
    { id: "signals", label: "Signaux" },
    { id: "certs", label: "Certifications" },
    { id: "actions", label: "Actions" },
  ];
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 50 }}>
      <div style={{ background: "#fff", borderRadius: 12, padding: 24, width: 480, maxWidth: "90vw", maxHeight: "80vh", overflowY: "auto" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
          <h3 style={{ fontWeight: 700, fontSize: 16 }}>{entity.name}</h3>
          <button onClick={onClose} style={{ background: "none", border: "none", cursor: "pointer", fontSize: 20 }}>×</button>
        </div>
        <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
          {tabs.map(t => (
            <button key={t.id} onClick={() => setTab(t.id)}
              style={{ padding: "6px 12px", borderRadius: 6, border: "none", cursor: "pointer",
                background: tab === t.id ? COLOR : "#f3f4f6",
                color: tab === t.id ? "#fff" : "#374151", fontWeight: 600, fontSize: 13 }}>
              {t.label}
            </button>
          ))}
        </div>
        {tab === "scores" && (
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 12 }}>
              <GaugeRing value={Math.round(score)} color={COLOR} />
              <div>
                <div style={{ fontSize: 14, color: "#6b7280" }}>Score composite</div>
                <div style={{ fontWeight: 700, fontSize: 22, color: COLOR }}>{score}</div>
                <div style={{ fontSize: 12, padding: "2px 8px", borderRadius: 4, display: "inline-block", marginTop: 4,
                  background: entity.risk_level === "critique" ? "#fef2f2" : entity.risk_level === "élevé" ? "#fff7ed" : entity.risk_level === "modéré" ? "#fefce8" : "#f0fdf4",
                  color: entity.risk_level === "critique" ? "#dc2626" : entity.risk_level === "élevé" ? "#ea580c" : entity.risk_level === "modéré" ? "#ca8a04" : "#16a34a" }}>
                  {entity.risk_level}
                </div>
              </div>
            </div>
            <div style={{ fontSize: 13, color: "#6b7280" }}>Index {TITLE}: <b>{String(entity[INDEX_KEY])}</b></div>
          </div>
        )}
        {tab === "signals" && (
          <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
            {SIGNALS.map(s => (
              <li key={s} style={{ padding: "8px 0", borderBottom: "1px solid #f3f4f6", fontSize: 13, color: "#374151" }}>• {s}</li>
            ))}
          </ul>
        )}
        {tab === "certs" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {certs.map(c => (
              <div key={c.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "8px 12px", borderRadius: 8, background: "#f9fafb" }}>
                <span style={{ fontWeight: 600, fontSize: 13 }}>{c.label}</span>
                <span style={{ fontSize: 12, padding: "2px 8px", borderRadius: 4,
                  background: c.status === "certified" ? "#dcfce7" : c.status === "in-progress" ? "#fef9c3" : "#fee2e2",
                  color: c.status === "certified" ? "#16a34a" : c.status === "in-progress" ? "#ca8a04" : "#dc2626" }}>
                  {c.status}
                </span>
              </div>
            ))}
          </div>
        )}
        {tab === "actions" && (
          <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
            {ACTIONS.map(a => (
              <li key={a} style={{ padding: "8px 0", borderBottom: "1px solid #f3f4f6", fontSize: 13, color: "#374151" }}>→ {a}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default function HyperlocalAdvertisingDashboard() {
  const [data, setData] = useState<DashData | null>(null);
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch(`/api/${DOMAIN}`)
      .then(r => r.json())
      .then(d => setData(d.payload ?? d))
      .catch(() => setData({ entities: [], avg_composite: 61.03, distribution: {} }));
  }, []);

  if (!data) return <div style={{ padding: 40, textAlign: "center", color: "#6b7280" }}>Chargement...</div>;

  return (
    <div style={{ padding: 32, maxWidth: 1100, margin: "0 auto" }}>
      <h1 style={{ fontSize: 24, fontWeight: 800, color: "#111827", marginBottom: 4 }}>{TITLE}</h1>
      <p style={{ color: "#6b7280", marginBottom: 24, fontSize: 14 }}>Analyse conformité CSDDD 2024/1760 — Advertising Intelligence</p>
      <div style={{ display: "flex", gap: 16, marginBottom: 28, flexWrap: "wrap" }}>
        <div style={{ background: "#f9fafb", borderRadius: 10, padding: "16px 24px", flex: 1, minWidth: 140 }}>
          <div style={{ fontSize: 12, color: "#6b7280", marginBottom: 4 }}>Score moyen</div>
          <div style={{ fontSize: 28, fontWeight: 800, color: COLOR }}>{data.avg_composite}</div>
        </div>
        {Object.entries(data.distribution || {}).map(([k, v]) => (
          <div key={k} style={{ background: "#f9fafb", borderRadius: 10, padding: "16px 24px", flex: 1, minWidth: 100 }}>
            <div style={{ fontSize: 12, color: "#6b7280", marginBottom: 4 }}>{k}</div>
            <div style={{ fontSize: 24, fontWeight: 700, color: "#111827" }}>{String(v)}</div>
          </div>
        ))}
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill,minmax(220px,1fr))", gap: 16 }}>
        {(data.entities || []).map(e => (
          <div key={e.name} onClick={() => setSelected(e)}
            style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 10, padding: 16, cursor: "pointer", boxShadow: "0 1px 3px rgba(0,0,0,0.06)" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
              <span style={{ fontWeight: 600, fontSize: 13, color: "#111827", lineHeight: 1.3 }}>{e.name}</span>
              <span style={{ fontSize: 11, padding: "2px 7px", borderRadius: 4, whiteSpace: "nowrap", marginLeft: 6,
                background: e.risk_level === "critique" ? "#fef2f2" : e.risk_level === "élevé" ? "#fff7ed" : e.risk_level === "modéré" ? "#fefce8" : "#f0fdf4",
                color: e.risk_level === "critique" ? "#dc2626" : e.risk_level === "élevé" ? "#ea580c" : e.risk_level === "modéré" ? "#ca8a04" : "#16a34a" }}>
                {e.risk_level}
              </span>
            </div>
            <GaugeRing value={Math.round(e.composite_score)} color={COLOR} />
            <div style={{ marginTop: 8, fontSize: 12, color: "#6b7280" }}>
              Index: <b>{String(e[INDEX_KEY])}</b>
            </div>
          </div>
        ))}
      </div>
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
