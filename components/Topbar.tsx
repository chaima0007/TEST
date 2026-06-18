"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { LiveIndicator } from "@/components/LiveIndicator";
import { alerts } from "@/lib/data";

// ─── Breadcrumb segment map ───────────────────────────────────────────────────

const SEGMENT_LABELS: Record<string, string> = {
  dashboard:   "Dashboard",
  competitors: "Concurrents",
  compare:     "Comparaison",
  pricing:     "Tarification",
  alerts:      "Alertes",
  reports:     "Rapports",
  settings:    "Paramètres",
  battlecards: "Battle Cards",
  signals:     "Signaux Faibles",
  simulate:    "Simulateur",
  plan:        "Plan de Conquête",
  success:     "Simulation Succès",
  radar:       "Radar Clients",
  commandant:  "COMMANDANT",
  resolveur:   "RÉSOLVEUR",
};

// ─── Command palette commands ─────────────────────────────────────────────────

type CommandGroup = "Navigation" | "Actions rapides";

interface Command {
  id: string;
  label: string;
  href: string;
  group: CommandGroup;
}

const COMMANDS: Command[] = [
  // Navigation group
  { id: "nav-dashboard",    label: "Dashboard",            href: "/dashboard",              group: "Navigation" },
  { id: "nav-competitors",  label: "Concurrents",          href: "/dashboard/competitors",  group: "Navigation" },
  { id: "nav-pricing",      label: "Tarification",         href: "/dashboard/pricing",      group: "Navigation" },
  { id: "nav-alerts",       label: "Alertes",              href: "/dashboard/alerts",       group: "Navigation" },
  { id: "nav-reports",      label: "Rapports",             href: "/dashboard/reports",      group: "Navigation" },
  { id: "nav-compare",      label: "Comparaison",          href: "/dashboard/compare",      group: "Navigation" },
  { id: "nav-battlecards",  label: "Battle Cards",         href: "/dashboard/battlecards",  group: "Navigation" },
  { id: "nav-signals",      label: "Signaux Faibles",      href: "/dashboard/signals",      group: "Navigation" },
  { id: "nav-simulate",     label: "Simulateur",           href: "/dashboard/simulate",     group: "Navigation" },
  { id: "nav-radar",        label: "Radar Clients",        href: "/dashboard/radar",        group: "Navigation" },
  { id: "nav-plan",         label: "Plan de Conquête",     href: "/dashboard/plan",         group: "Navigation" },
  { id: "nav-success",      label: "Simulation Succès",    href: "/dashboard/success",      group: "Navigation" },
  { id: "nav-settings",     label: "Paramètres",           href: "/dashboard/settings",     group: "Navigation" },
  // Actions rapides group
  { id: "act-report",       label: "Générer un rapport",   href: "/dashboard/reports",      group: "Actions rapides" },
  { id: "act-alerts",       label: "Voir les alertes",     href: "/dashboard/alerts",       group: "Actions rapides" },
  { id: "act-compare",      label: "Comparer concurrents", href: "/dashboard/compare",      group: "Actions rapides" },
];

const GROUP_ORDER: CommandGroup[] = ["Navigation", "Actions rapides"];

// ─── Alert type colors ────────────────────────────────────────────────────────

const ALERT_TYPE_COLOR: Record<string, string> = {
  pricing:     "bg-amber-400",
  feature:     "bg-indigo-400",
  acquisition: "bg-red-400",
  partnership: "bg-green-400",
  product:     "bg-slate-400",
};

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

