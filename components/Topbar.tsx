"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

const breadcrumbs: Record<string, string> = {
  "/dashboard": "Tableau de bord",
  "/dashboard/competitors": "Concurrents",
  "/dashboard/compare": "Comparaison",
  "/dashboard/pricing": "Tarification",
  "/dashboard/alerts": "Alertes",
  "/dashboard/reports": "Rapports",
  "/dashboard/settings": "Paramètres",
};

export default function Topbar() {
  const pathname = usePathname();
  const [alertCount, setAlertCount] = useState<number | null>(null);

  useEffect(() => {
    fetch("/api/stats")
      .then((r) => r.json())
      .then((d: { alerts?: number }) => setAlertCount(d.alerts ?? 0))
      .catch(() => {});
  }, []);

  const segments = pathname.split("/").filter(Boolean);
  const crumbs: { label: string; href: string }[] = [];
  let path = "";
  for (const seg of segments) {
    path += "/" + seg;
    const label = breadcrumbs[path];
    if (label) crumbs.push({ label, href: path });
    else crumbs.push({ label: seg, href: path });
  }

  const pageTitle = breadcrumbs[pathname] ?? crumbs[crumbs.length - 1]?.label ?? "Dashboard";

  return (
    <header className="h-14 bg-white border-b border-slate-200 flex items-center justify-between px-4 md:px-6 gap-4">
      {/* Breadcrumb — offset on mobile for hamburger */}
      <div className="flex items-center gap-1.5 text-sm ml-12 md:ml-0 min-w-0">
        {crumbs.map((c, i) => (
          <span key={c.href} className="flex items-center gap-1.5 min-w-0">
            {i > 0 && <span className="text-slate-300">/</span>}
            {i === crumbs.length - 1
              ? <span className="font-semibold text-slate-900 truncate">{c.label}</span>
              : <Link href={c.href} className="text-slate-500 hover:text-slate-800 transition-colors truncate">{c.label}</Link>
            }
          </span>
        ))}
      </div>

      {/* Right actions */}
      <div className="flex items-center gap-3 flex-shrink-0">
        <Link href="/dashboard/alerts" className="relative p-1.5 text-slate-500 hover:text-slate-800 transition-colors" title="Alertes">
          <span className="text-lg">🔔</span>
          {alertCount !== null && alertCount > 0 && (
            <span className="absolute -top-0.5 -right-0.5 w-4 h-4 bg-red-500 text-white text-[9px] font-bold rounded-full flex items-center justify-center">
              {alertCount > 9 ? "9+" : alertCount}
            </span>
          )}
        </Link>
        <span className="hidden sm:flex text-xs bg-emerald-100 text-emerald-700 px-2.5 py-1 rounded-full font-medium items-center gap-1">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          En ligne
        </span>
        <div className="w-7 h-7 rounded-full bg-indigo-500 flex items-center justify-center text-white text-xs font-bold">
          DU
        </div>
      </div>
    </header>
  );
}
