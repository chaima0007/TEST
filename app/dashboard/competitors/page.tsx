import Link from "next/link";
import { competitors } from "@/lib/data";

const threatColors = {
  high: "bg-red-100 text-red-700 border-red-200",
  medium: "bg-amber-100 text-amber-700 border-amber-200",
  low: "bg-emerald-100 text-emerald-700 border-emerald-200",
};

const threatLabels = {
  high: "Menace Élevée",
  medium: "Menace Moyenne",
  low: "Menace Faible",
};

export default function CompetitorsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Concurrents</h2>
          <p className="text-slate-500 text-sm mt-1">{competitors.length} concurrents surveillés</p>
        </div>
        <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors">
          + Ajouter un concurrent
        </button>
      </div>

      {/* Filter tabs */}
      <div className="flex gap-2">
        {["Tous", "Menace Élevée", "Menace Moyenne", "Menace Faible"].map((tab) => (
          <button
            key={tab}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              tab === "Tous"
                ? "bg-indigo-600 text-white"
                : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-50"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Grid */}
      <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-5">
        {competitors.map((c) => (
          <Link
            key={c.id}
            href={`/dashboard/competitors/${c.id}`}
            className="bg-white rounded-xl border border-slate-200 p-5 hover:border-indigo-300 hover:shadow-md transition-all group"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div
                  className="w-10 h-10 rounded-xl flex items-center justify-center text-white font-bold text-sm"
                  style={{ backgroundColor: c.color }}
                >
                  {c.logo}
                </div>
                <div>
                  <h3 className="font-semibold text-slate-900 group-hover:text-indigo-600 transition-colors">
                    {c.name}
                  </h3>
                  <p className="text-xs text-slate-400">{c.website}</p>
                </div>
              </div>
              <span className={`text-xs font-medium px-2 py-0.5 rounded-full border ${threatColors[c.threatLevel]}`}>
                {threatLabels[c.threatLevel]}
              </span>
            </div>

            <p className="text-sm text-slate-500 line-clamp-2 mb-4 leading-relaxed">{c.description}</p>

            <div className="grid grid-cols-2 gap-3">
              <div className="bg-slate-50 rounded-lg p-3">
                <p className="text-xs text-slate-400">Secteur</p>
                <p className="text-xs font-medium text-slate-700 mt-0.5">{c.industry}</p>
              </div>
              <div className="bg-slate-50 rounded-lg p-3">
                <p className="text-xs text-slate-400">Part de marché</p>
                <p className="text-xs font-medium text-slate-700 mt-0.5">{c.marketShare}%</p>
              </div>
              <div className="bg-slate-50 rounded-lg p-3">
                <p className="text-xs text-slate-400">Employés</p>
                <p className="text-xs font-medium text-slate-700 mt-0.5">{c.employees}</p>
              </div>
              <div className="bg-slate-50 rounded-lg p-3">
                <p className="text-xs text-slate-400">Mis à jour</p>
                <p className="text-xs font-medium text-slate-700 mt-0.5">{c.lastUpdated}</p>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
