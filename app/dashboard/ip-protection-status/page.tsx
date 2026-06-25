"use client";
import { useState } from "react";

const COLOR = "#1e293b";

const IP_ASSETS = [
  {
    category: "Marque & dénomination",
    items: [
      { name: "CaelumSwarm™", type: "Marque déposée", status: "PROTÉGÉ", level: "FORT", detail: "Dépôt OBPI + EUIPO recommandé — dénomination distinctive", action: "Déposer auprès de l'OBPI (Office Benelux) — ~350€" },
      { name: "Caelum Partners", type: "Dénomination sociale", status: "PROTÉGÉ", level: "FORT", detail: "Enregistrée à la BCE Belgique — protection territoriale BE", action: "Étendre via dépôt de marque EU" },
      { name: "Intelligence Concurrentielle CSDDD", type: "Concept métier", status: "À PROTÉGER", level: "MOYEN", detail: "Non déposé — protection par antériorité d'usage uniquement", action: "Documenter date de création + usage continu" },
    ],
  },
  {
    category: "Propriété intellectuelle logicielle",
    items: [
      { name: "Moteur de scoring composite (8 entités, 4 niveaux)", type: "Algorithme propriétaire", status: "PROTÉGÉ", level: "FORT", detail: "Protection automatique par droit d'auteur dès création — dépôt SABAM/i-DEPOT recommandé", action: "Déposer un i-DEPOT à la BOIP — preuve de date certaine — 35€" },
      { name: "Architecture CaelumSwarm™ multi-agents", type: "Architecture logicielle", status: "PROTÉGÉ", level: "FORT", detail: "Droit d'auteur EU automatique — ne pas divulguer les schémas techniques", action: "Garder le code source en dépôt privé" },
      { name: "340+ engines Python sectoriels", type: "Base de données / corpus", status: "PROTÉGÉ", level: "FORT", detail: "Protection sui generis base de données (Directive EU 96/9/CE)", action: "Mentionner © sur chaque export de données" },
      { name: "Indices de risque CSDDD par domaine", type: "Données & méthodologie", status: "PROTÉGÉ", level: "MOYEN", detail: "Protection par secret des affaires (Directive EU 2016/943)", action: "Accord NDA avant tout partage avec partenaires" },
    ],
  },
  {
    category: "Contenu & publications",
    items: [
      { name: "Dashboards & visualisations", type: "Œuvre graphique", status: "PROTÉGÉ", level: "FORT", detail: "Droit d'auteur automatique — ajouter © sur chaque export", action: "Watermark automatique sur les exports PDF/PNG" },
      { name: "Rapports d'analyse sectoriels", type: "Œuvre littéraire", status: "À PROTÉGER", level: "MOYEN", detail: "Protection par droit d'auteur — watermark recommandé", action: "Ajouter disclaimer IP sur chaque rapport partagé" },
      { name: "Méthodologie de conformité CSDDD", type: "Savoir-faire", status: "À PROTÉGER", level: "MOYEN", detail: "Protégeable comme secret des affaires si maintenu confidentiel", action: "NDA systématique + clause de confidentialité contrats" },
    ],
  },
];

const STATUS_COLOR: Record<string, string> = {
  "PROTÉGÉ": "#16a34a",
  "À PROTÉGER": "#d97706",
  "VULNÉRABLE": "#dc2626",
};
const LEVEL_COLOR: Record<string, string> = {
  FORT: "#16a34a", MOYEN: "#d97706", FAIBLE: "#dc2626",
};

const TEMPLATES = [
  {
    label: "Disclaimer partage externe",
    text: `© 2024-2026 Caelum Partners SPRL — CaelumSwarm™

Ce document contient des informations confidentielles et propriétaires.
Toute reproduction, diffusion ou utilisation sans autorisation écrite est strictement interdite.

Pour toute question : legal@caelumpartners.eu`,
  },
  {
    label: "Watermark export données",
    text: `CaelumSwarm™ © 2024-2026 Caelum Partners SPRL — CONFIDENTIEL
Généré le : ${new Date().toLocaleDateString("fr-FR")}
Usage strictement limité au destinataire désigné.
Redistribution interdite sans accord écrit préalable.`,
  },
  {
    label: "Clause NDA (résumé)",
    text: `Le destinataire s'engage à :
1. Garder confidentielles toutes les informations reçues de Caelum Partners SPRL
2. Ne pas reproduire, diffuser ou exploiter ces informations sans autorisation
3. Ne pas reverse-engineer la méthodologie CaelumSwarm™
4. Informer immédiatement Caelum Partners de toute violation constatée

Durée : 5 ans — Droit applicable : droit belge — Tribunal compétent : Bruxelles`,
  },
];

