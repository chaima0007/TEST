"use client";
import { useEffect, useState } from "react";

const COLOR = "#dc2626";
const DOMAIN = "livestreamadvertising-advertising";
const INDEX_KEY = "estimated_livestreamadvertising_index";
const TITLE = "Livestream Advertising";

const SIGNALS = [
  "Real-time viewer consent",
  "Stream data collection",
  "Interactive ad compliance",
  "Viewer profiling restrictions",
  "Live purchase data handling",
];

const ACTIONS = [
  "Deploy real-time consent",
  "Audit stream data flows",
  "Enforce interactive ad rules",
  "Limit viewer profiling",
  "Secure live purchase data",
];

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

function certColor(status: string) {
  if (status === "certified") return "#16a34a";
  if (status === "in-progress") return "#d97706";
  return "#dc2626";
}

function certLabel(status: string) {
  if (status === "certified") return "Certifié";
  if (status === "in-progress") return "En cours";
  return "Non certifié";
}

function riskColor(level: string) {
  if (level === "critique") return "#dc2626";
  if (level === "élevé") return "#ea580c";
  if (level === "modéré") return "#d97706";
  return "#16a34a";
}

type Tab = "scores" | "signaux" | "certs" | "actions";

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<Tab>("scores");
  const certs = deriveCerts(entity.composite_score);
  const tabs: { id: Tab; label: string }[] = [
    { id: "scores", label: "Scores" },
    { id: "signaux", label: "Signaux" },
    { id: "certs", label: "Certifications" },
    { id: "actions", label: "Actions" },
  ];
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 50 }}>
      <div style={{ background: "#fff", borderRadius: 12, width: 520, maxHeight: "80vh", overflow: "hidden", display: "flex", flexDirection: "column" }}>
        <div style={{ padding: "20px 24px 0", borderBottom: "1px solid #e5e7eb" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
            <div>
              <h2 style={{ margin: 0, fontSize: 18, fontWeight: 700, color: "#111827" }}>{entity.name}</h2>
              <span style={{ fontSize: 12, color: riskColor(entity.risk_level), fontWeight: 600, textTransform: "uppercase" }}>{entity.risk_level}</span>
            </div>
            <button onClick={onClose} style={{ background: "none", border: "none", fontSize: 20, cursor: "pointer", color: "#6b7280" }}>&#x2715;</button>
          </div>
          <div style={{ display: "flex", gap: 4 }}>
            {tabs.map(t => (
              <button key={t.id} onClick={() => setTab(t.id)} style={{
                padding: "8px 16px", border: "none", background: "none", cursor: "pointer",
                borderBottom: tab === t.id ? `2px solid ${COLOR}` : "2px solid transparent",
                color: tab === t.id ? COLOR : "#6b7280", fontWeight: tab === t.id ? 700 : 400, fontSize: 14,
              }}>{t.label}</button>
            ))}
          </div>
        </div>
        <div style={{ padding: 24, overflowY: "auto", flex: 1 }}>
          {tab === "scores" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
                <GaugeRing value={Math.round(entity.composite_score)} color={COLOR} />
                <div>
                  <div style={{ fontSize: 13, color: "#6b7280" }}>Score composite</div>
                  <div style={{ fontSize: 28, fontWeight: 800, color: COLOR }}>{entity.composite_score.toFixed(1)}</div>
                </div>
              </div>
              {INDEX_KEY in entity && (
                <div style={{ background: "#f9fafb", borderRadius: 8, padding: 12 }}>
                  <div style={{ fontSize: 12, color: "#6b7280" }}>Index estimé</div>
                  <div style={{ fontSize: 20, fontWeight: 700, color: "#111827" }}>{(entity[INDEX_KEY] as number).toFixed(2)}</div>
                </div>
              )}
            </div>
          )}
          {tab === "signaux" && (
            <ul style={{ listStyle: "none", margin: 0, padding: 0, display: "flex", flexDirection: "column", gap: 10 }}>
              {SIGNALS.map((s, i) => (
                <li key={i} style={{ display: "flex", alignItems: "center", gap: 10, padding: "10px 14px", background: "#f9fafb", borderRadius: 8 }}>
                  <span style={{ width: 8, height: 8, borderRadius: "50%", background: COLOR, flexShrink: 0, display: "inline-block" }} />
                  <span style={{ fontSize: 14, color: "#374151" }}>{s}</span>
                </li>
              ))}
            </ul>
          )}
          {tab === "certs" && (
            <ul style={{ listStyle: "none", margin: 0, padding: 0, display: "flex", flexDirection: "column", gap: 10 }}>
              {certs.map(c => (
                <li key={c.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 14px", background: "#f9fafb", borderRadius: 8 }}>
                  <span style={{ fontSize: 14, fontWeight: 600, color: "#374151" }}>{c.label}</span>
                  <span style={{ fontSize: 12, fontWeight: 700, color: certColor(c.status) }}>{certLabel(c.status)}</span>
                </li>
              ))}
            </ul>
          )}
          {tab === "actions" && (
            <ul style={{ listStyle: "none", margin: 0, padding: 0, display: "flex", flexDirection: "column", gap: 10 }}>
              {ACTIONS.map((a, i) => (
                <li key={i} style={{ display: "flex", alignItems: "flex-start", gap: 10, padding: "10px 14px", background: "#f9fafb", borderRadius: 8 }}>
                  <span style={{ fontSize: 13, fontWeight: 700, color: COLOR, flexShrink: 0 }}>{i + 1}.</span>
                  <span style={{ fontSize: 14, color: "#374151" }}>{a}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

export default function LivestreamadvertisingAdvertisingDashboard() {
  const [data, setData] = useState<DashData | null>(null);
  const [error, setError] = useState(false);
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch(`/api/${DOMAIN}`)
      .then(r => r.json())
      .then(d => setData(d.payload ?? d))
      .catch(() => setError(true));
  }, []);

  if (error) return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <p style={{ color: "#dc2626", fontWeight: 600 }}>Erreur de chargement des données.</p>
    </div>
  );

  if (!data) return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <p style={{ color: "#6b7280" }}>Chargement...</p>
    </div>
  );

  const distEntries = Object.entries(data.distribution);

  return (
    <div style={{ minHeight: "100vh", background: "#f9fafb", padding: "32px 24px", fontFamily: "system-ui, sans-serif" }}>
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        <div style={{ marginBottom: 32 }}>
          <h1 style={{ fontSize: 28, fontWeight: 800, color: "#111827", margin: 0 }}>{TITLE}</h1>
          <p style={{ color: "#6b7280", marginTop: 4, fontSize: 14 }}>Domaine : {DOMAIN} — Surveillance des risques publicitaires</p>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 16, marginBottom: 32 }}>
          <div style={{ background: "#fff", borderRadius: 12, padding: 20, boxShadow: "0 1px 3px rgba(0,0,0,0.08)", display: "flex", alignItems: "center", gap: 16 }}>
            <GaugeRing value={Math.round(data.avg_composite)} color={COLOR} />
            <div>
              <div style={{ fontSize: 12, color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.05em" }}>Score moyen</div>
              <div style={{ fontSize: 24, fontWeight: 800, color: COLOR }}>{data.avg_composite.toFixed(2)}</div>
            </div>
          </div>
          {distEntries.map(([level, count]) => (
            <div key={level} style={{ background: "#fff", borderRadius: 12, padding: 20, boxShadow: "0 1px 3px rgba(0,0,0,0.08)" }}>
              <div style={{ fontSize: 12, color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.05em" }}>{level}</div>
              <div style={{ fontSize: 28, fontWeight: 800, color: riskColor(level) }}>{count}</div>
              <div style={{ fontSize: 12, color: "#9ca3af" }}>entités</div>
            </div>
          ))}
        </div>

        <div style={{ background: "#fff", borderRadius: 12, boxShadow: "0 1px 3px rgba(0,0,0,0.08)", overflow: "hidden" }}>
          <div style={{ padding: "20px 24px", borderBottom: "1px solid #f3f4f6" }}>
            <h2 style={{ margin: 0, fontSize: 18, fontWeight: 700, color: "#111827" }}>Entités surveillées</h2>
          </div>
          <div style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ background: "#f9fafb" }}>
                  <th style={{ padding: "12px 24px", textAlign: "left", fontSize: 12, fontWeight: 600, color: "#6b7280", textTransform: "uppercase" }}>Entité</th>
                  <th style={{ padding: "12px 16px", textAlign: "left", fontSize: 12, fontWeight: 600, color: "#6b7280", textTransform: "uppercase" }}>Risque</th>
                  <th style={{ padding: "12px 16px", textAlign: "right", fontSize: 12, fontWeight: 600, color: "#6b7280", textTransform: "uppercase" }}>Score</th>
                  <th style={{ padding: "12px 16px", textAlign: "right", fontSize: 12, fontWeight: 600, color: "#6b7280", textTransform: "uppercase" }}>Index</th>
                  <th style={{ padding: "12px 24px", textAlign: "center", fontSize: 12, fontWeight: 600, color: "#6b7280", textTransform: "uppercase" }}>Détail</th>
                </tr>
              </thead>
              <tbody>
                {data.entities.map((e, i) => (
                  <tr key={i} style={{ borderTop: "1px solid #f3f4f6" }}>
                    <td style={{ padding: "14px 24px", fontWeight: 600, color: "#111827" }}>{e.name}</td>
                    <td style={{ padding: "14px 16px" }}>
                      <span style={{ fontSize: 12, fontWeight: 700, color: riskColor(e.risk_level), textTransform: "uppercase" }}>{e.risk_level}</span>
                    </td>
                    <td style={{ padding: "14px 16px", textAlign: "right" }}>
                      <span style={{ fontWeight: 700, color: riskColor(e.risk_level) }}>{e.composite_score.toFixed(1)}</span>
                    </td>
                    <td style={{ padding: "14px 16px", textAlign: "right", color: "#374151" }}>
                      {INDEX_KEY in e ? (e[INDEX_KEY] as number).toFixed(2) : "—"}
                    </td>
                    <td style={{ padding: "14px 24px", textAlign: "center" }}>
                      <button onClick={() => setSelected(e)} style={{
                        padding: "6px 14px", borderRadius: 6, border: `1px solid ${COLOR}`,
                        background: "none", color: COLOR, cursor: "pointer", fontSize: 13, fontWeight: 600,
                      }}>Voir</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div style={{ marginTop: 32, background: "#fff", borderRadius: 12, padding: 24, boxShadow: "0 1px 3px rgba(0,0,0,0.08)" }}>
          <h2 style={{ margin: "0 0 16px", fontSize: 16, fontWeight: 700, color: "#111827" }}>Signaux de risque</h2>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
            {SIGNALS.map((s, i) => (
              <div key={i} style={{ padding: "8px 14px", background: "#fef2f2", borderRadius: 20, fontSize: 13, color: COLOR, fontWeight: 600, border: `1px solid ${COLOR}22` }}>
                {s}
              </div>
            ))}
          </div>
        </div>

        <div style={{ marginTop: 16, background: "#fff", borderRadius: 12, padding: 24, boxShadow: "0 1px 3px rgba(0,0,0,0.08)" }}>
          <h2 style={{ margin: "0 0 16px", fontSize: 16, fontWeight: 700, color: "#111827" }}>Actions recommandées</h2>
          <ol style={{ margin: 0, padding: "0 0 0 20px", display: "flex", flexDirection: "column", gap: 8 }}>
            {ACTIONS.map((a, i) => (
              <li key={i} style={{ fontSize: 14, color: "#374151" }}>{a}</li>
            ))}
          </ol>
        </div>

        <p style={{ textAlign: "center", color: "#9ca3af", fontSize: 12, marginTop: 24 }}>
          Dernière mise à jour : {new Date().toLocaleString("fr-FR")} — revalidate 30s
        </p>
      </div>
    </div>
  );
}
