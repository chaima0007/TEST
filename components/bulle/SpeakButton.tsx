"use client";

import { useState } from "react";

/**
 * Lecture à voix haute — 100 % sur l’appareil (Web Speech API du navigateur).
 * Aucune requête réseau, aucune donnée envoyée. Utile aux enfants pré-lecteurs
 * et à l’accessibilité. Se dégrade en silence si l’API n’est pas disponible.
 */
export default function SpeakButton({
  text,
  label = "Écouter",
  className = "",
}: {
  text: string;
  label?: string;
  className?: string;
}) {
  const [speaking, setSpeaking] = useState(false);

  function speak() {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) return;
    const synth = window.speechSynthesis;
    synth.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = "fr-FR";
    u.rate = 0.95;
    u.onend = () => setSpeaking(false);
    u.onerror = () => setSpeaking(false);
    setSpeaking(true);
    synth.speak(u);
  }

  return (
    <button
      type="button"
      onClick={speak}
      aria-label={`${label} : ${text}`}
      className={`tap px-4 text-sm ${className}`}
      style={{ background: "#efeafe", color: "#4b3fb0" }}
    >
      <span aria-hidden>{speaking ? "🔊" : "🔈"}</span>
      {label}
    </button>
  );
}
