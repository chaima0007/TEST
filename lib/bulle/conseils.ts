// Espace parent — conseils SOURCÉS.
// RÈGLE ABSOLUE : jamais de conseil inventé. Chaque fiche = un principe reconnu
// + un organisme/ouvrage réel + une année (voir sources.ts).
// Ton : jamais moralisateur. Contenu informatif, ne remplace pas un professionnel.

export type ConseilCategory = "émotions" | "conflit" | "quotidien" | "crise";

export type Conseil = {
  id: string;
  category: ConseilCategory;
  title: string;
  /** Le principe, formulé simplement, sans culpabiliser. */
  body: string;
  /** Une action concrète à essayer. */
  tryThis: string;
  sourceId: string;
};

export const CONSEILS: Conseil[] = [
  {
    id: "nommer",
    category: "émotions",
    title: "Nommer l’émotion aide à l’apaiser",
    body:
      "Mettre des mots sur ce que l’enfant ressent (« tu as l’air en colère ») active les zones du cerveau qui régulent l’émotion et fait baisser l’intensité. On accueille l’émotion avant de parler du comportement.",
    tryThis: "Décrivez ce que vous observez sans juger : « Je vois que c’est difficile là. Tu ressens quoi ? »",
    sourceId: "siegel",
  },
  {
    id: "coaching",
    category: "émotions",
    title: "Accompagner plutôt que minimiser",
    body:
      "Les enfants dont les parents accueillent les émotions (les 5 étapes de l’« emotion coaching » : repérer, y voir une occasion de lien, écouter, nommer, poser un cadre) régulent mieux leurs émotions et ont de meilleures relations.",
    tryThis: "Évitez « ce n’est rien ». Préférez : « Je comprends que tu sois déçu, on va trouver ensemble. »",
    sourceId: "gottman",
  },
  {
    id: "toutes-emotions",
    category: "émotions",
    title: "Toutes les émotions sont permises, pas tous les comportements",
    body:
      "Aucune émotion n’est « mauvaise » : chacune est une information. Ce qu’on encadre, c’est le comportement (« tu as le droit d’être en colère, tu n’as pas le droit de taper »).",
    tryThis: "Séparez les deux à voix haute : « D’accord pour la colère. Pas d’accord pour taper. On souffle un coup ? »",
    sourceId: "ruler",
  },
  {
    id: "coreguler",
    category: "crise",
    title: "Se calmer d’abord, raisonner ensuite",
    body:
      "En pleine crise, le cerveau « logique » de l’enfant est hors ligne. Votre calme se transmet : c’est la co-régulation. On rassure et on respire AVEC l’enfant avant toute explication.",
    tryThis: "Baissez la voix, mettez-vous à sa hauteur, respirez lentement. Les mots et les leçons viendront après.",
    sourceId: "aap",
  },
  {
    id: "serve-return",
    category: "quotidien",
    title: "Les petits échanges construisent le lien (et le cerveau)",
    body:
      "Répondre aux sollicitations de l’enfant (un regard, une question, un dessin montré) par une attention réciproque — le « serve and return » — renforce les circuits de la sécurité affective et du langage.",
    tryThis: "Plusieurs fois par jour, arrêtez-vous 30 secondes pour répondre vraiment à ce qu’il/elle vous montre.",
    sourceId: "harvard",
  },
  {
    id: "desaccord",
    category: "conflit",
    title: "Le désaccord n’est pas dangereux, le mépris l’est",
    body:
      "Un désaccord exprimé avec respect apprend à l’enfant que des points de vue différents peuvent coexister. Ce qui abîme, c’est le mépris, la disqualification ou les rapports de force.",
    tryThis: "Dans une dispute, visez « on n’est pas d’accord ET on se respecte » plutôt que « qui a raison ».",
    sourceId: "yapaka",
  },
  {
    id: "parler-sentiments",
    category: "quotidien",
    title: "Parler des sentiments, tôt et souvent",
    body:
      "Nommer les émotions au quotidien — les siennes comme celles de l’enfant — enrichit son vocabulaire émotionnel et l’aide à demander de l’aide plutôt qu’à exploser ou se replier.",
    tryThis: "Commentez les émotions dans les histoires et les dessins animés : « Comment il se sent, là, à ton avis ? »",
    sourceId: "unicef",
  },
  {
    id: "rituels",
    category: "quotidien",
    title: "Des rituels simples valent mieux que de longs discours",
    body:
      "Des repères répétés et prévisibles (le rituel du soir, la météo des émotions) sécurisent l’enfant et créent des moments réguliers pour parler, sans attendre que « ça déborde ».",
    tryThis: "Choisissez UN petit rituel quotidien tenable même les jours pressés, et gardez-le.",
    sourceId: "one",
  },
];

export function conseilsByCategory(cat: ConseilCategory): Conseil[] {
  return CONSEILS.filter((c) => c.category === cat);
}

export const CATEGORIES: { key: ConseilCategory; label: string; emoji: string }[] = [
  { key: "émotions", label: "Émotions", emoji: "💛" },
  { key: "conflit", label: "Conflits", emoji: "🤝" },
  { key: "quotidien", label: "Au quotidien", emoji: "🌿" },
  { key: "crise", label: "Moments de crise", emoji: "🌊" },
];
