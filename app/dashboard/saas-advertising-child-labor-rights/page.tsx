"use client";
import { useState, useEffect } from "react";

const COLOR = "#6366f1";

type Entity = { name: string; composite_score: number; risk_level: string; estimated_index: number };
type ApiData = { entities: Entity[]; avg_composite: number; generatedAt: string; mode?: string };

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

const CERT_COLOR: Record<string, string> = { certified: "#16a34a", "in-progress": "#d97706", "not-certified": "#dc2626" };
const CERT_LABEL: Record<string, string> = { certified: "Certifié", "in-progress": "En cours", "not-certified": "Non certifié" };
const RISK_COLOR: Record<string, string> = { critique: "#dc2626", élevé: "#f97316", modéré: "#d97706", faible: "#16a34a" };

export default function SaasAdvertisingChildLaborRightsPage() {
  const [data, setData] = useState<ApiData | null>(null);
  const [selected, setSelected] = useState<Entity | null>(null);
  const [tab, setTab] = useState<"apercu" | "indicateurs" | "recommandations" | "certifications">("apercu");

  useEffect(() => {
    fetch("/api/saas-advertising-child-labor-rights")
      .then(r => r.json())
      .then(d => setData(d.payload ?? d));
  }, []);

  if (!data) return <div style={{ padding: 32, fontFamily: "sans-serif" }}>Chargement...</div>;

  return (
    <div style={{ padding: 32, fontFamily: "sans-serif", maxWidth: 1100, margin: "0 auto" }}>
      <h1 style={{ fontSize: 26, fontWeight: "bold", color: COLOR, marginBottom: 4 }}>Publicité SaaS &amp; Logiciels</h1>
      <p style={{ color: "#6b7280", marginBottom: 24 }}>Analyse droits humains &amp; travail des enfants — CaelumSwarm™ CSDDD 2024/1760</p>

      <div style={{ display: "flex", gap: 16, marginBottom: 28, flexWrap: "wrap" }}>
        <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: "16px 24px", flex: 1, minWidth: 160 }}>
          <div style={{ fontSize: 13, color: "#6b7280", marginBottom: 4 }}>Score moyen</div>
          <div style={{ fontSize: 28, fontWeight: "bold", color: COLOR }}>{data.avg_composite}</div>
          <div style={{ fontSize: 12, color: "#9ca3af" }}>/ 100</div>
        </div>
        <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: "16px 24px", flex: 1, minWidth: 160 }}>
          <div style={{ fontSize: 13, color: "#6b7280", marginBottom: 4 }}>Entités analysées</div>
          <div style={{ fontSize: 28, fontWeight: "bold", color: "#1e293b" }}>{data.entities.length}</div>
          <div style={{ fontSize: 12, color: "#9ca3af" }}>entreprises</div>
        </div>
        <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: "16px 24px", flex: 1, minWidth: 160 }}>
          <div style={{ fontSize: 13, color: "#6b7280", marginBottom: 4 }}>Niveau critique</div>
          <div style={{ fontSize: 28, fontWeight: "bold", color: "#dc2626" }}>{data.entities.filter(e => e.risk_level === "critique").length}</div>
          <div style={{ fontSize: 12, color: "#9ca3af" }}>entités à risque</div>
        </div>
        {data.mode === "fallback" && (
          <div style={{ background: "#fffbeb", border: "1px solid #fde68a", borderRadius: 12, padding: "16px 24px", flex: 1, minWidth: 160 }}>
            <div style={{ fontSize: 12, color: "#92400e" }}>Mode dégradé — données statiques</div>
          </div>
        )}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 14, marginBottom: 32 }}>
        {data.entities.map(e => (
          <div key={e.name} onClick={() => { setSelected(e); setTab("apercu"); }}
            style={{ background: "#fff", border: `2px solid ${selected?.name === e.name ? COLOR : "#e5e7eb"}`, borderRadius: 12, padding: 16, cursor: "pointer", textAlign: "center" }}>
            <GaugeRing value={Math.round(e.composite_score)} color={RISK_COLOR[e.risk_level] ?? COLOR} />
            <div style={{ fontWeight: 600, fontSize: 13, color: "#1e293b", marginTop: 8 }}>{e.name}</div>
            <div style={{ fontSize: 11, padding: "2px 8px", borderRadius: 9999, background: RISK_COLOR[e.risk_level], color: "#fff", display: "inline-block", marginTop: 4 }}>{e.risk_level}</div>
          </div>
        ))}
      </div>

      {selected && (
        <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 16, padding: 24 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
            <h2 style={{ fontSize: 18, fontWeight: "bold", color: "#1e293b" }}>{selected.name}</h2>
            <button onClick={() => setSelected(null)} style={{ background: "none", border: "none", fontSize: 20, cursor: "pointer", color: "#9ca3af" }}>×</button>
          </div>
          <div style={{ display: "flex", gap: 8, marginBottom: 20 }}>
            {(["apercu", "indicateurs", "recommandations", "certifications"] as const).map(t => (
              <button key={t} onClick={() => setTab(t)}
                style={{ padding: "6px 14px", borderRadius: 8, border: "1px solid #e5e7eb", cursor: "pointer", fontSize: 12,
                  fontWeight: tab === t ? 700 : 400, background: tab === t ? COLOR : "#fff", color: tab === t ? "#fff" : "#374151" }}>
                {t.charAt(0).toUpperCase() + t.slice(1)}
              </button>
            ))}
          </div>
          {tab === "apercu" && (
            <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
              <GaugeRing value={Math.round(selected.composite_score)} color={RISK_COLOR[selected.risk_level] ?? COLOR} />
              <div>
                <div style={{ fontSize: 13, color: "#6b7280" }}>Score composite</div>
                <div style={{ fontSize: 24, fontWeight: "bold", color: RISK_COLOR[selected.risk_level] }}>{selected.composite_score}</div>
                <div style={{ fontSize: 13, color: "#6b7280", marginTop: 8 }}>Niveau de risque</div>
                <div style={{ fontSize: 15, fontWeight: 600, color: RISK_COLOR[selected.risk_level], textTransform: "capitalize" }}>{selected.risk_level}</div>
                <div style={{ fontSize: 13, color: "#6b7280", marginTop: 8 }}>Indice estimé</div>
                <div style={{ fontSize: 15, fontWeight: 600, color: "#1e293b" }}>{selected.estimated_index} / 10</div>
              </div>
            </div>
          )}
          {tab === "indicateurs" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              {[["Travail des enfants", selected.composite_score], ["Conditions de travail", Math.max(0, selected.composite_score - 5)], ["Droits humains", Math.max(0, selected.composite_score - 3)], ["Gouvernance", Math.max(0, selected.composite_score - 8)]].map(([label, val]) => (
                <div key={String(label)}>
                  <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, marginBottom: 4 }}>
                    <span>{String(label)}</span><span style={{ fontWeight: 600 }}>{Number(val).toFixed(1)}</span>
                  </div>
                  <div style={{ background: "#f1f5f9", borderRadius: 4, height: 8 }}>
                    <div style={{ width: `${Number(val)}%`, height: "100%", background: COLOR, borderRadius: 4 }} />
                  </div>
                </div>
              ))}
            </div>
          )}
          {tab === "recommandations" && (
            <ul style={{ fontSize: 13, color: "#374151", lineHeight: 1.8, paddingLeft: 20 }}>
              <li>Auditer les fournisseurs de rang 1 et 2 selon CSDDD 2024/1760</li>
              <li>Mettre en place un mécanisme de plainte accessible aux travailleurs</li>
              <li>Publier un rapport annuel de diligence raisonnable</li>
              <li>Former les équipes achats aux droits humains fondamentaux</li>
              <li>Intégrer des clauses contractuelles anti-travail des enfants</li>
            </ul>
          )}
          {tab === "certifications" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {deriveCerts(selected.composite_score).map(c => (
                <div key={c.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "8px 12px", background: "#f8fafc", borderRadius: 8 }}>
                  <span style={{ fontSize: 13, fontWeight: 600 }}>{c.label}</span>
                  <span style={{ fontSize: 11, padding: "2px 10px", borderRadius: 9999, background: CERT_COLOR[c.status], color: "#fff" }}>{CERT_LABEL[c.status]}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
