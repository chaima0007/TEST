"use client";
import { useEffect, useState } from "react";

const ACCENT = "#78350f";

function GaugeRing({ score }: { score: number }) {
  const r = 36, cx = 44, cy = 44, sw = 8;
  const circ = 2 * Math.PI * r;
  const pct = Math.max(0, Math.min(100, score));
  const offset = circ * (1 - pct / 100);
  const color = score >= 60 ? "#dc2626" : score >= 40 ? "#f97316" : score >= 20 ? "#eab308" : "#22c55e";
  return (
    <svg viewBox="0 0 88 88" width={88} height={88}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#e5e7eb" strokeWidth={sw} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={sw}
        strokeDasharray={circ} strokeDashoffset={offset}
        strokeLinecap="round" transform={`rotate(-90 ${cx} ${cy})`} />
      <text x={cx} y={cy} textAnchor="middle" dominantBaseline="central"
        style={{ fontSize: 16, fontWeight: 700, fill: color }}>{score}</text>
    </svg>
  );
}

interface Entity {
  entity: string;
  composite_score: number;
  risk_level: string;
  estimated_asbestos_silicosis_index: number;
}

interface EngineData {
  avg_composite: number;
  distribution: { critique: number; "élevé": number; modéré: number; faible: number };
  entities: Entity[];
}

type ModalTab = "analyse" | "entites" | "methodologie";

