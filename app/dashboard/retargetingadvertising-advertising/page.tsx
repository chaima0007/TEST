"use client";
import { useEffect, useState } from "react";

const COLOR = "#d97706";
const DOMAIN = "retargetingadvertising-advertising";
const INDEX_KEY = "estimated_retargetingadvertising_index";
const TITLE = "Retargeting Advertising";

const SIGNALS = [
  "Cookie consent compliance",
  "Cross-site tracking limits",
  "Frequency capping",
  "Lookalike audience controls",
  "User opt-out mechanisms",
];

const ACTIONS = [
  "Enforce cookie consent",
  "Cap cross-site tracking",
  "Implement frequency limits",
  "Audit lookalike audiences",
  "Strengthen opt-out flows",
];

type Entity = { name: string; composite_score: number; risk_level: string; [key: string]: number | string };
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

const RISK_COLORS: Record<string, string> = {
  critique: "#dc2626",
  élevé: "#ea580c",
  modéré: "#ca8a04",
  faible: "#16a34a",
};

function certBadge(status: string) {
  if (status === "certified") return { bg: "#dcfce7", color: "#15803d", label: "Certifié" };
  if (status === "in-progress") return { bg: "#fef9c3", color: "#a16207", label: "En cours" };
  return { bg: "#fee2e2", color: "#b91c1c", label: "Non certifié" };
}

