"use client";

import { useState } from "react";

/**
 * ReadAloud — bouton de lecture à voix haute (gratuit, via le navigateur).
 * Pensé pour les personnes qui ne savent pas lire ou qui ont besoin d'être
 * rassurées : voix posée (débit ralenti), en français par défaut.
 * Utilise l'API Web Speech (SpeechSynthesis) — aucun coût, aucune donnée envoyée.
 */
export default function ReadAloud({ text, label = "Écouter", lang = "fr-BE" }: { text: string; label?: string; lang?: string }) {
  const [speaking, setSpeaking] = useState(false);

  const supported = typeof window !== "undefined" && "speechSynthesis" in window;

  function stop() {
    if (!supported) return;
    window.speechSynthesis.cancel();
    setSpeaking(false);
  }

  function speak() {
    if (!supported) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = lang;
    u.rate = 0.92;   // débit légèrement ralenti = plus rassurant et clair
    u.pitch = 1.0;
    u.onend = () => setSpeaking(false);
    u.onerror = () => setSpeaking(false);
    setSpeaking(true);
    window.speechSynthesis.speak(u);
  }

  if (!supported) return null;

  return (
    <button
      type="button"
      onClick={speaking ? stop : speak}
      aria-label={speaking ? "Arrêter la lecture" : "Lire à voix haute"}
      className="inline-flex items-center gap-2 text-sm font-medium text-indigo-700 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 rounded-full px-4 py-2 transition-colors"
    >
      {speaking ? (
        <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4"><rect x="6" y="5" width="4" height="14" rx="1" /><rect x="14" y="5" width="4" height="14" rx="1" /></svg>
      ) : (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8} className="w-4 h-4"><path d="M11 5L6 9H3v6h3l5 4V5z" strokeLinejoin="round" /><path d="M15.5 8.5a5 5 0 010 7" strokeLinecap="round" /></svg>
      )}
      {speaking ? "Arrêter" : label}
    </button>
  );
}
