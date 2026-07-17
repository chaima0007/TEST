// Rituels de dialogue guidés. Chaque étape s'appuie sur une approche reconnue
// (voir `source`). Aucun contenu inventé : ce sont des cadres établis, reformulés
// simplement et en français.

export interface RitualStep {
  title: string;
  prompt: string;
  placeholder?: string; // si présent → champ de saisie guidé
  examples?: string[];
}

export interface Ritual {
  slug: string;
  emoji: string;
  title: string;
  tagline: string;
  duration: string;
  source: string; // clé dans SOURCES
  sourceLabel: string;
  intro: string;
  steps: RitualStep[];
  // Gabarit final assemblé à partir des réponses (indices des étapes à saisie).
  summaryTemplate?: (answers: string[]) => string;
}

export const RITUALS: Ritual[] = [
  {
    slug: "exprimer-une-limite",
    emoji: "🧭",
    title: "Exprimer une limite",
    tagline: "Dire ce qui ne va pas sans blesser, en 4 temps.",
    duration: "3 min",
    source: "cnv",
    sourceLabel: "CNV — Rosenberg (OSBD)",
    intro:
      "Le modèle OSBD de la Communication NonViolente : décrire les faits, nommer son ressenti, relier au besoin, puis formuler une demande claire et négociable.",
    steps: [
      {
        title: "Observation",
        prompt: "Décris la situation en faits, sans jugement ni « toujours / jamais ».",
        placeholder: "Quand hier soir tu as regardé ton téléphone pendant le dîner…",
        examples: ["« Quand… »", "Des faits observables, pas une interprétation."],
      },
      {
        title: "Sentiment",
        prompt: "Nomme ce que tu ressens, sans accuser.",
        placeholder: "…je me suis senti·e seul·e et un peu invisible.",
        examples: ["« Je me sens… »", "Un sentiment, pas « je sens que tu… »"],
      },
      {
        title: "Besoin",
        prompt: "Quel besoin est en jeu derrière ce sentiment ?",
        placeholder: "…parce que j'ai besoin de me sentir prioritaire pour toi.",
        examples: ["« parce que j'ai besoin de… »", "Attention / lien / repos / sécurité…"],
      },
      {
        title: "Demande",
        prompt: "Formule une demande concrète, réalisable et négociable.",
        placeholder: "Est-ce qu'on pourrait poser nos téléphones pendant le repas ?",
        examples: ["« Est-ce que tu serais d'accord pour… »", "Concrète et positive."],
      },
    ],
    summaryTemplate: (a) =>
      [a[0], a[1], a[2], a[3]].filter(Boolean).join(" ").trim(),
  },
  {
    slug: "demander-le-consentement",
    emoji: "🤝",
    title: "Demander / accorder un consentement",
    tagline: "Un oui clair, libre et enthousiaste — ou un non respecté.",
    duration: "2 min",
    source: "fries",
    sourceLabel: "Consentement — FRIES",
    intro:
      "Le consentement se vérifie, il ne se suppose pas. Modèle FRIES : Libre, Réversible, Informé, Enthousiaste, Spécifique. Un « peut-être » ou un silence ne sont pas des oui.",
    steps: [
      {
        title: "Demander (spécifique)",
        prompt: "Formule une demande précise, sur une chose à la fois.",
        placeholder: "Est-ce que tu aurais envie qu'on se fasse un câlin, là ?",
      },
      {
        title: "Laisser le choix (libre & réversible)",
        prompt: "Rappelle que « non » et « plus tard » sont des réponses complètes, et qu'on peut changer d'avis à tout moment.",
        placeholder: "Tu peux dire non, ou pas maintenant — sans avoir à te justifier.",
      },
      {
        title: "Vérifier l'enthousiasme",
        prompt: "Cherche un oui enthousiaste, pas une résignation. Dans le doute, on s'arrête.",
        placeholder: "Tu en as vraiment envie, ou c'est pour me faire plaisir ?",
      },
      {
        title: "Accueillir la réponse",
        prompt: "Quel que soit le oui ou le non : remercie de la sincérité. C'est ça qui construit la sécurité.",
        placeholder: "Merci de me l'avoir dit franchement.",
      },
    ],
  },
  {
    slug: "desamorcer-une-tension",
    emoji: "🕊️",
    title: "Désamorcer une tension",
    tagline: "Sortir de l'escalade avant que ça déborde.",
    duration: "5 min",
    source: "gottman",
    sourceLabel: "Méthode Gottman",
    intro:
      "Gottman : quand on est « submergé » physiologiquement (cœur qui s'emballe), on n'entend plus l'autre. La pause et le démarrage en douceur évitent les quatre attitudes destructrices (critique, mépris, défensive, mur).",
    steps: [
      {
        title: "Repérer le débordement",
        prompt: "Nomme pour toi-même les signes : tu montes, ta gorge se serre, tu veux « gagner ». C'est le moment de ralentir.",
      },
      {
        title: "Demander une pause (pas une fuite)",
        prompt: "Propose une pause avec un rendez-vous pour reprendre. Une pause n'est pas un abandon.",
        placeholder: "Je tiens à cette conversation. J'ai besoin de 20 min pour me calmer, puis on reprend ?",
      },
      {
        title: "Se recentrer",
        prompt: "Pendant la pause : respirer, marcher, boire de l'eau. On ne rumine pas les reproches.",
      },
      {
        title: "Redémarrer en douceur",
        prompt: "Reprends par un « je », sur un fait et un besoin — pas par une critique.",
        placeholder: "Je me sens tendu·e sur ce sujet, et j'ai besoin qu'on trouve une solution ensemble.",
      },
      {
        title: "Tentative de réparation",
        prompt: "Un petit geste qui dit « nous > le conflit » : un mot doux, un peu d'humour partagé, la main tendue.",
        placeholder: "On est dans la même équipe, hein ?",
      },
    ],
  },
  {
    slug: "bilan-hebdo",
    emoji: "🗓️",
    title: "Bilan de couple (hebdo)",
    tagline: "20 minutes par semaine pour rester à jour l'un de l'autre.",
    duration: "20 min",
    source: "gottman",
    sourceLabel: "Gottman — bilan de couple",
    intro:
      "Un rendez-vous régulier inspiré du « State of the Union » de Gottman : on commence par le positif, on aborde un point de friction à la fois, on finit par un besoin pour la semaine.",
    steps: [
      {
        title: "Apprécier (5 min)",
        prompt: "Chacun cite 2 choses concrètes qu'il a appréciées chez l'autre cette semaine.",
        placeholder: "Cette semaine, j'ai aimé quand tu as…",
      },
      {
        title: "Un point à améliorer (à tour de rôle)",
        prompt: "Un seul sujet chacun, en mode « je » et sans dossier accumulé.",
        placeholder: "Il y a un truc sur lequel j'aimerais qu'on avance…",
      },
      {
        title: "Écouter avant de répondre",
        prompt: "Celui qui écoute reformule ce qu'il a compris avant de donner son avis.",
        placeholder: "Si je comprends bien, tu as besoin de…",
      },
      {
        title: "Un besoin pour la semaine",
        prompt: "Chacun formule UNE demande concrète pour les 7 jours qui viennent.",
        placeholder: "Cette semaine, ça m'aiderait beaucoup si…",
      },
    ],
  },
];

export function getRitual(slug: string): Ritual | undefined {
  return RITUALS.find((r) => r.slug === slug);
}
