import Link from "next/link";
import { competitors, alerts, stats } from "@/lib/data";

const threatColors = {
  high: "bg-red-100 text-red-700",
  medium: "bg-amber-100 text-amber-700",
  low: "bg-emerald-100 text-emerald-700",
};

const alertTypeIcons: Record<string, string> = {
  pricing: "💰",
  feature: "🚀",
  acquisition: "🤝",
  product: "📦",
  partnership: "🔗",
  website: "🌐",
};

const statCards = [
  {
    label: "Concurrents suivis",
    value: stats.competitorsTracked,
    icon: "🏢",
    color: "bg-indigo-50 text-indigo-600",
    href: "/dashboard/competitors",
  },
  {
    label: "Alertes actives",
    value: stats.activeAlerts,
    icon: "🔔",
    color: "bg-amber-50 text-amber-600",
    href: "/dashboard/alerts",
  },
  {
    label: "Rapports générés",
    value: stats.reportsGenerated,
    icon: "📊",
    color: "bg-emerald-50 text-emerald-600",
    href: "/dashboard/reports",
  },
  {
    label: "Score de marché",
    value: `${stats.marketScore}%`,
    icon: "📈",
    color: "bg-rose-50 text-rose-600",
    href: "/dashboard/compare",
  },
];

const recentActivity = [
  { action: "Salesforce a augmenté ses prix de 12%", time: "Il y a 2 jours", type: "pricing" },
  { action: "HubSpot a lancé une nouvelle fonctionnalité IA", time: "Il y a 7 jours", type: "feature" },
  { action: "Salesforce a acquis DataRobot pour 1,2 Md$", time: "Il y a 9 jours", type: "acquisition" },
  { action: "Pipedrive a lancé AI Sales Assistant en bêta", time: "Il y a 12 jours", type: "product" },
];

export default function DashboardPage() {
  const recentAlerts = alerts.filter((a) => !a.isRead).slice(0, 3);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-900">Tableau de bord</h2>
        <p className="text-slate-500 text-sm mt-1">Vue d&apos;ensemble de votre veille concurrentielle</p>
      </div>

      {/* Stats — each card links to its section */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((s) => (
          <Link
            key={s.label}
            href={s.href}
            className="bg-white rounded-xl border border-slate-200 p-5 hover:border-indigo-300 hover:shadow-md transition-all group"
          >
            <div className={`w-10 h-10 rounded-lg ${s.color} flex items-center justify-center text-lg mb-3 group-hover:scale-110 transition-transform`}>
              {s.icon}
            </div>
            <p className="text-2xl font-bold text-slate-900">{s.value}</p>
            <p className="text-xs text-slate-500 mt-0.5">{s.label}</p>
          </Link>
        ))}
      </div>

      {/* Quick actions */}
      <div className="bg-indigo-50 border border-indigo-100 rounded-xl p-5">
        <h3 className="font-semibold text-indigo-900 mb-3">Actions rapides</h3>
        <div className="flex flex-wrap gap-3">
          <Link
            href="/dashboard/competitors"
            className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors flex items-center gap-2"
          >
            <span>+</span> Ajouter un concurrent
          </Link>
          <Link
            href="/dashboard/reports"
            className="bg-white text-indigo-700 border border-indigo-200 px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-100 transition-colors flex items-center gap-2"
          >
            <span>✦</span> Générer un rapport
          </Link>
          <Link
            href="/dashboard/compare"
            className="bg-white text-indigo-700 border border-indigo-200 px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-100 transition-colors flex items-center gap-2"
          >
            <span>⚡</span> Comparer les concurrents
          </Link>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Competitors overview */}
        <div className="bg-white rounded-xl border border-slate-200">
          <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
            <h3 className="font-semibold text-slate-900">Concurrents</h3>
            <Link href="/dashboard/competitors" className="text-xs text-indigo-600 hover:underline">
              Voir tout
            </Link>
          </div>
          <div className="divide-y divide-slate-100">
            {competitors.map((c) => (
              <Link
                key={c.id}
                href={`/dashboard/competitors/${c.id}`}
                className="flex items-center gap-3 px-5 py-3.5 hover:bg-slate-50 transition-colors"
              >
                <div
                  className="w-8 h-8 rounded-lg flex items-center justify-center text-white text-xs font-bold flex-shrink-0"
                  style={{ backgroundColor: c.color }}
                >
                  {c.logo}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-slate-900">{c.name}</p>
                  <p className="text-xs text-slate-400">{c.industry}</p>
                </div>
                <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${threatColors[c.threatLevel]}`}>
                  {c.threatLevel === "high" ? "Élevée" : c.threatLevel === "medium" ? "Moyenne" : "Faible"}
                </span>
              </Link>
            ))}
          </div>
        </div>

        {/* Recent alerts */}
        <div className="bg-white rounded-xl border border-slate-200">
          <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
            <h3 className="font-semibold text-slate-900">Alertes récentes</h3>
            <Link href="/dashboard/alerts" className="text-xs text-indigo-600 hover:underline">
              Voir tout
            </Link>
          </div>
          <div className="divide-y divide-slate-100">
            {recentAlerts.map((a) => (
              <div key={a.id} className="px-5 py-4">
                <div className="flex items-start gap-3">
                  <span className="text-lg">{alertTypeIcons[a.type] || "📌"}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-slate-800 leading-snug">{a.message}</p>
                    <p className="text-xs text-slate-400 mt-1">{a.competitorName} · {a.date}</p>
                  </div>
                  <span className="w-2 h-2 rounded-full bg-indigo-500 flex-shrink-0 mt-1.5"></span>
                </div>
              </div>
            ))}
            {recentAlerts.length === 0 && (
              <p className="px-5 py-8 text-center text-slate-400 text-sm">Aucune alerte non lue</p>
            )}
          </div>
        </div>
      </div>

      {/* Activité récente */}
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <h3 className="font-semibold text-slate-900 mb-4">Activité récente</h3>
        <div className="space-y-0 divide-y divide-slate-50">
          {recentActivity.map((item, i) => (
            <div key={i} className="flex items-start gap-3 py-3">
              <span className="text-base flex-shrink-0 mt-0.5">
                {alertTypeIcons[item.type] || "📌"}
              </span>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-slate-700">{item.action}</p>
              </div>
              <span className="text-xs text-slate-400 flex-shrink-0 whitespace-nowrap">{item.time}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Market share */}
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <h3 className="font-semibold text-slate-900 mb-4">Parts de marché estimées</h3>
        <div className="space-y-3">
          {competitors.map((c) => (
            <div key={c.id} className="flex items-center gap-3">
              <span className="text-sm text-slate-600 w-28 truncate">{c.name}</span>
              <div className="flex-1 bg-slate-100 rounded-full h-2.5">
                <div
                  className="h-2.5 rounded-full transition-all"
                  style={{ width: `${(c.marketShare / 30) * 100}%`, backgroundColor: c.color }}
                ></div>
              </div>
              <span className="text-sm font-medium text-slate-700 w-12 text-right">{c.marketShare}%</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
