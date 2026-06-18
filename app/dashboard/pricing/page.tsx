"use client";

import { competitors } from "@/lib/data";
import Link from "next/link";
import { useState, useMemo, useRef } from "react";

function getPriceTrend(priceHistory: number[]): { trend: "up" | "down" | "stable"; pct: number } {
  const len = priceHistory.length;
  if (len < 2) return { trend: "stable", pct: 0 };
  const prev = priceHistory[Math.max(0, len - 2)];
  const curr = priceHistory[len - 1];
  if (curr === prev) return { trend: "stable", pct: 0 };
  const pct = Math.round(Math.abs(((curr - prev) / prev) * 100));
  return { trend: curr > prev ? "up" : "down", pct };
}

// Pure SVG sparkline for price history
function PriceSparkline({ data, color }: { data: number[]; color: string }) {
  const width = 80;
  const height = 28;
  const padding = 2;

  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;

  const points = data.map((v, i) => {
    const x = padding + (i / (data.length - 1)) * (width - padding * 2);
    const y = height - padding - ((v - min) / range) * (height - padding * 2);
    return `${x},${y}`;
  });

  const polyline = points.join(" ");

  // Fill area under sparkline
  const fillPoints = [
    `${padding},${height - padding}`,
    ...points,
    `${width - padding},${height - padding}`,
  ].join(" ");

  const trend = data[data.length - 1] > data[0] ? "up" : "down";

  return (
    <svg viewBox={`0 0 ${width} ${height}`} width={width} height={height} aria-hidden="true">
      <polygon points={fillPoints} fill={color} opacity="0.08" />
      <polyline
        points={polyline}
        fill="none"
        stroke={color}
        strokeWidth="1.5"
        strokeLinejoin="round"
        strokeLinecap="round"
      />
      {/* Last point dot */}
      {points.length > 0 && (() => {
        const last = points[points.length - 1].split(",");
        return (
          <circle
            cx={parseFloat(last[0])}
            cy={parseFloat(last[1])}
            r="2"
            fill={trend === "up" ? "#ef4444" : "#10b981"}
          />
        );
      })()}
    </svg>
  );
}