export default function IPProtectionStatusPage() {
  const [copied, setCopied] = useState<string | null>(null);
  const [expandedAsset, setExpandedAsset] = useState<string | null>(null);

  const copyText = (text: string, label: string) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(label);
      setTimeout(() => setCopied(null), 2000);
    });
  };

  const totalProtected = IP_ASSETS.flatMap(c => c.items).filter(i => i.status === "PROTÉGÉ").length;
  const totalToProtect = IP_ASSETS.flatMap(c => c.items).filter(i => i.status === "À PROTÉGER").length;
  const total = IP_ASSETS.flatMap(c => c.items).length;

  return (
    <div style={{ padding: 32, fontFamily: "sans-serif", maxWidth: 1000, margin: "0 auto" }}>
      <h1 style={{ fontSize: 26, fontWeight: "bold", color: COLOR, marginBottom: 4 }}>Protection Propriété Intellectuelle</h1>
      <p style={{ color: "#6b7280", marginBottom: 24 }}>Statut de protection des actifs CaelumSwarm™ — Caelum Partners SPRL</p>

      <div style={{ background: "#f0fdf4", border: "1px solid #86efac", borderRadius: 12, padding: 20, marginBottom: 24 }}>
        <div style={{ display: "flex", gap: 32, flexWrap: "wrap" }}>
          <div><div style={{ fontSize: 28, fontWeight: "bold", color: "#16a34a" }}>{totalProtected}/{total}</div><div style={{ fontSize: 12, color: "#166534" }}>Actifs protégés</div></div>
          <div><div style={{ fontSize: 28, fontWeight: "bold", color: "#d97706" }}>{totalToProtect}</div><div style={{ fontSize: 12, color: "#92400e" }}>Actions recommandées</div></div>
          <div style={{ flex: 1, minWidth: 200 }}>
            <div style={{ fontSize: 12, color: "#166534", marginBottom: 6 }}>Score de protection global</div>
            <div style={{ background: "#dcfce7", borderRadius: 4, height: 12 }}>
              <div style={{ width: `${Math.round((totalProtected / total) * 100)}%`, height: "100%", background: "#16a34a", borderRadius: 4 }} />
            </div>
            <div style={{ fontSize: 13, fontWeight: 700, color: "#16a34a", marginTop: 4 }}>{Math.round((totalProtected / total) * 100)}%</div>
          </div>
        </div>
      </div>

      {IP_ASSETS.map(cat => (
        <div key={cat.category} style={{ marginBottom: 24 }}>
          <h2 style={{ fontSize: 15, fontWeight: 700, color: "#374151", marginBottom: 12, paddingBottom: 6, borderBottom: "2px solid #e5e7eb" }}>{cat.category}</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {cat.items.map(asset => (
              <div key={asset.name} style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 10, overflow: "hidden" }}>
                <div onClick={() => setExpandedAsset(expandedAsset === asset.name ? null : asset.name)}
                  style={{ display: "flex", alignItems: "center", gap: 12, padding: "12px 16px", cursor: "pointer" }}>
                  <span style={{ fontSize: 11, fontWeight: 700, padding: "2px 10px", borderRadius: 9999, background: STATUS_COLOR[asset.status], color: "#fff", whiteSpace: "nowrap" }}>{asset.status}</span>
                  <span style={{ fontWeight: 600, fontSize: 14, color: "#1e293b", flex: 1 }}>{asset.name}</span>
                  <span style={{ fontSize: 11, color: "#6b7280", background: "#f3f4f6", padding: "2px 8px", borderRadius: 9999, whiteSpace: "nowrap" }}>{asset.type}</span>
                  <span style={{ fontSize: 11, fontWeight: 600, color: LEVEL_COLOR[asset.level], whiteSpace: "nowrap" }}>Protection {asset.level}</span>
                  <span style={{ color: "#9ca3af" }}>{expandedAsset === asset.name ? "▲" : "▼"}</span>
                </div>
                {expandedAsset === asset.name && (
                  <div style={{ padding: "0 16px 16px", borderTop: "1px solid #f1f5f9" }}>
                    <p style={{ fontSize: 13, color: "#374151", marginTop: 12 }}>{asset.detail}</p>
                    <div style={{ background: "#fffbeb", border: "1px solid #fde68a", borderRadius: 8, padding: "8px 14px", marginTop: 10, fontSize: 13, color: "#92400e" }}>
                      <strong>Action :</strong> {asset.action}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}

      <div style={{ marginTop: 32 }}>
        <h2 style={{ fontSize: 15, fontWeight: 700, color: "#374151", marginBottom: 12 }}>Templates prêts à l&apos;emploi</h2>
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {TEMPLATES.map(tpl => (
            <div key={tpl.label} style={{ background: "#f8fafc", border: "1px solid #e2e8f0", borderRadius: 10, padding: 16 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
                <span style={{ fontWeight: 600, fontSize: 13, color: "#374151" }}>{tpl.label}</span>
                <button onClick={() => copyText(tpl.text, tpl.label)}
                  style={{ padding: "4px 14px", borderRadius: 6, border: "1px solid #d1d5db", cursor: "pointer", fontSize: 12,
                    background: copied === tpl.label ? "#16a34a" : "#fff", color: copied === tpl.label ? "#fff" : "#374151" }}>
                  {copied === tpl.label ? "✓ Copié" : "Copier"}
                </button>
              </div>
              <pre style={{ fontSize: 12, color: "#475569", background: "#fff", padding: 12, borderRadius: 6, border: "1px solid #e5e7eb", whiteSpace: "pre-wrap", margin: 0 }}>{tpl.text}</pre>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
