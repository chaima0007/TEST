"use client";
import { useEffect, useState } from "react";

const COLOR = "#f59e0b";

interface TrendingPost {
  id: string;
  platform: string;
  format: string;
  topic: string;
  engagement: number;
  reach: number;
  virality: number;
  publishedAt: string;
  source: string;
  tags: string[];
  relevance: "TRÈS ÉLEVÉE" | "ÉLEVÉE" | "MOYENNE";
  actionable: string;
}

const MOCK_TRENDS: TrendingPost[] = [
  { id: "T001", platform: "LinkedIn", format: "Infographie", topic: "CSDDD 2024 — guide pratique entreprises", engagement: 8.4, reach: 42000, virality: 94, publishedAt: "il y a 2h", source: "Secteur conformité", tags: ["CSDDD", "conformité", "due diligence"], relevance: "TRÈS ÉLEVÉE", actionable: "Créer notre propre guide CSDDD avec notre angle agents IA" },
  { id: "T002", platform: "LinkedIn", format: "Carrousel", topic: "5 erreurs audit chaîne d'approvisionnement", engagement: 7.1, reach: 31000, virality: 87, publishedAt: "il y a 5h", source: "Cabinet conseil ESG", tags: ["audit", "supply chain", "ESG"], relevance: "TRÈS ÉLEVÉE", actionable: "Adapter en '5 erreurs que nos agents détectent automatiquement'" },
  { id: "T003", platform: "Instagram", format: "Reel", topic: "Behind the scenes — analyse data conformité", engagement: 9.2, reach: 18000, virality: 91, publishedAt: "il y a 1h", source: "LegalTech startup", tags: ["legaltech", "data", "transparence"], relevance: "TRÈS ÉLEVÉE", actionable: "Créer un reel montrant les dashboards CaelumSwarm en action" },
  { id: "T004", platform: "LinkedIn", format: "Article long", topic: "L'IA au service de la vigilance des droits humains", engagement: 5.8, reach: 27000, virality: 73, publishedAt: "il y a 8h", source: "Think tank droits humains", tags: ["IA", "droits humains", "vigilance"], relevance: "TRÈS ÉLEVÉE", actionable: "Point de vue signé Chaima Mhadbi sur l'IA éthique" },
  { id: "T005", platform: "LinkedIn", format: "Sondage", topic: "Votre entreprise est-elle prête pour CSDDD 2026 ?", engagement: 11.3, reach: 55000, virality: 96, publishedAt: "il y a 30min", source: "Association conformité EU", tags: ["CSDDD", "2026", "préparation"], relevance: "TRÈS ÉLEVÉE", actionable: "Lancer notre propre sondage avec data de nos 340+ agents" },
  { id: "T006", platform: "Instagram", format: "Infographie", topic: "Droits du travail dans la publicité digitale", engagement: 6.4, reach: 12000, virality: 78, publishedAt: "il y a 3h", source: "ONG droits travail", tags: ["droits travail", "pub digitale", "éthique"], relevance: "ÉLEVÉE", actionable: "Infographie sur nos scores secteur publicité (waves 328-340)" },
  { id: "T007", platform: "LinkedIn", format: "Vidéo courte", topic: "ISO 26000 en 60 secondes", engagement: 8.9, reach: 38000, virality: 89, publishedAt: "il y a 4h", source: "Cabinet RSE", tags: ["ISO 26000", "RSE", "formation"], relevance: "ÉLEVÉE", actionable: "Série de vidéos courtes sur chaque certification que nous couvrons" },
  { id: "T008", platform: "LinkedIn", format: "Post texte", topic: "Témoignage client — réduction risques fournisseurs 40%", engagement: 6.7, reach: 22000, virality: 81, publishedAt: "il y a 6h", source: "Directeur achats", tags: ["témoignage", "ROI", "fournisseurs"], relevance: "ÉLEVÉE", actionable: "Collecter et partager nos propres success stories clients" },
];

const REL_COLOR: Record<string, string> = {
  "TRÈS ÉLEVÉE": "#dc2626", "ÉLEVÉE": "#ea580c", "MOYENNE": "#d97706",
};
const PLATFORM_COLOR: Record<string, string> = {
  LinkedIn: "#0077b5", Instagram: "#e1306c", Twitter: "#1da1f2",
};

