"use client";
import { useEffect, useState } from "react";

const API_URL = "/api/media-advertising-child-labor-rights";
const TITLE = "Publicité Médias & Presse";
const COLOR = "#0369a1";

type Entity = { entity: string; composite_score: number; risk_level: string };
type ApiData = { entities: Entity[]; avg_composite: number; distribution: Record<string, number> };
type CertStatus = "certifié" | "en cours" | "non certifié";
interface Cert { code: string; label: string; issuer: string; status: CertStatus; year?: number }

const CERTS_TEMPLATE: Omit<Cert, "status" | "year">[] = [
  { code: "ISO-26000", label: "ISO 26000", issuer: "ISO" },
  { code: "SA8000", label: "SA8000", issuer: "Social Accountability International" },
  { code: "FAIR-TRADE", label: "Fair Trade Certified", issuer: "Fairtrade International" },
  { code: "CSDDD", label: "CSDDD 2024/1760", issuer: "Union Européenne" },
  { code: "ILO-C182", label: "Convention OIT C182", issuer: "OIT" },
];

const STATUS_COLOR: Record<CertStatus, string> = {
  "certifié": "#16a34a", "en cours": "#d97706", "non certifié": "#dc2626",
};
const STATUS_ICON: Record<CertStatus, string> = {
  "certifié": "✓", "en cours": "⏳", "non certifié": "✗",
};

function deriveCerts(score: number): Cert[] {
  return CERTS_TEMPLATE.map((t, i) => {
    const thresholds = [80, 65, 70, 75, 60];
    const s: CertStatus = score >= thresholds[i] + 15 ? "certifié" : score >= thresholds[i] ? "en cours" : "non certifié";
    return { ...t, status: s, year: s === "certifié" ? (score >= 90 ? 2023 : 2024) : undefined };
  });
}

function GaugeRing({ value, color }: { value: number; color: string }) {
  const r = 36, cx = 44, cy = 44, sw = 8;
  const circ = 2 * Math.PI * r;
  const pct = Math.min(Math.max(value, 0), 100);
  return (
    <svg width={88} height={88} viewBox="0 0 88 88">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#e5e7eb" strokeWidth={sw} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={sw}
        strokeDasharray={`${(pct / 100) * circ} ${circ}`}
        strokeLinecap="round" transform={`rotate(-90 ${cx} ${cy})`} />
      <text x={cx} y={cy + 5} textAnchor="middle" fontSize={14} fontWeight="bold" fill={color}>{Math.round(pct)}</text>
    </svg>
  );
}

