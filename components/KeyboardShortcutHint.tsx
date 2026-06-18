"use client";

import { useEffect, useState } from "react";

const STORAGE_KEY = "shortcuts_shown";

export function KeyboardShortcutHint() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (typeof window === "undefined") return;
    if (localStorage.getItem(STORAGE_KEY)) return;

    const showTimer = setTimeout(() => {
      setVisible(true);
    }, 3000);

    return () => clearTimeout(showTimer);
  }, []);

  useEffect(() => {
    if (!visible) return;

    const hideTimer = setTimeout(() => {
      setVisible(false);
      localStorage.setItem(STORAGE_KEY, "1");
    }, 5000);

    return () => clearTimeout(hideTimer);
  }, [visible]);

  if (!visible) return null;

  return (
    <div
      className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 pointer-events-none"
      role="status"
      aria-live="polite"
    >
      <div className="bg-slate-900/90 text-white text-[12px] font-medium px-4 py-2.5 rounded-full shadow-xl backdrop-blur-sm border border-white/10 flex items-center gap-3 whitespace-nowrap">
        <kbd className="font-mono opacity-80">⌘K</kbd>
        <span className="opacity-50">Recherche</span>
        <span className="opacity-30">·</span>
        <kbd className="font-mono opacity-80">⌘1–4</kbd>
        <span className="opacity-50">Navigation</span>
        <span className="opacity-30">·</span>
        <kbd className="font-mono opacity-80">?</kbd>
        <span className="opacity-50">Aide</span>
      </div>
    </div>
  );
}