function DetailModal({ data, onClose }: { data: EngineData; onClose: () => void }) {
  const [tab, setTab] = useState<ModalTab>("analyse");

  return (
    <div style={{
      position: "fixed", inset: 0, background: "rgba(0,0,0,0.75)",
      display: "flex", alignItems: "center", justifyContent: "center", zIndex: 50
    }}>
      <div style={{
        background: "#0f172a", borderRadius: 16, padding: 32,
        width: "90%", maxWidth: 700, maxHeight: "85vh", overflowY: "auto",
        border: "1px solid #1e293b"
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
          <h2 style={{ color: "#fff", fontSize: 20, fontWeight: 700 }}>Détails — Amiante et Silicose</h2>
          <button onClick={onClose} style={{ color: "#94a3b8", background: "none", border: "none", fontSize: 24, cursor: "pointer" }}>×</button>
        </div>

        <div style={{ display: "flex", gap: 8, marginBottom: 24 }}>
          {(["analyse", "entites", "methodologie"] as ModalTab[]).map((t) => (
            <button key={t} onClick={() => setTab(t)} style={{
              padding: "6px 16px", borderRadius: 8, border: "none", cursor: "pointer",
              background: tab === t ? ACCENT : "#1e293b",
              color: tab === t ? "#fff" : "#94a3b8", fontWeight: tab === t ? 700 : 400
            }}>
              {t === "analyse" ? "Analyse" : t === "entites" ? "Entités" : "Méthodologie"}
            </button>
          ))}
        </div>

        {tab === "analyse" && (
          <div style={{ color: "#cbd5e1", lineHeight: 1.7 }}>
            <p style={{ marginBottom: 12 }}>
              L&apos;exposition à l&apos;amiante et à la silice cristalline provoque des maladies professionnelles
              graves et irréversibles — asbestose, mésothéliome, silicose — dont les victimes sont
              principalement des travailleurs des mines, de la construction et de l&apos;industrie.
            </p>
            <p style={{ marginBottom: 12 }}>
              Score composite moyen : <strong style={{ color: "#fff" }}>{data.avg_composite.toFixed(2)}</strong> — niveau critique indiquant
              une exposition généralisée et des protections légales insuffisantes dans de nombreux pays.
            </p>
            <p>
              La distribution des risques révèle 4 entités en zone critique, confirmant l&apos;urgence
              d&apos;une réglementation renforcée sur les droits des travailleurs exposés.
            </p>
          </div>
        )}

        {tab === "entites" && (
          <div>
            {data.entities && data.entities.length > 0 ? (
              <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
                <thead>
                  <tr style={{ borderBottom: "1px solid #1e293b" }}>
                    <th style={{ color: "#64748b", textAlign: "left", padding: "8px 4px" }}>Entité</th>
                    <th style={{ color: "#64748b", textAlign: "right", padding: "8px 4px" }}>Score</th>
                    <th style={{ color: "#64748b", textAlign: "right", padding: "8px 4px" }}>Indice</th>
                    <th style={{ color: "#64748b", textAlign: "left", padding: "8px 4px" }}>Niveau</th>
                  </tr>
                </thead>
                <tbody>
                  {data.entities.map((e) => (
                    <tr key={e.entity} style={{ borderBottom: "1px solid #0f172a" }}>
                      <td style={{ color: "#e2e8f0", padding: "8px 4px" }}>{e.entity}</td>
                      <td style={{ color: "#f1f5f9", textAlign: "right", padding: "8px 4px" }}>{e.composite_score.toFixed(1)}</td>
                      <td style={{ color: "#f1f5f9", textAlign: "right", padding: "8px 4px" }}>{e.estimated_asbestos_silicosis_index.toFixed(2)}</td>
                      <td style={{ padding: "8px 4px" }}>
                        <span style={{
                          padding: "2px 8px", borderRadius: 6, fontSize: 11,
                          background: e.risk_level === "critique" ? "#450a0a" : e.risk_level === "élevé" ? "#431407" : e.risk_level === "modéré" ? "#422006" : "#052e16",
                          color: e.risk_level === "critique" ? "#fca5a5" : e.risk_level === "élevé" ? "#fdba74" : e.risk_level === "modéré" ? "#fde047" : "#86efac"
                        }}>
                          {e.risk_level}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p style={{ color: "#64748b" }}>Données entités non disponibles.</p>
            )}
          </div>
        )}

        {tab === "methodologie" && (
          <div style={{ color: "#cbd5e1", lineHeight: 1.7 }}>
            <p style={{ marginBottom: 12 }}>
              <strong style={{ color: "#fff" }}>Moteur :</strong> asbestos_silicosis_occupational_rights_engine
            </p>
            <p style={{ marginBottom: 12 }}>
              <strong style={{ color: "#fff" }}>Sous-scores :</strong> Exposition aux fibres (×0.30) ·
              Protection légale (×0.25) · Accès aux soins (×0.25) · Indemnisation (×0.20)
            </p>
            <p style={{ marginBottom: 12 }}>
              <strong style={{ color: "#fff" }}>Seuils :</strong> Critique ≥60 · Élevé ≥40 · Modéré ≥20 · Faible &lt;20
            </p>
            <p>
              <strong style={{ color: "#fff" }}>Distribution obligatoire :</strong> 4 critique / 2 élevé / 1 modéré / 1 faible sur 8 entités.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default function AsbestosSilicosisOccupationalRightsDashboard() {
  const [data, setData] = useState<EngineData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetch("/api/asbestos-silicosis-occupational-rights")
      .then((r) => r.json())
      .then((d) => {
        setData(d.payload ?? d);
        setLoading(false);
      })
      .catch(() => {
        setError("Erreur de chargement");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div style={{ minHeight: "100vh", background: "#020617", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ color: "#94a3b8", fontSize: 18 }}>Chargement...</div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div style={{ minHeight: "100vh", background: "#020617", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ color: "#f87171", fontSize: 18 }}>{error ?? "Données indisponibles"}</div>
      </div>
    );
  }

  const composite = data.avg_composite ?? 0;
  const dist = data.distribution ?? { critique: 0, "élevé": 0, modéré: 0, faible: 0 };

  return (
    <div style={{ minHeight: "100vh", background: "#020617", color: "#f1f5f9", padding: 24 }}>
      {showModal && <DetailModal data={data} onClose={() => setShowModal(false)} />}

      <div style={{ maxWidth: 1024, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ borderLeft: `4px solid ${ACCENT}`, paddingLeft: 24, marginBottom: 32 }}>
          <h1 style={{ fontSize: 28, fontWeight: 800, color: "#fff", margin: 0 }}>
            Droits — Amiante et Silicose
          </h1>
          <p style={{ color: "#94a3b8", marginTop: 8 }}>
            Droits Professionnels · Maladies Industrielles · Protection des Travailleurs · Indemnisation
          </p>
        </div>

        {/* KPI Cards */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 20, marginBottom: 32 }}>
          {/* Composite Score */}
          <div style={{ background: "#0f172a", borderRadius: 16, padding: 24, display: "flex", flexDirection: "column", alignItems: "center" }}>
            <GaugeRing score={Math.round(composite)} />
            <div style={{ fontSize: 32, fontWeight: 800, color: "#fff", marginTop: 12 }}>{composite.toFixed(2)}</div>
            <div style={{ color: "#94a3b8", fontSize: 13, marginTop: 4, textAlign: "center" }}>Score Composite Moyen</div>
          </div>

          {/* Critique count */}
          <div style={{ background: "#0f172a", borderRadius: 16, padding: 24, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
            <div style={{ fontSize: 52, fontWeight: 800, color: "#dc2626" }}>{dist.critique}</div>
            <div style={{ color: "#94a3b8", fontSize: 13, marginTop: 4 }}>Entités Critiques</div>
          </div>

          {/* Entities total */}
          <div style={{ background: "#0f172a", borderRadius: 16, padding: 24, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
            <div style={{ fontSize: 52, fontWeight: 800, color: "#f97316" }}>8</div>
            <div style={{ color: "#94a3b8", fontSize: 13, marginTop: 4 }}>Entités Analysées</div>
          </div>
        </div>

        {/* Risk Distribution */}
        <div style={{ background: "#0f172a", borderRadius: 16, padding: 24, marginBottom: 24 }}>
          <h2 style={{ color: "#fff", fontSize: 18, fontWeight: 700, marginBottom: 20 }}>Distribution des Risques</h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16 }}>
            <div style={{ background: "rgba(220,38,38,0.1)", border: "1px solid rgba(220,38,38,0.3)", borderRadius: 12, padding: 16, textAlign: "center" }}>
              <div style={{ fontSize: 36, fontWeight: 800, color: "#dc2626" }}>{dist.critique}</div>
              <div style={{ color: "#fca5a5", fontSize: 13, marginTop: 4 }}>Critique</div>
            </div>
            <div style={{ background: "rgba(249,115,22,0.1)", border: "1px solid rgba(249,115,22,0.3)", borderRadius: 12, padding: 16, textAlign: "center" }}>
              <div style={{ fontSize: 36, fontWeight: 800, color: "#f97316" }}>{dist["élevé"]}</div>
              <div style={{ color: "#fdba74", fontSize: 13, marginTop: 4 }}>Élevé</div>
            </div>
            <div style={{ background: "rgba(234,179,8,0.1)", border: "1px solid rgba(234,179,8,0.3)", borderRadius: 12, padding: 16, textAlign: "center" }}>
              <div style={{ fontSize: 36, fontWeight: 800, color: "#eab308" }}>{dist.modéré}</div>
              <div style={{ color: "#fde047", fontSize: 13, marginTop: 4 }}>Modéré</div>
            </div>
            <div style={{ background: "rgba(34,197,94,0.1)", border: "1px solid rgba(34,197,94,0.3)", borderRadius: 12, padding: 16, textAlign: "center" }}>
              <div style={{ fontSize: 36, fontWeight: 800, color: "#22c55e" }}>{dist.faible}</div>
              <div style={{ color: "#86efac", fontSize: 13, marginTop: 4 }}>Faible</div>
            </div>
          </div>
        </div>

        {/* Detail button */}
        <div style={{ textAlign: "center", marginBottom: 24 }}>
          <button
            onClick={() => setShowModal(true)}
            style={{
              background: ACCENT, color: "#fff", border: "none", borderRadius: 10,
              padding: "12px 32px", fontSize: 15, fontWeight: 700, cursor: "pointer"
            }}
          >
            Voir les détails complets
          </button>
        </div>

        {/* Footer */}
        <div style={{ color: "#475569", fontSize: 12, textAlign: "right" }}>
          Moteur : asbestos_silicosis_occupational_rights_engine · Wave 278 · Caelum Partners
        </div>
      </div>
    </div>
  );
}
