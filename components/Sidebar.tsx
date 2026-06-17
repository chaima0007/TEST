"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState, useEffect } from "react";

const navItems = [
  { href: "/dashboard", label: "Tableau de bord", icon: "⊞", exact: true },
  { href: "/dashboard/competitors", label: "Concurrents", icon: "🏢" },
  { href: "/dashboard/compare", label: "Comparaison", icon: "⚡" },
  { href: "/dashboard/pricing", label: "Tarification", icon: "💰" },
  { href: "/dashboard/alerts", label: "Alertes", icon: "🔔" },
  { href: "/dashboard/reports", label: "Rapports", icon: "📊" },
  { href: "/dashboard/settings", label: "Paramètres", icon: "⚙️" },
];

function NavContent({ onClose }: { onClose?: () => void }) {
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = async () => {
    await fetch("/api/auth/logout", { method: "POST" });
    router.push("/login");
  };
  return (
    <>
      <div className="px-6 py-5 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center flex-shrink-0">
            <span className="text-white text-xs font-bold">IQ</span>
          </div>
          <span className="text-white font-bold text-base">CompeteIQ</span>
        </div>
        {onClose && (
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl leading-none p-1 transition-colors" aria-label="Fermer le menu">
            ×
          </button>
        )}
      </div>

      <nav className="flex-1 px-3 py-4 space-y-0.5">
        {navItems.map((item) => {
          const isActive = item.exact
            ? pathname === item.href
            : pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              onClick={onClose}
              className={`sidebar-link ${isActive ? "sidebar-link-active" : ""}`}
            >
              <span className="text-base w-5 text-center flex-shrink-0">{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="px-4 py-4 border-t border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
            DU
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm text-white font-medium truncate">Demo User</p>
            <p className="text-xs text-slate-400 truncate">demo@competeiq.com</p>
          </div>
          <button onClick={handleLogout} className="text-slate-500 hover:text-slate-300 transition-colors text-xs" title="Déconnexion">
            ↪
          </button>
        </div>
      </div>
    </>
  );
}

export default function Sidebar() {
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => { if (e.key === "Escape") setMobileOpen(false); };
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, []);

  return (
    <>
      {/* Desktop sidebar */}
      <aside className="hidden md:flex w-64 min-h-screen bg-slate-900 flex-col flex-shrink-0">
        <NavContent />
      </aside>

      {/* Mobile: hamburger button in topbar slot */}
      <button
        onClick={() => setMobileOpen(true)}
        className="md:hidden fixed top-4 left-4 z-40 w-9 h-9 bg-slate-900 rounded-lg flex items-center justify-center text-white shadow-lg"
        aria-label="Ouvrir le menu"
      >
        <span className="text-lg">☰</span>
      </button>

      {/* Mobile: overlay + drawer */}
      {mobileOpen && (
        <>
          <div
            className="md:hidden fixed inset-0 z-40 bg-black/50"
            onClick={() => setMobileOpen(false)}
          />
          <aside className="md:hidden fixed inset-y-0 left-0 z-50 w-72 bg-slate-900 flex flex-col shadow-2xl">
            <NavContent onClose={() => setMobileOpen(false)} />
          </aside>
        </>
      )}
    </>
  );
}
