import type { Availability, LimitLevel, Severity } from "./types";

// ---------------------------------------------------------------------------
// Sources sérieuses (approches reconnues). Rien n'est inventé : les concepts
// sont attribués à leurs autrices/auteurs d'origine.
// ---------------------------------------------------------------------------
export interface Source {
  key: string;
  label: string;
  detail: string;
}

export const SOURCES: Source[] = [
  {
    key: "cnv",
    label: "Communication NonViolente (CNV) — Marshall B. Rosenberg",
    detail:
      "Modèle OSBD : Observation, Sentiment, Besoin, Demande. Center for Nonviolent Communication (cnvc.org).",
  },
  {
    key: "gottman",
    label: "Méthode Gottman — John & Julie Gottman",
    detail:
      "Démarrage en douceur, tentatives de réparation, pause quand on est « submergé », bilan hebdomadaire de couple. The Gottman Institute (gottman.com).",
  },
  {
    key: "fries",
    label: "Consentement — modèle FRIES (Planned Parenthood)",
    detail:
      "Un consentement est Libre, Réversible, Informé, Enthousiaste et Spécifique (Freely given, Reversible, Informed, Enthusiastic, Specific).",
  },
  {
    key: "cycle",
    label: "Phases du cycle menstruel — santé reproductive générale",
    detail:
      "Description générale des phases (menstruelle, folliculaire, ovulatoire, lutéale). Information de bien-être, non médicale (voir ACOG / NHS pour des sources cliniques).",
  },
  {
    key: "yesno",
    label: "Listes « Oui / Peut-être / Non »",
    detail:
      "Outil de communication pour exprimer envies et limites, largement utilisé en éducation à la relation et au consentement.",
  },
];

// ---------------------------------------------------------------------------
// Signaux « J'ai besoin de… » — vocabulaire à faible friction.
// Inspiré des « bids for connection » (Gottman) et des besoins CNV.
// ---------------------------------------------------------------------------
export interface NeedType {
  id: string;
  emoji: string;
  label: string;
  hint: string;
}

export const NEED_TYPES: NeedType[] = [
  { id: "calin", emoji: "🤗", label: "Un câlin", hint: "Du contact, sans rien avoir à expliquer." },
  { id: "parler", emoji: "💬", label: "Parler", hint: "J'ai besoin d'être écouté·e." },
  { id: "espace", emoji: "🌿", label: "De l'espace", hint: "Un moment seul·e, sans que ce soit un rejet." },
  { id: "silence", emoji: "🤫", label: "Du calme", hint: "Pas envie de parler tout de suite." },
  { id: "aide", emoji: "🫶", label: "De l'aide", hint: "Un coup de main, concret." },
  { id: "reassurance", emoji: "🌤️", label: "Être rassuré·e", hint: "J'ai besoin de me sentir en sécurité." },
  { id: "rire", emoji: "😄", label: "Rire un peu", hint: "Alléger l'ambiance ensemble." },
  { id: "proximite", emoji: "❤️", label: "De la proximité", hint: "Envie de tendresse / d'intimité." },
];

// ---------------------------------------------------------------------------
// Domaines de la « carte des limites & consentement ».
// ---------------------------------------------------------------------------
export interface ConsentArea {
  id: string;
  emoji: string;
  label: string;
  examples: string[];
}

export const CONSENT_AREAS: ConsentArea[] = [
  {
    id: "tendresse",
    emoji: "🤍",
    label: "Tendresse & contact",
    examples: ["Câlins en public", "Se tenir la main", "Bisous surprise", "Chatouilles"],
  },
  {
    id: "intimite",
    emoji: "❤️‍🔥",
    label: "Intimité",
    examples: ["Initier un moment", "En parler ouvertement", "Dire stop sans se justifier"],
  },
  {
    id: "temps",
    emoji: "⏳",
    label: "Temps & espace",
    examples: ["Soirées seul·e", "Temps avec les ami·es", "Besoin de décompresser après le travail"],
  },
  {
    id: "com",
    emoji: "🗣️",
    label: "Communication",
    examples: ["Régler un conflit à chaud", "Faire une pause dans la dispute", "Messages toute la journée"],
  },
  {
    id: "social",
    emoji: "🌍",
    label: "Vie sociale & famille",
    examples: ["Publier des photos de nous", "Voir la belle-famille", "Sorties en groupe"],
  },
  {
    id: "sujets",
    emoji: "🚧",
    label: "Sujets sensibles",
    examples: ["Argent", "Ex", "Corps & apparence", "Projets d'enfants"],
  },
];

// ---------------------------------------------------------------------------
// Libellés d'affichage.
// ---------------------------------------------------------------------------
export const AVAILABILITY_META: Record<Availability, { label: string; emoji: string; desc: string; className: string }> = {
  vert: {
    label: "Ouvert·e",
    emoji: "🟢",
    desc: "Disponible, partant·e pour se rapprocher.",
    className: "avail-vert",
  },
  orange: {
    label: "En réserve",
    emoji: "🟠",
    desc: "Là, mais énergie limitée — en douceur.",
    className: "avail-orange",
  },
  rouge: {
    label: "Besoin d'espace",
    emoji: "🔴",
    desc: "Pas un rejet : j'ai besoin de me recentrer.",
    className: "avail-rouge",
  },
};

export const LIMIT_META: Record<LimitLevel, { label: string; emoji: string; className: string }> = {
  oui: { label: "Oui", emoji: "💚", className: "limit-oui" },
  "peut-etre": { label: "Peut-être", emoji: "💛", className: "limit-peut-etre" },
  non: { label: "Non", emoji: "❤️", className: "limit-non" },
};

export const SEVERITY_META: Record<Severity, { label: string; className: string }> = {
  leger: { label: "Léger", className: "sev-leger" },
  moyen: { label: "Moyen", className: "sev-moyen" },
  fort: { label: "Important", className: "sev-fort" },
};

export const MOOD_EMOJI = ["😞", "😕", "😐", "🙂", "😄"];
export const ENERGY_LABEL = ["Vidé·e", "Bas", "Moyen", "Bon", "Plein·e"];
