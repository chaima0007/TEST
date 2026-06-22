"use client";
import { useEffect, useState } from "react";

const ACCENT = "#0891b2";
const SLUG = "mental-health-workplace-rights-engine";

const FALLBACK_ENTITIES = [
  { id: "MHW-001", name: "Amazon Warehouses", composite_score: 86.40, risk_level: "critique" },
  { id: "MHW-002", name: "Foxconn", composite_score: 90.75, risk_level: "critique" },
  { id: "MHW-003", name: "Uber Drivers", composite_score: 79.70, risk_level: "critique" },
  { id: "MHW-004", name: "Call Center Industry", composite_score: 76.65, risk_level: "critique" },
  { id: "MHW-005", name: "Walmart", composite_score: 55.75, risk_level: "élevé" },
  { id: "MHW-006", name: "Fast Food", composite_score: 54.45, risk_level: "élevé" },
  { id: "MHW-007", name: "Google", composite_score: 32.90, risk_level: "modéré" },
  { id: "MHW-008", name: "Patagonia", composite_score: 12.90, risk_level: "faible" },
];

const RC: Record<string, string> = {
  critique: "#dc2626", élevé: "#f97316", modéré: "#eab308", faible: "#22c55e",
};
const RB: Record<string, string> = {
  critique: "#450a0a", élevé: "#431407", modéré: "#422006", faible: "#052e16",
};

function GaugeRing({ score, color }: { score: number; color: string }) {
  const r = 36, cx = 44, cy = 44, sw = 8;
  const circ = 2 * Math.PI * r;
  const dash = (score / 100) * circ;
  return (
    <svg viewBox="0 0 88 88" style={{ width: 80, height: 80 }}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={sw} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={sw}
        strokeDasharray={`${dash} ${circ - dash}`} strokeDashoffset={circ / 4}
        strokeLinecap="round" />
      <text x={cx} y={cy + 5} textAnchor="middle" fontSize="13" fontWeight="bold" fill={color}>
        {score.toFixed(0)}
      </text>
    </svg>
  );
}

type Entity = {
  id: string;
  name: string;
  composite_score: number;
  risk_level: string;
  [key: string]: unknown;
};

