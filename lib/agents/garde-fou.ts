// ─── Garde-fou anti-survente, commun à tous les agents rédacteurs ────────────
//
// Corrige ERR-016 : le filtre `BANNED` n'était appliqué que dans les classes
// `LLM*`. Les classes `Heuristic*` n'étaient pas filtrées, alors qu'elles sont
// à la fois le repli de la classe LLM ET le seul chemin actif tant qu'aucune
// clé API n'est posée. Un contrôle dont le repli est la sortie non contrôlée ne
// protège rien.
//
// Choix du comportement en cas de violation : **lever une erreur**, pas se
// replier. L'heuristique EST déjà le repli — elle n'a nulle part où se replier.
// Entre émettre silencieusement une promesse intenable à un prospect et échouer
// bruyamment, le §14 tranche : « le verdict le plus prudent gagne par défaut ».

export class SurventeDetectee extends Error {
  readonly termes: string[];
  readonly contexte: string;

  constructor(contexte: string, termes: string[]) {
    super(
      `Survente détectée dans ${contexte} : ${termes.map((t) => `« ${t} »`).join(", ")}. ` +
        `Brouillon NON émis. Corrigez l'offre ou le gabarit — ne contournez pas ce contrôle (PROTOCOLE §13).`,
    );
    this.name = "SurventeDetectee";
    this.termes = termes;
    this.contexte = contexte;
  }
}

/**
 * Vérifie qu'aucun motif interdit n'apparaît dans les champs produits.
 * Lève `SurventeDetectee` si c'est le cas ; ne renvoie rien sinon.
 *
 * À appeler au **point de sortie** de chaque rédacteur — les deux chemins,
 * heuristique compris — et jamais seulement là où l'on se méfie du modèle.
 */
export function verifierSansSurvente(
  champs: ReadonlyArray<string | undefined>,
  motifs: ReadonlyArray<RegExp>,
  contexte: string,
): void {
  const texte = champs.filter((c): c is string => Boolean(c)).join("\n");
  const termes = motifs
    .map((re) => texte.match(re)?.[0])
    .filter((t): t is string => Boolean(t));
  if (termes.length > 0) throw new SurventeDetectee(contexte, termes);
}
