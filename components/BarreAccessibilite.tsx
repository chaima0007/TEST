"use client";

import { useEffect, useState } from "react";

// Barre d'accessibilité universelle — « facilités sur l'interface ».
// - Traduction de la page dans N'IMPORTE QUELLE langue (traduction automatique, clairement signalée).
//   On ne publie PAS de traduction juridique non vérifiée : c'est l'utilisateur qui déclenche la
//   traduction automatique de la page en cours (honnête et sûr pour du contenu de droit).
// - Taille du texte (A- / A+), contraste élevé. Choix mémorisés (localStorage).
// Aucune dépendance externe ; fonctionne sur tout l'app.

const LANGUES: { code: string; label: string }[] = [
  { code: "nl", label: "Nederlands" },
  { code: "en", label: "English" },
  { code: "ar", label: "العربية" },
  { code: "es", label: "Español" },
  { code: "pt", label: "Português" },
  { code: "tr", label: "Türkçe" },
  { code: "ro", label: "Română" },
  { code: "de", label: "Deutsch" },
  { code: "it", label: "Italiano" },
  { code: "pl", label: "Polski" },
  { code: "uk", label: "Українська" },
  { code: "ru", label: "Русский" },
  { code: "fa", label: "فارسی" },
  { code: "fr", label: "Français" },
];

function traduire(code: string) {
  if (typeof window === "undefined") return;
  const url = `https://translate.google.com/translate?sl=auto&tl=${code}&u=${encodeURIComponent(window.location.href)}`;
  window.open(url, "_blank", "noopener,noreferrer");
}

export default function BarreAccessibilite() {
  const [ouvert, setOuvert] = useState(false);
  const [taille, setTaille] = useState(100); // pourcentage
  const [contraste, setContraste] = useState(false);

  // Restaure les préférences
  useEffect(() => {
    try {
      const t = Number(localStorage.getItem("a11y_taille"));
      if (t >= 90 && t <= 160) setTaille(t);
      setContraste(localStorage.getItem("a11y_contraste") === "1");
    } catch {}
  }, []);

  // Applique taille de texte
  useEffect(() => {
    document.documentElement.style.fontSize = `${taille}%`;
    try { localStorage.setItem("a11y_taille", String(taille)); } catch {}
  }, [taille]);

  // Applique contraste élevé
  useEffect(() => {
    document.documentElement.classList.toggle("a11y-contraste", contraste);
    try { localStorage.setItem("a11y_contraste", contraste ? "1" : "0"); } catch {}
  }, [contraste]);

  return (
    <>
      {/* Styles du mode contraste élevé */}
      <style>{`
        .a11y-contraste, .a11y-contraste body { background:#000 !important; color:#fff !important; }
        .a11y-contraste a { color:#ffe600 !important; }
        .a11y-contraste *:not(svg):not(path) { border-color:#fff !important; }
      `}</style>

      {/* Bouton flottant */}
      <button
        type="button"
        onClick={() => setOuvert((v) => !v)}
        aria-expanded={ouvert}
        aria-label="Accessibilité et traduction"
        className="fixed z-50 bottom-4 left-4 w-12 h-12 rounded-full bg-indigo-600 text-white shadow-lg hover:bg-indigo-700 flex items-center justify-center text-xl"
        title="Accessibilité & traduction"
      >
        🌐
      </button>

      {ouvert && (
        <div
          role="dialog"
          aria-label="Outils d'accessibilité"
          className="fixed z-50 bottom-20 left-4 w-72 max-w-[90vw] rounded-2xl border border-slate-200 bg-white shadow-2xl p-4 text-slate-900"
        >
          <div className="flex items-center justify-between mb-3">
            <h2 className="font-bold text-sm">Accessibilité & traduction</h2>
            <button type="button" onClick={() => setOuvert(false)} aria-label="Fermer" className="text-slate-400 hover:text-slate-700">✕</button>
          </div>

          {/* Taille du texte */}
          <div className="mb-3">
            <p className="text-xs font-semibold text-slate-500 mb-1.5">Taille du texte</p>
            <div className="flex items-center gap-2">
              <button type="button" onClick={() => setTaille((t) => Math.max(90, t - 10))} className="flex-1 rounded-lg border border-slate-300 py-1.5 text-sm font-bold hover:bg-slate-50">A−</button>
              <span className="text-xs text-slate-500 w-12 text-center">{taille}%</span>
              <button type="button" onClick={() => setTaille((t) => Math.min(160, t + 10))} className="flex-1 rounded-lg border border-slate-300 py-1.5 text-sm font-bold hover:bg-slate-50">A+</button>
            </div>
          </div>

          {/* Contraste */}
          <div className="mb-3">
            <button
              type="button"
              onClick={() => setContraste((c) => !c)}
              className={"w-full rounded-lg border py-1.5 text-sm font-semibold " + (contraste ? "bg-slate-900 text-white border-slate-900" : "border-slate-300 hover:bg-slate-50")}
            >
              ◐ Contraste élevé {contraste ? "(activé)" : ""}
            </button>
          </div>

          {/* Traduction */}
          <div>
            <p className="text-xs font-semibold text-slate-500 mb-1.5">Traduire cette page</p>
            <div className="grid grid-cols-2 gap-1.5 max-h-44 overflow-auto">
              {LANGUES.map((l) => (
                <button
                  key={l.code}
                  type="button"
                  onClick={() => traduire(l.code)}
                  dir={l.code === "ar" || l.code === "fa" ? "rtl" : "ltr"}
                  className="rounded-lg border border-slate-200 px-2 py-1.5 text-sm hover:border-indigo-400 hover:bg-indigo-50 text-left"
                >
                  {l.label}
                </button>
              ))}
            </div>
            <p className="text-[11px] text-slate-400 mt-2 leading-snug">
              Traduction automatique (Google Translate), ouverte dans un nouvel onglet. Pour le contenu
              juridique vérifié, le français et le néerlandais font foi.
            </p>
          </div>
        </div>
      )}
    </>
  );
}
