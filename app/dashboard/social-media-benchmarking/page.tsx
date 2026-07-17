"use client";
import { useEffect, useState } from "react";

const COLOR = "#6366f1";

interface BrandMetrics {
  brand: string;
  isOurs: boolean;
  platform: string;
  followers: number;
  engagementRate: number;
  postsPerWeek: number;
  avgLikes: number;
  avgComments: number;
  avgShares: number;
  topFormat: string;
  sentimentScore: number;
  growthRate: number;
}

const MOCK_DATA: BrandMetrics[] = [
  { brand: "Caelum Partners", isOurs: true, platform: "LinkedIn", followers: 4200, engagementRate: 6.8, postsPerWeek: 4, avgLikes: 187, avgComments: 34, avgShares: 52, topFormat: "Infographie", sentimentScore: 84, growthRate: 12.4 },
  { brand: "Concurrent A", isOurs: false, platform: "LinkedIn", followers: 9800, engagementRate: 3.2, postsPerWeek: 7, avgLikes: 213, avgComments: 18, avgShares: 28, topFormat: "Vidéo courte", sentimentScore: 71, growthRate: 5.1 },
  { brand: "Concurrent B", isOurs: false, platform: "LinkedIn", followers: 6500, engagementRate: 4.5, postsPerWeek: 3, avgLikes: 195, avgComments: 27, avgShares: 41, topFormat: "Article", sentimentScore: 78, growthRate: 8.3 },
  { brand: "Concurrent C", isOurs: false, platform: "LinkedIn", followers: 12300, engagementRate: 2.1, postsPerWeek: 10, avgLikes: 178, avgComments: 12, avgShares: 19, topFormat: "Sondage", sentimentScore: 63, growthRate: 3.7 },
  { brand: "Caelum Partners", isOurs: true, platform: "Instagram", followers: 1850, engagementRate: 5.2, postsPerWeek: 5, avgLikes: 64, avgComments: 9, avgShares: 14, topFormat: "Carrousel", sentimentScore: 88, growthRate: 18.6 },
  { brand: "Concurrent A", isOurs: false, platform: "Instagram", followers: 4200, engagementRate: 2.8, postsPerWeek: 8, avgLikes: 82, avgComments: 6, avgShares: 11, topFormat: "Reel", sentimentScore: 69, growthRate: 7.2 },
];

const PLATFORMS = ["Tous", "LinkedIn", "Instagram"];
const METRICS = [
  { key: "engagementRate", label: "Taux engagement (%)", format: (v: number) => v.toFixed(1) + "%" },
  { key: "followers", label: "Abonnés", format: (v: number) => v.toLocaleString("fr-FR") },
  { key: "growthRate", label: "Croissance mensuelle (%)", format: (v: number) => "+" + v.toFixed(1) + "%" },
  { key: "sentimentScore", label: "Score sentiment", format: (v: number) => v + "/100" },
];

function Bar({ value, max, color }: { value: number; max: number; color: string }) {
  return (
    <div style={{ background: "#f1f5f9", borderRadius: 4, height: 8, overflow: "hidden", flex: 1 }}>
      <div style={{ width: `${Math.min((value / max) * 100, 100)}%`, height: "100%", background: color, borderRadius: 4, transition: "width 0.4s" }} />
    </div>
  );
}

