import { competitors } from "@/lib/data";
import Link from "next/link";

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

function getFeatureForCompetitor(c: (typeof competitors)[0], featureName: string) {
  return c.features.find((f) =>
    f.name.toLowerCase().includes(featureName.toLowerCase().split(" ")[0].toLowerCase()) ||
    featureName.toLowerCase().includes(f.name.toLowerCase().split(" ")[0].toLowerCase()) ||
    f.name === featureName
  );
}

function qualityBadge(quality: string, available: boolean) {
  if (!available) return <span className="text-slate-300 text-lg">✗</span>;
  const colors: Record<string, string> = {
    Excellent: "bg-emerald-100 text-emerald-700",
    Bien: "bg-indigo-100 text-indigo-700",
    Moyen: "bg-amber-100 text-amber-700",
  };
  return (
    <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${colors[quality] || "bg-slate-100 text-slate-500"}`}>
      {quality}
    </span>
  );
}

export default function ComparePage() {
  const scores = competitors.map((c) => {
    const total = c.features.reduce((acc, f) => acc + (f.available ? qualityScore[f.quality] ?? 0 : 0), 0);
    const max = c.features.length * 3;
    return { id: c.id, name: c.name, score: Math.round((total / max) * 100) };
  }).sort((a, b) => b.score - a.score);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-900">Comparaison des fonctionnalités</h2>
        <p className="text-slate-500 text-sm mt-1">Matrice de comparaison de tous vos concurrents</p>
      </div>

      {/* Scores summary */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        {scores.map((s, i) => {
          const c = competitors.find((c) => c.id === s.id)!;
          return (
            <div key={s.id} className="bg-white rounded-xl border border-slate-200 p-4 text-center">
              <div className="relative inline-flex items-center justify-center mb-2">
                <svg className="w-14 h-14 -rotate-90" viewBox="0 0 36 36">
                  <circle cx="18" cy="18" r="15.9" fill="none" stroke="#f1f5f9" strokeWidth="3" />
                  <circle
                    cx="18" cy="18" r="15.9" fill="none"
                    stroke={c.color} strokeWidth="3"
                    strokeDasharray={`${s.score} 100`}
                    strokeLinecap="round"
                  />
                </svg>
                <span className="absolute text-sm font-bold text-slate-800">{s.score}%</span>
              </div>
              {i === 0 && <div className="text-xs text-amber-500 font-medium mb-0.5">🏆 #1</div>}
              <p className="text-xs font-semibold text-slate-700">{s.name}</p>
            </div>
          );
        })}
      </div>

      {/* Feature matrix */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm min-w-[700px]">
            <thead>
              <tr className="border-b border-slate-100 bg-slate-50">
                <th className="text-left px-5 py-3.5 text-xs font-semibold text-slate-500 uppercase w-52">
                  Fonctionnalité
                </th>
                {competitors.map((c) => (
                  <th key={c.id} className="px-3 py-3.5 text-center">
                    <Link href={`/dashboard/competitors/${c.id}`} className="flex flex-col items-center gap-1 hover:opacity-80">
                      <div
                        className="w-7 h-7 rounded-lg flex items-center justify-center text-white text-xs font-bold"
                        style={{ backgroundColor: c.color }}
                      >
                        {c.logo}
                      </div>
                      <span className="text-xs font-medium text-slate-700">{c.name.split(" ")[0]}</span>
                    </Link>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-50">
              {featureNames.map((featureName) => (
                <tr key={featureName} className="hover:bg-slate-50/50">
                  <td className="px-5 py-3.5 text-sm font-medium text-slate-700">{featureName}</td>
                  {competitors.map((c) => {
                    const feature = getFeatureForCompetitor(c, featureName);
                    return (
                      <td key={c.id} className="px-3 py-3.5 text-center">
                        {feature
                          ? qualityBadge(feature.quality, feature.available)
                          : <span className="text-slate-300 text-base">—</span>
                        }
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="px-5 py-3 border-t border-slate-100 bg-slate-50 flex items-center gap-4 text-xs text-slate-500">
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-emerald-500"></span> Excellent</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-indigo-500"></span> Bien</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-amber-500"></span> Moyen</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-slate-200"></span> Non disponible</span>
        </div>
      </div>

      {/* Pricing comparison */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-100">
          <h3 className="font-semibold text-slate-900">Comparaison des prix d&apos;entrée</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm min-w-[700px]">
            <thead>
              <tr className="border-b border-slate-100 bg-slate-50">
                <th className="text-left px-5 py-3 text-xs font-semibold text-slate-500 uppercase w-52">Concurrent</th>
                <th className="text-left px-3 py-3 text-xs font-semibold text-slate-500 uppercase">Plan le moins cher</th>
                <th className="text-left px-3 py-3 text-xs font-semibold text-slate-500 uppercase">Prix</th>
                <th className="text-left px-3 py-3 text-xs font-semibold text-slate-500 uppercase">Plan Premium</th>
                <th className="text-left px-3 py-3 text-xs font-semibold text-slate-500 uppercase">Prix Premium</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-50">
              {competitors.map((c) => {
                const entry = c.pricing[0];
                const top = c.pricing[c.pricing.length - 1];
                return (
                  <tr key={c.id} className="hover:bg-slate-50/50">
                    <td className="px-5 py-3.5">
                      <div className="flex items-center gap-2">
                        <div className="w-6 h-6 rounded flex items-center justify-center text-white text-xs font-bold"
                          style={{ backgroundColor: c.color }}>
                          {c.logo}
                        </div>
                        <span className="font-medium text-slate-800">{c.name}</span>
                      </div>
                    </td>
                    <td className="px-3 py-3.5 text-slate-600">{entry.name}</td>
                    <td className="px-3 py-3.5 font-semibold text-slate-900">
                      {entry.price === 0 ? <span className="text-emerald-600">Gratuit</span> : `${entry.price}€/mois`}
                    </td>
                    <td className="px-3 py-3.5 text-slate-600">{top.name}</td>
                    <td className="px-3 py-3.5 font-semibold text-slate-900">
                      {top.price === 0 ? <span className="text-emerald-600">Gratuit</span> : `${top.price}€/mois`}
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