export default function TrendingContentRadarPage() {
  const [filter, setFilter] = useState("Tous");
  const [selected, setSelected] = useState<TrendingPost | null>(null);
  const [, setTick] = useState(0);

  useEffect(() => {
    const t = setInterval(() => setTick(n => n + 1), 30000);
    return () => clearInterval(t);
  }, []);

  const platforms = ["Tous", ...Array.from(new Set(MOCK_TRENDS.map(t => t.platform)))];
  const filtered = MOCK_TRENDS.filter(t => filter === "Tous" || t.platform === filter);

  return (
    <div style={{ padding: 32, fontFamily: "sans-serif", maxWidth: 1000, margin: "0 auto" }}>
      <h1 style={{ fontSize: 26, fontWeight: "bold", color: COLOR, marginBottom: 4 }}>Radar Contenus Tendance</h1>
      <p style={{ color: "#6b7280", marginBottom: 24 }}>Ce qui fonctionne dans notre secteur — inspirations actionnables pour Caelum Partners</p>

      <div style={{ background: "#fffbeb", border: "1px solid #fde68a", borderRadius: 12, padding: 16, marginBottom: 24, display: "flex", gap: 12, alignItems: "flex-start" }}>
        <span style={{ fontSize: 20 }}>💡</span>
        <div>
          <strong style={{ color: "#92400e" }}>Opportunité détectée :</strong>
          <p style={{ margin: "4px 0 0", fontSize: 13, color: "#78350f" }}>
            Les sondages LinkedIn génèrent 11,3% d&apos;engagement en moyenne (+67% vs autres formats). Votre prochaine action : sondage sur la préparation CSDDD 2026 avec vos données propriétaires.
          </p>
        </div>
      </div>

      <div style={{ display: "flex", gap: 8, marginBottom: 20 }}>
        {platforms.map(p => (
          <button key={p} onClick={() => setFilter(p)}
            style={{ padding: "6px 14px", borderRadius: 6, border: "1px solid #e5e7eb", cursor: "pointer", fontSize: 13,
              background: filter === p ? COLOR : "#fff", color: filter === p ? "#fff" : "#374151" }}>
            {p}
          </button>
        ))}
        <span style={{ marginLeft: "auto", fontSize: 12, color: "#6b7280", alignSelf: "center" }}>{filtered.length} tendances · mis à jour il y a 2 min</span>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {filtered.map(trend => (
          <div key={trend.id} onClick={() => setSelected(selected?.id === trend.id ? null : trend)}
            style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 10, padding: 16, cursor: "pointer",
              boxShadow: selected?.id === trend.id ? `0 0 0 2px ${COLOR}` : "0 1px 3px rgba(0,0,0,0.06)" }}>
            <div style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
              <div style={{ flex: 1 }}>
                <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 6 }}>
                  <span style={{ fontSize: 11, fontWeight: 700, padding: "1px 8px", borderRadius: 9999, background: (PLATFORM_COLOR[trend.platform] ?? "#6b7280") + "18", color: PLATFORM_COLOR[trend.platform] ?? "#6b7280" }}>{trend.platform}</span>
                  <span style={{ fontSize: 11, color: "#6b7280", background: "#f3f4f6", padding: "1px 8px", borderRadius: 9999 }}>{trend.format}</span>
                  <span style={{ fontSize: 11, fontWeight: 600, padding: "1px 8px", borderRadius: 9999, background: REL_COLOR[trend.relevance] + "18", color: REL_COLOR[trend.relevance] }}>Pertinence {trend.relevance}</span>
                  <span style={{ fontSize: 11, color: "#9ca3af", marginLeft: "auto" }}>{trend.publishedAt}</span>
                </div>
                <p style={{ fontWeight: 600, fontSize: 14, color: "#1e293b", margin: "0 0 8px" }}>{trend.topic}</p>
                <div style={{ display: "flex", gap: 20, fontSize: 12, color: "#6b7280" }}>
                  <span>Engagement : <strong style={{ color: COLOR }}>{trend.engagement}%</strong></span>
                  <span>Portée : <strong>{trend.reach.toLocaleString("fr-FR")}</strong></span>
                  <span>Viralité : <strong style={{ color: trend.virality >= 90 ? "#dc2626" : "#ea580c" }}>{trend.virality}/100</strong></span>
                </div>
              </div>
              <span style={{ color: "#9ca3af", fontSize: 18 }}>{selected?.id === trend.id ? "▲" : "▼"}</span>
            </div>
            {selected?.id === trend.id && (
              <div style={{ marginTop: 14, paddingTop: 14, borderTop: "1px solid #f1f5f9" }}>
                <p style={{ fontSize: 12, fontWeight: 700, color: "#374151", marginBottom: 6 }}>Action recommandée pour Caelum Partners :</p>
                <div style={{ background: "#fffbeb", border: "1px solid #fde68a", borderRadius: 8, padding: "10px 14px", fontSize: 13, color: "#78350f" }}>
                  {trend.actionable}
                </div>
                <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginTop: 10 }}>
                  {trend.tags.map(tag => (
                    <span key={tag} style={{ fontSize: 11, padding: "2px 8px", borderRadius: 9999, background: "#f3f4f6", color: "#6b7280" }}>#{tag}</span>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