function DetailModal({ entity, color, onClose }: { entity: Entity; color: string; onClose: () => void }) {
  const [tab, setTab] = useState<"apercu" | "indicateurs" | "recommandations" | "certifications">("apercu");
  const certs = deriveCerts(entity.composite_score);
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 50 }}>
      <div style={{ background: "#fff", borderRadius: 12, padding: 24, width: 520, maxWidth: "90vw", maxHeight: "80vh", overflowY: "auto" }}>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 16 }}>
          <h2 style={{ fontWeight: "bold", fontSize: 18 }}>{entity.entity}</h2>
          <button onClick={onClose} style={{ cursor: "pointer", fontSize: 20 }}>×</button>
        </div>
        <div style={{ display: "flex", gap: 6, marginBottom: 16, flexWrap: "wrap" }}>
          {(["apercu", "indicateurs", "recommandations", "certifications"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              style={{ padding: "4px 10px", borderRadius: 6, border: "1px solid #e5e7eb", fontSize: 12,
                background: tab === t ? color : "#f9fafb", color: tab === t ? "#fff" : "#374151", cursor: "pointer" }}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
        {tab === "apercu" && <div><p style={{ marginBottom: 8 }}>Score : <strong>{entity.composite_score}</strong></p><p>Risque : <strong style={{ color }}>{entity.risk_level}</strong></p></div>}
        {tab === "indicateurs" && <p>Conformité CSDDD 2024/1760 — encadrement de la publicité ciblant les mineurs dans les médias et la presse : interdiction du profilage publicitaire des enfants, obligation de vérification de l&apos;âge et respect des conventions ILO-C182 sur les pires formes de travail des enfants dans les chaînes d&apos;approvisionnement médiatiques.</p>}
        {tab === "recommandations" && <p>Mettre en place des politiques internes interdisant toute publicité ciblant les moins de 13 ans sans consentement parental explicite. Auditer les pratiques de sous-traitance publicitaire selon la CSDDD 2024/1760 et former les équipes éditoriales aux obligations de l&apos;ILO-C182 relatives aux droits des enfants dans les médias.</p>}
        {tab === "certifications" && (
          <div>
            <p style={{ fontSize: 12, color: "#6b7280", marginBottom: 12 }}>Attestations de conformité — {entity.entity}</p>
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {certs.map(cert => (
                <div key={cert.code} style={{ display: "flex", alignItems: "center", gap: 12, padding: "10px 14px", borderRadius: 8, border: `1px solid ${STATUS_COLOR[cert.status]}30`, background: STATUS_COLOR[cert.status] + "08" }}>
                  <span style={{ fontSize: 16, color: STATUS_COLOR[cert.status], fontWeight: "bold", width: 20, textAlign: "center" }}>{STATUS_ICON[cert.status]}</span>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 600, fontSize: 13 }}>{cert.label}</div>
                    <div style={{ fontSize: 11, color: "#6b7280" }}>{cert.issuer}</div>
                  </div>
                  <div style={{ textAlign: "right" }}>
                    <span style={{ fontSize: 11, fontWeight: 600, color: STATUS_COLOR[cert.status], padding: "2px 8px", borderRadius: 9999, background: STATUS_COLOR[cert.status] + "18" }}>{cert.status}</span>
                    {cert.year && <div style={{ fontSize: 10, color: "#9ca3af", marginTop: 2 }}>{cert.year}</div>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function Page() {
  const [data, setData] = useState<ApiData | null>(null);
  const [selected, setSelected] = useState<Entity | null>(null);
  useEffect(() => {
    fetch(API_URL).then(r => r.json()).then(d => setData(d.payload ?? d)).catch(console.error);
  }, []);
  if (!data) return <div style={{ padding: 32, textAlign: "center" }}>Chargement…</div>;
  const riskColors: Record<string, string> = { critique: "#dc2626", élevé: "#ea580c", modéré: "#d97706", faible: "#16a34a" };
  return (
    <div style={{ padding: 32, fontFamily: "sans-serif", maxWidth: 900, margin: "0 auto" }}>
      <h1 style={{ fontSize: 28, fontWeight: "bold", color: COLOR, marginBottom: 8 }}>{TITLE}</h1>
      <p style={{ color: "#6b7280", marginBottom: 24 }}>Score moyen composite : <strong>{data.avg_composite}</strong></p>
      <div style={{ display: "flex", gap: 16, marginBottom: 32, flexWrap: "wrap" }}>
        {Object.entries(data.distribution).map(([level, count]) => (
          <div key={level} style={{ background: "#f9fafb", border: "1px solid #e5e7eb", borderRadius: 8, padding: "12px 20px", minWidth: 120, textAlign: "center" }}>
            <div style={{ fontSize: 24, fontWeight: "bold", color: riskColors[level] ?? "#374151" }}>{count as number}</div>
            <div style={{ fontSize: 12, color: "#6b7280", textTransform: "capitalize" }}>{level}</div>
          </div>
        ))}
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 16 }}>
        {data.entities.map(e => (
          <div key={e.entity} onClick={() => setSelected(e)}
            style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 10, padding: 16, cursor: "pointer", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
              <span style={{ fontWeight: 600, fontSize: 13 }}>{e.entity}</span>
              <span style={{ fontSize: 11, padding: "2px 8px", borderRadius: 9999, background: (riskColors[e.risk_level] ?? "#374151") + "20", color: riskColors[e.risk_level] ?? "#374151" }}>{e.risk_level}</span>
            </div>
            <GaugeRing value={e.composite_score} color={riskColors[e.risk_level] ?? COLOR} />
          </div>
        ))}
      </div>
      {selected && <DetailModal entity={selected} color={COLOR} onClose={() => setSelected(null)} />}
    </div>
  );
}
