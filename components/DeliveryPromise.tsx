// Bandeau de réassurance réutilisable (dashboard, app, page de suivi).
// Matérialise la promesse « transparence logistique » de la boutique
// (docs/ARCHITECTURE_BOUTIQUE.md §2). Composant purement présentiel, sans état.

interface DeliveryPromiseItem {
  label: string;
  icon: React.ReactNode;
}

const items: DeliveryPromiseItem[] = [
  {
    label: "Expédié d'Europe",
    icon: (
      <path d="M3 7l9-4 9 4v10l-9 4-9-4V7z M3 7l9 4 9-4M12 21V11" />
    ),
  },
  {
    label: "Livré en 2-4 jours",
    icon: (
      <path d="M12 7v5l3 2M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    ),
  },
  {
    label: "Suivi en temps réel",
    icon: (
      <path d="M12 2v3M12 19v3M2 12h3M19 12h3M12 8a4 4 0 100 8 4 4 0 000-8z" />
    ),
  },
  {
    label: "Retours 30 jours",
    icon: (
      <path d="M3 12a9 9 0 019-9 9 9 0 016.7 3M21 3v5h-5M21 12a9 9 0 01-9 9 9 9 0 01-6.7-3M3 21v-5h5" />
    ),
  },
];

export function DeliveryPromise({ className = "" }: { className?: string }) {
  return (
    <div
      className={`rounded-2xl border border-slate-200 bg-white p-4 shadow-sm ${className}`}
      role="list"
      aria-label="Nos engagements livraison"
    >
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        {items.map((item) => (
          <div key={item.label} role="listitem" className="flex flex-col items-center gap-2 text-center">
            <span className="flex h-9 w-9 items-center justify-center rounded-full bg-indigo-50 text-indigo-600">
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                {item.icon}
              </svg>
            </span>
            <span className="text-xs font-medium leading-tight text-slate-600">{item.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DeliveryPromise;