type ApiData = {
  entities: Entity[];
  avg_composite?: number;
  risk_distribution?: Record<string, number>;
  confidence_score?: number;
  critical_alerts?: string[];
};

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const rl = entity.risk_level;
  return (
    <div style={{
      position: "fixed", inset: 0, zIndex: 50, display: "flex",
      alignItems: "center", justifyContent: "center",
      background: "rgba(0,0,0,0.7)", padding: 16,
    }}>
      <div style={{
        background: "#0f172a", border: "1px solid #334155",
        borderRadius: 16, width: "100%", maxWidth: 560,
        maxHeight: "90vh", overflowY: "auto",
      }}>
        <div style={{
          display: "flex", alignItems: "flex-start", justifyContent: "space-between",
          padding: "24px 24px 16px", borderBottom: "1px solid #334155",
        }}>
          <div>
            <h2 style={{ color: "#fff", fontSize: 18, fontWeight: 700, margin: 0 }}>{entity.name}</h2>
            <span style={{
              display: "inline-block", marginTop: 6, padding: "2px 8px",
              borderRadius: 4, fontSize: 12, fontWeight: 600,
              background: RB[rl], color: RC[rl],
            }}>{rl}</span>
          </div>
          <button onClick={onClose} style={{
            background: "none", border: "none", color: "#94a3b8",
            fontSize: 28, cursor: "pointer", lineHeight: 1,
          }}>×</button>
        </div>
        <div style={{ padding: 24 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <GaugeRing score={entity.composite_score} color={RC[rl]} />
            <div>
              <p style={{ color: "#fff", fontWeight: 600, margin: 0 }}>
                Score: {entity.composite_score.toFixed(2)}
              </p>
              <p style={{ color: "#94a3b8", fontSize: 14, margin: "4px 0 0" }}>
                Niveau: {rl}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function MentalHealthWorkplaceRightsPage() {
  const [data, setData] = useState<ApiData | null>(null);
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch(`/api/${SLUG}`)
      .then(r => r.json())
      .then(d => {
        const payload = d.payload ?? d;
        if (!payload.entities || payload.entities.length === 0) {
          setData({ ...payload, entities: FALLBACK_ENTITIES });
        } else {
          setData(payload);
        }
      })
      .catch(() => setData({ entities: FALLBACK_ENTITIES }));
  }, []);

  if (!data) return (
    <div style={{
      minHeight: "100vh", background: "#020617",
      display: "flex", alignItems: "center", justifyContent: "center",
    }}>
      <div style={{ color: "#94a3b8" }}>Chargement...</div>
    </div>
  );

  const entities = data.entities ?? FALLBACK_ENTITIES;
  const avgScore = data.avg_composite
    ?? (entities.reduce((s, e) => s + e.composite_score, 0) / (entities.length || 1));
  const critCount = data.risk_distribution?.["critique"]
    ?? entities.filter(e => e.risk_level === "critique").length;
  const alertCount = data.critical_alerts?.length ?? critCount;
  const confidence = data.confidence_score ?? 0.85;

  return (
    <div style={{ minHeight: "100vh", background: "#020617", color: "#fff", padding: 24 }}>
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
      <div style={{ maxWidth: 1280, margin: "0 auto" }}>
        <div style={{ marginBottom: 32 }}>
          <h1 style={{ fontSize: 30, fontWeight: 700, color: "#fff", margin: 0 }}>
            Santé Mentale &amp; Droits Travail
          </h1>
          <p style={{ color: "#94a3b8", marginTop: 4, fontSize: 15 }}>
            Surveillance des violations de droits en santé mentale au travail
          </p>
        </div>
        <div style={{
          display: "grid", gridTemplateColumns: "repeat(4, 1fr)",
          gap: 16, marginBottom: 32,
        }}>
          {[
            { label: "Score Moyen", value: avgScore.toFixed(2), color: ACCENT },
            { label: "Confiance", value: `${(confidence * 100).toFixed(0)}%`, color: "#fff" },
            { label: "Critique", value: String(critCount), color: "#ef4444" },
            { label: "Alertes", value: String(alertCount), color: "#fb923c" },
          ].map(card => (
            <div key={card.label} style={{
              background: "#0f172a", border: "1px solid #334155",
              borderRadius: 12, padding: 16,
            }}>
              <p style={{ color: "#94a3b8", fontSize: 12, margin: "0 0 4px" }}>{card.label}</p>
              <p style={{ fontSize: 24, fontWeight: 700, color: card.color, margin: 0 }}>{card.value}</p>
            </div>
          ))}
        </div>
        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
          gap: 16,
        }}>
          {entities.map(e => {
            const rl = e.risk_level;
            return (
              <button key={e.id} onClick={() => setSelected(e)} style={{
                background: "#0f172a", border: "1px solid #334155",
                borderRadius: 12, padding: 16, textAlign: "left",
                cursor: "pointer", transition: "border-color 0.2s",
                width: "100%",
              }}>
                <div style={{ display: "flex", alignItems: "flex-start", gap: 12 }}>
                  <GaugeRing score={e.composite_score} color={RC[rl]} />
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <p style={{
                      color: "#fff", fontSize: 14, fontWeight: 500,
                      margin: 0, overflow: "hidden",
                      display: "-webkit-box", WebkitLineClamp: 2,
                      WebkitBoxOrient: "vertical",
                    }}>{e.name}</p>
                    <span style={{
                      display: "inline-block", marginTop: 6,
                      padding: "2px 8px", borderRadius: 4,
                      fontSize: 12, fontWeight: 600,
                      background: RB[rl], color: RC[rl],
                    }}>{rl}</span>
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