// Mini comparison table for selected plans
function PlanComparisonTable({
  selectedPlanKeys,
}: {
  selectedPlanKeys: string[];
}) {
  const allPlans = competitors.flatMap((c) =>
    c.pricing.map((p) => ({ ...p, competitorName: c.name, competitorColor: c.color, key: `${c.id}::${p.name}` }))
  );
  const plans = allPlans.filter((p) => selectedPlanKeys.includes(p.key));

  // Collect all feature names across selected plans
  const allFeatures = Array.from(new Set(plans.flatMap((p) => p.features)));

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-xs min-w-[400px]">
        <thead>
          <tr className="border-b border-slate-100 bg-slate-50">
            <th className="text-left px-4 py-2 text-xs font-semibold text-slate-500 uppercase tracking-wide">
              Fonctionnalité
            </th>
            {plans.map((p) => (
              <th key={p.key} className="px-3 py-2 text-center">
                <div className="flex flex-col items-center gap-1">
                  <span
                    className="text-xs font-bold px-2 py-0.5 rounded text-white"
                    style={{ backgroundColor: p.competitorColor }}
                  >
                    {p.competitorName}
                  </span>
                  <span className="text-xs text-slate-600 font-medium">{p.name}</span>
                  <span className="text-sm font-bold text-slate-900">
                    {p.price === 0 ? "Gratuit" : `${p.price}${p.currency}/${p.interval}`}
                  </span>
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-50">
          {allFeatures.map((feat) => (
            <tr key={feat} className="hover:bg-slate-50 transition-colors">
              <td className="px-4 py-2 text-slate-600">{feat}</td>
              {plans.map((p) => (
                <td key={p.key} className="px-3 py-2 text-center">
                  {p.features.includes(feat) ? (
                    <span className="text-emerald-500 font-bold">✓</span>
                  ) : (
                    <span className="text-slate-300">—</span>
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function PricingPage() {
  // Budget filter
  const [maxBudget, setMaxBudget] = useState(500);

  // Plan comparator
  const [selectedPlanKeys, setSelectedPlanKeys] = useState<string[]>([]);
  const comparisonRef = useRef<HTMLDivElement>(null);

  const competitorsWithTrend = competitors.map((c) => ({
    ...c,
    ...getPriceTrend(c.priceHistory),
  }));

  const opportunities = competitorsWithTrend.filter((c) => c.trend === "down");

  // Budget-filtered competitors: show only competitors that have at least one plan ≤ maxBudget
  const filteredCompetitors = useMemo(
    () =>
      competitorsWithTrend.filter((c) =>
        c.pricing.some((p) => p.price <= maxBudget)
      ),
    [competitorsWithTrend, maxBudget]
  );

  // Count all plans across all competitors that are within budget
  const plansInBudget = useMemo(
    () =>
      competitorsWithTrend.reduce(
        (acc, c) => acc + c.pricing.filter((p) => p.price <= maxBudget).length,
        0
      ),
    [competitorsWithTrend, maxBudget]
  );

  function togglePlanSelect(key: string) {
    setSelectedPlanKeys((prev) =>
      prev.includes(key) ? prev.filter((k) => k !== key) : [...prev, key]
    );
  }

  function scrollToComparison() {
    comparisonRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  // CSV Export
  function handleExportCSV() {
    const rows: string[][] = [
      ["Concurrent", "Plan", "Prix", "Devise", "Intervalle", "Fonctionnalités"],
    ];
    competitors.forEach((c) => {
      c.pricing.forEach((p) => {
        rows.push([
          c.name,
          p.name,
          String(p.price),
          p.currency,
          p.interval,
          p.features.join("; "),
        ]);
      });
    });
    const csv = rows.map((r) => r.map((cell) => `"${cell}"`).join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `grille-tarifaire-${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div className="flex flex-col gap-1">
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
            Suivez l&apos;évolution des prix en temps réel
          </h2>
          <p className="text-slate-500 text-sm">
            Chaque baisse de prix chez un concurrent est une opportunité commerciale. Chaque hausse, un avantage à saisir.
          </p>
        </div>
        <button
          onClick={handleExportCSV}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-800 text-white text-sm font-semibold shadow-sm hover:bg-slate-900 transition-colors flex-shrink-0"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
          </svg>
          Exporter la grille tarifaire
        </button>
      </div>

      {/* AI Recommendation Card */}
      <div className="bg-indigo-50 border border-indigo-100 rounded-xl p-5">
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white text-base shadow-sm">
            💡
          </div>
          <div>
            <p className="text-sm font-semibold text-indigo-900 mb-1">Recommandation PRISM</p>
            <p className="text-sm text-indigo-800 leading-relaxed">
              Salesforce a augmenté ses prix de <strong>12% en mai 2026</strong>. HubSpot reste stable.{" "}
              <strong>Fenêtre d&apos;opportunité</strong> : positionnez-vous contre Salesforce sur les comptes{" "}
              <strong>&gt;100 utilisateurs</strong> avant juillet 2026.
            </p>
          </div>
        </div>
      </div>

      {/* Budget filter */}
      <div className="bg-white rounded-xl border border-slate-200 px-5 py-4 space-y-3">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-slate-900 text-sm">Filtre par budget</h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Affiche uniquement les concurrents avec au moins un plan dans votre budget.
            </p>
          </div>
          <span className="text-sm font-semibold text-indigo-600 tabular-nums">
            {plansInBudget} plan{plansInBudget !== 1 ? "s" : ""} dans votre budget
          </span>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-sm text-slate-500 whitespace-nowrap">
            Budget mensuel max :{" "}
            <span className="font-bold text-slate-900">
              {maxBudget === 500 ? "500€ (tout)" : `${maxBudget}€`}
            </span>
          </span>
          <input
            type="range"
            min={0}
            max={500}
            step={5}
            value={maxBudget}
            onChange={(e) => setMaxBudget(Number(e.target.value))}
            className="flex-1 h-1.5 rounded-full accent-indigo-600 cursor-pointer"
          />
        </div>
      </div>

      {/* Price cards grid */}
      <div className="grid lg:grid-cols-2 xl:grid-cols-3 gap-5">
        {filteredCompetitors.map((c) => {
          const trendIsUp = c.trend === "up";
          const historyMin = Math.min(...c.priceHistory);
          const historyMax = Math.max(...c.priceHistory);
          const historyFirst = c.priceHistory[0];
          const historyLast = c.priceHistory[c.priceHistory.length - 1];
          const trendArrow = historyLast > historyFirst ? "↑" : "↓";
          const trendColor = historyLast > historyFirst ? "text-red-500" : "text-emerald-600";

          return (
            <div key={c.id} className="bg-white rounded-xl border border-slate-200 overflow-hidden">
              <div
                className="px-5 py-4 flex items-center justify-between border-b border-slate-100"
                style={{ borderLeftColor: c.color, borderLeftWidth: 4 }}
              >
                <div className="flex items-center gap-3">
                  <div
                    className="w-8 h-8 rounded-lg flex items-center justify-center text-white text-xs font-bold shadow-sm"
                    style={{ backgroundColor: c.color }}
                  >
                    {c.logo}
                  </div>
                  <span className="font-semibold text-slate-900">{c.name}</span>
                </div>
                <div className="flex items-center gap-2">
                  {c.trend === "up" && (
                    <span className="inline-flex items-center gap-1 text-xs font-semibold px-2 py-1 rounded-full bg-red-50 text-red-600 border border-red-100">
                      ↑ Hausse récente
                    </span>
                  )}
                  {c.trend === "down" && (
                    <span className="inline-flex items-center gap-1 text-xs font-semibold px-2 py-1 rounded-full bg-emerald-50 text-emerald-600 border border-emerald-100">
                      ↓ Baisse
                    </span>
                  )}
                  <Link href={`/dashboard/competitors/${c.id}`} className="text-xs text-indigo-600 hover:underline">
                    Détails →
                  </Link>
                </div>
              </div>

              <div className="p-4 grid grid-cols-2 gap-3">
                {c.pricing
                  .filter((p) => p.price <= maxBudget)
                  .map((plan) => {
                    const planKey = `${c.id}::${plan.name}`;
                    const isChecked = selectedPlanKeys.includes(planKey);
                    return (
                      <div key={plan.name} className="bg-slate-50 rounded-lg p-3 relative">
                        <label className="absolute top-2 right-2 flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={isChecked}
                            onChange={() => togglePlanSelect(planKey)}
                            className="w-3.5 h-3.5 rounded accent-indigo-600 cursor-pointer"
                          />
                        </label>
                        <p className="text-xs text-slate-500 mb-0.5 pr-5">{plan.name}</p>
                        <p className="text-lg font-bold text-slate-900">
                          {plan.price === 0 ? (
                            <span className="text-emerald-600">Gratuit</span>
                          ) : (
                            `${plan.price}${plan.currency}`
                          )}
                          {plan.price > 0 && (
                            <span className="text-xs font-normal text-slate-400">/{plan.interval}</span>
                          )}
                        </p>
                        {isChecked && (
                          <span className="text-[10px] font-semibold text-indigo-600">Comparer</span>
                        )}
                      </div>
                    );
                  })}
              </div>

              {/* Price history sparkline */}
              <div className="px-4 pb-4">
                <div className="bg-slate-50 rounded-lg px-3 py-2">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-semibold text-slate-600">Historique des prix</span>
                    <span className={`text-xs font-bold ${trendColor}`}>
                      {trendArrow} {trendIsUp ? "Hausse" : "Baisse"}
                    </span>
                  </div>
                  <div className="flex items-center gap-3">
                    <PriceSparkline data={c.priceHistory} color={c.color} />
                    <div className="flex flex-col gap-0.5 text-[11px] text-slate-500">
                      <span>
                        Min :{" "}
                        <span className="font-semibold text-emerald-600">{historyMin}€</span>
                      </span>
                      <span>
                        Max :{" "}
                        <span className="font-semibold text-red-500">{historyMax}€</span>
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        })}

        {filteredCompetitors.length === 0 && (
          <div className="col-span-3 py-12 flex flex-col items-center justify-center gap-3 text-center">
            <span className="text-3xl">🔍</span>
            <p className="text-slate-600 font-medium">Aucun plan dans ce budget</p>
            <p className="text-sm text-slate-400">Augmentez le budget maximum pour voir plus de plans.</p>
          </div>
        )}
      </div>

      {/* Sticky comparator bar */}
      {selectedPlanKeys.length >= 2 && (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 bg-slate-900 text-white px-6 py-3 rounded-full shadow-xl flex items-center gap-4 text-sm font-semibold">
          <span>{selectedPlanKeys.length} plans sélectionnés</span>
          <span className="text-slate-500">—</span>
          <button
            onClick={scrollToComparison}
            className="text-indigo-400 hover:text-indigo-300 transition-colors"
          >
            Comparer →
          </button>
          <button
            onClick={() => setSelectedPlanKeys([])}
            className="text-slate-500 hover:text-slate-300 text-xs transition-colors"
          >
            ✕ Effacer
          </button>
        </div>
      )}

      {/* Plan comparator table */}
      {selectedPlanKeys.length >= 2 && (
        <div ref={comparisonRef} className="bg-white rounded-xl border border-indigo-200 overflow-hidden scroll-mt-8">
          <div className="px-5 py-4 border-b border-slate-100 bg-indigo-50 flex items-center justify-between">
            <div>
              <h3 className="font-semibold text-indigo-900">Comparateur de plans</h3>
              <p className="text-xs text-indigo-500 mt-0.5">
                {selectedPlanKeys.length} plans sélectionnés — comparaison côte à côte
              </p>
            </div>
            <button
              onClick={() => setSelectedPlanKeys([])}
              className="text-xs text-indigo-400 hover:text-indigo-600 transition-colors"
            >
              Effacer la sélection
            </button>
          </div>
          <PlanComparisonTable selectedPlanKeys={selectedPlanKeys} />
        </div>
      )}

      {/* Comparison table */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-100">
          <h3 className="font-semibold text-slate-900">Tableau comparatif — Plans d&apos;entrée de gamme</h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Comparez les offres de départ et leur évolution récente.
          </p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-100 bg-slate-50">
                <th className="text-left px-5 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide w-44">
                  Concurrent
                </th>
                <th className="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">
                  Plan
                </th>
                <th className="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">
                  Prix
                </th>
                <th className="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide hidden md:table-cell">
                  Fonctionnalités incluses
                </th>
                <th className="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">
                  Tendance
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {competitorsWithTrend.map((c) => {
                const entry = c.pricing[0];
                return (
                  <tr key={c.id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-5 py-3.5">
                      <div className="flex items-center gap-2">
                        <div
                          className="w-6 h-6 rounded flex items-center justify-center text-white text-xs font-bold"
                          style={{ backgroundColor: c.color }}
                        >
                          {c.logo}
                        </div>
                        <span className="font-medium text-slate-800">{c.name}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3.5 text-slate-600">{entry.name}</td>
                    <td className="px-4 py-3.5 font-semibold text-slate-900">
                      {entry.price === 0 ? (
                        <span className="text-emerald-600">Gratuit</span>
                      ) : (
                        `${entry.price}${entry.currency}/${entry.interval}`
                      )}
                    </td>
                    <td className="px-4 py-3.5 text-slate-500 hidden md:table-cell">
                      {entry.features.slice(0, 2).join(", ")}
                      {entry.features.length > 2 && (
                        <span className="text-slate-400"> +{entry.features.length - 2}</span>
                      )}
                    </td>
                    <td className="px-4 py-3.5">
                      {c.trend === "up" && (
                        <span className="inline-flex items-center gap-1 text-sm font-semibold text-red-500">
                          ↑ +{c.pct}%
                        </span>
                      )}
                      {c.trend === "down" && (
                        <span className="inline-flex items-center gap-1 text-sm font-semibold text-emerald-600">
                          ↓ -{c.pct}%
                        </span>
                      )}
                      {c.trend === "stable" && (
                        <span className="text-sm font-medium text-slate-400">— Stable</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Opportunity block */}
      {opportunities.length > 0 && (
        <div className="bg-emerald-50 border border-emerald-100 rounded-xl p-5">
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center text-white text-base font-bold shadow-sm">
              ↓
            </div>
            <div>
              <p className="text-sm font-bold text-emerald-900 mb-1">
                Opportunité commerciale détectée
              </p>
              <p className="text-sm text-emerald-800 leading-relaxed">
                {opportunities.length === 1 ? (
                  <>
                    <strong>{opportunities[0].name}</strong> a baissé ses prix récemment (
                    {opportunities[0].pct}%). C&apos;est le moment d&apos;activer vos offres comparatives
                    et de contacter vos prospects en phase de décision.
                  </>
                ) : (
                  <>
                    <strong>{opportunities.map((c) => c.name).join(" et ")}</strong> ont tous deux
                    réduit leurs tarifs. Capitalisez sur ce signal : vos équipes commerciales ont
                    maintenant un argument prix fort face à des concurrents en repli.
                  </>
                )}
              </p>
              <div className="mt-3 flex flex-wrap gap-2">
                {opportunities.map((c) => (
                  <Link
                    key={c.id}
                    href={`/dashboard/competitors/${c.id}`}
                    className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-700 bg-white border border-emerald-200 px-3 py-1.5 rounded-lg hover:bg-emerald-50 transition-colors"
                  >
                    <span
                      className="w-4 h-4 rounded text-white text-[10px] flex items-center justify-center font-bold"
                      style={{ backgroundColor: c.color }}
                    >
                      {c.logo}
                    </span>
                    Voir {c.name} →
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
