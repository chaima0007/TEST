"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

// Bannière multilingue d'accueil — fait défiler le slogan « Le droit accessible pour tous »
// traduit dans de nombreuses langues. Objectif : qu'une personne migrante reconnaisse
// immédiatement sa langue et comprenne que le site lui est accessible.
// Honnête : c'est bien le slogan qui est réellement traduit (pas une promesse de tout traduire).
// Cliquable (prop href) → mène à la page d'accueil multilingue d'orientation.

type Theme = "indigo" | "blue";

// Slogan traduit. dir: "rtl" pour les langues écrites de droite à gauche.
// cta: appel à l'action court, traduit, affiché à droite quand la bannière est cliquable.
const PHRASES: { code: string; label: string; text: string; cta: string; dir?: "rtl" }[] = [
  { code: "FR", label: "Français", text: "Le droit accessible pour tous", cta: "Bienvenue" },
  { code: "NL", label: "Nederlands", text: "Recht toegankelijk voor iedereen", cta: "Welkom" },
  { code: "EN", label: "English", text: "The law, accessible to everyone", cta: "Welcome" },
  { code: "AR", label: "العربية", text: "القانون في متناول الجميع", cta: "مرحبا", dir: "rtl" },
  { code: "ES", label: "Español", text: "El derecho accesible para todos", cta: "Bienvenido" },
  { code: "PT", label: "Português", text: "O direito acessível a todos", cta: "Bem-vindo" },
  { code: "TR", label: "Türkçe", text: "Herkes için erişilebilir hukuk", cta: "Hoş geldiniz" },
  { code: "RO", label: "Română", text: "Dreptul accesibil pentru toți", cta: "Bun venit" },
  { code: "DE", label: "Deutsch", text: "Recht für alle zugänglich", cta: "Willkommen" },
  { code: "IT", label: "Italiano", text: "Il diritto accessibile a tutti", cta: "Benvenuto" },
  { code: "PL", label: "Polski", text: "Prawo dostępne dla wszystkich", cta: "Witamy" },
  { code: "UK", label: "Українська", text: "Право, доступне кожному", cta: "Ласкаво просимо" },
  { code: "RU", label: "Русский", text: "Право, доступное каждому", cta: "Добро пожаловать" },
  { code: "FA", label: "فارسی", text: "قانون در دسترس همه", cta: "خوش آمدید", dir: "rtl" },
];

const THEMES: Record<Theme, { bar: string; hover: string }> = {
  indigo: {
    bar: "bg-indigo-950/95 text-indigo-50 border-indigo-800/50",
    hover: "hover:bg-indigo-900/95",
  },
  blue: {
    bar: "bg-blue-950/95 text-blue-50 border-blue-900/50",
    hover: "hover:bg-blue-900/95",
  },
};

export default function BanniereLangues({
  theme = "indigo",
  href,
}: {
  theme?: Theme;
  href?: string;
}) {
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
  const t = THEMES[theme];

  const inner = (
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

      {/* Appel à l'action traduit (uniquement si la bannière est cliquable) */}
      {href && (
        <span
          className="hidden sm:inline-flex items-center gap-1 flex-shrink-0 rounded-full bg-white/10 px-2.5 py-0.5 text-xs font-semibold transition-opacity duration-300 ease-in-out"
          style={{ opacity: visible ? 1 : 0 }}
        >
          {p.cta} <span aria-hidden="true">→</span>
        </span>
      )}

      {/* Texte fixe lisible par lecteur d'écran (le défilement est décoratif) */}
      <span className="sr-only">
        Le droit accessible pour tous — informations disponibles en langage clair.
        {href ? " Ouvrir la page d’accueil multilingue." : ""}
      </span>
    </div>
  );

  if (href) {
    return (
      <Link
        href={href}
        aria-label="Bienvenue — page d’accueil multilingue"
        className={`block w-full border-b transition-colors ${t.bar} ${t.hover}`}
      >
        {inner}
      </Link>
    );
  }

  return <div className={`w-full border-b ${t.bar}`}>{inner}</div>;
}
