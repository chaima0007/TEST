import { competitors } from "@/lib/data";
import Link from "next/link";

function getPriceTrend(priceHistory: number[]): { trend: "up" | "down" | "stable"; pct: number } {
  const len = priceHistory.length;
  if (len < 2) return { trend: "stable", pct: 0 };
  const prev = priceHistory[Math.max(0, len - 2)];
  const curr = priceHistory[len - 1];
  if (curr === prev) return { trend: "stable", pct: 0 };
  const pct = Math.round(Math.abs(((curr - prev) / prev) * 100));
  return { trend: curr > prev ? "up" : "down", pct };
}

export default function PricingPage() {
  const competitorsWithTrend = competitors.map((c) => ({
    ...c,
    ...getPriceTrend(c.priceHistory),
  }));

  const opportunities = competitorsWithTrend.filter((c) => c.trend === "down");

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col gap-1">
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
          Suivez l&apos;évolution des prix en temps réel
        </h2>
        <p className="text-slate-500 text-sm">
          Chaque baisse de prix chez un concurrent est une opportunité commerciale. Chaque hausse, un avantage à saisir.
        </p>
      </div>

      {/* Price cards grid */}
      <div className="grid lg:grid-cols-2 xl:grid-cols-3 gap-5">
        {competitorsWithTrend.map((c) => (
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
              {c.pricing.map((plan) => (
                <div key={plan.name} className="bg-slate-50 rounded-lg p-3">
                  <p className="text-xs text-slate-500 mb-0.5">{plan.name}</p>
                  <p className="text-lg font-bold text-slate-900">
                    {plan.price === 0
                      ? <span className="text-emerald-600">Gratuit</span>
                      : `${plan.price}${plan.currency}`}
                    {plan.price > 0 && (
                      <span className="text-xs font-normal text-slate-400">/{plan.interval}</span>
                    )}
                  </p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

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
                      {entry.price === 0
                        ? <span className="text-emerald-600">Gratuit</span>
                        : `${entry.price}${entry.currency}/${entry.interval}`}
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
