"use client";

import { useEffect, useState } from "react";

export function LiveIndicator({ label = "En direct" }: { label?: string }) {
  const [minutesAgo, setMinutesAgo] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setMinutesAgo((prev) => prev + 1);
    }, 60_000);
    return () => clearInterval(interval);
  }, []);

  function handleClick() {
    setMinutesAgo(0);
  }

  const refreshLabel =
    minutesAgo === 0
      ? "Actualisé à l'instant"
      : minutesAgo === 1
      ? "Actualisé il y a 1 min"
      : `Actualisé il y a ${minutesAgo} min`;

  return (
    <button
      onClick={handleClick}
      title="Cliquer pour actualiser"
      className="inline-flex items-center gap-2 rounded-full px-2.5 py-1 text-[11px] font-medium text-emerald-700 bg-emerald-50 border border-emerald-200 hover:bg-emerald-100 transition-colors select-none cursor-pointer"
    >
      <span className="relative flex h-2 w-2 flex-shrink-0">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
        <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
      </span>
      <span className="hidden sm:inline">{label} · </span>
      <span>{refreshLabel}</span>
    </button>
  );
}
