"use client";

import { competitors } from "@/lib/data";
import Link from "next/link";
import { useState, useMemo, useEffect, useCallback } from "react";

const featureNames = [
  "Intelligence Artificielle",
  "Automatisation des ventes",
  "Intégration email",
  "Rapports avancés",
  "Application mobile",
  "API ouverte",
];

const qualityScore: Record<string, number> = {
  Excellent: 3,
  Bien: 2,
  Moyen: 1,
  "-": 0,
};

// Weighted score quality mapping: Excellent=100, Bien=75, Moyen=50, "-"=0
const qualityWeightedScore: Record<string, number> = {
  Excellent: 100,
  Bien: 75,
  Moyen: 50,
  "-": 0,
};

function getFeatureForCompetitor(c: (typeof competitors)[0], featureName: string) {
  return c.features.find(
    (f) =>
      f.name.toLowerCase().includes(featureName.toLowerCase().split(" ")[0].toLowerCase()) ||
      featureName.toLowerCase().includes(f.name.toLowerCase().split(" ")[0].toLowerCase()) ||
      f.name === featureName
  );
}

function QualityBadge({ quality, available }: { quality: string; available: boolean }) {
  if (!available)
    return (
      <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-slate-100">
        <span className="text-slate-300 text-sm font-bold">✗</span>
      </span>
    );

  if (quality === "Excellent")
    return (
      <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-700 border border-emerald-200">
        <span className="text-emerald-500">✓</span> Excellent
      </span>
    );
  if (quality === "Bien")
    return (
      <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full bg-blue-100 text-blue-700 border border-blue-200">
        <span className="text-blue-400">✓</span> Bien
      </span>
    );
  if (quality === "Moyen")
    return (
      <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full bg-amber-100 text-amber-700 border border-amber-200">
        <span className="text-amber-400">✓</span> Moyen
      </span>
    );

  return <span className="text-slate-300 text-base">—</span>;
}

function getCompetitorScore(c: (typeof competitors)[0]): number {
  const total = c.features.reduce((acc, f) => acc + (f.available ? (qualityScore[f.quality] ?? 0) : 0), 0);
  const max = c.features.length * 3;
  return Math.round((total / max) * 100);
}

