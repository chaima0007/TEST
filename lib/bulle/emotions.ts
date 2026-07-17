// Cartes émotions — alphabétisation émotionnelle adaptée à l’âge.
// Principe fondateur (RULER / Yale ; Gottman) : AUCUNE émotion n’est « mauvaise ».
// Chaque émotion est un signal utile. On aide l’enfant à la NOMMER, la repérer
// dans son corps, puis à choisir un petit geste qui aide.
//
// Données de DÉMO fictives : aucune donnée réelle d’enfant n’est collectée.

export type AgeBand = "3-5" | "6-8" | "9-11";

export type Emotion = {
  id: string;
  /** Nom simple, à hauteur d’enfant. */
  name: string;
  emoji: string;
  /** Couleur douce de la carte (contrastes vérifiés pour le texte foncé). */
  color: string;
  /** Une phrase qui dit « c’est ok de ressentir ça ». */
  reassurance: string;
  /** Où ça se sent dans le corps (repérage corporel). */
  body: string[];
  /** Exemples de situations « ça arrive quand… ». */
  when: string[];
  /** Petits gestes qui aident, formulés pour l’enfant. */
  help: string[];
  bands: AgeBand[];
};

export const EMOTIONS: Emotion[] = [
  {
    id: "joie",
    name: "Joie",
    emoji: "😄",
    color: "#FFE59A",
    reassurance: "La joie, ça fait du bien à partager.",
    body: ["Le cœur qui saute", "Un grand sourire", "L’envie de bouger"],
    when: ["Je joue avec quelqu’un que j’aime", "J’ai réussi quelque chose", "On me fait un câlin"],
    help: ["Dire à qui je pense", "Partager mon sourire", "Garder ce beau moment dans ma tête"],
    bands: ["3-5", "6-8", "9-11"],
  },
  {
    id: "tristesse",
    name: "Tristesse",
    emoji: "😢",
    color: "#B9D4F1",
    reassurance: "Être triste, c’est normal. Ça passe, surtout si on en parle.",
    body: ["Les yeux qui piquent", "Une boule dans la gorge", "Envie de se cacher"],
    when: ["Un ami est parti", "J’ai perdu quelque chose", "On m’a dit non"],
    help: ["Demander un câlin", "En parler à un adulte de confiance", "Dessiner ce que je ressens"],
    bands: ["3-5", "6-8", "9-11"],
  },
  {
    id: "colere",
    name: "Colère",
    emoji: "😠",
    color: "#F7B7A3",
    reassurance: "La colère dit qu’un besoin est important. On peut la dire sans casser ni taper.",
    body: ["Le visage tout chaud", "Les poings serrés", "Le cœur qui bat vite"],
    when: ["Ce n’est pas mon tour", "On a cassé mon jeu", "Je trouve que c’est injuste"],
    help: ["Souffler comme sur 3 bougies", "Dire « je suis en colère parce que… »", "Serrer un coussin très fort"],
    bands: ["3-5", "6-8", "9-11"],
  },
  {
    id: "peur",
    name: "Peur",
    emoji: "😨",
    color: "#C9C2EC",
    reassurance: "La peur veut me protéger. Je peux demander de l’aide, je ne suis pas seul·e.",
    body: ["Le ventre serré", "Les jambes qui tremblent", "Envie de se blottir"],
    when: ["Il fait tout noir", "Un bruit fort", "Quelque chose de nouveau"],
    help: ["Prendre la main d’un adulte", "Respirer tout doucement", "Dire tout haut ce qui me fait peur"],
    bands: ["3-5", "6-8", "9-11"],
  },
  {
    id: "calme",
    name: "Calme",
    emoji: "😌",
    color: "#B6E3D4",
    reassurance: "Le calme, c’est mon endroit tranquille à l’intérieur.",
    body: ["La respiration lente", "Les épaules relâchées", "Tout mou, tout doux"],
    when: ["Après un câlin", "Une histoire du soir", "Quand j’ai fini de pleurer"],
    help: ["Rester dans ce moment", "Respirer par le ventre", "Fermer les yeux un instant"],
    bands: ["3-5", "6-8", "9-11"],
  },
  {
    id: "jalousie",
    name: "Jalousie",
    emoji: "😒",
    color: "#D6E5A3",
    reassurance: "La jalousie dit que j’ai peur de perdre une place qui compte. Ça se parle.",
    body: ["Le ventre noué", "L’envie de bouder", "Une boule d’injustice"],
    when: ["On félicite quelqu’un d’autre", "Mon frère/ma sœur a quelque chose", "Je me sens mis·e de côté"],
    help: ["Dire « j’aimerais aussi… »", "Demander un moment rien qu’à moi", "Me rappeler ce que j’aime chez moi"],
    bands: ["6-8", "9-11"],
  },
  {
    id: "fierte",
    name: "Fierté",
    emoji: "🤩",
    color: "#FBD1A2",
    reassurance: "Être fier·e, c’est reconnaître mes efforts. J’ai le droit d’en être content·e.",
    body: ["La poitrine qui se gonfle", "Le menton haut", "Un sourire fort"],
    when: ["J’ai osé", "J’ai aidé quelqu’un", "J’ai appris un truc difficile"],
    help: ["Me féliciter tout bas", "Le raconter à quelqu’un", "Choisir mon prochain défi"],
    bands: ["6-8", "9-11"],
  },
  {
    id: "gene",
    name: "Gêne",
    emoji: "😳",
    color: "#F3C6D3",
    reassurance: "La gêne arrive à tout le monde. Elle passe plus vite qu’on ne croit.",
    body: ["Les joues qui chauffent", "L’envie de disparaître", "Le regard qui fuit"],
    when: ["Je me suis trompé·e devant les autres", "On m’a regardé·e", "J’ai dit un truc de travers"],
    help: ["Respirer un coup", "Me dire « ce n’est pas grave »", "En rire gentiment si je peux"],
    bands: ["6-8", "9-11"],
  },
  {
    id: "ennui",
    name: "Ennui",
    emoji: "😑",
    color: "#D9D9D9",
    reassurance: "L’ennui, c’est le début de l’imagination. Mon cerveau se repose.",
    body: ["Le corps mou", "Le temps qui traîne", "L’envie de rien"],
    when: ["Je n’ai plus d’idée", "J’attends longtemps", "Je tourne en rond"],
    help: ["Inventer un jeu", "Bouger un peu", "Choisir une seule petite chose à faire"],
    bands: ["3-5", "6-8", "9-11"],
  },
  {
    id: "excitation",
    name: "Excitation",
    emoji: "🤗",
    color: "#FFC7A8",
    reassurance: "Trop d’énergie d’un coup, c’est chouette mais ça peut déborder. On peut la calmer.",
    body: ["L’envie de sauter partout", "Parler très vite", "Le corps qui pétille"],
    when: ["C’est bientôt mon anniversaire", "On part en sortie", "J’ai hâte"],
    help: ["Sauter 5 fois puis souffler", "Compter jusqu’à 5 tout bas", "Serrer et relâcher mes mains"],
    bands: ["3-5", "6-8"],
  },
];

export function emotionsForBand(band: AgeBand): Emotion[] {
  return EMOTIONS.filter((e) => e.bands.includes(band));
}

export function getEmotion(id: string): Emotion | undefined {
  return EMOTIONS.find((e) => e.id === id);
}