export default function SocialMediaBenchmarkingPage() {
  const [platform, setPlatform] = useState("LinkedIn");
  const [sortKey, setSortKey] = useState<keyof BrandMetrics>("engagementRate");
  const [, setTick] = useState(0);

  useEffect(() => {
    const t = setInterval(() => setTick(n => n + 1), 30000);
    return () => clearInterval(t);
  }, []);

  const filtered = MOCK_DATA
    .filter(d => platform === "Tous" || d.platform === platform)
    .sort((a, b) => (b[sortKey] as number) - (a[sortKey] as number));

  const ours = filtered.find(d => d.isOurs);
  const maxEng = Math.max(...filtered.map(d => d.engagementRate));
  const maxFol = Math.max(...filtered.map(d => d.followers));
  const maxGrowth = Math.max(...filtered.map(d => d.growthRate));
  const maxSent = Math.max(...filtered.map(d => d.sentimentScore));

  return (
    <div style={{ padding: 32, fontFamily: "sans-serif", maxWidth: 1000, margin: "0 auto" }}>
      <h1 style={{ fontSize: 26, fontWeight: "bold", color: COLOR, marginBottom: 4 }}>Benchmarking Image Réseaux Sociaux</h1>
      <p style={{ color: "#6b7280", marginBottom: 24 }}>Comparaison Caelum Partners vs concurrents — mis à jour toutes les 30 s</p>

      {ours && (
        <div style={{ background: "#eef2ff", border: "1px solid #c7d2fe", borderRadius: 12, padding: 20, marginBottom: 24, display: "flex", gap: 32, flexWrap: "wrap" }}>
          <div>
            <div style={{ fontSize: 11, color: "#6366f1", fontWeight: 600, textTransform: "uppercase", marginBottom: 4 }}>Notre taux d&apos;engagement</div>
            <div style={{ fontSize: 28, fontWeight: "bold", color: "#4338ca" }}>{ours.engagementRate.toFixed(1)}%</div>
            <div style={{ fontSize: 12, color: "#6b7280" }}>vs moy. concurrents : {(filtered.filter(d => !d.isOurs).reduce((s, d) => s + d.engagementRate, 0) / Math.max(1, filtered.filter(d => !d.isOurs).length)).toFixed(1)}%</div>
          </div>
          <div>
            <div style={{ fontSize: 11, color: "#6366f1", fontWeight: 600, textTransform: "uppercase", marginBottom: 4 }}>Croissance</div>
            <div style={{ fontSize: 28, fontWeight: "bold", color: "#16a34a" }}>+{ours.growthRate.toFixed(1)}%</div>
            <div style={{ fontSize: 12, color: "#6b7280" }}>par mois</div>
          </div>
          <div>
            <div style={{ fontSize: 11, color: "#6366f1", fontWeight: 600, textTransform: "uppercase", marginBottom: 4 }}>Format gagnant</div>
            <div style={{ fontSize: 22, fontWeight: "bold", color: "#4338ca" }}>{ours.topFormat}</div>
            <div style={{ fontSize: 12, color: "#6b7280" }}>format le plus performant</div>
          </div>
          <div>
            <div style={{ fontSize: 11, color: "#6366f1", fontWeight: 600, textTransform: "uppercase", marginBottom: 4 }}>Score sentiment</div>
            <div style={{ fontSize: 28, fontWeight: "bold", color: ours.sentimentScore >= 80 ? "#16a34a" : "#d97706" }}>{ours.sentimentScore}/100</div>
            <div style={{ fontSize: 12, color: "#6b7280" }}>perception audience</div>
          </div>
        </div>
      )}

      <div style={{ display: "flex", gap: 12, marginBottom: 20, flexWrap: "wrap" }}>
        {PLATFORMS.map(p => (
          <button key={p} onClick={() => setPlatform(p)}
            style={{ padding: "6px 16px", borderRadius: 6, border: "1px solid #e5e7eb", cursor: "pointer",
              background: platform === p ? COLOR : "#fff", color: platform === p ? "#fff" : "#374151", fontSize: 13 }}>
            {p}
          </button>
        ))}
        <select value={sortKey as string} onChange={e => setSortKey(e.target.value as keyof BrandMetrics)}
          style={{ marginLeft: "auto", padding: "6px 12px", borderRadius: 6, border: "1px solid #d1d5db", fontSize: 13 }}>
          {METRICS.map(m => <option key={m.key} value={m.key}>{m.label}</option>)}
        </select>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {filtered.map((d, i) => (
          <div key={`${d.brand}-${d.platform}`} style={{ background: d.isOurs ? "#eef2ff" : "#fff", border: `1px solid ${d.isOurs ? "#c7d2fe" : "#e5e7eb"}`, borderRadius: 10, padding: 16 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12 }}>
              <span style={{ fontSize: 12, fontWeight: 700, color: "#9ca3af", width: 20 }}>#{i + 1}</span>
              <span style={{ fontWeight: 700, fontSize: 15, color: d.isOurs ? COLOR : "#374151" }}>{d.brand}</span>
              {d.isOurs && <span style={{ fontSize: 10, fontWeight: 700, padding: "1px 8px", borderRadius: 9999, background: COLOR, color: "#fff" }}>NOUS</span>}
              <span style={{ fontSize: 11, color: "#6b7280", marginLeft: "auto" }}>{d.platform}</span>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))", gap: 12 }}>
              {[
                { label: "Engagement", value: d.engagementRate, max: maxEng, fmt: (v: number) => v.toFixed(1) + "%" },
                { label: "Abonnés", value: d.followers, max: maxFol, fmt: (v: number) => v.toLocaleString("fr-FR") },
                { label: "Croissance", value: d.growthRate, max: maxGrowth, fmt: (v: number) => "+" + v.toFixed(1) + "%" },
                { label: "Sentiment", value: d.sentimentScore, max: maxSent, fmt: (v: number) => v + "/100" },
              ].map(m => (
                <div key={m.label}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                    <span style={{ fontSize: 11, color: "#6b7280" }}>{m.label}</span>
                    <span style={{ fontSize: 12, fontWeight: 600, color: d.isOurs ? COLOR : "#374151" }}>{m.fmt(m.value)}</span>
                  </div>
                  <Bar value={m.value} max={m.max} color={d.isOurs ? COLOR : "#d1d5db"} />
                </div>
              ))}
            </div>
            <div style={{ marginTop: 10, fontSize: 12, color: "#6b7280" }}>
              Format phare : <strong style={{ color: d.isOurs ? COLOR : "#374151" }}>{d.topFormat}</strong> · {d.postsPerWeek} posts/sem · moy. {d.avgLikes} likes · {d.avgComments} commentaires
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
