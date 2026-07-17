// Sources reconnues utilisées dans l’Espace parent.
// RÈGLE : zéro conseil inventé. Chaque conseil renvoie à une source réelle,
// avec organisme, référence et année. Contenu INFORMATIF, non médical.
// Date de consultation des sources : 2026-07-17 (Europe/Brussels).

export type Source = {
  id: string;
  org: string;
  ref: string;
  year: string;
  url: string;
  /** Région/type pour situer la source (utile en Belgique francophone). */
  kind: "organisme public" | "recherche / clinique" | "ouvrage de référence";
};

export const CONSULTED_ON = "2026-07-17";

export const SOURCES: Record<string, Source> = {
  gottman: {
    id: "gottman",
    org: "The Gottman Institute",
    ref: "Emotion Coaching — 5 étapes ; John Gottman, « Raising an Emotionally Intelligent Child »",
    year: "1997",
    url: "https://www.gottman.com/blog/emotion-coaching-the-heart-of-parenting/",
    kind: "recherche / clinique",
  },
  siegel: {
    id: "siegel",
    org: "Dr Daniel Siegel & Tina Payne Bryson",
    ref: "« The Whole-Brain Child » — stratégie « Name it to tame it » (nommer pour apaiser)",
    year: "2011",
    url: "https://drdansiegel.com/book/the-whole-brain-child/",
    kind: "ouvrage de référence",
  },
  harvard: {
    id: "harvard",
    org: "Center on the Developing Child, Harvard University",
    ref: "« Serve and Return » — les échanges réciproques construisent le cerveau",
    year: "2020",
    url: "https://developingchild.harvard.edu/key-concept/serve-and-return/",
    kind: "recherche / clinique",
  },
  yapaka: {
    id: "yapaka",
    org: "Yapaka — Fédération Wallonie-Bruxelles",
    ref: "Programme de soutien à la parentalité et de prévention de la maltraitance",
    year: "2024",
    url: "https://www.yapaka.be/",
    kind: "organisme public",
  },
  one: {
    id: "one",
    org: "ONE — Office de la Naissance et de l’Enfance (Belgique)",
    ref: "Ressources « Grandir » et soutien à la parentalité",
    year: "2023",
    url: "https://www.one.be/",
    kind: "organisme public",
  },
  aap: {
    id: "aap",
    org: "American Academy of Pediatrics — HealthyChildren.org",
    ref: "Temper Tantrums / accompagner les grandes émotions",
    year: "2023",
    url: "https://www.healthychildren.org/English/family-life/family-dynamics/communication-discipline/Pages/Temper-Tantrums.aspx",
    kind: "organisme public",
  },
  unicef: {
    id: "unicef",
    org: "UNICEF Parenting",
    ref: "How to talk to children about their feelings",
    year: "2022",
    url: "https://www.unicef.org/parenting/",
    kind: "organisme public",
  },
  ruler: {
    id: "ruler",
    org: "Yale Center for Emotional Intelligence — RULER / Marc Brackett",
    ref: "« Permission to Feel » — toutes les émotions ont une raison d’être",
    year: "2019",
    url: "https://www.ycei.org/ruler",
    kind: "recherche / clinique",
  },
};

export function getSource(id: string): Source {
  const s = SOURCES[id];
  if (!s) throw new Error(`Source inconnue: ${id}`);
  return s;
}
