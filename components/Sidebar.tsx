"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState, useEffect } from "react";

// ─── SVG Icons ──────────────────────────────────────────────────────────────

function IconDashboard({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <rect x="2" y="2" width="7" height="7" rx="1" />
      <rect x="11" y="2" width="7" height="7" rx="1" />
      <rect x="2" y="11" width="7" height="7" rx="1" />
      <rect x="11" y="11" width="7" height="7" rx="1" />
    </svg>
  );
}

function IconCompetitors({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M3 7h4v10H3V7zM8 4h4v13H8V4zM13 9h4v8h-4V9z" />
    </svg>
  );
}

function IconComparison({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M2 10a8 8 0 1 1 16 0A8 8 0 0 1 2 10zm8-5v5h3l-4 5-4-5h3V5h2z" />
    </svg>
  );
}

function IconPricing({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M17.707 9.293l-7-7A1 1 0 0 0 10 2H4a2 2 0 0 0-2 2v6a1 1 0 0 0 .293.707l7 7a1 1 0 0 0 1.414 0l7-7a1 1 0 0 0 0-1.414zM6 7a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function IconAlerts({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 2a6 6 0 0 0-6 6v2.586l-.707.707A1 1 0 0 0 4 13h12a1 1 0 0 0 .707-1.707L16 10.586V8a6 6 0 0 0-6-6zM8.5 17a1.5 1.5 0 0 0 3 0H8.5z" />
    </svg>
  );
}

function IconReports({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M4 2a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.414A2 2 0 0 0 17.414 6L13 1.586A2 2 0 0 0 11.586 2H4zm7 1.5V7h3.5L11 3.5zM6 11h8v1.5H6V11zm0 3h5v1.5H6V14zm0-6h3v1.5H6V8z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function IconSwarm({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="4" r="2" />
      <circle cx="4" cy="14" r="2" />
      <circle cx="16" cy="14" r="2" />
      <circle cx="10" cy="10" r="1.5" />
      <path d="M10 6L4 12M10 6L16 12M10 6v2.5M4 12l4-1M16 12l-4-1" strokeWidth="1" stroke="currentColor" fill="none" />
    </svg>
  );
}

function IconSettings({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 0 1-2.286.948c-1.372-.836-2.942.734-2.106 2.106a1.533 1.533 0 0 1-.948 2.287c-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 0 1 .948 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 0 1 2.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 0 1 2.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 0 1 .947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 0 1-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 0 1-2.287-.947zM10 13a3 3 0 1 1 0-6 3 3 0 0 1 0 6z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function IconChevronLeft({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M12.707 5.293a1 1 0 0 1 0 1.414L9.414 10l3.293 3.293a1 1 0 0 1-1.414 1.414l-4-4a1 1 0 0 1 0-1.414l4-4a1 1 0 0 1 1.414 0z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function IconChevronRight({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M7.293 14.707a1 1 0 0 1 0-1.414L10.586 10 7.293 6.707a1 1 0 0 1 1.414-1.414l4 4a1 1 0 0 1 0 1.414l-4 4a1 1 0 0 1-1.414 0z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function IconLogout({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M3 3a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h6a1 1 0 1 0 0-2H4V5h5a1 1 0 1 0 0-2H3zm10.293 4.293a1 1 0 0 1 1.414 0l3 3a1 1 0 0 1 0 1.414l-3 3a1 1 0 0 1-1.414-1.414L14.586 11H8a1 1 0 1 1 0-2h6.586l-1.293-1.293a1 1 0 0 1 0-1.414z"
        clipRule="evenodd"
      />
    </svg>
  );
}

// ─── Nav structure ───────────────────────────────────────────────────────────

type NavItem = {
  href: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  exact?: boolean;
  badge?: number;
};

type NavSection = {
  title: string;
  items: NavItem[];
};

const navSections: NavSection[] = [
  {
    title: "ANALYSE",
    items: [
      { href: "/dashboard", label: "Tableau de bord", icon: IconDashboard, exact: true },
      { href: "/dashboard/compare", label: "Comparaison", icon: IconComparison },
      { href: "/dashboard/pricing", label: "Tarification", icon: IconPricing },
    ],
  },
  {
    title: "SURVEILLANCE",
    items: [
      { href: "/dashboard/competitors", label: "Concurrents", icon: IconCompetitors },
      { href: "/dashboard/alerts", label: "Alertes", icon: IconAlerts, badge: 3 },
      { href: "/dashboard/reports", label: "Rapports", icon: IconReports },
    ],
  },
  {
    title: "ESSAIM IA",
    items: [
      { href: "/dashboard/swarm", label: "50 Agents Swarm", icon: IconSwarm },
    ],
  },
  {
    title: "COMPTE",
    items: [
      { href: "/dashboard/settings", label: "Paramètres", icon: IconSettings },
    ],
  },
];

// ─── Inner nav content ───────────────────────────────────────────────────────

function NavContent({
  collapsed,
  onClose,
}: {
  collapsed: boolean;
  onClose?: () => void;
}) {
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = async () => {
    await fetch("/api/auth/logout", { method: "POST" });
    router.push("/login");
  };

  return (
    <>
      {/* Logo / brand */}
      <div
        className={`border-b border-slate-800 flex items-center ${
          collapsed ? "justify-center py-5 px-2" : "justify-between py-5 px-4"
        }`}
      >
        <div className="flex items-center gap-3 min-w-0">
          <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center flex-shrink-0">
            <span className="text-white text-xs font-bold">IQ</span>
          </div>
          {!collapsed && (
            <span className="text-white font-bold text-base truncate">CompeteIQ</span>
          )}
        </div>
        {!collapsed && onClose && (
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white text-xl leading-none p-1 transition-colors"
            aria-label="Fermer le menu"
          >
            ×
          </button>
        )}
      </div>

      {/* Navigation sections */}
      <nav className="flex-1 overflow-y-auto px-2 py-3 space-y-4">
        {navSections.map((section) => (
          <div key={section.title}>
            {/* Section label — hidden when collapsed */}
            {!collapsed && (
              <p className="px-3 mb-1 text-[10px] font-semibold tracking-widest text-slate-500 uppercase select-none">
                {section.title}
              </p>
            )}
            {collapsed && (
              <div className="border-t border-slate-800 my-2 mx-2" />
            )}

            <ul className="space-y-0.5">
              {section.items.map((item) => {
                const isActive = item.exact
                  ? pathname === item.href
                  : pathname.startsWith(item.href);
                const Icon = item.icon;

                return (
                  <li key={item.href}>
                    <Link
                      href={item.href}
                      onClick={onClose}
                      title={collapsed ? item.label : undefined}
                      className={`flex items-center gap-3 rounded-md text-sm font-medium transition-colors relative
                        ${collapsed ? "justify-center px-2 py-2.5" : "px-3 py-2"}
                        ${
                          isActive
                            ? "bg-blue-600 text-white"
                            : "text-slate-400 hover:bg-slate-800 hover:text-white"
                        }`}
                    >
                      {/* Icon + optional badge wrapper */}
                      <span className="relative flex-shrink-0">
                        <Icon className="w-5 h-5" />
                        {item.badge !== undefined && item.badge > 0 && (
                          <span className="absolute -top-1.5 -right-1.5 w-4 h-4 bg-red-500 text-white text-[9px] font-bold rounded-full flex items-center justify-center leading-none">
                            {item.badge > 9 ? "9+" : item.badge}
                          </span>
                        )}
                      </span>

                      {!collapsed && (
                        <>
                          <span className="flex-1 truncate">{item.label}</span>
                          {/* Badge also shows inline when expanded */}
                          {item.badge !== undefined && item.badge > 0 && (
                            <span className="ml-auto bg-red-500 text-white text-[10px] font-bold rounded-full min-w-[18px] h-[18px] flex items-center justify-center px-1">
                              {item.badge > 9 ? "9+" : item.badge}
                            </span>
                          )}
                        </>
                      )}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </nav>

      {/* User profile */}
      <div
        className={`border-t border-slate-800 ${collapsed ? "px-2 py-3" : "px-3 py-3"}`}
      >
        <div
          className={`flex items-center gap-3 ${collapsed ? "justify-center" : ""}`}
        >
          <div className="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
            DU
          </div>
          {!collapsed && (
            <>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-white font-medium truncate">Demo User</p>
                <p className="text-xs text-slate-400 truncate">demo@competeiq.com</p>
              </div>
              <button
                onClick={handleLogout}
                title="Déconnexion"
                className="text-slate-500 hover:text-slate-200 transition-colors p-1 rounded hover:bg-slate-800 flex-shrink-0"
                aria-label="Déconnexion"
              >
                <IconLogout className="w-4 h-4" />
              </button>
            </>
          )}
        </div>
        {/* Logout when collapsed — separate row */}
        {collapsed && (
          <button
            onClick={handleLogout}
            title="Déconnexion"
            className="mt-2 w-full flex justify-center text-slate-500 hover:text-slate-200 transition-colors p-1.5 rounded hover:bg-slate-800"
            aria-label="Déconnexion"
          >
            <IconLogout className="w-4 h-4" />
          </button>
        )}
      </div>
    </>
  );
}

// ─── Desktop sidebar shell with collapse toggle ──────────────────────────────

function DesktopSidebar() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={`hidden md:flex flex-col flex-shrink-0 min-h-screen bg-slate-900 transition-all duration-200 ${
        collapsed ? "w-16" : "w-64"
      }`}
    >
      <div className="flex-1 flex flex-col min-h-0">
        <NavContent collapsed={collapsed} />
      </div>

      {/* Collapse toggle */}
      <button
        onClick={() => setCollapsed((c) => !c)}
        className={`flex items-center gap-2 border-t border-slate-800 text-slate-500 hover:text-white hover:bg-slate-800 transition-colors text-xs font-medium py-3 px-4 ${
          collapsed ? "justify-center px-2" : ""
        }`}
        aria-label={collapsed ? "Déplier le menu" : "Replier le menu"}
      >
        {collapsed ? (
          <IconChevronRight className="w-4 h-4" />
        ) : (
          <>
            <IconChevronLeft className="w-4 h-4" />
            <span>Réduire</span>
          </>
        )}
      </button>
    </aside>
  );
}

// ─── Mobile drawer ───────────────────────────────────────────────────────────

function MobileSidebar() {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, []);

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="md:hidden fixed top-4 left-4 z-40 w-9 h-9 bg-slate-900 rounded-lg flex items-center justify-center text-white shadow-lg"
        aria-label="Ouvrir le menu"
      >
        <svg viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5" aria-hidden="true">
          <path
            fillRule="evenodd"
            d="M3 5h14a1 1 0 0 1 0 2H3a1 1 0 0 1 0-2zm0 4h14a1 1 0 0 1 0 2H3a1 1 0 0 1 0-2zm0 4h14a1 1 0 0 1 0 2H3a1 1 0 0 1 0-2z"
            clipRule="evenodd"
          />
        </svg>
      </button>

      {open && (
        <>
          <div
            className="md:hidden fixed inset-0 z-40 bg-black/50"
            onClick={() => setOpen(false)}
          />
          <aside className="md:hidden fixed inset-y-0 left-0 z-50 w-72 bg-slate-900 flex flex-col shadow-2xl">
            <NavContent collapsed={false} onClose={() => setOpen(false)} />
          </aside>
        </>
      )}
    </>
  );
}

// ─── Default export ──────────────────────────────────────────────────────────

export default function Sidebar() {
  return (
    <>
      <DesktopSidebar />
      <MobileSidebar />
    </>
  );
}