function IconArrow({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M10.293 5.293a1 1 0 0 1 1.414 0l4 4a1 1 0 0 1 0 1.414l-4 4a1 1 0 0 1-1.414-1.414L12.586 11H4a1 1 0 1 1 0-2h8.586l-2.293-2.293a1 1 0 0 1 0-1.414z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function IconDoc({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M4 4a2 2 0 0 1 2-2h4.586A2 2 0 0 1 12 2.586L15.414 6A2 2 0 0 1 16 7.414V16a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4zm2 6a1 1 0 0 1 1-1h6a1 1 0 1 1 0 2H7a1 1 0 0 1-1-1zm1 3a1 1 0 1 0 0 2h4a1 1 0 1 0 0-2H7z"
        clipRule="evenodd"
      />
    </svg>
  );
}

// ─── Command palette modal ─────────────────────────────────────────────────────

function CommandPalette({ onClose }: { onClose: () => void }) {
  const [query, setQuery] = useState("");
  const [activeIndex, setActiveIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const listRef = useRef<HTMLUListElement>(null);
  const router = useRouter();

  const filtered = query.trim()
    ? COMMANDS.filter((c) => c.label.toLowerCase().includes(query.toLowerCase()))
    : COMMANDS;

  useEffect(() => { setActiveIndex(0); }, [query]);
  useEffect(() => { inputRef.current?.focus(); }, []);

  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") { e.preventDefault(); onClose(); return; }
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setActiveIndex((i) => (i + 1) % Math.max(filtered.length, 1));
        return;
      }
      if (e.key === "ArrowUp") {
        e.preventDefault();
        setActiveIndex((i) => (i - 1 + Math.max(filtered.length, 1)) % Math.max(filtered.length, 1));
        return;
      }
      if (e.key === "Enter") {
        e.preventDefault();
        const cmd = filtered[activeIndex];
        if (cmd) { router.push(cmd.href); onClose(); }
        return;
      }
    };
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, [onClose, filtered, activeIndex, router]);

  useEffect(() => {
    const list = listRef.current;
    if (!list) return;
    const activeEl = list.querySelector("[data-active='true']");
    if (activeEl) (activeEl as HTMLElement).scrollIntoView({ block: "nearest" });
  }, [activeIndex]);

  const handleSelect = (href: string) => { router.push(href); onClose(); };

  const grouped = GROUP_ORDER.reduce<Record<CommandGroup, Command[]>>(
    (acc, group) => { acc[group] = filtered.filter((c) => c.group === group); return acc; },
    { Navigation: [], "Actions rapides": [] }
  );

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4"
      aria-modal="true"
      role="dialog"
      aria-label="Palette de commandes"
    >
      <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" onClick={onClose} />

      <div className="relative w-full max-w-lg bg-white rounded-xl shadow-2xl overflow-hidden ring-1 ring-slate-200">
        <div className="flex items-center gap-3 px-4 py-3 border-b border-slate-100">
          <IconSearch className="w-5 h-5 text-slate-400 flex-shrink-0" />
          <input
            ref={inputRef}
            type="text"
            placeholder="Rechercher une page ou une action..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 bg-transparent text-slate-900 placeholder-slate-400 text-sm outline-none"
            aria-autocomplete="list"
            aria-controls="cmd-palette-list"
          />
          <kbd className="hidden sm:inline-flex items-center gap-0.5 rounded border border-slate-200 bg-slate-50 px-1.5 py-0.5 text-[11px] font-medium text-slate-500">
            ESC
          </kbd>
        </div>

        <ul ref={listRef} id="cmd-palette-list" role="listbox" className="py-2 max-h-80 overflow-y-auto">
          {filtered.length === 0 ? (
            <li className="px-4 py-6 text-sm text-slate-400 text-center">
              Aucun résultat pour &ldquo;{query}&rdquo;
            </li>
          ) : (
            GROUP_ORDER.map((group) => {
              const items = grouped[group];
              if (items.length === 0) return null;
              const isAction = group === "Actions rapides";
              return (
                <li key={group} role="presentation">
                  <div className="px-4 pt-3 pb-1">
                    <span className="text-[10px] font-semibold uppercase tracking-widest text-slate-400 select-none">
                      {group}
                    </span>
                  </div>
                  <ul role="group" aria-label={group}>
                    {items.map((cmd) => {
                      const flatIdx = filtered.indexOf(cmd);
                      const isActive = flatIdx === activeIndex;
                      return (
                        <li
                          key={cmd.id}
                          role="option"
                          aria-selected={isActive}
                          data-active={isActive ? "true" : undefined}
                        >
                          <button
                            onMouseEnter={() => setActiveIndex(flatIdx)}
                            onClick={() => handleSelect(cmd.href)}
                            className={`w-full flex items-center gap-3 px-4 py-2.5 text-sm transition-colors text-left ${
                              isActive ? "bg-indigo-50 text-indigo-700" : "text-slate-700 hover:bg-slate-50"
                            }`}
                          >
                            {isAction ? (
                              <span className={`text-base leading-none flex-shrink-0 ${isActive ? "text-indigo-500" : "text-slate-400"}`} aria-hidden="true">
                                ⚡
                              </span>
                            ) : (
                              <IconArrow className={`w-3.5 h-3.5 flex-shrink-0 ${isActive ? "text-indigo-500" : "text-slate-300"}`} />
                            )}
                            <span className="flex-1">{cmd.label}</span>
                            <span className={`text-[11px] font-mono truncate max-w-[140px] ${isActive ? "text-indigo-400" : "text-slate-300"}`}>
                              {cmd.href}
                            </span>
                          </button>
                        </li>
                      );
                    })}
                  </ul>
                </li>
              );
            })
          )}
        </ul>

        <div className="border-t border-slate-100 px-4 py-2 flex items-center gap-4 text-[11px] text-slate-400 select-none">
          <span className="flex items-center gap-1">
            <kbd className="rounded border border-slate-200 bg-slate-50 px-1 py-0.5 font-medium">↑</kbd>
            <kbd className="rounded border border-slate-200 bg-slate-50 px-1 py-0.5 font-medium">↓</kbd>
            naviguer
          </span>
          <span className="flex items-center gap-1">
            <kbd className="rounded border border-slate-200 bg-slate-50 px-1 py-0.5 font-medium">↵</kbd>
            ouvrir
          </span>
          <span className="flex items-center gap-1">
            <kbd className="rounded border border-slate-200 bg-slate-50 px-1 py-0.5 font-medium">ESC</kbd>
            fermer
          </span>
        </div>
      </div>
    </div>
  );
}

