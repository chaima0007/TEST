"use client";
import { useEffect, useState } from "react";

const COLOR = "#10b981";

interface Recommendation {
  id: string;
  priority: "CRITIQUE" | "HAUTE" | "MOYENNE";
  category: string;
  title: string;
  insight: string;
  action: string;
  impact: string;
  effort: "FAIBLE" | "MOYEN" | "ÉLEVÉ";
  timeframe: string;
  examples: string[];
}

const RECOMMENDATIONS: Recommendation[] = [
  {
    id: "R001", priority: "CRITIQUE", category: "Fréquence", title: "Augmenter la cadence LinkedIn à 5 posts/sem",
    insight: "Vos concurrents top-performers publient 7-10x/sem. Vous êtes à 4x/sem avec un taux d'engagement 2x supérieur au leurs — un potentiel inexploité massif.",
    action: "Planifier 1 post de plus par semaine avec du contenu réutilisé (infographie → carrousel → sondage)",
    impact: "+35% de portée organique estimée", effort: "FAIBLE", timeframe: "Cette semaine",
    examples: ["Transformer vos rapports d'engine en infographies LinkedIn", "Recycler les scores CSDDD en sondages interactifs"],
  },
  {
    id: "R002", priority: "CRITIQUE", category: "Format", title: "Lancer une série de sondages CSDDD",
    insight: "Les sondages génèrent 11,3% d'engagement moyen vs 6,8% pour vos posts actuels. Votre data propriétaire (340+ domaines) est une mine d'or pour ce format.",
    action: "1 sondage/semaine posant une question sur l'état de préparation CSDDD dans un secteur spécifique",
    impact: "+67% engagement sur les posts concernés", effort: "FAIBLE", timeframe: "Dès demain",
    examples: ["'Le secteur pub digitale est-il prêt pour CSDDD 2026 ?'", "'Votre entreprise audite-t-elle sa chaîne de valeur ?'"],
  },
  {
    id: "R003", priority: "HAUTE", category: "Thought leadership", title: "Point de vue signé — IA & droits humains",
    insight: "Les articles de fond signés par un expert génèrent 5,8% d'engagement et 27k portée en moyenne dans votre secteur. Position 'IA éthique' non occupée par vos concurrents.",
    action: "Article LinkedIn ou sous-stack mensuel signé Chaima Mhadbi sur l'IA au service de la conformité",
    impact: "Positionnement expert unique, leads entrants +20%", effort: "MOYEN", timeframe: "Dans 2 semaines",
    examples: ["'Pourquoi l'IA ne remplace pas l'audit humain, elle le renforce'", "'340 domaines analysés — ce que nos agents ont appris'"],
  },
  {
    id: "R004", priority: "HAUTE", category: "Visibilité", title: "Instagram : créer des Reels de démo produit",
    insight: "Les reels 'behind the scenes' tech génèrent 9,2% d'engagement sur Instagram dans votre niche. Votre audience n'a jamais vu vos dashboards en action.",
    action: "3 reels de 30-60s montrant les alertes automatiques, les scores en temps réel et les certifications",
    impact: "+85% portée sur Instagram vs posts statiques", effort: "MOYEN", timeframe: "Dans 1 semaine",
    examples: ["'Alerte critique déclenchée en temps réel'", "'Onglet certifications — ISO 26000 pour 8 entités en 1 clic'"],
  },
  {
    id: "R005", priority: "HAUTE", category: "Engagement", title: "Répondre systématiquement dans les 2h",
    insight: "Le temps de réponse aux commentaires corrèle directement avec le reach organique LinkedIn. Chaque réponse dans les 2h booste la portée de +15% en moyenne.",
    action: "Activer les notifications LinkedIn et bloquer 15 min matin/soir pour les réponses",
    impact: "+15% portée par post, fidélisation audience", effort: "FAIBLE", timeframe: "Immédiatement",
    examples: ["Répondre avec des données propriétaires ('dans notre analyse de 340 domaines...')"],
  },
  {
    id: "R006", priority: "MOYENNE", category: "SEO social", title: "Optimiser les hashtags — 5 maximum",
    insight: "Vos concurrents à fort engagement utilisent 3-5 hashtags précis vs 8-12 génériques. La spécificité prime sur la quantité.",
    action: "Bannir les hashtags trop larges (#business, #innovation) et utiliser 3-5 hashtags ultra-ciblés",
    impact: "+22% impressions dans les feeds ciblés", effort: "FAIBLE", timeframe: "Dès le prochain post",
    examples: ["#CSDDD2026", "#ChaineDeValeur", "#DueDiligence", "#ConformiteEU", "#AgentsIA"],
  },
];

const PRIO_COLOR: Record<string, string> = {
  CRITIQUE: "#dc2626", HAUTE: "#ea580c", MOYENNE: "#d97706",
};
const EFFORT_COLOR: Record<string, string> = {
  FAIBLE: "#16a34a", MOYEN: "#d97706", "ÉLEVÉ": "#dc2626",
};