export default function RetargetingadvertisingAdvertisingDashboard() {
  const [data, setData] = useState<DashData | null>(null);
  const [selected, setSelected] = useState<Entity | null>(null);
  const [tab, setTab] = useState<"scores" | "signaux" | "certs" | "actions">("scores");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/${DOMAIN}`)
      .then((r) => r.json())
      .then((d) => setData(d.payload ?? d))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100vh" }}>
      <p style={{ color: "#6b7280", fontSize: 16 }}>Chargement {TITLE}...</p>
    </div>
  );

  if (!data) return (
    <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100vh" }}>
      <p style={{ color: "#dc2626", fontSize: 16 }}>Erreur de chargement.</p>
    </div>
  );

  const avg = Math.round(data.avg_composite ?? 61);
  const dist = data.distribution ?? {};
  const entities = data.entities ?? [];

  return (
    <div style={{ minHeight: "100vh", background: "#f9fafb", padding: "32px 24px", fontFamily: "system-ui, sans-serif" }}>
      {/* Header */}
      <div style={{ marginBottom: 32 }}>
        <h1 style={{ fontSize: 28, fontWeight: 700, color: "#111827", margin: 0 }}>{TITLE}</h1>
        <p style={{ color: "#6b7280", marginTop: 4, fontSize: 14 }}>Domaine : {DOMAIN}</p>
      </div>

      {/* KPI Row */}
      <div style={{ display: "flex", gap: 20, marginBottom: 32, flexWrap: "wrap" }}>
        <div style={{ background: "#fff", borderRadius: 12, padding: 24, boxShadow: "0 1px 4px rgba(0,0,0,.08)", display: "flex", alignItems: "center", gap: 20, flex: "1 1 200px" }}>
          <GaugeRing value={avg} color={COLOR} />
          <div>
            <p style={{ fontSize: 13, color: "#6b7280", margin: 0 }}>Score moyen</p>
            <p style={{ fontSize: 26, fontWeight: 700, color: COLOR, margin: "4px 0 0" }}>{avg}/100</p>
          </div>
        </div>
        {Object.entries(dist).map(([level, count]) => (
          <div key={level} style={{ background: "#fff", borderRadius: 12, padding: 24, boxShadow: "0 1px 4px rgba(0,0,0,.08)", flex: "1 1 120px", textAlign: "center" }}>
            <p style={{ fontSize: 13, color: "#6b7280", margin: 0, textTransform: "capitalize" }}>{level}</p>
            <p style={{ fontSize: 28, fontWeight: 700, color: RISK_COLORS[level] ?? "#374151", margin: "4px 0 0" }}>{count}</p>
          </div>
        ))}
      </div>

      {/* Entity Table */}
      <div style={{ background: "#fff", borderRadius: 12, boxShadow: "0 1px 4px rgba(0,0,0,.08)", overflow: "hidden", marginBottom: 32 }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "#f3f4f6" }}>
              <th style={{ padding: "12px 16px", textAlign: "left", fontSize: 13, fontWeight: 600, color: "#374151" }}>Entité</th>
              <th style={{ padding: "12px 16px", textAlign: "center", fontSize: 13, fontWeight: 600, color: "#374151" }}>Score</th>
              <th style={{ padding: "12px 16px", textAlign: "center", fontSize: 13, fontWeight: 600, color: "#374151" }}>Niveau</th>
              <th style={{ padding: "12px 16px", textAlign: "center", fontSize: 13, fontWeight: 600, color: "#374151" }}>Index</th>
              <th style={{ padding: "12px 16px", textAlign: "center", fontSize: 13, fontWeight: 600, color: "#374151" }}>Détail</th>
            </tr>
          </thead>
          <tbody>
            {entities.map((e, i) => (
              <tr key={e.name} style={{ borderTop: "1px solid #f3f4f6", background: i % 2 === 0 ? "#fff" : "#fafafa" }}>
                <td style={{ padding: "12px 16px", fontSize: 14, color: "#111827", fontWeight: 500 }}>{e.name}</td>
                <td style={{ padding: "12px 16px", textAlign: "center", fontSize: 14, color: "#374151" }}>{Math.round(e.composite_score)}</td>
                <td style={{ padding: "12px 16px", textAlign: "center" }}>
                  <span style={{ background: RISK_COLORS[e.risk_level] ?? "#6b7280", color: "#fff", borderRadius: 999, padding: "2px 10px", fontSize: 12, fontWeight: 600, textTransform: "capitalize" }}>
                    {e.risk_level}
                  </span>
                </td>
                <td style={{ padding: "12px 16px", textAlign: "center", fontSize: 14, color: COLOR, fontWeight: 600 }}>
                  {typeof e[INDEX_KEY] === "number" ? (e[INDEX_KEY] as number).toFixed(2) : "—"}
                </td>
                <td style={{ padding: "12px 16px", textAlign: "center" }}>
                  <button
                    onClick={() => { setSelected(e); setTab("scores"); }}
                    style={{ background: COLOR, color: "#fff", border: "none", borderRadius: 6, padding: "4px 12px", fontSize: 12, cursor: "pointer" }}
                  >
                    Voir
                  </button>
                </td>
              </tr>
            ))}
            {entities.length === 0 && (
              <tr>
                <td colSpan={5} style={{ padding: "24px 16px", textAlign: "center", color: "#9ca3af", fontSize: 14 }}>
                  Aucune entité disponible (mode fallback)
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Detail Modal */}
      {selected && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,.45)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 50 }}
          onClick={() => setSelected(null)}>
          <div style={{ background: "#fff", borderRadius: 16, width: "min(600px, 95vw)", maxHeight: "85vh", overflow: "auto", padding: 28, boxShadow: "0 8px 40px rgba(0,0,0,.18)" }}
            onClick={(ev) => ev.stopPropagation()}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 20 }}>
              <div>
                <h2 style={{ fontSize: 20, fontWeight: 700, color: "#111827", margin: 0 }}>{selected.name}</h2>
                <p style={{ fontSize: 13, color: "#6b7280", margin: "4px 0 0" }}>{TITLE}</p>
              </div>
              <button onClick={() => setSelected(null)}
                style={{ background: "none", border: "none", fontSize: 22, cursor: "pointer", color: "#9ca3af", lineHeight: 1 }}>&#x2715;</button>
            </div>

            {/* Tabs */}
            <div style={{ display: "flex", gap: 4, marginBottom: 20, borderBottom: "2px solid #f3f4f6" }}>
              {(["scores", "signaux", "certs", "actions"] as const).map((t) => (
                <button key={t} onClick={() => setTab(t)}
                  style={{ padding: "8px 16px", fontSize: 13, fontWeight: 600, border: "none", background: "none", cursor: "pointer", borderBottom: tab === t ? `2px solid ${COLOR}` : "2px solid transparent", color: tab === t ? COLOR : "#6b7280", marginBottom: -2, textTransform: "capitalize" }}>
                  {t}
                </button>
              ))}
            </div>

            {tab === "scores" && (
              <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "center", padding: 16 }}>
                  <GaugeRing value={Math.round(selected.composite_score)} color={COLOR} />
                </div>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                  {Object.entries(selected).filter(([k]) => k.startsWith("sub") || k.includes("score") || k.includes("index")).map(([k, v]) => (
                    <div key={k} style={{ background: "#f9fafb", borderRadius: 8, padding: "10px 14px" }}>
                      <p style={{ fontSize: 11, color: "#9ca3af", margin: 0, textTransform: "uppercase", letterSpacing: ".05em" }}>{k.replace(/_/g, " ")}</p>
                      <p style={{ fontSize: 16, fontWeight: 700, color: "#111827", margin: "4px 0 0" }}>{typeof v === "number" ? v.toFixed(2) : String(v)}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {tab === "signaux" && (
              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                {SIGNALS.map((s, i) => (
                  <div key={i} style={{ display: "flex", alignItems: "center", gap: 12, background: "#f9fafb", borderRadius: 8, padding: "12px 16px" }}>
                    <div style={{ width: 8, height: 8, borderRadius: "50%", background: COLOR, flexShrink: 0 }} />
                    <p style={{ fontSize: 14, color: "#374151", margin: 0 }}>{s}</p>
                  </div>
                ))}
              </div>
            )}

            {tab === "certs" && (
              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                {deriveCerts(selected.composite_score).map((c) => {
                  const badge = certBadge(c.status);
                  return (
                    <div key={c.id} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", background: "#f9fafb", borderRadius: 8, padding: "12px 16px" }}>
                      <div>
                        <p style={{ fontSize: 14, fontWeight: 600, color: "#111827", margin: 0 }}>{c.label}</p>
                        <p style={{ fontSize: 12, color: "#9ca3af", margin: "2px 0 0" }}>{c.id}</p>
                      </div>
                      <span style={{ background: badge.bg, color: badge.color, borderRadius: 999, padding: "3px 12px", fontSize: 12, fontWeight: 600 }}>{badge.label}</span>
                    </div>
                  );
                })}
              </div>
            )}

            {tab === "actions" && (
              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                {ACTIONS.map((a, i) => (
                  <div key={i} style={{ display: "flex", alignItems: "center", gap: 12, background: "#f9fafb", borderRadius: 8, padding: "12px 16px" }}>
                    <span style={{ background: COLOR, color: "#fff", borderRadius: "50%", width: 24, height: 24, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 700, flexShrink: 0 }}>{i + 1}</span>
                    <p style={{ fontSize: 14, color: "#374151", margin: 0 }}>{a}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
