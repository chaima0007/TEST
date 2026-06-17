import { competitors } from "@/lib/data";
import Link from "next/link";

export default function PricingPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-900">Suivi des prix</h2>
        <p className="text-slate-500 text-sm mt-1">Comparaison des tarifs de tous vos concurrents</p>
      </div>

      {/* Price cards grid */}
      <div className="grid lg:grid-cols-2 xl:grid-cols-3 gap-5">
        {competitors.map((c) => (
          <div key={c.id} className="bg-white rounded-xl border border-slate-200 overflow-hidden">
            <div className="px-5 py-4 flex items-center justify-between border-b border-slate-100"
              style={{ borderLeftColor: c.color, borderLeftWidth: 4 }}>
              <div className="flex items-center gap-3">
                <div
                  className="w-8 h-8 rounded-lg flex items-center justify-center text-white text-xs font-bold"
                  style={{ backgroundColor: c.color }}
                >
                  {c.logo}
                </div>
                <span className="font-semibold text-slate-900">{c.name}</span>
              </div>
              <Link href={`/dashboard/competitors/${c.id}`} className="text-xs text-indigo-600 hover:underline">
                Détails →
              </Link>
            </div>
            <div className="p-4 grid grid-cols-2 gap-3">
              {c.pricing.map((plan) => (
                <div key={plan.name} className="bg-slate-50 rounded-lg p-3">
                  <p className="text-xs text-slate-500 mb-0.5">{plan.name}</p>
                  <p className="text-lg font-bold text-slate-900">
                    {plan.price === 0 ? "Gratuit" : `${plan.price}${plan.currency}`}
                    {plan.price > 0 && <span className="text-xs font-normal text-slate-400">/{plan.interval}</span>}
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
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-100">
                <th className="text-left px-5 py-3 text-xs font-medium text-slate-500 uppercase w-40">Concurrent</th>
                <th className="text-left px-4 py-3 text-xs font-medium text-slate-500 uppercase">Plan</th>
                <th className="text-left px-4 py-3 text-xs font-medium text-slate-500 uppercase">Prix</th>
                <th className="text-left px-4 py-3 text-xs font-medium text-slate-500 uppercase hidden md:table-cell">Fonctionnalités</th>
                <th className="text-left px-4 py-3 text-xs font-medium text-slate-500 uppercase">Tendance</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {competitors.map((c) => {
                const entry = c.pricing[0];
                const prev = c.priceHistory[10];
                const curr = c.priceHistory[11];
                const trend = curr > prev ? "up" : curr < prev ? "down" : "stable";
                return (
                  <tr key={c.id} className="hover:bg-slate-50">
                    <td className="px-5 py-3">
                      <div className="flex items-center gap-2">
                        <div className="w-6 h-6 rounded flex items-center justify-center text-white text-xs font-bold"
                          style={{ backgroundColor: c.color }}>
                          {c.logo}
                        </div>
                        <span className="font-medium text-slate-800">{c.name}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-slate-600">{entry.name}</td>
                    <td className="px-4 py-3 font-semibold text-slate-900">
                      {entry.price === 0 ? "Gratuit" : `${entry.price}${entry.currency}/${entry.interval}`}
                    </td>
                    <td className="px-4 py-3 text-slate-500 hidden md:table-cell">
                      {entry.features.slice(0, 2).join(", ")}
                      {entry.features.length > 2 && <span className="text-slate-400"> +{entry.features.length - 2}</span>}
                    </td>
                    <td className="px-4 py-3">
                      <span className={`text-sm font-medium ${trend === "up" ? "text-red-500" : trend === "down" ? "text-emerald-500" : "text-slate-400"}`}>
                        {trend === "up" ? "↑ Hausse" : trend === "down" ? "↓ Baisse" : "— Stable"}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
