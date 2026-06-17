import { notFound } from "next/navigation";
import Link from "next/link";
import { competitors } from "@/lib/data";

const newsTypeColors: Record<string, string> = {
  product: "bg-indigo-100 text-indigo-700",
  pricing: "bg-amber-100 text-amber-700",
  acquisition: "bg-rose-100 text-rose-700",
  partnership: "bg-emerald-100 text-emerald-700",
};

const newsTypeLabels: Record<string, string> = {
  product: "Produit",
  pricing: "Tarifs",
  acquisition: "Acquisition",
  partnership: "Partenariat",
};

export default async function CompetitorDetailPage(props: PageProps<"/dashboard/competitors/[id]">) {
  const { id } = await props.params;
  const competitor = competitors.find((c) => c.id === id);
  if (!competitor) notFound();

  const maxPrice = Math.max(...competitor.priceHistory);

  return (
    <div className="space-y-6">
      {/* Back */}
      <Link href="/dashboard/competitors" className="text-sm text-slate-500 hover:text-slate-900 flex items-center gap-1">
        ← Retour aux concurrents
      </Link>

      {/* Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-6">
        <div className="flex items-start gap-4">
          <div
            className="w-16 h-16 rounded-2xl flex items-center justify-center text-white text-xl font-bold flex-shrink-0"
            style={{ backgroundColor: competitor.color }}
          >
            {competitor.logo}
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-3 flex-wrap">
              <h2 className="text-2xl font-bold text-slate-900">{competitor.name}</h2>
              <a
                href={`https://${competitor.website}`}
                className="text-sm text-indigo-600 hover:underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                {competitor.website} ↗
              </a>
            </div>
            <p className="text-slate-500 mt-1 text-sm">{competitor.description}</p>
            <div className="flex flex-wrap gap-4 mt-4">
              <span className="text-xs text-slate-500"><span className="font-medium text-slate-700">Fondé en</span> {competitor.founded}</span>
              <span className="text-xs text-slate-500"><span className="font-medium text-slate-700">Employés</span> {competitor.employees}</span>
              <span className="text-xs text-slate-500"><span className="font-medium text-slate-700">Revenue</span> {competitor.revenue}</span>
              <span className="text-xs text-slate-500"><span className="font-medium text-slate-700">Part de marché</span> {competitor.marketShare}%</span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Features */}
        <div className="bg-white rounded-xl border border-slate-200 p-5">
          <h3 className="font-semibold text-slate-900 mb-4">Fonctionnalités</h3>
          <div className="space-y-3">
            {competitor.features.map((f) => (
              <div key={f.name} className="flex items-center justify-between py-2 border-b border-slate-50 last:border-0">
                <div className="flex items-center gap-2">
                  <span className={`text-base ${f.available ? "text-emerald-500" : "text-slate-300"}`}>
                    {f.available ? "✓" : "✗"}
                  </span>
                  <span className="text-sm text-slate-700">{f.name}</span>
                </div>
                {f.available && (
                  <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                    f.quality === "Excellent" ? "bg-emerald-100 text-emerald-700" :
                    f.quality === "Bien" ? "bg-indigo-100 text-indigo-700" :
                    "bg-slate-100 text-slate-600"
                  }`}>
                    {f.quality}
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Price history chart */}
        <div className="bg-white rounded-xl border border-slate-200 p-5">
          <h3 className="font-semibold text-slate-900 mb-4">Évolution du prix (plan de base, 12 mois)</h3>
          <div className="flex items-end gap-1.5 h-40">
            {competitor.priceHistory.map((price, i) => {
              const height = Math.round((price / maxPrice) * 100);
              const months = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"];
              return (
                <div key={i} className="flex-1 flex flex-col items-center gap-1">
                  <span className="text-[9px] text-slate-400">{price}€</span>
                  <div
                    className="w-full rounded-t-sm"
                    style={{ height: `${height}%`, backgroundColor: competitor.color, opacity: i === 11 ? 1 : 0.5 + (i / 11) * 0.5 }}
                  ></div>
                  <span className="text-[9px] text-slate-400">{months[i]}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Pricing plans */}
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <h3 className="font-semibold text-slate-900 mb-4">Plans tarifaires actuels</h3>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {competitor.pricing.map((plan) => (
            <div key={plan.name} className="border border-slate-200 rounded-xl p-4">
              <h4 className="font-semibold text-slate-800 text-sm mb-1">{plan.name}</h4>
              <div className="flex items-baseline gap-0.5 mb-3">
                <span className="text-2xl font-bold text-slate-900">{plan.price}</span>
                <span className="text-sm text-slate-400">{plan.currency}/{plan.interval}</span>
              </div>
              <ul className="space-y-1.5">
                {plan.features.map((f) => (
                  <li key={f} className="text-xs text-slate-500 flex items-center gap-1.5">
                    <span className="text-emerald-500 text-xs">✓</span> {f}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      {/* News */}
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <h3 className="font-semibold text-slate-900 mb-4">Actualités récentes</h3>
        <div className="space-y-3">
          {competitor.news.map((n, i) => (
            <div key={i} className="flex items-start gap-3 py-3 border-b border-slate-50 last:border-0">
              <span className={`text-xs font-medium px-2 py-0.5 rounded-full flex-shrink-0 ${newsTypeColors[n.type] || "bg-slate-100 text-slate-600"}`}>
                {newsTypeLabels[n.type] || n.type}
              </span>
              <p className="text-sm text-slate-700 flex-1">{n.title}</p>
              <span className="text-xs text-slate-400 flex-shrink-0">{n.date}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
