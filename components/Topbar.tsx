"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";

// ─── Breadcrumb map ───────────────────────────────────────────────────────────

const breadcrumbLabels: Record<string, string> = {
  "/dashboard": "Tableau de bord",
  "/dashboard/competitors": "Concurrents",
  "/dashboard/compare": "Comparaison",
  "/dashboard/pricing": "Tarification",
  "/dashboard/alerts": "Alertes",
  "/dashboard/reports": "Rapports",
  "/dashboard/settings": "Paramètres",
};

// ─── Search suggestions (hardcoded for demo) ─────────────────────────────────

const SUGGESTIONS = [
  { label: "Tableau de bord", href: "/dashboard" },
  { label: "Concurrents", href: "/dashboard/competitors" },
  { label: "Alertes", href: "/dashboard/alerts" },
  { label: "Rapports", href: "/dashboard/reports" },
  { label: "Paramètres", href: "/dashboard/settings" },
];

// ─── SVG Icons ────────────────────────────────────────────────────────────────

function IconSearch({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M12.9 14.32a8 8 0 1 1 1.41-1.41l4.38 4.38-1.41 1.41-4.38-4.38zM8 14A6 6 0 1 0 8 2a6 6 0 0 0 0 12z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function IconBell({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 2a6 6 0 0 0-6 6v2.586l-.707.707A1 1 0 0 0 4 13h12a1 1 0 0 0 .707-1.707L16 10.586V8a6 6 0 0 0-6-6zM8.5 17a1.5 1.5 0 0 0 3 0H8.5z" />
    </svg>
  );
}

function IconChevronDown({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M5.293 7.293a1 1 0 0 1 1.414 0L10 10.586l3.293-3.293a1 1 0 1 1 1.414 1.414l-4 4a1 1 0 0 1-1.414 0l-4-4a1 1 0 0 1 0-1.414z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function IconUser({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M10 9a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-7 9a7 7 0 1 1 14 0H3z"
        clipRule="evenodd"
      />
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

// ─── Search modal ─────────────────────────────────────────────────────────────

function SearchModal({ onClose }: { onClose: () => void }) {
  const [query, setQuery] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();

  useEffect(() => {
    inputRef.current?.focus();
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, [onClose]);

  const filtered = query.trim()
    ? SUGGESTIONS.filter((s) =>
        s.label.toLowerCase().includes(query.toLowerCase())
      )
    : SUGGESTIONS;

  const handleSelect = (href: string) => {
    router.push(href);
    onClose();
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center pt-24 px-4"
      aria-modal="true"
      role="dialog"
    >
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/40 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Panel */}
      <div className="relative w-full max-w-lg bg-white rounded-xl shadow-2xl overflow-hidden ring-1 ring-slate-200">
        {/* Input row */}
        <div className="flex items-center gap-3 px-4 py-3 border-b border-slate-100">
          <IconSearch className="w-5 h-5 text-slate-400 flex-shrink-0" />
          <input
            ref={inputRef}
            type="text"
            placeholder="Rechercher..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 bg-transparent text-slate-900 placeholder-slate-400 text-sm outline-none"
          />
          <kbd className="hidden sm:inline-flex items-center gap-0.5 rounded border border-slate-200 bg-slate-50 px-1.5 py-0.5 text-[11px] font-medium text-slate-500">
            ESC
          </kbd>
        </div>

        {/* Suggestions */}
        <ul className="py-2 max-h-72 overflow-y-auto">
          {filtered.length === 0 ? (
            <li className="px-4 py-3 text-sm text-slate-400">Aucun résultat.</li>
          ) : (
            filtered.map((s) => (
              <li key={s.href}>
                <button
                  onClick={() => handleSelect(s.href)}
                  className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-slate-700 hover:bg-slate-50 transition-colors text-left"
                >
                  <IconSearch className="w-4 h-4 text-slate-400 flex-shrink-0" />
                  {s.label}
                </button>
              </li>
            ))
          )}
        </ul>
      </div>
    </div>
  );
}

// ─── User dropdown ────────────────────────────────────────────────────────────

function UserDropdown() {
  const [open, setOpen] = useState(false);
  const router = useRouter();
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  const handleLogout = async () => {
    setOpen(false);
    await fetch("/api/auth/logout", { method: "POST" });
    // Hard redirect: clears React state, router cache, and any in-memory session data
    window.location.href = "/login";
  };

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex items-center gap-1.5 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1"
        aria-haspopup="true"
        aria-expanded={open}
        aria-label="Menu utilisateur"
      >
        <div className="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
          DU
        </div>
        <IconChevronDown className="w-3.5 h-3.5 text-slate-500 hidden sm:block" />
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-52 bg-white rounded-xl shadow-lg ring-1 ring-slate-200 py-1 z-50">
          {/* User info header */}
          <div className="px-4 py-2.5 border-b border-slate-100">
            <p className="text-sm font-semibold text-slate-900">Demo User</p>
            <p className="text-xs text-slate-500 truncate">demo@competeiq.com</p>
          </div>

          {/* Menu items */}
          <Link
            href="/dashboard/settings"
            onClick={() => setOpen(false)}
            className="flex items-center gap-2.5 px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 transition-colors"
          >
            <IconUser className="w-4 h-4 text-slate-400" />
            Profil
          </Link>
          <Link
            href="/dashboard/settings"
            onClick={() => setOpen(false)}
            className="flex items-center gap-2.5 px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 transition-colors"
          >
            <IconSettings className="w-4 h-4 text-slate-400" />
            Paramètres
          </Link>

          <div className="my-1 border-t border-slate-100" />

          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-2.5 px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
          >
            <IconLogout className="w-4 h-4" />
            Déconnexion
          </button>
        </div>
      )}
    </div>
  );
}

// ─── Topbar ───────────────────────────────────────────────────────────────────

const ALERT_BADGE_COUNT = 3;

export default function Topbar() {
  const pathname = usePathname();
  const [searchOpen, setSearchOpen] = useState(false);

  // Build breadcrumb trail
  const segments = pathname.split("/").filter(Boolean);
  const crumbs: { label: string; href: string }[] = [];
  let path = "";
  for (const seg of segments) {
    path += "/" + seg;
    const label = breadcrumbLabels[path] ?? seg;
    crumbs.push({ label, href: path });
  }

  // ⌘K / Ctrl+K global shortcut
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setSearchOpen(true);
      }
    };
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, []);

  return (
    <>
      <header className="h-14 bg-white border-b border-slate-200 flex items-center justify-between px-4 md:px-6 gap-4">

        {/* ── Breadcrumb ── */}
        <nav
          className="flex items-center gap-0 text-sm ml-12 md:ml-0 min-w-0"
          aria-label="Fil d'Ariane"
        >
          {crumbs.map((c, i) => (
            <span key={c.href} className="flex items-center min-w-0">
              {i > 0 && (
                <span className="mx-1.5 text-slate-300 select-none" aria-hidden="true">
                  /
                </span>
              )}
              {i === crumbs.length - 1 ? (
                <span className="font-semibold text-slate-900 truncate">{c.label}</span>
              ) : (
                <Link
                  href={c.href}
                  className="text-slate-500 hover:text-slate-800 transition-colors truncate"
                >
                  {c.label}
                </Link>
              )}
            </span>
          ))}
        </nav>

        {/* ── Right actions ── */}
        <div className="flex items-center gap-2 flex-shrink-0">

          {/* Search button */}
          <button
            onClick={() => setSearchOpen(true)}
            className="hidden sm:flex items-center gap-2 rounded-lg border border-slate-200 bg-slate-50 px-3 py-1.5 text-sm text-slate-500 hover:border-slate-300 hover:bg-white transition-colors"
            aria-label="Rechercher"
          >
            <IconSearch className="w-4 h-4" />
            <span className="hidden md:inline">Rechercher...</span>
            <kbd className="hidden md:inline-flex items-center gap-0.5 rounded border border-slate-200 bg-white px-1.5 py-0.5 text-[11px] font-medium text-slate-400">
              ⌘K
            </kbd>
          </button>

          {/* Mobile search icon */}
          <button
            onClick={() => setSearchOpen(true)}
            className="sm:hidden p-2 text-slate-500 hover:text-slate-800 transition-colors rounded-lg hover:bg-slate-100"
            aria-label="Rechercher"
          >
            <IconSearch className="w-5 h-5" />
          </button>

          {/* Notification bell */}
          <Link
            href="/dashboard/alerts"
            className="relative p-2 text-slate-500 hover:text-slate-800 transition-colors rounded-lg hover:bg-slate-100"
            aria-label={`Alertes — ${ALERT_BADGE_COUNT} nouvelles`}
          >
            <IconBell className="w-5 h-5" />
            <span className="absolute top-1 right-1 w-4 h-4 bg-red-500 text-white text-[9px] font-bold rounded-full flex items-center justify-center leading-none">
              {ALERT_BADGE_COUNT}
            </span>
          </Link>

          {/* Status pill */}
          <span className="hidden sm:flex text-xs bg-emerald-100 text-emerald-700 px-2.5 py-1 rounded-full font-medium items-center gap-1.5 select-none">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
            En ligne
          </span>

          {/* User avatar + dropdown */}
          <UserDropdown />
        </div>
      </header>

      {/* Search modal */}
      {searchOpen && <SearchModal onClose={() => setSearchOpen(false)} />}
    </>
  );
}
