"use client";

import Link from "next/link";
import { useState } from "react";

/**
 * En-tête commun. Le bouton "Gros texte" bascule un attribut sur <html> pour
 * agrandir toute l’interface (accessibilité). Aucune donnée personnelle : c’est
 * une préférence d’affichage, gardée en mémoire le temps de la visite.
 */
export default function BulleHeader({ home = "/bulle" }: { home?: string }) {
  const [large, setLarge] = useState(false);

  function toggle() {
    const next = !large;
    setLarge(next);
    if (typeof document !== "undefined") {
      document.documentElement.dataset.bulleLarge = String(next);
    }
  }

  return (
    <header className="mb-6 flex items-center justify-between gap-3">
      <Link href={home} className="tap px-4" style={{ background: "#fff", borderColor: "#e6e1d6" }}>
        <span aria-hidden>🏠</span> Accueil
      </Link>
      <button
        type="button"
        onClick={toggle}
        aria-pressed={large}
        className="tap px-4 text-sm"
        style={{ background: large ? "var(--b-primary)" : "#fff", color: large ? "#fff" : "var(--b-ink)", borderColor: "#e6e1d6" }}
      >
        <span aria-hidden>🔎</span> Gros texte
      </button>
    </header>
  );
}
