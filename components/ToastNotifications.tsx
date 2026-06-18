"use client";

import {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
  useRef,
  ReactNode,
} from "react";
import Link from "next/link";

// ─── Types ────────────────────────────────────────────────────────────────────

type ToastType = "alert" | "insight" | "success" | "warning";

interface ToastItem {
  id: number;
  type: ToastType;
  title: string;
  message: string;
  href?: string;
  /** timestamp when the toast was added, used for progress bar */
  addedAt: number;
}

interface ToastContextValue {
  addToast: (opts: Omit<ToastItem, "id" | "addedAt">) => void;
}

// ─── Live events pool ─────────────────────────────────────────────────────────

const LIVE_EVENTS: Omit<ToastItem, "id" | "addedAt">[] = [
  {
    type: "alert",
    title: "Mouvement détecté — HubSpot",
    message: "HubSpot vient de modifier ses plans tarifaires",
    href: "/dashboard/pricing",
  },
  {
    type: "insight",
    title: "Signal faible — Salesforce",
    message: "23 nouvelles offres d'emploi NLP en 48h",
    href: "/dashboard/signals",
  },
  {
    type: "warning",
    title: "Risque client détecté",
    message: "Groupe Moreau SA — Score de risque passé à 87/100",
    href: "/dashboard/radar",
  },
  {
    type: "alert",
    title: "Acquisition confirmée",
    message: "Salesforce acquiert Spiff pour 419M$",
    href: "/dashboard/alerts",
  },
  {
    type: "insight",
    title: "Opportunité pricing",
    message: "Pipedrive a baissé ses prix de 15% — moment idéal",
    href: "/dashboard/pricing",
  },
  {
    type: "success",
    title: "Rapport généré",
    message: "Votre rapport exécutif mensuel est prêt",
    href: "/dashboard/reports",
  },
];

const DURATION_MS = 6000; // auto-dismiss after 6 s
const MAX_TOASTS = 3;

// ─── Context ──────────────────────────────────────────────────────────────────

const ToastNotificationsContext = createContext<ToastContextValue>({
  addToast: () => {},
});

// ─── Provider ─────────────────────────────────────────────────────────────────

export function ToastNotificationsProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<ToastItem[]>([]);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const addToast = useCallback((opts: Omit<ToastItem, "id" | "addedAt">) => {
    const item: ToastItem = { ...opts, id: Date.now(), addedAt: Date.now() };
    setToasts((prev) => {
      const next = [...prev, item];
      // Keep at most MAX_TOASTS, dropping the oldest ones
      return next.length > MAX_TOASTS ? next.slice(next.length - MAX_TOASTS) : next;
    });
    // Schedule auto-dismiss
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== item.id));
    }, DURATION_MS + 300); // +300 ms for slide-out animation
  }, []);

  const removeToast = useCallback((id: number) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  // ── Simulation: first toast after 8 s, then every 45–90 s ──────────────────
  useEffect(() => {
    let cancelled = false;

    const fireRandom = () => {
      if (cancelled) return;
      const event = LIVE_EVENTS[Math.floor(Math.random() * LIVE_EVENTS.length)];
      addToast(event);
      // Schedule next: 45 000 – 90 000 ms
      const delay = 45_000 + Math.random() * 45_000;
      timerRef.current = setTimeout(fireRandom, delay);
    };

    timerRef.current = setTimeout(fireRandom, 8_000);

    return () => {
      cancelled = true;
      if (timerRef.current !== null) clearTimeout(timerRef.current);
    };
  }, [addToast]);

  return (
    <ToastNotificationsContext.Provider value={{ addToast }}>
      {children}
      <ToastStack toasts={toasts} onRemove={removeToast} />
    </ToastNotificationsContext.Provider>
  );
}

// ─── Hook ─────────────────────────────────────────────────────────────────────

export function useToastNotifications(): ToastContextValue {
  return useContext(ToastNotificationsContext);
}

// Keep a short alias matching the spec
export function useToast(): ToastContextValue {
  return useToastNotifications();
}

// ─── Styles injected once ─────────────────────────────────────────────────────

const KEYFRAMES = `
@keyframes tn-slide-in {
  from { opacity: 0; transform: translateX(calc(100% + 1.5rem)); }
  to   { opacity: 1; transform: translateX(0); }
}
@keyframes tn-slide-out {
  from { opacity: 1; transform: translateX(0); }
  to   { opacity: 0; transform: translateX(calc(100% + 1.5rem)); }
}
@keyframes tn-progress {
  from { width: 100%; }
  to   { width: 0%; }
}
`;

// ─── Per-type config ──────────────────────────────────────────────────────────

interface TypeConfig {
  bg: string;
  border: string;
  bar: string;
  icon: React.ReactNode;
  label: string;
}

