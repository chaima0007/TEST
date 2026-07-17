// Rituels de dialogue guidés parent-enfant.
// PRINCIPE CLÉ (angle mort du projet) : ce sont des rituels À FAIRE ENSEMBLE.
// Le téléphone se passe de main en main (tour de parole). L’app aide à PARLER,
// jamais à surveiller l’enfant.
//
// Chaque rituel s’appuie sur une source reconnue (voir sources.ts).

import type { AgeBand } from "./emotions";

export type StepWho = "ensemble" | "parent" | "enfant";

export type RitualStep = {
  who: StepWho;
  text: string;
  /** Consigne d’accessibilité / geste concret optionnel. */
  hint?: string;
};

export type Ritual = {
  id: string;
  title: string;
  subtitle: string;
  emoji: string;
  /** Couleur douce d’accent. */
  color: string;
  durationMin: number;
  bands: AgeBand[];
  when: string;
  steps: RitualStep[];
  closing: string;
  /** id d’une source dans sources.ts */
  sourceId: string;
};

export const RITUALS: Ritual[] = [
  {
    id: "meteo",
    title: "La météo des émotions",
    subtitle: "Un petit rendez-vous pour dire comment on va.",
    emoji: "⛅",
    color: "#B9D4F1",
    durationMin: 3,
    bands: ["3-5", "6-8", "9-11"],
    when: "Le matin, le soir, ou dès qu’on veut se reconnecter.",
    steps: [
      { who: "ensemble", text: "On s’installe l’un en face de l’autre, on éteint les écrans autour." },
      { who: "enfant", text: "Aujourd’hui, dans mon cœur, il fait plutôt… soleil, nuages, pluie ou orage ?", hint: "Montre avec la main ou le visage." },
      { who: "parent", text: "Je répète ce que j’ai entendu, sans corriger : « Donc aujourd’hui c’est plutôt… »" },
      { who: "parent", text: "À mon tour : moi, ma météo intérieure c’est…", hint: "L’adulte se montre aussi, ça rassure l’enfant." },
      { who: "ensemble", text: "On se remercie d’avoir partagé. Aucune météo n’est interdite." },
    ],
    closing: "Se dire sa météo, c’est déjà prendre soin l’un de l’autre.",
    sourceId: "gottman",
  },
  {
    id: "baton",
    title: "Le bâton de parole",
    subtitle: "Pour se dire les choses sans se couper la parole.",
    emoji: "🪄",
    color: "#C9C2EC",
    durationMin: 5,
    bands: ["6-8", "9-11"],
    when: "Quand il y a un désaccord et que les voix montent.",
    steps: [
      { who: "ensemble", text: "On choisit un objet « bâton de parole » (un crayon, une peluche)." },
      { who: "ensemble", text: "Règle : seul·e celui/celle qui tient l’objet parle. L’autre écoute jusqu’au bout." },
      { who: "enfant", text: "Je dis ce que j’ai ressenti avec « je » : « Je me suis senti·e… quand… »", hint: "Parler de soi, pas accuser l’autre." },
      { who: "parent", text: "Je reformule sans me défendre : « Si je comprends bien, tu as ressenti… »" },
      { who: "parent", text: "Je passe l’objet et je dis à mon tour ce que MOI j’ai ressenti." },
      { who: "ensemble", text: "On cherche UNE petite idée pour que ça aille mieux la prochaine fois." },
    ],
    closing: "On n’a pas besoin d’être d’accord pour se respecter.",
    sourceId: "yapaka",
  },
  {
    id: "reparation",
    title: "La réparation",
    subtitle: "Après une dispute, se retrouver en douceur.",
    emoji: "🩹",
    color: "#F3C6D3",
    durationMin: 5,
    bands: ["6-8", "9-11"],
    when: "Une fois que tout le monde est un peu calmé, jamais dans la crise.",
    steps: [
      { who: "ensemble", text: "On respire trois fois ensemble avant de commencer." },
      { who: "enfant", text: "Je nomme ce que j’ai ressenti pendant la dispute." },
      { who: "parent", text: "Je reconnais ma part, même petite : « J’ai… et je comprends que ça t’ait… »", hint: "L’adulte montre qu’on peut réparer sans se sentir nul." },
      { who: "ensemble", text: "Chacun propose UN petit geste de réparation (un mot doux, un dessin, un câlin)." },
      { who: "ensemble", text: "On se dit ce qu’on aime chez l’autre, pour finir sur du beau." },
    ],
    closing: "Se réparer, c’est plus important que d’avoir raison.",
    sourceId: "gottman",
  },
  {
    id: "trois-ballons",
    title: "Les 3 ballons",
    subtitle: "Respirer ensemble pour faire redescendre la pression.",
    emoji: "🎈",
    color: "#B6E3D4",
    durationMin: 2,
    bands: ["3-5", "6-8", "9-11"],
    when: "Quand l’émotion est trop forte (colère, peur, trop d’excitation).",
    steps: [
      { who: "ensemble", text: "On pose une main sur le ventre." },
      { who: "ensemble", text: "On gonfle un ballon imaginaire en inspirant par le nez… 1, 2, 3." },
      { who: "ensemble", text: "On dégonfle tout doucement par la bouche… le ballon s’envole." },
      { who: "ensemble", text: "On recommence avec un 2e puis un 3e ballon, un peu plus lentement." },
      { who: "parent", text: "Je fais les gestes en même temps : co-réguler, c’est respirer avec l’enfant." },
    ],
    closing: "Le corps se calme d’abord, les mots viennent après.",
    sourceId: "siegel",
  },
  {
    id: "rose-epine",
    title: "La rose et l’épine",
    subtitle: "Un rituel de connexion à raconter à table ou au coucher.",
    emoji: "🌹",
    color: "#FBD1A2",
    durationMin: 4,
    bands: ["3-5", "6-8", "9-11"],
    when: "Chaque soir, pour garder le lien, même les jours pressés.",
    steps: [
      { who: "enfant", text: "Ma « rose » : le meilleur moment de ma journée." },
      { who: "enfant", text: "Mon « épine » : le moment le plus difficile." },
      { who: "parent", text: "J’écoute avec attention et je partage MA rose et MON épine.", hint: "Échange réciproque (« serve and return »)." },
      { who: "ensemble", text: "On se souhaite une belle rose pour demain." },
    ],
    closing: "Quelques minutes d’attention vraie valent plus qu’une longue journée.",
    sourceId: "harvard",
  },
];

export function getRitual(id: string): Ritual | undefined {
  return RITUALS.find((r) => r.id === id);
}
