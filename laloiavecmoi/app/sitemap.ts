import type { MetadataRoute } from "next";
import fs from "node:fs";
import path from "node:path";

// À adapter avec ton domaine définitif (ex. https://laloiavecmoi.be).
const BASE = "https://laloiavecmoi.be";

// Pages SEO par domaine, générées depuis la base vérifiée (data/belgium).
function domainesIds(): string[] {
  try {
    const dir = path.join(process.cwd(), "data", "belgium");
    return fs
      .readdirSync(dir)
      .filter((f) => f.endsWith(".json") && !f.startsWith("_"))
      .map((f) => {
        try {
          const d = JSON.parse(fs.readFileSync(path.join(dir, f), "utf-8"));
          return Array.isArray(d.faits) && d.faits.length ? (d.module as string) : null;
        } catch {
          return null;
        }
      })
      .filter((m): m is string => !!m);
  } catch {
    return [];
  }
}

const routes = [
  "",
  "/contact",
  "/loi-avec-moi/bienvenue",
  // Belgique FR
  "/loi-avec-moi",
  "/loi-avec-moi/logement",
  "/loi-avec-moi/travail",
  "/loi-avec-moi/consommation",
  "/loi-avec-moi/famille",
  "/loi-avec-moi/demarches",
  "/loi-avec-moi/trouver-un-avocat",
  "/loi-avec-moi/documents",
  "/loi-avec-moi/modeles",
  "/loi-avec-moi/quiz",
  "/loi-avec-moi/nos-assistants",
  "/loi-avec-moi/en-danger",
  "/loi-avec-moi/jeunes",
  "/loi-avec-moi/urgences",
  "/loi-avec-moi/contacts",
  "/base-juridique",
  "/transparence",
  // Belgique NL
  "/de-wet-met-mij",
  "/de-wet-met-mij/wonen",
  "/de-wet-met-mij/werk",
  "/de-wet-met-mij/juridische-hulp",
  "/de-wet-met-mij/consumentenrecht",
  "/de-wet-met-mij/familie",
  "/de-wet-met-mij/administratie",
  // France
  "/la-loi-avec-moi-france",
  "/la-loi-avec-moi-france/bienvenue",
  "/la-loi-avec-moi-france/logement",
  "/la-loi-avec-moi-france/travail",
  "/la-loi-avec-moi-france/consommation",
  "/la-loi-avec-moi-france/famille",
  "/la-loi-avec-moi-france/demarches",
  "/la-loi-avec-moi-france/trouver-un-avocat",
  "/la-loi-avec-moi-france/quiz",
  "/la-loi-avec-moi-france/nos-assistants",
  "/la-loi-avec-moi-france/en-danger",
];

export default function sitemap(): MetadataRoute.Sitemap {
  const statiques = routes.map((r) => ({
    url: `${BASE}${r}`,
    changeFrequency: "monthly" as const,
    priority: r === "" ? 1 : 0.7,
  }));
  const domaines = domainesIds().map((m) => ({
    url: `${BASE}/loi/${m}`,
    changeFrequency: "monthly" as const,
    priority: 0.6,
  }));
  return [...statiques, ...domaines];
}