export default function BrandImageOptimizerPage() {
  const [filter, setFilter] = useState("Tous");
  const [expanded, setExpanded] = useState<string | null>("R001");
  const [, setTick] = useState(0);

  useEffect(() => {
    const t = setInterval(() => setTick(n => n + 1), 30000);
    return () => clearInterval(t);
  }, []);

  const categories = ["Tous", ...Array.from(new Set(RECOMMENDATIONS.map(r => r.category)))];
  const filtered = RECOMMENDATIONS.filter(r => filter === "Tous" || r.category === filter);
  const criticalCount = RECOMMENDATIONS.filter(r => r.priority === "CRITIQUE").length;
  const quickWins = RECOMMENDATIONS.filter(r => r.effort === "FAIBLE").length;

  return (
    <div style={{ padding: 32, fontFamily: "sans-serif", maxWidth: 1000, margin: "0 auto" }}>
      <h1 style={{ fontSize: 26, fontWeight: "bold", color: COLOR, marginBottom: 4 }}>Optimiseur Image de Marque</h1>
      <p style={{ color: "#6b7280", marginBottom: 24 }}>Recommandations personnalisées pour Caelum Partners — basées sur l&apos;analyse concurrentielle</p>

      <div style={{ display: "flex", gap: 16, marginBottom: 24, flexWrap: "wrap" }}>
        {[
          { label: "Actions critiques", value: criticalCount, color: "#dc2626" },
          { label: "Quick wins (effort faible)", value: quickWins, color: "#16a34a" },
          { label: "Total recommandations", value: RECOMMENDATIONS.length, color: COLOR },
          { label: "Score image actuel", value: "78/100", color: "#6366f1" },
        ].map(c => (
          <div key={c.label} style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 10, padding: "12px 20px", textAlign: "center", boxShadow: "0 1px 3px rgba(0,0,0,0.06)" }}>
            <div style={{ fontSize: 26, fontWeight: "bold", color: c.color }}>{c.value}</div>
            <div style={{ fontSize: 12, color: "#6b7280" }}>{c.label}</div>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: 8, marginBottom: 20, flexWrap: "wrap" }}>
        {categories.map(cat => (
          <button key={cat} onClick={() => setFilter(cat)}
            style={{ padding: "5px 12px", borderRadius: 6, border: "1px solid #e5e7eb", cursor: "pointer", fontSize: 12,
              background: filter === cat ? COLOR : "#fff", color: filter === cat ? "#fff" : "#374151" }}>
            {cat}
          </button>
        ))}
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {filtered.map(rec => (
          <div key={rec.id} style={{ background: "#fff", border: `1px solid ${PRIO_COLOR[rec.priority]}30`, borderRadius: 10, overflow: "hidden" }}>
            <div onClick={() => setExpanded(expanded === rec.id ? null : rec.id)}
              style={{ display: "flex", alignItems: "center", gap: 12, padding: "14px 16px", cursor: "pointer" }}>
              <span style={{ fontSize: 11, fontWeight: 700, padding: "2px 10px", borderRadius: 9999, background: PRIO_COLOR[rec.priority], color: "#fff", whiteSpace: "nowrap" }}>{rec.priority}</span>
              <span style={{ fontSize: 11, color: "#6b7280", background: "#f3f4f6", padding: "2px 8px", borderRadius: 9999, whiteSpace: "nowrap" }}>{rec.category}</span>
              <span style={{ fontWeight: 600, fontSize: 14, color: "#1e293b", flex: 1 }}>{rec.title}</span>
              <span style={{ fontSize: 11, fontWeight: 600, color: EFFORT_COLOR[rec.effort], whiteSpace: "nowrap" }}>Effort {rec.effort}</span>
              <span style={{ fontSize: 11, color: "#9ca3af", whiteSpace: "nowrap" }}>{rec.timeframe}</span>
              <span style={{ color: "#9ca3af" }}>{expanded === rec.id ? "▲" : "▼"}</span>
            </div>
            {expanded === rec.id && (
              <div style={{ padding: "0 16px 16px", borderTop: `1px solid ${PRIO_COLOR[rec.priority]}20` }}>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginTop: 14 }}>
                  <div style={{ background: "#f8fafc", borderRadius: 8, padding: 12 }}>
                    <p style={{ fontWeight: 600, fontSize: 12, color: "#374151", marginBottom: 6 }}>Analyse</p>
                    <p style={{ fontSize: 13, color: "#374151", lineHeight: 1.5 }}>{rec.insight}</p>
                  </div>
                  <div style={{ background: "#f0fdf4", borderRadius: 8, padding: 12 }}>
                    <p style={{ fontWeight: 600, fontSize: 12, color: "#166534", marginBottom: 6 }}>Action concrète</p>
                    <p style={{ fontSize: 13, color: "#166534", lineHeight: 1.5 }}>{rec.action}</p>
                  </div>
                </div>
                <div style={{ marginTop: 12, display: "flex", gap: 12, flexWrap: "wrap" }}>
                  <div style={{ background: "#eff6ff", borderRadius: 8, padding: "8px 14px", flex: 1 }}>
                    <span style={{ fontSize: 11, color: "#1d4ed8", fontWeight: 600 }}>Impact estimé : </span>
                    <span style={{ fontSize: 12, color: "#1e40af" }}>{rec.impact}</span>
                  </div>
                </div>
                {rec.examples.length > 0 && (
                  <div style={{ marginTop: 12 }}>
                    <p style={{ fontWeight: 600, fontSize: 12, color: "#374151", marginBottom: 6 }}>Exemples concrets :</p>
                    <ul style={{ margin: 0, paddingLeft: 18 }}>
                      {rec.examples.map((ex, i) => <li key={i} style={{ fontSize: 13, color: "#374151", marginBottom: 3 }}>{ex}</li>)}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
