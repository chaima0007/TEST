import type { MetadataRoute } from "next";
import { loadNormes, slugFor } from "./conformite/data";
import { SECTEURS } from "./conformite/secteurs";

// Sitemap Caelum. L'URL de base vient de NEXT_PUBLIC_SITE_URL (à définir au déploiement).
const BASE = process.env.NEXT_PUBLIC_SITE_URL || "https://www.example.com";

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();

  const statiques = [
    "",
    "/en",
    "/conformite",
    "/conformite-2026",
    "/echeances-2026",
    "/calculateur-aide-nette",
    "/offres-conformite",
    "/fiduciaires",
    "/faq",
    "/plateforme-autonome",
    "/veille",
    "/tarifs",
    "/notre-force",
    "/contact",
  ].map((p) => ({
    url: `${BASE}${p}`,
    lastModified: now,
    changeFrequency: "weekly" as const,
    priority: p === "" ? 1 : 0.8,
  }));

  const normes = loadNormes().map((n) => ({
    url: `${BASE}/conformite/${slugFor(n)}`,
    lastModified: now,
    changeFrequency: "monthly" as const,
    priority: 0.7,
  }));

  const secteurs = SECTEURS.map((s) => ({
    url: `${BASE}/conformite/secteur/${s.slug}`,
    lastModified: now,
    changeFrequency: "monthly" as const,
    priority: 0.6,
  }));

  return [...statiques, ...normes, ...secteurs];
}