// ─── Notification bell dropdown ───────────────────────────────────────────────

function NotificationBell() {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  const unreadAlerts = alerts.filter((a) => !a.isRead);
  const unreadCount = unreadAlerts.length;
  const recentUnread = unreadAlerts.slice(0, 4);

  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={() => setOpen((o) => !o)}
        className="relative p-2 text-slate-500 hover:text-slate-800 transition-colors rounded-lg hover:bg-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-1"
        aria-label={`Alertes — ${unreadCount} non lues`}
        aria-haspopup="true"
        aria-expanded={open}
      >
        <IconBell className="w-5 h-5" />
        {unreadCount > 0 && (
          <span className="absolute top-1 right-1 w-4 h-4 bg-red-500 text-white text-[9px] font-bold rounded-full flex items-center justify-center leading-none">
            {unreadCount > 9 ? "9+" : unreadCount}
          </span>
        )}
      </button>

      {/* Dropdown */}
      <div
        className={`absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-xl border border-slate-200 z-50 overflow-hidden transition-all duration-150 origin-top-right ${
          open ? "opacity-100 scale-100" : "opacity-0 scale-95 pointer-events-none"
        }`}
        aria-hidden={!open}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-slate-100">
          <span className="text-sm font-semibold text-slate-900">Alertes récentes</span>
          {unreadCount > 0 && (
            <button className="text-xs text-indigo-600 hover:text-indigo-800 font-medium transition-colors">
              Tout marquer lu
            </button>
          )}
        </div>

        {/* Alert list */}
        <div className="divide-y divide-slate-50">
          {recentUnread.length === 0 ? (
            <div className="px-4 py-8 text-center text-sm text-slate-400">
              Aucune nouvelle alerte
            </div>
          ) : (
            recentUnread.map((alert) => {
              const dotColor = ALERT_TYPE_COLOR[alert.type] ?? "bg-slate-400";
              const truncated = alert.message.length > 60
                ? alert.message.slice(0, 60) + "…"
                : alert.message;
              return (
                <div key={alert.id} className="flex items-start gap-3 px-4 py-3 hover:bg-slate-50 transition-colors">
                  <span className={`mt-1 w-2 h-2 rounded-full flex-shrink-0 ${dotColor}`} aria-hidden="true" />
                  <div className="min-w-0 flex-1">
                    <p className="text-xs text-slate-800 leading-snug">{truncated}</p>
                    <p className="mt-0.5 text-[11px] text-slate-400">
                      {alert.competitorName} · {alert.date}
                    </p>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Footer */}
        <div className="border-t border-slate-100 px-4 py-2.5">
          <Link
            href="/dashboard/alerts"
            onClick={() => setOpen(false)}
            className="text-xs font-medium text-indigo-600 hover:text-indigo-800 transition-colors"
          >
            Voir toutes les alertes →
          </Link>
        </div>
      </div>
    </div>
  );
}

// ─── User avatar dropdown ─────────────────────────────────────────────────────

function UserDropdown() {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  const handleLogout = async () => {
    setOpen(false);
    await fetch("/api/auth/logout", { method: "POST" });
    window.location.href = "/login";
  };

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex items-center gap-1.5 rounded-full focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-1"
        aria-haspopup="true"
        aria-expanded={open}
        aria-label="Menu utilisateur"
      >
        <div className="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center text-white text-xs font-bold flex-shrink-0 select-none">
          CM
        </div>
        <IconChevronDown className="w-3.5 h-3.5 text-slate-500 hidden sm:block" />
      </button>

      {/* Dropdown */}
      <div
        className={`absolute right-0 mt-2 w-52 bg-white rounded-xl shadow-xl border border-slate-200 z-50 overflow-hidden transition-all duration-150 origin-top-right ${
          open ? "opacity-100 scale-100" : "opacity-0 scale-95 pointer-events-none"
        }`}
        aria-hidden={!open}
      >
        {/* User info header */}
        <div className="px-4 py-3 border-b border-slate-100">
          <p className="text-sm font-semibold text-slate-900">Chaima Mhadbi</p>
          <p className="text-xs text-slate-500">Administrateur</p>
        </div>

        {/* Menu items */}
        <div className="py-1">
          <Link
            href="/dashboard/settings"
            onClick={() => setOpen(false)}
            className="flex items-center gap-2.5 px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 transition-colors"
          >
            <IconSettings className="w-4 h-4 text-slate-400" />
            Paramètres
          </Link>
          <Link
            href="#"
            onClick={() => setOpen(false)}
            className="flex items-center gap-2.5 px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 transition-colors"
          >
            <IconDoc className="w-4 h-4 text-slate-400" />
            Documentation
          </Link>
        </div>

        <div className="border-t border-slate-100" />

        <div className="py-1">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-2.5 px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
          >
            <IconLogout className="w-4 h-4" />
            Déconnexion
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── Helper ───────────────────────────────────────────────────────────────────

function isInputFocused(): boolean {
  const el = document.activeElement;
  if (!el) return false;
  const tag = el.tagName.toLowerCase();
  return tag === "input" || tag === "textarea" || (el as HTMLElement).isContentEditable;
}

// ─── Topbar ───────────────────────────────────────────────────────────────────

export default function Topbar() {
  const pathname = usePathname();
  const router = useRouter();
  const [searchOpen, setSearchOpen] = useState(false);

  // Build breadcrumb trail from pathname segments
  const segments = pathname.split("/").filter(Boolean);
  const crumbs: { label: string; href: string }[] = [];
  let path = "";
  for (const seg of segments) {
    path += "/" + seg;
    const label = SEGMENT_LABELS[seg] ?? seg;
    crumbs.push({ label, href: path });
  }

  // Global keyboard shortcuts
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      const meta = e.metaKey || e.ctrlKey;

      if (meta && (e.key === "k" || e.key === "/")) {
        e.preventDefault();
        setSearchOpen(true);
        return;
      }

      if (isInputFocused()) return;

      if (meta && e.key === "1") { e.preventDefault(); router.push("/dashboard"); return; }
      if (meta && e.key === "2") { e.preventDefault(); router.push("/dashboard/competitors"); return; }
      if (meta && e.key === "3") { e.preventDefault(); router.push("/dashboard/alerts"); return; }
      if (meta && e.key === "4") { e.preventDefault(); router.push("/dashboard/reports"); return; }
    };

    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, [router]);

  return (
    <>
      <header data-topbar="" className="h-14 bg-white border-b border-slate-200 flex items-center justify-between px-4 md:px-6 gap-4">

        {/* ── Breadcrumb ── */}
        <nav className="flex items-center gap-0 text-sm ml-12 md:ml-0 min-w-0" aria-label="Fil d'Ariane">
          {crumbs.map((c, i) => (
            <span key={c.href} className="flex items-center min-w-0">
              {i > 0 && (
                <span className="mx-1.5 text-slate-400 select-none" aria-hidden="true">
                  /
                </span>
              )}
              {i === crumbs.length - 1 ? (
                <span className="font-medium text-slate-900 truncate">{c.label}</span>
              ) : i === 0 ? (
                <Link
                  href="/dashboard"
                  className="text-slate-500 hover:text-slate-800 transition-colors truncate"
                >
                  {c.label}
                </Link>
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

          {/* Search button — desktop */}
          <button
            onClick={() => setSearchOpen(true)}
            className="hidden sm:flex items-center gap-2 rounded-lg border border-slate-200 bg-slate-50 px-3 py-1.5 text-sm text-slate-500 hover:border-slate-300 hover:bg-white transition-colors"
            aria-label="Ouvrir la palette de commandes"
          >
            <IconSearch className="w-4 h-4" />
            <span className="hidden md:inline text-slate-400">Rechercher...</span>
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

          {/* Live status pill */}
          <span className="hidden sm:flex text-xs bg-emerald-50 text-emerald-700 px-2.5 py-1 rounded-full font-medium items-center gap-1.5 select-none border border-emerald-100">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" aria-hidden="true" />
            Système opérationnel
          </span>

          {/* Live indicator */}
          <div className="hidden md:block">
            <LiveIndicator />
          </div>

          {/* Notification bell with dropdown */}
          <NotificationBell />

          {/* User avatar + dropdown */}
          <UserDropdown />
        </div>
      </header>

      {/* Command palette modal */}
      {searchOpen && <CommandPalette onClose={() => setSearchOpen(false)} />}
    </>
  );
}