function generateAIInsight(selected: (typeof competitors)[0][]): string {
  if (selected.length === 0) return "";

  const scored = selected.map((c) => ({ c, score: getCompetitorScore(c) })).sort((a, b) => b.score - a.score);
  const best = scored[0];
  const weakest = scored[scored.length - 1];

  const bestFeature = best.c.features.find((f) => f.available && f.quality === "Excellent");
  const gap = best.score - weakest.score;

  if (selected.length === 1) {
    return `${best.c.name} affiche un score global de ${best.score}%. ${
      bestFeature ? `Son point fort : ${bestFeature.name.split("(")[0].trim()}, noté Excellent.` : ""
    } Surveillez leurs prochaines mises à jour produit pour anticiper leurs mouvements.`;
  }

  return `${best.c.name} domine cette comparaison avec ${best.score}% — un écart de ${gap} points sur ${weakest.c.name}. ${
    bestFeature ? `L'avantage clé : une maîtrise Excellent sur ${bestFeature.name.split("(")[0].trim()}.` : ""
  } Pour contrer ${best.c.name}, misez sur les angles où ils restent à Moyen${
    best.c.features.some((f) => f.quality === "Moyen") ? ` (${best.c.features.find((f) => f.quality === "Moyen")?.name.split("(")[0].trim()})` : ""
  } ou sur une valeur prix plus compétitive.`;
}

// Weighted score criteria
const CRITERIA = [
  { key: "prix", label: "Prix", defaultWeight: 40 },
  { key: "ia", label: "Fonctionnalités IA", defaultWeight: 25 },
  { key: "ux", label: "Facilité d'utilisation", defaultWeight: 20 },
  { key: "support", label: "Support", defaultWeight: 15 },
] as const;

type CriteriaKey = (typeof CRITERIA)[number]["key"];

// Map competitor features to criteria scores
function getCriteriaQualityScore(c: (typeof competitors)[0], key: CriteriaKey): number {
  switch (key) {
    case "prix": {
      // Inverse price score: lower price = higher score
      const lowestPrice = Math.min(...c.pricing.filter((p) => p.price > 0).map((p) => p.price));
      // Map price range 0-500 inversely to 0-100
      const allPrices = competitors.flatMap((comp) => comp.pricing.filter((p) => p.price > 0).map((p) => p.price));
      const maxPrice = Math.max(...allPrices);
      const minPrice = Math.min(...allPrices);
      return Math.round(100 - ((lowestPrice - minPrice) / (maxPrice - minPrice)) * 100);
    }
    case "ia": {
      const aiFeature = c.features.find((f) =>
        f.name.toLowerCase().includes("intelligence") || f.name.toLowerCase().includes("ia")
      );
      if (!aiFeature || !aiFeature.available) return 0;
      return qualityWeightedScore[aiFeature.quality] ?? 0;
    }
    case "ux": {
      const mobileFeature = c.features.find((f) => f.name.toLowerCase().includes("mobile"));
      if (!mobileFeature || !mobileFeature.available) return 50;
      return qualityWeightedScore[mobileFeature.quality] ?? 50;
    }
    case "support": {
      const apiFeature = c.features.find((f) => f.name.toLowerCase().includes("api"));
      if (!apiFeature || !apiFeature.available) return 0;
      return qualityWeightedScore[apiFeature.quality] ?? 0;
    }
  }
}

function computeWeightedScore(
  c: (typeof competitors)[0],
  weights: Record<CriteriaKey, number>
): number {
  const totalWeight = Object.values(weights).reduce((a, b) => a + b, 0);
  if (totalWeight === 0) return 0;
  const raw = CRITERIA.reduce((acc, criterion) => {
    const q = getCriteriaQualityScore(c, criterion.key);
    return acc + q * (weights[criterion.key] / 100);
  }, 0);
  // Normalize by total weight ratio
  return Math.min(100, Math.round((raw * 100) / totalWeight));
}

// Mock past comparisons
const PAST_COMPARISONS = [
  { label: "Salesforce vs HubSpot · 12 juin", ids: ["1", "2"] },
  { label: "Pipedrive vs Zoho · 8 juin", ids: ["3", "4"] },
  { label: "Tous vs Tous · 1 juin", ids: ["1", "2", "3"] },
];

export default function ComparePage() {
  const [selectedIds, setSelectedIds] = useState<string[]>(competitors.slice(0, 3).map((c) => c.id));

  // Weighted score state
  const [weights, setWeights] = useState<Record<CriteriaKey, number>>({
    prix: 40,
    ia: 25,
    ux: 20,
    support: 15,
  });

  // Notes state
  const [notes, setNotes] = useState("");
  const [noteSaved, setNoteSaved] = useState(false);

  // Load notes from localStorage on mount
  useEffect(() => {
    try {
      const saved = localStorage.getItem("compare_notes");
      if (saved) setNotes(saved);
    } catch {
      // ignore
    }
  }, []);

  function toggleSelect(id: string) {
    setSelectedIds((prev) => {
      if (prev.includes(id)) return prev.filter((x) => x !== id);
      if (prev.length >= 3) return prev;
      return [...prev, id];
    });
  }

  const selected = useMemo(
    () => competitors.filter((c) => selectedIds.includes(c.id)),
    [selectedIds]
  );

  const scores = useMemo(
    () =>
      selected
        .map((c) => ({ id: c.id, name: c.name, color: c.color, score: getCompetitorScore(c) }))
        .sort((a, b) => b.score - a.score),
    [selected]
  );

  const bestId = scores[0]?.id ?? null;
  const aiInsight = useMemo(() => generateAIInsight(selected), [selected]);

  const featureAvailableCounts = useMemo(
    () =>
      featureNames.map((featureName) => ({
        name: featureName,
        count: selected.filter((c) => {
          const f = getFeatureForCompetitor(c, featureName);
          return f?.available ?? false;
        }).length,
      })),
    [selected]
  );

  // Weighted scores per selected competitor
  const weightedScores = useMemo(
    () =>
      selected.map((c) => ({
        id: c.id,
        name: c.name,
        color: c.color,
        score: computeWeightedScore(c, weights),
      })).sort((a, b) => b.score - a.score),
    [selected, weights]
  );

  const weightedBest = weightedScores[0] ?? null;

  // Save notes handler
  const handleSaveNotes = useCallback(() => {
    try {
      localStorage.setItem("compare_notes", notes);
    } catch {
      // ignore
    }
    setNoteSaved(true);
    setTimeout(() => setNoteSaved(false), 2000);
  }, [notes]);

  // Export PDF (text blob)
  function handleExportPDF() {
    if (selected.length === 0) return;
    const lines: string[] = [
      "CompeteIQ — Comparaison des concurrents",
      `Exporté le ${new Date().toLocaleDateString("fr-FR")}`,
      "",
      "=== CONCURRENTS SÉLECTIONNÉS ===",
      ...selected.map((c) => `- ${c.name} (Score: ${scores.find((s) => s.id === c.id)?.score ?? 0}%)`),
      "",
      "=== MATRICE DES FONCTIONNALITÉS ===",
      ["Fonctionnalité", ...selected.map((c) => c.name)].join(" | "),
      ...featureNames.map((fn) => {
        const row = [fn, ...selected.map((c) => {
          const f = getFeatureForCompetitor(c, fn);
          return f ? (f.available ? f.quality : "Non dispo") : "—";
        })];
        return row.join(" | ");
      }),
      "",
      "=== SCORE PONDÉRÉ ===",
      ...weightedScores.map((ws) => `${ws.name}: ${ws.score}/100`),
      weightedBest ? `\nRecommandation : ${weightedBest.name} est le concurrent le mieux positionné` : "",
      "",
      "=== NOTES ===",
      notes || "(aucune note)",
    ];

    const blob = new Blob([lines.join("\n")], { type: "application/pdf" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `comparaison-concurrents-${new Date().toISOString().slice(0, 10)}.pdf`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  // Weighted score bar color
  function getBarColor(score: number): string {
    if (score >= 75) return "#10b981"; // emerald
    if (score >= 50) return "#3b82f6"; // blue
    if (score >= 25) return "#f59e0b"; // amber
    return "#ef4444"; // red
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div className="flex flex-col gap-1">
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
            Comparez vos concurrents en un coup d&apos;œil
          </h2>
          <p className="text-slate-500 text-sm">
            Sélectionnez jusqu&apos;à 3 concurrents et visualisez leurs forces, leurs lacunes et vos opportunités.
          </p>
        </div>
        <button
          onClick={handleExportPDF}
          disabled={selected.length === 0}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white text-sm font-semibold shadow-sm hover:bg-indigo-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors flex-shrink-0"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
          </svg>
          Exporter PDF
        </button>
      </div>

      {/* Competitor selector pills */}
      <div className="flex flex-wrap gap-2">
        {competitors.map((c) => {
          const isSelected = selectedIds.includes(c.id);
          const isDisabled = !isSelected && selectedIds.length >= 3;
          return (
            <button
              key={c.id}
              onClick={() => !isDisabled && toggleSelect(c.id)}
              disabled={isDisabled}
              className={[
                "inline-flex items-center gap-2 px-3.5 py-2 rounded-full text-sm font-medium border transition-all",
                isSelected
                  ? "text-white border-transparent shadow-sm"
                  : isDisabled
                  ? "bg-slate-50 text-slate-300 border-slate-200 cursor-not-allowed"
                  : "bg-white text-slate-700 border-slate-200 hover:border-slate-300 hover:bg-slate-50 cursor-pointer",
              ].join(" ")}
              style={isSelected ? { backgroundColor: c.color, borderColor: c.color } : {}}
            >
              <span
                className={[
                  "w-5 h-5 rounded flex items-center justify-center text-xs font-bold",
                  isSelected ? "bg-white/20" : "text-white",
                ].join(" ")}
                style={isSelected ? {} : { backgroundColor: c.color }}
              >
                {c.logo}
              </span>
              {c.name}
              {isSelected && (
                <span className="ml-0.5 opacity-75 text-xs">✕</span>
              )}
            </button>
          );
        })}
        {selectedIds.length >= 3 && (
          <span className="inline-flex items-center px-3 py-2 text-xs text-slate-400">
            Maximum 3 concurrents — désélectionnez-en un pour changer.
          </span>
        )}
      </div>

      {selected.length === 0 ? (
        <div className="bg-slate-50 border border-dashed border-slate-200 rounded-xl py-20 flex flex-col items-center justify-center gap-5 text-center">
          {/* Animated SVG illustration — two empty columns face to face */}
          <svg
            viewBox="0 0 160 100"
            className="w-40 h-auto text-slate-300"
            aria-hidden="true"
          >
            {/* Left column */}
            <rect x="8" y="20" width="58" height="72" rx="6" fill="currentColor" opacity="0.25" />
            <rect x="16" y="30" width="42" height="8" rx="3" fill="currentColor" opacity="0.4">
              <animate attributeName="opacity" values="0.4;0.7;0.4" dur="2.4s" repeatCount="indefinite" />
            </rect>
            <rect x="16" y="46" width="30" height="6" rx="3" fill="currentColor" opacity="0.3">
              <animate attributeName="opacity" values="0.3;0.6;0.3" dur="2.4s" begin="0.4s" repeatCount="indefinite" />
            </rect>
            <rect x="16" y="58" width="36" height="6" rx="3" fill="currentColor" opacity="0.3">
              <animate attributeName="opacity" values="0.3;0.6;0.3" dur="2.4s" begin="0.8s" repeatCount="indefinite" />
            </rect>
            <rect x="16" y="70" width="24" height="6" rx="3" fill="currentColor" opacity="0.3">
              <animate attributeName="opacity" values="0.3;0.6;0.3" dur="2.4s" begin="1.2s" repeatCount="indefinite" />
            </rect>

            {/* VS divider */}
            <circle cx="80" cy="56" r="12" fill="white" stroke="currentColor" strokeWidth="1.5" opacity="0.5" />
            <text x="80" y="60.5" textAnchor="middle" fontSize="9" fontWeight="bold" fill="currentColor" opacity="0.5">VS</text>

            {/* Right column (mirrored) */}
            <rect x="94" y="20" width="58" height="72" rx="6" fill="currentColor" opacity="0.25" />
            <rect x="102" y="30" width="42" height="8" rx="3" fill="currentColor" opacity="0.4">
              <animate attributeName="opacity" values="0.4;0.7;0.4" dur="2.4s" begin="1.2s" repeatCount="indefinite" />
            </rect>
            <rect x="102" y="46" width="30" height="6" rx="3" fill="currentColor" opacity="0.3">
              <animate attributeName="opacity" values="0.3;0.6;0.3" dur="2.4s" begin="1.6s" repeatCount="indefinite" />
            </rect>
            <rect x="102" y="58" width="36" height="6" rx="3" fill="currentColor" opacity="0.3">
              <animate attributeName="opacity" values="0.3;0.6;0.3" dur="2.4s" begin="2.0s" repeatCount="indefinite" />
            </rect>
            <rect x="102" y="70" width="24" height="6" rx="3" fill="currentColor" opacity="0.3">
              <animate attributeName="opacity" values="0.3;0.6;0.3" dur="2.4s" begin="0.4s" repeatCount="indefinite" />
            </rect>
          </svg>

          <div className="space-y-1.5">
            <p className="text-[15px] font-semibold text-slate-700">
              Sélectionnez 2 concurrents pour commencer la comparaison
            </p>
            <p className="text-[13px] text-slate-400 max-w-sm">
              Utilisez les pills ci-dessus pour choisir jusqu&apos;à 3 acteurs
            </p>
          </div>
        </div>
      ) : (
        <>
          {/* Score cards */}
          <div className={`grid gap-4 ${selected.length === 1 ? "grid-cols-1 max-w-xs" : selected.length === 2 ? "grid-cols-2 max-w-sm" : "grid-cols-3"}`}>
            {scores.map((s, i) => {
              const isBest = s.id === bestId && selected.length > 1;
              return (
                <div
                  key={s.id}
                  className={[
                    "rounded-xl border p-5 text-center relative transition-all",
                    isBest
                      ? "bg-blue-50 border-blue-200 shadow-sm"
                      : "bg-white border-slate-200",
                  ].join(" ")}
                >
                  {isBest && (
                    <span className="absolute -top-2.5 left-1/2 -translate-x-1/2 bg-blue-600 text-white text-xs font-semibold px-2.5 py-0.5 rounded-full">
                      Meilleur score
                    </span>
                  )}
                  <div className="relative inline-flex items-center justify-center mb-3">
                    <svg className="w-16 h-16 -rotate-90" viewBox="0 0 36 36">
                      <circle cx="18" cy="18" r="15.9" fill="none" stroke="#f1f5f9" strokeWidth="2.5" />
                      <circle
                        cx="18"
                        cy="18"
                        r="15.9"
                        fill="none"
                        stroke={s.color}
                        strokeWidth="2.5"
                        strokeDasharray={`${s.score} 100`}
                        strokeLinecap="round"
                      />
                    </svg>
                    <span className="absolute text-sm font-bold text-slate-800">{s.score}%</span>
                  </div>
                  {i === 0 && selected.length > 1 && (
                    <p className="text-xs text-amber-500 font-semibold mb-1"><span aria-hidden="true">🏆</span> #1 global</p>
                  )}
                  <p className="text-sm font-semibold text-slate-800">{s.name}</p>
                  <p className="text-xs text-slate-400 mt-0.5">
                    {featureAvailableCounts.filter((f) => {
                      const c = selected.find((cc) => cc.id === s.id)!;
                      const feat = getFeatureForCompetitor(c, f.name);
                      return feat?.available;
                    }).length} / {featureNames.length} features
                  </p>
                </div>
              );
            })}
          </div>

          {/* Feature matrix */}
          <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-slate-900">Matrice des fonctionnalités</h3>
                <p className="text-xs text-slate-400 mt-0.5">La colonne la mieux notée est mise en évidence.</p>
              </div>
              <div className="flex items-center gap-3 text-xs text-slate-500">
                <span className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block"></span> Excellent
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-blue-500 inline-block"></span> Bien
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-amber-400 inline-block"></span> Moyen
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-slate-200 inline-block"></span> Indisponible
                </span>
              </div>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm min-w-[500px]">
                <thead>
                  <tr className="border-b border-slate-100 bg-slate-50">
                    <th className="text-left px-5 py-3.5 text-xs font-semibold text-slate-500 uppercase tracking-wide w-48">
                      Fonctionnalité
                    </th>
                    {selected.map((c) => {
                      const isBest = c.id === bestId && selected.length > 1;
                      return (
                        <th
                          key={c.id}
                          className={["px-4 py-3.5 text-center", isBest ? "bg-blue-50" : ""].join(" ")}
                        >
                          <Link
                            href={`/dashboard/competitors/${c.id}`}
                            className="flex flex-col items-center gap-1.5 hover:opacity-80 transition-opacity"
                          >
                            <div
                              className="w-8 h-8 rounded-lg flex items-center justify-center text-white text-xs font-bold shadow-sm"
                              style={{ backgroundColor: c.color }}
                            >
                              {c.logo}
                            </div>
                            <span className="text-xs font-semibold text-slate-700">{c.name.split(" ")[0]}</span>
                            {isBest && (
                              <span className="text-[10px] font-semibold text-blue-600 bg-blue-100 px-1.5 py-0.5 rounded-full">
                                Leader
                              </span>
                            )}
                          </Link>
                        </th>
                      );
                    })}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-50">
                  {featureNames.map((featureName) => (
                    <tr key={featureName} className="hover:bg-slate-50/60 transition-colors">
                      <td className="px-5 py-3.5 text-sm font-medium text-slate-700">{featureName}</td>
                      {selected.map((c) => {
                        const feature = getFeatureForCompetitor(c, featureName);
                        const isBest = c.id === bestId && selected.length > 1;
                        return (
                          <td
                            key={c.id}
                            className={["px-4 py-3.5 text-center", isBest ? "bg-blue-50/50" : ""].join(" ")}
                          >
                            {feature ? (
                              <QualityBadge quality={feature.quality} available={feature.available} />
                            ) : (
                              <span className="text-slate-300 text-base">—</span>
                            )}
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
                <tfoot>
                  <tr className="border-t-2 border-slate-100 bg-slate-50">
                    <td className="px-5 py-3.5 text-xs font-bold text-slate-600 uppercase tracking-wide">
                      Score global
                    </td>
                    {selected.map((c) => {
                      const s = scores.find((sc) => sc.id === c.id)!;
                      const isBest = c.id === bestId && selected.length > 1;
                      const featCount = featureNames.filter((name) => {
                        const f = getFeatureForCompetitor(c, name);
                        return f?.available;
                      }).length;
                      return (
                        <td
                          key={c.id}
                          className={["px-4 py-3.5 text-center", isBest ? "bg-blue-50" : ""].join(" ")}
                        >
                          <div className="flex flex-col items-center gap-0.5">
                            <span
                              className={[
                                "text-base font-bold",
                                isBest ? "text-blue-700" : "text-slate-800",
                              ].join(" ")}
                            >
                              {s.score}%
                            </span>
                            <span className="text-xs text-slate-400">
                              {featCount}/{featureNames.length} features
                            </span>
                          </div>
                        </td>
                      );
                    })}
                  </tr>
                </tfoot>
              </table>
            </div>
          </div>

          {/* Weighted Score Section */}
          <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-100">
              <h3 className="font-semibold text-slate-900">Score pondéré</h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Ajustez les poids pour chaque critère selon vos priorités. Total affiché /100.
              </p>
            </div>
            <div className="p-5 space-y-6">
              {/* Weight sliders */}
              <div className="grid sm:grid-cols-2 gap-4">
                {CRITERIA.map((criterion) => (
                  <div key={criterion.key} className="space-y-1.5">
                    <div className="flex items-center justify-between">
                      <label className="text-sm font-medium text-slate-700">{criterion.label}</label>
                      <span className="text-sm font-semibold text-indigo-600 tabular-nums w-12 text-right">
                        {weights[criterion.key]}%
                      </span>
                    </div>
                    <input
                      type="range"
                      min={0}
                      max={100}
                      value={weights[criterion.key]}
                      onChange={(e) =>
                        setWeights((prev) => ({ ...prev, [criterion.key]: Number(e.target.value) }))
                      }
                      className="w-full h-1.5 rounded-full accent-indigo-600 cursor-pointer"
                    />
                  </div>
                ))}
              </div>

              {/* Weighted scores per competitor */}
              {selected.length > 0 && (
                <div className="space-y-3">
                  {weightedScores.map((ws, idx) => (
                    <div key={ws.id} className="space-y-1">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          {idx === 0 && selected.length > 1 && (
                            <span className="text-xs font-semibold text-amber-500">★</span>
                          )}
                          <span className="text-sm font-medium text-slate-700">{ws.name}</span>
                        </div>
                        <span
                          className="text-2xl font-extrabold tabular-nums"
                          style={{ color: getBarColor(ws.score) }}
                        >
                          {ws.score}
                          <span className="text-sm font-semibold text-slate-400">/100</span>
                        </span>
                      </div>
                      <div className="h-2.5 bg-slate-100 rounded-full overflow-hidden">
                        <div
                          className="h-full rounded-full transition-all duration-500"
                          style={{
                            width: `${ws.score}%`,
                            backgroundColor: getBarColor(ws.score),
                          }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Recommendation */}
              {weightedBest && selected.length > 1 && (
                <div className="bg-indigo-50 border border-indigo-100 rounded-lg px-4 py-3">
                  <p className="text-sm text-indigo-800">
                    <span className="font-semibold">Recommandation :</span>{" "}
                    <span className="font-bold">{weightedBest.name}</span> est le concurrent le mieux positionné
                    avec un score pondéré de{" "}
                    <span className="font-bold">{weightedBest.score}/100</span>.
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* AI Analysis */}
          {selected.length > 0 && (
            <div className="bg-blue-50 border border-blue-100 rounded-xl p-5">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white text-base font-bold shadow-sm">
                  ✦
                </div>
                <div>
                  <p className="text-sm font-semibold text-blue-900 mb-1">Analyse IA — Recommandation stratégique</p>
                  <p className="text-sm text-blue-800 leading-relaxed">{aiInsight}</p>
                  <p className="text-xs text-blue-400 mt-2">
                    Basé sur les données mises à jour le{" "}
                    {new Date(
                      Math.max(...selected.map((c) => new Date(c.lastUpdated).getTime()))
                    ).toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" })}
                  </p>
                </div>
              </div>
            </div>
          )}
        </>
      )}

      {/* Notes de comparaison */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 space-y-3">
        <h3 className="font-semibold text-slate-900 text-sm">Notes de comparaison</h3>
        <textarea
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          placeholder="Ajouter des notes à cette comparaison…"
          rows={3}
          className="w-full text-sm text-slate-700 placeholder-slate-400 border border-slate-200 rounded-lg px-3 py-2 resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
        />
        <div className="flex items-center gap-3">
          <button
            onClick={handleSaveNotes}
            className="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-indigo-600 text-white text-sm font-semibold hover:bg-indigo-700 transition-colors"
          >
            Sauvegarder
          </button>
          {noteSaved && (
            <span className="text-sm font-medium text-emerald-600 transition-opacity">
              ✓ Sauvegardé
            </span>
          )}
        </div>
      </div>

      {/* Historique des comparaisons */}
      <div className="space-y-3">
        <h3 className="font-semibold text-slate-700 text-sm">Comparaisons récentes</h3>
        <div className="flex flex-wrap gap-2">
          {PAST_COMPARISONS.map((comp) => (
            <button
              key={comp.label}
              onClick={() => setSelectedIds(comp.ids)}
              className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full border border-slate-200 bg-white text-sm text-slate-600 hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-700 transition-all cursor-pointer"
            >
              <svg className="w-3.5 h-3.5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {comp.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