function AlertIcon() {
  return (
    <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
      <path
        fillRule="evenodd"
        d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495zM10 5a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 5zm0 9a1 1 0 100-2 1 1 0 000 2z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function InsightIcon() {
  return (
    <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
      <path d="M10 1a6 6 0 00-3.815 10.631C7.237 12.5 8 13.443 8 14.456v.044a1 1 0 001 1h2a1 1 0 001-1v-.044c0-1.013.762-1.957 1.815-2.825A6 6 0 0010 1zM8.5 17.5a.5.5 0 000 1h3a.5.5 0 000-1h-3z" />
    </svg>
  );
}

function SuccessIcon() {
  return (
    <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
      <path
        fillRule="evenodd"
        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function WarningIcon() {
  return (
    <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
      <path
        fillRule="evenodd"
        d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-5a.75.75 0 01.75.75v4.5a.75.75 0 01-1.5 0v-4.5A.75.75 0 0110 5zm0 10a1 1 0 100-2 1 1 0 000 2z"
        clipRule="evenodd"
      />
    </svg>
  );
}

const TYPE_CONFIG: Record<ToastType, TypeConfig> = {
  alert: {
    bg: "bg-rose-950",
    border: "border-rose-700",
    bar: "bg-rose-400",
    icon: <AlertIcon />,
    label: "Alerte",
  },
  insight: {
    bg: "bg-indigo-950",
    border: "border-indigo-600",
    bar: "bg-indigo-400",
    icon: <InsightIcon />,
    label: "Insight",
  },
  success: {
    bg: "bg-emerald-950",
    border: "border-emerald-600",
    bar: "bg-emerald-400",
    icon: <SuccessIcon />,
    label: "Succès",
  },
  warning: {
    bg: "bg-amber-950",
    border: "border-amber-600",
    bar: "bg-amber-400",
    icon: <WarningIcon />,
    label: "Alerte",
  },
};

// ─── Single Toast ─────────────────────────────────────────────────────────────

interface SingleToastProps {
  toast: ToastItem;
  onRemove: (id: number) => void;
}

function SingleToast({ toast, onRemove }: SingleToastProps) {
  const [leaving, setLeaving] = useState(false);
  const cfg = TYPE_CONFIG[toast.type];

  const handleDismiss = () => {
    setLeaving(true);
    setTimeout(() => onRemove(toast.id), 280);
  };

  // Trigger leave animation just before the auto-dismiss timer fires
  useEffect(() => {
    const t = setTimeout(() => setLeaving(true), DURATION_MS - 280);
    return () => clearTimeout(t);
  }, []);

  return (
    <div
      className={`relative flex flex-col gap-1.5 w-80 rounded-xl border px-4 pt-3 pb-2 shadow-2xl text-white overflow-hidden ${cfg.bg} ${cfg.border}`}
      style={{
        animation: leaving
          ? "tn-slide-out 0.28s ease-in forwards"
          : "tn-slide-in 0.32s cubic-bezier(0.34,1.56,0.64,1) forwards",
      }}
    >
      {/* Header row */}
      <div className="flex items-start gap-2.5">
        {/* Icon badge */}
        <span className="mt-0.5 flex-shrink-0 opacity-90">{cfg.icon}</span>

        {/* Text */}
        <div className="flex-1 min-w-0">
          <p className="text-xs font-semibold uppercase tracking-wide opacity-60 leading-none mb-0.5">
            {cfg.label}
          </p>
          <p className="text-sm font-semibold leading-snug">{toast.title}</p>
          <p className="text-xs opacity-75 leading-snug mt-0.5 line-clamp-2">{toast.message}</p>
        </div>

        {/* Close button */}
        <button
          onClick={handleDismiss}
          aria-label="Fermer la notification"
          className="flex-shrink-0 -mt-0.5 -mr-1 w-6 h-6 rounded-md flex items-center justify-center opacity-50 hover:opacity-100 hover:bg-white/10 transition-opacity"
        >
          <svg viewBox="0 0 16 16" fill="currentColor" className="w-3.5 h-3.5">
            <path d="M3.72 3.72a.75.75 0 011.06 0L8 6.94l3.22-3.22a.75.75 0 111.06 1.06L9.06 8l3.22 3.22a.75.75 0 11-1.06 1.06L8 9.06l-3.22 3.22a.75.75 0 01-1.06-1.06L6.94 8 3.72 4.78a.75.75 0 010-1.06z" />
          </svg>
        </button>
      </div>

      {/* "Voir" button */}
      {toast.href && (
        <div className="flex justify-end mt-0.5">
          <Link
            href={toast.href}
            onClick={handleDismiss}
            className="text-xs font-medium px-2.5 py-1 rounded-md bg-white/10 hover:bg-white/20 transition-colors"
          >
            Voir →
          </Link>
        </div>
      )}

      {/* Progress bar */}
      <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-white/10 overflow-hidden">
        <div
          className={`h-full ${cfg.bar}`}
          style={{
            animation: `tn-progress ${DURATION_MS}ms linear forwards`,
          }}
        />
      </div>
    </div>
  );
}

// ─── Stack ────────────────────────────────────────────────────────────────────

interface ToastStackProps {
  toasts: ToastItem[];
  onRemove: (id: number) => void;
}

function ToastStack({ toasts, onRemove }: ToastStackProps) {
  if (toasts.length === 0) return null;

  return (
    <>
      <style>{KEYFRAMES}</style>
      <div
        role="region"
        aria-live="polite"
        aria-label="Notifications"
        className="fixed bottom-6 left-6 z-40 flex flex-col gap-2.5 items-start pointer-events-none"
      >
        {toasts.map((t) => (
          <div key={t.id} className="pointer-events-auto">
            <SingleToast toast={t} onRemove={onRemove} />
          </div>
        ))}
      </div>
    </>
  );
}

// ─── Default export (the standalone component for simple usage) ───────────────

/**
 * Drop-in component: renders the toast stack *and* sets up the simulation.
 * Use `ToastNotificationsProvider` + `useToast()` for programmatic access.
 */
export default function ToastNotifications() {
  // This component is intended to be used *inside* a ToastNotificationsProvider.
  // When rendered directly it simply renders nothing (stack is owned by provider).
  return null;
}
