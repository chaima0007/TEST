"use client";

import { useEffect, useRef, useState } from "react";

// Lecture audio d'une fiche (accessibilité radicale : âgés, malvoyants, difficultés de lecture,
// allophones lisant mal le français). Utilise la synthèse vocale native du navigateur
// (window.speechSynthesis) — aucune dépendance, aucune donnée envoyée à un tiers.

export default function EcouterFiche({ texte }: { texte: string }) {
  const [supporte, setSupporte] = useState(false);
  const [etat, setEtat] = useState<"arret" | "lecture" | "pause">("arret");
  const ref = useRef<SpeechSynthesisUtterance | null>(null);

  useEffect(() => {
    setSupporte(typeof window !== "undefined" && "speechSynthesis" in window);
    return () => { try { window.speechSynthesis?.cancel(); } catch {} };
  }, []);

  function lire() {
    if (!supporte) return;
    const synth = window.speechSynthesis;
    if (etat === "pause") { synth.resume(); setEtat("lecture"); return; }
    synth.cancel();
    const u = new SpeechSynthesisUtterance(texte);
    u.lang = "fr-BE"; u.rate = 1;
    u.onend = () => setEtat("arret");
    ref.current = u;
    synth.speak(u);
    setEtat("lecture");
  }
  function pause() { if (supporte) { window.speechSynthesis.pause(); setEtat("pause"); } }
  function stop() { if (supporte) { window.speechSynthesis.cancel(); setEtat("arret"); } }

  if (!supporte) return null;

  return (
    <div className="mt-4 inline-flex items-center gap-2">
      {etat !== "lecture" ? (
        <button
          type="button" onClick={lire}
          className="inline-flex items-center gap-2 rounded-lg bg-white/10 border border-white/25 px-4 py-2 text-sm font-semibold text-white hover:bg-white/20 transition-colors"
        >
          🔊 {etat === "pause" ? "Reprendre" : "Écouter cette fiche"}
        </button>
      ) : (
        <button
          type="button" onClick={pause}
          className="inline-flex items-center gap-2 rounded-lg bg-white/10 border border-white/25 px-4 py-2 text-sm font-semibold text-white hover:bg-white/20 transition-colors"
        >
          ⏸ Pause
        </button>
      )}
      {etat !== "arret" && (
        <button
          type="button" onClick={stop}
          className="inline-flex items-center gap-2 rounded-lg bg-white/10 border border-white/25 px-3 py-2 text-sm font-semibold text-white hover:bg-white/20 transition-colors"
        >
          ⏹ Stop
        </button>
      )}
    </div>
  );
}
