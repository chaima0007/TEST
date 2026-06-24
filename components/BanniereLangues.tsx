"use client";

import { useEffect, useState } from "react";

// Bannière multilingue d'accueil — fait défiler le slogan « Le droit accessible pour tous »
// traduit dans de nombreuses langues. Objectif : qu'une personne migrante reconnaisse
// immédiatement sa langue et comprenne que le site lui est accessible.
// Honnête : c'est bien le slogan qui est réellement traduit (pas une promesse de tout traduire).

type Theme = "indigo" | "blue";

// Slogan traduit. dir: "rtl" pour les langues écrites de droite à gauche.
const PHRASES: { code: string; label: string; text: string; dir?: "rtl" }[] = [
  { code: "FR", label: "Français", text: "Le droit accessible pour tous" },
  { code: "NL", label: "Nederlands", text: "Recht toegankelijk voor iedereen" },
  { code: "EN", label: "English", text: "The law, accessible to everyone" },
  { code: "AR", label: "العربية", text: "القانون في متناول الجميع", dir: "rtl" },
  { code: "ES", label: "Español", text: "El derecho accesible para todos" },
  { code: "PT", label: "Português", text: "O direito acessível a todos" },
  { code: "TR", label: "Türkçe", text: "Herkes için erişilebilir hukuk" },
  { code: "RO", label: "Română", text: "Dreptul accesibil pentru toți" },
  { code: "DE", label: "Deutsch", text: "Recht für alle zugänglich" },
  { code: "IT", label: "Italiano", text: "Il diritto accessibile a tutti" },
  { code: "PL", label: "Polski", text: "Prawo dostępne dla wszystkich" },
  { code: "UK", label: "Українська", text: "Право, доступне кожному" },
  { code: "RU", label: "Русский", text: "Право, доступное каждому" },
  { code: "FA", label: "فارسی", text: "قانون در دسترس همه", dir: "rtl" },
];

const THEMES: Record<Theme, string> = {
  indigo: "bg-indigo-950/95 text-indigo-50 border-indigo-800/50",
  blue: "bg-blue-950/95 text-blue-50 border-blue-900/50",
};

export default function BanniereLangues({ theme = "indigo" }: { theme?: Theme }) {
  const [i, setI] = useState(0);
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const fade = setInterval(() => {
      setVisible(false);
      const swap = setTimeout(() => {
        setI((prev) => (prev + 1) % PHRASES.length);
        setVisible(true);
      }, 350);
      return () => clearTimeout(swap);
    }, 2600);
    return () => clearInterval(fade);
  }, []);

  const p = PHRASES[i];

  return (
    <div className={`w-full border-b ${THEMES[theme]}`}>
      <div className="max-w-5xl mx-auto px-4 py-2 flex items-center justify-center gap-3 text-sm">
        {/* Globe */}
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth={1.6}
          className="w-4 h-4 flex-shrink-0 opacity-80"
          aria-hidden="true"
        >
          <circle cx="12" cy="12" r="9" />
          <path d="M3 12h18M12 3c2.5 2.5 2.5 15 0 18M12 3c-2.5 2.5-2.5 15 0 18" strokeLinecap="round" />
        </svg>

        <span
          dir={p.dir ?? "ltr"}
          className="font-medium transition-opacity duration-300 ease-in-out"
          style={{ opacity: visible ? 1 : 0 }}
        >
          <span className="opacity-60 text-xs mr-2 align-middle">{p.label}</span>
          {p.text}
        </span>

        {/* Texte fixe lisible par lecteur d'écran (le défilement est décoratif) */}
        <span className="sr-only">
          Le droit accessible pour tous — informations disponibles en langage clair.
        </span>
      </div>
    </div>
  );
}
