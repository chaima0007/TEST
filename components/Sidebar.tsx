"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/dashboard", label: "Tableau de bord", icon: "⊞" },
  { href: "/dashboard/competitors", label: "Concurrents", icon: "🏢" },
  { href: "/dashboard/pricing", label: "Tarification", icon: "💰" },
  { href: "/dashboard/alerts", label: "Alertes", icon: "🔔" },
  { href: "/dashboard/reports", label: "Rapports", icon: "📊" },
  { href: "/dashboard/settings", label: "Paramètres", icon: "⚙️" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 min-h-screen bg-slate-900 flex flex-col">
      {/* Logo */}
      <div className="px-6 py-5 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
            <span className="text-white text-xs font-bold">IQ</span>
          </div>
          <span className="text-white font-bold text-base">CompeteIQ</span>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map((item) => {
          const isActive =
            item.href === "/dashboard"
              ? pathname === "/dashboard"
              : pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`sidebar-link ${isActive ? "sidebar-link-active" : ""}`}
            >
              <span className="text-base">{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* User */}
      <div className="px-4 py-4 border-t border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center text-white text-xs font-bold">
            DU
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm text-white font-medium truncate">Demo User</p>
            <p className="text-xs text-slate-400 truncate">demo@competeiq.com</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
