import type { MetadataRoute } from "next";

// À adapter avec ton domaine définitif (ex. https://laloiavecmoi.be).
const BASE = "https://laloiavecmoi.be";

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
  return routes.map((r) => ({
    url: `${BASE}${r}`,
    changeFrequency: "monthly",
    priority: r === "" ? 1 : 0.7,
  }));
}
