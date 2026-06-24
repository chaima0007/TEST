"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

// Bouton flottant « SOS » — version FRANCE, pensé mobile d'abord.
// Numéros d'urgence officiels français (tel: lance l'appel sur mobile).
// Placé en bas à GAUCHE pour ne pas chevaucher d'autres widgets.
export default function SosFloatingButtonFR() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <div className="fixed bottom-5 left-5 z-40">
      {open && (
        <div className="mb-3 w-64 bg-white rounded-2xl shadow-2xl border border-slate-200 overflow-hidden">
          <div className="bg-rose-600 text-white px-4 py-3">
            <p className="font-bold text-sm">En cas d&apos;urgence</p>
            <p className="text-rose-100 text-xs mt-0.5">Numéros officiels français</p>
          </div>
          <div className="p-2.5 space-y-2">
            <a
              href="tel:112"
              className="flex items-center gap-3 rounded-xl bg-rose-50 hover:bg-rose-100 border border-rose-200 px-3 py-2.5 transition-colors"
            >
              <span className="flex-shrink-0 w-9 h-9 rounded-full bg-rose-600 text-white flex items-center justify-center font-black text-sm">112</span>
              <span className="text-left">
                <span className="block text-sm font-semibold text-slate-900">Urgence (UE)</span>
                <span className="block text-xs text-slate-500">Tous secours</span>
              </span>
            </a>
            <a
              href="tel:17"
              className="flex items-center gap-3 rounded-xl bg-blue-50 hover:bg-blue-100 border border-blue-200 px-3 py-2.5 transition-colors"
            >
              <span className="flex-shrink-0 w-9 h-9 rounded-full bg-blue-700 text-white flex items-center justify-center font-black text-sm">17</span>
              <span className="text-left">
                <span className="block text-sm font-semibold text-slate-900">Police / Gendarmerie</span>
                <span className="block text-xs text-slate-500">Secours police (France)</span>
              </span>
            </a>
            {pathname !== "/la-loi-avec-moi-france/en-danger" && (
              <Link
                href="/la-loi-avec-moi-france/en-danger"
                onClick={() => setOpen(false)}
                className="flex items-center gap-3 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 px-3 py-2.5 transition-colors"
              >
                <span className="flex-shrink-0 w-9 h-9 rounded-full bg-slate-700 text-white flex items-center justify-center">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4"><path d="M12 3l7 4v5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V7l7-4z" strokeLinecap="round" strokeLinejoin="round" /></svg>
                </span>
                <span className="text-left">
                  <span className="block text-sm font-semibold text-slate-900">En danger ?</span>
                  <span className="block text-xs text-slate-500">Tous les numéros d&apos;aide</span>
                </span>
              </Link>
            )}
          </div>
          <p className="px-4 pb-3 text-[11px] leading-snug text-slate-400">
            Raccourci vers les numéros officiels. En cas de danger, appelez le 112.
          </p>
        </div>
      )}

      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-label={open ? "Fermer le menu d'urgence" : "Ouvrir le menu d'urgence SOS"}
        aria-expanded={open}
        className="flex items-center gap-2 bg-rose-600 hover:bg-rose-700 active:scale-95 text-white font-bold rounded-full shadow-lg shadow-rose-600/40 pl-3.5 pr-4 py-3 transition-all"
      >
        {open ? (
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.5} className="w-5 h-5"><path d="M6 6l12 12M18 6L6 18" strokeLinecap="round" /></svg>
        ) : (
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-5 h-5"><path d="M12 3l7 4v5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V7l7-4z" strokeLinecap="round" strokeLinejoin="round" /><path d="M9 12l2 2 4-4" strokeLinecap="round" strokeLinejoin="round" /></svg>
        )}
        <span className="text-sm whitespace-nowrap">{open ? "Fermer" : "SOS"}</span>
      </button>
    </div>
  );
}
